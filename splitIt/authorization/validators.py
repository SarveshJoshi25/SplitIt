import re
from django.core.exceptions import ValidationError
from splitIt.models import Users
from email_validator import validate_email

def username_validator(username):
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError('Username must be alphanumeric or underscore')
    if len(username) < 4:
        raise ValidationError('Username must be at least 4 characters long')
    if Users.objects.filter(user_name=username).count() == 1:
        raise ValidationError('Username already exists')
    return username


def phone_number_validator(phone_number):
    if not re.match(r'^[0-9]+$', phone_number):
        raise ValidationError('Phone number must be numeric')
    if len(phone_number) != 10:
        raise ValidationError('Phone number must be 10 digits long')
    if Users.objects.filter(phone_number=phone_number).count() == 1:
        raise ValidationError('Phone number already exists')
    return phone_number


def email_validator(email_address):
    if not validate_email(email_address, check_deliverability=True, globally_deliverable=True):
        raise ValidationError('Invalid email address')
    if Users.objects.filter(email_address=email_address).count() == 1:
        raise ValidationError('Email Address already exists')
    return email_address
