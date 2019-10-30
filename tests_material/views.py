from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
import pdfkit
from django.template.loader import get_template
from django.db.models import F
