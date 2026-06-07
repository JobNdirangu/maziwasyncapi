from django.shortcuts import render

# Create your views here.
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum

from core.serializers import FarmerSerializer, MilkCollectionSerializer, NoticeSerializer, PorterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets

from core.models import (FarmerProfile, Notice,PorterProfile,MilkCollection,Feedback)


class AdminDashboardView(APIView):

    # Only administrators can access cooperative analytics
    permission_classes = [IsAdminUser]

    def get(self, request):

        # Get today's date according to Django timezone settings
        # Used for daily, weekly and monthly calculations
        today = timezone.localdate()

        # Calculate the starting date of the last 7 days
        # Used for weekly statistics
        week_start = today - timedelta(days=7)

        # ==================================================
        # FARMERS & PORTERS STATISTICS
        # ==================================================

        # Total registered farmers in the cooperative
        total_farmers = FarmerProfile.objects.count()

        # Total registered milk collectors/porters
        total_porters = PorterProfile.objects.count()

        # ==================================================
        # MILK COLLECTION STATISTICS
        # ==================================================

        # Retrieve all milk collection records
        # Reusing this queryset avoids repeating queries
        collections = MilkCollection.objects.all()

        # Total liters collected since the system started
        total_liters = collections.aggregate(
            total=Sum('liters')
        )['total'] or 0

        # Total liters collected today only
        today_liters = collections.filter(
            collection_date=today
        ).aggregate(
            total=Sum('liters')
        )['total'] or 0

        # Total liters collected during the last 7 days
        weekly_liters = collections.filter(
            collection_date__gte=week_start
        ).aggregate(
            total=Sum('liters')
        )['total'] or 0

        # Total liters collected during the current month
        monthly_liters = collections.filter(
            collection_date__year=today.year,
            collection_date__month=today.month
        ).aggregate(
            total=Sum('liters')
        )['total'] or 0

        # ==================================================
        # REVENUE STATISTICS
        # ==================================================

        # Total money generated from all milk collections
        total_revenue = collections.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Revenue generated today
        today_revenue = collections.filter(
            collection_date=today
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Revenue generated in the last 7 days
        weekly_revenue = collections.filter(
            collection_date__gte=week_start
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # Revenue generated in the current month
        monthly_revenue = collections.filter(
            collection_date__year=today.year,
            collection_date__month=today.month
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        # ==================================================
        # FEEDBACK ANALYTICS
        # ==================================================

        # Number of complaints/feedback not yet resolved
        pending_feedback = Feedback.objects.filter(
            status='PENDING'
        ).count()

        # Number of complaints already resolved
        resolved_feedback = Feedback.objects.filter(
            status='RESOLVED'
        ).count()

        # ==================================================
        # TOP FARMERS
        # ==================================================

        # Retrieve farmers with highest milk delivery
        # Ordered descending (-)
        # Limit to top 5 farmers only
        top_farmers = FarmerProfile.objects.order_by(
            '-total_milk_delivered'
        )[:5]

        # Convert FarmerProfile objects into JSON
        # Response() cannot directly return Django model objects
        top_farmers_data = FarmerSerializer(
            top_farmers,
            many=True
        ).data

        # ==================================================
        # RECENT COLLECTIONS
        # ==================================================

        # Get latest 10 collection records

        # select_related() performs SQL JOINs
        # Prevents N+1 Query Problem when accessing
        # farmer and porter information

        recent_collections = MilkCollection.objects.select_related(
            'farmer',
            'porter'
        ).order_by('-created_at')[:10]

        # Convert collection objects into JSON
        recent_collections_data = MilkCollectionSerializer(
            recent_collections,
            many=True
        ).data

        # ==================================================
        # DASHBOARD RESPONSE
        # ==================================================

        # Send all analytics data to frontend
        # React dashboard will consume this endpoint
        return Response({

            # User statistics
            "farmers": total_farmers,
            "porters": total_porters,

            # Milk collection analytics
            "total_liters": total_liters,
            "today_liters": today_liters,
            "weekly_liters": weekly_liters,
            "monthly_liters": monthly_liters,

            # Financial analytics
            "total_revenue": total_revenue,
            "today_revenue": today_revenue,
            "weekly_revenue": weekly_revenue,
            "monthly_revenue": monthly_revenue,

            # Feedback analytics
            "pending_feedback": pending_feedback,
            "resolved_feedback": resolved_feedback,

            # Performance analytics
            "top_farmers": top_farmers_data,

            # Operational analytics
            "recent_collections": recent_collections_data
        })
    

class FarmerViewSet(viewsets.ModelViewSet):

    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAdminUser]


class PorterViewSet(viewsets.ModelViewSet):

    queryset = PorterProfile.objects.all()
    serializer_class = PorterSerializer
    permission_classes = [IsAdminUser]


class MilkCollectionViewSet(viewsets.ModelViewSet):

    queryset = MilkCollection.objects.select_related(
        'farmer',
        'porter'
    )

    serializer_class = MilkCollectionSerializer
    permission_classes = [IsAdminUser]


class NoticeViewSet(viewsets.ModelViewSet):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):

        serializer.save(
            created_by=self.request.user
        )