from datetime import date
from django import template

register = template.Library()


@register.filter
def greater_than_today(note_date_limit):
    return date.today() > note_date_limit
