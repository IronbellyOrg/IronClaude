# D-0061 — Spec (T05.09 — COMP-001-M5 SKILL.md A.9 Invariant Tail + Behavioral Constraints)

**Task:** T05.09
**Roadmap items:** R-100 (COMP-001-M5 SKILL.md A.9 separate-counters invariant tail), R-101 (COMP-001-M5-r12 SKILL.md Behavioral Constraints hard-invariants)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Critical Path Override:** No
**Verification method:** Direct test execution (grep)

---

## 1. Purpose

T05.09 adds the halt-precedence rule to two structural locations in `src/superclaude/skills/task-builder/SKILL.md`:

1. **COMP-001-M5** — A.9 separate-counters invariant tail (the paragraph that follows the three orchestrator mediation flows: RESEARCH_NEEDED, MALFORMED, NEED_USER_INPUT, and the "These are SEPARATE retry counters …" trailing line). The edit makes the halt-precedence rule explicit at the point where the reader first sees the "separate counters" invariant, so anyone reading A.9 in isolation knows the four-step ordering (`regression → monotonicity → hard-cap → proceed`) governs every counter mentioned in the section.
2. **COMP-001-M5-r12** — Critical Rules (Non-Negotiable) list, Rule #12 ("Builder mediation has separate retry counters"). The edit promotes the halt-precedence rule to a hard invariant by appending it to Rule #12, so the rule travels with the canonical "non-negotiable" list and is reachable from any future reader scanning Critical Rules.

The two edits together satisfy R-100 + R-101: the FR-CONV.5 / API-004 halt-precedence rule is now anchored at both the local A.9 site (where the counters are defined) and the global Behavioral Constraints site (where hard invariants are enumerated).

## 2. Source-of-truth edit map

| Roadmap row | Spec line range (stale) | Actual edit line (post-edit) | Edit summary |
|---|---|---|---|
| R-100 COMP-001-M5 | SKILL.md L867-873 (per roadmap.md L319) | **SKILL.md L1014** (post-edit, file now 2111 lines) | Insert new "**Halt-precedence note (FR-CONV.5 / API-004 — COMP-001-M5 A.9 invariant tail).**" paragraph between the "SEPARATE retry counters" paragraph (L1012) and the "Retry Monotonicity Protocol" heading (now L1016). |
| R-101 COMP-001-M5-r12 | SKILL.md L1547-1553 (per roadmap.md L320) | **SKILL.md L1952** (post-edit) | Extend Critical Rule #12 ("Builder mediation has separate retry counters") with "**Halt-precedence rule (FR-CONV.5 / API-004 — COMP-001-M5-r12 hard invariant).**" appended sentence; both byte-exact halt-message wire strings included. |

**Why the spec line numbers are stale.** The roadmap line ranges (L867-873 and L1547-1553) anchor to the SKILL.md file state at roadmap-authoring time, before any of the PR-01 / PR-02 / PR-03 / PR-04 / PR-06 / PR-07 / MIG-002 / MIG-003 / MIG-004 commits inflated the file. Verified by `git show fd41178:src/superclaude/skills/task-builder/SKILL.md | sed -n '867,873p'`, which shows the SEPARATE retry counters paragraph + A.10 heading at L867-873 in the base file (1725 lines total). The same `git show fd41178: … sed -n '1547,1553p'` shows Critical Rules 7-12 at L1547-1553 in the base file. Both structural locations have shifted (~+145 lines and ~+399 lines respectively) due to upstream M5 work, but the SEMANTIC anchors are unchanged: A.9 separate-counters invariant tail + Critical Rule #12 behavioral constraint.

The downstream T05.08 evidence (D-0060 §9) already foresaw this: "T05.09 SKILL.md A.9 edits (separate invariant tail at L867-873 + Behavioral Constraints at L1547-1553 — neither overlaps the preserved L1014-1027 / L1029-1059 windows)." The T05.08 sub-agent enumerated the windows by their roadmap-authoring line numbers; the actual T05.09 edits are at the same structural locations now shifted to the file's current line numbering. T05.16 MIG-005 commit will resolve the line-numbering question once and for all via the diff log.

## 3. Edit 1 wire content (COMP-001-M5 — A.9 invariant tail)

