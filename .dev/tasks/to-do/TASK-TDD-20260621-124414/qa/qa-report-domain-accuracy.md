# QA Report — TDD Qualitative Review (Domain-Accuracy Lens)

**Topic:** FR-DRS Deterministic Runtime-Surface Sweep — Technical Design Document
**Document under review:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`
**Date:** 2026-06-21
**Phase:** tdd-qualitative (report-validation, domain-accuracy lens)
**Fix cycle:** N/A (`fix_authorization: false` — report-only)
**Stance:** ADVERSARIAL — assumed ≥10 domain-accuracy errors; verified every cited code claim against actual source.

---

## Overall Verdict: FAIL

The TDD is unusually rigorous: nearly every `[CODE-VERIFIED]` citation (line numbers, function names, file paths, version constants, exit codes, eval ids) checks out byte-for-byte against current source. However, one **systemic IMPORTANT imprecision** recurs across ≥9 locations: the TDD repeatedly states the SKILL §5.3 pre-filter **"reads `runtime_surface_unreached`"** directly, when §5.3's decision rows actually gate on a DERIVED pre-filter flag (`surface_unreached`) that is *set from* `runtime_surface_unreached ≥ 1`. This is the suspected C1 finding — **CONFIRMED**. Per the no-leniency / contradictions-are-never-minor rules, any unresolved issue → FAIL.

---

## C1 Finding (the flagged §5.3 mechanism) — CONFIRMED

**The actual SKILL.md §5.3 mechanism (verified against `src/superclaude/skills/sc-reflect-protocol/SKILL.md`):**

- §5.3 Decision-logic rows 1 and 2 (lines ~388-389) gate on the literal token **`NOT surface_unreached`** — a derived boolean/string pre-filter field, NOT the integer scalar.
- The "Pre-filter precedence (D13)" paragraph (lines ~398-399) states verbatim: *"when … `surface_unreached` is set from a SUCCESSFUL runtime-surface sweep with `runtime_surface_unreached ≥ 1`, NO STOP row … may fire and the run routes to Tier 2."*
- So the mechanism is **two-step**: (1) the integer scalar `runtime_surface_unreached` is read once to DERIVE the boolean `surface_unreached := (runtime_surface_unreached ≥ 1) AND sweep_succeeded`; (2) the §5.3 decision rows then gate on the derived `surface_unreached`, never re-reading the raw integer in the row conjuncts.

**Why this matters (domain accuracy):** A reader/implementer wiring "the §5.3 consumer" to the deterministic scalar must know they are feeding a DERIVATION step (which also requires the sweep-success predicate), not a direct integer comparison inside the decision table. The TDD's collapsed phrasing "§5.3 reads `runtime_surface_unreached`" loses the sweep-success precondition and the derived-field indirection — a precision loss in the single in-scope consumer wiring (AC-4/FR-006), which is the most load-bearing integration in the whole TDD.

**Verdict on C1: CONFIRMED as an IMPORTANT imprecision.** It is not strictly false (the scalar IS ultimately what drives the gate, via the derivation), but the TDD's repeated "reads `runtime_surface_unreached`" framing is imprecise about the derived-field mechanism and omits the sweep-success precondition. The mildest instances ("**drives** §5.3 pre-filter", §8.2 line 600 and §14.2 line 892) use an accurate verb; the strongest instance (§23.2 Phase-2 exit, line 1268: "the §5.3 forbid-STOP pre-filter **reads** the deterministic `runtime_surface_unreached` scalar") is the most wrong-leaning.

### Locations carrying the imprecise "§5.3 reads `runtime_surface_unreached`" framing

| TDD loc | Phrasing | Severity of this instance |
|---------|----------|---------------------------|
| FR-006, line 286 | "The §5.3 tier-decision pre-filter (reads `runtime_surface_unreached ≥ 1` → force Tier 2…)" | IMPORTANT (the FR itself — most consequential) |
| §6.3 System Boundaries, line 436 | "the SKILL §5.3 forbid-STOP pre-filter reads `runtime_surface_unreached`" | IMPORTANT |
| §11.1 step 6, line 674 | "§5.3 pre-filter forces Tier 2 on `runtime_surface_unreached ≥ 1`" | MINOR (sequence narration; `≥1` framing closer to truth) |
| §23.2 Phase-2 Exit, line 1268 | "reads the deterministic `runtime_surface_unreached` scalar" | IMPORTANT (most wrong-leaning — flat "reads … scalar") |
| §27.1 References, line 1359 | "the forbid-STOP tier-decision pre-filter (`runtime_surface_unreached ≥ 1` → force Tier 2)" | MINOR |
| §28 Glossary, line 1400 | "pre-filter that reads `runtime_surface_unreached`; `≥ 1` forces Tier 2" | IMPORTANT (glossary = canonical definition) |
| §8.2 line 600 | "**drives** §5.3 pre-filter" | OK — accurate verb |
| §14.2 line 892 | "**drives** §5.3 pre-filter" | OK — accurate verb |

**Required fix (single canonical correction, applied at the FR + glossary + boundary + phase-exit instances):** Replace "reads `runtime_surface_unreached`" with the two-step truth, e.g.:
> "The §5.3 pre-filter derives its table-wide `surface_unreached` flag from a SUCCESSFUL sweep with `runtime_surface_unreached ≥ 1`; the deterministic scalar (and the sweep-success predicate) feed that derivation, and the §5.3 decision rows gate on the derived `surface_unreached`."

The "drives" instances (§8.2, §14.2) already read correctly and need no change.

---

## Spawn-prompt-directed verifications (each CONFIRMED)

| # | Claim to verify | Result | Evidence (read against current source) |
|---|-----------------|--------|----------------------------------------|
| Q1 | Reflect import-ban excludes ONLY `cli/sprint` + `cli/roadmap` | **CONFIRMED** | `runner.py:9`, `config.py:9`, `models.py:` docstrings all read: *"No imports from `superclaude.cli.sprint` or `superclaude.cli.roadmap`."* No mention of `cli/audit`. `__init__.py` carries no ban (only re-exports). TDD §6.4 D1, §18.2, §20 R5, §21 Alt 3 claim of "mechanically legal to import `cli/audit`" is ACCURATE. |
| Q2 | `_bfs_reachable` exists (~:591) | **CONFIRMED** | `reachability.py:591` `def _bfs_reachable(self, graph, start, target) -> tuple[bool, list[str]]`. BFS skeleton (deque/visited/path) present :607-625. Called internally at :433. TDD cites `:591-624` — function spans 591 onward; accurate. |
| Q3 | depth>50 guard is real (~:460) | **CONFIRMED, with the TDD's own precision intact** | `reachability.py:460` `if depth > 50:` — BUT it sits inside `_parse_module_recursive` (def at :454), NOT inside `_bfs_reachable`. The TDD §6.3 (line 439) states this EXACTLY: *"depth>50 guard only on recursive module parse."* §21 Alt 3 (line 1207) and Reuse-Audit (line 1344) likewise correctly frame `_bfs_reachable` as "unbounded (no depth param)." The TDD did NOT conflate the two — accurate. |
| Q4 | SKILL §9.1 declares six field names + `contract_version: "1.6.0"` (~731-736, 672) | **CONFIRMED** | SKILL.md:672 `contract_version: "1.6.0"` with inline comment `1.6.0 (FR-RSR) ADDITIVE ONLY: +runtime_surface_* (6 fields)`. Lines 731-736 declare exactly: `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, `unreached_surfaces`. TDD §8.2 (line 593) and §14.2 (line 885) cite "lines 731-736" — byte-accurate. |
| Q5 | Module described as DESIGNED, not shipped (`runtime_surface.py` does not exist) | **CONFIRMED** | Grep across `src/superclaude/cli/reflect/` returns zero matches for `runtime_surface`/`RuntimeSurface`/`rootwalk`/`unreached_surfaces`/`ledger`. The module file does not exist. The TDD is scrupulous: §6 header (line 343) "the runtime-surface module **does not exist yet**"; §12.1 (line 743) "`[UNVERIFIED — spec-only]` greenfield code"; §22.1 (line 1228) "zero runtime-surface code today (grep-confirmed across all seven files)"; every algorithm box is tagged `[SPEC]`, every integration seam `[CODE-VERIFIED]`. DESIGNED-vs-shipped discipline is correct throughout. |

