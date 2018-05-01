# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, permissions, status, generics
from .serializers import RideSerializer
from .tasks import *

ride_model = apps.get_model('app.Ride')


# Create your views here.
def index(request):
    return render(request, 'index.html')




def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html')


class RideViewSet(viewsets.ModelViewSet, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ride_model.objects.all().order_by('-modified_at')
    serializer_class = RideSerializer

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.data['user_id']
        except:
            return JsonResponse({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            requested = ride_model.objects.filter(user=user_id, status__in=['waiting', 'ongoing']).exists()
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

    def user_rides(self, request, *args, **kwargs):
        try:
            user_id = request.GET['id']
        except:
            return JsonResponse({"message": "Please provide a User ID to fetch the status"},
                                status=status.HTTP_400_BAD_REQUEST)
        try:
            existing_rides = ride_model.objects.filter(user=user_id).order_by('-created_at')
            rides = self.serializer_class(existing_rides, many=True)
            # return Response(JSONRenderer().render(rides.data))
            return JsonResponse({"rides": rides.data}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"message": "Something went wrong while fetching your status"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def unassigned_rides(self, request, *args, **kwargs):
        try:
            waiting_rides = ride_model.objects.filter(status='waiting')
            serializer = self.serializer_class(waiting_rides, many=True)
            return JsonResponse({"waiting_rides": serializer.data}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"message": "There was some error while fetching the waiting rides"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def current_driver_ride(self, request, *args, **kwargs):
        try:
            driver_id = request.GET['driver_id']
        except:
            return JsonResponse({"message": "Driver ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ride_details = ride_model.objects.filter(pickup_driver=driver_id, status='ongoing')
            if ride_details.exists():
                ride_details = ride_details[0]
                serializer = self.serializer_class(ride_details)
                return JsonResponse({"ride_details": serializer.data}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"ride_details": None}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"message": "Something went wrong while fetching your current ride details"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def completed_rides(self, request, *args, **kwargs):
        try:
            driver_id = request.GET['driver_id']
        except:
            return JsonResponse({"message": "Driver ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ride_history = ride_model.objects.filter(pickup_driver=driver_id, status='complete')
            serializer = self.serializer_class(ride_history, many=True)
            return JsonResponse({"completed_rides": serializer.data}, status=status.HTTP_200_OK)
        except:
            return JsonResponse({"message": "Something went wrong while fetching your current ride details"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def pickup_ride(self, request, *args, **kwargs):
        try:
            driver_id = request.data['driver_id']
            ride_id = request.data['ride_id']
        except:
            return JsonResponse({"message": "Driver ID or ride ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ride_obj = ride_model.objects.filter(id=ride_id, status='waiting')
            if ride_obj.exists():
                ride_obj = ride_obj[0]
                if ride_model.objects.filter(pickup_driver=driver_id, status='ongoing').exists():
                    return JsonResponse({"message": "You can only pickup one ride at a time."}, 
                        status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(ride_obj, {'status': 'ongoing', 'pickup_driver': driver_id})
                if serializer.is_valid():
                    serializer.save()
                    mark_ride_as_complete.apply_async(kwargs={'ride_id': ride_id}, countdown=settings.DEFAULT_RIDE_TIMEOUT)
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return JsonResponse({"message": "Ride no longer available.."}, status=status.HTTP_404_NOT_FOUND)
        except:
            return JsonResponse({"message": "Something went wrong while fetching your current ride details"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def latest_rides(self, request, *args, **kwargs):
    #     latest_rides = ride_model.objects.all().order_by('-modified_at')
    #     serializer = self.get_serializer(latest_rides, many=True)
    #     return JsonResponse({'latest_rides': serializer.data}, status=status.HTTP_200_OK)
