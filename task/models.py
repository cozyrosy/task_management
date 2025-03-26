from django.db import models
from datetime import datetime
from user.models import UserProfile
# Create your models here.

class Tasks(models.Model):
    TASK_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    TASK_TYPE_CHOICES = [
        ("bug", "Bug"),
        ("feature", "Feature"),
        ("improvement", "Improvement"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_users = models.ManyToManyField(UserProfile, related_name="tasks")  # Many-to-Many relation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES, default="feature")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.title
