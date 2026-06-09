from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView
from missions.models import Candidature
from .models import Conversation, Message
from .forms import MessageForm


@login_required
def liste_conversations(request):
    conversations = Conversation.objects.filter(
        participants=request.user
    ).prefetch_related(
        'participants',
        'message_set'
    ).order_by('-date_creation')

    return render(request, 'messagerie/liste.html', {
        'conversations': conversations,
        'unread_messages': request.user.message_recus.filter(lu=False).count()
    })

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)

    # Vérification plus robuste des permissions
    allowed_participants = conversation.mission.get_participants()
    if request.user not in allowed_participants:
        raise PermissionDenied("Vous n'avez pas accès à cette conversation")

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.expediteur = request.user
            message.save()
            return redirect('messagerie:detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    # Marquer les messages comme lus
    Message.objects.filter(
        conversation=conversation,
        lu=False
    ).exclude(
        expediteur=request.user
    ).update(lu=True)

    return render(request, 'messagerie/conversation.html', {
        'conversation': conversation,
        'form': form,
        'messages': conversation.message_set.all().order_by('date_envoi')
    })


@login_required
def demarrer_conversation(request, mission_id, candidature_id):
    # Vérifier que l'utilisateur a le droit de démarrer la conversation
    candidature = get_object_or_404(Candidature, id=candidature_id, mission_id=mission_id)

    if request.user != candidature.mission.entreprise and request.user != candidature.freelance:
        return redirect('missions:listes')

    conversation, created = Conversation.objects.get_or_create(
        mission=candidature.mission,
        defaults={'date_creation': timezone.now()}
    )

    if created:
        conversation.participants.add(candidature.freelance, candidature.mission.entreprise)

    return redirect('messagerie:detail', conversation_id=conversation.id)