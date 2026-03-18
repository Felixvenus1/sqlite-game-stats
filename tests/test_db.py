from pathlib import Path
import sqlite3

from game_stats.db import DEFAULT_SCHEMA_PATH, check_database, initialise_db


def test_initialise_db_creates_required_tables() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        initialise_db(conn, DEFAULT_SCHEMA_PATH)

        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name IN ('games', 'sessions')
            ORDER BY name
            """
        ).fetchall()

        assert [row["name"] for row in tables] == ["games", "sessions"]
    finally:
        conn.close()


def test_check_database_creates_file_and_schema(tmp_path: Path) -> None:
    db_path = tmp_path / "stats.db"
    schema_path = DEFAULT_SCHEMA_PATH

    conn = check_database(db_path=db_path, schema_path=schema_path)
    try:
        assert db_path.exists()

        count = conn.execute(
            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type = 'table' AND name IN ('games', 'sessions')
            """
        ).fetchone()[0]

        assert count == 2
    finally:
        conn.close()
