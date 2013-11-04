from django.db import models
from setuptools.tests.doctest import is_private
from django.core.exceptions import ValidationError
import logging
import datetime
from django.db.models import Q
import pytz


logger = logging.getLogger(__name__)

# Create your models here.
class CareCode(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    # prix net = 88% du montant brut
    # prix brut
    gross_amount = models.DecimalField("montant brut", max_digits=5, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s: %s' % (self.code, self.name) 
    
class Patient(models.Model):
    code_sn = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    address = models.TextField(max_length=30)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    participation_statutaire = models.BooleanField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s' % ( self.name.strip() , self.first_name.strip() )
    
class Prestation(models.Model):
    patient = models.ForeignKey(Patient)
    carecode = models.ForeignKey(CareCode)
    date = models.DateTimeField('date')
    @property
    def net_amount(self):
        "Returns the net amount"
        if not self.patient.participation_statutaire:
            return self.carecode.gross_amount
        return ((self.carecode.gross_amount * 88) / 100)    
    
#     def save(self, *args, **kwargs):
#         q = InvoiceItem.objects.filter(invoice_paid = False).select_related()        
#         q.filter(prestation__patient = self.patient)
#         if not q:
#             newInvoice = InvoiceItem.objects.create(invoice_number = len(self.patient.name),
#                                        date = datetime.date.today(),
#                                        invoice_sent = False,
#                                        invoice_paid = False)
#             newInvoice.save()
#             invoice_item = newInvoice
#             print "***** q is emtpy"
#             super(Prestation, self).save(*args, **kwargs) # Call the "real" save() method.        
#         else:
#             print "**** q is  %s" % q
#             super(Prestation, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'code: %s - nom patient: %s' % (self.carecode.code , self.patient.name)

class InvoiceItem(models.Model):
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField('Invoice date')
    invoice_sent = models.BooleanField()
    invoice_paid = models.BooleanField()
    patient = models.ForeignKey(Patient, related_name='patient')
    prestations = models.ManyToManyField(Prestation, related_name='prestations')
                                          #editable=False, null=True, blank=True)
    url = models.URLField(blank=True)
    def save(self, *args, **kwargs):
        super(InvoiceItem, self).save(*args, **kwargs)
        if self.pk is not None:
            print 'patient pk = %s' % self.patient.pk
            prestationsq = Prestation.objects.filter(date__month=self.invoice_date.month).filter(patient__pk=self.patient.pk)
            for p in prestationsq:
                self.prestations.add(p)
            super(InvoiceItem, self).save(*args, **kwargs)
    def prestations_invoiced(self):
        pytz_chicago = pytz.timezone("America/Chicago")
        return ', '.join([a.carecode.code + pytz_chicago.normalize(a.date).strftime(':%m/%d/%Y') for a in self.prestations.all()])
    @property
    def invoice_month(self):
        return self.invoice_date.strftime("%B %Y")
    
    def __get_patients_without_invoice(self, current_month):
        qinvoices_of_current_month = InvoiceItem.objects.filter(date__month=current_month.month)
        patients_pks_having_an_invoice = list()
        for i in qinvoices_of_current_month:
            patients_pks_having_an_invoice.append(i.patient.pk)
        return patients_pks_having_an_invoice
    
    def clean(self):
        # # don't allow patient to have more than one invoice for a month
        iq = InvoiceItem.objects.filter(patient__pk=self.patient.pk).filter(Q(invoice_date__month=self.invoice_date.month))
        if iq.exists():
            raise ValidationError('Patient %s has already an invoice for the month ''%s'' ' % (self.patient , self.invoice_date.strftime('%B')))
        prestationsq = Prestation.objects.filter(date__month=self.invoice_date.month).filter(patient__pk=self.patient.pk)
        if not prestationsq.exists():
            raise ValidationError('Cannot create an invoice for month ''%s'' because there were no medical service ' % self.invoice_date.strftime('%B'))

    def __unicode__(self):  # Python 3: def __str__(self):
        return 'invocie no.: %s - nom patient: %s' % (self.invoice_number , self.patient)
    
