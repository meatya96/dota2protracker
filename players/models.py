from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50, verbose_name='Команда')
    team = models.CharField(max_length=50, verbose_name='Команда игрока')

    class Meta:
        verbose_name = 'Команда'
        ordering = ['name']

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ник игрока')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, verbose_name='Команда игрока', null=True, blank=True)

    class Meta:
        verbose_name = 'Игрок'
        ordering = ['team', 'name']

    def __str__(self):
        return self.name

