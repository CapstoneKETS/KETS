# <<<<<<< Chea-Dan-bi
# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import newsData

# def index(request):
#     details = newsData.objects
#     #미완성. newsData에서 요약문을 가져올 방법을 찾는 중입니다.
#     return render(request, 'details/index.html')
# # Create your views here.
# =======  02-18일자 단비님 커밋 부분
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

