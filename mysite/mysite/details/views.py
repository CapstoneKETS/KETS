from django.http import HttpResponse
from django.shortcuts import render
from .models import newsData

def index(request):
    return render(request, 'details/index.html')
# Create your views here.

def newsDataView(request):
    news_data_all = newsData.objects.all()
    return render(request, 'details/index.html', {'news_data_list': news_data_all})