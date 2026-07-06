# QA Report — Task Integrity (Consolidated Serialized Fix, A.10)

**Topic:** Additively harden RF QA + /sc:reflect vs PR #209 F1–F4 (FX1/FX2/FX3/FX5/FX7)
**Date:** 2026-07-03
**Phase:** task-integrity (fix-cycle / serialized consolidation)
**Role:** SERIALIZED FIX AGENT — fix_authorization: true
**Inputs merged:** qa-task-validation-b2-report.md (FAIL, 3 IMPORTANT + 3 MINOR) + qa-task-validation-structure-report.md (FAIL, 2 IMPORTANT-class + 4 MINOR); both 0 CRITICAL.

---

## Overall Verdict: PASS (all fixes applied)

Every consolidated finding from both structural lenses was fixed in place. No scope change; the four staleness overrides were preserved untouched (FX2 augment-in-place / 15-count / AX-2-no-AX-6; FX1 advisory-not-5th-class; FX7 builder-only no-exemption-edit no-status-degraded; F1–F4 framed as regression-guards). No forbidden CODE-CONTRADICTED item was introduced.

---

## Fixes Applied

| # | Sev | Finding | Fix applied | Verification |
|---|-----|---------|-------------|--------------|
| 1 | IMPORTANT | Bare relative `research/NN` paths do not resolve from items' cwd (worktree root) — research/ lives under `.dev/tasks/to-do/TASK-.../research/`; fresh-context spawn prompts handed unresolvable refs | Absolutized every backtick-relative `` `research/NN…` `` to the full `/config/…/TASK-RF-qa-reflect-harden-20260703-044500/research/NN-*.md` form via a scoped sed over backtick-delimited refs only | 50 backtick-research refs converted; `grep '`research/[0-9]'` = 0 remaining; absolute path `ls`-resolves. Bracket-form ledger doc-IDs `[research/NN]` intentionally left as identifiers (see Fix 5). |
| 2 | IMPORTANT | Step 3.3 edited models.py + contract.py + runner.py in one item (atomicity / TB-Add-5) | Split into per-file atomic items **3.3a** (models.py append defaulted `ReflectResult` fields), **3.3b** (contract.py `_make_result` populate via `c.get`), **3.3c** (runner.py `_build_reflect_post_value` + `write_sidecar` append + optional `--skip-if-pass` hardening) | Dependency order models→contract→runner preserved; each item edits exactly ONE file; downstream 3.5/3.6 unaffected (letter-suffix split). |
| 3 | IMPORTANT | Step 3.4 authored tests across 3 modules + fixtures in one item | Split into **3.4a** (fixtures FIRST), **3.4b** (test_ensemble_unit.py), **3.4c** (test_verdict_mapping.py), **3.4d** (test_writeback.py) | Fixtures-before-tests ordering enforced (item-11 intra-phase dep); each test module its own item; each references only its own file. |
| 4 | IMPORTANT | Steps 2.7 / 3.2 multi-surface batching | **2.7 SPLIT** into **2.7a** (conftest.py registry + `pytest_generate_tests` hook + existence/coverage/drift-alarm helper) and **2.7b** (new `test_gate_helper_coverage.py` parametrized test module) — 2 files → 2 items. **3.2 kept single**: it edits only `ensemble.py` (one module; the `run_tier2_ensemble` call-site thread is in the same file), below the ">1 file/module" split criterion | 2.7a→2.7b→2.8 ordering correct; hook/test wiring dependency respected. |
| 5 | MINOR (TB-Add-7) | `## Execution Context` References ledger saturated with `file.py:NN` citations | Stripped all `.py:NN` / bare `:NN` line citations from References R-002…R-006 (kept module names, symbol names, counts, and `[research/NN]` doc-IDs). Added a pointer note on R-002 that per-item file:line anchors live in the item Context fields | `grep '.py:[0-9]'` over the true block (`## Execution Context`..`## MANDATORY WORKFLOW`) = **0**. TB-Add-7 negative half now passes; per-item Context evidence binding (TB-Add-8) untouched. |
| 6 | MINOR | `run_tier2` symbol does not exist (real name `run_tier2_ensemble`, ensemble.py:168); `_degraded_reason` range conflated (def :249, skip-reason check :288-291) | Renamed `run_tier2`→`run_tier2_ensemble` at all 3 sites (R-004 ledger, Step 3.1, Step 3.2). Corrected `_degraded_reason` to "def L249; skip-reason check L288-291" at R-004, Step 3.1, Step GB.2 | Verified vs source: `def run_tier2_ensemble` @168, `def _degraded_reason` @249, skip check @289-290. `grep run_tier2` = 3×`run_tier2_ensemble`, 0 bare. |
| 7 | MINOR | Step 4.5 mixed a swallowed `ruff …cli/reflect/*.py 2>&1; true` no-op into a markdown step + a non-deterministic "run any markdown gate if configured" clause | Rewrote 4.5 as a clean deterministic markdownlint of the 3 changed briefs: `uv run pre-commit run markdownlint --files <3 briefs>`. Cited the actual configured hook (`.pre-commit-config.yaml` id `markdownlint`, `--fix`, `.dev/` excluded so the `src/` briefs are in-scope); added re-`make sync-dev` on `--fix` auto-correction | Verified the hook exists and does not exclude `src/…` paths; `grep 'cli/reflect/*.py 2>&1; true'` = 0. |
| 8 | MINOR | M4 fidelity-gate header (`### Post-Completion SOURCE-DOCUMENT FIDELITY Gate`) wrongly scoped finalization items PC.10-12 | Inserted a `### Finalization (Task Summary → POST reflect → Done)` subheading before PC.10; M4 header now scopes only PC.8-PC.9 | M4 header @458, Finalization @472 (before PC.10); reflect-penultimate/Done-last note preserved. |
| 9 | MINOR | PC.11 `git add -A` breadth | Confirmed the existing `.claude/{agents,skills}` unstage guard is intact; no tightening required because those mirrors are gitignored sync-dev output and cannot be staged by `git add -A` | Guard text present verbatim: "if `git add -A` would stage a tracked mirror, unstage it". No edit. |
| 10 | — | Post-edit re-verification | See Verification Summary below | 78 items; PC.11 penultimate / PC.12 last; no new TBD/TODO/FIXME; no forbidden staleness item reintroduced. |

