from django.contrib import admin
from invoices.models import CareCode, Prestation, Patient


# class PrestationsInline(admin.TabularInline):
#     model = Prestation
#     extra = 2
# 

class CareCoreAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'gross_amount', 'net_amount' , 'is_private')
    search_fields = ['code', 'name']
    
class PrestationAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('patient', 'carecode', 'date')
    search_fields = ['patient__name', 'patient__first_name']
#     fieldsets = [
#         (None,               {'fields': ['patient', 'carecode']}),
#         ('Date information', {'fields': ['date'], 'classes': ['collapse']}),
#     ]
#     inlines = [PrestationsInline]


    
admin.site.register(CareCode, CareCoreAdmin)
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(Patient)

