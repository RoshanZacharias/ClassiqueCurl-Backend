from django.shortcuts import render
from .models import HairSalon
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import HairSalonRegistrationSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from booking.models import CustomUser
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.middleware import csrf
# Create your views here.




class SalonRegistrationView(APIView):
    def post(self, request, format=None):
        print("************************")
        print(request.data)
        print(request.FILES)
        print("************************")
        serializer = HairSalonRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    





class SalonLoginView(APIView):
        def authenticatesalon(self, email, password):
             user = HairSalon.objects.filter(email=email, password=password).first()  # Example query based on username
             if user and user.check_password(password):
                return user
        
        def post(self, request, format=None):
            response = Response()
            email = request.data.get('email')
            print('*****email******', email)
            password = request.data.get('password')
            print('*****password*****', password)
            salon = HairSalon.objects.get(email=email)
       
             # salon = self.authenticatesalon(email=email, password=password)
            print('*******', salon)


            if salon is not None and check_password(password, salon.password) and salon.is_verified:
                data = get_tokens_for_user(salon)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","data":data}
                return response
            else:
                print(f'Authentication failed for email:{email}')
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            


def get_tokens_for_user(salon):
    refresh = RefreshToken.for_user(salon)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SalonLogin(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        print(f"Email: {email}, Password: {password}")
        salon = authenticate(email=email, password=password)
        print(f"Authenticated User: {salon}")

        if salon is not None:
            if salon.is_active:
                data = get_tokens_for_user(salon)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","data":data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)