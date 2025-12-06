from django.db import models
from django.conf import settings
from doctor.models import Availability

class Booking(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE, related_name='booking')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.patient.username} with {self.availability.doctor.username}"
