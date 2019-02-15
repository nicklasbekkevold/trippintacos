from trippinTacos.reservations import models
from datetime import timedelta
sentinel = object()

def delete(reservation_num):
    models.Reservation.objects.filter(id == reservation_num).delete()


def edit(reservation_num, newDate, new_start, new_end=sentinel):
    if new_end is sentinel:
        new_end = new_start + timedelta(hours=2)

    validity_tuple = isValidNewReservation(new_start, new_end, newDate, reservation_num)
    if validity_tuple[0]:
        # Todo In Reservations: change date and time. In Table: Remove res for old table, add res for new table.
        pass
    else:
        # Todo give a error to user which says the changes could not be made.
        pass


def isValidNewReservation(start, stop, ny_dato, reservation_num):
    _reservation = models.Reservation.objects.get(id == reservation_num)
    _table = _reservation.table
    if ny_dato == _reservation.date:
        # Todo Check if the table currently booked is available at new time at same date, with current time set temporarily as open.

        reservations_at_table = models.Reservation.objects.filter(models.Reservation.table == _table)
        for reservation1 in reservations_at_table:
            if reservation1.id != reservation_num:
                collision_bool = checkForCollision(start, stop, reservation1)
                if not collision_bool: # TOdo Men i faen nå kjem den te å si Ja uten å sjekke alle, Gjeld alle nedover. Her mp æ heller legg inn ved bruk av filter. Kutte ned på kodelengde og komplexitet.
                    return True, _table



        for checktable in models.Table.objects.filter(id != _table.id):
            reservations_at_table = models.Reservation.objects.filter(models.Reservation.table == checktable)
            for reservation2 in reservations_at_table:
                collision_bool = checkForCollision(start, stop, reservation2)
                if not collision_bool:
                    return True, _table
        return False, None
    else:
        # Todo Check if any table is available at new date & time
        # if not return false, 0

        for checktable2 in models.Table.objects.all():
            reservations_at_table2 = models.Reservation.objects.filter(models.Reservation.table == checktable2)
            for reservation3 in reservations_at_table2:
                collision_bool = checkForCollision(start, stop, reservation3)
                if not collision_bool:
                    return True, _table
    return False, None


    #Todo Sett inn støtte for Errors, DoesNotExist og MultipleObjectsReturned

def checkForCollision(start_of_new_res, end_of_new_res, preexisting_res):
    preexisting_start = preexisting_res.start_date_time
    preexisting_end = preexisting_res.end_date_time
    if start_of_new_res < preexisting_start and end_of_new_res < preexisting_start:
        return False
    if start_of_new_res > preexisting_end and end_of_new_res > preexisting_end:
        return False
    return True





