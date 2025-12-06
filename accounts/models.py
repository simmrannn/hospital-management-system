from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, default="General")

    def __str__(self):
        return f"Dr. {self.user.username}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Patient: {self.user.username}"
