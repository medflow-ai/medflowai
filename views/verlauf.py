"""Verlauf der in DIESER Sitzung erstellten Dokumente (nicht persistent)."""
from __future__ import annotations

import streamlit as st

from lib.branding import note, page_header
from lib.components import clear_history, get_history

page_header(
    title="Verlauf",
    subtitle="Alle in dieser Sitzung erstellten Dokumentationen – an einem Ort.",
    eyebrow="Arbeitsbereich",
)

history = get_history()

note(
    "🔒 Der Verlauf wird <strong>nur in dieser Sitzung im Arbeitsspeicher</strong> "
    "gehalten und beim Schließen oder Neuladen der Seite automatisch gelöscht. "
    "Es findet keine dauerhafte Speicherung statt.",
    kind="teal",
)
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

if not history:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center; padding:24px 8px; color:#64748B;'>"
            "🗂️<br><br><strong>Noch kein Verlauf.</strong><br>"
            "Erstelle im Bereich <em>Dokumentation</em> dein erstes Dokument.</div>",
            unsafe_allow_html=True,
        )
    st.stop()

top = st.columns([3, 1])
with top[0]:
    st.caption(f"{len(history)} Dokument(e) in dieser Sitzung")
with top[1]:
    if st.button("Verlauf leeren", use_container_width=True):
        clear_history()
        st.rerun()

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

for item in history:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="mf-result-head">
              <span class="mf-tag">{item['doc_icon']} {item['doc_label']}</span>
              <span class="mf-meta">{item['ts']} · {item['output_words']} Wörter · {item['model']}</span>
            </div>
            <div class="mf-meta" style="margin-top:2px;">Eingabe: {item['input_preview']}</div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Dokumentation anzeigen"):
            st.markdown(item["text"])
            d1, d2 = st.columns(2)
            with d1:
                with st.popover("📋 Kopieren", use_container_width=True):
                    st.code(item["text"], language="markdown")
            with d2:
                st.download_button(
                    "⬇️ Markdown",
                    data=item["text"],
                    file_name=f"medflowai_{item['id'][:8]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key=f"hist_dl_{item['id']}",
                )
