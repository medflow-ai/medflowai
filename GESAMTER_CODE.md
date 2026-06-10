# MedFlowAI – gesamter Code in einer Datei

> Diese Datei ist nur zum **Lesen / als Überblick / Backup**. Die App läuft weiterhin
> aus den einzelnen Dateien – das hier ist eine zusammengefügte Kopie, **nicht**
> die ausführbare Version. Maßgeblich bleibt die normale Ordnerstruktur.

Reihenfolge: Einstieg → lib/ (Logik) → views/ (Seiten) → Konfiguration.

---

## app.py

```python
"""MedFlowAI – Einstiegspunkt.

Multipage-App über st.navigation: gruppierte Sidebar-Navigation, einheitliches
Navy-Branding, Logo und Vertrauens-Badges. Die eigentlichen Seiten liegen in views/.

Start lokal:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

from lib import config as C
from lib.branding import apply_branding, render_logo, render_sidebar_extras

st.set_page_config(
    page_title=f"{C.APP_NAME} · {C.APP_TAGLINE}",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Globales Theme + Logo (über der Navigation).
apply_branding()
render_logo()

# Gruppierte Navigation.
nav = st.navigation(
    {
        "Arbeitsbereich": [
            st.Page("views/dokumentation.py", title="Dokumentation", icon="📝", default=True),
            st.Page("views/verlauf.py", title="Verlauf", icon="🗂️"),
        ],
        "Information": [
            st.Page("views/datenschutz.py", title="Datenschutz & Sicherheit", icon="🔒"),
            st.Page("views/ueber.py", title=f"Über {C.APP_NAME}", icon="ℹ️"),
        ],
    }
)

# Vertrauens-Badges + Version unterhalb der Navigation.
render_sidebar_extras()

nav.run()
```

---

## lib/config.py

```python
"""Zentrale Konfiguration: Markendaten, Farbpalette, Dokumentationstypen, Beispiele."""
from __future__ import annotations

from dataclasses import dataclass, field

# Markendaten
APP_NAME = "MedFlowAI"
APP_TAGLINE = "KI-gestützte medizinische Dokumentation"
APP_VERSION = "0.2.0"
SUPPORT_EMAIL = "support@medflowai.example"
COMPANY = "MedFlowAI"

# Farbpalette – "Tiefes Navy + Akzent"
NAVY_900 = "#0B1F3A"
NAVY_800 = "#0F2A4D"
NAVY_700 = "#13355F"
ACCENT = "#14B8A6"
ACCENT_400 = "#2DD4BF"
ACCENT_SOFT = "#CCFBF1"
INK = "#0F172A"
MUTED = "#64748B"
LINE = "#E2E8F0"
SURFACE = "#F8FAFC"
SUCCESS = "#15803D"
WARNING = "#B45309"
DANGER = "#B91C1C"


@dataclass(frozen=True)
class DocType:
    key: str
    label: str
    icon: str
    short: str
    description: str


DOC_TYPES: list[DocType] = [
    DocType("verlauf", "Verlaufsdokumentation", "📋",
            "Knappe Verlaufsnotiz für die Patientenakte",
            "Kompakte, chronologische Verlaufsnotiz für die Akte."),
    DocType("soap", "SOAP-Notiz", "🧾",
            "Strukturiert nach Subjective / Objective / Assessment / Plan",
            "Klassische SOAP-Struktur."),
    DocType("summary", "Patientenzusammenfassung", "💬",
            "Verständliche Zusammenfassung in einfacher Sprache",
            "Laienverständliche Zusammenfassung für den Patienten."),
    DocType("referral", "Überweisungs-/Briefentwurf", "✉️",
            "Entwurf für Arztbrief oder Überweisung",
            "Strukturierter Entwurf für Arztbrief/Überweisung. Reiner Entwurf."),
    DocType("todo", "To-do / weitere Abklärung", "✅",
            "Offene Punkte und nächste Schritte als Liste",
            "Liste offener Punkte und nächster Schritte zur Abklärung."),
]

DOC_TYPE_BY_KEY = {d.key: d for d in DOC_TYPES}
DOC_TYPE_LABELS = [f"{d.icon}  {d.label}" for d in DOC_TYPES]


def doc_type_from_label(label: str) -> DocType:
    for d in DOC_TYPES:
        if f"{d.icon}  {d.label}" == label:
            return d
    return DOC_TYPES[0]


@dataclass(frozen=True)
class Example:
    title: str
    text: str


EXAMPLES: list[Example] = [
    Example("Atemwegsinfekt",
            "Patient berichtet über seit 3 Tagen bestehenden Husten, Fieber bis "
            "38,5 °C und allgemeine Schwäche. Keine Atemnot. Lunge auskultatorisch "
            "frei. Vorerkrankung: arterielle Hypertonie. Dauermedikation Ramipril 5 mg."),
    Example("Rückenschmerz",
            "Akut aufgetretener Schmerz im unteren Rücken seit gestern nach Heben "
            "einer Kiste. Ausstrahlung ins rechte Bein, kein Taubheitsgefühl, keine "
            "Blasen-/Mastdarmstörung. Lasègue rechts grenzwertig positiv."),
    Example("Diabetes-Kontrolle",
            "Routinekontrolle bei bekanntem Typ-2-Diabetes. HbA1c heute 7,8 %. "
            "Patient klagt über gelegentliches Kribbeln in den Füßen abends. "
            "Aktuelle Medikation Metformin 1000 mg 2x täglich. Gewicht stabil."),
]

DEFAULT_MODEL = "gpt-4o-mini"
```

