# MathCopain v5 — Application de calcul mental

**MathCopain** est une application pédagogique pour apprendre le calcul mental du CE1 au CM2 par le jeu. Cette version propose un système d'exercices et de jeux, un suivi personnalisé des compétences et une adaptation dynamique selon la progression de chaque élève.

## Fonctionnalités principales
- **Exercices variés (addition, soustraction, multiplication, division, fractions, lignes numériques, problèmes, mesures, proportionnalité, décimaux).
- Système adaptatif basé sur la performance (AdaptiveSystem).
- Statistiques et suivi des progrès par élève (SkillTracker).
- Plusieurs modes : exercices classiques, défis quotidiens, jeux (émoticônes/memory, lignes numériques).
- Protection et suivi individualisé des comptes enfants (PIN, JSON sécurisé).

## Lancer l'application
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure du projet
- **app.py** : point d'entrée, interface Streamlit, logique principale, navigation.
- **adaptive_system.py** : adaptation dynamique, recommandations d'exercices.
- **skill_tracker.py** : suivi détaillé des compétences par domaine.
- **mesures_utils.py**, **division_utils.py**, **decimaux_utils.py** : générateurs d'exercices spécifiques par type.
- **utilisateur.py** : gestion des profils et sauvegarde des données utilisateurs.
- **authentification.py** : sécurisation des comptes, gestion PIN.
- **utilisateurs.json / utilisateurs_securises.json** : stockage des profils utilisateurs.
- **users_data.json, users_credentials.json** : données complémentaires, questions secrètes, stockage mots de passe.
- **README.md** : ce fichier
- **requirements.txt** : dépendances Python

## Données & sécurité
Les données sont stockées de façon sécurisée dans des fichiers JSON pour chaque élève et nécessitent un code PIN pour la connexion et la modification du profil.

## Contribuer
Toute suggestion ou PR est bienvenue ! Contact : mathcopain.contact@gmail.com

## Auteur
Développé par Pascal Dao. Version v5.2 (nov. 2025)

---