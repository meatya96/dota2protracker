from django.contrib import admin
from .models import DraftTiming
from django.utils.html import format_html

@admin.register(DraftTiming)
class DraftTimingAdmin(admin.ModelAdmin):
    list_display = ('match', 'hero_display', 'action_type', 'team_display', 'stage')
    list_filter = ('stage', 'is_pick')
    search_fields = ('match__match_id', 'hero__localized_name', 'team__name')
    list_select_related = ('match', 'hero', 'team')
    list_per_page = 50

    @admin.display(description='Hero')
    def hero_display(self, obj):
        return obj.hero.localized_name if obj.hero else '?'

    @admin.display(description='Action')
    def action_type(self, obj):
        return 'Pick' if obj.is_pick else 'Ban'

    @admin.display(description='Team')
    def team_display(self, obj):
        if not obj.team:
            return '?'
        team = obj.team
        color = 'green' if team.team_id == obj.match.radiant_team_id else 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            team.name
        )