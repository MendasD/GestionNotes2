# Generated by Django 5.1 on 2024-08-25 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connexion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='classe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='connexion.classe'),
        ),
    ]
