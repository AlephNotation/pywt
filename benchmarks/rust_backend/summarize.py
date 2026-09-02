"""Summarize paired benchmark rounds as CSV and Markdown."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

DIRECTION = {
    "dwt_axis0": "forward",
    "dwt_last_axis": "forward",
    "idwt_axis0": "inverse",
    "idwt_last_axis": "inverse",
    "dwt2": "forward",
    "idwt2": "inverse",
    "wavedec2": "forward",
    "waverec2": "inverse",
    "dwtn": "forward",
    "idwtn": "inverse",
}


def percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", type=Path)
    parser.add_argument("--baseline", default="vanilla")
    parser.add_argument("--candidate", default="rust")
    parser.add_argument("--csv", required=True, type=Path)
    parser.add_argument("--markdown", required=True, type=Path)
    args = parser.parse_args()

    rows = defaultdict(dict)
    with args.raw.open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            key = (row["case"], row["dtype"], int(row["round"]))
            rows[key][row["implementation"]] = {
                name: float(row[name]) for name in ("q1_ms", "median_ms", "q3_ms")
            }

    grouped = defaultdict(list)
    for (case, dtype, round_number), implementations in rows.items():
        if (
            args.baseline not in implementations
            or args.candidate not in implementations
        ):
            raise ValueError(f"incomplete comparison for {case}/{dtype}/{round_number}")
        baseline = implementations[args.baseline]
        candidate = implementations[args.candidate]
        grouped[(case, dtype)].append(
            {
                "round": round_number,
                "baseline": baseline,
                "candidate": candidate,
                "speedup": baseline["median_ms"] / candidate["median_ms"],
            }
        )

    summary = []
    for (case, dtype), rounds in grouped.items():
        baseline_times = [row["baseline"]["median_ms"] for row in rounds]
        candidate_times = [row["candidate"]["median_ms"] for row in rounds]
        candidate_q1 = [row["candidate"]["q1_ms"] for row in rounds]
        candidate_q3 = [row["candidate"]["q3_ms"] for row in rounds]
        speedups = [row["speedup"] for row in rounds]
        summary.append(
            {
                "case": case,
                "direction": DIRECTION[case],
                "dtype": dtype,
                "baseline_median_ms": statistics.median(baseline_times),
                "candidate_median_ms": statistics.median(candidate_times),
                "candidate_call_q1_ms": statistics.median(candidate_q1),
                "candidate_call_q3_ms": statistics.median(candidate_q3),
                "candidate_process_min_ms": min(candidate_times),
                "candidate_process_max_ms": max(candidate_times),
                "speedup": statistics.median(speedups),
                "speedup_q1": percentile(speedups, 0.25),
                "speedup_q3": percentile(speedups, 0.75),
            }
        )
    summary.sort(key=lambda row: (row["dtype"], list(DIRECTION).index(row["case"])))

    if not summary:
        raise ValueError("the input contains no complete comparisons")
    fields = list(summary[0])
    with args.csv.open("x", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)

    lines = []
    for dtype in ("float32", "float64"):
        selected = [row for row in summary if row["dtype"] == dtype]
        if not selected:
            continue
        lines.extend(
            [
                f"## {dtype}",
                "",
                f"| Operation | {args.baseline} | {args.candidate} | "
                f"{args.candidate} call IQR | Speedup | Speedup IQR |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in selected:
            lines.append(
                f"| `{row['case']}` | {row['baseline_median_ms']:.3f} ms | "
                f"{row['candidate_median_ms']:.3f} ms | "
                f"{row['candidate_call_q1_ms']:.3f}–"
                f"{row['candidate_call_q3_ms']:.3f} ms | "
                f"{row['speedup']:.2f}x | {row['speedup_q1']:.2f}–"
                f"{row['speedup_q3']:.2f}x |"
            )
        lines.append("")
        for direction in ("forward", "inverse"):
            speedups = [
                row["speedup"] for row in selected if row["direction"] == direction
            ]
            if speedups:
                lines.append(
                    f"- {direction.capitalize()} geometric mean: "
                    f"{statistics.geometric_mean(speedups):.2f}x"
                )
        lines.append(
            f"- Overall geometric mean: "
            f"{statistics.geometric_mean(row['speedup'] for row in selected):.2f}x"
        )
        lines.append("")

    args.markdown.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
