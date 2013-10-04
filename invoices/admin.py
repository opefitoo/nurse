from django.contrib import admin
from django import forms 
from invoices.models import CareCode, Prestation, Patient, InvoiceItem

class CareCoreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'gross_amount' )
    search_fields = ['code', 'name']

class PatientAdmin(admin.ModelAdmin):
    list_filter = ('city', )
    list_display = ('name', 'first_name', 'phone_number','code_sn', 'participation_statutaire')
    search_fields = ['name', 'first_name', 'code_sn']
    
class PrestationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('patient', 'carecode', 'date', 'net_amount')
    search_fields = ['patient__name', 'patient__first_name']

class InvoiceItemAdminForm(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'display_prestations')
    
admin.site.register(CareCode, CareCoreAdmin)
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdminForm)
