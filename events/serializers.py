from rest_framework import serializers

from .models import Attendance, Event


class EventSerializer(serializers.ModelSerializer):
	creator_username = serializers.CharField(source='creator.username', read_only=True)
	attendee_count = serializers.IntegerField(read_only=True)

	class Meta:
		model = Event
		fields = [
			'id',
			'title',
			'description',
			'date',
			'location',
			'latitude',
			'longitude',
			'creator',
			'creator_username',
			'attendee_count',
		]
		read_only_fields = ['id', 'creator', 'creator_username', 'attendee_count']


class AttendanceSerializer(serializers.ModelSerializer):
	user_username = serializers.CharField(source='user.username', read_only=True)
	event_title = serializers.CharField(source='event.title', read_only=True)

	class Meta:
		model = Attendance
		fields = [
			'id',
			'user',
			'user_username',
			'event',
			'event_title',
			'status',
		]
		read_only_fields = ['id', 'user', 'user_username', 'event_title']
