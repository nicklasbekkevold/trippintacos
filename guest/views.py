from django.shortcuts import render
from django.shortcuts import redirect
from guest.models import *
from reservations.models import *
from reservations.forms import ReservationForm
from reservations.reservation import make_reservation
from employee.helpers import send_confirmation


# Create your views here.


def guest(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(email=email, reminder=form.cleaned_data['reminder'])
                # guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'], form.cleaned_data['number_of_people'], 0)
            print("SUCCESS: ", success)
            if success:
                send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
                return render(request, 'success.html')
            else:
                return render(request, 'not_success.html')

    else:
        form = ReservationForm()
        return render(request, 'guestpage.html', {'form': form})