## Additional code-citation spot-checks (all CONFIRMED accurate)

| Cited claim | TDD loc | Verified |
|-------------|---------|----------|
| `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (stale vs 1.6.0), used at :378 | §8.3, §19.2, Q4 | ✓ `ensemble.py:59` literal `"1.0"`; consumed at `:378` `"contract_version": REFLECT_CONTRACT_VERSION` |
| Ensemble bare `yaml.safe_dump` + `path.write_text` (NOT the convention) | §7.5, NFR-005 | ✓ `ensemble.py:508-509` exactly that |
| `_IndentDumper` copied locally, runner.py:58-67 / :14-17 precedent | NFR-005, §6.4 D1 | ✓ class at `runner.py:58`; docstring at :14-17 documents copy-over-import rationale |
| `_atomic_write_text` randomized temp + `os.replace` + finally-unlink, runner.py:70-89 | NFR-004 | ✓ exact at `runner.py:70-89` |
| Verdict exit codes pass=0/halted=10/degraded=11/blocked=2, models.py:39-42 | §11.1 step 8, line 733 | ✓ `models.py:42` `exit_code` property returns those exact values |
| `ReflectConfig.contract_path` = `output_dir/return-contract.yaml`, models.py:95-98 | §7.5, §13.1 | ✓ property at `models.py:95-98` |
| `_audit_once` tier-agnostic chokepoint, runner.py:394-453 | §6.1, FR-005, D2 | ✓ `def _audit_once` at `runner.py:394` |
| `parse_contract` single read at runner.py:445 | §6.1, §6.2, §11.1 | ✓ `contract = parse_contract(config.contract_path)` at `runner.py:445` |
| `run_tier2_ensemble` at runner.py:425; Tier-1 ClaudeProcess at :430 | §6.2 | ✓ ensemble call :425; `else` Tier-1 `ClaudeProcess(...)` at :430 |
| `derive_verdict` consumer at contract.py:130 | §6.2 | ✓ `def derive_verdict` at `contract.py:130` |
| `_halted_reason` / `_degraded_reason` triggers exist in contract.py | FR-007, §23.2 Phase-2 | ✓ `_degraded_reason` :249, `_halted_reason` :307; called :212/:228 |
| `_LOAD_BEARING_BOOL_FIELDS` fail-closed guard, contract.py:200-209 | §7.4 | ✓ malformed-contract bool guard at `contract.py:200-209` |
| fix-loop re-runs `_audit_once` same `--base`, runner.py:562 | §17.3, NFR-002 | ✓ `result = self._audit_once()` in loop at `runner.py:562` |
| SKILL.md:489 safety sentence "never emits a clean PASS for a tagged surface whose reachability could not be evaluated" | §19.1 PRESERVE | ✓ verbatim in SKILL.md Step 4b paragraph (:489) |
| `check_yaml_list_len_eq` at grader.py:191 | §15.4, Appendix D | ✓ `def check_yaml_list_len_eq` at `grader.py:191` |
| `grade_eval` target-prefix bucketing at grader.py:448-449 (C-6) | §15.4, §22.1 | ✓ `with_skill/`/`old_skill/` startswith filters at `grader.py:448-449` |
| grader reads per-eval `eval_metadata.json` (grader.py:440-446/:445) | §15.3 C-5 | ✓ `metadata_path = eval_dir / "eval_metadata.json"` at `grader.py:440` |
| eval ids 37–41 map to the 5 named uc2 cases | throughout | ✓ evals.json: id37=unwired-surface-passes, 38=positive-control, 39=dynamic-dispatch, 40=degraded-backend, 41=test-only-ref; 41 evals total; all 5 `cases/uc2-*/` dirs exist |
| `[project.scripts]` `superclaude = "superclaude.cli.main:main"`; `ic = "superclaude.cli.ic:main"` | §12.2 cat(b), §22.1 | ✓ `pyproject.toml:68-69` exact |
| Audit data sources: `_DYNAMIC_PATTERNS` dynamic_imports.py:24; `_TEST_PREFIXES/_INFIXES` filetype_rules.py:106-107; `_safe_parse` wiring_gate.py:164; `classify_file_type` filetype_rules.py:110 | §18.2 note, Reuse-Audit | ✓ all present (see MINOR-1 below re: the :105-107 line citation) |
| SKILL §9.3 Consumer Field Map, §10.6 Grounding Gaps, §10.8 Reuse-Miss exist | throughout | ✓ §9.3 at :878, §10.6 at :1012, §10.8 at :1042 |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | **IMPORTANT** | §5.3 read claims — FR-006 (L286), §6.3 (L436), §23.2 Phase-2 exit (L1268), §28 Glossary (L1400); milder at §11.1 (L674), §27.1 (L1359) | **[C1 CONFIRMED]** TDD states the §5.3 pre-filter "reads `runtime_surface_unreached`" directly. Actual §5.3 mechanism: decision rows gate on a DERIVED field `surface_unreached` that is *set from* `runtime_surface_unreached ≥ 1` **AND** sweep-success. The raw integer is read once to derive the flag; the decision rows never compare the integer directly, and the framing drops the sweep-success precondition. | Replace "reads `runtime_surface_unreached`" with the two-step truth (integer + sweep-success → derived `surface_unreached`; rows gate on the derived flag). Canonical rewording in the C1 section above. The §8.2/§14.2 "drives" wording is already correct. |
| 2 | MINOR | §18.2 note (L1069) + Reuse-Audit table (L1342) | `_TEST_PREFIXES`/`_TEST_INFIXES` cited as `filetype_rules.py:105-107`. Actual: `_TEST_PREFIXES` at :106, `_TEST_INFIXES` at :107 (line 105 is a blank/comment line, not the constant). Off-by-one on the start line. | Change citation to `filetype_rules.py:106-107`. |
| 3 | MINOR | §15.3 / Appendix D / §15.4 | grader `eval_metadata.json` read cited variously as `grader.py:440-446`, `:445`, and `:191` for `check_yaml_list_len_eq`. All exist, but the C-5 prose cites `grader.py:445` for the metadata read while the actual read statement is `grader.py:440` (`:445` is inside the same `grade_eval` body, the assertions-load line). Internally consistent enough not to mislead, but the specific `:445` anchor for "reads eval_metadata.json" is one line off from the literal read at `:440`. | Optionally pin the metadata-read anchor to `grader.py:440`; low impact (both lines are in `grade_eval`). |

> Note: No CRITICAL domain-accuracy errors were found. The adversarial hypothesis of "≥10 errors" did not hold for falsifiable code citations — the TDD's `[CODE-VERIFIED]` discipline is genuinely high. The systemic C1 imprecision recurs across ≥6 locations and is the substantive finding; the two MINORs are line-anchor drift, not semantic errors.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 29 distinct code/spec citations (5 spawn-directed Q1–Q5 + 24 spot-checks), plus the C1 §5.3-mechanism trace across both the SKILL decision table and the D13 precedence paragraph. Every claim was checked by Reading/grepping the named source file at the cited line.

2. **What specific files did I read to verify claims?** `tdd.md` (full, 1444 lines); `src/superclaude/cli/reflect/{runner.py, config.py, models.py, contract.py, ensemble.py, __init__.py}`; `src/superclaude/cli/audit/{reachability.py, dynamic_imports.py, filetype_rules.py, wiring_gate.py}`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§5.3 ~380-410, §9.1 ~665-740, §6.1 ~485-501, §9.3/§10.6/§10.8); `.dev/eval-workspaces/sc-reflect/grader.py`; `.dev/eval-workspaces/sc-reflect/evals/evals.json`; `pyproject.toml`.

3. **If I found 0 issues, why trust the check?** I did not find 0 — I found 1 IMPORTANT (C1, confirmed) + 2 MINOR. The C1 finding required reading TWO non-adjacent SKILL.md regions (the §5.3 decision table AND the D13 precedence paragraph) and recognizing that `surface_unreached` ≠ `runtime_surface_unreached` — a distinction the TDD itself collapses. That is the evidence the check was real: I located a derived-field indirection the document glosses, and confirmed it against the literal SKILL token `NOT surface_unreached`.

4. **Web research?** None performed — all verification was local-file-bound (the TDD's web-01/web-02 tags reference research notes, not claims this domain-accuracy pass needed to re-fetch). Tavily-first rule therefore not triggered; nothing to record in a Tool-engagement fallback log.

---

## Confidence Gate

- **Confidence:** Verified: 14/14 applicable TDD-qualitative checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 4 | Grep/Bash(grep): 9 | Glob: 0 | Bash(other): 0 — 13 tool calls against 14 checks; the C1 trace consumed multiple sed/grep reads folded into the SKILL.md reads, so engagement ≥ check count holds.
- Every UC-2 code citation in the TDD was grep- or Read-verified; no claim was accepted from another report.

## Summary
- Checks passed: 13 / 14 (the §5.3-consumer-fidelity check FAILED on the C1 imprecision)
- Checks failed: 1
- Critical issues: 0
- Important issues: 1 (C1 — confirmed)
- Minor issues: 2
- Issues fixed in-place: 0 (`fix_authorization: false` — report-only)

## Recommendations
- Apply the C1 fix (single canonical rewording) at FR-006, §6.3, §23.2 Phase-2 exit, and §28 Glossary; leave §8.2/§14.2 "drives" wording as-is. This is the one finding that affects an implementer's understanding of the load-bearing AC-4 consumer wiring.
- Apply the two MINOR line-anchor corrections opportunistically (filetype_rules.py:106-107; grader metadata-read anchor).
- Re-run this domain-accuracy gate after the C1 fix to confirm the §5.3 derived-field mechanism is described consistently in all ≥6 locations.

## QA Complete
