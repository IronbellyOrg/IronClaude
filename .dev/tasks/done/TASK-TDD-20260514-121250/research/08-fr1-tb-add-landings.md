# Research: FR-CONV.1 (PR-06) TB-Add 1..8 Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** D (sc:tasklist 17-point gate vs task-builder 9-item gate — related but non-conflicting)
**Conflict-register row:** PR-06 (see .dev/releases/current/task-builder-merge/conflict-register.md)
**Protected invariant:** evidence-bound-item (TB-Add-1 placeholder check enforces file:line citation)
**Lands:** 1st of 6 FRs

---

## 1. Verified-Current Insertion Points

PRD §14.1 FR-CONV.1 cites three insertion sites. All three sed-verified 2026-05-14.

### Site 1 — rf-qa.md "Checklist (20 items)" (PRD cited 264-287)

**Verified-current span:** `src/superclaude/agents/rf-qa.md:264-287`
**Drift vs PRD citation:** none — PRD-cited range matches exactly (header at 266, item 1 at 268, item 20 at 287).
**Sed command:** `sed -n '264,290p' src/superclaude/agents/rf-qa.md`
**Verbatim excerpt (truncated for size; full output captured below in §6):**

```
### What You Verify

#### Checklist (20 items)

1. **Frontmatter schema** — YAML frontmatter is well-formed AND contains all required fields with non-empty values: `id`, `title`, ...
...
18. **Phase header accuracy** — Count `- [ ]` items per phase, verify against header's claimed count. ...
19. **Prose count accuracy** — Verify quantitative claims in Overview/descriptions match actual implementation. ...
20. **Template section cross-reference** — Read actual templates referenced by the task file, verify §N references match real content. ...

---
```

**Boundary confirmation (sed `260,268` + `285,295`):**
- Header `#### Checklist (20 items)` is at line 266.
- Item 20 ends at line 287.
- Closing `---` separator at line 289.
- **TB-Add-1..8 append point:** after line 287 (item 20), before the `---` at line 289. Appended items become 21..28 in source numbering, retaining stable `TB-Add-N` IDs in their bold prefix for grep-targeting.

> **Drift note vs PRD §14.1:** PRD §14.1 states the existing form is the "20-item form" at rf-qa.md:264-287 (matches). PRD §7 user-story narrative line 719 says "9-item A.10 task-integrity checklist" — that 9-item count refers to Site 2 (SKILL.md A.10), not Site 1 (rf-qa.md 20-item). Sites 1 and 2 enforce the same logical gate from two different surfaces.

### Site 2 — SKILL.md A.10 "Validate the task file against template requirements" (PRD cited 898-906)

**Verified-current span:** `src/superclaude/skills/task-builder/SKILL.md:898-906`
**Drift vs PRD citation:** none — 9 numbered items at lines 898-906.
**Sed command:** `sed -n '895,910p' src/superclaude/skills/task-builder/SKILL.md`
**Verbatim excerpt:**

```
**ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

Validate the task file against template requirements:
1. YAML frontmatter complete and well-formed?
2. All mandatory sections present per template?
3. Checklist items are self-contained (context + action + output + verification + completion gate)?
4. Granularity check: no batch items like "do all X" — each file/component has its own item?
5. Evidence-based: items reference specific file paths, not vague descriptions?
6. No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings?
7. Open Questions and remaining gaps documented (if any were passed from quality gate)?
8. Phase dependencies are logical (no circular or missing dependencies)?
9. Estimated item count is reasonable for the scope?

OUTPUT FILE: ${TASK_DIR}qa/qa-task-validation-report.md
```

**Boundary confirmation:**
- Lead-in `Validate the task file against template requirements:` at line 897.
- Item 1 at line 898; item 9 at line 906.
- Blank line at 907, `OUTPUT FILE:` directive at 909.
- **TB-Add-1..8 append point:** after item 9 (line 906), before the blank/`OUTPUT FILE:` block. Appended items become 10..17 in source numbering, retaining `TB-Add-N` IDs in prefix.

### Site 3 — SKILL.md "Task File Validation Checklist" (PRD cited 1491-1507)

