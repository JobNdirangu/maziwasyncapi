from django.urls import path
from .views import AddMilkCollection, MyCollectionsView,PorterDashboardView

urlpatterns = [
    path('dashboard/',PorterDashboardView,name='porter-dashboard'),
    path('milk-collections/add/', AddMilkCollection, name='add_milk_collection'),
    path('collections/my/', MyCollectionsView.as_view(), name='my-collections'),

]