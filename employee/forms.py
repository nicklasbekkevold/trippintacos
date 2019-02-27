from django import forms
from bootstrap_datepicker_plus import DatePickerInput

class DateForm(forms.Form):
    _ = forms.DateField(
        widget=DatePickerInput(
            options={
                    "format": "dddd DD. MMMM YYYY", # moment date-time format
                    "calendarWeeks": True,
                    "showClose": False,
                    "showClear": False,
                    "showTodayButton": False,
                }

        )
    )