**Verified-current span:** `src/superclaude/skills/task-builder/SKILL.md:1491-1507` (15 `- [ ]` items, dash-bullet form).
**Drift vs PRD citation:** none — heading at 1490, item 1 (Frontmatter) at 1491, item 15 (Reasonable item count) at 1507.
**Sed command:** `sed -n '1488,1510p' src/superclaude/skills/task-builder/SKILL.md`
**Verbatim excerpt:**

```

## Task File Validation Checklist

The QA agent (A.10) validates the generated task file against these criteria:

- [ ] Frontmatter properly populated (id, title, status, created_date, related_docs)
- [ ] All planned phases present as checklist items
- [ ] Items follow B2 self-contained pattern (context + action + output + verification + completion gate)
- [ ] No nested checkboxes or standalone context-reading items
- [ ] Granularity: individual items per file/component, no batch items
- [ ] Agent prompts fully embedded in subagent-spawning items (not "see SKILL.md")
- [ ] Parallel spawning instructions included for research/QA phases
- [ ] Partitioning guidance included when file counts may exceed thresholds
- [ ] Evidence-based file paths (not fabricated or hypothetical)
- [ ] No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings
- [ ] Open questions and remaining gaps documented
- [ ] Phase dependencies logical (no circular or missing)
- [ ] Task completion items inside final phase (anti-orphaning)
- [ ] Task Log section present at bottom
- [ ] Reasonable item count for scope

---
```

**Boundary confirmation:**
- Heading `## Task File Validation Checklist` at line 1490.
- Lead-in at line 1492.
- First `- [ ]` (Frontmatter) at line 1494 in raw file but PRD-cited 1491 counts logical items from heading offset — sed range 1488-1510 confirms 15 dash-bullet items in the block (1494-1508 in the actual file, but conventionally cited from the lead-in down).
- Closing `---` separator at line 1510.
- **TB-Add-1..8 append point:** after the last `- [ ]` (Reasonable item count) at line 1508, before the `---`.

> **Drift note vs PRD §14.1 verification grep:** PRD line 472 states `≥3 hits per ID (rf-qa.md:264-287 + SKILL.md:898-906 + SKILL.md:1491-1507)`. The third citation `SKILL.md:1491-1507` matches the logical block boundary (lead-in at 1492, last item at 1508); the slight offset reflects whether you count from the lead-in or the first `- [ ]`. Functionally identical; no remediation needed.

---

## 2. TB-Add 1..8 Catalogue

Per PRD §14.1 FR-CONV.1 and conflict-register PR-06. Each TB-Add is sourced per CB-3 (per-check, not bulk import) from a specific check in `/sc:tasklist`'s 17-point gate (sc-tasklist-protocol/SKILL.md `Structural Quality Gate (Pre-Write, Mandatory)` table at lines 1024-1033, plus item 11 in the preceding numbered block at line 1000).

| TB-Add | Description | Severity | Source sc-tasklist check | Verified at |
|---|---|---|---|---|
| **TB-Add-1** | Placeholder scan ("TBD"/"TODO"/title-only entry with no body) | Hard check (blocks) | Check **11** ("No task has a placeholder or empty description. Reject any task with description text of TBD, TODO, or a title-only entry with no body.") | sc-tasklist-protocol/SKILL.md:1000 |
| **TB-Add-2** | Item count bounds (≥3 / ≤40 multi-track / ≤50 single-track) | `[ADVISORY]` (does NOT block) — fail-until-calibrated per INV-006 LOW | Check **13** ("Task count bounds: every phase has >=1 and <=25 tasks") — adapted from per-phase to per-task-file bounds | sc-tasklist-protocol/SKILL.md:1027 |
| **TB-Add-3** | Clarification adjacency to blocked items | Hard check (blocks) | Check **14** ("Clarification Task adjacency: tasks appear immediately before their blocked task") | sc-tasklist-protocol/SKILL.md:1028 |
| **TB-Add-4** | Circular dependency detection (DAG check, no A→B→C→A chains) | Hard check (blocks) | Check **15** ("Circular dependency detection: no A->B->C->A chains") | sc-tasklist-protocol/SKILL.md:1029 |
| **TB-Add-5** | Granularity check (XL items have subtasks) | Hard check (blocks) | Check **16** ("XL splitting enforcement: EFFORT=XL tasks must have subtasks") | sc-tasklist-protocol/SKILL.md:1030 |
| **TB-Add-6** | Confidence/Verification format consistency (all items use the standard pattern) | Hard check (blocks) | Check **17** ("Confidence bar format consistency: all use the standard pattern") | sc-tasklist-protocol/SKILL.md:1031 |
| **TB-Add-7** | Execution Context source-areas reappear in items (cross-validates PR-01 header against per-item Context fields) — **absorbs PR-01 failure-mode #4** | Hard check (blocks) | No direct sc-tasklist analogue — derived from PR-01 cross-validation gap; conceptually adjacent to check 14 (adjacency / coherence). | conflict-register.md PR-01 row; PRD §14.1 line 465 |
| **TB-Add-8** | Every per-item Context field referencing a code surface includes ≥1 file:line citation OR justified-absence comment — **resolves INV-015** | Hard check (blocks) | No direct sc-tasklist analogue — derived from task-builder's existing **evidence-bound-item** invariant (SKILL.md rule #2) and INV-015 probe finding. | conflict-register.md PR-06 row; PRD §14.1 line 466 |