> Hinweis: In der echten `lib/config.py` stehen bei den Dok-Typen und Beispielen
> die ausführlichen Beschreibungstexte. Oben ist es zur besseren Lesbarkeit leicht
> gekürzt – die laufende App nutzt die vollständige Datei im Ordner.

---

## lib/prompts.py

```python
"""Prompt-Bausteine pro Dokumentationstyp."""
from __future__ import annotations

from lib.config import DocType

SYSTEM_PROMPT = (
    "Du bist ein sorgfältiger medizinischer Dokumentationsassistent für Arztpraxen "
    "im deutschsprachigen Raum. Deine einzige Aufgabe ist es, die vom Arzt "
    "eingegebenen Notizen zu strukturieren und sprachlich zu formulieren.\n\n"
    "Strikte Regeln:\n"
    "- Du stellst KEINE Diagnosen und triffst KEINE medizinischen Entscheidungen.\n"
    "- Du gibst keine eigenständigen Therapieanweisungen; du gibst nur das wieder, "
    "was der Arzt notiert hat.\n"
    "- Verwende ausschließlich Informationen aus den Notizen. Erfinde nichts.\n"
    "- Was fehlt oder unklar ist, nennst du knapp unter 'Offene Punkte'.\n"
    "- Schreibe in deutscher medizinischer Fachsprache, präzise und verständlich.\n"
    "- Kompakt statt ausschweifend. Keine Floskeln, keine Meta-Kommentare."
)

_TEMPLATES: dict[str, str] = {
    "verlauf": (
        "Erstelle eine kompakte Verlaufsdokumentation für die Patientenakte.\n"
        "Struktur:\n1. Anlass / Beschwerden\n2. Relevante Angaben & Befunde\n"
        "3. Einschätzung / mögliche Abklärung (nur als Notiz)\n4. Weiteres Vorgehen\n"
        "5. Offene Punkte"
    ),
    "soap": (
        "Erstelle eine strukturierte SOAP-Notiz.\nStruktur:\n"
        "**S – Subjektiv:** Angaben des Patienten\n**O – Objektiv:** Befunde\n"
        "**A – Assessment:** Einschätzung (offen, keine endgültige Diagnose)\n"
        "**P – Plan:** geplantes Vorgehen\nErgänze 'Offene Punkte', falls Angaben fehlen."
    ),
    "summary": (
        "Erstelle eine kurze, verständliche Zusammenfassung für den Patienten "
        "in einfacher Sprache.\nStruktur:\n1. Grund des Besuchs?\n2. Was wurde "
        "besprochen/festgestellt?\n3. Nächste Schritte für Sie?\n4. Wann wieder melden?"
    ),
    "referral": (
        "Erstelle den ENTWURF eines Arztbriefs bzw. einer Überweisung.\nStruktur:\n"
        "1. Anrede / Fragestellung\n2. Anamnese\n3. Aktuelle Befunde\n"
        "4. Bisheriges Vorgehen / Medikation\n5. Konkrete Fragestellung\n6. Offene Punkte\n"
        "Nutze Platzhalter wie [Empfänger], [Datum], wenn Angaben fehlen."
    ),
    "todo": (
        "Leite eine knappe To-do-/Abklärungsliste fürs Praxisteam ab.\nFormat:\n"
        "- Checkliste mit kurzen, konkreten Punkten\n- 'Weitere Abklärung' (Vorschläge)\n"
        "- 'Offene Punkte' für Fehlendes"
    ),
}


def build_messages(doc_type: DocType, notes: str) -> list[dict]:
    task = _TEMPLATES.get(doc_type.key, _TEMPLATES["verlauf"])
    user_prompt = (
        f"AUFGABE: {task}\n\n"
        f"ARZT-NOTIZEN (einzige Informationsquelle):\n\"\"\"\n{notes.strip()}\n\"\"\"\n\n"
        "Halte dich exakt an die Struktur. Antworte direkt mit der Dokumentation."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
```

