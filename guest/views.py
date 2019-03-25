from django.shortcuts import render
from django.contrib import messages
from reservations.forms import ReservationForm
from guest.models import Guest
from employee.helpers import send_confirmation, deleteGuest
from reservations.forms import ReservationForm, GuestReservationForm
from reservations.models import Guest
from datetime import datetime, time, date
from employee.helpers import send_confirmation
from reservations.reservation import make_reservation
from reservations.models import Reservation, Restaurant, Table
from guest.forms import DeleteMeForm
from django.core.exceptions import ObjectDoesNotExist


def guest_page(request):

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)

        print(reservation_form.errors)
        if reservation_form.is_valid():
            email = reservation_form.cleaned_data['email'].lower()
            email_liste = []
            for guestobj in Guest.objects.all():
                if guestobj.email is not None:
                    email_liste.append(guestobj.email.lower())

            if email not in email_liste:
                guest = Guest(
                    email=email,
                    first_name=reservation_form.cleaned_data['first_name'],
                    last_name=reservation_form.cleaned_data['last_name'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)

            if reservation_form.is_valid():
                start_date = reservation_form.cleaned_data['start_date']
                start_time = datetime.strptime(str(reservation_form.cleaned_data['start_time']), "%H:%M").time()
                start_date_time = datetime.combine(start_date, start_time)
                print(start_date_time)
                success = make_reservation(
                    Restaurant.objects.first(),
                    guest,
                    start_date_time,
                    reservation_form.cleaned_data['number_of_people'],
                    False,
                    reminder=reservation_form.cleaned_data['reminder'],
                    minutes_slot=120)

                if success:
                    send_confirmation(guest, Reservation.objects.all().get(id=success['reservation']))
                    messages.success(request, 'Reservasjonen din er registrert.')
                    reservation_form = ReservationForm()
                    return render(request, 'guestpage.html', {'form': reservation_form})
                else:
                    messages.error(request, 'Noe gikk galt. Venligst prøv igjen')
                    reservation_form = ReservationForm()
                    return render(request, 'guestpage.html', {'form': reservation_form})
        else:
            reservation_form = ReservationForm()
            return render(request, 'guestpage.html', {'form': reservation_form})
    
    else:
        messages.error(request, 'Det er noe galt med utfyllingen av feltene')
        reservation_form = ReservationForm()
        return render(request, 'guestpage.html', {'form': reservation_form})

def load_available_times(request):
    start_date = request.GET.get('start_date')
    number_of_people = request.GET.get('number_of_people')
    available_times = [tuple(["{}:00".format(x), "{}:00".format(x)]) for x in range(14, 18)]
    return render(request, 'guest/available_times_dropdown_list_options.html', {'available_times': available_times})


def deleteMe(request):
    if request.method == 'POST':
        delete_me_form = DeleteMeForm(request.POST)

        if delete_me_form.is_valid():
            try:
                guest = Guest.objects.all().get(email=delete_me_form.cleaned_data['email'].lower())
                try:
                    guest_with_last_name = Guest.objects.all().get(email=guest.email.lower(), last_name=delete_me_form.cleaned_data['last_name'])

                    if deleteGuest(guest_with_last_name):
                        return render(request, 'deleteMe.html', {'sucess': True, 'email': delete_me_form.cleaned_data['email'], 'last_name': delete_me_form.cleaned_data['last_name'], 'form': DeleteMeForm()})

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

        print("Email:", email)
        print("Last_name:", last_name)

        if last_name is not None and email is not None:
            try:
                deleteGuest(Guest.objects.all().get(last_name=last_name, email=email))
            except ObjectDoesNotExist:
                return render(request, 'deleteMe.html', {'error': True, 'form': DeleteMeForm()})
            return render(request, 'deleteMe.html', {'sucess': True, 'form': DeleteMeForm(), 'email': email})

        delete_me_form = DeleteMeForm()
        return render(request, 'deleteMe.html', {'form': delete_me_form})

