from django.db import models
from django.contrib.auth.models import User

GRADE_CHOICES = [
    ('I', '1er Nivel'),
    ('II', '2do Nivel'),
    ('III', '3er Nivel'),
    ('1er', '1er Grado'),
    ('2do', '2do Grado'),
    ('3er', '3er Grado'),
    ('4to', '4to Grado'),
    ('5to', '5to Grado'),
    ('6to', '6to Grado'),
    ('7mo', '7mo Grado'),
    ('8vo', '8vo Grado'),
    ('9no', '9no Grado'),
    ('10mo', '10mo Grado'),
    ('11vo', '11vo Grado'),
]


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


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Nombre')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'


class PersonalFile(models.Model):
    YES_OR_NOT_CHOICES = ((True, 'Si'), (False, 'No'))
    have_brothers_center = models.BooleanField(choices=YES_OR_NOT_CHOICES, null=False,
                                               verbose_name='¿Tiene hermanos en el centro?')
    how_many = models.PositiveSmallIntegerField(null=True, blank=True,
                                                verbose_name='¿Cuántos?')
    religion = models.CharField(max_length=20, null=True, blank=False,
                                verbose_name='Religión')
    origin_center = models.CharField(max_length=50, null=True, blank=False,
                                     verbose_name='Centro de Procedencia')
    year_taken_origin_center = models.CharField(max_length=4, choices=GRADE_CHOICES, null=True,
                                                verbose_name='Año cursado del centro de procedencia')
    diseases = models.CharField(max_length=350, null=True, blank=True,
                                verbose_name='Enfermedades')
    in_emergencies_call = models.CharField(max_length=350, null=True, blank=True,
                                           verbose_name='En caso de emergencias llamar a')

    def __str__(self):
        return self.have_brothers_center

    class Meta:
        verbose_name = 'Expediente Personal'
        verbose_name_plural = 'Expedientes Personales'
