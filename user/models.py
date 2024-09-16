from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# from tasks.manager import UserManager    


# Create your models here.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_group',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = UserManager()

    class Meta:
        verbose_name = "User Information"
        verbose_name_plural = verbose_name
    
    def __unicode__(self):
        return self.username

    def __str__(self):
        return self.username