---

## Verification Summary (post-fix)

- **Checklist item count:** 72 → **78** (+1 from 2.7 split, +2 from 3.3 split, +3 from 3.4 split). No impl-phase header states a numeric item count, so no header-count update was required (item-18).
- **TBD/TODO/FIXME:** only the two pre-existing *instructional* occurrences (Steps 2.2, 3.2 — "contains no placeholder/TODO"); no literal placeholder introduced.
- **Ordering:** Phase 3 = 3.1 → 3.2 → 3.3a → 3.3b → 3.3c → 3.4a → 3.4b → 3.4c → 3.4d → 3.5 → 3.6 (edit→test progression, fixtures before tests, models before consumers). Phase 2 = …2.7a → 2.7b → 2.8 → 2.9.
- **POST reflect wrapper:** PC.11 penultimate (line 484 header / item 482), PC.12 (status→Done) is the LAST checklist item (486); nothing after it.
- **Execution Context block:** 0 `.py:NN` citations (TB-Add-7 clean).
- **Symbol fidelity:** all `run_tier2` → `run_tier2_ensemble`; `_degraded_reason` def/check ranges corrected.
- **Staleness overrides preserved (untouched):** FX2 augment-in-place + 15-item count + AX-2/no-AX-6; FX1 advisory-only/no-5th-class; FX7 builder-only/no-exemption-edit/no-status:degraded; F1–F4 regression-guard framing.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep/Bash: 9 | Edit: 12 | Write: 1

## QA Complete

---

## A.10.25 Alignment Fixes

**Role:** A.10.25 ALIGNMENT FIX AGENT (single cycle) — fix_authorization: true
**Input:** `qa/qa-task-research-alignment-report.md` (VERDICT: FAIL — HIGH 1 · MEDIUM 1 · LOW 3)
**Verdict after fixes:** **PASS (all applied)**

### Overall verdict: PASS

All five findings from the research-alignment gate were fixed in place. The FX5 gate was made internally consistent and honest without weakening the additive-only/anti-gaming mandate, and no staleness override was disturbed.

### Fixes applied

