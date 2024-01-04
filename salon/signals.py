
#signals.py


from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from booking.models import Notification, Order

from .serializers import SalonNotificationSerializer
import json


@receiver(post_save, sender=Notification)
def create_notification_for_salon(sender, instance, created, **kwargs):
    salon = instance.salonUser
    if salon and created:

        # Send notification using channels to salon's channel
        channel_layer = get_channel_layer()
        salon_channel = f"notify_{instance.salonUser.id}"
        serialized_instance = SalonNotificationSerializer(instance).data

        
  
        async_to_sync(channel_layer.group_send)(
            salon_channel,
            {
                "type": "send_notification",
                "value": json.dumps(serialized_instance),
            }
        )







