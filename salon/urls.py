from django.urls import path
from .views import SalonRegistrationView,SalonLoginView, SalonLogin



urlpatterns = [
    path('salon-register/', SalonRegistrationView.as_view(), name='salon-register'),
    path('salon-login/', SalonLoginView.as_view(), name='salon-login'),
    
]
