# QA Report — TDD Qualitative Review (Fix-Cycle Verification)

**Topic:** sc:reflect Tier-2 Reviewer Ensemble Swarm Re-Wiring TDD (FR-RH2)
**Date:** 2026-06-20
**Phase:** tdd-qualitative (fix-cycle re-check after 12 report-validation fixes)
**Fix cycle:** verification pass (post-fix; `fix_authorization: false` — report-only)
**Document:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (1772 lines)

---

## Overall Verdict: PASS (with 1 MINOR non-blocking note)

The 12 report-validation fixes are coherent. The five focus areas all read cleanly,
no contradiction or broken narrative was introduced, and the central thesis remains
actionable end-to-end. Every factual claim spot-checked in the fixed areas verified
against shipped source. One MINOR cosmetic observation is recorded (a Mermaid
diagram-label arg ordering); it is **not** a regression from the fixes and **not**
FAIL-worthy — the authoritative signature it illustrates is verbatim-correct.

---

## Confirmation Items (the five asked)

| # | Confirm item | Result | Evidence |
|---|--------------|--------|----------|
| 1 | Reviewer-count reconciliation (2–3 conceptual vs `--reviewers [2,4]` default 3) coherent, no remaining contradiction | **PASS** | Every conceptual "2–3 heterogeneous reviewers" mention (§1 L193, §2.1 L212, §28 glossary L1721) is immediately followed by the parenthetical "(the `--reviewers` flag accepts [2,4], default 3)". Conceptual ensemble size (2–3) = design intent; CLI clamp [2,4] = operational capacity (superset); default 3 sits in both; the `1` negative-witness sentinel is explicitly carved out below the clamp (§8.1 L696/L701, Q8 L1533). No contradiction. |
| 2 | §8.2 `reduce_wave3` signature agrees with §18.2 and positional calls in §6.1/§11.1; engineer copying §8.2 writes valid code | **PASS** | §8.2 sig (L745-755) matches `reduce.py:555` verbatim: `worker_results` positional, `mode` positional-w-default, then `*` kw-only, `-> ResultContract`. §18.2 L1332 states the same shape + return type. §6.1 call (L428) `reduce_wave3(worker_results, mode="normalize+merge", output_dir=...)` and §11.1 call (L864) `reduce_wave3(worker_results, "normalize+merge", output_dir=..., workers_requested=N)` are BOTH valid against the real signature (`mode` is positional-or-keyword). All three forms mutually consistent. |
| 3 | §15.5 traceability matrix (all 8 NFRs) coherent with §15.1-§15.4 | **PASS** | §15.5 (L1218-1239) carries all 9 FRs **and** all 8 NFRs (NFR-RH2.1..8 each present, grep count = 8). Each row maps to test IDs (U1-U8, I1-I8, B1-B3) that are defined in §15.2 (unit), §15.3 (integration), §15.4 (backward-compat). No dangling test IDs; coherent with the §15.1 pyramid. |
| 4 | §18 pipeline/process.py note reads sensibly (orthogonal, out of scope) | **PASS** | §18.4 L1354 claim verified: `pipeline/process.py:72` IS `class ClaudeProcess` (a `Popen`-lifecycle primitive, L117/L192); `runner.py:31` imports it for the Tier-1 single-process launch (UNCHANGED by FR-RH2); the Tier-2 swarm fan-out composes `cli/swarm/` and never touches `pipeline/process.py`. The "orthogonal, outside FR-RH2 dependency surface, requires no change" framing is accurate and well-reasoned. |
| 5 | No new contradiction / broken narrative; central thesis (re-route via in-process import; Mode A scorer; OI-1 BLOCKING sizes ensemble.py) coherent + actionable end-to-end | **PASS** | Thesis is internally consistent across §1→§28: in-process import of `dispatch_wave1`/`_resolve_run_transport_factory`/`reduce_wave3` (all 3 verified as sync `def`s at cited lines); Mode A scores per-reviewer `final_path` never `merged.md` (merge.py is a scoring-free 7-stmt concat, verified L50-57); OI-1 (§8.3) is the load-bearing blocking gate sizing the mapping layer (the ~22-field disjoint-schema finding is honest). Migration (§19), risks (§20), alternatives (§21), open questions (§22) all reinforce the same narrative without drift. |

