from django.db import models
from accounts.models import MyUser

class Team(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(MyUser, related_name='teams')

    def __str__(self):
        return self.name
