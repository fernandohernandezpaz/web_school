$(function () {
    const filtro = $('.periods:checked').val();
    const input_tocken = $('input[name=csrfmiddlewaretoken]').val();
    const course = $('#course').val();
    const teacher = $('#teacher').val();
    const grade_section_course = $('#grade_section_course_id').val();

    crearGrafico();

    $('body')
        .on('change', '.periods', function () {
            const campos = {
                csrfmiddlewaretoken: input_tocken,
                period: $(this).val(),
                course_id: course,
                teacher_id: teacher,
                grade_section_course_id: grade_section_course,
            };
            crearGrafico(campos);
        });

    function crearGrafico(campos = {
        csrfmiddlewaretoken: input_tocken,
        period: filtro,
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
                const data = response['periods']
                const option = {
                    title: {
                        text: 'Definir nombre del grafico',
                        textStyle: {
                            fontSize: 13,
                            color: '#000'
                        }
                    },
                    tooltip: {
                        show: true,
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
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
                    series: [{
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
                    }, {
                        type: 'bar',
                        barGap: 0,
                        xAxisIndex: 1,
                        yAxisIndex: 1
                    }, {
                        type: 'bar',
                        barGap: 0,
                        xAxisIndex: 1,
                        yAxisIndex: 1
                    }, {
                        type: 'bar',
                        barGap: 0,
                        xAxisIndex: 1,
                        yAxisIndex: 1
                    }]
                };
                chart.setOption(option)
                chart.on('click', (params) => {
                    console.log(params);
                })
            }
        });
    }
});