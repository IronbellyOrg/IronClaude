---
topic: "Unattended mode for /sc:implement (build-ready spec for a GitHub feature issue)"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-23
---

# Seed Brief: implement-unattended

Dialogue was run unattended (no person to ask): the lead's job text is the answer set; owner decision O5 (build it) is approved, O3 (plan approval before implement) is not answered.

## Problem Statement

`/sc:implement` has no `## Unattended mode` section, so an Orca worker that runs it writes no `return-contract.yaml`; under WC-5 a worker with no contract reports `failed` even for a good run. The release pipeline (CONSENSUS.md topic d, Mode C) needs a coordinator-started worker to run `/sc:implement <plan path>` in a worktree with no person present, and read the result from a contract file. The protocol today asks a person at several points (Ruling after a halt, operator review on re-run, the Ruling question text) and stages `.dev/tasks` itself; none of that can happen in a worker.

## Known Context (all read on 2026-11-23 unless marked UNVERIFIED)

- Source of truth for the shipped primitives is origin/master (565748248). The local checkout (branch ironbelly/orch-ledger-20261122) is 150 commits behind origin/master; installed `~/.claude` copies of `implement.md`, the skill and its four refs equal origin/master byte for byte; installed `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` differ from origin/master (installed is newer or older: not determined).
- Pattern of other commands: `## Unattended mode` section with bullets Switch, Report directory, Contract, Person-mode flags, Gates, Nested invocations, Outward actions; shared rules in `~/.claude/WORKER-CONTRACT.md` (WC-2 no person-blocking step; WC-4 contract written on every outcome with `worker_contract_version`, `worker_status` succeeded|partial|failed|blocked, `command`, `report_path`, `artifacts`, `blocked_question`, `reason`; WC-9 no outward action, `.dev/tasks` staged by the coordinator, implement's private-index snapshots, `refs/superclaude/implement/` refs and revert stay allowed; WC-3 a Ruling halt is reported blocked and never asked; WC-10 waits at most 4 minutes; WC-11 parallel-safe writes).
- The contract already assumes implement is converted: WC-4 "for /sc:implement, also when blocked, carrying the STOP code"; WC-9 says the implement skills defer `.dev/tasks` staging under `--unattended`; `tests/skills/test_worker_contract.py` on origin/master classifies three implement `git add` lines as `deferred:P4` ("/sc:implement is converted in P4").
- `/sc:workflow` under `--unattended` skips `--handoff implement` (the implement executor "accepts the flag only in a later phase").
- Implement STOP table: E-NO-SOURCE, E-SOURCE-MISSING, E-NO-TASKS, E-NO-AC, E-LEGACY, E-HALT-QA, E-RESUME-NEEDED, E-NO-RULING, E-LEDGER-CORRUPT, E-LEDGER-PATH, E-MANAGED-INVALID, E-MANAGED-CONFLICT, E-MANAGED-REVIEW-FAIL, E-PLAN-CHANGED, E-ARCHIVE-MARKER, E-ARCHIVE-BLOCKED. Ladder: A1, A2 fix pass, repair, A3 to A5 with advisers, halt reasons (ladder-end, no-snapshot, batch, head-moved, budget, advice-rejected, dispute, no-runner-up, brief-invalid, no-evidence, operator-review). Resume rows 1, R, P, H, V, X, O, B, S; rows P and H run an "operator review" of the tree as it stands.
- Ledger is one append-only markdown file (legacy `.dev/implement/<slug>/progress.md`; managed `<pkg>/progress.md`); resume is implicit; managed plans (`workflow-plan/1.2`) archive to `.dev/tasks/done/` only via the helper after a fresh FINAL.
- Contract rule "After an /sc:implement stop (decision D2)": a plan is frozen when the latest implement contract is `blocked`, or `failed` with a STOP code other than E-RESUME-NEEDED, or the ledger's first non-complete task ends in halt/blocked with no eligible Ruling.
- Launch-level guard (`src/superclaude/hooks/scripts/launch-level-guard.sh`) denies starting `/sc:implement`, `/task`, `/sc:cleanup` at launch level `worktree` until a person types the command in that session (message LL-IMPL); ship gate `GOVERNED_LEVELS_ALLOWED = False` in `src/superclaude/cli/issue_watch/launch.py`; the issue pipeline's worker brief is a closed template with rows for research, spec, plan, debug only.
- Tests that pin the area: `tests/skills/test_worker_contract.py` (UNATTENDED_EXPECT, P1/P2 sets with exact counts, NOT_CONVERTED lists, `_check_no_unattended_sections`, write-verb audit `WRITE_VERB_CLASSIFICATION` keyed by exact line text, section must contain `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md`, `--report-dir`, no `src/superclaude/`, no Orca command names, and no `nested/` text when its nested list is empty); `tests/skills/test_implement_*.py`.
- `plugins/superclaude/` is a tracked mirror of commands and skills; `src/superclaude/` is the source; `make sync-dev` copies to `.claude/`.

## Constraints

- Never commit, push, merge or open a PR from the mode; stage nothing; no Orca calls inside the command (WC-8, WC-13); installed primitives never name `src/superclaude/` paths for an agent to read.
- Escalation must be a returned status and a written record, never a guess; no Ruling is ever written by the mode.
- Everything must be observable by a test or a file check.
- No em dashes; Python via `uv run`.

## Success Criteria

- `/sc:workflow` can turn the spec into a tasklist with no further questions.
- Both answers to O3 work.
- Every protocol point that asks a person has a defined unattended outcome.

## Open Questions

- O3 plan approval before implement (owner).
- Does the owner's O5 approval count as "the instruction naming /sc:implement" for the brief, or must a live check pass first?
- Parallel batches under unattended: force sequential?
