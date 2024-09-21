from django.shortcuts import redirect
from functools import wraps

def is_login(function):
    @wraps(function)  # Assure que le wrapper ait même nom et même docstring que la fonction originale
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_pk'):
            return redirect('connexion')  # On redirige sur la page de connexion si non authentifié
        else:
            response = function(request, *args, **kwargs)  # On appelle la fonction originale
            
            # Verifie si la view retourne une reponse http valide
            if response is None:
                raise ValueError("The view did not return an HttpResponse object.")
            
            return response
    return wrapper
