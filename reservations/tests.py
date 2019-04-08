from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from reservations.models import Reservation, Restaurant, Table
from guest.models import Guest
from datetime import *
from employee.helpers import *
from django.utils import timezone
from reservations.reservation import *
from reservations.forms import ReservationForm

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
# NOT IMPLEMENTED
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
'''


class DeleteReservationTestCase(TestCase):

    def setUp(self):
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",
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

'''
# DOES NOT WORK DUE TO OFFSET NAIVE AND AWARE DATETIMES, DUNNO
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
'''


class TestSendConfirmation(TestCase):
    def setUp(self):
        self.now = timezone.now()
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="sander.b.lindberg@gmail.com",
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
        self.assertTrue(send_confirmation(guest, res))

'''
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

'''


class TestGetAverageCapacity(TestCase):
    def setUp(self):
        Reservation.objects.create(
            id=1,
            guest=Guest.objects.create(
                email="test@testcase.no",

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
                email="test@testcase.no",

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


class TestViews(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()
        self.guest_url = reverse('terms_and_conditions')


    def test_termsandconditions_GET(self):
        response = self.client.get(self.guest_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'termsandconditions.html')

    def testCheckedTermsAndConditions(self):
        data = {
            'first_name': 'Sander',
            'last_name': 'Lindberg',
            'email': 'S.lindberg@test.com',
            'number_of_people': '3',
            'start_date': '2019-04-06',
            'start_time': '12:00',
            'i_have_read_and_agree_checkbox': False
        }
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            'first_name': 'Sander',
            'last_name': 'Lindberg',
            'email': 'S.lindberg@test.com',
            'number_of_people': '3',
            'start_date': '2019-04-06',
            'start_time': '12:00',
            'i_have_read_and_agree_checkbox': True
        }
        form = ReservationForm(data=data)

        self.assertTrue(form.is_valid())


class TestGetAvailableTimes(TestCase):
    
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
            guest=Guest.objects.all().get(email="test@testcase.no"),
            number_of_people=4,
            start_date_time=datetime(2019, 3, 27, 17),
            end_date_time=datetime(2019, 3, 27, 19),
            table=Table.objects.get(id=1),
            walkin=1,
        )

        Reservation.objects.create(
            id=2,
            guest=Guest.objects.all().get(
                email="test@testcase.no"
            ),
            number_of_people=4,
            start_date_time=datetime(2019, 3, 27, 20),
            end_date_time=datetime(2019, 3, 27, 22),
            table=Table.objects.get(id=1),
            walkin=0,
        )

    def test_get_available_times(self):
        self.assertEqual([('12:00', '12:00'),
                          ('12:30', '12:30'),
                          ('13:00', '13:00'),
                          ('13:30', '13:30'),
                          ('14:00', '14:00'),
                          ('14:30', '14:30'),
                          ('15:00', '15:00'),
                          ('22:00', '22:00')
                          ], get_available_times(4, '2019-03-27'))

        self.assertEqual([], get_available_times(6, '2019-03-27'))


class TestGetNextAvailableTable(TestCase):

    def setUp(self):
        Guest.objects.create(
            email="test@testcase.no",
            first_name="test",
            last_name="case"
        )

        Table.objects.create(
            id=1,
            number_of_seats=6
        )

        Table.objects.create(
            id=2,
            number_of_seats=5
        )

        Reservation.objects.create(
            id=1,
            guest=Guest.objects.all().get(email="test@testcase.no"),
            number_of_people=4,
            start_date_time=datetime(2019, 3, 27, 17),
            end_date_time=datetime(2019, 3, 27, 19),
            table=Table.objects.get(id=1),
            walkin=1,
        )


    def test_get_next_available_table(self):
        self.assertEqual(Table.objects.get(id=2), get_next_available_table(None,
                                                                             datetime(2019, 3, 27, 12), 4))
        self.assertEqual(Table.objects.get(id=2), get_next_available_table(None,
                                                                             datetime(2019, 3, 27, 17), 5))

        Reservation.objects.create(
            id=2,
            guest=Guest.objects.all().get(email="test@testcase.no"),
            number_of_people=4,
            start_date_time=datetime(2019, 3, 27, 17),
            end_date_time=datetime(2019, 3, 27, 19),
            table=Table.objects.get(id=2),
            walkin=1,
        )

        self.assertEqual(None, get_next_available_table(None,
                                                            datetime(2019, 3, 27, 17), 5))