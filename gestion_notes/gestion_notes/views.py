from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, FileResponse
from urllib.parse import quote  
from django.contrib import messages
import pandas as pd
from connexion.models import Etudiant, Note, Matiere, Classe, Responsable, Message, FichiersJoints
from .forms import NoteUploadForm, MatiereForm, ResponsableForm, EtudiantForm, ClasseForm, EtudiantUpdateForm, OneMessageForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from collections import defaultdict
from .mes_decorateurs import is_login
from django.utils import timezone
from django.contrib.auth.hashers import check_password,make_password
import json
import os
from django.http import HttpResponse
from django.http import Http404


@csrf_exempt
def ajouter_notes(request):
    """
        Cette fonction permet d'ajouter les notes des etudiants
        à partir d'un fichier Excel que l'on va parcourir ligne par ligne
    """
    if request.method == 'POST':
        try:
            data = request.POST  # Utilisation de request.POST pour les données textuelles
            fichier = request.FILES.get('fichier_excel')  # Récupération du fichier excel

            classeName = data.get('classe',"")
            semestre = data.get('semestre', "")
            matiereId = data.get('matiere', "")
            annee_scolaire = data.get('annee_scolaire', "")

            classe = Classe.objects.get(name=classeName)
            matiere = Matiere.objects.get(id=matiereId)

            try:
                df = pd.read_excel(fichier)
                for index, row in df.iterrows():
                    matricule = row['matricule']
                    try:
                        etudiant = Etudiant.objects.get(matricule=matricule)
                    except Etudiant.DoesNotExist:
                        messages.error(request, f"L'étudiant avec le matricule {matricule} n'existe pas.")
                        print("erreur 1")
                        return JsonResponse({'status': 'error', 'message': f"L'étudiant avec le matricule {matricule} n'existe pas."}, status=404)
                    
                    # Création des instances de Note pour chaque type de note
                    if 'note1' in df.columns:
                        Note.objects.create(
                            etudiant=etudiant,
                            matiere=matiere,
                            classe=classe,
                            note=row['note1'],
                            type_note='note1',
                            semestre=semestre,
                            annee_scolaire=annee_scolaire
                        )

                    if 'note2' in df.columns:
                        Note.objects.create(
                            etudiant=etudiant,
                            matiere=matiere,
                            classe=classe,
                            note=row['note2'],
                            type_note='note2',
                            semestre=semestre,
                            annee_scolaire=annee_scolaire
                        )
                request.session['last_activity'] = {'name': 'ajouter_notes', 'time': timezone.now().isoformat()}
                messages.success(request, "Les notes ont été importées avec succès.")
                return JsonResponse({'status': 'success'})
                    
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du fichier: {str(e)}")
                print(f"erreur 2: {str(e)}")
                return JsonResponse({'Erreur lors du traitement': str(e)}, status=500)
        except Exception as e:
            messages.error(request, f"Désolé, une erreur est survenue: {str(e)}")
            print("erreur 3")
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
def charger_notes(request):
    classes = Classe.objects.all()
    matieres = Matiere.objects.all()
    return render(request, 'charger_notes.html', {'classes': classes, 'matieres': matieres})

def filtrer_matieres(request):
    """
        Cette fonction prend en parametre une classe et/ou un semestre contenu dans la requete puis, 
        retourne la liste des matieres correspondantes grace à une reponse json
    """
    classe_name = request.GET.get('classe')
    semestre = request.GET.get('semestre')
    if classe_name and semestre:
        classe = Classe.objects.get(name=classe_name)
        matieres = Matiere.objects.filter(classe=classe, semestre=semestre, active=True)
    elif classe_name:
        classe = Classe.objects.get(name=classe_name)
        matieres = Matiere.objects.filter(classe=classe, active = True)
    elif semestre:
        matieres = Matiere.objects.filter(semestre=semestre, active=True)
    else:
        matieres = Matiere.objects.none()

    data = [{"id":mat.id, "name":mat.name} for mat in matieres]

    return JsonResponse(data, safe=False) # si safe=True, Django s'attend a recevoir un dictionnaire exclusivement. Pour safe=False, on peut passer un objet autre qu'un dictionnaire (une liste, un tuple par exemple)

