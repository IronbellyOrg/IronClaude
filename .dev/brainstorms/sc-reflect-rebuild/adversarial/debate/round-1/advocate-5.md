# Round 1 -- Advocate for Variant 5

## Position Summary

Variant 5 is the only variant that treats `sc:reflect` as a production system, not just a protocol document. Its unique Ops Integration section (S-012, U-001) bridges the gap between "well-specified protocol" and "deployable, CI-compatible skill that survives real Makefile runs, pre-commit hooks, and sync-dev drift." The other four variants produce admirable protocol specifications; V5 produces a protocol specification *plus* the operational contract that makes it buildable, testable, and maintainable in this repository's actual toolchain.

V5 also uniquely addresses env-var degraded-mode handling (U-013) -- a runtime failure mode that V1-V4 silently assume away. And V5's composite tier scoring (U-012) produces a deterministic 0-10 integer that is trivially machine-checkable, unlike the 4-9 rule-based branching systems in the other variants.

These strengths come at a cost: 864 lines is 33% above the 650-line upper bound, and the think_about_* retention and missing classification precedence rule are genuine weaknesses that should be conceded to opposing variants.

## Steelmen of Opposing Variants

### Variant 1 -- Elimination of think_about_* Is Architecturally Clean

V1 is the only variant that eliminates the `think_about_*` triad entirely (V1 SS7, line 353-356: "Zero references to deprecated `think_about_*` tools. The rebuild eliminates the legacy surface entirely"). This is architecturally honest: if the modern Serena symbolic surface (`get_symbols_overview`, `find_symbol`, `find_referencing_symbols`) provides the real grounding, then retaining meta-cognition tools as "mandatory scripted checkpoints" (V5 SS5, line 437) is a half-measure that adds audit-log noise without adding audit-log value. V1 replaces every think_about moment with a concrete symbol-anchored evidence chain (V1 SS6.1, lines 183-193, the mandatory 6-step evidence-gathering chain). This is the correct long-term direction: structural evidence over metacognitive self-nudging.

Additionally, V1's return contract is the richest in the field at ~28 fields (C-019), including `asymmetric_flags` with `spec_is_wrong` and `user_decision_required` -- downstream composability signals that no other variant provides at this granularity. V1's 6 eval dimensions (X-011) also include a `Tier-decision correctness` dimension that V2, V3, and V5 all lack.

### Variant 2 -- Hallucination Guardrails Are the Best Anti-Bias Mechanism in the Field

V2's dedicated Hallucination Guardrails section (SS11, U-002 through U-006, lines 435-477) is the strongest anti-bias mechanism across all five variants. The binary Grounded/`[INFERRED]` tag (V2 SS11.1, line 441-446) forces every claim into one of two buckets and *drops* everything that fits neither. This is a classification discipline that transforms the amorphous "unverified claim" problem into a binary audit surface.

The zero-drop flag (V2 SS11.2, line 452: "A pass that drops zero items is suspect") is an insight none of the other variants reach. It encodes the anti-confirmation principle: a reflection that finds zero errors is itself the error.

The classification precedence rule (V2 SS10.5, line 427: "Regression > Drift > Necessary > Authorized") resolves multi-signal ambiguity deterministically -- a gap V1, V3, and V5 all share. V2's contribution here is genuinely novel and should be adopted regardless of which variant wins the merge.

V2 also has the most explicitly documented deviation taxonomy (C-015), with detection signals, gold-standard references, and default remediations for each of the 4 categories -- far richer than V5's inline 4-row table (V5 SS3, lines 299-306).

### Variant 3 -- Leanest Is Deployable Soonest

V3 at 569 lines is the closest to the 450-650 target band (SS2). Its Kill List (V3 SS13, lines 519-544) enumerates 5 deliberately-excluded features with justification -- this is the only variant that treats scope-exclusion as a first-class design decision, not an afterthought. The explicit rejection of coverage-mapper, deviation-classifier, streaming dialogue, knowledge graph, and T1 multi-model shows disciplined scope management.

The 2-ref minimalism (V3 SS14, lines 546-557) reflects a legitimate philosophy: "every piece of logic that could be inline IS inline." V3's ~14-field return contract (C-019) is the leanest and most composable -- downstream consumers need parse only what matters. V3 could ship fastest and iterate from a working baseline, which is the correct engineering instinct for a v1.0.

