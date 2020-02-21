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


class Profile(models.Model):
    VOCATIONAL_CHOICES = [
        ('P', 'Primaria'),
        ('S', 'Secundaria'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    document = models.CharField(max_length=16, unique=True, null=False, blank=False, verbose_name='Cedula')
    vocation = models.CharField(max_length=2, choices=VOCATIONAL_CHOICES, verbose_name='Formación')
    cellphone = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Teléfono')
    address = models.TextField(max_length=200, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return "%s" % self.user

    class Meta:
        ordering = ['user']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
