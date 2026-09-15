import os
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'evolve_labs_battleground_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///battleground.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    total_kills = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    total_matches = db.Column(db.Integer, default=0)
    highest_survival_time = db.Column(db.Integer, default=0) # in seconds

class MatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    placement = db.Column(db.Integer, nullable=False)
    kills = db.Column(db.Integer, default=0)
    survival_time = db.Column(db.Integer, default=0) # in seconds
    weapon_used = db.Column(db.String(50), default='None')
    date_played = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class GameConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=False)

# --- Database Initialization & Admin Setup ---

def init_db():
    with app.app_context():
        db.create_all()
        
        # Check and create default Admin
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_pw_hash = generate_password_hash('AdminEvolve2025!', method='pbkdf2:sha256')
            admin_user = User(
                username='admin',
                email='admin@evolvelabs.local',
                password_hash=admin_pw_hash,
                role='admin',
                total_kills=15,
                total_wins=3,
                total_matches=5
            )
            db.session.add(admin_user)
            
        # Add basic dummy matches for Admin demonstration
        if not MatchHistory.query.filter_by(user_id=1).first() and admin_user:
            db.session.add(MatchHistory(user_id=1, placement=1, kills=6, survival_time=240, weapon_used='Assault Rifle'))
            db.session.add(MatchHistory(user_id=1, placement=3, kills=4, survival_time=180, weapon_used='Shotgun'))
            db.session.add(MatchHistory(user_id=1, placement=15, kills=1, survival_time=45, weapon_used='Pistol'))
            admin_user.total_kills = 11
            admin_user.total_wins = 1
            admin_user.total_matches = 3
            admin_user.highest_survival_time = 240
            
        # Default balance configurations
        default_configs = {
            'map_size': '2000',
            'bot_count': '15',
            'zone_shrink_speed': '0.3',
            'max_loot_spawn': '30'
        }
        for k, v in default_configs.items():
            if not GameConfig.query.filter_by(key=k).first():
                db.session.add(GameConfig(key=k, value=v))
                
        db.session.commit()

# --- Custom Context Processor ---
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return dict(current_user=user)

# --- Routes ---

@app.route('/')
def lobby():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Grab statistics
    user = User.query.get(session['user_id'])
    history = MatchHistory.query.filter_by(user_id=user.id).order_range(MatchHistory.id.desc()).limit(10).all()
    
    # Grab game parameters
    config_objs = GameConfig.query.all()
    configs = {c.key: c.value for c in config_objs}
    
    return render_template('index.html', user=user, history=history, configs=configs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Successfully logged in!', 'success')
            return redirect(url_for('lobby'))
        
        flash('Invalid username or password.', 'error')
    return render_template('index.html', show_login=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_pw, role='user')
        db.session.add(new_user)
        db.session.commit()
        
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['role'] = new_user.role
        flash('Registration successful! Welcome to the Arena.', 'success')
        return redirect(url_for('lobby'))
        
    return render_template('index.html', show_register=True)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/leaderboard')
def leaderboard():
    top_players = User.query.order_by(User.total_wins.desc(), User.total_kills.desc()).limit(15).all()
    return jsonify([{
        'username': p.username,
        'wins': p.total_wins,
        'kills': p.total_kills,
        'matches': p.total_matches,
        'survival': p.highest_survival_time
    } for p in top_players])

@app.route('/api/save_match', methods=['POST'])
def save_match():
    if 'user_id' not in session:
        return jsonify({'status': 'unauthorized'}), 401
        
    data = request.json
    user = User.query.get(session['user_id'])
    
    placement = int(data.get('placement', 10))
    kills = int(data.get('kills', 0))
    survival_time = int(data.get('survival_time', 0))
    weapon_used = data.get('weapon_used', 'None')
    
    # Save Match Record
    match = MatchHistory(
        user_id=user.id,
        placement=placement,
        kills=kills,
        survival_time=survival_time,
        weapon_used=weapon_used
    )
    db.session.add(match)
    
    # Update Stats
    user.total_matches += 1
    user.total_kills += kills
    if placement == 1:
        user.total_wins += 1
    if survival_time > user.highest_survival_time:
        user.highest_survival_time = survival_time
        
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'placement': placement,
        'kills': kills,
        'survival_time': survival_time,
        'total_wins': user.total_wins,
        'total_kills': user.total_kills
    })

@app.route('/admin/config', methods=['POST'])
def update_config():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'status': 'unauthorized'}), 403
        
    for key in ['map_size', 'bot_count', 'zone_shrink_speed', 'max_loot_spawn']:
        val = request.form.get(key)
        if val:
            config_item = GameConfig.query.filter_by(key=key).first()
            if config_item:
                config_item.value = val
                
    db.session.commit()
    flash('Game Balance configuration updated successfully!', 'success')
    return redirect(url_for('lobby'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)