V3's token cost profile (SS15, lines 560-569) is also the most explicit about wall-clock targets (T1: 1-2 min, T2 no adversarial: 3-5 min), which gives the eval harness concrete latency assertions.

### Variant 4 -- Testability Map Is the Correct Engineering Discipline

V4's Testability Map (SS16, U-007, lines 572-586) is the single best software-engineering contribution across all variants. The principle -- "a protocol step that cannot map to at least one deterministic or qualitative eval assertion should be simplified or removed" (V4 SS16, line 586) -- is a rigor filter that every variant should adopt.

V4's concrete evals JSON skeleton (V4 SS9, lines 311-381) with representative test cases, fixture paths, and assertion shapes is immediately actionable. Five concrete eval cases with `expected_use_case`, `expected_tier`, `expected_verdict`, and typed assertions -- no other variant provides this level of eval-readiness.

V4 also provides the only implementation sketch for `citation_resolves` (V4 SS11, lines 452-468) -- a Python function with fixture-root remapping. This is the most complex new assertion type and V4 is the only variant that makes it implementable today.

V4's iteration-3 "held-out hardening" pass (U-011, V4 SS9.4, lines 304-307) with seeded false citations, authorized deviation, regression, missing tests, and recommendation-scrutiny traps is the most adversarial eval design in the field.

## Strengths of Variant 5 (with evidence)

### S1. Ops Integration Is Uniquely Necessary (U-001, S-012)

V5 SS9 (lines 621-719) is the only section across all five variants that addresses how the built skill interacts with the repository's actual build and CI system. It enumerates:
- 5 existing Makefile targets the skill must pass (`sync-dev`, `verify-sync`, `lint`, `lint-architecture`, `test`) (V5 SS9.1, lines 625-634)
- 3 new proposed targets (`reflect-eval`, `reflect-eval-quick`, `eval-skill SKILL=sc-reflect-protocol`) (V5 SS9.1, lines 636-643)
- File-layout discipline under `src/superclaude/` as source of truth (V5 SS9.2, lines 645-677)
- PreToolUse hook awareness (V5 SS9.3, lines 679-686)
- sync-dev / verify-sync pre-commit hook compliance workflow (V5 SS9.4, lines 688-700)
- CI compatibility with cadence rules (V5 SS9.5, lines 702-718)

No other variant addresses any of these. A protocol that passes adversarial debate but fails `make verify-sync` is undeployable. The diff analysis confirms this gap: S-012 is the only "High" severity structural difference, driven entirely by V5's ops section.

### S2. Env-Var Degraded-Mode Handling (U-013)

V5 SS4 Wave 0 step 6 (lines 148-152) and SS12 (lines 834-837) explicitly handle missing `ANTHROPIC_DEFAULT_OPUS_MODEL` / `SONNET` / `HAIKU` env vars:
> "If missing, WARN and degrade gracefully (T2 uses available models only; do not abort on a missing alias -- heterogeneous duo is better than nothing)."

This is the only variant that treats env-var availability as a runtime condition rather than a silent assumption. The other variants will fail opaquely when aliases are unset -- the protocol will attempt to spawn opus and get an error with no documented fallback.

### S3. CLAUDE.md ABSOLUTE-RULES Defense

V5 explicitly references and enforces four CLAUDE.md absolute rules:
1. Source-of-truth discipline: V5 SS9.2 line 648 ("SOURCE OF TRUTH (edit here)") and the `-f` rule (lines 674-677)
2. Output-path guard: V5 SS9.2 ("never edit directly") and SS12 (line 835)
3. Plugin Override: V5 SS9.2 (line 663, "NEVER .claude/skills/*-workspace/")
4. PR target fork: V5 SS13 (line 861, "source of truth is src/superclaude/")

These are not abstract references -- they are woven into concrete STOP conditions, error-handling rows, and workflow steps. No other variant defends the CLAUDE.md rules this thoroughly. V1 and V3 have output-path guards (V3 SS2, line 84; V1 SS3, line 84) but none document the sync-dev pipeline, the pre-commit hook interaction, or the `-f` git add rule.

### S4. Composite Tier Scoring Is Machine-Checkable (U-012)

