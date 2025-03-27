from django.contrib import admin

from players.models import Player, Team


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team')
    list_filter = ('team',)
    search_fields = ('name',)

@admin.register(Team)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)