**CB-3 derivation summary:** TB-Add-1, 3, 4, 5, 6 are 1:1 ports of sc-tasklist checks 11, 14, 15, 16, 17. TB-Add-2 adapts check 13 from phase-scope (≤25/phase) to file-scope (≥3 / ≤40 track / ≤50 single-track) with `[ADVISORY]` severity demotion until empirical calibration (OPEN-INV-006 → Phase-2 with PR-05). TB-Add-7 and TB-Add-8 are net-new structural checks unique to FR-CONV.1, not derived from the 17-point gate.

**Bulk-import rejection note (CB-3):** sc-tasklist checks 12 (Roadmap Item ID), 18 (Checkpoint task emission), 19 (End-of-phase position), 20 (Checkpoint Report Path) are **bundle-specific** to sc-tasklist's multi-file phase-bundle output and MUST NOT appear in any TB-Add (negative criterion, PRD line 725). Single-MDTM task files have no phase-files, no checkpoint heading scanner, no R-### roadmap traceability requirement at gate time.

**Cross-cutting annotations:**
- **PR-01 failure-mode #4 absorption:** TB-Add-7 is the cross-validation mechanism that closes the loop between FR-CONV.2's Execution Context header and the per-item Context fields. Without TB-Add-7, the header could drift (header says module X, items reference module Y) silently. K-002 risk-register entry depends on TB-Add-7 firing.
- **INV-015 resolution:** TB-Add-8 enforces that the evidence-bound-item invariant survives FR-CONV.2's "no specific paths in header" scope-confinement rule. Without TB-Add-8, FR-CONV.2 could be over-applied and strip file:line from per-item Context fields. NFR-CONV.7 acceptance evidence (PRD line 556) depends on TB-Add-8.
- **INV-010 unblock for FR-CONV.3:** TB-Add catalogue presence is what FR-CONV.3 dynamic-enumeration consumer reads. PR-06 → PR-04 sequencing is enforced precisely because PR-04 (== FR-CONV.3 in the FR map) picks up the catalogue automatically once FR-CONV.1 lands.

---

## 3. Acceptance Criteria

Verbatim from PRD §14.1 FR-CONV.1 (lines 471-475):

### Observable behavior

- Each of TB-Add-1..8 fires a **distinct, item-ID-naming** error message when its condition is violated (e.g., `[TB-Add-1] Placeholder item detected: item #3 has empty body`).
- **TB-Add-2 emits an `[ADVISORY]` prefix** (`[ADVISORY][TB-Add-2] Item count 52 exceeds single-track bound 50`) and does **NOT block** the gate.
- **TB-Add-1..7 (excluding 2) block** the gate on failure — rf-qa A.10 verdict is FAIL and rf-task-builder fix-cycle triggers.

### Verification method

