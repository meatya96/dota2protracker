from django.shortcuts import render
from .models import League

def league_list(request):
    leagues = League.objects.all().order_by('-leagueid')
    return render(request, 'leagues/list.html', {'leagues': leagues})