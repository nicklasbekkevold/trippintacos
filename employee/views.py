from django.shortcuts import render, redirect
from django.contrib.auth.decorators import  login_required
from reservations.models import Reservation, Restaurant, Table
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation, Restaurant
from guest.models import Guest
from employee.forms import DateForm
from reservations.forms import ReservationForm, WalkinForm
from reservations.reservation import make_reservation
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from datetime import datetime
from django.views.generic import TemplateView
from employee.helpers import send_confirmation
from django.utils.decorators import method_decorator
# Create your views here.

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
    def post(self, request, date=datetime.now()):

        context = {
            'title': 'Ansatt',
            'form': DateForm(initial={'_': datetime(datetime.now().year, datetime.now().month, datetime.now().day)}),
            'reservations': showRes(request, datetime.strftime(datetime(datetime.now().year, datetime.now().month, datetime.now().day), '%Y-%m-%d')),
            'time_range': range(12, 25),
            'reservationForm': ReservationForm(),
            'walkinForm': WalkinForm(),
        }
        
        if request.POST.get('showRes') == 'showRes':
            '''
            print(request.GET.get('_'))
            date = request.GET.get('_').split(' ')
            day = date[1][0:2]
            month = MONTHS[date[2]]
            year = date[-1]
            updated_request = request.GET.copy()
            updated_request.update({'_': year + "-" + month + "-" + day})
            form = DateForm(updated_request)
            if form.is_valid():
                # tables = showRes(request, form.cleaned_data['_'])
                showRes(request, form.cleaned_data['_'])
                # context['reservations'] = tables
                #print("ADDED")
                # return render(request, )
                return
            else:
              print("-----------------------From not valid----------------------")
        print("CONTEXT: ", context)
        return render(request, self.template_name, context)
            '''
            date = request.POST.get('_').split(' ')
            day = date[1][0:2]
            month = MONTHS[date[2]]
            year = date[-1]
            full_date = year + "-" + month + "-" + day
            # print("FULL DATE: " + full_date)
            context['reservations'] = showRes(request, full_date)
            context['form'] = DateForm(initial={'_': request.POST.get('_')})
            # print(context)
            return render(request, self.template_name, context)
        elif request.POST.get('booking') == 'booking':
            if booking(request):
                return render(request, 'reservations/success.html')
            return render(request, 'reservations/not_success.html')

        elif request.POST.get('walkin') == 'walkin':
            if walkin(request):
                return render(request, 'reservations/success.html')
            return render(request, 'reservations/not_success.html')
        else:
            return render(request, self.template_name, context)

    def get(self, request):
        context = {
            'title': 'Ansatt',
            'form': DateForm(initial={'_': datetime(datetime.now().year, datetime.now().month, datetime.now().day)}),
            'reservations': showRes(request, datetime.strftime(datetime(datetime.now().year, datetime.now().month, datetime.now().day), '%Y-%m-%d')),
            'time_range': range(12, 25),
            'reservationForm': ReservationForm(),
            'walkinForm': WalkinForm(),
        }

        return render(request, self.template_name, context)

@login_required
def walkin(request):
    form = WalkinForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data['first_name'].lower()
        guest = Guest(first_name=form.cleaned_data['first_name'])
        guest.save()

        success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                   form.cleaned_data['number_of_people'], 1, 0)
        if success:
            return True
        else:
            return False


def booking(request):
    form = ReservationForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email'].lower()
        email_liste = []
        for each in Guest.objects.all():
            email_liste.append(each.email.lower())
        if email not in email_liste:
            guest = Guest(email=email,
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'])
            #guest = Guest.objects.create(email=email, reminder=form.cleaned_data['reminder'])
            guest.save()
        else:
            guest = Guest.objects.all().get(email=email)
        success = make_reservation(Restaurant.objects.first(), guest, form.cleaned_data['start_date_time'],
                                   form.cleaned_data['number_of_people'], 0, reminder=form.cleaned_data['reminder'])
        if success:
            send_confirmation(guest.email, Reservation.objects.all().get(id=success['reservation']))
            return True
        else:
            return False

    else:
        form = ReservationForm()
        return render(request, 'newwalkin.html', {'form': form})


def showRes(request, date):

    def compute_time_slots(res_this_table):
        time_slots = list()
        slot_number = 0
        while slot_number < 26:
            for reservation in res_this_table:
                start = reservation.start_date_time.time()
                end = reservation.end_date_time.time()
                index = 2*(start.hour%12) + start.minute//30
                duration = ((end.hour - start.hour)*60 + (end.minute - start.minute)) // 30
                if index == slot_number:
                    time_slots.append({
                        'info': reservation,
                        'duration': duration,
                    })
                    slot_number += duration
                    break
            else:
                time_slots.append({
                    'info': '',
                    'duration': '',
                })
                slot_number += 1 
        return time_slots
        
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]

    reservations_this_date = list()
    for res in Reservation.objects.all():
        if res.start_date_time.day == int(day) and res.start_date_time.year == int(year) and res.start_date_time.month == int(month):
            reservations_this_date.append(res)

    table_list = list()
    tables = Table.objects.all()
    for table in tables:
        res_this_table = list()
        for res in reservations_this_date:
            if res.table == table:
                res_this_table.append(res)

        table_list.append({
            'table': 'Bord ' + str(table.id),
            'number_of_seats': table.number_of_seats,
            'reservations': compute_time_slots(res_this_table),
        })
    return table_list

