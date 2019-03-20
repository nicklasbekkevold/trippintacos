from django.test import TestCase
from django.utils import timezone
from reservations.models import Reservation, Restaurant, Table
from guest.models import Guest
from datetime import *
from employee.helpers import *
from django.utils import timezone
from reservations.reservation import *
# Create your tests here.

'''
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
            start_date_time=str(datetime(2019, 2, 19, 20, 0, 0)),
            end_date_time=str(datetime(2019, 2, 19, 22, 0, 0)),
            created_date=timezone.now(),
            table=Table.objects.first()
        )

    def test_change_number(self):
        self.assertTrue(change_number_of_people(Reservation.objects.first(), 5))


class DeleteReservationTestCase(TestCase):

    def setUp(self):
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            start_date_time=timezone.now(),
            end_date_time=(timezone.now() + timedelta(hours=2)),
            table=Table.objects.create(
                restaurant=Restaurant.objects.first(),
                number_of_seats=5
            ),
        )
        Reservation.objects.create(
            id=2,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            start_date_time=timezone.now(),
            end_date_time=(timezone.now() + timedelta(hours=2)),
            table=Table.objects.create(
                restaurant=Restaurant.objects.first(),
                number_of_seats=5
            ),
        )

    def test_delete(self):
        self.assertEqual(1, delete(1, "test@testcase.no"))
        self.assertEqual(0, delete(2, "Sander.b.lindberg@dmail.com"))
        self.assertEqual(1, delete(2, "test@testcase.no"))


class EditReservationTestCase(TestCase):

    def setUp(self):
        self.now = timezone.now()
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
            ),
            number_of_people=4,
            start_date_time=self.now,
            end_date_time=(self.now + timedelta(hours=2)),
            table=Table.objects.create(
                id=1,
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0
            ),
            walkin=1,
        )
        Reservation.objects.create(
            id=2,
            guest=Guest.objects.create(
                email="test@testcase.no",
            ),
            number_of_people=4,
            start_date_time=(self.now + timedelta(days=1)),
            end_date_time=(self.now + timedelta(days=2)),
            table=Table.objects.get(id=1),
            walkin=0,
        )

    def testEditReservation(self):
        # Test edit to new open slot works
        res = Reservation.objects.get(id=1)
        self.assertTrue(edit(res.id, self.now + timedelta(days=3)))
        # Test edit to new slot open overlapping with the same reservation
        self.assertTrue(edit(res.id, res.start_date_time + timedelta(hours=1)))
        # Test edit slot taken by other reservation
        self.assertFalse(edit(res.id, self.now + timedelta(days=1)))
        pass

class MakeReservation(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            name='testRestaurant',
            description='testRestaurant',
            opening_time=datetime.time(12, '%h')
            
        )



class TestSendConfirmation(TestCase):
    def setUp(self):
        self.now = timezone.now()
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="sander.b.lindberg@gmail.com",
                reminder=False,
            ),
            number_of_people=4,
            start_date_time=(self.now + timedelta(days=1)),
            end_date_time=(self.now + timedelta(days=2)),
            table=Table.objects.create(
                id=1,
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0,
            ),
            walkin=0
        )

    def testSendEmail(self):
        res = Reservation.objects.all().get(id=1)
        guest = res.guest
        self.assertTrue(send_confirmation(guest.email, res))

class TestCountReservations(TestCase):
    def setUp(self):
        self.now = timezone.now()
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
                reminder=False
            ),
            number_of_people=4,
            start_date_time=self.now,
            end_date_time=(self.now + timedelta(hours=2)),
            table=Table.objects.create(
                id=1,
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0
            ),
            walkin=1,
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
            table=Table.objects.get(id=1),
            walkin=0,
        )

    def testCount(self):
        self.assertEquals(2, countReservations())
        print(countReservations())
        self.assertEquals(1, delete(1, "test@testcase.no"))
        self.assertEquals(1, countReservations())
        print(countReservations())


class TestGetAverageCapacity(TestCase):
    def setUp(self):
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no"
            ),
            number_of_people=4,
            start_date_time=datetime.today() + timedelta(hours=4) - timedelta(days=14),
            end_date_time=datetime.today() + timedelta(hours=8) - timedelta(days=14),
            table=Table.objects.create(
                id=1,
                restaurant=Restaurant.objects.first(),
                number_of_seats=5,
                is_occupied=0
            ),
            walkin=1,
        )
        Reservation.objects.create(
            id=2,
            guest=Guest.objects.create(
                email="test@testcase.no"
            ),
            number_of_people=7,
            start_date_time=datetime.today() + timedelta(hours=5) - timedelta(days=7),
            end_date_time=datetime.today() + timedelta(hours=9) - timedelta(days=7),
            table=Table.objects.get(id=1),
            walkin=0,
        )

    def testAveCap(self):
        capMat = get_average_capacity(datetime.today().weekday())
        print(capMat[0])
        print(capMat[1])
        print(capMat[2])

        matplotfuckeroo(capMat, datetime.today().weekday())

'''


class TestGetAvailableTable(TestCase):
    def setUp(self):
        Guest.objects.create(
            email="test@testcase.no",
            first_name="test",
            last_name="case"
        )

        Table.objects.create(
            id=1,
            restaurant=Restaurant.objects.first(),
            number_of_seats=5
        )

        Reservation.objects.create(
            id=1,
            guest=Guest.objects.get(email="test@testcase.no"),
            number_of_people=4,
            start_date_time=datetime.now() + timedelta(hours=4),
            end_date_time=datetime.now() + timedelta(hours=6),
            table=Table.objects.get(id=1),
            walkin=1,
        )

        Reservation.objects.create(
            id=2,
            guest=Guest.objects.get(
                email="test@testcase.no"
            ),
            number_of_people=4,
            start_date_time=datetime.now() + timedelta(hours=7),
            end_date_time=datetime.now() + timedelta(hours=9),
            table=Table.objects.get(id=1),
            walkin=0,
        )

    def test_get_available_times(self):
        print(get_available_times(5, datetime.now() + timedelta(hours=4)))