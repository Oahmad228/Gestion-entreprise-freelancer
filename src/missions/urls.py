from django.urls import path
from .views import MissionListView, MissionCreateView, MissionUpdateView, MissionDetailView, PostulerMissionView, \
    traiter_candidature, MissionDeleteView

app_name = 'missions'

urlpatterns = [
    path('', MissionListView.as_view(), name='liste'),
    path('<int:mission_id>/postuler/', PostulerMissionView.as_view(), name='postuler'),
    path('creer/', MissionCreateView.as_view(), name='creer'),
    path('<int:pk>/editer/', MissionUpdateView.as_view(), name='editer'),
    path('<int:pk>/', MissionDetailView.as_view(), name='detail'),
    path('candidature/<int:candidature_id>/<str:action>/', traiter_candidature, name='traiter_candidature'),
    path('<int:pk>/supprimer/', MissionDeleteView.as_view(), name='supprimer_mission'),
]