"""Pseudonymisiertes, opt-in Audit-Log – NUR Metadaten, niemals Patiententext.

Ersetzt das ursprüngliche access_log.json, das Eingaben und Ausgaben im Klartext
gespeichert hat (Gesundheitsdaten nach Art. 9 DSGVO – nicht zulässig ohne
Rechtsgrundlage und Schutzmaßnahmen).

Gespeichert werden ausschließlich:
- Zeitstempel, zufällige Vorgangs-ID
- Dokumentationstyp, verwendetes Modell, Dauer
- Längen (Wörter/Zeichen) der Ein- und Ausgabe
- optional ein gesalzener Fingerprint (Hash) der Eingabe zur Dublettenerkennung
  – NICHT umkehrbar, enthält keinen Text

Standardmäßig ist die Protokollierung AUS (Opt-in über die Datenschutz-Seite).

Hinweis: Auf Streamlit Cloud ist das Dateisystem flüchtig. Für den Produktivbetrieb
gehört dieses Log in eine zugriffsgeschützte, verschlüsselte Datenbank.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from lib.config import APP_VERSION

AUDIT_FILE = Path(__file__).resolve().parent.parent / "audit_log.jsonl"
_OPT_IN_KEY = "audit_opt_in"


# --------------------------------------------------------------------------- #
# Opt-in-Status (in der Session)
# --------------------------------------------------------------------------- #
def is_enabled() -> bool:
    return bool(st.session_state.get(_OPT_IN_KEY, False))


def set_enabled(value: bool) -> None:
    st.session_state[_OPT_IN_KEY] = bool(value)


# --------------------------------------------------------------------------- #
# Salt für den Fingerprint
# --------------------------------------------------------------------------- #
def _salt() -> str:
    """Bevorzugt ein konfiguriertes Secret; sonst ein pro-Session zufälliger Salt.

    Ein zufälliger Session-Salt bedeutet: Fingerprints sind nicht über Sitzungen
    hinweg vergleichbar – datensparsamer, aber für Dublettenerkennung innerhalb
    einer Sitzung weiterhin nutzbar.
    """
    try:
        if "AUDIT_SALT" in st.secrets:
            return str(st.secrets["AUDIT_SALT"])
    except Exception:
        pass
    if os.environ.get("AUDIT_SALT"):
        return os.environ["AUDIT_SALT"]
    if "_audit_salt" not in st.session_state:
        st.session_state["_audit_salt"] = secrets.token_hex(16)
    return st.session_state["_audit_salt"]


def _fingerprint(text: str) -> str:
    digest = hashlib.sha256((_salt() + text).encode("utf-8")).hexdigest()
    return digest[:16]


def _wc(text: str) -> int:
    return len(text.split())


# --------------------------------------------------------------------------- #
# Schreiben / Lesen
# --------------------------------------------------------------------------- #
def record_event(
    *,
    doc_type_key: str,
    notes: str,
    output_text: str,
    model: str,
    elapsed_s: float,
) -> None:
    """Schreibt einen Metadaten-Eintrag – nur wenn Opt-in aktiv ist."""
    if not is_enabled():
        return
    entry = {
        "id": uuid.uuid4().hex,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "app_version": APP_VERSION,
        "doc_type": doc_type_key,
        "model": model,
        "elapsed_s": round(float(elapsed_s), 2),
        "input_words": _wc(notes),
        "input_chars": len(notes),
        "output_words": _wc(output_text),
        "output_chars": len(output_text),
        "input_fingerprint": _fingerprint(notes),
        # bewusst NICHT enthalten: notes, output_text, Patientendaten jeglicher Art
    }
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        # Protokollierung darf den Arbeitsfluss niemals blockieren.
        pass


def read_events(limit: int = 200) -> list[dict]:
    if not AUDIT_FILE.exists():
        return []
    rows: list[dict] = []
    try:
        with open(AUDIT_FILE, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    except Exception:
        return rows
    return rows[-limit:]


def clear_log() -> bool:
    try:
        if AUDIT_FILE.exists():
            AUDIT_FILE.unlink()
        return True
    except Exception:
        # Fallback: Datei leeren – manche Dateisysteme verbieten das Löschen,
        # erlauben aber das Überschreiben.
        try:
            open(AUDIT_FILE, "w", encoding="utf-8").close()
            return True
        except Exception:
            return False
