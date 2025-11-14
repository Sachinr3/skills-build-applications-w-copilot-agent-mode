from rest_framework import serializers
from .models import Team, TeamMembership
from users.serializers import UserSerializer

class TeamMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TeamMembership
        fields = ['id', 'user', 'joined_at', 'is_admin']
        read_only_fields = ['id', 'joined_at']

class TeamSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    memberships = TeamMembershipSerializer(source='teammembership_set', many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'creator', 'total_points', 
                  'members_count', 'memberships', 'created_at', 'updated_at']
        read_only_fields = ['id', 'creator', 'total_points', 'created_at', 'updated_at']
    
    def get_members_count(self, obj):
        return obj.members.count()
    
    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        team = super().create(validated_data)
        # Add creator as admin member
        TeamMembership.objects.create(
            team=team,
            user=team.creator,
            is_admin=True
        )
        return team

class JoinTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
