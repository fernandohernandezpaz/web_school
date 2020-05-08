import datetime


def get_current_year():
    return int(datetime.date.today().year)


def convert_date(value):
    return datetime.datetime. \
        strptime(str(value), '%Y-%m-%d'). \
        strftime('%d-%m-%Y')
