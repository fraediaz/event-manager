from datetime import datetime, timezone as datetime_timezone
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Attendance, Event


class EventPermissionTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.admin = User.objects.create_user(username='admin', password='pass12345', is_staff=True)
		self.owner = User.objects.create_user(username='owner', password='pass12345')
		self.other = User.objects.create_user(username='other', password='pass12345')
		self.event = Event.objects.create(
			title='Evento 1',
			description='Desc',
			date=datetime(2026, 5, 1, 10, 0, tzinfo=datetime_timezone.utc),
			location='Santiago',
			latitude=Decimal('-33.448890'),
			longitude=Decimal('-70.669285'),
			creator=self.owner,
		)

	def test_user_can_only_see_own_events(self):
		self.client.force_authenticate(user=self.other)
		response = self.client.get(reverse('event-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 0)

	def test_admin_can_see_all_events(self):
		self.client.force_authenticate(user=self.admin)
		response = self.client.get(reverse('event-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_event_includes_coordinates(self):
		self.client.force_authenticate(user=self.admin)
		response = self.client.get(reverse('event-detail', args=[self.event.id]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['latitude'], '-33.448890')
		self.assertEqual(response.data['longitude'], '-70.669285')


class AttendancePermissionTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.admin = User.objects.create_user(username='admin', password='pass12345', is_staff=True)
		self.owner = User.objects.create_user(username='owner', password='pass12345')
		self.other = User.objects.create_user(username='other', password='pass12345')
		self.event = Event.objects.create(
			title='Evento 1',
			description='Desc',
			date=datetime(2026, 5, 1, 10, 0, tzinfo=datetime_timezone.utc),
			location='Santiago',
			creator=self.owner,
		)
		self.attendance = Attendance.objects.create(user=self.owner, event=self.event, status='going')

	def test_user_sees_only_own_attendance(self):
		self.client.force_authenticate(user=self.other)
		response = self.client.get(reverse('attendance-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 0)

	def test_admin_sees_all_attendances(self):
		self.client.force_authenticate(user=self.admin)
		response = self.client.get(reverse('attendance-list'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)


class EventRsvpViewTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='rsvp-user', password='pass12345')
		self.owner = User.objects.create_user(username='event-owner', password='pass12345')
		self.event = Event.objects.create(
			title='Evento RSVP',
			description='Prueba de asistencia',
			date=datetime(2026, 6, 1, 10, 0, tzinfo=datetime_timezone.utc),
			location='Santiago',
			creator=self.owner,
		)

	def test_authenticated_user_can_create_attendance(self):
		self.client.login(username='rsvp-user', password='pass12345')
		response = self.client.post(reverse('rsvp_event', args=[self.event.id]), {'status': 'going'})

		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		attendance = Attendance.objects.get(user=self.user, event=self.event)
		self.assertEqual(attendance.status, 'going')

	def test_authenticated_user_can_update_attendance(self):
		Attendance.objects.create(user=self.user, event=self.event, status='maybe')
		self.client.login(username='rsvp-user', password='pass12345')
		response = self.client.post(reverse('rsvp_event', args=[self.event.id]), {'status': 'not_going'})

		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
		attendance = Attendance.objects.get(user=self.user, event=self.event)
		self.assertEqual(attendance.status, 'not_going')

	def test_unauthenticated_user_is_redirected_to_login(self):
		response = self.client.post(reverse('rsvp_event', args=[self.event.id]), {'status': 'going'})
		self.assertEqual(response.status_code, status.HTTP_302_FOUND)
