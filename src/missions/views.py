from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
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
        return redirect('missions:liste')

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
    template_name = 'liste.html'
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
    template_name = 'formulaire.html'
    success_url = reverse_lazy('missions:liste')

    def form_valid(self, form):
        form.instance.entreprise = self.request.user
        return super().form_valid(form)

class MissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Mission
    form_class = MissionForm
    template_name = 'formulaire.html'
    success_url = reverse_lazy('missions:liste')

    def get_queryset(self):
        return Mission.objects.filter(entreprise=self.request.user)


class MissionDetailView(LoginRequiredMixin, DetailView):
    model = Mission
    template_name = 'detail.html'  # Chemin direct sans sous-dossier missions/
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
    template_name = 'postuler.html'

    def form_valid(self, form):
        form.instance.mission_id = self.kwargs['mission_id']
        # Assignez l'utilisateur directement au lieu du profil freelance
        form.instance.freelance = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('missions:detail', kwargs={'pk': self.kwargs['mission_id']})

class MissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Mission
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('missions:liste')

    def get_queryset(self):
        return Mission.objects.filter(entreprise=self.request.user)