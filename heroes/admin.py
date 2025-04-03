# heroes/admin.py
from django.contrib import admin
from .models import Hero

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'localized_name', 'name')
    search_fields = ('localized_name', 'name')
    list_display_links = ('localized_name',)
    ordering = ('id',)
    list_per_page = 100