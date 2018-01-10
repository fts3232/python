from django.http import HttpResponse
from django.shortcuts import render


def list(request):
    return render(request, 'index.html', content_type='text/html')


def single(request):
    return render(request, 'index.html', content_type='text/html')
