# QA Report — Research Gate (Gap-Detection Lens) — ROUND 2 (post gap-fill round 1)

**Topic:** Additive hardening of RF QA + /sc:reflect vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** research-gate (RE-RUN / fix-cycle verification)
**Lens:** gap-detection
**Fix cycle:** round 2 (verifying closures of prior gaps G1-G8)
**Fix authorization:** false (report-only)

---

## Scope

Verify the gap-fill research file `research/08-gap-fill.md` against the ACTUAL worktree code.
Adversarial stance: assume gaps remain; do not trust gap-fill self-assessment. Spot-check
load-bearing closures (G1, G3, G4, G5, G6) directly against source.

Prior verdict: FAIL — 8 gaps (G1 CRITICAL, G2-G6 IMPORTANT, G7-G8 MINOR).

---

## Verification Log (appended incrementally)

**Coverage note:** `08-gap-fill.md` contains detailed closures for **G1-G6 only**. Its
"GAP CLOSURE SUMMARY" lists G1-G6. **G7 and G8 are entirely absent** from the gap-fill
file (`grep -n "G7\|G8\|start_commit\|stale.*header" 08-gap-fill.md` → empty). Each prior
gap was independently re-verified below against actual worktree source (zero-trust).

### G1 [CRITICAL] — CLOSED (verified regression-free)
- Read `tests/audit/test_five_axes_overlay.py` in full. `:28` pins
  `CHECKLIST_HEADER = "#### Checklist (15 items)"` — confirmed the ONLY count-pin in
  `tests/` (grep: only hits are this file + prose in test_task_builder_merge.py /
  test_inherited_verdict_freshness, none of which pin the FX2 surface).
- **Branch A regression-freedom PROVEN against the assertion set:** the count-pinned
  assertions are `test_checklist_header_present_in_source` (`:72-75`, `CHECKLIST_HEADER in
  src_text`), `_ordering` (`:83`, `line.strip() == CHECKLIST_HEADER`), and
  `_slice_between_headers` (`:119`, same equality as the axes-slice END boundary). The
  Code-Compatibility items 4-6 live at `rf-qa-qualitative.md:672-676`, which is **AFTER**
  the checklist header at `:660` and **OUTSIDE** the axes slice (`:580`→`:660`). Therefore
  augmenting items 4-6 in place (a) leaves the "(15 items)" header string byte-unchanged,
  (b) does not move the checklist header relative to the axes header (ordering holds), and
  (c) does not alter the axes slice contents. All `:72-:141` assertions stay green,
  provided `make sync-dev` runs for the byte-parity gate (`:141-146`). **Branch A is
  genuinely regression-free.** Branch B's 3 mandatory atomic edits (L28→"16 items", brief
  header `:660` + prose `:580`/`:582`, sync-dev) are correctly and completely enumerated.

### G2 [IMPORTANT] — CLOSED
- `grep -rln "deviation-taxonomy" tests/` → **EMPTY**. Confirmed ZERO guarding tests over
  `deviation-taxonomy.md` — the gap-fill's claim is accurate. FX1's taxonomy edit has no
  deterministic regression test; gap-fill correctly flags "author one or accept
  manual-review-only." Guard map (byte-parity tripwires + sync-dev-mandatory) is sound.

