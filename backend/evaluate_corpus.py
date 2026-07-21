"""Aggregate blinded bilingual ratings for a candidate corpus release.

Input is JSON records with candidate_version, baseline_version, rater_id, sample_id,
rank (1-3), and fit (1-5). Rater identity is only used to deduplicate submissions.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ratings", type=Path)
    args = parser.parse_args()
    rows = json.loads(args.ratings.read_text(encoding="utf-8"))
    grouped: dict[str, list[float]] = defaultdict(list)
    seen: set[tuple[str, str, str, int]] = set()
    for row in rows:
        key = (row["candidate_version"], row["rater_id"], row["sample_id"], int(row["rank"]))
        if key in seen or not 1 <= int(row["rank"]) <= 3 or not 1 <= float(row["fit"]) <= 5:
            raise ValueError("Ratings must be unique, blinded top-3 records with fit from 1 to 5.")
        seen.add(key)
        grouped[row["candidate_version"]].append(float(row["fit"]))
    print(json.dumps({version: {"ratings": len(scores), "mean_fit": round(sum(scores) / len(scores), 3)} for version, scores in sorted(grouped.items())}, indent=2))


if __name__ == "__main__":
    main()
