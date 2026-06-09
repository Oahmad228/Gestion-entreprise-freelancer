from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.liste_conversations, name='liste'),
    path('<int:conversation_id>/', views.conversation_detail, name='detail'),
    path('nouvelle/<int:mission_id>/<int:candidature_id>/', views.demarrer_conversation, name='nouvelle'), # Ajoutez cette ligne
]