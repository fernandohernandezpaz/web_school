$(function ($) {
    let input_cantidad_hermanos = $('#id_personalfile-0-how_many');
    let select_cantidad_hermanos = $('#id_personalfile-0-have_brothers_center');

    // NOTE: validamos si existe el input de cuantos hermanos y lo deshabilitamos
    if (input_cantidad_hermanos.length > 0) {
        input_cantidad_hermanos.prop('disabled', true);
    }

    input_cantidad_hermanos.trigger('change');
    habilitarInputCantidadHermanos();

    $('body')
        .on('change', '#id_personalfile-0-have_brothers_center', function () {
            habilitarInputCantidadHermanos();
        });

    function habilitarInputCantidadHermanos() {
        const valor = select_cantidad_hermanos.val() === 'True';
        if (valor) {
            input_cantidad_hermanos.prop('disabled', !valor)
        }
    }
});