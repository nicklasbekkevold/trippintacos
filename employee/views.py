from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation, Restaurant
from guest.models import Guest

from employee.forms import DateForm
from reservations.forms import ReservationForm, WalkinForm
from reservations.views import booking
from reservations.reservation import make_reservation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


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
            booking(request)
            '''
            form = ReservationForm(request.POST)
            print(form.first_name)
            if form.is_valid():
                booking(request)

            else:
                print("-----------------------Form not valid----------------------")
'''
        elif request.POST.get('walkin') == 'walkin':
            walkin(request)
            '''form = WalkinForm(request.POST)
            if not form.is_valid():
                walkin(request)
            else:
                print("---------------WalkinForm not Valid--------------")
'''
        return render(request, self.template_name, self.context)


@login_required
def walkin(request):
    if request.method == 'POST':
        print("HEI")
        form = WalkinForm(request.POST)
        if form.is_valid():
            print("halla")
            first_name = form.cleaned_data['first_name'].lower()
            guest = Guest.objects.create(first_name=first_name, reminder=0)

            success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                       form.cleaned_data['number_of_people'], 1)
            if success:
                return render(request, 'success.html')
            else:
                return render(request, 'not_success.html')

    else:
        form = WalkinForm()
        return render(request, 'employeepage.html', {'form': form})
