from django.contrib import admin
from .models import Match
from django.utils.html import format_html

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'league_info', 'teams_display', 'start_time', 'duration_formatted', 'patch')
    list_filter = ('league', 'patch', 'radiant_win')
    search_fields = ('match_id', 'radiant_team__name', 'dire_team__name')
    list_select_related = ('league', 'radiant_team', 'dire_team')
    list_per_page = 30

    @admin.display(description='League')
    def league_info(self, obj):
        return f"{obj.league.name} ({obj.league.leagueid})"

    @admin.display(description='Teams')
    def teams_display(self, obj):
        return format_html(
            '<span style="color: green;">{}</span> vs <span style="color: red;">{}</span>',
            obj.radiant_team.name if obj.radiant_team else '?',
            obj.dire_team.name if obj.dire_team else '?'
        )

    @admin.display(description='Duration')
    def duration_formatted(self, obj):
        minutes = obj.duration // 60
        seconds = obj.duration % 60
        return f"{minutes}:{seconds:02d}"