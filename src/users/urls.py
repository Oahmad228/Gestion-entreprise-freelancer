from django.urls import path
from .views import LoginView, SignupView, LogoutView, ProfileView, CompleteProfileView, AccountDeleteView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('supprimer-compte/', AccountDeleteView.as_view(), name='supprimer_compte'),
]