def ajouter_matiere(request):
    """Ajoute une matière dans la base de données"""
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['last_activity'] = {'name': 'ajouter_matiere', 'time': timezone.now().isoformat()}
            messages.success(request, 'Matière ajoutée avec succès')
            return render(request, 'ajouter_matieres.html', {'form': MatiereForm()})
    else:
        form = MatiereForm()
    return render(request, 'ajouter_matieres.html', {'form': form})

def ajouter_matieres(request):
    """Ajoute des matieres reçues à partir d'un fichier excel"""
    if request.method == 'POST':
        data = request.POST
        fichier = request.FILES.get('fichier_excel')

        className = data.get('classe', "")
        try:
            classe = Classe.objects.get(name=className)
            try:
                df = pd.read_excel(fichier)
                for index, row in df.iterrows():
                    name = row['matiere']
                    semestre = row['semestre']
                    credit = row['credit']
                    Matiere.objects.create(name=name, semestre=semestre, classe=classe, credit=credit)
                request.session['last_activity'] = {'name': 'ajouter_matieres', 'time': timezone.now().isoformat()}
                messages.success(request, "Les matières ont été importées avec succès.")
                return JsonResponse({'status': 'success'})
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du fichier: {str(e)}")
                return JsonResponse({'Erreur lors du traitement': str(e)}, status=500)
        except Exception as e:
            messages.error(request, f"Désolé, une erreur est survenue: {str(e)}")
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
@is_login
def charger_matieres(request):
    """Renvoie sur une page html où sera fourni un fichier excel contenant 
    une liste des matières à ajouter dans la base"""
    try: 
        responsable = Responsable.objects.get(pk=request.session['user_pk'])
        if responsable.filiere == 'AS':
            classes = ['AS1','AS2','AS3']
        elif responsable.filiere == 'ISEP':
            classes = ['ISEP1','ISEP2']
        elif responsable.filiere == 'ISE':
            classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']
    except Responsable.DoesNotExist:
        classes = Classe.objects.none()
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
    return render(request, 'charger_matieres.html', {'classes': classes})

"""
   
    #matieres_etudiant = notes_etudiant.values_list('matiere__name', flat=True).distinct()

    # On recupere uniquement les noms des matieres pour la classe de l'etudiant et on range dans une liste
    #matieres_classe = Matiere.objects.filter(classe=etudiant.classe).values_list('name', flat=True)

    matieres_classe = Matiere.objects.filter(classe=etudiant.classe)

        # Initialiser un defaultdict pour les matières par semestre
    matieres_par_semestre = defaultdict(lambda: defaultdict(lambda: ['/','/']))

   
"""

@is_login
def notes_etudiants(request):
    """
        Cette fonction permet d'afficher les notes des etudiants
        selon la classe et le semestre selectionner par l'utilisateur
    """
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


def ajouter_responsable(request):
    if request.method == 'POST':
        form = ResponsableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Responsable ajouté avec succès')
            return render(request, 'ajouter_responsable.html', {'form': ResponsableForm()})
    else:
        form = ResponsableForm()
    return render(request, 'ajouter_responsable.html', {'form': form})

