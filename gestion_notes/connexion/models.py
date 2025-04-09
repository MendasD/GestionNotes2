from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import uuid

class Etudiant(models.Model):
    matricule = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name='etudiants')
    annee_inscription = models.CharField(max_length=4)
    nationalite = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    annee_scolaire_en_cours = models.CharField(max_length=9, blank=True)
    statut = models.CharField(
        max_length=100, 
        choices=[
            ('En cours de formation', 'En cours de formation'),
            ('Diplômé', 'Diplômé'),
            ('Exclus', 'Exclus')
        ],
        default='En cours de formation'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    annee_exclusion = models.CharField(max_length=9, null=True, blank=True)
    annee_diplomation = models.CharField(max_length=9, null=True, blank=True)
    nombre_redoublage = models.IntegerField(default=0)
    heure_absence = models.IntegerField(default=0)
    

    def get_notes(self):
        return self.notes.all()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Remplir annee_scolaire_en_cours dynamiquement à partir de  annee_inscription
        if not self.annee_scolaire_en_cours:
            annee_debut = int(self.annee_inscription)
            self.annee_scolaire_en_cours = f'{annee_debut}-{annee_debut+1}'
        super().save(*args, **kwargs)
    
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def __str__(self):
        return self.matricule
    
    @property
    def years_at_school(self):
        """Va retourner les annees passées à l'école depuis son inscription"""
        annees = []
        annee_debut = int(self.annee_inscription)
        annee_fin = int(self.annee_scolaire_en_cours.split('-')[0])

        for year in range(annee_debut, annee_fin + 1):
            annees.append(f"{year}-{year+1}")

        return annees
    
    def get_notes_by_year(self, annee_scolaire):
        return self.notes.filter(annee_scolaire=annee_scolaire)
    
    def add_year(self):
        annees=self.annee_scolaire_en_cours.split("-")
        annees=[str(int(i)+1) for i in annees]
        self.annee_scolaire_en_cours="-".join(annees)
        self.save()
    
    @property
    def Degrade_etudiant(self):
        """Pour faire redoubler un etudiant"""
        self.add_year()
        self.nombre_redoublage+=1
        if self.nombre_redoublage==2:
            self.statut='Exclus'
            self.annee_exclusion=self.annee_scolaire_en_cours
            
        self.save()


    @property
    def Upgrade_etudiant(self):
        AS = ['AS1','AS2','AS3']
        ISEP = ['ISEP1','ISEP2','ISEP3','ISE2']
        ISE = ['ISE1','ISE2','ISE3']
        classe_etudiant = self.classe.name

        if classe_etudiant in AS:
            i=0
            for classe_value in AS:
                if classe_etudiant in classe_value:
                    try:
                        classe_new_name=AS[i+1]
                        classe_new= Classe.objects.get(name =classe_new_name)
                        self.classe=classe_new
                        self.add_year()
                        self.statut= 'En cours de formation'
                        self.save()
                        break
                    except IndexError:
                        self.classe=self.classe
                        self.statut= 'Diplômé'
                        self.save()
                        Diplome.objects.create(etudiant=self)
                        break
                i=i+1
        elif classe_etudiant in ['ISEP1','ISEP2','ISEP3']:
            i=0
            for classe_value in ISEP:
                if classe_etudiant == classe_value:
                    try:
                        classe_new_name=ISEP[i+1]
                        classe_new= Classe.objects.get(name =classe_new_name)
                        self.classe=classe_new
                        self.add_year()
                        self.statut = 'En cours de formation'
                        self.save()
                        break
                    except IndexError:
                        self.classe=self.classe
                        self.statut= 'Diplômé'
                        self.annee_diplomation = self.annee_scolaire_en_cours
                        self.save()
                        Diplome.objects.create(etudiant=self)
                        break
                i=i+1
            
        else:
            i=0
            for classe_value in ISE:
                if classe_value in classe_etudiant:
                    try:
                        classe_new_name=ISE[i+1]
                        classe_new= Classe.objects.get(name =classe_new_name)
                        self.classe=classe_new
                        self.add_year()
                        self.statut = 'En cours de formation'
                        self.save()
                        break
                    except IndexError:
                        self.classe=self.classe
                        self.statut= 'Diplômé'
                        self.annee_diplomation = self.annee_scolaire_en_cours
                        self.save()
                        Diplome.objects.create(etudiant=self)
                        break
                i=i+1

class Diplome(models.Model):
    etudiant = models.ForeignKey(Etudiant,on_delete=models.CASCADE,related_name='diplome')
    fonction = models.CharField(null=True,blank=True,max_length=150)
    date = models.DateTimeField(auto_now_add=True)

class Motif_exclusion(models.Model):
    motif = models.CharField(unique=True,max_length=200)

class Exclu(models.Model):
    etudiant = models.ForeignKey(Etudiant,on_delete=models.CASCADE,related_name='exclu')
    motif = models.ForeignKey(Motif_exclusion,on_delete=models.CASCADE,related_name='motif_exclusion')
    description = models.CharField(null=True,blank=True,max_length=200)
    date = models.DateTimeField(auto_now_add=True)
 
    
class Classe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Matiere(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='matieres')
    credit = models.FloatField()
    active = models.BooleanField(default=True)
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('semestre1', 'Semestre 1'),
            ('semestre2', 'Semestre 2')
        ]
    )
    enseignant = models.ForeignKey('Enseignants', on_delete=models.SET_NULL, null=True, blank=True, related_name='matieres')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'classe'], name='unique_matiere_per_classe')
        ]

    def __str__(self):
        return self.name
    
