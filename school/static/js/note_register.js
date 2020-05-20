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
});