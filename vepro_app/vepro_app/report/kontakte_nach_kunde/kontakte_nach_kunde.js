frappe.query_reports["Kontakte nach Kunde"] = {
	filters: [
		{
			fieldname: "kunde",
			label: __("Kunde"),
			fieldtype: "Link",
			options: "Customer",
		},
	],
};
