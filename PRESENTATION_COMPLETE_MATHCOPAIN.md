# 📘 MATHCOPAIN - Présentation Complète
## Application d'Apprentissage Personnalisé des Mathématiques

---

# 🎯 PRÉSENTATION GÉNÉRALE

## Qu'est-ce que MathCopain ?

MathCopain est une **application éducative intelligente** conçue pour accompagner les élèves du **CE1 au CM2** dans leur apprentissage des mathématiques. L'application combine pédagogie bienveillante, intelligence artificielle adaptative, et gamification pour créer une expérience d'apprentissage engageante et efficace.

### Vision

Rendre les mathématiques **accessibles, motivantes et personnalisées** pour chaque enfant, en respectant son rythme et son style d'apprentissage.

### Mission

- ✅ **Personnaliser** l'apprentissage selon le niveau de chaque enfant
- ✅ **Encourager** avec un feedback toujours positif et constructif
- ✅ **Adapter** la difficulté automatiquement grâce à l'IA
- ✅ **Motiver** avec un système de badges et de progression visible
- ✅ **Rassurer** les parents avec un suivi clair et transparent

---

# 🏗️ ARCHITECTURE & TECHNOLOGIES

## Stack Technique

### Frontend
- **Streamlit** - Interface web interactive
- **Python 3.10+** - Langage principal
- **HTML/CSS/JavaScript** - Personnalisation UI

### Backend
- **PostgreSQL** - Base de données relationnelle
- **SQLAlchemy** - ORM Python
- **Alembic** - Migrations base de données

### Intelligence Artificielle
- **Gradient Boosting** (XGBoost/LightGBM) - Optimisation difficulté
- **LSTM + Random Forest** - Prédiction performance
- **SHAP** - Explainability (XAI)

### Sécurité
- **bcrypt** - Hashage PIN sécurisé
- **Rate limiting** - Protection anti-abus
- **HTTPS** - Chiffrement communications
- **RGPD compliant** - Protection données personnelles

### Tests & CI/CD
- **pytest** - Tests unitaires (85%+ coverage)
- **GitHub Actions** - Pipeline automatisé
- **Locust** - Tests de charge

---

# 📚 FONCTIONNALITÉS PRINCIPALES

## 1. Exercices Personnalisés

### 10 Domaines de Compétences

| Domaine | Sous-compétences | Niveaux |
|---------|------------------|---------|
| **Addition** | Retenue, nombres décimaux, grands nombres | CE1-CM2 |
| **Soustraction** | Retenue, nombres décimaux | CE1-CM2 |
| **Multiplication** | Tables, grands nombres, décimaux | CE2-CM2 |
| **Division** | Euclidienne, décimale, reste | CE2-CM2 |
| **Fractions** | Simplification, opérations, équivalence | CM1-CM2 |
| **Nombres Décimaux** | Lecture, comparaison, opérations | CE2-CM2 |
| **Géométrie** | Formes, périmètre, aire, volume | CE1-CM2 |
| **Mesures** | Longueur, masse, temps, conversions | CE1-CM2 |
| **Proportionnalité** | Échelles, pourcentages, ratios | CM1-CM2 |
| **Problèmes** | Monnaie, situations réelles | CE1-CM2 |

### Génération Intelligente

- **Algorithmes adaptés** par domaine
- **Difficulté progressive** (D1 Facile → D5 Expert)
- **Variations infinies** pour éviter mémorisation
- **Contextes réalistes** (monnaie, courses, etc.)

---

## 2. Intelligence Artificielle Adaptative

### Phase 7: Machine Learning

#### DifficultyOptimizer (Gradient Boosting)

**Objectif:** Maintenir l'enfant dans sa **zone de Flow** (70% réussite optimal)

**Fonctionnement:**
```
Input Features (10+):
├─ Taux réussite récent (10 derniers exercices)
├─ Temps moyen par exercice
├─ Tendance (amélioration/déclin)
├─ Streak (succès consécutifs)
├─ Fatigue estimée (0-1)
├─ Vélocité d'apprentissage
├─ Performance par heure/jour
└─ Maîtrise prérequis

    ↓ Gradient Boosting Model
    
Output: Difficulté optimale D1-D5
```

**Ajustement Flow Theory:**
- Si taux > 85% → Augmenter difficulté (+1 niveau)
- Si taux < 55% → Diminuer difficulté (-1 niveau)
- Si 55-85% → Maintenir niveau actuel

