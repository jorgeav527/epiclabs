from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import *

# Create your views here.

# STUDENT
#========

def register_student(request):
    if request.method == "POST":
        form = StudentRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el estudiante { username }")
            return redirect('accounts:login')
    else:
        form = StudentRegister()
    context = { "form": form }
    return render(request, 'accounts/register_student.html', context)


def profile_student(request):
    profile_account = AccountUpdateForm(request.POST, instance=request.user)
    profile_student = StudentUpdateForm(request.POST, instance=request.user.studentprofile)
    if profile_account.is_valid() and profile_student.is_valid():
        profile_account.save()
        profile_student.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_student')

    else:
        profile_account = AccountUpdateForm(instance=request.user)
        profile_student = StudentUpdateForm(instance=request.user.studentprofile)

    context = {
        "profile_account": profile_account,
        "profile_student": profile_student,
    }

    return render(request, 'accounts/profile_student.html', context)


# BACH
#=====

def register_bach(request):
    if request.method == "POST":
        form = BachRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el bachiller { username }")
            return redirect('accounts:login')
    else:
        form = BachRegister()
    context = { "form": form }
    return render(request, 'accounts/register_bach.html', context)


def profile_bach(request):
    profile_account = AccountUpdateForm(request.POST, instance=request.user)
    profile_bach = BachUpdateForm(request.POST, instance=request.user.bachprofile)
    if profile_account.is_valid() and profile_bach.is_valid():
        profile_account.save()
        profile_bach.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_bach')

    else:
        profile_account = AccountUpdateForm(instance=request.user)
        profile_bach = BachUpdateForm(instance=request.user.bachprofile)

    context = {
        "profile_account": profile_account,
        "profile_bach": profile_bach,
    }

    return render(request, 'accounts/profile_bach.html', context)


# TEACHER
#========

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el profesor { username }")
            return redirect('accounts:login')
    else:
        form = TeacherRegister()
    context = { "form": form }
    return render(request, 'accounts/register_teacher.html', context)


def profile_teacher(request):
    profile_account = AccountUpdateForm(request.POST, instance=request.user)
    profile_teacher = TeacherUpdateForm(request.POST, instance=request.user.teacherprofile)
    if profile_account.is_valid() and profile_teacher.is_valid():
        profile_account.save()
        profile_teacher.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_teacher')

    else:
        profile_account = AccountUpdateForm(instance=request.user)
        profile_teacher = TeacherUpdateForm(instance=request.user.teacherprofile)

    context = {
        "profile_account": profile_account,
        "profile_teacher": profile_teacher,
    }

    return render(request, 'accounts/profile_teacher.html', context)


# CLIENT
#========

def register_client(request):
    if request.method == "POST":
        form = ClientRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el cliente { username }")
            return redirect('accounts:login')
    else:
        form = ClientRegister()
    context = { "form": form }
    return render(request, 'accounts/register_client.html', context)


def profile_client(request):
    profile_account = AccountUpdateForm(request.POST, instance=request.user)
    profile_client = ClientUpdateForm(request.POST, instance=request.user.clientprofile)
    if profile_account.is_valid() and profile_client.is_valid():
        profile_account.save()
        profile_client.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_client')

    else:
        profile_account = AccountUpdateForm(instance=request.user)
        profile_client = ClientUpdateForm(instance=request.user.clientprofile)

    context = {
        "profile_account": profile_account,
        "profile_client": profile_client,
    }

    return render(request, 'accounts/profile_client.html', context)


# ADMIN
#========

def register_admin(request):
    if request.method == "POST":
        form = AdminRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el administrador { username }")
            return redirect('accounts:login')
    else:
        form = AdminRegister()
    context = { "form": form }
    return render(request, 'accounts/register_admin.html', context)


def profile_admin(request):
    profile_account = AccountUpdateForm(request.POST, instance=request.user)
    profile_admin = AdminUpdateForm(request.POST, instance=request.user.adminprofile)
    if profile_account.is_valid() and profile_admin.is_valid():
        profile_account.save()
        profile_admin.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_admin')

    else:
        profile_account = AccountUpdateForm(instance=request.user)
        profile_admin = AdminUpdateForm(instance=request.user.adminprofile)

    context = {
        "profile_account": profile_account,
        "profile_admin": profile_admin,
    }

    return render(request, 'accounts/profile_admin.html', context)
