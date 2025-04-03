from django.shortcuts import render
from .models import Hero

def hero_list(request):
    heroes = Hero.objects.all().order_by('localized_name')
    return render(request, 'heroes/list.html', {'heroes': heroes})