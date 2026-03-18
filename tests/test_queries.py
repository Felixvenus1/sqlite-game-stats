import sqlite3

import pytest

from game_stats.db import DEFAULT_SCHEMA_PATH
from game_stats.queries import (
    delete_session_by_id,
    get_aggregate_stats,
    get_sessions_by_game,
    insert_session,
)


@pytest.fixture
def conn() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(DEFAULT_SCHEMA_PATH.read_text(encoding="utf-8"))
    yield connection
    connection.close()


def test_insert_session_and_get_sessions_by_game(conn: sqlite3.Connection) -> None:
    session_id = insert_session(
        conn,
        game_name="MimeCraft",
        score=1200,
        level=8,
        duration_minutes=45,
        genre="Best Game Ever",
        created_at="2026-03-18 10:00:00",
    )

    assert session_id > 0

    rows = get_sessions_by_game(conn, "MimeCraft")
    assert len(rows) == 1
    assert rows[0]["game_name"] == "MimeCraft"
    assert rows[0]["score"] == 1200
    assert rows[0]["level"] == 8
    assert rows[0]["duration_minutes"] == 45
    assert rows[0]["genre"] == "Best Game Ever"


def test_insert_session_rejects_negative_values(conn: sqlite3.Connection) -> None:
    with pytest.raises(ValueError):
        insert_session(
            conn,
            game_name="Celeste",
            score=-1,
            level=3,
            duration_minutes=20,
        )


def test_get_aggregate_stats_returns_expected_values(conn: sqlite3.Connection) -> None:
    insert_session(
        conn,
        game_name="MimeCraft",
        score=100,
        level=3,
        duration_minutes=30,
        created_at="2026-03-18 10:00:00",
    )
    insert_session(
        conn,
        game_name="Warzone",
        score=300,
        level=7,
        duration_minutes=55,
        created_at="2026-03-18 11:00:00",
    )
    insert_session(
        conn,
        game_name="GTA san andreas",
        score=200,
        level=5,
        duration_minutes=40,
        created_at="2026-03-18 12:00:00",
    )

    stats = get_aggregate_stats(conn)

    assert stats["total_sessions"] == 3
    assert stats["average_score"] == 200.0
    assert stats["highest_score"] == 300
    assert stats["most_played_game"] == "GTA san andreas"
    assert stats["most_played_count"] == 1


def test_delete_session_by_id_returns_true_then_false(conn: sqlite3.Connection) -> None:
    session_id = insert_session(
        conn,
        game_name="warzone",
        score=900,
        level=9,
        duration_minutes=60,
        created_at="2026-03-18 09:00:00",
    )

    assert delete_session_by_id(conn, session_id) is True
    assert delete_session_by_id(conn, session_id) is False
