$(function () {
    const filtro = $('.scales:checked');
    const message = $('#danger_average');
    const corte = $('.corte');
    const promedio = $('.promedio');
    const input_tocken = $('input[name=csrfmiddlewaretoken]').val();
    const course = $('#course').val();
    const teacher = $('#teacher').val();
    const grade_section_course = $('#grade_section_course_id').val();

    crearGrafico();

    $('body')
        .on('change', '.scales', function () {
            const campos = {
                csrfmiddlewaretoken: input_tocken,
                scale: $(this).val(),
                course_id: course,
                teacher_id: teacher,
                grade_section_course_id: grade_section_course,
            };
            crearGrafico(campos, $(this));
        });

    function crearGrafico(campos = {
        csrfmiddlewaretoken: input_tocken,
        scale: filtro.val(),
        course_id: course,
        teacher_id: teacher,
        grade_section_course_id: grade_section_course,
    }) {
        $.ajax({
            url: URLS_API.statistics_period_notes,
            data: campos,
            dataType: 'json',
            type: 'POST',
            success: function (response) {
                const chart = echarts.init(document.getElementById('notes_graph'));
                const data = response['scales']
                const average = response['average'].toFixed(0);

                setearColorDependiendoEscala(data, average);
                cargarEstudiantesEnTabla(data[data.length - 1], '#notes_bad_students');
                cargarEstudiantesEnTabla(data[0], '#notes_good_students');
                let series = new Array(4).fill({
                    type: 'bar',
                    barGap: 0,
                    xAxisIndex: 1,
                    yAxisIndex: 1
                });

                series[0] = {
                    data: data.map(item => item['quantity_notes']),
                    type: 'bar',
                    label: {
                        show: true,
                        position: 'top',
                        textStyle: {
                            color: '#555'
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: (params) => {
                                let colors = data.map(item => item['color'])
                                return colors[params.dataIndex]
                            }
                        }
                    },
                    xAxisIndex: 0,
                    yAxisIndex: 0
                };

                const option = {
                    toolbox: setToolBox('Escala de Calificaciones'),
                    title: {
                        text: 'Escala de Calificaciones',
                        textStyle: {
                            fontSize: 17,
                            color: '#000',
                            fontWeight: 'bolder',
                            align: 'center'
                        },
                    },
                    tooltip: {
                        show: true,
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        },
                        formatter: (params) => {
                            let axisValue = `<p>${params[0].axisValue}</p>`;
                            params.forEach(item => {
                                axisValue += `<p>${item.marker} Estudiantes: ${item.data}</p>`;
                            });
                            return axisValue;
                        }
                    },
                    legend: {
                        data: data.map(item => item['nombre'])
                    },
                    color: data.map(item => item['color']),
                    grid: [
                        {
                            top: 100,
                            bottom: 101
                        },
                        {
                            height: 60,
                            bottom: 40
                        }
                    ],
                    xAxis: [{
                        type: 'category',
                        data: data.map(item => item.nombre),
                        gridIndex: 0,
                        axisLabel: {
                            color: '#333'
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#e7e7e7'
                            }
                        },
                        axisTick: {
                            lineStyle: {
                                color: '#e7e7e7'
                            }
                        },
                        zlevel: 2
                    }, {
                        type: 'category',
                        gridIndex: 1,
                        axisLine: {
                            show: false
                        },
                        zlevel: 1
                    }],
                    yAxis: [{
                        type: 'value',
                        gridIndex: 0,
                        axisLabel: {
                            color: '#333'
                        },
                        splitLine: {
                            lineStyle: {
                                type: 'dashed'
                            }
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#ccc'
                            }
                        },
                        axisTick: {
                            lineStyle: {
                                color: '#ccc'
                            }
                        }
                    }, {
                        type: 'value',
                        gridIndex: 1,
                        axisLabel: {
                            show: false
                        },
                        axisLine: {
                            show: false
                        },
                        splitLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        }
                    }],
                    series: series
                };
                chart.setOption(option);

                window.onresize = function () {
                    chart.resize();
                };

                chart.on('click', (params) => {
                    console.log(params);
                })
            }
        });
    }

    function setToolBox(title_1, isCustomTable) {
        let tableData = {
            show: true,
            feature: {
                restore: {
                    title: 'Refrescar'
                },
                saveAsImage: {
                    title: 'Descargar imagen'
                }
            }
        };
        if (isCustomTable)
            Object.assign(tableData, this.customTable());

        return tableData;
    }


    function cargarEstudiantesEnTabla(data, id_table) {
        let table = $(id_table).find('tbody');
        let students = data['student_list'].reverse();
        const column_name = $('.scales:checked').val();

        agregarFilaEstudiante(table, students, column_name);
    }

    function agregarFilaEstudiante(table, students, column_name, limit_data = 5) {
        let index = 1;
        table.html('');
        if (students.length > 0) {
            for (const student of students) {
                if (index > limit_data) {
                    break;
                }
                table.append(
                    `<tr><td>${index}</td>` +
                    `<td>${student['matriculation__student__names']} ${student['matriculation__student__last_name']}</td>` +
                    `<td>${student[column_name]}</td></tr>`
                )
                index++;
            }
        } else {
            table.append(
                `<tr><td colspan="3" style="text-align: center;"><strong>NO HAY REGISTROS</strong></td></tr>`
            )
        }
    }

    function setearColorDependiendoEscala(scales, average) {
        const nombre_corte_evaluativo = $('.scales:checked').parent().text();
        corte.html(nombre_corte_evaluativo);
        console.log(filtro);
	const scale = scales.find(scale => average >= scale.valoracion[0] && average <= scale.valoracion[1]);
        promedio.css('color', scale.color);
        promedio.html(average);
        message.css('color', scales.reverse()[0].color)
        if (average < 70) {
            message.fadeIn('slow');
        } else {
            message.fadeOut('slow');
        }
    }
});
