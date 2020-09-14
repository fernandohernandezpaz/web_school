from django.http import HttpResponse
from django.views.generic.list import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from .commons import get_current_year
from .models import Matriculation, CourseGradeSection, Student
from django.contrib.auth.models import User
from constance import config
from .commons import fields_note_spanish


def sendPDF(html, title):
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(title)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


class AttendanceReport(View):

    def get(self, request, *args, **kwargs):
        grade_section_course_id = kwargs.get('grade_section_course_id')
        teacher_id = kwargs.get('teacher_id')

        grade_section_course = CourseGradeSection.objects.get(pk=grade_section_course_id)
        teacher = User.objects.get(pk=teacher_id)

        year = get_current_year()

        students = Matriculation.objects. \
            filter(teaching_year=year,
                   grade_section__id=grade_section_course.grade_section_id,
                   status=1). \
            values('student__code_mined',
                   'student__names',
                   'student__last_name')
        title = 'Lista de asistencia {} {}'.format(grade_section_course, year)
        context = {
            'nombre_colegio': config.NOMBRE_DEL_COLEGIO,
            'students': students,
            'grade_section_course': grade_section_course,
            'teacher': teacher,
            'year': year,
            'title': title
        }
        template = get_template('report_html/attendance.html')
        html = template.render(context=context)

        return sendPDF(html, title)


class AcademicNotesReport(View):

    def get(self, request, *args, **kwargs):
        grade_section_course_id = kwargs.get('grade_section_course_id')
        teacher_id = kwargs.get('teacher_id')

        grade_section_course = CourseGradeSection.objects.get(pk=grade_section_course_id)
        teacher = User.objects.get(pk=teacher_id)

        year = get_current_year()

        students = Matriculation.objects. \
            filter(teaching_year=year,
                   grade_section__id=grade_section_course.grade_section_id,
                   status=1). \
            values('student__names',
                   'student__code_mined',
                   'student__last_name',
                   'note__bimonthly_I',
                   'note__bimonthly_II',
                   'note__bimonthly_III',
                   'note__bimonthly_IV',
                   'note__biannual_I',
                   'note__biannual_II',
                   'note__final'
                   )
        title = 'Notas de {} {}'.format(grade_section_course, year)
        context = {
            'nombre_colegio': config.NOMBRE_DEL_COLEGIO,
            'students_notes': students,
            'grade_section_course': grade_section_course,
            'teacher': teacher,
            'columnas': fields_note_spanish.values(),
            'year': year,
            'title': title
        }
        template = get_template('report_html/academic_notes.html')
        html = template.render(context=context)
        return sendPDF(html, title)


class MatriculationReport(View):

    def get(self, request, *args, **kwargs):
        matriculation_id = kwargs.get('id')

        matriculation = Matriculation.objects.get(pk=matriculation_id)
        year = matriculation.teaching_year
        title = 'Matricula {} {}'.format(year, matriculation.student)
        context = {
            'logo': config.LOGO_DEL_COLEGIO,
            'location': config.LOCACION_DEL_COLEGIO,
            'nombre_colegio': config.NOMBRE_DEL_COLEGIO,
            'year': year,
            'title': title,
            'matriculation': matriculation,
            'parents': {
                'papa': None,
                'mama': None
            },
            'hermanos': ''
        }

        if matriculation.student.family_members:
            for familiar in matriculation.student.family_members.all():
                if familiar.tutor and (familiar.mobile or familiar.phone):
                    context['tutor'] = familiar
                if familiar.family_role == 'PAPA':
                    context['parents']['papa'] = familiar
                if familiar.family_role == 'MAMA':
                    context['parents']['mama'] = familiar
                if familiar.family_role == 'HERMANO/A':
                    context['hermanos'] = '{}, {}'.format(familiar.full_name, context['hermanos'])
        context['hermanos'] = '{}.'.format(context['hermanos'][:-2])

        template = get_template('report_html/matriculation.html')
        html = template.render(context=context)
        return sendPDF(html, title)
