from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group

from employee.templatetags import auth_extras
import json


class TestViews(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()
        self.employee_url = reverse('employee')
        user = User.objects.create(username="owner", password="hvaskjer123")
        group = Group.objects.create(name="owner")

        group.save()
        user.save()

        user.groups.add(group)
        user.save()

        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.employee_url)
        self.assertRedirects(response, '/login/?next=/employee/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1', password='1X<ISRUkw+tuK')  # Log in user
        response = self.client.get(self.employee_url)
        self.assertEqual(str(response.context['user']), 'testuser1')  # Check if user is logged in
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'employeepage.html')

    def test_auth_statistic(self):

        owner = User.objects.filter(username="owner").get()
        self.assertTrue(auth_extras.has_group(owner, "owner"))

        guest = User.objects.filter(username="testuser1").get()
        self.assertFalse(auth_extras.has_group(guest, "owner"))

