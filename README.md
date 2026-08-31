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
| `Auswahl Position` | Stammdaten | Positionsbezeichnungen; wird im DocType „Kontakt" als Link-Feld verwendet und automatisch in das native Feld `designation` übertragen |
| `Supportvertrag` | Stammdaten | Supportvertrags-Typen (`24/7`, `+3h`, `Standard`, `kein Supportvertrag`); wird im DocType „Kunde" als Link-Feld verwendet |
| `Einstellungen Vepro` | Single (Einstellungen) | App-weite Einstellungen; Felder: `obergrenze_ohne_freigabe` (Currency), `untergrenze_mit_freigabe` (Currency) |

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
| `custom_auswahl_position` | Link → `Auswahl Position` | nach `salutation` (Anrede) | Auswahl der Position; Wert wird automatisch in das native Feld `designation` übertragen |
| `custom_ort` | Data | Zeile 10 | Ort des Kontakts |
| `custom_abteilung` | Link → `Abteilungstyp` | Zeile 11 | Abteilung des Kontakts |
| `custom_kunde` | Link → `Customer` | nach `custom_abteilung` | Zugeordneter Kunde; wird täglich automatisch aus den Dynamic Links befüllt |
| `custom_lieferant` | Link → `Supplier` | nach `custom_kunde` | Zugeordneter Lieferant |
| `custom_bemerkungen` | Small Text | Zeile 21 | Freitext-Bemerkungen |

#### Ausgeblendete native Felder

**DocType: Kontakt (`Contact`)**

| Feldname | Beschreibung |
|---|---|
| `status` | via Property Setter `hidden: 1` |
| `gender` | via Property Setter `hidden: 1` |
| `sync_with_google_contacts` | via Property Setter `hidden: 1` |
| `user` | via Property Setter `hidden: 1` |
| `middle_name` | via Property Setter `hidden: 1` |

