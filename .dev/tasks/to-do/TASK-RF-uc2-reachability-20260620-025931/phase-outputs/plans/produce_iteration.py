#!/usr/bin/env python3
"""Producer harness for the FR-RSR UC-2 reflect eval iteration.

For each selected case it:
  1. Materializes the fixture: reconstructs the POST-image of every file in
     input/diff.patch and writes it into a scratch tree under
     iterations/<iter>/eval-<name>/fixture/ (preserving the b/<path> layout),
     so the reflect reachability sweep has real symbols to walk. (No `git
     apply` — direct post-image write avoids context-match fragility.)
  2. (--run only) Invokes the CURRENT reflect skill headless via `claude -p`,
     scoped to the scratch tree, writing artifacts into
     eval-<name>/with_skill/outputs/. It then aliases return-contract.yaml ->
     contract.yaml (the name the grader assertions target).
  3. (--run + headline) Invokes the OLD snapshot (skill-snapshot/reflect-v1.md)
     via --append-system-prompt, writing eval-<name>/old_skill/outputs/REPORT.md.

Default mode is DRY-RUN: it only materializes scratch trees and prints the
exact claude commands it WOULD run, so the deterministic half can be validated
without spending proxy tokens. Pass --run to actually invoke claude.

Usage:
    uv run python .../produce_iteration.py [--iter fr-rsr-uc2] [--cases 37,38,...]
                                           [--run] [--grade]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

WS = Path(
    "/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/eval-workspaces/sc-reflect"
)
REGISTRY = WS / "evals" / "evals.json"
SNAPSHOT = WS / "skill-snapshot" / "reflect-v1.md"
GRADER = WS / "grader.py"

# Only the headline (37) needs an old_skill baseline run.
OLD_SKILL_IDS = {37}


def parse_postimage(patch_text: str) -> dict[str, str]:
    """Reconstruct the post-image of every file in a unified git diff.

    Returns {b_path: file_contents}. For a fully-added file the post-image is
    the complete new file; for a partial modification it is the concatenation
    of the changed hunks' context+added lines (enough for symbol resolution).
    """
    files: dict[str, list[str]] = {}
    cur: str | None = None
    in_hunk = False
    for line in patch_text.splitlines():
        if line.startswith("diff --git "):
            cur = None
            in_hunk = False
            continue
        if line.startswith("+++ "):
            target = line[4:].strip()
            if target == "/dev/null":
                cur = None
            else:
                cur = target[2:] if target.startswith("b/") else target
                files.setdefault(cur, [])
            in_hunk = False
            continue
        if line.startswith("--- "):
            continue
        if line.startswith("@@"):
            in_hunk = True
            continue
        if cur is None or not in_hunk:
            continue
        if line.startswith("+"):
            files[cur].append(line[1:])
        elif line.startswith("-"):
            continue
        elif line.startswith(" "):
            files[cur].append(line[1:])
        elif line == "":
            files[cur].append("")
    return {p: "\n".join(lines) + "\n" for p, lines in files.items() if lines}


def materialize(case_dir: Path, scratch: Path) -> list[str]:
    """Write the post-image of every file in the case diff into `scratch`.

    Does NOT manage the `.claude` skill symlink — that is set per-run by
    set_skill_link() so the current run can load a chosen skill ecosystem while
    the old_skill (v1 snapshot) run runs with NO skill symlink (uncontaminated).
    """
    if scratch.exists():
        shutil.rmtree(scratch)
    patch = (case_dir / "input" / "diff.patch").read_text(encoding="utf-8")
    post = parse_postimage(patch)
    written = []
    for rel, content in sorted(post.items()):
        dest = scratch / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(rel)
    return written


def set_skill_link(scratch: Path, skill_claude: Path | None) -> None:
    """Point `<scratch>/.claude` at the chosen skill ecosystem, or remove it.

    With a target: `cwd=scratch` resolves THAT skill (worktree=after, snapshot=before)
    while Serena still activates the fixture tree. With None: no skill symlink, so the
    old_skill v1-snapshot run cannot auto-load the 1.6.0 skill (faithful FAIL-pre baseline).
    """
    link = scratch / ".claude"
    if link.is_symlink() or link.exists():
        link.unlink()
    if skill_claude is not None:
        link.symlink_to(skill_claude)


def load_cases(ids: list[int]) -> list[dict]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_id = {int(e["id"]): e for e in registry["evals"]}
    out = []
    for i in ids:
        if i not in by_id:
            raise SystemExit(f"eval id {i} not in registry")
        out.append(by_id[i])
    return out


def current_skill_cmd(case: dict, scratch: Path, out_dir: Path, depth: str = "standard") -> list[str]:
    case_dir = WS / case["case_dir"]
    diff = case_dir / "input" / "diff.patch"
    tasklist = case_dir / "input" / "tasklist.md"
    prompt = (
        f"/sc:reflect --mode post --diff {diff} --tasklist {tasklist} "
        f"--scope {scratch} --output {out_dir} --depth {depth}"
    )
    return [
        "claude", "-p", prompt,
        "--permission-mode", "bypassPermissions",
        "--add-dir", str(scratch),
        "--add-dir", str(out_dir.parent),
    ]


def old_skill_cmd(case: dict, scratch: Path, out_dir: Path) -> list[str]:
    case_dir = WS / case["case_dir"]
    diff = case_dir / "input" / "diff.patch"
    tasklist = case_dir / "input" / "tasklist.md"
    report = out_dir / "REPORT.md"
    prompt = (
        "Apply the reflect protocol given in your system prompt as a UC-2 "
        f"post-execution audit of the diff at {diff} against the tasklist at "
        f"{tasklist}, with the affected source tree at {scratch}. Write your "
        f"full audit report (verdict + any deviations) to {report}."
    )
    return [
        "claude", "-p", prompt,
        "--permission-mode", "bypassPermissions",
        "--append-system-prompt", SNAPSHOT.read_text(encoding="utf-8"),
        "--add-dir", str(scratch),
        "--add-dir", str(out_dir.parent),
    ]


def alias_contract(out_dir: Path) -> None:
    rc = out_dir / "return-contract.yaml"
    cy = out_dir / "contract.yaml"
    if rc.exists() and not cy.exists():
        shutil.copy2(rc, cy)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iter", default="fr-rsr-uc2")
    ap.add_argument("--cases", default="37,38,39,40,41")
    ap.add_argument("--run", action="store_true", help="actually invoke claude (default: dry-run)")
    ap.add_argument("--grade", action="store_true", help="run grader.py after producing")
    ap.add_argument("--no-old", action="store_true", help="skip the old_skill snapshot run")
    ap.add_argument("--no-current", action="store_true", help="skip the with_skill current run (e.g. produce only the old_skill baseline)")
    ap.add_argument(
        "--skill-claude",
        default="/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.claude",
        help="path to the .claude ecosystem the CURRENT run loads. "
             "Worktree .claude = AFTER (strengthened); the before-strengthening "
             "snapshot = BEFORE. The old_skill run never uses this (no symlink).",
    )
    ap.add_argument("--reflect-depth", default="standard", choices=["quick", "standard", "deep"],
                    help="reflect --depth for the current run (quick = faster, skips T2 ensemble; field emission is unchanged)")
    args = ap.parse_args()
    skill_claude = Path(args.skill_claude).resolve()
    if not (skill_claude / "skills" / "sc-reflect-protocol" / "SKILL.md").exists():
        raise SystemExit(f"--skill-claude has no sc-reflect skill: {skill_claude}")

    ids = [int(x) for x in args.cases.split(",") if x.strip()]
    cases = load_cases(ids)
    iter_dir = WS / "iterations" / args.iter
    iter_dir.mkdir(parents=True, exist_ok=True)

    for case in cases:
        eid = int(case["id"])
        name = case["name"]
        eval_dir = iter_dir / f"eval-{name}"
        scratch = eval_dir / "fixture"
        with_out = eval_dir / "with_skill" / "outputs"
        with_out.mkdir(parents=True, exist_ok=True)
        # grader.py writes both with_skill/ and old_skill/ grading.json unconditionally,
        # so every case needs an old_skill/ dir even when it has no old_skill assertions.
        (eval_dir / "old_skill" / "outputs").mkdir(parents=True, exist_ok=True)

        written = materialize(WS / case["case_dir"], scratch)
        # Write the grader metadata so this iteration is self-gradeable (eval_id,
        # eval_name, assertions copied verbatim from the registry).
        (eval_dir / "eval_metadata.json").write_text(
            json.dumps({
                "eval_id": eid,
                "eval_name": name,
                "case_dir": case["case_dir"],
                "mode": case["mode"],
                "use_case": case["use_case"],
                "assertions": case["assertions"],
            }, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\n[{eid}] eval-{name}")
        print(f"  materialized {len(written)} file(s) -> {scratch.relative_to(WS)}:")
        for w in written:
            print(f"    {w}")

        cur_cmd = current_skill_cmd(case, scratch, with_out, args.reflect_depth)
        print("  CURRENT skill run (with_skill):")
        print(f"    cwd={scratch}  skill={skill_claude}")
        print(f"    claude -p \"/sc:reflect --mode post --diff .../input/diff.patch "
              f"--tasklist .../input/tasklist.md --scope {scratch.name} --output with_skill/outputs\"")
        if args.run and not args.no_current:
            set_skill_link(scratch, skill_claude)   # current run loads the chosen skill
            print("    >>> invoking claude (current skill)…")
            r = subprocess.run(cur_cmd, cwd=scratch, capture_output=True, text=True)
            (with_out / "claude-stdout.txt").write_text(r.stdout, encoding="utf-8")
            (with_out / "claude-stderr.txt").write_text(r.stderr, encoding="utf-8")
            alias_contract(with_out)
            print(f"    exit={r.returncode}; stdout/stderr captured under with_skill/outputs/")

        if eid in OLD_SKILL_IDS and not args.no_old:
            old_out = eval_dir / "old_skill" / "outputs"
            old_out.mkdir(parents=True, exist_ok=True)
            print("  OLD snapshot run (old_skill, headline only):")
            print(f"    claude -p --append-system-prompt \"$(cat skill-snapshot/reflect-v1.md)\" "
                  f"\"…audit… write to old_skill/outputs/REPORT.md\"")
            if args.run:
                set_skill_link(scratch, None)   # NO skill symlink → faithful v1 baseline
                print("    >>> invoking claude (old snapshot, no .claude symlink)…")
                old_cmd = old_skill_cmd(case, scratch, old_out)
                r = subprocess.run(old_cmd, cwd=scratch, capture_output=True, text=True)
                (old_out / "claude-stdout.txt").write_text(r.stdout, encoding="utf-8")
                (old_out / "claude-stderr.txt").write_text(r.stderr, encoding="utf-8")
                print(f"    exit={r.returncode}; captured under old_skill/outputs/")

    if args.grade:
        print("\n=== grading ===")
        subprocess.run(["uv", "run", "python", str(GRADER), str(iter_dir)], cwd=WS.parents[2])

    if not args.run:
        print("\nDRY-RUN complete. Re-run with --run to invoke claude, "
              "and add --grade to grade afterward.")


if __name__ == "__main__":
    main()
