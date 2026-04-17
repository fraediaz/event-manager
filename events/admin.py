from django.contrib import admin

from .models import Attendance, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'location', 'latitude', 'longitude', 'creator')
	list_filter = ('date', 'location', 'creator')
	search_fields = ('title', 'location', 'creator__username')
	ordering = ('-date', 'title')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
	list_display = ('user', 'event', 'status')
	list_filter = ('status', 'event')
	search_fields = ('user__username', 'event__title')
