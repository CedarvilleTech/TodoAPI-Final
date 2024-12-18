from rest_framework import serializers
from . import models

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Todo
        fields = ["id", "task", "completed", "user", "created", "updated"]
