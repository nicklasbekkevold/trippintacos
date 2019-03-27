from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservations.models import Reservation, Restaurant, Table
from reservations.models import Reservation, Restaurant
from guest.models import Guest
from employee.forms import DateForm, EditReservationFrom, statisticInputForm, EditTableForm
from reservations.forms import ReservationForm, WalkinForm
from reservations.reservation import make_reservation, get_available_times
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from datetime import datetime
from django.views.generic import TemplateView
from employee.helpers import send_confirmation, edit
from django.utils.decorators import method_decorator
from reservations.reservation import get_total_on_weekday, get_average_capacity, matplotfuckeroo, count_reservations, count_unique_guests

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
            'form': DateForm(initial={'reservation_date': datetime(datetime.now().year, datetime.now().month, datetime.now().day)}),
            'reservations': showRes(request, datetime.strftime(
                datetime(datetime.now().year, datetime.now().month, datetime.now().day), '%Y-%m-%d')),
            'time_range': range(12, 24),
            'reservationForm': ReservationForm(),
            'walkinForm': WalkinForm(),
        }

        if request.POST.get('showRes') == 'showRes':
            date = request.POST.get('reservation_date').split(' ')
            day = date[1][0:2]
            month = MONTHS[date[2]]
            year = date[-1]
            full_date = year + "-" + month + "-" + day
            context['reservations'] = showRes(request, full_date)
            context['form'] = DateForm(initial={'reservation_date': request.POST.get('reservation_date')})
            return render(request, self.template_name, context)
        elif request.POST.get('booking') == 'booking':
            if booking(request):
                messages.success(request, 'Reservasjonen ble registrert')
                return render(request, self.template_name, context)
            else:
                messages.success(request, 'Reservasjonen ble ikke registrert')
                return render(request, self.template_name, context)

        elif request.POST.get('walkin') == 'walkin':
            if walkin(request):
                messages.success(request, 'Walkin ble registrert')
                return render(request, self.template_name, context)
            return render(request, self.template_name, context)
        else:
            messages.warning(request, 'Div')
            return render(request, self.template_name, context)

    def get(self, request):
        context = {
            'title': 'Ansatt',
            'form': DateForm(initial={'reservation_date': datetime(datetime.now().year, datetime.now().month, datetime.now().day)}),
            'reservations': showRes(request, datetime.strftime(
                datetime(datetime.now().year, datetime.now().month, datetime.now().day), '%Y-%m-%d')),
            'time_range': range(12, 24),
            'reservationForm': ReservationForm(),
            'walkinForm': WalkinForm(),
        }

        return render(request, self.template_name, context)


