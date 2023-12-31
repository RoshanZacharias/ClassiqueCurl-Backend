from django.urls import path
from .views import SalonRegistrationView,SalonLoginView, SalonLogin, AddServiceView, SalonServicesView, AddStylistView, SalonStylistView, AddTimeSlotView, TimeSlotView, BookedAppointmentsView, OrderStatusUpdateView, SalonProfileAPIView, SalonNotificationsView, UpdateNotificationSeenStatusView



urlpatterns = [
    path('salon-register/', SalonRegistrationView.as_view(), name='salon-register'),
    path('salon-login/', SalonLoginView.as_view(), name='salon-login'),
    path('add-service/', AddServiceView.as_view(), name='add-service'),
    path('add-stylists/', AddStylistView.as_view(), name='add-stylists'),
    path('salon-services/', SalonServicesView.as_view(), name='salon-services'),
    path('salon-stylists/', SalonStylistView.as_view(), name='salon-stylists'),
    path('add-timeslot/', AddTimeSlotView.as_view(), name='add-timeslot'),
    path('salon-time-slot/', TimeSlotView.as_view(), name='time-slot'),
    path('booked-appointments/<int:salonId>/', BookedAppointmentsView.as_view(), name='booked-appointments'),
    path('order/update-status/<int:pk>/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('salon/<int:salon_id>/', SalonProfileAPIView.as_view(), name='salon-profile'),
    path('salon-notification/<int:pk>/', SalonNotificationsView.as_view(), name='salon-notification'),
    path('update-notification/<int:pk>/', UpdateNotificationSeenStatusView.as_view(), name='update-notification'),
]
    

