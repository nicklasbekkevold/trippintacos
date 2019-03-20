from django.shortcuts import render
from reservations.forms import ReservationForm
from .models import Guest
from employee.helpers import send_confirmation, deleteGuest
from reservations.reservation import make_reservation
from reservations.models import Reservation, Restaurant, Table
from guest.forms import DeleteMeForm
from django.core.exceptions import ObjectDoesNotExist


def guest(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                if each.email is not None:
                    email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(email=email, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                       form.cleaned_data['number_of_people'], 0, reminder=form.cleaned_data['reminder'])
            if success:
                send_confirmation(guest, Reservation.objects.all().get(id=success['reservation']))
                return render(request, 'reservations/success.html')
            else:
                return render(request, 'reservations/not_success.html')
    else:
        form = ReservationForm()
        return render(request, 'guestpage.html', {'form': form})


def deleteMe(request):
    if request.method == 'POST':
        form = DeleteMeForm(request.POST)

        if form.is_valid():
            try:
                guest = Guest.objects.all().get(email=form.cleaned_data['email'].lower())
                try:
                    guest_with_last_name = Guest.objects.all().get(email=guest.email.lower(), last_name=form.cleaned_data['last_name'])

                    if deleteGuest(guest_with_last_name):
                        return render(request, 'deleteMe.html', {'sucess': True, 'email': form.cleaned_data['email'], 'last_name': form.cleaned_data['last_name'], 'form': DeleteMeForm()})

                except ObjectDoesNotExist:
                    return render(request, 'deleteMe.html', {'form': DeleteMeForm(), 'invalid_last_name': True})

            except ObjectDoesNotExist:
                return render(request, 'deleteMe.html', {'form': DeleteMeForm(), 'invalid_email': True})

            return render(request, 'deleteMe.html', {'unexpected': True})

    else:
        if request.GET.get('email') is not None and request.GET.get('last_name') is not None:
            try:
                guest = Guest.objects.all().get(email=request.GET.get('email').lower())
            except ObjectDoesNotExist:
                pass
        last_name = request.GET.get('last_name')
        email = request.GET.get('email')

        print("Email:",email)
        print("Last_name:",last_name)

        if last_name is not None and email is not None:
            try:
                deleteGuest(Guest.objects.all().get(last_name=last_name, email=email))
            except ObjectDoesNotExist:
                return render(request, 'deleteMe.html', {'error': True, 'form': DeleteMeForm()})
            return render(request, 'deleteMe.html', {'sucess': True, 'form': DeleteMeForm(), 'email': email})

        form = DeleteMeForm()
        return render(request, 'deleteMe.html', {'form': form})

