from django.test import SimpleTestCase
from django.urls import reverse, resolve
from guest.views import guest

class TestUrls(SimpleTestCase):

    def test_guest_url_resolves(self):
        url = reverse('guest')
        self.assertEquals(resolve(url).func, guest)