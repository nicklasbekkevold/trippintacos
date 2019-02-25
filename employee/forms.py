from django import forms
from bootstrap_datepicker_plus import *

class DateForm(forms.Form):
    current_date = forms.DateField(
        widget=DatePickerInput(format='%A %m-%Y') #TODO fix formatting here by: format=' ... '
    )