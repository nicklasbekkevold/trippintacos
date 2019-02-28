from django.shortcuts import render
from reservations.forms import ReservationForm
from .models import Guest
from employee.helpers import send_confirmation
from reservations.reservation import make_reservation
from reservations.models import Reservation, Restaurant, Table


def guest(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(email=email, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                # guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                       form.cleaned_data['number_of_people'], 0, reminder=form.cleaned_data['reminder'])
            print("SUCCESS: ", success)
            if success:
                send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
                return render(request, 'reservations/success.html')
            else:
                return render(request, 'reservations/not_success.html')
        else:
            print("HÆÆÆÆÆÆÆÆÆÆÆÆÆÆ")
    else:
        form = ReservationForm()
        return render(request, 'guestpage.html', {'form': form})