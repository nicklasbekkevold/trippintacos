from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation, Restaurant
from guest.models import Guest

from employee.forms import DateForm
from reservations.forms import ReservationForm, WalkinForm
from reservations.reservation import make_reservation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from employee.helpers import send_confirmation


# Create your views here.

@method_decorator(login_required, name='get')
class Employee(TemplateView):
    template_name = 'employeepage.html'
    context = {
        'title': 'Ansatt',
        'form': DateForm(),
        'reservationForm': ReservationForm(),
        'walkinForm': WalkinForm(),
    }

    @method_decorator(login_required)
    def get(self, request):

        return render(request, self.template_name, self.context)

    def post(self, request):

        if request.POST.get('booking') == 'booking':
            if booking(request):
                return render(request, 'reservations/success.html')
            return render(request, 'reservations/not_success.html')
            '''
            form = ReservationForm(request.POST)
            print(form.first_name)
            if form.is_valid():
                booking(request)

            else:
                print("-----------------------Form not valid----------------------")
'''
        elif request.POST.get('walkin') == 'walkin':
            if walkin(request):
                return render(request, 'reservations/success.html')
            return render(request, 'reservations/not_success.html')
            '''form = WalkinForm(request.POST)
            if not form.is_valid():
                walkin(request)
            else:
                print("---------------WalkinForm not Valid--------------")
'''
        # return render(request, self.template_name, self.context)


@login_required
def walkin(request):
    print("HEI")
    form = WalkinForm(request.POST)
    if form.is_valid():
        print("halla")
        first_name = form.cleaned_data['first_name'].lower()
        guest = Guest.objects.create(first_name=first_name, reminder=0)

        success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                   form.cleaned_data['number_of_people'], 1)
        if success:
            return True
        else:
            return False


def booking(request):
    form = ReservationForm(request.POST)
    print('bookingHIE')
    if form.is_valid():
        print('formvalid')
        email = form.cleaned_data['email'].lower()
        email_liste = []
        for each in Guest.objects.all():
            email_liste.append(each.email.lower())

        if email not in email_liste:
            guest = Guest(email=email, reminder=form.cleaned_data['reminder'])
            #guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
            guest.save()
        else:
            guest = Guest.objects.all().get(email=email)
        success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'], form.cleaned_data['number_of_people'], 0)
        print("SUCCESS: ", success)
        if success:
            send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
            return True
        else:
            return False
