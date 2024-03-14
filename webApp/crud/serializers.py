from rest_framework import serializers
from .models import Cars  # import cars from models


# this in django will help us convert a sql query to json and vice versa
class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = '__all__'  # This will automatically adapt to the fields in the Cars model
