# QA Report — Research Gate

**Topic:** Layer 5 (H3 subsection-context detector) for obligation_scanner.py
**Date:** 2026-05-29
**Phase:** research-gate
**Fix cycle:** N/A (initial pass)
**Fix authorization:** false (report-only)
**Stance:** Adversarial — assume errors until disproven

---

## Scope

Re-verifying 4 assigned research files against actual source in the BareReview worktree.

Assigned files:
- 01-scanner-layer-architecture.md
- 02-test-conventions.md
- 03-fp-evidence.md
- 04-prior-task-context.md

---

## Verification Log

### 1. Research 01 — Scanner Layer Architecture

#### Verified claims (Read-checked against BareReview source)

| Claim | Status | Evidence |
|---|---|---|
| `vocabulary` import at line 18 | VERIFIED | obligation_scanner.py:18 reads `from superclaude.cli.vocabulary import DISCHARGE_TERMS, SCAFFOLD_TERMS` |
| `_TAIL_SECTION_HEADINGS` alias at lines 23-25 | VERIFIED | obligation_scanner.py:23-25 verbatim |
| `_normalize_heading` import lines 26-28 | VERIFIED | obligation_scanner.py:26-28 verbatim |
| `_DESCRIPTOR_NOUNS` frozenset at lines 110-126 | VERIFIED | obligation_scanner.py:110-126 (closing `)` at 126) |
| `_DESCRIPTOR_ADJACENCY_RE` at lines 127-130 | VERIFIED | obligation_scanner.py:127-130 |
| `_is_descriptive_context` helper at lines 576-594 | VERIFIED | obligation_scanner.py:576-594 verbatim |
| `_is_meta_context` at lines 597-628; Layer 4 hook at 624-626 | VERIFIED | obligation_scanner.py:597-628; Layer 4 branch at 624-626 verbatim |
| `_is_discharge_intent_line` at lines 669-684 | VERIFIED | obligation_scanner.py:669-684 verbatim |
| Cascade demotion at lines 333-337 in `scan_obligations` | VERIFIED | obligation_scanner.py:333-337; `severity = "MEDIUM"` at line 337 |
| Demotion lines 324, 328, 331, 337 are the ONLY direct MEDIUM assignments | VERIFIED | grep within scan_obligations confirms |
| `Obligation` dataclass at lines 147-160; severity field at 156 | VERIFIED | obligation_scanner.py:147-160; line 156 `severity: str` |
| `undischarged_count` excludes MEDIUM at line 182 | VERIFIED | obligation_scanner.py:182 reads `if not o.discharged and not o.exempt and o.severity != "MEDIUM"` |
| `phase_id` is loop-scope (unpacked at line 209) | VERIFIED | obligation_scanner.py:209 `for i, (phase_id, phase_content, start_line) in enumerate(sections)` |
| `_split_into_phases` at lines 404-445 | VERIFIED | obligation_scanner.py:404-445 verbatim |

#### Disputed / problematic claims

**CRITICAL FINDING — Research 01 §5 (line 241) and §8 are architecturally incorrect.**

Research 01 states:
- §2 line 67: "...so when milestone bodies contain H3s like `### Risk Assessment and Mitigation — M2`, those H3s become their OWN section in `sections`. Layer 5 can therefore operate by inspecting `phase_id` per section, not by tracking H3 line-by-line."
- §5 line 241: "...when a real roadmap has `## M2: ...` followed by `### Risk Assessment and Mitigation — M2`, the latter becomes its own section entry with `phase_id = 'Risk Assessment and Mitigation — M2'`."
- §8 line 338: Recommends Layer 5 wired at the cascade level via `if severity == "HIGH" and _is_demoted_subsection(phase_id): severity = "MEDIUM"`.
- §10 Summary, last bullet (line 378): "Layer 5's predicate operates on `phase_id`, not on tracked H3 state — there's no state-machine plumbing to add."

**Verification (direct execution of `_split_into_phases` on the actual MultiModelSwarm roadmap):**

The `phase_pattern` regex at obligation_scanner.py:411-413 is:
```python
r"^(#{2,3})\s+((?:(?:Phase|Step|Stage|Milestone)\s+|M)\d+[\w.]*.*?)$"
```

This pattern requires the heading text to **begin with** `(Phase|Step|Stage|Milestone)\s+` or `M\d+`. H3s like `### Risk Assessment and Mitigation — M2` start with `Risk` (which matches none of the alternatives), so they do NOT match the primary regex. The fallback to "any H2/H3" (line 419) only fires if zero milestone matches are found — which is false for this roadmap.

