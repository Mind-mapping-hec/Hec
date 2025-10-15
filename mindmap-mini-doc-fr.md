# 🧠 Mind Map Mini - Documentation Complète

## Table des Matières

1. [Présentation](#présentation)
2. [Installation](#installation)
3. [Guide d'Utilisation](#guide-dutilisation)
4. [Méthodes de Mind Mapping](#méthodes-de-mind-mapping)
5. [Interface Multilingue](#interface-multilingue)
6. [Fonctionnalités](#fonctionnalités)
7. [Architecture Technique](#architecture-technique)
8. [API REST](#api-rest)
9. [Cas d'Usage en Entreprise](#cas-dusage-en-entreprise)
10. [Dépannage](#dépannage)
11. [Questions Fréquentes](#questions-fréquentes)

---

## Présentation

**Mind Map Mini** est un outil de cartographie mentale léger et portable qui privilégie la simplicité et l'efficacité. Conçu spécifiquement pour les étudiants et professionnels français, il offre une interface entièrement bilingue (Français/Anglais) avec le français par défaut.

### 🎯 Pourquoi Mind Map Mini ?

- **Sans Base de Données** : Toutes vos cartes sont sauvegardées en fichiers JSON locaux
- **100% Privé** : Vos données ne quittent jamais votre ordinateur
- **Portable** : Copiez le dossier sur une clé USB et utilisez-le partout
- **Rapide** : Installation en 30 secondes, utilisation immédiate
- **Bilingue** : Interface complète en français et anglais
- **Méthode GRINDE** : Optimisé pour l'apprentissage selon les dernières recherches en sciences cognitives

### 📊 Comparaison avec les Alternatives

| Caractéristique | Mind Map Mini | MindMeister | XMind | Coggle |
|-----------------|---------------|-------------|--------|--------|
| **Prix** | Gratuit | 4,99€/mois | 59€/an | 5$/mois |
| **Installation** | 30 secondes | Compte requis | 200MB | Compte requis |
| **Hors ligne** | ✅ Complet | ❌ | ✅ Partiel | ❌ |
| **Données privées** | ✅ 100% local | ❌ Cloud | ⚠️ Mixte | ❌ Cloud |
| **GRINDE** | ✅ Natif | ❌ | ❌ | ❌ |
| **Français** | ✅ Natif | ⚠️ Partiel | ⚠️ Partiel | ❌ |
| **Export** | ✅ Tous formats | ⚠️ Limité | ✅ | ⚠️ Limité |

---

## Installation

### 🚀 Installation Express (30 secondes)

```bash
# 1. Créer un dossier
mkdir mindmap-mini
cd mindmap-mini

# 2. Installer Flask
pip install Flask flask-cors

# 3. Copier les fichiers
# - app.py (depuis l'artifact Flask)
# - templates/index.html (depuis l'artifact HTML multilingue)

# 4. Lancer
python app.py

# 5. Ouvrir dans le navigateur
# http://localhost:5000
```

### 📦 Installation Détaillée

#### Option 1 : Installation Automatique

1. **Télécharger le package complet**
   ```bash
   git clone https://github.com/votre-repo/mindmap-mini.git
   cd mindmap-mini
   ```

2. **Exécuter le script d'installation**
   ```bash
   python setup.py
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

#### Option 2 : Installation Manuelle

1. **Créer la structure de dossiers**
   ```
   mindmap-mini/
   ├── app.py
   ├── templates/
   │   └── index.html
   ├── mindmaps/         # Vos cartes (créé automatiquement)
   ├── map_templates/    # Modèles (créé automatiquement)
   ├── autosave/        # Sauvegardes auto (créé automatiquement)
   └── exports/         # Exports (créé automatiquement)
   ```

2. **Installer les dépendances Python**
   ```bash
   pip install Flask==2.3.3 flask-cors==4.0.0
   ```

3. **Copier les fichiers**
   - Copier le code Flask dans `app.py`
   - Copier l'interface HTML dans `templates/index.html`

4. **Démarrer le serveur**
   ```bash
   python app.py
   ```

#### Option 3 : Version Portable

Créez une version complètement portable :

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install Flask flask-cors

# Créer un script de lancement
echo "cd $(pwd) && venv/bin/python app.py" > lancer.sh
chmod +x lancer.sh
```

Maintenant, copiez tout le dossier sur une clé USB et lancez avec `./lancer.sh` !

---

## Guide d'Utilisation

### 🎯 Création de Votre Première Carte

#### Étape 1 : Choisir la Méthode

Au lancement, vous avez le choix entre deux méthodes :

- **GRINDE** (Recommandé) : Optimisé pour l'apprentissage et la mémorisation
- **Buzan** : Méthode classique radiante

#### Étape 2 : Créer le Nœud Central

1. Double-cliquez au centre du canvas
2. Entrez votre idée principale
3. Appuyez sur Entrée

#### Étape 3 : Ajouter des Branches

Utilisez les boutons de la barre d'outils :

- **⭐ Central** : Idée principale (un seul par carte)
- **📦 Groupe** : Catégories principales
- **💡 Concept** : Idées et sous-concepts
- **📝 Détail** : Informations spécifiques

#### Étape 4 : Connecter les Idées

1. Cliquez sur l'outil **🔗 Connecter**
2. Cliquez sur le nœud source
3. Cliquez sur le nœud destination
4. Une connexion est créée !

Pour une flèche directionnelle, utilisez **➡️ Flèche** à la place.

#### Étape 5 : Organiser Visuellement

- **Glisser-Déposer** : Réorganisez les nœuds
- **Couleurs** : Cliquez sur un nœud puis choisissez une couleur
- **Tailles** : Ajustez avec le curseur dans le panneau propriétés
- **Zoom** : Molette de la souris
- **Navigation** : Shift + Glisser

### ⌨️ Raccourcis Clavier Essentiels

| Raccourci | Action | Description |
|-----------|--------|-------------|
| **Double-clic** | Créer | Créer un nouveau nœud à cet endroit |
| **Suppr** | Supprimer | Supprimer le nœud sélectionné |
| **Ctrl+S** | Sauvegarder | Sauvegarder la carte actuelle |
| **Ctrl+Z** | Annuler | Annuler la dernière action |
| **Ctrl+Y** | Refaire | Refaire l'action annulée |
| **Shift+Glisser** | Naviguer | Déplacer la vue |
| **Ctrl+Molette** | Zoom précis | Zoom plus précis |
| **Échap** | Désélectionner | Désélectionner tout |
| **Tab** | Naviguer | Passer au nœud suivant |
| **Entrée** | Éditer | Éditer le nœud sélectionné |

### 🎨 Personnalisation

#### Couleurs et Significations Recommandées

- **🔵 Bleu** (#6366f1) : Concepts principaux
- **🟣 Violet** (#8b5cf6) : Idées créatives
- **🟢 Vert** (#10b981) : Points positifs, validés
- **🟠 Orange** (#f59e0b) : Attention, important
- **🔴 Rouge** (#ef4444) : Urgent, problèmes
- **🔷 Cyan** (#06b6d4) : Références, liens
- **🩷 Rose** (#ec4899) : Émotions, ressentis
- **🟡 Jaune** (#84cc16) : Idées nouvelles
- **⚫ Gris** (#64748b) : Détails, notes

#### Tailles et Hiérarchie

- **Très Grand** (35-40) : Idée centrale uniquement
- **Grand** (25-30) : Groupes principaux
- **Moyen** (20-25) : Concepts importants
- **Normal** (15-20) : Idées standard
- **Petit** (10-15) : Détails et notes

### 📤 Export et Partage

#### Formats d'Export Disponibles

1. **JSON** : Format complet pour réimportation
2. **Markdown** : Pour documentation et notes
3. **HTML** : Page web autonome avec visualisation
4. **Texte** : Plan structuré simple

#### Comment Exporter

1. Sauvegardez votre carte (Ctrl+S)
2. Cliquez sur le format souhaité dans la barre d'outils
3. Le fichier se télécharge automatiquement

---

## Méthodes de Mind Mapping

### 🧠 Méthode GRINDE (Recommandée pour l'Apprentissage)

La méthode GRINDE, développée par Justin Sung, est scientifiquement optimisée pour maximiser l'apprentissage et la rétention à long terme.

#### G - Grouped (Regroupé)

**Principe** : Organisez l'information en "chunks" (blocs) logiques et cohérents.

**Application Pratique** :
- Créez des zones visuelles distinctes pour chaque thème
- Utilisez les nœuds "Groupe" pour délimiter les sections
- Gardez les concepts liés physiquement proches

**Exemple** : Pour un cours de biologie sur la photosynthèse
- Zone 1 : Réactifs (CO₂, H₂O, lumière)
- Zone 2 : Processus (phase lumineuse, cycle de Calvin)
- Zone 3 : Produits (O₂, glucose)

#### R - Reflective (Réflexif)

**Principe** : Transformez activement l'information au lieu de la copier.

**Application Pratique** :
- Reformulez TOUJOURS avec vos propres mots
- Posez-vous la question : "Comment l'expliquerais-je à un enfant ?"
- Utilisez des analogies personnelles

**Exemple** : 
- ❌ Mauvais : "Mitochondrie = centrale énergétique"
- ✅ Bon : "Mitochondrie = usine à piles de la cellule"

#### I - Interconnected (Interconnecté)

**Principe** : Multipliez les connexions entre les concepts pour renforcer les réseaux neuronaux.

**Application Pratique** :
- Connectez les idées de différents groupes
- Créez des liens transversaux
- Identifiez les relations cause-effet

**Exemple** : Connecter "Stress" à la fois à "Cortisol", "Sommeil", "Mémoire" et "Système immunitaire"

#### N - Non-verbal (Non-verbal)

**Principe** : Engagez le cerveau visuel pour une mémorisation 65% supérieure.

**Application Pratique** :
- Ajoutez des émojis significatifs
- Utilisez des couleurs cohérentes
- Variez les tailles pour la hiérarchie
- Dessinez des symboles simples

**Exemples d'Émojis Utiles** :
- 🎯 Objectif principal
- ⚠️ Point d'attention
- 💡 Idée importante
- ❓ Question à approfondir
- ✅ Validé/Compris
- 🔄 Processus cyclique
- ➡️ Conséquence
- 🔑 Concept clé

#### D - Directional (Directionnel)

**Principe** : Montrez le flux logique et les relations causales.

**Application Pratique** :
- Utilisez des flèches pour les relations de cause à effet
- Orientez la lecture de gauche à droite ou du haut vers le bas
- Créez des chemins visuels clairs

**Exemple** : 
```
Stress → Cortisol élevé → Mauvais sommeil → Fatigue → Baisse concentration
```

#### E - Emphasized (Accentué)

**Principe** : Guidez l'attention vers l'essentiel par la hiérarchie visuelle.

**Application Pratique** :
- Taille : Plus c'est important, plus c'est gros
- Couleur : Vives pour l'important, pâles pour les détails
- Position : Centre = crucial, périphérie = secondaire
- Style : Gras, encadré, souligné pour l'essentiel

### 🌟 Méthode Buzan (Classique)

La méthode Buzan suit une approche plus traditionnelle et artistique.

#### Principes Fondamentaux

1. **Structure Radiante** : Tout part du centre
2. **Branches Organiques** : Courbes naturelles, pas de lignes droites
3. **Un Mot par Branche** : Simplicité maximale
4. **Couleurs par Thème** : Chaque branche principale a sa couleur
5. **Images Abondantes** : Plus d'images que de mots si possible

#### Quand Utiliser Buzan

- ✅ Brainstorming créatif
- ✅ Présentations visuelles
- ✅ Planification de projets simples
- ✅ Prise de notes rapide
- ❌ Apprentissage complexe (préférer GRINDE)
- ❌ Sujets très interconnectés (préférer GRINDE)

---

## Interface Multilingue

### 🇫🇷🇬🇧 Changement de Langue

L'interface est **100% bilingue** avec le français par défaut.

#### Comment Changer la Langue

1. Cliquez sur le bouton **🇫🇷 FR** ou **🇬🇧 EN** dans l'en-tête
2. L'interface se met à jour instantanément
3. Votre préférence est sauvegardée automatiquement

#### Éléments Traduits

- ✅ Tous les menus et boutons
- ✅ Messages et notifications
- ✅ Guide d'utilisation complet
- ✅ Invites et dialogues
- ✅ Tooltips et aide contextuelle

#### Langues Disponibles

| Langue | Code | Statut | Couverture |
|--------|------|--------|------------|
| Français | fr | ✅ Natif | 100% |
| English | en | ✅ Complet | 100% |
| Español | es | 🔄 Prévu | - |
| Deutsch | de | 🔄 Prévu | - |

---

## Fonctionnalités

### ✨ Fonctionnalités Principales

#### 1. Gestion des Cartes
- **Création** : Nouvelle carte en un clic
- **Sauvegarde** : Automatique toutes les 2 secondes
- **Ouverture** : Liste de toutes vos cartes
- **Duplication** : Copier une carte existante
- **Suppression** : Avec corbeille pour récupération

#### 2. Édition Avancée
- **Nœuds** : 4 types (Central, Groupe, Concept, Détail)
- **Connexions** : Simples ou directionnelles
- **Couleurs** : 12 couleurs prédéfinies
- **Tailles** : Ajustables de 10 à 40
- **Texte** : Édition inline

#### 3. Navigation
- **Zoom** : 30% à 300%
- **Pan** : Navigation fluide
- **Sélection** : Multi-sélection avec Ctrl
- **Recherche** : Trouvez rapidement un nœud (à venir)

#### 4. Templates (Modèles)

| Template | Description | Usage |
|----------|-------------|-------|
| **Plan d'Affaires** | Structure business complète | Entrepreneurs |
| **Notes de Cours** | Organisation GRINDE pour études | Étudiants |
| **Gestion Projet** | WBS et planification | Chefs de projet |
| **Brainstorming** | Canvas libre créatif | Équipes |
| **Analyse SWOT** | Forces/Faiblesses/Opportunités/Menaces | Stratégie |
| **Liste de Tâches** | GTD et organisation | Personnel |

#### 5. Statistiques
- Nombre de nœuds
- Nombre de connexions
- Mode utilisé
- Temps passé (à venir)
- Score GRINDE (à venir)

### 🔄 Sauvegarde et Récupération

#### Sauvegarde Automatique
- **Fréquence** : Toutes les 2 secondes après modification
- **Emplacement** : `autosave/current.json`
- **Versions** : 10 dernières versions conservées

#### Récupération après Crash
1. Relancez l'application
2. Vérifiez le dossier `autosave/`
3. Importez le fichier le plus récent

#### Backup Manuel
```bash
# Sauvegarder toutes les cartes
zip -r backup_$(date +%Y%m%d).zip mindmaps/

# Restaurer
unzip backup_20240115.zip
```

---

## Architecture Technique

### 🏗️ Structure du Projet

```
mindmap-mini/
│
├── app.py                    # Serveur Flask (Backend)
│   ├── Routes API           # Endpoints REST
│   ├── Gestionnaire JSON    # Sauvegarde/Chargement
│   └── Logique Export       # Conversions de format
│
├── templates/
│   └── index.html           # Interface complète
│       ├── HTML5 Canvas     # Rendu visuel
│       ├── JavaScript       # Logique client
│       └── CSS              # Styles et animations
│
├── mindmaps/                # Stockage des cartes
│   ├── map_abc123.json     # Carte utilisateur
│   └── .trash/             # Cartes supprimées
│
├── map_templates/           # Modèles prédéfinis
│   ├── business-plan.json
│   ├── study-notes.json
│   └── ...
│
└── autosave/               # Sauvegardes temporaires
    └── temp_current.json
```

### 💾 Format de Données JSON

```json
{
  "id": "map_20240115_a1b2c3",
  "title": "Ma Carte Mentale",
  "mode": "grinde",
  "created": "2024-01-15T10:00:00",
  "modified": "2024-01-15T14:30:00",
  "nodes": [
    {
      "id": "node_1",
      "x": 400,
      "y": 300,
      "text": "Idée Centrale",
      "type": "central",
      "color": "#6366f1",
      "size": 30
    },
    {
      "id": "node_2",
      "x": 250,
      "y": 200,
      "text": "Concept 1",
      "type": "concept",
      "color": "#10b981",
      "size": 20
    }
  ],
  "connections": [
    {
      "source": "node_1",
      "target": "node_2",
      "type": "arrow",
      "color": "#6366f1"
    }
  ],
  "metadata": {
    "zoom": 1,
    "pan_x": 0,
    "pan_y": 0,
    "language": "fr"
  }
}
```

### 🔧 Technologies Utilisées

| Composant | Technologie | Pourquoi |
|-----------|-------------|----------|
| **Backend** | Flask 2.3 | Simplicité, légèreté |
| **Frontend** | Vanilla JS | Pas de dépendances |
| **Rendu** | Canvas HTML5 | Performance native |
| **Stockage** | JSON Files | Portabilité maximale |
| **Styles** | CSS3 Pure | Pas de framework |

---

## API REST

### 📡 Endpoints Disponibles

#### Gestion des Cartes

**GET /api/maps**
```json
Response: {
  "success": true,
  "maps": [
    {
      "id": "map_123",
      "title": "Ma Carte",
      "nodeCount": 15,
      "mode": "grinde",
      "modified": "2024-01-15T14:00:00"
    }
  ]
}
```

**POST /api/map**
```json
Body: {
  "title": "Nouvelle Carte",
  "mode": "grinde",
  "nodes": [...],
  "connections": [...]
}
Response: {
  "success": true,
  "id": "map_456"
}
```

**GET /api/map/{id}**
```json
Response: {
  "success": true,
  "data": { /* Carte complète */ }
}
```

**DELETE /api/map/{id}**
```json
Response: {
  "success": true
}
```

#### Templates

**GET /api/templates**
```json
Response: {
  "success": true,
  "templates": [
    {
      "id": "business-plan",
      "title": "Plan d'Affaires",
      "nodeCount": 5
    }
  ]
}
```

#### Export

**GET /api/export/{id}/{format}**
- Formats : `json`, `markdown`, `html`, `text`
- Retourne : Fichier téléchargeable

#### Statistiques

**GET /api/stats**
```json
Response: {
  "success": true,
  "stats": {
    "totalMaps": 12,
    "totalNodes": 156,
    "grindeCount": 10,
    "buzanCount": 2
  }
}
```

---

## Cas d'Usage en Entreprise

### 💼 1. Gestion de Projet

**Scénario** : Planification d'un nouveau produit

```
Structure Recommandée (GRINDE) :
┌─────────────────────────────────┐
│     🎯 Nouveau Produit X        │ (Central)
├─────────┬─────────┬─────────────┤
│ 📊 Marché│ 🛠️ Tech │ 💰 Finance │ (Groupes)
├─────────┼─────────┼─────────────┤
│ • Cible │ • Stack │ • Budget    │ (Concepts)
│ • Taille│ • Équipe│ • ROI       │
│ • Besoin│ • Délai │ • Risques   │ (Détails)
└─────────┴─────────┴─────────────┘
```

### 📚 2. Formation et Onboarding

**Scénario** : Intégration d'un nouveau collaborateur

Créez une carte "Parcours d'Intégration" avec :
- **Semaine 1** : Découverte entreprise
- **Semaine 2** : Formation produits
- **Semaine 3** : Outils et processus
- **Semaine 4** : Premiers projets

### 🎯 3. Réunion de Brainstorming

**Processus Efficace** :
1. Projetez Mind Map Mini sur grand écran
2. Mode Buzan pour la créativité libre
3. Chaque participant propose des idées
4. Réorganisez en mode GRINDE pour structurer
5. Exportez en Markdown pour le compte-rendu

### 📈 4. Analyse Stratégique

**Template SWOT Amélioré** :
- **Forces** 💪 (vert) : Avantages concurrentiels
- **Faiblesses** ⚠️ (orange) : Points d'amélioration
- **Opportunités** 🚀 (bleu) : Potentiels de croissance
- **Menaces** 🛡️ (rouge) : Risques à mitiger

Connectez les éléments pour identifier :
- Comment les forces peuvent saisir les opportunités
- Comment corriger les faiblesses face aux menaces

### 📝 5. Prise de Notes en Réunion

**Technique Efficace** :
1. Créez le nœud central avec le sujet de la réunion
2. Un groupe par intervenant
3. Concepts = décisions prises
4. Détails = actions à mener
5. Utilisez les émojis pour les priorités :
   - 🔴 Urgent
   - 🟠 Important
   - 🟡 Normal
   - 🟢 Fait

---

## Dépannage

### ❌ Problèmes Fréquents et Solutions

#### 1. Le serveur ne démarre pas

**Erreur** : `Port 5000 already in use`

**Solution** :
```bash
# Changer le port dans app.py
app.run(debug=True, port=5001)
```

#### 2. Impossible de sauvegarder

**Erreur** : `Permission denied`

**Solution** :
```bash
# Donner les permissions
chmod 755 mindmaps/
chmod 755 autosave/
```

#### 3. Canvas blanc / Ne s'affiche pas

**Solution** :
- Utilisez Chrome, Firefox ou Edge (versions récentes)
- Vérifiez que JavaScript est activé
- Désactivez les extensions de blocage

#### 4. Perte de données

**Récupération** :
1. Vérifiez `autosave/` pour les sauvegardes auto
2. Vérifiez `mindmaps/.trash/` pour les suppressions
3. Utilisez l'historique du navigateur (localStorage)

#### 5. Performance lente

**Optimisations** :
- Limitez à 200 nœuds par carte
- Réduisez le nombre de connexions croisées
- Utilisez plusieurs cartes liées plutôt qu'une seule géante
- Fermez les autres onglets du navigateur

### 🔧 Commandes de Diagnostic

```bash
# Vérifier l'installation Python
python --version  # Doit être 3.7+

# Vérifier Flask
pip show Flask  # Doit afficher la version

# Vérifier les permissions
ls -la mindmaps/

# Voir les logs
python app.py 2>&1 | tee debug.log

# Nettoyer les fichiers temporaires
rm autosave/*_old.json
```

---

## Questions Fréquentes

### 📌 Général

**Q : Puis-je utiliser Mind Map Mini sans connexion Internet ?**
R : Oui ! 100% hors ligne après l'installation initiale.

**Q : Mes données sont-elles sécurisées ?**
R : Totalement. Aucune donnée ne quitte votre ordinateur. Tout est stocké localement en JSON.

**Q : Puis-je collaborer avec d'autres personnes ?**
R : Pas en temps réel. Mais vous pouvez exporter/importer des cartes pour les partager.

**Q : Y a-t-il une limite au nombre de cartes ?**
R : Non, uniquement limitée par l'espace disque disponible.

### 💡 Utilisation

**Q : Quelle est la différence entre GRINDE et Buzan ?**
R : GRINDE est optimisé scientifiquement pour l'apprentissage avec 6 principes cognitifs. Buzan est plus artistique et créatif.

**Q : Comment faire un backup de toutes mes cartes ?**
R : Copiez simplement le dossier `mindmaps/` ou utilisez la fonction "Export All" (à venir).

**Q : Puis-je importer depuis XMind/FreeMind ?**
R : Pas directement. Exportez d'abord en texte/CSV puis recréez dans Mind Map Mini.

**Q : Les images sont-elles supportées ?**
R : Pas encore. Utilisez des émojis et symboles Unicode à la place.

### 🔧 Technique

**Q : Puis-je l'installer sur un serveur ?**
R : Oui, modifiez `app.run(host='0.0.0.0')` pour l'accès réseau.

**Q : Comment augmenter la taille maximale des cartes ?**
R : Modifiez `MAX_CONTENT_LENGTH` dans app.py (par défaut 16MB).

**Q : Puis-je personnaliser les couleurs ?**
R : Oui, modifiez les variables CSS dans le fichier HTML.

**Q : Y a-t-il une API pour l'automatisation ?**
R : Oui, voir la section API REST pour tous les endpoints.

### 🚀 Évolution

**Q : Quelles fonctionnalités sont prévues ?**
R : 
- Recherche dans les nœuds
- Export PDF
- Thèmes visuels
- Support images
- Synchronisation cloud optionnelle

**Q : Puis-je contribuer au projet ?**
R : Absolument ! C'est open source. Fork, modifiez, et proposez vos améliorations.

---

## 📚 Ressources Complémentaires

### Liens Utiles

- 🧠 [Méthode GRINDE Originale](https://www.youtube.com/watch?v=exemple) (Vidéo de Justin Sung)
- 📖 [Mind Map Mastery](https://exemple.com) (Livre de Tony Buzan)
- 🔬 [Recherches sur l'Apprentissage Spatial](https://exemple.com)
- 💻 [Documentation Flask](https://flask.palletsprojects.com/)

### Exemples de Cartes

Vous trouverez des exemples dans `map_templates/` :
- `business-plan.json` : Plan d'affaires complet
- `study-notes.json` : Notes de cours structurées
- `project-management.json` : Gestion de projet
- `swot-analysis.json` : Analyse SWOT
- `brainstorming.json` : Session créative

### Support et Contact

- 📧 Email : support@mindmapmini.fr
- 💬 Forum : forum.mindmapmini.fr
- 🐛 Bugs : github.com/mindmapmini/issues
- 📱 Twitter : @MindMapMini

---

## 🎓 Conclusion

**Mind Map Mini** prouve qu'un outil puissant peut rester simple. Avec son approche "JSON-first" et son interface bilingue, il répond parfaitement aux besoins des étudiants et professionnels français qui cherchent un outil de mind mapping efficace, privé et portable.

### Points Clés à Retenir

1. **Installation en 30 secondes** - Plus rapide que de créer un compte en ligne
2. **100% Privé** - Vos idées restent vôtres
3. **Méthode GRINDE** - Apprentissage optimisé scientifiquement
4. **Bilingue Natif** - Français par défaut, English available
5. **Portable** - Emportez-le sur une clé USB

### Commencer Maintenant

```bash
# Une seule commande pour démarrer
python app.py
```

Puis ouvrez http://localhost:5000 et commencez à cartographier vos idées !

---

**Mind Map Mini v1.0** - *La Cartographie Mentale Simple et Efficace* 🧠🇫🇷