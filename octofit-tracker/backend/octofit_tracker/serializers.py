from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'team_id', 'team_name', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_team_name(self, obj):
        if obj.team_id:
            try:
                team = Team.objects.get(_id=ObjectId(obj.team_id))
                return team.name
            except Team.DoesNotExist:
                return None
        return None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']
    
    def get_id(self, obj):
        return str(obj._id)


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'user_name', 'activity_type', 'duration', 'distance', 'calories', 'date', 'notes']
    
    def get_id(self, obj):
        return str(obj._id)
    
    def get_user_name(self, obj):
        if obj.user_id:
            try:
                user = User.objects.get(_id=ObjectId(obj.user_id))
                return user.name
            except User.DoesNotExist:
                return None
        return None


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team_id', 'team_name', 'total_calories', 
                  'total_activities', 'total_duration', 'rank']
    
    def get_id(self, obj):
        return str(obj._id)


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'activity_type', 'difficulty_level', 
                  'duration', 'calories_estimate', 'instructions']
    
    def get_id(self, obj):
        return str(obj._id)
