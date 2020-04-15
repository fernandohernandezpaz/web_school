import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Nationality(models.Model):
    name = models.CharField(max_length=50, verbose_name='País')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'


class Gender(models.Model):
    name = models.CharField(max_length=20, verbose_name='Nombre')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'


class Section(models.Model):
    name = models.CharField(max_length=1, verbose_name='Seccion')
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = 'Seccion'
        verbose_name_plural = 'Secciones'


class Grade(models.Model):
    name = models.CharField(max_length=50, verbose_name='Grado')
    active = models.BooleanField(default=True, verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'


class Course(models.Model):
    name = models.CharField(max_length=50, null=True,
                            blank=True,
                            verbose_name='Nombre')
    active = models.BooleanField(default=True,
                                 verbose_name='Activo')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'


class GradeSection(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE,
                              verbose_name='Grado')
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                verbose_name='Seccion')

    def __str__(self):
        return '{} {}'.format(self.grade, self.section)

    class Meta:
        verbose_name = 'Grado Seccion'
        verbose_name_plural = 'Grados Secciones'
        unique_together = [['grade', 'section']]


class CourseGradeSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='Asignatura')
    grade_section = models.ForeignKey(GradeSection, on_delete=models.CASCADE,
                                      verbose_name='Grado Seccion')

    def __str__(self):
        return '{} {}'.format(self.course, self.grade_section)

    class Meta:
        verbose_name = 'Asignatura Grado Seccion'
        verbose_name_plural = 'Asignaturas Grados Secciones'
        unique_together = [['course', 'grade_section']]


class Profile(models.Model):
    VOCATIONAL_CHOICES = [
        ('PE', 'Pre-Escolar'),
        ('P', 'Primaria'),
        ('S', 'Secundaria'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Usuario')
    document = models.CharField(max_length=16, unique=True, null=False,
                                blank=False,
                                verbose_name='Cedula')
    vocation = models.CharField(max_length=2,
                                choices=VOCATIONAL_CHOICES,
                                verbose_name='Formación')
    cellphone = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            verbose_name='Teléfono')
    address = models.TextField(max_length=200, null=True,
                               blank=True,
                               verbose_name='Dirección')
    coursesgradesection = models.ManyToManyField(CourseGradeSection,
                                                 blank=True,
                                                 verbose_name='Asignaturas')

    def __str__(self):
        return "%s" % self.user

    class Meta:
        ordering = ['user']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Family(models.Model):
    FAMILY_ROLE_CHOICES = [
        ('PAPA', 'PAPA'),
        ('MAMA', 'MAMA'),
        ('HERMANO/A', 'HERMANO/A'),
        ('TIO/A', 'TIO/A'),
        ('ABUELO/A', 'ABUELO/A'),
    ]

    full_name = models.CharField(max_length=50,
                                 verbose_name='Nombre Completo')
    document = models.CharField(max_length=16, unique=True, null=False, blank=False,
                                verbose_name='Cédula')
    family_role = models.CharField(max_length=20, choices=FAMILY_ROLE_CHOICES,
                                   null=False, verbose_name='Rol Familiar')
    mobile = models.PositiveIntegerField(null=True, blank=True,
                                         verbose_name='Celular')
    cellphone = models.PositiveIntegerField(null=True, blank=True,
                                            verbose_name='Teléfono')
    tutor = models.BooleanField(default=False, verbose_name='Tutor')
    occupation = models.CharField(max_length=30, blank=True,
                                  verbose_name="Ocupación")

    def __str__(self):
        return '{}'.format(self.full_name)

    class Meta:
        verbose_name = 'Familiar'
        verbose_name_plural = 'Familiares'


class Student(models.Model):
    STUDENT_STATUS_CHOICE = [
        (1, 'Nuevo'),
        (2, 'Reingreso'),
        (3, 'Inactivo'),
    ]

    names = models.CharField(max_length=50,
                             verbose_name='Nombres')
    last_name = models.CharField(max_length=50,
                                 verbose_name='Apellidos')
    birthday = models.DateField(null=False,
                                verbose_name='Fecha Nacimiento')
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,
                               verbose_name='Género')
    nationality = models.ForeignKey(Nationality, on_delete=models.CASCADE,
                                    verbose_name='Nacionalidad')
    status = models.SmallIntegerField(choices=STUDENT_STATUS_CHOICE,
                                      verbose_name='Estado Estudiante')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Fecha de Registro')
    family_members = models.ManyToManyField(Family, blank=True,
                                            verbose_name='Familiares')

    def age(self):
        import datetime
        return int((datetime.datetime.now() - self.birthday).days / 365.25)

    def __str__(self):
        return '{} {}'.format(self.names, self.last_name)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'