### G3 [IMPORTANT] — CLOSED
- Read `rf-qa-qualitative.md:670-676`. Items 4 (`:672` "read the actual function... parameter
  names, types, return type... call sites won't break"), 5 (`:674` "read the full module"),
  6 (`:676` "trace all consumers of that output") **genuinely direct the reviewer to read
  source symbols.** R4-correct / R7-overstated conclusion is well-supported and in-scope.
- Closed vocab `{AX-1..AX-5, none}` confirmed at `:639`; `N/A` forbidden at `:648`. Annotate
  AX-2, add no AX-6 — sound.

### G4 [IMPORTANT] — CLOSED
- `SKILL.md:201` "Research quality gate ... (A.8)"; `:204` "Task file structural validation
  ... (A.10)" — confirmed these are the **task-builder's OWN internal gates**, not a
  pr_submit-pytest attach point. Gate rule verbatim confirmed present: "Gate PASSES when ALL
  verdicts are PASS with ALL findings resolved regardless of severity. A single FAIL from any
  agent fails the gate." The "FX3/FX5 = standalone CI + built-task L3 pytests, no SKILL.md
  edit" conclusion is sound and buildable. FX5 FAIL-rule mirrors the Verdict block at
  `rf-qa-qualitative.md:732-735` (confirmed present verbatim). Drop-the-Phase-2/4-framing
  guidance is correct.

### G5 [IMPORTANT] — CLOSED
- `pyproject.toml:111` `"--strict-markers"` active (confirmed). `grep -rn gate_helper tests/`
  → zero usages; `gate_helper` not in `[markers]`. Marker-free `parametrize` /
  `pytest_generate_tests` recommendation is the correct safe path; no pyproject edit needed.

### G6 [IMPORTANT] — CLOSED (with a builder caveat, not a reopen)
- `contract.py:36-38` `_VERIFICATION_SKIP_EXEMPTIONS = frozenset({"read-only-project",
  "tool-unavailable", "--no-verify"})` — confirmed unchanged; `"tool-unavailable"` present.
- `ensemble.py:492` `build_reflect_contract`, `:550` `"verification_ran": False`, `:551`
  `"verification_skip_reason": "tool-unavailable"`, `:560` `"degraded_components": []`, `:191`
  `reviewers = int(config.reviewers)` — ALL line refs verified exact.
- **Primary additive path (i) PROVEN against Trigger 12** (`contract.py:288-291`): `if
  verification_ran is False: if skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS: return
  "verification-skipped"`. Emitting a NON-exempt skip_reason fires an honest degrade with
  **no consumer edit** and the exemption set byte-unchanged. Additive path is real. Fail-safe
  HALT clause (record `needs_human_decision:true` + PENDING + HALT if a non-additive
  exemption change ever proves necessary) is **adequate** for the human-decision-must-HALT
  rule — it converts the residual risk into a gated HALT, not an auto-default.
- **CAVEAT for the builder (log, do not reopen):** gap-fill's *secondary* path (ii)
  "populate `degraded_components` → degrades WITHOUT consumer edit" is **imprecise**. The
  degrade Trigger 1-5 (`contract.py:258-260`) fires only for tokens in
  `_DEGRADED_COMPONENTS_HALT_SET` (`any(token in _DEGRADED_COMPONENTS_HALT_SET ...)`), NOT
  for an arbitrary populated list. A builder who appends a novel token believing "any
  populated list degrades" would ship a silently non-degrading change (vacuous-PASS bug
  persists). Path (i) fully closes G6, so this is a note — but the task MUST steer to path
  (i) (non-exempt skip_reason) or ensure any degraded_components token is a halt-set member.

### G7 [MINOR] — **STILL OPEN** (unaddressed by gap-fill)
- `08-gap-fill.md` never mentions `start_commit` / base-ref / R7 HL-1. `research/06` STILL
  prescribes the un-corrected `start_commit = git merge-base HEAD <integration-branch>` at
  `:44` and `:298`. R7's HL-1 finding (contract_setup + tests/pr_submit exist ONLY on this
  branch lineage, absent from `origin/master`) is NOT reconciled. If `<integration-branch>`
  resolves to `origin/master`, the entire `contract_setup` package lands in the audited diff
  — the diff-scope footgun that swamps the POST reflect gate. This is a real, known project
  footgun. Neither closed nor converted to a well-formed Open Question.

### G8 [MINOR] — **STILL OPEN** (unaddressed by gap-fill)
- `research/01-fx3-questions-resolution.md` STILL carries contradictory status: `:3`
  `Status: In Progress` vs `:353` `Status: Complete`. Trivial (a 1-line normalization), but
  a file-inventory check flags it and `fix_authorization:false` prevents me from fixing it.

---

