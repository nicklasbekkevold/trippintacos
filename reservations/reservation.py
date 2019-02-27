from datetime import timedelta
from .models import Reservation, Table
from datetime import datetime
from guest.models import *


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


def make_reservation(restaurant, guest, reservation_date_time, number_of_people, walkin, minutes_slot=120):
    # funksjon som bruker get_next_available_table for å reservere et ledig bord på et ledig tidspunkt
    # print("NUMBER OF PEOPLE:", number_of_people)
    table = get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot)
    print("TABLE:", table)
    if table:
        delta = timedelta(seconds=60 * minutes_slot)
        reservation = Reservation(guest=guest, number_of_people=number_of_people, start_date_time=reservation_date_time,
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
