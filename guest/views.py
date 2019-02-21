from django.shortcuts import render
from reservations.forms import ReservationForm

def guest(request):
    return render(request, 'guestpage.html')
