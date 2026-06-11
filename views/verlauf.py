"""Verlauf der in DIESER Sitzung erstellten Dokumente – Timeline mit Suche.

Weiterhin ausschließlich Session-Speicher: wird beim Neuladen automatisch gelöscht.
"""
from __future__ import annotations

import html

import streamlit as st

from lib.branding import note, page_header
from lib.components import clear_history, copy_button, get_history
from lib.export import markdown_to_pdf

page_header(
    title="Verlauf",
    subtitle="Alle in dieser Sitzung erstellten Dokumentationen – als durchsuchbare Zeitleiste.",
    eyebrow="Arbeitsbereich",
)

history = get_history()

note(
    "🔒 Der Verlauf wird <strong>nur in dieser Sitzung im Arbeitsspeicher</strong> "
    "gehalten und beim Schließen oder Neuladen automatisch gelöscht. "
    "Es findet keine dauerhafte Speicherung statt.",
    kind="teal",
)
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# --------------------------------------------------------------------------- #
# Leerer Zustand
# --------------------------------------------------------------------------- #
if not history:
    with st.container(border=True):
        st.markdown(
            "<div style='text-align:center; padding:28px 8px; color:#64748B;'>"
            "<div style='font-size:2rem;'>🗂️</div>"
            "<div style='font-weight:700; color:#0B1F3A; margin-top:8px;'>Noch kein Verlauf</div>"
            "<div style='margin-top:4px;'>Erstelle im Bereich <em>Dokumentation</em> dein erstes Dokument – "
            "es erscheint dann hier.</div></div>",
            unsafe_allow_html=True,
        )
    st.stop()

# --------------------------------------------------------------------------- #
# Werkzeugleiste: Suche + Leeren
# --------------------------------------------------------------------------- #
t1, t2 = st.columns([3, 1])
with t1:
    query = st.text_input(
        "Suche",
        placeholder="🔍  Verlauf durchsuchen (Typ, Inhalt …)",
        label_visibility="collapsed",
        key="hist_search",
    )
with t2:
    if st.button("Verlauf leeren", use_container_width=True):
        clear_history()
        st.session_state.pop("hist_search", None)
        st.rerun()

q = (query or "").strip().lower()


def _matches(item: dict) -> bool:
    if not q:
        return True
    haystack = (
        f"{item.get('case_label', '')} {item['doc_label']} "
        f"{item.get('input_preview', '')} {item['text']}"
    ).lower()
    return q in haystack


filtered = [it for it in history if _matches(it)]
st.caption(f"{len(filtered)} von {len(history)} Einträgen")
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

if not filtered:
    note("Keine Treffer für deine Suche. Versuch einen anderen Begriff.", kind="")
    st.stop()

# --------------------------------------------------------------------------- #
# Timeline
# --------------------------------------------------------------------------- #
for item in filtered:
    case_chip = (
        f"<span class='mf-tag gray'>🏷️ {html.escape(item['case_label'])}</span>"
        if item.get("case_label") else ""
    )
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
              <span style="width:10px; height:10px; border-radius:50%; background:#14B8A6;
                box-shadow:0 0 0 4px rgba(20,184,166,.15); display:inline-block;"></span>
              {case_chip}
              <span class="mf-tag">{item['doc_icon']} {item['doc_label']}</span>
              <span class="mf-meta">{item['ts']} · {item['output_words']} Wörter · {item['model']}</span>
            </div>
            <div class="mf-meta" style="margin-top:7px;">{html.escape(item['input_preview'])}</div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("Dokumentation anzeigen"):
            st.markdown(item["text"])
            st.divider()
            copy_button(item["text"], key=item["id"])
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button(
                    "⬇️ Markdown",
                    data=item["text"],
                    file_name=f"medflowai_{item['id'][:8]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                    key=f"hist_md_{item['id']}",
                )
            with c2:
                st.download_button(
                    "⬇️ Text",
                    data=item["text"],
                    file_name=f"medflowai_{item['id'][:8]}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"hist_txt_{item['id']}",
                )
            with c3:
                pdf_bytes = markdown_to_pdf(item["text"], item["doc_label"])
                if pdf_bytes:
                    st.download_button(
                        "⬇️ PDF",
                        data=pdf_bytes,
                        file_name=f"medflowai_{item['id'][:8]}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key=f"hist_pdf_{item['id']}",
                    )
                else:
                    st.button(
                        "⬇️ PDF",
                        disabled=True,
                        use_container_width=True,
                        key=f"hist_pdf_off_{item['id']}",
                        help="PDF-Export gerade nicht verfügbar.",
                    )
