"""Generate original long style descriptions for the offline creator catalogue.

Run manually with an OpenAI key before a catalogue release. The script receives only
our rubric values and short authored descriptors, never source transcripts or media.
"""

from __future__ import annotations

import argparse
import json
import os

from openai import OpenAI
from dotenv import load_dotenv

from backend.corpus import CREATORS_PATH, REQUIRED_STYLE_AXES, load_catalogue

SYSTEM = """Write exactly 2 or 3 original sentences describing HOW a creator talks.
Cover sentence structure, pacing, questions, directness, warmth, and movement between ideas.
Use only the supplied authored rubric. Do not quote, name videos, mention topics, or use catchphrases."""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=os.environ.get("DESCRIPTOR_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required to build long style descriptors.")
    catalogue = load_catalogue(CREATORS_PATH)
    client = OpenAI()
    rows = catalogue["creators"][: args.limit]
    for row in rows:
        rubric = {axis: row["style_profile"][axis] for axis in REQUIRED_STYLE_AXES}
        prompt = json.dumps({"role": row["role"], "short_descriptor": row["source_note"], "rubric": rubric})
        response = client.responses.create(
            model=args.model,
            instructions=SYSTEM,
            input=prompt,
            max_output_tokens=320,
        )
        descriptor = response.output_text.strip()
        if len(descriptor.split()) < 20 or descriptor.count(".") < 2:
            raise RuntimeError(f"Model returned an unusable descriptor for {row['id']}.")
        row["style_descriptor_long"] = descriptor
    CREATORS_PATH.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} descriptors using {args.model}.")


if __name__ == "__main__":
    main()
