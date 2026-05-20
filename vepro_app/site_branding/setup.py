import frappe


# Default rules inserted during migrate (if not already present).
# Order matters: lower priority = matched first.
# VEPRO PROD must come before VEPRO STAGE because "vepro-east.de"
# would also match the more specific "erp.vepro-east.de".

DEFAULT_RULES = [
    {
        "rule_name": "Local DEV",
        "enabled": 1,
        "match_type": "Host Contains",
        "match_value": "localhost",
        "priority": 10,
        "css": ":root { --bg-color: #eef4fd; }",
        "badge_enabled": 1,
        "badge_text": "DEV",
        "badge_position": "Top Right",
        "badge_color": "#2196f3",
        "badge_text_color": "#ffffff",
    },
    {
        "rule_name": "Local TEST",
        "enabled": 1,
        "match_type": "Host Contains",
        "match_value": "schmidtundtoechter.com",
        "priority": 20,
        "css": ":root { --bg-color: #fdeeed; }",
        "badge_enabled": 1,
        "badge_text": "TEST",
        "badge_position": "Top Right",
        "badge_color": "#f44336",
        "badge_text_color": "#ffffff",
    },
    {
        "rule_name": "VEPRO PROD",
        "enabled": 1,
        "match_type": "Host Contains",
        "match_value": "erp.vepro-east.de",
        "priority": 30,
        "css": "/* PROD – no visual changes */",
        "badge_enabled": 0,
        "badge_text": "",
        "badge_position": "Top Right",
        "badge_color": "",
        "badge_text_color": "",
    },
    {
        "rule_name": "VEPRO STAGE",
        "enabled": 1,
        "match_type": "Host Contains",
        "match_value": "vepro-east.de",
        "priority": 40,
        "css": ":root { --bg-color: #fdf6e6; }",
        "badge_enabled": 1,
        "badge_text": "STAGE",
        "badge_position": "Top Right",
        "badge_color": "#ff9800",
        "badge_text_color": "#ffffff",
    },
]


def create_default_branding_rules():
    """Insert default Site Branding Rules if they do not exist yet."""
    for rule in DEFAULT_RULES:
        if not frappe.db.exists("Site Branding Rule", rule["rule_name"]):
            doc = frappe.get_doc({"doctype": "Site Branding Rule", **rule})
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
