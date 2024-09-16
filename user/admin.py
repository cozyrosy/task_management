from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email']
    search_fields = ['username', 'email']
    list_filter = ['is_active']


admin.site.register(UserProfile, UserProfileAdmin)