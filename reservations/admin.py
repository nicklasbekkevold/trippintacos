from django.contrib import admin
from .models import Restaurant, Reservation, Table
# Register your models here.
admin.site.register(Reservation)
admin.site.register(Restaurant)
admin.site.register(Table)