from django.urls import path

from core_apps.common.views import HealthCheckAPIView

urlpatterns = [
    path("healthcheck/", HealthCheckAPIView.as_view(), name="healthcheck"), 
]
