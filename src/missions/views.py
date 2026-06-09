from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Mission, Candidature
from django.urls import reverse_lazy
from .forms import MissionForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def traiter_candidature(request, candidature_id, action):
    candidature = get_object_or_404(Candidature, pk=candidature_id)

    # Vérification que l'utilisateur est bien l'entreprise propriétaire de la mission
    if request.user != candidature.mission.entreprise:
        messages.error(request, "Action non autorisée")
        return redirect('missions:listes')

    if action == 'acceptee':
        candidature.statut = Candidature.StatutCandidature.ACCEPTEE
        messages.success(request, f"Candidature de {candidature.freelance.username} acceptée !")
    elif action == 'refusee':
        candidature.statut = Candidature.StatutCandidature.REFUSEE
        messages.warning(request, f"Candidature de {candidature.freelance.username} refusée.")

    candidature.save()
    return redirect('missions:detail', pk=candidature.mission.pk)


class MissionListView(LoginRequiredMixin, ListView):
    model = Mission
    template_name = 'missions/listes.html'
    context_object_name = 'missions'

    def get_queryset(self):
        if self.request.user.est_freelance:
            # Pour les freelances : missions actives où ils n'ont pas postulé
            missions_postulees = self.request.user.candidatures_envoyees.values_list('mission_id', flat=True)
            return Mission.objects.filter(est_active=True).exclude(id__in=missions_postulees)
        elif self.request.user.est_entreprise:
            # Pour les entreprises : leurs propres missions
            return Mission.objects.filter(entreprise=self.request.user)
        return Mission.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['est_freelance'] = self.request.user.est_freelance
        return context


class MissionCreateView(LoginRequiredMixin, CreateView):
    model = Mission
    form_class = MissionForm
    template_name = 'missions/formulaire.html'
    success_url = reverse_lazy('missions:listes')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.est_entreprise:
            messages.error(request, "Seules les entreprises peuvent créer des missions")
            return redirect('missions:listes')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.entreprise = self.request.user
        return super().form_valid(form)

class MissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'missions/formulaire.html'
    success_url = reverse_lazy('missions:listes')

    def get_queryset(self):
        return Mission.objects.filter(entreprise=self.request.user)


class MissionDetailView(LoginRequiredMixin, DetailView):
    model = Mission
    template_name = 'missions/detail.html'  # Chemin direct sans sous-dossier missions/
    context_object_name = 'mission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mission = self.object

        if self.request.user.est_freelance:
            context['a_postule'] = mission.candidatures.filter(freelance=self.request.user).exists()
        elif self.request.user.est_entreprise and mission.entreprise == self.request.user:
            context['candidatures'] = mission.candidatures.all().select_related('freelance')

        return context

class PostulerMissionView(LoginRequiredMixin, CreateView):
    model = Candidature
    fields = ['message']
    template_name = 'missions/postuler.html'

    def form_valid(self, form):
        form.instance.mission_id = self.kwargs['mission_id']
        # Assignez l'utilisateur directement au lieu du profil freelance
        form.instance.freelance = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('missions:detail', kwargs={'pk': self.kwargs['mission_id']})

class MissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Mission
    template_name = 'missions/confirm_delete.html'
    success_url = reverse_lazy('missions:listes')

    def get_queryset(self):
        return Mission.objects.filter(entreprise=self.request.user)


class MissionDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'missions/confirm_delete.html'
    success_url = reverse_lazy('missions:listes')

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.est_entreprise and hasattr(user, 'entreprise_profile')

    def get_queryset(self):
        return Mission.objects.filter(entreprise=self.request.user)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        """
        Supprime en cascade les objets liés avant la mission
        """
        self.object = self.get_object()

        # 1. Supprimer les messages associés
        conversations = self.object.conversation_set.all()
        for conv in conversations:
            conv.message_set.all().delete()

        # 2. Supprimer les conversations
        conversations.delete()

        # 3. Supprimer les candidatures
        self.object.candidatures.all().delete()

        # 4. Enfin supprimer la mission
        return super().delete(request, *args, **kwargs)