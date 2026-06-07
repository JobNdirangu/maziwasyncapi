from core.serializers import MilkCollectionSerializer, NoticeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView


from django.utils import timezone
from django.db.models import Sum

from core.models import FarmerProfile, Notice, PorterProfile, MilkCollection


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def PorterDashboardView(request):

    try:
        porter = request.user.porter_profile
    except:
        return Response(
            {"error": "Only porters can access this dashboard."},
            status=403
        )

    today = timezone.now().date()

    collections = MilkCollection.objects.filter(
        porter=porter,
        collection_date=today
    )

    total_liters = collections.aggregate(
        total=Sum('liters')
    )['total'] or 0

    total_amount = collections.aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_collections = collections.count()

    assigned_farmers = porter.assigned_farmers.count()

    return Response({
        "date": today,
        "assigned_farmers": assigned_farmers,
        "total_collections_today": total_collections,
        "total_liters_today": total_liters,
        "total_amount_today": total_amount
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddMilkCollection(request):

    # Get logged-in porter
    try:
        porter = request.user.porter_profile
    except PorterProfile.DoesNotExist:
        return Response(
            {"error": "Only porters can add milk collections."},
            status=status.HTTP_403_FORBIDDEN
        )

    farmer_code = request.data.get('farmer_code')

    try:
        farmer = FarmerProfile.objects.get(
            membership_number=farmer_code
        )
    except FarmerProfile.DoesNotExist:
        return Response(
            {"error": "Farmer not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    collection = MilkCollection.objects.create(
        farmer=farmer,
        porter=porter,
        liters=request.data.get('liters'),
        session=request.data.get('session')
    )

    return Response({
        "message": "Milk collection recorded successfully.",
        "collection_id": collection.id,
        "farmer": f"{farmer.first_name} {farmer.last_name}",
        "porter": f"{porter.first_name} {porter.last_name}",
        "liters": collection.liters
    }, status=status.HTTP_201_CREATED)




class MyCollectionsView(generics.ListAPIView):
    serializer_class = MilkCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        porter = self.request.user.porter_profile

        collections = (
            MilkCollection.objects
            .filter(porter=porter)
            .select_related('farmer')
            .order_by('-created_at')
        )

        return collections
    

class PorterNoticeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        notices = Notice.objects.filter(
            target__in=['ALL', 'PORTERS']
        ).order_by('-created_at')

        serializer = NoticeSerializer(notices, many=True)

        return Response(serializer.data)