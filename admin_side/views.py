from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .serializers import AdminSerializer, HairSalonSerializer
from salon.models import HairSalon
from booking.models import CustomUser, Order
from booking.serializers import OrderSerializer, UserRegistrationSerializer
from rest_framework import generics
from django.db.models import Q

# Create your views here.

class AdminLoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        password = request.data.get('password')
        print('******email******', email)


        user = authenticate(request, email=email, password=password)
        print('***********', user)

        if user is not None and user.is_staff:
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



class SalonListView(APIView):
    def get(self, request, format=None):
        salons = HairSalon.objects.all()
        serializer = HairSalonSerializer(salons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class SalonDetailsView(APIView):
    def get(self, request, salonId, format=None):
        print(salonId)
        salon = get_object_or_404(HairSalon, id=salonId)

        print('*****************************')
        print(salon)
        serializer = HairSalonSerializer(salon)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, salonId, format=None):
        salon = get_object_or_404(HairSalon, id=salonId)
        if salon.is_verified == True:
            salon.is_verified = False
            salon.save()
        else:
            salon.is_verified = True
            salon.save()
        
        
        
        return Response({'message': 'Salon verified successfully'}, status=status.HTTP_200_OK)
    

class UserListView(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = AdminSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserBlockView(APIView):
    def post(self, request,user_id, format=None):
        user = CustomUser.objects.get(id=user_id)
        user.is_blocked = True
        user.save()
        serializer = AdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserUnblockView(APIView):
    def post(self, request, user_id, format=None):
        user = CustomUser.objects.get(id=user_id)
        user.is_blocked = False
        user.save()
        serializer = AdminSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LatestPaidOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(isPaid=True).order_by('-order_date')
    


class SalonListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            salons = HairSalon.objects.all()
            serializer = HairSalonSerializer(salons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UserSearchView(APIView):
    def get(self, request, *args, **kwargs):
        print('request:', request)
        try:
            search_term = request.query_params.get('search', '')
            users = CustomUser.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(email__icontains=search_term)

            )
            print('USERS:', users)
            serializer = UserRegistrationSerializer(users, many=True)
            print("serializer serializer ", serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)