from django.contrib import admin

from leagues.models import League


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('leagueid', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)