@is_login
def liste_etudiants(request):

    if request.method == 'GET':

        # On filtre les classes qui correspondent au responsable connecté
        try: 
            responsable = Responsable.objects.get(pk=request.session['user_pk'])
            if responsable.filiere == 'AS':
                classes = ['AS1','AS2','AS3']
            elif responsable.filiere == 'ISEP':
                classes = ['ISEP1','ISEP2']
            elif responsable.filiere == 'ISE':
                classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']
        except Responsable.DoesNotExist:
            classes = Classe.objects.none()
            messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")

        # La liste des statuts possibles
        statuts=["En cours de formation","Diplômé","Exclus"]

        annee=request.GET.get('annee')
        statut=request.GET.get('statut')
        classe=request.GET.get('classe')

        selected_classe = classe
        selected_annee = annee
        selected_statut = statut

        all_notes = Note.objects.all()
        annees=[note.annee_scolaire for note in all_notes ]
        annees = list(set(annees))

        theme = request.session['theme'] if 'theme' in request.session else ''
        cycle1 = ['AS1','AS2','ISEP1','ISEP2','ISEP3','ISE1-eco','ISE1-maths','ISE2']
        responsable = Responsable.objects.get(pk=request.session['user_pk'])

        if not (annee or statut or classe ):
            etudiants = responsable.get_etudiants_by_filiere()
            
        elif annee and statut and classe:
            note_filter=Note.objects.filter(annee_scolaire=annee,classe__name=classe)
            etudiant_filter=[note.etudiant for note in note_filter]
            etudiant_filter=list(set(etudiant_filter))
            etudiants_resp = responsable.get_etudiants_by_filiere()
            etudiants_p=[]
            for etudiant in etudiant_filter:
                if etudiant.statut==statut:
                    etudiants_p.append(etudiant)

            for classe_responsable, eleves in etudiants_resp.items():
                if classe_responsable==classe:
                    etudiants={classe: etudiants_p}
                    break

            
        elif annee and classe:
            note_filter=Note.objects.filter(annee_scolaire=annee,classe__name=classe)
            etudiant_filter=[note.etudiant for note in note_filter]
            etudiants_p=list(set(etudiant_filter))
            etudiants_resp = responsable.get_etudiants_by_filiere()
            for classe_responsable, eleves in etudiants_resp.items():
                if classe_responsable==classe:
                    etudiants={classe: etudiants_p}
                    break

        elif annee and statut:
            note_filter=Note.objects.filter(annee_scolaire=annee)
            etudiant_filter=[note.etudiant for note in note_filter]
            etudiant_filter=list(set(etudiant_filter))
            etudiants_resp = responsable.get_etudiants_by_filiere()
            etudiants_p=[]
            for etudiant in etudiant_filter:
                if etudiant.statut==statut:
                    etudiants_p.append(etudiant)

            for classe_responsable, eleves in etudiants_resp.items():
                liste_etudiants=[]
                for etudiant in etudiants_p:
                    if classe_responsable==etudiant.classe.name:
                        liste_etudiants.append(etudiant)
                etudiants_resp[classe_responsable]=liste_etudiants

            etudiants=etudiants_resp

        elif statut and classe:
            etudiants_resp = responsable.get_etudiants_by_filiere()
            for classe_responsable, eleves in etudiants_resp.items():
                if classe_responsable == classe:
                    liste_etudiants=[]
                    for etudiant in eleves:
                        if etudiant.statut==statut:
                            liste_etudiants.append(etudiant)
                    etudiants_resp={classe_responsable:liste_etudiants}
                    break

            etudiants=etudiants_resp
        

        elif annee:
            note_filter=Note.objects.filter(annee_scolaire=annee)
            etudiant_filter=[note.etudiant for note in note_filter]
            etudiant_filter=list(set(etudiant_filter))
            etudiants_resp = responsable.get_etudiants_by_filiere()
                                 

            for classe_responsable, eleves in etudiants_resp.items():
                liste_etudiants=[]
                for etudiant in etudiant_filter:
                    if classe_responsable==etudiant.classe.name:
                        liste_etudiants.append(etudiant)
                etudiants_resp[classe_responsable]=liste_etudiants

            etudiants=etudiants_resp

        elif statut:
            etudiants_resp = responsable.get_etudiants_by_filiere()
            for classe_responsable, eleves in etudiants_resp.items():
                liste_etudiants=[]
                for etudiant in eleves:
                    if etudiant.statut==statut:
                        liste_etudiants.append(etudiant)
                etudiants_resp[classe_responsable]=liste_etudiants

            etudiants=etudiants_resp
            
    return render(request, 'liste_etudiants.html', {'etudiants': etudiants,'theme':theme,'cycle1':cycle1,'statuts':statuts,'classes':classes,'annees':annees,'selected_annee':selected_annee,'selected_classe':selected_classe,'selected_statut':selected_statut})


