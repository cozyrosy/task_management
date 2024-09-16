from rest_framework import serializers
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password']
    
    def create(self, validated_data):
        user = UserProfile(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['email', 'password']