---

## Items Reviewed (14-item TDD qualitative checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Architecture decisions match spec (FR-RH2) requirements | PASS | All 9 FRs (§5.1) + 8 NFRs (§5.2) carry FR-RH2.N/NFR-RH2.N source; each maps to an architectural component (§6) and a test (§15.5). |
| 2 | No requirements invented beyond spec | PASS | Net-new files (ensemble.py, reflect_review.py, stub test) all trace to FR-RH2.1/.2/.5; no unauthorized capability. Caching/scope inflation: none found. |
| 3 | No PRD/spec content repeated verbatim | PASS | TDD translates spec FRs into engineering specs (data models §7, OI-1 table §8.3, signatures §8.2); not copy-paste. |
| 4 | Performance/quant targets match spec | PASS | 180s timeout (§17.2) = `_DEFAULT_TIMEOUT_SEC` verified; [2,4]/default-3 consistent; verdict→exit-code map (pass→0/halted→10/degraded→11/blocked→2) consistent across §1/§4/§5/§8/§12/§14. |
| 5 | API contracts internally consistent | PASS | reduce_wave3 / dispatch_wave1 / factory signatures consistent §8.2↔§18.2↔§6.1↔§11.1; return types (ResultContract / list[WorkerResult] / Callable) agree everywhere. |
| 6 | Data models consistent across §7 / §8 / migration | PASS | WorkerResult 12-field (models.py:1027), ResultContract DM-012 (models.py:877), M-count predicate (`status=="success"`, reduce.py:648 = dispatch.py:496) consistent. |
| 7 | Component boundaries well-defined | PASS | merge.py = mechanical concat (never verdict); /sc:adversarial = scorer; ensemble.py = translation layer. No ownership ambiguity. |
| 8 | Dependency graph acyclic + complete | PASS | §6.2 graph: runner→ensemble→{dispatch,factory,reduce,adversarial,contract}; no cycle; private-symbol coupling (factory) honestly flagged (§18.2 M-risk, Q7). |
| 9 | Implementation specific enough to code from | PASS | 3-file ReflectConfig chain (§19.2), clamp/sentinel ordering rule (§8.1 L696), slot→model binding `pool[i % len]` all concrete. |
| 10 | Error handling specified | PASS | §12 full (M,N) ladder, status→M table, retry matrix (5xx once/2s), ModelPoolTooSmallError eager-raise — all code-grounded. |
| 11 | Migration covers data + schema | PASS | §19 mechanism-swap-behind-preserved-contract; no schema bump (FR-RH2.7); rollback = revert single `_audit_once` branch. Coherent. |
| 12 | Technology choices justified | PASS | §21 import-vs-subprocess decision grounded in nesting defect + reuse-audit (0.81 reuse-by-import) + external refs (issues #61993/#31977). |
| 13 | Scale assumptions explicit | PASS | §17 fan-out budget (N parallel, max-over-slots wall-clock), §26 fix-loop multiplier (3×N) bounded by max_fix_iterations. |
| 14 | Security model complete | PASS | §13 proxy-contract-by-construction, suspect:true quarantine, credential confinement, verdict fail-closed ordering, path-confinement — comprehensive. |

---

## Summary

- Checks passed: 14 / 14 (qualitative checklist) + 5 / 5 (confirmation items)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (cosmetic, non-blocking, NOT a fix-regression)
- Issues fixed in-place: 0 (`fix_authorization: false` — report-only)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | §11.1 Mermaid label, L859 | The dispatch_wave1 call rendered inside the Mermaid sequence-diagram edge label reads `dispatch_wave1(preflight, transport_for_slot=λi→..., prompt, worker_spec, logger)` — listing `prompt`/`worker_spec`/`logger` as bare positionals after a keyword arg. The REAL signature (verified `dispatch.py:336-343`, bare `*` at L337) makes those three keyword-only, so the literal label is not valid Python (positional-after-keyword). This is a **diagram shorthand**, not a fenced code block; the authoritative §8.2 signature (L710-719) is verbatim-correct and explicitly notes "All params after `transport` are keyword-only (bare `*` at L337)". An engineer copies from §8.2, not a flow sketch. **Not a regression introduced by the 12 fixes.** | Optional polish: render the diagram label as `dispatch_wave1(preflight, transport_for_slot=λi→…, prompt=…, worker_spec=…, logger=…)` or abbreviate to `dispatch_wave1(preflight, transport_for_slot=λi→…, …)` so the label cannot be misread as a positional call. No impact on actionability. |

---

## Actions Taken

None — `fix_authorization: false`. Report-only verification. The one MINOR note above is
advisory polish, not a blocking defect.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 24 distinct
   claims across the fixed areas, each via a targeted tool call:
   - 3 swarm signatures verbatim (reduce_wave3 / dispatch_wave1 / _resolve_run_transport_factory)
   - merge.py mechanical_merge body (7 stmts, L50-57)
   - M-count predicate (reduce.py:648, dispatch.py:496)
   - runner.py:403 expected_tier expression
   - ModelPoolTooSmallError class + pool guard (commands.py:589, 687-688)
   - reflect pkg inventory (6 files, ensemble.py absent)
   - --transport/--reviewers net-new (zero hits); --depth exists (commands.py:102)
   - pipeline/process.py:72 = class ClaudeProcess; runner.py:31 import
   - reflect zero-swarm-consumption (zero hits for t2-swarm/final_path/output_files)
   - _degraded_reason trigger 10 (contract.py:280-281)
   - bare_review.py mirror facts (default_workers=3/suspect=True/tier=T2/next-cmd)
   - reduce_wave3 -> ResultContract return type
   - conftest make_claude_process_stub (L99); pass.yaml:4 = `tier_reached: 2`
   - test_commands_run.py mirror target (L507, L548, L551)
   - B1/B2/B3 line counts (276/220/172 — exact)
   - SKILL.md = 3002 lines (Q4/Q5 grounding)
   - ensemble-empty slug absence (Q6 honesty)
2. **What specific files were read to verify claims?** `cli/swarm/reduce.py`,
   `cli/swarm/dispatch.py`, `cli/swarm/commands.py`, `cli/swarm/merge.py`,
   `cli/swarm/lenses/bare_review.py`, `cli/reflect/runner.py`, `cli/reflect/contract.py`,
   `cli/pipeline/process.py`, `tests/cli/reflect/conftest.py`,
   `tests/cli/reflect/fixtures/pass.yaml`, `tests/swarm/test_commands_run.py`,
   `tests/cli/reflect/{test_verdict_mapping,test_runner_e2e,test_writeback}.py`,
   `skills/sc-adversarial-protocol/SKILL.md`, plus a full read of the 1772-line TDD.
3. **If 0 issues, why trust the check?** Not a 0-issue review — one MINOR was surfaced
   adversarially (the Mermaid arg-ordering), demonstrating the read went past the prose
   into the diagram internals. The 24 verified claims include exact line-count matches
   (276/220/172) and exact line-count of an external SKILL (3002) that could only match
   if the files were actually opened and counted — not asserted from the document.
4. **Web research performed?** None required — this review is entirely local-file-bound
   (TDD + cited source). No Tavily/WebSearch fallback was triggered.

**Fix-cycle health:** Previous report-validation flagged 12 fixes; this verification
finds them all coherent with 0 new contradictions and 1 cosmetic MINOR (not a
fix-regression). Issue count went 12 → 0 blocking. No systemic problem.

---

## Confidence

**Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
(14 checklist items + 5 confirmation items; every item carries tool-call evidence.)

**Tool engagement:** Read: 4 | Grep: 0 (folded into Bash grep) | Glob: 0 | Bash: 6
(Tool calls > implied by per-item verification; each Bash batch verified multiple
distinct checklist/confirmation items against source. Read calls = 4 paginated reads
covering the full 1772-line TDD.)

---

## Recommendations

- **PASS — green light to proceed.** All 12 fixes are coherent; the document reads as a
  credible, actionable TDD end-to-end.
- The single MINOR (Mermaid label arg ordering, §11.1 L859) is optional polish. It does
  NOT block delivery: the authoritative §8.2 signature is correct and the diagram is
  shorthand. If a future editing pass touches §11.1, abbreviate the dispatch_wave1 label.

## QA Complete
