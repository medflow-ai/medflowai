"""Export-Helfer: Dokumentation als PDF.

Bewusst ohne Streamlit-Abhängigkeit und ohne System-Bibliotheken (fpdf2 ist reines
Python), damit es auf Streamlit Cloud zuverlässig läuft. fpdf wird erst beim
Aufruf importiert – fehlt das Paket, gibt die Funktion None zurück und die UI
blendet den PDF-Button aus, statt abzustürzen.
"""
from __future__ import annotations

from datetime import datetime

# fpdf2 (Kernschrift Helvetica) kodiert Text als Latin-1. Deutsche Umlaute sind
# darin enthalten; einige typografische Sonderzeichen ersetzen wir vorher.
_REPLACEMENTS = {
    "–": "-", "—": "-",      # – —
    "‘": "'", "’": "'",      # ‘ ’
    "“": '"', "”": '"',      # “ ”
    "„": '"', "«": '"', "»": '"',
    "•": "-", "…": "...",    # • …
    " ": " ", "→": "->", "✅": "", "⚠": "",
}


def _latin1(text: str) -> str:
    for src, dst in _REPLACEMENTS.items():
        text = text.replace(src, dst)
    return text.encode("latin-1", "replace").decode("latin-1")


def markdown_to_pdf(text: str, title: str) -> bytes | None:
    """Rendert die (Markdown-)Dokumentation als schlichtes, lesbares PDF.

    Gibt die PDF-Bytes zurück oder None, falls fpdf nicht verfügbar ist.
    """
    try:
        from fpdf import FPDF
    except Exception:
        return None

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)
    pdf.add_page()

    # Titel
    pdf.set_font("Helvetica", "B", 15)
    pdf.multi_cell(0, 8, _latin1(title))
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 5, _latin1("Erstellt mit MedFlowAI · " + datetime.now().strftime("%d.%m.%Y %H:%M")))
    pdf.set_text_color(20, 20, 20)
    pdf.ln(3)

    # Inhalt – einfache Markdown-Behandlung (Überschriften fett, ** entfernen)
    for raw in text.split("\n"):
        line = raw.rstrip()
        if not line:
            pdf.ln(3)
            continue
        if line.startswith("###"):
            pdf.set_font("Helvetica", "B", 11)
            content = line.lstrip("# ").strip()
        elif line.startswith("##"):
            pdf.set_font("Helvetica", "B", 12)
            content = line.lstrip("# ").strip()
        elif line.startswith("#"):
            pdf.set_font("Helvetica", "B", 13)
            content = line.lstrip("# ").strip()
        else:
            pdf.set_font("Helvetica", "", 11)
            content = line
        content = content.replace("**", "")
        pdf.multi_cell(0, 6, _latin1(content))

    # Fußzeile / Disclaimer
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(
        0, 4,
        _latin1("Dokumentationsvorschlag - aerztlich auf Richtigkeit und "
                "Vollstaendigkeit zu pruefen. Keine Diagnose."),
    )

    output = pdf.output()
    return bytes(output)
