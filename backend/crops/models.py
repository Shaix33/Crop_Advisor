from django.db import models
from django.contrib.auth.models import User

class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=100, blank=True)
    planting_season = models.CharField(max_length=50)
    growth_period_days = models.IntegerField()
    optimal_temp_min = models.FloatField()
    optimal_temp_max = models.FloatField()
    optimal_rainfall_min = models.FloatField()
    optimal_rainfall_max = models.FloatField()
    soil_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    LOCATION_SOURCE_CHOICES = [
        ("GPS", "GPS"),
        ("IP", "IP-based"),
        ("CITY", "Manual City Input"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=100)  # e.g. "Cape Town Farm"
    country = models.CharField(max_length=100, blank=True, help_text="Country where the location is.")
    latitude = models.FloatField()
    longitude = models.FloatField()
    source = models.CharField(max_length=10, choices=LOCATION_SOURCE_CHOICES, default="CITY")

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class WeatherSnapshot(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="weather_snapshots")
    date = models.DateField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    rainfall = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather on {self.date} for {self.location.name}"


class CropRecommendation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="recommendations")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    suitability_score = models.FloatField()
    reason = models.TextField(blank=True)  # explain why this crop was chosen
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop.name} for {self.location.name} ({self.suitability_score:.1f})"