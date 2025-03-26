from django.contrib import admin
from .models import Tasks
# Register your models here.


class TasksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']
    search_fields = ['title']
    # list_filter = ['is_completed']


admin.site.register(Tasks, TasksAdmin)