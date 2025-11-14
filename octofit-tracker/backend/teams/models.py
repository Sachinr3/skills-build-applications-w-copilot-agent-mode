from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', through='TeamMembership')
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        ordering = ['-total_points']

    def __str__(self):
        return self.name

    def update_total_points(self):
        # Update team points based on all members' activities
        from activities.models import Activity
        total = sum(
            Activity.objects.filter(user__in=self.members.all()).values_list('points_earned', flat=True)
        )
        self.total_points = total
        self.save()

class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = 'team_memberships'
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"
