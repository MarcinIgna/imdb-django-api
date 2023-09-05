from django.http import HttpResponse
from django.shortcuts import render, redirect


def frontpage(request):
    return render(request, 'core/frontpage.html')