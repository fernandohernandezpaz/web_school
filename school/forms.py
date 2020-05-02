import datetime
from django import forms
from .models import Matriculation, GradeSection


class MatriculationForm(forms.ModelForm):
    class Meta:
        model = Matriculation
        exclude = ['student']

    CHOICES = Matriculation.STUDENT_STATUS_CHOICE

    global_style = 'width: 380px;'
    student = forms.CharField(
        label='Estudiante',
        widget=forms.CharField.widget(
            attrs={
                'id': 'student_input_search',
                'placeholder': u'Buscar Estudiante por Nombre Completo ó Codigo MINED',
                'style': global_style
            }
        ),
        help_text='Ingrese el nombre completo ó codigo MINED del estudiante.'
    )

    grade_seccion = forms.ModelChoiceField(
        label='Grado Sección',
        queryset=GradeSection.objects.all(),
        required=True,
        widget=forms.ModelChoiceField.widget(
            attrs={
                'id': 'grade_seccion_select',
                'disabled': True,
                'placeholder': 'Seleccione el grado sección'
            }
        )
    )

    teaching_year = forms.IntegerField(
        label=u'Año lectivo',
        widget=forms.IntegerField.widget(
            attrs={
                'id': 'teaching_year_input',
                'readonly': True,
                'value': int(datetime.date.today().year)
            }
        )
    )

    status = forms.ChoiceField(
        widget=forms.ChoiceField.widget(
            attrs={
                'id': 'status_select',
                'style': global_style,
                'disabled': True,
                'value': Matriculation.STUDENT_STATUS_CHOICE[1][0]
            }
        ),
        choices=CHOICES,
        required=True
    )
