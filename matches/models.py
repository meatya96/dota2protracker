from django.db import models
from leagues.models import League
from teams.models import Team

class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Длительность матча в секундах")
    radiant_win = models.BooleanField()
    radiant_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='radiant_matches')
    dire_team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dire_matches'
    )
    patch = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Match {self.match_id} ({self.league.name})"