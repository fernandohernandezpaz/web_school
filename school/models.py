from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Nationality(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='País')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
