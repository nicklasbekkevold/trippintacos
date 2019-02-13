from django.shortcuts import render
from reservations.forms import ReservationForm
# Create your views here.


def test(request):
    return render(request, 'guest/test.html')
