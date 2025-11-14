from rest_framework import serializers
from .models import WorkoutSuggestion, UserWorkout

class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSuggestion
        fields = ['id', 'title', 'description', 'activity_type', 'difficulty', 
                  'duration', 'instructions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserWorkoutSerializer(serializers.ModelSerializer):
    suggestion = WorkoutSuggestionSerializer(read_only=True)
    suggestion_id = serializers.IntegerField(write_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserWorkout
        fields = ['id', 'user', 'username', 'suggestion', 'suggestion_id', 
                  'completed', 'completed_at', 'rating', 'feedback', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        suggestion_id = validated_data.pop('suggestion_id')
        validated_data['suggestion_id'] = suggestion_id
        return super().create(validated_data)
