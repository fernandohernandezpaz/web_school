from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard


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
                    'school.Nationality', 'school.GradeSection'),
            column=2,
            order=0
        ))

        self.available_children.append(modules.LinkList)
        self.children.append(modules.LinkList(
            'Registros de Notas',
            children=[
                {
                    'title': 'Asignaturas por Aula',
                    'url': '/school/asignaturas_grado_seccion',
                    'external': False
                }
            ],
            column=1,
            order=0
        ))

        if context.request.user.is_superuser:
            self.children.append(modules.RecentActions(
                'Recent Actions',
                10,
                column=2,
                order=1
            ))
