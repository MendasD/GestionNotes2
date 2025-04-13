# 🎓 GestionNotes – Application Django pour la Gestion Scolaire

**GestionNotes** est une application web complète développée avec **Django** pour la gestion des notes, des emplois du temps et de la communication scolaire. Elle est conçue conformément au fonctionnement de l'Ecole Nationale de la Statistique et de l'Analyse Economique Pierre NDIAYE de Dakar (**ENSAE**). Elle permet à l'établissement d'organiser toutes les informations académiques concernant les notes ou les emplois de temps suivant **l'année scolaire**, avec une interface intuitive pour les administrateurs et les étudiants. Cette application permet à cet effet d'automatiser certaines tâches courantes de l'ENSAE et également de conserver les différentes données dans le temps, et garantit un accès simple et rapide à ces données.

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

---

## 🎯 Objectifs du projet

Fournir une solution numérique performante pour :
- Faciliter le partage des notes aux différents élèves
- Contrôler les performances académiques des élèves.
- Planifier les emplois du temps.
- Faciliter la communication entre les responsables et étudiants.
- Conserver et consulter les données **par année scolaire**.

---

## ✨ Fonctionnalités

### 📚 Gestion des étudiants
- Ajouter un nouvel étudiant ou une liste d'étudiants avec informations personnelles et année scolaire d’inscription.
- Lister les étudiants filtrés par classe et année scolaire.
- Modifier les informations d’un étudiant.
- Supprimer un étudiant.
- Gérer la promotion en classe supérieure.
- Marquer un étudiant comme diplômé ou exclu...

### 📝 Gestion des notes
- Enregistrer les notes par matière, semestre, élève et année scolaire.
- Calcul automatique des moyennes.
- Génération de bulletins.
- Suivi des performances globales et par classe.
- Télécharger les fichiers récapitulatifs, côté responsable


### 🗓️ Gestion des emplois du temps
- Créer et modifier les emplois du temps selon les classes.
- Suppression d'emplois de temps
- Visualisation hebdomadaire.
- Emplois du temps enregistrés **par période**.

### 📬 Messagerie interne avec fichiers joints
- Envoi de messages des responsables aux étudiants.
- Ajout de **pièces jointes** (images, PDF, Word, etc.).


### 👤 Gestion des utilisateurs
- Authentification sécurisée avec rôles (responsable, étudiant).
- Interface personnalisée selon le rôle.
- Gestion des droits et permissions.

### 📆 Organisation par année scolaire
- Toutes les informations (étudiants, notes, emplois du temps, messages) sont **liées à une année scolaire**.
- Possibilité de consulter facilement les informations d’une année à une autre.
- Accès aux données des années précédentes.

---

## 🛠️ Technologies utilisées

- **Python 3.10**
- **Django**
- **SQLite**
- **HTML**
- **CSS**
- **Bootstrap 5**
- **JavaScript**

---


## 🚀 Installation et exécution

Voici comment cloner le projet et l'exécuter en local :

### 1. Cloner le dépôt

```bash
git clone https://github.com/MendasD/GestionNotes2.git
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

### 6. Créer un superutilisateur (optionnel)

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
├── gestion_notes/                 # App principale : gestion des notes
├── connexion/         # App pour la gestion des connections et authentifications
├── Messages_fichiers/            # Sauvegarde les fichiers joints aux différents messages
├── templates/             # Fichiers HTML
├── static/                # CSS, JS, images
├── modeles/                 # Contient les maquettes de bulletin
├── Fichiers_tests/     # Contient les fichiers tests utilisés pour l'ajout des matières, étudiants et notes
├── db.sqlite3             # Base de données locale
├── manage.py
└── requirements.txt
```

---

## 👨‍💻 Auteurs

Ce projet a été réalisé par une équipe de deux (02) étudiants de l'ENSAE, passionnés en développement web :

- 🧑‍💻 **David Christ NZONDE** – <christnzonde@gmail.com> - [Linkedin](https://www.linkedin.com/in/david-christ-mekontchou-nzonde-37a870304/)
- 👩‍💻 **Wilfred TCHAPDA** 


---

## 📌 Roadmap

- [x] Gestion des étudiants
- [x] Gestion des notes
- [x] Emplois du temps
- [x] Messagerie interne avec fichiers joints
- [x] Organisation par année scolaire
- [x] Export des bulletins
- [x] Téléchargement des fichiers recapitulatifs côté responsable
- [ ] Notification automatique par mail
- [ ] Modèle intelligent pour interagir avec la base de données
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

Merci !!! 🎓📊
