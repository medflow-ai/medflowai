"""Einstellungen: Darstellung & Lesbarkeit (sitzungsweit)."""
from __future__ import annotations

import streamlit as st

from lib.branding import note, page_header

page_header(
    title="Einstellungen",
    subtitle="Passe Darstellung und Lesbarkeit an – die Änderungen wirken sofort.",
    eyebrow="Einstellungen",
)

# Defaults setzen, damit die Schalter einen definierten Startwert haben.
for key in ("ui_dark", "ui_compact", "ui_large"):
    st.session_state.setdefault(key, False)

st.markdown("### Darstellung")

with st.container(border=True):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("**🌙 Dunkelmodus**")
        st.caption("Dunkle Oberfläche – angenehmer bei wenig Licht.")
    with c2:
        st.toggle("Dunkelmodus", key="ui_dark", label_visibility="collapsed")

with st.container(border=True):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("**↕️ Kompaktmodus**")
        st.caption("Weniger Abstände – mehr Inhalt auf einen Blick.")
    with c2:
        st.toggle("Kompaktmodus", key="ui_compact", label_visibility="collapsed")

with st.container(border=True):
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("**🔠 Große Schrift**")
        st.caption("Größere Schrift für bessere Lesbarkeit.")
    with c2:
        st.toggle("Große Schrift", key="ui_large", label_visibility="collapsed")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
note(
    "Diese Einstellungen gelten für die aktuelle Sitzung und werden nicht "
    "dauerhaft gespeichert.",
    kind="teal",
)
