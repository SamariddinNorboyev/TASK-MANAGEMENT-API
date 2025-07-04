from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'assigned_to', 'created_by']  # Add any fields you want

admin.site.register(Task, TaskAdmin)
