from .serializers import RideSerializer
from vuedj.celery import app
from django.apps import apps

ride_model = apps.get_model('app', 'Ride')


@app.task(name='mark_ride_as_complete')
def mark_ride_as_complete(**kwargs):
    ride_id = kwargs['ride_id']
    ride_obj = ride_model.objects.get(id=ride_id)
    serializer = RideSerializer(ride_obj, {'status': 'complete'})
    if serializer.is_valid():
        serializer.save()
        print "Completed the ride {id}".format(id=ride_id)
        print serializer.data
    else:
        print serializer.errors
    # Else: TODO: make an entry to the logs
