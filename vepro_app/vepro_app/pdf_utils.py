import re

import pdfkit
from packaging.version import Version

import frappe
from frappe.utils.data import scrub_urls
from frappe.utils.pdf import cleanup, get_wkhtmltopdf_version, prepare_options
from frappe.utils.print_format import print_language, validate_print_permission
from typing import Literal
from urllib.parse import urlparse


@frappe.whitelist(allow_guest=True)
def download_pdf(
	doctype: str,
	name: str,
	format=None,
	doc=None,
	no_letterhead=0,
	language=None,
	letterhead=None,
	pdf_generator: Literal["wkhtmltopdf", "chrome"] | None = None,
):
	"""
	Override von frappe.utils.print_format.download_pdf.

	Warum dieser Override notwendig ist:
	Frappe's get_pdf() ruft intern scrub_urls() auf, das ALLE relativen URLs im HTML
	zu absoluten URLs mit dem Site-Hostnamen expandiert (z.B. /assets/... wird zu
	http://d-code-vepro.localhost:8000/assets/...). wkhtmltopdf kann diesen Hostnamen
	nicht per DNS auflösen → HostNotFoundError.

	Ein einfaches Ersetzen des Hostnamens VOR dem get_pdf()-Aufruf wird deshalb immer
	durch scrub_urls() rückgängig gemacht. Der einzige zuverlässige Fix ist, die
	Verarbeitungsreihenfolge selbst zu kontrollieren:
	1. scrub_urls() manuell aufrufen (URL-Expansion: relativ → absolut)
	2. Anschließend ALLE Varianten des Hostnamens per Regex durch 127.0.0.1 ersetzen
	3. prepare_options() und pdfkit.from_string() direkt aufrufen (get_pdf() wird
	   umgangen, damit scrub_urls() nicht ein zweites Mal läuft)
	"""
	doc = doc or frappe.get_doc(doctype, name)
	validate_print_permission(doc)

	pdf_options = dict(frappe.conf.get("pdf_options") or {})
	pdf_options.setdefault("load-error-handling", "ignore")
	pdf_options.setdefault("load-media-error-handling", "ignore")

	with print_language(language):
		html = frappe.get_print(
			doctype,
			name,
			format,
			doc=doc,
			as_pdf=False,
			letterhead=letterhead,
			no_letterhead=no_letterhead,
		)

	# Schritt 1: URL-Expansion wie Frappe's get_pdf() sie intern ausführt.
	# Relative Pfade (/assets/...) werden zu absoluten URLs mit dem Site-Hostnamen.
	html = scrub_urls(html)

	# Schritt 2: Jetzt ALLE Formen des Hostnamens durch 127.0.0.1 ersetzen.
	# Die Regex erfasst http:// und https://, mit und ohne abweichenden Port.
	# Dieser Schritt muss nach scrub_urls() erfolgen, sonst wird er durch
	# die URL-Expansion wieder rückgängig gemacht.
	host_name = frappe.conf.get("host_name", "")
	if host_name:
		parsed = urlparse(host_name)
		hostname = parsed.hostname  # z.B. "d-code-vepro.localhost"
		port = parsed.port or (443 if parsed.scheme == "https" else 80)
		html = re.sub(
			r"https?://" + re.escape(hostname) + r"(?::\d+)?",
			f"http://127.0.0.1:{port}",
			html,
		)

	# Schritt 3: Optionen aufbereiten und pdfkit direkt aufrufen.
	# get_pdf() wird bewusst umgangen, damit scrub_urls() nicht erneut läuft.
	html, options = prepare_options(html, pdf_options)
	options.update({"disable-javascript": "", "disable-local-file-access": ""})
	if Version(get_wkhtmltopdf_version()) > Version("0.12.3"):
		options.update({"disable-smart-shrinking": ""})

	try:
		pdf_file = pdfkit.from_string(html, options=options, verbose=True)
	finally:
		cleanup(options)

	frappe.local.response.filename = "{name}.pdf".format(
		name=name.replace(" ", "-").replace("/", "-")
	)
	frappe.local.response.filecontent = pdf_file
	frappe.local.response.type = "pdf"
