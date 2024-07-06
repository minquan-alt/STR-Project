from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Không có sự kiện gì cả!!')

# Create your views here.
