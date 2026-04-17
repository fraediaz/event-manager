from django.db.models import Count
from rest_framework import viewsets

from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view

from .models import Attendance, Event
from .permissions import IsAttendanceOwnerOrAdmin, IsEventOwnerOrAdmin
from .serializers import AttendanceSerializer, EventSerializer


@extend_schema_view(
	list=extend_schema(
		summary='Listar eventos',
		description='Devuelve todos los eventos registrados con el número total de asistentes.',
		tags=['Eventos'],
	),
	retrieve=extend_schema(
		summary='Obtener evento',
		description='Devuelve el detalle de un evento específico.',
		tags=['Eventos'],
	),
	create=extend_schema(
		summary='Crear evento',
		description='Crea un nuevo evento usando el usuario autenticado como creador.',
		tags=['Eventos'],
		examples=[
			OpenApiExample(
				'Ejemplo de evento',
				value={
					'title': 'Tech Meetup',
					'description': 'Encuentro para hablar de producto y backend',
					'date': '2026-05-10T18:30:00Z',
					'location': 'Santiago',
				},
				request_only=True,
			)
		],
	),
	update=extend_schema(summary='Actualizar evento', tags=['Eventos']),
	partial_update=extend_schema(summary='Actualizar parcialmente evento', tags=['Eventos']),
	destroy=extend_schema(summary='Eliminar evento', tags=['Eventos']),
)
class EventViewSet(viewsets.ModelViewSet):
	permission_classes = [IsEventOwnerOrAdmin]
	queryset = Event.objects.all()
	serializer_class = EventSerializer

	def get_queryset(self):
		queryset = Event.objects.select_related('creator').annotate(
			attendee_count=Count('attendees', distinct=True)
		).order_by('date', 'title')

		if self.request.user.is_authenticated and not self.request.user.is_staff:
			return queryset.filter(creator=self.request.user)

		return queryset

	def perform_create(self, serializer):
		serializer.save(creator=self.request.user)


@extend_schema_view(
	list=extend_schema(
		summary='Listar asistencias',
		description='Devuelve solo las asistencias del usuario autenticado.',
		tags=['Asistencias'],
	),
	retrieve=extend_schema(
		summary='Obtener asistencia',
		description='Devuelve una asistencia propia del usuario autenticado.',
		tags=['Asistencias'],
	),
	create=extend_schema(
		summary='Crear asistencia',
		description='Registra la asistencia del usuario autenticado para un evento.',
		tags=['Asistencias'],
	),
	update=extend_schema(summary='Actualizar asistencia', tags=['Asistencias']),
	partial_update=extend_schema(summary='Actualizar parcialmente asistencia', tags=['Asistencias']),
	destroy=extend_schema(summary='Eliminar asistencia', tags=['Asistencias']),
)
class AttendanceViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAttendanceOwnerOrAdmin]
	queryset = Attendance.objects.all()
	serializer_class = AttendanceSerializer

	def get_queryset(self):
		queryset = Attendance.objects.select_related('user', 'event', 'event__creator').order_by(
			'event__date', 'event__title'
		)

		if self.request.user.is_authenticated and not self.request.user.is_staff:
			return queryset.filter(user=self.request.user)

		return queryset

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