@is_login
def Accueil_responsable(request):
    theme = request.session['theme'] if 'theme' in request.session else ''
    responsable = Responsable.objects.get(id = request.session['user_pk'])
    classes = []
    if responsable.filiere == 'AS':
        classes=['AS1','AS2','AS3']
    elif responsable.filiere == 'ISEP':
        classes = ['ISEP1','ISEP2']
    elif responsable.filiere == 'ISE':
        classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']

    last_login = responsable.last_login
    last_activity = request.session.get('last_activity')
    return render(request, 'responsable.html',{'classes':classes,'last_login':last_login,'last_activity':last_activity,'theme':theme})

@is_login
def ajouter_etudiant(request):
    """Ajoute un étudiant dans la base"""
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            matricule = form.cleaned_data['matricule']
            if Etudiant.objects.filter(matricule=matricule).exists():
                messages.error(request, f"L'étudiant avec le matricule {matricule} existe déjà.")
                return render(request, 'ajouter_etudiant.html', {'form': form})
            else:
                form.save()
                request.session['last_activity'] = {'name':'ajouter_etudiant','time':timezone.now().isoformat()}
                messages.success(request, f"Etudiant {form.cleaned_data['name']} ajouté avec succès !!!")
                return render(request, 'ajouter_etudiant.html', {'form': EtudiantForm()})
        else:
            messages.error(request, form.errors)
            return render(request, 'ajouter_etudiant.html', {'form': form})
    else:
        form = EtudiantForm()
        return render(request, 'ajouter_etudiant.html', {'form': form})

@is_login
def charger_etudiants(request):
    """Renvoie sur une page html où sera fourni un fichier excel contenant 
    une liste d'étudiants à ajouter dans la base"""
    try: 
        responsable = Responsable.objects.get(pk=request.session['user_pk'])
        if responsable.filiere == 'AS':
            classes = ['AS1','AS2','AS3']
        elif responsable.filiere == 'ISEP':
            classes = ['ISEP1','ISEP2']
        elif responsable.filiere == 'ISE':
            classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']
    except Responsable.DoesNotExist:
        classes = Classe.objects.none()
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
    return render(request, 'charger_etudiants.html', {'classes': classes})


def ajouter_etudiants(request):
    """
        Cette fonction permet d'ajouter les étudiants dans la base de données
        à partir d'un fichier Excel que l'on va parcourir ligne par ligne
    """
    if request.method == 'POST':
        try:
            data = request.POST
            fichier = request.FILES.get('fichier_excel')

            classeName = data.get('classe', "")
            annee_inscription = data.get('annee_inscription', "")

            classe = Classe.objects.get(name=classeName)

            try:
                df = pd.read_excel(fichier)
                for index,row in df.iterrows():
                    matricule = row['matricule']

                    if Etudiant.objects.filter(matricule=matricule).exists():
                        messages.error(request, f"L'étudiant avec le matricule {matricule} existe déjà.")
                        return JsonResponse({'status': 'error', 'message': f"L'étudiant avec le matricule {matricule} existe déjà."}, status=404)
                    else:
                        Etudiant.objects.create(
                            matricule=matricule,
                            name=row['nom'],
                            classe=classe,
                            email=row['email'],
                            password=row['password'],
                            annee_inscription=annee_inscription
                        )
                request.session['last_activity'] = {'name':'ajouter_etudiants','time':timezone.now().isoformat()}
                messages.success(request, "Les étudiants ont été ajoutés avec succès.")
                return JsonResponse({'status': 'success'})
            except Exception as e:
                messages.error(request, f"Erreur lors du traitement du fichier: {str(e)}")
                return JsonResponse({'Erreur lors du traitement': str(e)}, status=500)
        except Exception as e:
            messages.error(request, f"Désolé, une erreur est survenue: {str(e)}")
            return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    
