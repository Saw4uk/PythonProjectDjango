from django.shortcuts import render
from django.http import HttpResponse
from .models import *

import ApiLoader


def main(req):
    context = {
        'HTMLPASTEROBJECT': HTMLPaster.objects.get(theme = 'HTMLPASTEROBJECT').content
    }
    return render(req, 'main/main.html', context = context)

def geography(req):
    return render(req,'main/geography.html')

def needable(req):
    return render(req,'main/needable.html')

def skills(req):
    return render(req,'main/skills.html')

def vacancies(req):
    vacanciesList = ApiLoader.API_loader.Load_API()
    context = {'vacncies_list':vacanciesList}
    return render(req,'main/vacancies.html',context = context)