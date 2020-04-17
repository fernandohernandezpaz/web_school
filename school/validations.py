from django.core.validators import MaxValueValidator, MinValueValidator


def validateQuantityDigits(field, digits, message=None):
    if not message:
        message = 'El {} debe tener 8 digitos'.format(field)

    minor = ''
    higher = ''
    for i in range(digits):
        minor += str(1)
        higher += str(9)

    minor = int(minor)
    higher = int(higher)

    return [MinValueValidator(minor, message),
            MaxValueValidator(higher, message)]