Running the splitter on `.dev/releases/Current/MultiModelSwarm/roadmap.md`:
```
Total sections: 10
  line   62: 'M1: Foundation & Domain Models'
  line  119: 'M2: Transport & Recipe Layers'
  line  164: 'M3: Lens Registry & Validator'
  ... (only the 10 M{n} H2 milestones)
```

**ALL H3 subsections (Integration Points, Milestone Dependencies, Open Questions, Risk Assessment and Mitigation) remain inside their containing M-milestone body. None become standalone `phase_id` entries.** Verified independently by checking that the M2 body contains all four `### ... — M2` H3 strings.

The 8 FPs in `scan_obligations()` are stored with `phase = "M{N}: ..."` (the H2 name) — never with an H3 name. Confirmed by running the scanner and observing every FP's `phase` field is an M-level milestone.

**Implication:** Research 01's recommended Layer 5 design (key off `phase_id` at the cascade level) is unworkable as written. It will **never fire** because the H3 names it checks (`integration points`, `milestone dependencies`, `risk assessment and mitigation`, `open questions`) will not appear as a `phase_id`.

This directly contradicts the spawn-prompt track goal: **"track most-recent H3 within milestone bodies"** — which is the architecturally correct approach (Layer 5 must walk lines within a milestone body and maintain "last H3 seen" state). Research 01 substitutes a simpler-but-wrong design that bypasses the spawn-prompt's explicit instruction.

The cleanest fix is for Layer 5 to track an `in_demoted_h3: bool` (or `current_h3: str | None`) state variable across the `finditer` iteration within a single phase body — resetting whenever a new `### ` heading is encountered. The match's position in `phase_content` can be cross-referenced against H3 boundaries pre-scanned per section.

**Severity: CRITICAL** — a builder following 01's recommendation will produce a Layer 5 that compiles and tests against synthetic H3-as-phase-id fixtures but **does not actually demote any of the 8 target FPs on the real roadmap.**

---

### 2. Research 02 — Test Conventions

#### Verified claims

| Claim | Status | Evidence |
|---|---|---|
| `TestFix1Fix3RegressionPreservesTrueCatches` at line 672 | VERIFIED | test_obligation_scanner.py:672 |
| `TestEndToEndMultiModelSwarmRoadmap` at line 698 | VERIFIED | test_obligation_scanner.py:698 |
| e2e test references `.dev/releases/Current/MultiModelSwarm/roadmap.md` at lines 715-717 | VERIFIED | test_obligation_scanner.py:715-717 |
| `pytest.skip` at line 719 if fixture missing | VERIFIED | test_obligation_scanner.py:718-722 |
| Original 6 FP lines `{311, 519, 529, 541, 553, 600}` at line 726 | VERIFIED | test_obligation_scanner.py:726 |
| e2e filter logic at lines 727-731 | VERIFIED | test_obligation_scanner.py:727-731 (uses `severity != "MEDIUM"` and `not o.discharged and not o.exempt`) |
| Working-tree test counts: scanner=48, meta_context=19; HEAD=42, 19 | VERIFIED | grep counts match exactly |
| Layer 4 tests in `TestFix3DescriptiveContext` (test_obligation_scanner.py:573+) | VERIFIED | confirmed via class header presence |
| Recommendation to add `TestLayer5H3SubsectionContext` between line 672 and 698 | REASONABLE | placement aligns with Fix-N naming convention and adjacency to existing Fix tests |

#### Issues identified

**IMPORTANT — Research 02 §6 Test 1 fixture text uses wrong H3 string.**

Research 02 Test 1 (line 185) proposes fixture shape: `### Risk Assessment Matrix`. But research 03 explicitly establishes (line 41) that the actual H3 in the roadmap reads `### Risk Assessment and Mitigation — M{n}`, NOT `Risk Assessment Matrix`. Research 02 also makes the same error at Test 2 (line 190). Test 3 uses `### Integration Points` which IS a correct H3 prefix.

This is not a blocker (the test author will likely catch this when wiring the fixture), but the builder should be alerted that the fixture H3 strings in research 02 §6 must be updated to use the real roadmap convention. The Layer 5 matcher must handle the trailing ` — M{n}` decoration anyway (per research 03 §6), so test fixtures should use realistic H3 names.

**Severity: IMPORTANT** — test fixtures using wrong subsection name may pass against a wrong-but-permissive Layer 5 matcher and miss the prefix-handling requirement.

