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
