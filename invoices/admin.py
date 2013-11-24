from django.contrib import admin

from invoices.models import CareCode, Prestation, Patient, InvoiceItem
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

class CareCoreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'gross_amount')
    search_fields = ['code', 'name']

admin.site.register(CareCode, CareCoreAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_filter = ('city',)
    list_display = ('name', 'first_name', 'phone_number', 'code_sn', 'participation_statutaire')
    search_fields = ['name', 'first_name', 'code_sn']
admin.site.register(Patient, PatientAdmin)
    
class PrestationAdmin(AjaxSelectAdmin):
    date_hierarchy = 'date'
    list_display = ('patient', 'carecode', 'date')
    search_fields = ['patient__name', 'patient__first_name']
    list_filter = ('patient__name',)
    form = make_ajax_form( Prestation, {'patient': 'patient', 'carecode' : 'carecode'})
admin.site.register(Prestation, PrestationAdmin)
        
class InvoiceItemAdmin(AjaxSelectAdmin):
    from action import export_to_pdf
    list_display = ('invoice_number', 'patient', 'invoice_month', 'prestations_invoiced', 'invoice_sent' )
    list_filter =  ['invoice_date', 'patient__name', 'invoice_sent']
    search_fields = ['patient']
    actions = [export_to_pdf]
    form = make_ajax_form(InvoiceItem,{'patient':'patient_du_mois'})
admin.site.register(InvoiceItem, InvoiceItemAdmin)


