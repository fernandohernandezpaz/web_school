let list_students = [];
let quantity_school_space = 0;
$(function ($) {

    let student_input = $('#student_input_search');
    let select_grade_section = $('#grade_section_select');
    let teaching_year_input = $('#teaching_year_input');
    let select_status = $('#status_select');
    let input_tocken = $('input[name=csrfmiddlewaretoken]').val();
    let table_students = $('#students_rows');
    let message_space = $('#message_space');

    $('body')
        .on('click', '#search_student', function () {
            let value = student_input.val();

            if (jQuery.trim(value).length > 0) {
                let value_is = check_if_fullname_or_code(value);
                let keys_object = Object.keys(value_is);
                let object = value_is;
                if (keys_object.includes('is_code')) {

                    if (object['is_code']) {
                        console.log(object['message']);
                        search_and_get_student(value, 'code')
                    } else {
                        alert_message(object['message']);
                    }
                } else {
                    if (object['is_fullname']) {
                        console.log(object['message']);
                        search_and_get_student(value, 'fullname')
                    } else {
                        alert_message(object['message']);
                    }
                }
            } else {
                alert_message('¡Usted debe ingresar el nombre completo ó código MINED del estudiante a como se solicita!');
            }
        })
        .on('dblclick', '.select_row_student', function () {
            let student_id = $(this).data('student_id');
            const student = list_students.find(student => {
                return student.id === student_id
            });

            load_data_student_HTML(student);
            $('.close-modal').trigger('click');
        })
        .on('change', '#grade_section_select', function () {
            let data = {
                'csrfmiddlewaretoken': input_tocken,
                'id': parseInt($(this).val())
            };
            $.ajax({
                url: URLS_API.school_space,
                data: data,
                dataType: 'json',
                type: 'POST',
                success: function (response) {
                    quantity_school_space = response.school_space;
                    message_space
                        .html(response.message)
                        .fadeIn('fast');
                    if (quantity_school_space <= 0) {
                        $('.save').hide()
                    } else {
                        $('.save').show()
                    }
                }
            })
        })
        .on('submit', '#form_matricula', function (e) {
            e.preventDefault();
            if (quantity_school_space > 0) {
                const reload_page = $(this).data('continue');
                $.ajax({
                    url: URLS_API.save,
                    data: $('#form_matricula').serialize(),
                    dataType: 'json',
                    type: 'POST',
                    success: function (response) {
                        if (response.status) {
                            Swal.fire({
                                title: 'Guardado exitoso',
                                text: response.message,
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then(result => {
                                if (reload_page) {
                                    window.location = URLS_API.current_page;
                                } else {
                                    window.location = URLS_API.back_url;
                                }
                            });
                        } else {
                            alert_message(response.message);
                        }
                    }
                });
            } else {
                alert_message('No hay cupos disponibles');
            }
        })
        .on('click', '.save', function () {
            const flag_continue = Boolean($(this).data('continue'));
            $('#form_matricula').attr('data-continue', flag_continue);
        });


    if (typeof (student_data) !== 'undefined' && typeof (matriculacion) !== 'undefined') {
        const status = {
            id: matriculacion.status,
            label: matriculacion.status_name
        };
        load_data_student_HTML(student_data, status);
        teaching_year_input.val(matriculacion.teaching_year);
        select_grade_section.val(matriculacion.grade_seccion).trigger('change');
        $('#select2-grade_section_select-container')
            .attr('title', matriculacion.grade_seccion_name)
            .html(matriculacion.grade_seccion_name);

    }

    function check_if_fullname_or_code(str) {
        let contains_signs = str.includes('-');
        let length_str = str.length;
        let numbers = /\d+/;
        let message = '';
        if (contains_signs && length_str <= 19) {
            let format_code_MINED = str.split('-');
            let contains_numbers = numbers.test(format_code_MINED[0]);
            message = 'Código MINED digitado correcto';
            if (contains_numbers) {
                message = '¡Código MINED digitado incorrecto!';
            }
            return {
                'is_code': (contains_signs && !contains_numbers),
                'message': message
            };
        }
        let is_fullname = numbers.test(str);
        message = 'Es el nombre de un estudiante';
        if (is_fullname) {
            message = 'El nombre del estudiante es incorrecto';
        }
        return {
            'is_fullname': !is_fullname,
            'message': message
        };
    }

    function alert_message(message = 'Error', title = '¡Error!',
                           icon = 'error', confirm_button_label = 'Ok') {
        Swal.fire({
            title: title,
            text: message,
            icon: icon,
            confirmButtonText: confirm_button_label
        });
    }

    function load_data_student_table(students) {
        table_students.html('');
        list_students = students;
        for (const student of students) {
            student.code_mined = student.code_mined || '-';
            let family = '';
            if (student.family.length > 0) {
                for (const familiar of student.family) {
                    let tutor = familiar.tutor ? '(Tutor)' : '';
                    family += `<small>${familiar.name}(${familiar.rol})${tutor}</small><br>`;
                }
            }
            table_students.append(
                `<tr data-student_id="${student.id}" class="select_row_student">
                <td>${student.code_mined}</td>
                <td>${student.fullname}</td>
                <td>${student.birthday}</td>
                <td>${family}</td>
                </tr>`);
        }
    }

    function load_data_student_HTML(student, status = {id: 1, label: 'Activo'}) {
        for (const key in student) {
            if (key === 'id') {
                $(`#${key}`).val(student[key]);
            } else if (key === 'family') {
                let family = 'Ningun Familiar Registrado';
                if (student[key].length > 0) {
                    family = '';
                    for (const familiar of student[key]) {
                        let tutor = familiar.tutor ? '(Tutor)' : '';
                        family += `${familiar.name} (${familiar.rol})${tutor}<br>`;
                    }
                }
                $(`#${key}`).html(family);
            } else {
                $(`#${key}`).html(student[key]);
            }
        }
        $('#data-student').fadeIn('fast');

        select_status.val(status.id).trigger('change');
        $('#select2-status_select-container')
            .attr('title', status.label)
            .html(status.label);
        select_status.removeAttr('disabled');

        select_grade_section.removeAttr('disabled');
    }

    function search_and_get_student(value, key_search) {
        let data = {
            'csrfmiddlewaretoken': input_tocken
        };
        data[key_search] = value;
        data[key_search] = value;

        $.ajax({
            url: URLS_API.students_data,
            data: data,
            dataType: 'json',
            type: 'POST',
            success: function (response) {
                const students = response.students;
                if (students['message'] !== undefined) {
                    alert_message(students['message']);
                } else {
                    if (students.length === 1) {
                        load_data_student_HTML(students[0]);
                    } else {
                        load_data_student_table(students);

                        $('#ModalTable').modal({
                            fadeDuration: 500,
                            fadeDelay: 0.3
                        });
                    }
                }
            }
        })
    }
});