from django.shortcuts import render

from django.contrib.auth.decorators import login_required
# Create your views here.


def test(request):
    return render(request, 'employee/employeepage.html')


@login_required
def employee(request):
    context = {
        'title': 'Ansatt'
    }
    return render(request, 'employee/employeepage.html', context)

