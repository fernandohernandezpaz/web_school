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
            'CATALOGOS',
            models=('school.Gender', 'school.Section',
                    'school.Grade', 'school.Course',
                    'school.Nationality', 'school.GradeSection'),
            column=0,
            order=0
        ))
        #  self.children.append(modules.AppList(
        #     _('Quick Liks'),
        #   models=('monitoring.Project', 'monitoring.Organization',
        #           'monitoring.Contact', 'monitoring.Profile',
        #            'auth.User', 'auth.Group', 'auth.Permission',
        #           'constance.Config', 'monitoring.ProjectContact'),
        #   column=0,
        #   order=0
        # ))

        if context.request.user.is_superuser:
            self.children.append(modules.RecentActions(
                'Recent Actions',
                10,
                column=2,
                order=1
            ))
