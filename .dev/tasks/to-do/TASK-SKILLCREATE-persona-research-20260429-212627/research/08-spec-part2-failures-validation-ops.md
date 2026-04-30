# Spec Partition Analysis — Part 2: Failures, Validation, Ops

**Investigation type:** Spec Partition Analysis
**Scope:** /config/workspace/IronClaude/.dev/releases/current/persona-research/persona-research-skill-spec.md, lines 361-660 (§6 failure modes, §7 adversarial probes, §8 validation/three-questions, §9.1 promotion, §9.2 model tiering, Appendix C, Appendix D worked example)
**Status:** Complete
**Date:** 2026-04-29

---

## §6 Failure-Mode Table (Nygard) — verbatim

Source: lines 360-384 (heading at 360; table rows 362-383). The spec's table has 3 columns (Failure | Detection | Behavior). The "architecture component affected" column is not in the spec verbatim; I am inferring it from §5 component names referenced in Part 1 and marking each inference with [INFERRED] so reviewers can verify against Part 1.

| Failure (verbatim) | Detection (verbatim) | Behavior (verbatim) | Architecture component affected [INFERRED — verify against Part 1 §5] | Spec line |
|---|---|---|---|---|
| Identity ambiguous (multiple plausible humans) | Identity verifier finds >1 match above confidence threshold | Halt; ask user to disambiguate via aliases | Identity Verifier | 364 |
| Subject is deceased / minor / non-public | Identity verifier check | Refuse; explain | Identity Verifier | 365 |
| Subject has zero/near-zero public footprint | `footprint_score < 3` | Return `INSUFFICIENT_PUBLIC_DATA`; do not fabricate | Worker (footprint scoring) / Guard G3 | 366 |
| Source paywall (PitchBook, Bloomberg) | HTTP 401/402 or known-paywall URL | Flag as gap in dossier; continue | Worker (per-source fetch) | 367 |
| Source rate-limit (Twitter, LinkedIn) | HTTP 429 | Backoff once; if persistent, mark category as "rate-limited"; continue | Worker (per-source fetch) | 368 |
| Network failure on a single source | Exception during fetch | Retry once; on second failure, mark source as `unavailable`; continue | Worker (per-source fetch) | 369 |
| Worker exceeds budget (`per_subject_minutes`) | Wall-clock > budget | Worker returns partial with `status: INCOMPLETE` and the warnings field populated | Worker (budget enforcement) | 370 |
| Aggregator gets back 0/N successful workers | All workers `INCOMPLETE`/`REFUSED` | Halt; surface per-subject reasons; do not emit a config diff | Aggregator | 371 |
| Context overflow on heavily documented subject | Worker exceeds context window | Worker returns tiered output: full source list + summary dossier + "deep dive available" marker | Worker (context handling) | 372 |
| Cache hit on stale dossier | Dossier `> 90 days` old | Use cached but flag `STALE` in summary; recommend refresh | Cache layer (per FR-13) | 373 |
| Canonical store missing | Skill not properly installed; `<skill_root>/personas/` absent | Hard error: skill installation is broken; refuse to run | Archetype Manager (canonical store) | 374 |
| Local store missing | First run in a working project | Auto-create `./.claude/skills/sc-persona-research-protocol/personas/` (empty); warn user; proceed using canonical only | Archetype Manager (local store) | 375 |
| Both stores empty | Fresh install with no canonical bootstrap shipped | Use built-in `generic_public_figure` defined in code (failsafe); warn user | Archetype Manager (failsafe) | 376 |
| Archetype store corruption (malformed YAML) | Schema validation fails on load | Skip the corrupt file, continue with remaining archetypes; surface as `STORE_INTEGRITY_WARNING` (note which layer) | Archetype Manager (loader/validator) | 377 |
| Local-overrides-canonical with same `archetype_id` but divergent `archetype_version` | Local was forked from older canonical; canonical has since been updated upstream | Use local per merge_policy; surface as `STORE_DIVERGENCE_WARNING`; suggest user rebase local against new canonical | Archetype Manager (merge policy) | 378 |
| Two archetypes match in ambiguity band | Top-2 match scores within `ambiguity_band` of each other | Halt; show user both with scores; user picks or forces a third | Archetype Manager (matcher) / Guard G4 | 379 |
| Archetype matched but slot_schema has new required slots | Archetype version drift | Worker fills what it can; missing slots reported as `SLOT_GAPS` for archetype-refinement consideration | Worker + Archetype Manager (refinement) | 380 |
| Refinement proposal contradicts archetype's existing stable traits | Aggregator detects conflict | Surface to user; do not auto-apply; offer manual reconciliation | Aggregator (refinement reconciler) | 381 |
| Discovery worker proposes near-duplicate of existing archetype | New proposal's identity_signals overlap >0.85 with existing | Reject the new proposal; recommend refinement of the existing archetype instead | Aggregator (dedup) / Discovery Worker | 382 |
| Archetype store grows unboundedly | >100 archetypes (operational concern) | Warn at 50, 100; recommend manual consolidation pass; never auto-delete | Archetype Manager (capacity warn) | 383 |

