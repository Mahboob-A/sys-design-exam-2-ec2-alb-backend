from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class HealthCheckAPIView(APIView):
    """Health Check API View"""
    
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"})