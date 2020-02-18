from django.db import models


# Create your models here.
class Person(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    names = models.CharField(max_length=50, verbose_name='Nombres')
    last_name = models.CharField(max_length=50, verbose_name='Apellidos')
    birthday = models.DateField(null=False, verbose_name='Fecha Nacimiento')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    register_date = models.DateField(auto_now_add=True, verbose_name='Fecha Registro')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='Género')
    status = models.BooleanField(default=True, verbose_name='Estado')
    created_user = models.CharField(max_length=64, null=True, blank=True, verbose_name='Creado por')
    updated_user = models.CharField(max_length=64, null=True, blank=True, verbose_name='Actualizado por')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s: %s" % (self.names, self.last_name)

    def age(self):
        import datetime
        return int((datetime.datetime.now() - self.birthday).days / 365.25)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'


class Teacher(models.Model):
    VOCATIONAL_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    person = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name='Docente')
    cedula = models.CharField(max_length=16, unique=True)
    vocation = models.CharField(max_length=2, choices=VOCATIONAL_CHOICES, verbose_name='Formacion')

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
