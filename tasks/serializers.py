from rest_framework import serializers
from .models import Task
from accounts.models import MyUser
from django.shortcuts import get_object_or_404

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'team', 'assigned_to', 'status', 'created_at', 'updated_at',]
        read_only_fields = ['id', 'created_at', 'updated_at',]

class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'team', 'assigned_to', 'status',]

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'assigned_to', 'status',]

class AssignSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    user_id = serializers.IntegerField()