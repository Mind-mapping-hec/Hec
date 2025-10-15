# app.py - Mind Map Mini - Backend Flask Amélioré avec Support Multilingue

from flask import Flask, render_template, request, jsonify, send_file, make_response
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
import shutil
from pathlib import Path
import base64
import io
import zipfile
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindmap-mini-secret-2024'
app.config['DEFAULT_LANGUAGE'] = 'fr'  # Français par défaut
CORS(app)

# Autosave defaults exposed to the frontend via /api/settings
app.config['AUTOSAVE_ENABLED'] = True
app.config['AUTOSAVE_FREQUENCY'] = 60  # seconds

CORS(app)

# Configuration des dossiers
MAPS_FOLDER = 'mindmaps'
TEMPLATES_FOLDER = 'map_templates'
EXPORTS_FOLDER = 'exports'
AUTOSAVE_FOLDER = 'autosave'
BACKUP_FOLDER = 'backups'

# Créer les dossiers nécessaires
for folder in [MAPS_FOLDER, TEMPLATES_FOLDER, EXPORTS_FOLDER, AUTOSAVE_FOLDER, BACKUP_FOLDER, 'static', 'templates']:
    os.makedirs(folder, exist_ok=True)

# Traductions pour les exports
TRANSLATIONS = {
    'fr': {
        'mind_map': 'Carte Mentale',
        'mode': 'Mode',
        'created': 'Créé le',
        'modified': 'Modifié le',
        'central_idea': 'IDÉE CENTRALE',
        'groups': 'GROUPES',
        'concepts': 'CONCEPTS',
        'details': 'DÉTAILS',
        'connections': 'Connexions',
        'total_connections': 'Total des connexions',
        'nodes': 'nœuds',
        'statistics': 'Statistiques',
        'total_nodes': 'Total des nœuds',
        'copy': 'Copie',
        'untitled': 'Sans titre',
        'recent_maps': 'Cartes récentes',
        'no_maps': 'Aucune carte trouvée'
    },
    'en': {
        'mind_map': 'Mind Map',
        'mode': 'Mode',
        'created': 'Created',
        'modified': 'Modified',
        'central_idea': 'CENTRAL IDEA',
        'groups': 'GROUPS',
        'concepts': 'CONCEPTS',
        'details': 'DETAILS',
        'connections': 'Connections',
        'total_connections': 'Total connections',
        'nodes': 'nodes',
        'statistics': 'Statistics',
        'total_nodes': 'Total nodes',
        'copy': 'Copy',
        'untitled': 'Untitled',
        'recent_maps': 'Recent maps',
        'no_maps': 'No maps found'
    }
}

# ==============================================================================
# GESTION DES FICHIERS JSON AMÉLIORÉE
# ==============================================================================

