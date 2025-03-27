from django.contrib import admin

from leagues.models import League


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('league_id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
