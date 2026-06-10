"""OpenAI-Anbindung mit sauberer Fehlerbehandlung.

Wichtige Unterschiede zum MVP:
- Der Client wird NICHT beim Import erzeugt (kein App-Crash, wenn der Key fehlt).
- Der Key wird zwischengespeichert (@st.cache_resource) statt bei jedem Klick neu.
- Fehler werden in verständliche Meldungen übersetzt – nie als Stacktrace.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import streamlit as st

from lib.config import DEFAULT_MODEL, DocType
from lib.prompts import build_messages


class ConfigError(RuntimeError):
    """Konfigurationsproblem (z. B. fehlender API-Key)."""


class LLMError(RuntimeError):
    """Fehler bei der Generierung – mit nutzerfreundlicher Meldung."""


@dataclass
class GenerationResult:
    text: str
    model: str
    elapsed_s: float
    truncated: bool = False  # True, wenn die Ausgabe am Token-Limit abgeschnitten wurde


def _read_api_key() -> str | None:
    """Liest den Key aus st.secrets oder Umgebungsvariable – ohne zu crashen."""
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        # st.secrets kann werfen, wenn keine secrets.toml existiert.
        pass
    return os.environ.get("OPENAI_API_KEY")


@st.cache_resource(show_spinner=False)
def _get_client():
    """Erzeugt (einmalig) den OpenAI-Client. Wirft ConfigError, wenn kein Key da ist."""
    api_key = _read_api_key()
    if not api_key:
        raise ConfigError(
            "Kein OpenAI-API-Key gefunden. Bitte in der Streamlit-Cloud unter "
            "'Settings → Secrets' den Eintrag OPENAI_API_KEY hinterlegen "
            "(oder lokal als Umgebungsvariable setzen)."
        )
    try:
        from openai import OpenAI
    except Exception as exc:  # pragma: no cover
        raise ConfigError(
            "Das openai-Paket ist nicht installiert. Bitte 'pip install openai' "
            "ausführen."
        ) from exc
    # Timeout + ein Retry, damit ein hängender Request die UI nicht minutenlang blockiert.
    return OpenAI(api_key=api_key, timeout=45.0, max_retries=1)


def api_key_available() -> bool:
    """Für die UI: ist überhaupt ein Key konfiguriert?"""
    return bool(_read_api_key())


def generate_documentation(
    notes: str,
    doc_type: DocType,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 1500,
) -> GenerationResult:
    """Erzeugt die Dokumentation. Wirft ConfigError oder LLMError mit klaren Texten."""
    import time

    client = _get_client()  # kann ConfigError werfen
    messages = build_messages(doc_type, notes)

    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:  # Netzwerk / Auth / Rate-Limit / Quota …
        raise LLMError(_friendly_error(exc)) from exc

    elapsed = time.perf_counter() - start
    choice = response.choices[0]
    text = (choice.message.content or "").strip()
    if not text:
        raise LLMError(
            "Die KI hat keine Ausgabe zurückgegeben. Bitte erneut versuchen oder "
            "die Notizen etwas konkreter fassen."
        )
    # Wurde die Ausgabe am Längenlimit abgeschnitten? -> später als Warnung anzeigen.
    truncated = getattr(choice, "finish_reason", None) == "length"
    return GenerationResult(text=text, model=model, elapsed_s=elapsed, truncated=truncated)


def transcribe_audio(audio_bytes: bytes, *, language: str = "de",
                     model: str = "whisper-1") -> str:
    """Wandelt eine Audioaufnahme (WAV-Bytes) per Whisper in Text um.

    Wirft ConfigError (kein Key) oder LLMError (Transkriptionsfehler) mit
    verständlichen Meldungen.
    """
    client = _get_client()  # kann ConfigError werfen
    try:
        result = client.audio.transcriptions.create(
            model=model,
            file=("aufnahme.wav", audio_bytes),
            language=language,
        )
    except Exception as exc:
        raise LLMError(_friendly_error(exc)) from exc
    return (getattr(result, "text", "") or "").strip()


def _friendly_error(exc: Exception) -> str:
    """Übersetzt technische Ausnahmen in eine verständliche, knappe Meldung."""
    name = exc.__class__.__name__.lower()
    msg = str(exc).lower()
    if "authentication" in name or "401" in msg or "invalid api key" in msg:
        return (
            "Der OpenAI-API-Key wurde nicht akzeptiert. Bitte den Key in den "
            "Streamlit-Secrets prüfen."
        )
    # Quota ZUERST prüfen: erschöpftes Guthaben kommt als RateLimitError (429),
    # darf aber nicht als "bitte warten" fehlgemeldet werden.
    if "insufficient_quota" in msg or "quota" in msg or "billing" in msg:
        return (
            "Das OpenAI-Kontingent ist erschöpft. Bitte das Guthaben bzw. die "
            "Abrechnung im OpenAI-Konto prüfen."
        )
    if "ratelimit" in name or "rate limit" in msg or "429" in msg:
        return (
            "Aktuell sind zu viele Anfragen unterwegs (Rate-Limit). Bitte einen "
            "Moment warten und erneut versuchen."
        )
    if "timeout" in name or "timed out" in msg or "connection" in name:
        return (
            "Die Verbindung zum KI-Dienst war zu langsam oder unterbrochen. "
            "Bitte erneut versuchen."
        )
    return (
        "Bei der Erstellung ist ein technischer Fehler aufgetreten. Bitte erneut "
        "versuchen. Falls es bestehen bleibt, den Support kontaktieren."
    )
