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
            ba.account,
            b.fiscal_year,
            b.name AS budget_name,
            b.monthly_distribution,
            ba.budget_amount,
            mdp.month,
            mdp.percentage_allocation
        FROM `tabBudget` b 
        INNER JOIN `tabBudget Account` ba ON b.name = ba.parent 
        INNER JOIN `tabMonthly Distribution Percentage` mdp ON b.monthly_distribution = mdp.parent
        WHERE b.docstatus = 1 and 1=1 %s
    """% (condition), as_dict=True)
    data_dict = {}
    for row in raw_data:
        account = row['account']
        month = row['month'].lower()
        budget_amount = row['budget_amount']
        percentage_allocation = row['percentage_allocation'] / 100
        
        if account not in data_dict:
            data_dict[account] = {
                'account': account,
                'august': 0,
                'september': 0,
                'october': 0,
                'november': 0,
                'december': 0,
                'january': 0,
                'february': 0,
                'march': 0,
                'april': 0,
                'may': 0,
                'june': 0,
                'july': 0
            }
        data_dict[account][month] += budget_amount * percentage_allocation
    
    data = list(data_dict.values())
    return data

def get_condition(filters):
    conditions = ""
    if filters.get("account"):
        conditions += " and ba.account='{}'".format(filters.get("account"))
    if filters.get("fiscal_year"):
        conditions += " and b.fiscal_year='{}'".format(filters.get("fiscal_year"))
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
        }
    ]
