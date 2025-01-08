from django.db import models

# Create your models here.
class Valutak(models.Model):
    penznem = models.CharField(max_length=100)
    arfolyam = models.FloatField()
    valutanevek = models.CharField(max_length=100, default="   ")

    def __str__(self):
       	return f"{self.penznem} {self.arfolyam} {self.valutanevek}"