def modifier_matiere(request):
    """
        Cette fonction permet de modifier une matière spécifier lorsque la méthode est de type POST
        Pour les methodes GET, elle va filtrer la base et renvoyer les matières correspondantes, en fonction 
        de informations qui seront fournies par la méthode GET
    """
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        matiere = Matiere.objects.get(name=form.data['name'],classe = form.data['classe'])
        form2 = MatiereForm(request.POST, instance=matiere)
        if form2.is_valid():
            form2.save()
            request.session['last_activity'] = {'name':'modifier_matiere','time':timezone.now().isoformat()}
            messages.success(request, "Matière modifiée avec succès.")
            # Rediriger pour éviter un rechargement du POST
            return redirect('modifier_matiere')  
        else:
            # Si le formulaire n'est pas valide, on renvoie la même page avec les erreurs
            try: 
                responsable = Responsable.objects.get(pk=request.session['user_pk'])
                if responsable.filiere == 'AS':
                    classes = ['AS1','AS2','AS3']
                elif responsable.filiere == 'ISEP':
                    classes = ['ISEP1','ISEP2']
                elif responsable.filiere == 'ISE':
                    classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']
                
                semestres = [{'value':'semestre1','name':'Semestre 1'},
                            {'value':'semestre2','name':'Semestre 2'}]
            except Responsable.DoesNotExist:
                classes = Classe.objects.none()
                messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
                return render(request, 'modifier_matiere.html', {'classes': classes})
            else:   
                messages.error(request, "Erreur dans la modification de la matière.")
                return render(request,'modifier_matiere.html',{'form':form,'classes':classes,'semestres':semestres})
                
    elif request.method == 'GET':
        try: 
            responsable = Responsable.objects.get(pk=request.session['user_pk'])
            if responsable.filiere == 'AS':
                classes = ['AS1','AS2','AS3']
            elif responsable.filiere == 'ISEP':
                classes = ['ISEP1','ISEP2']
            elif responsable.filiere == 'ISE':
                classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']
            
            semestres = [{'value':'semestre1','name':'Semestre 1'},
                        {'value':'semestre2','name':'Semestre 2'}]
        except Responsable.DoesNotExist:
            classes = Classe.objects.none()
            messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
            return render(request, 'modifier_matiere.html', {'classes': classes})
        else:
            id_matiere = request.GET.get('id_matiere','')
            matiere = Matiere.objects.get(id=id_matiere) if id_matiere else None
            selected_matiere = (matiere.id if matiere else '')

            classe = request.GET.get('classe', '')
            classe = Classe.objects.get(name=classe) if classe else None
            selected_classe = (classe.name if classe else '')

            semestre = request.GET.get('semestre', '') 
            selected_semestre = semestre if semestre else ''

            if semestre and classe:
                matieres = Matiere.objects.filter(classe=classe, semestre=semestre, active=True)
            elif classe:
                matieres = Matiere.objects.filter(classe=classe, active=True)
            #elif semestre:
                #matieres = Matiere.objects.filter(semestre=semestre, active=True)
            else:
                matieres = Matiere.objects.none()
               
            # On charge les informations avant d'envoyer le formulaire
            form = MatiereForm(instance=matiere) if matiere else MatiereForm()

            return render(request, 'modifier_matiere.html', {'form':form,'matiere': matiere, 'classes': classes,'semestres':semestres, 'matieres': matieres,'selected_matiere':selected_matiere,'selected_classe':selected_classe,'selected_semestre':selected_semestre})
    
    # Au cas où la méthode n'est ni POST ni GET
    return render(request, 'modifier_matiere.html',{'form':MatiereForm()})

def ajouter_classe(request):
    """Cette fonction permet d'ajouter une nouvelle classe dans la base de données"""
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            classeName = form.cleaned_data['name']
            for classe in Classe.objects.all():
                if classe.name.lower() == classeName.lower():
                    messages.error(request, 'Cette classe existe déjà')
                    return render(request, 'ajouter_classe.html', {'form': form})
            form.save()
            request.session['last_activity'] = {'name':'ajouter_classe','time':timezone.now().isoformat()}
            messages.success(request, 'Classe ajoutée avec succès')
            return render(request, 'ajouter_classe.html', {'form': ClasseForm()})
        else:
            messages.error(request, form.errors)
            return render(request, 'ajouter_classe.html', {'form': form})
    else:
        form = ClasseForm()
    return render(request, 'ajouter_classe.html', {'form': form})

