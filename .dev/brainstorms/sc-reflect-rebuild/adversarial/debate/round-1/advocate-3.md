# Round 1 — Advocate for Variant 3

## Position Summary

Variant 3 is the leanest, most opinionated protocol in the field: 569 lines, 6 waves, 2 refs, a 14-field return contract, and zero tolerance for deprecated tool surfaces. Every other variant inflates the protocol with either (a) fractional waves and 9-wave architectures that duplicate gatekeeping work, (b) optional scripting of deprecated `think_about_*` tools that creates audit noise without evidence of value, (c) 20+ field return contracts that couple downstream consumers to unstable telemetry, or (d) Ops Integration sections that belong in CLAUDE.md, not a protocol skill. V3's minimalism is not a deficiency — it is the correct default for a v1 skill that must survive eval iteration without accumulating baggage.

The core thesis: **the simplest protocol that delegates everything non-orchestration to existing agents/skills will iterate fastest, ship soonest, and accumulate the least technical debt.** Every additional wave, ref file, return-contract field, and optional tool invocation is a maintenance surface that must survive unchanged across eval iterations. V3 minimizes that surface.

## Steelmen of Opposing Variants

### Variant 1 — Strongest Argument

V1's classification-precedence rule (§10.5: Regression > Drift > Necessary > Authorized) is the single most valuable structural contribution across all five variants. V3 defaults to Drift on ambiguity (§1.5, Wave 1 step 5) which is conservative but loses the ability to distinguish "I found evidence of regression AND an inline rationale" from "I found neither evidence nor rationale." V1 resolves this deterministically: rationale does not authorize contradiction. This is a genuine improvement in deviation classification precision that any merged output should adopt.

### Variant 2 — Strongest Argument

V2's `[INFERRED]` tag as a first-class claim category (§11.1) combined with the zero-drop audit flag (§11.2) creates a falsifiable hallucination guardrail that V3 lacks. V3 drops ungrounded claims silently and marks `status: partial`, but it does not surface *how many* claims were inference vs evidence. V2's binary Grounded/`[INFERRED]` tag makes the report auditable: a downstream consumer can see the inference ratio, a meta-eval can flag zero-drop passes as suspicious, and the report header surfaces `citations_inferred: N`. This is a low-cost, high-value structural guard that V3 should adopt.

### Variant 4 — Strongest Argument

V4's Testability Map (§16) is a design principle that should be a merge criterion: every protocol decision must map to at least one eval assertion. V3 has 5 eval dimensions and 4 assertion DSL types, but it does not explicitly link protocol steps to assertions. This creates a risk that eval iteration will leave protocol steps untested. V4's Testability Map is 11 rows, each mapping a protocol decision to a specific assertion type and target. If a protocol step cannot map, V4 says "simplify or remove it." This discipline would catch the parts of V3 that are untestable (e.g., the "default to Drift on ambiguity" rule has no dedicated assertion).

### Variant 5 — Strongest Argument

V5 is the only variant with a dedicated Ops Integration section (§9), and its Makefile target proposal (`make reflect-eval`, `make reflect-eval-quick`) closes the gap between "protocol is written" and "protocol is exercised in CI." V3's Build Path Decision (§10) describes the eval workspace layout but does not address how the eval gets run after the skill is installed. Without CI integration, the eval harness decays. V5's concrete Makefile targets and CI cadence (every PR touching the skill, <30s quick, <2min full) are production-grade operational discipline.

## Strengths of Variant 3 (with evidence)

### S1. Shortest protocol, lowest cognitive load — by design

At 569 lines, V3 is 13% shorter than V4 (586 lines), 12% shorter than V1 (658 lines), 12% shorter than V2 (650 lines), and 34% shorter than V5 (864 lines). This is not accidental — V3's §14 Refs explicitly states: "Two refs total. Intentionally minimal — the protocol logic lives in this SKILL.md; refs contain only schema templates" (V3 §14, lines 553-557). Every other variant has 4-7 refs files, each of which must be maintained, versioned, and kept consistent with the SKILL.md during eval iterations. Fewer refs = fewer sync surfaces = faster iteration cycles.

### S2. Only variant with an explicit Kill List