V5 SS3 (lines 74-102) uses a 5-signal 0-2-point composite scoring system that produces a deterministic 0-10 integer. Every other variant uses rule-based matching with 4-9 conditions that require branching logic. The composite score is:
- Trivially implementable in a grader assertion (`yaml_field_min composite_score`)
- Auditable in a single telemetry line
- Defensible: every escalation has a numeric score attached, not a rule-number reference

V1's 9-row table (V1 SS5.3, lines 141-151), V2's 8-rule priority logic (V2 SS5.3, lines 141-151), and V4's additive formula (V4 SS8, lines 264-273) are all valid, but V5's approach produces the smallest testing surface. V4's formula is also machine-checkable but uses floating-point arithmetic (`0.30 * coverage_gap_rate + 0.25 * evidence_conflict_rate + ...`), which introduces rounding ambiguity. V5's integer 0-10 score has no rounding ambiguity.

### S5. Comprehensive Error Handling

V5 SS12 (lines 812-837) covers 20+ failure scenarios including three that no other variant addresses:
- Model alias missing (lines 834-835)
- PreToolUse hook blocking a write (line 835)
- `make verify-sync` drift after edit (lines 836-837)

These are not hypothetical -- they are the failure modes this repository's hooks will actually trigger during the build phase.

### S6. Hook-Aware Build Path

V5 SS8 (lines 507-620) explicitly addresses the skill-creator workspace redirect hook as a build constraint, and V5 SS9.3 (lines 679-686) documents the hook's behavior:
> "The `.claude/settings.json` PreToolUse hook rejects writes to `.claude/skills/*-workspace/**` with a redirect to `.dev/eval-workspaces/<skill-name>/`."

This is operational knowledge that the other variants omit, leaving the implementor to discover the hook failure at build time.

### S7. Fail-Open on MCP With Degraded-Quality Tiers

V5 SS4 Wave 1 (lines 175-176) defines explicit fallback tiers: `quality_tier=fallback_1 then fallback_2`. V2 SS6.5 (line 225-227) states fail-open but does not define quality tiers. V3 SS11 (line 476) is similar. V5's tiered degradation gives downstream consumers a signal about how much to trust the reflection output, and the telemetry block (V5 SS10, lines 748-769) surfaces `calibration_method: agent | inline-fallback` so the consumer knows whether the confidence score was independently calibrated or estimated.

## Weaknesses of Opposing Variants (with evidence)

### V1 Weakness: No Ops Integration, No Env-Var Handling

V1 contains zero mention of Makefile targets, sync-dev compliance, PreToolUse hooks, or CI cadence. The 658-line protocol specifies what the skill should do but not how it survives the repository's build pipeline. At build time, V1 will fail `make lint-architecture` (bidirectional command<->skill link check) because the command file and skill file conventions are unspecified. Additionally, V1's model-rotation rules (V1 SS7.1, lines 250-257) assume `ANTHROPIC_DEFAULT_*` env vars are always set. The variant that requires the most heterogeneous model diversity (sonnet + haiku + optional qwen/kimi/deepseek) also makes the most assumptions about alias availability.

### V2 Weakness: Inferred-Claim Audit Is Soft, Not Structural

V2's Hallucination Guardrails section (SS11) is the best in the field, but the inferred-claim audit (V2 SS11.6, line 476) is a soft signal that "the report still ships." This means a report that is >50% inference can still be marked `status: success`. V5 and V3 both have harder gates: V5's evidence-validator drops unfounded items (V5 SS5 step 3, line 393), and V3's inline validation marks `status: partial` on any drop (V3 SS4 step 3, line 321). V2's guardrails are excellent at *detecting* the problem but weaker at *enforcing* a remedy.

### V3 Weakness: No T2 Adversarial Merge Fallback Protocol

V3 delegates to sc-adversarial when competing interpretations exist (V3 SS3 Wave 3 step 3, lines 273-284), but the convergence threshold is 0.65 with no explicit PASS/PARTIAL/FAIL trichotomy. V3 treats convergence <0.65 as `unresolved_conflict` and surfaces both interpretations -- but there is no F1/F2/F3 fallback protocol. If sc-adversarial returns empty, V3 has no documented recovery. V5 SS4 Wave 4 (lines 356-360) provides a three-level fallback (F1 retry with `--depth quick`, F2 highest-calibrated single review, F3 write `reflect-failed.md` with partial state). V3 also uses the fewest reviewer roles (confidence-calibrator + root-cause-analyst + optional quality-engineer) and the only variant that positions the calibrator as a reviewer rather than a post-hoc grader (X-012).

