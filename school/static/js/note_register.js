$(function ($) {
    $('body')
        .on('input', '.validar_maxymin', function () {
            let valor_nota = $(this).val();
            valor_nota = valor_nota.replace(/'+'/g, '');
            valor_nota = valor_nota.replace(/'-'/g, '');
            $(this).val(valor_nota);
            if (valor_nota > 100) {
                $(this).val(0);
                Swal.fire({
                    title: 'ERROR',
                    text: 'El valor ingresado no puede ser mayor a 100',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        })
        .on('focus', '.validar_maxymin', function () {
            const object_data_element = {
                span_id: $(this).data('span'),
                input_id: $(this).data('input'),
                value_1_id: $(this).data('value1'),
                value_2_id: $(this).data('value2'),
            };
            const value_1 = $('#' + object_data_element.value_1_id).val();
            const value_2 = $('#' + object_data_element.value_2_id).val();
            calculating_semestre(value_1, value_2,
                object_data_element.input_id,
                object_data_element.span_id);
        });

    function calculating_semestre(value_1, value_2, input_id, span_id) {
        value_1 = convert_to_zero(value_1);
        value_2 = convert_to_zero(value_2);
        const addition = value_1 + value_2;
        const result = (addition / 2).toFixed(0);
        $(`#${input_id}`).val(result);
        $(`#${span_id}`).text(result);
    }

    function convert_to_zero(value) {
        if (value === '')
            return 0;
        if (isNaN(Number(value)))
            return 0;

        return Number(value);
    }
});