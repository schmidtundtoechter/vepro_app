import frappe
from frappe.utils.print_format import validate_print_permission, print_language
from typing import Literal


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
	Liest pdf_options aus site_config (frappe.conf.pdf_options) und
	übergibt sie an get_print, damit z.B. load-error-handling wirkt.
	"""
	doc = doc or frappe.get_doc(doctype, name)
	validate_print_permission(doc)

	# Optionen aus site_config laden (z.B. load-error-handling: ignore)
	pdf_options = frappe.conf.get("pdf_options") or {}

	with print_language(language):
		pdf_file = frappe.get_print(
			doctype,
			name,
			format,
			doc=doc,
			as_pdf=True,
			letterhead=letterhead,
			no_letterhead=no_letterhead,
			pdf_generator=pdf_generator,
			pdf_options=pdf_options,
		)

	frappe.local.response.filename = "{name}.pdf".format(
		name=name.replace(" ", "-").replace("/", "-")
	)
	frappe.local.response.filecontent = pdf_file
	frappe.local.response.type = "pdf"
