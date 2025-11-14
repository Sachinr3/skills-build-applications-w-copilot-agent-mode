from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('strength_training', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(null=True, blank=True, help_text="Distance in km")
    calories_burned = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

    def save(self, *args, **kwargs):
        # Calculate points based on activity type and duration
        if not self.points_earned:
            self.points_earned = self.calculate_points()
        super().save(*args, **kwargs)

    def calculate_points(self):
        # Basic point calculation: 1 point per minute with type multipliers
        multipliers = {
            'running': 2.0,
            'walking': 1.0,
            'cycling': 1.5,
            'swimming': 2.5,
            'strength_training': 2.0,
            'yoga': 1.5,
            'sports': 2.0,
            'other': 1.0,
        }
        return int(self.duration * multipliers.get(self.activity_type, 1.0))
