from django.db import models
from guest.models import Guest
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'reservations'


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, unique=False)
    number_of_seats = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'reservations'


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=0)
    start_date_time = models.DateTimeField(default=timezone.now)
    end_date_time = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)  # added this field for later use when adding statistics
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    walkin = models.BooleanField(default=False)
    reminder = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.start_date_time) + " ID: " + str(self.id)

    class Meta:
        app_label = 'reservations'

class NewReservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    number_of_people = models.IntegerField(default=1)
    start_date = models.DateField(default=timezone.now)
    start_time = models.IntegerField()
    end_time = models.TimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)  # added this field for later use when adding statistics
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True, blank=True)
    walkin = models.BooleanField(default=False)
    reminder = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return str(self.start_date + self.start_time)

    class Meta:
        app_label = 'reservations'