---

## §7 Adversarial Probes (Whittaker) — verbatim

Source: lines 387-399. The spec presents these as prose paragraphs (not a table). The "Aggregator action" column the protocol asks for is not separately enumerated in §7; aggregator behavior is implicit in the "MUST" statements, which I quote verbatim and then mark the aggregator action as [DERIVED] when not literally stated.

| Probe (FR-tag from spec) | Trigger (verbatim) | Expected response (verbatim "MUST" / "SHOULD" rules) | Aggregator action | Spec line |
|---|---|---|---|---|
| **FR-2.1 Zero/Empty Attack** | "Subject with empty name, empty affiliation, zero sources returned, zero stable_traits extracted." | "Skill MUST NOT proceed past identity-verify with empty inputs; MUST NOT emit a persona with zero traits." | Aggregator never receives a persona for this subject (worker halted upstream); no persona block emitted [DERIVED from "MUST NOT emit a persona"] | 391 |
| **FR-2.2 Divergence Attack** | "Subject name resolves to two real public figures with overlapping affiliation history (e.g., 'John Smith' who worked at both Goldman *and* Polychain)." | "Identity verifier MUST surface both; orchestrator MUST halt." | Orchestrator halts upstream of aggregator; no aggregation occurs for this subject [DERIVED] | 393 |
| **FR-2.3 Sentinel Collision Attack** | "Subject whose entire public posture is 'no comment' or who systematically declines to articulate views (e.g., a fund partner with a sealed-lips reputation)." | "Worker MUST NOT confuse public silence with the user's `INSUFFICIENT_PUBLIC_DATA` sentinel; the dossier should explicitly note 'deliberate public reticence' as a stable trait." | Aggregator receives a normal persona block; the stable_traits list includes "deliberate public reticence" [DERIVED — emerges from worker dossier] | 395 |
| **FR-2.4 Sequence Attack** | "Research worker runs before identity verification completes." | "MUST be impossible by construction — verify is a sequential blocker per FR-2." | Aggregator never sees out-of-order outputs; structural invariant [DERIVED] | 397 |
| **FR-2.5 Accumulation Attack** | "Invocation with 50+ subjects." | "Skill SHOULD warn at N>10, hard-cap at N=25 unless `--force-large-batch` passed. Aggregator output for large batches MUST be paginated to avoid context overflow downstream." | Aggregator MUST paginate output for large batches (verbatim from §7) | 399 |

Note: §7 references "FR-2.x" sub-IDs as probe identifiers — these are probe labels, NOT references to FR-2 in §4. Cross-slice readers should not conflate them.

---

## §8 Three-Questions Test — verbatim

Source: lines 405-411 (heading `### 8.1 Acceptance gate per persona — Three-Questions Test`).

