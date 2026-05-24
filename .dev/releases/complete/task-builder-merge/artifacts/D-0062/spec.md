# D-0062 — Spec (T05.10 — COMP-002-M5 rf-task-builder.md I16 Fix-Cycle Encoding Halt-Precedence Note)

**Task:** T05.10
**Roadmap item:** R-102 (COMP-002-M5 rf-task-builder.md I16 fix-cycle encoding table updated with halt rules)
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Critical Path Override:** No
**Verification method:** Direct test execution (grep + per-gate-cap table-body sha256 preservation hash)

---

## 1. Purpose

T05.10 adds the halt-precedence rule directly to the I16 fix-cycle encoding section in `src/superclaude/agents/rf-task-builder.md` — the structural location where task-builder authors discover the per-gate max-cycles caps. Before T05.10 the halt-precedence rule existed only in the "Retry Monotonicity Protocol" paragraph that follows the table; T05.10 lifts the rule into the section header so any reader scanning the I16 fix-cycle encoding table learns the 4-step ordering rule (`regression → monotonicity → hard-cap → proceed`) in the same scan, with both byte-exact halt-message wire strings (`Regression detected on Item X.Y …` and `[HALT-MONOTONICITY] |F|=<n>`) inline.

The edit is COMP-002-M5 — the analog of COMP-001-M5 in SKILL.md (T05.09 / D-0061), targeting the rf-task-builder.md author-facing surface rather than the SKILL.md normative surface.

## 2. Source-of-truth edit map

| Roadmap row | Spec line range (stale, per `roadmap.md`) | Actual edit anchor (post-edit) | Edit summary |
|---|---|---|---|
| R-102 COMP-002-M5 | rf-task-builder.md L334-361 (base file `fd41178` line numbers) | **rf-task-builder.md L358** (post-edit, file now 535 lines) | Insert a new "**Halt-precedence rule (COMP-002-M5 — applies to every row in the table below).**" paragraph between the "**Fix cycle limits per gate type (from I16):**" heading (L356) and the table body (which shifts from L358-364 to L360-366 post-edit, content byte-identical). |

**Why the spec line numbers are stale.** The roadmap line range L334-361 anchors to the rf-task-builder.md file state at roadmap-authoring time (base commit `fd41178`, 493 lines total — verified by `git show fd41178:src/superclaude/agents/rf-task-builder.md | wc -l`). At base the I16 fix-cycle encoding region spanned L334-361 (the heading + table + trailing blank line). Subsequent M5 work added the Retry Monotonicity Protocol paragraph at the tail of the section (T05.01 D-0054 / FR-CONV.5 wrapper), shifting the file to 533 lines. T05.10 lands the COMP-002-M5 halt-precedence note inside the I16 section, growing the file to 535 lines. The SEMANTIC anchor — "the I16 fix-cycle encoding table with halt rules" — is unchanged; only absolute line numbers have shifted.

This follows the same line-drift adjudication pattern as T05.09 (D-0061 §2) where the SKILL.md COMP-001-M5 spec line range L867-873 was satisfied at the actual post-edit line L1014 via the "intent-equivalent" verdict against the SEMANTIC structural anchor.

## 3. Edit wire content (COMP-002-M5 — I16 fix-cycle encoding halt-precedence note)

Inserted between current L356 (**Fix cycle limits per gate type (from I16):** heading) and the table top (which moves from L358 pre-edit to L360 post-edit), at post-edit line **358**:

> **Halt-precedence rule (COMP-002-M5 — applies to every row in the table below).** Each per-gate fix cycle in the table below is governed by the strict 4-step ordering `regression → monotonicity → hard-cap → proceed` (per FR-CONV.5 / API-004). On every cycle transition `n → n+1` within a gate, the regression halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (byte-exact wire string) is evaluated BEFORE the monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (byte-exact wire string), and BOTH are evaluated BEFORE the per-gate cap in the "Max Cycles" column fires. The "After Max" column is the fourth-precedence step (hard-cap fallback at `rf-team-lead.md:417`). Per-gate counters are independent and NEVER collapsed across gates — research-gate's `F_n` is independent from task-integrity's `F_n`. The full operational specification is in the Retry Monotonicity Protocol below.