## Items Reviewed
| # | Prior gap | Round-2 result | Evidence |
|---|-----------|----------------|----------|
| G1 | FX2 breaks test_five_axes_overlay (CRITICAL) | CLOSED | Read full test; Branch A proven regression-free (items 4-6 at :672-676 outside :580-:660 axes slice + after :660 header) |
| G2 | Brief-guard map / taxonomy tests (IMPORTANT) | CLOSED | `grep deviation-taxonomy tests/` empty; guard map accurate |
| G3 | FX2 in-scope (items 4-6 read code) (IMPORTANT) | CLOSED | Read :670-676 — signatures/module/consumers; vocab :639, N/A forbidden :648 |
| G4 | Phase-2/4 wiring (IMPORTANT) | CLOSED | SKILL.md :201/:204 = builder's own gates; :732-735 Verdict shape confirmed |
| G5 | gate_helper vs --strict-markers (IMPORTANT) | CLOSED | pyproject :111 strict active; gate_helper 0 usages/unregistered |
| G6 | FX7 additive vs human-decision (IMPORTANT) | CLOSED (caveat) | contract.py :36-38/:288-291 + ensemble.py :191/:492/:550/:551/:560 verified; Trigger-12 path (i) proven; path (ii) imprecise |
| G7 | start_commit base-ref / HL-1 (MINOR) | **STILL OPEN** | Not in gap-fill; research/06 :44/:298 still uncorrected merge-base |
| G8 | research/01 stale status (MINOR) | **STILL OPEN** | research/01 :3 "In Progress" vs :353 "Complete" unchanged |

## Summary
- Prior gaps closed this cycle: 6 / 8 (G1 CRITICAL + G2-G6 IMPORTANT — all verified against actual code)
- Prior gaps still open: 2 / 8 (G7 MINOR base-ref, G8 MINOR stale header — both unaddressed by gap-fill)
- New issues introduced by fixes: 0
- Builder caveats logged (not reopens): 1 (G6 path-(ii) imprecision)
- Monotonicity: |F| 8 → 2 (strictly shrinking; no monotonicity/regression halt)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found (remaining)
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| G7 | MINOR | research/06 :44, :298 | `start_commit = git merge-base HEAD <integration-branch>` un-reconciled with R7 HL-1; risks origin/master diff-scope footgun swamping the POST reflect gate with the contract_setup package | Set start_commit to the branch's tight parent (NOT origin/master); note R7 HL-1 in frontmatter rationale — OR carry as a well-formed Open Question the builder resolves at build time |
| G8 | MINOR | research/01 :3 | Contradictory status header ("In Progress" vs ":353 Complete") | Normalize :3 to "Status: Complete" |

## Overall Verdict: FAIL

Six of eight prior gaps — including the single CRITICAL (G1) and all four load-bearing
IMPORTANT gaps (G2-G6) — are **genuinely closed and independently verified against actual
worktree source**, not merely self-asserted. The gap-fill's load-bearing conclusions (Branch
A regression-freedom, FX2 in-scope, Phase-2/4 de-framing, marker-free FX5, FX7 additive
builder-only path) all hold under adversarial re-verification.

However, per the verdict rule ("any still-open actionable gap = FAIL"), the two MINOR gaps
**G7 (base-ref footgun) and G8 (stale status header) remain open** — the gap-fill covered
only G1-G6 and never addressed them. Both are trivially closeable:
- **G7** is either a one-line reconciliation in `research/06` (pin the tight parent, cite
  HL-1) or a well-formed Open Question the builder carries into frontmatter.
- **G8** is a one-line status normalization in `research/01`.

Because `fix_authorization:false`, I cannot close them myself. Recommend one more micro
gap-fill round (or an authorized fixer) to close G7 + G8, after which this gate is green.
This is a monotonic improvement (8 → 2 gaps, both MINOR); no monotonicity or regression halt
triggered.

## Recommendations
1. **G7:** In `research/06`, replace the `merge-base HEAD <integration-branch>` prescription
   at :44/:298 with the harden branch's tight parent, citing R7 HL-1 — OR record it as a
   well-formed Open Question ("start_commit base must avoid origin/master to dodge the
   contract_setup diff-scope footgun; builder resolves at build time").
2. **G8:** Normalize `research/01:3` to "Status: Complete".
3. **G6 builder caveat:** Ensure the built FX7 task steers to path (i) (emit a non-exempt
   `verification_skip_reason` so Trigger 12 fires), not the imprecise path (ii).

## Confidence
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 6 (via Bash batches) | Glob: 0 | Bash: 6
- No web research required (all claims are local source-truth / test-suite facts).
- Every verdict is backed by a specific tool observation: full read of
  test_five_axes_overlay.py (G1); rf-qa-qualitative.md :630-750 read (G3/G4-verdict/vocab);
  grep deviation-taxonomy tests/ (G2); pyproject :111 + gate_helper grep (G5); contract.py
  :34-40/:250-295 + ensemble.py line grep (G6); research/06 + research/01 status grep (G7/G8).

## QA Complete
