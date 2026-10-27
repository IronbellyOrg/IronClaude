# D-0040 — T03.17 Spec: K-007 Sequencing-Inversion Contingency

**Task:** T03.17 (Phase 3)
**Roadmap items:** R-069 (M3 table row 21 — "K-007 mitigation"; cross-referenced as R-008 in the Risk Registry at `roadmap.md:558`)
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Risk Statement

**K-007** — PR-04 + PR-06 sequencing inversion: if FR-CONV.3 (PR-04 Gate
Results Passthrough) lands before FR-CONV.1 (PR-06 Structural Gate
Additions), then the `## Inherited Structural Verdict` block injected
into rf-qa-qualitative's spawn prompt would enumerate over an empty (or
partial) TB-Add-* catalogue, defeating INV-010 (`enumeration_rule:
"Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from
FR-CONV.1; no manual template edit required"`, release-spec §5.3
phase_contract).

Severity / likelihood — per release-spec §7 K-007 row (line 429) and
roadmap.md Risk Registry (line 558): **likelihood low, impact medium**.

## 2. Binding Sequencing Rule

The release-spec enforces the sequencing rule at three reinforcing
sites:

| Site | Form | Authority |
|---|---|---|
| `release-spec.md:338-353` (§4.6 Implementation Order) | Numbered list — `1. FR-CONV.1 (PR-06 …)` precedes `3. FR-CONV.3 (PR-04 …)`; item 3 carries the inline annotation `inherits TB-Add catalogue dynamically (INV-010 sequencing)` | Binding (per §9 SP-26: "binding sequence is §4.6's serial order") |
| `release-spec.md:429` (§7 K-007 row) | Arrow notation — "Sequencing rule **PR-06 → PR-04 enforced** (FR-CONV.1 lists before FR-CONV.3 in §4.6); PR-04 prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation)" | Cross-references §4.6 as the binding source |
| `release-spec.md:498` (§9 SP-26) | Reconciliation note — "The binding sequence is §4.6's serial order (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03). No parallel-land tolerance is permitted for SKILL.md:872-916 since FR-CONV.1 and FR-CONV.6 both edit overlapping ranges" | Re-affirms §4.6 binding status |

The acceptance criterion grep
`grep -n "PR-06 → PR-04" release-spec.md` returns exactly one literal
match — line 429 — which is the K-007 contingency row that
*enforces* the rule (verb: "enforced") and *cross-references* §4.6 as
the binding mechanism. See `evidence.md` § 2 for the AC interpretation
in full.

## 3. INV-010 Mitigation Path (auto-richening enumeration)

Even when the sequencing rule holds (PR-06 lands first), the
implementation defence-in-depth at SKILL.md §A.10.5 makes the
checklist self-healing under late catalogue activation:

1. The orchestrator's TB-Add catalogue enumeration procedure
   (8 steps, wired by T03.07 / D-0031; lands in MIG-003 commit
   `ad083b6`; lives at SKILL.md §A.10.5 `TB-Add catalogue
   enumeration (INV-010 dynamic catalogue lookup)`) re-pulls TB-Add-*
   IDs from `src/superclaude/agents/rf-qa.md`'s `#### Structural Gate
   Additions` region **at every spawn** — no hard-coded TB-Add-* list
   in SKILL.md.
2. Therefore, if a TB-Add-* row is published into `rf-qa.md` after
   FR-CONV.3 spawn-prompt injection is already wired, the *next*
   rf-qa-qualitative spawn auto-enumerates the new row into the
   inherited verdict table — no SKILL.md edit, no migration, no
   regression.
3. TEST-010 (`tests/audit/test_dynamic_enumeration_inv_010.py`,
   T03.15 / D-0038) asserts this: a synthetic TB-Add-N+1 stub injected
   into `rf-qa.md` auto-richens the spawn-prompt enumeration in the
   very next cycle. 19 assertions PASS.
4. Negative case: TEST-024 in the M5 plan
   (`test_sequencing_PR06_before_PR04`, roadmap M5 row 19 / line 327)
   exercises the inverted-landing scenario directly and asserts
   structural enrichment once the catalogue activates — the formal
   K-007 verification fixture.

**Net effect:** the sequencing inversion would degrade *only* the
first rf-qa-qualitative spawn between the inverted-land moment and the
next FR-CONV.1 landing. From that point onward, INV-010 dynamic
enumeration auto-recovers without intervention.

## 4. Inversion-Detection Re-Merge Procedure

If post-merge audit (release-spec §8.3 row 4 — first 5
rf-qa-qualitative runs after FR-CONV.3 lands) discovers that the
sequencing was inverted on `master`, follow this step-by-step re-merge:

1. **Detect** — Inspect `git log master --oneline --grep="FR-CONV"`
   and locate the commit SHAs for `FR-CONV.1` (PR-06) landing and
   `FR-CONV.3` (PR-04) landing (MIG-003 commit `ad083b6` is the
   M3-side anchor). If the FR-CONV.3 commit timestamp precedes the
   FR-CONV.1 commit timestamp on `master`, sequencing inversion is
   confirmed.
2. **Triage** — Run `grep -n "TB-Add-" src/superclaude/agents/rf-qa.md`
   and count rows under the `#### Structural Gate Additions` heading.
   If the count is < 8 (the M1 contract-frozen count from T01.13)
   and FR-CONV.3 is already live, the inherited verdict table is
   under-enumerated. Inspect any `qa-task-validation-report.md`
   generated since the inverted-land moment for missing TB-Add-* rows.
