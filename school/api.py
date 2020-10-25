import json
from django.http import JsonResponse
from django.db.models import Value, F
from django.db.models.functions import Concat
from .models import (Matriculation, GradeSection, Student,
                     Note, CourseGradeSection)
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
        from django.contrib.contenttypes.models import ContentType
        matriculation_type = ContentType.objects.get(app_label='school', model='matriculation')
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
            change_message = {
                key_message: {
                    'fields': ['estudiante', 'grado y sección', 'estado']
                }
            }

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
            change_message = {
                key_message: {}
            }

            message = 'Matrícula guardada exitosamente'

        django_log_entry.change_message = json.dumps([change_message])
        django_log_entry.content_type_id = matriculation_type.id
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


def statistics_period_notes(request):
    from django.db.models import Count, Case, When, IntegerField, Q, Avg
    column_note = request.POST.get('scale')
    teacher_id = int(request.POST.get('teacher_id'))
    current_year = get_current_year()
    grade_section_course_id = int(request.POST.get('grade_section_course_id', 0))
    course_id = int(request.POST.get('course_id'))

    filter_column_note = '{}__isnull'.format(column_note)
    filters = {
        filter_column_note: False,
        'teacher_id': teacher_id,
        'course_id': course_id,
        'matriculation__teaching_year': current_year,
        'course__coursegradesection__id': grade_section_course_id
    }

    if grade_section_course_id != 0:
        grade_section_course = CourseGradeSection.objects.get(pk=grade_section_course_id)
        filters['matriculation__grade_section'] = grade_section_course.grade_section_id

    students = Note.objects.filter(**filters). \
        values('id', column_note,
               'matriculation__student__names',
               'matriculation__student__last_name')

    scales_note = [{
        'nombre': 'Aprendizaje Avanzado',
        'valoracion': [90, 100],
        'color': '#0839ff',
    }, {
        'nombre': 'Aprendizaje Sastifactorio',
        'valoracion': [76, 89],
        'color': '#00f531',
    }, {
        'nombre': 'Aprendizaje Elemental',
        'valoracion': [60, 75],
        'color': '#ffee00'
    }, {
        'nombre': 'Aprendizaje Inicial',
        'valoracion': [0, 59],
        'color': '#f22e2e',
    }]

    for scale in scales_note:
        filter_column_note = {'{}__range'.format(column_note): scale.get('valoracion')}

        quantity_notes = students.aggregate(quantity=Count(Case(
            When(Q(**filter_column_note), then=1),
            output_field=IntegerField()
        )))

        start = scale.get('valoracion')[0]
        end = scale.get('valoracion')[1]
        scale['quantity_notes'] = quantity_notes.get('quantity', 0)
        scale['student_list'] = list(filter(lambda i: start <= i[column_note] <= end, students))

    average = students.aggregate(Avg(column_note))
    average_column = '{}__avg'.format(column_note)

    response = {
        'scales': scales_note,
        'average': average.get(average_column),
        'status': True
    }

    return JsonResponse(response)


def find_student(request):
    codigo_mined = request.POST.get('codigo_mined')
    current_year = get_current_year()
    if Student.objects.filter(code_mined=codigo_mined).exists():
        student = Student.objects.filter(code_mined=codigo_mined). \
            annotate(nombre_completo=Concat('names', Value(' '), 'last_name')). \
            get()
        student = {
            'id': student.id,
            'nombre_completo': student.nombre_completo,
            'genero': student.gender.name,
            'nacionalidad': student.nationality.name,
            'codigo_mined': student.code_mined,
            'fecha_nacimiento': student.birthday,
            'edad': student.calculate_age()
        }

        matriculation = Matriculation.objects. \
            filter(teaching_year=current_year,
                   student_id=student.get('id')).get()
        matriculation = {
            'id': matriculation.id,
            'grado_seccion': matriculation.grade_section.__str__(),
            'anio_curso': matriculation.teaching_year,
            'fecha_registro': matriculation.registration_date,
        }

        notes_set = Note.objects.filter(matriculation_id=matriculation.get('id')).all()

        notes = list()
        if notes_set.exists():
            for note in notes_set.iterator():
                notes.append({
                    'Asignatura': note.course.name,
                    'Docente': '{} {}'.format(note.teacher.first_name, note.teacher.last_name),
                    'Bimensual I': note.bimonthly_I or 0,
                    'Bimensual II': note.bimonthly_II or 0,
                    'Semestral I': note.biannual_I or 0,
                    'Bimensual III': note.bimonthly_III or 0,
                    'Bimensual IV': note.bimonthly_IV or 0,
                    'Semestral II': note.biannual_II or 0,
                    'Nota Final': note.final or 0
                })
    else:
        student = None
        matriculation = None
        notes = None

    response = {
        'student': student,
        'matriculation': matriculation,
        'notes': notes,
        'status': True
    }

    return JsonResponse(response)
