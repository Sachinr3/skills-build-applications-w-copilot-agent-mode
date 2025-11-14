"""octofit_tracker URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os

from users.views import UserViewSet, UserProfileViewSet
from activities.views import ActivityViewSet
from teams.views import TeamViewSet
from leaderboard.views import LeaderboardViewSet
from workouts.views import WorkoutSuggestionViewSet, UserWorkoutViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workout-suggestions', WorkoutSuggestionViewSet, basename='workout-suggestion')
router.register(r'user-workouts', UserWorkoutViewSet, basename='user-workout')

@api_view(['GET'])
def api_root(request):
    """API root view showing available endpoints"""
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = "http://localhost:8000"
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'endpoints': {
            'users': f'{base_url}/api/users/',
            'profiles': f'{base_url}/api/profiles/',
            'activities': f'{base_url}/api/activities/',
            'teams': f'{base_url}/api/teams/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'workout_suggestions': f'{base_url}/api/workout-suggestions/',
            'user_workouts': f'{base_url}/api/user-workouts/',
            'auth': {
                'login': f'{base_url}/api/auth/login/',
                'logout': f'{base_url}/api/auth/logout/',
                'register': f'{base_url}/api/users/register/',
            }
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
