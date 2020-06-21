from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   fullname = models.CharField(verbose_name="Nombre Completo",  max_length=256)
   address = models.CharField(verbose_name="Direccion de Entrega",  max_length=256)
   phonenumber = models.CharField(verbose_name="Numero de Telefono", max_length=10)

   def __str__(self):
      return self.fullname

