# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status
from .serializers import RideSerializer
from .models import Ride


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def userapp_view(request):
    if request.method == 'GET':
        return render(request, 'userapp.html')


def driverapp_view(request):
    if request.method == 'GET':
        return render(request, 'driverapp.html')


def dashboard_view(request):
    if request.method == 'GET':
        return render(request, 'dashboard.html')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RideSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.POST['user_id']
        except:
            return JsonResponse({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            requested = Ride.objects.filter(user=user_id, status__in=['waiting', 'ongoing']).exists()
            if requested:
                return JsonResponse({"message": "Request already registered"}, status=status.HTTP_202_ACCEPTED)
            else:
                new_ride = self.serializer_class(data={'user': user_id})
                if new_ride.is_valid():
                    new_ride.save()
                    return JsonResponse(new_ride.data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({"message": "Invalid data", "errors": new_ride.errors},
                                        status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({"message": "Something went wrong while requesting your ride"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
