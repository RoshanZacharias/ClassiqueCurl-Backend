from django.shortcuts import render
from rest_framework import generics, permissions, status
# from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Appointment, Order, ReimbursedAmount, Wallet, Notification
from salon.models import HairSalon, Service, Stylist, TimeSlot
from .serializers import UserRegistrationSerializer, GoogleUserSerializer, AppointmentSerializer, OrderSerializer, WalletSerializer
from salon.serializers import HairSalonRegistrationSerializer, ServiceSerializer, StylistSerializer, TimeSlotSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView,Response
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.middleware import csrf
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
import environ
import razorpay
import json
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal
from django.db import transaction 
from rest_framework.generics import RetrieveAPIView
from django.db.models import Q

from .serializers import WalletSerializer





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
        selected_date = request.data.get('date')
        print('selected_date:', selected_date)
        selected_time_slot_str = request.data.get('time_slot')['start_time']
        selected_time_slot = datetime.strptime(selected_time_slot_str, '%H:%M:%S').time()
        print('selected_time_slot:', selected_time_slot)

        if Appointment.objects.filter(date=selected_date, time_slot__start_time=selected_time_slot).exists():
            print('***Time slot already booked***')
            return Response({'error': 'This time slot is already booked'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        orders = Order.objects.filter(user_id=user_id)  
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class OrderCancellationView(APIView):
    def patch(self, request, orderId, *args, **kwargs):
        try:
            order = Order.objects.get(id=orderId)
            if order.isPaid and order.status == 'Pending':
                order_amount_decimal = Decimal(order.order_amount)
                reimbursed_amount = order_amount_decimal - order.convenience_fee
                print('reimbursed_amount:', reimbursed_amount)
                remaining_amount = order_amount_decimal - order.convenience_fee

                with transaction.atomic():
                    # Check if the user has a wallet
                    wallet, created = Wallet.objects.get_or_create(user=order.user, defaults={'balance': Decimal('0.00')})


                    # Update user's wallet balance
                    wallet.balance += remaining_amount
                    wallet.save()

                    # Create a record for the reimbursed amount
                    ReimbursedAmount.objects.create(user=order.user, order=order, amount=reimbursed_amount)

                    # Update order status
                    order.status = 'Cancelled'
                    order.save()
                return Response({'message': 'Order canceled successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
            

class ReimbursedAmountView(APIView):
    def get(self, request, orderId, *args, **kwargs):
        try:
            order = Order.objects.get(id=orderId)
            return Response({'reimbursed_amount': order.reimbursed_amount}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        


class WalletBalanceView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('userId')
        print('userId', user_id)
        wallet = get_object_or_404(Wallet, user_id=user_id)

        
        response_data = {
            'user_id': user_id,
            'wallet_balance': float(wallet.balance),  # Convert Decimal to float for JSON serialization
        }

        return Response(response_data, status=status.HTTP_200_OK)
        


class ReimbursedSumView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        sum_reimbursed_amount = ReimbursedAmount.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        return Response({'sum_reimbursed_amount': sum_reimbursed_amount}, status=status.HTTP_200_OK)


env = environ.Env()
environ.Env.read_env()

class start_payment(APIView):
    def post(self,request,id):
        print("***REQUEST DATA***", request.data)
        service_name = request.data['service_name']
        stylist_name = request.data['stylist_name']
        amount = request.data['amount']
        user_id = request.data['user']
        user_name = request.data['user_name']
        user_email = request.data['user_email']
        salon_id = request.data['salon']
        salon_name = request.data['salon_name']
        time_slot_date = request.data['time_slot_date']
        time_slot_day = request.data['time_slot_day']
        time_slot_start_time = request.data['time_slot_start_time']
        time_slot_end_time = request.data['time_slot_end_time']

        user = get_object_or_404(CustomUser, id=user_id)
        salon = get_object_or_404(HairSalon,id=salon_id)

        print("Razorpay Public Key:", env('PUBLIC_KEY'))
        print("Razorpay Secret Key:", env('SECRET_KEY'))

        client = razorpay.Client(auth=("rzp_test_ZQL2ChZEK9SL7A", "qiIPMJQP7dND0mDggXkRa3Xr"))

        payment = client.order.create({
        "amount": int(float(amount) * 100),  
        "currency": "INR",
        "payment_capture": "1"
         })
        try:
            # Create an Order object in the database
            order = Order.objects.create(
                order_service=service_name,
                order_stylist=stylist_name,
                order_amount=amount,
                order_payment_id=payment['id'],
                user= user,
                user_name=user_name,
                user_email=user_email,
                salon=salon,
                salon_name=salon_name,
                time_slot_date=time_slot_date,
                time_slot_day=time_slot_day,
                time_slot_start_time=time_slot_start_time,
                time_slot_end_time=time_slot_end_time
            )
            
            print('***order***', order)

            serializer = OrderSerializer(order)
            print('***serializer data***', serializer.data)

            data = {
                "payment": payment,
                "order": serializer.data
            }
            print('***data***', data)
            
            return Response(data)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': 'Object does not exist'}, status=404)
        except Exception as e:
            # Log the error for debugging
            print(f"Error during payment processing: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)





class handle_payment_success(APIView):
    def post(self, request):
        print('*********handle_payment_success************')
        # request.data is coming from frontend
        res = json.loads(request.data["response"])
        print('***res***', res)


        

        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]


        print('Order Payment ID:', ord_id)

        # get order by payment_id which we've created earlier with isPaid=False
        order = Order.objects.get(order_payment_id=ord_id)
        print('***order***', order)

        # we will pass this whole data in razorpay client to verify the payment
        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        client = razorpay.Client(auth=("rzp_test_ZQL2ChZEK9SL7A", "qiIPMJQP7dND0mDggXkRa3Xr"))

        # checking if the transaction is valid or not by passing above data dictionary in 
        # razorpay client if it is "valid" then check will return None
        check = client.utility.verify_payment_signature(data)
        print('***CHECK***', check)

        if check is  None:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'})

        # if payment is successful that means check is None then we will turn isPaid=True
        order.isPaid = True
        order.save()

        Notification.objects.create(
            customer=order.user, salonUser=order.salon, message=f'{order.user_name} has booked an appointment.',
            receiver_type=Notification.RECEIVER_TYPE[1][0],notification_type=Notification.NOTIFICATION_TYPES[0][0]
            )

        res_data = {
            'message': 'payment successfully received!'
        }

        return Response(res_data)



# @api_view(['POST'])
# def start_payment(request):
#     try:
#         # request.data is coming from frontend
#         amount = request.data['amount']
#         print('****AMOUNT****', amount)
#         service_name = request.data['service_name']
#         print('****SERVICE_NAME****', service_name)
#         stylist_name = request.data['stylist_name']
#         print('****STYLIST_NAME****', stylist_name)
#         print("**************")

#         # setup razorpay client this is the client to whome user is paying money that's you
#         client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
#         print('***CLIENT***', client)

#         # create razorpay order
#         # the amount will come in 'paise' that means if we pass 50 amount will become
#         # 0.5 rupees that means 50 paise so we have to convert it in rupees. So, we will 
#         # mumtiply it by 100 so it will be 50 rupees.
#         payment = client.order.create({"amount": int(amount) * 100, 
#                                     "currency": "INR", 
#                                     "payment_capture": "1"})
#         print("***PAYMENT***", payment)

#         # we are saving an order with isPaid=False because we've just initialized the order
#         # we haven't received the money we will handle the payment succes in next 
#         # function
#         order = Order.objects.create(order_service=service_name,
#                                     order_stylist=stylist_name,
#                                     order_amount=amount, 
#                                     order_payment_id=payment['id'])
#         print('***order***', order)

#         serializer = OrderSerializer(order)
#         print('***serailzier***', serializer.data)

       

#         data = {
#             "payment": payment,
#             "order": serializer.data
#         }
#         print('***data***', data)
#         return Response(data)
#     except ObjectDoesNotExist as e:
#         return JsonResponse({'error': 'Object does not exist'}, status=404)
#     except Exception as e:
#         # Log the error for debugging
#         print(f"Error during payment processing: {str(e)}")
#         return JsonResponse({'error': 'Internal Server Error'}, status=500)





class UserProfileAPIView(APIView):
    def get(self, request,user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer = UserRegistrationSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'detail:', 'User not found'}, status=status.HTTP_404_NOT_FOUND)


    

class UserProfilePictureUpload(APIView):
    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            print('***USER***', user)

            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
                user.save()

                serializer = UserRegistrationSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No profile picture provided"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        


class SalonSearchView(APIView):
    def get(self, request, *args, **kwargs):
        print('request:', request)
        try:
            search_term = request.query_params.get('search', '')
            salons = HairSalon.objects.filter(
                Q(salon_name__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(location__icontains=search_term)

            )
            print('SALONS:', salons)
            serializer = HairSalonRegistrationSerializer(salons, many=True)
            print("serializer serializer ", serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)