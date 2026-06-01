from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerDashboardView, FarmerCollectionsView, FeedbackViewSet

router = DefaultRouter()
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('dashboard/', FarmerDashboardView.as_view(), name='farmer-dashboard'),
    path('collections/', FarmerCollectionsView.as_view(), name='farmer-collections'),
    path('', include(router.urls)),
]