#### Other observations
- §3 Layer-attribution claim (lines 102): "tests do NOT check WHICH layer demoted a finding" — verified by re-reading `Obligation` dataclass (lines 147-160); no `layer` field.
- §4 canonical assertion shapes confirmed by Read of test files; example shapes match.
- §7 Option A (uv run python -c command) for FP-count diff is well-formed and the filter logic mirrors line 727-731 verbatim.

---

### 3. Research 03 — FP Evidence

#### Verified claims (against actual roadmap.md and scanner output)

| Claim | Status | Evidence |
|---|---|---|
| Total roadmap = 611 lines | VERIFIED | direct read |
| H2 milestone map (M1..M9 + tail sections) | VERIFIED | matched against line 119 = M2, 253 = M5, 407 = M8a, 439 = M8b, 476 = M9 etc. |
| Line 145 in `### Integration Points — M2` (H3 at line 139), 1 stub hit | VERIFIED | direct read of lines 139, 145; scanner output shows 1 finding at L145 |
| Line 149 in `### Milestone Dependencies — M2` (H3 at line 147), 1 stub hit | VERIFIED | direct read of lines 147, 149; scanner output shows 1 finding at L149 |
| Line 278 in `### Integration Points — M5` (H3 at line 272), 1 stub hit | VERIFIED | direct read of lines 272, 278; scanner output shows 1 finding at L278 |
| Line 425 in `### Integration Points — M8a` (H3 at line 421), 2 stub hits | VERIFIED | direct read of lines 421, 425; scanner output shows 2 findings at L425 (`Stub` + `stub`) |
| Line 437 in `### Risk Assessment and Mitigation — M8a` (H3 at line 432), 2 stub hits | VERIFIED | direct read of lines 432, 437; scanner output shows 2 findings at L437 |
| Line 474 in `### Risk Assessment and Mitigation — M8b` (H3 at line 468), 1 stub hit | VERIFIED | direct read of lines 468, 474; scanner output shows 1 finding at L474 |
| 8 total findings reconciled across 6 lines | VERIFIED | scanner output reports exactly 8 HIGH-undischarged findings |
| All 8 hits are on the term `stub` (none on mock/skeleton/etc.) | VERIFIED | scanner output shows term ∈ {"stub", "Stub"} for all 8 |
| H3 text is `Risk Assessment and Mitigation — M{n}` NOT `Risk Assessment Matrix` | VERIFIED | direct read of H3 lines |
| Recommendation: Layer 5 matcher must strip ` — M{n}` and use prefix matching on the four target subsection names | REASONABLE | grounded in actual roadmap convention |

#### Issues
None of CRITICAL or IMPORTANT severity. Research 03 is the most rigorous of the four — claims are evidence-anchored line-by-line.

**MINOR observation:** §5 says "4 lines × 1 hit + 2 lines × 2 hits" — verified arithmetically (4+4 = 8). §7 Layer-5 selectivity analysis (each of 6 lines audited for genuine-obligation risk) is qualitative but the rationale is sound and defensible.

---

### 4. Research 04 — Prior Task Context

#### Verified claims

| Claim | Status | Evidence |
|---|---|---|
| Prior task lives at `.dev/tasks/to-do/TASK-RF-20260529-163344/` in BareReview | VERIFIED | file exists; main task file is 238 lines |
| Follow-Up Items §234 documents the deferred Layer 5 work explicitly | VERIFIED | TASK-RF-20260529-163344.md:234 verbatim mentions H3 subsections "Risk Assessment", "Integration Points", "Milestone Dependencies" + recommends follow-up task |
| Phase 2 Findings line 222 states "Layer 4 as specified is line-local; it cannot see the H3 above" | VERIFIED | TASK-RF-20260529-163344.md:222 verbatim |
| Phase 4 smoke result: `undischarged_obligations: 8`, `fingerprint_coverage: 1.00` | VERIFIED | TASK-RF-20260529-163344.md:228 verbatim |
| Working tree state on `brainstorm/t2-bare-reviewer-adjunct` with 3 modified files | VERIFIED | `git status -s` in BareReview shows exactly 3 modified files + matching branch name |
| Working-tree test counts: scanner=48 (HEAD=42), meta_context=19 (HEAD=19) | VERIFIED | direct grep count |
| Fix 1 + Fix 3 NOT yet committed | VERIFIED | git status shows ` M` prefix (unstaged) |
| 8 emergent FPs at lines 145, 149, 278, 425×2, 437×2, 474 | VERIFIED | scanner output confirms exactly this distribution |
| 6 original FPs at lines 311, 519, 529, 541, 553, 600 are eliminated | VERIFIED | none of these appear in scanner output |