> ### 8.1 Acceptance gate per persona — Three-Questions Test
>
> For each produced persona, the worker writes three concrete questions the persona should ask any pitch in their domain. The Validator (when `--validate` is passed):
> 1. Spawns the persona as a subagent with no other context.
> 2. Presents it with the user's `context_artifact` (or a default board-pitch fixture).
> 3. Records the persona's first three questions.
> 4. Scores 0–10 on overlap with the worker-authored three-questions. Threshold: ≥7 = `OK`; <7 = `NEEDS_REFINEMENT`.

**Pass criteria (verbatim):** Threshold: **≥7 = `OK`; <7 = `NEEDS_REFINEMENT`** (line 411).

**Companion gates from §8 (lines 413-423):**

§8.2 Cross-cohort consistency (line 415, verbatim): "Spawn the same persona against two different topics (the user's pitch + an unrelated control fixture). The persona's vocabulary, frameworks, and pet-issues should remain stable across topics. Drift signals an over-specified context overlay leaking into the stable traits."

§8.3 Regression / reproducibility (line 419, verbatim): "Re-running the skill on the same subject within the cache TTL MUST return the same dossier and persona description (cache hit). Re-running after cache expiry MAY produce a new dossier; diff is reported in the summary."

§8.4 Fabrication probe — the hard test (line 423, verbatim): "Validator presents the persona with a leading question like 'what did you say about X in 2024?' where X is something the dossier does NOT cover. A faithful persona responds with hedging or 'I haven't taken a public position on that.' A fabricating persona invents content — that's a failure."

**Note on the relationship to FR-23:** the protocol task description references "the optional Validator invokes per FR-23." FR-23 itself lives in Part 1 (§4) and is outside this slice. Cross-slice readers should verify that FR-23 in Part 1 specifies "optional Validator invocation gated by `--validate` flag" consistent with §8.1's wording "when `--validate` is passed." [CROSS-SLICE-DEPENDENCY]

---

## §9.2 Model-Tiering Rules — verbatim

Source: lines 455-484 (heading `### 9.2 Model selection & tool routing — tiered for cost/speed`).

**Header rationale (line 457, verbatim):** "Per user spec: small/fast model for volume work, Opus reserved for synthesis-heavy stages."

**Stage → model table (verbatim, lines 459-469):**

| Stage | Recommended model | Rationale |
|---|---|---|
| Identity Verification | `claude-haiku-4-5-20251001` (Haiku) | Single-shot disambiguation; cheap and fast |
| Archetype Manager (matching) | Deterministic Python (no LLM) | §F algorithm is keyword-weighted; no model call needed |
| Per-source web search & extraction | **Tavily MCP** (preferred) → results processed by `claude-haiku-4-5-20251001` (Haiku) | High-volume, parallel; per-source extraction is mechanical pattern-matching against the archetype's source recipe |
| Per-source fact extraction & dossier-fragment writing | `claude-haiku-4-5-20251001` (Haiku) | One Haiku call per source; runs in parallel within a worker |
| Discovery worker — broad sweep | `claude-haiku-4-5-20251001` (Haiku) | Same volume profile as archetype-driven worker, just wider |
| **Cross-source consolidation per subject** | `claude-opus-4-7` (Opus) | Synthesis across many Haiku-extracted fragments into a coherent dossier requires Opus reasoning |
| **Persona description generation** | `claude-opus-4-7` (Opus) | The "modeled on" persona description is the highest-stakes output; voice fidelity matters |
| **Archetype proposal / refinement synthesis** | `claude-opus-4-7` (Opus) | Inferring the right generic-template structure from a subject's research is synthesis work |
| Validator (three-questions test spawn) | Same model as production party-mode usage | Validator must mirror runtime conditions for fidelity score to be meaningful |

**Hard rules (verbatim, lines 471-474):**

