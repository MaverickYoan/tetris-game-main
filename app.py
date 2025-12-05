#!/usr/bin/env python3
"""
Application Flask pour le jeu Tetris.
Un jeu Tetris complet avec authentification des utilisateurs, notation et intégration de base de données."""

import os
import random
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
from psycopg2 import sql

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration de la base de données
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://tetris_user:tetris_password@localhost:5432/tetris_db')

# Constantes du jeu Tetris
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TETROMINO_SHAPES = {
    'I': [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    'O': [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    'T': [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    'S': [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '..#..']
    ],
    'Z': [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '.##..',
         '.#...']
    ],
    'J': [
        ['.....',
         '.....',
         '.#...',
         '.#...',
         '##...'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.##..',
         '.#...',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '..#..']
    ],
    'L': [
        ['.....',
         '.....',
         '.#...',
         '.#...',
         '.##..'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '#....'],
        ['.....',
         '.....',
         '##...',
         '.#...',
         '.#...'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ],
# Nouveau triomino000
    'A': [
        ['.....',
         '.....',
         '.....',
         '#....',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '.....',
         '##...',
         '#....',
         '.....'],
        ['.....',
         '.....',
         '.....',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '.....',
         '##...',
         '.#...',
         '.....']
    ],
# Nouveau triomino001
    'B': [
        ['.....',
         '.....',
         '.....',
         '#....',
         '.....',
         '.....']
    ],
# Nouveau triomino002
    'C': [
        ['.....',
         '.....',
         '.....',
         '#....',
         '#....',
         '.....'],
        ['.....',
         '.....',
         '.....',
         '##...',
         '.....',
         '.....']
    ]
}

def get_db_connection():
    """Obtenir la connexion à la base de données.
    """
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)

def login_required(f):
    """Le site exigera une connexion pour certains itinéraires."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentification requise'}), 401
        return f(*args, **kwargs)
    return decorated_function

class TetrisGame:
    """Class pour le jeu Tetris."""
    
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.current_piece = self.generate_piece()
        self.next_piece = self.generate_piece()
        self.piece_x = BOARD_WIDTH // 2 - 2
        self.piece_y = 0
        self.piece_rotation = 0
        self.game_over = False
        self.start_time = datetime.now()
        
        # Système de combo et statistiques avancées
        self.combo_count = 0
        self.max_combo = 0
        self.perfect_clears = 0
        self.total_pieces = 0
        self.last_action_cleared_lines = False
        
        # Système Hold/Reserve
        self.held_piece = None
        self.can_hold = True
        
        # Statistiques de pièces
        self.piece_stats = {piece: 0 for piece in TETROMINO_SHAPES.keys()}
        
        # Mode de jeu (normal, sprint)
        self.game_mode = 'normal'
        self.sprint_start_time = None
        self.sprint_target_lines = 40
        
        # Système d'achievements
        self.achievements_unlocked = []
        self.achievements_progress = {
            'first_line': False,
            'tetris_master': 0,  # Compteur de Tetris (4 lignes)
            'combo_king': 0,  # Max combo atteint
            'speed_demon': False,  # Sprint en moins de 2 minutes
            'perfectionist': 0,  # Perfect clears
            'century': False,  # 100 lignes
            'survivor': False,  # Niveau 10
        }
        
    def generate_piece(self):
        """Générer un morceau de tétromino aléatoire."""
        return random.choice(list(TETROMINO_SHAPES.keys()))
    
    def get_piece_shape(self, piece_type, rotation=0):
        """Obtenez la matrice de forme d'une pièce à une rotation donnée."""
        shapes = TETROMINO_SHAPES[piece_type]
        return shapes[rotation % len(shapes)]
    
    def is_valid_position(self, piece_type, x, y, rotation):
        """Vérifiez si une position de pièce est valide."""
        shape = self.get_piece_shape(piece_type, rotation)
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    new_x = x + col_idx
                    new_y = y + row_idx
                    
                    if (new_x < 0 or new_x >= BOARD_WIDTH or 
                        new_y >= BOARD_HEIGHT or 
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True
    
    def place_piece(self):
        """Placez la pièce actuelle sur le plateau."""
        shape = self.get_piece_shape(self.current_piece, self.piece_rotation)
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    board_x = self.piece_x + col_idx
                    board_y = self.piece_y + row_idx
                    if board_y >= 0:
                        self.board[board_y][board_x] = ord(self.current_piece)
    
    def clear_lines(self):
        """Effacez les lignes complétées."""
        lines_to_clear = []
        
        for y in range(BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(BOARD_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
<<<<<<< HEAD
            self.last_action_cleared_lines = True
            
            # Système de combo
            self.combo_count += 1
            self.max_combo = max(self.max_combo, self.combo_count)
            
            # Vérifier perfect clear (toute la grille est vide)
            if all(all(cell == 0 for cell in row) for row in self.board):
                self.perfect_clears += 1
                perfect_clear_bonus = 3000 * self.level
            else:
                perfect_clear_bonus = 0
            
            # Scoring system amélioré avec combo
=======
            # Système de notation : niveau 100 * pour le simple, niveau 300 * pour le double, etc..
>>>>>>> ac9254e3373d7b1fdff573946c2a5595cf552151
            score_multiplier = [0, 100, 300, 500, 800]
            base_score = score_multiplier[min(lines_cleared, 4)] * self.level
            
            # Bonus de combo (50 points par niveau de combo)
            combo_bonus = 50 * self.combo_count * self.level
            
            self.score += base_score + combo_bonus + perfect_clear_bonus
            self.level = min(10, 1 + self.lines_cleared // 10)
        else:
            # Réinitialiser le combo si aucune ligne n'est détruite
            if self.last_action_cleared_lines:
                self.combo_count = 0
            self.last_action_cleared_lines = False
        
        return lines_cleared
    
    def move_piece(self, dx, dy, rotation_change=0):
        """Déplacer ou faire pivoter la pièce actuelle."""
        new_x = self.piece_x + dx
        new_y = self.piece_y + dy
        new_rotation = self.piece_rotation + rotation_change
        
        if self.is_valid_position(self.current_piece, new_x, new_y, new_rotation):
            self.piece_x = new_x
            self.piece_y = new_y
            self.piece_rotation = new_rotation
            return True
        return False
    
    def drop_piece(self):
        """Déposez la pièce actuelle d'une rangée vers le bas."""
        if self.move_piece(0, 1):
            return True
        else:
            # La pièce ne peut pas descendre, placez-la et récupérez la pièce suivante
            self.place_piece()
            lines_cleared = self.clear_lines()
            
            # Track Tetris achievements
            if lines_cleared == 4:
                self.achievements_progress['tetris_master'] += 1
            
            # Track piece statistics
            self.piece_stats[self.current_piece] += 1
            self.total_pieces += 1
            
            # Générer la pièce suivante
            self.current_piece = self.next_piece
            self.next_piece = self.generate_piece()
            self.piece_x = BOARD_WIDTH // 2 - 2
            self.piece_y = 0
            self.piece_rotation = 0
            
<<<<<<< HEAD
            # Reset hold ability for new piece
            self.can_hold = True
            
            # Start sprint timer on first piece
            if self.game_mode == 'sprint' and self.sprint_start_time is None and self.total_pieces == 1:
                self.sprint_start_time = datetime.now()
            
            # Check game over
=======
            # Vérifier la fin du jeu
>>>>>>> ac9254e3373d7b1fdff573946c2a5595cf552151
            if not self.is_valid_position(self.current_piece, self.piece_x, self.piece_y, self.piece_rotation):
                self.game_over = True
                
            return False
    
    def hard_drop(self):
<<<<<<< HEAD
        """Drop piece all the way down."""
        drop_distance = 0
=======
        """Déposez le morceau jusqu'en bas."""
>>>>>>> ac9254e3373d7b1fdff573946c2a5595cf552151
        while self.drop_piece():
            drop_distance += 1
        
        # Bonus pour hard drop (2 points par ligne)
        if drop_distance > 0:
            self.score += drop_distance * 2
        
        return drop_distance
    
    def get_ghost_position(self):
        """Calculate where the current piece will land."""
        ghost_y = self.piece_y
        while self.is_valid_position(self.current_piece, self.piece_x, ghost_y + 1, self.piece_rotation):
            ghost_y += 1
        return ghost_y
    
    def hold_piece(self):
        """Hold/swap the current piece."""
        if not self.can_hold:
            return False
        
        if self.held_piece is None:
            # First hold - store current piece and get next
            self.held_piece = self.current_piece
            self.current_piece = self.next_piece
            self.next_piece = self.generate_piece()
        else:
            # Swap current with held
            self.held_piece, self.current_piece = self.current_piece, self.held_piece
        
        # Reset position and rotation
        self.piece_x = BOARD_WIDTH // 2 - 2
        self.piece_y = 0
        self.piece_rotation = 0
        
        # Can't hold again until next piece
        self.can_hold = False
        
        # Check if position is valid (game over if not)
        if not self.is_valid_position(self.current_piece, self.piece_x, self.piece_y, self.piece_rotation):
            self.game_over = True
            return False
        
        return True
    
    def check_achievements(self):
        """Check and unlock achievements."""
        new_achievements = []
        
        # First Line
        if not self.achievements_progress['first_line'] and self.lines_cleared >= 1:
            self.achievements_progress['first_line'] = True
            new_achievements.append({
                'id': 'first_line',
                'name': 'Première Ligne',
                'description': 'Complétez votre première ligne'
            })
        
        # Tetris Master (5 Tetris)
        if self.achievements_progress['tetris_master'] >= 5 and 'tetris_master' not in self.achievements_unlocked:
            new_achievements.append({
                'id': 'tetris_master',
                'name': 'Maître du Tetris',
                'description': 'Réalisez 5 Tetris (4 lignes)'
            })
            self.achievements_unlocked.append('tetris_master')
        
        # Combo King (combo de 5+)
        if self.max_combo >= 5 and self.achievements_progress['combo_king'] < 5:
            self.achievements_progress['combo_king'] = self.max_combo
            new_achievements.append({
                'id': 'combo_king',
                'name': 'Roi du Combo',
                'description': 'Atteignez un combo de 5'
            })
        
        # Perfectionist (1 perfect clear)
        if self.perfect_clears >= 1 and self.achievements_progress['perfectionist'] == 0:
            self.achievements_progress['perfectionist'] = self.perfect_clears
            new_achievements.append({
                'id': 'perfectionist',
                'name': 'Perfectionniste',
                'description': 'Réalisez un Perfect Clear'
            })
        
        # Century (100 lines)
        if not self.achievements_progress['century'] and self.lines_cleared >= 100:
            self.achievements_progress['century'] = True
            new_achievements.append({
                'id': 'century',
                'name': 'Centenaire',
                'description': 'Complétez 100 lignes'
            })
        
        # Survivor (reach level 10)
        if not self.achievements_progress['survivor'] and self.level >= 10:
            self.achievements_progress['survivor'] = True
            new_achievements.append({
                'id': 'survivor',
                'name': 'Survivant',
                'description': 'Atteignez le niveau 10'
            })
        
        # Speed Demon (Sprint < 2 minutes)
        if self.game_mode == 'sprint' and self.lines_cleared >= self.sprint_target_lines:
            if self.sprint_start_time:
                elapsed = (datetime.now() - self.sprint_start_time).total_seconds()
                if elapsed < 120 and not self.achievements_progress['speed_demon']:
                    self.achievements_progress['speed_demon'] = True
                    new_achievements.append({
                        'id': 'speed_demon',
                        'name': 'Démon de Vitesse',
                        'description': 'Terminez le Sprint en moins de 2 minutes'
                    })
        
        return new_achievements
    
    def get_state(self):
<<<<<<< HEAD
        """Get current game state."""
        state = {
=======
        """Obtenir l'état actuel du jeu."""
        return {
>>>>>>> ac9254e3373d7b1fdff573946c2a5595cf552151
            'board': self.board,
            'current_piece': {
                'type': self.current_piece,
                'x': self.piece_x,
                'y': self.piece_y,
                'rotation': self.piece_rotation,
                'shape': self.get_piece_shape(self.current_piece, self.piece_rotation)
            },
            'next_piece': {
                'type': self.next_piece,
                'shape': self.get_piece_shape(self.next_piece, 0)
            },
            'held_piece': {
                'type': self.held_piece,
                'shape': self.get_piece_shape(self.held_piece, 0) if self.held_piece else None
            } if self.held_piece else None,
            'can_hold': self.can_hold,
            'ghost_y': self.get_ghost_position(),
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'combo_count': self.combo_count,
            'max_combo': self.max_combo,
            'perfect_clears': self.perfect_clears,
            'game_over': self.game_over,
            'piece_stats': self.piece_stats,
            'game_mode': self.game_mode,
            'achievements': self.check_achievements()
        }
        
        # Add sprint-specific data
        if self.game_mode == 'sprint':
            if self.sprint_start_time:
                elapsed = (datetime.now() - self.sprint_start_time).total_seconds()
                state['sprint_time'] = elapsed
            state['sprint_target'] = self.sprint_target_lines
            state['sprint_complete'] = self.lines_cleared >= self.sprint_target_lines
        
        return state

# Stocker les jeux actifs en mémoire (en production, utiliser Redis ou base de données)
active_games = {}

@app.route('/')
def index():
    """Page principale."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Tous les champs sont obligatoires'}), 400
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Vérifier si l'utilisateur existe déjà
            cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cur.fetchone():
                return jsonify({'error': 'Username or email already exists'}), 400
            
            # Créer un nouvel utilisateur
            password_hash = generate_password_hash(password)
            # Définir le rôle en fonction du nom d'utilisateur (admin si username == 'admin')
            role = 'admin' if username.lower() == 'admin' else 'standard'
            cur.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, password_hash, role)
            )
            user_id = cur.fetchone()['id']
            
            conn.commit()
            cur.close()
            conn.close()
            
            session['user_id'] = str(user_id)
            session['username'] = username
            session['role'] = role
            
            return jsonify({'success': True, 'message': 'Inscription réussie'})
            
        except Exception as e:
            return jsonify({'error': f'L\'inscription a échoué: {str(e)}'}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Le nom d\'utilisateur et le mot de passe sont requis'}), 400
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute(
                "SELECT id, username, password_hash FROM users WHERE username = %s AND is_active = TRUE",
                (username,)
            )
            user = cur.fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                # Mettre à jour la dernière connexion
                cur.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s",
                    (user['id'],)
                )
                conn.commit()
                
                # Récupérer le rôle de l'utilisateur
                cur.execute("SELECT role FROM users WHERE id = %s", (user['id'],))
                user_role = cur.fetchone()
                
                session['user_id'] = str(user['id'])
                session['username'] = user['username']
                session['role'] = user_role['role'] if user_role else 'standard'
                
                cur.close()
                conn.close()
                return jsonify({'success': True, 'message': 'Connexion réussie'})
            else:
                cur.close()
                conn.close()
                return jsonify({'error': 'Nom d\'utilisateur ou mot de passe invalide'}), 401
                
        except Exception as e:
            return jsonify({'error': f'La connexion a échoué: {str(e)}'}), 500
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    # return jsonify({'success': True, 'message': 'Déconnecté avec succès'})
    return redirect(url_for('index'))

@app.route('/game')
@login_required
def game():
    """Game page."""
    return render_template('game.html')

@app.route('/api/game/start', methods=['POST'])
@login_required
def start_game():
    """Start a new game."""
    user_id = session['user_id']
    data = request.get_json() or {}
    game_mode = data.get('mode', 'normal')
    
    game = TetrisGame(user_id)
    game.game_mode = game_mode
    active_games[user_id] = game
    
    return jsonify({
        'success': True,
        'game_state': game.get_state()
    })

@app.route('/api/game/move', methods=['POST'])
@login_required
def move_piece():
    """Move or rotate a piece."""
    user_id = session['user_id']
    if user_id not in active_games:
        return jsonify({'error': 'No active game'}), 400
    
    game = active_games[user_id]
    if game.game_over:
        return jsonify({'error': 'Game over'}), 400
    
    data = request.get_json()
    action = data.get('action')
    
    if action == 'left':
        game.move_piece(-1, 0)
    elif action == 'right':
        game.move_piece(1, 0)
    elif action == 'down':
        game.drop_piece()
    elif action == 'rotate':
        game.move_piece(0, 0, 1)
    elif action == 'hard_drop':
        game.hard_drop()
    
    return jsonify({
        'success': True,
        'game_state': game.get_state()
    })

@app.route('/api/game/drop', methods=['POST'])
@login_required
def auto_drop():
    """Auto-drop piece (called by game timer)."""
    user_id = session['user_id']
    if user_id not in active_games:
        return jsonify({'error': 'No active game'}), 400
    
    game = active_games[user_id]
    if game.game_over:
        return jsonify({'error': 'Game over'}), 400
    
    game.drop_piece()
    
    return jsonify({
        'success': True,
        'game_state': game.get_state()
    })

@app.route('/api/game/hold', methods=['POST'])
@login_required
def hold_piece():
    """Hold/swap the current piece."""
    user_id = session['user_id']
    if user_id not in active_games:
        return jsonify({'error': 'No active game'}), 400
    
    game = active_games[user_id]
    if game.game_over:
        return jsonify({'error': 'Game over'}), 400
    
    success = game.hold_piece()
    
    return jsonify({
        'success': success,
        'game_state': game.get_state()
    })

@app.route('/api/game/end', methods=['POST'])
@login_required
def end_game():
    """End the current game and save score."""
    user_id = session['user_id']
    if user_id not in active_games:
        return jsonify({'error': 'No active game'}), 400
    
    game = active_games[user_id]
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Calculate time played
        time_played = int((datetime.now() - game.start_time).total_seconds())
        
        # Save high score
        cur.execute(
            """INSERT INTO high_scores (user_id, score, lines_cleared, level_reached, time_played)
               VALUES (%s, %s, %s, %s, %s)""",
            (user_id, game.score, game.lines_cleared, game.level, time_played)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Remove game from active games
        del active_games[user_id]
        
        return jsonify({
            'success': True,
            'final_score': int(game.score),
            'lines_cleared': int(game.lines_cleared),
            'level': int(game.level),
            'time_played': int(time_played)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to save score: {str(e)}'}), 500

@app.route('/api/leaderboard')
def leaderboard():
    """Get top scores leaderboard."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """SELECT u.username, hs.score, hs.lines_cleared, hs.level_reached, 
                      hs.time_played, hs.created_at
               FROM high_scores hs
               JOIN users u ON hs.user_id = u.id
               ORDER BY hs.score DESC
               LIMIT 10"""
        )
        
        scores = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'scores': [dict(score) for score in scores]
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get leaderboard: {str(e)}'}), 500

@app.route('/api/user/stats')
@login_required
def user_stats():
    """Get user statistics."""
    user_id = session['user_id']
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT * FROM user_stats WHERE user_id = %s",
            (user_id,)
        )
        
        stats = cur.fetchone()
        cur.close()
        conn.close()
        
        if stats:
            return jsonify({
                'success': True,
                'stats': dict(stats)
            })
        else:
            return jsonify({
                'success': True,
                'stats': {
                    'total_games_played': 0,
                    'total_score': 0,
                    'total_lines_cleared': 0,
                    'total_time_played': 0,
                    'best_score': 0,
                    'best_level': 0
                }
            })
            
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        if not all([name, email, subject, message]):
            return jsonify({'error': 'All fields are required'}), 400
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
                (name, email, subject, message)
            )
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'success': True, 'message': 'Ton message a bien été envoyé, merci.'})
        except Exception as e:
            return jsonify({'error': f'Failed to send message: {str(e)}'}), 500
    return render_template('contact.html')



@app.route('/Tetris')
def tetris():
    """Page Tetris."""
    return render_template('Tetris.html')




@app.route('/admin/messages')
@login_required
def admin_messages():
    # Vérifiez si l'utilisateur est administrateur
    # Le décorateur login_required vérifie déjà si user_id est en session
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Check user role
        cur.execute("SELECT role FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        if not user or user['role'] != 'admin':
            cur.close()
            conn.close()
            return redirect(url_for('login'))
        # Fetch messages
        cur.execute("SELECT id, name, email, subject, message, created_at FROM messages ORDER BY created_at DESC")
        messages = []
        for message in cur.fetchall():
            messages.append({
                'id': message['id'],
                'name': message['name'],
                'email': message['email'],
                'subject': message['subject'],
                'message': message['message'],
                'created_at': message['created_at']
            })
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching messages: {e}")
        messages = []
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/messages/update', methods=['POST'])
@login_required
def update_message():
    # Vérifier si l'utilisateur est admin
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Vérifier le rôle de l'utilisateur
        cur.execute("SELECT role FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        if not user or user['role'] != 'admin':
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        # Récupérer les données du message modifié
        data = request.get_json()
        if not data or 'id' not in data:
            return jsonify({'success': False, 'error': 'Données invalides'}), 400
        
        # Extraire les champs à mettre à jour
        message_id = data.get('id')
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message_text = data.get('message')
        
        # Vérifier que le message existe
        cur.execute("SELECT id FROM messages WHERE id = %s", (message_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Message non trouvé'}), 404
        
        # Mettre à jour le message dans la base de données
        cur.execute(
            "UPDATE messages SET name = %s, email = %s, subject = %s, message = %s WHERE id = %s",
            (name, email, subject, message_text, message_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error updating message: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/messages/delete/<int:message_id>', methods=['DELETE'])
@login_required
def delete_message(message_id):
    # Vérifier si l'utilisateur est admin
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Vérifier le rôle de l'utilisateur
        cur.execute("SELECT role FROM users WHERE id = %s", (session['user_id'],))
        user = cur.fetchone()
        if not user or user['role'] != 'admin':
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Accès non autorisé'}), 403
        
        # Vérifier que le message existe
        cur.execute("SELECT id FROM messages WHERE id = %s", (message_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'error': 'Message non trouvé'}), 404
        
        # Supprimer le message de la base de données
        cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error deleting message: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
