from django.urls import path
from .views import AvailableSlotsView, BookAppointmentView, PatientBookingsView

urlpatterns = [
    path('slots/', AvailableSlotsView.as_view(), name='available-slots'),
    path('book/<int:pk>/', BookAppointmentView.as_view(), name='book-appointment'),
    path('my-bookings/', PatientBookingsView.as_view(), name='patient-bookings'),
]
