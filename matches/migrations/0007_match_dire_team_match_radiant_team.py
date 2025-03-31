# Generated by Django 5.1.7 on 2025-03-30 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0006_remove_match_dire_team_id_and_more'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='dire_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dire_matches', to='teams.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='radiant_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='radiant_matches', to='teams.team'),
        ),
    ]
