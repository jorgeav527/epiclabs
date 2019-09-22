from django.shortcuts import render

# Create your views here.

def sector_student_view(request):
    return render(request, 'sectors/sector_student.html')

def sector_thesis_view(request):
    return render(request, 'sectors/sector_thesis.html')

def sector_client_view(request):
    return render(request, 'sectors/sector_client.html')