---

## lib/llm.py

```python
"""OpenAI-Anbindung mit sauberer Fehlerbehandlung."""
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


def _read_api_key() -> str | None:
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY")


@st.cache_resource(show_spinner=False)
def _get_client():
    api_key = _read_api_key()
    if not api_key:
        raise ConfigError(
            "Kein OpenAI-API-Key gefunden. Bitte unter 'Settings → Secrets' den "
            "Eintrag OPENAI_API_KEY hinterlegen."
        )
    try:
        from openai import OpenAI
    except Exception as exc:
        raise ConfigError("Das openai-Paket ist nicht installiert.") from exc
    return OpenAI(api_key=api_key)


def api_key_available() -> bool:
    return bool(_read_api_key())


def generate_documentation(notes, doc_type, *, model=DEFAULT_MODEL,
                           temperature=0.2, max_tokens=900) -> GenerationResult:
    import time
    client = _get_client()
    messages = build_messages(doc_type, notes)
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=max_tokens,
        )
    except Exception as exc:
        raise LLMError(_friendly_error(exc)) from exc
    elapsed = time.perf_counter() - start
    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise LLMError("Die KI hat keine Ausgabe zurückgegeben. Bitte erneut versuchen.")
    return GenerationResult(text=text, model=model, elapsed_s=elapsed)


def _friendly_error(exc: Exception) -> str:
    name = exc.__class__.__name__.lower()
    msg = str(exc).lower()
    if "authentication" in name or "401" in msg or "invalid api key" in msg:
        return "Der OpenAI-API-Key wurde nicht akzeptiert. Bitte den Key prüfen."
    if "ratelimit" in name or "rate limit" in msg or "429" in msg:
        return "Zu viele Anfragen (Rate-Limit). Bitte kurz warten und erneut versuchen."
    if "insufficient_quota" in msg or "quota" in msg or "billing" in msg:
        return "Das OpenAI-Kontingent ist erschöpft. Bitte das Guthaben prüfen."
    if "timeout" in name or "timed out" in msg or "connection" in name:
        return "Verbindung zum KI-Dienst zu langsam/unterbrochen. Bitte erneut versuchen."
    return "Technischer Fehler bei der Erstellung. Bitte erneut versuchen."
```

