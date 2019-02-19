from django.shortcuts import render
from .forms import ReservationForm
from django.shortcuts import redirect


# Create your views here.


def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect(request, 'base.html')

    else:
        form = ReservationForm()
    return render(request, 'booking.html', {'form': form})


