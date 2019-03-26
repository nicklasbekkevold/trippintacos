from datetime import timedelta
from .models import Reservation, Table
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
from guest.models import *
from django.db import models as djangomodels
from employee import helpers



def get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot=120):
    # skal returnere det første tilgjengelige bordet på en restaurant, for et gitt antall folk på et gitt tidspunkt.
    delta = timedelta(seconds=60 * minutes_slot)
    lower_bound_time = reservation_date_time
    upper_bound_time = reservation_date_time + delta

    tables_booked_ids = []

    # ekskluder allerede bookede bord som inneholder den initielle booking_date_time

    tables_booked = Reservation.objects.filter(table__restaurant=restaurant,
                                               start_date_time__lt=lower_bound_time,
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

    tables = Table.objects.filter(
        restaurant=restaurant,
        restaurant__opening_time__lte=str(reservation_date_time.hour) + ":" + str(reservation_date_time.minute),
        restaurant__closing_time__gte=str((reservation_date_time + timedelta(hours=temp_time_hardcode)).hour) + ":" +
        str((reservation_date_time + timedelta(hours=temp_time_hardcode)).minute),
        number_of_seats__gte=number_of_people).exclude(id__in=tables_booked_ids).order_by('number_of_seats')
    if tables.count() == 0:
        return None
    else:
        return tables[0]


def make_reservation(restaurant, guest, reservation_date_time, number_of_people, walkin, reminder, minutes_slot=120):
    # funksjon som bruker get_next_available_table for å reservere et ledig bord på et ledig tidspunkt
    # print("NUMBER OF PEOPLE:", number_of_people)
    table = get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot)
    print("TABLE:", table)
    if table:
        delta = timedelta(seconds=60 * minutes_slot)
        reservation = Reservation(guest=guest, reminder=reminder, number_of_people=number_of_people, start_date_time=reservation_date_time,
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
    cap = [[], [0]*12, [0]*12]
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


def get_average_capacity(dayofweek: int): # 0 is monday, 6 is sunday
    cap, res_start = get_total_on_weekday(dayofweek)
    week_difference = (datetime.today().date() - res_start).days // 7
    for i in range(12):
        cap[1][i] = cap[1][i] / week_difference
        cap[2][i] = cap[2][i] / week_difference
    return cap

def matplotfuckeroo(capacity_matrix, dayofweek):
    res_count = capacity_matrix[1]
    guest_count = capacity_matrix[2]
    ind = np.arange(len(res_count))
    width = 0.15

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, res_count, width, color='SkyBlue', label='Reservations')
    rects2 = ax.bar(ind + width/2, guest_count, width, color='IndianRed', label='Guests')

    ax.set_ylabel('Count')
    ax.set_xticklabels('timeOfDay')
    ax.set_title('Count of customers and guests on day' + str(dayofweek))
    ax.set_xticks(ind)
    ax.set_xticklabels(('12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'))
    ax.legend()

    autolabel(ax, rects1, "left")
    autolabel(ax, rects2, "right")

    plt.show()

def autolabel(ax, rects, xpos='center',):
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
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(int(round(height))), ha=ha[xpos], va='bottom')
                

def get_available_times(numberOfPersons:int, dateOfReservation:djangomodels.DateField):
    """
    :param numberOfPersons: Number of people in pending reservation
    :param date: date of proposed reservation
    :return: list of available times for reservation at date and with numberOfPeople on form (datetime,
    """
    # convert dateOfReservation to datetime
    _day = dateOfReservation.day
    _month = dateOfReservation.month
    _year = dateOfReservation.year

    d_start = datetime(_year, _month, _day, 12, 0, 0).replace(tzinfo=None)
    d_end = datetime(_year, _month, _day, 23, 59, 59).replace(tzinfo=None)


    # filter by date to get all reservations on date equal to dateOfReservation
    print("Reservations: ", Reservation.objects.all())
    '''
    QS_reservations_at_date = Reservation.objects.filter(start_date_time__year=_year) #, start_date_time__month=_month, start_date_time__year=_year)
    QS_reservations_at_date = QS_reservations_at_date.filter(start_date_time__month=_month)
    QS_reservations_at_date = QS_reservations_at_date.filter(start_date_time__day=_day)
    '''
    QS_reservations_at_date = Reservation.objects.filter(start_date_time__gte=d_start, end_date_time__lte=d_end)
    # use for loop to iterate through times and check for collision for it and two hours forward
    # Check for collisions and too early vs too late
    # if a time is available the tuple (time, something) will be added to the returned-list
    available_times_list = []
    tables = Table.objects.filter(number_of_seats__gte=numberOfPersons)
    datetime_time = datetime(_year, _month, _day, 11)
    find = False
    coll = False
    while datetime_time.replace(tzinfo=None) <= datetime(_year, _month, _day, 22).replace(tzinfo=None):
        for _table in tables:
            QS_reservations_at_date_at_table = QS_reservations_at_date.filter(table=_table.id)
            for reservation in QS_reservations_at_date_at_table:
                if helpers.checkForCollision(datetime_time, datetime_time + timedelta(hours=2), reservation):
                    coll = True
                    break  # if there is a collision, we break and go on to a new table
            if not coll:
                available_times_list.append((datetime_time + timedelta(hours=1), datetime_time.hour + 1 + datetime_time.minute/60))  # else we append the available list with the tuple of its time and ___?___
                break
        datetime_time = datetime_time + timedelta(minutes=30)
    print(available_times_list)
    return available_times_list

