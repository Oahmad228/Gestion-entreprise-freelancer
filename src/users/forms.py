from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Utilisateur, Freelance, Entreprise


class FreelanceProfileForm(forms.ModelForm):
    class Meta:
        model = Freelance
        fields = ['bio', 'competences', 'tarif_horaire', 'lien_portfolio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'competences': forms.TextInput(attrs={'placeholder': 'Séparez par des virgules'}),
        }

class EntrepriseProfileForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        fields = ['nom_entreprise', 'description', 'site_web', 'email_contact']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email ou nom d'utilisateur"),
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    error_messages = {
        'invalid_login': _(
            "Veuillez entrer un email/nom d'utilisateur et mot de passe valides."
        ),
        'inactive': _("Ce compte est inactif."),
    }


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    type_utilisateur = forms.ChoiceField(
        label=_("Type de compte"),
        choices=Utilisateur.TypeUtilisateur.choices,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'type_utilisateur', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise ValidationError(_("Un utilisateur avec cet email existe déjà."))
        return email