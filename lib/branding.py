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
footer, [data-testid="stToolbar"] {{ visibility: hidden; }}
hr {{ border-color: var(--line); }}

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
