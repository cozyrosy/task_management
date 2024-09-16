from django.contrib import admin
from django.urls import path, include
from user.models import TaskListView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='user-tasks'),
    path('tasks/', TaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
]