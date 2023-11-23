from rest_framework import serializers
from booking.models import CustomUser
from salon.models import HairSalon



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_blocked')
        

class HairSalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairSalon
        fields = '__all__'