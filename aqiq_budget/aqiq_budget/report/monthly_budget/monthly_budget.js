// Copyright (c) 2024, aqiq Budget and contributors
// For license information, please see license.txt

frappe.query_reports["Monthly Budget"] = {
	"filters": [
		{
            'fieldname': 'account',
            'fieldtype': 'Link',
            'label': 'Account',
			'options': 'Account',
            'width': 180,
        },
		{
            'fieldname': 'fiscal_year',
            'fieldtype': 'Link',
            'label': 'Fiscal Year',
			'options': 'Fiscal Year',
            'width': 180,
        }
	]
};