#### PerformancePredictor (LSTM + Random Forest)

**Objectif:** Anticiper difficultés et prédire trajectoires

**Fonctionnalités:**
1. **Probabilité de succès** prochain exercice (0-1)
2. **Détection élèves à risque** (abandon potentiel)
3. **Timeline maîtrise** (combien d'exercices restants?)

**Ensemble Voting:**
```
LSTM (40% poids) - Analyse séries temporelles
    +
Random Forest (60% poids) - Classification risque
    =
Prédiction finale (0-100% confiance)
```

#### Explainability (XAI)

Chaque décision IA est **expliquée en langage humain**:

> "J'ai choisi difficulté 3 car:
> ✓ Tu réussis bien (75% cette semaine)
> 📈 Tu progresses régulièrement
> 😴 Tu sembles un peu fatigué aujourd'hui"

**Valeurs SHAP** pour transparence totale.

---

## 3. Feedback Pédagogique Transformatif

### Phase 6: Fondations Pédagogiques

#### ErrorAnalyzer

**500+ erreurs mathématiques cataloguées** par type:

| Type Erreur | Exemple | Feedback Généré |
|-------------|---------|-----------------|
| **Conceptuelle** | Confusion fraction/division | Explication concept + schéma |
| **Procédurale** | Oubli retenue addition | Rappel procédure étape par étape |
| **Calcul** | Erreur table multiplication | Suggestion réviser tables |

#### TransformativeFeedback (Multi-Couches)

**5 niveaux de feedback** après chaque exercice:

1. **Immédiat** (5 mots): "C'est presque ça!" / "✅ Exact!"
2. **Explication** (50 mots): Pourquoi réponse correcte/incorrecte
3. **Stratégie Alternative** (50 mots): Autre méthode résolution
4. **Remédiation** (Action): Exercice similaire plus simple si échec
5. **Encouragement** (Personnalisé): Basé sur historique utilisateur

**Théorie fondatrice:** Hattie 2008 - Feedback transformatif (effet-taille 0.79)

**Principe:** Jamais de messages négatifs ("Faux", "Mauvais") → Toujours constructif et bienveillant

---

## 4. Métacognition & Autorégulation

### Questions Réflexives Post-Exercice

**4 questions (30 secondes max):**

1. **Stratégie utilisée?**
   - Sur mes doigts / Mental / Dessin / Formule / Autre

2. **Difficulté ressentie?**
   - Slider: Facile ← → Difficile

3. **Auto-explication** (optionnel)
   - "Comment tu as trouvé la réponse?"

4. **Intention future** (optionnel)
   - "Prochaine fois je vais..."

### Portfolio Stratégies

L'app **enregistre les stratégies préférées** de l'enfant et:
- Identifie patterns (ex: toujours doigts pour addition)
- Suggère diversification méthodes
- Adapte présentation exercices

### Self-Regulation

Suggestions intelligentes basées sur session:
- "Tu sembles frustré. Pause de 5 min?" (après 3 échecs)
- "5 bonnes d'affilée! Défi plus difficile?" (après streak)
- "Tu fatigues. Peut-être assez pour aujourd'hui?" (baisse performance)

---

## 5. Adaptation Styles d'Apprentissage

### 5 Profils Identifiés

| Style | Caractéristiques | Adaptations App |
|-------|------------------|-----------------|
| **Visual** | Préfère graphiques, couleurs | Diagrammes, number lines, code couleur |
| **Auditory** | Préfère descriptions verbales | Instructions audio, explications détaillées |
| **Kinesthetic** | Préfère manipuler, interactif | Drag & drop, manipulables virtuels |
| **Logical** | Préfère comprendre "pourquoi" | Explications causales, démonstrations |
| **Narrative** | Préfère histoires, contextes | Problèmes mis en scène, personnages |

### Détection Automatique

**Quiz initial** (5-7 questions) + **Inférence performance**

```
Style primaire (60% poids) + Style secondaire (40% poids)
    ↓
Adaptation présentation exercices
```

**Exemple concret:**

Exercice: "Calcule 12 × 5"

- **Visual:** Affiche grille 12 lignes × 5 colonnes
- **Auditory:** "Douze fois cinq, c'est comme cinq fois douze..."
- **Kinesthetic:** Drag 12 groupes de 5 objets
- **Logical:** "12 × 5 = 10 × 5 + 2 × 5 = ?"
- **Narrative:** "Tu as 12 boîtes avec 5 billes chacune..."

---

## 6. Gamification & Motivation

### Système de Badges

**10 badges MVP:**

| Badge | Icône | Condition | Impact |
|-------|-------|-----------|--------|
| Première Étoile | 🌟 | Premier exercice réussi | Onboarding |
| Persévérant | 💪 | 10 exercices d'affilée | Régularité |
| Éclair | ⚡ | 5 exercices <1 min chacun | Vitesse |
| Champion Addition | ➕ | 20 additions réussies | Domaine |
| Champion Multiplication | ✖️ | 20 multiplications réussies | Domaine |
| Explorateur | 🧭 | 5 domaines essayés | Diversité |
| Régulier | 📅 | 5 jours consécutifs | Assiduité |
| Centurion | 💯 | 100 exercices complétés | Milestone |
| Perfectionniste | 🎯 | 10 parfaits d'affilée | Excellence |
| Chouette de nuit | 🦉 | Exercice après 20h | Fun |

### Progression Visible

- **Barre progression** par domaine (0-100%)
- **Graphique temporel** évolution compétences
- **Classement personnel** (pas de compétition entre élèves)
- **Objectifs hebdomadaires** personnalisés

---

## 7. Dashboard Parents

### Vue d'Ensemble Hebdomadaire

**3 métriques clés:**

```
┌─────────────────────────────────────────┐
│  📊 Cette Semaine                       │
├─────────────────────────────────────────┤
│  ⏰ Temps passé        2h 15min  +25min│
│  ✅ Exercices          28       +5      │
│  📈 Taux réussite      78%      +5%     │
└─────────────────────────────────────────┘
```

### Graphique Progression (7 jours)

- **Ligne 1:** Temps quotidien (minutes)
- **Ligne 2:** Taux réussite quotidien (%)

### Compétences Travaillées (Top 5)

```
✅ Addition (CE2)         - Maîtrisée
🔄 Soustraction retenue   - En cours (67%)
⏳ Multiplication tables  - À venir
✅ Géométrie formes       - Maîtrisée
🔄 Problèmes monnaie      - En cours (54%)
```

### Points Forts / À Améliorer

**3 points forts identifiés automatiquement:**
- "Très bon en calcul mental"
- "Progresse vite en géométrie"
- "Régulier dans sa pratique"

**3 axes d'amélioration:**
- "Ralentir sur les énoncés de problèmes"
- "Relire avant de valider"
- "Revoir les fractions équivalentes"

### Suggestions Personnalisées

L'IA suggère exercices ciblés:
- "Fractions (Niveau 2)" - Point faible identifié
- "Géométrie (Niveau 3)" - Poursuivre progrès

### Bouton Encouragement

Parents peuvent envoyer message prédéfini encourageant que l'enfant verra à sa prochaine connexion.

---

## 8. Sécurité & Confidentialité

### Conformité RGPD

✅ **Banner consentement** première visite
✅ **Politique confidentialité** accessible
✅ **Export données** JSON complet téléchargeable
✅ **Droit à l'oubli** suppression compte + données
✅ **Consentement parental** obligatoire inscription

### Sécurité Technique

- **PIN hashé** bcrypt (jamais stocké en clair)
- **Rate limiting** 5 tentatives / 15 minutes
- **Session timeout** 30 minutes inactivité
- **HTTPS obligatoire** chiffrement SSL/TLS
- **Input validation** protection XSS/SQL injection
- **Backup automatique** quotidien PostgreSQL

---

## 9. Accessibilité

### Conformité WCAG AA

✅ **Contraste texte** ratio 4.5:1 minimum
✅ **Taille police** ajustable (Normal/Grand/Très Grand)
✅ **Navigation clavier** complète (Tab, Enter, Escape)
✅ **Alt text** toutes images/icônes
✅ **Mode contraste élevé** fond noir + texte blanc
✅ **Pas de dépendance couleur seule** pour info critique

### Raccourcis Clavier

- `Ctrl + H` - Aide
- `Ctrl + M` - Menu
- `Escape` - Fermer modals
- `Tab` - Navigation éléments
- `Enter` - Valider

---

# 📊 MÉTRIQUES & RÉSULTATS ATTENDUS

## Objectifs Pédagogiques

| Métrique | Baseline | Cible Phase 6 | Cible Phase 7 |
|----------|----------|---------------|---------------|
| **Taux apprentissage** | Référence | +35-40% | +45-50% |
| **Engagement** (temps session) | 10 min | 15-20 min | 20-25 min |
| **Rétention J+7** | 40% | 60% | 70% |
| **Taux complétion exercice** | 65% | 80% | 85% |
| **Satisfaction parents** | N/A | 85%+ | 90%+ |

## Métriques IA (Phase 7)

- **Précision difficulté** (MAE < 0.3 niveau)
- **Taux Flow maintenu** (65-75% succès)
- **Prédiction performance** (accuracy > 75%)
- **Fairness** (0 biais détecté démographiques)

## Métriques Techniques

- **Temps réponse** < 2 secondes (99e percentile)
- **Disponibilité** 99.5%+ (uptime)
- **Capacité** 1000+ utilisateurs simultanés
- **Coverage tests** 85%+
- **Zero bugs critiques** post-lancement

---

# 🎯 PHASES DE DÉVELOPPEMENT

## Roadmap Complète

### Phase 1-5: Fondations (Complété)
- ✅ Architecture modulaire
- ✅ Génération exercices 10 domaines
- ✅ Tests unitaires 500+
- ✅ Sécurité bcrypt
- ✅ CI/CD GitHub Actions

### Phase 6: Fondations Pédagogiques (18 semaines)
- ✅ Feedback transformatif (ErrorAnalyzer + 500 erreurs)
- ✅ Métacognition & autorégulation
- ✅ Profiling styles apprentissage (5 adapters)

### Phase 7: Infrastructure & IA (22 semaines)
- ✅ Migration PostgreSQL (7 tables)
- ✅ ML Adaptive Learning (Gradient Boosting + LSTM)
- ✅ Explainability (SHAP + feedback humain)

### Phase 8: Déploiement Institutionnel (24 semaines) - **En cours**
- ⏳ Mode Enseignant (reporté post-MVP)
- ⏳ Analytics Dashboard enseignant (reporté)
- ✅ **Focus actuel: MVP Parents + Enfants**

---

# 🚀 MVP ACTUEL (Déploiement Imminent)

## Fonctionnalités Incluses

✅ **Exercices personnalisés** 10 domaines
✅ **Intelligence artificielle** adaptative
✅ **Feedback transformatif** multi-couches
✅ **Dashboard parents** simplifié
✅ **Gamification** 10 badges
✅ **Onboarding** interactif
✅ **Sécurité RGPD** complète
✅ **Accessibilité** WCAG AA
✅ **Performance** 50+ users simultanés

## Fonctionnalités Post-MVP

⏳ Dashboard enseignant complet
⏳ Gestion classes & assignations
⏳ Rapports avancés (PDF/CSV/PPT)
⏳ Curriculum mapping Éducation Nationale
⏳ Application mobile (PWA)
⏳ Mode hors-ligne
⏳ Internationalisation (EN, ES)

---

# 👥 UTILISATEURS CIBLES

## Enfants (Primaires)
- **Âge:** 7-11 ans (CE1 à CM2)
- **Besoins:** Apprendre en s'amusant, progresser à son rythme
- **Pain points:** Maths ennuyeux, trop difficile, peur de l'échec

## Parents (Secondaires)
- **Profil:** Parents actifs, soucieux éducation enfants
- **Besoins:** Suivre progression, identifier difficultés, encourager
- **Pain points:** Manque visibilité, ne sait pas comment aider

## Enseignants (Futur - Phase 8 complète)
- **Profil:** Professeurs écoles primaires
- **Besoins:** Gérer classes, assigner travail, suivre élèves
- **Pain points:** Temps limité, classes chargées, différenciation difficile

---

# 💼 MODÈLE ÉCONOMIQUE

## Freemium (Envisagé)

**Version Gratuite:**
- 10 exercices/jour
- Feedback basique
- Dashboard parents limité

**Version Premium** (5-10€/mois):
- Exercices illimités
- Feedback avancé + IA
- Dashboard parents complet
- Rapports détaillés
- Support prioritaire

## B2B Écoles (Phase 8)
- Licence par classe (50-100€/an)
- Dashboard enseignant complet
- Formation incluse
- Support dédié

---

# 📞 CONTACT & SUPPORT

**Email:** support@mathcopain.fr
**Site:** www.mathcopain.fr
**Documentation:** docs.mathcopain.fr

---

**Version:** 1.0 MVP  
**Date:** Novembre 2025  
**Auteur:** Équipe MathCopain
