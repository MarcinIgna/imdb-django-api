from django.http import HttpResponse



def main(request):
    return HttpResponse("Hello, world. You're at the polls index.")