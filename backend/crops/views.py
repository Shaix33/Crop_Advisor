from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Crop, Location, CropRecommendation
from .serializers import (
    CropSerializer,
    LocationSerializer,
    LocationWriteSerializer,
    CropRecommendationReadSerializer,
    CropRecommendationWriteSerializer
)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return LocationWriteSerializer
        return LocationSerializer

    def perform_create(self, serializer):
        # Tie the location to the logged-in user
        serializer.save(user=self.request.user)


class CropRecommendationViewSet(viewsets.ModelViewSet):
    queryset = CropRecommendation.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CropRecommendationWriteSerializer
        return CropRecommendationReadSerializer

    @action(detail=False, methods=["post"])
    def recommend(self, request):
        """
        Custom action to suggest crops based on weather & soil data.
        Input: { location_id, temp, rainfall, soil_type }
        """
        location_id = request.data.get("location")
        temp = request.data.get("temp")
        rainfall = request.data.get("rainfall")
        soil_type = request.data.get("soil_type")

        if not location_id or temp is None or rainfall is None or not soil_type:
            return Response(
                {"error": "location, temp, rainfall, and soil_type are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        location = get_object_or_404(Location, id=location_id, user=request.user)

        # Filter crops that fit the input conditions
        crops = Crop.objects.filter(
            optimal_temp_min__lte=temp,
            optimal_temp_max__gte=temp,
            optimal_rainfall_min__lte=rainfall,
            optimal_rainfall_max__gte=rainfall,
            soil_type=soil_type
        )

        recommendations = []
        for crop in crops:
            # Example: basic suitability score (can be improved with real algorithm)
            temp_score = 1 - abs((temp - ((crop.optimal_temp_min + crop.optimal_temp_max) / 2)) / 10)
            rain_score = 1 - abs((rainfall - ((crop.optimal_rainfall_min + crop.optimal_rainfall_max) / 2)) / 50)
            suitability_score = round((temp_score + rain_score) / 2, 2)

            rec = CropRecommendation.objects.create(
                location=location,
                crop=crop,
                suitability_score=suitability_score,
                reason=f"Matches temp {temp}°C and rainfall {rainfall}mm for {soil_type} soil"
            )
            recommendations.append(rec)

        serializer = CropRecommendationReadSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