class PersonalFile(models.Model):
    YES_OR_NOT_CHOICES = ((True, 'Si'), (False, 'No'))
    student = models.OneToOneField(Student, on_delete=models.CASCADE,
                                   verbose_name='Estudiante')
    have_brothers_center = models.BooleanField(choices=YES_OR_NOT_CHOICES, null=False,
                                               verbose_name='¿Tiene hermanos en el centro?')
    how_many = models.PositiveSmallIntegerField(null=True, blank=True,
                                                verbose_name='¿Cuántos?')
    religion = models.CharField(max_length=20, null=True, blank=False,
                                verbose_name='Religión')
    origin_center = models.CharField(max_length=50, null=True, blank=False,
                                     verbose_name='Centro de Procedencia')
    year_taken_origin_center = models.ForeignKey(Grade, on_delete=models.SET_NULL,
                                                 null=True, blank=True,
                                                 verbose_name='Año cursado del centro de procedencia')
    diseases = models.CharField(max_length=350, null=True, blank=True,
                                verbose_name='Enfermedades')
    in_emergencies_call = models.CharField(max_length=350, null=True, blank=True,
                                           verbose_name='En caso de emergencias llamar a')

    def __str__(self):
        return '{} {}'.format(self.student.names, self.student.last_name)

    class Meta:
        verbose_name = 'Expediente Personal'
        verbose_name_plural = 'Expedientes Personales'


class Matriculation(models.Model):
    STUDENT_STATUS_CHOICE = [
        (0, 'Inactivo'),
        (1, 'Activo'),
        (2, 'Finalizo Satisfactoriamente'),
        (3, 'Reprobado'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                verbose_name='Alumno')
    teaching_year = models.IntegerField(null=False,
                                        default=int(datetime.date.today().year),
                                        verbose_name='Año Lectivo')
    registration_date = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Fecha de Matricula')
    grade_section = models.ForeignKey(GradeSection,
                                      on_delete=models.CASCADE,
                                      verbose_name='Grado y Sección')
    status = models.SmallIntegerField(choices=STUDENT_STATUS_CHOICE,
                                      default=1,
                                      verbose_name='Estado')

    def __str__(self):
        return '{} {} - {}'.format(self.student.names,
                                   self.student.last_name,
                                   self.teaching_year)

    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'
        unique_together = [['student', 'teaching_year']]


class PaperCenter(models.Model):
    matriculation = models.ForeignKey(Matriculation, on_delete=models.CASCADE,
                                      verbose_name='Matricula')
    academic_notes = models.BooleanField(default=False,
                                         verbose_name='¿Entrego boletin de notas?')
    diploma = models.BooleanField(default=False,
                                  verbose_name='¿Entrego Diploma?')
    birth_certificate = models.BooleanField(default=False,
                                            verbose_name='¿Entrego Partida de nacimiento?')
    conduct_certificate = models.BooleanField(default=False,
                                              verbose_name='¿Entrego Certificado de conducta?')
    observations = models.TextField(null=True, blank=True,
                                    verbose_name='Observaciones')

    def __str__(self):
        return '{}'.format(self.matriculation)

    class Meta:
        verbose_name = 'Papeles para el Centro'
        verbose_name_plural = 'Papeles para el Centro'


class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='Asignatura')
    matriculation = models.ForeignKey(Matriculation,
                                      on_delete=models.CASCADE,
                                      verbose_name='Matricula')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,
                                verbose_name='Docente')
    bimonthly_I = models.PositiveIntegerField(null=True, blank=True,
                                              verbose_name='Bimensual I')
    bimonthly_II = models.PositiveIntegerField(null=True, blank=True,
                                               verbose_name='Bimensual II')
    biannual_I = models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name='Semestral I')
    bimonthly_III = models.PositiveIntegerField(null=True, blank=True,
                                                verbose_name='Bimensual III')
    bimonthly_IV = models.PositiveIntegerField(null=True, blank=True,
                                               verbose_name='Bimensual IV')
    biannual_II = models.PositiveIntegerField(null=True, blank=True,
                                              verbose_name='Semestral II')
    final = models.PositiveIntegerField(null=True, blank=True,
                                        verbose_name='Final')
    registration_date = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Fecha de Registro')

    def __str__(self):
        return '{} {}'.format(self.course.name, self.matriculation)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = [['matriculation', 'course']]


class NoteControlEdition(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE,
                             verbose_name='Nota')
    edit_field = models.CharField(max_length=10, verbose_name='Campo Edición')
    value_edit_field = models.IntegerField(verbose_name='Valor')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE,
                                   null=True, blank=True,
                                   verbose_name='Supervisor')
    registration_date = models.DateTimeField(auto_now_add=True,
                                             verbose_name='Fecha de Registro')

    class Meta:
        verbose_name = 'Nota Control Edición'
        verbose_name_plural = 'Notas Control Edición'