V3 §13 (lines 518-544) enumerates 5 deliberately-excluded features with justification: coverage-mapper agent, deviation-classifier agent, streaming dialogue, knowledge graph, T1 multi-model. No other variant has this. The Kill List serves two functions: (a) it prevents scope creep during implementation — a future contributor cannot "discover" that coverage-mapper should have been a separate agent without confronting the documented rationale, and (b) it provides a clear escalation path — "Extract only if eval shows Wave 1 inline logic is fragile" (V3 §13, item 1). This is engineering discipline that the other variants lack.

### S3. Cleanest think_about_* elimination

V3 §6 (lines 352-373) states: "Zero references to deprecated think_about_* tools. The rebuild eliminates the legacy surface entirely." Compare V1 §6.4 which wires all three as "mandatory scripted nudges," V4 §4 Wave 1.5 which makes them "mandatory checkpoint gates," and V5 §5 which calls them "mandatory scripted checkpoints." The diff analysis flags this as X-005 (High severity) — the variants genuinely disagree on whether these tools are current, deprecated, load-bearing, or optional. V3 takes the strongest, simplest position: eliminate them. If future eval evidence shows they add value, they can be added back. But starting without them avoids the ambiguity that V1/V4/V5 embed by having "mandatory but not load-bearing" invocations that consume audit-log space and developer attention without measurable impact.

### S4. Leanest return contract — minimal coupling

V3's stable return contract has ~14 fields (§3, lines 84-103). V1 has ~28 fields (§9.1, lines 303-347). V2 has ~22 fields. V4 has ~18 fields. V5 has ~15 fields. V3's contract contains exactly what a downstream consumer needs: status, mode, tier, coverage, deviation counts, recommendation, and paths. It omits `citations_dropped`, `citations_inferred`, `reviewer_cards`, `asymmetric_flags`, `escalation_rule_matched`, `best_practice_grade`, and other telemetry that belongs in the non-stable block. This is a composability advantage: `/sc:task`, `/sc:tasklist`, and CI pipelines can parse V3's contract without depending on fields that change across versions.

### S5. Fewest waves — simplest execution graph

V3 has 6 waves (W0-W5). V1 and V4 have 9 waves. V2 has 7. V5 has 7. V3 achieves T1+T2+T3 in 6 waves because it does not separate "evidence validation" into its own wave (it is embedded in Wave 4 Synthesis) and does not have a fractional wave (W2.5) for the tier gate (it is Wave 2 in V3). The diff analysis notes S-004 as Medium severity. The practical impact is lower: fewer waves means fewer handoff points, fewer audit-log entries, and fewer opportunities for mid-wave state corruption.

### S6. Conservative deviation classification defaults to Drift

V3 Wave 1 step 5 (lines 208-209): "Items without a documented rationale default to drift (conservative)." This is the safest default for a v1 protocol because drift is actionable (it triggers escalation in Wave 2) but not irreversible (it does not force T3 remediation). V2's precedence rule is more sophisticated, but V3's default is simpler to implement, simpler to test, and simpler to explain to users. Combined with V2's precedence rule in a merge, V3's conservative default provides the floor while V2 provides the ceiling.

### S7. Token cost profile is explicitly bounded

V3 §15 (lines 559-569) gives per-tier token estimates with T1 at 3-9k Claude tokens, which matches the diff analysis's practical concern about keeping T1 cheap. V1 estimates T1 at 3-8k (similar), V2 at 3-8k, but V5's T1 range extends to 3-8k and T2 to 35-70k Claude tokens without the explicit "hard kill at 1.25x" guard that V1 and V2 include. V3's T1 estimate of 3-9k is the tightest band, reflecting the minimal-wave architecture.

## Weaknesses of Opposing Variants (with evidence)

### Against V1: Over-engineered wave architecture

V1's 9-wave architecture includes Wave 1A, 1B, 1C, 1D as sub-waves of Wave 1, plus a fractional Wave 2.5 for the tier gate, plus a separate Wave 6 for evidence validation that could be embedded in the synthesis wave. The 9-wave structure (V1 §4, lines 91-106) creates 9 entry/exit boundary pairs that must each be tested. V3 achieves the same T1→T2→T3 escalation in 6 waves. The extra waves in V1 do not add capabilities — they add coordination overhead.

### Against V1: 7 ref files create maintenance drag

