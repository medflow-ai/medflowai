"""Hauptseite: Notizen → strukturierte Dokumentation."""
from __future__ import annotations

import streamlit as st

from lib import audit
from lib.branding import note, page_header
from lib.components import (
    NOTES_KEY,
    add_to_history,
    example_buttons,
    render_result_card,
)
from lib.config import DEFAULT_MODEL, DOC_TYPE_BY_KEY, DOC_TYPES
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
st.markdown("#### 1 · Arzt-Notizen / Gesprächsinhalt")
st.session_state.setdefault(NOTES_KEY, "")
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
st.markdown("#### 2 · Art der Dokumentation")
idx = st.radio(
    "Dokumentationstyp",
    options=list(range(len(DOC_TYPES))),
    format_func=lambda i: f"{DOC_TYPES[i].icon}  {DOC_TYPES[i].label}",
    captions=[d.short for d in DOC_TYPES],
    label_visibility="collapsed",
    key="doc_type_idx",
)
doc_type = DOC_TYPES[idx]

# Erweiterte Optionen
with st.expander("Erweiterte Optionen"):
    model = st.selectbox(
        "Modell",
        options=[DEFAULT_MODEL, "gpt-4o"],
        index=0,
        help="gpt-4o-mini ist schnell und günstig; gpt-4o liefert bei komplexen "
        "Notizen etwas präzisere Formulierungen.",
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# 3) Aktion
# --------------------------------------------------------------------------- #
b1, b2 = st.columns([3, 1])
with b1:
    run = st.button(
        "Dokumentation erstellen",
        type="primary",
        use_container_width=True,
        disabled=(not notes.strip()) or (not key_ok),
    )
with b2:
    if st.button("Leeren", use_container_width=True):
        st.session_state[NOTES_KEY] = ""
        st.session_state.pop("last_result", None)
        st.rerun()

# --------------------------------------------------------------------------- #
# Generierung
# --------------------------------------------------------------------------- #
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
