from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, DeleteView
from .models import Utilisateur, Freelance, Entreprise


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('missions:listes')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, _("Connexion réussie !"))
            return redirect('missions:listes')  # Redirection vers la liste des missions
        else:
            messages.error(request, _("Identifiants incorrects."))
            return render(request, self.template_name)


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('missions:listes')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')  # Reçoit "FR" ou "EN"

        # Validation
        if not all([username, email, password1, password2, user_type]):
            messages.error(request, _("Tous les champs obligatoires doivent être remplis."))
            return render(request, self.template_name)

        if password1 != password2:
            messages.error(request, _("Les mots de passe ne correspondent pas."))
            return render(request, self.template_name)

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, _("Ce nom d'utilisateur est déjà pris."))
            return render(request, self.template_name)

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, _("Un compte avec cet email existe déjà."))
            return render(request, self.template_name)

        try:
            # Création utilisateur
            user = Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password1,
                type_utilisateur=user_type  # "FR" ou "EN"
            )

            # Création profil spécifique
            if user_type == 'FR':
                Freelance.objects.create(
                    utilisateur=user,
                    bio=request.POST.get('bio', ''),
                    competences=request.POST.get('competences', ''),
                    tarif_horaire=float(request.POST.get('tarif_horaire', 0))
                )
            elif user_type == 'EN':
                nom_entreprise = request.POST.get('nom_entreprise')
                if not nom_entreprise:
                    messages.error(request, _("Le nom de l'entreprise est obligatoire."))
                    user.delete()  # Annule la création
                    return render(request, self.template_name)

                Entreprise.objects.create(
                    utilisateur=user,
                    nom_entreprise=nom_entreprise,
                    description=request.POST.get('description', ''),
                    site_web=request.POST.get('site_web', '')
                )

            login(request, user)
            messages.success(request, _("Inscription réussie !"))
            return redirect('missions:listes')  # Redirection vers la liste des missions

        except Exception as e:
            messages.error(request, _(f"Erreur lors de la création du compte: {str(e)}"))
            return render(request, self.template_name)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, _("Vous avez été déconnecté."))
        return redirect('users:login')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'  # Chemin direct sans sous-dossier

    def get(self, request):
        user = request.user
        context = {
            'user': user,
        }

        # Ajoutez ces méthodes à votre modèle Utilisateur si elles n'existent pas
        if hasattr(user, 'candidatures_envoyees'):
            context['candidatures_envoyees'] = user.candidatures_envoyees.all()

        if hasattr(user, 'missions_publiees'):
            context['missions_publiees'] = user.missions_publiees.all()

        return render(request, self.template_name, context)


class CompleteProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'complete_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        user = self.request.user
        if user.est_freelance:
            return user.freelance_profile
        elif user.est_entreprise:
            return user.entreprise_profile
        return None

    def get_form_class(self):
        if self.request.user.est_freelance:
            from .forms import FreelanceProfileForm
            return FreelanceProfileForm
        else:
            from .forms import EntrepriseProfileForm
            return EntrepriseProfileForm


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('users:login')

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)