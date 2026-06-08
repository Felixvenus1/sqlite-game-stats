"""Render the entity-relationship diagram (ARTEFACT 01-A) as docs/erd.png.

Run from the project root:

    python docs/generate_erd.py

Produces a simple two-table ERD matching sql/schema.sql so the README can embed
a real image without depending on an external diagramming service.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HEADER = "#2e86ab"
BODY = "#f4f7fb"
BORDER = "#1b4965"
TEXT_LIGHT = "white"

GAMES = {
    "title": "games",
    "rows": [
        "game_id      INTEGER  PK  AUTOINCREMENT",
        "game_name    TEXT     NOT NULL  UNIQUE",
        "genre        TEXT",
    ],
}

SESSIONS = {
    "title": "sessions",
    "rows": [
        "session_id        INTEGER  PK  AUTOINCREMENT",
        "game_id           INTEGER  NOT NULL  FK",
        "score             INTEGER  NOT NULL  CHECK >= 0",
        "level             INTEGER  NOT NULL  CHECK >= 0",
        "duration_minutes  INTEGER  NOT NULL  CHECK >= 0",
        "created_at        TEXT     NOT NULL  DEFAULT now",
    ],
}


def _draw_table(ax, x: float, y_top: float, table: dict, width: float = 4.6) -> tuple[float, float]:
    row_h = 0.42
    header_h = 0.5
    n = len(table["rows"])
    total_h = header_h + n * row_h

    # Body box
    ax.add_patch(
        FancyBboxPatch(
            (x, y_top - total_h),
            width,
            total_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.5,
            edgecolor=BORDER,
            facecolor=BODY,
            zorder=2,
        )
    )
    # Header band
    ax.add_patch(
        FancyBboxPatch(
            (x, y_top - header_h),
            width,
            header_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            linewidth=1.5,
            edgecolor=BORDER,
            facecolor=HEADER,
            zorder=3,
        )
    )
    ax.text(
        x + width / 2,
        y_top - header_h / 2,
        table["title"],
        ha="center",
        va="center",
        color=TEXT_LIGHT,
        fontsize=12,
        fontweight="bold",
        zorder=4,
    )
    for i, row in enumerate(table["rows"]):
        ax.text(
            x + 0.18,
            y_top - header_h - row_h / 2 - i * row_h,
            row,
            ha="left",
            va="center",
            color="#13293d",
            fontsize=8.5,
            family="monospace",
            zorder=4,
        )
    return total_h, width


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis("off")

    _draw_table(ax, x=0.6, y_top=5.4, table=GAMES)
    _draw_table(ax, x=8.0, y_top=5.6, table=SESSIONS)

    # One-to-many relationship: games (1) --< sessions (many)
    arrow = FancyArrowPatch(
        (5.2, 4.4),
        (8.0, 4.6),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=1.8,
        color=BORDER,
        zorder=1,
    )
    ax.add_patch(arrow)
    ax.text(6.55, 4.75, "1", ha="center", va="bottom", fontsize=11, fontweight="bold", color=BORDER)
    ax.text(7.75, 4.85, "N", ha="center", va="bottom", fontsize=11, fontweight="bold", color=BORDER)
    ax.text(
        6.6,
        4.25,
        "one game has many sessions\n(FK game_id, ON DELETE CASCADE)",
        ha="center",
        va="top",
        fontsize=8.5,
        color="#5a6b7b",
    )

    ax.set_title(
        "SQLite Game Stats — Entity Relationship Diagram",
        fontsize=14,
        fontweight="bold",
        color=BORDER,
        pad=12,
    )

    out = Path(__file__).resolve().parent / "erd.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
