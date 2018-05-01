# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from .tasks import mark_ride_as_complete


# @receiver(post_save, sender='app.Ride')
# def auto_mark_ride_complete(ride_instance, **kwargs):
#     if ride_instance.status == 'ongoing':
#         mark_ride_as_complete.apply_async(kwargs={'ride_id': ride_instance.id}, countdown=settings.DEFAULT_RIDE_TIMEOUT)
