from django.shortcuts import render

def index(request):
    return render(request, 'exp/index.html')

def add_exp(request):
    return render(request, 'exp/add_exp.html')