class MindMapManager:
    """Gestionnaire amélioré pour les mind maps sauvegardées en JSON"""
    
    @staticmethod
    def generate_id():
        """Générer un ID unique avec timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique = str(uuid.uuid4())[:6]
        return f"map_{timestamp}_{unique}"
    
    @staticmethod
    def get_map_path(map_id):
        """Obtenir le chemin du fichier JSON d'une carte"""
        return os.path.join(MAPS_FOLDER, f"{map_id}.json")
    
    @staticmethod
    def list_maps(language='fr'):
        """Lister toutes les cartes disponibles avec support multilingue"""
        maps = []
        if os.path.exists(MAPS_FOLDER):
            for filename in os.listdir(MAPS_FOLDER):
                if filename.endswith('.json') and not filename.startswith('.'):
                    try:
                        with open(os.path.join(MAPS_FOLDER, filename), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Calculer le score GRINDE si applicable
                            grinde_score = MindMapManager.calculate_grinde_score(data) if data.get('mode') == 'grinde' else None
                            
                            maps.append({
                                'id': filename[:-5],
                                'title': data.get('title', TRANSLATIONS[language]['untitled']),
                                'mode': data.get('mode', 'grinde'),
                                'created': data.get('created', ''),
                                'modified': data.get('modified', ''),
                                'nodeCount': len(data.get('nodes', [])),
                                'connectionCount': len(data.get('connections', [])),
                                'preview': data.get('preview', ''),
                                'language': data.get('metadata', {}).get('language', 'fr'),
                                'grindeScore': grinde_score
                            })
                    except Exception as e:
                        print(f"Erreur lecture {filename}: {e}")
                        continue
        
        # Trier par date de modification (plus récent en premier)
        return sorted(maps, key=lambda x: x.get('modified', ''), reverse=True)
    
    @staticmethod
    def calculate_grinde_score(data):
        """Calculer le score GRINDE d'une carte"""
        if data.get('mode') != 'grinde':
            return None
        
        score = {
            'grouped': 0,
            'reflective': 0,
            'interconnected': 0,
            'nonverbal': 0,
            'directional': 0,
            'emphasized': 0,
            'total': 0
        }
        
        nodes = data.get('nodes', [])
        connections = data.get('connections', [])
        
        # G - Grouped: Présence de groupes
        group_nodes = [n for n in nodes if n.get('type') == 'group']
        score['grouped'] = min(100, len(group_nodes) * 25)
        
        # R - Reflective: Diversité du vocabulaire
        unique_words = set()
        for node in nodes:
            words = node.get('text', '').lower().split()
            unique_words.update(words)
        score['reflective'] = min(100, len(unique_words) * 3)
        
        # I - Interconnected: Ratio connexions/nœuds
        if len(nodes) > 1:
            connectivity_ratio = len(connections) / (len(nodes) - 1)
            score['interconnected'] = min(100, int(connectivity_ratio * 60))
        
        # N - Non-verbal: Présence d'émojis/symboles
        emoji_count = 0
        for node in nodes:
            text = node.get('text', '')
            # Compter les émojis (caractères Unicode dans certaines plages)
            emoji_count += sum(1 for c in text if ord(c) > 127)
        score['nonverbal'] = min(100, emoji_count * 15)
        
        # D - Directional: Connexions directionnelles
        arrow_connections = [c for c in connections if c.get('type') == 'arrow']
        if connections:
            score['directional'] = int((len(arrow_connections) / len(connections)) * 100)
        
        # E - Emphasized: Variété de tailles et couleurs
        sizes = set(n.get('size', 20) for n in nodes)
        colors = set(n.get('color', '#6366f1') for n in nodes)
        score['emphasized'] = min(100, (len(sizes) * 10 + len(colors) * 10))
        
        # Score total
        score['total'] = sum([score[k] for k in ['grouped', 'reflective', 'interconnected', 
                                                  'nonverbal', 'directional', 'emphasized']]) // 6
        
        return score
    
    @staticmethod
    def load_map(map_id):
        """Charger une carte depuis son fichier JSON"""
        filepath = MindMapManager.get_map_path(map_id)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la carte {map_id}: {e}")
            return None
    
    @staticmethod
    def save_map(map_id, data):
        """Sauvegarder une carte en JSON avec backup automatique"""
        if not map_id:
            map_id = MindMapManager.generate_id()
        
        # Ajouter les métadonnées
        data['id'] = map_id
        data['modified'] = datetime.now().isoformat()
        if 'created' not in data:
            data['created'] = datetime.now().isoformat()
        
        # Ajouter les métadonnées de langue si non présentes
        if 'metadata' not in data:
            data['metadata'] = {}
        if 'language' not in data['metadata']:
            data['metadata']['language'] = app.config['DEFAULT_LANGUAGE']
        
        # Générer un aperçu textuel
        if 'nodes' in data and len(data['nodes']) > 0:
            central = next((n for n in data['nodes'] if n.get('type') == 'central'), None)
            if central:
                data['preview'] = central.get('text', '')[:50]
        
        # Créer un backup de l'ancienne version si elle existe
        filepath = MindMapManager.get_map_path(map_id)
        if os.path.exists(filepath):
            backup_path = os.path.join(BACKUP_FOLDER, f"{map_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            shutil.copy2(filepath, backup_path)
        
        # Sauvegarder la nouvelle version
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Créer une sauvegarde automatique
        autosave_path = os.path.join(AUTOSAVE_FOLDER, f"{map_id}_latest.json")
        shutil.copy2(filepath, autosave_path)
        
        # Nettoyer les vieilles sauvegardes
        MindMapManager.cleanup_old_backups(map_id)
        
        return map_id
    
    @staticmethod
    def cleanup_old_backups(map_id, keep_days=7):
        """Nettoyer les backups de plus de X jours"""
        cutoff_date = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)
        
        for filename in os.listdir(BACKUP_FOLDER):
            if filename.startswith(f"{map_id}_"):
                filepath = os.path.join(BACKUP_FOLDER, filename)
                if os.path.getmtime(filepath) < cutoff_date:
                    os.remove(filepath)
    
    @staticmethod
    def search_maps(query, language='fr'):
        """Rechercher dans les cartes"""
        results = []
        query_lower = query.lower()
        
        for map_info in MindMapManager.list_maps(language):
            # Charger la carte complète pour rechercher dans le contenu
            map_data = MindMapManager.load_map(map_info['id'])
            if map_data:
                # Rechercher dans le titre
                if query_lower in map_data.get('title', '').lower():
                    results.append(map_info)
                    continue
                
                # Rechercher dans les nœuds
                for node in map_data.get('nodes', []):
                    if query_lower in node.get('text', '').lower():
                        results.append(map_info)
                        break
        
        return results

    @staticmethod
    def delete_map(map_id):
        """Supprimer définitivement une carte"""
        try:
            file_path = MindMapManager.get_map_path(map_id)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Erreur lors de la suppression de {map_id}: {e}")
            return False

    @staticmethod
    def rename_map(map_id, new_title):
        """Renommer une carte"""
        try:
            file_path = MindMapManager.get_map_path(map_id)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data['title'] = new_title
                data['modified'] = datetime.now().isoformat()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                return True
            return False
        except Exception as e:
            print(f"Erreur lors du renommage de {map_id}: {e}")
            return False

# ==============================================================================
# TEMPLATES AMÉLIORÉS
# ==============================================================================

def init_templates():
    """Initialiser les templates par défaut en français et anglais"""
    templates = {
        'business-plan': {
            'fr': {
                'title': 'Plan d\'Affaires',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '🎯 Plan d\'Affaires', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '📊 Vision & Mission', 'type': 'group', 'x': 200, 'y': 150, 'color': '#8b5cf6', 'size': 25},
                    {'id': '3', 'text': '🎯 Analyse Marché', 'type': 'group', 'x': 600, 'y': 150, 'color': '#10b981', 'size': 25},
                    {'id': '4', 'text': '📦 Produit/Service', 'type': 'group', 'x': 200, 'y': 450, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '💰 Plan Financier', 'type': 'group', 'x': 600, 'y': 450, 'color': '#ef4444', 'size': 25},
                    {'id': '6', 'text': '👥 Équipe', 'type': 'group', 'x': 400, 'y': 150, 'color': '#06b6d4', 'size': 25},
                    {'id': '7', 'text': '📈 Stratégie Marketing', 'type': 'group', 'x': 400, 'y': 450, 'color': '#ec4899', 'size': 25}
                ],
                'connections': [
                    {'source': '1', 'target': '2', 'type': 'simple'},
                    {'source': '1', 'target': '3', 'type': 'simple'},
                    {'source': '1', 'target': '4', 'type': 'simple'},
                    {'source': '1', 'target': '5', 'type': 'simple'},
                    {'source': '1', 'target': '6', 'type': 'simple'},
                    {'source': '1', 'target': '7', 'type': 'simple'}
                ]
            },
            'en': {
                'title': 'Business Plan',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '🎯 Business Plan', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '📊 Vision & Mission', 'type': 'group', 'x': 200, 'y': 150, 'color': '#8b5cf6', 'size': 25},
                    {'id': '3', 'text': '🎯 Market Analysis', 'type': 'group', 'x': 600, 'y': 150, 'color': '#10b981', 'size': 25},
                    {'id': '4', 'text': '📦 Product/Service', 'type': 'group', 'x': 200, 'y': 450, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '💰 Financial Plan', 'type': 'group', 'x': 600, 'y': 450, 'color': '#ef4444', 'size': 25},
                    {'id': '6', 'text': '👥 Team', 'type': 'group', 'x': 400, 'y': 150, 'color': '#06b6d4', 'size': 25},
                    {'id': '7', 'text': '📈 Marketing Strategy', 'type': 'group', 'x': 400, 'y': 450, 'color': '#ec4899', 'size': 25}
                ],
                'connections': [
                    {'source': '1', 'target': '2', 'type': 'simple'},
                    {'source': '1', 'target': '3', 'type': 'simple'},
                    {'source': '1', 'target': '4', 'type': 'simple'},
                    {'source': '1', 'target': '5', 'type': 'simple'},
                    {'source': '1', 'target': '6', 'type': 'simple'},
                    {'source': '1', 'target': '7', 'type': 'simple'}
                ]
            }
        },
        'study-notes': {
            'fr': {
                'title': 'Notes de Cours',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '📚 Titre du Cours', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🔑 Concepts Clés', 'type': 'group', 'x': 250, 'y': 200, 'color': '#3b82f6', 'size': 25},
                    {'id': '3', 'text': '💡 Exemples', 'type': 'group', 'x': 550, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '4', 'text': '❓ Questions', 'type': 'group', 'x': 250, 'y': 400, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '⚡ À Retenir', 'type': 'group', 'x': 550, 'y': 400, 'color': '#ef4444', 'size': 25},
                    {'id': '6', 'text': '📝 Exercices', 'type': 'group', 'x': 400, 'y': 500, 'color': '#8b5cf6', 'size': 25}
                ],
                'connections': []
            },
            'en': {
                'title': 'Study Notes',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '📚 Course Title', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🔑 Key Concepts', 'type': 'group', 'x': 250, 'y': 200, 'color': '#3b82f6', 'size': 25},
                    {'id': '3', 'text': '💡 Examples', 'type': 'group', 'x': 550, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '4', 'text': '❓ Questions', 'type': 'group', 'x': 250, 'y': 400, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '⚡ To Remember', 'type': 'group', 'x': 550, 'y': 400, 'color': '#ef4444', 'size': 25},
                    {'id': '6', 'text': '📝 Exercises', 'type': 'group', 'x': 400, 'y': 500, 'color': '#8b5cf6', 'size': 25}
                ],
                'connections': []
            }
        },
        'project-management': {
            'fr': {
                'title': 'Gestion de Projet',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '💼 Nom du Projet', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🎯 Objectifs', 'type': 'group', 'x': 200, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '3', 'text': '👥 Équipe', 'type': 'group', 'x': 600, 'y': 200, 'color': '#3b82f6', 'size': 25},
                    {'id': '4', 'text': '📋 Tâches', 'type': 'group', 'x': 200, 'y': 400, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '📅 Planning', 'type': 'group', 'x': 600, 'y': 400, 'color': '#8b5cf6', 'size': 25},
                    {'id': '6', 'text': '⚠️ Risques', 'type': 'group', 'x': 300, 'y': 500, 'color': '#ef4444', 'size': 25},
                    {'id': '7', 'text': '💰 Budget', 'type': 'group', 'x': 500, 'y': 500, 'color': '#06b6d4', 'size': 25}
                ],
                'connections': []
            },
            'en': {
                'title': 'Project Management',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '💼 Project Name', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🎯 Goals', 'type': 'group', 'x': 200, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '3', 'text': '👥 Team', 'type': 'group', 'x': 600, 'y': 200, 'color': '#3b82f6', 'size': 25},
                    {'id': '4', 'text': '📋 Tasks', 'type': 'group', 'x': 200, 'y': 400, 'color': '#f59e0b', 'size': 25},
                    {'id': '5', 'text': '📅 Timeline', 'type': 'group', 'x': 600, 'y': 400, 'color': '#8b5cf6', 'size': 25},
                    {'id': '6', 'text': '⚠️ Risks', 'type': 'group', 'x': 300, 'y': 500, 'color': '#ef4444', 'size': 25},
                    {'id': '7', 'text': '💰 Budget', 'type': 'group', 'x': 500, 'y': 500, 'color': '#06b6d4', 'size': 25}
                ],
                'connections': []
            }
        },
        'swot': {
            'fr': {
                'title': 'Analyse SWOT',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '🎯 Analyse SWOT', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '💪 Forces', 'type': 'group', 'x': 250, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '3', 'text': '⚠️ Faiblesses', 'type': 'group', 'x': 550, 'y': 200, 'color': '#f59e0b', 'size': 25},
                    {'id': '4', 'text': '🚀 Opportunités', 'type': 'group', 'x': 250, 'y': 400, 'color': '#3b82f6', 'size': 25},
                    {'id': '5', 'text': '🛡️ Menaces', 'type': 'group', 'x': 550, 'y': 400, 'color': '#ef4444', 'size': 25}
                ],
                'connections': []
            },
            'en': {
                'title': 'SWOT Analysis',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '🎯 SWOT Analysis', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '💪 Strengths', 'type': 'group', 'x': 250, 'y': 200, 'color': '#10b981', 'size': 25},
                    {'id': '3', 'text': '⚠️ Weaknesses', 'type': 'group', 'x': 550, 'y': 200, 'color': '#f59e0b', 'size': 25},
                    {'id': '4', 'text': '🚀 Opportunities', 'type': 'group', 'x': 250, 'y': 400, 'color': '#3b82f6', 'size': 25},
                    {'id': '5', 'text': '🛡️ Threats', 'type': 'group', 'x': 550, 'y': 400, 'color': '#ef4444', 'size': 25}
                ],
                'connections': []
            }
        },
        'brainstorming': {
            'fr': {
                'title': 'Brainstorming',
                'mode': 'buzan',
                'nodes': [
                    {'id': '1', 'text': '💡 Idée Principale', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 35}
                ],
                'connections': []
            },
            'en': {
                'title': 'Brainstorming',
                'mode': 'buzan',
                'nodes': [
                    {'id': '1', 'text': '💡 Main Idea', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 35}
                ],
                'connections': []
            }
        },
        'todo': {
            'fr': {
                'title': 'Liste de Tâches',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '✅ Tâches', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🔴 Urgent', 'type': 'group', 'x': 250, 'y': 200, 'color': '#ef4444', 'size': 25},
                    {'id': '3', 'text': '🟠 Important', 'type': 'group', 'x': 550, 'y': 200, 'color': '#f59e0b', 'size': 25},
                    {'id': '4', 'text': '🟡 Normal', 'type': 'group', 'x': 250, 'y': 400, 'color': '#fbbf24', 'size': 25},
                    {'id': '5', 'text': '🟢 Fait', 'type': 'group', 'x': 550, 'y': 400, 'color': '#10b981', 'size': 25}
                ],
                'connections': []
            },
            'en': {
                'title': 'Task List',
                'mode': 'grinde',
                'nodes': [
                    {'id': '1', 'text': '✅ Tasks', 'type': 'central', 'x': 400, 'y': 300, 'color': '#6366f1', 'size': 30},
                    {'id': '2', 'text': '🔴 Urgent', 'type': 'group', 'x': 250, 'y': 200, 'color': '#ef4444', 'size': 25},
                    {'id': '3', 'text': '🟠 Important', 'type': 'group', 'x': 550, 'y': 200, 'color': '#f59e0b', 'size': 25},
                    {'id': '4', 'text': '🟡 Normal', 'type': 'group', 'x': 250, 'y': 400, 'color': '#fbbf24', 'size': 25},
                    {'id': '5', 'text': '🟢 Done', 'type': 'group', 'x': 550, 'y': 400, 'color': '#10b981', 'size': 25}
                ],
                'connections': []
            }
        }
    }
    
    # Sauvegarder les templates dans les deux langues
    for template_id, template_data in templates.items():
        for lang in ['fr', 'en']:
            filepath = os.path.join(TEMPLATES_FOLDER, f"{template_id}_{lang}.json")
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(template_data[lang], f, indent=2, ensure_ascii=False)

