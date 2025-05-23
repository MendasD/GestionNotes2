# Generated by Django 5.1 on 2025-04-03 00:14

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0028_enseignants_sexe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emploidetemps',
            name='numero',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='EmploiDuTemps',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('periode', models.CharField(max_length=100)),
                ('semestre', models.CharField(choices=[('semestre1', 'Semestre 1'), ('semestre2', 'Semestre 2')], max_length=20)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emploi_du_temps', to='connexion.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Programmation_cours',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('horaire', models.CharField(max_length=100)),
                ('numero', models.IntegerField()),
                ('emploi_du_temps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programmation_cours', to='connexion.emploidutemps')),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programmation_cours', to='connexion.matiere')),
            ],
        ),
    ]
