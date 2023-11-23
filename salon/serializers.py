from rest_framework import serializers
from .models import HairSalon



class HairSalonRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HairSalon
        fields = ('id', 'salon_name', 'email', 'mobile', 'password', 'licence', 'licence_number', 'salon_image', 'location', 'is_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = HairSalon.objects.create_user(**validated_data)
        return user