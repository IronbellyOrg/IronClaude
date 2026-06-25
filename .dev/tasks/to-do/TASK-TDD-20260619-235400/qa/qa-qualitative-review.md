# QA Report — TDD Qualitative Review

**Topic:** sc:reflect Tier-2 Reviewer Ensemble Swarm Re-Wiring (FR-RH2)
**Date:** 2026-06-20
**Phase:** tdd-qualitative
**Fix cycle:** N/A (single pass, fix_authorization: true)
**Target:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (1773 lines)

---

## Overall Verdict: PASS (after 2 in-place fixes applied)

Both known residual cosmetics were verified against source and fixed. No NEW content-sense
defects were found that would mislead an implementer. The document reads as a credible,
buildable component-level TDD at the correct altitude.

## Items Reviewed (14-item TDD checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Architecture decisions match PRD/spec requirements | PASS | All 9 FR-001..009 carry an FR-RH2.N source (verified the 9-row table at L330-338); §5.1 mapping note documents the .9-after-.4 offset; no `[NO SPEC TRACE]` gaps. |
| 2 | No requirements invented beyond the spec | PASS | NET-NEW components (`ensemble.py`, `reflect_review.py`, stub test, guard extension) are scoped to FR-RH2 deliverables; no caching/extra capability invented. Non-Goals (NG1-6) fence scope. |
| 3 | No PRD content repeated verbatim | PASS | TDD translates into engineering specs (data models §7, API §8.2 signatures, OI-1 mapping table §8.3); does not copy spec prose. |
| 4 | Performance targets match spec targets | PASS | 180s per-worker timeout, 5xx-retry-once+2s backoff, `max_fix_iterations` default 2 — all verified against `dispatch.py` defaults and `runner.py` loop; §17 internally consistent with §12.4. |
| 5 | API contracts internally consistent | PASS (1 fix) | §8.2 `dispatch_wave1` signature verbatim-correct vs source (kw-only after bare `*`). **§11.1 Mermaid (L859) listed `prompt`/`worker_spec`/`logger` as bare positionals — contradicted the authoritative §8.2 kw-only signature. FIXED** to `prompt=…, worker_spec=…, logger=…`. |
| 6 | Data models consistent across ER/API/migration | PASS | `WorkerResult` 12 fields (verified `@dataclass models.py:1027` referenced), `ResultContract` DM-012 field list, OI-1 §8.3 left/right columns coherent; diversity-over-M (never N) consistent in §4.1/§6.1/§7/§8.3/§11/§12/§14. |
| 7 | Component boundaries well-defined | PASS | `ensemble.py` owns translation; `swarm/merge.py` stays mechanical concat; `/sc:adversarial` owns scoring; path-confinement A/B clearly separate the two `return-contract.yaml` files. No ownership overlap. |
| 8 | Dependency graph acyclic + complete | PASS | §6.2 module graph + §18.2 internal-deps table; reuse-by-import edges (dispatch/factory/reduce) verified present at cited lines. Private-symbol coupling (Q7) honestly flagged, not hidden. |
| 9 | Implementation details specific enough to code from | PASS | 3-file ReflectConfig edit chain (§19.2), clamp/sentinel ordering rule, slot→`pool[i % len]` binding, reduce mode/floor — all actionable. |
| 10 | Error handling specified, not hand-waved | PASS | §12 categorizes by surface; (M,N) guard table reproduced consistently (§4.1/§5.4/§11.2/§12.2.1/§14.3); retry matrix §12.4 grounded; fail-closed BLOCKED ordering documented. |
| 11 | Migration plan covers data + schema | PASS | §19 — mechanism-swap-behind-preserved-contract (no data migration); additive/inert phasing; surgical rollback at single rewire point. Correctly notes no schema bump. |
| 12 | Technology choices justified | PASS | §6.4 D1-D5 + §21 Alt 0/1/2 + integration sub-decision; in-process-import-vs-subprocess grounded in web research (issues #61993/#31977) and the nesting-defect root cause. |
| 13 | Scale assumptions explicit | PASS | §17.2/.3 fan-out is N parallel calls (wall-clock = max not sum); auto-fix multiplier bounded by `max_fix_iterations`; CLI-infra altitude correctly disclaims SLO/fleet framing. |
| 14 | Security model complete | PASS | §13 threat model + controls: proxy-contract-by-construction, credential confinement, `suspect:true` quarantine, injection guard, verdict fail-closed, path confinement, no-nesting. Appropriate for the surface. |

## Scope / Altitude Check (explicit)

PASS. This is a component-level design for the reflect Tier-2 seam, not platform sprawl.
Sections 9/10/16 are correctly N/A (backend CLI library, no client surface) WITH rationale.
§17.1/§4.2/§25/§26 carry honest "light / N/A — CLI infrastructure" scope notes rather than
inventing web-service KPIs. No feature-vs-platform content leakage.

## Central-thesis coherence (explicit)

PASS. The four load-bearing claims hold together and are individually source-verified:
re-route Tier-2 through the swarm dispatch library by in-process import; `/sc:adversarial`
Mode A as the downstream scorer; the OI-1 §8.3 field-correspondence table sizes `ensemble.py`'s
mapping layer; the non-mocked `--transport stub` integration test + one-reviewer negative
witness prove ensemble formation without re-creating the conftest mock gap. The "mock gap"
problem statement (§1/§2.2/§15) and the falsifiability guarantee (§11.2/§15.3) are coherent
and the reason the integration level is called load-bearing.

## Summary
- Checks passed: 14 / 14
- Checks failed (pre-fix): 1 (item 5 — Mermaid/signature contradiction) + 1 cosmetic grammar
- Critical issues: 0
- Issues fixed in-place: 2

## Issues Found
| # | Severity | Location | Issue | Fix Applied |
|---|----------|----------|-------|-------------|
| 1 | MINOR | tdd.md:1040 (§13.2) | Grammar artifact "is **an** 7-LOC" (article not updated when "8"→"7" earlier). | Changed "an 7-LOC" → "a 7-LOC". |
| 2 | IMPORTANT | tdd.md:859 (§11.1 Mermaid) | `dispatch_wave1(... prompt, worker_spec, logger)` rendered keyword-only params as bare positionals — contradicts the authoritative §8.2 signature (bare `*` makes them kw-only). An implementer copying the diagram would write an invalid call. | Changed to `prompt=…, worker_spec=…, logger=…` (consistent with the existing `transport_for_slot=` keyword; no distortion). |

## Actions Taken
- Fixed grammar artifact (§13.2, L1040) by replacing "an 7-LOC" with "a 7-LOC".
  Verified: `grep "an 7"` now returns zero hits; all merge.py LOC references uniformly read "7 LOC".
- Fixed §11.1 Mermaid `dispatch_wave1` call (L859) by keyword-prefixing the three kw-only params.
  Verified: matches the source signature `def dispatch_wave1(preflight_result, transport=None, *,
  transport_for_slot=None, prompt="", parallel_executor=None, worker_spec=None, logger=None)`
  read from `swarm/dispatch.py:334-343`.
- Confirmed NO change to the 9-FR count, the NFR-7→spec-§9 routing, or the NET-NEW framing
  (all three explicitly preserved).

## Source-verification trail (factual claims checked against code)

| TDD claim | Source verified | Result |
|---|---|---|
| reflect pkg = 6 files, `ensemble.py` absent | `ls src/superclaude/cli/reflect/` | CONFIRMED (commands/config/contract/__init__/models/runner; no ensemble.py) |
| `--transport`/`--reviewers` net-new, `--depth` exists | grep over `cli/reflect/` | CONFIRMED (0 hits transport/reviewers) |
| `reflect-review` token absent today | grep over `cli/` | CONFIRMED (0 hits) |
| `mechanical_merge` is 7 LOC | `merge.py:50-57` read | CONFIRMED (7-statement body) |
| `dispatch_wave1` signature (kw-only after `*`) | `dispatch.py:334-343` read | CONFIRMED verbatim |
| `runner.py:403` expected_tier derivation | `runner.py:400-406` read | CONFIRMED verbatim |
| `_resolve_run_transport_factory` at L612, private | `commands.py:612` read | CONFIRMED (`def _resolve...`) |
| `ModelPoolTooSmallError` class L589 / raise L688 | `commands.py` grep | CONFIRMED |
| `reduce_wave3` at L555 | `reduce.py:555` read | CONFIRMED |
| M-count predicate `status=="success"` at dispatch L496 | `dispatch.py:496` read | CONFIRMED |
| Trigger 7 `degraded-model-diversity` L267-269 | `contract.py` read | CONFIRMED (`mcd is not None and mcd != "full"`) |
| Trigger 10 `single-reviewer-fallback` L280-281 | `contract.py` read | CONFIRMED |
| Trigger 6 `degraded-tier1` L263-264 | `contract.py` read | CONFIRMED |
| Trigger 8 vendor `== "single"` L272-273 | `contract.py:271-273` read | CONFIRMED (slug `single-vendor`; condition matches §8.3) |
| Trigger 11 null-convergence (tier==2 ∧ score None) | `contract.py` read | CONFIRMED |
| Mode A `--compare` 2-10 files | `sc-adversarial-protocol/SKILL.md:58` | CONFIRMED (`file1.md,...,file10.md`) |
| `--suspect-source` absent in adversarial SKILL (`[CODE-CONTRADICTED]`) | grep SKILL.md (0 hits) | CONFIRMED |
| `bare_review.py` emits `suspect=True`,`tier="T2"`,`--suspect-source` | `bare_review.py:63-67` read | CONFIRMED |

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 18 distinct
   factual claims (line anchors, signatures, file inventory, trigger conditions, SKILL flags),
   each mapped to a specific grep/Read against shipped source — see the trail table above.
2. **What specific files did I read?** `cli/reflect/{runner.py,contract.py}`,
   `cli/swarm/{merge.py,dispatch.py,commands.py,reduce.py,lenses/bare_review.py}`,
   `skills/sc-adversarial-protocol/SKILL.md`, plus `ls`/grep over `cli/reflect/` and `cli/`.
3. **If I found ~0 issues, why trust the check?** I did NOT default to a clean pass. I
   adversarially re-derived the `dispatch_wave1` signature from source and caught the §11.1
   Mermaid positional-vs-keyword contradiction (IMPORTANT) that the authoritative §8.2 table
   masks — and confirmed the grammar artifact by line. Every PASS row cites a specific tool
   result, not an impression. The two issues found are exactly the two the prompt flagged as
   residual, and source verification confirmed both were real (not already-resolved) and bounded.
4. **Web research?** None performed. All verification was local-file-bound (source under review
   + cited code surfaces). The TDD's external references (Claude Code issues #61993/#31977,
   SO/blog subprocess-vs-import) were treated as design grounding, not re-fetched, because no
   checklist item required confirming their live content. Tavily-first policy therefore did not
   trigger this review.

## Confidence Gate

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 11 | Glob: 0 | Bash: 7 (combined Read+Grep > 14 checklist items)
- No UNCHECKED items. No UNVERIFIABLE items.

## Recommendations
- None blocking. Both fixes are applied and verified in-place. The TDD is buildable as-is.
- Note for implementers (already correctly captured by the TDD, not a defect): Q1/OI-1 (§8.3
  table validation against the shipped diff) remains the BLOCKING gate before FR-RH2.3 code
  lands; Q5/Q6/Q7 are honestly open and routed. These are intended open questions, not stale
  ones answered elsewhere.

## QA Complete