---

## lib/audit.py

```python
"""Pseudonymisiertes, opt-in Audit-Log – NUR Metadaten, niemals Patiententext."""
from __future__ import annotations

import hashlib, json, os, secrets, uuid
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from lib.config import APP_VERSION

AUDIT_FILE = Path(__file__).resolve().parent.parent / "audit_log.jsonl"
_OPT_IN_KEY = "audit_opt_in"


def is_enabled() -> bool:
    return bool(st.session_state.get(_OPT_IN_KEY, False))


def set_enabled(value: bool) -> None:
    st.session_state[_OPT_IN_KEY] = bool(value)


def _salt() -> str:
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
    return hashlib.sha256((_salt() + text).encode("utf-8")).hexdigest()[:16]


def _wc(text: str) -> int:
    return len(text.split())


def record_event(*, doc_type_key, notes, output_text, model, elapsed_s) -> None:
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
        # bewusst NICHT enthalten: notes, output_text, Patientendaten
    }
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
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
        try:
            open(AUDIT_FILE, "w", encoding="utf-8").close()
            return True
        except Exception:
            return False
```

---

## lib/branding.py

```python
"""Branding & UI-Schicht: CSS-Theme, Seitenkopf, Sidebar-Extras, kleine Bausteine."""
from __future__ import annotations

from pathlib import Path
import streamlit as st
from lib import config as C

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# Das vollständige CSS (Navy-Theme, Karten, Hero, Badges, Hinweis-Boxen,
# responsive Regeln) steht in der echten lib/branding.py im Ordner.
# Es wird über apply_branding() per st.markdown(..., unsafe_allow_html=True) injiziert.


def apply_branding() -> None:
    """Injiziert das globale CSS. Einmal pro Seitenaufruf aufrufen."""
    st.markdown(_CSS, unsafe_allow_html=True)


def render_logo() -> None:
    """Markenlogo oben in der Sidebar (über der Navigation)."""
    logo = ASSETS / "logo.svg"
    icon = ASSETS / "icon.svg"
    try:
        st.logo(str(logo), icon_image=str(icon))
    except Exception:
        st.sidebar.markdown(f"### {C.APP_NAME}")


def render_sidebar_extras() -> None:
    """Vertrauens-Badges, Version und Support unterhalb der Navigation."""
    # Rendert DSGVO-/Prüf-/Medizinprodukt-Badges + Version + Support-Link.
    ...


def page_header(title, subtitle="", eyebrow="", badges=None) -> None:
    """Einheitlicher Seitenkopf (Navy-Hero-Band)."""
    ...


def note(text: str, kind: str = "") -> None:
    """Hinweis-Box. kind: '' | 'amber' | 'teal' | 'red'."""
    cls = f"mf-note {kind}".strip()
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)
```

> Hinweis: `branding.py` enthält einen großen CSS-Block. Hier ist nur das Gerüst
> gezeigt; den vollständigen CSS-Text findest du in der Datei `lib/branding.py`.

---

## lib/components.py

