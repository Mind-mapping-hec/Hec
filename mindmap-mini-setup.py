# setup.py - Quick setup script for Mind Map Mini

import os
import shutil

def setup_mindmap_mini():
    """Setup Mind Map Mini application"""
    
    print("""
    ╔══════════════════════════════════════╗
    ║     Mind Map Mini Setup v1.0         ║
    ║   Lightweight Mind Mapping Tool       ║
    ╚══════════════════════════════════════╝
    """)
    
    # Create directory structure
    directories = [
        'mindmaps',
        'map_templates', 
        'exports',
        'autosave',
        'static',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create requirements.txt
    requirements = """# Mind Map Mini - Minimal Requirements
Flask==2.3.3
flask-cors==4.0.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")
    
    # Create templates/index.html
    # Note: Copy the HTML artifact content here
    print("✅ Created templates/index.html (copy from HTML artifact)")
    
    # Create run.sh script
    run_script = """#!/bin/bash
# Run Mind Map Mini

echo "🚀 Starting Mind Map Mini..."
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "🧠 Launching application..."
python app.py
"""
    
    with open('run.sh', 'w') as f:
        f.write(run_script)
    os.chmod('run.sh', 0o755)
    print("✅ Created run.sh script")
    
    # Create run.bat for Windows
    run_bat = """@echo off
echo Starting Mind Map Mini...
echo Installing requirements...
pip install -r requirements.txt

echo Launching application...
python app.py
pause
"""
    
    with open('run.bat', 'w') as f:
        f.write(run_bat)
    print("✅ Created run.bat script")
    
    # Create README.md
    readme = """# 🧠 Mind Map Mini

A lightweight, JSON-based mind mapping tool with GRINDE and Buzan methods support.

## Features

- 🚀 **No Database Required** - Everything saves as JSON files
- 🧠 **GRINDE Method** - Optimized for learning
- 🌟 **Buzan Method** - Classic mind mapping
- 💾 **Auto-save** - Never lose your work
- 📤 **Multiple Export Formats** - JSON, Markdown, HTML
- 🎨 **Clean Interface** - Distraction-free design
- 📱 **Responsive** - Works on all devices

## Quick Start

### Option 1: Using the setup script
```bash
python setup.py
python app.py
```

### Option 2: Manual setup
```bash
pip install Flask flask-cors
python app.py
```

Then open http://localhost:5000 in your browser.

## Usage

1. **Create a Node**: Double-click on canvas
2. **Connect Nodes**: Use Connect tool, click two nodes
3. **Move Nodes**: Drag and drop
4. **Pan Canvas**: Shift + Drag
5. **Zoom**: Mouse wheel
6. **Save**: Ctrl+S or click Save button

## Keyboard Shortcuts

- `Double-click` - Create new node
- `Delete` - Delete selected node
- `Ctrl+S` - Save map
- `Ctrl+Z` - Undo
- `Ctrl+Y` - Redo
- `Shift+Drag` - Pan canvas
- `Ctrl+Wheel` - Zoom

## File Structure

```
mind-map-mini/
├── app.py              # Flask application
├── mindmaps/          # Saved mind maps (JSON)
├── map_templates/     # Template files
├── autosave/         # Auto-saved files
├── exports/          # Exported files
└── templates/        # HTML templates
```

## GRINDE Method

The GRINDE method is optimized for learning:

- **G**rouped - Organize information in chunks
- **R**eflective - Use your own words
- **I**nterconnected - Create multiple connections
- **N**on-verbal - Use colors and symbols
- **D**irectional - Show logical flow
- **E**mphasized - Highlight importance

## Export Formats

- **JSON** - Complete map data
- **Markdown** - Structured text
- **HTML** - Standalone visualization
- **Text** - Plain text outline

## Requirements

- Python 3.7+
- Flask 2.3+
- Modern web browser

## License

MIT License - Free to use and modify

## Support

Create an issue on GitHub or contact support.

---

Made with ❤️ for simple, effective mind mapping
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    print("✅ Created README.md")
    
    print("""
    ✨ Setup Complete!
    
    To start Mind Map Mini:
    1. Copy the HTML content to templates/index.html
    2. Run: python app.py
    3. Open: http://localhost:5000
    
    Enjoy mind mapping! 🧠
    """)

if __name__ == '__main__':
    setup_mindmap_mini()

# ============================================================
# templates/index.html - Flask template wrapper
# ============================================================
"""
Note: Create a file templates/index.html with the HTML artifact content.
The Flask app will serve this automatically.
"""

# ============================================================
# Simple test file for the API
# ============================================================
# test_api.py

import requests
import json

def test_mindmap_api():
    """Test Mind Map Mini API endpoints"""
    
    base_url = 'http://localhost:5000/api'
    
    print("Testing Mind Map Mini API...")
    
    # Test 1: Get maps list
    print("\n1. Getting maps list...")
    response = requests.get(f'{base_url}/maps')
    print(f"   Status: {response.status_code}")
    print(f"   Maps: {len(response.json()['maps'])}")
    
    # Test 2: Create a new map
    print("\n2. Creating new map...")
    test_map = {
        'title': 'Test Map',
        'mode': 'grinde',
        'nodes': [
            {'id': '1', 'x': 400, 'y': 300, 'text': 'Test Central', 'type': 'central', 'color': '#6366f1', 'size': 30},
            {'id': '2', 'x': 200, 'y': 200, 'text': 'Test Node', 'type': 'concept', 'color': '#10b981', 'size': 20}
        ],
        'connections': [
            {'source': '1', 'target': '2', 'type': 'simple'}
        ]
    }
    
    response = requests.post(f'{base_url}/map', json=test_map)
    print(f"   Status: {response.status_code}")
    result = response.json()
    if result['success']:
        map_id = result['id']
        print(f"   Map ID: {map_id}")
        
        # Test 3: Load the created map
        print("\n3. Loading created map...")
        response = requests.get(f'{base_url}/map/{map_id}')
        print(f"   Status: {response.status_code}")
        map_data = response.json()['data']
        print(f"   Title: {map_data['title']}")
        print(f"   Nodes: {len(map_data['nodes'])}")
        
        # Test 4: Export map
        print("\n4. Testing exports...")
        for format in ['json', 'markdown', 'html']:
            response = requests.get(f'{base_url}/export/{map_id}/{format}')
            print(f"   {format.upper()}: {response.status_code}")
        
        # Test 5: Delete map
        print("\n5. Deleting test map...")
        response = requests.delete(f'{base_url}/map/{map_id}')
        print(f"   Status: {response.status_code}")
    
    # Test 6: Get templates
    print("\n6. Getting templates...")
    response = requests.get(f'{base_url}/templates')
    print(f"   Status: {response.status_code}")
    templates = response.json()['templates']
    print(f"   Templates: {len(templates)}")
    for template in templates:
        print(f"   - {template['title']} ({template['mode']})")
    
    # Test 7: Get stats
    print("\n7. Getting statistics...")
    response = requests.get(f'{base_url}/stats')
    print(f"   Status: {response.status_code}")
    stats = response.json()['stats']
    print(f"   Total Maps: {stats['totalMaps']}")
    print(f"   Total Nodes: {stats['totalNodes']}")
    
    print("\n✅ All tests completed!")

if __name__ == '__main__':
    test_mindmap_api()