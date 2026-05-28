# D-0060 — T05.08 Spec: Preserve 3-Cycle Hard Cap + Four Counters + X-003 Rejection

**Task:** T05.08 (Phase 5 — M5 Retry Monotonicity + Regression Halts)
**Roadmap items:** R-097 (3-cycle hard cap preservation — `rf-team-lead.md:417` byte-diff zero), R-098 (four-counter independence — `rf-task-builder.md` I16 per-gate table preserved), R-099 (X-003 rejection enforcement — slow-shrink `|F|=5,4` continues)
**Date:** 2026-05-18
**Status:** PASS
**Tier:** STRICT
**Confidence:** [█████████-] 90%
**Critical Path Override:** Yes (preservation invariants govern fix-cycle escalation safety)
**Verification method:** Sub-agent (quality-engineer) — read-only ratification of preservation invariants + synthetic-fixture self-consistency on X-003 rejection
**Sub-Agent Delegation:** Required (executed; report at `quality-engineer-report.md`)
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`

---

## 1. Scope

T05.08 is a **non-editing preservation gate**. It produces no source changes; its purpose is to (a) pin the byte-identity of the two preservation regions named in the roadmap (R-097, R-098), (b) re-prove the X-003 rejection invariant (R-099) with a slow-shrink `|F|=5,4` fixture that demonstrates strict shrink continues without any halt, and (c) ratify all three invariants against a quality-engineer sub-agent.

The three deliverables (per task spec):

1. **Byte-diff zero on `rf-team-lead.md:417`.** The pre-existing 3-cycle hard cap at the line "**Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings." MUST NOT be replaced or short-circuited by the M5 FR-CONV.5 wrapper; it remains the **fourth-precedence backstop** below regression → monotonicity → hard-cap → proceed.
2. **Four-counter independence verified at `rf-task-builder.md:354-360`.** The QA-gate fix-cycle counter table preamble (and the four named per-gate counters it introduces — research-gate, synthesis-gate, report-validation, task-integrity, with "Any qualitative gate" as a category modifier) MUST remain byte-identical at the canonical line range (354-360) named by the task spec; the full table (354-364) is also captured here for completeness against the T05.01..T05.07 baseline `121de142…`.
3. **X-003 rejection enforced — slow-shrink fixture continues.** A `|F_1|=5, |F_2|=4` fixture (shrink by 1, the smallest legitimate strict-shrink delta) MUST proceed to cycle 3 with NO halt of any kind. No rate-of-shrink tunable parameter is consulted; the monotonicity check is the binary predicate `|F_{n+1}| >= |F_n|`, which is FALSE when 4 < 5, so Step 2 returns PROCEED and Step 4 re-spawns the next cycle.

The placement is preservation-only — T05.08 introduces no SKILL.md / rf-task-builder.md / rf-qa.md edits. The byte-identity claims are verified against the same baselines captured in D-0058 (T05.05) and D-0059 (T05.07).

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| 3-cycle hard cap (preservation target R-097) | `src/superclaude/agents/rf-team-lead.md` L417 | The pre-existing backstop; must remain byte-identical to baseline `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| Per-gate counter table (preservation target R-098) | `src/superclaude/agents/rf-task-builder.md` L354-360 (canonical task-spec range); L354-364 (full table) | The four independent retry counters at I16; canonical range `354-360` SHA256 baseline `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1`; full-table range `354-364` SHA256 baseline `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` (matches D-0058 §9.4 / D-0059 §1) |
| Four-counter independence statement (FR-CONV.5 wrapper) | `src/superclaude/agents/rf-task-builder.md` L370 | Canonical wording added by T05.01/MIG-005: "The per-gate retry counters … are independent and NEVER collapsed; FR-CONV.5 layers halts ON TOP without merging counter state across gates." |
| X-003 rejection rule (preservation target R-099) | `.dev/releases/current/task-builder-merge/roadmap.md` row 10 (M5) | "Rate-threshold halt design (X-003) REJECTED; `\|F\|= 5, 4` (shrink by 1) MUST continue" — no rate-of-shrink parameter introduced |
| FR-CONV.5 wrapper text (referencing rf-team-lead.md:417) | `src/superclaude/skills/task-builder/SKILL.md` L1014-1027 | T05.01 baseline `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5`; cites the rf-team-lead.md:417 cap as the fourth-precedence backstop |
| API-004 contract block + 4-step ordering rule | `src/superclaude/skills/task-builder/SKILL.md` L1029-1059 | T05.02..T05.07 baseline `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099`; Step 2 monotonicity check is the binary predicate consulted in the X-003 fixture |
| INV-012 cross-cycle dedup composition (T05.07) | `src/superclaude/skills/task-builder/SKILL.md` L1061-1075 | The immediately preceding milestone establishing INV-012 — confirms that T05.08 inherits the F-set identity rule with no further composition changes |
| Roadmap item R-097 | `.dev/releases/current/task-builder-merge/roadmap.md` row 8 (M5) | "byte-diff-rf-team-lead.md:417-line-pre/post:0; cap:remains-as-fourth-precedence-backstop" |
| Roadmap item R-098 | `.dev/releases/current/task-builder-merge/roadmap.md` row 9 (M5) | "per-gate-counters-at-rf-task-builder.md:354-360:preserved; no-shared-monotonicity-state-across-counters" |
| Roadmap item R-099 | `.dev/releases/current/task-builder-merge/roadmap.md` row 10 (M5) | "slow-shrink-fixture:continues-to-next-cycle; no-rate-of-shrink-parameter-introduced" |
| T05.05 evidence (predecessor baseline) | `.dev/releases/current/task-builder-merge/artifacts/D-0058/evidence.md` §9.3-9.4 | Source of the four preserved hashes consulted here |
| T05.07 evidence (immediate predecessor) | `.dev/releases/current/task-builder-merge/artifacts/D-0059/evidence.md` §1 + §3 | Re-confirms the four preserved hashes at end of cycle T05.07; T05.08 inherits and re-verifies |