```python
"""Wiederverwendbare UI-Bausteine: Ergebnis-Karte, Kopieren/Download, Feedback, Verlauf."""
from __future__ import annotations

import uuid
from datetime import datetime
import streamlit as st
from lib.config import DocType, EXAMPLES

NOTES_KEY = "notes_input"
HISTORY_KEY = "history"


def add_to_history(*, doc_type, text, model, elapsed_s,
                   input_preview, input_words, output_words) -> None:
    item = {
        "id": uuid.uuid4().hex,
        "ts": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "doc_label": doc_type.label, "doc_icon": doc_type.icon,
        "text": text, "model": model, "elapsed_s": elapsed_s,
        "input_preview": input_preview,
        "input_words": input_words, "output_words": output_words,
    }
    st.session_state.setdefault(HISTORY_KEY, []).insert(0, item)


def get_history() -> list[dict]:
    return st.session_state.get(HISTORY_KEY, [])


def clear_history() -> None:
    st.session_state[HISTORY_KEY] = []


def _set_example(text: str) -> None:
    st.session_state[NOTES_KEY] = text


def example_buttons() -> None:
    st.caption("Beispiel laden:")
    cols = st.columns(len(EXAMPLES))
    for col, ex in zip(cols, EXAMPLES):
        with col:
            st.button(f"＋ {ex.title}", key=f"ex_{ex.title}",
                      on_click=_set_example, args=(ex.text,),
                      use_container_width=True)


def _filename(doc_type: DocType, ext: str) -> str:
    return f"medflowai_{doc_type.key}_{datetime.now():%Y%m%d_%H%M}.{ext}"


def render_result_card(*, text, doc_type, model, elapsed_s,
                       key_prefix="res", show_feedback=True) -> None:
    words = len(text.split())
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")
    with st.container(border=True):
        st.markdown(
            f'<div class="mf-result-head">'
            f'<span class="mf-tag">{doc_type.icon} {doc_type.label}</span>'
            f'<span class="mf-meta">{ts} · {words} Wörter · {model} · {elapsed_s:.1f}s</span>'
            f'</div>', unsafe_allow_html=True)
        st.markdown(text)
        st.divider()
        c1, c2, c3 = st.columns([1.1, 1, 1])
        with c1:
            with st.popover("📋 Kopieren", use_container_width=True):
                st.caption("Mit dem Symbol oben rechts im Block kopieren:")
                st.code(text, language="markdown")
        with c2:
            st.download_button("⬇️ Markdown", data=text,
                               file_name=_filename(doc_type, "md"),
                               mime="text/markdown", use_container_width=True,
                               key=f"{key_prefix}_dl_md")
        with c3:
            st.download_button("⬇️ Text", data=text,
                               file_name=_filename(doc_type, "txt"),
                               mime="text/plain", use_container_width=True,
                               key=f"{key_prefix}_dl_txt")
        st.markdown(
            '<div class="mf-note amber" style="margin-top:10px;">'
            "⚠️ <strong>Vorschlag zur Dokumentation.</strong> Vor Übernahme in die "
            "Akte ärztlich prüfen.</div>", unsafe_allow_html=True)
        if show_feedback:
            _feedback_row(key_prefix)


def _feedback_row(key_prefix: str) -> None:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    fc1, fc2 = st.columns([1, 3])
    with fc1:
        st.caption("War das hilfreich?")
        try:
            rating = st.feedback("thumbs", key=f"{key_prefix}_fb")
        except Exception:
            rating = None
    if rating is not None:
        with fc2:
            st.caption("Danke! Dein Feedback hilft, MedFlowAI zu verbessern.")
```

---

## views/dokumentation.py

