import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

fields_note_spanish = {
    'bimonthly_I': 'Bimensual I',
    'bimonthly_II': 'Bimensual II',
    'biannual_I': 'Semestral I',
    'bimonthly_III': 'Bimensual III',
    'bimonthly_IV': 'Bimensual IV',
    'biannual_II': 'Semestral II',
    'final': 'Nota Final',
}


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


def control_edition_note(list_control_fields_edited, note, teacher_id=None, supervisor_id=None):
    from .models import NoteControlEdition
    from django.contrib.admin.models import LogEntry
    from django.contrib.contenttypes.models import ContentType
    import json
    note_type = ContentType.objects.get(app_label='school', model='note')

    fields = []
    for register_edited in list_control_fields_edited:
        note_edited_control = NoteControlEdition()
        note_edited_control.note_id = note.id
        note_edited_control.edit_field = register_edited.get('field_name')
        note_edited_control.value_edit_field = register_edited.get('value')
        note_edited_control.supervisor_id = supervisor_id
        note_edited_control.save()

        key = fields_note_spanish[register_edited['field_name']]
        fields.append(
            '{} - {}'.format(key, register_edited['value'])
        )

    flag_add = NoteControlEdition.objects.filter(note_id=note.id).count()
    flag_add = 1 if flag_add <= 1 else 2
    django_log_entry = LogEntry()
    django_log_entry.object_id = note.id
    django_log_entry.object_repr = note.__str__()
    django_log_entry.action_flag = flag_add

    key_message = 'added' if flag_add <= 1 else 'changed'
    if key_message == 'added':
        change_message = {
            key_message: {}
        }
    else:
        change_message = {
            key_message: {
                'fields': fields
            }
        }

    django_log_entry.change_message = json.dumps([change_message])
    django_log_entry.content_type_id = note_type.id
    django_log_entry.user_id = supervisor_id or teacher_id

    django_log_entry.save()


# class to check if user is logged
class CheckIsLoggin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        return True