V1 §16 (lines 600-611) lists 7 ref files: `input-resolution.md`, `reflection-rubric.md`, `deviation-taxonomy.md`, `coverage-mapping.md`, `reviewer-spec.md`, `report-template.md`, `remediation-handoff.md`. Each ref must be authored, reviewed, and kept consistent with the SKILL.md during eval iterations. V3 has 2 refs. The diff analysis C-020 shows V1 with 6 refs, V2 with 7, V4 unspecified, V5 with 4. More refs means more places for the protocol to drift from its documentation. V3's approach — protocol logic inline, only schema templates externalized — reduces this risk.

### Against V2: Hallucination guardrails section is feature creep for v1

V2's dedicated §11 Hallucination Guardrails section (5 subsections, ~70 lines) introduces the `[INFERRED]` tag, zero-drop audit flag, blind calibration explanation, heterogeneous ensemble explanation, citation re-Read window, and inferred-claim audit threshold. These are all valuable, but they are not protocol steps — they are design justifications and behavioral assertions that belong in a SPEC.md or design rationale, not in a SKILL.md that an LLM reads at session start. Every line in SKILL.md costs session-context tokens. V3 achieves the same behavioral outcome (drop ungrounded claims, mark status partial) in 3 lines of Wave 4 step 3.

### Against V2: 5 hallucination guards are design rationale, not execution instructions

More specifically, V2 §11.3 (blind calibration) and §11.4 (heterogeneous ensemble) explain *why* the protocol works, not *what to do*. The LLM reading the SKILL.md does not need to be convinced of its own architecture — it needs step-by-step execution instructions. V3 embeds calibration as Wave 3 step 2 ("Calibrate each output independently") and heterogeneity as Wave 3 agent table ("calibrator sonnet, root-cause sonnet/opus, optional quality-engineer haiku"). These are equivalent behaviors without the prose overhead.

### Against V4: think_about_* in allowed-tools frontmatter is a footgun

V4 is the only variant that lists `mcp__serena__think_about_collected_information`, `mcp__serena__think_about_task_adherence`, and `mcp__serena__think_about_whether_you_are_done` in the `allowed-tools` frontmatter (V4 §frontmatter, line 7). This makes them load-bearing by declaration: the protocol says "these tools are authorized" and then says "they are mandatory checkpoint gates." If the tools are removed or renamed upstream, V4 breaks. V3's approach — zero references, not even in the frontmatter — has no such dependency. The diff analysis X-006 notes this as High severity: "V4 is the ONLY variant with think_about_* in allowed-tools." A single-variant dependency on a contested tool surface is a risk, not a strength.

### Against V4: 5-category deviation taxonomy adds an escape hatch

V4 is the only variant with a 5th deviation category: `unknown` (diff analysis X-009). This is an escape hatch that reduces classification precision: when the classifier is uncertain, it can tag `unknown` instead of making the hard choice. V3 forces the hard choice with its "default to Drift on ambiguity" rule. The `unknown` category sounds safe but it is not — it produces a report that says "I found something but I don't know what it is," which is less actionable than "I found something and my best classification is Drift (conservative default)." An `unknown` classification also cannot drive remediation: V4 has no default remediation for `unknown` items, so they become dead-end findings that consume report space without resolution path.

### Against V4: 7 eval dimensions dilute grading focus

V4 §9 defines 7 grading dimensions (diff analysis X-011): Citation accuracy, Source coverage, Deviation classification, Best-practice grounding, Recommendation actionability, Tier-routing correctness, Artifact contract compliance. V3 has 5 dimensions. The extra dimensions in V4 (Tier-routing correctness, Artifact contract compliance) test protocol mechanics, not reflection quality. A tier-routing bug is a code bug, not a skill-quality issue — it should be caught by unit tests, not by the eval rubric. V3's 5 dimensions focus on what matters: coverage, classification, citations, recommendations, false-positives.

### Against V5: Ops Integration section belongs in CLAUDE.md, not SKILL.md

V5 §9 (lines 622-711) devotes ~90 lines to Makefile targets, file-layout discipline, PreToolUse hook awareness, sync-dev/verify-sync compliance, and CI cadence. Every one of these concerns is either (a) already enforced by CLAUDE.md absolute rules, (b) already enforced by the PreToolUse hook in `.claude/settings.json`, or (c) generic to every skill in the repo, not specific to sc:reflect. Including them in SKILL.md bloats the protocol file without adding protocol-specific logic. If every skill repeated these rules, the repo would double in size with zero new information. The Makefile targets themselves (`make reflect-eval`, `make reflect-eval-quick`) are valuable but belong in the project Makefile, not in the skill protocol.

