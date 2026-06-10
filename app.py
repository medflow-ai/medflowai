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