### V4 Weakness: think_about_* in allowed-tools Without Testability Alignment

V4 is the only variant that lists `mcp__serena__think_about_collected_information`, `think_about_task_adherence`, and `think_about_whether_you_are_done` in its `allowed-tools` frontmatter (X-006, V4 frontmatter line 7). This is a declaration that these tools are load-bearing -- but V4's own Testability Map (SS16) does not include an assertion for think_about invocation (the `checkpoint_logged` assertion at V4 SS16 line 579 checks audit.log, not tool invocation). The declaration and the testability commitment are misaligned. V4 also adds a 5th deviation category `unknown` (X-009) without defining its detection signals or default remediation -- this is an escape hatch that undermines the 4-category taxonomy's precision.

## Concessions (genuine V5 weaknesses)

### C1. 864 Lines vs 450-650 Target -- Bloat Is Real

V5 is 864 lines, which is 214 lines above the 650-line upper bound and 414 lines above the 450-line lower bound (SS2). This is not marginally over -- it is 33-93% beyond the target band. The bloat is driven by:
- SS9 (Ops Integration): ~100 lines. This section is genuinely valuable (see S1 above) but could be compressed to ~40 lines by moving Makefile target tables and file-layout diagrams to a ref file.
- SS4 Wave details: ~230 lines. The per-wave step descriptions are more verbose than any other variant's. V3 covers the same waves in ~120 lines. V5's Wave 3 agent persona assignment table (lines 264-269) adds detail that could live in a ref.
- SS12 (Error Handling): ~25 lines. The additional rows (env-var, hook, verify-sync) are necessary but the existing rows overlap with other variants.

**Mitigation**: The 864-line SKILL.md can be reduced to ~620 lines by: (a) extracting SS9 to a `refs/ops-integration.md` ref file (~100 lines saved), (b) compressing per-wave step prose while preserving the exit criteria and tool tables (~80 lines saved), and (c) consolidating the error-handling matrix by removing rows that duplicate the Boundaries section (~15 lines saved). The protocol logic itself does not need to change.

### C2. think_about_* Retention Is the Wrong Call

V5 retains `think_about_*` as "mandatory scripted checkpoints" (V5 SS5, lines 437-442). V1 and V3 eliminate them entirely. The research consensus (Topic 1) is that these tools are "cheap meta-cognition prompts" (V2 SS6.4, line 213) -- they provide ~200 tokens of nudging value but their output is non-deterministic and non-load-bearing. Making them mandatory adds audit-log overhead without measurable quality improvement. V1's approach -- replace every think_about moment with a concrete symbol-anchored operation -- is cleaner and more auditable. This should be conceded to V1/V3.

### C3. No Classification Precedence Rule

V5 does not define classification precedence for the 4-category deviation taxonomy (X-010). V2 SS10.5 defines "Regression > Drift > Necessary > Authorized" with the key insight that "rationale does not authorise contradiction" (V2 SS10.5, line 427). V3 defaults to Drift on ambiguity (V3 SS5 step 5, line 209). V5 has no rule, which means the reviewer's classification is unresolvable when multiple signals match. This is a genuine gap that should be adopted from V2.

### C4. No Dedicated Hallucination Guardrails Section

V5's hallucination contract (SS1, lines 48-52) is a single paragraph stating "Every claim in the final reflection report must cite a real file:line." V2's five-structural-guard approach (SS11, U-002 through U-006) is significantly more rigorous. The `[INFERRED]` tag, the zero-drop flag, and the inferred-claim audit are innovations V5 should adopt.

### C5. Multi-Domain Override (+3) Is Under-Specified

V5 SS3 (line 101) adds +3 to the composite score when multi-domain span is detected, but the domain detection heuristic is not defined. V1's rule 4 (V1 SS5.3, line 147: `S_domains >= 3`) and V2's rule 4 (V2 SS5.3, line 147: `S_domains >= 3`) use a counted `S_domains` signal with explicit domain categories (code, infra, docs, tests, config). V5's +3 override is a blunt instrument that can push a score from 2 (T1) to 5 (T1 with escalation) on a single heuristic. The domain detection should be specified as a countable signal, not an override.

## Shared Assumption Responses