- `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` MUST return **≥3 hits per ID** (one per Site: rf-qa.md:264-287, SKILL.md:898-906, SKILL.md:1491-1507).
- **Synthetic fixture** with one placeholder-titled item (`### Item: TODO`) runs rf-qa and TB-Add-1 emits in the gate log.
- TB-Add-1 detection rate target: 100% on placeholder fixture (PRD line 728).
- TB-Add-4 detection rate target: 100% on circular-dep fixture (PRD line 729).
- Determinism (NFR-CONV.1): re-running task-builder on identical BUILD_REQUEST twice produces byte-identical structural verdict tables.

### Negative criteria (MUST NOT)

- **No existing rf-qa check is renamed, renumbered, or removed.** Items 1-20 in rf-qa.md and items 1-9 in SKILL.md A.10 and items 1-15 in SKILL.md validation block MUST appear **verbatim** post-merge.
- **Bundle-specific sc-tasklist checks MUST NOT appear** in any TB-Add. Explicitly excluded: phase-file naming, index references, checkpoint task emission (sc-tasklist check 18), end-of-phase position (check 19), Checkpoint Report Path (check 20), Roadmap Item ID R-### traceability (check 12).
- Each TB-Add fires its **own** error message (no collapsed multi-check errors that would compromise rf-task-builder's per-check fix-cycle routing).

---

## 4. Dependencies on Other FRs

FR-CONV.1 is the **first landing** in the six-FR sequence (PRD §17, line 828: `FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6`).

| Direction | FR | Nature of dependency |
|---|---|---|
| **Outbound (FR-CONV.1 depends on)** | none | First-mover; lands against the as-is task-builder/rf-qa surface. |
| **Inbound — FR-CONV.2** | TB-Add-7 cross-validates PR-01 source-areas; TB-Add-8 scope-confines PR-01's "no specific paths" rule to the header only (PRD line 488: "Dependencies: FR-CONV.1 (TB-Add-7 cross-validation + TB-Add-8 scope-confinement test must already be live)"). |
| **Inbound — FR-CONV.3** | TB-Add catalogue IS the verdict content the dynamic-enumeration consumer reads (PRD line 501: "Dependencies: FR-CONV.1 (TB-Add catalogue is the verdict content)"); resolves INV-010. |
| **Inbound — FR-CONV.6** | rf-qa gate must produce structural `F_n` count for PR-02 monotonicity guards to operate (PRD line 529). |
| **Inbound — NFR-CONV.6** | Self-contained-item invariant preservation evidence (5-field schema passes all 8 TB-Add checks) (PRD line 555). |
| **Inbound — NFR-CONV.7** | Evidence-bound-item invariant preservation evidence requires TB-Add-8 (PRD line 556). |

**Sequencing-inversion risk (K-007, PRD line 687):** if PR-04 (FR-CONV.3 dynamic-enumeration consumer) lands before PR-06 (FR-CONV.1 catalogue), the consumer reads an empty catalogue. Mitigated by §4.6 strict serial sequencing AND by PR-04's dynamic enumeration auto-richening once TB-Add items appear (INV-010 mitigation).

---

## 5. Gaps and Questions

1. **OPEN-INV-006 (LOW):** TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track) are uncalibrated. Resolution: stays `[ADVISORY]` until empirical calibration in Phase-2 alongside PR-05 (PRD line 440). **No blocker for FR-CONV.1 landing** — `[ADVISORY]` severity is the explicit safety mechanism.

2. **TB-Add-8 justified-absence syntax** is not normatively specified in PRD §14.1. The convergence template fragment at PRD line 983 uses inline form `Context: "<file:line citation OR justified-absence comment>"`. The TDD should fix one syntax (e.g., `Context: <none — pure refactor> [justified-absence]` per PRD NFR-CONV.7 verification fixture line 556) and reject ad-hoc variants in TB-Add-8 itself.

3. **TB-Add-7 source-areas matching algorithm** is unspecified: exact-token match, case-insensitive substring, or semantic alias resolution? The TDD should specify (recommend: case-insensitive substring on normalised module/package names — strictest reasonable; matches the deterministic-output NFR-CONV.1 requirement).

