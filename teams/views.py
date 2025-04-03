from django.shortcuts import render, get_object_or_404
from .models import Team


def team_list(request):
    teams = Team.objects.all().order_by('-wins')
    return render(request, 'teams/list.html', {'teams': teams})


def team_detail(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)

    # Получаем статистику по команде
    effective_bans = team.get_effective_bans()
    top_heroes = team.get_top_heroes()

    return render(request, 'teams/detail.html', {
        'team': team,
        'effective_bans': effective_bans,
        'top_heroes': top_heroes,
    })