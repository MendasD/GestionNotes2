from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Etudiant, Responsable, Message
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def connexion(request):
    return render(request, 'connexion.html')

def Login(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')

        if Etudiant.objects.filter(matricule=matricule).exists():
            etudiant = Etudiant.objects.get(matricule=matricule)
            if etudiant.check_password(password):
                
                request.session['user_pk'] = etudiant.pk
                request.session['last_activity'] = {'name':'connexion','time':timezone.now().isoformat()}
                nb_messages_non_lus = Message.objects.filter(etudiant=etudiant).filter(lu=False).count()
                messages.success(request, f'Bienvenue {etudiant.name}')
                return render(request, 'note_etudiant.html', {'nb_message': nb_messages_non_lus})
            else:
                error_message = "Mot de passe incorrect"
                return render(request, 'connexion.html', {'error_message': error_message})
        elif Responsable.objects.filter(email=matricule).exists():
            responsable = Responsable.objects.get(email=matricule)
            if responsable.check_password(password):
                
                request.session['user_pk'] = responsable.pk
                request.session['last_activity'] = {'name':'connexion','time':timezone.now().isoformat()}
                messages.success(request, f'Bienvenue {responsable.name}')
                return redirect('accueil_responsable')
            else:
                error_message = "Mot de passe incorrect"
                return render(request, 'connexion.html', {'error_message': error_message})
        else:
            error_message = "Matricule ou email non enregistré"
            return render(request, 'connexion.html', {'error_message': error_message})
    else:
        return render(request, 'connexion.html')
    
def logout(request):
    #del request.session['user_pk']
    try:
        user = Etudiant.objects.get(pk=request.session['user_pk'])
    except Etudiant.DoesNotExist:
        try:
            user = Responsable.objects.get(pk=request.session['user_pk'])
        except Responsable.DoesNotExist:
            user = None
    if user:
        user.update_last_login()
    
    # On vide la session
    request.session.flush()
    return redirect('connexion')