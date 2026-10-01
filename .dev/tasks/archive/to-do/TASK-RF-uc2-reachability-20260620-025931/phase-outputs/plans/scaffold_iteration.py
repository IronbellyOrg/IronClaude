#!/usr/bin/env python3
"""Scaffold an FR-RSR UC-2 eval iteration directory for the grader.

Reads .dev/eval-workspaces/sc-reflect/evals/evals.json, and for each requested
eval id creates:

    iterations/<name>/eval-<eval_name>/
        eval_metadata.json          # {eval_id, eval_name, assertions}
        with_skill/outputs/artifacts/
        old_skill/outputs/

The producer then runs the reflect protocol against each case's fixtures and
drops the generated REPORT.md / contract.yaml / artifacts/* into the
with_skill/outputs/ (and, for the headline, old_skill/outputs/) directories,
then runs grader.py over the iteration dir.

Usage:
    uv run python .../scaffold_iteration.py <iteration-name> [id ...]

Defaults: iteration-name=fr-rsr-uc2 ; ids=37 38 39 40 41
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

WORKSPACE = Path(
    "/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect"
)
REGISTRY = WORKSPACE / "evals" / "evals.json"
DEFAULT_IDS = [37, 38, 39, 40, 41]


def main() -> None:
    iteration_name = sys.argv[1] if len(sys.argv) > 1 else "fr-rsr-uc2"
    ids = [int(a) for a in sys.argv[2:]] or DEFAULT_IDS

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_id = {int(e["id"]): e for e in registry["evals"]}

    iter_dir = WORKSPACE / "iterations" / iteration_name
    iter_dir.mkdir(parents=True, exist_ok=True)

    produced = []
    for eval_id in ids:
        entry = by_id.get(eval_id)
        if entry is None:
            raise SystemExit(f"eval id {eval_id} not found in registry")
        eval_name = entry["name"]
        eval_dir = iter_dir / f"eval-{eval_name}"

        # Output drop targets the producer must fill by running the skill.
        (eval_dir / "with_skill" / "outputs" / "artifacts").mkdir(parents=True, exist_ok=True)
        (eval_dir / "old_skill" / "outputs" / "artifacts").mkdir(parents=True, exist_ok=True)

        metadata = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "case_dir": entry["case_dir"],
            "mode": entry["mode"],
            "use_case": entry["use_case"],
            "assertions": entry["assertions"],
        }
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
        )

        with_targets = sorted(
            {a["target"] for a in entry["assertions"] if a.get("target", "").startswith("with_skill/")}
        )
        old_targets = sorted(
            {a["target"] for a in entry["assertions"] if a.get("target", "").startswith("old_skill/")}
        )
        produced.append((eval_id, eval_name, with_targets, old_targets))

    print(f"Scaffolded iteration dir: {iter_dir}")
    for eval_id, eval_name, with_targets, old_targets in produced:
        print(f"\n[{eval_id}] eval-{eval_name}")
        print("  PRODUCER must create (run CURRENT skill -> with_skill/outputs):")
        for t in with_targets:
            print(f"    eval-{eval_name}/{t}")
        if old_targets:
            print("  PRODUCER must create (run OLD snapshot reflect-v1.md -> old_skill/outputs):")
            for t in old_targets:
                print(f"    eval-{eval_name}/{t}")
        else:
            print("  (no old_skill assertions; old_skill run not required)")


if __name__ == "__main__":
    main()
