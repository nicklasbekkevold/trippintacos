from django.shortcuts import render
from .forms import ReservationForm
from django.shortcuts import redirect
from guest.models import *
from reservations.models import *
from reservations.reservation import make_reservation


# Create your views here.


def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            print("EMAIL LISTE:", email_liste, "EMAIL:", email)
            if email not in email_liste:
                guest = Guest(email=email, reminder=form.cleaned_data['reminder'])
                # guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
                print("GUEST: ", guest)
            else:
                guest = Guest.objects.all().get(email=email)
                print("GUEST: ", guest)
            # form.guest = guest
            print(make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'], form.cleaned_data['number_of_people']))

            # post = form.save()
            # post.save()
            return render(request, 'success.html')

    else:
        form = ReservationForm()
        return render(request, 'booking.html', {'form': form})


