from django import forms
from bootstrap_datepicker_plus import *

class DateForm(forms.Form):
    current_date = forms.DateField(
        widget=DatePickerInput(format='%d-%m-%Y') #TODO fix formatting here by: format=' ... '
    )