class Note(models.Model):
    id = models.AutoField(primary_key=True)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='notes')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='notes', default=1)
    note = models.FloatField()
    poids = models.FloatField(default=0.5,max_length=3)
    type_note = models.CharField(
        max_length=20,
        choices=[
            ('note1', 'Note 1'),
            ('note2', 'Note 2'),
            ('note1_et_note2', 'Note 1 et Note 2')
        ]
    )
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('semestre1', 'Semestre 1'),
            ('semestre2', 'Semestre 2')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    annee_scolaire = models.CharField(max_length=9, default='1999-2000')

   

   

    def __str__(self):
        return f"{self.etudiant.name} - {self.matiere.name} - {self.note} ({self.annee_scolaire})"
    
class Moyenne(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='moyennes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='moyennes')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='moyennes')
    annee_scolaire = models.CharField(max_length=9, default='1999-2000')
    moyenne = models.FloatField()

class Enseignants(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, default='', blank=True, null=True)
    nationalite = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(max_length=1, blank=True, null=True)
    is_permanent = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.name

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)
    
class Responsable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    filiere = models.CharField(
        max_length=4,
        choices=[
            ('AS', 'Analyste Statisticien'),
            ('ISEP', 'Ingénieur Statisticien Economiste Préparatoire'),
            ('ISE1', 'Ingénieur Statisticien Economiste première année'),
            ('ISE', 'Ingénieur Statisticien Economiste ')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True,blank=True)

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def get_classes_by_filiere(self):
        filiere = self.filiere
        if filiere == 'AS':
            classes = ['AS1','AS2','AS3-data_science','AS3-eco']
        elif filiere == 'ISEP':
            classes = ['ISEP1','ISEP2']
        elif filiere == 'ISE1':
            classes = ['ISEP3','ISE1-eco','ISE1-maths']
        elif filiere == 'ISE':
            classes = ['ISE2','ISE3-eco','ISE3-evaluation_impact']
        return classes

    def get_etudiants_by_filiere(self):
        filiere = self.filiere
        if filiere == 'AS':
            etudiants = {'AS1': [], 'AS2': [], 'AS3': []}

            etudiants['AS1']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='AS1',statut='En cours de formation')]
            etudiants['AS2']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='AS2',statut='En cours de formation')]
            etudiants['AS3']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='AS3',statut='En cours de formation')] 

        elif filiere == 'ISEP':
            etudiants = {'ISEP1': [], 'ISEP2': []}

            etudiants['ISEP1']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISEP1',statut='En cours de formation')]
            etudiants['ISEP2']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISEP2',statut='En cours de formation')]

        elif filiere == 'ISE1':
            etudiants = {'ISEP3':[],'ISE1-maths': [], 'ISE1-eco': []}

            etudiants['ISEP3']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISEP3',statut='En cours de formation')]
            etudiants['ISE1-maths']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISE1-maths',statut='En cours de formation')]
            etudiants['ISE1-eco']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISE1-eco',statut='En cours de formation')]
        
        elif filiere == 'ISE':
            etudiants = {'ISE2': [], 'ISE3-eco': [],'ISE3-evaluation_impact':[]}
            etudiants['ISE2']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISE2',statut='En cours de formation')]
            etudiants['ISE3-eco']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISE3-eco',statut='En cours de formation')]
            etudiants['ISE3-evaluation_impact']=[etudiant for etudiant in Etudiant.objects.filter(classe__name='ISE3-evaluation_impact',statut='En cours de formation')]

        return etudiants
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, related_name='messages')
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='messages')
    sujet = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    visible_etudiant = models.BooleanField(default=True)
    visible_responsable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.responsable.name} à  {self.etudiant.name}: {self.message[:20]}..."
    
    def diffuse_to_class(self, classes:list):
        for classe in classes:
            etudiants = Etudiant.objects.filter(classe__name=classe)
            for etudiant in etudiants:
                Message.objects.create(responsable=self.responsable, etudiant=etudiant, message=self.message)
                print(f"Message envoyé à {etudiant.name} de la classe {classe}")
    
    def send_to_etudiant(self, etudiant_pk):
        try:
            etudiant = Etudiant.objects.get(pk=etudiant_pk)
            Message.objects.create(responsable=self.responsable, etudiant=etudiant, message=self.message)
            print(f"Message envoyé à {etudiant.name}")
        except Etudiant.DoesNotExist:
            print(f"Etudiant avec le pk {etudiant_pk} n'existe pas")

