# 🎮 Tetris Game - Full Stack Web Application

A modern, full-featured Tetris game built with Python Flask, PostgreSQL, and Docker. Features user authentication, real-time gameplay, leaderboards, and database administration through pgAdmin.

![Tetris Game](https://img.shields.io/badge/Python-Flask-blue) ![Database](https://img.shields.io/badge/Database-PostgreSQL-blue) ![Docker](https://img.shields.io/badge/Container-Docker-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎮 Game Features
- **Classic Tetris Gameplay**: Authentic Tetris experience with all standard pieces
- **Real-time Scoring**: Dynamic scoring system with level progression
- **Multiple Controls**: Keyboard controls + mobile-friendly touch buttons
- **Pause/Resume**: Game state management with pause functionality
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 👥 User Management
- **User Registration & Authentication**: Secure user accounts with password hashing
- **Session Management**: Persistent login sessions
- **Personal Statistics**: Track your progress and achievements
- **Profile Management**: User account management

### 🏆 Competitive Features
- **Global Leaderboards**: Compete with players worldwide
- **Personal Stats Tracking**: Monitor your improvement over time
- **High Score History**: Keep track of all your best games
- **Real-time Updates**: Live leaderboard updates

### 🛠 Technical Features
- **Database Persistence**: All game data stored in PostgreSQL
- **Docker Containerization**: Easy deployment and scaling
- **Database Administration**: Built-in pgAdmin interface
- **RESTful API**: Clean API design for game interactions
- **Security**: Password hashing and secure session management

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask App     │    │   PostgreSQL    │
│   (HTML/CSS/JS) │◄──►│   (Python)      │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     pgAdmin     │
                       │  (DB Management)│
                       └─────────────────┘
```

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed on your system
- **Git** (to clone the repository)
- At least **2GB RAM** and **1GB disk space**

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd tetris-game
```

### 2. Start the Application
```bash
docker-compose up -d
```

### 3. Access the Application
- **Tetris Game**: http://localhost:5000
- **pgAdmin**: http://localhost:5050
  - Email: `admin@tetris.com`
  - Password: `admin123`

### 4. Demo Account
For testing, use the pre-created demo account:
- **Username**: `demo_user`
- **Password**: `demo123`

## 📖 Detailed Setup

### Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Modify `.env` with your preferred settings:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://tetris_user:tetris_password@postgres:5432/tetris_db
   
   # Flask Configuration
   SECRET_KEY=your-super-secret-key-here
   FLASK_ENV=development
   
   # pgAdmin Configuration
   PGADMIN_DEFAULT_EMAIL=admin@tetris.com
   PGADMIN_DEFAULT_PASSWORD=admin123
   ```

### Development Mode
For development with hot reloading:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Production Deployment
For production deployment:
1. Update environment variables in `.env`
2. Set `FLASK_ENV=production`
3. Use a strong `SECRET_KEY`
4. Consider using external database and reverse proxy

## 🎯 How to Play

### Controls
- **← / →**: Move piece left/right
- **↑**: Rotate piece clockwise
- **↓**: Soft drop (faster descent)
- **Space**: Hard drop (instant placement)
- **P**: Pause/Resume game

### Scoring System
- **Single Line**: 100 × Level
- **Double Lines**: 300 × Level  
- **Triple Lines**: 500 × Level
- **Tetris (4 lines)**: 800 × Level

### Progression
- **Level increases** every 10 lines cleared
- **Speed increases** with each level
- **Maximum level**: 10

## 🔧 Development

### Project Structure
```
tetris-game/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   └── game.html         # Game interface
├── database/
│   └── init.sql          # Database initialization
├── static/               # Static files (if needed)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Flask app container
├── docker-compose.yml   # Multi-container setup
└── README.md           # This file
```

### API Endpoints

#### Authentication
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

#### Game Management
- `POST /api/game/start` - Start new game
- `POST /api/game/move` - Make game move
- `POST /api/game/drop` - Auto-drop piece
- `POST /api/game/end` - End game and save score

#### Data Retrieval
- `GET /api/leaderboard` - Get top scores
- `GET /api/user/stats` - Get user statistics

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### High Scores Table
```sql
CREATE TABLE high_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    lines_cleared INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    time_played INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 📊 pgAdmin Database Management

### Accessing pgAdmin
1. Navigate to http://localhost:5050
2. Login with credentials from docker-compose.yml
3. Add server connection:
   - **Name**: Tetris Database
   - **Host**: postgres
   - **Port**: 5432
   - **Username**: tetris_user
   - **Password**: tetris_password
   
### Opérations de base de données communes
- **View Tables**: Navigate to Servers → Tetris Database → Databases → tetris_db → Schemas → public → Tables
- **Query Data**: Use the Query Tool to run SQL commands
- **Monitor Performance**: Check server activity and statistics
- **Backup/Restore**: Use built-in backup and restore functions

## 🐛 Dépannage

### Problèmes communs

#### Conflits portuaires
If ports 5000 or 5050 are in use:
```bash
# Check what's using the port
netstat -an | findstr :5000

# Modify docker-compose.yml to use different ports
ports:
  - "5001:5000"  # Use port 5001 instead
```

#### Problèmes de connexion de la base de données
```bash
# Check container logs
docker-compose logs postgres
docker-compose logs flask_app

# Restart services
docker-compose restart postgres flask_app
```

#### Problèmes d'autorisation
```bash
# On Linux/Mac, ensure proper permissions
sudo chown -R $USER:$USER .

# Reset Docker volumes if needed
docker-compose down -v
docker-compose up -d
```
### Optimisation des performances
- **Database Indexing**: Indexes are automatically created on frequently queried columns
- **Connection Pooling**: PostgreSQL handles connection pooling automatically  
- **Static File Serving**: Consider using nginx for static files in production
- **Caching**: Add Redis for session storage and caching in production
## 🔒 Considérations de sécurité

### fonctionnalités de sécurité actuelles
- **Password Hashing**: Werkzeug's secure password hashing
- **Session Management**: Flask's secure session handling
- **SQL Injection Prevention**: Parameterized queries with psycopg2
- **CSRF Protection**: Built-in Flask protections
- **Input Validation**: Server-side validation for all inputs

Liste de contrôle de sécurité de la production ###
- [ ] Change default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database access restrictions
- [ ] Rate limiting implementation
- [ ] Input sanitization review

## 🤝 Contribution
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Licence

Ce projet est autorisé en vertu de la licence MIT - voir le fichier [licence] (licence) pour plus de détails.
## 🙏 Remerciements

- Conception classique de jeu Tetris par Alexey Pajitnov
- Framework Web Flask
- Base de données PostgreSQL
- conteneurisation Docker
- outil de gestion de la base de données PGADMIN

## 📞 support

Si vous rencontrez des problèmes ou si vous avez des questions:

1. Vérifiez la section [Dépannage] (# - Dépannage)
2. Regardez les problèmes de github existants
3. Créez un nouveau problème avec des informations détaillées:
- Système opérateur
- Version Docker
- Messages d'erreur
- étapes pour reproduire

## 🚀 Améliorations futures

- [] Support multijoueur
- [] Système de tournoi
- [] Application mobile (React Native / Flutter)
- [] statistiques et analyses avancées
- [] Caractéristiques sociales (amis, défis)
- [] thèmes et skins personnalisés
- [] effets sonores et musique
- [] mode spectateur
- [] Système de relecture
- [] AI BOT APPOSONNES

---

** Joyeux jeu!🎮 ** Commencez votre voyage Tetris et montez les classements!
