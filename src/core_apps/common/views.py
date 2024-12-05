from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from core_apps.common.utils import get_current_host, generate_full_url


class HealthCheckAPIView(APIView):
    """Health Check API View"""

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        
        host = request.get_host()
        
        return Response(
            {"status": "OK", "host": host},
            status=HTTP_200_OK,
        )
