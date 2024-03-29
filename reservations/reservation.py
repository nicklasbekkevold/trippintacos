from datetime import timedelta
from reservations.models import Reservation, Table
from datetime import datetime
from matplotlib import pyplot as plt
import mpld3
import numpy as np
from guest.models import *
from django.utils import timezone
import cgi
from django.db import models as djangomodels
from employee import helpers
import pytz
import math

from io import *
import os
from io import BytesIO

os.environ['DJANGO_SETTINGS_MODULE'] = 'trippinTacos.settings'

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot=120):
    # skal returnere det første tilgjengelige bordet på en restaurant, for et gitt antall folk på et gitt tidspunkt.
    delta = timedelta(seconds=60 * minutes_slot)
    lower_bound_time = reservation_date_time
    upper_bound_time = reservation_date_time + delta

    tables_booked_ids = []

    tables_booked = Reservation.objects.filter(start_date_time=lower_bound_time,
                                               end_date_time=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # ekskluder allerede bookede bord som inneholder den initielle booking_date_time

    tables_booked = Reservation.objects.filter(start_date_time__lt=lower_bound_time,
                                               end_date_time__gt=lower_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    # ekskluder allerede bookede bord som har den etterspurte sluttiden

    tables_booked = Reservation.objects.filter(start_date_time__lt=upper_bound_time,
                                               end_date_time__gt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp
    # ekskluderer bookede bord som er inni den aktuelle tidsperioden. er dette jalla?

    tables_booked = Reservation.objects.filter(start_date_time__gt=lower_bound_time,
                                               end_date_time__lt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp
    # ekskluderer bord som inkluderer den etterspurte booking-luken

    tables_booked = Reservation.objects.filter(start_date_time__lt=lower_bound_time,
                                               end_date_time__gt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp
    # lager liste med alle bord av nødvendig størrelse, tilgjengelige i restauranten
    # ekskluderer den forrige listen av utilgjengelige bord. Listen er rangert fra minst til størst tilgjengelig kapasitet,
    # og det ledige bordet med minst kapasitet returneres.
    temp_time_hardcode = (minutes_slot / float(60))

    tables = Table.objects.filter(number_of_seats__gte=number_of_people).exclude(id__in=tables_booked_ids).order_by('number_of_seats')

    if tables.count() == 0:
        return None
    else:
        return tables[0]


def make_reservation(restaurant, guest, reservation_date_time, number_of_people, walkin, reminder, minutes_slot=120):
    # funksjon som bruker get_next_available_table for å reservere et ledig bord på et ledig tidspunkt
    # print("NUMBER OF PEOPLE:", number_of_people)
    # reservation_date_time = pytz.utc.localize(reservation_date_time)
    table = get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot)

    print("TABLE:", table)
    if table:
        delta = timedelta(seconds=60 * minutes_slot)
        reservation = Reservation(guest=guest, reminder=reminder, number_of_people=number_of_people,
                                  start_date_time=reservation_date_time,
                                  end_date_time=reservation_date_time + delta, created_date=datetime.now(), table=table,
                                  walkin=walkin)
        reservation.save()
        return {'reservation': reservation.id, 'table': table.id}
    else:
        return None
    # kjernefunksjonaliteten skal nå være fullstendig for make_reservation.


def count_reservations():
    return Reservation.objects.count()


def count_unique_guests():
    return Guest.objects.count()


def get_total_on_weekday(dayofweek: int):
    cap = [[], [0] * 12, [0] * 12]
    for i in range(12, 24):
        cap[0].append(i)
    resStart = datetime.today().date()
    for res in Reservation.objects.all():
        if res.start_date_time.date() < datetime.today().date():
            if res.start_date_time.date() < resStart:
                resStart = res.start_date_time.date()
            if res.start_date_time.weekday() == dayofweek:
                start_hour = res.start_date_time.hour
                end_hour = res.end_date_time.hour
                cap[1][start_hour - 12] += 1
                cap[2][start_hour - 12] += res.number_of_people
                start_hour += 1
                while start_hour <= end_hour:
                    cap[1][start_hour - 12] += 1
                    cap[2][start_hour - 12] += res.number_of_people
                    start_hour += 1
    return cap, resStart


def get_average_capacity(dayofweek: int):  # 0 is monday, 6 is sunday
    cap, res_start = get_total_on_weekday(dayofweek)
    week_difference = ((datetime.today().date() - res_start).days // 7) + 1
    for i in range(12):
        cap[1][i] = math.ceil(cap[1][i] / week_difference)
        cap[2][i] = math.ceil(cap[2][i] / week_difference)
    return cap


DAGER = {
    0:'mandager',
    1:'tirsdager',
    2:'onsdager',
    3:'torsdager',
    4:'fredager',
    5:'lørdager',
    6:'søndager',
}

def matplotfuckeroo(capacity_matrix, dayofweek):
    res_count = capacity_matrix[1]
    guest_count = capacity_matrix[2]
    ind = np.arange(len(res_count))
    width = 0.15

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width / 2, res_count, width, color='SkyBlue', label='Reservasjoner')
    rects2 = ax.bar(ind + width / 2, guest_count, width, color='IndianRed', label='Gjester')

    ax.set_ylabel('Antall')
    #ax.set_xticklabels('timeOfDay')
    ax.set_xlabel('Klokkeslett')
    ax.set_title('Antall besøkende på ' + DAGER[dayofweek])
    ax.set_xticks(ind)
    ax.set_xticklabels(('12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))
    ax.legend()

    autolabel(ax, rects1, "left")
    autolabel(ax, rects2, "right")




    return mpld3.fig_to_html(fig)


'''
    format = "png"
    sio = StringIO()
    plt.savefig(sio, format=format)
    print("Content-Type: image/%s\n" % format)

    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)  # Needed this on windows, IIS
    sys.stdout.write(sio.getvalue())

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    '''




def autolabel(ax, rects, xpos='center', ):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(int(round(height))), ha=ha[xpos], va='bottom')
                

# def get_available_times(numberOfPersons:int, dateOfReservation:str):
#     """
#     :param numberOfPersons: Number of people in pending reservation
#     :param date: date of proposed reservation
#     :return: list of available times for reservation at date and with numberOfPeople on form (datetime,
#     """
#
#     # convert dateOfReservation to datetime
#     date_list = dateOfReservation.split("-")
#     _day = int(date_list[2]) # dateOfReservation.day
#     _month = int(date_list[1]) # dateOfReservation.month
#     _year = int(date_list[0]) # dateOfReservation.year
#
#     d_start = datetime(_year, _month, _day, 12, 0, 0).replace(tzinfo=None)
#     d_end = datetime(_year, _month, _day, 23, 59, 59).replace(tzinfo=None)
#
#     # filter by date to get all reservations on date equal to dateOfReservation
#     # print("Reservations: ", Reservation.objects.all())
#     '''
#     QS_reservations_at_date = Reservation.objects.filter(start_date_time__year=_year) #, start_date_time__month=_month, start_date_time__year=_year)
#     QS_reservations_at_date = QS_reservations_at_date.filter(start_date_time__month=_month)
#     QS_reservations_at_date = QS_reservations_at_date.filter(start_date_time__day=_day)
#     '''
#     QS_reservations_at_date = Reservation.objects.filter(start_date_time__gte=d_start, end_date_time__lte=d_end)
#     print("RESERVATIONS THIS DATE: ", QS_reservations_at_date)
#     # use for loop to iterate through times and check for collision for it and two hours forward
#     # Check for collisions and too early vs too late
#     # if a time is available the tuple (time, something) will be added to the returned-list
#     available_times_list = set()
#     tables = Table.objects.filter(number_of_seats__gte=numberOfPersons)
#     print("TABLES: ", tables)
#     datetime_time = datetime(_year, _month, _day, 11)
#     find = False
#     coll = False
#     while datetime_time <= datetime(_year, _month, _day, 22):
#         # coll = False
#         for _table in tables:
#             QS_reservations_at_date_at_table = QS_reservations_at_date.filter(table_id=_table.id)
#             for reservation in QS_reservations_at_date_at_table:
#                 if not helpers.checkForCollision(datetime_time, datetime_time + timedelta(hours=2), reservation):
#                     print("Time:", datetime_time)
#                     if str(datetime_time.minute) == '30':
#                         datetimeTemp = str((datetime_time + timedelta(hours=1)).hour) + ":30"
#                     else:
#                         datetimeTemp = str((datetime_time + timedelta(hours=1)).hour) + ":00"
#
#                     available_times_list.add((datetimeTemp, datetimeTemp))
#
#             '''
#             if not coll:
#                 print("Coll: ", datetime_time)
#                 coll = True
#                 break  # if there is a collision, we break and go on to a new table
#             '''
#         datetime_time = datetime_time + timedelta(minutes=30)
#     return sorted(list(available_times_list), key=lambda x: x[0])

# print(get_available_times(4, '2019-03-27'))


def get_available_times(numberOfPeople:int, date:str):
    date_list = date.split("-")

    day = int(date_list[2])  # dateOfReservation.day
    month = int(date_list[1])  # dateOfReservation.month
    year = int(date_list[0])  # dateOfReservation.year

    times_set_hardcode = {
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('15:30', '15:30'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('17:30', '17:30'),
        ('18:00', '18:00'),
        ('18:30', '18:30'),
        ('19:00', '19:00'),
        ('20:00', '20:00'),
        ('20:30', '20:30'),
        ('21:00', '21:00'),
        ('21:30', '21:30'),
        ('22:00', '22:00')
    }

    d_start = datetime(year, month, day, 12, 0, 0).replace(tzinfo=None)
    d_end = datetime(year, month, day, 23, 59, 59).replace(tzinfo=None)

    QS_reservations_at_date = Reservation.objects.filter(start_date_time__gte=d_start, end_date_time__lte=d_end)
    tables = Table.objects.filter(number_of_seats__gte=numberOfPeople)

    if len(tables) == 0:
        return list()

    times = {}
    for table in tables:
        reservations = QS_reservations_at_date.filter(table__id=table.id)
        for res in reservations:
            if res.start_date_time in times:
                times[res.start_date_time] += 1
            else:
                times[res.start_date_time] = 1

    booked_times = {}
    for time in times:
        for i in range(times[time]):
            datetime_time = datetime(time.year, time.month, time.day, time.hour) - timedelta(hours=1, minutes=30)

            while datetime_time <= (time + timedelta(hours=1, minutes=30)).replace(tzinfo=None):
                if datetime_time >= datetime_time + timedelta(hours=2):
                    break

                if str(datetime_time.minute) == '30':
                    datetimeTemp = str((datetime_time + timedelta(hours=1)).hour) + ":30"
                else:
                    datetimeTemp = str((datetime_time + timedelta(hours=1)).hour) + ":00"

                print("Added: ", datetimeTemp)
                if (datetimeTemp, datetimeTemp) in booked_times:
                    booked_times[(datetimeTemp, datetimeTemp)] += 1
                else:
                    booked_times[(datetimeTemp, datetimeTemp)] = 1
                datetime_time += timedelta(minutes=30)

    booked_times_set = set()
    for time in booked_times:
        if booked_times[time] >= len(tables):
            booked_times_set.add(time)

    return sorted(list(times_set_hardcode-booked_times_set), key=lambda x: x[0])
