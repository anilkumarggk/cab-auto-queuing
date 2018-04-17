# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


RIDE_STATUS_CHOICES = (
    ('waiting', 'Waiting'),
    ('ongoing', 'Ongoing'),
    ('complete', 'Complete')
)

AVAILABLE_DRIVER_CHOICES = (
    ('driver1', 'Driver 1'),
    ('driver2', 'Driver 2'),
    ('driver3', 'Driver 3'),
    ('driver4', 'Driver 4'),
    ('driver5', 'Driver 5')
)


class Ride(models.Model):
    user = models.IntegerField(null=False, default=0)
    status = models.CharField(choices=RIDE_STATUS_CHOICES, default='waiting', max_length=64)
    pickup_driver = models.CharField(choices=AVAILABLE_DRIVER_CHOICES, null=True, max_length=64)
