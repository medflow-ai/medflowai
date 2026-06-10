"""Wiederverwendbare UI-Bausteine: Ergebnis-Karte, Kopieren/Download, Feedback,
Beispiel-Buttons und der (session-basierte) Verlauf."""
from __future__ import annotations

import json
import uuid
from datetime import datetime

import streamlit as st

from lib.config import DOC_TYPES, DocType, EXAMPLES
from lib.export import markdown_to_pdf

NOTES_KEY = "notes_input"
HISTORY_KEY = "history"


# --------------------------------------------------------------------------- #
# Verlauf (nur in der Session – wird beim Neuladen gelöscht)
# --------------------------------------------------------------------------- #
def add_to_history(*, doc_type: DocType, text: str, model: str, elapsed_s: float,
                   input_preview: str, input_words: int, output_words: int) -> None:
    item = {
        "id": uuid.uuid4().hex,
        "ts": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "doc_label": doc_type.label,
        "doc_icon": doc_type.icon,
        "text": text,
        "model": model,
        "elapsed_s": elapsed_s,
        "input_preview": input_preview,
        "input_words": input_words,
        "output_words": output_words,
    }
    st.session_state.setdefault(HISTORY_KEY, []).insert(0, item)


def get_history() -> list[dict]:
    return st.session_state.get(HISTORY_KEY, [])


def clear_history() -> None:
    st.session_state[HISTORY_KEY] = []


# --------------------------------------------------------------------------- #
# Beispiel-Buttons (befüllen das Eingabefeld, statt es vorzubelegen)
# --------------------------------------------------------------------------- #
def _set_example(text: str) -> None:
    st.session_state[NOTES_KEY] = text


def example_buttons() -> None:
    st.caption("Beispiel laden:")
    cols = st.columns(len(EXAMPLES))
    for col, ex in zip(cols, EXAMPLES):
        with col:
            st.button(
                f"＋ {ex.title}",
                key=f"ex_{ex.title}",
                on_click=_set_example,
                args=(ex.text,),
                use_container_width=True,
            )


# --------------------------------------------------------------------------- #
# Voice-Input (Diktat → Transkription)
# --------------------------------------------------------------------------- #
_AUDIO_HASH_KEY = "last_audio_hash"


def voice_input() -> None:
    """Mikrofon-Aufnahme aufnehmen, per Whisper transkribieren und ins Notizfeld einfügen."""
    from lib.llm import ConfigError, LLMError, transcribe_audio

    with st.container(border=True):
        st.markdown(
            "<div style='font-weight:600;color:#0B1F3A;'>🎙️ Diktieren</div>"
            "<div style='color:#64748B;font-size:.85rem;margin-bottom:8px;'>"
            "Notizen einfach einsprechen – der Text wird automatisch unten eingefügt.</div>",
            unsafe_allow_html=True,
        )
        try:
            audio = st.audio_input("Aufnahme", label_visibility="collapsed", key="voice_audio")
        except Exception:
            st.caption("Spracheingabe wird von dieser Streamlit-Version nicht unterstützt.")
            return

    if audio is None:
        return
    try:
        data = audio.getvalue()
    except Exception:
        return
    if not data:
        return

    audio_id = hash(data)
    if st.session_state.get(_AUDIO_HASH_KEY) == audio_id:
        return  # diese Aufnahme wurde bereits transkribiert

    with st.spinner("Transkribiere Aufnahme …"):
        try:
            text = transcribe_audio(data)
        except (ConfigError, LLMError) as exc:
            st.session_state[_AUDIO_HASH_KEY] = audio_id  # nicht endlos neu versuchen
            st.error(str(exc))
            return

    st.session_state[_AUDIO_HASH_KEY] = audio_id
    if text:
        current = st.session_state.get(NOTES_KEY, "").strip()
        st.session_state[NOTES_KEY] = (current + ("\n" if current else "") + text).strip()
        st.toast("Transkription eingefügt", icon="✅")
        st.rerun()


# --------------------------------------------------------------------------- #
# Dokumentationstyp-Auswahl als Karten
# --------------------------------------------------------------------------- #
DOC_TYPE_IDX_KEY = "doc_type_idx"


