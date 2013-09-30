from django.test import TestCase
from invoices.models import CareCode, Patient, Prestation

# Create your models here.
class CareCodeTestCase(TestCase):
    def setUp(self):
        carecode1 = CareCode.objects.create(code ='code1', 
                               name= "code1", 
                               description= "descr", 
                               gross_amount = 10)
        Patient.objects.create(code_sn ='codesn')
        Prestation.objects.create(patient =  Patient.objects.get(code_sn = 'codesn'), 
                                  carecode = carecode1)
    def test_simple_creation(self):
        code1 = CareCode.objects.get(name = "code1")
        self.assertEqual(code1.code, "code1")
        codes = CareCode.objects.all()
        self.assertEqual(len(list(codes)), 1)
        patients = Patient.objects.all()
        self.assertEqual(len(list(patients)), 1)
        
        prests = Prestation.objects.all()
        self.assertEqual(len(list(prests)), 1)
        
    def test_failing_test(self):
        self.assertFalse(False, "msg")
#     code = models.CharField(max_length=30)
#     name = models.CharField(max_length=50)
#     description = models.TextField(max_length=100)
#     # prix net = 88% du montant brut
#     # prix brut
#     gross_amount = models.DecimalField("montant brut", max_digits=5, decimal_places=2)
#     
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return '%s: %s' % (self.code, self.name) 
#     
# class Patient(models.Model):
#     code_sn = models.CharField(max_length=30)
#     first_name = models.CharField(max_length=30)
#     name = models.CharField(max_length=30)
#     address = models.TextField(max_length=30)
#     zipcode = models.CharField(max_length=10)
#     city = models.CharField(max_length= 30)
#     phone_number = models.CharField(max_length=30)
#     participation_statutaire = models.BooleanField()
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return '%s %s' % (self.first_name, self.last_name)
#     
# class Prestation(models .Model):
#     patient = models.ForeignKey(Patient)
#     carecode = models.ForeignKey(CareCode)
#     date = models.DateTimeField('date')
#     #invoice_item = models.ForeignKey(InvoiceItem)
#     @property
#     def net_amount(self):
#         "Returns the net amount"
#         if not self.patient.participation_statutaire:
#             return self.carecode.gross_amount
#         return ((self.carecode.gross_amount * 88) / 100 )
#     
#     def save(self, *args, **kwargs):
#         q = InvoiItem.objects.filter(__invoice_paid__ != True)
#         q.filter(__patient__code_sn__ == self.patient.code_sn)
#         
#         if self.name == "Yoko Ono's blog":
#             return # Yoko shall never have her own blog!
#         else:
#             super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
#     
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return 'code: %s - nom patient: %s' % (self.carecode.code , self.patient.name)
#     
# class InvoiceItem(models.Model):
#     invoice_number = models.CharField(max_length = 50)
#     date = models.DateField('Invoice date')
#     invoice_sent = models.BooleanField()
#     invoice_paid = models.BooleanField()
#     def __unicode__(self):  # Python 3: def __str__(self):
#         return 'invoice# %s' % (self.invoice_number)
#     
#     
