from django import forms
from connexion.models import Matiere, Responsable, Etudiant, Classe, Message, FichiersJoints
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


SEXE_CHOICES = [
    ('M', 'Masculin'),
    ('F', 'Féminin'),
]

NATIONALITY_CHOICES = [
    ('afrique_du_sud', 'Sud-Africaine'),
    ('algerie', 'Algérienne'),
    ('angola', 'Angolaise'),
    ('benin', 'Béninoise'),
    ('botswana', 'Botswanaise'),
    ('burkina_faso', 'Burkinabé'),
    ('burundi', 'Burundaise'),
    ('cameroun', 'Camerounaise'),
    ('cap_vert', 'Cap-Verdienne'),
    ('comores', 'Comorienne'),
    ('congo_brazzaville', 'Congolaise (Brazzaville)'),
    ('congo_kinshasa', 'Congolaise (Kinshasa)'),
    ('cote_d_ivoire', 'Ivoirienne'),
    ('djibouti', 'Djiboutienne'),
    ('egypte', 'Égyptienne'),
    ('erythree', 'Érythréenne'),
    ('eswatini', 'Swazie'),
    ('ethiopie', 'Éthiopienne'),
    ('gabon', 'Gabonaise'),
    ('gambie', 'Gambienne'),
    ('ghana', 'Ghanéenne'),
    ('guinee', 'Guinéenne'),
    ('guinee_bissau', 'Bissau-Guinéenne'),
    ('guinee_equatoriale', 'Équatoguinéenne'),
    ('kenya', 'Kényane'),
    ('lesotho', 'Lesothane'),
    ('liberia', 'Libérienne'),
    ('libye', 'Libyenne'),
    ('madagascar', 'Malgache'),
    ('malawi', 'Malawite'),
    ('mali', 'Malienne'),
    ('maroc', 'Marocaine'),
    ('maurice', 'Mauricienne'),
    ('mauritanie', 'Mauritanienne'),
    ('mozambique', 'Mozambicaine'),
    ('namibie', 'Namibienne'),
    ('niger', 'Nigérienne'),
    ('nigeria', 'Nigériane'),
    ('ouganda', 'Ougandaise'),
    ('rwanda', 'Rwandaise'),
    ('sao_tome_et_principe', 'Santoméenne'),
    ('senegal', 'Sénégalaise'),
    ('seychelles', 'Seychelloise'),
    ('sierra_leone', 'Sierraléonaise'),
    ('somalie', 'Somalienne'),
    ('soudan', 'Soudanaise'),
    ('soudan_du_sud', 'Sud-Soudanaise'),
    ('tanzanie', 'Tanzanienne'),
    ('tchad', 'Tchadienne'),
    ('togo', 'Togolaise'),
    ('tunisie', 'Tunisienne'),
    ('zambie', 'Zambienne'),
    ('zimbabwe', 'Zimbabwéenne'),
   
]

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

    def __init__(self, *args, **kwargs):
        
        filiere_responsable = kwargs.pop('filiere_responsable', None)
        super().__init__(*args, **kwargs)

        # On filtre les classes en fonction de la filiere du responsable
        if filiere_responsable:
            if filiere_responsable == 'AS':
                classes = Classe.objects.filter(name__startswith='AS')
            elif filiere_responsable == 'ISEP':
                classes = Classe.objects.filter(name__startswith='ISEP').exclude(name__startswith='ISEP3')
            elif filiere_responsable == 'ISE1':
                classes = Classe.objects.filter(name__startswith='ISE1',name='ISEP3')
            elif filiere_responsable == 'ISE':
                classes = Classe.objects.filter(name__startswith='ISE').exclude(name__startswith='ISEP').exclude(name__startswith='ISE1')
            
            self.fields['classe'].queryset = classes


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
        exclude = ('statut','annee_scolaire_en_cours','last_login','password','annee_exclusion','annee_diplomation','nombre_redoublage')
        widgets = {
            'password': forms.PasswordInput(),
            'sexe': forms.Select(choices=SEXE_CHOICES),
            'nationalite': forms.Select(choices=NATIONALITY_CHOICES),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'annee_inscription': forms.NumberInput(attrs={'type': 'number', 'min': 1990, 'max': 2200})
           
        }

    def save(self, commit=True):
        etudiant = super().save(commit=False)
        etudiant.set_password(self.data['matricule']) # Le matricule est le mot de passe par defaut lors de l'ajout d'un étudiant
        if commit:
            etudiant.save()
        return etudiant

class EtudiantUpdateForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('last_login','matricule')
        widgets = {
            'password': forms.PasswordInput(),
            'sexe': forms.Select(choices=SEXE_CHOICES),
            'nationalite': forms.Select(choices=NATIONALITY_CHOICES),
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'annee_inscription': forms.NumberInput(attrs={'type': 'number', 'min': 1990, 'max': 2200})
           

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

