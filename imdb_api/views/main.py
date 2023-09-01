from django.http import HttpResponse
from django.shortcuts import render, redirect



def main(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def frontpage(request):
    return render(request, 'core/frontpage.html')