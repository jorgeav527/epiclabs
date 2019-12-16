from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import *
from thesis.models import Thesis
from construction.models import Construction
from reference_person.models import ReferencePerson
from students.models import StudentGroup
from accounts.models import GroupProfile

# Create your views here.

# GROUP
#========

def register_group(request):
    if request.method == "POST":
        form = GroupRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Cuenta creada para el estudiante { username }")
            return redirect('accounts:login')
    else:
        form = GroupRegister()
    context = { "form": form }
    return render(request, 'accounts/register_group.html', context)


def profile_group(request):
    student_group = StudentGroup.objects.filter(group_profile=request.user.groupprofile)
    obj = get_object_or_404(GroupProfile, id=request.user.groupprofile.id) # !! to dont colapce the db
    profile_account = GroupAccountUpdatedForm(request.POST, instance=request.user)
    profile_group = GroupUpdateForm(request.POST, instance=request.user.groupprofile)

    if profile_account.is_valid() and profile_group.is_valid():
        profile_account.save()
        profile_group.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_group')

    else:
        profile_account = GroupAccountUpdatedForm(instance=request.user)
        profile_group = GroupUpdateForm(instance=request.user.groupprofile)

    context = {
        "obj": obj,
        "student_group": student_group,
        "profile_account": profile_account,
        "profile_group": profile_group,
    }

    return render(request, 'accounts/profile_group.html', context)


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
    thesis = Thesis.objects.filter(bach_profile=request.user.bachprofile)
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
        "obj_list": thesis,
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
    reference_person = ReferencePerson.objects.filter(client_profile=request.user.clientprofile)
    construction = Construction.objects.filter(client_profile=request.user.clientprofile)
    profile_account = ClientAccountUpdatedForm(request.POST, instance=request.user)
    profile_client = ClientUpdateForm(request.POST, instance=request.user.clientprofile)
    if profile_account.is_valid() and profile_client.is_valid():
        profile_account.save()
        profile_client.save()
        messages.success(request, f"La cuenta ha sido actualizada")
        return redirect('accounts:profile_client')

    else:
        profile_account = ClientAccountUpdatedForm(instance=request.user)
        profile_client = ClientUpdateForm(instance=request.user.clientprofile)

    context = {
        "obj_list_reference_person": reference_person, 
        "obj_list_construction": construction,
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
