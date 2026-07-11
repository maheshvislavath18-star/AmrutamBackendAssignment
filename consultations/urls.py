from django.urls import path
from .views import ConsultationListCreateView, ConsultationDetailView

urlpatterns = [
    path("", ConsultationListCreateView.as_view()),
    path("<int:pk>/", ConsultationDetailView.as_view()),
]