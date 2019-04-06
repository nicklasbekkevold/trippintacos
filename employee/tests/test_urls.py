from django.test import SimpleTestCase, Client
from django.urls import reverse, resolve
from employee.views import Employee

class TestUrls(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.employee_url = reverse('employee')

    def test_employee_url_resolves(self):
        response = self.client.get(self.employee_url)
        self.assertEquals(response.status_code, 302)
        

        '''
        url = reverse('employee')
        self.assertEquals(resolve(url).func, Employee.get)
        '''