@is_login
def detail_etudiant(request, matricule):
    """Cette fonction permet d'afficher les informations d'un étudiant spécifique"""
    
    etudiant = Etudiant.objects.get(pk=matricule)
    notes_etudiant = Note.objects.filter(etudiant=etudiant)

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

    return render(request, 'detail_etudiant.html', {
        'etudiant': etudiant,
        'notes_semestre1': notes_par_semestre1,
        'notes_semestre2': notes_par_semestre2,
        'annees_scolaires': annees_scolaires,
        'selected_year': selected_year,
        'classe_annee': class_annee
    })

@is_login
def modifier_etudiant(request,matricule):
    """
        Cette fonction permet de modifier un étudiant spécifié lorsque la méthode est de type POST
    """
    if request.method == 'POST':
        form = EtudiantUpdateForm(request.POST, instance=Etudiant.objects.get(pk=matricule))
        if form.is_valid():
            etudiant = Etudiant.objects.get(pk=matricule)
            password = form.data['password']
            if not check_password(password, etudiant.password):
                etudiant.password = make_password(password)
            form.save()
            request.session['last_activity'] = {'name':'modifier_etudiant','time':timezone.now().isoformat()}
            messages.success(request, f'Etudiant immatriculé {matricule} modifié avec succès')
            return redirect('detail_etudiant', matricule=matricule)
        else:
            messages.error(request, form.errors)
            return render(request, 'modifier_etudiant.html', {'form': form})
    else:
        form = EtudiantUpdateForm(instance=Etudiant.objects.get(pk=matricule))
        return render(request, 'modifier_etudiant.html', {'form': form})
    
def modifier_responsable(request,id_responsable):
    if request.method == 'POST':
        try:
            responsable = Responsable.objects.get(pk=id_responsable)
            form = ResponsableForm(request.POST, instance=responsable)
            if form.is_valid():
                password = form.data['password']
                if not check_password(password, responsable.password):
                    responsable.password = make_password(password)
                form.save()
                request.session['last_activity'] = {'name':'modifier_responsable','time':timezone.now().isoformat()}
                messages.success(request, f'Responsable immatriculé {id_responsable} modifié avec succès')
                return redirect('accueil_responsable')
            else:
                messages.error(request, form.errors)
                return render(request, 'modifier_responsable.html', {'form': form})
        except Responsable.DoesNotExist:
            messages.error(request, "Aucun responsable avec cet identifiant dans la base.")
            return redirect('accueil_responsable')
    else:
        try:
            responsable = Responsable.objects.get(pk=id_responsable)
            form = ResponsableForm(instance=responsable)
            return render(request, 'modifier_responsable.html', {'form': form})
        except Responsable.DoesNotExist:
            messages.error(request, "Aucun responsable avec cet identifiant dans la base.")
            return redirect('accueil_responsable')
        
def set_theme(request):
    """Permet de stocker le  thème appliqué dans la session"""
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        request.session['theme'] = theme
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def send_message(request, matricule):
    responsable = Responsable.objects.get(pk=request.session['user_pk'])
    etudiant = Etudiant.objects.get(pk=matricule)
    if request.method == 'POST':
        form = OneMessageForm(request.POST)
        fichiers = request.FILES.getlist('fichier')
        if form.is_valid():
            message = form.save(commit=False)
            message.etudiant = Etudiant.objects.get(pk=matricule)
            message.responsable = responsable
            message.save()
            if fichiers:
                for fichier in fichiers:
                    FichiersJoints.objects.create(message=message, fichier=fichier)
            messages.success(request, 'Message envoyé avec succès')
            return render(request, 'send_message.html', {'form': OneMessageForm(),'etudiant':etudiant})
        else:
            messages.error(request, form.errors)
            return render(request, 'send_message.html', {'form': form, 'etudiant':etudiant})
    else:
        form = OneMessageForm()
        return render(request, 'send_message.html', {'form': form,'etudiant':etudiant})

