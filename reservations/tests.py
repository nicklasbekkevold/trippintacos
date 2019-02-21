from django.test import TestCase
from django.utils import timezone
from unittest import TestCase
from django.test import TestCase
from trippinTacos.reservations.models import *
from trippinTacos.guest.models import *
from datetime import *
from trippinTacos.employee.helpers import *
# Create your tests here.


class GetTablesWithCapacityTestCase(TestCase):
    def setUp(self):
        Table.objects.create(
            restaurant=Restaurant.objects.first(),
            number_of_seats=5,
            is_occupied=0
        )
        Table.objects.create(
            restaurant=Restaurant.objects.first(),
            number_of_seats=4,
            is_occupied=0
        )

    def test_get_tables(self):
        # Test for table with 5 or more seats
        tables = get_tables_with_capacity(5)
        self.assertEqual(1, len(tables))
        # Test for table with 6 or more seats
        tables = get_tables_with_capacity(6)
        self.assertEqual(0, len(tables))
        # Test for tables with 4 or more seats
        tables = get_tables_with_capacity(4)
        self.assertEqual(2, len(tables))


'''
class ChangeNumberOfPeopleTestCase(TestCase):
    def setUp(self):
        Table.objects.create(
            restaurant=Restaurant.objects.first(),
            number_of_seats=5,
            is_occupied=0
        )

        Guest.objects.create(
            email="Sander.b.lindberg@gmail.com",
            reminder=1
        )

        print("TABLE: ", Table.objects.first())
        Reservation.objects.create(
            guest=Guest.objects.first(),
            number_of_people=2,
            start_date_time=datetime(2019, 2, 19, 20, 0, 0),
            end_date_time=datetime(2019, 2, 19, 22, 0, 0),
            created_date=timezone.now,
            table=Table.objects.first()
        )

    def test_change_number(self):
        self.assertTrue(change_number_of_people(Reservation.objects.first(), 5))
'''


class DeleteReservationTestCase(TestCase):
    def setUp(self):
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            end_date_time=(timezone.now() + timedelta(hours=2)),
            table=Table.objects.create(
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0
            )
        )

    def test_delete(self):
        self.assertEqual(1, delete(1, "test@testcase.no"))


class EditReservationTestCase(TestCase):
    def setUp(self):
        self.now = datetime.now()
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            end_date_time=(self.now + timedelta(hours=2)),
            table=Table.objects.create(
                id=1,
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0
            )
        )
        Reservation.objects.create(
            id=2,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            start_date_time=(self.now + timedelta(days=1)),
            end_date_time=(self.now + timedelta(days=2)),
            table=Table.objects.get(Table.objects.id == 1)
        )

    def testEditReservation(self):
        # Test edit to new open slot works
        res = Reservation.objects.get(Reservation.objects.id == 1)
        self.assertTrue(edit(res, self.now + timedelta(days=3)))
        # Test edit to new slot open overlapping with the same reservation
        self.assertTrue(edit(res, res.start_date_time + timedelta(hours=1)))
        # Test edit slot taken by other reservation
        self.assertFalse(edit(res, self.now + timedelta(days=1)))
