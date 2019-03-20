from reservations import models
from guest import models as guestModels
from datetime import timedelta
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string
from trippinTacos.settings import EMAIL_HOST_USER
import smtplib

sentinel = object()


def delete(reservation_num, _email):
    """
    Function for deleting a given reservation.
    :param reservation_num: The unique ID of the reservation.
    :param _email: The email with which the reservation has been made.
    :return: whether a reservation has been deleted.
    """
    '''
    # Getting correct guest
    _guest = guestModels.Guest.objects.all().get(email=_email)
    # Deleting guest's reservation by id and email
    num = models.Reservation.objects.filter(id=reservation_num,
                                            guest=_guest).delete()

    print("Guest: ", _guest)
    print("Num: ", num)
    '''

    return models.Reservation.objects.filter(guest__email=_email, id=reservation_num).delete()[0]


def edit(reservation_num, new_start: datetime, new_end=sentinel):
    """
    Function for editing a current reservation to a new time.
    :param reservation_num: The unique ID of the reservation to edit.
    :param newDate: The proposed new date of the reservation.
    :param new_start: The proposed new start time of the reservation.
    :param new_end: The proposed new end time of the reservation, which has a default of two hours after new_start.
    :return: Returns a bool indicating the success of the edit.
    """
    if new_end is sentinel:
        new_end = new_start + timedelta(hours=2)

    newDate = new_start.date()

    validity_tuple = isValidNewReservation(new_start, new_end, newDate, reservation_num)
    print(validity_tuple[0])
    if validity_tuple[0]:
        rezzy = models.Reservation.objects.get(id=reservation_num)
        rezzy.start_date_time = new_start  # Todo In Reservations: change date and time. In Table: Remove res for old table, add res for new table.
        rezzy.end_date_time = new_end
        rezzy.created_date = datetime.now()
        rezzy.table = validity_tuple[1]
        rezzy.save()
        return True
    else:
        # Todo give a error to user which says the changes could not be made.
        return False


def isValidNewReservation(start, stop, newDate, reservation_num):
    """
    Helper function to iterate through tables looking for a valid new reservation with the new parameters.
    :param start: start of proposed new reservation time.
    :param stop: end of proposed new reservation time.
    :param newDate: The proposed new date of the reservation.
    :param reservation_num: The unique ID of the reservation to edit.
    :return: A tuple containing a bool value indicating the avaliability of the new times, and a int indicating the
    table number.
    """
    _reservation = models.Reservation.objects.get(id=reservation_num)
    _table = _reservation.table
    old_date=_reservation.start_date_time.date()
    if newDate == _reservation.start_date_time.date():
        # Check if the table currently booked is available at new time at same date, with current time set temporarily as open.
        coll = 0
        reservations_at_table = models.Reservation.objects.filter(
            table=_table).exclude(id=_reservation.id)
        for reservation1 in reservations_at_table:
            if checkForCollision(start, stop,
                                 reservation1):
                coll += 1
                break  # Breaks if collision as checking any more at same table is redundant
        if coll == 0:
            return True, _table  # If no collisions at the table, return table and

        # checks if any other table is available at new time
        for checktable in models.Table.objects.filter(~Q(id=_table.id)):
            coll = 0
            reservations_at_table = models.Reservation.objects.filter(~Q(id=_reservation.id), table=checktable)
            for reservation2 in reservations_at_table:
                if checkForCollision(start, stop,
                                     reservation2):
                    coll += 1
                    break  # Breaks if collision as checking any more at same table is redundant
            if coll == 0:
                return True, checktable
        return False, None

    else:  # Checks if any table is available at new date & time
        for checktable2 in models.Table.objects.all():
            coll = 0
            reservations_at_table2 = models.Reservation.objects.filter(table=checktable2)
            for reservation3 in reservations_at_table2:
                if checkForCollision(start, stop, reservation3):
                    coll += 1
                    break
            if coll == 0:
                return True, checktable2
        return False, None


        # Todo Sett inn støtte for Errors, DoesNotExist og MultipleObjectsReturned


