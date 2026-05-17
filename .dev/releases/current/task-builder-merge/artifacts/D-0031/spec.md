# D-0031 — T03.07 Spec: Wire INV-010 Dynamic Checklist Enumeration

**Task:** T03.07 (Phase 3)
**Roadmap items:** R-057
**Date:** 2026-05-17
**Tier:** STANDARD
**Verification:** Direct test execution

---

## 1. Goal

Wire the INV-010 dynamic-enumeration rule into the orchestrator's
A.10.5 spawn procedure so that the TB-Add-* catalogue handed to the
rf-qa-qualitative consumer is **always pulled live from `rf-qa.md`'s
"Structural Gate Additions" region** — never hand-maintained inside
this skill. Future structural additions (FR-CONV.1 catalogue growth)
MUST flow through to the PR-04 passthrough with zero edits to SKILL.md
or orchestrator code.

Source: roadmap.md R-057 — "Injected verdict table row count enumerates
over TB-Add catalogue at runtime (auto-picks up FR-CONV.1 additions);
structural diff before/after FR-CONV.1 landing shows enrichment";
release-spec §4 INV-010; DM-005 `enumeration_rule:
INV-010-auto-pick-TB-Add` field (SKILL.md:1258).

## 2. Implementation surface

Single file edited: `src/superclaude/skills/task-builder/SKILL.md`
(+13 lines / -0 in §A.10.5).

The edit inserts a new directive block titled **"TB-Add catalogue
enumeration (INV-010 dynamic catalogue lookup)"** at SKILL.md:1213
(immediately after the INV-002 freshness procedure that ends at
:1211 and before A.10.6 at :1226). The block defines an 8-step
procedure the orchestrator MUST execute on every spawn (initial entry
**and** every fix-cycle re-entry, dovetailing with the INV-002
freshness step 4):

| Step | Action                                                                                            |
|------|---------------------------------------------------------------------------------------------------|
| 1    | Locate `rf-qa.md` via the agent registry (canonical: `src/`; mirror: `.claude/`)                  |
| 2    | Bound the catalogue region to `#### Structural Gate Additions` → next `####`/`###`/`##` heading   |
| 3    | Regex-extract TB-Add IDs via `^[0-9]+\. \*\*TB-Add-([0-9]+):` (Python `re`, MULTILINE)             |
| 4    | Build `LIVE_TB_ADD` (deduped, sorted ascending by N); K = runtime size                            |
| 5    | Cross-check against producer's Items Reviewed: orphan ID → FAIL `INV-010-orphan-tb-add` and halt   |
| 6    | Forbid hard-coded enumeration in this A.10.5 block (operator self-check via grep)                  |
| 7    | Emit structured log `INV-010: enumerated TB-Add-* catalogue size=K ids=[...] source_sha256=<hex8>` |
| 8    | Auto-richening invariant: append a `**TB-Add-N+1: <name>` to rf-qa.md → K grows by 1, zero edits   |

Steps 1-4 are the enumeration mechanism; step 5 is the cross-check
that prevents the consumer from acting on a stale producer; step 6 is
the self-check that prevents this skill from regressing to a hand-
maintained list; step 7 is the operator-visible audit-trail (TEST-010
assertion surface); step 8 declares the invariant the fixture
demonstrates.

## 3. Why steps 5, 6, and 8 are not redundant with the existing prose

