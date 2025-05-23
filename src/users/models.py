from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _


class Utilisateur(AbstractUser):
    class TypeUtilisateur(models.TextChoices):
        FREELANCE = 'FR', _('Freelance')
        ENTREPRISE = 'EN', _('Entreprise')

    type_utilisateur = models.CharField(
        max_length=2,
        choices=TypeUtilisateur.choices,
        blank=True,
        null=True,
        verbose_name=_("Type d'utilisateur")
    )

    username = models.CharField(
        max_length=15,
        unique=True,
        validators=[MinLengthValidator(4)],
        verbose_name=_("Nom d'utilisateur")
    )

    password = models.CharField(
        max_length=128,  # Stockage du hash, pas besoin de limiter à 25
        verbose_name=_("Mot de passe")
    )

    # Suppression des champs inutiles (est_freelance/est_entreprise)
    # Utilisation de type_utilisateur à la place

    def __str__(self):
        return self.username

    @property
    def est_freelance(self):
        return self.type_utilisateur == self.TypeUtilisateur.FREELANCE

    @property
    def est_entreprise(self):
        return self.type_utilisateur == self.TypeUtilisateur.ENTREPRISE

    @property
    def candidatures_acceptees(self):
        return self.candidatures_envoyees.filter(statut='acceptee').count()


class Freelance(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': Utilisateur.TypeUtilisateur.FREELANCE},
        related_name='freelance_profile'
    )

    bio = models.TextField(
        blank=True,
        verbose_name=_("Biographie"),
        help_text=_("Décrivez votre parcours et expérience")
    )

    competences = models.TextField(
        verbose_name=_("Compétences"),
        help_text=_("Liste de compétences séparées par des virgules")
    )

    tarif_horaire = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Tarif horaire (€)"),
        help_text=_("Tarif horaire moyen pour vos prestations")
    )

    lien_portfolio = models.URLField(
        blank=True,
        verbose_name=_("Lien vers le portfolio"),
        help_text=_("URL de votre portfolio en ligne")
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )

    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )

    class Meta:
        verbose_name = _("Profil Freelance")
        verbose_name_plural = _("Profils Freelance")
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.utilisateur.username} (Freelance)"


class Entreprise(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': Utilisateur.TypeUtilisateur.ENTREPRISE},
        related_name='entreprise_profile'
    )

    nom_entreprise = models.CharField(
        max_length=255,
        verbose_name=_("Nom de l'entreprise")
    )

    description = models.TextField(
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Présentation de votre entreprise")
    )

    site_web = models.URLField(
        blank=True,
        verbose_name=_("Site web")
    )

    email_contact = models.EmailField(
        verbose_name=_("Email de contact")
    )

    siret = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name=_("Numéro SIRET")
    )

    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )

    date_mise_a_jour = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )

    class Meta:
        verbose_name = _("Profil Entreprise")
        verbose_name_plural = _("Profils Entreprise")
        ordering = ['nom_entreprise']

    def __str__(self):
        return f"{self.nom_entreprise} (Entreprise)"