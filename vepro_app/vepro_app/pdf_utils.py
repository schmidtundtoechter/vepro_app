import frappe
from frappe.utils.pdf import get_pdf
from frappe.utils.print_format import validate_print_permission, print_language
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

	Löst den wkhtmltopdf-HostNotFoundError dauerhaft:
	1. HTML wird zuerst als Text generiert.
	2. Der Site-Hostname im HTML wird durch http://127.0.0.1:<port> ersetzt,
	   damit wkhtmltopdf lokale Assets (CSS, Bilder) ohne DNS-Auflösung laden kann.
	3. pdf_options aus site_config werden angewendet; load-error-handling: ignore
	   wird als Sicherheitsnetz erzwungen.
	"""
	doc = doc or frappe.get_doc(doctype, name)
	validate_print_permission(doc)

	# Optionen aus site_config laden; Netzwerkfehler immer ignorieren
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

	# Hostnamen im HTML durch 127.0.0.1 ersetzen, damit wkhtmltopdf
	# lokale Ressourcen ohne DNS-Auflösung laden kann (verhindert HostNotFoundError)
	host_name = frappe.conf.get("host_name", "")
	if host_name:
		parsed = urlparse(host_name)
		port = parsed.port or (443 if parsed.scheme == "https" else 80)
		html = html.replace(host_name, f"http://127.0.0.1:{port}")

	pdf_file = get_pdf(html, options=pdf_options)

	frappe.local.response.filename = "{name}.pdf".format(
		name=name.replace(" ", "-").replace("/", "-")
	)
	frappe.local.response.filecontent = pdf_file
	frappe.local.response.type = "pdf"
