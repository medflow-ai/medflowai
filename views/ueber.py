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
