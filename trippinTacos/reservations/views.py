from django.shortcuts import render
from .forms import ReservationForm


# Create your views here.


def booking(request):
    form = ReservationForm()
    return render(request, 'booking.html', {'form': form})
