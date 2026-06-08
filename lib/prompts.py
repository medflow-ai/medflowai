"""Prompt-Bausteine pro Dokumentationstyp.

Getrennt von der LLM-Logik, damit medizinische Vorgaben leicht überprüfbar und
versionierbar bleiben. Die Leitplanken (keine Diagnose, nur vorhandene Infos)
stehen sowohl im System- als auch im User-Prompt – doppelt hält besser.
"""
from __future__ import annotations

from lib.config import DocType

SYSTEM_PROMPT = (
    "Du bist ein sorgfältiger medizinischer Dokumentationsassistent für Arztpraxen "
    "im deutschsprachigen Raum. Deine einzige Aufgabe ist es, die vom Arzt "
    "eingegebenen Notizen zu strukturieren und sprachlich zu formulieren.\n\n"
    "Strikte Regeln:\n"
    "- Du stellst KEINE Diagnosen und triffst KEINE medizinischen Entscheidungen.\n"
    "- Du gibst keine eigenständigen Therapieanweisungen; du gibst nur das wieder, "
    "was der Arzt notiert hat.\n"
    "- Verwende ausschließlich Informationen aus den Notizen. Erfinde nichts und "
    "ergänze keine plausiblen, aber nicht genannten Befunde.\n"
    "- Was fehlt oder unklar ist, nennst du knapp unter 'Offene Punkte'.\n"
    "- Schreibe in deutscher medizinischer Fachsprache, präzise und verständlich.\n"
    "- Kompakt statt ausschweifend. Keine Einleitungs- oder Schlussfloskeln, "
    "keine Meta-Kommentare über dich selbst."
)

# Typ-spezifische Aufgabe + Zielstruktur
_TEMPLATES: dict[str, str] = {
    "verlauf": (
        "Erstelle eine kompakte Verlaufsdokumentation für die Patientenakte.\n"
        "Struktur:\n"
        "1. Anlass / Beschwerden\n"
        "2. Relevante Angaben & Befunde\n"
        "3. Einschätzung / mögliche Abklärung (nur als Notiz, keine Festlegung)\n"
        "4. Weiteres Vorgehen\n"
        "5. Offene Punkte"
    ),
    "soap": (
        "Erstelle eine strukturierte SOAP-Notiz.\n"
        "Struktur:\n"
        "**S – Subjektiv:** Angaben und Beschwerden des Patienten\n"
        "**O – Objektiv:** erhobene Befunde, Messwerte, Untersuchung\n"
        "**A – Assessment:** zusammenfassende Einschätzung (offen formuliert, "
        "keine endgültige Diagnose)\n"
        "**P – Plan:** geplantes Vorgehen / nächste Schritte\n"
        "Ergänze am Ende 'Offene Punkte', falls Angaben fehlen."
    ),
    "summary": (
        "Erstelle eine kurze, gut verständliche Zusammenfassung für den Patienten "
        "in einfacher Sprache (kein Fachjargon, kurze Sätze).\n"
        "Struktur:\n"
        "1. Was war der Grund des Besuchs?\n"
        "2. Was wurde besprochen / festgestellt?\n"
        "3. Was sind die nächsten Schritte für Sie?\n"
        "4. Wann sollten Sie sich wieder melden?\n"
        "Formuliere wertschätzend und beruhigend, ohne Versprechen zu machen."
    ),
    "referral": (
        "Erstelle den ENTWURF eines Arztbriefs bzw. einer Überweisung "
        "(klar als Entwurf zur ärztlichen Prüfung).\n"
        "Struktur:\n"
        "1. Anrede / Fragestellung an die mitbehandelnde Stelle\n"
        "2. Anamnese (Zusammenfassung)\n"
        "3. Aktuelle Befunde\n"
        "4. Bisheriges Vorgehen / Medikation\n"
        "5. Konkrete Fragestellung / Bitte um Mitbeurteilung\n"
        "6. Offene Punkte\n"
        "Verwende neutrale Platzhalter wie [Empfänger], [Datum], wenn Angaben fehlen."
    ),
    "todo": (
        "Leite aus den Notizen eine knappe To-do- / Abklärungsliste für das "
        "Praxisteam ab.\n"
        "Format:\n"
        "- Checkliste mit kurzen, konkreten Punkten (Was, ggf. von wem/bis wann, "
        "falls notiert)\n"
        "- Abschnitt 'Weitere Abklärung' für sinnvolle nächste diagnostische "
        "Schritte, die sich aus den Notizen ergeben (als Vorschlag, nicht als "
        "Anweisung)\n"
        "- Abschnitt 'Offene Punkte' für Fehlendes"
    ),
}


def build_messages(doc_type: DocType, notes: str) -> list[dict]:
    """Baut die Chat-Messages für die OpenAI-API."""
    task = _TEMPLATES.get(doc_type.key, _TEMPLATES["verlauf"])
    user_prompt = (
        f"AUFGABE: {task}\n\n"
        f"ARZT-NOTIZEN (einzige Informationsquelle):\n\"\"\"\n{notes.strip()}\n\"\"\"\n\n"
        "Halte dich exakt an die Struktur. Antworte direkt mit der Dokumentation."
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