| # | Sev | Finding | Fix applied | Verification |
|---|-----|---------|-------------|--------------|
| HIGH-1 | HIGH | FX5 registered ~21 helpers for coverage-checking but authored pairs for only 5, plus an ad-hoc per-helper exemption escape-hatch → not green-as-written; ≈24% real anti-gaming coverage; weakens the gate | (a) **Removed the exemption escape-hatch entirely** from Step 2.7a — replaced with an explicit "NO per-helper exemption; a registered helper may NEVER skip its pair" rule. (b) **Made the enforced registry == authored-pair set**: Step 2.7a now defines `GATE_LOAD_BEARING_HELPERS == HELPER_TEST_MAP.keys()` and adds a `set(GATE_LOAD_BEARING_HELPERS) == set(HELPER_TEST_MAP)` assertion so the two can never diverge. (c) **Step 2.5 now authors a negative+differential pair for EVERY enforced-registry helper** (the full F4-load-bearing module-level `def` family — `_path_resolves`, `_findings_locus`, `_review_completeness_signal`, `_selected_identity`, `_selected_app_slug`, `_paths_resolve`, `_emission_shape_observed`, `_resolve_optional_path`, plus `required_unobserved`), treating research §5's 5 examples as IDIOM TEMPLATES not the complete set. (d) **Step 2.4 redefines the enforced registry** as the cleanly-enumerable module-level `def` gate-shaped set (research §4.3 basis) and lists `ValidationReport.passed` + the residual `_*_checks` family as EXPLICIT documented residual-risk auto-enumeration NON-GOALS (never silently in-or-out). (e) **Step 2.8 is now reachable**: enforced set == authored set == matchable set. Anti-gaming coverage rises 5→~11 helpers (strengthened, not weakened). | Registry ≡ authored-pair set stated at Steps 2.4/2.7a; `grep` for exemption-hatch language = **0**; every §5 differential (§5.1–§5.5) retained + expanded; drift-alarm matched set is a strict SUBSET of the registry (reconciled only by authoring a pair OR tightening the single documented pattern — never a carve-out). |
| MEDIUM-2 | MEDIUM | Drift-alarm regex cannot match the `_*_checks` family / dataclass methods it was told to register → registry/alarm/authored-pairs referenced inconsistent sets | Chose the **narrow-to-module-level-def** option consistent with HIGH-1: the enforced registry + drift-alarm are scoped to the gate-shaped module-level `def` set; the two research-§5 load-bearing dataclass/checks differentials (`required_unobserved` §5.3, `_negative_control_checks` §5.5) are EXPLICITLY hand-registered WITH pairs (coverage-checked via `HELPER_TEST_MAP`, not AST); `ValidationReport.passed` + the residual `_*_checks` builders are documented residual-risk auto-enumeration non-goals. Registry, alarm, and authored pairs now reference the SAME set (registry ⊇ alarm-matches, registry ≡ authored). Stated explicitly in Steps 2.4/2.6/2.7a + Open Questions. | One reviewed gate-shaped pattern governs registry, alarm, and pairs together; residual-risk non-goals documented as code comments (2.7a) and in the Open Questions block. |
| LOW-1 | LOW | FX6 excluded outright though research-notes framed it "advisory-only" (parallel to the shipped-advisory FX1) — surfaced, not silently dropped | Added an explicit **Open Question** entry noting FX6 is excluded as advisory-annotation-only per plan §2 / research-notes (no research file scoped it with a target/anchor), kept OUT of implementation items, flagged for user confirmation. | Open Questions block now carries the FX6 note; no FX6 implementation item introduced. |
| LOW-2 | LOW | `reviewers_verified = reviewer_count >= reviewers_requested` `TypeError`s when `reviewers_requested is None` (the additive-safe default) | Step 3.2(d) now specifies the None-guard: `reviewers_verified = True if reviewers_requested is None else reviewer_count >= reviewers_requested` (never compare against `None`; unknown requested count → vacuously satisfied so direct-call/test sites are unaffected). | `grep "reviewers_requested is None else"` = 1; additive-safe default preserved. |
| LOW-3 | LOW | `persona_lens` described as an "enum" where research/04 shows a free-form "e.g." field | Step 4.2(b) reworded: add a `no-spec-correctness` value to the **free-form `persona_lens` field** (extend its example list); explicitly notes it is NOT a closed enum and not to introduce a strict enum declaration. | `grep "free-form \`persona_lens\` field"` = 1; FX1 never-gating/advisory constraints untouched. |

### Post-fix re-verification

- **FX5 internally consistent:** enforced set == authored set == matchable set; `GATE_LOAD_BEARING_HELPERS == HELPER_TEST_MAP.keys()` asserted in-collector; NO exemption hatch (grep = 0); Step 2.8 per-helper coverage reachable/green-as-written.
- **Anti-gaming differential mandate preserved & strengthened:** every registered helper carries a mutation-must-fail differential; coverage breadth 5→~11 helpers; all research §5.1–§5.5 differentials retained; the only demotions (`ValidationReport.passed` + 4 non-anti-gaming `_*_checks` builders) are exactly the §4.3-flagged blind-spots for which research gave NO differential example, now explicitly documented as residual-risk non-goals.
- **Gate-lens self-consistency:** reconciled the stale `≥21`/dataclass-inclusion criteria in the Gate-A lens spawn items (evidence-anchor 256, domain-accuracy 258, completeness-analyst 259) so the gate's own lenses no longer contradict the corrected FX5 design; the completeness analyst now reads §6 TOGETHER WITH §4.3.
- **Item count sane:** 78 `- [ ]` items (unchanged — all fixes are in-item prose edits; no item added/removed/split).
- **POST reflect ordering intact:** PC.11 (reflect wrapper) penultimate; PC.12 (status→Done) last.
- **No staleness override disturbed:** FX2 augment-in-place + 15-count + AX-2/no-AX-6; FX1 advisory-only/no-5th-class/never-gating (LOW-3 only clarified free-form field, not the gating constraint); FX7 builder-only/no-exemption-edit/no-status:degraded (LOW-2 only added a None-guard); F1–F4 regression-guard framing — all untouched.

**Confidence:** Verified: 5/5 findings | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep/Bash: 4 | Edit: 12 | Write: 0

## A.10.25 Alignment Fixes Complete
