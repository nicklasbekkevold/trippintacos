from django.shortcuts import render
from reservations.forms import ReservationForm
# Create your views here.


def guest(request):
    return render(request, 'guest/guestpage.html')
