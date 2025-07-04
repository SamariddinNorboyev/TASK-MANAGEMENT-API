from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Team, TeamAdmin)