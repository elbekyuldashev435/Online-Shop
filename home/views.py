from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home_page(request):
    return render(request, 'index.html')