- **A-001** (user capable of reading 400-700 line SKILL.md): **QUALIFY**. The assumption holds for the target audience, but V5 itself violates the 700-line upper bound at 864 lines. A reader who can parse 700 lines may still balk at 864. The mitigation in C1 (compress to ~620 lines) resolves this. If the compression is not performed before merge, V5 should be penalized on this assumption.

- **A-002** (ANTHROPIC_DEFAULT_* env vars remain set): **QUALIFY**. V5 is the only variant that partially addresses this (SS4 Wave 0 step 6, lines 148-152). The degraded-mode handling is explicit: "do not abort on a missing alias -- heterogeneous duo is better than nothing." However, V5 does not specify what happens when *all* aliases are missing (no opus, no sonnet, no haiku). The fallback should be: WARN and run T1-only, since T2 requires heterogeneous models. V5 SS3 agent selection table (lines 256-261) shows "opus only -> 1 agent (degraded)" but does not say "0 aliases -> T1 only." This stronger fallback should be added.

- **A-003** (output dir convention `.dev/reflect/<mode>-<slug>-<timestamp>/`): **QUALIFY**. V5 uses this convention (SS4 Wave 0 step 7, line 154) but contradicts the eval workspace naming by using `sc-reflect-protocol` instead of `sc-reflect` (V5 SS9.2, line 663). The eval workspace name should align with V1-V4's `sc-reflect/` to maintain consistency with the sibling skill pattern (`sc-brainstorm/` uses the skill name, not the skill-plus-protocol suffix).

- **A-004** (60/40 train/test split is right for reflect): **ACCEPT**. The Anthropic default is well-established and no variant provides evidence that reflect's eval domain needs a different split.

- **A-005** (STOP and ask on low confidence / ambiguous input): **ACCEPT**. This aligns with CLAUDE.md global rule 3 and is universally adopted across all five variants.

## Per-Point Position on Key Contradictions

### X-001 (T1 coverage floor): V5 says >= 0.90

V1 requires >= 0.95 (V1 SS4 Wave 2.5, line 182). V3 requires >= 0.85 (V3 SS4, line 229). V4 requires `coverage_gap_rate = 0` (i.e., 1.00) (V4 SS8, line 275).

**V5's position**: 0.90 is the correct floor. Rationale:
- 0.95 (V1) is excessively strict for a single-agent pass. A T1 reflection that maps 94% of requirements and misses one edge case should not be forced to escalate to T2. The 0.90 floor aligns with CLAUDE.md global rule 3 (>= 90% confidence to proceed without alternatives).
- 1.00 (V4) is unrealistic for any non-trivial spec. Coverage gaps from ambiguous spec language or implicit requirements will trigger false escalations constantly.
- 0.85 (V3) is too permissive. A 15% gap in a 20-item spec means 3 unmapped requirements, which is enough to hide a regression.
- **Counter from V1**: 0.95 catches one more edge case per 20 items. Worth the cost for a safety-critical skill.
- **V5 rebuttal**: The 0.90 floor applies *only* to T1 stop. Any T1 reflection below 0.90 escalates to T2, which has no coverage floor (the ensemble debate surfaces gaps). The T2 safety net makes 0.90 sufficient.

### X-003 (convergence PASS): V5 says 0.65

V1 and V2 require 0.75 (V1 SS5, line 279; V2 SS5 step 3, lines 278-280). V3 requires 0.65 (V3 SS3, line 282).

**V5's position**: 0.65 PASS / 0.50 PARTIAL is the correct threshold. Rationale:
- Reflection is reviewing completed work, not generating novel solutions. The adversarial debate is resolving classification disagreements (was this drift or necessary deviation?), not resolving existential disagreements. A 0.65 consensus means two of three reviewers agree on classification -- that is sufficient for a report that will be human-reviewed anyway.
- 0.75 is appropriate for brainstorm (where creative output is being merged) but overly strict for reflection (where the output is a classification + coverage audit). At 0.75, many valid reflections will fall to PARTIAL and produce unnecessary re-runs.
- **Counter from V1/V2**: 0.75 is the sc-adversarial default. Deviating from it requires evidence that reflection's domain is different.
- **V5 rebuttal**: The convergence threshold should match the task, not the tool's default. The sc-adversarial default is calibrated for creative merge; classification merge tolerates lower convergence because the categories are discrete and the fallback (surface both interpretations) is informative rather than destructive.

### X-005 (think_about_*): V5 says CURRENT mandatory scripted checkpoints

