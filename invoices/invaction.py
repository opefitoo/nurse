# -*- coding: utf-8 -*-
import decimal

from django.http import HttpResponse
from django.utils.encoding import smart_unicode
import pytz
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.flowables import Spacer, PageBreak
from reportlab.platypus.para import Paragraph
from reportlab.platypus.tables import Table, TableStyle

from invoices.models import Patient, InvoiceItem
import datetime


def previous_months_invoices_march(modeladmin, request, queryset):
    
    response = HttpResponse(content_type='text')
    
    previous_month_patients = Patient.objects.raw("select p.id, p    .name, p.first_name "+  
        "from public.invoices_patient p, public.invoices_prestation prest "+
        "where p.id = prest.patient_id "+
        "and prest.date between '2014-03-01'::DATE and '2014-03-31'::DATE "+ 
        "and (select count(inv.id) from public.invoices_invoiceitem inv "+
        "where inv.invoice_date between '2014-03-01'::DATE and '2014-03-31'::DATE "+ 
        "and inv.patient_id = p.id) = 0" + 
        "group by p.id "+
        "order by p.name")
    invoice_counters = 0
    for p in previous_month_patients:
        invoiceitem = InvoiceItem(patient=p, 
                                  invoice_date=datetime.datetime(2014, 03, 31), 
                                  invoice_sent=False, 
                                  invoice_paid=False)
        invoiceitem.clean()
        invoiceitem.save()
        invoice_counters  = invoice_counters + 1 
    #response.message_user(request, "%s successfully created." % invoice_counters)
    
def previous_months_invoices_february(modeladmin, request, queryset):
    
    response = HttpResponse(content_type='text')

    previous_month_patients = Patient.objects.raw("select p.id, p    .name, p.first_name "+  
        "from public.invoices_patient p, public.invoices_prestation prest "+
        "where p.id = prest.patient_id "+
        "and prest.date between '2014-02-01'::DATE and '2014-02-28'::DATE "+ 
        "and (select count(inv.id) from public.invoices_invoiceitem inv "+
        "where inv.invoice_date between '2014-02-01'::DATE and '2014-02-28'::DATE "+ 
        "and inv.patient_id = p.id) = 0" + 
        "group by p.id "+
        "order by p.name")
    invoice_counters = 0
    for p in previous_month_patients:
        invoiceitem = InvoiceItem(patient=p, 
                                  invoice_date=datetime.datetime(2014, 02, 28), 
                                  invoice_sent=False, 
                                  invoice_paid=False)
        invoiceitem.clean()
        invoiceitem.save()
        invoice_counters  = invoice_counters + 1 
    #response.message_user(request, "%s successfully created." % invoice_counters)
