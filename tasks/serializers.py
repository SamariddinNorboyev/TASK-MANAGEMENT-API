from rest_framework import serializers
from .models import Task
from accounts.models import MyUser
from django.shortcuts import get_object_or_404
from teams.models import Team

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'team', 'created_by', 'assigned_to', 'status', 'created_at', 'updated_at',]
        read_only_fields = ['id', 'created_at', 'updated_at',]

class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_by', 'team', 'assigned_to', 'status',]
        extra_kwargs = {'created_by': {'read_only': True}}

    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        team = attrs.get('team')
        assigned_to = attrs.get('assigned_to')
        
        if team:
            if not user or user != team.owner:
                raise serializers.ValidationError("You are not the owner of this team. Please select another team.")

            if assigned_to and assigned_to not in team.members.all():
                raise serializers.ValidationError("Assigned user is not a member of this team.")
            
        if not team and assigned_to:
            raise serializers.ValidationError("It is not allowed to assign task to the user if there is not a team!")
        
        return attrs

class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_by','team', 'assigned_to', 'status',]
        extra_kwargs = {'created_by': {'read_only': True}}


    def validate(self, attrs):
        request = self.context['request']
        user = request.user

        team = attrs.get('team')
        assigned_to = attrs.get('assigned_to')

        if not self.instance.team and assigned_to:
            raise serializers.ValidationError("It is not allowed to assign task to the user if there is not a team!")
        
        if team:
            if not user or user != team.owner:
                raise serializers.ValidationError("You are not the owner of this team. Please select another team.")

            if assigned_to and assigned_to not in team.members.all():
                raise serializers.ValidationError("Assigned user is not a member of this team.")
        
        return attrs