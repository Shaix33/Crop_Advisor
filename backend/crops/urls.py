from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CropViewSet, LocationViewSet, CropRecommendationViewSet

router = DefaultRouter()
router.register('crops', CropViewSet)
router.register('locations', LocationViewSet)
router.register('recommendations', CropRecommendationViewSet, basename='recommendations')

urlpatterns = [
    path('', include(router.urls)),
]
