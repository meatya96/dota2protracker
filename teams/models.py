from django.db import models


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=10, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def get_effective_bans(self):
        from draft_timings.models import DraftTiming
        from django.db.models import Count

        # Самые эффективные баны против команды (чаще всего банились против них)
        return DraftTiming.objects.filter(
            is_pick=False,
            team=self
        ).values('hero__localized_name').annotate(
            ban_count=Count('hero')
        ).order_by('-ban_count')[:5]

    def get_top_heroes(self):
        from matches.models import Match
        from django.db.models import Count, Case, When, FloatField

        # Герои с самым высоким винрейтом у команды
        return Match.objects.filter(
            models.Q(radiant_team=self) | models.Q(dire_team=self)
        ).annotate(
            hero_side=Case(
                When(radiant_team=self, then='radiant'),
                When(dire_team=self, then='dire'),
                output_field=models.CharField()
            )
        ).values(
            'hero_side',
            'draft_timings__hero__localized_name'
        ).annotate(
            total=Count('draft_timings__hero'),
            wins=Count(
                Case(
                    When(
                        models.Q(radiant_win=True, hero_side='radiant') |
                        models.Q(radiant_win=False, hero_side='dire'),
                        then=1
                    ),
                    output_field=models.IntegerField()
                )
            ),
            win_rate=Case(
                When(total=0, then=0.0),
                default=100.0 * models.F('wins') / models.F('total'),
                output_field=FloatField()
            )
        ).order_by('-win_rate')[:5]

    def __str__(self):
        return self.name