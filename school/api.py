from django.http import JsonResponse
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import Matriculation, GradeSection, Student
from .commons import (get_current_year, convert_date)
from web_school.constance_settings import CONSTANCE_CONFIG


def get_school_space(request):
    try:
        quantity_students = CONSTANCE_CONFIG['CANTIDAD_ALUMNOS_POR_AULA'][0]
        year = get_current_year()
        filters = {
            'teaching_year': year
        }

        id = request.POST.get('id')

        if id:
            filters['grade_section__id'] = id

        count_student_maculation = Matriculation.objects. \
            filter(**filters). \
            count()

        nombre_grado_seccion = GradeSection.objects. \
            get(id=id)

        school_space = quantity_students - count_student_maculation

        if school_space > 0:
            mensaje = 'Aun tenemos {spaces} cupos diponibles para el aula {gradoseccion}'. \
                format(spaces=school_space, gradoseccion=nombre_grado_seccion)
        else:
            mensaje = 'No hay cupos disponibles para el aula {gradoseccion}'. \
                format(gradoseccion=nombre_grado_seccion)

        response = {
            'school_space': school_space,
            'message': mensaje
        }

        return JsonResponse(response)
    except:
        return JsonResponse({})


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


def guardar_formulario(request):
    try:
        student_id = int(request.POST.get('student_id'))
        grade_section_id = int(request.POST.get('grade_section'))
        teaching_year = int(request.POST.get('teaching_year'))
        status = int(request.POST.get('teaching_year'))

        matriculation_exist = Matriculation.objects.filter(
            student_id=student_id,
            teaching_year=teaching_year,
        ).first()

        flag_continue = True
        if matriculation_exist:
            if matriculation_exist.grade_section_id == grade_section_id:
                message = 'No se puede crear una nueva' \
                          ' matricula para el estudiante {}'.format(matriculation_exist.student)
                flag_continue = False
            else:
                message = 'Matricula actualizada exitosamente'
        else:
            message = 'Matricula guardada exitosamente'

        if flag_continue:
            matriculation = Matriculation()
            matriculation.student_id = student_id
            matriculation.grade_section_id = grade_section_id
            matriculation.status = status
            matriculation.save()

        response = {
            'message': message,
            'status': flag_continue
        }
    except:
        response = {
            'status': False,
            'message': 'Error al guardar'
        }

    return JsonResponse(response)
