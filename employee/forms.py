from django import forms
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput



class DateForm(forms.Form):
    reservation_date = forms.DateField(
        label="",
        widget=DatePickerInput(options={
            "format": "dddd DD. MMMM YYYY",  # moment date-time format
            "calendarWeeks": True,
            "showClose": False,
            "showClear": False,
            "showTodayButton": False,
        })
    )


class EditReservationFrom(forms.Form):
    reservation_id = forms.IntegerField()
    new_start = forms.DateTimeField(widget=DateTimePickerInput(

    ))
    new_end = forms.DateTimeField(
        widget=DateTimePickerInput(

        ),
        required=False
    )
    '''
    class Meta:
        fields = ('reservation_id', 'email', 'new_start')
    '''


class statisticInputForm(forms.Form):
    liste = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    day = forms.ChoiceField(required=False,choices=[(x, x) for x in liste],label= "Velg dag:")


class EditTableForm(forms.Form):
    id = forms.IntegerField(widget=forms.NumberInput(attrs={
        'readonly': True,
    }))
    number_of_people = forms.IntegerField()

