from django.contrib import admin
from reservations.models import Restaurant, Reservation, Table


admin.site.register(Reservation)
admin.site.register(Restaurant)
admin.site.register(Table)
