from django.views.generic import FormView
from .forms import MatriculationForm


# Create your views here.
class NewMatriculationFormView(FormView):
    template_name = 'form_matriculation.html'
    form_class = MatriculationForm
    form = MatriculationForm

    def get_context_data(self, **kwargs):
        context = super(NewMatriculationFormView, self).get_context_data(**kwargs)
        return context