@is_login
def delete_etudiant(request, matricule):
    try:
        etudiant = Etudiant.objects.get(pk=matricule)
        etudiant.delete()
        messages.success(request, f'Etudiant immatriculé {matricule} supprimé avec succès')
    except Etudiant.DoesNotExist:
        messages.error(request, "Aucun étudiant avec cet identifiant dans la base.")
    return redirect('liste_etudiants')

def mes_messages(request):
    theme = request.session['theme'] if 'theme' in request.session else ''
    etudiant = Etudiant.objects.get(pk=request.session['user_pk'])
    messages = Message.objects.filter(etudiant=etudiant,visible_etudiant=True).order_by('-created_at')
    nb_messages_non_lus = messages.filter(lu=False).count()

    return render(request, 'mes_messages.html', {'mes_messages': messages, 'nb_message':nb_messages_non_lus,'theme':theme})

def delete_message(request, message_id):
    """L'étudiant n'étant pas habileté à supprimer un message dans la base
    on va juste rendre le message qu'il souhaite supprimer invisible sur son interface"""
    try:
        message = Message.objects.get(pk=message_id)
        message.visible_etudiant = False
        message.save()
        messages.success(request, 'Message supprimé avec succès')
    except Message.DoesNotExist:
        messages.error(request, "Aucun message avec cet identifiant dans la base.")
    return redirect('mes_messages')

