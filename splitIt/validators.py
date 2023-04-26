import re
from django.core.exceptions import ValidationError


def username_validator(username):
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError('Username must be alphanumeric or underscore')
