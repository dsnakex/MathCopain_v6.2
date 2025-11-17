# Guide de test Frontend - MathCopain Phase 8 UI

## Préparation

### 1. Démarrer l'API et créer les données de test

```bash
# Terminal 1 : Créer les données
python -m tests.seed_data

# Terminal 2 : Démarrer l'API
python -m api.app
# → http://localhost:5000
```

### 2. Démarrer le frontend

```bash
# Terminal 3 : Frontend
cd frontend
python -m http.server 8080
# → http://localhost:8080
```

### 3. Ouvrir dans le navigateur

Ouvrir http://localhost:8080 dans Chrome/Firefox

---

## Tests du Dashboard (Tableau de bord)

### ✅ Vue d'ensemble

**Actions** :
1. Ouvrir http://localhost:8080
2. Observer l'interface

**Vérifications** :
- [ ] Header présent avec logo "MathCopain" et badge "Dashboard Enseignant"
- [ ] Navigation avec 6 onglets : Dashboard, Classes, Devoirs, Analytics, Rapports, Compétences EN
- [ ] Onglet "Dashboard" actif (surligné en vert)
- [ ] Pas de message d'erreur dans la console

### ✅ Cartes de statistiques

**Vérifications** :
- [ ] **Carte 1 - Classes actives** :
  - Icône école (🏫)
  - Nombre = 2
  - Texte "Classes actives"

- [ ] **Carte 2 - Élèves au total** :
  - Icône utilisateurs
  - Nombre = 25
  - Texte "Élèves au total"

- [ ] **Carte 3 - Élèves à risque** :
  - Icône warning (⚠️)
  - Nombre > 0 (selon données)
  - Texte "Élèves à risque"
  - Badge rouge si > 0

- [ ] **Carte 4 - Taux de réussite moyen** :
  - Icône graphique
  - Pourcentage entre 50% et 95%
  - Couleur verte si ≥ 70%, jaune sinon

### ✅ Tableau des classes

**Vérifications** :
- [ ] Titre "Mes classes"
- [ ] Bouton "Nouvelle classe"
- [ ] 2 lignes de classes affichées :
  - CE2 - Classe A
  - CM1 - Classe B
- [ ] Colonnes : Classe, Niveau, Élèves, Taux de réussite, À risque, Actions
- [ ] Progress bar animée pour taux de réussite
- [ ] Badge "À risque" rouge si > 0
- [ ] Bouton "Voir" cliquable

### ✅ Interactions

**Test 1 : Clic sur "Voir" une classe**
- [ ] Cliquer sur "Voir" pour "CE2 - Classe A"
- [ ] Navigation vers onglet "Classes"
- [ ] Classe sélectionnée

---

## Tests de Gestion de Classes

### ✅ Vue liste des classes

**Actions** :
1. Cliquer sur onglet "Classes"

**Vérifications** :
- [ ] Titre "Gestion des classes"
- [ ] Bouton "Créer une classe"
- [ ] Tableau avec 2 classes
- [ ] Colonnes : Classe, Niveau, Année, Élèves, Capacité, Actions
- [ ] Badges bleus pour niveaux (CE2, CM1)
- [ ] Boutons : "Élèves", "Modifier" (crayon), "Supprimer" (poubelle)

### ✅ Créer une classe

**Actions** :
1. Cliquer "Créer une classe"
2. Modal apparaît (TODO: à implémenter)

**Résultat attendu** :
- Modal avec formulaire :
  - Nom (texte)
  - Niveau (select: CE1, CE2, CM1, CM2)
  - Année scolaire (texte)
  - Capacité max (nombre, défaut 30)
  - Boutons "Annuler" et "Créer"

### ✅ Gestion des élèves

**Actions** :
1. Cliquer sur "Élèves" pour "CE2 - Classe A"

**Vérifications** :
- [ ] Section "Élèves de CE2 - Classe A" apparaît
- [ ] Formulaire d'ajout en haut :
  - Input "Nom d'utilisateur de l'élève"
  - Bouton "Ajouter"
- [ ] Tableau avec ~15 élèves
- [ ] Colonnes : Élève, Niveau, Exercices, Taux de réussite, Statut, Actions
- [ ] Progress bars pour taux de réussite
- [ ] Badges :
  - Rouge "À risque" si at_risk = true
  - Vert "Normal" sinon
- [ ] Bouton "Retirer" pour chaque élève