```python
"""Hauptseite: Notizen → strukturierte Dokumentation."""
from __future__ import annotations

import streamlit as st
from lib import audit
from lib.branding import note, page_header
from lib.components import NOTES_KEY, add_to_history, example_buttons, render_result_card
from lib.config import DEFAULT_MODEL, DOC_TYPE_BY_KEY, DOC_TYPES
from lib.llm import ConfigError, LLMError, api_key_available, generate_documentation

page_header(
    title="Dokumentation erstellen",
    subtitle="Aus knappen Notizen wird strukturierte, prüfbare Dokumentation – in Sekunden.",
    eyebrow="Arbeitsbereich",
    badges=["🔒 Keine Speicherung von Patiententext", "🩺 Ärztliche Prüfung erforderlich"],
)

note("🔐 <strong>Bitte keine direkt identifizierenden Daten eingeben</strong> "
     "(Name, Geburtsdatum, Versichertennummer, Adresse).", kind="teal")
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

key_ok = api_key_available()
if not key_ok:
    note("⚙️ <strong>Noch nicht einsatzbereit:</strong> Kein OPENAI_API_KEY "
         "konfiguriert (Settings → Secrets).", kind="amber")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

st.markdown("#### 1 · Arzt-Notizen / Gesprächsinhalt")
st.session_state.setdefault(NOTES_KEY, "")
example_buttons()
st.text_area("Notizen", key=NOTES_KEY, height=190,
             placeholder="Stichpunkte oder Fließtext zum Patientenkontakt …",
             label_visibility="collapsed")
notes = st.session_state.get(NOTES_KEY, "")
st.caption(f"{len(notes)} Zeichen · {len(notes.split())} Wörter")

st.markdown("#### 2 · Art der Dokumentation")
idx = st.radio("Dokumentationstyp", options=list(range(len(DOC_TYPES))),
               format_func=lambda i: f"{DOC_TYPES[i].icon}  {DOC_TYPES[i].label}",
               captions=[d.short for d in DOC_TYPES],
               label_visibility="collapsed", key="doc_type_idx")
doc_type = DOC_TYPES[idx]

with st.expander("Erweiterte Optionen"):
    model = st.selectbox("Modell", options=[DEFAULT_MODEL, "gpt-4o"], index=0)

b1, b2 = st.columns([3, 1])
with b1:
    run = st.button("Dokumentation erstellen", type="primary",
                    use_container_width=True,
                    disabled=(not notes.strip()) or (not key_ok))
with b2:
    if st.button("Leeren", use_container_width=True):
        st.session_state[NOTES_KEY] = ""
        st.session_state.pop("last_result", None)
        st.rerun()

if run:
    error_msg = None
    result = None
    with st.status("KI verarbeitet die Notizen …", expanded=True) as status:
        st.write("Eingaben werden geprüft …")
        try:
            result = generate_documentation(notes, doc_type, model=model)
        except (ConfigError, LLMError) as exc:
            error_msg = str(exc)
            status.update(label="Erstellung fehlgeschlagen", state="error")
        else:
            st.write(f"Struktur „{doc_type.label}“ wird angewendet …")
            status.update(label=f"Dokumentation erstellt ({result.elapsed_s:.1f}s)",
                          state="complete")
    if error_msg:
        st.error(error_msg)
    elif result is not None:
        import uuid
        st.session_state["last_result"] = {
            "id": uuid.uuid4().hex[:8], "text": result.text,
            "doc_type": doc_type.key, "model": result.model,
            "elapsed": result.elapsed_s,
        }
        audit.record_event(doc_type_key=doc_type.key, notes=notes,
                           output_text=result.text, model=result.model,
                           elapsed_s=result.elapsed_s)
        add_to_history(doc_type=doc_type, text=result.text, model=result.model,
                       elapsed_s=result.elapsed_s,
                       input_preview=(notes[:90] + "…") if len(notes) > 90 else notes,
                       input_words=len(notes.split()),
                       output_words=len(result.text.split()))
        st.toast("Dokumentation erstellt", icon="✅")

lr = st.session_state.get("last_result")
if lr:
    st.markdown("### Ergebnis")
    render_result_card(text=lr["text"], doc_type=DOC_TYPE_BY_KEY[lr["doc_type"]],
                       model=lr["model"], elapsed_s=lr["elapsed"], key_prefix=lr["id"])
```

---

## views/verlauf.py