class FichiersJoints(models.Model):
    message = models.ForeignKey(Message,on_delete=models.CASCADE,related_name='fichier_joint')
    fichier = models.FileField(upload_to='Messages_fichiers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EmploiDeTemps(models.Model):
    numero = models.AutoField(primary_key=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='emploi_de_temps')
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('semestre1', 'Semestre 1'),
            ('semestre2', 'Semestre 2')
        ]
    )

    def __str__(self):
        return f"{self.classe.name} - {self.periode}"
    
class EmploiDuTemps(models.Model):
    """classe réellement utilisée pour créer les emploi de temps"""
    id = models.AutoField(primary_key=True)
    periode = models.CharField(max_length=100)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='emploi_du_temps')
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('semestre1', 'Semestre 1'),
            ('semestre2', 'Semestre 2')
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['periode', 'classe'], name='unique_emploi_du_temps')
        ]

    def __str__(self):
        return f"{self.classe.name} - {self.periode}"

class Programmation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='programmation')
    horaire = models.CharField(max_length=100)
    emploi_de_temps = models.ForeignKey(EmploiDeTemps, on_delete=models.CASCADE, related_name='programmation')

    def __str__(self):
        return f"{self.matiere.name} - {self.horaire}"
    
class Programmation_cours(models.Model):
    """classe réellement utilisée pour la programmation des cours"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='programmation_cours', null=True, blank=True)
    horaire = models.CharField(max_length=100)
    jour = models.CharField(max_length=100, null=True, blank=True)
    numero = models.IntegerField() # position du cours dans la journée
    emploi_du_temps = models.ForeignKey(EmploiDuTemps, on_delete=models.CASCADE, related_name='programmation_cours')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.matiere.name} - {self.horaire}"
    