**DocType: Angebot (`Quotation`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_leistungszeitraum` | Data | nach `valid_till` | Standardwert: „Der Leistungszeitraum wird nach der Beauftragung mit dem Projektmanager individuell abgestimmt.“ |
| `custom_vor_ort` | Check | nach `custom_leistungszeitraum` | Leistungsort: Standard ist „im Haus“ – Kreuz gesetzt bedeutet „vor Ort“ |
| `custom_incoterm_benutzen` | Check | nach `column_break_34` (vor `incoterm`) | Steuert Sichtbarkeit von `incoterm` und `named_place`; setzt Standardwert „CPT“ beim Aktivieren |

**DocType: Auftrag (`Sales Order`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_leistungszeitraum` | Data | nach `delivery_date` | Kein Standardwert |
| `custom_vor_ort` | Check | nach `custom_leistungszeitraum` | Leistungsort: Standard ist „im Haus“ – Kreuz gesetzt bedeutet „vor Ort“ |
| `custom_incoterm_benutzen` | Check | nach `column_break_49` (vor `incoterm`) | Steuert Sichtbarkeit von `incoterm` und `named_place`; setzt Standardwert „CPT“ beim Aktivieren |

**DocType: Ausgangsrechnung (`Sales Invoice`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_incoterm_benutzen` | Check | nach `column_break_55` (vor `incoterm`) | Steuert Sichtbarkeit von `incoterm` und `named_place`; setzt Standardwert „CPT“ beim Aktivieren |

**DocType: Lieferschein (`Delivery Note`)**

| Feldname | Feldtyp | Position | Beschreibung |
|---|---|---|---|
| `custom_incoterm_benutzen` | Check | nach `column_break_39` (vor `incoterm`) | Steuert Sichtbarkeit von `incoterm` und `named_place`; setzt Standardwert „CPT“ beim Aktivieren |

**DocTypes: Angebot, Auftrag, Ausgangsrechnung, Lieferschein (`Quotation`, `Sales Order`, `Sales Invoice`, `Delivery Note`)**

| Feldname | Beschreibung |
|---|---|
| `scan_barcode` | via Property Setter `hidden: 1` |

#### Server Scripts

| Name | Typ | Zeitplan | Beschreibung |
|---|---|---|---|
| `Kontakt Kunde Sync` | Scheduler Event | täglich 03:00 Uhr (`0 3 * * *`) | Durchsucht alle Kontakte mit leerem Feld `custom_kunde` und trägt automatisch den ersten verknüpften Kunden aus der Dynamic-Links-Tabelle ein |

#### Workspace

| Name | Beschreibung |
|---|---|
| `VEPRO` | Eigener Workspace im Frappe Desk; Icon `color-review-points`; Bereich **Schnellzugriff** mit Links zu `Kunde`, `Kontakt`, `Adresse`, `Mitarbeiter`, `Lead`, `Projekt`, `Lieferant`; Bereich **Berichte** mit Links zu „Artikelbezogene Übersicht der Verkäufe“, „Kontakte nach Kunde“, „Telefonbuch“, „Adressen nach Ort“; Bereich **Hilfe** mit Links zu `App-Informationen`, `Anpassungen` und `Versionshistorie`; Bereich **Administration** mit Links zu `System Diagnostics` und `Einstellungen Vepro` |

#### Help Articles

| Name | Kategorie | Beschreibung |
|---|---|---|
| `App-Informationen` | VEPRO App | Allgemeine App-Informationen und Branch-Übersicht |
| `Anpassungen` | VEPRO App | DocTypes, Custom Fields, Workspace und Help Articles der vepro_app |
| `Versionshistorie` | VEPRO App | Changelog der vepro_app als HTML-Seite im Frappe Desk |

---

### Changelog

| Version | Datum | Änderungen |
|---|---|---|
| `0.0.43` | 2026-08-31 | Workspace VEPRO: absolute URLs der drei Berichte-Links (`Item-wise Sales Register`, `Telefonbuch`, `Adressen nach Ort`) auf relative Pfade umgestellt (`/app/...`) |
| `0.0.42` | 2026-08-28 | Custom Field `custom_incoterm_benutzen` (Check, „Incoterm benutzen“) in `Angebot`, `Auftrag`, `Ausgangsrechnung`, `Lieferschein` – jeweils direkt vor `incoterm`; steuert Sichtbarkeit von `incoterm` und `named_place` via `depends_on`; Client Script setzt Standardwert „CPT“ beim Aktivieren und leert die Felder beim Deaktivieren; neue JS-Dateien `sales_order.js`, `sales_invoice.js`, `delivery_note.js` in `hooks.py` registriert |
| `0.0.41` | 2026-08-28 | Custom Fields `custom_leistungszeitraum` (Data, „Leistungszeitraum“) in `Angebot` nach `valid_till` (Standardwert vorausgefüllt) und in `Auftrag` nach `delivery_date` (kein Standardwert) |
| `0.0.40` | 2026-08-28 | Workspace VEPRO: neuer Abschnitt **Berichte** (zwischen Schnellzugriff und Hilfe) mit Links zu „Artikelbezogene Übersicht der Verkäufe“, „Kontakte nach Kunde“, „Telefonbuch“ und „Adressen nach Ort“; „Kontakte nach Kunde“ aus Schnellzugriff entfernt; Custom Fields `custom_vor_ort` (Check, „vor Ort“) in `Angebot` nach `valid_till` und in `Auftrag` nach `delivery_date` |
| `0.0.39` | 2026-08-11 | DocTypes `Angebot`, `Auftrag`, `Ausgangsrechnung`: Feld `payment_terms_template` als Pflichtfeld gesetzt (Property Setter `reqd: 1`) |
| `0.0.38` | 2026-08-06 | DocTypes `Ausgangsrechnung`, `Angebot`, `Auftrag`: diverse Felder ausgeblendet und Feldreihenfolge via Property Setter angepasst; Custom Fields `custom_zu_haenden_von` (Angebot, Data, „zu Händen von") und `custom_column_break_jnybe` (Auftrag, Column Break) als Fixtures registriert |
| `0.0.37` | 2026-08-03 | Neuer Single-DocType `Einstellungen Vepro` mit Feldern `obergrenze_ohne_freigabe` und `untergrenze_mit_freigabe` (Currency); Workspace VEPRO: Shortcut „Einstellungen Vepro" unter Administration |
| `0.0.36` | 2026-08-03 | DocTypes `Angebot`, `Auftrag`, `Ausgangsrechnung`, `Lieferschein`: Feld `scan_barcode` ausgeblendet via Property Setter `hidden: 1` |
| `0.0.35` | 2026-07-29 | Alle 12 manuellen Property Setter sowie Custom Field `custom_lieferant` korrekt als App-Fixtures registriert (Deinstallation macht Änderungen rückgängig); DocType `Kontakt`: 5 native Felder ausgeblendet (`status`, `gender`, `sync_with_google_contacts`, `user`, `middle_name`) via Property Setter `hidden: 1` |
| `0.0.34` | 2026-07-20 | DocType `Kontakt`: neues Custom Field `custom_lieferant` (Link → `Supplier`) nach `custom_kunde`, mit Feldbeschreibung |
| `0.0.33` | 2026-07-06 | DocType `Kontakt`: Standard-Filter `Status` entfernt (Property Setter `in_standard_filter: 0`); Custom Field `custom_kunde` mit Option „In Standard Filter" versehen |
| `0.0.32` | 2026-07-03 | DocType `Kontakt`: neues Custom Field `custom_kunde` (Link → `Customer`) nach `custom_abteilung`, mit Feldbeschreibung; Server Script `Kontakt Kunde Sync` (Scheduler Event, täglich 03:00 Uhr): befüllt `custom_kunde` automatisch aus den Dynamic Links |
| `0.0.31` | 2026-06-24 | DocType `Adresse`: Feldbeschreibungen (blau) für `address_title` (Person/Firma), `address_line1` (Straße + Hausnummer) und `address_line2` (zusätzliche Adresszeile) als Property Setter |
| `0.0.30` | 2026-06-24 | Workspace VEPRO: neuer Shortcut **Kontakte nach Kunde** (Typ: Report) im Abschnitt **Schnellzugriff** direkt nach „Kontakt“ |
| `0.0.29` | 2026-06-24 | Neuer Script Report **Kontakte nach Kunde**: filtert Kontakte anhand des verknüpften Kunden (Child-Table `Dynamic Link`); Filter-Feld als `Link`-Feld mit Autocomplete |
| `0.0.28` | 2026-06-15 | DocType `Kunde`: 3 neue Custom Fields nach `custom_supportvertrag` – `custom_telefonnummer` (Telefonnummer, Data), `custom_e_mail_adresse` (E-Mail-Adresse, Data), `custom_website` (Website, Data) |
| `0.0.27` | 2026-06-15 | Workspace VEPRO: neuer Abschnitt **Administration** mit Shortcut **System Diagnostics** → `/system_diagnostics` (relative URL, funktioniert auf jeder Site) |
| `0.0.26` | 2026-06-15 | App `sut_app_core` installiert (Branch: `main`); Modul `site_branding` aus `vepro_app` entfernt (hooks.py, modules.txt, Ordner, JS-Datei) – Funktionalität liegt jetzt vollständig in `sut_app_core`; Bugfix `devcontainer.json`: grep-Bedingung in `postStartCommand` auf `d-code-vepro.localhost` korrigiert, damit wkhtmltopdf den Hostnamen auflösen kann (HostNotFoundError bei PDF-Generierung) |
| `0.0.25` | 2026-06-04 | Feldbeschreibungen für `custom_auswahl_position` und natives Feld `designation` (Position) im DocType `Kontakt` hinzugefügt; neues Fixture `property_setter.json` für Standard-Feldbeschreibung |
| `0.0.24` | 2026-06-01 | Neuer DocType `Auswahl Position` (Stammdaten für Positionsbezeichnungen); neues Custom Field `custom_auswahl_position` (Link → `Auswahl Position`) im DocType `Kontakt` nach `salutation`; Client Script `public/js/contact.js`: Wert wird bei Auswahl automatisch in das native Feld `designation` übertragen |
| `0.0.23` | 2026-06-01 | Bugfix: Help Articles `App-Informationen` und `Anpassungen` – `author`-Feld auf `l.maeurer@schmidtundtoechter.com` gesetzt (war `user_fullname`-Platzhalter → Fixture-Import schlug auf neuen Systemen fehl → "Page not found") |
| `0.0.22` | 2026-06-01 | Bugfix: Workspace VEPRO – Hilfe-Shortcuts (`App-Informationen`, `Anpassungen`, `Versionshistorie`) verwendeten falsches Feld `link_to` statt `url`; nach `export-doc` korrigiert – Links funktionieren jetzt auch auf neuen Sites nach `bench migrate` |
| `0.0.21` | 2026-05-28 | Neue Help Articles `App-Informationen` und `Anpassungen` (Kategorie `VEPRO App`) als Fixtures; Workspace VEPRO: Hilfe-Shortcuts auf öffentliche Routen umgestellt; Reihenfolge im Bereich **Hilfe**: App-Informationen, Anpassungen, Versionshistorie |
| `0.0.20` | 2026-05-28 | Workspace VEPRO: Shortcut „Versionshistorie" in neuen Abschnitt **Hilfe** verschoben; Abschnitt **Schnellzugriff** nur noch mit DocType-Links |
| `0.0.19` | 2026-05-28 | Help Article `Versionshistorie` (Kategorie `VEPRO App`) als Fixture; README-Inhalt als HTML im Frappe Desk; Workspace-Shortcut; Client Script `public/js/customer.js` für Hintergrundfarbe von `custom_supportvertrag` (24/7 → grün, +3h → gelb, Standard → blau, kein Supportvertrag → rot); eingebunden via `doctype_js`-Hook |
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