# ==============================================================================
# ROUTES FLASK AMÉLIORÉES
# ==============================================================================

@app.route('/')
def index():
    """Page principale avec détection de langue"""
    return send_file('mindmap-mini-multilingual.html')


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Return application settings consumed by the frontend."""
    settings = {
        'autosave': {
            'default': app.config.get('AUTOSAVE_ENABLED', True),
            'frequency_seconds': app.config.get('AUTOSAVE_FREQUENCY', 60)
        },
        'default_language': app.config.get('DEFAULT_LANGUAGE', 'fr')
    }
    return jsonify(settings)

@app.route('/api/maps', methods=['GET'])
def get_maps():
    """Obtenir la liste des cartes avec support multilingue"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    maps = MindMapManager.list_maps(language)
    return jsonify({'success': True, 'maps': maps})

@app.route('/api/map/<map_id>', methods=['GET'])
def get_map(map_id):
    """Obtenir une carte spécifique"""
    data = MindMapManager.load_map(map_id)
    if data:
        # Calculer le score GRINDE si applicable
        if data.get('mode') == 'grinde':
            data['grindeScore'] = MindMapManager.calculate_grinde_score(data)
        return jsonify({'success': True, 'data': data})
    return jsonify({'success': False, 'error': 'Map not found'}), 404