def doc_type_selector() -> DocType:
    """Zeigt die Dokumentationstypen als auswählbare Karten und gibt den gewählten Typ zurück."""
    if DOC_TYPE_IDX_KEY not in st.session_state:
        st.session_state[DOC_TYPE_IDX_KEY] = 0
    selected = st.session_state[DOC_TYPE_IDX_KEY]

    per_row = 3
    for start in range(0, len(DOC_TYPES), per_row):
        cols = st.columns(per_row)
        for col_i in range(per_row):
            gi = start + col_i
            if gi >= len(DOC_TYPES):
                continue
            dt = DOC_TYPES[gi]
            is_sel = gi == selected
            with cols[col_i]:
                with st.container(border=True):
                    title_cls = "mf-doc-title sel" if is_sel else "mf-doc-title"
                    if is_sel:
                        check = "<div class='mf-doc-check'>✓ Ausgewählt</div>"
                    else:
                        check = "<div class='mf-doc-check' style='visibility:hidden'>•</div>"
                    st.markdown(
                        f"<div class='mf-doc-card'>"
                        f"<div class='mf-doc-icon'>{dt.icon}</div>"
                        f"<div class='{title_cls}'>{dt.label}</div>"
                        f"<div class='mf-doc-desc'>{dt.short}</div>"
                        f"{check}</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        "Ausgewählt" if is_sel else "Auswählen",
                        key=f"dtbtn_{dt.key}",
                        type="primary" if is_sel else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state[DOC_TYPE_IDX_KEY] = gi
                        st.rerun()
    return DOC_TYPES[st.session_state[DOC_TYPE_IDX_KEY]]


# --------------------------------------------------------------------------- #
# Ergebnis-Karte
# --------------------------------------------------------------------------- #
def _filename(doc_type: DocType, ext: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f"medflowai_{doc_type.key}_{stamp}.{ext}"


def copy_button(text: str, key: str = "cpy") -> None:
    """Echter Kopier-Button mit sichtbarem Erfolgs-Feedback (✓ Kopiert!)."""
    import streamlit.components.v1 as components

    safe = json.dumps(text)
    bid = f"cpy_{key}"
    html = f"""
    <button id="{bid}" style="width:100%;padding:11px 14px;border:none;
        border-radius:12px;background:#14B8A6;color:#fff;font-weight:600;
        font-size:14px;cursor:pointer;box-shadow:0 6px 16px rgba(20,184,166,.25);
        font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
        transition:background .15s ease;">📋 In Zwischenablage kopieren</button>
    <script>
    (function() {{
      const b = document.getElementById("{bid}");
      const label = "📋 In Zwischenablage kopieren";
      b.addEventListener("click", async () => {{
        try {{
          await navigator.clipboard.writeText({safe});
          b.textContent = "✓ Kopiert!";
          b.style.background = "#15803D";
          setTimeout(() => {{ b.textContent = label; b.style.background = "#14B8A6"; }}, 1800);
        }} catch (e) {{
          b.textContent = "Bitte Text oben manuell markieren & kopieren";
          b.style.background = "#B45309";
        }}
      }});
    }})();
    </script>
    """
    components.html(html, height=54)


def render_result_card(
    *,
    text: str,
    doc_type: DocType,
    model: str,
    elapsed_s: float,
    key_prefix: str = "res",
    show_feedback: bool = True,
) -> None:
    """Rendert die Dokumentation als Karte mit Kopier-/Download-Aktionen."""
    words = len(text.split())
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")

    with st.container(border=True):
        # Kopfzeile
        st.markdown(
            f"""
            <div class="mf-result-head">
              <span class="mf-tag">{doc_type.icon} {doc_type.label}</span>
              <span class="mf-meta">{ts} · {words} Wörter · {model} · {elapsed_s:.1f}s</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Inhalt (echtes Markdown-Rendering)
        st.markdown(text)

        st.divider()

        # Kopieren – mit sichtbarem Erfolgs-Feedback
        copy_button(text, key=key_prefix)

        # Export: Markdown · Text · PDF
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "⬇️ Markdown",
                data=text,
                file_name=_filename(doc_type, "md"),
                mime="text/markdown",
                use_container_width=True,
                key=f"{key_prefix}_dl_md",
            )
        with c2:
            st.download_button(
                "⬇️ Text",
                data=text,
                file_name=_filename(doc_type, "txt"),
                mime="text/plain",
                use_container_width=True,
                key=f"{key_prefix}_dl_txt",
            )
        with c3:
            pdf_bytes = markdown_to_pdf(text, doc_type.label)
            if pdf_bytes:
                st.download_button(
                    "⬇️ PDF",
                    data=pdf_bytes,
                    file_name=_filename(doc_type, "pdf"),
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"{key_prefix}_dl_pdf",
                )
            else:
                st.button(
                    "⬇️ PDF",
                    disabled=True,
                    use_container_width=True,
                    key=f"{key_prefix}_pdf_off",
                    help="PDF-Export wird nach dem nächsten Deploy verfügbar.",
                )

        # Pflichthinweis direkt am Ergebnis
        st.markdown(
            '<div class="mf-note amber" style="margin-top:10px;">'
            "⚠️ <strong>Vorschlag zur Dokumentation.</strong> Vor Übernahme in die "
            "Akte ärztlich auf Richtigkeit und Vollständigkeit prüfen.</div>",
            unsafe_allow_html=True,
        )

        if show_feedback:
            _feedback_row(key_prefix)


def _feedback_row(key_prefix: str) -> None:
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    fc1, fc2 = st.columns([1, 3])
    with fc1:
        st.caption("War das hilfreich?")
        try:
            rating = st.feedback("thumbs", key=f"{key_prefix}_fb")
        except Exception:
            rating = None
    if rating is not None:
        with fc2:
            st.caption("Danke! Dein Feedback hilft, MedFlowAI zu verbessern.")