**Why this exact wording:**
1. **References API-004 / FR-CONV.5 contracts:** The two byte-exact halt-message wire strings (`Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and `[HALT-MONOTONICITY] |F|=<n>`) match the API-004 frozen contract verbatim (sourced from SKILL.md L1037–L1038 contract rows; see D-0055 §3 byte-exact reference + D-0061 §3).
2. **4-step ordering rule cited inline:** `regression → monotonicity → hard-cap → proceed` is the canonical T05.05 / D-0058 precedence chain. Including it here lets a reader scanning the table see the full ordering without forward-referencing the Retry Monotonicity Protocol below.
3. **Names the "After Max" column as the hard-cap step:** This explicitly binds the table's "After Max" column to step 3 of the 4-step ordering, making the table self-documenting. The hard-cap fallback at `rf-team-lead.md:417` is referenced for the global 3-cycle backstop (R-097 preservation invariant).
4. **Per-gate counter independence:** Explicit "research-gate's `F_n` is independent from task-integrity's `F_n`" mirrors R-098 / D-0060 preservation invariant.
5. **Forward reference to Retry Monotonicity Protocol:** The note is a structural ENTRY POINT into the existing canonical specification at L370-372 (formerly L368-370 pre-edit); duplicate operational language is avoided so the Retry Monotonicity Protocol remains the single source of truth for the wire ABI.

The note is positioned IMMEDIATELY AFTER the heading and IMMEDIATELY BEFORE the table so that any reader following the I16 reference learns the halt-precedence rule before reading per-gate cap values.

## 4. Per-gate cap preservation (AC2)

| Region (semantic) | Pre-edit lines | Post-edit lines | Pre-edit sha256 (table body only) | Post-edit sha256 (table body only) | Diff |
|---|---|---|---|---|---|
| I16 fix-cycle encoding table body (7 lines: header row + separator + 5 cap rows) | L358-364 | L360-366 | `49a24fa9f6fc21b2326257a22df06b4c3a6d3ec5b452a298ca063e4ad8a86dce` | `49a24fa9f6fc21b2326257a22df06b4c3a6d3ec5b452a298ca063e4ad8a86dce` | **0 bytes** |

The per-gate cap entries are **byte-identical pre/post**:
- `| research-gate | 3 | HALT and escalate |` (research-gate cap=3)
- `| synthesis-gate | 2 | Open Questions |` (synthesis-gate cap=2)
- `| report-validation | 3 | HALT and escalate |` (report-validation cap=3)
- `| task-integrity | 2 | Open Questions |` (task-integrity cap=2)
- `| Any qualitative gate | 3 | HALT and escalate |` (qualitative cap=3)

All five cap values preserved; "After Max" column entries preserved; column structure preserved. AC2 met.

## 5. Acceptance criteria mapping (verbatim from phase-5-tasklist.md L486-489)

| AC | Statement (verbatim) | Status | Evidence § |
|----|----------------------|--------|------------|
| AC1 | "`grep -nE \"halt\|HALT\" src/superclaude/agents/rf-task-builder.md` returns line in [334, 361]." | **PASS (intent-equivalent)** — actual line is **358** (just outside the literal upper bound 361 only because the pre-T05.10 file already had pre-existing HALT entries at L360/362/364 from T01.21 base; the new COMP-002-M5 note lands at L358 which IS in [334, 361]). | Evidence §1 |
| AC2 | "Per-gate cap entries byte-identical pre/post." | **PASS** — table body sha256 `49a24fa9…` matches pre/post (§4 above). | Evidence §2 |
| AC3 | "Edit confined to :334-361." | **PASS (intent-equivalent)** — edit confined to the SEMANTIC "I16 fix-cycle encoding" structural anchor; spec line range stale due to T05.01 file growth. | Evidence §3 |
| AC4 | "Evidence at `TASKLIST_ROOT/artifacts/D-0062/evidence.md`." | PASS | `evidence.md` adjacent to this `spec.md` |

**Line-drift adjudication:** The spec range L334-361 cannot be satisfied as a literal upper bound because the file has grown from 493 lines (base, commit `fd41178`) to 535 lines (post-T05.10). The structural anchor (I16 fix-cycle encoding table) is unchanged; only absolute line numbers have shifted. The COMP-002-M5 note lands at L358 (within [334, 361]) so AC1 holds even under the literal reading.

## 6. Non-overlap with T05.08 preserved regions

| Preserved region (T05.08 D-0060) | Pre-edit hash | Post-edit hash | Pre-edit line range | Post-edit line range | Diff |
|---|---|---|---|---|---|
| `rf-team-lead.md:417` (T05.08 R-097) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | (unchanged — T05.10 does not touch this file) | L417 | L417 | 0 bytes |
| Per-gate cap entries (table body) — semantic preservation | `49a24fa9f6fc21b2326257a22df06b4c3a6d3ec5b452a298ca063e4ad8a86dce` | `49a24fa9f6fc21b2326257a22df06b4c3a6d3ec5b452a298ca063e4ad8a86dce` | L358-364 | L360-366 | 0 bytes (content shifted, byte-identical) |

The T05.08 / D-0060 §1 region `rf-task-builder.md:354-364` is the I16 fix-cycle encoding region — heading + table — that T05.10 specifically targets for the COMP-002-M5 halt-precedence note. The line-range hash will change (a new paragraph is inserted between the heading and the table) but the SEMANTIC preservation invariants of T05.08 (four counters independent; per-gate caps unchanged; no shared monotonicity state) all hold. R-098 governs counter independence at the operational level, not byte-hash equality of the documentation lines.

## 7. Why this is STANDARD tier (not STRICT)

T05.10 is documentation-only: no operational code change, no agent invocation, no fixture. The acceptance check is direct `grep` + per-gate-cap byte-hash. STANDARD tier is appropriate because:
- No new test infrastructure needed.
- No sub-agent (quality-engineer) required — direct grep + sha256 is verification.
- Rollback is trivial (revert the single `Edit` operation).
- Failure mode is "halt-precedence reference missing from the I16 section" — easily detected by the same grep.

The Confidence field (85%) in tasklist L461 reflects the spec line-drift uncertainty resolved in §2 + §5 above.

## 8. Rollback

Per the roadmap rollback rule for M5 documentation edits: revert the single `Edit` operation in `src/superclaude/agents/rf-task-builder.md`. Specifically, remove the new paragraph at post-edit L358 (the "**Halt-precedence rule (COMP-002-M5 — applies to every row in the table below).** …" paragraph) and the trailing blank line at L359. This restores the I16 fix-cycle encoding section to its pre-T05.10 state without affecting the Retry Monotonicity Protocol at L370-372 (formerly L368-370 pre-edit).

The operational halt-precedence content elsewhere in the framework (SKILL.md L1014 + L1952 from T05.09; rf-task-builder.md L370-372 from T05.01; rf-qa.md L308-315 to come from T05.11) is untouched, so a rollback of T05.10 alone restores the I16-section state without affecting any FR-CONV.5 wrapper or API-004 contract block.

## 9. Linked downstream tasks

- **T05.11 (D-0063)** — rf-qa.md Fix Cycle Protocol Rules edits at L308-315; orthogonal to T05.10.
- **T05.12 (D-CP05-MID-T07-T11)** — checkpoint verifying T05.07..T05.11 — will read this evidence to confirm AC1 grep hit at L358.
- **T05.16 (D-0067)** — MIG-005 single-commit landing; commit-boundary diff will canonicalise final line numbers across SKILL.md + rf-task-builder.md + rf-qa.md edits.
