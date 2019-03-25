from django import forms
from reservations.models import NewReservation, Reservation, Restaurant, Table
from guest.models import Guest
#from bootstrap_datepicker_plus import *
from django.utils.safestring import mark_safe

#class DynamicReservationForm(forms.ModelForm):
#
#    class Meta:
#        model = NewReservation
#        fields = ('number_of_people', 'start_date', 'start_time', 'end_time', 'reminder')
#        AVAILABLE_TIMES = [("", "---------")]
#        widgets = {
#            'number_of_people': forms.NumberInput(
#                attrs={
#                    'id': 'numberpicker',
#                    'min': 1,
#                }
#            ),
#            'start_date': forms.DateInput(
#                attrs={
#                    'id': 'datepicker',
#                },
#                options={
#                    "format": "DD/MM/YYYY",
#                    "locale": "nb",
#                    'calendarWeeks': True,
#                }
#            ),
#            'start_time': forms.Select(
#                attrs={
#                    'id': 'timepicker',
#                },
#                choices=AVAILABLE_TIMES
#            ),
#            'reminder': forms.CheckboxInput(
#
#            ),
#        }
#        
#        def __init__(self, *args, **kwargs):
#            super().__init__(*args, **kwargs)
#

class GuestReservationForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ('email', 'first_name', 'last_name')


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True, label='Fornavn')
    last_name = forms.CharField(max_length=40, required=False, label='Etternavn')
    email = forms.EmailField(required=True, label='E-post')
    reminder = forms.BooleanField(required=False, label='Påminnelse på e-post')
    number_of_people = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'id': 'numberpicker',
                'min': 1
            }
        ),
        label='Antall gjester'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'id': 'datepicker',
                'type': 'date'
            },
            format=['%d/%m/%Y'],
        )
    )
    start_time = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id': 'timepicker'
            },
        ),
        choices=[tuple(["{}:00".format(x), "{}:00".format(x)]) for x in range(12, 24)],
        label='Starttid for reservasjon'
    )
    i_have_read_and_agree_checkbox = forms.BooleanField(
        required=True,
        label=mark_safe('Jeg har lest og forstått <a href=termsandconditions/ target="_blank"> Brukervilkår og Personvernpolicy</a>'))


class WalkinForm(forms.Form):

    first_name = forms.CharField(max_length=40, required=True, initial="Walk in")
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=forms.DateInput(
        )
    )
    end_date_time = forms.DateTimeField(
        widget=forms.DateInput(
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
    id = forms.CharField(label='Reservasjons-ID (mottatt på e-mail)')
    email = forms.CharField(label='E-mail')

    class Meta:
        fields = ('id', 'email')

