"""
URL configuration for gestion_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('connexion.urls')),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('responsable/charger_notes/',views.charger_notes,name='charger_notes'),
    path('filtrer-matieres/', views.filtrer_matieres, name='filtrer_matieres'),
    path('responsable/ajouter_notes/', views.ajouter_notes, name='ajouter_notes'),
    path('responsable/ajouter_matiere/',views.ajouter_matiere,name='ajouter_matiere'),
    path('etudiant/mes_notes/', views.notes_etudiants, name='notes_etudiants'),
    path('etudiant/Messagerie/',views.mes_messages,name='mes_messages'),
    path('etudiant/Messagerie/message_to_lu/<int:message_id>/',views.turn_to_lu,name='lire_message'),
    path('etudiant/delete_message/<int:message_id>/',views.delete_message, name='delete_message'),
    path('etudiant/ouvrir_fichier/<int:fichier_joint_id>/',views.ouvrir_fichier, name='ouvrir_fichier'),
    path('etudiant/enregistrer_fichier/<int:fichier_joint_id>/',views.enregistrer_fichier, name='enregistrer_fichier'),
    path('ajouter_responsable/', views.ajouter_responsable, name='ajouter_responsable'),
    path('responsable/modifier/gsdfjghgldkfjfuhg<int:id_responsable>lfhxtvdpeirut/',views.modifier_responsable,name='modifier_responsable'),
    path('responsable/liste_etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('responsable/accueil/',views.Accueil_responsable,name='accueil_responsable'),
    path('responsable/ajouter_etudiant/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('responsable/charger_etudiants/', views.charger_etudiants, name='charger_etudiants'),
    path('responsable/ajouter_etudiants/', views.ajouter_etudiants, name='ajouter_etudiants'),
    path('responsable/charger_matieres/', views.charger_matieres, name='charger_matieres'),
    path('responsable/ajouter_matieres/', views.ajouter_matieres, name='ajouter_matieres'),
    path('responsable/modifier_matiere/', views.modifier_matiere, name='modifier_matiere'),
    path('responsable/ajouter_classe/', views.ajouter_classe, name='ajouter_classe'),
    path('responsable/etudiant/detail/<str:matricule>/',views.detail_etudiant, name='detail_etudiant'),
    path('responsable/etudiant/upgrade/<str:matricule>/',views.Upgrade_etudiant, name='upgrade_etudiant'),
    path('responsable/classe/upgrade/',views.Upgrade_classe, name='upgrade_classe'),
    path('responsable/etudiant/degrade/<str:matricule>/',views.Degrade_etudiant, name='degrade_etudiant'),
    path('responsable/etudiant/modifier/<str:matricule>/', views.modifier_etudiant, name='modifier_etudiant'),
    path('responsable/send_message/etudiant/<str:matricule>', views.send_message, name='send_message'),
    path('responsable/etudiant/delete/<str:matricule>/', views.delete_etudiant, name='delete_etudiant'),
    path('responsable/messages/',views.messages_responsable,name='messages'),
    path('responsable/delete_message/<int:message_id>/',views.responsable_delete_message, name='responsable_delete_message'),
    path('responsable/cacher_message/<int:message_id>/',views.responsable_cacher_message, name='responsable_cacher_message'),
    path('responsable/new_message/',views.new_message,name='new_message'),
    path('responsable/notes_etudiants/', views.Responsable_notes, name='responsable_notes'),
    path('responsable/notes_etudiants/telecharger_recapitulatif/', views.modifier_et_telecharger_excel, name='telecharger_recap'),
   
    
   
    
]
