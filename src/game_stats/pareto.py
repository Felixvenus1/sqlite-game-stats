"""Pareto analysis visualizations for IT questionnaire responses."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

MAX_SCORE = 5.0


@dataclass(frozen=True)
class QuestionScore:
    category: str
    item: str
    score: float


QUESTIONNAIRE_DATA: list[QuestionScore] = [
    QuestionScore("Business benefits of IT", "I realise the importance of IT solutions and tools", 4.5),
    QuestionScore("Business benefits of IT", "IT benefits and costs are documented", 2.0),
    QuestionScore("Business benefits of IT", "IT supports coordination of my work and communication", 3.5),
    QuestionScore("Business benefits of IT", "IT plays an important role in my decision making", 3.0),
    QuestionScore("Business benefits of IT", "IT plays a significant role in daily implementation of my responsibilities", 5.0),
    QuestionScore("Business information and data", "I know what information and data are produced in my area", 3.0),
    QuestionScore("Business information and data", "I know where required information and data are stored", 3.0),
    QuestionScore("Business information and data", "I know what information and data are needed in my area", 3.5),
    QuestionScore("Business information and data", "I know how to get the information and data I need", 3.5),
    QuestionScore("Business information and data", "I know who can access the information and data in my area", 4.0),
    QuestionScore("IT Strategy", "I know how IT leverage in my area supports company business", 4.0),
    QuestionScore("IT Strategy", "I have set operational IT objectives", 2.5),
    QuestionScore("IT Strategy", "I have prepared an action plan to realize IT benefits", 3.0),
    QuestionScore("IT Strategy", "I have prepared the IT budget", 2.5),
    QuestionScore("IT Strategy", "I follow achievement of IT utilization goals", 2.5),
    QuestionScore("IT Ownership and responsibilities", "Information systems have assigned owners for benefits and costs", 2.5),
    QuestionScore("IT Ownership and responsibilities", "System owners report on suitability and development needs", 1.5),
    QuestionScore("IT Ownership and responsibilities", "Systems have assigned superusers/administrators", 3.0),
    QuestionScore("IT Ownership and responsibilities", "Superusers report failures, opportunities, and skills needs", 3.0),
    QuestionScore("IT Ownership and responsibilities", "Responsibilities of owners and superusers are documented", 1.5),
    QuestionScore("IT assets", "I know what hardware and software are used in my area", 5.0),
    QuestionScore("IT assets", "I know users and purpose of hardware and software", 4.5),
    QuestionScore("IT assets", "I have up-to-date documentation of used IT licenses", 2.5),
    QuestionScore("IT assets", "I know how much and where information systems are used", 3.5),
    QuestionScore("IT assets", "I know what hardware/software/licenses will be purchased next 12 months", 2.5),
    QuestionScore("IT support and services", "I know actions and responsible people in case of IT failures", 4.0),
    QuestionScore("IT support and services", "IT failures affecting my area decreased during the past year", 3.0),
    QuestionScore("IT support and services", "I regularly follow IT support and provider activities", 2.5),
    QuestionScore("IT support and services", "I am aware of proactive actions to prevent IT failures", 3.0),
    QuestionScore("IT support and services", "Current IT support and service align with business needs", 3.5),
    QuestionScore("IT infrastructure", "IT infrastructure corresponds well to business needs", 4.0),
    QuestionScore("IT infrastructure", "I have up-to-date IT infrastructure documentation", 1.5),
    QuestionScore("IT infrastructure", "We have documented and tested critical systems/services", 1.5),
    QuestionScore("IT infrastructure", "Critical applications can be accessed from outside premises", 5.0),
    QuestionScore("IT infrastructure", "Only designated individuals can change IT infrastructure", 4.5),
]


def _improvement_gap(score: float) -> float:
    return max(0.0, MAX_SCORE - score)


def build_item_pareto_rows(data: list[QuestionScore]) -> list[dict[str, float | str]]:
    rows = [
        {
            "label": f"{item.category}: {item.item}",
            "gap": _improvement_gap(item.score),
            "score": item.score,
        }
        for item in data
    ]
    rows.sort(key=lambda row: row["gap"], reverse=True)

    total_gap = sum(float(row["gap"]) for row in rows)
    running = 0.0
    for row in rows:
        running += float(row["gap"])
        row["cumulative_pct"] = (running / total_gap * 100.0) if total_gap else 0.0
    return rows


def build_category_pareto_rows(data: list[QuestionScore]) -> list[dict[str, float | str]]:
    category_gaps: dict[str, float] = {}
    for item in data:
        category_gaps[item.category] = category_gaps.get(item.category, 0.0) + _improvement_gap(item.score)

    rows = [{"label": category, "gap": gap} for category, gap in category_gaps.items()]
    rows.sort(key=lambda row: row["gap"], reverse=True)

    total_gap = sum(float(row["gap"]) for row in rows)
    running = 0.0
    for row in rows:
        running += float(row["gap"])
        row["cumulative_pct"] = (running / total_gap * 100.0) if total_gap else 0.0
    return rows


def _plot_pareto(rows: list[dict[str, float | str]], title: str, y_label: str, output_path: Path) -> None:
    labels = [str(row["label"]) for row in rows]
    values = [float(row["gap"]) for row in rows]
    cumulative = [float(row["cumulative_pct"]) for row in rows]

    fig, ax1 = plt.subplots(figsize=(16, 8))
    bars = ax1.bar(range(len(values)), values, color="#2e86ab", alpha=0.9)
    ax1.set_title(title)
    ax1.set_xlabel("Items sorted by highest improvement opportunity")
    ax1.set_ylabel(y_label)
    ax1.set_xticks(range(len(labels)))
    ax1.set_xticklabels(labels, rotation=85, ha="right", fontsize=8)

    for bar, value in zip(bars, values, strict=False):
        if value > 0:
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=8,
            )

    ax2 = ax1.twinx()
    ax2.plot(range(len(cumulative)), cumulative, color="#f18f01", marker="o", linewidth=2)
    ax2.set_ylabel("Cumulative percentage (%)")
    ax2.set_ylim(0, 105)
    ax2.axhline(80, color="#c73e1d", linestyle="--", linewidth=1)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)


def generate_pareto_charts(output_dir: Path, show: bool = False) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    item_rows = build_item_pareto_rows(QUESTIONNAIRE_DATA)
    category_rows = build_category_pareto_rows(QUESTIONNAIRE_DATA)

    item_chart = output_dir / "pareto_items.png"
    category_chart = output_dir / "pareto_categories.png"

    _plot_pareto(
        rows=item_rows,
        title="Pareto Analysis - Questionnaire Items (Gap from Score 5)",
        y_label="Improvement gap (5 - score)",
        output_path=item_chart,
    )
    _plot_pareto(
        rows=category_rows,
        title="Pareto Analysis - Categories (Total Improvement Gap)",
        y_label="Total category improvement gap",
        output_path=category_chart,
    )

    if show:
        plt.show()
    else:
        plt.close("all")

    return [item_chart, category_chart]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="game-stats-pareto",
        description="Generate Pareto analysis visualizations for the IT questionnaire dataset.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("docs") / "pareto",
        help="Directory to write generated chart images.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display chart windows in addition to saving image files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_files = generate_pareto_charts(output_dir=args.output_dir, show=args.show)
    print("Generated Pareto charts:")
    for path in output_files:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())