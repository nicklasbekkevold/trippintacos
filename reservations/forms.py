from django import forms
from .models import *
from bootstrap_datepicker_plus import *
from django.utils.safestring import mark_safe


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True)
    last_name = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(required=True)
    reminder = forms.BooleanField(required=False)
    number_of_people = forms.IntegerField()
    start_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(
        )
    )
    end_date_time = forms.DateTimeField(
        widget=DateTimePickerInput(

        )
    )
    i_have_read_and_agree_to_the_Terms_and_Conditions_and_Privacy_Policy = forms.BooleanField(label=mark_safe('I have read and agree to <a href="/termsandconditions/" target="_blank"> Terms of Use and Privacy Policy</a>'))


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

