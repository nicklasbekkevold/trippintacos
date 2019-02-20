from django import forms
from .models import *


class ReservationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    reminder = forms.BooleanField()

    class Meta:
        model = Reservation
        fields = ('number_of_people', 'start_date_time', 'end_date_time', 'created_date',
                  )



class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'opening_time', 'closing_time',)


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('restaurant', 'number_of_seats', 'is_occupied',)
