from django.contrib import admin

from .models import Task, TaskStep #,CustomUser
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskStep)
# admin.site.register(CustomUser)