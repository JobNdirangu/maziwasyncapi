from django.urls import include, path

from cooperative.views import AdminDashboardView, FarmerViewSet, MilkCollectionViewSet, NoticeViewSet, PorterViewSet,PaymentViewSet ,farmers_with_balance, mpesa_callback, pay_farmer
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register( r'farmers',FarmerViewSet)
router.register( r'porters',PorterViewSet)
router.register( r'collections', MilkCollectionViewSet )
router.register( r'notices', NoticeViewSet)
router.register( r'payment', PaymentViewSet)


urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='farmer-dashboard'),
    # path('payments', PaymentTest),
    path('dashboard/', AdminDashboardView.as_view()),
    path('farmers/balance/', farmers_with_balance),
    path('payfarmer/', pay_farmer),
    path('callback', mpesa_callback),

    path('', include(router.urls)),
]