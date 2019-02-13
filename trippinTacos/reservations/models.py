from django.db import models
from guest.models import Guest
from django.utils import timezone
# Create your models here.


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_date = models.DateTimeField(default=timezone.now) #added this field for later use when adding statistics


class Table(models.Model):
    number_of_seats = models.IntegerField()
    is_occupied = models.BooleanField()
    reservation = models.ForeignKey(Reservation, models.SET_NULL, blank=True, null=True)