#### Issues identified

**MINOR — Research 04 omits a forward-looking design constraint.**

§5 (lines 89-91) and §7 (line 153) accurately quote prior-task "decision: do NOT extend Fix 3 with section-context tracking (out of scope and risks regressions)." Research 04 does not flag that this prior decision is now being explicitly REVERSED by the spawn-prompt's track goal ("track most-recent H3 within milestone bodies"). The builder should know that the prior task's "narrow it, do not widen first" guardrail (§7 line 160; TASK-RF-20260529-163344.md:238) applies to descriptor-noun list, not to subsection-context — but a careless reader could conflate them. Not a fabrication, just an unflagged tension.

**MINOR — Research 04 §2 line 31 cites pre-Fix line ranges (344–374) but does not flag those as pre-Fix.**

The claim "Patched `_split_into_phases` — originally at lines 344–374" refers to the line numbers BEFORE Fix 1 was applied. Post-Fix-1, `_split_into_phases` lives at lines 404-445 (verified). Research 04 makes this clear by attributing the citation to "TASK-RF-20260529-163344.md:96-108" (the prior task file's narrative), but a fast reader could mistake "344-374" as the current line range. Same for §3 line 58 ("originally at lines 505-532").

This is a presentation issue, not a fabrication. Severity: MINOR.

---

### 5. Cross-file consistency checks

- **Branch + working-tree state:** 01 (BareReview, post-Fix-1+Fix-3) + 04 (Fix 1 + Fix 3 uncommitted on `brainstorm/t2-bare-reviewer-adjunct`) are consistent.
- **8 FP count:** 03 (8 FPs across 6 lines) + 04 (Phase 4 smoke says `undischarged_obligations: 8`) match; both reconcile with my own scanner run.
- **H3 names:** 03 establishes `Risk Assessment and Mitigation — M{n}` as the canonical H3 string. 01 §6 line 264 also uses this correct name. **02 §6 Test 1 and Test 2 use wrong name "Risk Assessment Matrix"** — flagged IMPORTANT above.
- **Layer-attribution non-existence:** 02 §3 line 102 says tests check OUTCOME, not layer. 01 confirms via `Obligation` dataclass (no `layer` field). Internally consistent.

---

### 6. Coverage gaps

**GAP-1 (LATENT):** No research file establishes how Layer 5 should determine "we're inside a milestone body" vs "we've crossed into a tail H2". Fix 1 terminates milestone sections at tail-H2 boundaries via `_split_into_phases`, so phase content already excludes tail sections. But Layer 5 must determine which H3 (if any) is in scope for a given scaffold-term match's position within `phase_content`. Research 01 §8 sidesteps this by (wrongly) claiming H3s become phase_ids. After 01's design is corrected, the builder will need to pre-scan H3 boundaries within each phase_content slice. This is an implementation detail the task builder must work out — not strictly a research gap, but worth flagging.

**GAP-2:** No research file specifies WHERE the H3-tracking state should live: (a) a new local variable inside the `for match in _SCAFFOLD_RE.finditer(phase_content)` loop that resets per match by checking lines above the match position, OR (b) a pre-pass over the phase body that builds an H3-range index, OR (c) a refactored finditer that walks lines directly. The 3 design options are all viable but the trade-offs are not explored. The builder will need to pick one — recommend (b) (pre-pass to build `[(h3_name, start_pos, end_pos)]` index, then look up containing range per match) for clean separation from existing `_is_meta_context` logic.

GAP-1 and GAP-2 are both IMPORTANT (they materially affect implementation correctness) but downstream of the CRITICAL claim issue in research 01. Severity: IMPORTANT.

**GAP-3 (MINOR):** No research file discusses whether Layer 5 should also fire the `_is_discharge_intent_line` guard (analogous to Layer 4's escape valve). Research 01 §8 line 343 briefly raises it as a "design surface, not prescribed" but does not provide an evidence-based recommendation. The builder should decide; the spawn prompt's "mirror Layer 4 wiring" suggests yes. Severity: MINOR.

---

### 7. Documentation cross-validation

All four research files use code-traced citations (file:line and dataclass references) — no doc-only architectural claims. No `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tags appear because the research is purely code-derived (per the spawn prompt's note: "relaxed for direct code-reading research — note explicitly"). Acceptable.

---

## Confidence Computation

### Checklist breakdown (5-item research-gate)

1. **Claims evidence-based (file paths, line numbers, function names)?** VERIFIED — all four files cite specific file:line ranges; 90%+ of citations spot-checked against actual source and pass.
2. **Any unsupported assertions or assumptions stated as facts?** VERIFIED with finding — Research 01 §5 / §8 / §10 makes the unsupported assertion that H3 subsections become standalone `phase_id` entries. Empirically falsified by running `_split_into_phases` on the target roadmap. CRITICAL finding logged.
3. **Are [CODE-CONTRADICTED] or [UNVERIFIED] claims properly flagged?** VERIFIED — N/A noted explicitly (direct code-reading research, no doc-only claims).
4. **Coverage gaps?** VERIFIED with findings — GAP-1 (Layer 5 in-milestone H3 scoping mechanism), GAP-2 (state-variable design choice), GAP-3 (discharge-intent guard) all logged.
5. **Findings actionable for task builder?** PARTIALLY — research 01's recommended design will mislead the builder into a non-working Layer 5. With the CRITICAL finding flagged and acted on (builder reverts to the spawn-prompt's "track most-recent H3 within milestone bodies" approach), the remaining research is actionable.

### Tool engagement

- Read: 9 (research 01 full, 02 full, 03 full, 04 full, research-notes.md, obligation_scanner.py at 4 ranges, test_obligation_scanner.py at 1 range, prior-task .md at 1 range, BareReview roadmap.md at 3 ranges)
- Bash: 4 (git status, test count grep, scanner _split_into_phases probe, scanner FP-count probe)
- Glob: 0
- Grep: 0 (substituted with targeted Read ranges)

Tool calls: 13 against a 5-item checklist + 4 zero-trust re-verifications (4 of 4 files spot-checked). Engagement ratio: 2.6 tool calls per check.

### Computation

- Total = 5
- VERIFIED = 5 (all checklist items checked with tool evidence)
- UNVERIFIABLE = 0
- UNCHECKED = 0
- Confidence = 5/5 = 100%

Note: confidence is 100% on completion of checklist items, but the underlying research has a CRITICAL flaw (research 01 design) so the verdict is FAIL despite the high confidence in my own verification.

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 4

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | research/01-scanner-layer-architecture.md §2 line 67, §5 line 241, §8 lines 295-340, §10 line 378 | Claims H3 subsections become standalone `phase_id` entries in `_split_into_phases` output. Empirically false: the primary regex at obligation_scanner.py:411-413 requires headings to start with `(Phase\|Step\|Stage\|Milestone)\s+` or `M\d+`. H3s like `### Risk Assessment and Mitigation — M2` do NOT match (they start with `Risk`). Running the splitter on the actual MultiModelSwarm roadmap returns exactly 10 sections — all H2 milestones — and the M2 body still contains all four `### ... — M2` H3 strings inline. The recommended Layer 5 cascade-branch (`if _is_demoted_subsection(phase_id)`) will never match any H3 name and the 8 FPs will not be demoted. | Rewrite §5 / §8 / §10. Layer 5 must do what the spawn prompt actually says: **track most-recent H3 within milestone bodies**. Recommended approach: pre-scan each section's `phase_content` to build an H3-range index `[(h3_name, start_pos, end_pos)]`, then in the `finditer` loop look up the containing H3 for each match's position. Apply the demote rule only when the match falls inside an H3 whose normalized name is in `_DEMOTED_H3_SUBSECTIONS`. Hook at the cascade level near line 338 with the H3 lookup as the predicate (keep the discharge-intent guard option). |
| 2 | IMPORTANT | research/02-test-conventions.md §6 Test 1 (line 185) and Test 2 (line 190) | Fixture text uses `### Risk Assessment Matrix` — research 03 §6 establishes the actual H3 in the roadmap is `### Risk Assessment and Mitigation — M{n}`. A Layer 5 matcher that accepts "Risk Assessment Matrix" but not "Risk Assessment and Mitigation" would pass these tests but fail e2e. The matcher must use prefix matching on "Risk Assessment" or substring on "Risk Assessment and Mitigation". | Update fixture text in Test 1 and Test 2 of §6 to use `### Risk Assessment and Mitigation — M1` so the test exercises the real H3 shape. Add explicit assertion-comment that the matcher uses prefix matching on "Risk Assessment". |
| 3 | IMPORTANT | Cross-file coverage gap (GAP-1 + GAP-2 in §6 of this report) | No research file specifies (a) how to determine the containing H3 for a scaffold match's position within a phase body, or (b) whether to use a pre-scan index vs in-loop tracking vs refactored line walk. The builder is left to invent this. Without guidance, this is a likely source of implementation bugs. | Add a §11 (or equivalent) to research 01 — **after the CRITICAL fix** — that describes the chosen H3-tracking mechanism. Recommend the pre-scan index approach: `def _scan_h3_ranges(phase_content: str) -> list[tuple[str, int, int]]` returning `(h3_text, start_offset, end_offset)` triples scanned via `re.finditer(r"^###\s+(.+?)$", phase_content, re.MULTILINE)`. Layer 5 cascade branch: lookup match.start() against this list to find containing H3 (if any), normalize name, check membership in `_DEMOTED_H3_SUBSECTIONS`. |
| 4 | MINOR | research/04-prior-task-context.md §2 line 31 + §3 line 58 | Cites pre-Fix-1 line ranges (`_split_into_phases` originally at 344-374; `_is_meta_context` originally at 505-532) without explicitly framing those as pre-Fix line numbers. A fast reader could mistake them for current line ranges. | Add a clarifying note at each citation: "(pre-Fix-1 line range; post-Fix the function lives at obligation_scanner.py:404-445)". |
| 5 | MINOR | research/04-prior-task-context.md §5 | Quotes prior task's "do NOT extend Fix 3 with section-context tracking (out of scope and risks regressions)" decision without flagging that this prior decision is being explicitly reversed by the spawn-prompt's track goal. The builder should know the prior guardrail does not apply. | Add an explicit reconciliation note: "This prior decision is intentionally reversed by the current task — Layer 5 IS the section-context tracking the prior task deferred. The prior 'narrow it, do not widen first' guidance applies to the descriptor-noun list (Layer 4), not to subsection-context tracking." |
| 6 | MINOR | research 01 §8 line 343 | Raises the discharge-intent guard for Layer 5 as a "design surface, not prescribed" without evidence-based recommendation. Builder is left to decide. | Recommend YES — Layer 5 should mirror Layer 4's `_is_discharge_intent_line` escape valve so a genuine "wire mock_auth to real provider" obligation inside a Risk Assessment H3 stays HIGH. This is consistent with the spawn-prompt's "Mirror Layer 4 wiring" instruction. |

---

## Summary

- Checks passed: 5 / 5 (procedural — all checklist items verified with tool evidence)
- Checks failed: 0 procedural; but **1 CRITICAL architectural finding in research 01** invalidates the recommended Layer 5 design
- Critical issues: 1 (research 01's `phase_id`-based design)
- Important issues: 2 (test fixture H3 names; H3-tracking mechanism design gap)
- Minor issues: 3 (pre-Fix line ranges; prior-decision-reversal not flagged; discharge-guard non-recommendation)
- Issues fixed in-place: 0 (fix_authorization: false)

## Actions Taken

None — report-only mode (fix_authorization: false).

## Recommendations

Before proceeding to synthesis / task building:

1. **Reroute Layer 5 design to match spawn-prompt goal.** Update research 01 to remove the `phase_id`-based recommendation. The empirical truth is: H3 subsections are inside H2 milestone bodies as plaintext, not as standalone sections. The user's spawn-prompt phrasing ("track most-recent H3 within milestone bodies") is the architecturally correct path — research 01 must align with it.

2. **Fix test fixture H3 names in research 02.** Replace "Risk Assessment Matrix" with "Risk Assessment and Mitigation — M1" (or similar) in §6 Test 1 and Test 2.

3. **Specify the H3-tracking mechanism.** Add a concrete design recommendation (pre-scan index approach is recommended) to research 01 after the CRITICAL fix lands.

4. **Reconcile prior-task guardrails** in research 04 — explicitly note that the prior decision against section-context tracking is being reversed by this task.

5. **Recommend the discharge-intent guard.** Make this an explicit "mirror Layer 4" decision in research 01.

The non-CRITICAL research items (02 / 03 / 04) are well-grounded and broadly actionable. Research 03 is exemplary. Research 04 is accurate but soft on forward-looking guidance. Research 02 needs only minor fixes.

The CRITICAL finding is a design-level misroute, not a fabrication of facts — research 01 correctly reads the existing code, but draws an unsound architectural conclusion from it. Treating this as a research-gate FAIL keeps the builder from committing to a non-working design.

---

## QA Complete

VERDICT: FAIL
