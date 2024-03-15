from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cars  # import cars from models


# this in django will help us convert a sql query to json and vice versa
class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'  # This will automatically adapt to the fields in the Cars model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        # Use Django's User model manager to handle user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),  # Email is optional
            password=validated_data['password']
        )
        return user
