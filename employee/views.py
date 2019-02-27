from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
from reservations.models import Reservation, Restaurant, Table
from guest.models import Guest
from employee.forms import DateForm
from reservations.forms import ReservationForm
from reservations.reservation import make_reservation
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

RESERVATIONS = [
    {
        'table': 'Bord 1',
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

@login_required
def employee(request):
    context = {
        'title': 'Ansatt',
        'form': DateForm(),
        'reservations': RESERVATIONS,
        'time_range': range(12, 25)
    }
    return render(request, 'employeepage.html', context)

@method_decorator(login_required, name='get')
class Employee(TemplateView):
    template_name = 'employeepage.html'

    @method_decorator(login_required)
    def get(self, request):

        context = {
            'title': 'Ansatt',
            'form': DateForm(),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        if request.POST.get('showRes') == 'showRes':

            print(request.POST.get('_'))
            date = request.POST.get('_').split(' ')
            day = date[1][0:2]
            month = MONTHS[date[2]]
            year = date[-1]
            updated_request = request.POST.copy()
            updated_request.update({'_': year + "-" + month + "-" + day})
            form = DateForm(updated_request)
            if form.is_valid():
                print("---------------Form IS valid-----------------")
                showRes(request, form.cleaned_data['_'])

            else:
              print("-----------------------From not valid----------------------")

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
    '''
    reservations_this_date = Reservation.objects.filter(start_date_time__year=date.year,
                                                        start_date_time__day=date.day,
                                                        start_date_time__month=date.month,
                                                        )
    '''
    reservations_this_date = list()
    for res in Reservation.objects.all():
        if res.start_date_time.day == date.day and res.start_date_time.year == date.year and res.start_date_time.month == date.month:
            reservations_this_date.append(res)


    '''
    {
       'table': 'Bord 1',
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
   }    
    '''
    lst = list()
    for res in reservations_this_date:
        lst.append({
            'table': 'Bord ' + str(res.table_id),
            'number_of_seats': res.table.number_of_seats,
            'reservations': [
                
            ]
        })