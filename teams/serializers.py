from rest_framework import serializers
from .models import Team
from accounts.models import MyUser
from django.shortcuts import get_object_or_404

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

class CreateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

    def validate(self, attrs):
        members = attrs.get('members') or []
        if len(members) > 15:
            raise serializers.ValidationError("No more than 15 users!")

        owner = attrs.get('owner')
        if Team.objects.filter(owner=owner).count() >= 3:
            raise serializers.ValidationError("You are not allowed to create more than 3 teams!")

        return attrs

class UpdateTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members']

    def validate(self, attrs):
        members = attrs.get('members') or []
        if len(members) > 15:
            raise serializers.ValidationError("No more than 15 users!")

        return attrs
    

class AddOrRemoveMemberSerializer(serializers.Serializer):
    user = serializers.IntegerField()

    def validate(self, attrs):
        user_id = attrs.get('user')
        try:
            user = MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError({'user': 'Invalid user ID'})
        attrs['user_instance'] = user
        return attrs
    
