"""
configuraciones para django constances
"""
from datetime import date

CONSTANCE_CONFIG = {
    'CANTIDAD_ALUMNOS_POR_AULA': (30, 'La cantidad limite de alumnos por cada aula(Grado Sección)', int),
    'LIMITE_REPARACIONES': (3, 'La cantidad limite de Asignaturas por reparar(Asignatura)', int),
    'NOTA_MINIMA_APROVADO': (60, 'Nota minima para aprovar una evaluacion(Nota)', int),
    'INTENTOS_PARA_REGISTRAR_NOTA': (2, 'Numero de intentos para registrar una nota(Nota)', int),
    'FECHA_LIMITE_REGISTRO_I_BIMENSUAL': (date(2020, 6, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_II_BIMENSUAL': (date(2020, 8, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_III_BIMENSUAL': (date(2020, 10, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_IV_BIMENSUAL': (date(2020, 12, 12), "Ultima fecha de registro"),

}

