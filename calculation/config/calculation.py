from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Document"),
			"items": [
				{
					"type": "doctype",
					"name": "Rebate Calculation",
					"description":_("Rebate Calculation"),
					"onboard": 1,
				},
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Rebate Setting",
					"description":_("Rebate Setting"),
					"onboard": 1,
				},
			]
		},
	]