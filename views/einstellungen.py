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
