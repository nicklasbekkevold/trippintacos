from django.shortcuts import render
from .forms import ReservationForm, CancelForm
from django.shortcuts import redirect
from guest.models import *
from reservations.models import *
from reservations.reservation import make_reservation
from employee.helpers import send_confirmation, send_cancellation


# Create your views here.


def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(email=email, first_name=form.cleaned_data['first_name'],
                              last_name=form.cleaned_data['last_name'])
                #guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                       form.cleaned_data['number_of_people'], 0, reminder=form.cleaned_data['reminder'])
            if success:
                send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
                return render(request, 'reservations/success.html')
            else:
                return render(request, 'not_success.html')

    else:
        form = ReservationForm()
        return render(request, 'booking.html', {'form': form})


def cancel(request):
    if request.method == 'POST':
        form = CancelForm(request.POST)
        if form.is_valid():
            res = Reservation.objects.all().get(id=int(form.cleaned_data['id']))
            if res.guest.email == form.cleaned_data['email']:
                res.delete()
                send_cancellation(form.cleaned_data['email'], int(form.cleaned_data['id']))
                return render(request, 'reservations/success.html')
        return render(request, 'reservations/not_success.html')
    else:
        form = CancelForm()
        return render(request, 'cancel.html', {'form': form})
