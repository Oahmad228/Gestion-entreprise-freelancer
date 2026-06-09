from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from users.models import Utilisateur


class Mission(models.Model):
    entreprise = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': Utilisateur.TypeUtilisateur.ENTREPRISE},
        related_name='missions_publiees',
        verbose_name=_("Entreprise recruteuse")
    )

    titre = models.CharField(
        max_length=255,
        verbose_name=_("Titre de la mission")
    )

    description = models.TextField(
        verbose_name=_("Description détaillée")
    )

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Budget alloué (€)")
    )

    competences_requises = models.TextField(
        blank=True,
        verbose_name=_("Compétences requises"),
        help_text=_("Listez les compétences nécessaires séparées par des virgules")
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de publication")
    )

    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Dernière mise à jour")
    )

    date_limite = models.DateField(
        verbose_name=_("Date limite de candidature")
    )

    est_active = models.BooleanField(
        default=True,
        verbose_name=_("Mission active")
    )

    class Meta:
        verbose_name = _("Mission")
        verbose_name_plural = _("Missions")
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['-date_creation']),
            models.Index(fields=['entreprise']),
            models.Index(fields=['est_active']),
        ]

    def __str__(self):
        return f"{self.titre} - {self.entreprise.entreprise_profile.nom_entreprise}"

    def get_participants(self):
        """Retourne les participants autorisés pour cette mission"""
        participants = {self.entreprise}
        participants.update([candidature.freelance for candidature in self.candidatures.all()])
        return participants


class Candidature(models.Model):
    class StatutCandidature(models.TextChoices):
        EN_ATTENTE = 'en_attente', _('En attente')
        ACCEPTEE = 'acceptee', _('Acceptée')
        REFUSEE = 'refusee', _('Refusée')

    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name='candidatures',
        verbose_name=_("Mission concernée")
    )

    freelance = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': Utilisateur.TypeUtilisateur.FREELANCE},
        related_name='candidatures_envoyees',
        verbose_name=_("Freelance candidat")
    )

    message = models.TextField(
        verbose_name=_("Message de motivation")
    )

    date_postulation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de candidature")
    )

    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Dernière modification")
    )

    statut = models.CharField(
        max_length=20,
        choices=StatutCandidature.choices,
        default=StatutCandidature.EN_ATTENTE,
        verbose_name=_("Statut de la candidature")
    )

    class Meta:
        verbose_name = _("Candidature")
        verbose_name_plural = _("Candidatures")
        unique_together = ('mission', 'freelance')
        ordering = ['-date_postulation']
        indexes = [
            models.Index(fields=['-date_postulation']),
            models.Index(fields=['statut']),
        ]

    def __str__(self):
        return f"{self.freelance.username} → {self.mission.titre} ({self.get_statut_display()})"

    @property
    def est_acceptee(self):
        return self.statut == self.StatutCandidature.ACCEPTEE

    @property
    def est_en_attente(self):
        return self.statut == self.StatutCandidature.EN_ATTENTE