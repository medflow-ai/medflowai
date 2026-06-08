"""Branding & UI-Schicht: CSS-Theme, Seitenkopf, Sidebar-Extras, kleine Bausteine.

Hier liegt das gesamte visuelle Erscheinungsbild. Die Seiten (views/) bleiben
dadurch schlank und konsistent.
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
}}

/* ---------- Grundlayout ---------- */
.block-container {{ padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1040px; }}
[data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3 {{
  color: var(--navy-900); letter-spacing: -0.01em;
}}
[data-testid="stMain"] p, [data-testid="stMain"] li {{ color: var(--ink); }}
footer {{ visibility: hidden; }}

/* ---------- Sidebar: tiefes Navy ---------- */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, var(--navy-900) 0%, var(--navy-800) 100%);
  border-right: 1px solid rgba(255,255,255,.06);
}}
section[data-testid="stSidebar"] * {{ color: #E2E8F0; }}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{ color: #FFFFFF; }}

/* Navigationslinks (st.navigation) */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {{
  border-radius: 10px; margin: 2px 6px; padding: 6px 10px;
  color: #CBD5E1 !important; transition: all .15s ease;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {{
  background: rgba(45,212,191,.14); color: #FFFFFF !important;
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {{
  background: rgba(20,184,166,.22); color: #FFFFFF !important;
  box-shadow: inset 3px 0 0 var(--accent-400);
}}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {{ color: inherit !important; }}

/* ---------- Karten (st.container(border=True)) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {{
  background: #FFFFFF;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 6px 16px rgba(16,24,40,.05);
  padding: 4px 2px;
}}

/* ---------- Eingaben ---------- */
textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
  border-radius: 10px !important;
}}
textarea:focus, .stTextInput input:focus {{
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(20,184,166,.18) !important;
}}

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {{
  border-radius: 10px; font-weight: 600; transition: all .15s ease;
}}
.stButton > button[kind="primary"] {{
  background: var(--accent); border: 1px solid var(--accent);
}}
.stButton > button[kind="primary"]:hover {{
  background: #0FA295; border-color: #0FA295;
}}
.stButton > button[kind="secondary"] {{
  border: 1px solid var(--line); color: var(--navy-800);
}}
.stButton > button[kind="secondary"]:hover {{
  border-color: var(--accent); color: var(--navy-900);
}}

/* ---------- Hero / Seitenkopf ---------- */
.mf-hero {{
  background: linear-gradient(135deg, var(--navy-900) 0%, var(--navy-700) 100%);
  border-radius: 16px; padding: 22px 26px; margin-bottom: 18px; color: #fff;
  box-shadow: 0 10px 30px rgba(11,31,58,.18);
}}
.mf-hero h1 {{ color:#fff !important; margin:0; font-size: 1.55rem; letter-spacing:-.02em; }}
.mf-hero p {{ color:#C7D2E0 !important; margin:.35rem 0 0; font-size: .98rem; }}
.mf-hero .mf-eyebrow {{
  display:inline-block; font-size:.72rem; font-weight:700; letter-spacing:.12em;
  text-transform:uppercase; color: var(--accent-400); margin-bottom:.4rem;
}}

/* ---------- Badges ---------- */
.mf-badges {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }}
.mf-badge {{
  display:inline-flex; align-items:center; gap:6px;
  font-size:.74rem; font-weight:600; padding:4px 10px; border-radius:999px;
  background: rgba(255,255,255,.10); color:#E2E8F0; border:1px solid rgba(255,255,255,.16);
}}

/* Helle Badges für den Inhaltsbereich */
.mf-tag {{
  display:inline-flex; align-items:center; gap:6px; font-size:.74rem; font-weight:600;
  padding:3px 10px; border-radius:999px; background: var(--accent-soft);
  color:#0F766E; border:1px solid #99F6E4;
}}
.mf-tag.gray {{ background:#F1F5F9; color:#475569; border-color:#E2E8F0; }}

/* ---------- Hinweis-Boxen ---------- */
.mf-note {{
  border-radius:12px; padding:12px 14px; font-size:.9rem; line-height:1.5;
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
.mf-result-body {{ line-height:1.62; }}
.mf-result-body h1,.mf-result-body h2,.mf-result-body h3 {{ font-size:1.02rem; margin:.7rem 0 .3rem; }}

/* Sidebar-Fußzeile */
.mf-sb-foot {{ font-size:.74rem; color:#94A3B8; line-height:1.5; }}

/* ---------- Responsive ---------- */
@media (max-width: 640px) {{
  .block-container {{ padding-top: 1.3rem; }}
  .mf-hero {{ padding:18px; }}
  .mf-hero h1 {{ font-size:1.3rem; }}
}}
</style>
"""


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
        # Ältere Streamlit-Version ohne st.logo: Fallback in der Sidebar.
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


def note(text: str, kind: str = "") -> None:
    """Hinweis-Box. kind: '' | 'amber' | 'teal' | 'red'."""
    cls = f"mf-note {kind}".strip()
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)