V1 and V3 eliminate entirely (V1 SS7, line 353: "Zero references"; V3 SS6, line 354: "Zero references to deprecated"). V2 says CURRENT scripted nudges, NOT load-bearing (V2 SS6.4, lines 213-222). V4 says CURRENT mandatory checkpoint gates (V4 SS5, line 104).

**V5's position**: The tools are current (not deprecated) and provide ~200-token meta-cognition value at defined protocol moments. Making them mandatory ensures they appear in the audit log for post-hoc analysis. They are NOT the load-bearing signal -- evidence-validator is.
- **Counter from V1/V3**: Any checkpoint that is not load-bearing is dead weight. The audit log should record decisions, not nudges. If the tool's output does not gate anything, it should not be in the protocol.
- **V5 rebuttal**: The audit-log value is real. When the evidence-validator drops a citation, the audit log should show whether think_about_collected_information flagged the gap before evidence-validator found it. This is a calibration signal, not a gate. However, I concede (see C2) that V1/V3's approach is cleaner and V5 should defer to the merge on this point.

### X-012 (T2 reviewer agent set): V5's ensemble

V1 uses rf-qa + rf-qa-qualitative + root-cause-analyst. V2 uses rf-qa + rf-qa-qualitative + root-cause-analyst + calibrator. V3 uses confidence-calibrator + root-cause-analyst + optional quality-engineer (calibrator-as-reviewer). V4 uses a 5-role topology: rf-qa + rf-qa-qualitative + root-cause-analyst + quality-engineer/auggie-reviewer + calibrator.

**V5's position**: root-cause-analyst + rf-qa + rf-qa-qualitative + confidence-calibrator (V5 SS7, lines 489-501). The calibrator is a post-hoc grader, not a reviewer. The reviewer roles are analyzer (root-cause depth), qa (coverage + boundary), and refactorer (code health). This 3-role topology with per-role persona assignment (V5 SS3, lines 263-269) is simpler than V4's 5-role topology and avoids V3's anti-pattern of putting the calibrator in the reviewer seat.

### X-002 (T2 coverage trigger): V5 defers to composite score

V1 uses <0.80 (V1 SS4 Wave 2.5, line 183). V2 uses `S_dev_density > 0.20` (V2 SS5.3, line 148). V3 uses <0.70 (V3 SS4, line 232). V4 uses `coverage_gap_rate > 0` (V4 SS8, line 276). V5 uses composite score >= 6 (V5 SS3, line 94).

**V5's position**: Deferring to the composite score rather than a single coverage threshold is more robust. A reflection with 85% coverage but 0 deviations in a single-domain change should not escalate, while a reflection with 90% coverage but a regression in a multi-domain change should. The composite score captures this nuance; a single coverage threshold does not.
- **Counter from V2**: `S_dev_density` is a more targeted signal than a composite because it measures the specific structural ambiguity (ratio of unmapped to total artifacts) rather than mixing scope size with coverage.
- **V5 rebuttal**: V2's density signal is valuable and should be adopted as one of the 5 composite inputs. But using it alone (V2's approach) misses the case where density is low but blast radius is high. The composite captures both.

### X-004 (T1 max-files for stop): V5 says scope_size < 5 = 0 pts

V1 says <= 5 files (V1 SS4 Wave 2.5, line 182). V2 says <= 5 files for strict T1 stop, <= 10 for relaxed T1 (V2 SS5.3, lines 144-145). V3 says <= 3 files (V3 SS4, line 229). V4 does not use file count (V4 SS8, uses blast_radius_score).

**V5's position**: V5 uses a 0-2 point signal (`scope_size`) rather than a hard file-count threshold. <5 files = 0 pts, 5-20 = 1 pt, >20 = 2 pts. This is smoother than V1's hard <=5 cutoff and avoids the cliff edge where 6 files suddenly triggers escalation while 5 files does not. V3's <=3 is too strict (most real diffs touch >= 3 files). V4's approach is reasonable but harder to audit.

### X-007 (wave count): V5 uses 7 waves (Wave 0-6)

V1 uses 9 waves (Wave 0-8). V3 uses 6 waves (Wave 0-5). V4 uses 9 waves (Wave 0-8).

