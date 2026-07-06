# Research Completeness Verification — BREADTH Lens

**Topic:** Template-02 MDTM task additively hardening RF QA + /sc:reflect vs PR #209 spec-conformant bug class (F1-F4)
**Fixes in scope:** FX3 (AST field-resolution test, P0 det), FX5 (negative/differential gate-helper mandate, P0 det), FX7 (honest degrade accounting, P0 det), FX2 (cross-symbol invariant lens, P1 LLM), FX1 (advisory no-spec oracle slot, P1 LLM ADVISORY)
**Lens:** BREADTH — does every fix have research coverage sufficient to write per-file/per-symbol checklist items?
**Date:** 2026-07-03
**Analyst:** rf-analyst (completeness-verification, single instance)

---

## Method

Reading all 7 assigned research files, then spot-verifying 3-4 cited symbols against worktree code. Nine breadth criteria evaluated PASS/FAIL with evidence. Verdict at end.

---

## Spot-Verification of Cited Symbols (adversarial, done by this analyst)

Read the actual worktree source for 4 cited symbols to confirm the research is not fabricating line numbers.

| # | Cited symbol | Claim source | Actual code | Verdict |
|---|-------------|-------------|-------------|---------|
| 1 | `contract.py:35-38` `_VERIFICATION_SKIP_EXEMPTIONS` = `{read-only-project, tool-unavailable, --no-verify}` | 03 §3a, 07 FX7 | Exactly lines 35-38, verbatim frozenset + comment. `_LOAD_BEARING_BOOL_FIELDS` incl. `verification_ran` at 47-57 as claimed. | **VERIFIED** |
| 2 | `candidate.py:360` `_path_resolves`, all-None list collapse fix | 02 §2.1, 07 D4 | Sig at 360; list-comp `is not None` filter 372-376; `if current in (None, []): return False` guard at 379. Fix-comment 369-371. Matches. | **VERIFIED** |
| 3 | `rf-qa-qualitative.md:670-676` Code Compatibility group (items 4/5/6) | 04 §1b, FX2 home | `##### Code Compatibility` at 670; items 4 (Function signature), 5 (Module context), 6 (Downstream consumer) at 672/674/676 verbatim. FX2 "insert after item 6" anchor confirmed. | **VERIFIED** |
| 4 | `questions.py` SetupAnswers 17 fields; `probe_pr` L19; `augment_app_slug` L28 (no `pr_number` field) | 01 §1, 07 D3 | 17 fields confirmed; `probe_pr:int` at 19; `augment_app_slug` at 28 with the exact "not tunnelled through decline_detection_fields" comment; no `pr_number` field exists. | **VERIFIED** |

**All 4 spot-checks pass.** Line numbers, symbol names, and semantic claims are accurate. Notably, R7 (file 07) independently cross-validates R1-R6's claims and tags each CODE-VERIFIED/CONTRADICTED/UNVERIFIED — the research corpus is self-checking, which materially raises confidence.

---

## Per-Criterion Breadth Assessment

### Criterion 1 — Source files identified with paths + exports for each fix? **PASS**
Every fix has a full symbol inventory:
- **FX3** → `questions.py`: 17 `SetupAnswers` fields + 13 `EvidenceBundle` attrs + all 16 `SETUP_QUESTIONS` derivers with per-row resolution trace (01 §1-3).
- **FX5** → 4 modules with complete helper tables: lockgate 14, candidate 18, diagnosis 14, validation 11, each with signature·line·purpose·load-bearing flag (02 §1).
- **FX7** → `cli/reflect/{ensemble.py, contract.py, runner.py, models.py}` with exact line-level targets (03 §1-4).
- **FX2** → `rf-qa-qualitative.md` Code Compatibility group, exports enumerated (04 §1).
- **FX1** → `reflect-reviewer.md` + `deviation-taxonomy.md`, structure enumerated (04 §3-4).

