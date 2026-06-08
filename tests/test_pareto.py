"""Tests for the Pareto analysis utility (bonus visualisation module)."""

from __future__ import annotations

from game_stats import pareto


def test_improvement_gap_clamps_to_zero() -> None:
    assert pareto._improvement_gap(5.0) == 0.0
    assert pareto._improvement_gap(2.0) == 3.0
    # Scores above the max never produce a negative gap.
    assert pareto._improvement_gap(6.0) == 0.0


def test_build_item_pareto_rows_is_sorted_and_cumulative() -> None:
    rows = pareto.build_item_pareto_rows(pareto.QUESTIONNAIRE_DATA)

    assert len(rows) == len(pareto.QUESTIONNAIRE_DATA)
    # Gaps are sorted descending (largest improvement opportunity first).
    gaps = [row["gap"] for row in rows]
    assert gaps == sorted(gaps, reverse=True)
    # Cumulative percentage is monotonic and ends at 100%.
    cumulative = [row["cumulative_pct"] for row in rows]
    assert cumulative == sorted(cumulative)
    assert cumulative[-1] == 100.0


def test_build_category_pareto_rows_aggregates_by_category() -> None:
    rows = pareto.build_category_pareto_rows(pareto.QUESTIONNAIRE_DATA)

    categories = {item.category for item in pareto.QUESTIONNAIRE_DATA}
    assert {row["label"] for row in rows} == categories
    assert rows[-1]["cumulative_pct"] == 100.0


def test_build_rows_handle_empty_input() -> None:
    assert pareto.build_item_pareto_rows([]) == []
    assert pareto.build_category_pareto_rows([]) == []


def test_generate_pareto_charts_writes_files(tmp_path) -> None:
    outputs = pareto.generate_pareto_charts(output_dir=tmp_path)

    assert len(outputs) == 2
    for path in outputs:
        assert path.exists()
        assert path.stat().st_size > 0


def test_main_generates_charts(tmp_path, capsys) -> None:
    exit_code = pareto.main(["--output-dir", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Generated Pareto charts" in captured.out
    assert (tmp_path / "pareto_items.png").exists()
    assert (tmp_path / "pareto_categories.png").exists()
