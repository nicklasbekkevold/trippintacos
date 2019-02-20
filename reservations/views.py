from django.shortcuts import render
from .forms import ReservationForm
from django.shortcuts import redirect
from guest.models import *


# Create your views here.


def booking(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            email_liste = []
            for each in Guest.objects.all():
                email_liste.append(each)

            if email not in email_liste:
                Guest.objects.create(email, form.cleaned_data['reminder'])

            post = form.save()
            post.save()
            return redirect(request, 'base.html')

    else:
        form = ReservationForm()
        return render(request, 'booking.html', {'form': form})


