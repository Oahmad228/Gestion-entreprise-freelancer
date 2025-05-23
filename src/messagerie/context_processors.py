from .models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        return {
            'unread_messages': Message.objects.filter(
                conversation__participants=request.user,
                lu=False
            ).exclude(expediteur=request.user).count()
        }
    return {}