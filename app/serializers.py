from rest_framework import serializers
from django.apps import apps
from .models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ('id', 'user', 'pickup_driver', 'status', 'created_at', 'modified_at')
