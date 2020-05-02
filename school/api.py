from django.http import JsonResponse
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import Matriculation, GradeSection, Student
from .commons import (get_current_year, convert_date)
from web_school.constance_settings import CONSTANCE_CONFIG


def get_school_space(request):
    quantity_students = CONSTANCE_CONFIG['CANTIDAD_ALUMNOS_POR_AULA'][0]
    filters = {
        'teaching_year': get_current_year
    }

    if request.GET.get('id'):
        filters['grade_section__id'] = request.GET.get('id')

    count_student_maculation = Matriculation.objects. \
        filter(**filters). \
        count()

    nombre_grado_seccion = GradeSection.objects. \
        get(id=request.GET.get('id'))

    school_space = quantity_students - count_student_maculation

    if school_space > 0:
        mensaje = 'Aun tenemos cupos diponibles para el aula {gradoseccion}'. \
            format(gradoseccion=nombre_grado_seccion)
    else:
        mensaje = 'No hay cupos disponibles para el aula {gradoseccion}'. \
            format(gradoseccion=nombre_grado_seccion)

    response = {
        'school_space': school_space,
        'mensaje': mensaje
    }

    return JsonResponse(response)


def get_students(request):
    from .models import Family
    enrolled_students = Matriculation.objects. \
        filter(teaching_year=get_current_year()). \
        values_list('student_id', flat=True)
    students = Student.objects. \
        exclude(id__in=list(enrolled_students)). \
        annotate(fullname=Concat('names',
                                 Value(' '),
                                 'last_name'))
    search_field = ''
    filters = {}
    if request.POST.get('code'):
        search_field = 'código MINED'
        filters['code_mined'] = request.POST.get('code')
    elif request.POST.get('fullname'):
        search_field = 'Nombre del estudiante'
        filters['fullname__icontains'] = request.POST.get('fullname')

    students = students. \
        filter(**filters). \
        values('id',
               'code_mined',
               'fullname',
               'birthday')

    for row in students:
        row['birthday'] = convert_date(row['birthday'])

        row['family'] = []
        if Family.objects.filter(student__id=row['id']).exists():
            row['family'] = list(Student.objects.
                                    filter(id=row['id']).
                                    values(name=F('family_members__full_name'),
                                           rol=F('family_members__family_role'),
                                           tutor=F('family_members__tutor')))

    response = {
        'students': list(students),
    }
    if students.count() == 0:
        response['message'] = 'No se ningun estudiante con ' \
                              'coincidencia en el campo {}'. \
            format(search_field)

    return JsonResponse(response)
