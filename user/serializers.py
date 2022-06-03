from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BluePrint(serializers.ModelSerializer):

	class Meta:
		abstract = True
		model = User
		fields = ('id', 'name', 'cover')


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(
		write_only=True,
		required=True,
		style={'input_type': 'password', 'placeholder': 'Password'}
	)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username',
				  'password',)


class SnippetUserSerializer(BluePrint):
	pass


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user': SnippetUserSerializer(self.user).data})
        return data