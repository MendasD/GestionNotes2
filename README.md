# 🎓 GestionNotes – Application Django pour la Gestion Scolaire

**GestionNotes** est une application web complète développée avec **Django** pour la gestion des notes, des emplois du temps et de la communication scolaire. Elle permet aux établissements d'organiser toutes les informations académiques autour de **l'année scolaire**, avec une interface intuitive pour les administrateurs, enseignants et étudiants.

---

## 🧭 Table des matières

- [🎯 Objectifs du projet](#-objectifs-du-projet)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🛠️ Technologies utilisées](#-technologies-utilisées)
- [🚀 Installation et exécution](#-installation-et-exécution)
- [📁 Structure du projet](#-structure-du-projet)
- [👨‍💻 Auteurs](#-auteurs)
- [📌 Roadmap](#-roadmap)
- [📄 Licence](#-licence)
- [📬 Contact](#-contact)

---

## 🎯 Objectifs du projet

Fournir une solution numérique performante pour :
- Suivre les performances académiques des élèves.
- Planifier les emplois du temps.
- Faciliter la communication entre les acteurs pédagogiques.
- Conserver et consulter les données **par année scolaire**.

---

## ✨ Fonctionnalités

### 📚 Gestion des étudiants
- Ajouter un nouvel étudiant avec photo, informations personnelles et année scolaire d’inscription.
- Lister les étudiants filtrés par classe et année scolaire.
- Modifier les informations d’un étudiant.
- Supprimer un étudiant.
- Gérer la promotion en classe supérieure.
- Marquer un étudiant comme diplômé ou retiré.

### 📝 Gestion des notes
- Enregistrer les notes par matière, semestre, élève et année scolaire.
- Calcul automatique des moyennes.
- Génération de relevés de notes par semestre/année.
- Suivi des performances globales par classe, par matière ou par élève.
- Archivage des notes par année scolaire.

### 🗓️ Gestion des emplois du temps
- Créer et modifier les emplois du temps selon les classes et les niveaux.
- Affecter des matières à des créneaux horaires.
- Gestion des enseignants, des salles et des plages horaires.
- Visualisation hebdomadaire et possibilité d’impression.
- Emplois du temps enregistrés **par année scolaire**.

### 📬 Messagerie interne avec fichiers joints
- Envoi de messages entre administrateurs, enseignants et étudiants.
- Ajout de **pièces jointes** (images, PDF, Word, etc.).
- Boîte de réception et d’envoi.
- Historique et archivage des échanges.

### 👤 Gestion des utilisateurs
- Authentification sécurisée avec rôles (admin, enseignant, étudiant).
- Interface personnalisée selon le rôle.
- Gestion des droits et permissions.

### 📆 Organisation par année scolaire
- Toutes les informations (étudiants, notes, emplois du temps, messages) sont **liées à une année scolaire**.
- Possibilité de basculer facilement d’une année à une autre.
- Accès aux archives des années précédentes.

---

## 🚀 Installation et exécution

Voici comment cloner le projet et l'exécuter en local :

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/gestion-notes.git
cd gestion-notes
```

### 2. Créer un environnement virtuel

```bash
python -m venv env
```

### 3. Activer l’environnement virtuel

- Sur **Windows** :
```bash
env\Scripts\activate
```

- Sur **macOS/Linux** :
```bash
source env/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Accédez à l’application sur [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 Structure du projet (aperçu rapide)

```plaintext
gestion-notes/
├── notes/                 # App principale : gestion des notes
├── emplois_temps/         # App pour la gestion des emplois du temps
├── users/                 # Gestion des utilisateurs et rôles
├── messagerie/            # Système de messagerie avec pièces jointes
├── templates/             # Fichiers HTML
├── static/                # CSS, JS, images
├── media/                 # Fichiers uploadés
├── db.sqlite3             # Base de données locale
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Auteurs

Ce projet a été réalisé par une équipe d’étudiants passionnés en développement web :

- 🧑‍💻 [Nom 1] – Développement backend & intégration
- 👩‍💻 [Nom 2] – UI/UX et développement frontend
- 🧑‍💻 [Nom 3] – Tests et documentation
- 👨‍🏫 [Nom 4] – Conception des modèles pédagogiques

**Encadré par** : Prénom Nom (enseignant·e référent·e)

---

## 📌 Roadmap

- [x] Gestion des étudiants
- [x] Gestion des notes
- [x] Emplois du temps
- [x] Messagerie interne avec fichiers joints
- [x] Organisation par année scolaire
- [ ] Export PDF des bulletins
- [ ] Notification automatique par mail
- [ ] Interface mobile responsive

---

## 📄 Licence

Ce projet est sous licence **MIT**. Vous pouvez l’utiliser, le modifier et le distribuer librement.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

## 📬 Contact

Pour toute question, suggestion ou collaboration :

- ✉️ Email : contact@gestionnotes.dev
- 🌐 Site Web : [https://gestionnotes.dev](https://gestionnotes.dev)
- 📘 Documentation technique : bientôt disponible

---

Merci d’avoir choisi GestionNotes ! 🎓📊