from django.db import models

# Create your models here.


class Precios_Excel(models.Model):  # this model.Model lest us create a class and save it on database
    nombre = models.CharField(verbose_name="Nombre",  max_length=50)
    excel_file = models.FileField(upload_to='precios_excels/')

    def __str__(self):
        return self.nombre