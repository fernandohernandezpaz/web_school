$(function () {
    let btn_save = $('#btn_save');
    let btn_enabled_edition = $('#enabled_inputs');
    let table = $('#history_table');
    if (table.length > 0) {
        if (table.find('tbody').find('tr td').length > 1) {
            table.dataTable({
                'lengthMenu': [[15, 25, 50, -1], [15, 25, 50, 'Todos']],
                'language': {
                    'sProcessing': 'Procesando...',
                    'sLengthMenu': 'Mostrar _MENU_ registros',
                    'sZeroRecords': 'No se encontraron resultados',
                    'sEmptyTable': 'Ningún dato disponible en esta tabla',
                    'sInfo': 'Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
                    'sInfoEmpty': 'Mostrando registros del 0 al 0 de un total de 0 registros',
                    'sInfoFiltered': '(filtrado de un total de _MAX_ registros)',
                    'sInfoPostFix': '',
                    'sSearch': 'Buscar:',
                    'sUrl': '',
                    'sInfoThousands': '',
                    'sLoadingRecords': 'Cargando...',
                    'oPaginate': {
                        'sFirst': 'Primero',
                        'sLast': 'Último',
                        'sNext': 'Siguiente',
                        'sPrevious': 'Anterior'
                    },
                    'oAria': {
                        'sSortAscending': ': Activar para ordenar la columna de manera ascendente',
                        'sSortDescending': ': Activar para ordenar la columna de manera descendente'
                    },
                    'buttons': {
                        'copy': 'Copiar',
                        'colvis': 'Visibilidad'
                    }
                }
            });
        }
    }
    $('body')
        .on('click', 'input[name="tabs"]', function () {
            const tab_id = $(this).attr('id');
            switch (tab_id) {
                case 'tab1':
                    btn_save.fadeIn();
                    btn_enabled_edition.fadeIn();
                    break;
                case 'tab2':
                case 'tab3':
                    btn_save.fadeOut();
                    btn_enabled_edition.fadeOut();
                    $(window).trigger('resize');
                    break
            }
        });
});