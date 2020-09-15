$(function () {
    let btn_save = $('#btn_save');
    let btn_enabled_edition = $('#enabled_inputs');
    let table = $('#history_table');
    if (table.length > 0) {
        table.DataTable();
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
                    break
            }
        });
});