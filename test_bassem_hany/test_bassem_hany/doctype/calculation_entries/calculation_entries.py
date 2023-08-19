# Copyright (c) 2023, Bassem Hany and contributors
# For license information, please see license.txt

import frappe,datetime,calendar
from frappe.model.document import Document
from datetime import datetime as dt
from frappe.utils import getdate
from frappe.utils import formatdate
from itertools import groupby
from operator import itemgetter

@frappe.whitelist()
def get_serial(customer):
	serial=frappe.db.sql(""" select max(serial) from `tabCalculation Entries` where customer=%s """,(str(customer)))[0][0]
	if not serial:
		serial=1
	else:
		serial=serial+1
	return serial

class CalculationEntries(Document):
	# pass
	@frappe.whitelist()
	def before_save(self):
		kw=0
		kwh=0
		for record in self.records:
			kw+=record.kw_record
			kwh+=record.kwh_record
			t=record.date_time
			date=getdate(str(record.date_time))
			record.year=date.year
			record.month=date.day
			t = dt.strptime(t, '%Y-%m-%d %H:%M:%S')
			record.time=t.strftime('%H:%M:%S')
			if record.time<"5:59" and record.time>"23:00":
				record.tariff_period="Low"
			else:
				record.tariff_period="High"
		avg_kw=kw/float(len(self.records))
		avg_kwh=kwh/float(len(self.records))
		self.avg_kw=avg_kw
		self.avg_kwh=avg_kwh
		records=frappe.db.sql(""" select year,month,tariff_period,kw_record,kwh_record from `tabEntries` where parent=%s """,(str(self.name)))
		records_list=[]
		for i in records:
			record={}
			record["year"]=i[0]
			record["month"]=i[1]
			record["tariff_period"]=i[2]
			record["kw_record"]=i[3]
			record["kwh_record"]=i[4]
			records_list.append(record)
		records_list=sorted(records_list,key = itemgetter('year','month','tariff_period'))
		for key, value in groupby(records_list,key = (itemgetter('year','month'))):
			x=0
			y=0
			for k in value:
				x+=1
				y+=k["kwh_record"]
			avg_kwh_for_month=y/x
			low_tariff=0.1*avg_kwh_for_month
			high_tariff=0.3*avg_kwh_for_month
			self.append('monthly_average_tariff',{'idx':x-1,'month':calendar.month_name[k['month']],'year':k['year'],'low_tariff':low_tariff,'high_tariff':high_tariff})