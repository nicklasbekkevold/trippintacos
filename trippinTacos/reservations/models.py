from django.db import models
from guest.models import Guest
from django.utils import timezone
# Create your models here.



class Restaurant(models.Model):
    


class Table(models.Model):
    number_of_seats = models.IntegerField()
    is_occupied = models.BooleanField()
    reservation = models.ForeignKey(Reservation, models.SET_NULL, blank=True, null=True)


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    created_date = models.DateTimeField(default=timezone.now) # added this field for later use when adding statistics
    table = models.ForeignKey(Table, on_delete=pass)