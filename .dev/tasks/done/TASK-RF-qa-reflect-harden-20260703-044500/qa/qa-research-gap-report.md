# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** Additive hardening of RF QA + /sc:reflect vs PR #209 F1-F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** research-gate
**Lens:** gap-detection (find areas researchers missed that the builder will need)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)

---

## Scope

Assigned files: research/01 through 07. Adversarial stance — assume researchers missed things.
Driving plan: FINAL-remediation-plan.md §2 fix table + §3 residual risk.

## Overall Verdict: FAIL

Gap-detection lens found **7 gaps** (1 effectively CRITICAL, 4 IMPORTANT, 2 MINOR). Per
research-gate rules, ANY gap of any severity = FAIL; all must be resolved/carried into the
brief set before the builder proceeds. The research is *broad and mostly excellent* — the
plan §3 residual risks are carried thoroughly and per-symbol findings are highly actionable —
but there is a **class of coverage the research team collectively missed: the existing pytest
suite that asserts the STRUCTURE of the markdown briefs FX1/FX2 edit.** That miss produces a
guaranteed green→red test regression (G1) plus unresolved cross-file contradictions (G3, G6).

---

## Items Reviewed (gap-detection lens)
| # | Lens check | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Per-fix coverage (target symbols / wiring pinned) | PARTIAL (G4) | FX3 (R1), FX5 (R2), FX7 (R3), FX2/FX1 briefs (R4) all pin concrete symbols w/ file:line. BUT the FX3 "Phase-2 gate prerequisite" / FX5 "Phase-4 FAIL rule" WIRING surface was handed off by R4 to R6/R7 and picked up by neither — task-builder SKILL.md §A.8/§A.10 are the builder's OWN internal gates, not a pr_submit-pytest wiring point. |
| 2 | Actionable for builder (per-symbol) | PASS | file:line density high across all 7 files; concrete symbol names, line numbers, verbatim quotes. |
| 3 | Missing integration points (sync-dev/verify-sync, markers) | FAIL (G5) | Brief edits ARE sync-dev surfaces (R4 §5, R5 §4) — covered. BUT R2's proposed `@pytest.mark.gate_helper` marker is UNregistered (verified: 0 usages, not in pyproject.toml [markers]) and `--strict-markers` is on → CI ERROR; pyproject.toml is not a plan §5 target. |
| 4 | Missing test/verification coverage | FAIL (G1,G2) | FX7 test files identified well (R3 §6). BUT the FX1/FX2 markdown-brief edits have EXISTING structural tests R5 never swept: `test_reviewer_brief_constraints.py`, `test_five_axes_overlay.py`, `test_axis_column_populated.py`. `test_five_axes_overlay.py:28` hardcodes `"#### Checklist (15 items)"` → FX2's 15→16 bump breaks it. |
| 5 | Plan §3 residual risks carried | PASS (strong) | §3.1 (R4 §3c/§6), §3.2 getattr (R1 §5), §3.3 out-of-scan helpers (R2 §4.3), §3.4 FX7 consumers (R3 §5), §3.5 gaming/differential (R2 §5). All explicit. |
| 6 | Additive/advisory guardrails traceable | PARTIAL (G6) | Well-traced (R3 §3.4, R4 §3b/§4a). BUT FX7 additivity is CONTRADICTED between R3 (clean additive builder path) and R7 (not additive, human-decision) — unreconciled. |

## Summary
- Lens checks passed: 2 / 6 (fully); 2 partial; 2 fail
- Gaps found: 7 (CRITICAL-effective: 1 · IMPORTANT: 4 · MINOR: 2)
- Contradictions between research files: 2 (G3 FX2 surface R4↔R7; G6 FX7 additivity R3↔R7)
- Issues fixed in-place: 0 (fix_authorization: false — report only)

---

## Gaps Found

