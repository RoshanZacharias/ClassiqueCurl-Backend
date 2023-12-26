from django.urls import path
from .views import *



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user-google-auth/', GoogleAuthLogin.as_view(), name='user-google-auth'),
    path('salon-detail/<int:id>/', SalonDetailsView.as_view(), name='salon-detail'),
    path('services/<int:salon_id>/', ServiceListView.as_view(), name='service-list-view'),
    path('stylists/<int:salon_id>/', StylistListView.as_view(), name='stylist-list-view'),
    path('time-slots/<int:salon_id>/', TimeSlotListView.as_view(), name='time-slot-list-view'),
    path('appointments/<int:userId>/', AppointmentCreateView.as_view(), name='create-appointment'),
    path('booking-overview/<int:pk>/', BookingOverviewAPIView.as_view(), name='booking-overview'),
    path('appointments/update-booking-status/', UpdateBookingStatusView.as_view(), name='update-booking-status'),
    path('bookings/<int:userId>/', UserBookingsView.as_view(), name='user-bookings'),
    path('orders/cancel/<int:orderId>/', OrderCancellationView.as_view(), name='order-cancellation'),
    path('orders/reimbursed-amount/<int:orderId>/', ReimbursedAmountView.as_view(), name='reimbursed-amount'),
    path('orders/reimbursed-sum/', ReimbursedSumView.as_view(), name='reimbursed-sum'),
    path('pay/<int:id>/', start_payment.as_view(), name="payment"),
    path('payment/success/', handle_payment_success.as_view(), name="payment_success"),
    path('wallet/<int:userId>/', WalletBalanceView.as_view(), name='wallet-balance'),
]