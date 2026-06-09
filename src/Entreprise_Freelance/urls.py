from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('messagerie/', include('messagerie.urls', namespace='messagerie')), # Doit être avant 'missions/'
    path('missions/', include('missions.urls', namespace='missions')),
    path('', RedirectView.as_view(url='/missions/')),  # Redirection racine explicite
]