@login_required
def walkin(request):
    form = WalkinForm(request.POST)
    if form.is_valid():
        guest = Guest(first_name=form.cleaned_data['first_name'],)
        guest.save()
        start_date = form.cleaned_data['start_date']
        start_time = datetime.strptime(str(form.cleaned_data['start_time']), "%H:%M").time()
        start_date_time = datetime.combine(start_date, start_time)
        success = make_reservation(Restaurant.objects.first(), 
            guest, 
            start_date_time,
            form.cleaned_data['number_of_people'], 
            1, 
            0)

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
            if each.email is not None:
                email_liste.append(each.email.lower())
        if email not in email_liste:
            guest = Guest(
                email=email,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'])
            guest.save()
        else:
            guest = Guest.objects.all().get(email=email)
        
        start_date = form.cleaned_data['start_date']
        start_time = datetime.strptime(str(form.cleaned_data['start_time']), "%H:%M").time()
        start_date_time = datetime.combine(start_date, start_time)
        success = make_reservation(
            Restaurant.objects.first(), 
            guest, 
            start_date_time,
            form.cleaned_data['number_of_people'], 
            0, 
            reminder=form.cleaned_data['reminder'])
        if success:
            send_confirmation(guest, Reservation.objects.all().get(id=success['reservation']))
            return True
        else:
            return False

    else:
        form = ReservationForm()
        return render(request, 'newwalkin.html', {'form': form})


def load_available_times(request):
    start_date = request.GET.get('start_date')
    number_of_people = int(request.GET.get('number_of_people'))
    available_times = get_available_times(number_of_people, start_date)
    return render(request, 'guest/available_times_dropdown_list_options.html', {'available_times': available_times})


def showRes(request, date):
    def compute_time_slots(res_this_table):
        time_slots = list()
        slot_number = 0
        while slot_number < 24:
            for reservation in res_this_table:
                start = reservation.start_date_time.time()
                end = reservation.end_date_time.time()
                index = 2 * (start.hour % 12) + start.minute // 30
                duration = ((end.hour - start.hour) * 60 + (end.minute - start.minute)) // 30
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
        if res.start_date_time.day == int(day) and res.start_date_time.year == int(
                year) and res.start_date_time.month == int(month):
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


@login_required
def editReservation(request):
    if request.method == 'POST':
        form = EditReservationFrom(request.POST)

        if form.is_valid():
            res = Reservation.objects.filter(id=int(form.cleaned_data['reservation_id']))[0]

            if form.cleaned_data['new_end'] is not None:
                if edit(res.id, form.cleaned_data['new_start'], form.cleaned_data['new_end']):
                    return render(request, 'reservations/success.html')
            else:
                if edit(res.id, form.cleaned_data['new_start']):
                    return render(request, 'reservations/success.html')
        return render(request, 'reservations/not_success.html')
    else:
        form = EditReservationFrom()

        return render(request, 'editreservation.html', {'form': form})


@login_required
def showStatistikk(request):
    if request.method == 'POST':
        form = statisticInputForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['day']

            input = dayToInt(input)

            html_code = matplotfuckeroo(get_average_capacity(input), input)

            return render(request, 'statistikk.html', {'code': html_code, 'form': form, 'tall': count_reservations(),'totguests': count_unique_guests()})

    form = statisticInputForm(request.POST)
    html_code = matplotfuckeroo(get_average_capacity(0), 0)
    return render(request, 'statistikk.html', {'form': form, 'code': html_code, 'tall': count_reservations(),'totguests': count_unique_guests()})





def dayToInt(day):
    liste = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]
    i = 0
    for each in liste:
        if each == day:
            return i
        i += 1

'''def allTimeVisits(request):
    pass
'''


''''
def cloud_gen(request):
   if request.method == 'POST':
       form = CharForm(request.POST)
       if form.is_valid():
           text = form.cleaned_data['post']
           phrases = ''
           stopWords = ''

           MyData= dict(countWords(text, phrases, stopWords, True))
           wc = WordCloud(scale=10, max_words=100).generate_from_frequencies(MyData)

           plt.figure(figsize=(32,18))
           plt.imshow(wc, interpolation="bilinear", aspect='auto')

           fig = plt.gcf()
           buf = io.BytesIO()
           fig.savefig(buf, format='png')
           buf.seek(0)
           string = base64.b64encode(buf.read())

           uri = 'data:image/png;base64,' + urllib.parse.quote(string)

           args = {'form':form, 'text':text, 'image':uri}
           return render(request, 'wordcloudgen/cloud_gen.html', args)
   else:
       form = CharForm()
       return render(request, 'wordcloudgen/cloud_gen.html', {'form':form})
'''

@login_required
def editTable(request):
    if request.method == 'POST':
        form = EditTableForm(request.POST)

        print(request.POST)
        if form.is_valid():
            table = Table.objects.all().get(id=int(form.cleaned_data['id']))
            table.number_of_seats = int(form.cleaned_data['number_of_people'])
            table.save()

            QS_tables = Table.objects.all()
            tables = list()

            for table in QS_tables:
                tables.append(table.id)

            return render(request, 'editTable.html',
                          {'success': True,
                           'form': EditTableForm(initial={'id': int(form.cleaned_data['id'])}),
                           'requested_id': int(form.cleaned_data['id']),
                           'table_ids': tables})
        return render(request, 'editTable.html', {'not_success': True})

    else:
        print(request.GET)
        if request.GET.get('id') is not None:
            requested_id = request.GET.get('id')
        else:
            requested_id = None

        QS_tables = Table.objects.all()
        tables = list()

        for table in QS_tables:
            tables.append(table.id)

        form = EditTableForm(initial={'id': requested_id})
        return render(request, 'editTable.html', {'table_ids': tables, 'requested_id': requested_id, 'form': form})
