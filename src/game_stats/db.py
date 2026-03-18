"""Database connection and schema initialisation."""

from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = BASE_DIR / "stats.db"

DEFAULT_SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_db_connection(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Connect to SQLite database."""

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialise_db(conn: sqlite3.Connection, schema_path: Path | str = DEFAULT_SCHEMA_PATH) -> None:
    """Initialise database schema from SQL file."""
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    schema_sql = path.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    conn.commit()

def check_database(db_path: Path | str = DEFAULT_DB_PATH, schema_path: Path | str = DEFAULT_SCHEMA_PATH) -> sqlite3.Connection:
    """Check database exists and is initialised."""
    conn = get_db_connection(db_path)
    initialise_db(conn, schema_path)
    return conn