def checkForCollision(start_of_new_res, end_of_new_res, preexisting_res):
    """
    Function for checking whether a collision happens between a preexisting reservation and the given parameters
    :param start_of_new_res: The start time of the new reservation
    :param end_of_new_res: The start time of the new reservation
    :param preexisting_res: The reservation object of the preexisting reservation
    :return: A bool value indicating whether a collision will happen.
    """
    preexisting_start = preexisting_res.start_date_time
    preexisting_end = preexisting_res.end_date_time
    if start_of_new_res < preexisting_start and end_of_new_res <= preexisting_start:
        return False
    if start_of_new_res >= preexisting_end and end_of_new_res > preexisting_end:
        return False
    return True


####################################################################################################
# This function returns a list containing tuples on the form                                       #
# (reservation start(datetime object), reservation end(datetime object), duration(hours), tableID) #
####################################################################################################

def get_all_booked_dates_and_time():
    """
    NAME = get_all_booked_dates_and_time
    DESCRIPTION = Returns a list containing tuples on the form:
    (reservation start(datetime object), reservation end(datetime object), duration(hours), tableID)
    :return: list of dates
    """
    # Get all reservations
    reservations = models.Reservation.objects.all()
    dates = []

    # Loop through all reservations to get start time, end time and table.
    for res in reservations:
        dates.append((res.start_date_time,
                      res.end_date_time,
                      res.start_date_time - res.end_date_time,
                      res.table))

    return dates


def get_tables_with_capacity(num):
    """
    NAME: get_tables_with_capaxity
    DESCRIPTION: gets tables that have capacity greater than or equal to a certain number
    :param num: Minimum capacity
    :return: QuerySet containing tables with capacity greater than or equal to :param num
    """
    return models.Table.objects.filter(number_of_seats__gte=num)


def change_number_of_people(res, num):
    """
    NAME: change_number_of_people
    DESCRIPTION: Changes the number of people on a reservation
    :param res: reservation to be changed
    :param num: how many people it will be changed into
    :return: true/false
    """
    # If the table already has enough seats, just return true
    if res.table.number_of_seats >= num:
        return True

    # Get tables with right capacity
    tables = get_tables_with_capacity(num)

    # Get all res, except the one being changed
    all_res = models.Reservation.objects.filter(end_date_time__lte=res.start_date_time,
                                                start_date_time__gte=res.end_date_time)

    # Check if any tables in all_res is in tables list with right capacity, if it is, change table for res
    for reservation in all_res:
        if reservation.table in tables:
            res.table.is_occupied = 0
            res.table = reservation.table
            return True

    return False


def send_confirmation(guest, res):
    '''
    Sends confirmation mail.
    :param email:
    :param res:
    :return: True
    '''
    msg_plain = render_to_string('employee/email.txt', {'res_num': res.id, 'email': guest.email, 'last_name': guest.last_name})

    send_mail(
        'TrippinTacos reservation ' + str(res.id),
        msg_plain,
        EMAIL_HOST_USER,
        [str(guest.email)],
    )

    return True


def send_cancellation(email, id):
    """
    Sends confirmation mail.
    :param email: The email of the client
    :param res: The reservation of which is cancelling
    :return: Bool value indicating whether mail was sent.
    """

    msg_plain = "Your reservation with reservation ID " + str(id) + " has now been successfully cancelled."
    try:
        send_mail(
            'Cancellation confirmation ' + str(id),
            msg_plain,
            EMAIL_HOST_USER,
            [str(email)],
        )

        return True

    except smtplib.SMTPException:
        return False


def get_booked_times_by_date(date, number_of_people):
    """

    :param date: date to check
    :param number_of_people: number of people that will be dining
    :return:
    """

    reservations = models.Reservation.objects.filter(
        start_date_time__year=2019,
    )

    print(reservations)


get_booked_times_by_date(datetime(2019, 2, 25, 12, 0, 0), 5)


def deleteGuest(guest):

    guest.email = None
    guest.first_name = None
    guest.last_name = None
    guest.save()

    return True
