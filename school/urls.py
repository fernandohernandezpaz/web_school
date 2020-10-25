"""
monitoring URL Configuration. Included as root ''
"""
from django.urls import path
from .views import (NewMatriculationFormView,
                    NewViewCourseGradeSectionList,
                    NewRegisterNote)
from . import api, reports

app_name = 'school'

urlpatterns = [
    path('matricula', NewMatriculationFormView.as_view(), name='new_form_matriculation'),
    path('matricula/<int:id>/', NewMatriculationFormView.as_view(), name='matriculation_detail'),
    path('<int:teacher_id>/asignaturas_grado_seccion', NewViewCourseGradeSectionList.as_view(),
         name='lista_de_asignaturas_por_seccion'),
    path('<int:teacher_id>/grado_seccion_asignatura/<int:id>/registro_de_notas',
         NewRegisterNote.as_view(),
         name='lista_de_alumnos_por_asignatura'),

    # URL of apis
    path('guardar/nota', api.save_note, name='api_save_note'),
    path('school_space', api.get_school_space, name='api_school_space'),
    path('students', api.get_students, name='api_students'),
    path('matricula/guardar', api.save_form, name='api_save'),
    path('estadisticas/periodos/notas', api.statistics_period_notes, name='api_statistics_period_notes'),
    path('buscar/estudiante', api.find_student, name='api_find_student'),

    # URL of reports
    path('<int:teacher_id>/lista_asistencia/<int:grade_section_course_id>', reports.AttendanceReport.as_view(),
         name='report_attendance'),
    path('<int:teacher_id>/listado_notas/<int:grade_section_course_id>', reports.AcademicNotesReport.as_view(),
         name='report_academic_notes'),
    path('matricula/<int:id>/pdf/', reports.MatriculationReport.as_view(), name='report_matriculation')
]
