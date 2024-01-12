import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timesince import timesince

from .models import ChatMessage
from booking.models import CustomUser, Order
from salon.models import HairSalon
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.appointment_id = self.scope['url_route']['kwargs']['appointment_id']
        self.appointment = await self.get_appointment_instance(self.appointment_id)

        await self.channel_layer.group_add(
            f'chat_{self.appointment_id}',
            self.channel_name
        )

        await self.accept()
        
        # Fetch existing messages and send them to the connected client
        existing_messages = await self.get_existing_messages()
        for message in existing_messages:
            await self.send(text_data=json.dumps({
                'message': message['message'],
            }))

    @database_sync_to_async
    def get_existing_messages(self):
        # Assuming you have a ChatMessage model with a 'message' field
        messages = ChatMessage.objects.filter(appointment=self.appointment)
        return [{'message': message.message} for message in messages]

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f'chat_{self.appointment_id}',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sendername = data.get('sendername', 'Anonymous')

        await self.save_message(sendername, message)

        await self.channel_layer.group_send(
            f'chat_{self.appointment_id}',
            {
                'type': 'chat.message',
                'data': {
                'message': message,
                'sendername': sendername,
            },
            }
        )

    async def chat_message(self, event):
        message = event['data']['message']
        sendername = event['data']['sendername']

        await self.send(text_data=json.dumps({
            'message': message,
            'sendername': sendername,
        }))

    @classmethod
    async def send_chat_message(cls, appointment_id, message):
        await cls.send_group(f'chat_{appointment_id}', {
            'type': 'chat.message',
            'message': message,
        })

    @database_sync_to_async
    def get_appointment_instance(self, appointment_id):
        try:
            appointment = Order.objects.get(id=appointment_id)
            return appointment
        except Order.DoesNotExist:
            print("Failed to find the appointment")

    async def save_message(self,sendername, message):
        sender = await self.get_user_instance(self.appointment.user_id)
        receiver = await self.get_order_instance(self.appointment.salon_id)
        sendername = sendername
        await self.save_message_to_db(sender, receiver, sendername, message)

    @database_sync_to_async
    def save_message_to_db(self, sender, receiver, sendername, message):
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message,
            appointment=self.appointment,
            sendername=sendername
        )

    @database_sync_to_async
    def get_user_instance(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            print('User instance:', user)
            return user
        except CustomUser.DoesNotExist:
            print("Failed to find the user")

    @database_sync_to_async
    def get_order_instance(self, salon_id):
        try:
            salon = HairSalon.objects.get(id=salon_id)
            return salon
        except HairSalon.DoesNotExist:
            print("Failed to find the salon")