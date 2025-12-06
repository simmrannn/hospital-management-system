from rest_framework import generics, permissions
from .models import Availability
from .serializers import AvailabilitySerializer
from django.utils import timezone

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor

class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class AvailabilityDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        return Availability.objects.filter(doctor=self.request.user)
