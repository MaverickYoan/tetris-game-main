# 🎮 Jeu Tetris - Application Web Full Stack 

Un jeu Tetris moderne et complet construit avec Python Flask, PostgreSQL et Docker. Comprend l'authentification des utilisateurs, un jeu en temps réel, des classements et une administration de base de données via pgAdmin.

![Tetris Game](https://img.shields.io/badge/Python-Flask-blue) ![Database](https://img.shields.io/badge/Database-PostgreSQL-blue) ![Docker](https://img.shields.io/badge/Container-Docker-blue) ![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Caractéristiques

### 🎮 Caractéristiques du jeu 
- **Gameplay Tetris classique** : expérience Tetris authentique avec toutes les pièces standard 
- **Score en temps réel** : système de notation dynamique avec progression de niveau 
- **Contrôles multiples** : commandes du clavier + boutons tactiles adaptés aux appareils mobiles 
- **Pause/Resume** : gestion de l'état du jeu avec fonctionnalité de pause 
- **Conception réactive** : fonctionne de manière transparente sur les ordinateurs de bureau et les appareils mobiles 

### 👥 Gestion des utilisateurs 
- **Enregistrement et authentification des utilisateurs** : comptes d'utilisateurs sécurisés avec hachage de mot de passe 
- **Gestion des sessions** : sessions de connexion persistantes 
- **Statistiques personnelles** : suivez vos progrès et vos réalisations 
- **Gestion de profil** : gestion des comptes utilisateur 

### 🏆 Fonctionnalités concurrentes 
- **Classements mondiaux** : rivalisez avec des joueurs du monde entier 
- **Suivi des statistiques personnelles** : surveillez votre amélioration au fil du temps 
- **Historique des meilleurs scores** : gardez une trace de tous vos meilleurs jeux 
- **Mises à jour en temps réel** : mises à jour du classement en direct 

### 🛠 Caractéristiques techniques 
- **Persistance de la base de données** : toutes les données de jeu stockées dans PostgreSQL 
- **Conteneurisation Docker** : déploiement et mise à l'échelle faciles 
- **Administration de base de données** : interface pgAdmin intégrée 
- **API RESTful** : conception d'API épurée pour les interactions de jeu 
- **Sécurité** : hachage de mot de passe et gestion sécurisée des sessions 

## 🏗Architecture

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

## 📋 Conditions préalables 

- **Docker** et **Docker Compose** installés sur votre système 
- **Git** (pour cloner le dépôt) 
- Au moins **2 Go de RAM** et **1 Go d'espace disque** 

## 🚀 Démarrage rapide 

### 1. Cloner le référentiel
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
## 🎯 Comment jouer 

### Contrôles 
- **← / →** : Déplacer la pièce vers la gauche/droite 
- **↑** : Tourner la pièce dans le sens des aiguilles d'une montre 
- **↓** : Soft drop (descente plus rapide) 
- **Espace** : Hard drop (placement instantané) 
- **P** : Pause/Reprise du jeu 

### Système de notation 
- **Ligne unique** : 100 × niveau 
- **Lignes doubles** : 300 × niveau 
- **Triple Lines** : 500 × Niveau 
- **Tetris (4 lignes)** : 800 × Niveau 

### Progression 
- **Le niveau augmente** toutes les 10 lignes effacées 
- **La vitesse augmente** à chaque niveau 
- **Niveau maximum** : 10 

## 🔧 Développement 

### Structure du projet
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
### Points de terminaison de l'API 

#### Authentification
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
```### Optimisation des performances 
- **Indexation de base de données** : les index sont automatiquement créés sur les colonnes fréquemment interrogées 
- **Connection Pooling** : PostgreSQL gère automatiquement le pool de connexions 
- **Serving de fichiers statiques** : envisagez d'utiliser nginx pour les fichiers statiques en production 
- **Caching** : ajoutez Redis pour le stockage de session et la mise en cache en production 
## 🔒Considérations de sécurité 

### fonctionnalités de sécurité actuelles 
- **Password Hashing** : le hachage de mot de passe sécurisé de Werkzeug 
- **Gestion de session** : gestion sécurisée des sessions de Flask 
- **SQL Injection Prevention** : Requêtes paramétrées avec psycopg2 
- **Protection CSRF** : protections de flacon intégrées 
- **Validation des entrées** : validation côté serveur pour toutes les entrées 

## Liste de contrôle de sécurité de la production ### 
- [ ] Modifier les mots de passe par défaut 
- [ ] Utilisez SECRET_KEY fort 
- [ ] Activer HTTPS 
- [ ] Configurer les règles de pare-feu 
- [ ] Mises à jour de sécurité régulières 
- [ ] Restrictions d'accès à la base de données 
- [ ] Implémentation de la limitation de débit 
- [ ] Examen de la désinfection des entrées

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