## 3. Preservation invariants (verbatim baselines)

| Region | Line range | SHA256 baseline | Source of baseline |
|---|---|---|---|
| `rf-team-lead.md:417` (3-cycle hard cap — R-097) | 417 (single line) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | T05.01 + D-0058 §9.3 + D-0059 §1 |
| `rf-task-builder.md` L354-360 (canonical task-spec range — R-098) | 354..360 | `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1` | Newly pinned at T05.08 (matches current file content, no edits between T05.01 baseline window and T05.08) |
| `rf-task-builder.md` L354-364 (full I16 table — R-098 full-table audit window) | 354..364 | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | T05.01 + D-0058 §9.4 + D-0059 §1 |
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — also referenced from §2 above) | 1014..1027 | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | T05.01 + D-0058 §9.1 + D-0059 §1 |
| `SKILL.md` L1029-1059 (API-004 contract block + 4-step ordering rule — also referenced from §2 above) | 1029..1059 | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | T05.02 + D-0058 §9.2 + D-0059 §1 |

All five regions match their baselines at T05.08 pre-edit and post-step measurement (T05.08 makes no edits). See §7 of evidence for the byte-identity hash log.

## 4. X-003 rejection fixture (R-099)

Fixture path: `.dev/releases/current/task-builder-merge/artifacts/D-0060/fixture-slow-shrink-F-5-4.log`.

Scenario: cycle 1 emits `F_1 = {item-3.1, item-3.2, item-3.3, item-3.4, item-3.5}` (`|F_1|=5`); cycle 2 emits `F_2 = {item-3.2, item-3.3, item-3.4, item-3.5}` (`|F_2|=4`, strict shrink by 1 — the minimum legitimate slow-shrink delta); cycle 3 emits `F_3 = ∅` (gate converges). The 4-step ordering rule at SKILL.md L1050-1059 evaluates:

| Cycle transition | Step 1 (regression) | Step 2 (monotonicity) | Step 3 (hard-cap) | Step 4 (proceed) |
|---|---|---|---|---|
| 1→2 | PASS (PASS_1 ∩ FAIL_2 = ∅) | PROCEED (4 < 5 → strict shrink → predicate `|F_{n+1}| >= |F_n|` is FALSE) | PROCEED (research-gate counter 2/3) | re-spawn cycle 3 |
| 2→3 | PASS (FAIL_3 = ∅) | SKIP (`|F_3|=0` precondition `|F_n|>0` not met) | PROCEED (counter 3/3 at proceed boundary; not consulted, all-PASS) | gate converges |

