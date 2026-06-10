# MedFlowAI – gesamter Code (Stand v0.3.0)

> Automatisch aus den aktuellen Projektdateien zusammengestellt – nur zum Lesen.
> Die App läuft aus den Einzeldateien; maßgeblich bleibt immer die Ordnerstruktur.

**Reihenfolge:** Einstieg → lib/ (Logik) → views/ (Seiten) → Konfiguration.

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
            st.Page("views/ueber.py", title=f"Über {C.APP_NAME}", icon="ℹ️"),
            st.Page("views/datenschutz.py", title="Datenschutz & Sicherheit", icon="🔒"),
            st.Page("views/grenzen.py", title="Grenzen", icon="⚠️"),
        ],
        "Einstellungen": [
            st.Page("views/einstellungen.py", title="Einstellungen", icon="⚙️"),
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
"""Zentrale Konfiguration: Markendaten, Farbpalette, Dokumentationstypen, Beispiele.

Alles, was an mehreren Stellen gebraucht wird, lebt hier – so bleibt das UI
konsistent und Anpassungen (Branding, neue Dok-Typen) passieren an einer Stelle.
"""
from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Markendaten
# --------------------------------------------------------------------------- #
APP_NAME = "MedFlowAI"
APP_TAGLINE = "KI-gestützte medizinische Dokumentation"
APP_VERSION = "0.3.0"
SUPPORT_EMAIL = "support@medflowai.example"
COMPANY = "MedFlowAI"

# --------------------------------------------------------------------------- #
# Farbpalette – "Tiefes Navy + Akzent"
# --------------------------------------------------------------------------- #
NAVY_900 = "#0B1F3A"   # Sidebar / Kopfband
NAVY_800 = "#0F2A4D"
NAVY_700 = "#13355F"
ACCENT = "#14B8A6"     # Teal – Akzent / CTA
ACCENT_400 = "#2DD4BF"
ACCENT_SOFT = "#CCFBF1"
INK = "#0F172A"        # Haupttext (Slate-900)
MUTED = "#64748B"      # Sekundärtext (Slate-500)
LINE = "#E2E8F0"       # Trennlinien (Slate-200)
SURFACE = "#F8FAFC"    # Sehr helle Fläche (Slate-50)
SUCCESS = "#15803D"
WARNING = "#B45309"
DANGER = "#B91C1C"

# --------------------------------------------------------------------------- #
# Dokumentationstypen
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class DocType:
    key: str
    label: str
    icon: str
    short: str          # eine Zeile für die Auswahl
    description: str     # ausführlicher in der Info-Box


DOC_TYPES: list[DocType] = [
    DocType(
        key="verlauf",
        label="Verlaufsdokumentation",
        icon="📋",
        short="Knappe Verlaufsnotiz für die Patientenakte",
        description=(
            "Kompakte, chronologische Verlaufsnotiz für die Akte. "
            "Fokus auf Beschwerden, relevante Befunde und das weitere Vorgehen."
        ),
    ),
    DocType(
        key="soap",
        label="SOAP-Notiz",
        icon="🧾",
        short="Strukturiert nach Subjective / Objective / Assessment / Plan",
        description=(
            "Klassische SOAP-Struktur: Subjektiv (Angaben des Patienten), "
            "Objektiv (Befunde), Assessment (Einschätzung) und Plan."
        ),
    ),
    DocType(
        key="summary",
        label="Patientenzusammenfassung",
        icon="💬",
        short="Verständliche Zusammenfassung in einfacher Sprache",
        description=(
            "Laienverständliche Zusammenfassung für den Patienten – ohne "
            "Fachjargon, mit klaren nächsten Schritten."
        ),
    ),
    DocType(
        key="referral",
        label="Überweisungs-/Briefentwurf",
        icon="✉️",
        short="Entwurf für Arztbrief oder Überweisung",
        description=(
            "Strukturierter Entwurf für einen Arztbrief oder eine Überweisung "
            "(Anamnese, Befund, Fragestellung). Reiner Entwurf zur Prüfung."
        ),
    ),
    DocType(
        key="todo",
        label="To-do / weitere Abklärung",
        icon="✅",
        short="Offene Punkte und nächste Schritte als Liste",
        description=(
            "Liste offener Punkte und vorgeschlagener nächster Schritte zur "
            "Abklärung – als Checkliste fürs Praxisteam."
        ),
    ),
]

DOC_TYPE_BY_KEY = {d.key: d for d in DOC_TYPES}


# --------------------------------------------------------------------------- #
# Beispielanfragen (als Buttons, nicht im Eingabefeld vorbelegt)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Example:
    title: str
    text: str


EXAMPLES: list[Example] = [
    Example(
        title="Atemwegsinfekt",
        text=(
            "Patient berichtet über seit 3 Tagen bestehenden Husten, Fieber bis "
            "38,5 °C und allgemeine Schwäche. Keine Atemnot. Lunge auskultatorisch "
            "frei. Vorerkrankung: arterielle Hypertonie. Dauermedikation Ramipril 5 mg."
        ),
    ),
    Example(
        title="Rückenschmerz",
        text=(
            "Akut aufgetretener Schmerz im unteren Rücken seit gestern nach Heben "
            "einer Kiste. Ausstrahlung ins rechte Bein, kein Taubheitsgefühl, keine "
            "Blasen-/Mastdarmstörung. Lasègue rechts grenzwertig positiv."
        ),
    ),
    Example(
        title="Diabetes-Kontrolle",
        text=(
            "Routinekontrolle bei bekanntem Typ-2-Diabetes. HbA1c heute 7,8 %. "
            "Patient klagt über gelegentliches Kribbeln in den Füßen abends. "
            "Aktuelle Medikation Metformin 1000 mg 2x täglich. Gewicht stabil."
        ),
    ),
]

# Standardmodell (zentral, damit leicht austauschbar)
DEFAULT_MODEL = "gpt-4o-mini"

```

---

## lib/branding.py

```python
"""Branding & UI-Schicht: CSS-Theme, Seitenkopf, Sidebar, Step-Header, Bausteine.

Das gesamte visuelle Erscheinungsbild liegt hier. Premium-Healthcare-Look:
tiefes Navy, Türkis-Akzent, weiße Flächen, weiche Schatten, großzügiges Spacing.
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from lib import config as C

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# --------------------------------------------------------------------------- #
# Globales CSS
# --------------------------------------------------------------------------- #
_CSS = f"""
<style>
:root {{
  --navy-900:{C.NAVY_900}; --navy-800:{C.NAVY_800}; --navy-700:{C.NAVY_700};
  --accent:{C.ACCENT}; --accent-400:{C.ACCENT_400}; --accent-soft:{C.ACCENT_SOFT};
  --ink:{C.INK}; --muted:{C.MUTED}; --line:{C.LINE}; --surface:{C.SURFACE};
  --success:{C.SUCCESS}; --warning:{C.WARNING}; --danger:{C.DANGER};
  --radius:16px; --shadow-sm:0 1px 2px rgba(16,24,40,.05);
  --shadow:0 4px 14px rgba(16,24,40,.06), 0 1px 3px rgba(16,24,40,.05);
  --shadow-lg:0 18px 40px rgba(11,31,58,.14);
}}

/* ---------- Grundlayout & Typografie ---------- */
html, body, [class*="css"] {{ -webkit-font-smoothing: antialiased; }}
.block-container {{ padding-top: 2.4rem; padding-bottom: 5rem; max-width: 1000px; }}
[data-testid="stMain"] {{ color: var(--ink); }}
[data-testid="stMain"] h1,[data-testid="stMain"] h2,[data-testid="stMain"] h3 {{
  color: var(--navy-900); letter-spacing: -0.018em; font-weight: 700;
}}
[data-testid="stMain"] p, [data-testid="stMain"] li {{ color: var(--ink); line-height: 1.6; }}
[data-testid="stMain"] a {{ color: #0FA295; }}
footer {{ visibility: hidden; }}
hr {{ border-color: var(--line); }}

/* Sidebar-Toggle / Bedienelemente immer sichtbar halten */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stHeader"] {{
  visibility: visible !important; opacity: 1 !important;
}}

/* ---------- Sidebar: tiefes Navy ---------- */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, var(--navy-900) 0%, var(--navy-800) 100%);
  border-right: 1px solid rgba(255,255,255,.06);
}}
section[data-testid="stSidebar"] * {{ color: #E2E8F0; }}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{ color: #FFFFFF; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
  border-radius: 10px; margin: 2px 8px; padding: 8px 12px;
  color: #CBD5E1 !important; transition: all .15s ease; font-weight: 500;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
  background: rgba(45,212,191,.14); color: #FFFFFF !important;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
  background: rgba(20,184,166,.20); color: #FFFFFF !important;
  box-shadow: inset 3px 0 0 var(--accent-400);
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {{ color: inherit !important; }}

/* ---------- Karten ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: #FFFFFF;
  border: 1px solid var(--line) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow);
  padding: 6px 4px;
}}

/* ---------- Eingaben ---------- */
textarea, .stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {{
  border-radius: 12px !important; border-color: var(--line) !important;
  font-size: 1rem !important;
}}
textarea {{ padding: 14px !important; line-height: 1.55 !important; }}
textarea:focus, .stTextInput input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(20,184,166,.18) !important;
}}

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {{
  border-radius: 12px; font-weight: 600; padding: .5rem 1rem;
  transition: transform .12s ease, background .15s ease, border-color .15s ease, box-shadow .15s ease;
}}
.stButton > button[kind="primary"], .stDownloadButton > button {{
  background: var(--accent); border: 1px solid var(--accent); color: #fff;
  box-shadow: 0 6px 16px rgba(20,184,166,.25);
}}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {{
  background: #0FA295; border-color: #0FA295; transform: translateY(-1px);
}}
.stButton > button[kind="secondary"] {{
  border: 1px solid var(--line); color: var(--navy-800); background:#fff;
}}
.stButton > button[kind="secondary"]:hover {{
  border-color: var(--accent); color: var(--navy-900); transform: translateY(-1px);
}}

