from django.contrib import admin
from school.models import Nacionalidad


# Admin Class for Nacionalidad
class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')


# Register your models here.
admin.site.register(Nacionalidad, NacionalidadAdmin)
