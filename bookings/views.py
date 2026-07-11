from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import IsAdmin, IsPatient


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    # Search, Filter & Ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "appointment_date"]
    search_fields = ["doctor__user__username"]
    ordering_fields = ["appointment_date"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Appointment.objects.all()

        elif user.role == "DOCTOR":
            return Appointment.objects.filter(doctor__user=user)

        return Appointment.objects.filter(patient=user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsPatient()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Appointment.objects.all()

        elif user.role == "DOCTOR":
            return Appointment.objects.filter(doctor__user=user)

        return Appointment.objects.filter(patient=user)