Key assertion: `grep -cE "^TRANSITION.*verdict=HALT-MONOTONICITY"` returns `0` — the monotonicity check is the binary predicate, not a rate threshold; shrink-by-1 is sufficient to PROCEED. This codifies X-003 rejection: there is no `min_shrink_rate` parameter consulted at any step.

Acceptance bullets covered by this fixture (T05.08 task spec):
- "`|F|=5,4` slow-shrink fixture continues to cycle 3 (X-003 NOT triggered)" — verified by `grep -c "^CYCLE 3 START" = 1`.
- "Existing `rf-team-lead.md:417` 3-cycle hard cap referenced as fallback" — the fixture annotates the hard-cap step for both transitions with `research-gate counter N/3 (rf-task-builder.md:354-364)`.

## 5. Acceptance criteria coverage

| AC | Statement (verbatim from T05.08 task) | Where verified |
|----|----------------------------------------|----------------|
| AC1 | "Byte-diff of `rf-team-lead.md:417` pre/post M5 changes is zero." | §3 hash log (pre-edit baseline `51725c0f…` == post-step measurement `51725c0f…`); evidence §7 |
| AC2 | "Per-gate counters at `rf-task-builder.md:354-360` are independent (no shared monotonicity state)." | §3 hash log (`72200fbe…` canonical task-spec range + `121de142…` full-table range, both byte-identical) AND `rf-task-builder.md` L370 four-counter independence statement byte-identical; evidence §7-§8 |
| AC3 | "`|F|=5,4` slow-shrink fixture continues to cycle 3 (X-003 NOT triggered)." | §4 fixture (`fixture-slow-shrink-F-5-4.log` line 41 / 53 — `CYCLE 3 START` present + `GATE VERDICT: PASS`); evidence §6 |
| AC4 | "Sub-agent report confirms three preservation invariants." | quality-engineer sub-agent report at `quality-engineer-report.md` §7 verdict; evidence §5 |

## 6. Sub-agent verification contract

A quality-engineer sub-agent re-runs the preservation hashes, re-grep-checks the four-counter independence statement at rf-task-builder.md:370, re-runs the fixture grep assertions, and emits a structured PASS/FAIL verdict per AC. Report path: `.dev/releases/current/task-builder-merge/artifacts/D-0060/quality-engineer-report.md`.

## 7. Linked downstream tasks

- **T05.09 (D-0061)** — SKILL.md A.9 invariant tail + Behavioral Constraints halt-precedence edits; relies on T05.08's preservation of L1014-1027 and L1029-1059.
- **T05.10 (D-0062)** — rf-task-builder.md I16 fix-cycle encoding edits at :334-361; relies on T05.08's preservation of L354-360 (and the surrounding I16 context).
- **T05.13 (D-0064)** — TEST-015 + TEST-016 fixtures; the X-003 rejection rule established here is required for TEST-015's strict-monotonicity halt assertions to remain calibrated.
- **T05.14 (D-0065)** — TEST-017 + TEST-022 fixtures; the slow-shrink fixture here is the prototype the TEST-017 pytest fixture codifies for automated CI execution.
- **T05.16 (D-0067)** — MIG-005 landing migration; verifies the byte-identity claims one more time at the commit boundary.
- **T05.17 (D-0100)** — Final K-005 false-halt-rate sweep; re-runs `|F|=5,4`, `|F|=5,3`, `|F|=5,2` with this fixture as the baseline calibration.

## 8. Rollback

As stated in roadmap (M5 R-097..R-099): preservation invariants are read-only and have no rollback surface — they only fail if a downstream edit drifts. If a future commit drifts the byte-identity of `rf-team-lead.md:417` or `rf-task-builder.md:354-360`, the T05.16 MIG-005 sub-agent diff spot-check at AC3 ("rf-team-lead.md:417 byte-identical and four counters preserved") will block the merge.

## 9. Confidence

[█████████-] **90%** — the preservation invariants are mechanical (hash equality) and the X-003 fixture is a 53-line synthetic execution log with byte-exact grep assertions. The 10% residual covers: (a) the canonical task-spec line range (354-360) is narrower than the full counter table (354-364), so the evidence captures both ranges to avoid future ambiguity; (b) the four-counter wording is canonical across the M5 roadmap but the actual table has 5 rows ("Any qualitative gate" is a category modifier — explicit clarification in §1 / §3 of this spec and in the sub-agent report).
