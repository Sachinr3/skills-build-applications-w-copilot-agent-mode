from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Team, TeamMembership
from .serializers import TeamSerializer, JoinTeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Show all teams for listing, but filter for user's teams with action
        if self.action == 'my_teams':
            return Team.objects.filter(members=self.request.user)
        return Team.objects.all()

    @action(detail=False, methods=['get'])
    def my_teams(self, request):
        teams = Team.objects.filter(members=request.user)
        serializer = self.get_serializer(teams, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        team = self.get_object()
        
        # Check if already a member
        if TeamMembership.objects.filter(team=team, user=request.user).exists():
            return Response(
                {'message': 'You are already a member of this team'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add user to team
        TeamMembership.objects.create(team=team, user=request.user)
        
        return Response({
            'message': f'Successfully joined {team.name}',
            'team': TeamSerializer(team).data
        })

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        team = self.get_object()
        
        try:
            membership = TeamMembership.objects.get(team=team, user=request.user)
            
            # Prevent creator from leaving
            if team.creator == request.user:
                return Response(
                    {'message': 'Team creator cannot leave the team'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            membership.delete()
            return Response({'message': f'Successfully left {team.name}'})
            
        except TeamMembership.DoesNotExist:
            return Response(
                {'message': 'You are not a member of this team'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def update_points(self, request, pk=None):
        team = self.get_object()
        team.update_total_points()
        return Response({
            'message': 'Team points updated',
            'total_points': team.total_points
        })