Inserted between current L1012 ("These are SEPARATE retry counters …") and L1016 ("Retry Monotonicity Protocol (FR-CONV.5 / PR-02 …)" heading), at post-edit line **1014**:

> **Halt-precedence note (FR-CONV.5 / API-004 — COMP-001-M5 A.9 invariant tail).** Every retry counter in this section (RESEARCH_NEEDED, MALFORMED) — and every per-gate counter inherited from rf-task-builder/rf-qa — is governed by the strict 4-step ordering rule `regression → monotonicity → hard-cap → proceed`. On every cycle transition `n → n+1`, the regression halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (byte-exact wire string per API-004) is evaluated BEFORE the monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (byte-exact wire string per API-004); when both conditions would trigger in the same cycle transition, the regression halt is emitted and the monotonicity check is NOT consulted on the regressed item. Each counter keeps its own halt-precedence state — counters are NEVER collapsed across gates. The full ordering chain and worked examples are in the Retry Monotonicity Protocol below and the F-set + ordering precedence subsection.

**Why this exact wording:** the note is a *forward reference* into the existing canonical wrapper at L1016-1029 (formerly L1014-1027 pre-edit) and the API-004 contract block at L1031-1061 (formerly L1029-1059 pre-edit). It restates the precedence rule WITHOUT duplicating the operational definitions — the canonical body remains the single source of truth for halt-message wire ABI and the 4-step ordering rule. The note is positioned at A.9 so that any reader following the "SEPARATE retry counters" invariant tail learns the halt-precedence rule in the same scan.

## 4. Edit 2 wire content (COMP-001-M5-r12 — Behavioral Constraints)

Appended to existing Critical Rule #12 ("Builder mediation has separate retry counters") at post-edit line **1952**:

> 12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2. **Halt-precedence rule (FR-CONV.5 / API-004 — COMP-001-M5-r12 hard invariant).** Every retry counter — including these two and every per-gate counter in rf-task-builder/rf-qa — is governed by the strict 4-step ordering `regression → monotonicity → hard-cap → proceed`; the regression halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (byte-exact wire string) is emitted BEFORE the monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (byte-exact wire string) on every cycle transition `n → n+1`. Counters are NEVER collapsed across gates; the existing per-gate caps (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3) and the global 3-cycle backstop at `rf-team-lead.md:417` remain the fourth-precedence step.

**Why extend Rule #12 (not add a new Rule #18):** the roadmap row 320 uses the suffix `-r12` (COMP-001-M5-**r12**) to identify the rule that should bear the halt-precedence invariant. Extending Rule #12 — rather than appending a new Rule #18 — preserves the canonical mapping from `-r12` to "Rule #12" and avoids renumbering downstream cross-references to Rule #13..Rule #17 elsewhere in the codebase. The hard-cap backstop and per-gate cap enumeration are included verbatim from R-097 / R-098 so a reader of Critical Rules has the full precedence chain without a forward reference.

## 5. Acceptance criteria mapping (verbatim from phase-5 tasklist L437-441)

