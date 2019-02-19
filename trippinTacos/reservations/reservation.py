from datetime import timedelta
from .models import Reservation, Table
from guest.models import Guest
from datetime import datetime


def get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot = 120):

    #skal returnere det første tilgjengelige bordet på en restaurant, for et gitt antall folk på et gitt tidspunkt.
    delta = timedelta(seconds=60*minutes_slot)
    lower_bound_time = reservation_date_time
    upper_bound_time = reservation_date_time + delta

    tables_booked_ids = []

    #ekskluder allerede bookede bord

    tables_booked = Reservation.objects.filter(table_restaurant =restaurant,booking_date_time_start__lt=lower_bound_time, booking_date_time_end__gt=lower_bound_time).values('table')
    tables_booked_ids_temp = [x['table'] for x in tables_booked]
    tables_booked_ids = tables_booked_ids + tables_booked_ids_temp






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
    #kjernefunksjonaliteten skal være fullstendig for make_reservation.




