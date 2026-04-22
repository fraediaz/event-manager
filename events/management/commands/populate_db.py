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
            {'username': 'ana', 'password': 'ana123456', 'email': 'ana@example.com', 'is_staff': False},
            {'username': 'pedro', 'password': 'pedro123456', 'email': 'pedro@example.com', 'is_staff': False},
            {'username': 'sofia', 'password': 'sofia123456', 'email': 'sofia@example.com', 'is_staff': False},
            {'username': 'diego', 'password': 'diego123456', 'email': 'diego@example.com', 'is_staff': False},
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
            {
                'title': 'Data Engineering Night Antofagasta',
                'description': 'Charlas de pipelines, ETL y observabilidad de datos en tiempo real.',
                'location': 'Antofagasta, Chile',
                'latitude': Decimal('-23.6509'),
                'longitude': Decimal('-70.3975'),
                'date': timezone.now() + timezone.timedelta(days=12),
                'creator': users['ana'],
            },
            {
                'title': 'IA Product Meetup Viña del Mar',
                'description': 'Casos reales de productos con IA y estrategias de lanzamiento.',
                'location': 'Viña del Mar, Chile',
                'latitude': Decimal('-33.0245'),
                'longitude': Decimal('-71.5518'),
                'date': timezone.now() + timezone.timedelta(days=18),
                'creator': users['pedro'],
            },
            {
                'title': 'Cloud Security Day Temuco',
                'description': 'Buenas prácticas de seguridad cloud, IAM y hardening.',
                'location': 'Temuco, Chile',
                'latitude': Decimal('-38.7359'),
                'longitude': Decimal('-72.5904'),
                'date': timezone.now() + timezone.timedelta(days=22),
                'creator': users['sofia'],
            },
            {
                'title': 'Mobile Dev Jam Iquique',
                'description': 'Sesiones prácticas de desarrollo móvil multiplataforma.',
                'location': 'Iquique, Chile',
                'latitude': Decimal('-20.2307'),
                'longitude': Decimal('-70.1357'),
                'date': timezone.now() + timezone.timedelta(days=28),
                'creator': users['diego'],
            },
            {
                'title': 'API Design Workshop Rancagua',
                'description': 'Diseño de APIs REST robustas, versionado y documentación OpenAPI.',
                'location': 'Rancagua, Chile',
                'latitude': Decimal('-34.1708'),
                'longitude': Decimal('-70.7444'),
                'date': timezone.now() + timezone.timedelta(days=16),
                'creator': users['ana'],
            },
            {
                'title': 'DevOps Hands-on Talca',
                'description': 'CI/CD, contenedores y despliegues automatizados paso a paso.',
                'location': 'Talca, Chile',
                'latitude': Decimal('-35.4264'),
                'longitude': Decimal('-71.6554'),
                'date': timezone.now() + timezone.timedelta(days=14),
                'creator': users['pedro'],
            },
            {
                'title': 'UX Research Lab Arica',
                'description': 'Métodos de investigación de usuarios y pruebas de usabilidad.',
                'location': 'Arica, Chile',
                'latitude': Decimal('-18.4783'),
                'longitude': Decimal('-70.3126'),
                'date': timezone.now() + timezone.timedelta(days=24),
                'creator': users['sofia'],
            },
            {
                'title': 'Backend Architecture Summit Chillan',
                'description': 'Arquitecturas limpias, escalabilidad y patrones backend.',
                'location': 'Chillán, Chile',
                'latitude': Decimal('-36.6066'),
                'longitude': Decimal('-72.1034'),
                'date': timezone.now() + timezone.timedelta(days=32),
                'creator': users['diego'],
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
        self.stdout.write('  User: ana / ana123456')
        self.stdout.write('  User: pedro / pedro123456')
        self.stdout.write('  User: sofia / sofia123456')
        self.stdout.write('  User: diego / diego123456')
