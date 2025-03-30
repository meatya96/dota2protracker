from django.db import models
from leagues.models import League


class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    start_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Длительность матча в секундах")
    radiant_win = models.BooleanField()
    radiant_team_id = models.IntegerField(null=True, blank=True)
    dire_team_id = models.IntegerField(null=True, blank=True)
    patch = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Match {self.match_id} ({self.league.name})"