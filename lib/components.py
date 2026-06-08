"""Wiederverwendbare UI-Bausteine: Ergebnis-Karte, Kopieren/Download, Feedback,
Beispiel-Buttons und der (session-basierte) Verlauf."""
from __future__ import annotations

import uuid
from datetime import datetime

import streamlit as st

from lib.config import DocType, EXAMPLES

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
# Ergebnis-Karte
# --------------------------------------------------------------------------- #
def _filename(doc_type: DocType, ext: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f"medflowai_{doc_type.key}_{stamp}.{ext}"


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

        # Aktionen
        c1, c2, c3 = st.columns([1.1, 1, 1])
        with c1:
            with st.popover("📋 Kopieren", use_container_width=True):
                st.caption("Mit dem Symbol oben rechts im Block kopieren:")
                st.code(text, language="markdown")
        with c2:
            st.download_button(
                "⬇️ Markdown",
                data=text,
                file_name=_filename(doc_type, "md"),
                mime="text/markdown",
                use_container_width=True,
                key=f"{key_prefix}_dl_md",
            )
        with c3:
            st.download_button(
                "⬇️ Text",
                data=text,
                file_name=_filename(doc_type, "txt"),
                mime="text/plain",
                use_container_width=True,
                key=f"{key_prefix}_dl_txt",
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
