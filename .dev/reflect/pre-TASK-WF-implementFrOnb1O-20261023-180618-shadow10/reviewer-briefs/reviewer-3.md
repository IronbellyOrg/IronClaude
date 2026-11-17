# Reviewer brief 3 — persona: refactorer (model class opus, model claude-opus-5-5, reviewer_id t1a-1)

## T1 card excerpt

```text
# Tier 1 reflection card (UC-1 pre, corpus: archived work unit TASK-WF-implementFrOnb1O-20261023-180618)

## Context
- Spec input is a 1-line source.md pointing at .dev/releases/backlog/ironclaude-onboarding-deck/spec.md (FR-ONB.1 Part A). That file does not exist in any reachable checkout (grounding constraint C-01).
- Tasklist: 7 tasks, 2 phases, constraints embed the spec's authoritative wording verbatim (plan:19-31).
- The work unit was EXECUTED 2026-10-23 (progress.md: all 7 tasks compliant, FINAL: pass) and archived. This shadow re-audit checks (a) plan-vs-spec coverage, (b) plan internal quality/fidelity, (c) recorded-evidence corroboration.

## Findings (candidates; reviewers pressure-test)
- C-01 [constraint] Driving spec absent on disk everywhere (main checkout backlog dir lacks it; never committed under that name). Audit grounding = tasklist-embedded verbatim quotes + package artifacts. No contradiction found between embedded quotes and recorded diffs.
- C-02 [fidelity, positive] All 7 tasks have compliant ledger rows with per-AC file:line anchors; t3-consistency.log records 8 prose-vs-routing-row AGREE checks; t7-tests.log records verify-sync rc=0 and 5/5 tie-break lines carrying the exception; t7-regression.log proves the helper fails on both old fixtures.
- C-03 [residue] Current master evolved past the plan's pinned wording (A1/A3/A4/A8 empty; CHANGELOG entry gone). Expected for archived corpus; ACs are not re-runnable against HEAD. Severity judgment belongs to reviewers: is a plan whose ACs are frozen against a moved baseline still "good"? (It was correct at execution time; later PRs reworked the wording.)
- C-04 [process, minor candidate] progress.md records extras=test:fail for T1 and T2 (md-only edits, no test AC) alongside verdict=compliant; T3-T7 record test:pass. Ledger test-extras semantics on non-test tasks are ambiguous; a reader may misread test:fail as a failed gate.
- C-05 [plan-quality, minor candidate] Task 4's walk-through AC and Task 7's fixture AC are both satisfied by on-disk artifacts (t4-recommend-walk.md, t7-regression.log) — good self-proving design.
- C-06 [open] Plan line 30 (stacked branch, open PR only after #285 merges) is a process constraint outside the package; PR landing is not evidenced inside the package (return-contract has no PR field). Not a defect; noted.

## Coverage
parsed=0, inferred=6, all matched; coverage_pct_union=1.0; parsed-sparse -> Tier 2 (pinned anyway).
```