**Test : Ajouter un élève**
1. Taper "nouveau_test" dans l'input
2. Cliquer "Ajouter"

**Résultat** :
- [ ] Notification erreur (élève n'existe pas) OU
- [ ] Élève ajouté si existe dans la DB

**Test : Retirer un élève**
1. Cliquer "Retirer" sur un élève
2. Confirmer la popup

**Résultat** :
- [ ] Popup de confirmation
- [ ] Élève retiré de la liste
- [ ] Notification "Élève retiré de la classe"

### ✅ Fermer la section élèves

**Actions** :
1. Cliquer "Fermer" (X) dans le header de la section

**Résultat** :
- [ ] Section se ferme
- [ ] Retour au tableau des classes

---

## Tests des Devoirs

### ✅ Vue liste des devoirs

**Actions** :
1. Cliquer sur onglet "Devoirs"

**Vérifications** :
- [ ] Titre "Gestion des devoirs"
- [ ] Select de filtre : "Tous", "Publiés", "Brouillons"
- [ ] Bouton "Nouveau devoir"
- [ ] Tableau avec ~4 devoirs
- [ ] Colonnes : Titre, Classe, Domaines, Exercices, Échéance, Statut, Actions
- [ ] Badges :
  - Vert "Publié" ou Jaune "Brouillon"
  - Bleu "Adaptatif" si mode ML activé
- [ ] Domaines affichés (max 2)

### ✅ Filtres

**Test 1 : Filtre "Publiés"**
1. Sélectionner "Publiés" dans le select

**Résultat** :
- [ ] Seuls les devoirs publiés affichés
- [ ] Titre montre le bon nombre

**Test 2 : Filtre "Brouillons"**
1. Sélectionner "Brouillons"

**Résultat** :
- [ ] Seuls les brouillons affichés

### ✅ Créer un devoir

**Actions** :
1. Cliquer "Nouveau devoir"
2. Modal apparaît (TODO)

**Form attendu** :
- Titre
- Classe (select)
- Domaines (multi-select ou checkboxes)
- Mode adaptatif (toggle ON/OFF)
- Difficulté (si adaptatif OFF : select D1-D5)
- Nombre d'exercices (10 par défaut)
- Date d'échéance
- Description (textarea)

### ✅ Publier un devoir

**Actions** :
1. Trouver un devoir "Brouillon"
2. Cliquer bouton "Publier" (icône avion)

**Résultat** :
- [ ] Notification "Devoir publié avec succès"
- [ ] Badge devient "Publié" (vert)
- [ ] Devoir disparaît du filtre "Brouillons"

### ✅ Suivi de complétion

**Actions** :
1. Cliquer "Suivi" sur un devoir publié

**Vérifications** :
- [ ] Section "Suivi : [Titre du devoir]" apparaît
- [ ] Tableau des complétions :
  - Colonnes : Élève, Progression, Réussite, Temps (min), Statut
  - Progress bars pour progression
  - Badges : Vert "Terminé" ou Jaune "En cours"
- [ ] Bouton "Fermer"

---

## Tests Analytics

### ✅ Sélection de classe

**Actions** :
1. Cliquer onglet "Analytics"

**Vérifications** :
- [ ] Titre "Analytics"
- [ ] Card "Sélectionnez une classe"
- [ ] Select avec liste des classes
- [ ] Message "Sélectionnez une classe pour voir les analytics"

### ✅ Leaderboard

**Actions** :
1. Sélectionner "CE2 - Classe A" dans le select

**Vérifications** :
- [ ] Section "Classement (Top 10)" apparaît
- [ ] Tableau avec max 10 élèves
- [ ] Colonnes : Rang, Élève, Exercices, Réussite, Score
- [ ] Icônes de rang :
  - #1 : Trophée 🏆 (doré)
  - #2 : Médaille 🥈
  - #3 : Récompense 🥉
  - #4-10 : Numéro simple
- [ ] Progress bars pour taux de réussite
- [ ] Tri par score décroissant

### ✅ Placeholder graphiques

**Vérifications** :
- [ ] Card "Graphiques d'évolution"
- [ ] Message "Graphiques de trajectoire de progression disponibles via l'API"
- [ ] Note "Utilisez Chart.js pour visualiser..."

---

## Tests Rapports

### ✅ Configuration

**Actions** :
1. Cliquer onglet "Rapports"

**Vérifications** :
- [ ] Titre "Génération de rapports"
- [ ] Card "Configurer le rapport"
- [ ] Formulaire :
  - Type (select) : "Vue d'ensemble classe", "Élèves à risque", "Couverture curriculum"
  - Classe (select)
  - Niveau scolaire (si type = curriculum)
- [ ] Bouton "Générer le rapport" (désactivé si classe non sélectionnée)

### ✅ Types de rapports

**Test 1 : Vue d'ensemble classe**
1. Sélectionner "Vue d'ensemble classe"
2. Sélectionner "CE2 - Classe A"
3. Cliquer "Générer le rapport"

**Résultat** :
- [ ] Notification "Génération du rapport en cours..."
- [ ] Puis "Rapport généré avec succès"
- [ ] Console : Objet rapport avec `statistics`, `trajectory`, `leaderboard`

**Test 2 : Élèves à risque**
1. Sélectionner "Élèves à risque"
2. Générer

**Résultat** :
- [ ] Rapport avec `total_at_risk`, liste détaillée

**Test 3 : Couverture curriculum**
1. Sélectionner "Couverture curriculum"
2. Choisir niveau "CE2"
3. Générer

**Résultat** :
- [ ] Rapport avec `well_covered`, `partially_covered`, `neglected`

### ✅ Informations

**Vérifications** :
- [ ] Card "Types de rapports disponibles"
- [ ] 3 descriptions avec icônes et couleurs

---

## Tests Compétences EN

### ✅ Sélection

**Actions** :
1. Cliquer onglet "Compétences EN"

**Vérifications** :
- [ ] Titre "Compétences Éducation Nationale"
- [ ] Card "Sélection"
- [ ] Formulaire :
  - Classe (select)
  - Niveau scolaire (select : CE1, CE2, CM1, CM2)
- [ ] Message "Sélectionnez une classe et un niveau"

### ✅ Vue d'ensemble

**Actions** :
1. Sélectionner "CE2 - Classe A"
2. Sélectionner "CE2"

**Vérifications** :
- [ ] 2 cartes de stats :
  - Total compétences (25 pour CE2)
  - Maîtrise moyenne classe (%)
- [ ] Card "Détail des compétences"
- [ ] Tableau avec 25 lignes (compétences CE2)
- [ ] Colonnes :
  - Code (e.g., CE2.C.3.2)
  - Compétence (titre)
  - Domaine (badge bleu)
  - Élèves maîtrisant (X / 15)
  - Taux de maîtrise (progress bar + %)
  - Niveau moyen (badge coloré)

### ✅ Couleurs des badges

**Vérifications** :
- [ ] Badge VERT si niveau ≥ 70%
- [ ] Badge JAUNE si 30% ≤ niveau < 70%
- [ ] Badge ROUGE si niveau < 30%

### ✅ Changement de niveau

**Actions** :
1. Changer niveau de "CE2" à "CM1"

**Résultat** :
- [ ] Tableau se met à jour
- [ ] 30 compétences CM1 affichées
- [ ] Stats recalculées

---

## Tests de Navigation

### ✅ Onglets

**Test : Clic sur chaque onglet**
1. Cliquer Dashboard → Classes → Devoirs → Analytics → Rapports → Compétences

**Vérifications pour chaque** :
- [ ] Onglet devient actif (vert)
- [ ] Contenu change instantanément
- [ ] Pas de rechargement de page
- [ ] Pas d'erreur console

### ✅ Bouton retour navigateur

**Actions** :
1. Naviguer entre plusieurs onglets
2. Cliquer "Retour" du navigateur

**Résultat** :
- [ ] Pas de changement (SPA sans routing)
- [ ] OU naviguer vers page précédente si routing implémenté

---

## Tests de Notifications

### ✅ Toast notifications

**Déclencheurs** :
- Créer une classe
- Ajouter un élève
- Retirer un élève
- Publier un devoir
- Générer un rapport
- Erreur API

**Vérifications pour chaque** :
- [ ] Notification apparaît en haut à droite
- [ ] Icône appropriée :
  - ✓ Success (vert)
  - ✗ Error (rouge)
  - ⚠ Warning (jaune)
  - ℹ Info (bleu)
- [ ] Message clair et descriptif
- [ ] Bouton X pour fermer
- [ ] Disparaît automatiquement après 5 secondes
- [ ] Animation slide-in depuis la droite

---

## Tests Responsive (Mobile)

### ✅ Affichage mobile (< 768px)

**Actions** :
1. Réduire largeur navigateur < 768px OU
2. Ouvrir DevTools (F12) → Mode mobile (Ctrl+Shift+M)

**Vérifications** :
- [ ] Header passe en colonne (logo au-dessus, actions en dessous)
- [ ] Navigation horizontale scrollable
- [ ] Stats en colonne unique
- [ ] Tableaux scroll horizontalement
- [ ] Modals occupent 95% de largeur
- [ ] Tout reste lisible et utilisable

---

## Tests de Performance

### ✅ Temps de chargement

**Actions** :
1. Ouvrir DevTools → Network
2. Rafraîchir la page (Ctrl+R)

**Vérifications** :
- [ ] index.html < 50ms
- [ ] style.css < 100ms
- [ ] Tous les .js < 200ms total
- [ ] API calls < 500ms chacun
- [ ] Page interactive en < 2 secondes

### ✅ Mémoire

**Actions** :
1. DevTools → Performance → Record
2. Naviguer entre onglets pendant 1 minute
3. Arrêter recording

**Vérifications** :
- [ ] Pas de memory leaks visibles
- [ ] Heap size stable
- [ ] FPS > 30 (idéalement 60)

---

## Tests d'Erreurs

### ✅ API indisponible

**Actions** :
1. Arrêter l'API Flask (Ctrl+C dans terminal)
2. Rafraîchir la page
3. Essayer de charger des classes

**Résultat** :
- [ ] Erreur dans console
- [ ] Notification "Erreur lors du chargement des données"
- [ ] Message user-friendly (pas de crash)

### ✅ Données manquantes

**Actions** :
1. Base de données vide (sans seed data)
2. Ouvrir l'interface

**Résultat** :
- [ ] Empty states affichés :
  - "Aucune classe créée"
  - "Aucun devoir"
  - etc.
- [ ] Boutons CTA ("Créer une classe", etc.)
- [ ] Pas d'erreur JavaScript

### ✅ Session expirée

**Actions** :
1. Simuler session expirée (vider cookies)
2. Essayer une action

**Résultat** :
- [ ] Erreur 401 de l'API
- [ ] Notification "Authentication required"
- [ ] Redirection vers login (si implémenté)

---

## Checklist Complète

### ✅ Dashboard
- [ ] Stats cards (4)
- [ ] Tableau classes
- [ ] Navigation vers Classes

### ✅ Classes
- [ ] Liste classes
- [ ] Créer classe (modal)
- [ ] Modifier classe
- [ ] Supprimer classe
- [ ] Liste élèves
- [ ] Ajouter élève
- [ ] Retirer élève

### ✅ Devoirs
- [ ] Liste devoirs
- [ ] Filtres (tous/publiés/brouillons)
- [ ] Créer devoir (modal)
- [ ] Publier devoir
- [ ] Suivi complétion

### ✅ Analytics
- [ ] Sélection classe
- [ ] Leaderboard Top 10
- [ ] Icônes de rang
- [ ] Placeholder graphiques

### ✅ Rapports
- [ ] 3 types de rapports
- [ ] Configuration
- [ ] Génération
- [ ] Notifications

### ✅ Compétences EN
- [ ] Sélection classe/niveau
- [ ] Stats (2 cards)
- [ ] Tableau 108 compétences
- [ ] Badges colorés

### ✅ UI/UX
- [ ] Navigation onglets
- [ ] Notifications toast
- [ ] Loading states
- [ ] Empty states
- [ ] Responsive mobile
- [ ] Animations smooth

### ✅ Performance
- [ ] Chargement < 2s
- [ ] Pas de memory leaks
- [ ] FPS stable

### ✅ Gestion erreurs
- [ ] API indisponible
- [ ] Données vides
- [ ] Session expirée

---

## Rapport de bugs

Si vous trouvez des bugs, documentez :

```markdown
**Page** : [Dashboard/Classes/etc.]
**Action** : [Ce que vous avez fait]
**Résultat attendu** : [Ce qui devrait se passer]
**Résultat réel** : [Ce qui s'est passé]
**Console errors** : [Copier erreurs console]
**Screenshots** : [Si applicable]
```

---

## Conclusion

Une fois tous les tests passés :

✅ **Interface complète et fonctionnelle**
✅ **Toutes les vues opérationnelles**
✅ **Interactions fluides**
✅ **Gestion d'erreurs robuste**
✅ **Ready for production!**
