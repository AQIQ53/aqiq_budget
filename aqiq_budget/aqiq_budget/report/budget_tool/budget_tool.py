# Copyright (c) 2024, aqiq Budget and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns, data = [], []
    condition=get_condition(filters)
    columns = get_column()
    data = get_data_budget(filters,condition)
    return columns, data

def get_data_budget(filters,condition):
    raw_data = frappe.db.sql("""
        SELECT 
            mbdt.account,
            bt.name,
            bt.monthly_distribution_template,
            mbdt.august,
            mbdt.september,
            mbdt.october,
            mbdt.november,
            mbdt.december,
            mbdt.january,
            mbdt.february,
            mbdt.march,
            mbdt.april,
            mbdt.may,
            mbdt.june,
            mbdt.july,
            mbdt.total_amount
        FROM `tabBudget Tool` bt
        INNER JOIN `tabMonthly Budget Distribution Table` mbdt ON bt.name = mbdt.parent
        WHERE bt.docstatus != 2 and 1=1 %s
    """% (condition), as_dict=True)    
    data = raw_data
    return data

def get_condition(filters):
    conditions = ""
    if filters.get("account"):
        conditions += " and mbdt.account='{}'".format(filters.get("account"))
    if filters.get("docstatus"):
        if filters.get("docstatus")=='Draft':
            conditions += " and bt.docstatus='{}'".format('0')
        else:
            conditions += " and bt.docstatus='{}'".format('1')
    if filters.get("monthly_distribution_template"):
        conditions += " and bt.monthly_distribution_template='{}'".format(filters.get("monthly_distribution_template"))
    return conditions

def get_column():
    return [
        {
            'fieldname': 'account',
            'fieldtype': 'Data',
            'label': 'Account',
            'width': 180,
        },
        {
            'fieldname': 'august',
            'fieldtype': 'Currency',
            'label': 'August',
            'width': 200,
        },
        {
            'fieldname': 'september',
            'fieldtype': 'Currency',
            'label': 'September',
            'width': 150,
        },
        {
            'fieldname': 'october',
            'fieldtype': 'Currency',
            'label': 'October',
            'width': 150,
        },
        {
            'fieldname': 'november',
            'fieldtype': 'Currency',
            'label': 'November',
            'width': 150,
        },
        {
            'fieldname': 'december',
            'fieldtype': 'Currency',
            'label': 'December',
            'width': 150,
        },
        {
            'fieldname': 'january',
            'fieldtype': 'Currency',
            'label': 'January',
            'width': 150,
        },
        {
            'fieldname': 'february',
            'fieldtype': 'Currency',
            'label': 'February',
            'width': 150,
        },
        {
            'fieldname': 'march',
            'fieldtype': 'Currency',
            'label': 'March',
            'width': 150,
        },
        {
            'fieldname': 'april',
            'fieldtype': 'Currency',
            'label': 'April',
            'width': 150,
        },
        {
            'fieldname': 'may',
            'fieldtype': 'Currency',
            'label': 'May',
            'width': 150,
        },
        {
            'fieldname': 'june',
            'fieldtype': 'Currency',
            'label': 'June',
            'width': 150,
        },
        {
            'fieldname': 'july',
            'fieldtype': 'Currency',
            'label': 'July',
            'width': 150,
        },
        {
            'fieldname': 'total_amount',
            'fieldtype': 'Currency',
            'label': 'Total Amount',
            'width': 150,
        }
    ]
