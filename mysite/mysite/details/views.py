from django.http import HttpResponse
from django.shortcuts import render
from .models import newsData

def index(request):
    return render(request, 'details/index.html')
# Create your views here.

def newsDataView(request, filter):
    # news_data_all = newsData.objects.all()
    news_data = newsData.objects.get(url=filter)
    return render(request, 'details/index.html', {'news_data': news_data})