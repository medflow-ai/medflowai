# Wettbewerbsvergleich: MedFlowAI vs. Heidi Health

_Stand: 11.06.2026 · Quellen: heidihealth.com/de-de (Startseite, Lösungen/Allgemeinmedizin, Preise)_

## Kurzfazit

Heidi ist kein reines Dokumentations-Tool mehr, sondern eine **Plattform**:
Ambient-Scribe (nimmt das ganze Gespräch auf) + Vorlagen-Ökosystem + klinische
Wissensdatenbank („Evidenz") + Konten/Teams/Integrationen + breite Zertifizierungen.

MedFlowAI macht den **Kern** (Notiz → strukturierte Dokumentation) sauber und ist
beim **Datenschutz-by-default** und der klaren „kein Medizinprodukt"-Positionierung
sogar konservativer. Die Lücke liegt v. a. in **Funktionsumfang** und **Reife**
(Authentifizierung, Integrationen, Compliance-Nachweise).

## Funktionsvergleich

| Bereich | Heidi | MedFlowAI (aktuell) |
|---|---|---|
| Spracherfassung | Ambient-Aufnahme des ganzen Gesprächs, online + offline, 110+ Sprachen | Push-to-Diktat → Whisper, Deutsch |
| Dokumentarten | Viele + eigene & geteilte Vorlagen (Community) | 5 → **jetzt 8 + eigene Vorlage** |
| Wissens-/Evidenzmodul | „Evidenz"/Frag Heidi mit Quellenangaben (BMJ, MIMS …) | bewusst nicht (Doku-Fokus, kein Medizinprodukt) |
| Patienten-/Sitzungsbezug | Verknüpfung + Sitzungsstatus, persistent | Session-Verlauf (nicht persistent) |
| Abrechnung | Abrechnungscode-Vorschläge | – |
| Integrationen | PVS/EHR-Integrationen (Add-on) | – (Export MD/Text/PDF) |
| Konten/Teams | Login, Teams, SSO, zentrale Abrechnung | – (eine öffentliche App) |
| Compliance | SOC 2, ISO 27001/42001, HIPAA, NHS, DSGVO, Trust Center | Datensparsamkeit, kein PHI-Storage, Opt-in-Audit |
| Plattform | Native Apps, eigenes Hosting, individuelle Aufbewahrung | Streamlit Cloud |
| Geschäftsmodell | Free / Evidenz Pro / Premium / Enterprise | – |

## Was wir gleich gut / besser machen

Sauberer Notiz→Doku-Kern (SOAP/Verlauf/Überweisung), Diktat→Transkription, Export
(MD/Text/PDF) mit Copy-Feedback, durchsuchbarer Verlauf, modernes Design,
Dark-/Kompakt-/Großschrift-Modus. Beim Datenschutz strenger: **kein Patiententext
serverseitig gespeichert**, pseudonymisiertes Opt-in-Audit, explizite
„kein Diagnose-Ersatz / kein Medizinprodukt"-Haltung.

## Übernahme-Plan (priorisiert)

**Schnell & wertvoll**

1. ✅ Eigene Vorlagen (freie Struktur pro Dokument) — _umgesetzt in dieser Phase_
2. ✅ Mehr Dokumentarten: Behandlungsplan, Gesprächszusammenfassung, Verlaufskontrolle — _umgesetzt_
3. Ausgabesprache wählbar
4. Pseudonymes Fall-Label im Verlauf

**Mittel**

5. Abrechnungscode-Vorschläge (ICD-10/GOÄ/EBM) — als „Vorschlag, ärztlich zu prüfen"
6. Längere/Ambient-Aufnahme („Gespräch aufnehmen")
7. Trust-/Compliance-Seite (Sub-Auftragsverarbeiter, Aufbewahrung, AVV-Status)

**Strategisch (Infrastruktur nötig)**

8. Konten/Anmeldung → persistenter, verschlüsselter Verlauf, Teams
9. PVS-Export (GDT/HL7/FHIR)
10. EU-konformer KI-Pfad (Azure OpenAI EU + AVV), perspektivisch Zertifizierungen

## Bewusst NICHT 1:1 kopieren

- **„Evidenz"/klinische Antworten**: verlässt die Doku-Nische Richtung
  Entscheidungsunterstützung → könnte die App regulatorisch zum **Medizinprodukt**
  machen. Vorerst fokussiert bleiben.
- **Compliance-Logos** (SOC2/ISO/HIPAA) erst zeigen, wenn tatsächlich erworben.
