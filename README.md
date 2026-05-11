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

#### Custom Fields

**DocType: Kunde (`Customer`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_section_break_8lhrp` | Section Break | nach `image` | Abschnittswechsel „Produkttabelle" |
| `custom_produkte` | Table → `Produkte` | nach Abschnittswechsel | Tabelle mit verlinkten Produkten und Bemerkungen |
| `custom_supportvertrag` | Data | nach `customer_group` | Freitextfeld für den Supportvertrag |

**DocType: Kontakt (`Contact`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_ort` | Data | Zeile 10 | Ort des Kontakts |
| `custom_abteilung` | Link → `Abteilungstyp` | Zeile 11 | Abteilung des Kontakts |
| `custom_bemerkungen` | Data | Zeile 21 | Freitext-Bemerkungen |

#### Workspace

| Name | Beschreibung |
|---|---|
| `VEPRO` | Eigener Workspace im Frappe Desk; Icon `color-review-points`; enthält Schnellzugriff-Shortcuts für `Kunde`, `Kontakt`, `Adresse`, `Mitarbeiter`, `Lead` und `Projekt` |

---

### Changelog

| Version | Datum | Änderungen |
|---|---|---|
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
