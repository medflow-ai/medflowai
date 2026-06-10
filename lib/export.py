"""Export-Helfer: Dokumentation als PDF.

Bewusst ohne Streamlit-Abhängigkeit und ohne System-Bibliotheken (fpdf2 ist reines
Python), damit es auf Streamlit Cloud zuverlässig läuft. Schlägt die PDF-Erzeugung
aus irgendeinem Grund fehl, gibt die Funktion None zurück und die UI blendet den
PDF-Button aus, statt die App abstürzen zu lassen.
"""
from __future__ import annotations

from datetime import datetime

# fpdf2 (Kernschrift Helvetica) kodiert Text als Latin-1. Deutsche Umlaute sind
# darin enthalten; einige typografische Sonderzeichen ersetzen wir vorher.
_REPLACEMENTS = {
    "–": "-", "—": "-",
    "‘": "'", "’": "'",
    "“": '"', "”": '"', "„": '"', "«": '"', "»": '"',
    "•": "-", "…": "...",
    "·": "-", " ": " ", "→": "->", "✅": "", "⚠": "", "️": "",
}


def _latin1(text: str) -> str:
    for src, dst in _REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


def markdown_to_pdf(text: str, title: str) -> bytes | None:
    """Rendert die (Markdown-)Dokumentation als schlichtes, lesbares PDF.

    Gibt die PDF-Bytes zurück oder None, falls fpdf fehlt oder die Erzeugung
    fehlschlägt (die App stürzt dadurch nie ab). Das Caching erfolgt bewusst pro
    Sitzung in components.get_pdf (st.session_state) statt prozessweit – so bleibt
    kein Patiententext über Sitzungen hinweg im Serverspeicher.
    """
    try:
        from fpdf import FPDF

        # Jede Zeile beginnt wieder am linken Rand und rückt nach unten,
        # damit immer die volle Breite verfügbar ist.
        def line(txt: str, size: int, bold: bool = False, italic: bool = False,
                 gray: bool = False, height: float = 6.0):
            style = ("B" if bold else "") + ("I" if italic else "")
            pdf.set_font("Helvetica", style, size)
            pdf.set_text_color(120, 120, 120) if gray else pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, height, _latin1(txt), new_x="LMARGIN", new_y="NEXT")

        pdf = FPDF(format="A4")
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.set_margins(18, 16, 18)
        pdf.add_page()

        line(title, 15, bold=True, height=8)
        line("Erstellt mit MedFlowAI - " + datetime.now().strftime("%d.%m.%Y %H:%M"),
             9, gray=True, height=5)
        pdf.ln(3)

        for raw in text.split("\n"):
            content = raw.rstrip()
            if not content:
                pdf.ln(3)
                continue
            if content.startswith("###"):
                line(content.lstrip("# ").strip().replace("**", ""), 11, bold=True)
            elif content.startswith("##"):
                line(content.lstrip("# ").strip().replace("**", ""), 12, bold=True)
            elif content.startswith("#"):
                line(content.lstrip("# ").strip().replace("**", ""), 13, bold=True)
            else:
                line(content.replace("**", ""), 11)

        pdf.ln(4)
        line("Dokumentationsvorschlag - aerztlich auf Richtigkeit und "
             "Vollstaendigkeit zu pruefen. Keine Diagnose.",
             8, italic=True, gray=True, height=4)

        return bytes(pdf.output())
    except Exception:
        return None
