# Generated by Django 5.1.7 on 2025-03-30 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_alter_match_patch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='dire_team',
        ),
        migrations.RemoveField(
            model_name='match',
            name='radiant_team',
        ),
        migrations.AddField(
            model_name='match',
            name='dire_team_id',
            field=models.IntegerField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='radiant_team_id',
            field=models.IntegerField(blank=True, max_length=255, null=True),
        ),
    ]