Your lens: structural invariants — the three-copy sync (guide / plugins copy / core CLAUDE.md level-table block), plugin parity, closed key list and frozen classifier example in prompts.py, regression-test design (helper + fixtures), and whether any plan instruction could silently leave a mirror out of sync (cf. the repo's known plugin-mirror drift class).

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:11:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Hunks are cited by repo-relative path; Read them yourself for full context (you are read-only; audit the hunks, the plan file, the package artifacts, and the current tree).

### .dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/source.md:1 (spec body, whole)
```text
Implement FR-ONB.1 only (Part A) of /home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/spec.md: every bullet and acceptance criterion in FR-ONB.1, and the Part A rows of section 4.2 (all FR-ONB.1 wording is approved by the user on 2026-10-23, including the level 5 re-point). Work in the current repository (this worktree). Do not build the onboarding deck (FR-ONB.2-7) or file issues. Keep src/superclaude/core/HOW-WE-WORK.md, its byte-for-byte copy plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md, and the level-table copy in src/superclaude/core/CLAUDE.md in sync; run make sync-dev; never stage .claude/.
```

### .dev/tasks/done/TASK-WF-implementFrOnb1O-20261023-180618/progress.md (ledger, verbatim)
```text
# implement ledger — source: ./TASK-WF-implementFrOnb1O-20261023-180618.md — created: 2026-10-23T19:01:39Z
PLAN: sha256=c0f2d33c07bc735eae4b9de09fa586d08747fa2c8d72c24bb03ec5f77dc57cb2 source_sha256=63b28da00b47a33b0a7719f3ea39270491e840c683a977c8cff25200d1e8534e
T1: start sha=8b749fec46db0268935842ff6aa94b3078461357
T1: complete verdict=compliant ac=T1.AC1,T1.AC2,T1.AC3,T1.AC4,T1.AC5 evidence=T1.AC1@src/superclaude/core/HOW-WE-WORK.md:17,T1.AC1@src/superclaude/core/HOW-WE-WORK.md:18,T1.AC2@src/superclaude/core/HOW-WE-WORK.md:9,T1.AC3@./artifacts/t1-checks.log:4,T1.AC4@src/superclaude/core/HOW-WE-WORK.md:19,T1.AC5@src/superclaude/core/HOW-WE-WORK.md:11 extras=lint:skip,typecheck:skip,test:fail files=src/superclaude/core/HOW-WE-WORK.md
T2: start sha=df0518936104d5498cb19a4a979efd16c0ddff08
T2: complete verdict=compliant ac=T2.AC1,T2.AC2,T2.AC3,T2.AC4,T2.AC5,T2.AC6,T2.AC7 evidence=T2.AC1@src/superclaude/core/HOW-WE-WORK.md:222,T2.AC2@src/superclaude/core/HOW-WE-WORK.md:100-106,T2.AC3@src/superclaude/core/HOW-WE-WORK.md:128,T2.AC3@src/superclaude/core/HOW-WE-WORK.md:203,T2.AC4@src/superclaude/core/HOW-WE-WORK.md:53,T2.AC5@src/superclaude/core/HOW-WE-WORK.md:40,T2.AC6@src/superclaude/core/HOW-WE-WORK.md:134-135,T2.AC7@./artifacts/t2-few-files.log:2-3 extras=lint:skip,typecheck:skip,test:fail files=src/superclaude/core/HOW-WE-WORK.md
T3: start sha=667569fb33885c37b56abcdf3b312e4c37c8b70a
T3: complete verdict=compliant ac=T3.AC1,T3.AC2,T3.AC3,T3.AC4,T3.AC5,T3.AC6 evidence=T3.AC1@plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:9,T3.AC2@src/superclaude/core/HOW-WE-WORK.md:321-322,T3.AC3@src/superclaude/core/HOW-WE-WORK.md:323,T3.AC3@src/superclaude/core/HOW-WE-WORK.md:326,T3.AC4@./artifacts/t3-consistency.log:2-10,T3.AC5@src/superclaude/core/HOW-WE-WORK.md:243,T3.AC5@src/superclaude/core/CLAUDE.md:67,T3.AC6@./artifacts/t3-tests.log:1 extras=lint:skip,typecheck:skip,test:pass files=src/superclaude/core/HOW-WE-WORK.md,src/superclaude/core/CLAUDE.md,plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
T4: start sha=491375adddb5c1a0c4357a57084e4fa6141102b3
T4: complete verdict=compliant ac=T4.AC1,T4.AC2,T4.AC3,T4.AC4,T4.AC5 evidence=T4.AC1@src/superclaude/skills/sc-recommend/SKILL.md:155,T4.AC1@src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:38,T4.AC2@src/superclaude/skills/sc-recommend/SKILL.md:58,T4.AC2@plugins/superclaude/skills/sc-recommend/SKILL.md:58,T4.AC3@./artifacts/t4-checks.log:4-6,T4.AC4@./artifacts/t4-recommend-walk.md:1,T4.AC5@./artifacts/t4-tests.log:15 extras=lint:skip,typecheck:skip,test:pass files=src/superclaude/skills/sc-recommend/SKILL.md,src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md,plugins/superclaude/skills/sc-recommend/SKILL.md,plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md
T5: start sha=61f0ddef72fda0c8fd0a1216491191cb929381e3
T5: complete verdict=compliant ac=T5.AC1,T5.AC2,T5.AC3,T5.AC4 evidence=T5.AC1@src/superclaude/cli/recommend/prompts.py:166-168,T5.AC2@src/superclaude/cli/recommend/prompts.py:28-39,T5.AC2@src/superclaude/cli/recommend/prompts.py:72-87,T5.AC3@./artifacts/t5-checks.log:4,T5.AC4@./artifacts/t5-tests.log:1 extras=lint:pass,typecheck:skip,test:pass files=src/superclaude/cli/recommend/prompts.py
T6: start sha=e3b2665263b58b0e97352f65366a61bf4a8a6aa8
T6: complete verdict=compliant ac=T6.AC1,T6.AC2 evidence=T6.AC1@docs/user-guide/commands.md:43,T6.AC1@docs/user-guide/commands.md:70,T6.AC1@docs/user-guide/commands.md:456,T6.AC1@docs/user-guide/commands.md:695,T6.AC1@docs/user-guide/session-management.md:125,T6.AC2@./artifacts/t6-sweep.log:1 extras=lint:skip,typecheck:skip,test:pass files=docs/user-guide/commands.md,docs/user-guide/session-management.md
T7: start sha=c73b479df5ea8a7263044af7cb723192e60c1735
T7: complete verdict=compliant ac=T7.AC1,T7.AC2,T7.AC3,T7.AC4,T7.AC5 evidence=T7.AC1@tests/core/test_how_we_work_routing_table.py:372,T7.AC1@./artifacts/t7-regression.log:1-4,T7.AC2@./artifacts/t7-tests.log:1-2,T7.AC3@./artifacts/t7-manual-check.md:9,T7.AC4@./artifacts/t7-tests.log:12,T7.AC5@./artifacts/t7-tests.log:20 extras=lint:pass,typecheck:skip,test:pass files=tests/core/test_how_we_work_routing_table.py,CHANGELOG.md
FINAL: pass evidence=src/superclaude/core/HOW-WE-WORK.md:9,src/superclaude/core/HOW-WE-WORK.md:222,src/superclaude/core/CLAUDE.md:67,src/superclaude/skills/sc-recommend/SKILL.md:58,src/superclaude/cli/recommend/prompts.py:166-168,docs/user-guide/commands.md:695,tests/core/test_how_we_work_routing_table.py:393,./artifacts/t7-tests.log:12 state=74469b5938817914b471a932a12505a3cf264f0c4cff5ab02395b857aede55b4
ARCHIVE: start id=TASK-WF-implementFrOnb1O-20261023-180618 token=424911c66078122b
```

## Coverage slice

| Requirement | Matched | Grounding |
|---|---|---|
| INF-001 implement FR-ONB.1 Part A only | Task 1-3 | plan:12-15 |
| INF-002 every bullet + AC of FR-ONB.1 | Task 1-7 | plan:19,56,82-91,113,130,146,159 |
| INF-003 Part A rows of 4.2, user-approved 2026-10-23 incl. level 5 re-point | Task 1 | plan:19,42 |
| INF-004 work in current repository (worktree) | Task 3 | plan:20 |
| INF-005 do NOT build deck FR-ONB.2-7, no issues | Constraints | plan:22 |
| INF-006 three copies in sync + make sync-dev + never stage .claude/ | Task 3, Task 4 | plan:23-24,93-97,116-117 |

All 6 inferred rows matched; coverage_pct_union 1.0; parsed=0 (parsed-sparse).

## Card format (findings-v2, schema in src/superclaude/cli/review/findings_v2.py)

One JSON object per line inside a ```findings-v2 fenced block; fields: id (F1..), severity CRITICAL|MAJOR|MINOR, blocking bool (never true with MINOR), category (one of the reflect-pre set; use contradiction / missing-requirement / unpassable-check / ordering / other as fits), claim (one sentence), citations [{role: plan|spec|source|test|diff|artifact, path: repo-relative, line_start, line_end}], self_confidence 0..1. Paths repo-relative, quotes <=200 chars. Zero findings is valid; then emit a single line {"id":"F0","severity":"MINOR","blocking":false,"category":"other","claim":"no defects found in scope","citations":[],"self_confidence":0.5}? NO — if you find nothing, emit an empty findings block and state what you checked in prose. Then the reviewer_model_self_report line.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.
