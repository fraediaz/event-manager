from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from events.models import Event, Attendance
import json


class Command(BaseCommand):
    help = 'Populate the database with test users and events'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        # Create test users
        users_data = [
            {'username': 'admin', 'password': 'admin123456', 'email': 'admin@example.com', 'is_staff': True},
            {'username': 'juan', 'password': 'juan123456', 'email': 'juan@example.com', 'is_staff': False},
            {'username': 'maria', 'password': 'maria123456', 'email': 'maria@example.com', 'is_staff': False},
            {'username': 'carlos', 'password': 'carlos123456', 'email': 'carlos@example.com', 'is_staff': False},
        ]

        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_staff': user_data['is_staff'],
                    'is_superuser': user_data['is_staff'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user_data["username"]}'))
            else:
                self.stdout.write(f'User already exists: {user_data["username"]}')
            users[user_data['username']] = user

        # Create test events with real coordinates (Chile)
        events_data = [
            {
                'title': 'Tech Meetup Santiago',
                'description': 'Encuentro de desarrolladores para hablar sobre tecnología, backend y cloud.',
                'location': 'Santiago, Chile',
                'latitude': Decimal('-33.4489'),
                'longitude': Decimal('-70.6693'),
                'date': timezone.now() + timezone.timedelta(days=15),
                'creator': users['juan'],
            },
            {
                'title': 'React Workshop Valparaíso',
                'description': 'Workshop intensivo de React 18 con hooks, context y performance optimization.',
                'location': 'Valparaíso, Chile',
                'latitude': Decimal('-33.0457'),
                'longitude': Decimal('-71.6270'),
                'date': timezone.now() + timezone.timedelta(days=20),
                'creator': users['maria'],
            },
            {
                'title': 'Django Community Meetup',
                'description': 'Sesión de networking y charlas sobre Django en producción.',
                'location': 'Concepción, Chile',
                'latitude': Decimal('-36.8267'),
                'longitude': Decimal('-73.0498'),
                'date': timezone.now() + timezone.timedelta(days=10),
                'creator': users['carlos'],
            },
            {
                'title': 'Python Bootcamp La Serena',
                'description': 'Bootcamp de 4 semanas intensivas para aprender Python desde cero.',
                'location': 'La Serena, Chile',
                'latitude': Decimal('-29.9019'),
                'longitude': Decimal('-71.5521'),
                'date': timezone.now() + timezone.timedelta(days=30),
                'creator': users['juan'],
            },
            {
                'title': 'Frontend Summit Puerto Montt',
                'description': 'Conferencia sobre tendencias en desarrollo frontend y UX/UI.',
                'location': 'Puerto Montt, Chile',
                'latitude': Decimal('-41.3169'),
                'longitude': Decimal('-72.4886'),
                'date': timezone.now() + timezone.timedelta(days=25),
                'creator': users['maria'],
            },
        ]

        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'description': event_data['description'],
                    'location': event_data['location'],
                    'latitude': event_data['latitude'],
                    'longitude': event_data['longitude'],
                    'date': event_data['date'],
                    'creator': event_data['creator'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created event: {event_data["title"]}'))
            else:
                self.stdout.write(f'Event already exists: {event_data["title"]}')

        # Create test attendances
        all_events = Event.objects.all()
        attendance_statuses = ['going', 'maybe', 'not_going']

        for event in all_events:
            for user in users.values():
                # Don't create attendance for the creator (they're organizing it)
                if user == event.creator:
                    continue

                # Create attendance for some users randomly
                status = attendance_statuses[(hash(f'{event.id}{user.id}') % 3)]
                attendance, created = Attendance.objects.get_or_create(
                    user=user,
                    event=event,
                    defaults={'status': status}
                )
                if created:
                    self.stdout.write(f'Created attendance: {user.username} -> {event.title} ({status})')

        self.stdout.write(self.style.SUCCESS('\nDatabase population completed!'))
        self.stdout.write('\nTest credentials:')
        self.stdout.write('  Admin: admin / admin123456')
        self.stdout.write('  User: juan / juan123456')
        self.stdout.write('  User: maria / maria123456')
        self.stdout.write('  User: carlos / carlos123456')