### Criterion 2 — Output paths/formats clear (new test files, brief edit anchors, contract fields)? **PASS**
- FX3: new file `tests/pr_submit/test_setup_questions_resolution.py` (05, 07 confirm correctly-missing).
- FX5: `tests/pr_submit/conftest.py` collector (Option A `pytest_generate_tests`) or `test_gate_coverage.py` (Option B) — both spelled out (05 §1).
- FX7: exact edit anchors + new field names in a §7 edit-map table (03).
- FX2: insertion after `rf-qa-qualitative.md:676` + Adaptation Guidance table (699-715) + item-count bump (660/738) (04 §1b).
- FX1: `reflect-reviewer.md` Role/persona_lens/Output-Format anchors + new `## Correctness-gap` advisory section near `deviation-taxonomy.md:127/:129` (04 §3c/4c).

### Criterion 3 — Logical phase/step breakdown derivable? **PASS**
File 06 supplies the full Template-02 body/phase structure, gate placement (I15/I17/F2), and the natural fix grouping (P0 det tests FX3+FX5 → P0 det cli/reflect FX7 → P1 LLM briefs FX2+FX1). I18 mandates ≥1 L3 test item for the code-modifying surfaces.

### Criterion 4 — Patterns & conventions documented? **PASS**
- Test idioms: AST-introspection precedent (mirror `test_no_scoring_engine.py`), naming, `_`-prefixed builders, `tmp_path`, PR#-tagged regression docstrings (05 §2).
- Brief lens form: axis-charter form (04 §1a), numbered-bold-prose checklist-item form (04 §1b), 4-part taxonomy-category form + grounding-gaps parallel-artifact schema (04 §4b).
- Contract additive-safety: read-and-ignore NFR-8, key-based consumers, the field-order-preserving frontmatter writer (03 §5).

### Criterion 5 — MDTM template notes present w/ rule refs (06)? **PASS**
File 06 cites B2/B3/B4/B5, D3, I15-I22, M2/M3/M4, L1-L6, F2, and the POST-gate SKILL lines (2204-2207, 2263, 2322) with the exact flat guard+wrapper command and exit-code consumption. Concrete analogue folder (uc2 reachability-gate) identified for imitation.

### Criterion 6 — Granularity sufficient for per-symbol items? **PASS**
- FX5 helper set: registry of ≥21 dotted names (02 §4.1) incl. the two dataclass methods and `*_checks` family a naive scan misses (§4.3).
- FX3 valid-name sets: exact literal lists to extract + the two runtime-built valid sets + subset-direction rule + `Constant`-arg guard (01 §4).
- FX7 exact functions: `build_reflect_contract` (ensemble.py:492), `_build_reflect_post_value` (runner.py:93), `derive_verdict`/`_degraded_reason` (contract.py:130/249), `_make_result` (contract.py:104) with line ranges (03).

### Criterion 7 — Doc cross-validation tagged CODE-VERIFIED/CONTRADICTED/UNVERIFIED (07)? **PASS**
File 07 tags every plan/post-mortem claim, with git evidence for branch-location claims and file:line for code claims. Two headline CONTRADICTIONS (HL-1 branch premise, HL-2 F1-F4 already fixed) plus three fix-level contradictions (FX7 exemption, FX1 5th-category, FX2 rename-vs-scope-expansion) are each tagged and evidenced.

### Criterion 8 — Solution approaches evaluated where new (FX3 AST, FX5 collector)? **PASS**
- FX3 AST: call-site-arg vs getattr-node resolution, subset-not-onto direction, facade-vs-source import, `Constant`-arg guard, optional named-deriver `ast.Attribute` pass (01 §4-5); repo idiom choice + `inspect` alternative (05 §2).
- FX5 collector: registry-anchored vs pure name-pattern (02 §4.1), Option A `pytest_generate_tests` vs Option B parametrized module vs why-not `modifyitems`/raise-in-hook (05 §1), with the coexistence proof against the plugin hook.

### Criterion 9 — Unresolved ambiguities documented (FX2 scope-fit, FX7 exemption conflict, FX1 no-5th constraint)? **PASS**
All three named ambiguities are richly documented AND flagged as human-decision points:
- **FX2 scope-fit**: `rf-qa-qualitative.md` is a *document*-QA agent (its own line-3 charter); no literal `internal-consistency` lens exists; grafting a Python cross-symbol lens is a scope EXPANSION, not a rename (04 CRITICAL FRAMING; 07 D6 — recommends considering `rf-qa` structural / a new code lens instead).
- **FX7 exemption conflict**: `tool-unavailable` is a deliberate member of `_VERIFICATION_SKIP_EXEMPTIONS`; the post-mortem's own smoking gun is exempt by design → FX7 is NOT purely additive if it touches the consumer set; 03 §2c/§3.4 routes the additive path through the BUILDER (ensemble.py) instead and flags the design tension (07 FX7).
- **FX1 no-5th-category**: `deviation-taxonomy.md:5/:131/:154 (§17.7 Kill List)` explicitly rejects a 5th class → FX1 must be an advisory parallel artifact mirroring grounding-gaps, never a 5th gating category (04 §4a; 07 FX1).

