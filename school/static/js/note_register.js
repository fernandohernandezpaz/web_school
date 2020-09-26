$(function ($) {
    const btn_save = $('#btn_save');
    btn_save.attr('disabled', 'disabled');
    const data_form = [];          // array to save the student with note edited
    let input_tocken = $('input[name=csrfmiddlewaretoken]').val();
    let input_course = $('#course').val();
    let input_teacher = $('#teacher').val();


    $('body')
        .on('change', '.validar_maxymin', function () {
            collect_data_by_input_edit($(this));
            add_bad_note_class($(this));
        })
        .on('input', '.validar_maxymin', function () {
            let valor_nota = $(this).val();
            valor_nota = valor_nota.replace(/'+'/g, '');
            valor_nota = valor_nota.replace(/'-'/g, '');
            $(this).val(valor_nota);
            if (valor_nota > 100) {
                Swal.fire({
                    title: 'ERROR',
                    text: 'El valor ingresado no puede ser mayor a 100',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
                setTimeout(() => {
                    btn_save.attr('disabled', 'disabled');
                }, 100)
            } else if (valor_nota.length === 0) {
                setTimeout(() => {
                    btn_save.attr('disabled', 'disabled');
                }, 100);
                add_bad_note_class($(this))
            } else {
                add_bad_note_class($(this));
                btn_save.prop('disabled', false);
                btn_save.removeAttr('disabled');
                const object_data_element = {
                    span_id: $(this).data('span'),
                    input_id: $(this).data('input'),
                    value_1_id: $(this).data('value1'),
                    value_2_id: $(this).data('value2'),
                };
                const value_1 = $(`#${object_data_element.value_1_id}`).val();
                const value_2 = $(`#${object_data_element.value_2_id}`).val();
                if (validate_no_empties_inputs(value_1, value_2)) {
                    calculating_semestre(value_1, value_2,
                        object_data_element.input_id,
                        object_data_element.span_id);

                    calculate_semestre_final(object_data_element.input_id);
                }
            }
        })
        .on('keyup', '.validar_maxymin', function () {
            collect_data_by_input_edit($(this))
        })
        .on('keydown', '.validar_maxymin', function () {
            clearTimeout(typingTimer);
        })
        .on('submit', '#form_register_note', function (e) {
            e.preventDefault();

            const data = {
                'csrfmiddlewaretoken': input_tocken,
                'course_id': input_course,
                'teacher_id': input_teacher,
                'students_notes': JSON.stringify(data_form)
            };
            $.ajax({
                url: URLS_API.save,
                data: data,
                dataType: 'json',
                type: 'POST',
                success: function (response) {
                    if (response.status) {
                        setTimeout(() => {
                            btn_save.attr('disabled', 'disabled');
                        }, 100);
                        Swal.fire({
                            title: 'Guardado exitoso',
                            text: response.message,
                            icon: 'success',
                            confirmButtonText: 'OK'
                        }).then(result => {
                            if (result.value) {
                                location.reload()
                            }
                        });
                    }
                }
            });
        })
        .on('click', '#enabled_inputs', function () {
            Swal.fire({
                title: 'Aviso',
                text: 'Formulario habilitado para editar las notas',
                icon: 'info',
                confirmButtonText: 'OK'
            });
            $('.validar_maxymin').prop('disabled', false);

        });

    function add_bad_note_class(element) {
        var note_red = element.val();
        if (note_red < NOTA_MINIMA_APROBADO) {
            element.parent('td')
                .addClass('red-cell');
        } else {
            element.parent('td')
                .removeClass('red-cell');
        }
        if (note_red.length === 0) {
            element.parent('td')
                .removeClass('red-cell');
        }

        $.each($('.red-cell'), function (index, element) {
            const nota = $(element).find('input').val();
            if (nota >= NOTA_MINIMA_APROBADO) {
                $(element).removeClass('red-cell');
            }
        });
    }

    function calculating_semestre(value_1, value_2, input_id, span_id) {
        value_1 = convert_to_zero_if_empty(value_1);
        value_2 = convert_to_zero_if_empty(value_2);
        const addition = value_1 + value_2;
        const result = (addition / 2).toFixed(0);
        $(`#${input_id}`).val(result);
        $(`#${span_id}`).text(result);
    }

    function convert_to_zero_if_empty(value) {
        if (value === '')
            return 0;
        if (isNaN(Number(value)))
            return 0;

        return Number(value);
    }

    function calculate_semestre_final(input_id) {
        const input = $(`#${input_id}`);
        const object_data_element = {
            span_id: input.data('span'),
            input_id: input.data('input'),
            value_1_id: input.data('value1'),
            value_2_id: input.data('value2'),
        };
        const value_1 = $(`#${object_data_element.value_1_id}`).val();
        const value_2 = $(`#${object_data_element.value_2_id}`).val();
        if (validate_no_empties_inputs(value_1, value_2)) {
            calculating_semestre(value_1, value_2,
                object_data_element.input_id,
                object_data_element.span_id);
        }
    }

    function validate_no_empties_inputs(value_1, value_2) {
        return value_1 !== '' && value_2 !== '';
    }

    function collect_data_by_input_edit(input_edited) {
	    if (input_edited.val() <= 100 && input_edited.val() !== '') {
		    const row_contain_input = input_edited.parent().parent();
                    const matriculation_input = row_contain_input.find('td:eq(0)')
                        .find('.matriculation_id');
                    const matriculation_id = convert_to_zero_if_empty(matriculation_input.val());

                    const student_note = data_form.find(student => {
                        return student.matriculation_id === matriculation_id;
                    });

                    let id_input = input_edited.attr('id')
                    id_input = id_input.replace(/[0-9]/g, ''); // clean the id of numbers

                    if (student_note) {
                        student_note[id_input] = Number(input_edited.val())
                    } else {
                        const student_note = {
                            matriculation_id: matriculation_id,
                            note_id: convert_to_zero_if_empty(matriculation_input.data('note_id'))
                        };
                        student_note[id_input] = Number(input_edited.val())
                        data_form.push(
                            student_note
                        );
                    }
	    }
    }
});
