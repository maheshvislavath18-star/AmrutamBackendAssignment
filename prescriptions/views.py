from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Prescription
from .serializers import PrescriptionSerializer
from accounts.permissions import IsAdmin, IsDoctor

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class PrescriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = [
        "appointment",
    ]

    search_fields = [
        "medicines",
        "instructions",
    ]

    ordering_fields = [
        "created_at",
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Prescription.objects.all()

        elif user.role == "DOCTOR":
            return Prescription.objects.filter(
                appointment__doctor__user=user
            )

        return Prescription.objects.filter(
            appointment__patient=user
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsDoctor()]
        return [IsAuthenticated()]


class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":
            return Prescription.objects.all()

        elif user.role == "DOCTOR":
            return Prescription.objects.filter(
                appointment__doctor__user=user
            )

        return Prescription.objects.filter(
            appointment__patient=user
        )

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsDoctor()]
        return [IsAuthenticated()]