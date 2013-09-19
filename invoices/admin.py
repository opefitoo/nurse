from django.contrib import admin
from invoices.models import CareCode, Prestation, Patient


class CareCoreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'gross_amount', 'net_amount' , 'is_private')
    search_fields = ['code', 'name']

class PatientAdmin(admin.ModelAdmin):
    list_filter = ('city', )
    list_display = ('name', 'first_name', 'phone_number','code_sn')
    search_fields = ['name', 'first_name', 'code_sn']
    
class PrestationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('patient', 'carecode', 'date')
    search_fields = ['patient__name', 'patient__first_name']

    
admin.site.register(CareCode, CareCoreAdmin)
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(Patient, PatientAdmin)

