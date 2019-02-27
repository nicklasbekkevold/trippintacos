from django import forms
from .models import *
from bootstrap_datepicker_plus import *
from employee.helpers import get_all_booked_dates_and_time

booked = get_all_booked_dates_and_time()


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(required=True)
    reminder = forms.BooleanField()
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            format='%d/%m/%Y, %H:%M',
            options={
                'disabledDates': booked
            }
        )
    )
    end_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            format='%d/%m/%Y, %H:%M'
        )
    )


class WalkinForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True, initial="Walk in")
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            format='%d/%m/%Y, %H:%M',
            options={
                'disabledDates': booked
            }
        )
    )
    end_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            format='%d/%m/%Y, %H:%M'
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
