from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def frontpage(request):
    return render(request, 'core/frontpage.html')

def logged_in_frontpage(request):
    return render(request, '')