**V5's position**: 7 waves is a reasonable middle ground. V1 and V4 separate evidence validation and synthesis into two waves (Wave 6 + Wave 7), which adds orchestration complexity without clear benefit. V5 combines synthesis + evidence validation in Wave 5 and separates only the optional Tier 3 handoff into Wave 6. V3's 6-wave design is the leanest but folds evidence validation into the synthesis wave (V3 SS4), which means validation and report generation share a token budget.
- **Counter from V3**: Fewer waves = fewer orchestration steps = fewer failure modes.
- **V5 rebuttal**: True for the happy path. But V5's separation of Wave 3 (review) from Wave 4 (merge) from Wave 5 (synthesis) means each wave can fail independently and recover. V3 folds adversarial merge into Wave 3 (V3 SS3), which means a merge failure also loses the review outputs.

### X-009 (deviation taxonomy count): V5 says 4 categories

V1, V2, V3, and V5 use 4 categories. V4 adds a 5th (`unknown`) (V4 SS8, line 149, the deviation-ledger).

**V5's position**: 4 categories is correct. The `unknown` escape hatch (V4) is dangerous because it gives reviewers a path to avoid classification. Every deviation can be placed in one of the 4 categories -- if the evidence is insufficient, the deviation should be flagged as a Grounding Gap, not as "unknown." V2's classification precedence rule (V2 SS10.5) further strengthens the 4-category model by providing deterministic resolution for multi-signal cases.
- **Counter from V4**: Real diffs contain changes that genuinely do not fit the 4 categories (e.g., whitespace-only, auto-formatter output, dependency version bumps).
- **V5 rebuttal**: Those changes are either Authorized expansion (if the tasklist includes "update dependencies"), Necessary deviation (if a formatter ran as a side effect of a build step), or Drift (if they happened silently). None requires `unknown`. The 4 categories are exhaustive by design; the gap is in the evidence, not the taxonomy.

### X-011 (eval dimension count): V5 says 5 dimensions

V1 uses 6 dimensions. V2 uses 5. V3 uses 5. V4 uses 7.

**V5's position**: 5 dimensions is sufficient. V1's 6th dimension ("Tier-decision correctness") is better handled as a deterministic assertion (`yaml_field tier_decision.yaml tier`) than as a qualitative dimension -- tier routing is mechanical, not judgment-based. V4's 7 dimensions include "Artifact contract compliance" which is also deterministic (file_exists + yaml_field assertions). Only genuinely judgment-based dimensions should be qualitative. V5's 5 dimensions (Citation accuracy, Coverage completeness, Deviation-classification precision, Recommendation actionability, Best-practice compliance) cover the judgment surface without mixing in mechanical checks.

### Workspace Path (sc-reflect-protocol vs sc-reflect)

V5 uses `sc-reflect-protocol` for the eval workspace (V5 SS9.2, line 663) and the skill directory name. V1-V4 use `sc-reflect`.

**V5's position**: The eval workspace name should follow the skill directory name, which is `sc-reflect-protocol` (matching the `name:` field in frontmatter). However, the convention in this repository is to use the short skill name for eval workspaces (e.g., `sc-brainstorm/` not `sc-brainstorm-protocol/`).
- **Counter from V1-V4**: Consistency with existing eval workspaces (`sc-brainstorm/`) outweighs consistency with the skill directory name.
- **V5 concession**: V1-V4 are correct. The eval workspace should be `.dev/eval-workspaces/sc-reflect/` to match the existing pattern. The skill directory can remain `sc-reflect-protocol` (matching the `name:` frontmatter convention), but the eval workspace should use the short form.

---

---

## Closing Statement

V5's unique value is operational: it is the only variant that addresses how the protocol survives the repository's build system, hooks, and CI pipeline. This is not a nice-to-have -- it is the difference between a protocol that passes debate and a protocol that ships. The weaknesses are real (864-line bloat, think_about retention, missing classification precedence) and should be conceded to the opposing variants. The path forward is: adopt V5's Ops Integration and env-var handling as mandatory sections, adopt V2's hallucination guardrails and classification precedence, adopt V4's Testability Map and concrete evals skeleton, adopt V3's Kill List scope discipline, and compress the merged result to ~620 lines. The merge should preserve V5's operational layer as a non-negotiable foundation and draw the protocol's anti-bias mechanisms from V2. Every protocol decision in the merged document should survive V4's Testability Map test: if it cannot map to an eval assertion, it should be simplified or removed.
