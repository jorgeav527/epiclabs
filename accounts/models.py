from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from course.models import Course
from category.models import Category

# Create your models here.

class User(AbstractUser):
    is_student  = models.BooleanField(default=False)
    is_bach     = models.BooleanField(default=False)
    is_teacher  = models.BooleanField(default=False)
    is_client   = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class StudentProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    dni         = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    codigo      = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student {self.user.first_name} {self.user.last_name} {self.codigo} as {self.user.username}"


class BachProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    dni         = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    codigo      = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bach {self.user.first_name} {self.user.last_name} {self.codigo} as {self.user.username}"


class TeacherProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    course      = models.ManyToManyField(Course)
    dni         = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    codigo      = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ing. {self.user.first_name} {self.user.last_name} {self.codigo} as {self.user.username}"


class ClientProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    long_name   = models.CharField(max_length=64, null=True, blank=True)
    direction   = models.CharField(max_length=64, null=True, blank=True)
    reference   = models.CharField(max_length=64, null=True, blank=True)
    category    = models.ManyToManyField(Category)
    ruc         = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    phone       = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Org. {self.user.username} {self.ruc}"


class AdminProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    staff       = models.CharField(max_length=5)
    dni         = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    codigo      = models.BigIntegerField(null=True, blank=True, validators=[alphanumeric])
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ing. {self.user.first_name} {self.user.last_name} {self.codigo} as {self.user.username} {self.staff}"