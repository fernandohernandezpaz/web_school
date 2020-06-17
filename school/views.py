import json

from django.views.generic import FormView
from .forms import MatriculationForm
from .models import Matriculation, Student, Family, UserCoursesByYear, CourseGradeSection
from django.db.models import F
from django.views.generic.list import ListView
from .commons import get_current_year
from django.views.generic import TemplateView
from constance import config


# Create your views here.
class NewMatriculationFormView(FormView):
    template_name = 'form_matriculation.html'
    form_class = MatriculationForm
    form = MatriculationForm

    def get_context_data(self, **kwargs):
        context = super(NewMatriculationFormView, self).get_context_data(**kwargs)
        id = self.kwargs.get('id')
        if id:
            matriculacion = Matriculation.objects. \
                get(id=id)
            student = Student.objects. \
                get(id=matriculacion.student_id)
            family = list({})
            if Family.objects.filter(student__id=student.id).exists():
                family = list(Student.objects.filter(id=student.id).
                              values(name=F('family_members__full_name'),
                                     rol=F('family_members__family_role'),
                                     tutor=F('family_members__tutor')))

            context['matriculacion'] = matriculacion
            context['student'] = student
            context['family'] = json.dumps(family)

        return context


class NewViewCourseGradeSectionList(ListView):
    model = UserCoursesByYear
    paginate_by = 15
    template_name = 'listview_coursesgradesection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = UserCoursesByYear.objects. \
            filter(year=get_current_year()). \
            values(curso=F('coursesgradesection__course__name'),
                   curso_id=F('coursesgradesection__course_id'),
                   grado=F('coursesgradesection__grade_section__grade__name'),
                   grado_id=F('coursesgradesection__grade_section__grade_id'),
                   seccion=F('coursesgradesection__grade_section__section__name'),
                   seccion_id=F('coursesgradesection__grade_section__section_id'),
                   grado_seccion=F('coursesgradesection__grade_section'),
                   grado_seccion_id=F('coursesgradesection__grade_section__id'),
                   grado_seccion_curso_id=F('coursesgradesection__id'))

        return queryset


class NewRegisterNote(TemplateView):
    template_name = 'form_register_note.html'

    def get_context_data(self, **kwargs):
        context = {}
        grado_seccion_curso = CourseGradeSection.objects.get(pk=kwargs['id'])
        queryset = Matriculation.objects. \
            filter(teaching_year=get_current_year(),
                   grade_section__id=grado_seccion_curso.grade_section_id,
                   status=1). \
            values('student__code_mined',
                   'student__names',
                   'student__last_name')
        context['students'] = queryset
        context['grade_section_course'] = grado_seccion_curso
        context['config'] = config
        return context
