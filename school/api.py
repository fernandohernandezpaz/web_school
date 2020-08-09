from django.http import JsonResponse
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import Matriculation, GradeSection, Student, Note
from .commons import (get_current_year, convert_date)
from constance import config


def get_school_space(request):
    try:
        quantity_students = config.CANTIDAD_ALUMNOS_POR_AULA
        year = get_current_year()
        filters = {
            'teaching_year': year,
            'status': 1
        }

        id = request.POST.get('id')

        if id:
            filters['grade_section__id'] = id

        count_student_matriculation = Matriculation.objects. \
            filter(**filters). \
            count()

        nombre_grado_seccion = GradeSection.objects. \
            get(id=id)

        school_space = quantity_students - count_student_matriculation

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


def save_form(request):
    try:
        from django.contrib.admin.models import LogEntry
        import json
        student_id = int(request.POST.get('student_id'))
        grade_section_id = int(request.POST.get('grade_section'))
        teaching_year = int(request.POST.get('teaching_year'))
        status = int(request.POST.get('status'))

        matriculation_exist = Matriculation.objects.filter(
            student_id=student_id,
            teaching_year=teaching_year,
        ).first()

        django_log_entry = LogEntry()
        if matriculation_exist:
            matriculation_exist.student_id = student_id
            matriculation_exist.grade_section_id = grade_section_id
            matriculation_exist.status = status
            matriculation_exist.save()

            django_log_entry.action_flag = 2
            key_message = 'changed'
            django_log_entry.object_id = matriculation_exist.id
            django_log_entry.object_repr = matriculation_exist.__str__()

            message = 'Matrícula actualizada exitosamente'
        else:
            matriculation = Matriculation()
            matriculation.student_id = student_id
            matriculation.grade_section_id = grade_section_id
            matriculation.status = status
            matriculation.save()

            django_log_entry.action_flag = 1
            key_message = 'added'
            django_log_entry.object_id = matriculation.id
            django_log_entry.object_repr = matriculation.__str__()

            message = 'Matrícula guardada exitosamente'

        change_message = {
            key_message: {
                'fields': ['estudiante', 'grado y sección', 'estado']
            }
        }

        django_log_entry.change_message = json.dumps([change_message])
        django_log_entry.content_type_id = 17  # django contenttype_id of note
        django_log_entry.user_id = request.user.id

        django_log_entry.save()

        response = {
            'message': message,
            'status': True
        }
    except:
        response = {
            'status': False,
            'message': 'Error al guardar'
        }

    return JsonResponse(response)


def save_note(request):
    import json
    from datetime import date
    from .commons import calculate_note, control_edition_note
    course_id = request.POST.get('course_id')
    teacher_id = request.POST.get('teacher_id')
    students_notes = request.POST.get('students_notes')
    students_notes = list(json.loads(students_notes))

    for student_note in students_notes:
        control_fields_edited = []
        note_from_student = Note.objects. \
            filter(matriculation_id=student_note['matriculation_id'],
                   course_id=course_id).first()

        # if no exists note from the student we create a instance of Note
        if not note_from_student:
            note_from_student = Note()
            note_from_student.course_id = course_id
            note_from_student.matriculation_id = student_note.get('matriculation_id')
            note_from_student.teacher_id = teacher_id

        if student_note.get('ibimensual'):
            note_from_student.bimonthly_I = int(student_note.get('ibimensual'))
            note_from_student.bimonthly_I_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'bimonthly_I',
                'value': int(student_note.get('ibimensual'))
            })

        if student_note.get('iibimensual'):
            note_from_student.bimonthly_II = int(student_note.get('iibimensual'))
            note_from_student.bimonthly_II_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'bimonthly_II',
                'value': int(student_note.get('iibimensual'))
            })

        if note_from_student.bimonthly_I is not None and note_from_student.bimonthly_II is not None:
            first_semestral = calculate_note(note_from_student.bimonthly_I, note_from_student.bimonthly_II)
            note_from_student.biannual_I = round(first_semestral)
            note_from_student.biannual_I_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'biannual_I',
                'value': note_from_student.biannual_I
            })

        if student_note.get('iiibimensual'):
            note_from_student.bimonthly_III = int(student_note.get('iiibimensual'))
            note_from_student.bimonthly_III_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'bimonthly_III',
                'value': int(student_note.get('iiibimensual'))
            })

        if student_note.get('ivbimensual'):
            note_from_student.bimonthly_IV = int(student_note.get('ivbimensual'))
            note_from_student.bimonthly_IV_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'bimonthly_IV',
                'value': int(student_note.get('ivbimensual'))
            })

        if note_from_student.bimonthly_III is not None and note_from_student.bimonthly_IV is not None:
            second_semestral = calculate_note(note_from_student.bimonthly_III, note_from_student.bimonthly_IV)
            note_from_student.biannual_II = round(second_semestral)
            note_from_student.biannual_II_date_register = date.today()
            control_fields_edited.append({
                'field_name': 'biannual_II',
                'value': note_from_student.biannual_II
            })

        if note_from_student.biannual_I is not None and note_from_student.biannual_II is not None:
            final = calculate_note(note_from_student.biannual_I, note_from_student.biannual_II)
            note_from_student.final = round(final)
            control_fields_edited.append({
                'field_name': 'final',
                'value': note_from_student.final
            })

        note_from_student.save()

        supervisor_id = None
        group = request.user.groups.first()
        if group and group.name.lower() != 'docente'.lower():
            supervisor_id = request.user.id
        else:
            if request.user.is_superuser:
                supervisor_id = request.user.id

        control_edition_note(control_fields_edited, note_from_student, teacher_id, supervisor_id)

    response = {
        'status': True,
        'message': 'Notas guardadas exitosamente'
    }

    return JsonResponse(response)
