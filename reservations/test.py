import unittest
from .models import *


def fun(x):
    return x+1

def math(x):
    if x>10:
        return True
    return False

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)

    def test2(self):
        self.assertTrue(math(11))

class ReservationTest(unittest.TestCase):
    def setUp(self):
      Table.objects.create(restaurant = True,number_of_people= 6,is_occupied = False)

    def test3(self):
        test.setUp(self)
        if (Table):
            print('table finnes')
        else:
            print('table finnes ikke')
