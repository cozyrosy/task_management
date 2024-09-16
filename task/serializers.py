from rest_framework import serializers
from .models import Tasks


class TasksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at']

        