@app.route('/api/map', methods=['POST'])
def save_map():
    """Sauvegarder une carte (nouvelle ou existante)"""
    data = request.json
    map_id = data.get('id')
    
    # Sauvegarder
    map_id = MindMapManager.save_map(map_id, data)
    
    return jsonify({'success': True, 'id': map_id})

@app.route('/api/map/<map_id>', methods=['DELETE'])
def delete_map(map_id):
    """Supprimer une carte (déplacer vers la corbeille)"""
    if MindMapManager.delete_map(map_id):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Map not found'}), 404

@app.route('/api/map/<map_id>/rename', methods=['POST'])
def rename_map(map_id):
    """Renommer une carte"""
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'success': False, 'error': 'Title is required'}), 400
        
        if MindMapManager.rename_map(map_id, data['title']):
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Map not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/map/<map_id>/duplicate', methods=['POST'])
def duplicate_map(map_id):
    """Dupliquer une carte"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    original = MindMapManager.load_map(map_id)
    if original:
        new_id = MindMapManager.generate_id()
        copy_text = TRANSLATIONS[language]['copy']
        original['title'] = f"{original.get('title', TRANSLATIONS[language]['untitled'])} ({copy_text})"
        original['id'] = new_id
        MindMapManager.save_map(new_id, original)
        return jsonify({'success': True, 'id': new_id})
    return jsonify({'success': False, 'error': 'Map not found'}), 404

@app.route('/api/search', methods=['GET'])
def search_maps():
    """Rechercher dans les cartes"""
    query = request.args.get('q', '')
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    
    if not query:
        return jsonify({'success': False, 'error': 'No query provided'}), 400
    
    results = MindMapManager.search_maps(query, language)
    return jsonify({'success': True, 'results': results})

@app.route('/api/autosave', methods=['POST'])
def autosave():
    """Sauvegarde automatique temporaire"""
    data = request.json
    map_id = data.get('id', 'temp')
    
    # Sauvegarder dans le dossier autosave
    filepath = os.path.join(AUTOSAVE_FOLDER, f"{map_id}_current.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return jsonify({'success': True})

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Obtenir la liste des templates dans la langue demandée"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    templates = []
    
    for filename in os.listdir(TEMPLATES_FOLDER):
        if filename.endswith(f'_{language}.json'):
            template_id = filename.replace(f'_{language}.json', '')
            with open(os.path.join(TEMPLATES_FOLDER, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                templates.append({
                    'id': template_id,
                    'title': data.get('title', 'Template'),
                    'mode': data.get('mode', 'grinde'),
                    'nodeCount': len(data.get('nodes', [])),
                    'preview': data.get('nodes', [{}])[0].get('text', '')[:30] if data.get('nodes') else ''
                })
    
    return jsonify({'success': True, 'templates': templates})

@app.route('/api/template/<template_id>', methods=['GET'])
def get_template(template_id):
    """Obtenir un template spécifique dans la langue demandée"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    filepath = os.path.join(TEMPLATES_FOLDER, f"{template_id}_{language}.json")
    
    # Fallback vers l'anglais si la traduction n'existe pas
    if not os.path.exists(filepath):
        filepath = os.path.join(TEMPLATES_FOLDER, f"{template_id}_en.json")
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify({'success': True, 'data': data})
    
    return jsonify({'success': False, 'error': 'Template not found'}), 404

