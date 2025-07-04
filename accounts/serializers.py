from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    refresh = serializers.CharField(read_only = True)
    access = serializers.CharField(read_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Username and password are required.')

        user = authenticate(username=username, password=password)
        print(user)

        if user:
            data['user'] = user

            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            return data
        else:
            raise serializers.ValidationError('Username or password is incorrect.')
        



class RegisterSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only = True)
    access = serializers.CharField(read_only = True)

    class Meta:
        model = MyUser
        fields = ['username', 'password', 'access', 'refresh']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            'username': user.username,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    


