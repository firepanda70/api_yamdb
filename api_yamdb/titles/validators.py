import datetime as dt

from django.core.exceptions import ValidationError

UNVALID_YEAR_MESSAGE = ('Произведение еще не вышло')


def year_validation(value):
    year = dt.date.today().year
    if value > year:
        raise ValidationError(UNVALID_YEAR_MESSAGE)
    return value
