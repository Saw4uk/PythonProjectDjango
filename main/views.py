from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return render(req,'main/index.html')


def about(req):
    return HttpResponse('<h4>About</h4>')
