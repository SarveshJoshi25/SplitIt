import uuid
from django.utils import timezone
from django.db import models

# Create your models here.

class Users(models.Model):
    user_id = models.CharField(primary_key=True, default=str(uuid.uuid4()), editable=False, max_length=36)
    user_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=30)
    email_address = models.EmailField()
    hashed_password = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='static/profile_pictures', blank=True, null=True,
                                        default='static/profile_pictures/default_profile.png')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_validated = models.BooleanField(default=False)
    time_created = models.DateTimeField(default=timezone.now)





