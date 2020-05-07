# -*- coding: utf-8 -*-
# Copyright (c) 2020, Rico Nova and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class RebateCalculation(Document):
	

	def validate(self):
		# do calculation
		total_amount = 0
		for i in self.rebate_calculation_child :

			i.column_d = float(i.invoice_amount) * (float(i.column_d_setting) / 100)
			i.column_e = float(i.column_d) / float(i.column_e_setting)
			i.amount = float(i.invoice_amount) - float(i.column_d)
			total_amount = total_amount + float(i.amount)

		self.total_amount = total_amount




@frappe.whitelist()
def sales_invoice_submit(doc,method):

	# penambahan comment buat test git

	rebate_setting = frappe.get_single("Rebate Setting")
	column_e = 0
	column_d = 0

	check_customer_ada = 0

	if rebate_setting.rebate_setting_child :
		for rs in rebate_setting.rebate_setting_child :
			if rs.customer_id == doc.customer :

				check_customer_ada = 1
				column_e = rs.column_e
				column_d = rs.column_d

	if check_customer_ada == 1 :


		# branch
		customer_id = doc.customer
		customer_name = doc.name_customer
		
		year = str(doc.posting_date).split("-")[0]
		month_angka = str(doc.posting_date).split("-")[1]
		month_huruf = ""

		if month_angka == "01" :
			month_huruf = "January"
		elif month_angka == "02" :
			month_huruf = "February"
		elif month_angka == "03" :
			month_huruf = "March"
		elif month_angka == "04" :
			month_huruf = "April"
		elif month_angka == "05" :
			month_huruf = "May"
		elif month_angka == "06" :
			month_huruf = "June"
		elif month_angka == "07" :
			month_huruf = "July"
		elif month_angka == "08" :
			month_huruf = "August"
		elif month_angka == "09" :
			month_huruf = "September"
		elif month_angka == "10" :
			month_huruf = "October"
		elif month_angka == "11" :
			month_huruf = "November"
		elif month_angka == "12" :
			month_huruf = "December"

		kombinasi_nama = customer_name +" | "+ month_huruf + " " + year

		cek_dulu = frappe.get_value("Rebate Calculation", {"name":kombinasi_nama}, "name")

		if cek_dulu :

			# ada dokumennya
			get_doc = frappe.get_doc("Rebate Calculation", kombinasi_nama)

			if get_doc.rebate_calculation_child :

				count = 0
				for i in get_doc.rebate_calculation_child :
					if i.branch == customer_id :

						i.invoice_amount = float(i.invoice_amount) + float(doc.grand_total)

						i.column_d = float(i.invoice_amount) * (float(column_d) / 100)
						i.column_e = float(i.column_d) / float(column_e)
						i.amount = float(i.invoice_amount) - float(i.column_d)

						count = 1

				if count == 0 :
					new_row = get_doc.append("rebate_calculation_child", {})

					new_row.invoice_amount = float(doc.grand_total)
					new_row.branch = doc.customer
					new_row.column_d_setting = column_d
					new_row.column_e_setting = column_e

					new_row.column_d = float(new_row.invoice_amount) * (float(new_row.column_d_setting) / 100)
					new_row.column_e = float(new_row.column_d) / float(new_row.column_e_setting)
					new_row.amount = float(new_row.invoice_amount) - float(new_row.column_d)




				total_count = 0
				for i in get_doc.rebate_calculation_child :
					total_count = total_count + float(i.amount)

				get_doc.total_amount = total_count

			get_doc.flags.ignore_permission = True
			get_doc.save()


		else :

			# ada dokumennya
			new_doc = frappe.new_doc("Rebate Calculation")

			new_doc.document_name = kombinasi_nama
			new_doc.month = month_huruf
			new_doc.year = year
			new_doc.customer = customer_name
			
			new_row = new_doc.append("rebate_calculation_child", {})
			new_row.branch = doc.customer
			new_row.invoice_amount = float(doc.grand_total)
			new_row.column_d_setting = column_d
			new_row.column_e_setting = column_e
			
			new_row.column_d = float(new_row.invoice_amount) * (float(new_row.column_d_setting) / 100)
			new_row.column_e = float(new_row.column_d) / float(new_row.column_e_setting)
			new_row.amount = float(new_row.invoice_amount) - float(new_row.column_d)


			new_doc.total_amount = float(doc.grand_total)
			new_doc.flags.ignore_permission = True
			new_doc.save()





@frappe.whitelist()
def sales_invoice_cancel(doc,method):

	rebate_setting = frappe.get_single("Rebate Setting")


	column_e = 0
	column_d = 0

	check_customer_ada = 0

	if rebate_setting.rebate_setting_child :
		for rs in rebate_setting.rebate_setting_child :
			if rs.customer_id == doc.customer :

				check_customer_ada = 1
				column_e = rs.column_e
				column_d = rs.column_d

	if check_customer_ada == 1 :

		# branch
		customer_id = doc.customer
		customer_name = doc.name_customer
		
		year = str(doc.posting_date).split("-")[0]
		month_angka = str(doc.posting_date).split("-")[1]
		month_huruf = ""

		if month_angka == "01" :
			month_huruf = "January"
		elif month_angka == "02" :
			month_huruf = "February"
		elif month_angka == "03" :
			month_huruf = "March"
		elif month_angka == "04" :
			month_huruf = "April"
		elif month_angka == "05" :
			month_huruf = "May"
		elif month_angka == "06" :
			month_huruf = "June"
		elif month_angka == "07" :
			month_huruf = "July"
		elif month_angka == "08" :
			month_huruf = "August"
		elif month_angka == "09" :
			month_huruf = "September"
		elif month_angka == "10" :
			month_huruf = "October"
		elif month_angka == "11" :
			month_huruf = "November"
		elif month_angka == "12" :
			month_huruf = "December"

		kombinasi_nama = customer_name +" | "+ month_huruf + " " + year

		cek_dulu = frappe.get_value("Rebate Calculation", {"name":kombinasi_nama}, "name")

		if cek_dulu :

			# ada dokumennya
			get_doc = frappe.get_doc("Rebate Calculation", kombinasi_nama)

			if get_doc.rebate_calculation_child :

				count = 0
				for i in get_doc.rebate_calculation_child :
					if i.branch == customer_id :

						i.invoice_amount = float(i.invoice_amount) - float(doc.grand_total)

						i.column_d_setting = column_d
						i.column_e_setting = column_e
						

						i.column_d = float(i.invoice_amount) * (float(i.column_d_setting) / 100)
						i.column_e = float(i.column_d) / float(i.column_e_setting)
						i.amount = float(i.invoice_amount) - float(i.column_d)

						count = 1


				total_count = 0
				for i in get_doc.rebate_calculation_child :
					total_count = total_count + float(i.amount)

				get_doc.total_amount = total_count

			get_doc.flags.ignore_permission = True
			get_doc.save()