### Against V5: Composite scoring adds complexity without demonstrated precision

V5's tier rubric (§3, lines 77-101) uses a 5-signal 0-2-point composite scoring system (max 10 points) with a multi-domain override that adds +3 points. This is more complex than V3's 4-signal threshold table, but the diff analysis (C-001) notes all approaches as "High severity" disagreement, meaning none has empirical justification over the others. V3's simpler approach — 4 signals, threshold-based routing, no composite arithmetic — is easier to debug, easier to test, and easier to explain. If eval evidence shows the composite approach is more accurate, it can be adopted in v1.1. The multi-domain +3 override is particularly concerning: a cross-module change that would otherwise score 2 (T1 territory) gets bumped to 5 (T2 territory) purely because it touches two domains. This may be appropriate but the +3 bonus is uncalibrated and could produce false escalations on trivial cross-domain changes (e.g., updating a doc string in both `src/` and `docs/`).

### Against V5: Longest variant at 864 lines defeats the "load on-demand" design

V5 is 864 lines — 52% longer than V3. The skill-loading mechanism described in CLAUDE.md states that skills are "loaded on-demand, ~50 tokens each at session start." The SKILL.md file itself is the skill — a longer file means more tokens consumed at load time, more context window pressure during execution, and more surface area for inconsistencies. V3's 569-line protocol is within the 400-700 line band that V1-V4 occupy; V5 is the outlier at 864 lines, well above the next longest (V1 at 658). The extra length comes primarily from the Ops Integration section and the detailed Build Path analysis, neither of which the LLM needs to read at execution time.

## Concessions (genuine V3 weaknesses)

### C1. V3 lacks a classification-precedence rule

V3 defaults to Drift on ambiguity but does not specify what happens when signals for multiple categories coexist. V2's Regression > Drift > Necessary > Authorized precedence (§10.5) is genuinely better. V3 should adopt this in the merged output.

### C2. V3's T1 coverage floor (>=0.85) is the lowest in the field

The diff analysis X-001 shows V3 at 0.85, V1 at 0.95, V4 at 1.00. V3's floor means a T1 pass can ship with 15% of requirements unmapped. This is defensible for a quick-pass tier (V3 explicitly says `--depth quick` forces T1 even if the rubric says escalate), but it is the most permissive stopping condition. If merged output raises the floor to 0.90 (matching V2 and V5), V3's simpler rubric still works.

### C3. V3 has no hallucination-specific guardrail section

V3 drops ungrounded claims in Wave 4 step 3 but does not tag inference vs evidence, does not audit zero-drop passes, and does not surface inference ratios. These are genuinely useful for meta-evaluation and should be adopted from V2's §11.1 and §11.2 in the merged output.

### C4. V3's return contract is missing fields that downstream consumers need

V3 omits `citations_dropped`, `confidence_calibrated`, `escalation_rule_matched`, and `grounding_quality_tier`. A CI pipeline consuming V3's contract cannot distinguish "passed with zero dropped citations" from "passed because evidence-validator was skipped." V1's asymmetric_flags block (§9.1, lines 344-346) addresses this and should influence the merged output.

### C5. V3 does not address env-var model-alias awareness

V5 §4 Wave 0 step 6 checks `ANTHROPIC_DEFAULT_*` env vars and degrades gracefully. V3 assumes model aliases are available. If the user's environment lacks `ANTHROPIC_DEFAULT_HAIKU_MODEL`, V3's T2 reviewer topology (confidence-calibrator as sonnet, root-cause-analyst as sonnet/opus, quality-engineer as haiku) cannot spawn the optional quality-engineer. V3 should add a degraded-mode check in Wave 0.

### C6. V3's adversarial invocation is less detailed than V1/V2

V3's Wave 3 step 3 (lines 277-284) invokes sc:adversarial with a 4-line command template and a single convergence threshold check. V1 §8 (lines 286-293) includes explicit empty-response/partial-parse/missing-file guards with a 3-tier fallback protocol (F1/F2/F3). V2 §13 (lines 527-554) includes a "Sequenced build" table with explicit phase/tool/output columns. V3's brevity here means the implementer must infer fallback behavior rather than follow explicit instructions. V3 should adopt V1's 3-tier fallback guard without inflating the wave count.

### C7. V3 lacks explicit "both present → post" mode-detection rule

