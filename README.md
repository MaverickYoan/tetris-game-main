# Jeu Tetris - Application Web Full Stack

Un jeu Tetris moderne et complet construit avec Python Flask, PostgreSQL et Docker. Comprend l'authentification des utilisateurs, un jeu en temps réel, des classements et une administration de base de données via pgAdmin.

![Jeu Tetris](https://img.shields.io/badge/Python-Flask-blue) ![Base de données](https://img.shields.io/badge/Database-PostgreSQL-blue) ![Docker](https://img.shields.io/badge/Container-Docker-blue) ![Licence](https://img.shields.io/badge/License-MIT-green) 

## Fonctionnalités 

### Caractéristiques du jeu 
- **Gameplay Tetris classique** : expérience Tetris authentique avec toutes les pièces standard 
- **Score en temps réel** : système de notation dynamique avec progression de niveau 
- **Contrôles multiples** : commandes du clavier + boutons tactiles adaptés aux appareils mobiles 
- **Pause/Resume** : gestion de l'état du jeu avec fonctionnalité de pause 
- **Conception réactive** : fonctionne de manière transparente sur les ordinateurs de bureau et les appareils mobiles 

### Gestion des utilisateurs 
- **Enregistrement et authentification des utilisateurs** : comptes d'utilisateurs sécurisés avec hachage de mot de passe 
- **Gestion des sessions** : sessions de connexion persistantes 
- **Statistiques personnelles** : suivez vos progrès et vos réalisations 
- **Gestion de profil** : gestion des comptes utilisateur 

### Fonctionnalités concurrentes 
- **Classements mondiaux** : rivalisez avec des joueurs du monde entier 
- **Suivi des statistiques personnelles** : surveillez votre amélioration au fil du temps 
- **Historique des meilleurs scores** : gardez une trace de tous vos meilleurs jeux 
- **Mises à jour en temps réel** : mises à jour du classement en direct 

### Caractéristiques techniques 
- **Persistance de la base de données** : toutes les données de jeu stockées dans PostgreSQL 
- **Conteneurisation Docker** : déploiement et mise à l'échelle faciles 
- **Administration de base de données** : interface pgAdmin intégrée 
- **API RESTful** : conception d'API épurée pour les interactions de jeu 
- **Sécurité** : hachage de mot de passe et gestion sécurisée des sessions 

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌────────────────────────┐
│   Frontend      │    │   Flask App     │    │   PostgreSQL           │
│   (HTML/CSS/JS) │◄──►│   (Python)      │◄──►│   (Base de données)    │
└─────────────────┘    └─────────────────┘    └────────────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     pgAdmin     │
                       │  (DB Gestion)│
                       └─────────────────┘
```

## Conditions préalables

- **Docker** et **Docker Compose** installés sur votre système 
- **Git** (pour cloner le dépôt) 
- Au moins **2 Go de RAM** et **1 Go d'espace disque**

## Quick Start
### 1. Cloner le référentiel 
```bash 
git clone <votre-url-depot> 
jeu cd tetris 
``` 

### 2. Démarrez l'application 
```bash 
docker-compose up -d 
``` 

### 3. Accédez à l'application 
- **Jeu Tetris** : http://localhost:5000 
- **pgAdmin** : http://localhost:5050 
- E-mail : `admin@tetris.com` 
- Mot de passe : `admin123` 

### 4. Compte démo 
Pour les tests, utilisez le compte démo pré-créé : 
- **Nom d'utilisateur** : `demo_user` 
- **Mot de passe** : `demo123`

## Configuration détaillée 

### Configuration de l'environnement 
1. Copiez l'exemple de fichier d'environnement : 
```bash 
cp .env.exemple .env 
``` 

2. Modifiez `.env` avec vos paramètres préférés : 
```env 
``` 

# Configuration de la base de données 
DATABASE_URL=postgresql://tetris_user:tetris_password@postgres:5432/tetris_db 

# Configuration du flacon 
SECRET_KEY=votre-clé-super-secrète-ici 
FLASK_ENV=développement 

# Configuration de pgAdmin 
PGADMIN_DEFAULT_EMAIL=admin@tetris.com 
PGADMIN_DEFAULT_PASSWORD=admin123 


### Mode de développement 
Pour le développement avec rechargement à chaud : 
```bash 
docker-compose -f docker-compose.yml -f docker-compose.dev.yml haut 
``` 

### Déploiement en production 
Pour le déploiement en production : 
1. Mettre à jour les variables d'environnement dans `.env` 
2. Définissez `FLASK_ENV=production` 
3. Utilisez un `SECRET_KEY` fort 
4. Pensez à utiliser une base de données externe et un proxy inverse 

## Comment jouer 

### Contrôles 
- **← / →** : Déplacer la pièce vers la gauche/droite 
- **↑** : Tourner la pièce dans le sens des aiguilles d'une montre 
- **↓** : Chute douce (descente plus rapide) 
- **Espace** : Chute rapide (descente instantanée) 
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

## Développement 

### Structure du projet
```
jeu-tetris/ 
├── app.py                                # Menu Application Flask 
├── Templates/                              # Templates HTML 
│ ├── base.html                           # page de base 
│ ├── index.html                          # page d'index 
│ ├── login.html                          # Page d'authentification 
│ ├── registre.html                       # Page d'inscription 
│ └── game.html                           # page de l'interface de jeu 
├── base de données/ 
│ └── init.sql                            # Initialisation de la base de données 
├── static/                               # Fichiers statiques 
├── requirements.txt                         # Dépendances Python 
├── Conteneur d'application Dockerfile    # Flask 
├── docker-compose.yml                    # Configuration multi-conteneurs 
└── README.md                             # Fichier Lisez-moi 
```

### API Points de terminaison

#### Authentication
- `POST /register` - Inscription des utilisateurs 
- `POST /login` - Connexion utilisateur 
- `GET /logout` - Déconnexion de l'utilisateur 

#### Game Management
- `POST /api/game/start` - Commencer un nouveau jeu 
- `POST /api/game/move` - Contrôles du jeu 
- `POST /api/game/drop` - Pièce à chute automatique 
- `POST /api/game/end` - Terminer le jeu et sauvegarder le score 

#### Data Retrieval
- `GET /api/leaderboard` - Classements des scores 
- `GET /api/user/stats` - Obtenir des statistiques sur les utilisateurs 

### Schéma de base de données

#### Table des utilisateurs
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

#### Table des meilleurs scores
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

## pgAdmin - Gestion de base de données

### Accès pgAdmin
1. Accédez à http://localhost:5050 
2. Connectez-vous avec les informations d'identification de docker-compose.yml 
3. Ajoutez une connexion au serveur : 
   - **Nom**: Tetris Database
   - **Host**: postgres
   - **Port**: 5432
   - **Nom d'utilisateur**: tetris_user
   - **Mot de passe**: tetris_password
   
### Opérations de base de données communes
- **Afficher les tables** : Accédez à Serveurs → Base de données Tetris → Bases de données → tetris_db → Schémas → public → Tables 
- **Données de requête** : Utilisez l'outil de requête pour exécuter des commandes SQL 
- **Surveiller les performances** : Vérifiez l'activité et les statistiques du serveur 
- **Sauvegarde/Restauration** : utilisez les fonctions de sauvegarde et de restauration intégrées 

#### Dépannages

#### Problèmes communs

#### Conflits de ports
Si les ports 5000 ou 5050 sont utilisés : 
```bash 
# Vérifiez ce qui utilise le port 
netstat -un | findstr : 5000

# Modifiez docker-compose.yml pour utiliser différents ports 
ports : 
- "5001:5000" # Utilisez plutôt le port 5001 
```

#### Problèmes de connexion de la base de données
```bash
# Vérifier les journaux du conteneur docker-compose postgres
docker-compose logs flask_app

# Redémarrer les services
docker-compose restart postgres flask_app
```

#### Problèmes d'autorisation
```bash
# Sous Linux/Mac, assurez-vous des autorisations appropriées
sudo chown -R $USER:$USER .

# Réinitialiser les volumes Docker si nécessaire
docker-compose down -v
docker-compose up -d
```

### Optimisation des performances
- **Indexation de base de données** : les index sont automatiquement créés sur les colonnes fréquemment interrogées 
- **Connection Pooling** : PostgreSQL gère automatiquement le pool de connexions 
- **Portion de fichiers statiques** : envisagez d'utiliser nginx pour les fichiers statiques en production 
- **Mise en cache** : ajoutez Redis pour le stockage de session et la mise en cache en production 

## Considérations de sécurité 

### fonctionnalités de sécurité actuelles 
- **Hachage de mot de passe** : le hachage de mot de passe sécurisé de Werkzeug 
- **Gestion de session** : gestion sécurisée des sessions de Flask 
- **SQL Prévention des injections** : Requêtes paramétrées avec psycopg2 
- **Protection CSRF** : protections de flacon intégrées 
- **Validation des entrées** : validation côté serveur pour toutes les entrées 

### Liste de contrôle de sécurité de la production à cocher (si la mise en production doit être effectuée) 
- [ ] Modifier les mots de passe par défaut 
- [ ] Utilisez SECRET_KEY fort 
- [ ] Activer HTTPS 
- [ ] Configurer les règles de pare-feu 
- [ ] Mises à jour de sécurité régulières 
- [ ] Restrictions d'accès à la base de données 
- [ ] Implémentation de la limitation de débit 
- [ ] Examen de la désinfection des entrées 

## Contribution 
1. Fork le référentiel 
2. Créez une branche de fonctionnalités (`git checkout -b feature/amazing-feature`) 
3. Validez vos modifications (`git commit -m 'Ajouter une fonctionnalité étonnante'`) 
4. Poussez vers la branche (`git push origin feature/amazing-feature`) 
5. Ouvrez une demande de tirage

## Licence

Ce projet est autorisé en vertu de la licence MIT - voir le fichier [licence] (licence) pour plus de détails. 

## Remerciements

- Conception classique de jeu Tetris par Alexey Pajitnov
- Framework Web Flask
- Base de données PostgreSQL
- conteneurisation Docker
- outil de gestion de la base de données PGADMIN

## support

Si vous rencontrez des problèmes ou si vous avez des questions:

1. Vérifiez la section [Dépannage] (# - Dépannage)
2. Regardez les problèmes de github existants
3. Créez un nouveau problème avec des informations détaillées:
- Système opérateur
- Version Docker
- Messages d'erreur
- étapes pour reproduire

## Améliorations futures

- [ ] Support multijoueur
- [ ] Système de tournoi
- [ ] Application mobile (React Native / Flutter)
- [ ] statistiques et analyses avancées
- [ ] Caractéristiques sociales (amis, défis)
- [ ] thèmes et skins personnalisés
- [ ] effets sonores et musique
- [ ] mode spectateur
- [ ] Système de relecture
- [ ] AI BOT APPOSONNES

---

** Have a good trail ** Commencez votre voyage Tetris 
