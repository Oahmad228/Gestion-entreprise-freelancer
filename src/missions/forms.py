from django import forms
from .models import Mission

from django import forms
from .models import Mission
from django.utils.translation import gettext_lazy as _

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['titre', 'description', 'budget', 'competences_requises', 'date_limite']
        labels = {
            'titre': _('Titre de la mission'),
            'description': _('Description détaillée'),
            'budget': _('Budget (€)'),
            'competences_requises': _('Compétences requises'),
            'date_limite': _('Date limite'),
        }
        help_texts = {
            'competences_requises': _('Séparez les compétences par des virgules'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_limite': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full px-3 py-2 border rounded'})