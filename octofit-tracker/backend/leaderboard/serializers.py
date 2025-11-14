from rest_framework import serializers

class LeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    total_points = serializers.IntegerField()
    activity_count = serializers.IntegerField()

class TeamLeaderboardSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    team_name = serializers.CharField()
    total_points = serializers.IntegerField()
    member_count = serializers.IntegerField()
