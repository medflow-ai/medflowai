"""Hauptseite: Notizen → strukturierte Dokumentation."""
from __future__ import annotations

from datetime import datetime

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

# Optionales, pseudonymes Fall-Label (hilft beim Wiederfinden im Verlauf).
st.text_input(
    "Fall-Label",
    key="case_label",
    max_chars=60,
    placeholder='🏷️ Fall-Label (optional, pseudonym) – z. B. "Fall A", kein Klarname',
    label_visibility="collapsed",
)
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

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
    max_chars=8000,
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

custom_instruction = None
if doc_type.key == "custom":
    st.caption("Eigene Vorlage – gewünschte Struktur/Abschnitte vorgeben:")
    custom_instruction = st.text_area(
        "Eigene Vorlage",
        key="custom_template",
        height=130,
        max_chars=1500,
        placeholder="z. B.:\nAnamnese\nBefund\nBeurteilung\nProcedere",
        label_visibility="collapsed",
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# 3) Aktion
# --------------------------------------------------------------------------- #
def _clear_notes() -> None:
    """Callback: läuft vor dem nächsten Rendern, daher darf das Notizfeld geleert werden."""
    st.session_state[NOTES_KEY] = ""
    st.session_state.pop("last_result", None)


out_lang = st.selectbox(
    "Ausgabesprache",
    ["Deutsch", "English", "Français", "Español", "Italiano", "Türkçe"],
    index=0,
    key="out_lang",
    help="Sprache der erzeugten Dokumentation.",
)

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
            result = generate_documentation(
                notes, doc_type, custom_instruction=custom_instruction, language=out_lang
            )
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

        case_label = st.session_state.get("case_label", "").strip()
        st.session_state["last_result"] = {
            "id": uuid.uuid4().hex[:8],
            "text": result.text,
            "doc_type": doc_type.key,
            "model": result.model,
            "elapsed": result.elapsed_s,
            "ts": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "truncated": result.truncated,
            "case_label": case_label,
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
            case_label=case_label,
        )
        st.toast("Dokumentation erstellt", icon="✅")

# --------------------------------------------------------------------------- #
# Ergebnis anzeigen (bleibt über Reruns erhalten)
# --------------------------------------------------------------------------- #
lr = st.session_state.get("last_result")
if lr:
    st.markdown("### Ergebnis")
    if lr.get("truncated"):
        note(
            "⚠️ <strong>Möglicherweise unvollständig:</strong> Die Ausgabe wurde an der "
            "Längengrenze abgeschnitten. Bitte auf Vollständigkeit prüfen – ggf. die "
            "Notizen kürzen oder die Dokumentation in Teilen erstellen.",
            kind="amber",
        )
    render_result_card(
        text=lr["text"],
        doc_type=DOC_TYPE_BY_KEY[lr["doc_type"]],
        model=lr["model"],
        elapsed_s=lr["elapsed"],
        created_ts=lr.get("ts"),
        case_label=lr.get("case_label", ""),
        key_prefix=lr["id"],
    )
