from django.test import TestCase, Client
from django.urls import reverse
from guest.models import Guest
from django.test.client import RequestFactory
from guest.views import deleteMe
import json


class TestViews(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()
        self.guest_url = reverse('guest')

    def test_guest_GET(self):
        response = self.client.get(self.guest_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'guestpage.html')


class TestDeleteMe(TestCase):

    def setUp(self):

        self.c = RequestFactory()

        Guest.objects.create(
            id=1,
            email="sander.b.lindberg@gmail.com",
            first_name="Sander",
            last_name="Lindberg",
        ),

    def testDelete(self):
        guest = Guest.objects.all().get(id=1)
        self.assertEqual(guest.email, "sander.b.lindberg@gmail.com")
        self.assertEqual(guest.first_name, "Sander")
        self.assertEqual(guest.last_name, "Lindberg")

        request = self.c.get('http://localhost:8000/deleteme', {'last_name': "Lindberg", 'email': "adrian@gmail.com"})
        deleteMe(request)

        guest = Guest.objects.all().get(id=1)
        self.assertEqual(guest.email, "sander.b.lindberg@gmail.com")
        self.assertEqual(guest.first_name, "Sander")
        self.assertEqual(guest.last_name, "Lindberg")

        request = self.c.get("http://localhost:8000/deleteme", {'last_name': "Langseth", 'email': "sander.b.lindberg@gmail.com"})
        deleteMe(request)

        guest = Guest.objects.all().get(id=1)
        self.assertEqual(guest.email, "sander.b.lindberg@gmail.com")
        self.assertEqual(guest.first_name, "Sander")
        self.assertEqual(guest.last_name, "Lindberg")

        request = self.c.get("http://localhost:8000/deleteme", {'last_name': "Lindberg", 'email': "sander.b.lindberg@gmail.com"})
        deleteMe(request)

        guest = Guest.objects.all().get(id=1)
        self.assertIsNone(guest.email)
        self.assertIsNone(guest.first_name)
        self.assertIsNone(guest.last_name)
