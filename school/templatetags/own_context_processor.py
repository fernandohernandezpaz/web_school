from datetime import date
from django import template
from constance import config

register = template.Library()


@register.filter
def less_than_today(note_date_limit):
    return date.today() > note_date_limit


@register.filter
def between_the_period(date_start, date_end):
    return date_start <= date.today() <= date_end


@register.filter
def get_value(dict, key):
    return dict.get(key)


def info(request):
    return {
        'logo_colegio': config.LOGO_DEL_COLEGIO,
        'nombre_colegio': config.NOMBRE_DEL_COLEGIO
    }