"""
configuraciones para django constances
"""
from datetime import date

CONSTANCE_CONFIG = {
    'CANTIDAD_ALUMNOS_POR_AULA': (30, 'La cantidad limite de alumnos por cada aula(Grado Sección)', int),
    'FECHA_LIMITE_REGISTRO_I_BIMENSUAL': (date(2020, 6, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_II_BIMENSUAL': (date(2020, 8, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_III_BIMENSUAL': (date(2020, 10, 29), "Ultima fecha de registro"),
    'FECHA_LIMITE_REGISTRO_IV_BIMENSUAL': (date(2020, 12, 12), "Ultima fecha de registro"),

}
CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': ('CANTIDAD_ALUMNOS_POR_AULA', 'FECHA_LIMITE_REGISTRO_I_BIMENSUAL',
                        'FECHA_LIMITE_REGISTRO_II_BIMENSUAL', 'FECHA_LIMITE_REGISTRO_III_BIMENSUAL',
                        'FECHA_LIMITE_REGISTRO_IV_BIMENSUAL'),
}
