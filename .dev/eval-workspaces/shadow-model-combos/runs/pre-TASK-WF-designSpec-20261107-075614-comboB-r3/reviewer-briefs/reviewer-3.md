# Reviewer brief 3 (persona: refactorer)

## T1 card excerpt

# Tier 1 reflection card (UC-1, pre): merge-guard design spec vs. its 13-task plan

Spec: `source.md` (378 lines, sha256 a865f397...). Plan: `TASK-WF-designSpec-20261107-075614.md` (200 lines, sha256 044809e3...).
Code facts are checked against base commit e8db2fe6 (the commit the spec says it was read from); excerpts are in `artifacts/base-grounding.md`. HEAD has evolved (the feature has since landed), so HEAD files are not evidence for what the plan could know.

## Verified non-issues (checked, no finding)

- Event-count pins: every "43" at base is in the Task 2 edit list (`artifacts/base-grounding.md` 80-89).
- No import cycle: `merge_guard` -> `conflicts` -> `fsm` -> `loop_guard/models/severity_router`; `run_log` imports only `models` (`artifacts/base-grounding.md` 9-32). Task 5's fresh-interpreter import check covers it anyway.
- `allowed-tools` already grants `Bash(gh|git|uv|make|jq *)` and scripts are checked only for existence (`artifacts/base-grounding.md` 4-7, 52-77), so no front-matter edit is missing.
- Real crash-window API exists: `resolve_crash_window(run_log, dangling, *, remote_reachable, observed_remote_sha)` returns `(branch, state)` (`artifacts/base-grounding.md` 43-49), so Task 11's "real branch" tests are feasible.

## Recommendation

Plan is largely faithful (union coverage 0.81, all 12 named tests and all section 4.1 tables carried). Fix T1-F1 before execution by giving `resume_decision` the `cycle_id`, `applied_edits` and `target_sha` inputs (or stating that row 4 returns a release request the caller completes). Escalation is forced regardless (tier pin 2, `coverage_degraded`).

self-reported confidence: 0.70

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T05:55:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Files you may Read directly (repo-relative): .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md (spec), .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (plan), .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r3/artifacts/base-grounding.md (base-commit excerpts). Cite spec/plan lines by these paths.

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:17-27

````markdown
## Constraints

- Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:283-301

````markdown
## 6. Files to change

| File | Kind | Notes |
|---|---|---|
| `src/superclaude/pr_submit/merge_guard.py` | new | section 4.1 |
| `src/superclaude/pr_submit/models.py` | edit | 2 members, docstring and count |
| `src/superclaude/pr_submit/run_log.py` | edit | `rebuild_state` key, append docstring count |
| `src/superclaude/pr_submit/fsm.py` | edit | flag, `SkillArgs`, `parse_args` |
| `src/superclaude/pr_submit/__init__.py` | edit | export the public guard names |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | new | section 4.4 |
| `.../refs/merge-guard.md` | new | section 4.5 |
| `.../SKILL.md`, `.../refs/state-machine.md`, `.../refs/loop-guard.md` | edit | additive only (loop-guard: the 43 to 45 enumeration text) |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/skills/test_worker_contract.py` | edit | one `WRITE_VERB_CLASSIFICATION` entry per new hit line (section 4.7); added last in each task that writes a file with hits |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441`; `"draft_guard": None` at `test_run_log.py:312`; `merge_guard.py` into the zero-token file set; script lists only after checking each list's purpose; flag default and choices test mirroring `--conflict-max-tier` |

