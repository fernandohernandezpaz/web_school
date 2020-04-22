from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from jet.admin import CompactInline
from school.models import (Nationality, Profile, Course,
                           PersonalFile, Student, Grade,
                           Family, Gender, Matriculation,
                           PaperCenter, Note, Section,
                           GradeSection, CourseGradeSection,
                           NoteControlEdition)
from constance.admin import ConstanceAdmin, ConstanceForm, Config


# Inlines
class ProfileInline(admin.TabularInline):
    model = Profile


class PersonalFileInline(admin.StackedInline):
    model = PersonalFile


class MatriculationInline(CompactInline):
    model = Matriculation
    readonly_fields = ('teaching_year',)


class PaperCenterInline(admin.StackedInline):
    model = PaperCenter


# Admin Class for Catalogs
class CatalogsAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


class MatriculationAdmin(admin.ModelAdmin):
    readonly_fields = ['teaching_year']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [
        PersonalFileInline,
        MatriculationInline,
        PaperCenterInline
    ]

    # show the importants field of the model
    list_display = ('fullname', 'gender', 'nationality', 'status')
    # quantity of register per page
    list_per_page = 20
    # order the registrar by
    ordering = ['-names']
    # convert field to link to go the change form.
    # can be the same fields fo list_display
    list_display_links = ('fullname',)
    # searchible fields
    search_fields = ['names', 'last_name']
    # define the fields that can be selects
    list_filter = [
        'gender',
        'nationality',
        'status'
    ]
    # define the distribution and order of the fields of the model
    fieldsets = [
        ('Información General del Estudiante',
         {'fields': ['names', 'last_name', 'birthday',
                     'gender', 'nationality',
                     'status', 'family_members',
                     'code_mined']}),
    ]

    # method to concat names and last_name field
    def fullname(self, student):
        return u'{names} {last_names}'.format(names=student.names,
                                              last_names=student.last_name)

    # method.short_description, you define a label
    fullname.short_description = 'Nombre Completo del Estudiante'

    class Media:
        js = ('js/validations_registration_student.js',)


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    pass
    # show the importants field of the model
    list_display = ('full_name', 'family_role', 'tutor')
    # quantity of register per page
    list_per_page = 20
    # order the registrar by
    ordering = ['-full_name']
    # convert field to link to go the change form.
    # can be the same fields fo list_display
    list_display_links = ('full_name',)
    # searchible fields
    search_fields = ['full_name', 'family_role']
    # define the fields that can be selects
    list_filter = [
        'family_role',
        'tutor',

    ]
    # define the distribution and order of the fields of the model
    fieldsets = [
        ('Información General del Familiar',
         {'fields': ['full_name', 'document', 'family_role',
                     'mobile', 'cellphone',
                     'tutor', 'occupation']}),
    ]

    # method to concat names and last_name field
    def full_name(self, family):
        return u'{full_name}'.format(full_name=family.full_name)

    # method.short_description, you define a label
    full_name.short_description = 'Nombre Completo del Familiar'

    class Media:
        css = {
            'all': ('css/own_styles.css',),
        }


class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline]


class ConfigAdmin(ConstanceAdmin):
    pass


# Unregister Models
admin.site.unregister(User)
admin.site.unregister([Config])

# Register your models here.
admin.site.register(Nationality, CatalogsAdmin)
admin.site.register(Course, CatalogsAdmin)
admin.site.register(Gender, CatalogsAdmin)
admin.site.register(Grade, CatalogsAdmin)
admin.site.register(Section, CatalogsAdmin)
admin.site.register(Profile)
admin.site.register(PersonalFile)
# admin.site.register(Family, FamilyAdmin)
admin.site.register(Matriculation, MatriculationAdmin)
admin.site.register(PaperCenter)
admin.site.register(Note)
admin.site.register(GradeSection)
admin.site.register(CourseGradeSection)
admin.site.register(NoteControlEdition)
admin.site.register(User, MyUserAdmin)
admin.site.register([Config], ConfigAdmin)
