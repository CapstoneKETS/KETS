from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    details = NewsDetailData.objects

    return render(request, 'details/index.html')
# Create your views here.
