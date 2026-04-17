"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from rest_framework_simplejwt.views import TokenObtainPairView
from config.views import home, public_events, event_detail, user_login, user_logout, user_signup, create_event, edit_event, rsvp_event

urlpatterns = [
    path('', home, name='home'),
    path('accounts/login/', user_login, name='user_login'),
    path('accounts/logout/', user_logout, name='user_logout'),
    path('accounts/signup/', user_signup, name='user_signup'),
    path('event/create/', create_event, name='create_event'),
    path('event/<uuid:event_id>/edit/', edit_event, name='edit_event'),
    path('event/<uuid:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('api/events/public/', public_events, name='public_events'),
    path('event/<uuid:event_id>/', event_detail, name='event_detail'),
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
