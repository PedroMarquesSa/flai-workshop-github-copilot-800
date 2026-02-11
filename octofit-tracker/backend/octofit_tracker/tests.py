from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description'
        )
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123',
            team_id=str(self.team._id)
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.team_id, str(self.team._id))
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description'
        )
    
    def test_team_creation(self):
        """Test team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'Test team description')
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now(),
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test activity is created correctly"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.calories, 300)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test description'
        )
        self.user_data = {
            'name': 'API Test User',
            'email': 'apitest@example.com',
            'password': 'testpass123',
            'team_id': str(self.team._id)
        }
    
    def test_create_user(self):
        """Test creating a user via API"""
        response = self.client.post('/api/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().name, 'API Test User')
    
    def test_get_users_list(self):
        """Test getting list of users"""
        User.objects.create(**self.user_data)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.team_data = {
            'name': 'API Test Team',
            'description': 'Test team via API'
        }
    
    def test_create_team(self):
        """Test creating a team via API"""
        response = self.client.post('/api/teams/', self.team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
    
    def test_get_teams_list(self):
        """Test getting list of teams"""
        Team.objects.create(**self.team_data)
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123'
        )
        self.activity_data = {
            'user_id': str(self.user._id),
            'activity_type': 'Running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat(),
            'notes': 'Test run'
        }
    
    def test_create_activity(self):
        """Test creating an activity via API"""
        response = self.client.post('/api/activities/', self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
    
    def test_get_activities_list(self):
        """Test getting list of activities"""
        Activity.objects.create(
            user_id=self.activity_data['user_id'],
            activity_type=self.activity_data['activity_type'],
            duration=self.activity_data['duration'],
            distance=self.activity_data['distance'],
            calories=self.activity_data['calories'],
            date=datetime.now(),
            notes=self.activity_data['notes']
        )
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user = User.objects.create(
            name='Test User',
            email='test@example.com',
            password='testpass123',
            team_id=str(self.team._id)
        )
        self.leaderboard_data = {
            'user_id': str(self.user._id),
            'user_name': 'Test User',
            'team_id': str(self.team._id),
            'team_name': 'Test Team',
            'total_calories': 1000,
            'total_activities': 5,
            'total_duration': 150,
            'rank': 1
        }
    
    def test_get_leaderboard(self):
        """Test getting leaderboard"""
        Leaderboard.objects.create(**self.leaderboard_data)
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'Test workout description',
            'activity_type': 'Running',
            'difficulty_level': 'beginner',
            'duration': 30,
            'calories_estimate': 300,
            'instructions': 'Run for 30 minutes'
        }
    
    def test_create_workout(self):
        """Test creating a workout via API"""
        response = self.client.post('/api/workouts/', self.workout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
    
    def test_get_workouts_list(self):
        """Test getting list of workouts"""
        Workout.objects.create(**self.workout_data)
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
