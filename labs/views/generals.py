from django.shortcuts import render

from accounts.models import *

# Create your views here.

def intro_view(request):
    return render(request, 'labs/generals/intro.html')

def home_view(request):
    return render(request, 'labs/generals/home.html')


def pricing_view(request):
    return render(request, 'labs/generals/pricing.html')


def contact_view(request):
    return render(request, 'labs/generals/contact.html')



