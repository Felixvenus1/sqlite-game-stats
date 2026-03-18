"""Query functions for session CRUD and aggregate statistics."""

import sqlite3
from typing import Any


def insert_session(
    conn: sqlite3.Connection,
    game_name: str,
    score: int,
    level: int,
    duration_minutes: int,
    genre: str | None = None,
    created_at: str | None = None,
) -> int:
    if score < 0 or level < 0 or duration_minutes < 0:
        raise ValueError("score, level, and duration_minutes must be non-negative")

    conn.execute(
        """
        INSERT INTO games (game_name, genre) VALUES (?, ?) 
        ON CONFLICT(game_name) DO NOTHING
        """,
        (game_name, genre),
    )

    row = conn.execute(
        "SELECT game_id FROM games WHERE game_name = ?",
        (game_name,),
    ).fetchone()
    if row is None:
        raise RuntimeError(f"Could not resolve game_id for game_name={game_name}")

    game_id = row["game_id"]

    if created_at is None:
        cur = conn.execute(
            """INSERT INTO sessions (game_id, score, level, duration_minutes) VALUES (?, ?, ?, ?)""",
            (game_id, score, level, duration_minutes),
        )
    else:
        cur = conn.execute(
            """
            INSERT INTO sessions (game_id, score, level, duration_minutes, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (game_id, score, level, duration_minutes, created_at),
        )

    conn.commit()
    return int(cur.lastrowid)



def get_sessions_by_game(conn: sqlite3.Connection, game_name: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
            s.session_id,
            g.game_name,
            g.genre,
            s.score,
            s.level,
            s.duration_minutes,
            s.created_at
        FROM sessions AS s
        JOIN games AS g ON g.game_id = s.game_id
        WHERE g.game_name = ?
        ORDER BY s.created_at DESC, s.session_id DESC
        """,
        (game_name,),
    ).fetchall()
    return [dict(row) for row in rows]

def get_aggregate_stats(conn: sqlite3.Connection) -> dict[str, Any]:
    base = conn.execute(
        """
        SELECT
            COUNT(*) AS total_sessions,
            AVG(score) AS average_score,
            MAX(score) AS highest_score
        FROM sessions
        """
    ).fetchone()

    most_played = conn.execute(
        """
        SELECT
            g.game_name,
            COUNT(*) AS play_count
        FROM sessions AS s
        JOIN games AS g ON g.game_id = s.game_id
        GROUP BY g.game_name
        ORDER BY play_count DESC, g.game_name ASC
        LIMIT 1
        """
    ).fetchone()

    average_score = None
    if base["average_score"] is not None:
        average_score = round(float(base["average_score"]), 2)

    return {
        "total_sessions": int(base["total_sessions"]),
        "average_score": average_score,
        "highest_score": base["highest_score"],
        "most_played_game": most_played["game_name"] if most_played else None,
        "most_played_count": int(most_played["play_count"]) if most_played else 0,
    }


def delete_session_by_id(conn: sqlite3.Connection, session_id: int) -> bool:
    cur = conn.execute(
        "DELETE FROM sessions WHERE session_id = ?",
        (session_id,),
    )
    conn.commit()
    return cur.rowcount > 0
