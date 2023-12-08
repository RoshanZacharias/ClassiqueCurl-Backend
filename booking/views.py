from django.shortcuts import render
from rest_framework import generics, permissions, status
# from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Appointment
from salon.models import HairSalon, Service, Stylist, TimeSlot
from .serializers import UserRegistrationSerializer, GoogleUserSerializer, AppointmentSerializer
from salon.serializers import HairSalonRegistrationSerializer, ServiceSerializer, StylistSerializer, TimeSlotSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView,Response
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.middleware import csrf
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404





class UserRegistrationView(APIView):
    def post(self, request, format=None):
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
                response = JsonResponse({
                    "data": data,
                    "user": {
                        "id": user.id,
                        "username": user.email,
                        "name": user.first_name,
                    }
                })
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



# class LogoutView(APIView):
#     print("res**********************************")
#     def post(self, request):
#         print("res**********************************")
#         response = JsonResponse({"message": "Logged out successfully"})

#         # Clear the authentication cookie
#         response.delete_cookie(
#             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#             path='/',
#             domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
#         )

#         # Expire the cookie immediately
#         response.set_cookie(
#             key=settings.SIMPLE_JWT['AUTH_COOKIE'],
#             value='',
#             expires=timezone.now() - timedelta(days=1),
#             path='/',
#             domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
#         )
#         print("res**********************************")
#         return response
       

class LogoutView(APIView):
    def get(self, request):
        response = JsonResponse({"message": "Logged out successfully"})

        # Clear the authentication cookie
        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            path='/',
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None)  # Set to None if not present
        )

        # Expire the cookie immediately
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value='',
            expires=timezone.now() - timedelta(days=1),
            path='/',
            domain=settings.SIMPLE_JWT.get('AUTH_COOKIE_DOMAIN', None)  # Set to None if not present
        )

        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]



class GoogleAuthLogin(APIView):
    def post(self, request):
        data = request.data
        print('*****', data)
        email = data.get('email', None)
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            if user is not None:
                if user.is_active:
                    data = get_tokens_for_user(user)
                    response = JsonResponse({
                        "data": data,
                        "user": {
                            "id": user.id,
                            "username": user.email,
                            "name": user.first_name,
                        }
                    })
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
            serializer = GoogleUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                if user is not None:
                    if user.is_active:
                        data = get_tokens_for_user(user)
                        response = JsonResponse({
                            "data": data,
                            "user": {
                                "id": user.id,
                                "username": user.email,
                                "name": user.first_name,
                            }
                        })
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





class SalonDetailsView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            salon = HairSalon.objects.get(id=id)
        except HairSalon.DoesNotExist:
            return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = HairSalonRegistrationSerializer(salon)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ServiceListView(APIView):
    def get(self, request, salon_id):
        services = Service.objects.filter(salon_id=salon_id)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class StylistListView(APIView):
    def get(self, request, salon_id):
        stylists = Stylist.objects.filter(salon_id=salon_id)
        serializer = StylistSerializer(stylists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TimeSlotListView(APIView):
    def get(self, request, salon_id):
        time_slots = TimeSlot.objects.filter(salon_id=salon_id)
        serializer = TimeSlotSerializer(time_slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class AppointmentCreateView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookingOverviewAPIView(APIView):
    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('pk')
        appointment = get_object_or_404(Appointment, id=appointment_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class UpdateBookingStatusView(APIView):
    def patch(self, request, *args, **kwargs):
        appointment_id = request.data.get('appointmentId')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_booked = True
            appointment.save()
            return Response({'detail': 'Booking status updated successfully'})
        except Appointment.DoesNotExist:
            return Response({'detail': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        



class UserBookingsView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('userId')
        bookings = Appointment.objects.filter(user_id=user_id, is_booked=True)
        serializer = AppointmentSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class BookingCancellationView(APIView):
        def patch(self, request, appointmentId, *args, **kwargs):
            try:
                appointment = Appointment.objects.get(id=appointmentId)
                appointment.is_booked = False
                appointment.save()
                return Response({'message': 'Booking canceled successfully'}, status=status.HTTP_200_OK)
            except Appointment.DoesNotExist:
                return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)