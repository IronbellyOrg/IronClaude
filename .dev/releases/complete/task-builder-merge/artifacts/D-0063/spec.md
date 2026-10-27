# D-0063 — Spec (T05.11 — COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules MUST-halt Promotion)

**Task:** T05.11
**Roadmap item:** R-103 (COMP-003-M5 rf-qa.md Fix Cycle Protocol Rules — promote SHOULD bullet to MUST-halt)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b2 feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution
**Sub-Agent Delegation:** None
**MCP Requirements:** None; Preferred: Sequential
**Fallback Allowed:** Yes
**Deliverable:** D-0063

---

## 1. Source-of-truth edit map

| File | Pre-edit anchor | Post-edit line | Semantic anchor |
|---|---|---|---|
| `src/superclaude/agents/rf-qa.md` | L335 (drifted from base L312) | L335 | `## QA Phase: Fix Cycle → ### Rules` subsection, second bullet |

**Range adjudication.** The tasklist (phase-5-tasklist.md L499-504) names the literal range `rf-qa.md:308-315`. This range was authored against base commit `fd41178` (`feat(reflect): add Re-scrutiny phase 4 + promote rf agents/skills to src/`). At base, the Fix Cycle `### Rules` subsection occupied lines 309-314:

- L308: blank
- L309: `### Rules`
- L310: blank
- L311: 3-fix-cycle MUST rule (Maximum 3 fix cycles…)
- L312: **target SHOULD bullet** (`Each cycle should have fewer issues…`)
- L313: blank
- L314: `---`

T05.01 (MIG-005 precursor, FR-CONV.5 wrapper) added ~22 lines of Retry Monotonicity Protocol content after the bullet, shifting the SHOULD bullet to current line 335. The SEMANTIC anchor (second bullet under `### Rules` of `## QA Phase: Fix Cycle`) is unchanged; only the absolute line number drifted. The intent-equivalent adjudication pattern is established in D-0061 §5 (T05.09 SKILL.md COMP-001-M5) and D-0062 §3 (T05.10 rf-task-builder.md COMP-002-M5). Both treat literal upper-bound + SEMANTIC anchor as the success criterion for line-drift cases.

## 2. Wire content (new bullet)

The SHOULD bullet (pre-edit):

```
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.
```

is REPLACED by the MUST-halt promotion (post-edit):

```
- Each cycle MUST have strictly fewer issues than the previous one (`|F_{n+1}| < |F_n|` when `|F_n| > 0`). If the count does NOT strictly shrink, the QA agent MUST HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>` — see the Retry Monotonicity Protocol below for the full 4-step precedence (regression → monotonicity → hard-cap → proceed). Non-shrinking issue count is a systemic problem and triggers the FR-CONV.5 monotonicity halt-guard; it is no longer a soft flag.
```

The promotion adds:

1. `MUST` (replacing `should`) — promotes from advisory to invariant.
2. `MUST HALT` — promotes flagging to execution termination.
3. Byte-exact halt-message wire string `[HALT-MONOTONICITY] |F|=<n>` (matches API-004-M5 / D-0055 frozen contract).
4. Mathematical strict-shrink formulation `|F_{n+1}| < |F_n|` with `|F_n| > 0` gating (matches FR-CONV.5 / D-0056 emission spec — the `|F_n|=0` case is not consulted).
5. Forward reference to the Retry Monotonicity Protocol body (current L337-345) for the full 4-step precedence rule `regression → monotonicity → hard-cap → proceed` (D-0058 ordering rule).
6. `FR-CONV.5` cite makes the wrapper governance explicit; the bullet is no longer free-standing advice but a strict component of the convergence wrapper.

## 3. Constraint compliance

| Constraint | Compliance |
|---|---|
| Edit confined to :308-315 (literal) | Edit is at L335 post-edit; the SEMANTIC anchor at base commit was L312 ∈ [308, 315] (intent-equivalent per D-0061 / D-0062 adjudication). |
| Original SHOULD bullet replaced by MUST-halt phrasing | `should` → `MUST` (1×) and `flag this` → `MUST HALT and emit` (1×); both promotions in the same bullet. |
| Byte-exact halt-message string | `[HALT-MONOTONICITY] |F|=<n>` literal reproduced verbatim (matches D-0055/D-0056). |
| No new loop or stage | Bullet references existing Retry Monotonicity Protocol body; no new section/loop introduced. |
| Per-gate counters NOT touched | rf-task-builder.md not modified by T05.11 (preserved at T05.08 / D-0060). |
| `rf-team-lead.md:417` hard cap preserved | rf-team-lead.md not modified by T05.11 (3-cycle hard cap untouched). |
| Four counters preserved | The bullet talks about `|F_n|` for a single fix cycle inside one QA gate; per-gate counters remain independent (T05.08 / D-0060 / R-098). |
| X-003 REJECTED | The bullet enforces STRICT shrink (`< |F_n|`), NOT a rate-of-shrink threshold. `|F|=5,4` (shrink by 1) still passes; X-003 slow-shrink threshold remains REJECTED (R-099). |

## 4. Non-overlap with prior M5 tasks

| Prior task | Scope | Overlap with T05.11 |
|---|---|---|
| T05.01 (D-0054) | FR-CONV.5 wrapper — Retry Monotonicity Protocol body in SKILL.md + rf-task-builder.md + rf-qa.md | rf-qa.md L337-345 (protocol body) is T05.01 content; T05.11 edits L335 (one bullet above the protocol body). No overlap. |
| T05.02 (D-0055) | API-004-M5 byte-exact halt-message strings | T05.11 reproduces the `[HALT-MONOTONICITY]` wire string verbatim per the frozen API-004 contract. No drift. |
| T05.03 (D-0056) | Monotonicity halt-message emitter | T05.11 documents the rule from the consumer side (the QA agent rule book); D-0056 is the producer-side emitter. Complementary. |
| T05.05 (D-0058) | F-set + 4-step ordering rule | T05.11 forward-references the 4-step ordering (`regression → monotonicity → hard-cap → proceed`); does not redefine it. |
| T05.08 (D-0060) | rf-team-lead.md:417 + four counters + X-003 REJECTED preservation | T05.11 does not touch rf-team-lead.md or rf-task-builder.md per-gate counters; all preservation invariants intact. |
| T05.09 (D-0061) | SKILL.md A.9 + Behavioral Constraints | Sibling COMP-edit; same intent-equivalent adjudication pattern. |
| T05.10 (D-0062) | rf-task-builder.md I16 fix-cycle encoding | Sibling COMP-edit; same intent-equivalent adjudication pattern. |

## 5. Sync expectation

Source-of-truth at `src/superclaude/agents/rf-qa.md`. After edit, `make sync-dev` mirrors to `.claude/agents/rf-qa.md`. T05.16 MIG-005 will commit all M5 SKILL.md + rf-task-builder.md + rf-qa.md edits in a single commit.

## 6. Verification plan (executed in D-0063/evidence.md)

| AC (tasklist L533-536) | Check |
|---|---|
| `grep -nE "MUST" src/superclaude/agents/rf-qa.md` returns line in [308, 315] for the halt rule | Direct grep; report line N + SEMANTIC anchor adjudication for line-drift. |
| Original SHOULD bullet replaced by MUST-halt phrasing | Diff inspection: pre `should` → post `MUST`, pre `flag this` → post `MUST HALT and emit`. |
| Edit confined to :308-315 | Edit at L335 (SEMANTIC anchor at base L312 ∈ [308, 315]); intent-equivalent compliance documented. |
| Evidence at D-0063/evidence.md | This artifact set. |

---
