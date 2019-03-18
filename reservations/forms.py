from django import forms
from reservations.models import NewReservation, Reservation, Restaurant, Table
from guest.models import Guest
from bootstrap_datepicker_plus import *

class DynamicReservationForm(forms.ModelForm):

    class Meta:
        model = NewReservation
        fields = ('number_of_people', 'start_date', 'start_time', 'end_time', 'reminder')
        AVAILABLE_TIMES = [("", "---------")]
        widgets = {
            'start_date': DatePickerInput(
                attrs={
                    'id': 'datepicker',
                    'type': 'date',
                },
                options={
                    'calendarWeeks': True,
                }
            ),
            'start_time': forms.Select(
                attrs={
                    'id': 'timepicker',
                },
                choices=AVAILABLE_TIMES
            ),
            'reminder': forms.CheckboxInput(),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

class GuestReservationForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ('email', 'first_name', 'last_name')



class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(required=True)
    reminder = forms.BooleanField(required=False)
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
            options={
                'calendarWeeks': True,
                'sideBySide': True,
                'enabledHours': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                'stepping': 30,
            }
        )
    )
    start_time = forms.TimeField(
        widget=TimePickerInput(
            options={
                'enabledHours': [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                'stepping': 30,
            }
        )
    )
    duration = forms.TimeField(
        widget=TimePickerInput(
            options={
                'enabledHours': [0, 1, 2, 3, 4],
                'stepping': 30,
            }
        )
    )


class WalkinForm(forms.Form):

    first_name = forms.CharField(max_length=40, required=True, initial="Walk in")
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


class CancelForm(forms.Form):
    id = forms.CharField()
    email = forms.CharField()

    class Meta:
        fields = ('id', 'email')

