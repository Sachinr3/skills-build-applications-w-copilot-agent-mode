from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from users.models import UserProfile
from teams.models import Team
from activities.models import Activity
from .serializers import LeaderboardSerializer, TeamLeaderboardSerializer

class LeaderboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def users(self, request):
        """Get user leaderboard based on total points"""
        limit = int(request.query_params.get('limit', 10))
        
        profiles = UserProfile.objects.select_related('user').order_by('-total_points')[:limit]
        
        leaderboard_data = []
        for rank, profile in enumerate(profiles, start=1):
            activity_count = Activity.objects.filter(user=profile.user).count()
            leaderboard_data.append({
                'rank': rank,
                'username': profile.user.username,
                'total_points': profile.total_points,
                'activity_count': activity_count
            })
        
        serializer = LeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def teams(self, request):
        """Get team leaderboard based on total points"""
        limit = int(request.query_params.get('limit', 10))
        
        teams = Team.objects.annotate(
            member_count=Count('members')
        ).order_by('-total_points')[:limit]
        
        leaderboard_data = []
        for rank, team in enumerate(teams, start=1):
            leaderboard_data.append({
                'rank': rank,
                'team_name': team.name,
                'total_points': team.total_points,
                'member_count': team.member_count
            })
        
        serializer = TeamLeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_rank(self, request):
        """Get current user's rank"""
        user_profile = UserProfile.objects.get(user=request.user)
        higher_ranked = UserProfile.objects.filter(
            total_points__gt=user_profile.total_points
        ).count()
        
        return Response({
            'rank': higher_ranked + 1,
            'username': request.user.username,
            'total_points': user_profile.total_points
        })
