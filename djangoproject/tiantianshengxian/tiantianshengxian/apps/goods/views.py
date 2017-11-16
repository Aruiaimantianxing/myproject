from django.shortcuts import render

# Create your views here.

# from django.views.generic import View


def index(request):

    return render(request,'html/index.html')