### G1 — [CRITICAL] FX2's researched edit breaks an existing green test (`test_five_axes_overlay.py`)
**Location:** `tests/audit/test_five_axes_overlay.py:28,72` + `src/superclaude/agents/rf-qa-qualitative.md:660`
**What's missing:** R4 recommends FX2 add a new checklist item in the task-qualitative "Code
Compatibility" group and bump the header "Checklist (15 items)" → 16 (R4 §1b/§2, notes count at
:660/:738). Independently verified: `test_five_axes_overlay.py:28` hardcodes
`CHECKLIST_HEADER = "#### Checklist (15 items)"` and `test_checklist_header_present_in_source`
(+ `_in_mirror`) assert it in BOTH the src and the `.claude` mirror; `test_byte_identical_files`
additionally requires src == mirror byte-for-byte. **FX2 as researched will turn this green
test red.** Neither R4 (brief structure) nor R5 (test infra, scoped only to `tests/pr_submit/`)
identified this test. This is the concrete answer to the prompt's item-4 question ("how is a
prose edit's correctness verified with no runtime test?"): there IS a runtime test, and it is an
unflagged regression surface.
**Required fix (carry into research):** FX2's item set MUST include updating
`test_five_axes_overlay.py` `CHECKLIST_HEADER` "15 items"→"16 items" (an UNLISTED target beyond
plan §5 SCOPE) AND running `make sync-dev` so the byte-identical assertion stays green. Add
`tests/audit/test_five_axes_overlay.py` and `tests/audit/test_axis_column_populated.py` to the
FX2 verification/regression set.

### G2 — [IMPORTANT] Verification/regression coverage of the FX1/FX2/skill markdown edits is unresearched
**Location:** `tests/cli/reflect/test_reviewer_brief_constraints.py`, `tests/cli/reflect/test_reviewer_readonly_tools.py`, `tests/audit/test_five_axes_overlay.py`, `tests/audit/test_axis_column_populated.py`, `tests/skills/test_task_builder_merge.py`
**What's missing:** R5 (the "tests & conventions" researcher) scoped ENTIRELY to `tests/pr_submit/`
(FX3/FX5). The FX1 target (`reflect-reviewer.md`) is guarded by
`test_reviewer_brief_constraints.py` (asserts the `## Constraints (READ-ONLY)` section, the
read-only/no-shell/git-mutation language, and cross-file rotation-table consistency) and
`test_reviewer_readonly_tools.py`. The FX2 target (`rf-qa-qualitative.md`) is guarded by the
`test_five_axes_overlay.py` axis/ordering/count/byte-identical suite. These tests are BOTH the
verification mechanism for the prose edits AND a regression risk. The builder needs them named as
the FX1/FX2 acceptance gate.
**Required fix:** Add a research note enumerating these brief-guarding tests as the FX1/FX2
verification surface; FX1 must preserve the asserted anchors in `reflect-reviewer.md` (READ-ONLY
section, rotation tables) — the advisory correctness sub-section (R4 §3c) must be additive to
Output Format without disturbing them.

### G3 — [IMPORTANT] Unresolved contradiction: FX2 target surface (R4 vs R7)
**Location:** research 04 §CRITICAL-FRAMING + §1b vs research 07 Deliverable 6
**What's contradicted:** R4 says augment the task-qualitative **Code Compatibility** group in
`rf-qa-qualitative.md` (new item after item 6). R7 says `rf-qa-qualitative` is a **document-QA
agent** that "does NOT review Python code modules," so grafting a Python cross-symbol lens is a
scope mismatch — use `rf-qa` or a new code lens instead. **I independently verified
`rf-qa-qualitative.md:670-676`:** the task-qualitative phase DOES contain a "Code Compatibility"
group (item 4 Function-signature verification, item 5 Module-context analysis, item 6
Downstream-consumer analysis) plus a "Test and Verification Quality" group — i.e. it already
reviews code. **R4 is the better-supported position; R7's "does not review Python code" is
overstated** (R7 read only the document-oriented phases + the `internal-consistency` occurrences,
not the task-qualitative Code Compatibility group). Per QA rule 6, I surface rather than silently
resolve: the builder MUST be handed R4's surface as the decision, with R7's scope-expansion
caveat noted, else FX2 risks landing in the wrong agent.