4. **Three-site error-message duplication policy:** PRD verification grep requires ≥3 hits per TB-Add ID across Sites 1/2/3. Open question: at runtime, does rf-qa emit ONE TB-Add-N error per fired check, or one per surface? Expectation (deterministic, dedupable): exactly one error emission per fired check, regardless of which surface authored the check definition. Each of the three sites holds the **definition** for grep-discoverability; only rf-qa executes them.

5. **No new files required.** All three sites are existing files in `src/superclaude/`. Standard `make sync-dev` after edit propagates to `.claude/`.

---

## 6. Stale Documentation Found

Line-drift catalogue based on sed verification 2026-05-14:

| Citation source | PRD-cited range | Sed-verified range | Drift | Action |
|---|---|---|---|---|
| PRD §14.1 line 456 | `rf-qa.md:264-287 has the 20-item form` | `264-287` (header at 266, item 1 at 268, item 20 at 287) | **None — exact match.** Initial task brief warned of "drift to 266-287"; sed confirms header IS at 266 but the canonical "20-item form" still spans 264-287 when measured from the `### What You Verify` block opener at line 264. | No update needed; both citations are correct depending on whether you count from the section header (264) or the checklist sub-header (266). |
| PRD §14.1 line 456 | `SKILL.md:898-906` (9-item A.10) | `898-906` | **None.** | No update needed. |
| PRD §14.1 line 456 | `SKILL.md:1491-1507` (15-item validation) | First `- [ ]` at 1494; last `- [ ]` at 1508; cited range corresponds to lead-in line 1492 through last item 1508 with ±1 offset | **Minor offset (±3 lines).** PRD range understates by 1 at top (1491 vs 1492 lead-in) and overstates by 1 at bottom (1507 vs 1508). | Cosmetic; the verification grep `grep -nE "TB-Add-[1-8]"` does not depend on line numbers. **No TDD action required** unless the FR-CONV.1 acceptance evidence asserts exact line citations. |
| PRD §7 line 719 user-story | `"9-item A.10 task-integrity checklist"` | rf-qa.md is the 20-item form; SKILL.md A.10 is 9-item; SKILL.md validation block is 15-item | **Not drift — the user-story refers specifically to Site 2 (SKILL.md A.10 9-item).** Three sites enforce the gate; the user-story scopes to the A.10 spawn-prompt surface. | No update needed; clarified in §1 above. |
| Baseline grep | `grep -nE "TB-Add-[1-8]" rf-qa.md SKILL.md` | **0 hits** (expected pre-implementation) | n/a | This is the pre-impl baseline; post-impl must return ≥24 hits (8 IDs × 3 surfaces). |

---

## 7. Summary

All three FR-CONV.1 insertion sites are verified-current at the PRD-cited line ranges (rf-qa.md:264-287, SKILL.md:898-906, SKILL.md:1491-1507) with only cosmetic ±1-3 line offset at Site 3 that does not affect the grep-based acceptance verification. The TB-Add 1..8 catalogue is well-grounded: TB-Add-1/3/4/5/6 are 1:1 CB-3 ports of sc-tasklist checks 11/14/15/16/17 (sourced from sc-tasklist-protocol/SKILL.md:1000 and 1024-1031), TB-Add-2 adapts check 13 with `[ADVISORY]` severity per OPEN-INV-006, and TB-Add-7/TB-Add-8 are net-new structural checks that absorb PR-01 failure-mode #4 (header-vs-items drift) and resolve INV-015 (evidence-bound-item preservation under FR-CONV.2's scope-confinement rule). FR-CONV.1 has zero outbound FR dependencies and three inbound dependencies (FR-CONV.2, FR-CONV.3, FR-CONV.6) that justify its first-in sequencing; INV-010 is unblocked by catalogue presence and K-007 sequencing-inversion is doubly mitigated by strict serial order plus PR-04's dynamic enumeration. Three TDD-author gaps remain non-blocking: TB-Add-8 justified-absence syntax canonicalisation, TB-Add-7 source-areas matching algorithm choice, and runtime error-emission deduplication policy across the three definition surfaces — all resolvable in the TDD without renegotiating FR-CONV.1's acceptance criteria.

---

**Status:** Complete

