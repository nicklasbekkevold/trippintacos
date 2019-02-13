from django import forms
from .models import *


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('guest', 'start_date_time')
