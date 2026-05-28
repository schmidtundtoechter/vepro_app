### vepro_app

Diese App wurde für VEPRO geschrieben. 
Sie dienst als Ergänzung zu ERPNext 15 und soll alle UI Veränderungen am System beinhalten. 

Die drei wichtigsten Branches sind: 
main:      Hier findet man den komplett durchgetesteten und funktionierenden Code.
staging:   Code der durch SUT getestet wurde. Es muss noch durch VEPPRO selbst zur Migration in den Main-Branch freigegeben werden.
develop:   Code im Zwischenstadium befindet sich hier oder im passenden Feature Branch.

### Anpassungen

#### DocTypes (neu eingeführt)

| DocType | Typ | Beschreibung |
|---|---|---|
| `Produkte` | Child Table | Produktliste; wird im DocType „Kunde" als Tabelle eingebettet |
| `Abteilungstyp` | Stammdaten | Auswahlliste für Abteilungen; wird im DocType „Kontakt" als Link-Feld verwendet |
| `Supportvertrag` | Stammdaten | Supportvertrags-Typen (`24/7`, `+3h`, `Standard`, `kein Supportvertrag`); wird im DocType „Kunde" als Link-Feld verwendet |

#### Custom Fields

**DocType: Kunde (`Customer`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_section_break_8lhrp` | Section Break | nach `image` | Abschnittswechsel „Produkttabelle" |
| `custom_produkte` | Table → `Produkte` | nach Abschnittswechsel | Tabelle mit verlinkten Produkten und Bemerkungen |
| `custom_supportvertrag` | Link → `Supportvertrag` | nach `customer_group` | Verknüpfungsfeld für den Supportvertrag |

**DocType: Kontakt (`Contact`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_ort` | Data | Zeile 10 | Ort des Kontakts |
| `custom_abteilung` | Link → `Abteilungstyp` | Zeile 11 | Abteilung des Kontakts |
| `custom_bemerkungen` | Small Text | Zeile 21 | Freitext-Bemerkungen |

#### Workspace

| Name | Beschreibung |
|---|---|
| `VEPRO` | Eigener Workspace im Frappe Desk; Icon `color-review-points`; enthält Schnellzugriff-Shortcuts für `Kunde`, `Kontakt`, `Adresse`, `Mitarbeiter`, `Lead` und `Projekt` |

---

### Changelog

| Version | Datum | Änderungen |
|---|---|---|
| `0.0.19` | 2026-05-28 | Client Script für DocType `Customer`: Hintergrundfarbe von `custom_supportvertrag` abhängig vom gewählten Supportvertrag (24/7 → grün, +3h → gelb, Standard → blau, kein Supportvertrag → rot); neue Datei `public/js/customer.js`, eingebunden via `doctype_js`-Hook |
| `0.0.18` | 2026-05-27 | Version-Bump |
| `0.0.17` | 2026-05-21 | `pdf_utils.py`: HostNotFoundError dauerhaft behoben – Verarbeitungsreihenfolge korrigiert: `scrub_urls()` wird nun manuell aufgerufen, danach erst Hostnamen per Regex durch `127.0.0.1` ersetzt; Frappe's `get_pdf()` wird umgangen, sodass `scrub_urls()` nicht ein zweites Mal läuft und die Ersetzung rückgängig macht |
| `0.0.16` | 2026-05-21 | Version-Bump für site_branding-Release |
| `0.0.15` | 2026-05-21 | Neues Modul `site_branding`: DocType `Site Branding Rule` zur umgebungsabhängigen Steuerung von Custom-CSS und optischen Badges im Frappe-Desk; Matching per Hostname oder URL (Host Equals, Host Contains, URL Contains, Regex); Priorität steuerbar; Standard-Regeln für DEV, TEST, STAGE und PROD werden beim Migrate automatisch angelegt (`setup.py`); clientseitige Auswertung via `site_branding.js` (eingebunden über `app_include_js`) |
| `0.0.14` | 2026-05-19 | Neues Feld `bemerkungen` (Data) im DocType `Supportvertrag` hinzugefügt |
| `0.0.13` | 2026-05-19 | `pdf_utils.py`: HostNotFoundError dauerhaft behoben – Hostname im HTML wird vor wkhtmltopdf-Übergabe durch `127.0.0.1` ersetzt; `load-error-handling: ignore` wird im Code erzwungen |
| `0.0.12` | 2026-05-18 | `custom_bemerkungen` im DocType `Contact` von `Data` auf `Small Text` geändert |
| `0.0.9` | 2026-05-12 | Neuer DocType `Supportvertrag` mit 4 Stammdaten-Dokumenten; `custom_supportvertrag` von `Select` auf `Link → Supportvertrag` umgestellt |
| `0.0.8` | 2026-05-11 | `custom_supportvertrag` von `Data` auf `Select` geändert; Optionen: `24/7`, `+3h`, `Standard`, `kein Supportvertrag` |
| `0.0.7` | 2026-05-11 | Workspace VEPRO: Schnellzugriffe für `Adresse`, `Mitarbeiter`, `Lead` und `Projekt` ergänzt; Karte „Stammdaten" entfernt |
| `0.0.6` | 2026-05-11 | Workspace VEPRO mit Shortcuts (`Kunde`, `Kontakt`) und Karte „Stammdaten" befüllt |
| `0.0.5` | 2026-05-08 | Versionsbump |
| `0.0.4` | 2026-05-08 | Workspace VEPRO angelegt (leer); Icon auf `color-review-points` gesetzt |
| `0.0.3` | 2026-05-08 | Alle Custom Fields in einer Fixture zusammengefasst (`Customer` + `Contact`) |
| `0.0.2` | 2026-05-08 | Custom Field `custom_supportvertrag` im DocType `Customer` hinzugefügt; README erweitert |
| `0.0.1` | 2026-05-08 | Custom Fields für `Customer` und `Contact`; neue DocTypes `Abteilungstyp` und `Produkte` |

---

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app vepro_app
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/vepro_app
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
