from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models

class WorkoutSuggestion(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=30)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.IntegerField(help_text="Suggested duration in minutes")
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workout_suggestions'
        ordering = ['difficulty', 'activity_type']

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_workouts')
    suggestion = models.ForeignKey(WorkoutSuggestion, on_delete=models.CASCADE, related_name='user_workouts')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, help_text="Rating from 1-5")
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_workouts'
        ordering = ['-created_at']

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.user.username} - {self.suggestion.title} ({status})"