> - **FR-24:** Workers MUST NOT call Opus for per-source processing. Static check: budget allocator caps Opus token spend per worker at the consolidation step only.
> - **FR-25:** Web searches MUST route through Tavily MCP when Tavily is configured. Fallback to direct fetch only when Tavily is unavailable or for sources Tavily can't reach (e.g., authenticated PACER queries, on-chain block explorers via their own APIs).
> - **FR-26:** The run summary MUST report token spend per model tier so the user can see Opus is being reserved appropriately (target: <15% of total tokens spent on Opus).

**Per-worker cost shape (verbatim, line 483):** "This separation means a typical 12-minute per-subject worker runs ~50–100 Haiku calls (Tavily + extraction) and 1–2 Opus calls (consolidation, persona description)."

**Mapping to the protocol's three asks:**
- *Haiku per-source extraction (per-worker, per-source-call):* row 4 of table — "One Haiku call per source; runs in parallel within a worker" (line 464).
- *Opus cross-source consolidation (per-worker, after Haiku extraction):* row 6 of table — "Cross-source consolidation per subject" → Opus, plus the worked sequence on lines 481-483 ("After all sources processed, **Opus** consolidates the per-source fragments into the dossier markdown, stable_traits list, and three_questions").
- *<15% Opus token spend cap:* FR-26 line 474 (target). Acceptance test #12 (line 527) asserts the same threshold — verbatim: "Per FR-24/FR-26, Opus token spend in a typical per-subject worker run is <15% of total tokens." Note: FR-26 wording calls <15% a *target*, while acceptance test #12 treats it as an *assertion threshold*. [INTERNAL-WORDING-TENSION — see Internal Contradictions below.]

---

## §9.2 Tavily Routing Rules — verbatim

Source: same section, lines 463, 473, 476-481.

**Tavily-preferred routing (verbatim, line 463):** "Per-source web search & extraction | **Tavily MCP** (preferred) → results processed by `claude-haiku-4-5-20251001` (Haiku)"

**Mandate (verbatim, FR-25 line 473):** "Web searches MUST route through Tavily MCP when Tavily is configured. Fallback to direct fetch only when Tavily is unavailable or for sources Tavily can't reach (e.g., authenticated PACER queries, on-chain block explorers via their own APIs)."

**Fallback rules:** §9.2 does NOT enumerate specific 5xx/429 thresholds. The only fallback condition stated is "Tavily is unavailable" (line 473). The protocol asks for "fallback rules on 5xx errors" — these are NOT specified in §9.2. The spec explicitly defers this question: §12 Open Question 9 (line 550, verbatim): "Tavily-MCP availability fallback. Per FR-25, fallback to direct fetch when Tavily is unavailable. What's the threshold for declaring 'unavailable' — first 429, repeated 5xx, MCP disconnect? Define operational policy." [SPEC-GAP — operational threshold for "unavailable" is an open question, not a verbatim rule.]

**Source-category-to-API mapping (verbatim, lines 476-481, "Tavily MCP usage pattern (per worker)"):**

> 1. For each source in the matched archetype's `source_recipe`, the worker constructs the query from the slot bindings (e.g., `tavily_search(query="Polychain Capital Form D site:sec.gov")`).
> 2. Tavily returns ranked results with snippets.
> 3. Haiku processes each result against an extraction template ("from this snippet, extract: deal date, amount, lead/follow signal, attributed quotes if any, source URL").
> 4. Extracted fragments accumulate per source category.
> 5. After all sources processed, **Opus** consolidates the per-source fragments into the dossier markdown, stable_traits list, and three_questions.

**Source-category mapping NOT verbatim:** The spec exemplifies "PACER queries" and "on-chain block explorers via their own APIs" as cases Tavily can't reach (line 473), implying a category split — but it does not enumerate a complete category-to-API mapping. The closest enumeration of source categories is in Appendix E `source_recipe` (lines 766-774, outside this slice) which references `tier_1_regulatory: SEC_EDGAR`, `tier_2_deal_history` (truncated at slice boundary). [CROSS-SLICE-DEPENDENCY — full category enumeration is in Appendix E, which Part 3 owns past line 660.]

---

## §9.1 Promotion Workflow — verbatim summary

