from django.shortcuts import render
from django.http import HttpResponseRedirect


def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})