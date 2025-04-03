from django.urls import path
from . import views

app_name = 'leagues'

urlpatterns = [
    path('', views.league_list, name='list'),
]