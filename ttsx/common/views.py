from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'duser/index.html')


def detail(request):
    return render(request, 'duser/detail.html')


def more_goods(request):
    return render(request, 'duser/list.html')

