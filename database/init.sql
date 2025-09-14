-- Tetris Game Database Schema
-- This script initializes the database with tables for users, scores, and game sessions

-- Enable UUID extension for generating unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table for authentication and user management
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) DEFAULT 'admin'
);

CREATE TABLE administrateurs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

INSERT INTO administrateurs (username, email) VALUES
('Yoan', 'yoan.demenezes@gmail.com'),
('MaverickYoan', 'maverick.yoan@gmail.com'),
('admin', 'admin@admin.com');

-- High scores table to track player achievements
CREATE TABLE high_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    lines_cleared INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    time_played INTEGER NOT NULL, -- in seconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Game sessions table to track ongoing games
CREATE TABLE game_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    current_score INTEGER DEFAULT 0,
    current_level INTEGER DEFAULT 1,
    lines_cleared INTEGER DEFAULT 0,
    game_board TEXT, -- JSON representation of the game board
    current_piece TEXT, -- JSON representation of the current tetromino
    next_piece TEXT, -- JSON representation of the next tetromino
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User statistics table for additional metrics
CREATE TABLE user_stats (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    total_games_played INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    total_lines_cleared INTEGER DEFAULT 0,
    total_time_played INTEGER DEFAULT 0, -- in seconds
    best_score INTEGER DEFAULT 0,
    best_level INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des messages pour les soumissions de formulaire de contact
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_high_scores_user_id ON high_scores(user_id);
CREATE INDEX idx_high_scores_score ON high_scores(score DESC);
CREATE INDEX idx_game_sessions_user_id ON game_sessions(user_id);
CREATE INDEX idx_game_sessions_active ON game_sessions(is_active);

-- Function to update user stats after a game
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Update user statistics when a new high score is recorded
    INSERT INTO user_stats (user_id, total_games_played, total_score, total_lines_cleared, total_time_played, best_score, best_level)
    VALUES (NEW.user_id, 1, NEW.score, NEW.lines_cleared, NEW.time_played, NEW.score, NEW.level_reached)
    ON CONFLICT (user_id) DO UPDATE SET
        total_games_played = user_stats.total_games_played + 1,
        total_score = user_stats.total_score + NEW.score,
        total_lines_cleared = user_stats.total_lines_cleared + NEW.lines_cleared,
        total_time_played = user_stats.total_time_played + NEW.time_played,
        best_score = GREATEST(user_stats.best_score, NEW.score),
        best_level = GREATEST(user_stats.best_level, NEW.level_reached),
        updated_at = CURRENT_TIMESTAMP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update user stats
CREATE TRIGGER trigger_update_user_stats
    AFTER INSERT ON high_scores
    FOR EACH ROW
    EXECUTE FUNCTION update_user_stats();

-- Function to update game session timestamp
CREATE OR REPLACE FUNCTION update_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update session timestamp
CREATE TRIGGER trigger_update_session_timestamp
    BEFORE UPDATE ON game_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_session_timestamp();

-- Insert some sample data for testing
INSERT INTO users (username, email, password_hash) VALUES
('demo_user', 'demo@tetris.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWX3Gqvfx/DKG'), -- password: demo123
('player1', 'player1@tetris.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewdBWX3Gqvfx/DKG'); -- password: demo123

-- Insert sample high scores
INSERT INTO high_scores (user_id, score, lines_cleared, level_reached, time_played) 
SELECT 
    u.id, 
    (RANDOM() * 50000)::INTEGER, 
    (RANDOM() * 100)::INTEGER, 
    (RANDOM() * 10 + 1)::INTEGER, 
    (RANDOM() * 1800 + 300)::INTEGER
FROM users u
WHERE u.username IN ('demo_user', 'player1');

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tetris_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tetris_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO tetris_user;
