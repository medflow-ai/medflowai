"""Zentrale Konfiguration: Markendaten, Farbpalette, Dokumentationstypen, Beispiele.

Alles, was an mehreren Stellen gebraucht wird, lebt hier – so bleibt das UI
konsistent und Anpassungen (Branding, neue Dok-Typen) passieren an einer Stelle.
"""
from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Markendaten
# --------------------------------------------------------------------------- #
APP_NAME = "MedFlowAI"
APP_TAGLINE = "KI-gestützte medizinische Dokumentation"
APP_VERSION = "0.3.0"
SUPPORT_EMAIL = "support@medflowai.example"
COMPANY = "MedFlowAI"

# --------------------------------------------------------------------------- #
# Farbpalette – "Tiefes Navy + Akzent"
# --------------------------------------------------------------------------- #
NAVY_900 = "#0B1F3A"   # Sidebar / Kopfband
NAVY_800 = "#0F2A4D"
NAVY_700 = "#13355F"
ACCENT = "#14B8A6"     # Teal – Akzent / CTA
ACCENT_400 = "#2DD4BF"
ACCENT_SOFT = "#CCFBF1"
INK = "#0F172A"        # Haupttext (Slate-900)
MUTED = "#64748B"      # Sekundärtext (Slate-500)
LINE = "#E2E8F0"       # Trennlinien (Slate-200)
SURFACE = "#F8FAFC"    # Sehr helle Fläche (Slate-50)
SUCCESS = "#15803D"
WARNING = "#B45309"
DANGER = "#B91C1C"

# --------------------------------------------------------------------------- #
# Dokumentationstypen
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class DocType:
    key: str
    label: str
    icon: str
    short: str          # eine Zeile für die Auswahl
    description: str     # ausführlicher in der Info-Box


DOC_TYPES: list[DocType] = [
    DocType(
        key="verlauf",
        label="Verlaufsdokumentation",
        icon="📋",
        short="Knappe Verlaufsnotiz für die Patientenakte",
        description=(
            "Kompakte, chronologische Verlaufsnotiz für die Akte. "
            "Fokus auf Beschwerden, relevante Befunde und das weitere Vorgehen."
        ),
    ),
    DocType(
        key="soap",
        label="SOAP-Notiz",
        icon="🧾",
        short="Strukturiert nach Subjective / Objective / Assessment / Plan",
        description=(
            "Klassische SOAP-Struktur: Subjektiv (Angaben des Patienten), "
            "Objektiv (Befunde), Assessment (Einschätzung) und Plan."
        ),
    ),
    DocType(
        key="summary",
        label="Patientenzusammenfassung",
        icon="💬",
        short="Verständliche Zusammenfassung in einfacher Sprache",
        description=(
            "Laienverständliche Zusammenfassung für den Patienten – ohne "
            "Fachjargon, mit klaren nächsten Schritten."
        ),
    ),
    DocType(
        key="referral",
        label="Überweisungs-/Briefentwurf",
        icon="✉️",
        short="Entwurf für Arztbrief oder Überweisung",
        description=(
            "Strukturierter Entwurf für einen Arztbrief oder eine Überweisung "
            "(Anamnese, Befund, Fragestellung). Reiner Entwurf zur Prüfung."
        ),
    ),
    DocType(
        key="todo",
        label="To-do / weitere Abklärung",
        icon="✅",
        short="Offene Punkte und nächste Schritte als Liste",
        description=(
            "Liste offener Punkte und vorgeschlagener nächster Schritte zur "
            "Abklärung – als Checkliste fürs Praxisteam."
        ),
    ),
]

DOC_TYPE_BY_KEY = {d.key: d for d in DOC_TYPES}


# --------------------------------------------------------------------------- #
# Beispielanfragen (als Buttons, nicht im Eingabefeld vorbelegt)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Example:
    title: str
    text: str


EXAMPLES: list[Example] = [
    Example(
        title="Atemwegsinfekt",
        text=(
            "Patient berichtet über seit 3 Tagen bestehenden Husten, Fieber bis "
            "38,5 °C und allgemeine Schwäche. Keine Atemnot. Lunge auskultatorisch "
            "frei. Vorerkrankung: arterielle Hypertonie. Dauermedikation Ramipril 5 mg."
        ),
    ),
    Example(
        title="Rückenschmerz",
        text=(
            "Akut aufgetretener Schmerz im unteren Rücken seit gestern nach Heben "
            "einer Kiste. Ausstrahlung ins rechte Bein, kein Taubheitsgefühl, keine "
            "Blasen-/Mastdarmstörung. Lasègue rechts grenzwertig positiv."
        ),
    ),
    Example(
        title="Diabetes-Kontrolle",
        text=(
            "Routinekontrolle bei bekanntem Typ-2-Diabetes. HbA1c heute 7,8 %. "
            "Patient klagt über gelegentliches Kribbeln in den Füßen abends. "
            "Aktuelle Medikation Metformin 1000 mg 2x täglich. Gewicht stabil."
        ),
    ),
]

# Standardmodell (zentral, damit leicht austauschbar)
DEFAULT_MODEL = "gpt-4o-mini"
