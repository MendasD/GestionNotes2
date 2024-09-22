from django import forms
from connexion.models import Matiere, Responsable, Etudiant, Classe, Message, FichiersJoints
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class NoteUploadForm(forms.Form):
    fichier_excel = forms.FileField(label="Choisir un fichier Excel")
    matiere = forms.ModelChoiceField(queryset=Matiere.objects.all(), label="Matière")
    semestre = forms.ChoiceField(
        choices=[
            ('semestre1', 'Semestre 1'),
            ('semestre2', 'Semestre 2')
        ],
        label="Semestre"
    )

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = '__all__'

class ResponsableForm(forms.ModelForm):
    class Meta:
        model = Responsable
        exclude = ('last_login',)
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        responsable = super().save(commit=False)
        responsable.set_password(self.data['password'])
        if commit:
            responsable.save()
        return responsable
    
class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('statut','annee_scolaire_en_cours','last_login','password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        etudiant = super().save(commit=False)
        etudiant.set_password(self.data['password'])
        if commit:
            etudiant.save()
        return etudiant

class EtudiantUpdateForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('last_login','matricule')
        widgets = {
            'password': forms.PasswordInput(),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre le champ password facultatif
        self.fields['password'].required = False

    def save(self, commit=True):
        etudiant = super().save(commit=False) # obtenir une instance du modèle associée au formulaire sans la sauvegarder immédiatement
        if self.data.get('password'):
            etudiant.set_password(self.data['password'])
        
        if commit:
            etudiant.save()
        return etudiant

    def clean_password(self):
        password = self.data.get('password')
        if not password:
            # Retourne l'ancien password si un nouveau n'est pas spécifié
            return self.instance.password
        return password
    

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = '__all__'

class OneMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sujet','message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
        }

