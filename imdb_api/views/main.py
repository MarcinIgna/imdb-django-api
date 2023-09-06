from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from imdb_api.models.person_model import Person


def frontpage(request):
    return render(request, 'core/frontpage.html')

@login_required(login_url='imdb:login')
def logged_in_homepage(request):
    return render(request, 'core/logged_in_homepage.html')

