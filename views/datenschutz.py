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
            "Notizen werden getippt **oder per Mikrofon diktiert** und "
            "verschlüsselt (TLS) übertragen. Empfehlung: keine direkt "
            "identifizierenden Daten."
        )
with c2:
    with st.container(border=True):
        st.markdown("**2 · KI-Verarbeitung**")
        st.markdown(
            "**Notizen und Diktat-Audio** gehen zur Verarbeitung an die "
            "**OpenAI-API** (Text-Modell bzw. Whisper für die Transkription) – "
            "ein Auftragsverarbeiter ggf. außerhalb der EU."
        )
with c3:
    with st.container(border=True):
        st.markdown("**3 · Ergebnis**")
        st.markdown(
            "Das Ergebnis wird angezeigt. Patiententext wird **nicht dauerhaft "
            "(auf Datenträger) gespeichert** – nur temporär im Arbeitsspeicher der "
            "Sitzung gehalten und mit Sitzungsende verworfen."
        )

note(
    "⚠️ <strong>Wichtig:</strong> Für den realen Praxiseinsatz mit echten "
    "Patientendaten ist ein <strong>Auftragsverarbeitungsvertrag (AVV)</strong> mit "
    "dem KI-Anbieter erforderlich. Empfehlenswert sind EU-Verarbeitung "
    "(z. B. Azure OpenAI in der EU-Region) und ein Endpoint mit "
    "<strong>Zero Data Retention</strong>.",
    kind="amber",
)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
note(
    "⬇️ <strong>Export beachten:</strong> Heruntergeladene Dateien (PDF/Text/Markdown) "
    "enthalten den vollständigen Text und liegen danach <strong>lokal auf deinem "
    "Gerät</strong> – außerhalb der Kontrolle der App. Bitte sicher ablegen oder löschen.",
    kind="",
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

note(
    "ℹ️ Das Protokoll liegt aktuell in einer gemeinsamen Datei und ist "
    "<strong>nicht für den Mehr-Nutzer-/Mehr-Praxen-Betrieb</strong> ausgelegt "
    "(echte Mandantentrennung erst mit Anmeldung). Die Vorschau zeigt nur die "
    "eigene Sitzung.",
    kind="",
)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

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

sid = audit.session_id()
events = audit.read_events(session=sid)
if events:
    st.markdown("#### Erfasste Metadaten dieser Sitzung")
    st.caption(f"{len(events)} Einträge · nur diese Sitzung · enthält keinen Patiententext")
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
        if st.button("🗑️ Einträge dieser Sitzung löschen", use_container_width=True):
            audit.clear_session(sid)
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
