# teams/models.py
from django.db import models


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, help_text="ID команды из OpenDota API")
    name = models.CharField(max_length=255, db_index=True)
    tag = models.CharField(max_length=10, blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    last_match_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['-rating']

    def __str__(self):
        return f"{self.name} ({self.tag})" if self.tag else self.name