---

## Contradictions / Cross-Researcher Consistency Notes (surfaced, not resolved)

These do not lower the breadth verdict (coverage exists for every fix), but the task-builder MUST carry them into item wording:

1. **[Framing, load-bearing]** F1-F4 are ALREADY FIXED at HEAD `46a787da` (07 HL-2, corroborated by 01 headline, 02 §2.1, 03 §3c). FX2/FX3/FX5/FX7 items must be worded as **regression-guards / recurrence-prevention**, NOT live-bug fixes. Any item asserting an open F1-F4 defect is stale.
2. **[Build mechanics]** `contract_setup` + `tests/pr_submit` exist ONLY on this branch (`harden/qa-reflect-blindspot-pr209` / `DetectionContractBranch`), ZERO copies on `origin/master` (07 HL-1). `start_commit` / build-base derivation must target this branch, not `origin/master` as the plan §5 premise states.
3. **[FX7 target precision]** R7 (07 D5) maps "FX7 target" to `contract.py`; R3 (03) shows the PRIMARY additive target is `ensemble.py:492 build_reflect_contract` (the vacuous-clean builder), with an explicit warning that editing the `contract.py` consumer exemption would be a behavior change, not additive. **Follow R3's edit map (03 §7), not R7's single-file mapping.** Not a gap (03 coverage is more complete) — a reconciliation note.
4. **[FX2 home]** 04 recommends the `rf-qa-qualitative.md` Code Compatibility group; 07 D6 questions whether a document-QA agent is the right surface AT ALL and suggests `rf-qa` structural or a new code lens. This surface choice is the single most load-bearing open decision and should be resolved by a human before FX2 items are written. Research coverage to write items exists under EITHER resolution.
5. **[M4 fidelity gate]** 06 recommends INCLUDING an M4 source-fidelity gate because a spec drives the fixes; the not-applicable escape remains only if the fixes are judged purely mechanical (they are not). Builder decision, well-scoped.

---

## VERDICT: PASS

All 9 breadth criteria PASS with file:line evidence, and all 4 independent spot-checks of cited symbols confirm accuracy. Every fix (FX1, FX2, FX3, FX5, FX7) has research coverage sufficient to write per-file / per-symbol checklist items: source files + exports, output paths/formats, phase/step breakdown, conventions, MDTM rule refs, per-symbol granularity, CODE-VERIFIED/CONTRADICTED tagging, new-approach evaluation, and documented ambiguities are all present. The corpus is unusually strong: R7 independently cross-validates R1-R6, and the three named design ambiguities (FX2 scope, FX7 exemption, FX1 5th-category) are each flagged as human-decision points rather than silently assumed.

**No breadth GAPS block task-building.** The five contradiction/consistency notes above are DECISION items (branch premise, fixed-not-live framing, FX7 target file, FX2 surface choice, M4 inclusion) that the task-builder must carry forward — they are completeness-of-decision points the research correctly surfaced, not completeness-of-research gaps. Per the BREADTH lens (does coverage exist to write items?), coverage exists under every resolution of those decisions.

**Non-blocking recommendations to the task-builder:**
- Word all FX2/FX3/FX5/FX7 items as regression-guards (F1-F4 already fixed at HEAD).
- Resolve the FX2 surface question (doc-QA agent vs code-reviewing surface) as a human-decision item before writing FX2 items.
- Treat FX7 and FX1 as reconciliations-with-existing-design (builder-side ensemble.py edit for FX7; advisory parallel artifact for FX1), never as gate-weakening or 5th-category additions.
- Derive `start_commit` from this branch, not `origin/master`.
- Include the M4 source-fidelity gate (spec drives the fixes).
