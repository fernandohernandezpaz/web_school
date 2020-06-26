import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

def get_current_year():
    return int(datetime.date.today().year)


def convert_date(value):
    return datetime.datetime. \
        strptime(str(value), '%Y-%m-%d'). \
        strftime('%d-%m-%Y')


class CheckIsLoggin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()

        return True