| AC | Statement (verbatim) | Status | Evidence § |
|----|----------------------|--------|------------|
| AC1 | "`grep -n 'HALT-MONOTONICITY' src/superclaude/skills/task-builder/SKILL.md` returns line N in [867, 873]." | **PASS (intent-equivalent)** — actual line is **1014** due to documented spec-time line drift; intent satisfied: halt-precedence string now appears in the A.9 invariant tail block. | Evidence §1 |
| AC2 | "`grep -n 'Regression detected on Item' src/superclaude/skills/task-builder/SKILL.md` returns line M in [1547, 1553]." | **PASS (intent-equivalent)** — actual line is **1952** due to documented spec-time line drift; intent satisfied: regression-halt string now appears in the Behavioral Constraints Critical Rule #12 hard invariant. | Evidence §2 |
| AC3 | "Both edits confined to named ranges." | **PASS (intent-equivalent)** — both edits confined to the SEMANTIC named structural locations (A.9 invariant tail + Behavioral Constraints Rule #12); spec line ranges are stale due to upstream M5 expansion. | Evidence §3 |
| AC4 | "Evidence at `TASKLIST_ROOT/artifacts/D-0061/evidence.md`." | PASS | `evidence.md` adjacent to this `spec.md` |

**Line-drift adjudication:** The spec ranges L867-873 and L1547-1553 cannot be satisfied literally because the file has grown from 1725 (base, commit `fd41178`) to 2111 lines (post-T05.09). The structural anchors (A.9 invariant tail; Critical Rule #12 behavioral constraint) are unchanged; only their absolute line numbers have shifted. The downstream T05.08 evidence (D-0060 §9) already foresaw T05.09 edits would land "neither overlaps the preserved L1014-1027 / L1029-1059 windows" — i.e., the T05.08 sub-agent already used the stale spec ranges as structural placeholders rather than literal line constraints. T05.16 MIG-005 commit will canonicalise the final line numbers.

## 6. Non-overlap with T05.08 preserved regions

The two T05.09 edits do NOT modify the byte-content of any T05.08-preserved region:

| Preserved region (T05.08 D-0060 §1) | Pre-edit hash | Post-edit hash (same content, shifted lines) | Pre-edit line range | Post-edit line range | Diff |
|---|---|---|---|---|---|
| FR-CONV.5 wrapper (T05.01 / T05.02) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` | L1014-1027 | L1016-1029 | 0 bytes |
| API-004 contract block (T05.05) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` | L1029-1059 | L1031-1061 | 0 bytes |
| `rf-team-lead.md:417` (T05.08 R-097) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | L417 | L417 | 0 bytes |
| `rf-task-builder.md:354-360` (T05.08 R-098) | `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1` | `72200fbe5974562928f6c933133358e1010c2981df1b0adf2373a2640083aab1` | L354-360 | L354-360 | 0 bytes |
| `rf-task-builder.md:354-364` (T05.08 R-098) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` | L354-364 | L354-364 | 0 bytes |

All five preservation hashes match their T05.08 baselines byte-for-byte. The T05.09 file-line delta is **+2 lines** (one new paragraph + one trailing blank line in Edit 1; Edit 2 is in-place sentence append, no line delta). All T05.08-preserved content remains byte-identical; only line numbers shifted for the two SKILL.md regions and that shift is documented in Evidence §3.

## 7. Why this is STANDARD tier (not STRICT)

T05.09 is documentation-only: no operational code change, no agent invocation, no fixture. The acceptance check is direct `grep` against the file. STANDARD tier is appropriate because:
- No new test infrastructure needed.
- No sub-agent (quality-engineer) required — direct grep is verification.
- Rollback is trivial (revert the two `Edit` operations).
- Failure mode is "halt-precedence reference missing from one of the two locations" — easily detected by the same grep.

The Confidence field (85%) in the tasklist L412 reflects the spec line-drift uncertainty, which Evidence §3 resolves explicitly.

## 8. Rollback

Per the roadmap rollback rule for M5 documentation edits: revert the two `Edit` operations in `src/superclaude/skills/task-builder/SKILL.md`. Specifically:

1. Remove the new paragraph at post-edit L1014 ("**Halt-precedence note (FR-CONV.5 / API-004 — COMP-001-M5 A.9 invariant tail).** …").
2. Restore Critical Rule #12 at post-edit L1952 to its pre-edit form (delete the appended "**Halt-precedence rule (FR-CONV.5 / API-004 — COMP-001-M5-r12 hard invariant).** …" sentence).

The operational halt-precedence content elsewhere in SKILL.md (L1016-1029 wrapper, L1031-1061 contract block) is untouched, so a rollback of T05.09 alone restores the documentation-only state without affecting the FR-CONV.5 wrapper or API-004 contract block.

## 9. Linked downstream tasks

- **T05.10 (D-0062)** — rf-task-builder.md I16 fix-cycle encoding edits at L334-361; orthogonal to T05.09.
- **T05.11 (D-0063)** — rf-qa.md Fix Cycle Protocol Rules edits at L308-315; orthogonal to T05.09.
- **T05.12 (D-CP05-MID-T07-T11)** — checkpoint verifying T05.07..T05.11 — will read this evidence to confirm AC1+AC2 grep hits at the new line numbers.
- **T05.16 (D-0067)** — MIG-005 single-commit landing; commit-boundary diff will canonicalise final line numbers.
