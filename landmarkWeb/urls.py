#My routes
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detection/', views.detection, name ='detection'),
    path('detected/', views.detected, name ='detected')
]