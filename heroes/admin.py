from django.contrib import admin
from .models import Hero

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('id', 'localized_name', 'name')
    search_fields = ('localized_name', 'name')
    ordering = ('id',)