After editing under `src/superclaude/`: `make sync-dev`, then `make verify-sync`. Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because `tests/cli/test_verify_sync_hooks.py` runs `make verify-sync` inside the full suite; the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`. A repo-wide pin (F12) escaped two reviews because only `tests/pr_submit` was run, so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result (`uv run pytest -q tests`: pass count and every failing test id) on the base commit before the first code edit (pre-existing failures are not this feature's). Never stage `.claude/`. Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests, `test_conflict_sync_protocol.py:576` (no `src/superclaude` text in skill or command files).
````

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboB-r3/artifacts/base-grounding.md:1-99

````markdown
# Base-commit grounding (read-only excerpts at e8db2fe6, the commit the plan was written against; HEAD has evolved)

## G1 SKILL.md front matter (e8db2fe6:src/superclaude/skills/sc-pr-submit-protocol/SKILL.md lines 1-4)
---
name: sc:pr-submit-protocol
description: "PR-review auto-remediation monitor — opens a PR on the fork, runs an attended in-session poll loop for the Augment Code and Codex reviews (each reviewer optional and detected on the PR
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill

## G2 pr_submit imports (e8db2fe6)
fsm.py:
19:from __future__ import annotations
21:import argparse
22:import re
23:from dataclasses import dataclass, field
24:from typing import Callable
26:from .loop_guard import should_halt as loop_guard_should_halt
27:from .models import Finding, MonitorState, PushDecision, SkillResult
28:from .severity_router import ROUTE_REPORT_ONLY, remap_severity, route
conflicts.py:
25:import base64
26:import re
27:from dataclasses import dataclass
34:from .fsm import run_validation_gates
35:from .models import MonitorState
run_log.py:
16:from __future__ import annotations
18:import hashlib
19:import json
20:import os
21:import re
22:from pathlib import Path
24:from .models import EventType

## G3 recovery.py (e8db2fe6:src/superclaude/pr_submit/recovery.py)
BRANCH_A_LANDED = "landed"
BRANCH_B_NOT_LANDED = "not_landed"
BRANCH_C_AMBIGUOUS = "ambiguous"

def detect_crash_window(run_log: RunLog) -> dict | None:
    """Return the dangling ``push_initiated`` event (no matching ``push_completed``), or None.

    Matches on ``idempotency_key``: a ``push_initiated`` whose key has no later
def resolve_crash_window(
    run_log: RunLog,
    dangling: dict,
    *,
    remote_reachable: bool | None,
    observed_remote_sha: str | None = None,
) -> tuple[str, MonitorState]:
    """Resolve a crash window from the LIVE remote-reachability result (INV-007 3-way).

## G4 test_allowed_tools_cover_every_program (e8db2fe6:tests/pr_submit/test_conflict_sync_protocol.py)
def test_allowed_tools_cover_every_program():
    """Every `MECHANICAL_RULES` argv[0] and the first word of every fenced command
    line in the two refs is git, gh, uv, make, jq or a `scripts/` path, and each of
    those programs is granted as `Bash(<prog> *)` in the SKILL front matter."""
    front = _read(SKILL_MD).split("\n---\n", 1)[0]
    tools_line = next(
        line for line in front.splitlines() if line.startswith("allowed-tools:")
    )
    granted = set(re.findall(r"Bash\((\S+) \*\)", tools_line))
    programs = set()
    for rule in MECHANICAL_RULES:
        programs.add(rule.regenerate[0])
        if rule.check:
            programs.add(rule.check[0])
    scripts = set()
    for path in NEW_REFS:
        for word in _fenced_first_words(path):
            if word.startswith("scripts/"):
                scripts.add(word)
            else:
                programs.add(word)
    assert programs <= ALLOWED_PROGRAMS, programs - ALLOWED_PROGRAMS
    assert programs <= granted, programs - granted
    for script in scripts:
        assert (SKILL_DIR / script).is_file(), script


## G5 every '43' event-count pin at e8db2fe6
e8db2fe6:src/superclaude/pr_submit/models.py:3:Defines the closed run-log event enum (exactly 43 members — the 32 from spec
e8db2fe6:src/superclaude/pr_submit/models.py:24:    """Closed enum of run-log event types — EXACTLY 43 members.
e8db2fe6:src/superclaude/pr_submit/run_log.py:117:        Raises :class:`ValueError` if ``event_type`` is not one of the 43 closed
e8db2fe6:src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86:### The 43 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers + conflict cycles)
e8db2fe6:src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:88:The closed `EventType` enum has EXACTLY 43 members — the 32 from §11.3 plus
e8db2fe6:tests/pr_submit/test_codex_reviews.py:441:    assert len(EventType) == 43
e8db2fe6:tests/pr_submit/test_run_log.py:172:    """The closed EventType enum has EXACTLY 43 members, including INV-S1, the two
e8db2fe6:tests/pr_submit/test_run_log.py:174:    assert len(EventType) == 43
e8db2fe6:tests/pr_submit/test_run_log.py:175:    assert len(list(EventType)) == 43

## G6 scripts at e8db2fe6
src/superclaude/skills/sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh

````

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-051: Without `published` no row would match and the PR would stay draft. | T4 | covered (containment 0.83) | source.md:280 |
| INF-052: next checkpoint: `state != OPEN` -> halt `pr_not_open`, nothing pushed, report the local c | T8 | covered (containment 0.75) | source.md:281 |
| INF-053: Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skil | T8 | covered (containment 0.92) | source.md:301 |
| INF-054: the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures wi | T1 | covered (containment 0.87) | source.md:301 |
| INF-055: Never stage `.claude/`. | none | UNMATCHED by containment (best T3 0.33) | source.md:301 |
| INF-056: Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tes | T2 | covered (containment 0.67) | source.md:301 |
| INF-057: `merge_guard.py` into the zero-token file set | T8 | covered (containment 0.83) | source.md:299 |
| INF-058: A static test asserts `merge_guard.py` has no `gh` or `git` word. | T3 | covered (containment 1.00) | source.md:322 |
| INF-059: No task makes a live PR call, and the run that opens the PR must not enable the feature (` | T1 | covered (containment 0.83) | source.md:326 |
| INF-060: The user guide states that draft behaviour is unverified until then, and the PR body state | T1 | covered (containment 1.00) | source.md:326 |
| INF-061: Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCR | none | UNMATCHED by containment (best T1 0.56) | source.md:362 |
| INF-062: Declare dependencies completely, one `Depends on:` line per dependency | none | UNMATCHED by containment (best T8 0.50) | source.md:363 |
| INF-063: The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (s | T8 | covered (containment 0.61) | source.md:364 |
| INF-064: The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3  | none | UNMATCHED by containment (best T8 0.56) | source.md:366 |
| INF-065: The pre-build record task states the release-gate decision of section 8 and records the ba | T1 | covered (containment 0.87) | source.md:367 |
| INF-066: Protocol prose written by the plan never carries `file:NNN` pointers and never contains th | T10 | covered (containment 0.74) | source.md:369 |
| INF-067: its acceptance criterion is a test that the literal line is in `SKILL.md`, and a fresh L2  | T9 | covered (containment 0.85) | source.md:374 |
| INF-068: the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window | none | UNMATCHED by containment (best T11 0.57) | source.md:375 |
| INF-069: the acceptance criteria test both directions and the fresh baseline. | T3 | covered (containment 0.83) | source.md:376 |
| INF-070: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `tes | T11 | covered (containment 0.69) | source.md:377 |
| INF-071: the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against | T10 | covered (containment 0.81) | source.md:377 |
| INF-072: the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition. | T9 | covered (containment 1.00) | source.md:378 |
| INF-073: `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | T7 | covered (containment 1.00) | source.md:292 |
| INF-074: `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | T3 | covered (containment 0.80) | source.md:297 |
| INF-075: How scripts are granted and invoked in the SKILL front matter | T1 | covered (containment 1.00) | source.md:340 |
