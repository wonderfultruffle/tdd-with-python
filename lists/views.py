from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    # 책 방식: Get 과 POST를 모두 공통으로 처리
    return render(request, "lists/home.html", {"new_item_text": request.POST.get("item_text", '')})
    
    # 내 방식: request가 Get 일 때와 POST일 때를 나누어 처리
    # if request.method == "POST":
    #     return render(request, "lists/home.html", {"new_item_text": request.POST["item_text"]})
    # return render(request, "lists/home.html")
