from django.contrib import admin
from .models import League

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('leagueid', 'name')
    search_fields = ('name', 'leagueid')
    list_per_page = 50
    ordering = ('leagueid',)