from pathlib import Path

from game_stats.cli import main


def test_cli_log_and_query(tmp_path: Path, capsys) -> None:
    db_path = tmp_path / "cli_test.db"

    exit_code = main(
        [
            "log",
            "--game",
            "Hades",
            "--score",
            "500",
            "--level",
            "4",
            "--duration",
            "30",
            "--db-path",
            str(db_path),
        ]
    )
    assert exit_code == 0

    query_code = main(["query", "--game", "Hades", "--db-path", str(db_path)])
    assert query_code == 0

    output = capsys.readouterr().out
    assert "Logged session" in output
    assert "game=Hades" in output


def test_cli_stats_and_delete(tmp_path: Path, capsys) -> None:
    db_path = tmp_path / "cli_test_stats.db"

    main(
        [
            "log",
            "--game",
            "Celeste",
            "--score",
            "900",
            "--level",
            "9",
            "--duration",
            "60",
            "--db-path",
            str(db_path),
        ]
    )

    stats_code = main(["stats", "--db-path", str(db_path)])
    assert stats_code == 0

    stats_output = capsys.readouterr().out
    assert "total_sessions: 1" in stats_output
    assert "highest_score: 900" in stats_output

    delete_code = main(["delete", "--session-id", "1", "--db-path", str(db_path)])
    assert delete_code == 0

    delete_output = capsys.readouterr().out
    assert "Deleted session 1." in delete_output


def test_cli_query_no_sessions_returns_zero(tmp_path: Path, capsys) -> None:
    db_path = tmp_path / "empty.db"

    query_code = main(["query", "--game", "Unknown", "--db-path", str(db_path)])
    assert query_code == 0

    output = capsys.readouterr().out
    assert "No sessions found for 'Unknown'." in output


def test_cli_log_invalid_values_returns_error_code(tmp_path: Path, capsys) -> None:
    db_path = tmp_path / "invalid.db"

    exit_code = main(
        [
            "log",
            "--game",
            "BadGame",
            "--score",
            "-10",
            "--level",
            "2",
            "--duration",
            "15",
            "--db-path",
            str(db_path),
        ]
    )

    assert exit_code == 2
    output = capsys.readouterr().out
    assert "must be non-negative" in output


def test_cli_delete_missing_session_returns_one(tmp_path: Path, capsys) -> None:
    db_path = tmp_path / "delete_missing.db"

    exit_code = main(["delete", "--session-id", "999", "--db-path", str(db_path)])
    assert exit_code == 1

    output = capsys.readouterr().out
    assert "Session 999 not found." in output
