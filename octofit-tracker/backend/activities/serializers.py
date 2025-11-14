from rest_framework import serializers
from .models import Activity
from django.contrib.auth.models import User

class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user', 'username', 'activity_type', 'duration', 'distance', 
                  'calories_burned', 'points_earned', 'notes', 'date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'points_earned', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # User will be set from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