@app.route('/api/export/<map_id>/<format>', methods=['GET'])
def export_map(map_id, format):
    """Exporter une carte dans différents formats avec support multilingue"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    data = MindMapManager.load_map(map_id)
    
    if not data:
        return jsonify({'success': False, 'error': 'Map not found'}), 404
    
    t = TRANSLATIONS[language]
    
    if format == 'json':
        # Export JSON
        response = make_response(json.dumps(data, indent=2, ensure_ascii=False))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{data.get("title", "mindmap")}.json"'
        return response
    
    elif format == 'text':
        # Export texte simple
        text = generate_text_export(data, language)
        response = make_response(text)
        response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{data.get("title", "mindmap")}.txt"'
        return response
    
    elif format == 'markdown':
        # Export Markdown
        md = generate_markdown_export(data, language)
        response = make_response(md)
        response.headers['Content-Type'] = 'text/markdown; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{data.get("title", "mindmap")}.md"'
        return response
    
    elif format == 'html':
        # Export HTML autonome
        html = generate_html_export(data, language)
        response = make_response(html)
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename="{data.get("title", "mindmap")}.html"'
        return response
    
    return jsonify({'success': False, 'error': 'Format not supported'}), 400

@app.route('/api/export-all', methods=['GET'])
def export_all():
    """Exporter toutes les cartes en ZIP"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Ajouter toutes les cartes
        for filename in os.listdir(MAPS_FOLDER):
            if filename.endswith('.json') and not filename.startswith('.'):
                filepath = os.path.join(MAPS_FOLDER, filename)
                zip_file.write(filepath, f'maps/{filename}')
        
        # Ajouter les templates
        for filename in os.listdir(TEMPLATES_FOLDER):
            if filename.endswith('.json'):
                filepath = os.path.join(TEMPLATES_FOLDER, filename)
                zip_file.write(filepath, f'templates/{filename}')
    
    zip_buffer.seek(0)
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'mindmap_mini_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
    )

