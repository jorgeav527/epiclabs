from django.shortcuts import render

# Create your views here.

def home_view(request):
    return render(request, 'labs/generals/home.html')


def pricing_view(request):
    return render(request, 'labs/generals/pricing.html')


def contact_view(request):
    return render(request, 'labs/generals/contact.html')
