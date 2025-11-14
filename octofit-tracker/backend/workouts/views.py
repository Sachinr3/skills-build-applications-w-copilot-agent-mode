from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import WorkoutSuggestion, UserWorkout
from .serializers import WorkoutSuggestionSerializer, UserWorkoutSerializer
from users.models import UserProfile

class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = WorkoutSuggestion.objects.all()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by activity type
        activity_type = self.request.query_params.get('activity_type', None)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        return queryset

    @action(detail=False, methods=['get'])
    def personalized(self, request):
        """Get workout suggestions based on user's fitness level"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            suggestions = WorkoutSuggestion.objects.filter(difficulty=profile.fitness_level)
            serializer = self.get_serializer(suggestions, many=True)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'message': 'Please complete your profile first'},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserWorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = UserWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserWorkout.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        user_workout = self.get_object()
        user_workout.completed = True
        user_workout.completed_at = timezone.now()
        user_workout.save()
        
        serializer = self.get_serializer(user_workout)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        user_workout = self.get_object()
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response(
                {'message': 'Rating must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_workout.rating = rating
        user_workout.feedback = feedback
        user_workout.save()
        
        serializer = self.get_serializer(user_workout)
        return Response(serializer.data)
