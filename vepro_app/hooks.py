app_name = "vepro_app"
app_title = "VEPRO App"
app_publisher = "Schmidt und Toechter"
app_description = "Vepro Application"
app_email = "kontakt@schmidtundtoechter.com"
app_license = "mit"

fixtures = [
	# Help Article
	{
		"dt": "Help Category",
		"filters": [["name", "=", "VEPRO App"]],
	},
	{
		"dt": "Help Article",
		"filters": [["name", "in", ["App-Informationen", "Anpassungen", "Versionshistorie"]]],
	},
	# Benutzerdefinierte Felder für Customer und Contact
	{
		"dt": "Custom Field",
		"filters": [
			["fieldname", "in", [
				"custom_section_break_8lhrp",
				"custom_produkte",
				"custom_supportvertrag",
				"custom_telefonnummer",
				"custom_e_mail_adresse",
				"custom_website",
				"custom_ort",
				"custom_abteilung",
				"custom_kunde",
				"custom_bemerkungen",
				"custom_auswahl_position",
				"custom_lieferant",
				"custom_zu_haenden_von",
				"custom_column_break_jnybe",
			]],
		],
	},
	# Property Setter für Standard-Felder (z.B. Beschreibungen)
	{
		"dt": "Property Setter",
		"filters": [
			["name", "in", [
				"Contact-designation-description",
				"Address-address_title-description",
				"Address-address_line1-description",
				"Address-address_line2-description",
				"Contact-status-in_standard_filter",
				"Contact-status-hidden",
				"Contact-gender-hidden",
				"Contact-sync_with_google_contacts-hidden",
				"Contact-user-hidden",
				"Contact-middle_name-hidden",
				"Contact-main-field_order",
				"Customer-main-field_order",
				"Quotation-scan_barcode-hidden",
				"Sales Order-scan_barcode-hidden",
				"Sales Invoice-scan_barcode-hidden",
				"Delivery Note-scan_barcode-hidden",
				"Sales Invoice-loyalty_points_redemption-hidden",
				"Sales Invoice-main-field_order",
				"Sales Invoice-section_break2-hidden",
				"Sales Invoice-cost_center-hidden",
				"Sales Invoice-accounting_dimensions_section-collapsible",
				"Quotation-disable_rounded_total-hidden",
				"Quotation-in_words-hidden",
				"Quotation-lost_reasons_section-hidden",
				"Quotation-main-field_order",
				"Quotation-contact_person-hidden",
				"Quotation-company_address_section-hidden",
				"Sales Order-section_break1-hidden",
				"Sales Order-col_break46-hidden",
				"Sales Order-dispatch_address_name-hidden",
				"Sales Order-last_scanned_warehouse-hidden",
				"Sales Order-sec_warehouse-hidden",
				"Sales Order-main-field_order",
				"Sales Order-cost_center-hidden",
				"Sales Order-accounting_dimensions_section-collapsible",
			]],
		],
	},
	# Server Scripts (geplante Aufgaben, sichtbar im Frontend)
	{
		"dt": "Server Script",
		"filters": [["name", "=", "Kontakt Kunde Sync"]],
	},
	# Supportvertrag-Stammdaten
	{
		"dt": "Supportvertrag",
		"filters": [
			["name", "in", ["24/7", "+3h", "Standard", "kein Supportvertrag"]],
		],
	},
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "vepro_app",
# 		"logo": "/assets/vepro_app/logo.png",
# 		"title": "vepro_app",
# 		"route": "/vepro_app",
# 		"has_permission": "vepro_app.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/vepro_app/css/vepro_app.css"
# app_include_js = []

# include js, css files in header of web template
# web_include_css = "/assets/vepro_app/css/vepro_app.css"
# web_include_js = "/assets/vepro_app/js/vepro_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "vepro_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Customer": "public/js/customer.js",
	"Contact":  "public/js/contact.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "vepro_app/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "vepro_app.utils.jinja_methods",
# 	"filters": "vepro_app.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "vepro_app.install.before_install"
# after_install = "vepro_app.install.after_install"

# Migration
# ---------

# after_migrate = []
after_migrate = ["vepro_app.vepro_app.tasks.reload_vepro_workspace"]

# Uninstallation
# ------------

# before_uninstall = "vepro_app.uninstall.before_uninstall"
# after_uninstall = "vepro_app.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "vepro_app.utils.before_app_install"
# after_app_install = "vepro_app.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "vepro_app.utils.before_app_uninstall"
# after_app_uninstall = "vepro_app.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "vepro_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------
# Geplante Aufgaben werden als Server Scripts verwaltet (sichtbar unter Settings → Server Script).
# Manuelle Implementierung: vepro_app.vepro_app.tasks

# Testing
# -------

# before_tests = "vepro_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	# Überschreibt download_pdf, damit frappe.conf.pdf_options (aus site_config.json)
	# tatsächlich an wkhtmltopdf weitergegeben werden.
	# Ohne diesen Override werden die site_config-Einträge komplett ignoriert.
	"frappe.utils.print_format.download_pdf": "vepro_app.vepro_app.pdf_utils.download_pdf"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "vepro_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["vepro_app.utils.before_request"]
# after_request = ["vepro_app.utils.after_request"]

# Job Events
# ----------
# before_job = ["vepro_app.utils.before_job"]
# after_job = ["vepro_app.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"vepro_app.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

