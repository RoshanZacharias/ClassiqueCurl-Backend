
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
        # self.room_group_name = f"notify_{salon.id}"
        # salon_channel = f"salon_{instance.salonUser.id}"
        salon_channel = f"notify_{instance.salonUser.id}"
        # notifications = Notification.objects.filter(receiver_type='SALONUSER', salonUser=salon)
        serialized_instance = SalonNotificationSerializer(instance).data

        
  
        async_to_sync(channel_layer.group_send)(
            salon_channel,
            {
                "type": "send_notification",
                # "message": "New Booked Appointment",
                "value": json.dumps(serialized_instance),
            }
        )




# @receiver(post_save, sender=Notification)
# def notification_post_save_handler(sender, instance, created, **kwargs):
#     user = instance.to_user
#     if user.is_authenticated:
#         channel_layer = get_channel_layer()
#         if created:
#             count = Notification.objects.filter(is_seen=False, to_user=user).count()
#             serialized_instance = NotificationSerializer(instance).data
#             async_to_sync(channel_layer.group_send)(
#                 f"notify_{user.id}",
#                 {
#                     "type": "send_notification",
#                     "value": json.dumps(serialized_instance),
#                 }
#             )



# @receiver(post_save, sender=Order)
# def order_post_save_handler(sender, instance, created, **kwargs):
#     if created:
#         salon_user = instance.salon.user  # Assuming there is a ForeignKey from Order to HairSalon
#         print('SALON USER:', salon_user)

#         if salon_user:
#             channel_layer = get_channel_layer()
#             notification_type = 'booked'  # You can adjust this based on your notification types
#             message = f'New {notification_type.capitalize()} Order'
#             print("MESSAGE:", message)
            
#             Notification.objects.create(
#                 customer=instance.user,
#                 salonUser=salon_user,
#                 receiver_type='salonuser',
#                 message=message,
#                 notification_type=notification_type,
#             )

#             serialized_instance = {'order_id': instance.id, 'order_service': instance.order_service}
#             print("SERIALIZED INSTANCE:", serialized_instance)
#             async_to_sync(channel_layer.group_send)(
#                 f"notify_{salon_user.id}",
#                 {
#                     "type": "send_notification",
#                     "value": json.dumps(serialized_instance),
#                 }
#             )
