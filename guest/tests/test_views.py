from django.test import TestCase, Client
from django.urls import reverse
from guest.models import Guest
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
