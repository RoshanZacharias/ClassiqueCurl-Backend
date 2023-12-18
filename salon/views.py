from django.shortcuts import render
from .models import HairSalon, Service, Stylist
from booking.models import Appointment, Order
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import HairSalonRegistrationSerializer, ServiceSerializer, StylistSerializer, TimeSlotSerializer, TimeSlot
from booking.serializers import AppointmentSerializer, OrderSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from booking.models import CustomUser
from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.middleware import csrf
import time
from django.http import JsonResponse
from rest_framework import generics

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
                response = JsonResponse({
                    "data": data,
                    "salon": {
                        "id": salon.id,
                        "username": salon.email,
                        "name": salon.salon_name,
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
        



class AddServiceView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract salon_id from the request data
        salon_id = request.data.get('salon_id')

        # Ensure that the salon_id is valid
        try:
            salon = HairSalon.objects.get(id=salon_id)
            print('****salon****', salon)
        except HairSalon.DoesNotExist:
            return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)

        # Associate the service with the salon
        request.data['salon'] = salon.id

        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AddStylistView(APIView):
    def post(self, request):
        salon_id = request.data.get('salon_id')
        try:
            salon = HairSalon.objects.get(id=salon_id)
            print('***Salon***', salon)
        except HairSalon.DoesNotExist:
            return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)
        request.data['salon'] = salon.id

        serializer = StylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


class SalonServicesView(APIView):
    def get(self, request):
        salon_id = request.query_params.get('salon_id', None)
        print(salon_id)
        salon = HairSalon.objects.get(id=salon_id)
        services = Service.objects.filter(salon=salon)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    





class SalonStylistView(APIView):
    def get(self, request):
        salon_id = request.query_params.get('salon_id', None)
        print(salon_id)
        salon = HairSalon.objects.get(id=salon_id)
        stylist = Stylist.objects.filter(salon=salon)
        serializer = StylistSerializer(stylist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AddTimeSlotView(APIView):
    def post(self, request, *args, **kwargs):
        salon_id = request.data.get('salon_id')
        try:
            salon = HairSalon.objects.get(id=salon_id)
            print('***Salon***', salon)
        except HairSalon.DoesNotExist:
            return Response({'error': 'Salon not found'}, status=status.HTTP_404_NOT_FOUND)
        request.data['salon'] = salon.id


        serializer = TimeSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TimeSlotView(APIView):
    def get(self, request):
        salon_id = request.query_params.get('salon_id', None)
        print(salon_id)
        salon = HairSalon.objects.get(id=salon_id)
        time_slots = TimeSlot.objects.filter(salon=salon)
        data = [{'day': slot.day, 'start_time': slot.start_time, 'end_time': slot.end_time} for slot in time_slots]
        return JsonResponse(data, safe=False)


class BookedAppointmentsView(APIView):
    def get(self, request, *args, **kwargs):
        salon_id = self.kwargs.get('salonId')
        bookings = Order.objects.filter(salon_id=salon_id)
        print(f"Salon ID: {salon_id}")
        print(f"Number of Booked Appointments: {bookings.count()}")
        serializer = OrderSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')
        instance.status = new_status
        instance.save()
        return Response({'message': 'Order status updated successfully'})