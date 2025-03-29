from django.db import models


class League(models.Model):
    leagueid = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name