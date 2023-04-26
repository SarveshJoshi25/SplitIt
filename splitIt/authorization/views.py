import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from .serializers import UserSerializer
from splitIt.models import Users
from django.db.models import Q
import bcrypt
from .authentication_tokens import create_tokens, decode_tokens
import redis

redis_instance = redis.Redis(host='localhost', port=6379, db=0)


class CreateAccount(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serialised_data = UserSerializer(data=request.data)

            if not serialised_data.is_valid():
                return Response({"error": serialised_data.errors}, status=500)

            serialised_data = serialised_data.save()

            return Response({"message": "Account created successfully"}, status=200)

        except Exception as e:
            print(e.args)
            return Response({"error": e.args}, status=500)


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user = Users.objects.get(Q(user_name__iexact=request.data['login_id'])
                                     | Q(email_address__iexact=request.data['login_id']))

            if not bcrypt.checkpw(request.data['password'].encode('utf-8'), user.hashed_password.encode('utf-8')):
                return Response({"error": "Password didn't match."}, status=500)

            access_token = create_tokens(user.user_id, True)
            response = Response({"access_token": access_token}, status=200)

            if request.data['remember_me']:
                response.set_cookie(key='refresh_token', value=create_tokens(user.user_id, False), httponly=True)
            response.set_cookie(key='access_token', value=access_token, httponly=True)

            return response

        except Users.DoesNotExist:
            return Response({"error": "User doesn't exist."}, status=500)

        except Exception as e:
            print(e.args)
            return Response({"error": e.args}, status=500)


class AuthenticateUser(APIView):
    authentication_classes = []

    def get(self, request):
        try:
            authentication_token = get_authorization_header(request).split()
            if authentication_token and len(authentication_token) == 2:
                authentication_token = authentication_token[1].decode('utf-8')

                user_id = decode_tokens(authentication_token, True)['user_id']
                user = Users.objects.get(user_id=user_id)

                return Response(UserSerializer(user).data, status=200)
        except exceptions.AuthenticationFailed:
            return Response({"message": "User is not authenticated."}, status=401)
        except Exception as e:
            return Response({"error": e.args}, status=500)


class RefreshToken(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            user_id = decode_tokens(refresh_token, False)['user_id']

            blacklist = redis_instance.lrange("blacklist", 0, -1)

            for each in blacklist:
                if each.decode('utf-8') == str(refresh_token):
                    return Response({"message": "User is not authenticated."}, status=401)

            access_token = create_tokens(user_id, True)
            response = Response({"access_token": access_token})
            response.set_cookie(key='access_token', value=access_token, httponly=True)

            return response
        except exceptions.AuthenticationFailed:
            return Response({"message": "User is not authenticated."}, status=401)
        except Exception as e:
            return Response({"error": e.args}, status=500)


class LogoutUser(APIView):
    authentication_classes = []
    def post(self, request):
        try:
            response = Response({"message": "User logged out successfully."})
            response.delete_cookie('access_token')

            redis_instance.lpush("blacklist", request.COOKIES.get('refresh_token'))

            response.delete_cookie('refresh_token')

            return response
        except Exception as e:
            return Response({"error": e.args}, status=500)
