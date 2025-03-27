from django.db import models

class League(models.Model):
    name = models.CharField(max_length=50, verbose_name='Лига')
    league_id = models.CharField(max_length=50, verbose_name='Айди Лиги')

    class Meta:
        verbose_name = 'Лига'
        ordering = ['name']

    def __str__(self):
        return self.name