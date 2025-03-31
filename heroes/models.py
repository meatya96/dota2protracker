from django.db import models

class Hero(models.Model):
    id = models.IntegerField(
        primary_key=True,
        verbose_name='ID героя'
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Техническое название',
        help_text='Имя героя для API (например: "npc_dota_hero_antimage")'
    )
    localized_name = models.CharField(
        max_length=50,
        verbose_name='Локализованное имя',
        help_text='Имя героя для отображения (например: "Anti-Mage")'
    )

    class Meta:
        verbose_name = 'Герой'
        verbose_name_plural = 'Герои'
        ordering = ['localized_name']

    def __str__(self):
        return self.localized_name