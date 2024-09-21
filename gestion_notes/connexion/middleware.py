from django.utils import timezone
from datetime import timedelta

class UpdateLastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')  

        if user_id:
            from .models import Etudiant, Responsable  

            try:
                user = Etudiant.objects.get(pk=user_id)
            except Etudiant.DoesNotExist:
                try:
                    user = Responsable.objects.get(pk=user_id)
                except Responsable.DoesNotExist:
                    user = None

            if user:
                last_activity = request.session.get('last_activity', {})
                now = timezone.now()

                # Extraire les informations du dictionnaire
                last_activity_name = last_activity.name
                last_activity_time = last_activity.time

                if last_activity_time:
                    last_activity_time = timezone.datetime.fromisoformat(last_activity_time)

                    # Mettre à jour last_login si plus de 10 minutes se sont écoulées
                    if now - last_activity_time > timedelta(minutes=1):
                        user.last_login = now
                        user.save()

                # Mettre à jour la session avec l'heure actuelle de l'activité
                request.session['last_activity'] = {
                    'name': last_activity_name,  
                    'time': now.isoformat()
                }

        response = self.get_response(request)
        return response