Source: lines 435-453.

**Policy (verbatim, line 437):** "The skill does NOT auto-promote local archetypes into the canonical store. Promotion is a deliberate human action because canonical archetypes ship with the skill and affect every future install."

**Promotion-candidate criteria (verbatim, lines 441-445):**

> A local archetype is a promotion candidate when ALL of the following hold:
> 1. It has been refined from ≥3 distinct subjects (`refined_from_subject_count >= 3`)
> 2. It has been stable (no refinement deltas) for ≥30 days
> 3. Its `archetype_version` >= 2 (proves at least one refinement cycle happened)
> 4. No corresponding `archetype_id` exists in the canonical store, OR the local version is materially newer than canonical

**Manual workflow (verbatim, lines 447-451):**

> When the user decides to promote, the workflow is the standard SuperClaude src/.claude pattern:
> 1. User copies the local archetype YAML from `./.claude/skills/sc-persona-research-protocol/personas/<id>.yaml` to `<IronClaude>/src/superclaude/skills/sc-persona-research-protocol/personas/<id>.yaml`
> 2. User runs `make sync-dev` (per global CLAUDE.md) so all `.claude/` install copies pick it up
> 3. User commits the change to the IronClaude repo
> 4. On next invocation in any project, the archetype is now resolved from canonical

**Skill behavior (verbatim, line 453):** "The skill's run summary SHOULD print the suggested copy command for each candidate. It does not execute the copy."

---

## Appendix C — Three-Questions Test Template

Source: lines 656-672.

Appendix C provides a **template format** (not additional rules). Verbatim block (lines 661-670):

```
Three-Questions Test for [Persona Code]
========================================

1. [Question]
   Why: [What this question reveals about the persona's worldview / area of focus]
   Source signal: [Which dossier evidence anchors this question]

2. [...]
3. [...]
```

**Validator scoring detail (verbatim, line 672):** "When run by the Validator, a faithful persona spawns and (without seeing this test) asks questions whose Jaccard similarity with the test set is ≥0.5 over question keywords/concepts."

**Cross-reference to §8.1 — possible internal tension:** §8.1 line 411 states the threshold as "0–10 score, ≥7 = OK." Appendix C line 672 states the underlying similarity metric is "Jaccard similarity ≥0.5 over question keywords/concepts." These can be reconciled (0–10 scaled = 0.7 normalized, while Jaccard 0.5 may be the floor of the lowest passing band) but the spec does NOT define the explicit mapping between the 0-10 score and Jaccard 0.5. [INTERNAL-METRIC-AMBIGUITY — flagged below.]

---

## Appendix D — Worked Example Trace

Source: lines 676-692.

**Inputs (verbatim, lines 681-685):**

```yaml
subjects:
  - { name: "Josh Rosenthal",   affiliation: "Polychain Capital",       role: "Partner" }
  - { name: "Pierre Planche",   affiliation: "Griffin Gaming Partners", role: "Partner" }
  - { name: "Thomas Larrison",  affiliation: "Gala",                    role: "Executive" }
context_artifact: "@/config/workspace/shrapnel-gov/board-presentation-brief.md"
```

**Expected outputs (verbatim, lines 689-692):**
- 3 dossier files in `_bmad-output/planning-artifacts/persona-research/`
- 3 persona TOML blocks
- 1 unified diff against `_bmad/custom/config.toml` adding `board-rosenthal-mod`, `board-planche-mod`, `board-larrison-mod` while preserving the generic archetypes (`board-polly`, `board-greta`)
- Validation report (if `--validate` passed) with three fidelity scores

**Component flow trace (input → component → output):**

