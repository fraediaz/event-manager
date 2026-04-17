from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from events.models import Event, Attendance


def home(request):
    sections = [
        {
            'title': 'Qué incluye',
            'items': [
                'CRUD de eventos y asistencias',
                'Autenticación JWT y sesión para la UI',
                'Documentación OpenAPI con Swagger y ReDoc',
            ],
        },
        {
            'title': 'Endpoints clave',
            'items': [
                'POST /api/token/',
                'GET /api/events/',
                'GET /api/schema/',
            ],
        },
        {
            'title': 'Enlaces útiles',
            'items': [
                'Swagger UI en /api/docs/',
                'ReDoc en /api/redoc/',
                'Todos los eventos en el mapa',
            ],
        },
    ]

    context = {
        'project_name': 'Event Manager',
        'tagline': 'Una API limpia para organizar eventos, asistentes y autenticación en un solo lugar.',
        'sections': sections,
    }

    if request.user.is_authenticated:
        # Usuario logged in - mostrar panel
        upcoming_events = Event.objects.filter(
            attendees__user=request.user
        ).distinct().order_by('date')[:5]
        my_events = Event.objects.filter(creator=request.user).order_by('date')[:5]
        context.update({
            'user': request.user,
            'upcoming_events': upcoming_events,
            'my_events': my_events,
        })
        return render(request, 'dashboard.html', context)
    else:
        # Usuario no logged - mostrar portada con login
        return render(request, 'home.html', context)


def public_events(request):
    events = Event.objects.all()
    data = [
        {
            'id': str(event.id),
            'title': event.title,
            'description': event.description,
            'location': event.location,
            'date': event.date.isoformat(),
            'latitude': str(event.latitude) if event.latitude else None,
            'longitude': str(event.longitude) if event.longitude else None,
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_attendance = None
    attendance_summary = {
        'going': 0,
        'maybe': 0,
        'not_going': 0,
    }

    grouped_statuses = (
        Attendance.objects.filter(event=event)
        .values('status')
        .annotate(total=Count('id'))
    )
    for row in grouped_statuses:
        attendance_summary[row['status']] = row['total']

    if request.user.is_authenticated:
        user_attendance = Attendance.objects.filter(
            user=request.user, event=event
        ).first()
    return render(
        request,
        'event_detail.html',
        {
            'event': event,
            'latitude': float(event.latitude) if event.latitude else 0,
            'longitude': float(event.longitude) if event.longitude else 0,
            'user_attendance': user_attendance,
            'attendance_summary': attendance_summary,
        },
    )


@login_required(login_url='user_login')
def rsvp_event(request, event_id):
    if request.method != 'POST':
        return redirect('event_detail', event_id=event_id)

    status_value = request.POST.get('status')
    valid_statuses = {choice[0] for choice in Attendance.STATUS_CHOICES}

    if status_value not in valid_statuses:
        return redirect('event_detail', event_id=event_id)

    event = get_object_or_404(Event, id=event_id)
    Attendance.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={'status': status_value},
    )
    return redirect('event_detail', event_id=event_id)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña inválidos'})

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if not username or not email or not password:
            return render(request, 'signup.html', {'error': 'Completa todos los campos'})

        if password != password_confirm:
            return render(request, 'signup.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'El usuario ya existe'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


@login_required(login_url='user_login')
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date = request.POST.get('date')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Validación básica
        if not all([title, description, location, date]):
            return render(request, 'create_event.html', {'error': 'Completa todos los campos requeridos'})

        try:
            event = Event.objects.create(
                title=title,
                description=description,
                location=location,
                date=date,
                latitude=latitude if latitude else None,
                longitude=longitude if longitude else None,
                creator=request.user
            )
            return redirect('event_detail', event_id=event.id)
        except Exception as e:
            return render(request, 'create_event.html', {'error': f'Error al crear evento: {str(e)}'})

    return render(request, 'create_event.html')


@login_required(login_url='user_login')
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Verificar que el usuario sea el creador
    if event.creator != request.user and not request.user.is_staff:
        return render(request, 'error.html', {
            'error': 'No tienes permiso para editar este evento',
            'status': 403
        }, status=403)
    
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.description = request.POST.get('description', event.description)
        event.location = request.POST.get('location', event.location)
        event.date = request.POST.get('date', event.date)
        
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if latitude:
            event.latitude = latitude
        if longitude:
            event.longitude = longitude
        
        try:
            event.save()
            return redirect('event_detail', event_id=event.id)
        except Exception as e:
            return render(request, 'edit_event.html', {
                'event': event,
                'error': f'Error al actualizar evento: {str(e)}'
            })
    
    return render(request, 'edit_event.html', {'event': event})
