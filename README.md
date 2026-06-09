# Gestion de Tâches entre Freelancers et Entreprises

Ce projet est une plateforme web de mise en relation et de gestion de missions entre les entreprises et les freelancers. Elle facilite la publication de projets par les entreprises, le dépôt de candidatures par les freelances et permet une communication fluide via une messagerie interne.

## Fonctionnalités Principales

### 1. Gestion des Utilisateurs & Profils
*   **Inscription et Connexion** : Inscription avec choix de rôle explicite (**Freelance** ou **Entreprise**).
*   **Profils Dédiés** :
    *   **Freelance** : Bio, liste des compétences (séparées par des virgules), tarif horaire et lien vers le portfolio.
    *   **Entreprise** : Nom de l'entreprise, description, site web, email de contact et numéro SIRET.
*   **Gestion de Compte** : Formulaire de modification de profil et possibilité de suppression définitive du compte.

### 2. Gestion des Missions
*   **Publication** : Les entreprises peuvent créer, modifier ou supprimer des missions (contenant le titre, la description, le budget, les compétences requises et la date limite).
*   **Filtrage Intelligent** :
    *   Les **Freelances** visualisent uniquement les missions actives auxquelles ils n'ont pas encore postulé.
    *   Les **Entreprises** voient un tableau de bord contenant exclusivement les missions qu'elles ont publiées.
*   **Détail des Missions** : Fiche détaillée de la mission avec la liste des candidats et le suivi des candidatures.

### 3. Système de Postulation (Candidatures)
*   **Candidatures** : Les freelances peuvent postuler à des missions actives en saisissant un message de motivation.
*   **Validation** : L'entreprise propriétaire de la mission peut **accepter** ou **refuser** la candidature d'un freelance.

### 4. Messagerie Interne
*   **Conversations Automatiques** : Une conversation est initiée automatiquement dès qu'un freelance postule à une mission.
*   **Messagerie** : Échange de messages en temps réel entre l'entreprise et les freelances candidats.
*   **Notifications** : Indicateur visuel (pastille rouge) dans la barre de navigation indiquant la présence de messages non lus.

---

## Arborescence du Projet

Voici la structure de l'application Django :

```text
├── src/
│   ├── Entreprise_Freelance/      # Configuration globale de l'application Django
│   │   ├── settings.py           # Configuration de l'application (base de données, applications, etc.)
│   │   ├── urls.py               # Routage global du site
│   │   └── wsgi.py / asgi.py     # Serveurs d'application web
│   │
│   ├── messagerie/               # Application de messagerie
│   │   ├── templates/messagerie/ # Interfaces de messagerie (liste, conversation)
│   │   ├── models.py             # Modèles de données (Conversation, Message)
│   │   ├── views.py              # Logique d'affichage et d'envoi de messages
│   │   └── urls.py               # URLs de l'application messagerie
│   │
│   ├── missions/                 # Application de gestion des missions et candidatures
│   │   ├── templates/missions/   # Formulaires et affichages (creer_mission, detail, listes, postuler, etc.)
│   │   ├── models.py             # Modèles de données (Mission, Candidature)
│   │   ├── views.py              # Logique d'affichage, de création et de validation de candidatures
│   │   └── urls.py               # URLs de l'application missions
│   │
│   ├── users/                    # Application de gestion des comptes utilisateurs
│   │   ├── templates/            # Formulaires d'accès (login, signup, profile, complete_profile)
│   │   ├── models.py             # Modèles de profil (Utilisateur hérité de AbstractUser, Freelance, Entreprise)
│   │   ├── views.py              # Logique d'authentification et de profil
│   │   └── urls.py               # URLs de l'application users
│   │
│   ├── templates/                # Gabarit parent partagé
│   │   └── base.html             # Structure de page globale (Header, Navbar, Footer, Messages Flash)
│   │
│   ├── db.sqlite3                # Base de données SQLite de développement
│   └── manage.py                 # Script de commande principal de Django
│
├── .gitignore                    # Fichiers et dossiers à exclure de Git
└── README.md                     # Documentation du projet (ce fichier)
```

---

## Spécifications Techniques

*   **Langage** : Python 3.13+
*   **Framework Backend** : Django 5.2+ / 6.0+
*   **Interface Frontend** : Gabarits Django (templates HTML) avec intégration de **Tailwind CSS** (via CDN).
*   **Base de Données** : SQLite (`db.sqlite3` local de développement).

---

## Installation et Lancement

### 1. Prérequis
Assurez-vous d'avoir installé **Python 3** sur votre machine.

### 2. Configuration et Lancement de l'Application

1.  **Activer l'environnement virtuel (optionnel mais recommandé)** :
    ```bash
    # Sous Windows
    .venv\Scripts\activate
    ```
2.  **Appliquer les migrations** (si vous souhaitez réinitialiser ou synchroniser la base) :
    ```bash
    python src/manage.py migrate
    ```
3.  **Lancer le serveur de développement** :
    ```bash
    python src/manage.py runserver
    ```
4.  **Accéder à l'application** :
    Ouvrez votre navigateur et accédez à l'adresse suivante : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Auteur et Encadrement

*   **Développeur** : Ouédraogo Amine Ahmad (Année universitaire 2024/2025)
*   **Professeur encadrant** : Pr. Ennahbaoui
*   **Établissement** : Université de Lyon 1
