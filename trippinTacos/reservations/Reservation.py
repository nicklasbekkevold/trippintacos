from datetime import timedelta
from .models import Reservation, Table, Guest

def get_next_available_table(restaurant, reservation_date_time, number_of_people, minutes_slot = 120):

def make_reservation(restaurant, guest, reservation_date_time,number_of_people, minutes_slot = 120,):

    #funksjon som bruker get_next_available_table for å reservere et ledig bord på et ledig tidspunkt

    table = get_next_available_table(restaurant, reservation_date_time, minutes_slot)

    if table:
        delta = timedelta(seconds=60*minutes_slot)
        reservation = Reservation(guest = guest, number_of_people = number_of_people, )






