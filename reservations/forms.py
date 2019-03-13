from django import forms
from .models import *
from bootstrap_datepicker_plus import *
from django.utils.safestring import mark_safe


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True,label='Fornavn')
    last_name = forms.CharField(max_length=40, required=False, label='Etternavn')
    email = forms.EmailField(required=True, label='E-mail')
    reminder = forms.BooleanField(required=False,label = 'Påminnelse på E-mail')
    number_of_people = forms.IntegerField(label= 'Antall gjester')
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
        ), label = 'Starttid for reservasjon'
    )
    end_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(

        ), label = 'Sluttid for reservasjon'
    )
    i_have_read_and_agree_checkbox = forms.BooleanField(label=mark_safe('Jeg har lest og forstått <a href=termsandconditions/ target="_blank"> Brukervilkår og Personvernpolicy</a>'),required=True)


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
    id = forms.CharField(label= 'Reservasjons-ID (mottatt på e-mail)')
    email = forms.CharField(label= 'E-mail')

    class Meta:
        fields = ('id', 'email')

