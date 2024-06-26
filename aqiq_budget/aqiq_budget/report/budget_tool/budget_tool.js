// Copyright (c) 2024, aqiq Budget and contributors
// For license information, please see license.txt

frappe.query_reports["Budget Tool"] = {
	"filters": [
		{
            'fieldname': 'account',
            'fieldtype': 'Link',
            'label': 'Account',
			'options': 'Account',
            'width': 180,
        },
        {
            'fieldname': 'monthly_distribution_template',
            'fieldtype': 'Link',
            'label': 'Monthly Distribution Template',
			'options': 'Monthly Distribution Mapping',
            'width': 180,
        },
		{
            'fieldname': 'docstatus',
            'fieldtype': 'Select',
            'label': 'Status',
			'options': ['','Draft','Submitted'],
            'width': 180,
        }
	]
};
