from rest_framework import serializers
from .models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('user', 'pickup_driver', 'status', 'created_at', 'modified_at')
