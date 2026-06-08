# MedFlowAI – komplette Schritt-für-Schritt-Anleitung

Für Mac · mit **GitHub Desktop** · ganz ohne Terminal.
Arbeite die Teile **in dieser Reihenfolge** ab. Jeder Schritt sagt dir, worauf du
klickst und was du danach sehen solltest (👉).

Reihenfolge:
1. Alten OpenAI-Key sichern & neuen erstellen
2. Projekt mit GitHub Desktop veröffentlichen
3. App bei Streamlit Cloud online stellen
4. Key eintragen & testen
5. Altes Repo aufräumen

---

## Teil 1 · OpenAI-Key widerrufen und neuen erstellen

Warum zuerst: Dein alter Key lag möglicherweise im öffentlichen Code. Solche Keys
gelten als unsicher und sollten ersetzt werden.

1. Öffne **https://platform.openai.com/api-keys** und melde dich an.
   👉 Du siehst eine Liste „API keys".
2. Suche deinen alten Schlüssel in der Liste. Klick rechts in der Zeile auf das
   **Mülleimer-Symbol** (oder „⋯ → Revoke").
   👉 Ein Fenster „Revoke secret key?" erscheint → auf **Revoke key** klicken.
3. Jetzt einen neuen erstellen: Button **+ Create new secret key** (oben rechts).
   - Name: z. B. `MedFlowAI`
   - **Create secret key** klicken.
4. 👉 Der Schlüssel wird **nur jetzt einmal** angezeigt. Auf **Copy** klicken und
   ihn sofort sicher speichern (z. B. in einer Notiz). Er beginnt mit `sk-...`.
5. Prüfe, dass Guthaben da ist: links **Settings → Billing**. Falls leer, eine
   Zahlungsmethode hinzufügen und z. B. 5 $ aufladen.

✅ Du hast jetzt einen frischen, sicheren Key. Lege ihn beiseite – du brauchst ihn
in Teil 4.

---

## Teil 2 · Projekt mit GitHub Desktop veröffentlichen

> Hinweis: Falls die Dateien bereits in deinem geklonten `medflowai`-Ordner liegen
> (z. B. weil sie für dich hineinkopiert wurden), überspringe 2.1–2.2 und mache
> direkt bei **2.3 (Commit)** weiter.

Voraussetzung: Du bist in GitHub Desktop mit deinem GitHub-Konto angemeldet.
(Prüfen unter Menü **GitHub Desktop → Settings → Accounts**.)

### 2.1 Den Ordner als Repository hinzufügen
1. Oben im Menü auf **File → Add Local Repository…**
   ⚠️ *Nicht* „New Repository" – das würde einen leeren Ordner anlegen.
2. Im Fenster auf **Choose…** klicken → den Projektordner auswählen → **Open / Add**.
3. 👉 Falls der Hinweis *„This directory does not appear to be a Git repository"*
   erscheint → auf den blauen Link **„create a repository"** klicken.

### 2.2 Repository anlegen (nur falls nötig)
4. Im Fenster **„Create a Repository"**:
   - **Name:** `medflowai`
   - **Git Ignore:** auf **None** lassen (eine `.gitignore` ist schon dabei)
   - Klick auf **Create Repository**.

### 2.3 Ersten Commit machen
5. 👉 Links unter **Changes** erscheinen alle Dateien (app.py, lib, views …).
6. Unten links im Feld **Summary** eintippen: `Initial commit`
7. Klick auf den blauen Button **Commit to main**.
   👉 Die Dateiliste links wird leer – das ist richtig.

### 2.4 Auf GitHub hochladen
8. Oben auf **Push origin** (oder **Publish repository**, falls das Repo noch nicht
   online ist) klicken.
9. Bei „Publish": Name `medflowai`, **„Keep this code private" angehakt lassen**.
10. 👉 Mit **Repository → View on GitHub** im Browser kontrollieren – du solltest
    `app.py`, `lib/`, `views/`, `assets/` und `.streamlit/` sehen.

✅ Dein Projekt liegt jetzt sauber und privat auf GitHub.

---

## Teil 3 · App bei Streamlit Cloud online stellen

1. Öffne **https://share.streamlit.io**
2. **Sign in** → **Continue with GitHub** → den Zugriff bestätigen (**Authorize**).
   - 👉 Falls gefragt wird, ob Streamlit auch **private** Repos sehen darf:
     **erlauben** (sonst taucht dein `medflowai`-Repo später nicht auf).
3. Klick auf **Create app** (oben rechts).
4. Wähle die Option, eine App **aus einem bestehenden GitHub-Repo** zu starten.
5. Fülle die drei Felder aus:
   - **Repository:** `deinname/medflowai`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Klick auf **Deploy**.
   👉 Es läuft eine Installation (mehrere Minuten). Eine kurze Fehlermeldung wegen
   fehlendem Key ist hier **normal** – das beheben wir in Teil 4.

> Taucht dein Repo in der Liste nicht auf? Klick auf den Link zum Verwalten der
> GitHub-Berechtigungen („workspace permissions" / „Connect GitHub") und erlaube
> Zugriff auf private Repositories.

---

## Teil 4 · Key eintragen und testen

1. Bei deiner App in Streamlit Cloud oben rechts auf **⋮ (Menü) → Settings**.
2. Reiter **Secrets** öffnen.
3. Genau diese Zeile einfügen und deinen **neuen** Key aus Teil 1 einsetzen:

   ```toml
   OPENAI_API_KEY = "sk-dein-neuer-schluessel"
   ```

4. **Save** klicken. 👉 Die App startet automatisch neu.
5. Öffne die App-Adresse (z. B. `https://medflowai-xxxx.streamlit.app`).
6. **Test:** im Bereich *Dokumentation* ein Beispiel laden → Typ wählen →
   **Dokumentation erstellen**. 👉 Nach ein paar Sekunden erscheint die Ergebnis-Karte.

✅ Die App ist live und einsatzbereit.

---

## Teil 5 · Altes Repo aufräumen

Dein altes, öffentliches Repo mit den Test-Dateien wird nicht mehr gebraucht.

1. Gehe auf **https://github.com** und öffne das **alte** Repository.
2. Oben auf den Reiter **Settings** (im Repo, nicht dein Profil).
3. Ganz nach unten scrollen bis **Danger Zone**.
4. Klick auf **Delete this repository**.
5. 👉 Zur Bestätigung den Repo-Namen eintippen und bestätigen. Eventuell wird dein
   Passwort/2FA abgefragt.

✅ Damit sind die alten Test-Dateien und die alte Historie (inkl. evtl. altem Key)
endgültig weg.

---

## Wenn etwas klemmt

| Problem | Lösung |
|---|---|
| Repo fehlt in Streamlit Cloud | GitHub-Zugriff für **private** Repos erlauben (Teil 3, Hinweis-Kasten). |
| „Kein OpenAI-API-Key gefunden" | Teil 4 prüfen: `OPENAI_API_KEY` exakt geschrieben, Key in Anführungszeichen, gespeichert. |
| „Quota"/„Kontingent erschöpft" | Bei OpenAI Guthaben aufladen (Teil 1, Schritt 5). |
| App findet `app.py` nicht | In den App-Settings **Main file path** auf `app.py` stellen. |

---

## Später Änderungen am Code

Wenn du etwas am Projekt änderst: in GitHub Desktop links die Änderungen sehen →
**Summary** eintippen → **Commit to main** → oben **Push origin**. Streamlit Cloud
aktualisiert die App danach automatisch.

---

_Hinweis: MedFlowAI unterstützt nur bei der Dokumentation und stellt keine
Diagnosen. Vor dem Einsatz mit echten Patientendaten die Seite „Datenschutz &
Sicherheit" in der App beachten (AVV mit dem KI-Anbieter, möglichst EU-Verarbeitung)._