| Step | Component invoked | Input | Output | FR/Component reference |
|---|---|---|---|---|
| 1 | Identity Verifier (Haiku per §9.2) | 3 `{name, affiliation, role}` triples | 3 verified identities (assuming none ambiguous/deceased) | FR-2 sequential blocker (§4, Part 1); §6 row "Identity ambiguous" (line 364) |
| 2 | Archetype Manager (deterministic Python per §9.2) | 3 verified subjects + canonical+local archetype roster | 3 match decisions: likely `MATCH` for Rosenthal (crypto-native VC archetype), `MATCH` for Planche (gaming-VC archetype if exists, else `NO_MATCH`), `MATCH` for Larrison (strategic-corporate-exec archetype if exists, else `NO_MATCH`) | §5.6 merge rules (line 345); Guard G4 (line 591); §12 OQ-6 (line 547) re bootstrap archetypes |
| 3a | Archetype-Driven Workers (parallel) | matched subjects + their archetype source_recipe | per-subject dossier + stable_traits + three_questions | §5.1 architecture (Part 1); FR-2 parallel; §9.2 worker pattern lines 476-481 |
| 3b | Discovery Workers (parallel, if NO_MATCH) | unmatched subjects | per-subject dossier + proposed new archetype | §6 line 382 (dedup check); §9.2 row "Discovery worker — broad sweep" (line 465) |
| 4 | Per-source extraction inside each worker | source_recipe entries | per-source fragments | Tavily MCP → Haiku per §9.2 lines 463-464, 476-481 |
| 5 | Cross-source consolidation (Opus) inside each worker | per-source fragments | dossier markdown + stable_traits + three_questions | §9.2 row "Cross-source consolidation" (line 466); FR-24 (line 472) |
| 6 | Persona description generation (Opus) | consolidated dossier | "modeled on" persona description | §9.2 row "Persona description generation" (line 467); §10.1 disclaimer prepended (lines 491-493, **outside slice — Part 3**) |
| 7 | Aggregator | 3 persona blocks + K archetype proposals/refinements | 1 unified `config.toml` diff + archetype proposals | §6 lines 381-382 (refinement reconciliation); Appendix B Stage 5 (lines 630-633) |
| 8 | Approval Gate | aggregator output | user-approved diffs | Appendix B Stage 6 (lines 635-637); Acceptance #11 (line 526) |
| 9 | Validator (optional, if `--validate`) | 3 personas + their three_questions tests | 3 fidelity scores | §8.1 (lines 405-411); FR-23 [Part 1]; §9.2 row "Validator" (line 469) |

**FR/component invocations explicitly named in Appendix D:** None directly cited by FR-number. The example is illustrative; trace is reconstructed by mapping outputs ("3 dossiers", "3 TOML blocks", "1 unified diff", "validation report") to the components in §5 (Part 1) and the model-tier table in §9.2.

**Companion archetypes preserved:** Output bullet line 691 says "while preserving the generic archetypes (`board-polly`, `board-greta`)." This is a verbatim instance of FR's `archetype_companion: true` default referenced in §10.4 (line 508, **outside slice — Part 3**). [CROSS-SLICE-DEPENDENCY]

---

## Cross-Slice References

References from §6/§7/§8/§9 (this slice) that point INTO Part 1 (§4 FRs) or Part 3 (§10 ethics):

