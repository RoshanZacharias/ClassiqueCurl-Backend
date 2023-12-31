from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/salon-notification/<int:salon_id>/', consumers.NotificationConsumer.as_asgi()),

]
