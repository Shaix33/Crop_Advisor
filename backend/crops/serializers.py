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

# Serializer for reading data
class LocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Location
        fields = '__all__'

# Serializer for writing data
class LocationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude']
    
        def create(self, validated_data):
            # Automatically set the user to the logged-in user
            user = self.context['request'].user
            return Location.objects.create(user=user, **validated_data)

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

class CropRecommendationReadSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)  # Include crop details
    location = LocationSerializer(read_only=True)  # Include location details

    class Meta:
        model = CropRecommendation
        fields = '__all__'

class CropRecommendationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropRecommendation
        fields = ['crop', 'location', 'recommendation']  

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        # Create user with hashed password
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
