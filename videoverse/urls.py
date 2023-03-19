from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='Main'),
    path('s', views.video_search, name='video_search'),
    path('watch', views.watch, name='watch'),
]