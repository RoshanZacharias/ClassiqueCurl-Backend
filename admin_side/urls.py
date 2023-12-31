from django.urls import path
from .views import AdminLoginView, SalonListView, UserListView, SalonDetailsView, UserBlockView, UserUnblockView, LatestPaidOrdersView, UserSearchView



urlpatterns = [
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('salon-list/', SalonListView.as_view(), name='salon-list'),
    path('salon-request-approval/<int:salonId>/', SalonDetailsView.as_view(), name='salon-request-approval'),
    path('salon-list/<int:salonId>/', SalonDetailsView.as_view(), name='salon-details'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/block/', UserBlockView.as_view(), name='user-block'),
    path('users/<int:user_id>/unblock/', UserUnblockView.as_view(), name='user-unblock'),
    path('latest-paid-orders/', LatestPaidOrdersView.as_view(), name='latest-paid-orders'),
    path('salons/', SalonListView.as_view(), name='salon-list'),
    path('users/search/', UserSearchView.as_view(), name='user-search'),
]