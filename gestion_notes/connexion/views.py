from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Etudiant, Responsable, Message, Note, Matiere
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
                
                # On recupere ses notes
                theme = request.session['theme'] if 'theme' in request.session else ''

                etudiant = Etudiant.objects.get(pk=request.session['user_pk'])
                notes_etudiant = Note.objects.filter(etudiant=etudiant)

                nb_messages_non_lus = Message.objects.filter(etudiant=etudiant, lu=False).count()

                # Obtenir les annees passees à l'école
                annees_scolaires = etudiant.years_at_school
                
                # Recuperer l'annee selectionner, depuis la methode GET effectuee
                selected_year = request.GET.get('annee_scolaire', etudiant.annee_scolaire_en_cours)
                
                # filtrer les notes de l'etudiant suivant le selected year
                notes_etudiant_annee = notes_etudiant.filter(annee_scolaire=selected_year)

                class_annee = notes_etudiant_annee.first().classe if notes_etudiant_annee.exists() else None
                
                # On recupere toutes les matieres pour la classe correspondante
                matieres_classe = Matiere.objects.filter(classe=class_annee)
                
                # On range les matieres suivant le semestre
                matieres_semestre1 = matieres_classe.filter(semestre='semestre1')
                matieres_semestre2 = matieres_classe.filter(semestre='semestre2')
                
                # On initialise les dictionnaires pour stocker les notes par matière et semestre
                notes_par_semestre1 = {}
                notes_par_semestre2 = {}

                # On remplit les notes pour les matieres du semestre 1
                for matiere in matieres_semestre1:
                    note1 = notes_etudiant_annee.filter(matiere=matiere, semestre='semestre1', type_note='note1').first()
                    note2 = notes_etudiant_annee.filter(matiere=matiere, semestre='semestre1', type_note='note2').first()
                    notes_par_semestre1[matiere] = [
                        note1.note if note1 else '/', 
                        note2.note if note2 else '/'
                    ]

                #  On remplit les notes pour les matieres du semestre 2
                for matiere in matieres_semestre2:
                    note1 = notes_etudiant_annee.filter(matiere=matiere, semestre='semestre2', type_note='note1').first()
                    note2 = notes_etudiant_annee.filter(matiere=matiere, semestre='semestre2', type_note='note2').first()
                    notes_par_semestre2[matiere] = [
                        note1.note if note1 else '/', 
                        note2.note if note2 else '/'
                    ]
                
                messages.success(request, f'Bienvenue {etudiant.name}')

                return render(request, 'note_etudiant.html', {
                    'etudiant': etudiant,
                    'notes_semestre1': notes_par_semestre1,
                    'notes_semestre2': notes_par_semestre2,
                    'annees_scolaires': annees_scolaires,
                    'selected_year': selected_year,
                    'classe_annee': class_annee,
                    'theme': theme,
                    'nb_message': nb_messages_non_lus
                })

                
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