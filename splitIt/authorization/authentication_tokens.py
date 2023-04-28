import jwt, datetime
from config import AccessSecretKey, RefreshSecretKey
from rest_framework import exceptions
from .serializers import UserSerializer
from rest_framework.authentication import get_authorization_header
from splitIt.models import Users

def create_tokens(user_id, is_access) -> jwt:
    if is_access:
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                'iat': datetime.datetime.utcnow(),
                'type': 'access'
            }, AccessSecretKey, algorithm='HS256')
    else:
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                'iat': datetime.datetime.utcnow(),
                'type': 'refresh'
            }, RefreshSecretKey, algorithm='HS256')


def decode_tokens(token, is_access):
    try:
        if is_access:
            return jwt.decode(token, AccessSecretKey, algorithms=['HS256'])
        else:
            return jwt.decode(token, RefreshSecretKey, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token expired.')


def authenticate_user(request) -> UserSerializer:
    try:
        authentication_token = get_authorization_header(request).split()
        if authentication_token and len(authentication_token) == 2:
            authentication_token = authentication_token[1].decode('utf-8')

            user = decode_tokens(authentication_token, True)

            user = Users.objects.get(user_id=user['user_id'])

            if not user.is_email_validated:
                raise exceptions.AuthenticationFailed('User email not validated.')

            return user
    except exceptions.AuthenticationFailed:
        raise exceptions.AuthenticationFailed('User is not authenticated.')
    except Exception as e:
        raise Exception(e.args)
