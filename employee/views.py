from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from reservations.models import Reservation, Restaurant
from guest.models import Guest
from reservations.forms import ReservationForm
from reservations.reservation import make_reservation

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def employee(request):
    context = {
        'title': 'Ansatt'
    }
    return render(request, 'employeepage.html', context)


@login_required
def walkin(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'], form.cleaned_data['number_of_people'], 1)

            if success:
                return render(request, 'success.html')
            else:
                return render(request, 'not_success.html')

    else:
        form = ReservationForm()
        return render(request, 'newwalkin.html', {'form': form})