### G4 — [IMPORTANT] FX3 "Phase-2 gate prerequisite" / FX5 "Phase-4 FAIL rule" wiring is a dropped handoff
**Location:** plan §2 fix table ("wire into RF Phase-2 as a gate prerequisite" / "Phase-4 FAIL
rule in agents/rf-qa-qualitative.md"); research 04 §2 (handoff to R6/R7); research 06 (did not pick up)
**What's missing:** R4 correctly flagged that the literal "Phase 2"/"Phase 4" pipeline numbers
live in `task-builder/SKILL.md` (out of R4's 3-file scope) and handed off to R6/R7. R6 researched
`task-builder/SKILL.md` but only for gate-ENCODING rules (I18 L3 test items, I19/I20 agent counts,
POST wrapper) — **it did not map FX3→"Phase-2 gate prerequisite" or FX5→"Phase-4 FAIL rule" to a
concrete edit.** Verified: SKILL.md §A.8 is the builder's "Research Quality Gate" and §A.10 is
"Task File Validation" — these are the TASK-BUILDER's own internal QA gates, not a place a
pr_submit pytest attaches. So the plan's "gate prerequisite" language has three undisambiguated
readings: (a) CI/`make test` regression guard, (b) a built-task L3 pytest item (R6 I18), or (c) an
actual SKILL.md gate-wiring edit. R5 §3 leans (a)+(b); R4 §2 maps FX5's FAIL-rule to the
rf-qa-qualitative Verdict block form (:732-735) — partial coverage — but no researcher pins the
plan's exact "Phase-2 prerequisite" instruction to an actionable location.
**Required fix:** Disambiguate. Most defensible: FX3/FX5 are pytest regression guards executed as
L3 test items in the built task and by CI; drop the "RF Phase-2/Phase-4 gate" framing OR pin the
exact SKILL.md/agent edit if a real gate-wiring change is intended.

### G5 — [IMPORTANT] FX5 custom marker collides with --strict-markers; pyproject.toml is an unlisted target
**Location:** research 02 §4.1 step 3 (`@pytest.mark.gate_helper(...)`) vs research 05 §4 (--strict-markers); `pyproject.toml:114-145`
**What's missing:** R2 proposes enumerating helper coverage via a
`@pytest.mark.gate_helper("candidate._path_resolves")` convention. Verified: `gate_helper` has
zero usages and is NOT in `pyproject.toml [markers]` (114-145); R5 confirmed `--strict-markers`
is active → an unregistered marker is a **collection ERROR in CI**, not a soft warning. Neither
researcher connected R2's marker proposal to R5's rule. Also `pyproject.toml` is NOT among the
plan §5 SCOPE target files, so registering the marker adds an unlisted edit target.
**Required fix:** Either (a) implement FX5 with the marker-free `pytest_generate_tests` /
parametrize approach (R5 Option A/B — recommended, keeps the target set to §5), or (b) add
`pyproject.toml` as an explicit target and register `gate_helper` in [markers].

### G6 — [IMPORTANT] Unreconciled contradiction: is FX7 additive or a human-decision item? (R3 vs R7)
**Location:** research 03 §2c/§3.4/§7 vs research 07 "FX7 CONTRADICTS an existing deliberate exemption"
**What's contradicted:** R7 concludes FX7 ("verification_ran:false ⇒ degraded") is **NOT purely
additive** because it collides with the deliberate `_VERIFICATION_SKIP_EXEMPTIONS` (incl.
`tool-unavailable`) at `contract.py:35-38,287-291`, and recommends flagging it for a **human
decision**. R3 offers a **clean additive path** (change what the ENSEMBLE BUILDER emits at
`ensemble.py:551` for the ensemble case, keeping the consumer exemption set intact) that preserves
additivity. These are not the same recommendation. Given the project rule that human-decision
items must HALT (not auto-default) and the "additive only" BUILD_REQUEST constraint, the builder
needs a decisive resolution: is FX7 a `needs_human_decision` HALT item, or the R3 additive
builder-only edit? R3's path likely resolves R7's concern, but that reconciliation is not stated
in either file.
**Required fix:** Reconcile explicitly. If R3's builder-scoped path is adopted, document that FX7
stays additive by NOT touching `_VERIFICATION_SKIP_EXEMPTIONS` and by emitting an honest skip
reason/degrade signal only in the ensemble builder; otherwise mark FX7 `needs_human_decision`.

### G7 — [MINOR] start_commit audit base interacts with R7's branch correction (HL-1) — unaddressed
**Location:** research 06 §1a (`start_commit = git merge-base HEAD <integration-branch>`) vs research 07 HL-1
**What's missing:** R6 prescribes `start_commit = git merge-base HEAD <integration-branch>` for the
POST reflect wrapper's audit base, without R7's finding that `contract_setup` + `tests/pr_submit`
exist ONLY on this branch / `DetectionContractBranch` lineage and are ABSENT from `origin/master`.
A merge-base against `origin/master` would place the entire `contract_setup` package (15 files) in
the audited diff (the diff-scope footgun), swamping the reflect audit. The correct base must be the
harden branch's immediate parent so only the FX task edits are audited.
**Required fix:** Set `start_commit` to the tight parent (e.g. merge-base with the DetectionContract
lineage tip / the branch's own base), NOT `origin/master`; note R7 HL-1 in the frontmatter rationale.

### G8 (bookkeeping) — [MINOR] research/01 has a stale status header
**Location:** `research/01-fx3-questions-resolution.md:3` ("Status: In Progress") vs `:353` ("Status: Complete")
File 01 carries contradictory status markers. Body is complete; the line-3 header is stale.
Trivial, but a file-inventory check flags it — normalize to "Complete".

---

## Recommendations (before synthesis / task build)
1. **G1/G2 (must-do):** Add the brief-guarding tests to the FX1/FX2 scope — update
   `test_five_axes_overlay.py` CHECKLIST_HEADER 15→16, run `make sync-dev` (byte-identical test),
   and name `test_reviewer_brief_constraints.py` as the FX1 acceptance/regression gate. These are
   the "no runtime test" answer: there ARE runtime tests over the briefs.
2. **G3/G6 (contradictions):** Hand the builder decisive answers — FX2 → R4's task-qualitative
   Code Compatibility surface (R7's blanket "document-only" claim is overstated per verified
   :670-676); FX7 → R3's additive builder-only path OR an explicit `needs_human_decision` HALT.
3. **G4:** Drop or concretely pin the "RF Phase-2/Phase-4 gate" framing for FX3/FX5 (default:
   L3 pytest items + CI regression guards).
4. **G5:** Prefer the marker-free parametrize implementation for FX5, or add pyproject.toml as a
   target and register `gate_helper`.
5. **G7:** Pin `start_commit` to the branch's tight parent, not `origin/master`.

---

## Confidence
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 9 (via 4 Bash batches) | Glob: 0 | Bash: 4
- No web research required (all claims are local source-truth / test-suite facts).
- Every gap above is backed by a specific tool observation: rf-qa-qualitative.md:660-676 read
  (G3), `test_five_axes_overlay.py:28,72` grep (G1), tests/ sweep for brief refs (G2),
  SKILL.md §A.8/§A.10 grep (G4), pyproject.toml [markers] + gate_helper zero-usage grep (G5).
- Ran in parallel with rf-analyst (analyst reports present in qa/ but NOT relied upon —
  verified independently per zero-trust).

## QA Complete
