from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Crop, Location, WeatherSnapshot, CropRecommendation


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class LocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


class WeatherSnapshotSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = WeatherSnapshot
        fields = '__all__'


class CropRecommendationSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = CropRecommendation
        fields = '__all__'
