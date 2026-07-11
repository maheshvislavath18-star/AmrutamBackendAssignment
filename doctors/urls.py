from django.urls import path
from .views import DoctorListCreateView, DoctorDetailView, AvailabilityListCreateView

urlpatterns = [
    path("", DoctorListCreateView.as_view()),
    path("<int:pk>/", DoctorDetailView.as_view()),
    path("availability/", AvailabilityListCreateView.as_view()),
]