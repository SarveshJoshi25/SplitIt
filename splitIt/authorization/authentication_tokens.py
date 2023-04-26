import jwt, datetime
from config import AccessSecretKey, RefreshSecretKey
from rest_framework import exceptions


def create_tokens(user_id, is_access) -> jwt:
    if is_access:
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
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
