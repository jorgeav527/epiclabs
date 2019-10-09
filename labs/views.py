from django.shortcuts import render

# Create your views here.

def labs_home_view(request):
    return render(request, 'labs/home.html')

def labs_concrete_view(request):
    return render(request, 'labs/concrete.html')

def labs_material_view(request):
    return render(request, 'labs/material.html')

def labs_soil_view(request):
    return render(request, 'labs/soil.html')


def sector_client_view(request):
    return render(request, 'labs/sector_client.html')


def pricing_view(request):
    return render(request, 'labs/pricing.html')

def contact_view(request):
    return render(request, 'labs/contact.html')