| From (this slice, line) | To (other slice) | Verbatim text |
|---|---|---|
| §7 line 397 | Part 1 §4 FR-2 | "MUST be impossible by construction — verify is a sequential blocker per **FR-2**." |
| §8.1 lines 405-411 | Part 1 §4 FR-23 (per protocol description) | Three-questions test is the gate the optional Validator invokes per FR-23. The text "FR-23" does NOT appear verbatim in §8.1; the linkage is via the protocol task description. The verbatim trigger is: "The Validator (when `--validate` is passed)" (line 407). |
| §9 line 429 | Part 1 §4 FR-13 | "Per **FR-13**, dossiers cached at `<dossier_dir>/.cache/<sha>/`." |
| §9.2 line 472 | Part 1 §4 FR-24 (introduces FR-24) | "**FR-24:** Workers MUST NOT call Opus for per-source processing." (FR-24 is *defined* here, not just referenced — Part 1's FR table must include it for consistency.) |
| §9.2 line 473 | Part 1 §4 FR-25 (introduces FR-25) | "**FR-25:** Web searches MUST route through Tavily MCP when Tavily is configured." (FR-25 is *defined* here.) |
| §9.2 line 474 | Part 1 §4 FR-26 (introduces FR-26) | "**FR-26:** The run summary MUST report token spend per model tier..." (FR-26 is *defined* here.) |
| §11 Acceptance #1 line 516 | Part 1 §4 FR-1 through FR-23 | "✅ FR-1 through FR-23 all pass (per-FR acceptance criteria above)." |
| §11 Acceptance #2 line 517 | §7 (this slice) | "All five Whittaker probes (§7) verified by red-team test cases" |
| §11 Acceptance #3 line 518 | Part 3 §10.1 | "The mandatory disclaimer (§10.1) appears verbatim in every produced persona description." |
| §11 Acceptance #9 line 524 | Part 1 FR-22 | "A linter check rejects any archetype containing person names, fund names, or company names in core fields (FR-22)." |
| §11 Acceptance #12 line 527 | §9.2 FR-24/FR-26 | "Per FR-24/FR-26, Opus token spend in a typical per-subject worker run is <15% of total tokens." |
| §11 Acceptance #13 line 528 | §9.2 FR-25 | "Per FR-25, when Tavily MCP is configured, all general web searches route through Tavily." |
| §12 OQ-3 (resolved) line 537 | §9.2 (this slice) | Validator model selection resolved against §9.2. |
| §12 OQ-9 line 550 | §9.2 FR-25 | "Per FR-25, fallback to direct fetch when Tavily is unavailable. What's the threshold..." |
| §10.1, §10.4 | Part 3 | Disclaimer (§10.1) and `archetype_companion` (§10.4) referenced by §11 acceptance and Appendix D respectively but DEFINED in Part 3. |

**Most important structural finding:** **FR-24, FR-25, FR-26 are *introduced* (defined) inside §9.2 of this slice, not in §4.** Part 1's FR table (§4) MUST include these three FRs to be consistent. The protocol asked us to flag cross-slice contradictions; this is the most actionable one. [CROSS-SLICE-CONSISTENCY-RISK — Part 1 must enumerate FR-24/25/26.]

---

## Internal Contradictions / Tensions

1. **FR-26 "target <15%" vs Acceptance #12 "assert <15%":** FR-26 line 474 phrases the Opus spend cap as a target ("target: <15% of total tokens spent on Opus"). Acceptance #12 line 527 phrases it as an assertion ("assert the per-tier spend report"). Targets are aspirational; assertions are pass/fail. The spec should clarify which it is. [INTERNAL-WORDING-TENSION]

2. **§8.1 score ≥7/10 vs Appendix C Jaccard ≥0.5:** §8.1 line 411 specifies a 0–10 score with ≥7 pass threshold. Appendix C line 672 specifies "Jaccard similarity ≥0.5 over question keywords/concepts." The mapping between the 0–10 score and the Jaccard value is not defined. A persona could plausibly score Jaccard 0.5 (passing per Appendix C) but compute to <7 on the 0-10 scale (failing per §8.1) depending on how the score is derived. [INTERNAL-METRIC-AMBIGUITY]

3. **§7 FR-2.1 "MUST NOT emit a persona with zero traits" vs §6 row 366 "Return INSUFFICIENT_PUBLIC_DATA; do not fabricate":** Compatible — both prevent empty persona emission — but they use different sentinel languages. §6 names a sentinel (`INSUFFICIENT_PUBLIC_DATA`); §7 just says "MUST NOT emit." The implementation needs both behaviors unified: refuse-with-sentinel, not silent-skip. [MINOR-WORDING-DIVERGENCE]

4. **§9.2 Tavily fallback "when Tavily is unavailable" vs §12 OQ-9 "what's the threshold for unavailable":** FR-25 mandates a fallback rule but the threshold is explicitly an open question. The spec is internally consistent in flagging the gap, but downstream implementers cannot satisfy FR-25 without resolving OQ-9. [SPEC-GAP, ACKNOWLEDGED]

5. **§6 row 379 ambiguity-band halt vs Appendix A Guard G4 line 600 "AMBIGUOUS" handling:** Both say halt-on-ambiguous; consistent. But Guard G4 line 601 also defines `archetype_hint` → `MATCH(forced)` (skip scoring), which §6 does not enumerate as a failure-mode escape hatch. Not a contradiction, but the failure-mode table is incomplete relative to the guard table. [MINOR-OMISSION]

6. **§9.2 Validator model row "same model as production party-mode usage" (line 469) vs §11 Acceptance #4 "≥7/10 fidelity on a held-out test subject" (line 519):** The validator model is specified as runtime-mirroring; acceptance #4 specifies a fidelity threshold. These are compatible but the held-out test subject is not defined ("e.g., a well-documented public figure not in the original use case"). A concrete fixture is missing. [TESTING-GAP]

7. **§9.2 hard rule FR-24 applies to "per-source processing" but §9.2 table row 6 line 466 names cross-source consolidation as the Opus step:** Consistent — the hard rule excludes Opus from per-source work, and the consolidation row places Opus at the synthesis step. No contradiction; clean separation.

---

## Summary

This slice (lines 361-660) of the persona-research spec defines:

- **§6:** A 21-row failure-mode table (Failure | Detection | Behavior) covering identity, sourcing, worker budget, archetype-store integrity, merge divergence, ambiguity, and capacity. Architecture-component mapping is implicit; Part 1's §5 names the components.

- **§7:** Five Whittaker adversarial probes (FR-2.1 through FR-2.5) covering empty-input, name-divergence, sentinel-collision, sequence-violation, and accumulation attacks. Aggregator behavior is mostly derived from upstream MUST/MUST NOT rules rather than enumerated separately.

- **§8:** A four-part validation regime — three-questions test (≥7/10 score gate per §8.1), cross-cohort consistency (§8.2), regression (§8.3), and fabrication probe (§8.4, the hard test that overrides the soft fidelity gate per the §-end disagreement-resolution note line 718). Appendix C provides the test template format and reveals the underlying Jaccard ≥0.5 metric.

- **§9.1:** Promotion workflow — explicit no-auto-promote policy, four-criteria candidate definition (≥3 subjects, ≥30 days stable, version ≥2, not-in-canonical-or-newer), manual src/.claude pattern.

- **§9.2:** Tiered model strategy with three NEW FRs introduced here (FR-24 no-Opus-per-source, FR-25 Tavily-MCP-mandate, FR-26 token-spend-reporting <15% Opus target). Per-worker shape: ~50–100 Haiku calls + 1–2 Opus calls per 12-min subject.

- **Appendix D:** Worked example for the Neon Machine board-prep use case with 3 named subjects (Rosenthal/Planche/Larrison) and expected 3 dossiers + 3 TOML blocks + 1 unified diff + optional validation report.

**Top cross-slice action items for the team:**

1. **Part 1 §4 FR table MUST include FR-24, FR-25, FR-26** — they are introduced here, not in §4. Without this, the spec's FR numbering is inconsistent.
2. **Part 3 §10.1 disclaimer** is referenced by §11 acceptance #3 in this slice but defined in Part 3. Verify wording matches.
3. **Part 3 §10.4 archetype_companion default** is the basis for the "preserving generic archetypes" guarantee in Appendix D's expected output.
4. **§12 OQ-9 (Tavily-unavailable threshold)** is a known operational gap that downstream implementation tasks must resolve before FR-25 can be tested deterministically.

**Top internal tensions:**
- FR-26 "target" vs Acceptance #12 "assert" wording on the <15% Opus cap.
- §8.1 0–10 score vs Appendix C Jaccard 0.5 — unmapped metric translation.
- §6 sentinel `INSUFFICIENT_PUBLIC_DATA` vs §7 "MUST NOT emit a persona with zero traits" — same intent, different language.

**Status:** Complete
