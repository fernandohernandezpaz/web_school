import json

from django.views.generic import FormView
from .forms import MatriculationForm
from .models import (Matriculation, Student, Family,
                     UserCoursesByYear, CourseGradeSection,
                     Note)
from django.db.models import F
from django.forms.models import model_to_dict
from django.views.generic.list import ListView
from .commons import get_current_year, CheckIsLoggin
from django.views.generic import TemplateView
from constance import config


def fill_with_data_from_db_or_empty(student, notes):
    keys = {'note_id': 'id', 'bi_i': 'bimonthly_I',
            'bi_ii': 'bimonthly_II', 'semestral_i': 'biannual_I',
            'bi_iii': 'bimonthly_III', 'bi_iv': 'bimonthly_IV',
            'semestral_ii': 'biannual_II', 'final': 'final'}
    if notes:
        notes_dict = model_to_dict(notes)
        for key in keys:
            key_db = keys[key]
            student[key] = notes_dict[key_db]
    else:
        for key in keys:
            student[key] = ''


# Create your views here.
class NewMatriculationFormView(CheckIsLoggin, FormView):
    template_name = 'form_matriculation.html'
    form_class = MatriculationForm
    form = MatriculationForm

    def get_context_data(self, **kwargs):
        context = super(NewMatriculationFormView, self).get_context_data(**kwargs)
        id = self.kwargs.get('id')
        if id:
            matriculation = Matriculation.objects. \
                get(id=id)
            matriculation_status_dict = dict((key, value) for key, value in Matriculation.STUDENT_STATUS_CHOICE)
            matriculation.status_name = matriculation_status_dict[matriculation.status]
            student = Student.objects. \
                get(id=matriculation.student_id)
            family = list({})
            if Family.objects.filter(student__id=student.id).exists():
                family = list(Student.objects.filter(id=student.id).
                              values(name=F('family_members__full_name'),
                                     rol=F('family_members__family_role'),
                                     tutor=F('family_members__tutor')))

            context['matriculation'] = matriculation
            context['student'] = student
            context['family'] = json.dumps(family)

        return context


class NewViewCourseGradeSectionList(CheckIsLoggin, ListView):
    model = UserCoursesByYear
    paginate_by = 15
    template_name = 'listview_coursesgradesection.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_id'] = self.kwargs['teacher_id']
        return context

    def get_queryset(self):
        queryset = UserCoursesByYear.objects. \
            filter(year=get_current_year(),
                   user_id=self.kwargs['teacher_id']). \
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


class NewRegisterNote(CheckIsLoggin, TemplateView):
    template_name = 'form_register_note.html'

    def get_context_data(self, **kwargs):
        context = {}
        grado_seccion_curso = CourseGradeSection.objects.get(pk=kwargs['id'])
        # getting a list of students with matriculation active and
        # they are registered in a specific course
        students = Matriculation.objects. \
            filter(teaching_year=get_current_year(),
                   grade_section__id=grado_seccion_curso.grade_section_id,
                   status=1). \
            values('id',  # id of matriculation
                   'student_id',
                   'student__code_mined',
                   'student__names',
                   'student__last_name')

        # creating keys of each note for each student
        for student in students:
            notes = Note.objects.filter(
                teacher_id=kwargs['teacher_id'],
                matriculation_id=student['id'],  # id of matriculation
                course_id=grado_seccion_curso.course_id
            ).first()
            fill_with_data_from_db_or_empty(student, notes)

        context['teacher_id'] = kwargs['teacher_id']
        context['students'] = students
        context['grade_section_course'] = grado_seccion_curso
        context['config'] = config
        return context
