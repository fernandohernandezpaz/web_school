from django.http import HttpResponse
from django.views.generic.list import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from .commons import get_current_year
from .models import Matriculation, CourseGradeSection
from django.contrib.auth.models import User
from constance import config


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
        context = {
            'nombre_colegio': config.NOMBRE_DEL_COLEGIO,
            'students': students,
            'grade_section_course': grade_section_course,
            'teacher': teacher,
            'year': year
        }
        template = get_template('report_html/attendance.html')
        html = template.render(context=context)
        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'attachment; filename="lista_asistencia {aula} {anio}.pdf"'.format(
            aula=grade_section_course, anio=year
        )

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response
