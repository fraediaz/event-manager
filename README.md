# Event Manager

Aplicación web + API para gestión de eventos, con autenticación JWT y experiencia visual con mapas.

## Demo funcional

- Portada pública con mapa: `/`
- Dashboard autenticado: `/` (cuando inicias sesión)
- Crear evento desde UI: `/event/create/`
- Detalle de evento + RSVP: `/event/<uuid>/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Stack técnico

- Backend: Django + Django REST Framework
- Auth: Session Auth + JWT (`djangorestframework-simplejwt`)
- Documentación: OpenAPI 3 con `drf-spectacular`
- Frontend: Django Templates + Tailwind CDN + Leaflet + OpenStreetMap
- Base de datos: SQLite (dev)
- CI: GitHub Actions

## Funcionalidades clave

- CRUD de eventos y asistencias vía API REST.
- UI con mapa público de eventos georreferenciados en Chile.
- Registro/login/logout de usuarios.
- Dashboard con eventos creados y asistencias del usuario.
- RSVP desde la vista de detalle (`Voy`, `Quizás`, `No voy`).
- Permisos por rol:
	- Admin: acceso total.
	- Usuario: solo sus propios recursos para edición/gestión.

## Endpoints principales

- `GET/POST /api/events/`
- `GET/PATCH/PUT/DELETE /api/events/<uuid>/`
- `GET/POST /api/attendances/`
- `GET/PATCH/PUT/DELETE /api/attendances/<id>/`
- `GET /api/events/public/`
- `POST /api/token/`
- `POST /api/token/refresh/`
- `POST /api/token/verify/`

## Arquitectura (resumen)

- `events/models.py`: `Event` y `Attendance`.
- `events/views.py`: ViewSets DRF con permisos por rol.
- `config/views.py`: vistas HTML (home, auth, crear/editar evento, RSVP).
- `templates/`: UI server-rendered.
- `.github/workflows/ci.yml`: pipeline de validación.

## Ejecutar en local

1. Crear entorno virtual e instalar dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Migrar y poblar datos de demo:

```bash
python manage.py migrate
python manage.py populate_db
```

3. Levantar servidor:

```bash
python manage.py runserver 8000
```

4. Abrir en navegador:

- `http://127.0.0.1:8000/`

## Credenciales de prueba

- Admin: `admin / admin123456`
- Usuario: `juan / juan123456`
- Usuario: `maria / maria123456`
- Usuario: `carlos / carlos123456`

## Calidad y validación

- Validación local:

```bash
python manage.py check
python manage.py test
```

- CI automático en cada PR/push a `main`:
	- install dependencies
	- `check`
	- `migrate`
	- `test`

