from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name="exp"),
    path("add-exp", views.add_exp, name="add-exp"),
    
]