@app.route('/api/import', methods=['POST'])
def import_map():
    """Importer une carte depuis un fichier JSON"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    try:
        # Lire le fichier JSON
        content = file.read().decode('utf-8')
        data = json.loads(content)
        
        # Générer un nouvel ID et sauvegarder
        new_id = MindMapManager.save_map(None, data)
        
        return jsonify({'success': True, 'id': new_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtenir les statistiques globales avec support multilingue"""
    language = request.args.get('lang', app.config['DEFAULT_LANGUAGE'])
    maps = MindMapManager.list_maps(language)
    
    # Calculer les statistiques détaillées
    total_nodes = sum(m['nodeCount'] for m in maps)
    total_connections = sum(m.get('connectionCount', 0) for m in maps)
    grinde_maps = [m for m in maps if m['mode'] == 'grinde']
    buzan_maps = [m for m in maps if m['mode'] == 'buzan']
    
    # Score GRINDE moyen
    avg_grinde_score = 0
    if grinde_maps:
        scores = [m.get('grindeScore', {}).get('total', 0) for m in grinde_maps if m.get('grindeScore')]
        if scores:
            avg_grinde_score = sum(scores) / len(scores)
    
    stats = {
        'totalMaps': len(maps),
        'totalNodes': total_nodes,
        'totalConnections': total_connections,
        'grindeCount': len(grinde_maps),
        'buzanCount': len(buzan_maps),
        'avgGrindeScore': round(avg_grinde_score, 1),
        'recentMaps': maps[:5],
        'mostUsedMode': 'grinde' if len(grinde_maps) >= len(buzan_maps) else 'buzan',
        'avgNodesPerMap': round(total_nodes / len(maps), 1) if maps else 0
    }
    
    return jsonify({'success': True, 'stats': stats})

# ==============================================================================
# FONCTIONS D'EXPORT MULTILINGUES
# ==============================================================================

