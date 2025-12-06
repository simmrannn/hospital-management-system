from rest_framework import serializers
from .models import Availability

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('id', 'doctor', 'start_time', 'end_time', 'is_booked')
        read_only_fields = ('doctor', 'is_booked')
