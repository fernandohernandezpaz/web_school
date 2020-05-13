import json

from django.views.generic import FormView
from .forms import MatriculationForm
from .models import Matriculation, Student, Family
from django.db.models import F


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
