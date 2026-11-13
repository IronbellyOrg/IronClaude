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
