from rest_framework import serializers
from .models import CustomUser, Appointment, Order, Wallet, Notification
from salon.models import Service, Stylist, TimeSlot
from salon.serializers import ServiceSerializer, StylistSerializer, TimeSlotSerializer


class  UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 'mobile', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user 
    

class GoogleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email']

    def get_name(self, obj):
        return obj.get_full_name()
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        user = CustomUser.objects.create(**validated_data)
        user.email = email
        user.username = email
        user.save()
        return user
    


class AppointmentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)
    service = ServiceSerializer()
    stylist = StylistSerializer()
    time_slot = TimeSlotSerializer()

    # Include the 'price' field from the Service model
    price = serializers.IntegerField(source='service.price', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'user_id', 'user_name', 'user_email', 'salon', 'salon_name', 'service', 'stylist', 'date', 'time_slot', 'price', 'created_at', 'is_booked']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
                validated_data['user'] = user
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({'user_id': 'User not found.'})

        # Create or get the nested objects (Service, Stylist, TimeSlot)
        service_data = validated_data.pop('service', None)
        stylist_data = validated_data.pop('stylist', None)
        time_slot_data = validated_data.pop('time_slot', None)

        service_instance, _ = Service.objects.get_or_create(**service_data)
        stylist_instance, _ = Stylist.objects.get_or_create(**stylist_data)
        time_slot_instance, _ = TimeSlot.objects.get_or_create(**time_slot_data)
        time_slot_instance.is_booked = True
        time_slot_instance.save()

        validated_data['service'] = service_instance
        validated_data['stylist'] = stylist_instance
        validated_data['time_slot'] = time_slot_instance

        

        return super().create(validated_data)



class OrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")

    class Meta:
        model = Order
        fields = '__all__'
        depth = 2




class ReimbursedSumSerializer(serializers.Serializer):
    sum_reimbursed_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'





