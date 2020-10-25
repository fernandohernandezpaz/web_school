$(function () {
    const inputSearch = $('#buscador');
    const input_tocken = $('input[name="csrfmiddlewaretoken"]');

    $('body')
        .on('click', '.find', function () {
            if (inputSearch.val() !== null && inputSearch.val().trim().length > 0) {
                $.ajax({
                    url: urls.find_student,
                    data: {
                        csrfmiddlewaretoken: input_tocken.val(),
                        codigo_mined: inputSearch.val(),
                    },
                    dataType: 'json',
                    type: 'POST',
                    success: function (response) {
                        if (response.student) {
                            const student = response.student;
                            const matriculation = response.matriculation;
                            const notes = response.notes;
                            Object.keys(student).forEach(llave => {
                                $(`#${llave}`).text(student[llave]);
                            });

                            Object.keys(matriculation).forEach(llave => {
                                $(`#${llave}`).text(matriculation[llave]);
                            });
                            const class_css = 'class="text-center"';
                            const body_table = $('#body_table');
                            body_table.html('');
                            let fila = '', campo_nota = '';
                            for (const nota of notes) {
                                fila = `<tr><th>${nota.Asignatura}</th>`;
                                campo_nota = '';
                                for (const campo of campos) {
                                    campo_nota += `<td ${class_css}>${nota[campo]}</td>`;
                                }
                                fila += campo_nota;
                                fila += `<td ${class_css}>${nota.Docente}</td></tr>`;
                                body_table.append(fila);
                            }

                            timer = 1500;
                            Swal.fire({
                                text: `El estudiante ${student.nombre_completo} fue encontrado.`,
                                target: '#dummy-target',
                                customClass: {
                                    container: 'position-absolute'
                                },
                                timer: timer + 1000,
                                toast: true,
                                position: 'bottom-right'
                            });
                            setTimeout(() => {
                                $('#cover').fadeOut('slow');
                                $('#tabla_information').fadeIn('slow');
                            }, timer - 200);
                        } else {
                            Swal.fire({
                                html: `<b>No se encontro ningun estudiante con el codigo mined ${inputSearch.val()}</b>`,
                                target: '#dummy-target',
                                customClass: {
                                    container: 'position-absolute'
                                },
                                toast: true,
                                position: 'bottom-right'
                            });
                        }
                    }
                });
            }
        });
});