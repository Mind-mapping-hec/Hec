#!/usr/bin/env python3
"""
Mind Map Mini - All-in-One Quick Start Script
This single file sets up and runs the entire Mind Map Mini application
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def create_app_file():
    """Create the main Flask application file"""
    # This would contain the full app.py content
    # Truncated here for brevity - use the full app.py artifact
    return '''
# This is a placeholder - replace with full app.py content from artifact
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("Mind Map Mini - Running on http://localhost:5000")
    app.run(debug=True, port=5000)
'''

def create_html_template():
    """Create the HTML template file"""
    # This would contain the full HTML content
    # Truncated here for brevity - use the full HTML artifact
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Mind Map Mini</title>
</head>
<body>
    <h1>Mind Map Mini</h1>
    <p>Replace this with the full HTML content from the artifact</p>
</body>
</html>
'''

def quick_start():
    """Complete setup and launch of Mind Map Mini"""
    
    print("""
    ╔════════════════════════════════════════╗
    ║     🧠 Mind Map Mini Quick Start       ║
    ║    Lightweight Mind Mapping Tool       ║
    ╚════════════════════════════════════════╝
    """)
    
    print("📦 Setting up Mind Map Mini...\n")
    
    # Step 1: Create directory structure
    print("1️⃣ Creating directories...")
    directories = [
        'mindmaps',
        'map_templates',
        'exports', 
        'autosave',
        'static',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # Step 2: Check Python version
    print("\n2️⃣ Checking Python version...")
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("   ❌ Python 3.7+ required")
        sys.exit(1)
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Step 3: Install Flask
    print("\n3️⃣ Installing dependencies...")
    try:
        import flask
        print("   ✅ Flask already installed")
    except ImportError:
        print("   📥 Installing Flask...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Flask', 'flask-cors'])
        print("   ✅ Flask installed")
    
    # Step 4: Create app.py if it doesn't exist
    if not Path('app.py').exists():
        print("\n4️⃣ Creating app.py...")
        with open('app.py', 'w') as f:
            f.write(create_app_file())
        print("   ✅ app.py created")
        print("   ⚠️  NOTE: Replace with full app.py content from artifact!")
    else:
        print("\n4️⃣ app.py already exists ✅")
    
    # Step 5: Create HTML template if it doesn't exist
    if not Path('templates/index.html').exists():
        print("\n5️⃣ Creating HTML template...")
        with open('templates/index.html', 'w') as f:
            f.write(create_html_template())
        print("   ✅ templates/index.html created")
        print("   ⚠️  NOTE: Replace with full HTML content from artifact!")
    else:
        print("\n5️⃣ templates/index.html already exists ✅")
    
    # Step 6: Create sample templates
    print("\n6️⃣ Creating sample templates...")
    
    business_template = {
        "title": "Business Plan",
        "mode": "grinde",
        "nodes": [
            {"id": "1", "text": "Business Plan", "type": "central", "x": 400, "y": 300, "color": "#6366f1", "size": 30},
            {"id": "2", "text": "Vision", "type": "group", "x": 200, "y": 200, "color": "#8b5cf6", "size": 25},
            {"id": "3", "text": "Market", "type": "group", "x": 600, "y": 200, "color": "#10b981", "size": 25},
            {"id": "4", "text": "Product", "type": "group", "x": 200, "y": 400, "color": "#f59e0b", "size": 25},
            {"id": "5", "text": "Finance", "type": "group", "x": 600, "y": 400, "color": "#ef4444", "size": 25}
        ],
        "connections": [
            {"source": "1", "target": "2", "type": "simple"},
            {"source": "1", "target": "3", "type": "simple"},
            {"source": "1", "target": "4", "type": "simple"},
            {"source": "1", "target": "5", "type": "simple"}
        ]
    }
    
    import json
    with open('map_templates/business-plan.json', 'w') as f:
        json.dump(business_template, f, indent=2)
    print("   ✅ Business Plan template")
    
    study_template = {
        "title": "Study Notes",
        "mode": "grinde", 
        "nodes": [
            {"id": "1", "text": "Course Title", "type": "central", "x": 400, "y": 300, "color": "#6366f1", "size": 30},
            {"id": "2", "text": "📚 Key Concepts", "type": "group", "x": 250, "y": 200, "color": "#3b82f6", "size": 25},
            {"id": "3", "text": "💡 Examples", "type": "group", "x": 550, "y": 200, "color": "#10b981", "size": 25},
            {"id": "4", "text": "❓ Questions", "type": "group", "x": 250, "y": 400, "color": "#f59e0b", "size": 25},
            {"id": "5", "text": "⚡ Remember", "type": "group", "x": 550, "y": 400, "color": "#ef4444", "size": 25}
        ],
        "connections": []
    }
    
    with open('map_templates/study-notes.json', 'w') as f:
        json.dump(study_template, f, indent=2)
    print("   ✅ Study Notes template")
    
    # Step 7: Create README
    print("\n7️⃣ Creating README...")
    readme = """# 🧠 Mind Map Mini

A lightweight mind mapping tool with GRINDE and Buzan methods.

## Quick Start
```bash
python quickstart.py
```

## Features
- No database required (JSON storage)
- GRINDE and Buzan methods
- Auto-save
- Multiple export formats
- Templates

## Usage
1. Double-click to create nodes
2. Drag to move nodes
3. Shift+drag to pan
4. Ctrl+S to save

## Files
- `mindmaps/` - Your saved maps
- `templates/` - HTML interface
- `map_templates/` - Map templates
- `autosave/` - Temporary saves

Made with ❤️ for simple mind mapping
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    print("   ✅ README.md created")
    
    # Step 8: Launch the application
    print("\n" + "="*50)
    print("✨ Setup complete! Starting Mind Map Mini...")
    print("="*50 + "\n")
    
    print("🚀 Launching server...")
    print("📱 Opening browser in 3 seconds...")
    print("\n" + "─"*50)
    print("Server will run at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("─"*50 + "\n")
    
    # Open browser after a delay
    def open_browser():
        time.sleep(3)
        webbrowser.open('http://localhost:5000')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Mind Map Mini stopped. Goodbye!")

if __name__ == '__main__':
    quick_start()

# ============================================================
# INSTRUCTIONS FOR USE:
# ============================================================
"""
COMPLETE SETUP INSTRUCTIONS:

1. Save this file as 'quickstart.py'

2. Replace the placeholder functions with actual content:
   - In create_app_file(): paste the full app.py content
   - In create_html_template(): paste the full HTML content

3. Run the quick start:
   python quickstart.py

4. The script will:
   - Create all necessary directories
   - Install Flask if needed
   - Create app files
   - Set up templates
   - Launch the server
   - Open your browser

That's it! Your Mind Map Mini is ready to use.

ALTERNATIVE: Manual Setup
-------------------------
If you prefer manual setup:

1. Create these files:
   - app.py (from Flask artifact)
   - templates/index.html (from HTML artifact)

2. Install Flask:
   pip install Flask flask-cors

3. Run:
   python app.py

4. Open http://localhost:5000
"""