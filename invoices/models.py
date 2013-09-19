from django.db import models
from setuptools.tests.doctest import is_private

# Create your models here.
class CareCode(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    # prix net = 88% du montant brut
    # prix brut
    gross_amount = models.DecimalField("montant brut", max_digits=5, decimal_places=2)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.code + ":" +self.name 
    
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
        return self.name + " " + self.first_name
    
class Prestation(models .Model):
    patient = models.ForeignKey(Patient)
    carecode = models.ForeignKey(CareCode)
    date = models.DateTimeField('date')
    @property
    def net_amount(self):
        "Returns the net amount"
        if not self.patient.participation_statutaire:
            return self.carecode.gross_amount
        return ((self.carecode.gross_amount * 88) / 100 )
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return "code:" + self.carecode.code + "- nom patient:" + self.patient.name
    
