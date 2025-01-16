from django.db import models

# Create your models here.
class Valutak(models.Model):
    penznem = models.CharField(max_length=100)
    arfolyam = models.FloatField()
    valutanevek = models.CharField(max_length=100, default="   ")

    def __str__(self):
       	return f"{self.penznem} {self.arfolyam} {self.valutanevek}"
    

class mnb_deviza(models.Model):
    date = models.DateField()
    currency = models.CharField(max_length=10)
    value = models.FloatField()

    def __str__(self):
        return self.currency
    class Meta:
        verbose_name_plural="Valuta"

class mnb_name_good(models.Model):
    currency = models.CharField(max_length=10)
    longname = models.CharField(max_length=50)

    def __str__(self):
        return self.longname
    class Meta:
        verbose_name_plural="deviza neve"

class mnb_name(models.Model):
    smallname = models.CharField(max_length=5)
    longname = models.CharField(max_length=50)

    def __str__(self):
        return self.longname
    class Meta:
        verbose_name_plural="deviza neve"
