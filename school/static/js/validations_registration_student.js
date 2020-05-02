$(function ($) {
    let input_cantidad_hermanos = $('#id_personalfile-0-how_many');

    // NOTE: validamos si existe el input de cuantos hermanos y lo deshabilitamos
    if (input_cantidad_hermanos.length > 0) {
        input_cantidad_hermanos.prop('disabled', true);
    }

    $('body')
        .on('change', '#id_personalfile-0-have_brothers_center', function () {
            const valor = $(this).val() === 'True';
            if (valor) {
                input_cantidad_hermanos.prop('disabled', !valor)
            }
        });


});