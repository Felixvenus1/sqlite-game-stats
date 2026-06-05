# SQLite Game Stats Tracker

A hand-written Python CLI project that tracks game sessions in a local SQLite database.

## Phase 1 Status

Bootstrap complete: repository structure and placeholder modules are in place.

## Functional Requirements (Project 01)

- FR-01: Log a new game session.
- FR-02: Query sessions for a specific game.
- FR-03: Show aggregate statistics.
- FR-04: Delete a session by session ID.
- FR-05: Auto-create database on first run.
- FR-06: Expose all actions through CLI commands.

## Environment Verified

Date: 2026-03-18

- Python 3.11+: PASS
- pytest installed: PASS
- ruff installed: PASS
- sqlite3 stdlib import: PASS
- Git user.name configured: PASS
- Git user.email configured: PASS
- Git core.autocrlf=input: PASS
- VS Code extension ms-python.python: PASS
- VS Code extension ms-python.vscode-pylance: PASS
- VS Code extension charliermarsh.ruff: PASS

## Planned Commands (Phase 2)

```powershell
python -m game_stats log --game "Game Name" --score 100 --level 2 --duration 45
python -m game_stats query --game "Game Name"
python -m game_stats stats
python -m game_stats delete --session-id 1
```

## Repository Structure

```text
sqlite-game-stats/
|-- README.md
|-- .gitignore
|-- requirements.txt
|-- pyproject.toml
|-- src/
|   `-- game_stats/
|       |-- __init__.py
|       |-- db.py
|       |-- queries.py
|       `-- cli.py
|-- sql/
|   `-- schema.sql
|-- tests/
|   |-- __init__.py
|   |-- test_db.py
|   `-- test_queries.py
`-- docs/
    `-- erd.png
```
