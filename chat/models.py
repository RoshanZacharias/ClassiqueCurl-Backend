from django.db import models
from booking.models import CustomUser, Order
from salon.models import HairSalon
# Create your models here.

class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(HairSalon, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='chat_messages', null=True)
    sendername = models.TextField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message}'