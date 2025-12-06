from rest_framework import serializers
from .models import Booking
from doctor.serializers import AvailabilitySerializer

class BookingSerializer(serializers.ModelSerializer):
    availability_details = AvailabilitySerializer(source='availability', read_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'patient', 'availability', 'availability_details', 'created_at')
        read_only_fields = ('patient', 'created_at')
