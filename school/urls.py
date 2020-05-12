"""
monitoring URL Configuration. Included as root ''
"""
from django.urls import path
from .views import NewMatriculationFormView
from . import api

app_name = 'school'

urlpatterns = [
    path('matricula', NewMatriculationFormView.as_view(), name='new_form_matriculation'),
    path('matricula/<int:id>', NewMatriculationFormView.as_view(), name='matriculation_detail'),
    path('school_space', api.get_school_space, name='api_school_space'),
    path('students', api.get_students, name='api_students'),
    path('matricula/guardar', api.save_form, name='api_save'),
]
