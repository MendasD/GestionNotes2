from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Etudiant)
admin.site.register(Classe)
admin.site.register(Note)
admin.site.register(Matiere)
admin.site.register(Responsable)
admin.site.register(Message)
admin.site.register(FichiersJoints)
admin.site.register(Diplome)
admin.site.register(Exclu)

