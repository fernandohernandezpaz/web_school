from django.contrib import admin
from school.models import (Nationality, Profile, Course,
                           PersonalFile, Student)


# Admin Class for Catalogs
class CatalogsAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


# Register your models here.
admin.site.register(Nationality, CatalogsAdmin)
admin.site.register(Course, CatalogsAdmin)
admin.site.register(Profile)
admin.site.register(PersonalFile)
admin.site.register(Student)


