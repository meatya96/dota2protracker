from django.shortcuts import render, get_object_or_404
from .models import Match

def match_list(request):
    matches = Match.objects.select_related('league').all()
    return render(request, 'matches/list.html', {'matches': matches})

def match_detail(request, match_id):
    match = get_object_or_404(Match.objects.select_related('league'), match_id=match_id)
    return render(request, 'matches/detail.html', {'match': match})