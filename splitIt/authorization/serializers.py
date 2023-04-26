from rest_framework import serializers
import uuid
from .validators import username_validator, phone_number_validator, email_validator
import bcrypt
from django.utils import timezone
from splitIt.models import Users


class UserSerializer(serializers.Serializer):
    class Meta:
        extra_kwargs = {'hashed_password': {'write_only': True}}

    user_id = serializers.CharField(default=str(uuid.uuid4()))
    user_name = serializers.CharField(max_length=30, validators=[username_validator])
    full_name = serializers.CharField(max_length=30, min_length=1)
    email_address = serializers.EmailField(validators=[email_validator])
    hashed_password = serializers.CharField(max_length=120)
    phone_number = serializers.CharField(max_length=10, validators=[phone_number_validator])
    profile_picture = serializers.ImageField(default='static/profile_pictures/default_profile.png')
    is_active = serializers.BooleanField(default=True)
    is_admin = serializers.BooleanField(default=False)
    is_email_validated = serializers.BooleanField(default=False)
    time_created = serializers.DateTimeField(default=timezone.now)

    def create(self, validated_data):
        validated_data['hashed_password'] = bcrypt.hashpw(validated_data['hashed_password'].encode('utf-8'),
                                                          bcrypt.gensalt()).decode('utf-8')
        return Users.objects.create(**validated_data)
