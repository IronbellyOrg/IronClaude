# QA Report — Synthesis Gate (Content-Quality Lens)

**Topic:** FR-DRS — sc:reflect Deterministic Runtime-Surface Sweep TDD
**Date:** 2026-06-21
**Phase:** synthesis-gate (content-quality lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Adversarial stance:** assumed ≥5 content-quality/consistency errors; verified each ask independently against source.

---

## Overall Verdict: PASS (with 1 IMPORTANT advisory)

The synthesis content is unusually internally consistent. Every targeted ask resolved in the
synthesis's favor: the six field names match research/03 byte-exactly, the count-invariant string is
identical wherever it appears, FR traceability holds, and the reflect→audit import-boundary
recommendation is consistent across all four sections. One genuine content-quality tension exists
(FR-006 / AC-4 sprint-executor actionability) — it is openly *flagged* in synth-02 G2 but not
*resolved*, so it is recorded as IMPORTANT (advisory), not a blocking FAIL. The assumed ≥5 errors did
not materialize; this is reported honestly rather than padded.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Six `runtime_surface_*` field names in synth-04 §8.2 match research/03 §1 EXACTLY | PASS | synth-04:143-148 lists `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces` — identical to research/03 lines 27-32. grep-counted all six present in synth-04 (8/8/1/1/2/8). |
| 2 | "Only 5 carry the prefix" caveat correctly surfaced | PASS | synth-04:150 CRITICAL prefix caveat ("Only 5 of the 6 … `startswith` would silently drop `unreached_surfaces`"), matching research/03:22-23 + Gap #2. Also flagged in synth-02 G4. |
| 3 | Count invariant `len(unreached_surfaces) == runtime_surface_unreached` identical in synth-02, synth-04, synth-07 | PASS | Byte-identical string in synth-02:24,64; synth-04:103; synth-07:29,53,69,110. grep confirmed same operator/spacing/operand order in all 7 synth files that state it (also synth-01,05,06,08,09). No drift. |
| 4 | FR traceability — spot-check 3 FRs cite a valid AC-1..AC-6 source | PASS | FR-001→AC-1 (ledger+scalars every run); FR-006→AC-4 (§5.3 + sprint read deterministic); FR-003→AC-3 (count invariant). All three ACs verified verbatim in research/00 §6 (AC-1 line 95, AC-3 line 97, AC-4 line 98). No `[NO PRD TRACE]` rows; per-AC coverage map (synth-02:60-67) exercises all six ACs. |
| 5 | reflect→audit import-boundary decision consistent across synth-03 §6.4, synth-09 §21, §22 (recommendation = reflect-local copy / Option C for v1) | PASS | synth-03:105 D1 "Option C (reflect-local copy) for v1 … avoid Option A". synth-09:105 Alt 3 "Option C … recommended v1 choice … Option A is the one to AVOID". synth-09:237/240 reuse audit + R5:20 all say reflect-local copy, Option B long-term. synth-08:92 §18.2 agrees. Zero contradiction. |
| 6 | FRs actionable with testable acceptance criteria (Given/When/Then or specific) | PASS (1 exception → Issue #1) | All 13 FRs + 7 NFRs use Given/When/Then or concrete file:line criteria. FR-004/005/009/013 name exact symbols/paths. Exception: FR-006's sprint-executor clause (see Issues). |
| 7 | AC-2 per-case deterministic expectations consistent across synth-01/05/07/09 | PASS | case 39 dynamic-dispatch = "degraded true, regression 0" in synth-01:154, synth-05:123, synth-07:86, synth-09:191. cases 37/41 = "unreached 1, regression 1, tier 2". No cross-file divergence. |
| 8 | Sprint executor framed consistently (SPEC-ONLY / not-implemented) | PASS | synth-02:74 G2 "spec-only, not implemented"; synth-03:96 "spec-only consumer today (not yet wired)"; synth-07:130 "SPEC-ONLY today"; synth-09:116,193 same. Uniform — no section claims it is already wired. |
| 9 | Section numbering matches template (no fabricated/renumbered sections) | PASS | synth-03 §6/§7/§8, synth-06 §12/§13, synth-04 §7/§8 etc. all match tdd_template.md canonical headers (§1-§28). N/A sections (9,10,16) correctly justified as backend/no-UI. |
| 10 | No fabricated facts / hallucinated paths in content claims | PASS (within content-lens scope) | Spot-checks: `runner.py:445` parse_contract chokepoint, `runner.py:14-17` _IndentDumper copy precedent, `ensemble.py:59` version stamp, `grader.py:191`/`:448-449` — all consistently cited across synth files and traceable to research 02/03/04/05. (Deep file:line re-verification vs live source is the structural-lens QA's scope, not this content-lens pass.) |

## Summary

- Checks passed: 10 / 10 (Check #6 passes with one documented exception captured as Issue #1)
- Checks failed: 0
- Critical issues: 0
- Important issues: 1 (advisory — already flagged in-synthesis, not hidden)
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | synth-02 FR-006 (line 27) ↔ synth-09 §23.2 Phase 2 (lines 154-161) ↔ AC-4 | **FR-006 sprint-executor clause is a Must-Have with a testable AC that no implementation phase delivers and that research says is unbuilt.** FR-006 is rated *Must Have* and asserts "the sprint executor's regression-mapping gate reads from the deterministic contract." research/03 §5.2-5.3 proved `cli/sprint/executor.py` reads NO reflect contract today (imports `TurnLedger` for budget only) — wiring it is net-new. synth-09 Phase 2 deliverables wire `runner._audit_once`, `contract.py`, and the bare-skill shell-out, but contain **no deliverable that wires the sprint executor**, yet Phase 2's exit criterion still claims "§5.3 pre-filter + `sprint run` executor read the deterministic scalars (AC-4)." So a Must-Have FR + an exit-criterion both assert a consumer read that no planned work builds. synth-02 G2 honestly flags the in-scope/deferred decision ("FR-006 as written assumes the read path exists") but the TDD never resolves it, and no Non-Goal excludes the sprint wiring. | Resolve the scope decision the synthesis already surfaced: either (a) split FR-006 into FR-006a (§5.3 pre-filter — in scope, deliverable exists) and FR-006b (sprint-executor wiring — explicitly deferred / Non-Goal, demote from Must-Have or mark "blocked by OQ"), OR (b) add an explicit Phase-2 deliverable wiring `cli/sprint/executor.py` to read the reflect contract and reflect that in AC-4 coverage. Remove the unqualified "sprint executor read the deterministic scalars" from Phase 2's exit criterion until the read path is in a deliverable. This is the completion-criteria-honesty class: do not assert a satisfiable AC for an unbuilt consumer. |

## Adversarial-Stance Note

I entered assuming ≥5 content-quality/consistency errors. After independently verifying every targeted
ask against source (research/00 ACs, research/03 field names, byte-level invariant grep, per-case AC-2
values, four-section boundary-decision cross-read, template section numbering), only **one** genuine
finding survived — and it is one the synthesis itself already flags (synth-02 G2). The remaining
"suspect" areas (5-vs-6 prefix naming, NON-GATING-vs-GATING §9.3/§5.3 tension, contract-version 1.0/1.6.0
mismatch, AC-4 sprint gap) are all explicitly surfaced and correctly reconciled in the synthesis rather
than left as latent contradictions. Per Principle 9 (report honestly; a false FAIL is as bad as a false
PASS), I report the true count rather than manufacture findings to hit a quota. The single IMPORTANT
issue does not block the synthesis gate on its own (it is an openly-tracked open decision, not a hidden
defect), hence PASS-with-advisory.

## Recommendations

- Before assembly, the TDD author should resolve Issue #1's scope decision so AC-4's sprint-executor
  half is either delivered or explicitly deferred. This is the one content item that could mislead a
  downstream task-builder into planning a consumer read that has no producer-side or wiring deliverable.
- No other content-quality remediation required prior to assembly.

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 4 | Glob: 1 | Bash: 4 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
  - No external lookup was required: every claim verified is intrinsically local (synthesis ↔ research ↔ template). Tavily-first rule did not trigger.
- All checklist items VERIFIED with cited tool output (file:line or grep/sed result). No UNVERIFIABLE or UNCHECKED items.

## QA Complete