3. **Quarantine (optional)** — Disable
   `FF_INHERITED_STRUCTURAL_VERDICT` per the per-line rollback
   procedure documented in `D-0039/spec.md` § 3 ("Per-line rollback
   path"). rf-qa-qualitative falls back to standalone structural
   re-checking per Critical Rule #11 in rf-qa-qualitative.md
   ("fall back to your standalone behavior"). This is *not* required
   if the audit window has not yet completed — INV-010 auto-recovery
   may resolve the gap on the next spawn.
4. **Re-merge in correct order** — Revert the FR-CONV.3 landing
   commit (`git revert <FR-CONV.3-SHA>`) on a hotfix branch, then
   re-apply the FR-CONV.1 landing first (cherry-pick or re-merge the
   FR-CONV.1 commits onto the hotfix branch ahead of FR-CONV.3),
   followed by FR-CONV.3. The release-spec §4.6 numbered list is the
   authoritative ordering: `1. FR-CONV.1` → `2. FR-CONV.2` →
   `3. FR-CONV.3`. Open a hotfix PR documenting the corrective
   re-sequencing in the commit body, citing this K-007 procedure.
5. **Verify** — Run the four M3 audit fixtures
   (`uv run pytest tests/audit/test_inherited_verdict_present.py
   tests/audit/test_inherited_verdict_freshness_inv_002.py
   tests/audit/test_self_audit_inv_019.py
   tests/audit/test_dynamic_enumeration_inv_010.py -v`).
   All MUST pass. Then run `make verify-sync` and confirm exit 0.
6. **Re-enable** — Re-enable `FF_INHERITED_STRUCTURAL_VERDICT` if it
   was disabled in step 3, and resume the K-003 audit window from the
   re-merge commit.
7. **Backfill audit** — Inspect any `qa-task-validation-report.md`
   produced during the inverted-sequence window. If any report shows
   TB-Add-* under-enumeration in its Items Reviewed table, file a
   regression issue and instruct rf-team-lead to re-run rf-qa on the
   affected BUILD_REQUESTs. The K-003 audit window resets — five
   fresh post-re-merge runs MUST be audited (release-spec §8.3 row 4).

**Authoritative re-merge sequence:** `FR-CONV.1 (PR-06)` →
`FR-CONV.2 (PR-01)` → `FR-CONV.3 (PR-04)` →
`FR-CONV.4 (PR-07)` → `FR-CONV.5 (PR-02)` →
`FR-CONV.6 (PR-03)` (release-spec §4.6 numbered list, lines 341–352).

## 5. Acceptance Criteria mapping (phase-3-tasklist.md L829–834)

| AC | Status | Evidence location |
|---|---|---|
| File `TASKLIST_ROOT/artifacts/D-0040/spec.md` exists and documents the K-007 contingency | PASS | This file |
| Sequencing rule PR-06 → PR-04 explicitly named in the note | PASS | This spec § 2 + § 4 (authoritative re-merge sequence) |
| INV-010 mitigation cited | PASS | This spec § 3 (auto-richening enumeration; TEST-010 / TEST-024) |
| `grep -n "PR-06 → PR-04" <release-spec>` returns a match within §4.6, confirming sequencing rule is enforced (not merely documented in artifact note) | PASS (with interpretation) | This spec § 2 + `evidence.md` § 2 — single literal match at line 429 (§7 K-007 row) which enforces the rule and cross-references §4.6's numbered list; §4.6's authority is re-affirmed at §9 SP-26 (line 498) |
| Re-merge procedure described step-by-step | PASS | This spec § 4 (7-step procedure) |

## 6. Dependencies

- T03.16 PASS (`D-0039/spec.md` + `D-0039/evidence.md` — MIG-003
  landed at commit `ad083b6`; FF_INHERITED_STRUCTURAL_VERDICT
  governance entry recorded; per-line rollback path documented)
- T03.15 PASS (`D-0038/evidence.md` — TEST-010 dynamic enumeration
  INV-010 fixture green; demonstrates the auto-richening defence-
  in-depth that the K-007 procedure relies on)

## 7. Cross-references

- Release-spec §4.6 Implementation Order (lines 338–353) — binding sequencing list
- Release-spec §7 K-007 row (line 429) — risk + mitigation summary
- Release-spec §9 SP-26 (line 498) — §4.6 binding-authority reaffirmation
- Release-spec §8.3 row 4 — K-003 audit window (first 5 rf-qa-qualitative runs post-FR-CONV.3)
- Roadmap.md M3 table row 21 (line 228) — R-069 K-007 mitigation
- Roadmap.md M3 Risk Register row 2 (line 256) — R-M3-2 K-007 owner: Engineering Lead
- Roadmap.md Cross-Milestone Risk Registry row R-008 (line 558) — portfolio-level K-007 entry
- Roadmap.md M5 row 19 (line 327) — TEST-024 `test_sequencing_PR06_before_PR04` formal verification fixture
- D-0031 / D-0038 — INV-010 dynamic enumeration wiring + fixture evidence
- D-0039 § 3 — per-line rollback path quoted in step 3 of this procedure
