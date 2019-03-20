from django import forms


class DeleteMeForm(forms.Form):
    email = forms.EmailField(required=True, label='Epost')
    last_name = forms.CharField(required=True, label='Etternavn')

