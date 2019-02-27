from django import forms
from .models import *
from bootstrap_datepicker_plus import *
from employee.helpers import get_all_booked_dates_and_time

class ReservationForm(forms.Form):
    email = forms.EmailField(required=True)
    reminder = forms.BooleanField()
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
        )
    )
    end_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
        )
    )


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'opening_time', 'closing_time',)


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ('restaurant', 'number_of_seats', 'is_occupied',)
