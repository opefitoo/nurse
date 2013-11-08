from django.db import models
from django.core.exceptions import ValidationError
import logging
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
    
    def get_patients_that_have_prestations(self, monthyear):
        ##XXX use this later for raw sql
#         Patient.objects.raw("select p.name, p.first_name " 
#         + " from public.invoices_patient p, public.invoices_prestation prest"
#         + " where p.id = prest.patient_id"
#         + " and prest.date between '2013-10-01'::DATE and '2013-10-31'::DATE group by p.id" % (start_date, end_date)
        
        patients_sans_facture = Patient.objects.raw("select p.name, p.first_name "+  
        "from public.invoices_patient p, public.invoices_prestation prest "+
        "where p.id = prest.patient_id "+
        "and prest.date between '2013-10-01'::DATE and '2013-10-31'::DATE "+ 
        "and (select count(inv.id) from public.invoices_invoiceitem inv "+
        "where inv.invoice_date between '2013-10-01'::DATE and '2013-10-31'::DATE "+ 
        "and inv.patient_id = p.id) = 0 "+
        "group by p.id "+
        "order by p.name")
        return patients_sans_facture
       
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
    
    def clean(self):
        "if same prestation same date same code same patient, disallow creation"
        prestationsq = Prestation.objects.filter(date=self.date).filter(patient__pk=self.patient.pk).filter(carecode__pk=self.carecode.pk)
        if prestationsq.exists():
            raise ValidationError('Cannot create medical service "code:%s on:%s for:%s" because is already exists' % (self.carecode,
                                                                                                                            self.date.strftime('%d-%m-%Y'),
                                                                                                                            self.patient ))
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return 'code: %s - nom patient: %s' % (self.carecode.code , self.patient.name)

class InvoiceItem(models.Model):
    invoice_number = models.CharField(max_length=50)
    accident_id = models.CharField(max_length=30, help_text=u"Numero d'accident est facultatif", null=True, blank=True)
    accident_date = models.DateField( help_text=u"Date d'accident est facultatif", null=True, blank=True)
    invoice_date = models.DateField('Invoice date')
    invoice_sent = models.BooleanField()
    invoice_paid = models.BooleanField()
    patient = models.ForeignKey(Patient, related_name='patient', help_text='choisir parmi ces patients pour le mois precedent')
    prestations = models.ManyToManyField(Prestation, related_name='prestations', editable=False, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super(InvoiceItem, self).save(*args, **kwargs)
        if self.pk is not None:
            prestationsq = Prestation.objects.filter(date__month=self.invoice_date.month).filter(date__year=self.invoice_date.year).filter(patient__pk=self.patient.pk)
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
        iq = InvoiceItem.objects.filter(patient__pk=self.patient.pk).filter(
                                                                            Q(invoice_date__month=self.invoice_date.month) & Q(invoice_date__year=self.invoice_date.year)
                                                                            )
        if iq.exists():
            raise ValidationError('Patient %s has already an invoice for the month ''%s'' ' % (self.patient , self.invoice_date.strftime('%B')))
        prestationsq = Prestation.objects.filter(date__month=self.invoice_date.month).filter(date__year=self.invoice_date.year).filter(patient__pk=self.patient.pk)
        if not prestationsq.exists():
            raise ValidationError('Cannot create an invoice for ''%s '' because there were no medical service ' % self.invoice_date.strftime('%B-%Y'))

    def __unicode__(self):  # Python 3: def __str__(self):
        return 'invocie no.: %s - nom patient: %s' % (self.invoice_number , self.patient)
    
