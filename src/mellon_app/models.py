from django.conf import settings
from django.db import models

class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    date = models.DateTimeField
    has_reminder = models.BooleanField
    day_of_week = models.IntegerField

class Reminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateTimeField
    sent = models.BooleanField(default=False)