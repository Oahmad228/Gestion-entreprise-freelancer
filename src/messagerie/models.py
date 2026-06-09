from django.db import models
from users.models import Utilisateur
from missions.models import Mission, Candidature

class Conversation(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Utilisateur)
    date_creation = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE)
    expediteur = models.ForeignKey('users.Utilisateur', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_envoi']