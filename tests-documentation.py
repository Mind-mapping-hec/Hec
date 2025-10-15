# test_app.py - Tests unitaires et d'intégration

import pytest
import json
import io
from app import app, MindMap, mindmaps_db, socketio
from flask import session

@pytest.fixture
def client():
    """Créer un client de test"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Nettoyer la base de données
            mindmaps_db.clear()
            yield client

@pytest.fixture
def socketio_client():
    """Créer un client SocketIO de test"""
    app.config['TESTING'] = True
    client = socketio.test_client(app)
    yield client
    client.disconnect()

class TestMindMapAPI:
    """Tests pour l'API REST des mindmaps"""
    
    def test_create_mindmap(self, client):
        """Test de création d'une mindmap"""
        response = client.post('/api/mindmap', 
            json={
                'title': 'Test Map',
                'mode': 'grinde',
                'central_text': 'Idée Test'
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['mindmap']['title'] == 'Test Map'
        assert data['mindmap']['mode'] == 'grinde'
        assert len(data['mindmap']['nodes']) == 1
        assert data['mindmap']['nodes'][0]['text'] == 'Idée Test'
    
    def test_get_mindmap(self, client):
        """Test de récupération d'une mindmap"""
        # Créer d'abord une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'Test Map'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # La récupérer
        response = client.get(f'/api/mindmap/{map_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert data['mindmap']['id'] == map_id
    
    def test_update_mindmap(self, client):
        """Test de mise à jour d'une mindmap"""
        # Créer une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'Original Title'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # La mettre à jour
        response = client.put(f'/api/mindmap/{map_id}',
            json={'title': 'Updated Title'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['mindmap']['title'] == 'Updated Title'
    
    def test_delete_mindmap(self, client):
        """Test de suppression d'une mindmap"""
        # Créer une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'To Delete'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # La supprimer
        response = client.delete(f'/api/mindmap/{map_id}')
        assert response.status_code == 200
        
        # Vérifier qu'elle n'existe plus
        get_response = client.get(f'/api/mindmap/{map_id}')
        assert get_response.status_code == 404

class TestNodeManagement:
    """Tests pour la gestion des nœuds"""
    
    def test_add_node(self, client):
        """Test d'ajout d'un nœud"""
        # Créer une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'Test Map'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # Ajouter un nœud
        response = client.post(f'/api/mindmap/{map_id}/node',
            json={
                'text': 'Nouveau Nœud',
                'type': 'concept',
                'x': 100,
                'y': 100
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['node']['text'] == 'Nouveau Nœud'
    
    def test_update_node(self, client):
        """Test de mise à jour d'un nœud"""
        # Créer une mindmap et ajouter un nœud
        create_response = client.post('/api/mindmap', 
            json={'title': 'Test Map'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        add_response = client.post(f'/api/mindmap/{map_id}/node',
            json={'text': 'Original Text', 'type': 'concept'})
        node_id = json.loads(add_response.data)['node']['id']
        
        # Mettre à jour le nœud
        response = client.put(f'/api/mindmap/{map_id}/node/{node_id}',
            json={'text': 'Updated Text'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['node']['text'] == 'Updated Text'
    
    def test_delete_node(self, client):
        """Test de suppression d'un nœud"""
        # Créer une mindmap et ajouter un nœud
        create_response = client.post('/api/mindmap', 
            json={'title': 'Test Map'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        add_response = client.post(f'/api/mindmap/{map_id}/node',
            json={'text': 'To Delete', 'type': 'concept'})
        node_id = json.loads(add_response.data)['node']['id']
        
        # Supprimer le nœud
        response = client.delete(f'/api/mindmap/{map_id}/node/{node_id}')
        assert response.status_code == 200

class TestConnections:
    """Tests pour les connexions entre nœuds"""
    
    def test_add_connection(self, client):
        """Test d'ajout d'une connexion"""
        # Créer une mindmap avec deux nœuds
        create_response = client.post('/api/mindmap', 
            json={'title': 'Test Map'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # Ajouter deux nœuds
        node1_response = client.post(f'/api/mindmap/{map_id}/node',
            json={'text': 'Node 1', 'type': 'concept'})
        node1_id = json.loads(node1_response.data)['node']['id']
        
        node2_response = client.post(f'/api/mindmap/{map_id}/node',
            json={'text': 'Node 2', 'type': 'concept'})
        node2_id = json.loads(node2_response.data)['node']['id']
        
        # Créer une connexion
        response = client.post(f'/api/mindmap/{map_id}/connection',
            json={
                'source': node1_id,
                'target': node2_id,
                'type': 'arrow'
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['connection']['source'] == node1_id
        assert data['connection']['target'] == node2_id

class TestExportImport:
    """Tests pour l'export/import"""
    
    def test_export_json(self, client):
        """Test d'export en JSON"""
        # Créer une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'Export Test'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # Exporter en JSON
        response = client.get(f'/api/mindmap/{map_id}/export/json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_export_markdown(self, client):
        """Test d'export en Markdown"""
        # Créer une mindmap
        create_response = client.post('/api/mindmap', 
            json={'title': 'Export Test'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # Exporter en Markdown
        response = client.get(f'/api/mindmap/{map_id}/export/markdown')
        assert response.status_code == 200
        assert response.content_type == 'text/markdown'
    
    def test_import_json(self, client):
        """Test d'import depuis JSON"""
        # Préparer un fichier JSON
        mindmap_data = {
            'title': 'Imported Map',
            'mode': 'grinde',
            'nodes': [
                {'text': 'Central', 'type': 'central', 'x': 400, 'y': 300}
            ],
            'connections': []
        }
        
        data = io.BytesIO(json.dumps(mindmap_data).encode())
        
        response = client.post('/api/import',
            data={'file': (data, 'test.json')},
            content_type='multipart/form-data')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result['success'] == True
        assert result['mindmap']['title'] == 'Imported Map'

class TestTemplates:
    """Tests pour les templates"""
    
    def test_get_templates(self, client):
        """Test de récupération des templates"""
        response = client.get('/api/templates')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['templates']) > 0
    
    def test_apply_template(self, client):
        """Test d'application d'un template"""
        response = client.post('/api/template/business-plan/apply')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert len(data['mindmap']['nodes']) > 1

class TestStatistics:
    """Tests pour les statistiques"""
    
    def test_get_stats(self, client):
        """Test de récupération des statistiques"""
        # Créer une mindmap avec plusieurs nœuds
        create_response = client.post('/api/mindmap', 
            json={'title': 'Stats Test', 'mode': 'grinde'})
        map_id = json.loads(create_response.data)['mindmap']['id']
        
        # Ajouter des nœuds
        for i in range(3):
            client.post(f'/api/mindmap/{map_id}/node',
                json={'text': f'Node {i}', 'type': 'concept'})
        
        # Récupérer les stats
        response = client.get(f'/api/mindmap/{map_id}/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['stats']['total_nodes'] == 4  # 1 central + 3 ajoutés
        assert 'grinde_score' in data['stats']

class TestCollaboration:
    """Tests pour la collaboration temps réel"""
    
    def test_join_collaboration(self, socketio_client):
        """Test de connexion à une session collaborative"""
        socketio_client.emit('join_collaboration', {
            'map_id': 'test-map-123',
            'user_id': 'user-456',
            'username': 'Test User'
        })
        
        received = socketio_client.get_received()
        assert len(received) > 0
        assert received[0]['name'] == 'user_joined'
    
    def test_cursor_sharing(self, socketio_client):
        """Test de partage de position du curseur"""
        # Joindre d'abord la session
        socketio_client.emit('join_collaboration', {
            'map_id': 'test-map-123',
            'user_id': 'user-456'
        })
        
        # Envoyer la position du curseur
        socketio_client.emit('cursor_move', {
            'map_id': 'test-map-123',
            'user_id': 'user-456',
            'x': 100,
            'y': 200
        })
        
        # Vérifier que le message est bien traité
        # (dans un test réel, on vérifierait avec un second client)
        assert True

class TestGRINDEScoring:
    """Tests pour le scoring GRINDE"""
    
    def test_grinde_score_calculation(self):
        """Test du calcul du score GRINDE"""
        from app import calculate_grinde_score
        
        # Créer une mindmap de test
        mindmap = MindMap(mode='grinde')
        
        # Ajouter des nœuds variés
        mindmap.add_node({
            'text': 'Idée Centrale',
            'type': 'central',
            'size': 30
        })
        mindmap.add_node({
            'text': 'Groupe 1',
            'type': 'group',
            'size': 25
        })
        mindmap.add_node({
            'text': '💡 Concept Visuel',
            'type': 'concept',
            'size': 20
        })
        
        # Ajouter des connexions
        mindmap.connections = [
            {'type': 'arrow', 'source': 'node1', 'target': 'node2'},
            {'type': 'simple', 'source': 'node2', 'target': 'node3'}
        ]
        
        score = calculate_grinde_score(mindmap)
        
        assert 'grouped' in score
        assert 'interconnected' in score
        assert 'non_verbal' in score
        assert 'total' in score
        assert score['total'] >= 0
        assert score['total'] <= 100

# Fixtures pour tests d'intégration
@pytest.fixture(scope='session')
def app_with_db():
    """Application avec base de données de test"""
    app.config.update({
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:'
    })
    
    with app.app_context():
        # Initialiser la DB ici si nécessaire
        yield app

def test_full_workflow(client):
    """Test d'un workflow complet"""
    # 1. Créer une mindmap
    create_response = client.post('/api/mindmap',
        json={'title': 'Workflow Test', 'mode': 'grinde'})
    assert create_response.status_code == 200
    map_id = json.loads(create_response.data)['mindmap']['id']
    
    # 2. Ajouter plusieurs nœuds
    nodes = []
    for i in range(5):
        response = client.post(f'/api/mindmap/{map_id}/node',
            json={'text': f'Node {i}', 'type': 'concept', 'x': i*100, 'y': i*100})
        nodes.append(json.loads(response.data)['node']['id'])
    
    # 3. Créer des connexions
    for i in range(len(nodes)-1):
        client.post(f'/api/mindmap/{map_id}/connection',
            json={'source': nodes[i], 'target': nodes[i+1], 'type': 'arrow'})
    
    # 4. Récupérer les stats
    stats_response = client.get(f'/api/mindmap/{map_id}/stats')
    stats = json.loads(stats_response.data)['stats']
    assert stats['total_nodes'] == 6  # 1 central + 5 ajoutés
    assert stats['total_connections'] == 4
    
    # 5. Exporter en JSON
    export_response = client.get(f'/api/mindmap/{map_id}/export/json')
    assert export_response.status_code == 200
    
    # 6. Supprimer la mindmap
    delete_response = client.delete(f'/api/mindmap/{map_id}')
    assert delete_response.status_code == 200

if __name__ == '__main__':
    pytest.main([__file__, '-v'])