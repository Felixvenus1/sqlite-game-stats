"""Command-line interface for the SQLite Game Stats tracker."""

from __future__ import annotations

import argparse
from pathlib import Path

from game_stats.db import check_database
from game_stats.queries import (
	delete_session_by_id,
	get_aggregate_stats,
	get_sessions_by_game,
	insert_session,
)


def _add_common_db_arg(parser: argparse.ArgumentParser) -> None:
	parser.add_argument(
		"--db-path",
		type=Path,
		default=None,
		help="Optional SQLite database path. Defaults to project stats.db.",
	)


def _handle_log(args: argparse.Namespace) -> int:
	conn = check_database(db_path=args.db_path) if args.db_path else check_database()
	try:
		session_id = insert_session(
			conn=conn,
			game_name=args.game,
			score=args.score,
			level=args.level,
			duration_minutes=args.duration,
			genre=args.genre,
			created_at=args.created_at,
		)
		print(f"Logged session {session_id} for '{args.game}'.")
		return 0
	except ValueError as exc:
		print(f"Error: {exc}")
		return 2
	finally:
		conn.close()


def _handle_query(args: argparse.Namespace) -> int:
	conn = check_database(db_path=args.db_path) if args.db_path else check_database()
	try:
		sessions = get_sessions_by_game(conn, args.game)
		if not sessions:
			print(f"No sessions found for '{args.game}'.")
			return 0

		for row in sessions:
			print(
				" | ".join(
					[
						f"id={row['session_id']}",
						f"game={row['game_name']}",
						f"genre={row['genre']}",
						f"score={row['score']}",
						f"level={row['level']}",
						f"duration={row['duration_minutes']}m",
						f"created_at={row['created_at']}",
					]
				)
			)
		return 0
	finally:
		conn.close()


def _handle_stats(args: argparse.Namespace) -> int:
	conn = check_database(db_path=args.db_path) if args.db_path else check_database()
	try:
		stats = get_aggregate_stats(conn)
		print(f"total_sessions: {stats['total_sessions']}")
		print(f"average_score: {stats['average_score']}")
		print(f"highest_score: {stats['highest_score']}")
		print(f"most_played_game: {stats['most_played_game']}")
		print(f"most_played_count: {stats['most_played_count']}")
		return 0
	finally:
		conn.close()


def _handle_delete(args: argparse.Namespace) -> int:
	conn = check_database(db_path=args.db_path) if args.db_path else check_database()
	try:
		deleted = delete_session_by_id(conn, args.session_id)
		if deleted:
			print(f"Deleted session {args.session_id}.")
			return 0
		print(f"Session {args.session_id} not found.")
		return 1
	finally:
		conn.close()


def build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(
		prog="game-stats",
		description="Track and query game sessions using SQLite.",
	)
	subparsers = parser.add_subparsers(dest="command", required=True)

	log_parser = subparsers.add_parser("log", help="Log a new game session.")
	log_parser.add_argument("--game", required=True, help="Game name.")
	log_parser.add_argument("--score", type=int, required=True, help="Session score.")
	log_parser.add_argument("--level", type=int, required=True, help="Level reached.")
	log_parser.add_argument(
		"--duration",
		type=int,
		required=True,
		help="Session duration in minutes.",
	)
	log_parser.add_argument("--genre", default=None, help="Optional game genre.")
	log_parser.add_argument(
		"--created-at",
		default=None,
		help="Optional timestamp (format: YYYY-MM-DD HH:MM:SS).",
	)
	_add_common_db_arg(log_parser)
	log_parser.set_defaults(handler=_handle_log)

	query_parser = subparsers.add_parser("query", help="List sessions for a game.")
	query_parser.add_argument("--game", required=True, help="Game name.")
	_add_common_db_arg(query_parser)
	query_parser.set_defaults(handler=_handle_query)

	stats_parser = subparsers.add_parser("stats", help="Show aggregate statistics.")
	_add_common_db_arg(stats_parser)
	stats_parser.set_defaults(handler=_handle_stats)

	delete_parser = subparsers.add_parser("delete", help="Delete a session by ID.")
	delete_parser.add_argument(
		"--session-id",
		type=int,
		required=True,
		help="Session ID to delete.",
	)
	_add_common_db_arg(delete_parser)
	delete_parser.set_defaults(handler=_handle_delete)

	return parser


def main(argv: list[str] | None = None) -> int:
	parser = build_parser()
	args = parser.parse_args(argv)
	return args.handler(args)


if __name__ == "__main__":
	raise SystemExit(main())
