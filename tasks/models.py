from django.db import models
from accounts.models import MyUser
from teams.models import Team

class Task(models.Model):    
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        INPROGRESS = "INPROGRESS", "In Progress"
        INREVIEW = "INREVIEW", "In Review"
        DONE = "DONE", "Done"

    name = models.CharField(max_length=255)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TODO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