def ouvrir_fichier(request, fichier_joint_id):
    """
        Cette fonction permet d'ouvrir un fichier (si le navigateur le permet car pour certains types
        notamment les fichiers excel, certains navigateurs autorisent uniquement le telechargement)
    """
    try:
        fichier_joint = FichiersJoints.objects.get(pk=fichier_joint_id)
       
        file_path = fichier_joint.fichier.path

        # Définir le type de contenu en fonction de l'extension du fichier
        if file_path.endswith('.pdf'):
            content_type = 'application/pdf'
        elif file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            content_type = 'image/*'
        elif file_path.endswith('.txt'):
            content_type = 'text/plain'
        else:
            content_type = 'application/octet-stream'  # Type par défaut pour les fichiers binaires

        response = FileResponse(fichier_joint.fichier.open(), content_type=content_type)
        response['content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    
        return response
           
    except FichiersJoints.DoesNotExist:
        messages.error(request, "Aucun fichier avec cet identifiant dans la base.")
        Http404("Aucun fichier avec cet identifiant dans la base.")

def enregistrer_fichier(request, fichier_joint_id):
    try:
        fichier_joint = FichiersJoints.objects.get(pk=fichier_joint_id)
        
        file_path = fichier_joint.fichier.path
        response = FileResponse(open(file_path, 'rb'))
        # quote permet de gerer les caractères spéciaux dans le nom du fichier
        response['content-Disposition'] = f'attachement; filename="{quote(os.path.basename(file_path))}"'
        return response
            
       
    except FichiersJoints.DoesNotExist:
        messages.error(request, "Aucun fichier avec cet identifiant dans la base.")
        Http404("Aucun fichier avec cet identifiant dans la base.")

def turn_to_lu(request, message_id):
    if request.method == 'GET':
        try:
            message = Message.objects.get(pk=message_id)
            message.lu = True
            message.save()
            nb_messages_non_lus = Message.objects.filter(etudiant=message.etudiant, lu=False).count()
            return JsonResponse({'status': 'success','nb_messages_non_lus':nb_messages_non_lus})
        except Message.DoesNotExist:
            return JsonResponse({'status': 'error','message':'Aucun message avec cet identifiant dans la base'}, status=404)
        
    else:
        return JsonResponse({'status':'error','message': 'Méthode non autorisée'}, status=405)
    
def messages_responsable(request):
    """Il s'agit de la view pour la page messages de 
    l'interface des responsables"""
    theme = request.session['theme'] if 'theme' in request.session else ''

    responsable = Responsable.objects.get(pk=request.session['user_pk'])
    messages = Message.objects.filter(responsable=responsable,visible_responsable=True).order_by('-created_at')
    return render(request, 'messages.html',{'messages_envoyes':messages,'theme':theme})

def responsable_cacher_message(request, message_id):
    """Cette fonction rend un message non disponible sur l'interface du responsable"""
    try:
        message = Message.objects.get(pk=message_id)
        message.visible_responsable = False
        message.save()
    except Message.DoesNotExist:
        messages.error(request, "Aucun message avec cet identifiant dans la base.")
    return redirect('messages')

def responsable_delete_message(request, message_id):
    """Cette fonction supprime le message spécifié dans la base"""
    try:
        message = Message.objects.get(pk=message_id)
        message.delete()
        messages.success(request, 'Message supprimé avec succès')
    except Message.DoesNotExist:
        messages.error(request, "Aucun message avec cet identifiant dans la base.")
    return redirect('messages')


def new_message(request):
    theme = request.session['theme'] if 'theme' in request.session else '' 
    if request.method == 'GET':
        try:
            classe_id = request.GET.get('classe_id')
            if classe_id:
                etudiants = Etudiant.objects.filter(classe__id=classe_id)
                selected_class = Classe.objects.get(pk=classe_id)
                # Convertir les objets Etudiant en dictionnaire (liste d'étudiants sérialisée)
                #etudiants_data = [{'id': etudiant.id, 'name': etudiant.name} for etudiant in etudiants]
                #return JsonResponse({'status': 'success','etudiants':etudiants_data})
            else:
                etudiants = Etudiant.objects.none()
                selected_class = None
            responsable = Responsable.objects.get(pk=request.session['user_pk'])
            if responsable.filiere == 'AS':
                classes = ['AS1','AS2','AS3']
            elif responsable.filiere == 'ISEP':
                classes = ['ISEP1','ISEP2']
            elif responsable.filiere == 'ISE':
                classes = ['ISEP3','ISE1-eco','ISE1-maths','ISE2','ISE3']

            classes = Classe.objects.filter(name__in=classes)    
            return render(request, 'new_message.html', {'classes': classes,'etudiants':etudiants,'selected_class':selected_class,'theme':theme})
        
        except Responsable.DoesNotExist:
            classes = Classe.objects.none()
            messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
            return render(request, 'new_message.html', {'classes': classes})
    else:
        responsable = Responsable.objects.get(pk=request.session['user_pk'])
        sujet = request.POST.get('sujet')
        contenu = request.POST.get('contenu')
        fichiers = request.FILES.getlist('fichier') if 'fichier' in request.FILES else None
        classe_id = request.POST.get('classe_selected')
        classe = Classe.objects.get(pk=classe_id) if classe_id else None
        etudiants_selectionnes_id = request.POST.getlist('etudiants_selected') if 'etudiants_selected' in request.POST else None
        if etudiants_selectionnes_id:
            for etudiant_id in etudiants_selectionnes_id:
                etudiant = Etudiant.objects.get(pk=etudiant_id)
                message = Message.objects.create(responsable=responsable, etudiant=etudiant, sujet=sujet, message=contenu)
                if fichiers:
                    for fichier in fichiers:
                        FichiersJoints.objects.create(message=message, fichier=fichier)
            messages.success(request, 'Message envoyé avec succès au groupe d\'étudiants sélectionné')
        else:
            etudiants = Etudiant.objects.filter(classe=classe)
            for etudiant in etudiants:
                message = Message.objects.create(responsable=responsable, etudiant=etudiant, sujet=sujet, message=contenu)
                if fichiers:
                    for fichier in fichiers:
                        FichiersJoints.objects.create(message=message, fichier=fichier)
            messages.success(request, 'Message envoyé avec succès à toute la classe')

        return redirect('new_message')
        
def Upgrade_etudiant(request,matricule):
    try:
        etudiant = Etudiant.objects.get(pk=matricule) 
        etudiant.Upgrade_etudiant
        messages.success(request,f"étudiant envoyé en {etudiant.classe} avec le statut {etudiant.statut}") 
        return redirect('liste_etudiants')
    except Etudiant.DoesNotExist:
        messages.error(request, "Aucun étudiant avec cet identifiant dans la base.")
        return redirect('liste_etudiants')
    
