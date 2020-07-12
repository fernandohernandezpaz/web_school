from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from school.models import Profile


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.AppList(
            'REGISTRO PARA UN NUEVO ESTUDIANTE',
            models=('school.Student', 'school.PersonalFile',
                    'school.Family', 'school.PaperCenter',
                    'school.Matriculation'),
            column=0,
            order=0
        ))

        self.children.append(modules.AppList(
            'REGISTRO PARA UN ESTUDIANTE DE REINGRESO',
            models='school.Matriculation',
            column=0,
            order=1
        ))

        self.children.append(modules.AppList(
            'CATALOGOS',
            models=('school.Gender', 'school.Section',
                    'school.Grade', 'school.Course',
                    'school.Nationality', 'school.GradeSection',
                    'school.Profile'),

            column=2,
            order=0
        ))

        is_teacher = Profile.objects. \
            filter(user_id=context.request.user.id). \
            exists()
        if is_teacher:
            from django.urls import reverse
            user_id = context.request.user.id
            url = reverse('school:lista_de_asignaturas_por_seccion', args=(user_id,))

            self.available_children.append(modules.LinkList)
            self.children.append(modules.LinkList(
                'Registros de Notas',
                children=[
                    {
                        'title': 'Asignaturas por Aula',
                        'url': url,
                        'external': False
                    }
                ],
                column=1,
                order=0
            ))

        if context.request.user.is_superuser:
            self.children.append(modules.RecentActions(
                'Acciones recientes',
                10,
                column=2,
                order=1
            ))
