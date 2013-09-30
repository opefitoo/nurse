from django.db import models
from setuptools.tests.doctest import is_private
import logging
import datetime

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
    city = models.CharField(max_length= 30)
    phone_number = models.CharField(max_length=30)
    participation_statutaire = models.BooleanField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
    
class InvoiceItem(models.Model):
    invoice_number = models.CharField(max_length = 50)
    date = models.DateField('Invoice date')
    invoice_sent = models.BooleanField()
    invoice_paid = models.BooleanField()
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'invoice# %s' % (self.invoice_number)
    
class Prestation(models .Model):
    patient = models.ForeignKey(Patient)
    carecode = models.ForeignKey(CareCode)
    date = models.DateTimeField('date')
    invoice_item = models.ForeignKey(InvoiceItem)
    @property
    def net_amount(self):
        "Returns the net amount"
        if not self.patient.participation_statutaire:
            return self.carecode.gross_amount
        return ((self.carecode.gross_amount * 88) / 100 )
    
    def save(self, *args, **kwargs):
        q = InvoiceItem.objects.filter(invoice_paid = False).select_related()        
        q.filter(prestation__patient = self.patient)
        if not q:
            newInvoice = InvoiceItem.objects.create(invoice_number = len(self.patient.name),
                                       date = datetime.date.today(),
                                       invoice_sent = False,
                                       invoice_paid = False)
            newInvoice.save()
            invoice_item = newInvoice
            print "***** q is emtpy"
            super(Prestation, self).save(*args, **kwargs) # Call the "real" save() method.        
        else:
            print "**** q is  %s" % q
            super(Prestation, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'code: %s - nom patient: %s' % (self.carecode.code , self.patient.name)

    
    
