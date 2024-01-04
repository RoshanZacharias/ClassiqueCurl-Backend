from rest_framework import serializers
from .models import HairSalon, Service, Stylist, TimeSlot
from booking.models import Notification


class HairSalonRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairSalon
        fields = ('id', 'salon_name', 'email', 'mobile', 'password', 'licence', 'licence_number', 'profile_picture', 'salon_image', 'location', 'is_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = HairSalon.objects.create_user(**validated_data)
        return user
    


class ServiceSerializer(serializers.ModelSerializer):
    salon_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Service
        fields = ['id', 'service_name', 'description', 'price', 'salon_id', 'salon']
        read_only_fields = ['salon']

    def create(self, validated_data):
        # Pop salon_id from validated_data and associate the service with the salon
        salon_id = validated_data.pop('salon_id', None)
        if salon_id:
            try:
                salon = HairSalon.objects.get(id=salon_id)
                validated_data['salon'] = salon
            except HairSalon.DoesNotExist:
                raise serializers.ValidationError({'salon_id': 'Salon not found.'})

        return super().create(validated_data)




class StylistSerializer(serializers.ModelSerializer):
    salon_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Stylist
        fields = ['id', 'stylist_name', 'stylist_image', 'salon_id', 'salon']
        read_only_fields = ['salon']

    def create(self, validated_data):
        # Pop salon_id from validated_data and associate the service with the salon
        salon_id = validated_data.pop('salon_id', None)
        if salon_id:
            try:
                salon = HairSalon.objects.get(id=salon_id)
                validated_data['salon'] = salon
            except HairSalon.DoesNotExist:
                raise serializers.ValidationError({'salon_id': 'Salon not found.'})

        return super().create(validated_data)







class TimeSlotSerializer(serializers.ModelSerializer):
    salon_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = TimeSlot
        fields = ['id', 'day', 'start_time', 'end_time', 'salon_id', 'salon']

    def create(self, validated_data):
        # Pop salon_id from validated_data and associate the service with the salon
        salon_id = validated_data.pop('salon_id', None)
        if salon_id:
            try:
                salon = HairSalon.objects.get(id=salon_id)
                validated_data['salon'] = salon
            except HairSalon.DoesNotExist:
                raise serializers.ValidationError({'salon_id': 'Salon not found.'})

        return super().create(validated_data)
        



class SalonNotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = HairSalon
        fields = ('id', 'salon_name', 'email')



class SalonNotificationSerializer(serializers.ModelSerializer):
    from_user = SalonNotifySerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('notification_type',)

    def validate_notification_type(self, value):
        choices = dict(Notification.NOTIFICATION_TYPES)
        if value not in choices:
            raise serializers.ValidationError("Invalid notification type.")
        return value