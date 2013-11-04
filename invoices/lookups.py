from ajax_select import LookupChannel

from invoices.models import Patient, InvoiceItem


class PatientLookup(LookupChannel):

    model = InvoiceItem 

    def get_query(self,q,request):
        return Patient.objects.all()