V3 §2 (lines 70-74) has 3 auto-detection rules. V1 §3.2 (lines 70-76) has 4 rules plus hard STOP conditions. V2 §2 (lines 65-69) has a 4-row signal table. V4 §2 (lines 47-52) has a 4-row signal table. V5 §3 (lines 56-64) has 6 rules. V3's 3-rule set is the simplest but may not cover all input combinations — specifically, V3 does not explicitly handle "both plan AND completed-work present" (it handles "diff, commit range, output-dir, or --scope pointing to changed files → post" but not "tasklist + output-dir simultaneously"). The merged output should adopt V1/V2's explicit "both present → post" rule.

## Shared Assumption Responses

### A-001: "The user is technically capable of reading a 400-700 line SKILL.md and translating section refs into action"

**QUALIFY.** V3 is 569 lines — the shortest variant — specifically because it minimizes this assumption's burden. A 569-line protocol is meaningfully easier to navigate than an 864-line one (V5). But the assumption holds: even 569 lines requires technical literacy. The correct mitigation is not shorter files (V3 is already near the minimum) but better ref files and clearer section headers, which V3 provides.

### A-002: "The ANTHROPIC_DEFAULT_* env-var aliases will remain set in the user's environment"

**QUALIFY.** V3 should adopt V5's degraded-mode check in Wave 0. Currently V3 assumes aliases are present. A single env-var check + WARN in Wave 0 step 4 (after Serena activation) would close this gap without inflating the protocol. V3's fail-open policy on Serena (V3 §6, line 371) should extend to model aliases.

### A-003: "The .dev/eval-workspaces/sc-reflect/ workspace path is the right naming"

**ACCEPT.** V3 §9 (line 414) explicitly states `.dev/eval-workspaces/sc-reflect/` and cites the CLAUDE.md override. This is consistent with V1-V4. V5's use of `sc-reflect-protocol` (V5 §9.2) is the outlier.

### A-004: "The 60/40 train/test split (Anthropic skill-creator default) is the right split for reflect's eval matrix specifically"

**QUALIFY.** The 60/40 split is inherited, not justified. For a skill with as few eval cases as sc:reflect (3 pilot, 8-12 expanded), the held-out set at 40% is 1-5 cases — too few for statistical power. V3 should use 60/40 for iteration-1 (matching the tooling) but consider a fixed held-out set of at least 5 cases for iteration-2+, regardless of the ratio that produces.

### A-005: "The skill operates on a single repo / single project context"

**ACCEPT.** All 5 variants assume single-repo. Multi-repo reflection is a different product. V3's memory key convention (`reflection-last-pass-{project-slug}`) is scoped per-project, which is the right boundary for v1.

## Per-Point Position on Key Contradictions

### X-001 (T1 coverage floor)

V3 says >=0.85 (§4, line 229). Counter from V1/V2/V4/V5: the floor should be >=0.90 or higher.

**Position:** 0.85 is defensible for a `--depth quick` T1 fast pass. But for the default T1 stop (no depth override), 0.90 is the better floor. V3 should adopt 0.90 for the default path and keep 0.85 as the `--depth quick` floor. This matches the majority (V2, V5) while preserving V3's quick-pass economics.

### X-002 (T2 coverage trigger)

V3 says <0.70 (§4, line 227). Counter: V1 uses <0.80, V4 uses coverage_gap_rate > 0.

**Position:** V3's 0.70 trigger is the most permissive — it allows more work to stay at T1. The conservative position is V1's <0.80. However, V3's trigger is paired with additional signals (scope breadth >3 files, >150 lines, >10 requirements) that catch cases where coverage is above 0.70 but scope is large. The combined rubric is safer than a single coverage threshold. V3's position is defensible as-is, but should document why 0.70 + multi-signal is equivalent to 0.80 single-signal.

### X-003 (convergence PASS)

V3 says 0.65 (§5, Wave 3 step 3, line 282). Counter: V1/V2 say 0.75, V5 says 0.65 PASS / 0.50 PARTIAL.

