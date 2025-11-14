from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Activity
from .serializers import ActivitySerializer
from users.models import UserProfile

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset

    def perform_create(self, serializer):
        activity = serializer.save(user=self.request.user)
        # Update user's total points
        profile = UserProfile.objects.get(user=self.request.user)
        profile.total_points += activity.points_earned
        profile.save()

    @action(detail=False, methods=['get'])
    def stats(self, request):
        activities = self.get_queryset()
        total_activities = activities.count()
        total_duration = sum(a.duration for a in activities)
        total_points = sum(a.points_earned for a in activities)
        
        return Response({
            'total_activities': total_activities,
            'total_duration': total_duration,
            'total_points': total_points,
            'by_type': self._get_activity_breakdown(activities)
        })

    def _get_activity_breakdown(self, activities):
        breakdown = {}
        for activity in activities:
            if activity.activity_type not in breakdown:
                breakdown[activity.activity_type] = {
                    'count': 0,
                    'duration': 0,
                    'points': 0
                }
            breakdown[activity.activity_type]['count'] += 1
            breakdown[activity.activity_type]['duration'] += activity.duration
            breakdown[activity.activity_type]['points'] += activity.points_earned
        return breakdown
