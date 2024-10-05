from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=200)
    due_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task
