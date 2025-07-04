from django.contrib import admin
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from .models import MyUser



class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']  # Add any fields you want

admin.site.register(MyUser, UserAdmin)