def generate_text_export(data, language='fr'):
    """Générer un export en texte simple avec support multilingue"""
    t = TRANSLATIONS[language]
    
    text = f"{data.get('title', t['mind_map'])}\n"
    text += "=" * len(data.get('title', t['mind_map'])) + "\n\n"
    text += f"{t['mode']}: {data.get('mode', 'grinde').upper()}\n"
    text += f"{t['created']}: {data.get('created', '')[:10]}\n"
    text += f"{t['modified']}: {data.get('modified', '')[:10]}\n\n"
    
    # Organiser les nœuds par type
    nodes_by_type = defaultdict(list)
    for node in data.get('nodes', []):
        node_type = node.get('type', 'concept')
        nodes_by_type[node_type].append(node.get('text', ''))
    
    # Afficher les nœuds
    if 'central' in nodes_by_type:
        text += f"{t['central_idea']}:\n"
        for item in nodes_by_type['central']:
            text += f"  ★ {item}\n"
        text += "\n"
    
    if 'group' in nodes_by_type:
        text += f"{t['groups']}:\n"
        for item in nodes_by_type['group']:
            text += f"  ◆ {item}\n"
        text += "\n"
    
    if 'concept' in nodes_by_type:
        text += f"{t['concepts']}:\n"
        for item in nodes_by_type['concept']:
            text += f"  • {item}\n"
        text += "\n"
    
    if 'detail' in nodes_by_type:
        text += f"{t['details']}:\n"
        for item in nodes_by_type['detail']:
            text += f"  - {item}\n"
        text += "\n"
    
    # Statistiques
    text += f"\n{t['statistics']}:\n"
    text += f"  {t['total_nodes']}: {len(data.get('nodes', []))}\n"
    text += f"  {t['total_connections']}: {len(data.get('connections', []))}\n"
    
    return text

def generate_markdown_export(data, language='fr'):
    """Générer un export en Markdown avec support multilingue"""
    t = TRANSLATIONS[language]
    
    md = f"# {data.get('title', t['mind_map'])}\n\n"
    md += f"**{t['mode']}:** {data.get('mode', 'grinde').upper()}  \n"
    md += f"**{t['created']}:** {data.get('created', '')[:10]}  \n"
    md += f"**{t['modified']}:** {data.get('modified', '')[:10]}  \n\n"
    
    # Score GRINDE si applicable
    if data.get('mode') == 'grinde':
        score = MindMapManager.calculate_grinde_score(data)
        if score:
            md += f"## 📊 Score GRINDE: {score['total']}/100\n\n"
            md += f"- Grouped: {score['grouped']}/100\n"
            md += f"- Reflective: {score['reflective']}/100\n"
            md += f"- Interconnected: {score['interconnected']}/100\n"
            md += f"- Non-verbal: {score['nonverbal']}/100\n"
            md += f"- Directional: {score['directional']}/100\n"
            md += f"- Emphasized: {score['emphasized']}/100\n\n"
    
    # Organiser les nœuds
    nodes_by_type = defaultdict(list)
    for node in data.get('nodes', []):
        node_type = node.get('type', 'concept')
        nodes_by_type[node_type].append(node.get('text', ''))
    
    # Afficher les nœuds
    if 'central' in nodes_by_type:
        md += f"## 🎯 {t['central_idea']}\n\n"
        for item in nodes_by_type['central']:
            md += f"**{item}**\n\n"
    
    if 'group' in nodes_by_type:
        md += f"## 📦 {t['groups']}\n\n"
        for item in nodes_by_type['group']:
            md += f"### {item}\n\n"
    
    if 'concept' in nodes_by_type:
        md += f"## 💡 {t['concepts']}\n\n"
        for item in nodes_by_type['concept']:
            md += f"- {item}\n"
        md += "\n"
    
    if 'detail' in nodes_by_type:
        md += f"## 📝 {t['details']}\n\n"
        for item in nodes_by_type['detail']:
            md += f"  - {item}\n"
        md += "\n"
    
    # Ajouter les connexions si présentes
    if data.get('connections'):
        md += f"\n## 🔗 {t['connections']}\n\n"
        md += f"{t['total_connections']}: {len(data['connections'])}\n"
    
    return md

