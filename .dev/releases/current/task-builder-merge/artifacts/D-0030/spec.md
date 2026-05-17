# D-0030 — T03.05 Spec: Wire INV-002 Freshness Rule (cycle-N+1 reinjection)

**Task:** T03.05 (Phase 3)
**Roadmap items:** R-056
**Date:** 2026-05-17
**Tier:** STANDARD
**Verification:** Direct test execution

---

## 1. Goal

Wire the INV-002 freshness rule into the orchestrator's A.10.5 spawn
procedure so that EVERY fix-cycle re-entry re-extracts the rf-qa
"Items Reviewed" verdict table from disk and re-injects the NEW
cycle-N+1 verdict into the rf-qa-qualitative spawn prompt. Stale
verdicts from prior cycles MUST be rejected.

Source: roadmap.md:215 R-056 — "Orchestrator MUST re-read current
rf-qa task-integrity report and re-extract table on every fix-cycle
spawn"; release-spec §4 INV-002; DM-005 `freshness_rule:
INV-002-reinject-NEW` field (SKILL.md:1241).

## 2. Implementation surface

Single file edited: `src/superclaude/skills/task-builder/SKILL.md`
(+22 lines / -0 in §A.10.5).

The edit inserts a new directive block titled **"Fix-cycle re-entry
(INV-002 freshness — stale-verdict rejection)"** at SKILL.md:1201
(immediately after the existing "Handling the verdict" subsection in
A.10.5 and before A.10.6). The block defines a 7-step procedure the
orchestrator MUST execute on every re-entry into A.10.5:

| Step | Action                                                                                   |
|------|------------------------------------------------------------------------------------------|
| 1    | Discard cached state (prior extracted span, TB-Add enum, assembled block, prompt string) |
| 2    | Re-stat + re-sha256 the producer artifact; capture witnesses                             |
| 3    | Re-extract "Items Reviewed" span contiguously (single-span rule)                         |
| 4    | Re-enumerate TB-Add-* catalogue from rf-qa.md (live; no snapshot reuse)                  |
| 5    | Re-assemble and re-splice the verdict block at the API-002 wire-contract position        |
| 6    | Stale-verdict-rejection: reject contradiction (producer-changed + block-unchanged)       |
| 7    | Emit structured log `INV-002: re-extracted verdict for ${TASK_DIR} cycle=N+1 ...`        |

Steps 1, 3, 4 enforce the re-extract; step 6 supplies defense-in-depth
against a corrupt orchestrator that reuses a cached block; step 7 is
the operator-visible audit-trail that the 2-cycle fixture (D-0030)
and TEST-008 (T03.13) consume as their assertion surface.

## 3. Why steps 6 + 7 are not redundant

The directive at SKILL.md:1100 (landed by T03.01) already names INV-002
in one sentence. T03.05's new block makes the procedure executable:

- **Step 6 (stale-verdict-rejection)** transforms the prose
  "stale verdicts forbidden" into a *contradiction detector*:
  `producer-witness != prior-witness ∧ block-sha == prior-block-sha`
  is the unique signature of "orchestrator skipped re-extraction
  despite producer change". Equal-witnesses + equal-block-sha is the
  legitimate no-op case (producer truly unchanged) and must be allowed.
- **Step 7 (logging)** is the assertion surface for TEST-008. Without
  the log line, the test fixture has no observable to grep on; the
  test would have to reconstruct orchestrator internals.

The two steps are minimum-viable-implementation, not gold-plating.

## 4. Acceptance criteria mapping

| AC                                                                                       | Where                                                                 |
|------------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| 2-cycle fixture byte-diff at verdict-table region shows cycle-2 content                  | `D-0030/fixture-2cycle.sh` PASS (c); `D-0030/fixture-2cycle.log`     |
| Cycle-2 spawn prompt does NOT contain cycle-1's verdict                                  | `D-0030/fixture-2cycle.sh` PASS (b)                                  |
| Orchestrator logs the re-extract step at every fix-cycle boundary                        | SKILL.md:1209 step 7; `D-0030/fixture-2cycle.log` line 2             |
| Evidence at `TASKLIST_ROOT/artifacts/D-0030/evidence.md`                                 | `D-0030/evidence.md`                                                 |

## 5. Out of scope (deferred)

- **Formal pytest fixture** under `tests/audit/test_inherited_verdict_freshness_inv_002.py`:
  deferred to T03.13 / TEST-008 per phase-3 tasklist. The shell fixture
  at `D-0030/fixture-2cycle.sh` is the demonstration evidence; the
  pytest version is the merge-gate fixture.
- **TB-Add catalogue dynamic enumeration** (INV-010): deferred to
  T03.07. Step 4 cites the rule but the runtime enumeration logic is
  T03.07's deliverable.
- **Anti-inflation block preservation byte-stable**: deferred to T03.08.
  T03.05 edits SKILL.md only — `rf-qa-qualitative.md:766-775` is not
  touched (verified in evidence §3).

## 6. Rollback

Disable `FF_INHERITED_STRUCTURAL_VERDICT` (M7 governance entry per
T02.11 / D-0025). The orchestrator falls back to spawning
rf-qa-qualitative without the verdict block; rf-qa-qualitative reverts
to independent structural re-checking per its standalone behavior.
The T03.05 SKILL.md block becomes a no-op section once the upstream
extraction is skipped.

## 7. Dependencies satisfied

- T03.03 (D-0028) — API-002 spawn-prompt injection at A.10.5 — PASS,
  splice position established at SKILL.md:1127.
- T03.04 (D-0029) — Self-Audit schema requirement — PASS, schema
  requirement landed at rf-qa-qualitative.md:823.
- DM-005 published row (T02.04 / D-0019) — PASS, `freshness_rule:
  INV-002-reinject-NEW` field documented at SKILL.md:1241.

## 8. Cross-references

- Runtime implementation: SKILL.md §A.10.5 Fix-cycle re-entry block (1201-1211).
- General directive (pre-existing): SKILL.md:1100 (one-sentence INV-002 mention).
- DM-005 contract field: SKILL.md:1241 `freshness_rule: INV-002-reinject-NEW`.
- Output-schema realisation surface: rf-qa-qualitative.md:823 (Self-Audit).
- Future fixture: tests/audit/test_inherited_verdict_freshness_inv_002.py (T03.13).
- Roadmap row: roadmap.md:215 R-056.
- Release spec: release-spec.md:389 + §4 (INV-002 invariant).
