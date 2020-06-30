$(function ($) {
    let btn_save = $('#btn_save');
    btn_save.attr('disabled', 'disabled');
    let typingTimer;               // timer identifier
    let doneTypingInterval = 500; // time in ms
    const data_form = [];          // array to save the student with note edited


    $('body')
        .on('input', '.validar_maxymin', function () {
            let valor_nota = $(this).val();
            valor_nota = valor_nota.replace(/'+'/g, '');
            valor_nota = valor_nota.replace(/'-'/g, '');
            $(this).val(valor_nota);
            if (valor_nota > 100) {
                $(this).val('');
                Swal.fire({
                    title: 'ERROR',
                    text: 'El valor ingresado no puede ser mayor a 100',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            } else {
                btn_save.prop('disabled', false);
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

            $()


        })

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
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
                if (input_edited.val() <= 100) {
                    const row_contain_input = input_edited.parent().parent();
                    const matriculation_input = row_contain_input.find('td:eq(0)')
                        .find('.matriculation_id');
                    const matriculatrion_id = convert_to_zero_if_empty(matriculation_input.val());

                    const student_note = data_form.find(student => {
                        return student.matricula_id === matriculatrion_id;
                    });

                    let id_input = input_edited.attr('id')
                    id_input = id_input.replace(/[0-9]/g, ''); // clean the id of numbers

                    if (student_note) {
                        student_note[id_input] = Number(input_edited.val())
                    } else {
                        const student_note = {
                            matricula_id: matriculatrion_id,
                            note_id: convert_to_zero_if_empty(matriculation_input.data('note_id'))
                        };
                        for (const key of keys_note) {
                            if (id_input === key) {
                                student_note[key] = Number(input_edited.val())
                            } else {
                                student_note[key] = null;
                            }
                        }
                        data_form.push(
                            student_note
                        );
                    }
                }
            },
            doneTypingInterval
        );
    }
});