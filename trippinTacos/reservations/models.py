from django.db import models
from guest.models import Guest
from django.utils import timezone
from datetime import date
from django.utils.timezone import now

# Create your models here.


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date = models.DateField(default=date.today, blank=False)
    time = models.TimeField(default=now(), blank=False)
    created_date = models.DateTimeField(default=timezone.now) #added this field for later use when adding statistics


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    opening_time = models.TimeField()
    closing_time = models.TimeField()


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    number_of_seats = models.IntegerField()
    is_occupied = models.BooleanField()


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=0)
    start_date_time = models.DateTimeField(default="1970-01-01")
    end_date_time = models.DateTimeField(default="1970-01-01")
    created_date = models.DateTimeField(default=timezone.now) # added this field for later use when adding statistics
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)

