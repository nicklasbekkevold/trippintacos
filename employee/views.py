from django.shortcuts import render

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def employee(request):
    context = {
        'title': 'Ansatt'
    }
    return render(request, 'employeepage.html', context)

