from django import forms
from django.utils.safestring import mark_safe
from reservations.models import Restaurant, Table


class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=True, label='Fornavn')
    last_name = forms.CharField(max_length=40, required=False, label='Etternavn')
    email = forms.EmailField(required=True, label='E-post')
    reminder = forms.BooleanField(required=False, label='Jeg ønsker påminnelse på e-post')
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
        choices=[tuple(["{}:{}".format(hours, minuttes), "{}:{}".format(hours, minuttes)]) for hours in range(12, 23) for minuttes in ["00", "30"]][:-1],
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

