# Guide de Démarrage Rapide - MathCopain v6.4

## ✅ Base de Données PostgreSQL Créée !

La base de données PostgreSQL est maintenant opérationnelle avec les données de test.

### 📊 Données Disponibles

- **25 élèves** (15 en CE2, 10 en CM1)
- **1 enseignant** : prof.dupont@mathcopain.fr
- **2 classes** : CE2 - Classe A & CM1 - Classe B
- **3833 exercices** complétés (historique de 30 jours)
- **4 devoirs** (3 publiés, 1 brouillon)

### 🔐 Identifiants de Test

**Compte Enseignant :**
- Email: `prof.dupont@mathcopain.fr`
- Mot de passe: `password123`

**Exemples d'élèves :**
- `alice_ce2`, `bob_ce2`, `charlie_ce2` (CE2)
- `alice_cm1`, `bob_cm1`, `charlie_cm1` (CM1)
- PIN: `1234` (fictif pour tests)

---

## 🚀 Démarrage de l'Application

### 1. Lancer l'Application Streamlit (Élèves)

```bash
cd /home/user/MathCopain_v6.2
streamlit run app.py
```

**Accès :** http://localhost:8501

**Fonctionnalités disponibles :**
- ✅ Exercices classiques (addition, soustraction, multiplication, etc.)
- ✅ Jeux mathématiques
- ✅ Fractions, géométrie, décimaux
- ✅ **NOUVEAU : Intelligence IA** (ML adaptatif)
- ✅ Statistiques et progression

### 2. Lancer l'API Flask (Backend Enseignants)

```bash
cd /home/user/MathCopain_v6.2
python -m api.app
```

**Accès :** http://localhost:5000

**Endpoints disponibles :**
- GET `/api/health` - Status de l'API
- GET `/api/teacher/classrooms` - Liste des classes
- GET `/api/teacher/analytics/...` - Analytics ML
- Voir `tests/API_TEST_GUIDE.md` pour la liste complète

### 3. Tester l'API

```bash
# Health check
curl http://localhost:5000/api/health

# Liste des classes (mock session)
curl -X GET http://localhost:5000/api/teacher/classrooms \
  --cookie "teacher_id=2"
```

---

## 🤖 Tester les Fonctionnalités ML

### Dans l'Application Streamlit

1. Démarrer Streamlit: `streamlit run app.py`
2. Se connecter avec un compte élève
3. Sélectionner **"Intelligence IA"** dans le menu
4. Explorer les 4 onglets :
   - **Exercice Adaptatif** : Difficulté ajustée automatiquement
   - **Mes Performances** : Graphiques de progression
   - **Compétences EN** : Suivi du curriculum officiel
   - **Prédictions** : Forecasts ML sur 7 jours

### Via l'API

```bash
# Prédiction de difficulté optimale
curl "http://localhost:5000/api/teacher/analytics/forecast?student_id=1&skill_domain=multiplication&days_ahead=7"

# Leaderboard de classe
curl "http://localhost:5000/api/teacher/analytics/leaderboard?classroom_id=2&days_back=30&top_n=10"
```

---

## 📁 Structure du Projet

```
MathCopain_v6.2/
├── app.py                    # Application Streamlit (élèves)
├── database/
│   ├── models.py            # Modèles SQLAlchemy (14 tables)
│   └── connection.py        # Gestion connexions PostgreSQL
├── core/
│   ├── ml/                  # Modules ML (DifficultyOptimizer, etc.)
│   └── classroom/           # CurriculumMapper, AnalyticsEngine
├── api/
│   └── app.py              # API Flask (enseignants)
├── ui/
│   ├── ml_section.py       # Interface ML Streamlit
│   └── ...                 # Autres sections UI
└── tests/
    ├── seed_data.py        # Script de données de test
    ├── test_api.py         # Tests pytest (25+)
    └── validate_all.py     # Validation automatique
```

---

## 🔧 Configuration PostgreSQL

**Connexion Actuelle :**
- Host: `localhost`
- Port: `5432`
- Database: `mathcopain`
- User: `mathcopain_user`
- Password: `mathcopain_password`

**Variables d'environnement (optionnel) :**

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=mathcopain
export DB_USER=mathcopain_user
export DB_PASSWORD=mathcopain_password
```

---

## ✅ Tests Automatiques

### Lancer tous les tests

```bash
# Validation complète (pytest + endpoints)
python -m tests.validate_all

# Tests pytest uniquement
pytest tests/test_api.py -v

# Avec couverture
pytest tests/test_api.py --cov=api --cov-report=html
```

**Résultat attendu :**
```
✅ ALL TESTS PASSED
Report saved to: tests/validation_report.json
```

---

## 🐛 Troubleshooting

### PostgreSQL ne démarre pas

```bash
# Vérifier le statut
pg_ctlcluster 16 main status

# Redémarrer
pg_ctlcluster 16 main restart
```

### Erreur de connexion à la base de données

```bash
# Tester la connexion
PGPASSWORD=mathcopain_password psql -U mathcopain_user -d mathcopain -c "SELECT version();"

# Recréer les tables si nécessaire
python -c "from database.connection import init_database; init_database()"
```

### L'application Streamlit ne trouve pas les utilisateurs

```bash
# Vérifier que les élèves existent dans PostgreSQL
PGPASSWORD=mathcopain_password psql -U mathcopain_user -d mathcopain -c "SELECT id, username, grade_level FROM users LIMIT 10;"
```

---

## 📚 Documentation Complète

- **API Tests** : `tests/API_TEST_GUIDE.md`
- **Frontend Tests** : `tests/FRONTEND_TEST_GUIDE.md`
- **Tests Suite** : `tests/README.md`

---

## 🎯 Prochaines Étapes

1. ✅ Tester l'interface ML dans Streamlit
2. ✅ Tester l'API Flask avec curl
3. ⏳ Fixer CurriculumMapper (curriculum sync désactivé temporairement)
4. ⏳ Créer le dashboard enseignant frontend (Vue.js)
5. ⏳ Déployer en production

---

## 💡 Notes Importantes

- **Curriculum Sync** : Temporairement désactivé en raison d'incompatibilités de modèle
- **Authentification** : Simplifiée pour les tests (utiliser un vrai système auth en production)
- **Données** : Générées aléatoirement, à remplacer par des vraies données

---

Bon développement ! 🚀
