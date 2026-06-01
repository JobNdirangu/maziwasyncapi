from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.exceptions import PermissionDenied


from core.models import (MilkCollection,Feedback)

from core.serializers import (MilkCollectionSerializer,FeedbackSerializer)


# ============================================================
# FARMER DASHBOARD
# ============================================================

class FarmerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        farmer = request.user.farmer_profile

        collections = MilkCollection.objects.filter(
            farmer=farmer
        )

        total_collections = collections.count()

        total_liters = collections.aggregate(
            total=Sum('liters')
        )['total'] or 0

        total_amount = collections.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        return Response({
            "total_collections": total_collections,
            "total_liters": total_liters,
            "total_amount": total_amount,
        })


# ============================================================
# FARMER COLLECTIONS
# ============================================================

class FarmerCollectionsView(ListAPIView):
    serializer_class = MilkCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        farmer = self.request.user.farmer_profile

        collections = (
            MilkCollection.objects
            .filter(farmer=farmer)
            .select_related('porter')
            .order_by('-created_at')
        )

        return collections


# ============================================================
# FEEDBACK CRUD
# ============================================================

class FeedbackViewSet(ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        try:
            farmer = self.request.user.farmer_profile
        except:
            raise PermissionDenied(
                "Only farmers can access this endpoint."
            )

        feedbacks = Feedback.objects.filter(
            farmer=farmer
        ).order_by('-created_at')

        return feedbacks

    def perform_create(self, serializer):

        farmer = self.request.user.farmer_profile

        serializer.save(
            farmer=farmer
        )