```python
"""Verlauf der in DIESER Sitzung erstellten Dokumente (nicht persistent)."""
from __future__ import annotations

import streamlit as st
from lib.branding import note, page_header
from lib.components import clear_history, get_history

page_header(title="Verlauf",
            subtitle="Alle in dieser Sitzung erstellten Dokumentationen.",
            eyebrow="Arbeitsbereich")

history = get_history()
note("🔒 Der Verlauf wird nur in dieser Sitzung gehalten und beim Neuladen gelöscht.",
     kind="teal")

if not history:
    with st.container(border=True):
        st.markdown("<div style='text-align:center;padding:24px 8px;color:#64748B;'>"
                    "🗂️<br><br><strong>Noch kein Verlauf.</strong></div>",
                    unsafe_allow_html=True)
    st.stop()

top = st.columns([3, 1])
with top[0]:
    st.caption(f"{len(history)} Dokument(e) in dieser Sitzung")
with top[1]:
    if st.button("Verlauf leeren", use_container_width=True):
        clear_history()
        st.rerun()

for item in history:
    with st.container(border=True):
        st.markdown(
            f'<div class="mf-result-head">'
            f'<span class="mf-tag">{item["doc_icon"]} {item["doc_label"]}</span>'
            f'<span class="mf-meta">{item["ts"]} · {item["output_words"]} Wörter · {item["model"]}</span>'
            f'</div><div class="mf-meta">Eingabe: {item["input_preview"]}</div>',
            unsafe_allow_html=True)
        with st.expander("Dokumentation anzeigen"):
            st.markdown(item["text"])
            d1, d2 = st.columns(2)
            with d1:
                with st.popover("📋 Kopieren", use_container_width=True):
                    st.code(item["text"], language="markdown")
            with d2:
                st.download_button("⬇️ Markdown", data=item["text"],
                                   file_name=f"medflowai_{item['id'][:8]}.md",
                                   mime="text/markdown", use_container_width=True,
                                   key=f"hist_dl_{item['id']}")
```

---

## views/datenschutz.py

```python
"""Datenschutz & Sicherheit: Transparenz, Audit-Opt-in, Produktiv-Checkliste."""
from __future__ import annotations

import json
import streamlit as st
from lib import audit
from lib.branding import note, page_header

page_header(title="Datenschutz & Sicherheit",
            subtitle="Transparenz darüber, welche Daten wie verarbeitet werden.",
            eyebrow="Information",
            badges=["Art. 9 DSGVO", "Datensparsamkeit", "Privacy by Default"])

st.markdown("### So fließen die Daten")
c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("**1 · Eingabe**")
        st.markdown("Notizen im Browser, verschlüsselt (TLS) übertragen.")
with c2:
    with st.container(border=True):
        st.markdown("**2 · KI-Verarbeitung**")
        st.markdown("Verarbeitung über die OpenAI-API (Auftragsverarbeiter, ggf. außerhalb der EU).")
with c3:
    with st.container(border=True):
        st.markdown("**3 · Ergebnis**")
        st.markdown("Patiententext wird serverseitig nicht gespeichert.")

note("⚠️ Für echten Praxiseinsatz: AVV mit dem KI-Anbieter, möglichst EU-Region "
     "und Zero Data Retention.", kind="amber")
st.divider()

st.markdown("### Pseudonymisiertes Audit-Log")
enabled = st.toggle("Audit-Log aktivieren (nur Metadaten)", value=audit.is_enabled())
audit.set_enabled(enabled)
if enabled:
    note("✅ Audit-Log aktiv – nur Metadaten.", kind="teal")
else:
    note("⛔ Audit-Log deaktiviert.", kind="")

events = audit.read_events()
if events:
    st.caption(f"{len(events)} Einträge · enthält keinen Patiententext")
    st.dataframe([{ "Zeitpunkt": e.get("ts"), "Typ": e.get("doc_type"),
                    "Modell": e.get("model"), "Fingerprint": e.get("input_fingerprint") }
                  for e in reversed(events)], use_container_width=True, hide_index=True)
    d1, d2 = st.columns(2)
    with d1:
        jsonl = "\n".join(json.dumps(e, ensure_ascii=False) for e in events)
        st.download_button("⬇️ Audit-Log exportieren (JSONL)", data=jsonl,
                           file_name="medflowai_audit_log.jsonl",
                           mime="application/x-ndjson", use_container_width=True)
    with d2:
        if st.button("🗑️ Audit-Log löschen", use_container_width=True):
            audit.clear_log(); st.rerun()

st.divider()
st.markdown("### Checkliste für den Produktivbetrieb")
st.markdown("- AVV mit dem KI-Anbieter (EU-Region & Zero Data Retention)\n"
            "- Zugriffsschutz (Authentifizierung, Rollen)\n"
            "- Verschlüsselung ruhender Daten\n"
            "- Löschkonzept & Aufbewahrungsfristen\n"
            "- Verfahrensverzeichnis / DSFA\n- Mandantentrennung je Praxis/MVZ")
note("ℹ️ Technische Orientierung, <strong>kein Rechtsrat</strong>.", kind="")
```