The pre-T03.07 directive at SKILL.md:1100 already names INV-010 in one
sentence ("dynamically enumerate every TB-Add-* item from rf-qa.md's
current checklist — do NOT hand-maintain the list"), and step 4 of the
INV-002 freshness procedure at SKILL.md:1206 cites a re-enumeration
requirement. T03.07 makes the rule executable:

- **Step 5 (cross-check)** transforms the prose "dynamically enumerate"
  into a *consumer-side defense*. The producer might be running on a
  stale catalogue snapshot (e.g., orchestrator-fleet rolling upgrade
  inverted PR-06 / PR-04 — K-007 sequencing-inversion). When the
  producer's table references a TB-Add-N that does NOT appear in the
  live `LIVE_TB_ADD`, that is the unique signature of "producer
  enumerated a stale catalogue version" — halt the spawn and surface
  the contradiction.
- **Step 6 (forbid hard-coded enumeration)** is the regression-
  prevention guard. Without an explicit prohibition, a well-meaning
  future edit could append `[TB-Add-1, TB-Add-2, TB-Add-3, ...]` as a
  literal list to the orchestrator's directive — defeating the
  dynamic property. The operator self-check (`grep TB-Add-[0-9]+`
  inside the A.10.5 span) is a 5-second sanity check that catches the
  regression at code-review time.
- **Step 8 (auto-richening invariant)** is the formal statement of
  what FR-CONV.1 catalogue growth is supposed to do: one line added
  to `rf-qa.md`'s bounded region → one entry added to `LIVE_TB_ADD`,
  zero edits anywhere else. The TEST-010 fixture (T03.15) consumes
  this as its assertion: synthetic TB-Add-(K+1) stub → K grows by 1.

The three steps are minimum-viable-implementation, not gold-plating.

## 4. Acceptance criteria mapping

| AC                                                                                            | Where                                                                |
|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Structural diff before/after catalogue growth shows new entries                               | `D-0031/fixture-enum.sh` PASS (c); `D-0031/fixture-enum.log` diff   |
| Adding a synthetic TB-Add-9 stub auto-richens the checklist (no code changes)                 | `D-0031/fixture-enum.sh` PASS (a) + (b)                              |
| Evidence at `TASKLIST_ROOT/artifacts/D-0031/evidence.md`                                      | `D-0031/evidence.md`                                                 |
| TB-Add catalogue lookup is dynamic (no hard-coded list of TB-Add IDs in enumeration logic)    | SKILL.md:1220 step 6 (operator self-check); `D-0031/evidence.md` §3.3 |

## 5. Out of scope (deferred)

- **Formal pytest fixture** under `tests/audit/test_dynamic_enumeration_inv_010.py`:
  deferred to T03.15 / TEST-010 per phase-3 tasklist. The shell fixture
  at `D-0031/fixture-enum.sh` is the demonstration evidence; the
  pytest version is the merge-gate fixture.
- **Anti-inflation block preservation byte-stable**: continues to be
  T03.08's canonical assertion. T03.07 edits SKILL.md only —
  `rf-qa-qualitative.md:766-775` is not touched (verified in evidence
  §3.2).
- **Producer-side enumeration**: the rf-qa producer is presumed to
  emit its own TB-Add-* rows from the same `rf-qa.md` source. T03.07
  is the consumer-side enforcement only; producer-side runtime
  alignment is a rf-qa concern owned outside this task.

## 6. Rollback

Disable `FF_INHERITED_STRUCTURAL_VERDICT` (M7 governance entry per
T02.11 / D-0025). The orchestrator falls back to spawning
rf-qa-qualitative without the verdict block; rf-qa-qualitative reverts
to independent structural re-checking per its standalone behavior. The
T03.07 SKILL.md block becomes a no-op section once upstream extraction
is skipped — no rollback edit to the block itself is required.

## 7. Dependencies satisfied

- T03.03 (D-0028) — API-002 spawn-prompt injection at A.10.5 — PASS,
  splice position established at SKILL.md:1127.
- T03.05 (D-0030) — INV-002 freshness re-entry procedure — PASS,
  step 4 of the freshness procedure now invokes T03.07's enumeration.
- TB-Add catalogue (M1) — frozen at rf-qa.md:292-310 (TB-Add-1
  through TB-Add-8), 8 entries enumerated by the regex in step 3.

## 8. Cross-references

- Runtime implementation: SKILL.md §A.10.5 TB-Add catalogue
  enumeration block (1213-1224).
- General directive (pre-existing): SKILL.md:1100 (one-sentence
  INV-010 mention) + SKILL.md:1206 step 4 (re-enumeration on
  fix-cycle).
- DM-005 contract field: SKILL.md:1242 + 1258
  `enumeration_rule: INV-010-auto-pick-TB-Add`.
- Catalogue source: `src/superclaude/agents/rf-qa.md:292-310`
  Structural Gate Additions.
- Future fixture: `tests/audit/test_dynamic_enumeration_inv_010.py`
  (T03.15 / TEST-010).
- Roadmap row: roadmap.md R-057.
- Release spec: release-spec §4 INV-010; §4.6 K-007 sequencing
  contingency.
