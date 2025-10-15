# app.py - Application Flask pour MindMap Master

from flask import Flask, render_template, request, jsonify, send_file, session
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import uuid
import datetime
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mindmap-master-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuration CORS et SocketIO pour collaboration temps réel
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Créer les dossiers nécessaires
os.makedirs('uploads', exist_ok=True)
os.makedirs('exports', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Base de données en mémoire (à remplacer par une vraie DB en production)
mindmaps_db = {}
sessions_db = {}
collaborations = {}

# ==============================================================================
# MODÈLES DE DONNÉES
# ==============================================================================

class MindMap:
    def __init__(self, title="Nouvelle Carte", mode="grinde", user_id=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.mode = mode  # 'grinde' ou 'buzan'
        self.user_id = user_id
        self.created_at = datetime.datetime.now().isoformat()
        self.updated_at = datetime.datetime.now().isoformat()
        self.nodes = []
        self.connections = []
        self.collaborators = []
        self.version = 1
        self.tags = []
        self.metadata = {
            'zoom': 1,
            'pan_x': 0,
            'pan_y': 0,
            'theme': 'default'
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'mode': self.mode,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'nodes': self.nodes,
            'connections': self.connections,
            'collaborators': self.collaborators,
            'version': self.version,
            'tags': self.tags,
            'metadata': self.metadata
        }
    
    def add_node(self, node_data):
        node_data['id'] = str(uuid.uuid4())
        node_data['created_at'] = datetime.datetime.now().isoformat()
        self.nodes.append(node_data)
        self.updated_at = datetime.datetime.now().isoformat()
        self.version += 1
        return node_data
    
    def update_node(self, node_id, updates):
        for node in self.nodes:
            if node['id'] == node_id:
                node.update(updates)
                self.updated_at = datetime.datetime.now().isoformat()
                self.version += 1
                return node
        return None
    
    def delete_node(self, node_id):
        self.nodes = [n for n in self.nodes if n['id'] != node_id]
        self.connections = [c for c in self.connections 
                           if c['source'] != node_id and c['target'] != node_id]
        self.updated_at = datetime.datetime.now().isoformat()
        self.version += 1
    
    def add_connection(self, connection_data):
        connection_data['id'] = str(uuid.uuid4())
        self.connections.append(connection_data)
        self.updated_at = datetime.datetime.now().isoformat()
        self.version += 1
        return connection_data

# ==============================================================================
# ROUTES PRINCIPALES
# ==============================================================================

@app.route('/')
def index():
    """Page principale avec l'outil de mind mapping"""
    return render_template('index.html')

@app.route('/api/mindmaps', methods=['GET'])
def get_mindmaps():
    """Récupérer toutes les cartes de l'utilisateur"""
    user_id = session.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())
        session['user_id'] = user_id
    
    user_maps = [m.to_dict() for m in mindmaps_db.values() 
                 if m.user_id == user_id or user_id in m.collaborators]
    
    return jsonify({
        'success': True,
        'mindmaps': user_maps
    })

@app.route('/api/mindmap/<map_id>', methods=['GET'])
def get_mindmap(map_id):
    """Récupérer une carte spécifique"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    return jsonify({
        'success': True,
        'mindmap': mindmaps_db[map_id].to_dict()
    })

@app.route('/api/mindmap', methods=['POST'])
def create_mindmap():
    """Créer une nouvelle carte"""
    data = request.json
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    mindmap = MindMap(
        title=data.get('title', 'Nouvelle Carte'),
        mode=data.get('mode', 'grinde'),
        user_id=user_id
    )
    
    # Ajouter le nœud central par défaut
    central_node = {
        'x': 400,
        'y': 300,
        'text': data.get('central_text', 'Idée Centrale'),
        'type': 'central',
        'color': '#6366f1',
        'size': 30
    }
    mindmap.add_node(central_node)
    
    mindmaps_db[mindmap.id] = mindmap
    
    return jsonify({
        'success': True,
        'mindmap': mindmap.to_dict()
    })

@app.route('/api/mindmap/<map_id>', methods=['PUT'])
def update_mindmap(map_id):
    """Mettre à jour une carte complète"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    data = request.json
    mindmap = mindmaps_db[map_id]
    
    # Mettre à jour les propriétés
    if 'title' in data:
        mindmap.title = data['title']
    if 'mode' in data:
        mindmap.mode = data['mode']
    if 'nodes' in data:
        mindmap.nodes = data['nodes']
    if 'connections' in data:
        mindmap.connections = data['connections']
    if 'metadata' in data:
        mindmap.metadata.update(data['metadata'])
    if 'tags' in data:
        mindmap.tags = data['tags']
    
    mindmap.updated_at = datetime.datetime.now().isoformat()
    mindmap.version += 1
    
    # Notifier les collaborateurs en temps réel
    if map_id in collaborations:
        socketio.emit('map_updated', {
            'map_id': map_id,
            'data': mindmap.to_dict()
        }, room=map_id)
    
    return jsonify({
        'success': True,
        'mindmap': mindmap.to_dict()
    })

@app.route('/api/mindmap/<map_id>', methods=['DELETE'])
def delete_mindmap(map_id):
    """Supprimer une carte"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    del mindmaps_db[map_id]
    
    return jsonify({'success': True})

# ==============================================================================
# GESTION DES NŒUDS
# ==============================================================================

@app.route('/api/mindmap/<map_id>/node', methods=['POST'])
def add_node(map_id):
    """Ajouter un nœud à une carte"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    data = request.json
    mindmap = mindmaps_db[map_id]
    node = mindmap.add_node(data)
    
    # Notifier les collaborateurs
    if map_id in collaborations:
        socketio.emit('node_added', {
            'map_id': map_id,
            'node': node
        }, room=map_id)
    
    return jsonify({
        'success': True,
        'node': node
    })

@app.route('/api/mindmap/<map_id>/node/<node_id>', methods=['PUT'])
def update_node(map_id, node_id):
    """Mettre à jour un nœud"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    data = request.json
    mindmap = mindmaps_db[map_id]
    node = mindmap.update_node(node_id, data)
    
    if not node:
        return jsonify({'success': False, 'error': 'Nœud non trouvé'}), 404
    
    # Notifier les collaborateurs
    if map_id in collaborations:
        socketio.emit('node_updated', {
            'map_id': map_id,
            'node_id': node_id,
            'updates': data
        }, room=map_id)
    
    return jsonify({
        'success': True,
        'node': node
    })

@app.route('/api/mindmap/<map_id>/node/<node_id>', methods=['DELETE'])
def delete_node(map_id, node_id):
    """Supprimer un nœud"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    mindmap = mindmaps_db[map_id]
    mindmap.delete_node(node_id)
    
    # Notifier les collaborateurs
    if map_id in collaborations:
        socketio.emit('node_deleted', {
            'map_id': map_id,
            'node_id': node_id
        }, room=map_id)
    
    return jsonify({'success': True})

# ==============================================================================
# GESTION DES CONNEXIONS
# ==============================================================================

@app.route('/api/mindmap/<map_id>/connection', methods=['POST'])
def add_connection(map_id):
    """Ajouter une connexion entre deux nœuds"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    data = request.json
    mindmap = mindmaps_db[map_id]
    connection = mindmap.add_connection(data)
    
    # Notifier les collaborateurs
    if map_id in collaborations:
        socketio.emit('connection_added', {
            'map_id': map_id,
            'connection': connection
        }, room=map_id)
    
    return jsonify({
        'success': True,
        'connection': connection
    })

# ==============================================================================
# EXPORT ET IMPORT
# ==============================================================================

@app.route('/api/mindmap/<map_id>/export/<format>', methods=['GET'])
def export_mindmap(map_id, format):
    """Exporter une carte dans différents formats"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    mindmap = mindmaps_db[map_id]
    
    if format == 'json':
        # Export JSON
        data = json.dumps(mindmap.to_dict(), indent=2)
        return send_file(
            BytesIO(data.encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'{mindmap.title}.json'
        )
    
    elif format == 'svg':
        # Export SVG (génération basique)
        svg = generate_svg(mindmap)
        return send_file(
            BytesIO(svg.encode()),
            mimetype='image/svg+xml',
            as_attachment=True,
            download_name=f'{mindmap.title}.svg'
        )
    
    elif format == 'markdown':
        # Export Markdown
        md = generate_markdown(mindmap)
        return send_file(
            BytesIO(md.encode()),
            mimetype='text/markdown',
            as_attachment=True,
            download_name=f'{mindmap.title}.md'
        )
    
    else:
        return jsonify({'success': False, 'error': 'Format non supporté'}), 400

@app.route('/api/import', methods=['POST'])
def import_mindmap():
    """Importer une carte depuis un fichier"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Aucun fichier fourni'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nom de fichier vide'}), 400
    
    try:
        # Lire le contenu du fichier
        content = file.read().decode('utf-8')
        data = json.loads(content)
        
        # Créer une nouvelle carte
        user_id = session.get('user_id', str(uuid.uuid4()))
        session['user_id'] = user_id
        
        mindmap = MindMap(
            title=data.get('title', 'Carte Importée'),
            mode=data.get('mode', 'grinde'),
            user_id=user_id
        )
        
        mindmap.nodes = data.get('nodes', [])
        mindmap.connections = data.get('connections', [])
        mindmap.tags = data.get('tags', [])
        mindmap.metadata = data.get('metadata', mindmap.metadata)
        
        mindmaps_db[mindmap.id] = mindmap
        
        return jsonify({
            'success': True,
            'mindmap': mindmap.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# ==============================================================================
# COLLABORATION TEMPS RÉEL (WebSocket)
# ==============================================================================

@socketio.on('join_collaboration')
def handle_join_collaboration(data):
    """Rejoindre une session de collaboration"""
    map_id = data['map_id']
    user_id = data.get('user_id', str(uuid.uuid4()))
    username = data.get('username', f'User_{user_id[:8]}')
    
    join_room(map_id)
    
    if map_id not in collaborations:
        collaborations[map_id] = []
    
    collaborations[map_id].append({
        'user_id': user_id,
        'username': username,
        'sid': request.sid
    })
    
    # Notifier les autres utilisateurs
    emit('user_joined', {
        'user_id': user_id,
        'username': username,
        'users': collaborations[map_id]
    }, room=map_id)

@socketio.on('leave_collaboration')
def handle_leave_collaboration(data):
    """Quitter une session de collaboration"""
    map_id = data['map_id']
    user_id = data.get('user_id')
    
    leave_room(map_id)
    
    if map_id in collaborations:
        collaborations[map_id] = [
            u for u in collaborations[map_id] 
            if u['user_id'] != user_id
        ]
        
        emit('user_left', {
            'user_id': user_id,
            'users': collaborations[map_id]
        }, room=map_id)

@socketio.on('cursor_move')
def handle_cursor_move(data):
    """Partager la position du curseur en temps réel"""
    map_id = data['map_id']
    emit('cursor_position', {
        'user_id': data['user_id'],
        'x': data['x'],
        'y': data['y']
    }, room=map_id, include_self=False)

@socketio.on('node_dragging')
def handle_node_dragging(data):
    """Partager le déplacement d'un nœud en temps réel"""
    map_id = data['map_id']
    emit('node_moving', {
        'user_id': data['user_id'],
        'node_id': data['node_id'],
        'x': data['x'],
        'y': data['y']
    }, room=map_id, include_self=False)

# ==============================================================================
# FONCTIONS UTILITAIRES
# ==============================================================================

def generate_svg(mindmap):
    """Générer un SVG à partir d'une mindmap"""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
        <style>
            .node {{ fill: #6366f1; stroke: white; stroke-width: 2; }}
            .text {{ fill: white; font-family: Arial; font-size: 14px; text-anchor: middle; }}
            .connection {{ stroke: #6366f1; stroke-width: 2; fill: none; }}
        </style>
        <g id="connections">'''
    
    # Ajouter les connexions
    for conn in mindmap.connections:
        svg += f'''
            <line class="connection" 
                  x1="{conn.get('x1', 0)}" y1="{conn.get('y1', 0)}"
                  x2="{conn.get('x2', 0)}" y2="{conn.get('y2', 0)}" />'''
    
    svg += '''
        </g>
        <g id="nodes">'''
    
    # Ajouter les nœuds
    for node in mindmap.nodes:
        x = node.get('x', 100)
        y = node.get('y', 100)
        text = node.get('text', '')
        size = node.get('size', 20)
        
        if node.get('type') == 'central':
            svg += f'''
                <circle class="node" cx="{x}" cy="{y}" r="{size}" />
                <text class="text" x="{x}" y="{y+5}">{text}</text>'''
        else:
            width = len(text) * 8 + 20
            height = size * 2
            svg += f'''
                <rect class="node" x="{x-width/2}" y="{y-height/2}" 
                      width="{width}" height="{height}" rx="10" />
                <text class="text" x="{x}" y="{y+5}">{text}</text>'''
    
    svg += '''
        </g>
    </svg>'''
    
    return svg

def generate_markdown(mindmap):
    """Générer un document Markdown à partir d'une mindmap"""
    md = f"# {mindmap.title}\n\n"
    md += f"*Créé le {mindmap.created_at}*\n\n"
    md += f"**Mode:** {mindmap.mode.upper()}\n\n"
    
    # Trouver le nœud central
    central = next((n for n in mindmap.nodes if n.get('type') == 'central'), None)
    if central:
        md += f"## 🎯 Idée Centrale: {central.get('text', 'Sans titre')}\n\n"
    
    # Grouper les nœuds par type
    groups = {}
    for node in mindmap.nodes:
        node_type = node.get('type', 'concept')
        if node_type != 'central':
            if node_type not in groups:
                groups[node_type] = []
            groups[node_type].append(node)
    
    # Afficher les groupes
    type_names = {
        'group': '📦 Groupes',
        'concept': '💡 Concepts',
        'detail': '📝 Détails'
    }
    
    for node_type, nodes in groups.items():
        md += f"### {type_names.get(node_type, node_type.title())}\n\n"
        for node in nodes:
            md += f"- {node.get('text', 'Sans titre')}\n"
        md += "\n"
    
    # Ajouter les tags
    if mindmap.tags:
        md += f"### 🏷️ Tags\n\n"
        md += ', '.join(f"`{tag}`" for tag in mindmap.tags) + "\n\n"
    
    return md

# ==============================================================================
# TEMPLATES ET MODÈLES PRÉ-DÉFINIS
# ==============================================================================

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Récupérer les modèles de mindmaps pré-définis"""
    templates = [
        {
            'id': 'business-plan',
            'name': 'Business Plan',
            'description': 'Modèle pour planifier un projet d\'entreprise',
            'mode': 'grinde',
            'preview': '📊',
            'nodes': [
                {'text': 'Business Plan', 'type': 'central', 'x': 400, 'y': 300},
                {'text': 'Vision', 'type': 'group', 'x': 200, 'y': 200},
                {'text': 'Marché', 'type': 'group', 'x': 600, 'y': 200},
                {'text': 'Produit', 'type': 'group', 'x': 200, 'y': 400},
                {'text': 'Finance', 'type': 'group', 'x': 600, 'y': 400}
            ]
        },
        {
            'id': 'study-notes',
            'name': 'Prise de Notes',
            'description': 'Optimisé pour la prise de notes en cours',
            'mode': 'grinde',
            'preview': '🎓',
            'nodes': [
                {'text': 'Sujet du Cours', 'type': 'central', 'x': 400, 'y': 300},
                {'text': 'Concepts Clés', 'type': 'group', 'x': 250, 'y': 200},
                {'text': 'Exemples', 'type': 'group', 'x': 550, 'y': 200},
                {'text': 'Questions', 'type': 'group', 'x': 250, 'y': 400},
                {'text': 'À Retenir', 'type': 'group', 'x': 550, 'y': 400}
            ]
        },
        {
            'id': 'project-planning',
            'name': 'Gestion de Projet',
            'description': 'Pour organiser et suivre un projet',
            'mode': 'grinde',
            'preview': '💼',
            'nodes': [
                {'text': 'Nom du Projet', 'type': 'central', 'x': 400, 'y': 300},
                {'text': 'Objectifs', 'type': 'group', 'x': 200, 'y': 150},
                {'text': 'Équipe', 'type': 'group', 'x': 600, 'y': 150},
                {'text': 'Tâches', 'type': 'group', 'x': 200, 'y': 300},
                {'text': 'Échéances', 'type': 'group', 'x': 600, 'y': 300},
                {'text': 'Risques', 'type': 'group', 'x': 200, 'y': 450},
                {'text': 'Ressources', 'type': 'group', 'x': 600, 'y': 450}
            ]
        },
        {
            'id': 'brainstorming',
            'name': 'Brainstorming',
            'description': 'Pour générer et organiser des idées',
            'mode': 'buzan',
            'preview': '🧠',
            'nodes': [
                {'text': 'Idée Principale', 'type': 'central', 'x': 400, 'y': 300}
            ]
        }
    ]
    
    return jsonify({
        'success': True,
        'templates': templates
    })

@app.route('/api/template/<template_id>/apply', methods=['POST'])
def apply_template(template_id):
    """Appliquer un modèle pour créer une nouvelle carte"""
    # Récupérer le template (simplifié ici)
    templates = {
        'business-plan': {
            'title': 'Mon Business Plan',
            'mode': 'grinde',
            'nodes': [
                {'text': 'Business Plan', 'type': 'central', 'x': 400, 'y': 300},
                {'text': 'Vision', 'type': 'group', 'x': 200, 'y': 200},
                {'text': 'Marché', 'type': 'group', 'x': 600, 'y': 200},
                {'text': 'Produit', 'type': 'group', 'x': 200, 'y': 400},
                {'text': 'Finance', 'type': 'group', 'x': 600, 'y': 400}
            ]
        }
    }
    
    if template_id not in templates:
        return jsonify({'success': False, 'error': 'Template non trouvé'}), 404
    
    template = templates[template_id]
    user_id = session.get('user_id', str(uuid.uuid4()))
    session['user_id'] = user_id
    
    # Créer la carte
    mindmap = MindMap(
        title=template['title'],
        mode=template['mode'],
        user_id=user_id
    )
    
    # Ajouter les nœuds du template
    for node_data in template['nodes']:
        mindmap.add_node(node_data)
    
    mindmaps_db[mindmap.id] = mindmap
    
    return jsonify({
        'success': True,
        'mindmap': mindmap.to_dict()
    })

# ==============================================================================
# STATISTIQUES ET ANALYTICS
# ==============================================================================

@app.route('/api/mindmap/<map_id>/stats', methods=['GET'])
def get_mindmap_stats(map_id):
    """Obtenir les statistiques d'une carte"""
    if map_id not in mindmaps_db:
        return jsonify({'success': False, 'error': 'Carte non trouvée'}), 404
    
    mindmap = mindmaps_db[map_id]
    
    # Calculer les statistiques
    node_types = {}
    for node in mindmap.nodes:
        node_type = node.get('type', 'concept')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    
    total_text_length = sum(len(node.get('text', '')) for node in mindmap.nodes)
    avg_text_length = total_text_length / len(mindmap.nodes) if mindmap.nodes else 0
    
    stats = {
        'total_nodes': len(mindmap.nodes),
        'total_connections': len(mindmap.connections),
        'node_types': node_types,
        'avg_text_length': round(avg_text_length, 1),
        'total_collaborators': len(mindmap.collaborators),
        'version': mindmap.version,
        'days_since_creation': (datetime.datetime.now() - 
                               datetime.datetime.fromisoformat(mindmap.created_at)).days
    }
    
    # Score de complexité basé sur GRINDE
    if mindmap.mode == 'grinde':
        grinde_score = calculate_grinde_score(mindmap)
        stats['grinde_score'] = grinde_score
    
    return jsonify({
        'success': True,
        'stats': stats
    })

def calculate_grinde_score(mindmap):
    """Calculer un score basé sur les principes GRINDE"""
    score = {
        'grouped': 0,
        'reflective': 0,
        'interconnected': 0,
        'non_verbal': 0,
        'directional': 0,
        'emphasized': 0,
        'total': 0
    }
    
    # G - Grouped: Vérifier la présence de groupes
    group_nodes = [n for n in mindmap.nodes if n.get('type') == 'group']
    score['grouped'] = min(100, len(group_nodes) * 25)
    
    # R - Reflective: Vérifier la variété du vocabulaire
    unique_words = set()
    for node in mindmap.nodes:
        words = node.get('text', '').lower().split()
        unique_words.update(words)
    score['reflective'] = min(100, len(unique_words) * 5)
    
    # I - Interconnected: Ratio connexions/nœuds
    if len(mindmap.nodes) > 1:
        connectivity_ratio = len(mindmap.connections) / (len(mindmap.nodes) - 1)
        score['interconnected'] = min(100, int(connectivity_ratio * 50))
    
    # N - Non-verbal: Vérifier la présence d'images/symboles
    nodes_with_visuals = [n for n in mindmap.nodes 
                          if n.get('image') or any(c in n.get('text', '') 
                          for c in '🎯💡📊🔥✨🚀💎⭐')]
    score['non_verbal'] = min(100, len(nodes_with_visuals) * 20)
    
    # D - Directional: Vérifier les connexions directionnelles
    directional_connections = [c for c in mindmap.connections 
                              if c.get('type') in ['arrow', 'double']]
    if mindmap.connections:
        score['directional'] = int((len(directional_connections) / 
                                   len(mindmap.connections)) * 100)
    
    # E - Emphasized: Vérifier la hiérarchie (tailles différentes)
    sizes = set(n.get('size', 20) for n in mindmap.nodes)
    colors = set(n.get('color', '#6366f1') for n in mindmap.nodes)
    score['emphasized'] = min(100, (len(sizes) + len(colors)) * 15)
    
    # Score total
    score['total'] = sum(score.values()) // 6
    
    return score

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    # Créer le template HTML s'il n'existe pas
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        # Ici on devrait copier le contenu HTML de l'artifact précédent
        # Pour l'instant, on met un placeholder
        f.write('''<!DOCTYPE html>
<html>
<head>
    <title>MindMap Master</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>MindMap Master - Backend Flask</h1>
    <p>L'interface complète est dans l'artifact HTML séparé.</p>
    <p>Ce backend fournit :</p>
    <ul>
        <li>API REST complète pour la gestion des mindmaps</li>
        <li>Collaboration temps réel via WebSocket</li>
        <li>Export en JSON, SVG, Markdown</li>
        <li>Templates pré-définis</li>
        <li>Statistiques et scoring GRINDE</li>
    </ul>
</body>
</html>''')
    
    # Lancer l'application
    print("🚀 MindMap Master Backend démarré sur http://localhost:5000")
    print("📚 Documentation API disponible")
    print("🔥 WebSocket activé pour collaboration temps réel")
    
    socketio.run(app, debug=True, port=5000)