from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer
from doctor.models import Availability
from doctor.serializers import AvailabilitySerializer
from django.utils import timezone

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient

class AvailableSlotsView(generics.ListAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Availability.objects.filter(
            is_booked=False,
            start_time__gt=timezone.now()
        )

class BookAppointmentView(views.APIView):
    permission_classes = [IsPatient]

    def post(self, request, pk):
        try:
            with transaction.atomic():
                # Lock the availability row
                availability = Availability.objects.select_for_update().get(pk=pk)
                
                if availability.is_booked:
                    return Response(
                        {"error": "This slot is already booked."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create booking
                booking = Booking.objects.create(
                    patient=request.user,
                    availability=availability
                )
                
                # Mark as booked
                availability.is_booked = True
                availability.save()
                
                # Trigger email and calendar sync
                try:
                    from backend.services.calendar_service import CalendarService
                    from backend.services.email_client import EmailClient
                    
                    # Send Email to Patient
                    email_client = EmailClient()
                    email_client.send_email(
                        recipient=request.user.email,
                        subject="Booking Confirmation",
                        message=f"Your appointment with Dr. {availability.doctor.username} is confirmed for {availability.start_time}."
                    )
                    
                    # Create Calendar Event
                    calendar_service = CalendarService()
                    calendar_service.create_event(
                        doctor_email=availability.doctor.email,
                        patient_email=request.user.email,
                        start_time=availability.start_time,
                        end_time=availability.end_time,
                        summary=f"Appointment: {request.user.username} with Dr. {availability.doctor.username}"
                    )
                except Exception as e:
                    print(f"Error in post-booking actions: {e}")
                
                return Response(
                    BookingSerializer(booking).data,
                    status=status.HTTP_201_CREATED
                )
        except Availability.DoesNotExist:
            return Response(
                {"error": "Availability slot not found."},
                status=status.HTTP_404_NOT_FOUND
            )

class PatientBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return Booking.objects.filter(patient=self.request.user)
