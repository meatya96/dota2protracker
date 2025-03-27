# Generated by Django 5.1.7 on 2025-03-27 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Лига')),
                ('league_id', models.CharField(max_length=50, verbose_name='Айди Лиги')),
            ],
            options={
                'verbose_name': 'Лига',
                'ordering': ['name'],
            },
        ),
    ]
