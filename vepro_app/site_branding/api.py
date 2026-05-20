import frappe


@frappe.whitelist()
def get_branding_rules():
    """Return all active Site Branding Rules, ordered by priority ascending.

    Accessible to any logged-in desk user so the frontend can load branding
    without requiring System Manager privileges.
    """
    return frappe.get_all(
        "Site Branding Rule",
        filters={"enabled": 1},
        fields=[
            "name",
            "rule_name",
            "match_type",
            "match_value",
            "priority",
            "css",
            "badge_text",
            "badge_enabled",
            "badge_position",
            "badge_color",
            "badge_text_color",
        ],
        order_by="priority asc",
    )
