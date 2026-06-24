import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": "Kontakt",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Contact",
            "width": 200,
        },
        {
            "label": "Vorname",
            "fieldname": "first_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Nachname",
            "fieldname": "last_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "E-Mail",
            "fieldname": "email_id",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": "Telefon",
            "fieldname": "phone",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": "Verknüpfter Kunde",
            "fieldname": "kunde",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 220,
        },
    ]


def get_data(filters):
    kunde = filters.get("kunde") if filters else None

    conditions = "dl.link_doctype = 'Customer'"
    values = {}

    if kunde:
        conditions += " AND dl.link_name = %(kunde)s"
        values["kunde"] = kunde

    return frappe.db.sql(
        f"""
        SELECT
            c.name,
            c.first_name,
            c.last_name,
            c.email_id,
            c.phone,
            dl.link_name AS kunde
        FROM
            `tabContact` c
        INNER JOIN
            `tabDynamic Link` dl ON dl.parent = c.name AND dl.parenttype = 'Contact'
        WHERE
            {conditions}
        ORDER BY
            dl.link_name, c.last_name, c.first_name
        """,
        values,
        as_dict=True,
    )
