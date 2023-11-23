from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, UserLoginView, LoginView, LogoutView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]