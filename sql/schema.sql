-- Project 01 schema skeleton (Phase 1)

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_name TEXT NOT NULL UNIQUE,
    genre TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 0),
    level INTEGER NOT NULL CHECK (level >= 0),
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes >= 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_game_id ON sessions(game_id);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);
