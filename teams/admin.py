from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'name', 'tag', 'wins', 'losses', 'win_rate_display')
    list_filter = ('tag',)
    search_fields = ('name', 'tag', 'team_id')
    readonly_fields = ('win_rate_display',)
    list_per_page = 50

    @admin.display(description='Win Rate')
    def win_rate_display(self, obj):
        return f"{obj.win_rate}%"