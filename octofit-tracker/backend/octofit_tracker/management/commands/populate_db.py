from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from pymongo import MongoClient


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create unique index on email field for users
        self.stdout.write('Creating unique index on email field...')
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes united in fitness'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League working together for peak performance'
        )

        # Create Marvel Users
        self.stdout.write('Creating Marvel superheroes...')
        marvel_users = [
            User.objects.create(
                name='Tony Stark',
                email='ironman@marvel.com',
                password='arc_reactor_3000',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Steve Rogers',
                email='captainamerica@marvel.com',
                password='shield_throw_76',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Natasha Romanoff',
                email='blackwidow@marvel.com',
                password='red_room_secret',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Bruce Banner',
                email='hulk@marvel.com',
                password='gamma_smash',
                team_id=str(team_marvel._id)
            ),
            User.objects.create(
                name='Thor Odinson',
                email='thor@marvel.com',
                password='mjolnir_worthy',
                team_id=str(team_marvel._id)
            ),
        ]

        # Create DC Users
        self.stdout.write('Creating DC superheroes...')
        dc_users = [
            User.objects.create(
                name='Bruce Wayne',
                email='batman@dc.com',
                password='dark_knight_rises',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Clark Kent',
                email='superman@dc.com',
                password='krypton_forever',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Diana Prince',
                email='wonderwoman@dc.com',
                password='amazonian_warrior',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Barry Allen',
                email='flash@dc.com',
                password='speed_force_run',
                team_id=str(team_dc._id)
            ),
            User.objects.create(
                name='Arthur Curry',
                email='aquaman@dc.com',
                password='atlantis_king',
                team_id=str(team_dc._id)
            ),
        ]

        all_users = marvel_users + dc_users

        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Swimming', 'Cycling', 'Weightlifting', 'Yoga', 'Boxing', 'Martial Arts']
        
        for i, user in enumerate(all_users):
            # Each user gets 3-5 activities
            num_activities = 3 + (i % 3)
            for j in range(num_activities):
                activity_type = activity_types[j % len(activity_types)]
                duration = 30 + (j * 15) + (i * 5)
                distance = round(duration * 0.15, 2) if activity_type in ['Running', 'Swimming', 'Cycling'] else None
                calories = duration * (8 + (i % 4))
                days_ago = j + (i * 2)
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=datetime.now() - timedelta(days=days_ago),
                    notes=f'{user.name} completed {activity_type} session'
                )

        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(a.calories for a in user_activities)
            total_duration = sum(a.duration for a in user_activities)
            total_activities = user_activities.count()
            
            team = team_marvel if user in marvel_users else team_dc
            
            Leaderboard.objects.create(
                user_id=str(user._id),
                user_name=user.name,
                team_id=str(team._id),
                team_name=team.name,
                total_calories=total_calories,
                total_activities=total_activities,
                total_duration=total_duration
            )

        # Update leaderboard ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_calories')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()

        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Iron Man Power Training',
                'description': 'High-intensity workout inspired by Tony Stark\'s training regime',
                'activity_type': 'Weightlifting',
                'difficulty_level': 'advanced',
                'duration': 60,
                'calories_estimate': 500,
                'instructions': '1. Warm up for 10 minutes\n2. Bench press 4x10\n3. Deadlifts 4x8\n4. Shoulder press 3x12\n5. Cool down and stretch'
            },
            {
                'name': 'Captain America Endurance Run',
                'description': 'Build stamina like the First Avenger',
                'activity_type': 'Running',
                'difficulty_level': 'intermediate',
                'duration': 45,
                'calories_estimate': 450,
                'instructions': '1. 5-minute warm-up jog\n2. 30 minutes steady pace run\n3. 5-minute sprint intervals\n4. 5-minute cool down walk'
            },
            {
                'name': 'Black Widow Combat Circuit',
                'description': 'Martial arts and agility training',
                'activity_type': 'Martial Arts',
                'difficulty_level': 'advanced',
                'duration': 50,
                'calories_estimate': 550,
                'instructions': '1. Shadow boxing 10 minutes\n2. Kicks and punches combo 15 minutes\n3. Agility drills 15 minutes\n4. Core work 10 minutes'
            },
            {
                'name': 'Thor Hammer Swings',
                'description': 'Build power with functional movements',
                'activity_type': 'Weightlifting',
                'difficulty_level': 'intermediate',
                'duration': 40,
                'calories_estimate': 400,
                'instructions': '1. Kettlebell swings 4x15\n2. Battle rope slams 3x30 seconds\n3. Medicine ball slams 4x12\n4. Farmer\'s carry 3x50 meters'
            },
            {
                'name': 'Batman Night Patrol',
                'description': 'Stealth and endurance training for the Dark Knight',
                'activity_type': 'Running',
                'difficulty_level': 'intermediate',
                'duration': 55,
                'calories_estimate': 480,
                'instructions': '1. 10-minute warm-up\n2. Hill sprints 10x30 seconds\n3. Recovery jog 20 minutes\n4. Cooldown 5 minutes'
            },
            {
                'name': 'Superman Flight Training',
                'description': 'Core and upper body strength like the Man of Steel',
                'activity_type': 'Weightlifting',
                'difficulty_level': 'advanced',
                'duration': 65,
                'calories_estimate': 600,
                'instructions': '1. Pull-ups 5x10\n2. Superman holds 4x45 seconds\n3. Plank variations 5 minutes\n4. Overhead press 4x10\n5. Core circuit 10 minutes'
            },
            {
                'name': 'Wonder Woman Warrior Yoga',
                'description': 'Flexibility and strength combined',
                'activity_type': 'Yoga',
                'difficulty_level': 'beginner',
                'duration': 30,
                'calories_estimate': 200,
                'instructions': '1. Sun salutations 10 minutes\n2. Warrior poses sequence 10 minutes\n3. Balance poses 5 minutes\n4. Relaxation and meditation 5 minutes'
            },
            {
                'name': 'Flash Speed Work',
                'description': 'Sprint training for maximum velocity',
                'activity_type': 'Running',
                'difficulty_level': 'advanced',
                'duration': 35,
                'calories_estimate': 420,
                'instructions': '1. Dynamic warm-up 10 minutes\n2. 100m sprints 8x (2 min rest)\n3. Cool down jog 5 minutes\n4. Stretching 5 minutes'
            },
            {
                'name': 'Aquaman Ocean Swim',
                'description': 'Swimming workout for aquatic excellence',
                'activity_type': 'Swimming',
                'difficulty_level': 'intermediate',
                'duration': 45,
                'calories_estimate': 500,
                'instructions': '1. Warm up 400m easy\n2. Main set: 10x100m intervals\n3. Cool down 200m easy\n4. Stretch on deck'
            },
            {
                'name': 'Avengers Assembly Circuit',
                'description': 'Full-body team-inspired workout',
                'activity_type': 'Weightlifting',
                'difficulty_level': 'beginner',
                'duration': 30,
                'calories_estimate': 300,
                'instructions': '1. Jumping jacks 2 minutes\n2. Push-ups 3x10\n3. Squats 3x15\n4. Lunges 3x10 each leg\n5. Plank 3x30 seconds'
            },
        ]

        for workout_data in workouts:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(all_users)} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Activity.objects.count()} activities'))
        self.stdout.write(self.style.SUCCESS(f'Created {Leaderboard.objects.count()} leaderboard entries'))
        self.stdout.write(self.style.SUCCESS(f'Created {Workout.objects.count()} workouts'))
