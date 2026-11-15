# east-westflying.de

Statische Webseite von East-Westflying. Kein WordPress, keine Datenbank, keine Plugins.

## Wo was liegt

| Ordner | Inhalt |
|---|---|
| `src/pages/` | Inhalt der einzelnen Seiten (Texte stehen direkt im HTML) |
| `src/partials/` | Kopfbereich, Menü und Fußbereich, gilt für alle Seiten |
| `assets/css/site.css` | Farben, Schriften, Abstände für die ganze Seite |
| `assets/img/` | Bilder |
| `tools/bilder.txt` | Liste der Bilder, die GitHub automatisch von einer Adresse holt |
| `build.py` | Setzt die Seiten zusammen |

## Text ändern

Datei in `src/pages/` öffnen, Text ersetzen, speichern. Die Adressen der Seiten (`slug`) und die Titel für Google stehen oben in `build.py`.

## Seite bauen

```
python3 build.py live      # fertige Seite in dist/live
python3 build.py preview   # Vorschau mit relativen Links in dist/preview
```

`dist/` wird nicht gespeichert, der Server baut die Seite selbst.

## Neue Seite

1. Datei in `src/pages/` anlegen.
2. In `build.py` unter `PAGES` eintragen (Adresse, Titel, Beschreibung).
3. Links auf noch nicht umgezogene Seiten zeigen automatisch auf die bisherige Seite.

## Server

Hetzner Cloud, Falkenstein. Der Server holt sich alle zwei Minuten den neuesten Stand aus diesem Repository (`server/update.sh`), baut die Seite und schaltet sie live. Webserver-Einstellungen stehen in `server/Caddyfile` und werden ebenfalls automatisch übernommen. Die Ersteinrichtung des Servers steht in `server/cloud-init.yaml`.

Welcher Stand gerade live ist, steht unter `/version.txt` (Commit und Uhrzeit, UTC).
