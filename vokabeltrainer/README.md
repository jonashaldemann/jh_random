# Parole in Palestra 🇮🇹

Ein Italienisch-Vokabeltrainer (Italienisch ↔ Deutsch) mit drei Übungsmodi
(Tippen, Multiple Choice, Rückwärts) und Kategorie-Filtern.

## Projektstruktur

```
├── index.html              Grundgerüst (HTML) – lädt CSS/JS extern
├── css/
│   └── style.css           Gesamtes Styling
├── js/
│   └── app.js               App-Logik (lädt die JSON-Daten per fetch())
└── data/
    ├── vocabulary.json      Nomen, Verben, Adjektive, Phrasen
    └── konjugation.json     Konjugationstabellen (getrennt, wie gewünscht)
```

Die Wortdaten liegen nicht mehr im Code, sondern in zwei JSON-Dateien unter
`data/`. `js/app.js` lädt beide beim Start per `fetch()` und führt sie zu
`ALL_WORDS` zusammen. Neue Vokabeln oder Konjugationen hinzufügen heißt also:
einfach die passende JSON-Datei erweitern, kein Codeeditieren nötig.

### Format `vocabulary.json`
```json
{ "it": "la casa", "de": "das Haus", "cat": "nomen" }
```

### Format `konjugation.json`
```json
{
  "it": "io vedrei",
  "de": "ich würde sehen",
  "cat": "konjugation",
  "hint": "vedere · Condizionale presente"
}
```
`cat` steuert die Filter-Buttons (`nomen`, `verben`, `adjektive`, `phrasen`,
`konjugation`). `hint` ist optional und wird unter der Frage angezeigt.

## Lokal testen

Da `app.js` die JSON-Dateien per `fetch()` lädt, funktioniert das **nicht**,
wenn man `index.html` einfach per Doppelklick im Browser öffnet
(`file://`-URLs blockieren `fetch` aus CORS-Gründen). Stattdessen lokal einen
simplen Webserver starten, z. B.:

```bash
cd vokabeltrainer
python3 -m http.server 8080
# dann im Browser: http://localhost:8080
```

oder mit Node (`npx serve`), oder die VS-Code-Erweiterung "Live Server".

## Veröffentlichen auf GitHub Pages

1. Neues Repository auf GitHub anlegen (z. B. `parole-in-palestra`).
2. Diesen Ordnerinhalt hochladen/pushen:
   ```bash
   git init
   git add .
   git commit -m "Vokabeltrainer: Initial commit"
   git branch -M main
   git remote add origin https://github.com/<dein-user>/parole-in-palestra.git
   git push -u origin main
   ```
3. Im Repository unter **Settings → Pages**:
   - **Source**: „Deploy from a branch“
   - **Branch**: `main`, Ordner `/ (root)`
   - Speichern.
4. Nach ein bis zwei Minuten ist die Seite erreichbar unter:
   `https://<dein-user>.github.io/parole-in-palestra/`

GitHub Pages liefert die Dateien über HTTPS aus einer echten Domain aus,
daher funktioniert `fetch('data/vocabulary.json')` dort ohne weitere
Konfiguration.

## Weitere Vokabeln/Konjugationen ergänzen

Einfach ein neues Objekt in die passende JSON-Datei einfügen, z. B. in
`data/vocabulary.json`:
```json
{ "it": "il gatto", "de": "die Katze", "cat": "nomen" }
```
oder eine neue Verbtabelle in `data/konjugation.json` nach demselben Muster
wie die bestehenden Einträge (6 Formen pro Zeitform, mit `hint`).
