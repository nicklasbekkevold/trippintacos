from django.test import SimpleTestCase
from django.urls import reverse, resolve
from employee.views import employee

class TestUrls(SimpleTestCase):

    def test_employee_url_resolves(self):
        url = reverse('employee')
        self.assertEquals(resolve(url).func, employee)