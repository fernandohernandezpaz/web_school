"""
monitoring URL Configuration. Included as root ''
"""
from django.urls import path
from .views import (NewMatriculationFormView,
                    NewViewCourseGradeSectionList,
                    NewRegisterNote)
from . import api

app_name = 'school'

urlpatterns = [
    path('matricula', NewMatriculationFormView.as_view(), name='new_form_matriculation'),
    path('matricula/<int:id>', NewMatriculationFormView.as_view(), name='matriculation_detail'),
    path('school_space', api.get_school_space, name='api_school_space'),
    path('students', api.get_students, name='api_students'),
    path('matricula/guardar', api.save_form, name='api_save'),
    path('<int:teacher_id>/asignaturas_grado_seccion', NewViewCourseGradeSectionList.as_view(),
         name='lista_de_asignaturas_por_seccion'),
    path('<int:teacher_id>/grado_seccion_asignatura/<int:id>/registro_de_notas',
         NewRegisterNote.as_view(),
         name='lista_de_alumnos_por_asignatura'),
]
