# MedFlowAI

KI-gestützte **medizinische Dokumentation** für Hausärzt:innen, Fachärzt:innen,
Praxen und MVZ. Aus knappen Notizen oder Gesprächsinhalten entsteht strukturierte,
prüfbare Dokumentation. **Keine Diagnosen, keine medizinischen Entscheidungen** –
ausschließlich Dokumentationsunterstützung.

---

## Schnellstart

```bash
pip install -r requirements.txt

# Key hinterlegen:
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
#   → OPENAI_API_KEY eintragen

streamlit run app.py
```

In der **Streamlit Cloud**: Repo verbinden, unter *Settings → Secrets* den
`OPENAI_API_KEY` setzen. Einstiegsdatei: `app.py`.

---

## Architektur

Echte Multipage-App über `st.navigation`. Die Logik liegt in `lib/`, die Seiten in
`views/` – so bleibt jede Seite schlank und konsistent.

```
medflowai/
├── app.py                  # Einstieg: Navigation, Branding, Logo
├── views/
│   ├── dokumentation.py    # Kern: Notizen → Dokumentation
│   ├── verlauf.py          # Session-Verlauf (nicht persistent)
│   ├── datenschutz.py      # Datenfluss, Audit-Opt-in, Checkliste
│   └── ueber.py            # Positionierung, Grenzen, Impressum
├── lib/
│   ├── config.py           # Marke, Farben, Dok-Typen, Beispiele
│   ├── branding.py         # CSS-Theme, Hero, Sidebar, Bausteine
│   ├── llm.py              # OpenAI-Anbindung + Fehlerbehandlung
│   ├── prompts.py          # Prompt je Dokumentationstyp
│   ├── audit.py            # pseudonymisiertes Opt-in-Audit (nur Metadaten)
│   └── components.py       # Ergebnis-Karte, Kopieren/Download, Verlauf
├── assets/                 # Logo (SVG)
├── .streamlit/
│   ├── config.toml         # Navy-Theme
│   └── secrets.toml.example
└── requirements.txt
```

---

## Was sich gegenüber dem MVP geändert hat

| Bereich | Vorher | Jetzt |
|---|---|---|
| Datenschutz | Patiententext **im Klartext** in `access_log.json` | **Kein** Patiententext gespeichert; nur **Opt-in-Metadaten** |
| Robustheit | API-Key beim Import → App-Crash; kein `try/except` | Key-Check ohne Crash; verständliche Fehlermeldungen |
| Optik | Streamlit-Default + Emoji | Navy-SaaS-Theme, Logo, Karten, Farbhierarchie |
| Navigation | eine Seite | gruppierte Sidebar (Arbeitsbereich / Information) |
| Ergebnis | roher `st.write`-Text | Karte mit Kopieren + Download (.md/.txt) |
| Eingabe | Beispiel im Feld vorbelegt | Beispiel-Buttons; bessere Typ-Auswahl mit Beschreibung |
| Vertrauen | knapper Caption-Disclaimer | klare Positionierung (kein Diagnose-Ersatz, kein Medizinprodukt), DSGVO-Hinweise |
| Feedback/Laden | Default-Spinner | Status-Animation, Feedback-Button, responsives Layout |

---

## Datenschutz (Kurzfassung)

- Eingaben gehen zur Verarbeitung an die **OpenAI-API** (Auftragsverarbeiter, ggf.
  außerhalb der EU). **Patiententext wird serverseitig nicht gespeichert.**
- Das **Audit-Log** ist standardmäßig **aus** und erfasst – wenn aktiviert – nur
  Metadaten (Zeit, Typ, Längen, nicht umkehrbarer Fingerprint).
- Vor dem Praxiseinsatz mit echten Daten: **AVV**, möglichst **EU-Region** und
  **Zero Data Retention** beim KI-Anbieter (z. B. Azure OpenAI EU).
- Hinweise sind technischer Natur und **kein Rechtsrat**.

---

## Roadmap

**Medium**
- Authentifizierung (Praxis-Accounts, Rollen, Mandantentrennung)
- EU-konformer LLM-Pfad (Azure OpenAI EU / Zero-Retention, AVV)
- Verschlüsselter, persistenter Verlauf pro Nutzer (DB statt Session)
- Export/Integration: GDT, HL7/FHIR, Anbindung an PVS
- Praxiseigene Vorlagen, fachrichtungsspezifische Dokumenttypen

**Low**
- Dark-Mode-Toggle, Onboarding-Tour, Tastenkürzel
- Aggregiertes (anonymes) Nutzungs-Dashboard
- A/B-Tests von Prompts

---

_MedFlowAI ist ein Dokumentations-Hilfswerkzeug. Jede Ausgabe ist ein Vorschlag und
muss ärztlich geprüft werden._