def generate_html_export(data, language='fr'):
    """Générer un export HTML autonome avec visualisation et support multilingue"""
    t = TRANSLATIONS[language]
    
    html = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('title', t['mind_map'])}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #6366f1;
            border-bottom: 3px solid #6366f1;
            padding-bottom: 10px;
        }}
        .meta {{
            color: #6b7280;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .section {{
            margin: 20px 0;
        }}
        .section h2 {{
            color: #4b5563;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .central {{
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0;
        }}
        .group {{
            background: #f3f4f6;
            padding: 15px;
            border-left: 4px solid #f59e0b;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .concept {{
            background: #e0f2fe;
            padding: 10px;
            border-left: 4px solid #3b82f6;
            margin: 8px 0;
            border-radius: 5px;
        }}
        .detail {{
            padding: 8px;
            margin: 5px 0;
            color: #6b7280;
        }}
        .stats {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        .stat {{
            background: #f9fafb;
            padding: 15px;
            border-radius: 10px;
            flex: 1;
            min-width: 150px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #6366f1;
        }}
        .stat-label {{
            color: #6b7280;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .grinde-score {{
            background: linear-gradient(135deg, #8b5cf6, #7c3aed);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        .score-bar {{
            background: rgba(255,255,255,0.3);
            height: 20px;
            border-radius: 10px;
            margin: 10px 0;
            overflow: hidden;
        }}
        .score-fill {{
            background: white;
            height: 100%;
            border-radius: 10px;
            transition: width 0.5s ease;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data.get('title', t['mind_map'])}</h1>
        
        <div class="meta">
            <strong>{t['mode']}:</strong> {data.get('mode', 'grinde').upper()} | 
            <strong>{t['created']}:</strong> {data.get('created', '')[:10]} | 
            <strong>{t['modified']}:</strong> {data.get('modified', '')[:10]}
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(data.get('nodes', []))}</div>
                <div class="stat-label">{t['nodes']}</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(data.get('connections', []))}</div>
                <div class="stat-label">{t['connections']}</div>
            </div>
            <div class="stat">
                <div class="stat-value">{data.get('mode', 'grinde').upper()}</div>
                <div class="stat-label">{t['mode']}</div>
            </div>
        </div>
        """
    
    # Ajouter le score GRINDE si applicable
    if data.get('mode') == 'grinde':
        score = MindMapManager.calculate_grinde_score(data)
        if score:
            html += f"""
        <div class="grinde-score">
            <h2>📊 Score GRINDE: {score['total']}/100</h2>
            <div>
                <div>Grouped ({score['grouped']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['grouped']}%"></div></div>
            </div>
            <div>
                <div>Reflective ({score['reflective']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['reflective']}%"></div></div>
            </div>
            <div>
                <div>Interconnected ({score['interconnected']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['interconnected']}%"></div></div>
            </div>
            <div>
                <div>Non-verbal ({score['nonverbal']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['nonverbal']}%"></div></div>
            </div>
            <div>
                <div>Directional ({score['directional']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['directional']}%"></div></div>
            </div>
            <div>
                <div>Emphasized ({score['emphasized']}/100)</div>
                <div class="score-bar"><div class="score-fill" style="width: {score['emphasized']}%"></div></div>
            </div>
        </div>
            """
    
    # Organiser et afficher les nœuds
    nodes_by_type = defaultdict(list)
    for node in data.get('nodes', []):
        nodes_by_type[node.get('type', 'concept')].append(node)
    
    # Central
    if 'central' in nodes_by_type:
        for node in nodes_by_type['central']:
            html += f'<div class="central">{node.get("text", "")}</div>'
    
    # Groupes
    if 'group' in nodes_by_type:
        html += f'<div class="section"><h2>📦 {t["groups"]}</h2>'
        for node in nodes_by_type['group']:
            html += f'<div class="group">{node.get("text", "")}</div>'
        html += '</div>'
    
    # Concepts
    if 'concept' in nodes_by_type:
        html += f'<div class="section"><h2>💡 {t["concepts"]}</h2>'
        for node in nodes_by_type['concept']:
            html += f'<div class="concept">{node.get("text", "")}</div>'
        html += '</div>'
    
    # Détails
    if 'detail' in nodes_by_type:
        html += f'<div class="section"><h2>📝 {t["details"]}</h2>'
        for node in nodes_by_type['detail']:
            html += f'<div class="detail">• {node.get("text", "")}</div>'
        html += '</div>'
    
    html += """
    </div>
</body>
</html>"""
    
    return html

# ==============================================================================
# INITIALISATION
# ==============================================================================

def initialize():
    """Initialiser l'application au premier démarrage"""
    init_templates()
    print("✅ Mind Map Mini initialisé")
    print(f"📁 Dossier des cartes : {os.path.abspath(MAPS_FOLDER)}")
    print(f"💾 Dossier de sauvegarde auto : {os.path.abspath(AUTOSAVE_FOLDER)}")
    print(f"🌍 Langue par défaut : {app.config['DEFAULT_LANGUAGE']}")

# ==============================================================================
# POINT D'ENTRÉE
# ==============================================================================

if __name__ == '__main__':
    # Initialize the application
    initialize()
    
    print("""
    ╔══════════════════════════════════════╗
    ║     🧠 Mind Map Mini - v1.0.0       ║
    ║   Outil de Cartographie Mentale      ║
    ║     Multilingue FR/EN - JSON         ║
    ╚══════════════════════════════════════╝
    
    🚀 Démarrage du serveur sur http://localhost:5000
    🇫🇷 Interface en français par défaut
    📁 Toutes les cartes sauvées dans ./mindmaps/
    💾 Sauvegarde automatique activée
    """)
    
    app.run(debug=True, port=5000, host='127.0.0.1')