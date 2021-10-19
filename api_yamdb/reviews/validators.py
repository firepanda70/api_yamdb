from django.core.exceptions import ValidationError

UNVALID_SCORE_MESSAGE = ('Оценка произведения должна '
                         'быть в диапазоне от 1 до 10')


def score_validation(value):
    if value < 1 or value > 10:
        raise ValidationError(UNVALID_SCORE_MESSAGE)
    return value
