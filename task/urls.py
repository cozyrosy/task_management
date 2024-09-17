from django.contrib import admin
from django.urls import path, include
from .views import TaskListView, TaskDetailView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='user-tasks'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('create_task/', TaskDetailView.as_view(), name='create-task'),
    path('update_task/<int:task_id>/', TaskDetailView.as_view(), name='update-task'),
    path('delete_task/<int:task_id>/', TaskDetailView.as_view(), name='delete-task')
]