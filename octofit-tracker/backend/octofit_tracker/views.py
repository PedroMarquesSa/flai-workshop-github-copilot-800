from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user._id))
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        members = User.objects.filter(team_id=str(team._id))
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get leaderboard for a specific team"""
        team = self.get_object()
        leaderboard = Leaderboard.objects.filter(team_id=str(team._id)).order_by('rank')
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned activities to a given user,
        by filtering against a `user_id` query parameter in the URL.
        """
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-date')


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing leaderboard
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    def get_queryset(self):
        """
        Get leaderboard ordered by rank
        """
        return Leaderboard.objects.all().order_by('rank')
    
    @action(detail=False, methods=['get'])
    def top_ten(self, request):
        """Get top 10 users on the leaderboard"""
        top_users = Leaderboard.objects.all().order_by('rank')[:10]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned workouts by activity type or difficulty,
        by filtering against query parameters in the URL.
        """
        queryset = Workout.objects.all()
        activity_type = self.request.query_params.get('activity_type', None)
        difficulty = self.request.query_params.get('difficulty', None)
        
        if activity_type is not None:
            queryset = queryset.filter(activity_type=activity_type)
        if difficulty is not None:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts grouped by difficulty level"""
        difficulty = request.query_params.get('level', 'beginner')
        workouts = Workout.objects.filter(difficulty_level=difficulty)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
