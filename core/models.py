from django.db import models
from django.contrib.auth.models import User, AbstractUser, UserManager, PermissionsMixin
from django.forms import ModelForm
from django.utils import timezone
from django import forms

import datetime
# Create your models here.

# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("You haven ot provided a valid e-mail address")
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)

#         return user
    
#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
    
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self._create_user(email, password, **extra_fields)


# class CustomUser(AbstractUser, PermissionsMixin):
#     email = models.EmailField(blank=True, default='', unique=True)

#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)

#     objects = CustomUserManager()

#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user_date = models.DateTimeField()
    def __str__(self):
        return self.title


class TaskStep(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    step = models.TextField(max_length=50)

    def __str__(self):
        return '%s' % (self.step)
    
        