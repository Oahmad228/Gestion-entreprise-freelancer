from django.views.generic.base import RedirectView
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', RedirectView.as_view(url='/auth/login/', permanent=True)),  # Redirection
    path('auth/', include('users.urls')),
    path('', include('missions.urls')),
    path('messages/', include('messagerie.urls', namespace='messagerie')),

]