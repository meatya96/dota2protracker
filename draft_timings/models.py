from django.db import models
from matches.models import Match
from teams.models import Team
from heroes.models import Hero

class DraftTiming(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='draft_timings',
        verbose_name='Матч'
    )
    hero = models.ForeignKey(
        Hero,
        on_delete=models.CASCADE,
        verbose_name='Герой'
    )
    is_pick = models.BooleanField(
        verbose_name='Тип действия',
        help_text='True - пик, False - бан'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Команда',
        help_text='Команда, совершившая действие'
    )
    order = models.IntegerField(
        verbose_name='Порядковый номер действия'
    )
    stage = models.CharField(
        max_length=20,
        verbose_name='Стадия драфта',
        choices=[
            ('ban_1-7', 'Первый этап банов(1-7)'),
            ('first_pick', 'Первый пик'),
            ('second_pick', 'Второй пик'),
            ('ban_10-12', 'Второй этап банов(10-12)'),
            ('pick_13-18', 'Второй этап пиков(13-18)'),
            ('ban_19-22', 'Третий этап банов(19-22)'),
            ('pick_23', '23 пик'),
            ('pick_24', 'Ластпик')
        ]
    )

    class Meta:
        verbose_name = 'Действие драфта'
        verbose_name_plural = 'Тайминг драфта'
        ordering = ['match', 'order']
        unique_together = [['match', 'order']]

    def __str__(self):
        action = 'Пик' if self.is_pick else 'Бан'
        return f"{self.match_id} - {action} {self.hero} ({self.stage})"

    @property
    def active_team_side(self):
        """Возвращает сторону команды (Radiant/Dire)"""
        return 'Radiant' if self.team_id == self.match.radiant_team_id else 'Dire'