---

## views/ueber.py

```python
"""Über MedFlowAI: Positionierung, Zielgruppe, Grenzen, Impressum."""
from __future__ import annotations

import streamlit as st
from lib import config as C
from lib.branding import note, page_header

page_header(title=f"Über {C.APP_NAME}", subtitle=C.APP_TAGLINE, eyebrow="Information",
            badges=[f"Version {C.APP_VERSION}", "Made for Praxen & MVZ"])

st.markdown(f"**{C.APP_NAME}** verwandelt knappe Arzt-Notizen in strukturierte, "
            "prüfbare Dokumentation.")

st.markdown("### Was die Anwendung leistet")
f1, f2, f3 = st.columns(3)
for col, (icon, title, body) in zip((f1, f2, f3), [
    ("⏱️", "Zeit sparen", "Aus Stichpunkten in Sekunden strukturierte Notizen."),
    ("🧩", "Konsistente Struktur", "Einheitliche Form über alle Dokumente."),
    ("🔍", "Prüfbar", "Nutzt nur eingegebene Angaben; Fehlendes wird ausgewiesen."),
]):
    with col:
        with st.container(border=True):
            st.markdown(f"#### {icon} {title}")
            st.markdown(body)

st.divider()
st.markdown("### Klare Abgrenzung")
note("🩺 <strong>Unterstützung, kein Ersatz.</strong> Keine Diagnosen, keine "
     "medizinischen Entscheidungen. Jede Ausgabe ist ein Vorschlag und muss "
     "ärztlich geprüft werden.", kind="teal")
note("⚖️ <strong>Kein Medizinprodukt</strong> im Sinne der MDR (EU 2017/745).",
     kind="amber")

st.divider()
left, right = st.columns(2)
with left:
    st.markdown("### Für wen")
    st.markdown("- Hausärzt:innen\n- Fachärzt:innen\n- Arztpraxen\n- MVZ")
with right:
    st.markdown("### In drei Schritten")
    st.markdown("1. Notizen eingeben\n2. Dokumentationstyp wählen\n3. Ergebnis prüfen & übernehmen")

st.divider()
st.markdown("### Impressum & Kontakt")
st.markdown(f"{C.COMPANY} · [Platzhalter Anschrift] · Verantwortlich: [Name] · "
            f"[{C.SUPPORT_EMAIL}](mailto:{C.SUPPORT_EMAIL})")
```

---

## Konfiguration

### requirements.txt
```text
streamlit>=1.40,<2
openai>=1.30
```

### .streamlit/config.toml
```toml
[theme]
primaryColor = "#14B8A6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1F5F9"
textColor = "#0F172A"
font = "sans serif"

[browser]
gatherUsageStats = false
```

### .gitignore
```text
.streamlit/secrets.toml
audit_log.jsonl
__pycache__/
*.py[cod]
.DS_Store
```

---

_Dies ist eine zusammengefügte Lesefassung. Einige sehr lange Blöcke (z. B. der
CSS-Text in `branding.py` und die ausführlichen Beschreibungstexte in `config.py`)
sind hier zur Lesbarkeit gekürzt – die laufende App nutzt immer die vollständigen
Einzeldateien im Ordner._
