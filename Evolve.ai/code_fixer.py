import os
import sys
import subprocess

def analyze_and_fix_code(file_path):
    # Auto-fix logic yahan aayegi
    print(f"[Code Fixer] Analyzing {file_path}...")
    return True
# Auto-fixer: Check and install required packages automatically if missing
required_packages = ['flask', 'flask_sqlalchemy']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"[Auto-Fixer] Installing missing package: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'admin_secret_key_12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model for Admin & Game Data
class AdminUser(db.Model):
    id = db.Model.metadata.tables.get('admin_user', None) # safe reference or standard
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

with app.app_context():
    try:
        db.create_all()
        # Create default admin if not exists
        # Default Admin Credentials: username -> admin, password -> admin123
        if not db.session.query(db.select(AdminUser).filter_by(username='admin')).scalar():
            default_admin = AdminUser(username='admin', password='admin123')
            db.session.add(default_admin)
            db.session.commit()
            print("[Auto-Fixer] Default admin created: username 'admin', password 'admin123'")
    except Exception as e:
        print(f"[Auto-Fixer] Database initialization note: {e}")

# HTML Frontend Template with Admin Panel & Game Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evolve AI - Game & Admin Portal</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-neutral-950 text-neutral-100 h-screen flex flex-col justify-between p-6">
    <header class="flex justify-between items-center border-b border-neutral-800 pb-4">
        <h1 class="text-xl font-bold text-orange-500">Evolve AI Game Portal</h1>
        <div class="space-x-3">
            <a href="/" class="text-xs bg-neutral-800 px-3 py-1.5 rounded-lg hover:bg-neutral-700">Home / Game</a>
            <a href="/admin" class="text-xs bg-orange-600 px-3 py-1.5 rounded-lg hover:bg-orange-500 font-semibold">Admin Panel</a>
        </div>
    </header>

    <main class="flex-1 flex flex-col items-center justify-center text-center space-y-4">
        {% if role == 'admin' %}
            <div class="bg-neutral-900 border border-neutral-800 p-8 rounded-2xl max-w-lg w-full space-y-4 shadow-xl">
                <h2 class="text-2xl font-bold text-emerald-400">Admin Dashboard</h2>
                <p class="text-xs text-neutral-400">Welcome, Admin! You have full control over the game system.</p>
                <div class="p-4 bg-neutral-950 rounded-xl text-left text-xs font-mono space-y-2 border border-neutral-800">
                    <p class="text-emerald-300">System Status: Active & Secured</p>
                    <p class="text-neutral-400">Default Admin Username: <span class="text-white font-bold">admin</span></p>
                    <p class="text-neutral-400">Default Admin Password: <span class="text-white font-bold">admin123</span></p>
                </div>
                <a href="/logout" class="block w-full bg-rose-600/20 text-rose-400 border border-rose-600/40 py-2 rounded-xl text-xs font-semibold hover:bg-rose-600/30">Logout</a>
            </div>
        {% elif role == 'login' %}
            <div class="bg-neutral-900 border border-neutral-800 p-8 rounded-2xl max-w-sm w-full space-y-4 shadow-xl">
                <h2 class="text-xl font-bold">Admin Login</h2>
                {% if error %}<p class="text-xs text-rose-500">{{ error }}</p>{% endif %}
                <form method="POST" action="/admin" class="space-y-3 text-left">
                    <div>
                        <label class="text-xs text-neutral-400 block mb-1">Username</label>
                        <input type="text" name="username" class="w-full bg-neutral-950 border border-neutral-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-orange-500" required>
                    </div>
                    <div>
                        <label class="text-xs text-neutral-400 block mb-1">Password</label>
                        <input type="password" name="password" class="w-full bg-neutral-950 border border-neutral-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-orange-500" required>
                    </div>
                    <button type="submit" class="w-full bg-orange-600 hover:bg-orange-500 text-white py-2.5 rounded-xl text-xs font-semibold transition">Login as Admin</button>
                </form>
            </div>
        {% else %}
            <div class="space-y-3 max-w-xl">
                <h2 class="text-3xl font-serif">Welcome to Evolve Game Arena</h2>
                <p class="text-sm text-neutral-400">Your interactive gaming and AI interface is running successfully on localhost.</p>
                <div class="pt-4">
                    <button onclick="alert('Game session active!')" class="bg-white text-black font-semibold px-6 py-3 rounded-xl text-sm hover:bg-neutral-200 transition">Start Playing</button>
                </div>
            </div>
        {% endif %}
    </main>

    <footer class="text-center text-xs text-neutral-500 border-t border-neutral-800 pt-4 font-mono">
        Evolve AI • Localhost Server Running
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, role='home')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check credentials
        admin_user = AdminUser.query.filter_by(username=username, password=password).first()
        if admin_user or (username == 'admin' and password == 'admin123'):
            session['admin'] = True
            return render_template_string(HTML_TEMPLATE, role='admin')
        else:
            return render_template_string(HTML_TEMPLATE, role='login', error='Invalid username or password! (Hint: admin / admin123)')
            
    if session.get('admin'):
        return render_template_string(HTML_TEMPLATE, role='admin')
    return render_template_string(HTML_TEMPLATE, role='login')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("\n[Auto-Fixer] Starting Flask server locally...")
    print("[Auto-Fixer] Access your app at: http://127.0.0.1:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)