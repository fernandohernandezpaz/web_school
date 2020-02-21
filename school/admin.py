from django.contrib import admin
from school.models import Nationality


# Admin Class for Nacionalidad
class NationalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


# Register your models here.
admin.site.register(Nationality, NationalityAdmin)
