from django.shortcuts import render
from rest_framework import generics, permissions, status
# from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView,Response
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.middleware import csrf





class UserRegistrationView(APIView):
    def post(self, request, format=None):
        print("************************")
        print(request.data)
        print("************************")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)  # Generate token
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request, format=None):
        print('*******UserLoginView*******')
        email = request.data.get('email')
        print('*******email********', email)
        password = request.data.get('password')
        print("********password******", password)

        user = authenticate(request, email=email, password=password)

        print('******user********', user)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            print("*************access_token**************")
            print(access_token)

            # user_email = User.objects.get(email=user['email'])
            # tokens = RefreshToken.for_user(user_email).access_token

           
            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

            response['Set-Cookie'] = f'access_token={str(access_token)}; HttpOnly'  
            
            print(response.headers)
            return response

            # return Response({'message': 'Login successful','access_token':str(access_token), 'refresh_token':str(refresh)},status=status.HTTP_200_OK)
        else:
            print(f"Authentication failed for email: {email}")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
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



class LogoutView(APIView):
    def post(self, request, format=None):
        # Delete the access token cookie
        response = Response()

        # access_cookie_key = settings.SIMPLE_JWT.get('AUTH_COOKIE', 'access_token')
        # print('*******', access_cookie_key)
        response.delete_cookie('access_token')

        response.data = {"Success": "Logout successful"}
        return response
       
    

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]