/* ---------- Hero / Seitenkopf ---------- */
.mf-hero {{
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, var(--navy-900) 0%, var(--navy-700) 100%);
  border-radius: 20px; padding: 26px 30px; margin-bottom: 22px; color: #fff;
  box-shadow: var(--shadow-lg);
}}
.mf-hero::after {{
  content:""; position:absolute; right:-60px; top:-60px; width:220px; height:220px;
  background: radial-gradient(circle, rgba(45,212,191,.22), transparent 70%);
}}
.mf-hero h1 {{ color:#fff !important; margin:0; font-size: 1.7rem; letter-spacing:-.025em; }}
.mf-hero p {{ color:#C7D2E0 !important; margin:.4rem 0 0; font-size: 1rem; max-width: 60ch; }}
.mf-hero .mf-eyebrow {{
  display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.14em;
  text-transform:uppercase; color: var(--accent-400); margin-bottom:.5rem;
}}

/* ---------- Step-Header ---------- */
.mf-step {{ display:flex; align-items:center; gap:11px; margin: 18px 0 12px; }}
.mf-step-num {{
  width:28px; height:28px; border-radius:50%; flex:0 0 auto;
  background: var(--accent); color:#fff; font-weight:700; font-size:.9rem;
  display:inline-flex; align-items:center; justify-content:center;
  box-shadow: 0 4px 10px rgba(20,184,166,.3);
}}
.mf-step-title {{ font-weight:700; color:var(--navy-900); font-size:1.08rem; letter-spacing:-.01em; }}

/* ---------- Dokumentationstyp-Karten ---------- */
.mf-doc-card {{ text-align:center; padding: 10px 6px 2px; }}
.mf-doc-icon {{ font-size: 1.8rem; line-height:1; margin-bottom:8px; }}
.mf-doc-title {{ font-weight:700; color: var(--navy-900); font-size:.96rem; }}
.mf-doc-title.sel {{ color: #0F766E; }}
.mf-doc-desc {{ color: var(--muted); font-size:.78rem; margin-top:5px; min-height: 2.6em; line-height:1.4; }}
.mf-doc-check {{ font-size:.72rem; font-weight:700; color:#0F766E; margin:7px 0 2px; }}

/* ---------- Badges ---------- */
.mf-badges {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }}
.mf-badge {{
  display:inline-flex; align-items:center; gap:6px;
  font-size:.74rem; font-weight:600; padding:4px 11px; border-radius:999px;
  background: rgba(255,255,255,.10); color:#E2E8F0; border:1px solid rgba(255,255,255,.16);
}}
.mf-tag {{
  display:inline-flex; align-items:center; gap:6px; font-size:.74rem; font-weight:600;
  padding:3px 10px; border-radius:999px; background: var(--accent-soft);
  color:#0F766E; border:1px solid #99F6E4;
}}
.mf-tag.gray {{ background:#F1F5F9; color:#475569; border-color:#E2E8F0; }}

/* ---------- Hinweis-Boxen ---------- */
.mf-note {{
  border-radius:14px; padding:13px 15px; font-size:.9rem; line-height:1.55;
  border:1px solid var(--line); background: var(--surface); color: var(--ink);
}}
.mf-note.amber {{ background:#FFFBEB; border-color:#FDE68A; color:#92400E; }}
.mf-note.teal  {{ background:#F0FDFA; border-color:#99F6E4; color:#115E59; }}
.mf-note.red   {{ background:#FEF2F2; border-color:#FECACA; color:#991B1B; }}
.mf-note strong {{ color: inherit; }}

/* ---------- Ergebnis-Karte ---------- */
.mf-result-head {{
  display:flex; align-items:center; justify-content:space-between;
  gap:10px; flex-wrap:wrap; margin-bottom:4px;
}}
.mf-meta {{ color: var(--muted); font-size:.8rem; }}

/* Sidebar-Fußzeile */
.mf-sb-foot {{ font-size:.74rem; color:#94A3B8; line-height:1.5; }}

/* ---------- Responsive ---------- */
@media (max-width: 640px) {{
  .block-container {{ padding-top: 1.4rem; padding-left: .8rem; padding-right: .8rem; }}
  .mf-hero {{ padding:20px; border-radius:16px; }}
  .mf-hero h1 {{ font-size:1.35rem; }}
  .mf-hero p {{ font-size:.94rem; }}
  .mf-doc-desc {{ min-height: 0; }}
}}
</style>
"""


# --------------------------------------------------------------------------- #
# Darstellungsmodi (über die Einstellungen-Seite umschaltbar)
# --------------------------------------------------------------------------- #
_DARK_CSS = """
.stApp, [data-testid="stMain"], [data-testid="stHeader"] { background-color:#0B1220 !important; }
[data-testid="stMain"] p, [data-testid="stMain"] li, [data-testid="stMain"] label { color:#E2E8F0 !important; }
[data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3 { color:#F8FAFC !important; }
[data-testid="stVerticalBlockBorderWrapper"] { background:#16233B !important; border-color:#334155 !important; box-shadow:none !important; }
[data-testid="stMain"] textarea,
[data-testid="stMain"] .stTextInput input,
[data-testid="stMain"] .stSelectbox div[data-baseweb="select"] > div {
  background:#0F1B30 !important; color:#E2E8F0 !important; border-color:#334155 !important; }
.mf-note:not(.amber):not(.teal):not(.red) { background:#16233B !important; border-color:#334155 !important; color:#E2E8F0 !important; }
.mf-meta { color:#94A3B8 !important; }
.mf-step-title, .mf-doc-title { color:#F8FAFC !important; }
[data-testid="stMain"] .stButton > button[kind="secondary"] {
  background:#16233B !important; color:#E2E8F0 !important; border-color:#334155 !important; }
[data-testid="stMain"] [data-testid="stExpander"] summary,
[data-testid="stMain"] [data-testid="stExpander"] summary * { color:#E2E8F0 !important; }
"""

_COMPACT_CSS = """
.block-container { padding-top:1.1rem !important; padding-bottom:2.5rem !important; }
.mf-hero { padding:16px 18px !important; margin-bottom:12px !important; }
.mf-hero h1 { font-size:1.35rem !important; }
.mf-step { margin:10px 0 7px !important; }
[data-testid="stVerticalBlockBorderWrapper"] { padding:2px !important; }
.mf-note { padding:9px 12px !important; }
"""

_LARGE_CSS = """
[data-testid="stMain"] p, [data-testid="stMain"] li { font-size:1.12rem !important; line-height:1.7 !important; }
[data-testid="stMain"] textarea { font-size:1.1rem !important; }
.mf-step-title { font-size:1.22rem !important; }
.mf-doc-title { font-size:1.05rem !important; }
.mf-doc-desc { font-size:.9rem !important; }
[data-testid="stMain"] .stButton > button { font-size:1.02rem !important; }
.mf-hero h1 { font-size:1.95rem !important; }
.mf-hero p { font-size:1.1rem !important; }
"""


def _mode_css() -> str:
    # Liest aus dauerhaften pref_*-Schlüsseln (nicht an Widgets gebunden),
    # damit die Einstellung über Seitenwechsel hinweg erhalten bleibt.
    ss = st.session_state
    parts = []
    if ss.get("pref_dark"):
        parts.append(_DARK_CSS)
    if ss.get("pref_compact"):
        parts.append(_COMPACT_CSS)
    if ss.get("pref_large"):
        parts.append(_LARGE_CSS)
    return "\n".join(parts)


def apply_branding() -> None:
    """Injiziert das Basis-CSS plus die aktiven Darstellungsmodi. Einmal pro Seite."""
    st.markdown(_CSS, unsafe_allow_html=True)
    mode = _mode_css()
    if mode:
        st.markdown(f"<style>{mode}</style>", unsafe_allow_html=True)


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
    with st.sidebar:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="mf-badges" style="padding:0 6px;">
              <span class="mf-badge">🔒 DSGVO-orientiert</span>
              <span class="mf-badge">🩺 Ärztliche Prüfung</span>
              <span class="mf-badge">⚖️ Kein Medizinprodukt</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="mf-sb-foot" style="padding:0 6px;">
              {C.APP_NAME} v{C.APP_VERSION}<br>
              Unterstützung bei der Dokumentation –<br>kein Ersatz für ärztliche Entscheidungen.<br>
              <a href="mailto:{C.SUPPORT_EMAIL}" style="color:#5EEAD4;">Feedback &amp; Support</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_header(title: str, subtitle: str = "", eyebrow: str = "", badges: list[str] | None = None) -> None:
    """Einheitlicher Seitenkopf (Navy-Hero-Band)."""
    eyebrow_html = f'<span class="mf-eyebrow">{eyebrow}</span>' if eyebrow else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    badges_html = ""
    if badges:
        chips = "".join(f'<span class="mf-badge">{b}</span>' for b in badges)
        badges_html = f'<div class="mf-badges">{chips}</div>'
    st.markdown(
        f"""
        <div class="mf-hero">
          {eyebrow_html}
          <h1>{title}</h1>
          {subtitle_html}
          {badges_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def step(num: int, title: str) -> None:
    """Nummerierter Schritt-Header für den Step-by-Step-Flow."""
    st.markdown(
        f"<div class='mf-step'><span class='mf-step-num'>{num}</span>"
        f"<span class='mf-step-title'>{title}</span></div>",
        unsafe_allow_html=True,
    )


def note(text: str, kind: str = "") -> None:
    """Hinweis-Box. kind: '' | 'amber' | 'teal' | 'red'."""
    cls = f"mf-note {kind}".strip()
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)

```

---

## lib/components.py

```python
"""Wiederverwendbare UI-Bausteine: Ergebnis-Karte, Kopieren/Download, Feedback,
Beispiel-Buttons und der (session-basierte) Verlauf."""
from __future__ import annotations

import json
import uuid
from datetime import datetime

import streamlit as st

from lib.config import DOC_TYPES, DocType, EXAMPLES
from lib.export import markdown_to_pdf

NOTES_KEY = "notes_input"
HISTORY_KEY = "history"


# --------------------------------------------------------------------------- #
# Verlauf (nur in der Session – wird beim Neuladen gelöscht)
# --------------------------------------------------------------------------- #
def add_to_history(*, doc_type: DocType, text: str, model: str, elapsed_s: float,
                   input_preview: str, input_words: int, output_words: int) -> None:
    item = {
        "id": uuid.uuid4().hex,
        "ts": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "doc_label": doc_type.label,
        "doc_icon": doc_type.icon,
        "text": text,
        "model": model,
        "elapsed_s": elapsed_s,
        "input_preview": input_preview,
        "input_words": input_words,
        "output_words": output_words,
    }
    st.session_state.setdefault(HISTORY_KEY, []).insert(0, item)


def get_history() -> list[dict]:
    return st.session_state.get(HISTORY_KEY, [])


def clear_history() -> None:
    st.session_state[HISTORY_KEY] = []


# --------------------------------------------------------------------------- #
# Beispiel-Buttons (befüllen das Eingabefeld, statt es vorzubelegen)
# --------------------------------------------------------------------------- #
def _set_example(text: str) -> None:
    st.session_state[NOTES_KEY] = text


def example_buttons() -> None:
    st.caption("Beispiel laden:")
    cols = st.columns(len(EXAMPLES))
    for col, ex in zip(cols, EXAMPLES):
        with col:
            st.button(
                f"＋ {ex.title}",
                key=f"ex_{ex.title}",
                on_click=_set_example,
                args=(ex.text,),
                use_container_width=True,
            )


# --------------------------------------------------------------------------- #
# Voice-Input (Diktat → Transkription)
# --------------------------------------------------------------------------- #
_AUDIO_HASH_KEY = "last_audio_hash"


def voice_input() -> None:
    """Mikrofon-Aufnahme aufnehmen, per Whisper transkribieren und ins Notizfeld einfügen."""
    from lib.llm import ConfigError, LLMError, transcribe_audio

    with st.container(border=True):
        st.markdown(
            "<div style='font-weight:600;color:#0B1F3A;'>🎙️ Diktieren</div>"
            "<div style='color:#64748B;font-size:.85rem;margin-bottom:8px;'>"
            "Notizen einfach einsprechen – der Text wird automatisch unten eingefügt.</div>",
            unsafe_allow_html=True,
        )
        try:
            audio = st.audio_input("Aufnahme", label_visibility="collapsed", key="voice_audio")
        except Exception:
            st.caption("Spracheingabe wird von dieser Streamlit-Version nicht unterstützt.")
            return

    if audio is None:
        return
    try:
        data = audio.getvalue()
    except Exception:
        return
    if not data:
        return

    audio_id = hash(data)
    if st.session_state.get(_AUDIO_HASH_KEY) == audio_id:
        return  # diese Aufnahme wurde bereits transkribiert

    with st.spinner("Transkribiere Aufnahme …"):
        try:
            text = transcribe_audio(data)
        except (ConfigError, LLMError) as exc:
            st.session_state[_AUDIO_HASH_KEY] = audio_id  # nicht endlos neu versuchen
            st.error(str(exc))
            return

    st.session_state[_AUDIO_HASH_KEY] = audio_id
    if text:
        current = st.session_state.get(NOTES_KEY, "").strip()
        st.session_state[NOTES_KEY] = (current + ("\n" if current else "") + text).strip()
        st.toast("Transkription eingefügt", icon="✅")
        st.rerun()


# --------------------------------------------------------------------------- #
# Dokumentationstyp-Auswahl als Karten
# --------------------------------------------------------------------------- #
DOC_TYPE_IDX_KEY = "doc_type_idx"


def doc_type_selector() -> DocType:
    """Zeigt die Dokumentationstypen als auswählbare Karten und gibt den gewählten Typ zurück."""
    if DOC_TYPE_IDX_KEY not in st.session_state:
        st.session_state[DOC_TYPE_IDX_KEY] = 0
    selected = st.session_state[DOC_TYPE_IDX_KEY]

    per_row = 3
    for start in range(0, len(DOC_TYPES), per_row):
        cols = st.columns(per_row)
        for col_i in range(per_row):
            gi = start + col_i
            if gi >= len(DOC_TYPES):
                continue
            dt = DOC_TYPES[gi]
            is_sel = gi == selected
            with cols[col_i]:
                with st.container(border=True):
                    title_cls = "mf-doc-title sel" if is_sel else "mf-doc-title"
                    if is_sel:
                        check = "<div class='mf-doc-check'>✓ Ausgewählt</div>"
                    else:
                        check = "<div class='mf-doc-check' style='visibility:hidden'>•</div>"
                    st.markdown(
                        f"<div class='mf-doc-card'>"
                        f"<div class='mf-doc-icon'>{dt.icon}</div>"
                        f"<div class='{title_cls}'>{dt.label}</div>"
                        f"<div class='mf-doc-desc'>{dt.short}</div>"
                        f"{check}</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "Ausgewählt" if is_sel else "Auswählen",
                        key=f"dtbtn_{dt.key}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state[DOC_TYPE_IDX_KEY] = gi
                        st.rerun()
    return DOC_TYPES[st.session_state[DOC_TYPE_IDX_KEY]]


# --------------------------------------------------------------------------- #
# Ergebnis-Karte
# --------------------------------------------------------------------------- #
def _filename(doc_type: DocType, ext: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f"medflowai_{doc_type.key}_{stamp}.{ext}"


def copy_button(text: str, key: str = "cpy") -> None:
    """Echter Kopier-Button mit sichtbarem Erfolgs-Feedback (✓ Kopiert!)."""
    import streamlit.components.v1 as components

    safe = json.dumps(text)
    bid = f"cpy_{key}"
    html = f"""
    <button id="{bid}" style="width:100%;padding:11px 14px;border:none;
        border-radius:12px;background:#14B8A6;color:#fff;font-weight:600;
        font-size:14px;cursor:pointer;box-shadow:0 6px 16px rgba(20,184,166,.25);
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
        transition:background .15s ease;">📋 In Zwischenablage kopieren</button>
    <script>
    (function() {{
      const b = document.getElementById("{bid}");
      const label = "📋 In Zwischenablage kopieren";
      b.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText({safe});
          b.textContent = "✓ Kopiert!";
          b.style.background = "#15803D";
          setTimeout(() => {{ b.textContent = label; b.style.background = "#14B8A6"; }}, 1800);
        }} catch (e) {{
          b.textContent = "Bitte Text oben manuell markieren & kopieren";
          b.style.background = "#B45309";
        }}
      }});
    }})();
    </script>
    """
    components.html(html, height=54)


def render_result_card(
    *,
    text: str,
    doc_type: DocType,
    model: str,
    elapsed_s: float,
    key_prefix: str = "res",
    show_feedback: bool = True,
) -> None:
    """Rendert die Dokumentation als Karte mit Kopier-/Download-Aktionen."""
    words = len(text.split())
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")

    with st.container(border=True):
        # Kopfzeile
        st.markdown(
            f"""
            <div class="mf-result-head">
              <span class="mf-tag">{doc_type.icon} {doc_type.label}</span>
              <span class="mf-meta">{ts} · {words} Wörter · {model} · {elapsed_s:.1f}s</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Inhalt (echtes Markdown-Rendering)
        st.markdown(text)

        st.divider()

        # Kopieren – mit sichtbarem Erfolgs-Feedback
        copy_button(text, key=key_prefix)

        # Export: Markdown · Text · PDF
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "⬇️ Markdown",
                data=text,
                file_name=_filename(doc_type, "md"),
                mime="text/markdown",
                use_container_width=True,
                key=f"{key_prefix}_dl_md",
            )
        with c2:
            st.download_button(
                "⬇️ Text",
                data=text,
                file_name=_filename(doc_type, "txt"),
                mime="text/plain",
                use_container_width=True,
                key=f"{key_prefix}_dl_txt",
            )
        with c3:
            pdf_bytes = markdown_to_pdf(text, doc_type.label)
            if pdf_bytes:
                st.download_button(
                    "⬇️ PDF",
                    data=pdf_bytes,
                    file_name=_filename(doc_type, "pdf"),
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"{key_prefix}_dl_pdf",
                )
            else:
                st.button(
                    "⬇️ PDF",
                    disabled=True,
                    use_container_width=True,
                    key=f"{key_prefix}_pdf_off",
                    help="PDF-Export wird nach dem nächsten Deploy verfügbar.",
                )

        # Pflichthinweis direkt am Ergebnis
        st.markdown(
            '<div class="mf-note amber" style="margin-top:10px;">'
            "⚠️ <strong>Vorschlag zur Dokumentation.</strong> Vor Übernahme in die "
            "Akte ärztlich auf Richtigkeit und Vollständigkeit prüfen.</div>",
            unsafe_allow_html=True,
        )

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

## lib/llm.py

```python
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
    return OpenAI(api_key=api_key)


def api_key_available() -> bool:
    """Für die UI: ist überhaupt ein Key konfiguriert?"""
    return bool(_read_api_key())


def generate_documentation(
    notes: str,
    doc_type: DocType,
    *,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 900,
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
    text = (response.choices[0].message.content or "").strip()
    if not text:
        raise LLMError(
            "Die KI hat keine Ausgabe zurückgegeben. Bitte erneut versuchen oder "
            "die Notizen etwas konkreter fassen."
        )
    return GenerationResult(text=text, model=model, elapsed_s=elapsed)


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
    if "ratelimit" in name or "rate limit" in msg or "429" in msg:
        return (
            "Aktuell sind zu viele Anfragen unterwegs (Rate-Limit). Bitte einen "
            "Moment warten und erneut versuchen."
        )
    if "insufficient_quota" in msg or "quota" in msg or "billing" in msg:
        return (
            "Das OpenAI-Kontingent ist erschöpft. Bitte das Guthaben bzw. die "
            "Abrechnung im OpenAI-Konto prüfen."
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

```

---

## lib/prompts.py

```python
"""Prompt-Bausteine pro Dokumentationstyp.

Getrennt von der LLM-Logik, damit medizinische Vorgaben leicht überprüfbar und
versionierbar bleiben. Die Leitplanken (keine Diagnose, nur vorhandene Infos)
stehen sowohl im System- als auch im User-Prompt – doppelt hält besser.
"""
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
    "- Verwende ausschließlich Informationen aus den Notizen. Erfinde nichts und "
    "ergänze keine plausiblen, aber nicht genannten Befunde.\n"
    "- Was fehlt oder unklar ist, nennst du knapp unter 'Offene Punkte'.\n"
    "- Schreibe in deutscher medizinischer Fachsprache, präzise und verständlich.\n"
    "- Kompakt statt ausschweifend. Keine Einleitungs- oder Schlussfloskeln, "
    "keine Meta-Kommentare über dich selbst."
)

# Typ-spezifische Aufgabe + Zielstruktur
_TEMPLATES: dict[str, str] = {
    "verlauf": (
        "Erstelle eine kompakte Verlaufsdokumentation für die Patientenakte.\n"
        "Struktur:\n"
        "1. Anlass / Beschwerden\n"
        "2. Relevante Angaben & Befunde\n"
        "3. Einschätzung / mögliche Abklärung (nur als Notiz, keine Festlegung)\n"
        "4. Weiteres Vorgehen\n"
        "5. Offene Punkte"
    ),
    "soap": (
        "Erstelle eine strukturierte SOAP-Notiz.\n"
        "Struktur:\n"
        "**S – Subjektiv:** Angaben und Beschwerden des Patienten\n"
        "**O – Objektiv:** erhobene Befunde, Messwerte, Untersuchung\n"
        "**A – Assessment:** zusammenfassende Einschätzung (offen formuliert, "
        "keine endgültige Diagnose)\n"
        "**P – Plan:** geplantes Vorgehen / nächste Schritte\n"
        "Ergänze am Ende 'Offene Punkte', falls Angaben fehlen."
    ),
    "summary": (
        "Erstelle eine kurze, gut verständliche Zusammenfassung für den Patienten "
        "in einfacher Sprache (kein Fachjargon, kurze Sätze).\n"
        "Struktur:\n"
        "1. Was war der Grund des Besuchs?\n"
        "2. Was wurde besprochen / festgestellt?\n"
        "3. Was sind die nächsten Schritte für Sie?\n"
        "4. Wann sollten Sie sich wieder melden?\n"
        "Formuliere wertschätzend und beruhigend, ohne Versprechen zu machen."
    ),
    "referral": (
        "Erstelle den ENTWURF eines Arztbriefs bzw. einer Überweisung "
        "(klar als Entwurf zur ärztlichen Prüfung).\n"
        "Struktur:\n"
        "1. Anrede / Fragestellung an die mitbehandelnde Stelle\n"
        "2. Anamnese (Zusammenfassung)\n"
        "3. Aktuelle Befunde\n"
        "4. Bisheriges Vorgehen / Medikation\n"
        "5. Konkrete Fragestellung / Bitte um Mitbeurteilung\n"
        "6. Offene Punkte\n"
        "Verwende neutrale Platzhalter wie [Empfänger], [Datum], wenn Angaben fehlen."
    ),
    "todo": (
        "Leite aus den Notizen eine knappe To-do- / Abklärungsliste für das "
        "Praxisteam ab.\n"
        "Format:\n"
        "- Checkliste mit kurzen, konkreten Punkten (Was, ggf. von wem/bis wann, "
        "falls notiert)\n"
        "- Abschnitt 'Weitere Abklärung' für sinnvolle nächste diagnostische "
        "Schritte, die sich aus den Notizen ergeben (als Vorschlag, nicht als "
        "Anweisung)\n"
        "- Abschnitt 'Offene Punkte' für Fehlendes"
    ),
}


def build_messages(doc_type: DocType, notes: str) -> list[dict]:
    """Baut die Chat-Messages für die OpenAI-API."""
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

## lib/audit.py

```python
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

```

---

## lib/export.py

```python
"""Export-Helfer: Dokumentation als PDF.

Bewusst ohne Streamlit-Abhängigkeit und ohne System-Bibliotheken (fpdf2 ist reines
Python), damit es auf Streamlit Cloud zuverlässig läuft. Schlägt die PDF-Erzeugung
aus irgendeinem Grund fehl, gibt die Funktion None zurück und die UI blendet den
PDF-Button aus, statt die App abstürzen zu lassen.
"""
from __future__ import annotations

from datetime import datetime
from functools import lru_cache

# fpdf2 (Kernschrift Helvetica) kodiert Text als Latin-1. Deutsche Umlaute sind
# darin enthalten; einige typografische Sonderzeichen ersetzen wir vorher.
_REPLACEMENTS = {
    "–": "-", "—": "-",
    "‘": "'", "’": "'",
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "•": "-", "…": "...",
    "·": "-", " ": " ", "→": "->", "✅": "", "⚠": "", "️": "",
}


def _latin1(text: str) -> str:
    for src, dst in _REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


@lru_cache(maxsize=64)
def markdown_to_pdf(text: str, title: str) -> bytes | None:
    """Rendert die (Markdown-)Dokumentation als schlichtes, lesbares PDF.

    Ergebnisse werden zwischengespeichert (lru_cache), damit z. B. die Verlaufs-
    Suche nicht bei jedem Tastendruck alle PDFs neu erzeugt. Gibt die PDF-Bytes
    zurück oder None, falls fpdf fehlt oder die Erzeugung fehlschlägt (die App
    stürzt dadurch nie ab).
    """
    try:
        from fpdf import FPDF

        # Jede Zeile beginnt wieder am linken Rand und rückt nach unten,
        # damit immer die volle Breite verfügbar ist.
        def line(txt: str, size: int, bold: bool = False, italic: bool = False,
                 gray: bool = False, height: float = 6.0):
            style = ("B" if bold else "") + ("I" if italic else "")
            pdf.set_font("Helvetica", style, size)
            pdf.set_text_color(120, 120, 120) if gray else pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, height, _latin1(txt), new_x="LMARGIN", new_y="NEXT")

        pdf = FPDF(format="A4")
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.set_margins(18, 16, 18)
        pdf.add_page()

        line(title, 15, bold=True, height=8)
        line("Erstellt mit MedFlowAI - " + datetime.now().strftime("%d.%m.%Y %H:%M"),
             9, gray=True, height=5)
        pdf.ln(3)

        for raw in text.split("\n"):
            content = raw.rstrip()
            if not content:
                pdf.ln(3)
                continue
            if content.startswith("###"):
                line(content.lstrip("# ").strip().replace("**", ""), 11, bold=True)
            elif content.startswith("##"):
                line(content.lstrip("# ").strip().replace("**", ""), 12, bold=True)
            elif content.startswith("#"):
                line(content.lstrip("# ").strip().replace("**", ""), 13, bold=True)
            else:
                line(content.replace("**", ""), 11)

        pdf.ln(4)
        line("Dokumentationsvorschlag - aerztlich auf Richtigkeit und "
             "Vollstaendigkeit zu pruefen. Keine Diagnose.",
             8, italic=True, gray=True, height=4)

        return bytes(pdf.output())
    except Exception:
        return None

```

---

## views/dokumentation.py

```python
"""Hauptseite: Notizen → strukturierte Dokumentation."""
from __future__ import annotations

import streamlit as st

from lib import audit
from lib.branding import note, page_header, step
from lib.components import (
    NOTES_KEY,
    add_to_history,
    doc_type_selector,
    example_buttons,
    render_result_card,
    voice_input,
)
from lib.config import DOC_TYPE_BY_KEY
from lib.llm import ConfigError, LLMError, api_key_available, generate_documentation

page_header(
    title="Dokumentation erstellen",
    subtitle="Aus knappen Notizen wird strukturierte, prüfbare Dokumentation – in Sekunden.",
    eyebrow="Arbeitsbereich",
    badges=["🔒 Keine Speicherung von Patiententext", "🩺 Ärztliche Prüfung erforderlich"],
)

# Datenschutz-Hinweis ganz oben – bewusst prominent.
note(
    "🔐 <strong>Bitte keine direkt identifizierenden Daten eingeben</strong> "
    "(Name, Geburtsdatum, Versichertennummer, Adresse). Für die Dokumentation "
    "genügen die medizinisch relevanten Angaben.",
    kind="teal",
)
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Key-Verfügbarkeit prüfen (kein Crash, klare Anleitung).
key_ok = api_key_available()
if not key_ok:
    note(
        "⚙️ <strong>Noch nicht einsatzbereit:</strong> Es ist kein OpenAI-API-Key "
        "konfiguriert. In der Streamlit Cloud unter <em>Settings → Secrets</em> den "
        "Eintrag <code>OPENAI_API_KEY</code> hinterlegen.",
        kind="amber",
    )
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# 1) Notizen
# --------------------------------------------------------------------------- #
step(1, "Arzt-Notizen / Gesprächsinhalt")
st.session_state.setdefault(NOTES_KEY, "")
voice_input()
example_buttons()
st.text_area(
    "Notizen",
    key=NOTES_KEY,
    height=190,
    placeholder="Stichpunkte oder Fließtext zum Patientenkontakt … "
    "z. B. Beschwerden, Befunde, Vorerkrankungen, Medikation.",
    label_visibility="collapsed",
)
notes = st.session_state.get(NOTES_KEY, "")
st.caption(f"{len(notes)} Zeichen · {len(notes.split())} Wörter")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# 2) Dokumentationstyp
# --------------------------------------------------------------------------- #
step(2, "Art der Dokumentation")
doc_type = doc_type_selector()

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# 3) Aktion
# --------------------------------------------------------------------------- #
def _clear_notes() -> None:
    """Callback: läuft vor dem nächsten Rendern, daher darf das Notizfeld geleert werden."""
    st.session_state[NOTES_KEY] = ""
    st.session_state.pop("last_result", None)


step(3, "Erstellen & prüfen")
b1, b2 = st.columns([3, 1])
with b1:
    run = st.button(
        "Dokumentation erstellen",
        type="primary",
        use_container_width=True,
        disabled=(not notes.strip()) or (not key_ok),
    )
with b2:
    st.button("Leeren", use_container_width=True, on_click=_clear_notes)

# --------------------------------------------------------------------------- #
# Generierung
# --------------------------------------------------------------------------- #
if run:
    error_msg = None
    result = None
    with st.status("KI verarbeitet die Notizen …", expanded=True) as status:
        st.write("Eingaben werden geprüft …")
        try:
            result = generate_documentation(notes, doc_type)
        except (ConfigError, LLMError) as exc:
            error_msg = str(exc)
            status.update(label="Erstellung fehlgeschlagen", state="error")
        else:
            st.write(f"Struktur „{doc_type.label}“ wird angewendet …")
            status.update(
                label=f"Dokumentation erstellt ({result.elapsed_s:.1f}s)",
                state="complete",
            )

    if error_msg:
        st.error(error_msg)
    elif result is not None:
        import uuid

        st.session_state["last_result"] = {
            "id": uuid.uuid4().hex[:8],
            "text": result.text,
            "doc_type": doc_type.key,
            "model": result.model,
            "elapsed": result.elapsed_s,
        }
        # Pseudonymisiertes Audit (nur wenn Opt-in aktiv) – kein Patiententext.
        audit.record_event(
            doc_type_key=doc_type.key,
            notes=notes,
            output_text=result.text,
            model=result.model,
            elapsed_s=result.elapsed_s,
        )
        # Session-Verlauf
        add_to_history(
            doc_type=doc_type,
            text=result.text,
            model=result.model,
            elapsed_s=result.elapsed_s,
            input_preview=(notes[:90] + "…") if len(notes) > 90 else notes,
            input_words=len(notes.split()),
            output_words=len(result.text.split()),
        )
        st.toast("Dokumentation erstellt", icon="✅")

# --------------------------------------------------------------------------- #
# Ergebnis anzeigen (bleibt über Reruns erhalten)
# --------------------------------------------------------------------------- #
lr = st.session_state.get("last_result")
if lr:
    st.markdown("### Ergebnis")
    render_result_card(
        text=lr["text"],
        doc_type=DOC_TYPE_BY_KEY[lr["doc_type"]],
        model=lr["model"],
        elapsed_s=lr["elapsed"],
        key_prefix=lr["id"],
    )

```

---

## views/verlauf.py

```python
"""Verlauf der in DIESER Sitzung erstellten Dokumente – Timeline mit Suche.

Weiterhin ausschließlich Session-Speicher: wird beim Neuladen automatisch gelöscht.
"""
from __future__ import annotations

import streamlit as st

from lib.branding import note, page_header
from lib.components import clear_history, copy_button, get_history
from lib.export import markdown_to_pdf

page_header(
    title="Verlauf",
    subtitle="Alle in dieser Sitzung erstellten Dokumentationen – als durchsuchbare Zeitleiste.",
    eyebrow="Arbeitsbereich",
)

history = get_history()

note(
    "🔒 Der Verlauf wird <strong>nur in dieser Sitzung im Arbeitsspeicher</strong> "
    "gehalten und beim Schließen oder Neuladen automatisch gelöscht. "
    "Es findet keine dauerhafte Speicherung statt.",
    kind="teal",
)
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Leerer Zustand
# --------------------------------------------------------------------------- #
if not history:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center; padding:28px 8px; color:#64748B;'>"
            "<div style='font-size:2rem;'>🗂️</div>"
            "<div style='font-weight:700; color:#0B1F3A; margin-top:8px;'>Noch kein Verlauf</div>"
            "<div style='margin-top:4px;'>Erstelle im Bereich <em>Dokumentation</em> dein erstes Dokument – "
            "es erscheint dann hier.</div></div>",
            unsafe_allow_html=True,
        )
    st.stop()

# --------------------------------------------------------------------------- #
# Werkzeugleiste: Suche + Leeren
# --------------------------------------------------------------------------- #
t1, t2 = st.columns([3, 1])
with t1:
    query = st.text_input(
        "Suche",
        placeholder="🔍  Verlauf durchsuchen (Typ, Inhalt …)",
        label_visibility="collapsed",
        key="hist_search",
    )
with t2:
    if st.button("Verlauf leeren", use_container_width=True):
        clear_history()
        st.session_state.pop("hist_search", None)
        st.rerun()

q = (query or "").strip().lower()


def _matches(item: dict) -> bool:
    if not q:
        return True
    haystack = f"{item['doc_label']} {item.get('input_preview', '')} {item['text']}".lower()
    return q in haystack


filtered = [it for it in history if _matches(it)]
st.caption(f"{len(filtered)} von {len(history)} Einträgen")
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if not filtered:
    note("Keine Treffer für deine Suche. Versuch einen anderen Begriff.", kind="")
    st.stop()

# --------------------------------------------------------------------------- #
# Timeline
# --------------------------------------------------------------------------- #
for item in filtered:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span style="width:10px; height:10px; border-radius:50%; background:#14B8A6;
                box-shadow:0 0 0 4px rgba(20,184,166,.15); display:inline-block;"></span>
              <span class="mf-tag">{item['doc_icon']} {item['doc_label']}</span>
              <span class="mf-meta">{item['ts']} · {item['output_words']} Wörter · {item['model']}</span>
            </div>
            <div class="mf-meta" style="margin-top:7px;">{item['input_preview']}</div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Dokumentation anzeigen"):
            st.markdown(item["text"])
            st.divider()
            copy_button(item["text"], key=item["id"])
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button(
                    "⬇️ Markdown",
                    data=item["text"],
                    file_name=f"medflowai_{item['id'][:8]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key=f"hist_md_{item['id']}",
                )
            with c2:
                st.download_button(
                    "⬇️ Text",
                    data=item["text"],
                    file_name=f"medflowai_{item['id'][:8]}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"hist_txt_{item['id']}",
                )
            with c3:
                pdf_bytes = markdown_to_pdf(item["text"], item["doc_label"])
                if pdf_bytes:
                    st.download_button(
                        "⬇️ PDF",
                        data=pdf_bytes,
                        file_name=f"medflowai_{item['id'][:8]}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"hist_pdf_{item['id']}",
                    )
                else:
                    st.button(
                        "⬇️ PDF",
                        disabled=True,
                        use_container_width=True,
                        key=f"hist_pdf_off_{item['id']}",
                        help="PDF-Export gerade nicht verfügbar.",
                    )

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

page_header(
    title="Datenschutz & Sicherheit",
    subtitle="Transparenz darüber, welche Daten wie verarbeitet werden.",
    eyebrow="Information",
    badges=["Art. 9 DSGVO", "Datensparsamkeit", "Privacy by Default"],
)

# --------------------------------------------------------------------------- #
# Datenfluss
# --------------------------------------------------------------------------- #
st.markdown("### So fließen die Daten")
c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("**1 · Eingabe**")
        st.markdown(
            "Die Notizen werden im Browser eingegeben und verschlüsselt (TLS) "
            "übertragen. Empfehlung: keine direkt identifizierenden Daten."
        )
with c2:
    with st.container(border=True):
        st.markdown("**2 · KI-Verarbeitung**")
        st.markdown(
            "Die Verarbeitung erfolgt über die **OpenAI-API**. Dabei verlässt der "
            "Text die Anwendung und wird bei einem Auftragsverarbeiter (ggf. außerhalb "
            "der EU) verarbeitet."
        )
with c3:
    with st.container(border=True):
        st.markdown("**3 · Ergebnis**")
        st.markdown(
            "Das Ergebnis wird angezeigt. **Patiententext wird serverseitig nicht "
            "gespeichert.** Der Verlauf bleibt nur in der Sitzung."
        )

note(
    "⚠️ <strong>Wichtig:</strong> Für den realen Praxiseinsatz mit echten "
    "Patientendaten ist ein <strong>Auftragsverarbeitungsvertrag (AVV)</strong> mit "
    "dem KI-Anbieter erforderlich. Empfehlenswert sind EU-Verarbeitung "
    "(z. B. Azure OpenAI in der EU-Region) und ein Endpoint mit "
    "<strong>Zero Data Retention</strong>.",
    kind="amber",
)

st.divider()

# --------------------------------------------------------------------------- #
# Audit-Log (Opt-in)
# --------------------------------------------------------------------------- #
st.markdown("### Pseudonymisiertes Audit-Log")
st.markdown(
    "Optional kann ein **technisches Protokoll** geführt werden – ausschließlich "
    "mit **Metadaten** (Zeitpunkt, Dokumenttyp, Modell, Längen, nicht umkehrbarer "
    "Fingerprint). **Kein Patiententext, keine Ausgaben** werden gespeichert. "
    "Standardmäßig ist diese Funktion deaktiviert."
)

enabled = st.toggle(
    "Audit-Log aktivieren (nur Metadaten)",
    value=audit.is_enabled(),
    help="Schreibt pro Erstellung eine Metadaten-Zeile. Lässt sich jederzeit wieder "
    "abschalten und löschen.",
)
audit.set_enabled(enabled)

if enabled:
    note("✅ Audit-Log ist aktiv. Es werden ausschließlich Metadaten erfasst.", kind="teal")
else:
    note("⛔ Audit-Log ist deaktiviert. Es werden keinerlei Vorgänge protokolliert.", kind="")

events = audit.read_events()
if events:
    st.markdown("#### Erfasste Metadaten (Vorschau)")
    st.caption(f"{len(events)} Einträge · enthält keinen Patiententext")
    # Nur unkritische Spalten zeigen.
    preview = [
        {
            "Zeitpunkt": e.get("ts", ""),
            "Typ": e.get("doc_type", ""),
            "Modell": e.get("model", ""),
            "Eingabe (Wörter)": e.get("input_words", ""),
            "Ausgabe (Wörter)": e.get("output_words", ""),
            "Dauer (s)": e.get("elapsed_s", ""),
            "Fingerprint": e.get("input_fingerprint", ""),
        }
        for e in reversed(events)
    ]
    st.dataframe(preview, use_container_width=True, hide_index=True)

    d1, d2 = st.columns(2)
    with d1:
        jsonl = "\n".join(json.dumps(e, ensure_ascii=False) for e in events)
        st.download_button(
            "⬇️ Audit-Log exportieren (JSONL)",
            data=jsonl,
            file_name="medflowai_audit_log.jsonl",
            mime="application/x-ndjson",
            use_container_width=True,
        )
    with d2:
        if st.button("🗑️ Audit-Log löschen", use_container_width=True):
            audit.clear_log()
            st.rerun()
else:
    st.caption("Noch keine Einträge erfasst.")

st.divider()

# --------------------------------------------------------------------------- #
# Sicherheits- und Produktiv-Hinweise
# --------------------------------------------------------------------------- #
st.markdown("### Checkliste für den Produktivbetrieb")
st.markdown(
    "Diese Punkte sind vor dem Einsatz mit echten Patientendaten zu klären:"
)
st.markdown(
    "- **AVV** mit dem KI-Anbieter abschließen; möglichst EU-Region & Zero Data Retention.\n"
    "- **Zugriffsschutz**: Authentifizierung (Praxis-Accounts), Rollen, sichere Sitzungen.\n"
    "- **Verschlüsselung** ruhender Daten (falls künftig persistiert wird).\n"
    "- **Löschkonzept & Aufbewahrungsfristen** definieren.\n"
    "- **Verfahrensverzeichnis** und ggf. **Datenschutz-Folgenabschätzung (DSFA)**.\n"
    "- **Mitarbeitenden-Schulung** zur Pseudonymisierung der Eingaben.\n"
    "- **Mandantentrennung** je Praxis / MVZ."
)

note(
    "ℹ️ Diese Hinweise sind eine technische Orientierung und <strong>kein "
    "Rechtsrat</strong>. Die datenschutzrechtliche Bewertung sollte mit einer/einem "
    "Datenschutzbeauftragten erfolgen.",
    kind="",
)

```

---

## views/grenzen.py

```python
"""Grenzen & verantwortungsvoller Einsatz (Limitations) – als Karten."""
from __future__ import annotations

import streamlit as st

from lib.branding import note, page_header

page_header(
    title="Grenzen & verantwortungsvoller Einsatz",
    subtitle="Was MedFlowAI leistet – und was bewusst nicht.",
    eyebrow="Information",
    badges=["Patientensicherheit zuerst"],
)

note(
    "🩺 <strong>Unterstützung, kein Ersatz.</strong> MedFlowAI hilft beim "
    "Formulieren und Strukturieren von Dokumentation. Die medizinische "
    "Verantwortung bleibt vollständig bei der behandelnden Ärztin / dem Arzt.",
    kind="teal",
)
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

LIMITS = [
    ("🚫", "Keine Diagnose", "Stellt keine Diagnosen und trifft keine medizinischen "
     "Entscheidungen. Jede Ausgabe ist ausdrücklich nur ein Vorschlag."),
    ("👩‍⚕️", "Ärztliche Prüfung", "Jede generierte Dokumentation muss vor der "
     "Übernahme in die Akte ärztlich auf Richtigkeit und Vollständigkeit geprüft werden."),
    ("⚠️", "Mögliche Fehler", "KI-Ausgaben können Fehler enthalten oder Nuancen "
     "übersehen – besonders bei knappen oder unklaren Notizen."),
    ("🔒", "Pseudonymisieren", "Bitte keine direkt identifizierenden Patientendaten "
     "eingeben (Name, Geburtsdatum, Versichertennummer). Siehe Datenschutz & Sicherheit."),
    ("🧩", "Kein PVS-Ersatz", "Ersetzt weder das Praxisverwaltungssystem noch die "
     "klinische Beurteilung – es ergänzt sie nur."),
    ("⚖️", "Kein Medizinprodukt", "Dokumentations-Hilfswerkzeug, nach derzeitiger "
     "Auslegung kein Medizinprodukt im Sinne der MDR (EU 2017/745)."),
]

per_row = 2
for start in range(0, len(LIMITS), per_row):
    cols = st.columns(per_row)
    for col_i in range(per_row):
        gi = start + col_i
        if gi >= len(LIMITS):
            continue
        icon, title, body = LIMITS[gi]
        with cols[col_i]:
            with st.container(border=True):
                st.markdown(
                    f"<div style='display:flex; align-items:flex-start; gap:10px;'>"
                    f"<div style='font-size:1.5rem; line-height:1;'>{icon}</div>"
                    f"<div><div style='font-weight:700; color:#0B1F3A;'>{title}</div>"
                    f"<div style='color:#475569; font-size:.9rem; margin-top:3px;'>{body}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
note(
    "Im Zweifel gilt: Die ärztliche Entscheidung hat immer Vorrang vor jeder "
    "KI-generierten Formulierung.",
    kind="amber",
)

```

---

## views/ueber.py

```python
"""Über MedFlowAI: Positionierung, Zielgruppe, Grenzen, Impressum."""
from __future__ import annotations

import streamlit as st

from lib import config as C
from lib.branding import note, page_header

page_header(
    title=f"Über {C.APP_NAME}",
    subtitle=C.APP_TAGLINE,
    eyebrow="Information",
    badges=[f"Version {C.APP_VERSION}", "Made for Praxen & MVZ"],
)

# --------------------------------------------------------------------------- #
# Wertversprechen
# --------------------------------------------------------------------------- #
st.markdown(
    f"**{C.APP_NAME}** verwandelt knappe Arzt-Notizen oder Gesprächsinhalte in "
    "klar strukturierte, prüfbare Dokumentation – damit mehr Zeit für die Patientin "
    "oder den Patienten bleibt und weniger für die Tastatur."
)

st.markdown("### Was die Anwendung leistet")
f1, f2, f3 = st.columns(3)
for col, (icon, title, body) in zip(
    (f1, f2, f3),
    [
        ("⏱️", "Zeit sparen", "Aus Stichpunkten werden in Sekunden strukturierte Verlaufs- oder SOAP-Notizen."),
        ("🧩", "Konsistente Struktur", "Einheitliche, nachvollziehbare Form über alle Dokumente hinweg."),
        ("🔍", "Prüfbar", "Nutzt nur die eingegebenen Angaben; Fehlendes wird offen ausgewiesen."),
    ],
):
    with col:
        with st.container(border=True):
            st.markdown(f"#### {icon} {title}")
            st.markdown(body)

st.divider()

# --------------------------------------------------------------------------- #
# Abgrenzung / Positionierung
# --------------------------------------------------------------------------- #
st.markdown("### Klare Abgrenzung")
note(
    "🩺 <strong>Unterstützung, kein Ersatz.</strong> MedFlowAI stellt <strong>keine "
    "Diagnosen</strong>, gibt keine Therapieanweisungen und trifft keine "
    "medizinischen Entscheidungen. Jede Ausgabe ist ein <strong>Dokumentations­"
    "vorschlag</strong> und muss ärztlich geprüft werden.",
    kind="teal",
)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
note(
    "⚖️ <strong>Kein Medizinprodukt.</strong> Die Anwendung ist ein "
    "Dokumentations-Hilfswerkzeug und nach derzeitiger Auslegung "
    "<strong>kein Medizinprodukt</strong> im Sinne der Verordnung (EU) 2017/745 "
    "(MDR), da sie weder diagnostiziert noch therapeutische Entscheidungen trifft. "
    "Eine verbindliche regulatorische Einordnung ist im Einzelfall mit Fachexpertise "
    "vorzunehmen.",
    kind="amber",
)

st.divider()

# --------------------------------------------------------------------------- #
# Zielgruppe & Ablauf
# --------------------------------------------------------------------------- #
left, right = st.columns(2)
with left:
    st.markdown("### Für wen")
    st.markdown(
        "- Hausärztinnen und Hausärzte\n"
        "- Fachärztinnen und Fachärzte\n"
        "- Arztpraxen\n"
        "- Medizinische Versorgungszentren (MVZ)"
    )
with right:
    st.markdown("### In drei Schritten")
    st.markdown(
        "1. Notizen oder Gesprächsinhalt eingeben\n"
        "2. Art der Dokumentation wählen\n"
        "3. Ergebnis prüfen, kopieren und ins PVS übernehmen"
    )

st.divider()

# --------------------------------------------------------------------------- #
# Impressum (Platzhalter)
# --------------------------------------------------------------------------- #
st.markdown("### Impressum & Kontakt")
st.markdown(
    f"{C.COMPANY} · [Platzhalter Anschrift] · Verantwortlich: [Name] · "
    f"Kontakt: [{C.SUPPORT_EMAIL}](mailto:{C.SUPPORT_EMAIL})  \n"
    f"_{C.APP_NAME} v{C.APP_VERSION} · Research-Preview / MVP_"
)
st.caption(
    "Platzhalter – vor Veröffentlichung durch vollständiges Impressum gemäß § 5 DDG "
    "und Datenschutzerklärung ersetzen."
)

```

---

## views/einstellungen.py

```python
"""Einstellungen: Darstellung & Lesbarkeit (sitzungsweit, über Seiten hinweg stabil).

Hintergrund: Streamlit verwirft den Wert eines Widgets, sobald das Widget nicht
mehr auf der aktiven Seite liegt. Damit die Einstellung beim Seitenwechsel nicht
verloren geht, speichern wir sie in dauerhaften pref_*-Schlüsseln und synchronisieren
die Schalter per Callback dorthin. Das globale CSS (apply_branding) liest pref_*.
"""
from __future__ import annotations

import streamlit as st

from lib.branding import note, page_header

page_header(
    title="Einstellungen",
    subtitle="Passe Darstellung und Lesbarkeit an – die Änderungen wirken sofort und bleiben in dieser Sitzung erhalten.",
    eyebrow="Einstellungen",
)

# (pref_key, widget_key, Titel, Beschreibung)
OPTIONS = [
    ("pref_dark", "tg_dark", "🌙 Dunkelmodus", "Dunkle Oberfläche – angenehmer bei wenig Licht."),
    ("pref_compact", "tg_compact", "↕️ Kompaktmodus", "Weniger Abstände – mehr Inhalt auf einen Blick."),
    ("pref_large", "tg_large", "🔠 Große Schrift", "Größere Schrift für bessere Lesbarkeit."),
]

# Dauerhafte Werte vorbelegen und Schalter daraus initialisieren.
for pref_key, widget_key, _title, _desc in OPTIONS:
    st.session_state.setdefault(pref_key, False)
    if widget_key not in st.session_state:
        st.session_state[widget_key] = st.session_state[pref_key]


def _sync(pref_key: str, widget_key: str) -> None:
    """Callback: Schalterwert in den dauerhaften Schlüssel übernehmen."""
    st.session_state[pref_key] = st.session_state.get(widget_key, False)


st.markdown("### Darstellung")

for pref_key, widget_key, title, desc in OPTIONS:
    with st.container(border=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{title}**")
            st.caption(desc)
        with c2:
            st.toggle(
                title,
                key=widget_key,
                on_change=_sync,
                args=(pref_key, widget_key),
                label_visibility="collapsed",
            )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
note(
    "Diese Einstellungen gelten für die aktuelle Sitzung und werden nicht "
    "dauerhaft auf einem Server gespeichert.",
    kind="teal",
)

```

---

## requirements.txt

```text
streamlit>=1.40,<2
openai>=1.30
fpdf2>=2.7

```

---

## .streamlit/config.toml

```toml
# MedFlowAI – Streamlit Theme
# Tiefes Navy als Markenfarbe, Teal als Akzent. Helle, ruhige Arbeitsfläche.

[theme]
primaryColor = "#14B8A6"          # Akzent (Buttons, Fokus, Slider)
backgroundColor = "#FFFFFF"        # Arbeitsfläche
secondaryBackgroundColor = "#F1F5F9"  # Karten / Inputs
textColor = "#0F172A"              # Slate-900
font = "sans serif"

[server]
# Keine Nutzungsstatistiken an Dritte senden.
gatherUsageStats = false

[browser]
gatherUsageStats = false

```

---

## .gitignore

```text
# Secrets niemals committen
.streamlit/secrets.toml

# Laufzeit-Artefakte
audit_log.jsonl

# Python
__pycache__/
*.py[cod]
.venv/
venv/
.DS_Store

```

