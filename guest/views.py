from django.shortcuts import render
from reservations.forms import DynamicReservationForm, GuestReservationForm
from reservations.models import Guest
from employee.helpers import send_confirmation
from reservations.reservation import make_reservation
from reservations.models import Reservation, Restaurant, Table


def guest(request):

    if request.method == 'POST':
        guestForm = GuestReservationForm(request.POST)
        reservationForm = DynamicReservationForm(request.POST)

        if guestForm.is_valid():
            email = guestForm.cleaned_data['email'].lower()
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each.email.lower())

            if email not in email_liste:
                guest = Guest(
                    email=email, 
                    first_name=guestForm.cleaned_data['first_name'], 
                    last_name=guestForm.cleaned_data['last_name'])
                # guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
                guest.save()
            else:
                guest = Guest.objects.all().get(email=email)
        if reservationForm.is_valid():
            success = make_reservation(
                Restaurant.objects.first(), 
                guest, 
                reservationForm.cleaned_data['start_date_time'], 
                reservationForm.cleaned_data['number_of_people'], 
                0, 
                reminder=reservationForm.cleaned_data['reminder'])

            if success:
                send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
                return render(request, 'reservations/success.html') # TODO change this
            else:
                return render(request, 'reservations/not_success.html') # TODO change this
        else:
            pass # form is invalid
    
    else:
        guestForm = GuestReservationForm()
        reservationForm = DynamicReservationForm()
        return render(request, 'guestpage.html', {'guestForm': guestForm, 'reservationForm': reservationForm})

def load_available_times(request):
    start_date = request.GET.get('start_date')
    available_times = [tuple([x,x]) for x in range(12, 18)]
    return render(request, 'guest/available_times_dropdown_list_options.html', {'available_times': available_times})
