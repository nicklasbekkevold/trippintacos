from django.shortcuts import render, redirect
from django.contrib.auth.decorators import  login_required
from reservations.models import Reservation, Restaurant, Table
from guest.models import Guest
from employee.forms import DateForm
from reservations.forms import ReservationForm
from reservations.reservation import make_reservation
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from datetime import datetime
# Create your views here.

from django.utils.decorators import method_decorator

RESERVATIONS = [
    {
        'table': 'Bord 1',
        'number_of_seats': 4,
        'reservations': [
            {

            },  
            {
                'name': 'Kari',
                'number_of_guests': 3,
                'duration': 4,
                'is_walk_in': False,
            },
            {

            },
            {
                'name': 'Lars',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': False,
            },
            {
                'name': 'Walk in',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': True,
            }
        ]
    },
    {
        'table': 'Bord 2',
        'number_of_seats': 4,
        'reservations': [
            {
                'name': 'Kari',
                'number_of_guests': 3,
                'duration': 4,
                'is_walk_in': False,
            },
            {
                'name': 'Lars',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': False,
            },
            {
                'name': 'Walk in',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': True,
            }
        ]
    },
    {
        'table': 'Bord 3',
        'number_of_seats': 4,
        'reservations': [
            {
                'name': 'Kari',
                'number_of_guests': 3,
                'duration': 4,
                'is_walk_in': False,
            },
            {
                'name': 'Lars',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': False,
            },
            {
                'name': 'Walk in',
                'number_of_guests': 4,
                'duration': 6,
                'is_walk_in': True,
            }
        ]
    },
]

MONTHS = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12',

}

@method_decorator(login_required, name='get')
class Employee(TemplateView):
    template_name = 'employeepage.html'

    @method_decorator(login_required)
    def get(self, request, date=datetime.now()):

        context = {
            'title': 'Ansatt',
            'form': DateForm(initial={'_': datetime(datetime.now().year, datetime.now().month, datetime.now().day)}),
            'reservations': RESERVATIONS,
            'time_range': range(12, 25)
        }
        
        if request.GET.get('showRes') == 'showRes':
            date = request.GET.get('_').split(' ')
            day = date[1][0:2]
            month = MONTHS[date[2]]
            year = date[-1]
            full_date = year + "-" + month + "-" + day
            print("FULL DATE: " + full_date)
            context['reservations'] = showRes(request, full_date)
            context['form'] = DateForm(initial={'_': request.GET.get('_')})
            print(context)
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, context)

    def post(self, request):
        return render(request, self.template_name)


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


def showRes(request, date):
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]

    reservations_this_date = list()
    for res in Reservation.objects.all():
        print(res.start_date_time.day, res.start_date_time.year, res.start_date_time.month)
        if res.start_date_time.day == int(day) and res.start_date_time.year == int(year) and res.start_date_time.month == int(month):
            reservations_this_date.append(res)

    lst = list()
    table_ids = list()
    for res in reservations_this_date:
        if res.table_id not in table_ids:
            lst.append({
                'table': 'Bord ' + str(res.table_id),
                'number_of_seats': res.table.number_of_seats,
                'reservations': reservations_this_date
            })
            table_ids.append(res.table_id)
    return lst
