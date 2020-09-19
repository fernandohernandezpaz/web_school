from datetime import date
from django import template

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
