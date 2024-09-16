from django.db import models
from datetime import datetime
from user.models import UserProfile
# Create your models here.

class Tasks(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=150, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
