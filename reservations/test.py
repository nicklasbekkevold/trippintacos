import unittest
from django.test import TestCase
from .models import *


def fun(x):
    return x+1

def math(x):
    if x>10:
        return True
    return False

class MyTestTestCase(TestCase):
    def test11(self):
        self.assertEqual(fun(3), 4)

    def test2(self):
        self.assertTrue(math(11))

class ReservationTestCase(TestCase):
    def func(self):
      Table.objects.create(id = 1, restaurant = True,number_of_people= 6,is_occupied = False)

    def test3(self):
        t= Table.objects.all().get(id=1)
        if t is not None:
            print('table finnes')
        else:
            print('table finnes ikke')
