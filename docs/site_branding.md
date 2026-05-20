# Site Branding

Ermöglicht umgebungsabhängiges CSS und ein optisches Badge im Frappe-Desk,
basierend auf der Browser-URL zur Laufzeit – unabhängig vom internen Frappe-Site-Namen.

## Funktionsprinzip

1. Beim Laden des Desk ruft `site_branding.js` die aktiven Regeln per `frappe.call` ab.
2. Clientseitig wird die **erste passende Regel** (kleinste `priority`-Zahl) angewendet.
3. Das Custom-CSS wird als `<style id="site-branding-dynamic-css">` in den `<head>` injiziert.
4. Optional wird ein Badge (`<div id="site-branding-badge">`) im `<body>` angezeigt.

Da die Erkennung im Browser über `window.location.hostname` / `window.location.href`
erfolgt, funktioniert das auch nach einem PROD→STAGE-Datenbankimport korrekt, solange
in der Datenbank eine Regel für die STAGE-Domain vorhanden ist.

---

## DocType: Site Branding Rule

Pfad: **Site Branding > Site Branding Rule**  
Zugriff: nur **System Manager**

| Feld | Typ | Beschreibung |
|---|---|---|
| `enabled` | Check | Regel aktiv/inaktiv |
| `rule_name` | Data | Eindeutiger Name (wird zum Dokument-ID) |
| `match_type` | Select | Matching-Strategie (s. u.) |
| `match_value` | Data | Wert, gegen den gematcht wird |
| `priority` | Int | Niedrigere Zahl = höhere Priorität (Standard: 100) |
| `css` | Code (CSS) | CSS-Code, der bei Match angewendet wird |
| `badge_enabled` | Check | Badge anzeigen |
| `badge_text` | Data | Text im Badge, z. B. `STAGE` |
| `badge_position` | Select | `Top Right` / `Top Left` / `Bottom Right` / `Bottom Left` |
| `badge_color` | Data | Hintergrundfarbe als Hex, z. B. `#ff9800` |
| `badge_text_color` | Data | Textfarbe als Hex, z. B. `#ffffff` |
| `notes` | Small Text | Interne Notizen |

### Match-Typen

| Typ | Bedingung |
|---|---|
| `Host Equals` | `window.location.hostname === match_value` |
| `Host Contains` | `window.location.hostname` enthält `match_value` |
| `URL Contains` | `window.location.href` enthält `match_value` |
| `Regex` | Regulärer Ausdruck gegen `window.location.href` |

### Priorität

Mehrere Regeln können gleichzeitig in der DB existieren. Nur die Regel mit der
**kleinsten `priority`-Zahl** wird angewendet. Bei Gleichstand gewinnt die, die
zuerst zurückgegeben wird (alphabetisch nach `name`).

---

## Beispiel-Regeln

### STAGE – Host Contains

```
rule_name:    STAGE Environment
enabled:      ✓
match_type:   Host Contains
match_value:  stage
priority:     10
css:
  body { background-color: #fff7e6 !important; }
  .navbar, .desk-sidebar { border-top: 4px solid #ff9800 !important; }
badge_enabled:    ✓
badge_text:       STAGE
badge_position:   Top Right
badge_color:      #ff9800
badge_text_color: #ffffff
```

### TEST – URL Contains

```
rule_name:    TEST Environment
match_type:   URL Contains
match_value:  test.
priority:     20
badge_enabled:    ✓
badge_text:       TEST
badge_color:      #2196f3
badge_text_color: #ffffff
```

### DEV – Regex

```
rule_name:    Local DEV
match_type:   Regex
match_value:  ^https?://(localhost|127\.0\.0\.1)
priority:     1
css:
  body::before {
    content: "LOCAL DEV";
    display: block;
    background: #f44336;
    color: #fff;
    text-align: center;
    padding: 4px;
    font-weight: bold;
  }
badge_enabled:    ✓
badge_text:       DEV
badge_color:      #f44336
badge_text_color: #ffffff
```

---

## Deployment

Nach jeder Änderung am Code folgende Bench-Befehle ausführen:

```bash
# DocType in der DB anlegen / migrieren
bench --site <site-name> migrate

# JavaScript-Assets neu bauen
bench build --app vepro_app

# Frappe-Server neu starten
bench restart
```

Nur bei reinen CSS/Badge-Änderungen in bestehenden Regeln (keine Code-Änderungen)
reicht ein einfacher Browser-Reload.

---

## Verhalten bei Nicht-Übereinstimmung

Wenn keine Regel auf die aktuelle URL passt:
- kein `<style>` wird eingefügt
- kein Badge wird angezeigt
- das System verhält sich vollständig normal
- Fehler im API-Call werden still abgefangen und verursachen keine UI-Störung

---

## API-Endpunkt

```
POST /api/method/vepro_app.site_branding.api.get_branding_rules
```

Gibt alle aktiven Regeln (sortiert nach `priority ASC`) zurück.
Zugriff: jeder eingeloggte Desk-Benutzer (kein System Manager erforderlich).

Rückgabe-Felder: `name`, `rule_name`, `match_type`, `match_value`, `priority`,
`css`, `badge_text`, `badge_enabled`, `badge_position`, `badge_color`, `badge_text_color`.
