from django.shortcuts import render

# Create your views here.

def labs_concrete_view(request):
    return render(request, 'labs/labs/concrete.html')


def labs_material_view(request):
    return render(request, 'labs/labs/material.html')


def labs_soil_view(request):
    return render(request, 'labs/labs/soil.html')