**Position:** 0.65 is the lowest PASS threshold. V3 and V5 agree. The concern is that a convergence of 0.65 means 35% of the adversarial output is unresolved — that is a high unresolved fraction for a "PASS" label. V3 should adopt a two-tier approach: >=0.75 = PASS (matching V1/V2), 0.65-0.74 = PARTIAL (currently V3 treats both as PASS), <0.65 = unresolved_conflict (V3's current position). This aligns with the majority without losing V3's tolerance for partial resolution.

### X-005 (think_about_* status)

V3 says eliminated entirely (§6, lines 353-356). Counter from V1/V2: current but not load-bearing. Counter from V4/V5: current and mandatory.

**Position:** V3 is the strictest here and I maintain this is correct for v1. The research (enrichment/research-deep.md) says the tools are "current but under-leveraged." None of the variants provides empirical evidence that wiring them improves any measurable outcome. V1/V4/V5 add them because "they are cheap" (~200 tokens each), but cheap != valuable — they consume audit-log space, add protocol complexity, and create a dependency on a tool surface that may change. V3's elimination is the correct default: add them back only if eval shows a measurable improvement. The merged output should adopt V3's position with a note that V1/V4/V5's scripted-nudge approach can be restored if eval evidence supports it.

### X-004 (T1 max-files for stop)

V3 says <=3 files (§4, line 229). Counter: V1/V2 say <=5, V5 says <5 = 0pts.

**Position:** V3's <=3 is the most restrictive T1 stop condition, which means more work escalates to T2. This is conservative in the right direction — the cost of a false-negative T1 stop (missing a deviation in a 4-file change) exceeds the cost of a false-positive T2 escalation (spending T2 tokens on a clean 4-file change). V3 should adopt <=5 for the default path (matching the majority) but keep <=3 as the `--depth quick` maximum.

### X-009 (deviation taxonomy category count)

V3 says 4 categories (Wave 1 step 5, lines 202-209). Counter: V4 adds `unknown` as a 5th.

**Position:** 4 categories with a conservative default-to-Drift rule (V3) is superior to 5 categories with an `unknown` escape hatch (V4). The `unknown` category reduces classification precision and produces less actionable reports. V3 should adopt V2's precedence rule but keep the 4-category taxonomy.

### X-012 (T2 reviewer agent set)

V3 uses confidence-calibrator + root-cause-analyst + optional quality-engineer (§5, Wave 3, lines 244-258). Counter: V1/V2/V5 use rf-qa + rf-qa-qualitative + root-cause-analyst. V4 uses a 5-role topology.

**Position:** V3's reviewer set is the leanest, using agents that already have proven track records in sc-troubleshoot. The rf-qa + rf-qa-qualitative pair used by V1/V2/V5 is designed for QA review of diffs, which is appropriate for UC-2 but less natural for UC-1 pre-execution validation. V3's confidence-calibrator as the primary reviewer for re-grading the coverage map is a defensible choice for v1 — it uses an agent whose calibration behavior is well-understood. The merged output should allow both sets based on mode (UC-1: confidence-calibrator + quality-engineer; UC-2: rf-qa + root-cause-analyst), which V3 partially supports with its mode-aware agent selection.

### Kill List (V3-specific)

V3 §13 (lines 518-544) explicitly excludes 5 features. No other variant has this section.

**Position:** The Kill List is a feature, not a deficiency. It prevents scope creep during implementation and provides clear escalation criteria. The merged output should adopt V3's Kill List as a dedicated section and add V1's §7.2 note about the four rejected candidate agents (coverage-mapper, deviation-classifier, tasklist-vs-diff-comparator, reflection-synthesizer) as additional kill-list items with justification.

### X-007 (wave count)

V3 has 6 waves. V1/V4 have 9. V2/V5 have 7.

**Position:** 6 is the right number for v1. V1's 9-wave architecture separates evidence validation (Wave 6) and synthesis (Wave 7) into distinct waves, but the evidence-validator output feeds directly into the synthesis step — there is no reason to interleave another wave boundary between them. V3 embeds evidence validation as step 3 of Wave 4 (Synthesis), which is the correct granularity: it is a sub-step of report finalization, not a distinct protocol phase. The merged output should adopt V3's 6-wave frame.

### X-010 (classification precedence explicit or not)

V3 defaults to Drift. V2 defines Regression > Drift > Necessary > Authorized explicitly (§10.5). V4 uses `unknown` to escape. V1/V5 do not define precedence.

**Position:** V3 should adopt V2's explicit precedence rule. V3's default-to-Drift is the correct fallback when signals are ambiguous, but it is not sufficient when multiple signals coexist with different strengths. The merged output should have V2's precedence as the primary rule and V3's default-to-Drift as the fallback when no signals match.

### X-011 (eval dimension count)

V3 has 5 dimensions. V1 has 6. V4 has 7. V2/V5 have 5.

**Position:** 5 dimensions is the majority position (V2, V3, V5 all agree). V1's 6th dimension (Tier-decision correctness) and V4's 7th (Artifact contract compliance) test protocol mechanics rather than reflection quality. These should be unit tests, not eval dimensions. V3's 5 dimensions are sufficient for v1.

### X-013 (build path)

V3 says skill-creator first → Sprint CLI for production. V1/V2/V5 say hybrid. V4 says skill-creator iterative first → Sprint CLI after stabilizes.

**Position:** All variants converge on the same practical answer: skill-creator for draft/eval iteration, Sprint CLI for production execution. The "hybrid" label in V1/V2/V5 and the "sequential" label in V3/V4 describe the same thing. This is a non-contradiction disguised as a disagreement by terminology. V3's phrasing is clearest: "Skill-creator first → Sprint CLI for production."

### X-014 (Serena memory key naming)

V3 uses `reflection-last-pass-{project-slug}` (dash-separated, no path hierarchy). V1 uses `reflect/last-pass-{slug}` (slash-separated hierarchy). V4 uses `reflection/last-pass/<project-slug>` (slash-separated with path). V5 uses `reflection/<project-slug>/last-pass` (project-first hierarchy).

**Position:** This is a cosmetic disagreement with no functional impact. Serena memory keys are opaque strings. V3's flat key `reflection-last-pass-{project-slug}` is marginally simpler to search (single `list_memories` call with prefix match) than hierarchical keys that require path-component parsing. V3's convention is defensible but the merged output should adopt whatever convention the existing Serena memory keys use in sc-troubleshoot and sc-brainstorm for consistency.

### X-008 (mode selection "both present")

V3 says diff/commit/output-dir → post; ambiguous → STOP. V1 says input includes both tasklist AND completed-work → post (rule 4). V2 says both present → post (post subsumes pre). V4 says both plan and diff present → post with plan as source-of-truth. V5 says both present → post.

**Position:** V3's "ambiguous → STOP" is the safest default for a v1 protocol because it avoids silently choosing the wrong mode. But "both present" is not ambiguous — it is clearly UC-2 (post-execution), because post-execution review subsumes pre-execution validation: you can validate coverage AND check deviations. V3 should adopt the majority position: "both present → post." This is a concession (see C7 above) that strengthens the merged output.

### C-006 (think_about_* handling) and C-007 (allowed-tools listing)

V3 eliminates entirely. V1/V2: current but not load-bearing, not listed in frontmatter. V4: mandatory checkpoints, listed in frontmatter. V5: mandatory scripted checkpoints, not listed.

**Position:** V3 is correct for v1. The two distinct issues — (a) whether to invoke the tools, and (b) whether to list them in allowed-tools — should both be answered "no." Listing them in allowed-tools (V4 only) creates a dependency. Invoking them as mandatory checkpoints (V1/V4/V5) creates audit noise. The merged output should adopt V3's position and add a design note in SPEC.md explaining that this decision can be revisited if eval evidence supports restoration.

### C-010 (T2 multi-model topology)

V3 uses 2-3 agents with model assignments: calibrator sonnet, root-cause sonnet/opus, optional quality-engineer haiku. V1 uses 2-3 reviewers rotating opus/sonnet/haiku. V2 uses 2 (sonnet+haiku) or 3 (+ cross-vendor). V4 uses 5 roles. V5 uses 2-3 based on available aliases.

**Position:** V3's 3-agent topology is sufficient. V4's 5-role topology (coverage/qualitative/root-cause/code-system/calibrator) is over-engineered for v1 — it spawns more agents than the eval matrix has cases to validate. V3's approach — calibrator handles re-grading, root-cause handles deviation investigation, quality-engineer handles edge cases — covers the three distinct review tasks. The merged output should adopt V3's 3-agent default with V1's model-rotation rules (ensuring heterogeneity).

## Summary Judgment

V3 is the correct skeletal structure for the merged output: 6 waves, minimal refs, lean return contract, eliminated legacy tools, and an explicit kill list. The other variants contribute valuable additions — V1's classification precedence, V2's `[INFERRED]` tagging and zero-drop audit, V4's Testability Map principle, V5's CI integration targets — but these should be grafted onto V3's frame, not the reverse. Starting from V3's minimalism and adding proven-value features is safer than starting from V5's 864-line comprehensiveness and trying to trim.
