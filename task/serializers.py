from rest_framework import serializers
from .models import Tasks


class TasksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', 'status']


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['title', 'assigned_users', 'description', 'status', 'created_at', 'updated_at']
