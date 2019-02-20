from datetime import timedelta
from .models import Reservation, Table
from datetime import datetime


def get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot = 120):

    #skal returnere det første tilgjengelige bordet på en restaurant, for et gitt antall folk på et gitt tidspunkt.
    delta = timedelta(seconds=60*minutes_slot)
    lower_bound_time = reservation_date_time
    upper_bound_time = reservation_date_time + delta

    tables_booked_ids = []

    #ekskluder allerede bookede bord som inneholder den initielle booking_date_time

    tables_booked = Reservation.objects.filter(table_restaurant =restaurant,reservation_date_time_start__lt=lower_bound_time, reservation_date_time_end__gt=lower_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    #ekskluder allerede bookede bord som har den etterspurte sluttiden

    tables_booked = Reservation.objects.filter(reservation_date_time_start_lt=upper_bound_time, reservation_date_time_end__gt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    #ekskluderer bookede bord som er inni den aktuelle tidsperioden. er dette jalla?

    tables_booked = Reservation.objects.filter(reservation_date_time_start__gt=lower_bound_time, reservation_date_time_end__lt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    #ekskluderer bord som inkluderer den etterspurte booking-luken

    tables_booked = Reservation.objects.filter(booking_date_time_start__lt=lower_bound_time,booking_date_time_end__gt=upper_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp

    #lager liste med alle bord av nødvendig størrelse, tilgjengelige i restauranten
    #ekskluderer den forrige listen av utilgjengelige bord. Listen er rangert fra minst til størst tilgjengelig kapasitet,
    #og det ledige bordet med minst kapasitet returneres.

    tables = Table.objects.filter(restaurant =restaurant, restaurant__opening_time_lte = reservation_date_time.hour, restaurant__closing_time__gte = reservation_date_time.hour + (minutes_slot / float(60)), size__gte=number_of_people).exclude(id__in= tables_booked_ids).order_by('size')

    if tables.count() == 0:
        return None
    else:
        return tables[0]


def make_reservation(restaurant, guest, reservation_date_time,number_of_people, minutes_slot = 120,):

    #funksjon som bruker get_next_available_table for å reservere et ledig bord på et ledig tidspunkt

    table = get_next_available_table(restaurant, reservation_date_time, minutes_slot)

    if table:
        delta = timedelta(seconds=60*minutes_slot)
        reservation = Reservation(guest = guest, number_of_people = number_of_people, start_date_time = reservation_date_time, end_date_time = reservation_date_time + delta, createdDate = datetime.now(), table = table)
        reservation.save()
        return {'reservation': reservation.id, 'table': table.id}
    else:
        return None
    #kjernefunksjonaliteten skal nå være fullstendig for make_reservation.




