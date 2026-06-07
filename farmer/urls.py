from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerDashboardView, FarmerCollectionsView, FarmerNoticeView, FeedbackViewSet

router = DefaultRouter()
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('dashboard/', FarmerDashboardView.as_view(), name='farmer-dashboard'),
    path('collections/', FarmerCollectionsView.as_view(), name='farmer-collections'),
    path('notices/', FarmerNoticeView.as_view(), name='farmer-notices'),

    path('', include(router.urls)),
]
