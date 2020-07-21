import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


# function return the current year
def get_current_year():
    return int(datetime.date.today().year)


# function to convert a date with format 'Y-m-d' to 'd-m-Y'
def convert_date(value):
    return datetime.datetime. \
        strptime(str(value), '%Y-%m-%d'). \
        strftime('%d-%m-%Y')


def calculate_note(note_1, note_2, decimals=0):
    if not note_1:
        return 0
    if not note_2:
        return 0
    if note_2 == 0:
        return 0

    return round((int(note_1) + int(note_2)) / 2, decimals)


def control_edition_note(list_control_fields_edited, note_id, supervisor_id=None):
    from .models import NoteControlEdition

    for register_edited in list_control_fields_edited:
        noteEditedControl = NoteControlEdition()
        noteEditedControl.note_id = note_id
        noteEditedControl.edit_field = register_edited.get('field_name')
        noteEditedControl.value_edit_field = register_edited.get('value')
        noteEditedControl.supervisor_id = supervisor_id
        noteEditedControl.save()


# class to check if user is logged
class CheckIsLoggin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        return True
