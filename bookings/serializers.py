from rest_framework import serializers
from .models import Appointment
from doctors.models import Availability


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["patient"]

    def validate(self, data):
        doctor = data["doctor"]
        appointment_date = data["appointment_date"]
        appointment_time = data["appointment_time"]

        # Prevent double booking
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already booked for this slot."
            )

        # Check doctor availability
        day_name = appointment_date.strftime("%A")

        available = Availability.objects.filter(
            doctor=doctor,
            day=day_name,
            is_available=True,
            start_time__lte=appointment_time,
            end_time__gte=appointment_time
        ).exists()

        if not available:
            raise serializers.ValidationError(
                "Doctor is not available at this time."
            )

        return data