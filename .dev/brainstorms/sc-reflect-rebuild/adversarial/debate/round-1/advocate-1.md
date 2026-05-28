# Round 1 — Advocate for Variant 1

## Position Summary

Variant 1 is the strongest base for three reasons:

1. It is the only proposal that fully internalizes the "thin orchestrator + heavy delegation" pattern already proven in the sibling sc-troubleshoot / sc-brainstorm / sc-validate-roadmap surface — a 9-wave architecture with a Tier-Decision Gate as a *fractional* wave (Wave 2.5), an asymmetric-flag-bearing return contract that mirrors sc:troubleshoot's downstream-automation contract verbatim, and a deviation taxonomy lifted straight into the matrix-construction wave.
2. It picks the highest-defensible numeric thresholds (≥0.95 T1 coverage floor, 0.75 convergence PASS) — high enough that T1-only is a real safety guarantee, low enough not to escalate every common case.
3. Its weaknesses (no Ops Integration section, no precedence rule on the deviation taxonomy, no explicit `[INFERRED]` tag) are additive fixes the merge should incorporate, not structural defects in the base.

The merge should pick V1 as the base and bolt on: V2's §11 Hallucination Guardrails (with precedence rule), V4's §16 Testability Map, V5's Wave 0 env-var checks, and the V3 Kill List discipline. Every other variant either weakens the numeric thresholds (V2/V3/V5 lower the T1 floor; V4 makes it impossibly strict) or trades clean orchestrator discipline for ad-hoc surface area (V4's think_about_* in allowed-tools; V5's Ops content inside the SKILL.md).

## Steelmen of Opposing Variants

### Variant 2 (strongest argument)

V2's strongest move is treating the *hallucination contract* as a first-class structural section (§11) rather than scattered policy.

The "Grounded vs `[INFERRED]` binary" with the *zero-drop-as-flag* rule (§11.2 quote: "a pass that drops zero items is suspect") is a genuine epistemic upgrade — it inverts the default failure mode of evidence validation, where a clean result is normally treated as positive evidence rather than as a warning sign.

Combined with the explicit classification precedence rule "Regression > Drift > Necessary > Authorized" (§10.5: "rationale does not authorise contradiction"), V2 produces a deviation taxonomy that is deterministic under multi-signal ambiguity in a way the other four are not.

The argument is: if reflection's defining contribution is *trustworthy* verdicts, then the structural anti-self-confirmation mechanisms are the load-bearing parts, and V2 is the only variant that names them as such. Per V2 §1: "Reflection that confirms its own conclusions is worse than no reflection."

### Variant 3 (strongest argument)

V3's strongest argument is *parsimony as a discipline*.

With only 2 refs (vs V1's 6, V2's 7), a leaner 6-wave architecture, a strict "Kill List" §13 enumerating 5 deliberately-excluded features with rationale, and the lowest absolute file length (569 lines), V3 demonstrates that every load-bearing decision in V1/V2/V4/V5 can be expressed in less surface area.

The Kill List ("New `coverage-mapper` agent... extract only if eval shows Wave 1 inline logic is fragile") is the most honest articulation of YAGNI in the variant set.

V3's argument is: SKILL.md size IS a quality dimension — Claude reads it every session at ~50 tokens for the loader summary but every full activation pays the full cost; a 569-line skill that delegates equivalently is strictly better than a 658-line skill that delegates the same.

### Variant 4 (strongest argument)

V4's strongest move is the **Testability Map** §16: every protocol decision has a concrete eval-assertion mapping ("A protocol step that cannot map to at least one deterministic or qualitative eval assertion should be simplified or removed").

This is methodologically stronger than V1/V2/V3/V5 because it directly closes the gap between protocol-spec and grader.py — V4 commits to 6 new `grader.py` assertion types (vs V1's 3) including a full Python implementation sketch of `citation_resolves` (§11) with fixture-root remapping.

The additive `complexity_score` formula (§8: 0.30 × coverage_gap_rate + 0.25 × evidence_conflict_rate + 0.25 × blast_radius_score + 0.20 × stakes_score) is also more calibrate-able than V1's named-signal table — it produces a single bounded number whose components can each be A/B tested independently.

V4's argument is: "rubric-as-formula" is what makes the rubric falsifiable. A named-signal table cannot be regressed; a weighted formula can.

### Variant 5 (strongest argument)

V5's unique contribution is the **Ops Integration §9** (U-001) — the only variant that wires the skill build into the actual repo tooling.

This includes: `make reflect-eval`, `make reflect-eval-quick`, `make eval-skill SKILL=...`, plus explicit PreToolUse-hook awareness, `make verify-sync` pre-commit compliance, and CI cadence with concrete latency budgets ("`reflect-eval-quick` (3 pilot cases) runs in < 30s. The full `reflect-eval` runs in < 2 min").

It is also the only variant that addresses A-002 partially — the env-var aliases `ANTHROPIC_DEFAULT_OPUS_MODEL` etc. are explicitly checked in Wave 0 step 6 with "degrade gracefully on missing aliases" rather than assumed.

V5's argument is: a protocol that ships without binding to the Makefile, the pre-commit hook, and the CI cadence is half-shipped; the other four variants implicitly assume the operator already knows how to wire it.

## Strengths of Variant 1 (with evidence)

1. **Tier-Gate as fractional Wave 2.5 is the right architectural primitive (S-005)**
   - Evidence: V1 §4 Wave 2.5 sits BETWEEN coverage-matrix construction (Wave 2) and Tier-1 reflection (Wave 3).
   - Why this matters: the gate has all the inputs it needs (`coverage_pct`, `drift_count`, `regression_count`, scope size, multi-domain detection) AND it executes *before* the agent subprocess fires.
   - Escalation decisions are therefore made on real data, not on heuristics-of-input-shape. V3 puts its gate at Wave 2 without a coverage matrix; V4 computes `complexity_score` at Wave 2 but uses heuristics that don't all come from real grounding.
   - The fractional numbering preserves the linear-wave reading order while making it explicit that 2.5 is a *decision*, not a *production* step.

2. **Asymmetric-flag return contract directly mirrors sc-troubleshoot (C-019)**
   - Evidence: V1 §5 stable contract includes `asymmetric_flags: {blocked_by_low_confidence, spec_is_wrong, user_decision_required}`.
   - Why this matters: these three flags are the exact downstream-automation signal that lets `/sc:task`, `/sc:pm`, and CI pipelines short-circuit *without parsing prose*.
   - V2 has `cannot_validate_without_user_input + regression_present + unauthorized_deviation_present` — close but framed as facts, not as routing flags. V3's stable contract has 14 fields and no asymmetric-flag block. V5 has 15 fields and no asymmetric-flag block.
   - The composability section (V1 §5) names the consumers explicitly. This is a higher form of cross-skill discipline than the others demonstrate.

3. **Wave 2 deviation taxonomy is collocated with matrix construction (C-015, X-009)**
   - Evidence: V1 §4 Wave 2 step 4 classifies UC-2 deviations inline in the wave that builds the matrix, with the 4-cell taxonomy fully defined.
   - Why this matters: classification happens *in the same pass* that produces the cell-by-cell coverage data — no separate wave, no agent round-trip.
   - V4 splits this across Wave 3 (synthesis) and Wave 7 (validation), creating a context-handoff that V1 avoids.
   - V5 puts the taxonomy in Wave 3 reviewer instructions, which means T1 cannot classify deviations without escalating.

4. **Reviewer matrix differentiates by mode (C-011)**
   - Evidence: V1 §4 Wave 4 reviewer-selection table: UC-1 → requirements-analyst + system-architect + quality-engineer; UC-2 → rf-qa + rf-qa-qualitative + root-cause-analyst, with explicit N=2 fallback drops named (`drop system-architect`, `drop rf-qa-qualitative`).
   - Why this matters: mode is the strongest signal for which agent persona owns the work.
   - UC-1 is "is this plan good" (requirements + architecture + quality); UC-2 is "did the diff match the contract" (structural QA + content QA + root cause).
   - V3 collapses to "calibrator + root-cause + optional quality-engineer" for both modes; V5 uses identical reviewer composition for both modes.
   - Mode-aware reviewer rotation is a free win on representational diversity.

5. **Citation re-grounding budget policy is explicit (S-010 inline)**
   - Evidence: V1 §4 Wave 6 step 3: "for cards with ≤ 20 citations re-Read all. For cards with > 20 citations, re-Read every HIGH-stakes citation (those tied to `regression` or `drift` rows) plus a random 30% sample of the rest, AND spawn `audit-validator` for a parallel 10% spot-check".
   - Why this matters: this is the only variant that names a *bounded* policy for citation re-validation cost at scale.
   - V2's §11.2 names the zero-drop-flag but doesn't bound the validation cost. V4 doesn't address the cost asymmetry. V5 leaves "non-negotiable" without a sampling rule.
   - Per the sc-troubleshoot Tier 3 audit-validator pattern, this is the canonical way to scale citation validation without unbounded token spend.

6. **Mechanical tier rubric with named numeric thresholds in one place (§4 Wave 2.5 + §6)**
   - Evidence: V1 §4 Wave 2.5 lists 9 rubric signals; §6 restates "Numeric thresholds (canonical): coverage 0.95/0.80, drift 3, regression 1, diff 1000 LOC, confidence 0.85, convergence 0.75/0.60".
   - Why this matters: the rubric is data, not code (V1 §6: "consumed by the orchestrator AND by `confidence-calibrator`").
   - The single canonical-threshold restatement means the calibrator can re-grade against the same numbers the orchestrator routes by.
   - V4 hides the same numbers inside a weighted formula — easier to A/B test individual weights but harder to audit "did the agent route per the rubric?".

7. **Refs loaded on-demand list is explicit and load-time-mapped (S-006, §14)**
   - Evidence: V1 §14 table maps each ref to the wave that loads it (`tier-rubric.md → Wave 2.5 + Wave 3`, `deviation-taxonomy.md → Wave 2 step 4 UC-2 only`).
   - Why this matters: the "do not pre-load" discipline is observable from the SKILL.md alone.
   - V3's 2-ref minimalism is admirable but reflects load-bearing logic crammed inline (Kill List item #1 already concedes "Extract only if eval shows Wave 1 inline logic is fragile" — admitting the inline path may not hold).
   - V4 doesn't enumerate refs as a distinct section. V1 hits the right balance: 6 refs, each with a single load-point.

8. **Wave 5 sc-adversarial integration uses three-tier guard sequence (X-013 + Error Handling Matrix)**
   - Evidence: V1 §4 Wave 5 step 3: "Empty-response guard: empty/unparseable response → FAIL Wave 5 / Partial-parse guard: structured but `convergence_score` missing → fallback 0.5 ONLY IF `merged_output_path` exists on disk / Missing-file guard: `merged_output_path` must exist before status routing".
   - Why this matters: this is the canonical sc-brainstorm-protocol guard pattern lifted verbatim and applied at the right point.
   - V4 §14 collapses this to a single "fail closed to status: partial and use the highest calibrated Tier 2 verdict as fallback" — which silently *replaces* the failure mode with a fallback verdict, hiding the divergence signal from downstream consumers.
   - V1 distinguishes the three failure modes explicitly so the asymmetric_flags block (cf. Strength 2) can route them differently.

9. **T1 always runs even when T2 is planned (§4 Wave 3 preconditions + §15 Will)**
   - Evidence: V1 §15 Will: "Run T1 even when T2 is planned (T1 output feeds T2 reviewers)".
   - Why this matters: T1 produces the matrix and the initial reflection card that T2 reviewers consume — without it, T2 reviewers each independently rebuild the matrix, multiplying token cost by N.
   - V3 §5 Wave 1 "always runs" matches this; V5 §4 Wave 1 also runs always.
   - But V4 §3 architecture has Wave 3 (Tier 1 verdict synthesis) as a wave T2 may skip in §4 Wave 4 ("Tier 2 runs when Wave 2 escalates. Spawn independent reviewers in parallel; do not give them each other's findings.").
   - V1's explicit "T1 output feeds T2 reviewers" is the right design — independence does NOT require starting from zero, only running without coordination.

## Weaknesses of Opposing Variants (with evidence)

### V2: Hallucination Guardrails over-rotates on the `[INFERRED]` binary

- Evidence: V2 §11.1: "There is no third bucket. Findings the reviewer could not tag either way are *dropped* before Wave 5 synthesis."
- Why this is a weakness: the binary forces a false choice.
- Real-world reflection findings include "this looks anomalous but I can't cite a contrary example" — these are valuable hedged observations the user wants surfaced, not dropped.
- The `[INFERRED]` tag is a sensible *third* category (which V2 itself partly admits in §11.6 by surfacing `citations_inferred: N` as a soft warning) but the rule "drop everything that fits neither bucket" is too strict.
- V1's approach (every claim cited file:line; un-cited findings allowed in narrative recommendations) is more honest about the distinction between *load-bearing* citations and *contextualizing* observations.

### V2: Coverage threshold ≥0.90 is too low for T1 stop (X-001 + C-002)

- Evidence: V2 §5.3 rule 1: "C ≥ 0.90 AND S_scope ≤ 5 files AND S_domains == 1 AND S_dev_density ≤ 0.05 → STOP at T1".
- Why this is a weakness: when up to 10% of spec requirements are unmapped AND the protocol calls "STOP at T1", the protocol is *certifying incomplete coverage as good enough for a single-agent verdict*.
- The asymmetric cost (shipping a missed regression) argues for V1's 0.95 floor: a single-agent verdict should only ship when coverage is near-perfect.
- Anything 0.80-0.95 should escalate to T2 *precisely because* a 5-10% gap is exactly where ensemble pressure matters.

### V3: Two-ref minimalism hides load-bearing logic inline (S-006, §13 Kill List item 1)

- Evidence: V3 §13 item 1: "the coverage mapping logic is narrow enough to handle inline in Wave 1; a dedicated agent adds coordination overhead without sufficient complexity reduction. Extract only if eval shows Wave 1 inline logic is fragile."
- Why this is a weakness: V3 simultaneously claims (a) the logic is narrow enough to inline, AND (b) it may need extraction if eval shows fragility.
- This is the exact "we'll know it when we see it" anti-pattern that the refs/ pattern exists to neutralize.
- V1's 6-ref structure pre-commits to externalizing the logic that *would* be fragile (tier-rubric, deviation-taxonomy, coverage-matrix-template) — V3 has to discover fragility through eval failure, then refactor.
- V1's pre-commit is cheaper.

### V3: Coverage threshold ≥0.85 is even lower than V2 (X-001)

- Evidence: V3 §4 row 1: "Coverage completeness (from Wave 1 scan) < 70% of spec items mapped → T2" and §5 Wave 2 stop rule "coverage_pct >= 0.85 AND deviations_found == 0 AND scope ≤ 3 files → STOP at T1".
- Why this is a weakness: same critique as V2 but more severe.
- At 0.85 coverage stop, *15% of spec requirements can be unmapped* and the protocol stops at T1.
- That is not reflection; that is rubber-stamping.

### V4: think_about_* in allowed-tools frontmatter is a structural bet on a deprecated surface (X-005, X-006, C-007, U-010)

- Evidence: V4 frontmatter line 7: lists `mcp__serena__think_about_collected_information`, `mcp__serena__think_about_task_adherence`, `mcp__serena__think_about_whether_you_are_done` as first-class declared tools.
- Why this is a weakness: per the research enrichment (cited in V1 §7 and the diff-analysis), the `think_about_*` triad is *current but under-leveraged* — load-bearing reflection logic should live on the symbolic surface, not on meta-cognition nudges.
- V4 §4 Wave 1.5 makes the checkpoints *mandatory routing gates* ("If it identifies mode/source mismatch, STOP with a corrective usage message").
- This wires the protocol to a tool family that may be deprecated by Serena in a future release without warning, AND makes the protocol's correctness depend on a free-form LLM nudge's interpretation.
- V1's positioning (optional scripted checkpoints, never load-bearing) is the safer default.

### V4: 5-category deviation taxonomy with `unknown` class is an escape valve (X-009, C-015)

- Evidence: V4 §3 UC-2 outputs: "deviation-ledger.yaml: each mismatch classified as authorized expansion, necessary deviation, drift, regression, or unknown."
- Why this is a weakness: the `unknown` class breaks the deterministic precedence that makes the taxonomy useful for downstream automation.
- V2's classification precedence rule "Regression > Drift > Necessary > Authorized" cannot apply when `unknown` is allowed — every ambiguous case becomes `unknown`, which is exactly the rubber-stamp failure mode the taxonomy exists to prevent.
- V1's 4-category structure forces the orchestrator to pick a class (with `drift` as the conservative default on ambiguity, per V3's better default rule which V1 should adopt).

### V5: Ops Integration §9 should be a separate doc, not part of the SKILL.md (S-012)

- Evidence: V5 §9.1-§9.5 add ~50 lines of Makefile target descriptions, file-layout diagrams, PreToolUse hook descriptions, and CI cadence.
- Why this is a weakness: the SKILL.md is the *behavioral protocol* loaded by Claude Code at activation time.
- Operator-facing build instructions (Makefile targets, pre-commit-hook compliance, CI cadence) belong in `.dev/eval-workspaces/sc-reflect/SPEC.md` or in the README — they don't change the skill's runtime behavior.
- V5's §9.5 even names "The pre-commit hook runs `make verify-sync`" — which is operator workflow, not protocol logic.
- V1 omits this entirely, which is the right call for the SKILL.md *as a runtime artifact*. The Ops content from V5 should be merged into SPEC.md, not into the skill body.

### V5: `--strategy enterprise` and +3 multi-domain bonus are speculative magic numbers

- Evidence: V5 §3 override: "Multi-domain span detected... adds +3 to score"; V5 §7 "Reviewer model heterogeneity: Tier 2 reviewers MUST run on different model classes. If only one model alias is available, WARN that T2 is degraded".
- Why this is a weakness: the +3 multi-domain override is a magic number with no calibration evidence.
- V5 doesn't justify why +3 is the right size versus +1 or +5.
- V1's multi-domain rule ("touches frontend + backend, or code + infra → escalate, even on high coverage") is a *binary* escalation with a clearer testability story.

### V5: Memory key convention contradicts the sibling pattern (X-014)

- Evidence: V5 §4 Wave 1.5 step 4: "Memory key convention: `reflection/<project-slug>/last-pass` and `reflection/<project-slug>/deviation-log-<date>`."
- Why this is a weakness: V1's convention (`reflection/last-pass-{project-slug}`) puts the *project-slug suffix* on the key name.
- V5's slash-after-namespace shape (`reflection/<project-slug>/last-pass`) creates an implicit directory hierarchy that Serena's flat-key memory model does not actually support.
- V1's pattern matches `sc-validate-roadmap-protocol`'s convention exactly.
- The wider lesson: V5 invents new conventions where sibling skills already converged on one; the merge should adopt V1's keying.

### V3: Skipping the heterogeneous-model-class discipline at T2 (C-010)

- Evidence: V3 §6 Wave 3 agent table: "confidence-calibrator sonnet, root-cause-analyst sonnet OR opus, quality-engineer haiku".
- Why this is a weakness: V3's table assigns the same model class (`sonnet`) to two of three reviewers, defeating the entire purpose of T2 ensemble pressure.
- V1 §4 Wave 4 model rotation: "rotate across `--models` (default `opus, sonnet, haiku`). For `--depth deep` prefer opus for the first reviewer. The third reviewer (when present) runs on a third model class — explicitly heterogeneous".
- Per Wisdom of Silicon Crowd and HDEE (cited in V2 §1), intra-vendor stacks underperform cross-vendor stacks.
- V3's loose model assignment treats heterogeneity as a soft preference rather than a hard discipline.

### V4: 9-wave count with Wave 7 + Wave 8 splits validation across two waves (S-004, X-007)

- Evidence: V4 §3 architecture: "Wave 6: Final evidence validation + recommendation re-scrutiny / Wave 7: Tier 3 remediation handoff (opt-in only) / Wave 8: Return contract + memory write".
- Why this is a weakness: V4 spreads "validate → report → contract → memory" across Waves 6-8 when these are mechanically one synthesis pass with optional handoff.
- V1 §4 collapses this into Wave 7 (Synthesis + Report + Return Contract) + Wave 8 (T3 Remediation) — same 9-wave count but with sharper boundaries.
- V4's split creates three small waves where one bigger wave reads better and runs in the same time.

## Concessions (genuine weaknesses in Variant 1)

1. **No dedicated Hallucination Guardrails section** — V2 §11 is genuinely better-structured than V1's distributed-across-§4-Wave-6-and-§7 approach. Even if V1's policy is equivalent in effect, a reader scanning V2's table of contents *immediately* finds the anti-hallucination posture; the equivalent V1 reader has to assemble it from three locations. The merge should adopt V2's §11 verbatim and trim V1's distributed mentions to back-references.

2. **No classification precedence rule** — V1 §4 Wave 2 step 4 names the 4-cell taxonomy but does NOT state precedence under multi-signal matches. V2 §10.5 ("Regression > Drift > Necessary > Authorized... rationale does not authorise contradiction") is the right rule. V3's "default to Drift on ambiguity" is the right *fallback* when no signal dominates. The merge should adopt both.

3. **No `[INFERRED]` tag as a structural claim category** — V2 §11.1 surfaces this as a first-class tag with a counter in the report header. V1 has no equivalent. While I argued above that V2's binary is too strict, the *tag itself* is a real upgrade — the merge should adopt the tag and the per-report counter, without V2's "drop unclassifiable" rule.

4. **No Testability Map** — V4 §16 is a genuine methodological contribution. V1 has assertion-DSL extensions in §10 but doesn't map every protocol decision to an assertion. The merge should adopt V4's §16 pattern; it would force V1 to defend or delete any wave step that has no eval coverage.

5. **No explicit env-var alias degradation** — A-002 is partially addressed by V5 only; V1 assumes `ANTHROPIC_DEFAULT_*` is set. The merge should adopt V5's Wave 0 step 6 (check env vars; degrade gracefully on missing aliases).

6. **Wave 2.5 numeric thresholds restated in §6 creates two sources of truth** — Evidence: V1 §4 Wave 2.5 table AND V1 §6 "Numeric thresholds (canonical)" both enumerate the same numbers. Why this is a weakness: if a reader edits one and not the other, they drift. V3's single-table-in-§4 approach is structurally cleaner; the merge should keep V1's rubric in §4 and replace §6 with a back-reference, not a restatement.

7. **Memory key list is duplicated across §7 and Wave 7 step 2** — Evidence: V1 §7 lists 3 memory keys (`reflection/last-pass-{slug}`, `/deviation-patterns/{slug}`, `/false-positives/{slug}`) AND Wave 7 step 2 says "key `reflection/last-pass-{project-slug}` and key `reflection/deviation-patterns/{project-slug}`" — only 2 of the 3. The §7 list says 3 keys; the Wave step uses 2. The merge should align the §7 ref-table with the actual Wave 7 writes.

8. **No dedicated Ops Integration section (S-012)** — V5 §9 is the only variant addressing Makefile targets, PreToolUse-hook compliance, and CI cadence. While I argued the SKILL.md is the wrong host for that content, V1's complete silence on it is a real omission. The merge should either (a) extract V5's §9 into SPEC.md and link, or (b) add a short §17 "Build + Ops" cross-reference in V1 to make the operator workflow discoverable.

9. **No Kill List with explicit YAGNI rationales (S-011, U-014)** — V3 §13 enumerates 5 deliberately-excluded features. V1 §15 "Will / Will Not" enumerates *behaviors*, not features. The distinction matters: a Will-Not list says "we don't do X"; a Kill List says "we considered X and decided against it for these reasons." The latter helps future maintainers avoid re-litigating decisions. The merge should add a Kill List subsection inside V1 §15 covering: coverage-mapper agent, deviation-classifier agent, streaming dialogue, knowledge graph, T1 multi-model, `unknown` deviation class, the +3 multi-domain bonus, the `--strategy enterprise` flag.

10. **No explicit `[INFERRED]` tag** — V2 §11.1 and U-004 surface this as a first-class structural primitive. V1 implicitly treats every claim as Grounded (via evidence-validator re-Read), which means findings that *should* be tagged as inferred are either smuggled in as if grounded or dropped silently. The merge should adopt the tag without V2's "drop unclassifiable" rule.

## Shared Assumption Responses

- **A-001** (400-700 line SKILL.md readable by user): QUALIFY — readable by the operator at *commit-review time* (where length tradeoffs in V1 vs V3 matter), not by Claude at runtime (where the loader summary is ~50 tokens regardless). V1's 658 lines is fine; V5's 864 lines crosses into "compress or split."
- **A-002** (env-var aliases remain set): REJECT — V5 already partially proves this is not safe to assume; the merge must adopt explicit env-var checks with graceful degradation.
- **A-003** (.dev/reflect/ parent dir): ACCEPT — 4/5 variants converge on `.dev/reflect/`; the name reads as "reflection outputs" naturally and matches sibling skills' `.dev/<skill>/` convention.
- **A-004** (60/40 train/test split): QUALIFY — 60/40 is the Anthropic skill-creator default and reasonable for the 12-case iteration-2 matrix, but for the 3-case iteration-1 pilot the split is statistically meaningless; eval-1 should be all-train, eval-2 onward should apply 60/40.
- **A-005** (single-repo / single-project): ACCEPT — the project-slug memory-key convention (V1 §7) already implicitly handles cross-project state without claiming cross-project reflection; multi-repo reflection is out-of-scope for v1 and should be explicit in the Kill List.

## Per-Point Position on Key Contradictions

- **X-001** (T1 coverage floor): V1 says ≥0.95. Counter consideration: V2/V5 ≥0.90 is closer to user-friendly defaults but ships incomplete-coverage verdicts at T1; V4 =1.00 is too strict (no real-world spec maps perfectly to a tasklist). V1's 0.95 is the right floor — high enough that "T1 stop" is a meaningful safety guarantee, not so high that every real-world case escalates.
- **X-002** (T2 coverage trigger): V1 says <0.80. Counter consideration: V2/V5 use composite scores instead of a direct coverage threshold, which is more flexible but less auditable ("which rule fired?" is harder to answer post-hoc). V1's <0.80 is auditable in one number; V3's <0.70 is too permissive (lets 30%-uncovered specs slip to T1).
- **X-003** (convergence PASS threshold): V1 says 0.75. Counter consideration: V3/V5 use 0.65 to match a lower bar for "consensus reached". The right answer depends on what convergence_score *means* in sc-adversarial — if it's a Jaccard-like overlap, 0.65 is "moderate agreement" and 0.75 is "strong agreement". For a reflection skill whose value is *trustworthy* verdicts, the stronger bar wins; 0.75 should be the default with 0.65 available via `--convergence`.
- **X-005** (think_about_* status): V1's position (current-but-non-load-bearing). Counter consideration: V4 declares them load-bearing in `allowed-tools` AND as mandatory checkpoint gates; V3 eliminates them entirely. V1's middle position is the only one that survives a Serena deprecation announcement *without breaking the protocol* — they're optional scripted checkpoints, so losing them downgrades quality but doesn't break behavior.
- **X-009** (deviation taxonomy categories): V1 has 4. Counter consideration: V4's 5th `unknown` class is an escape valve that defeats deterministic classification. V1's 4-cell + a "default to drift on ambiguity" rule (borrowed from V3) is the right shape.
- **X-012** (T2 reviewer agent set UC-2 default): V1 says rf-qa + rf-qa-qualitative + root-cause-analyst, with N=2 dropping rf-qa-qualitative. Counter consideration: V3 collapses to calibrator + root-cause + optional quality-engineer, treating the calibrator as a *reviewer*. That conflates roles — the calibrator's job is to re-grade *other* reviewers' cards, not to produce a first-pass card itself. V1's separation (rf-qa for structure, rf-qa-qualitative for content, root-cause-analyst for deviation investigation; calibrator runs per-card in parallel afterward) is the cleaner role split.
- **X-013** (build path pick): V1 says "Hybrid — skill-creator iter → sprint production." Counter consideration: V3 and V4 frame this sequentially (skill-creator first, *then* sprint), not as a hybrid. The substantive difference is small (both end at sprint CLI for production execution), but V1's "hybrid" framing names the fact that the eval workspace stays under skill-creator's harness *while* the final integration test runs via sprint — they're not strictly sequential. V5 §8.3 expands this into a 3-stage build with hand-author + sync between skill-creator and sprint, which is more honest about the actual workflow than V1's two-stage telescoping. The merge should adopt V5's 3-stage framing under V1's "hybrid" label.
- **X-014** (memory keying with project-slug): V1 uses `reflection/last-pass-{project-slug}` (suffix style). Counter consideration: V5 uses `reflection/<project-slug>/last-pass` (path-style). The suffix style matches sibling skills (`sc-validate-roadmap-protocol`, per V1 §7) and works directly against Serena's flat-key memory model. V5's path-style implies hierarchy that Serena does not natively support. V1 wins this one on the strength of sibling-skill consistency.
- **X-004** (T1 max-files for stop): V1 says ≤5 files. Counter consideration: V3 says ≤3 (too tight — misses common multi-file refactors); V4 doesn't use file count, opting for `blast_radius_score` which folds files into a composite. V1's 5-file ceiling is the right middle ground: tight enough that "narrow scope" is meaningful, loose enough to cover real PRs.
- **X-006** (think_about_* in allowed-tools frontmatter): V1 says No (not listed). Counter consideration: V4 lists all three. V1's exclusion is correct — declaring a tool in `allowed-tools` is a structural commitment that the protocol will *use* it; V1 §7 positions the triad as optional checkpoints that *may* be wired into the T1 agent's brief, which is a runtime decision, not a frontmatter declaration. Listing them in frontmatter as V4 does signals "load-bearing" to readers and future maintainers, contradicting V4's own §6.4-equivalent positioning. V1's restraint is the consistent move.
- **X-007** (number of waves): V1 has 9. Counter consideration: V3 has 6 (leanest), V2/V5 have 7. The wave count is not a quality dimension on its own; what matters is whether each wave does a *distinct* piece of work. V1's Wave 2.5 (Tier Gate) and Wave 6 (Evidence Validation) are genuine extra steps that the 6- and 7-wave variants either fuse into adjacent waves (losing the audit-log "Wave N complete" emit) or skip entirely (V3 has no separate evidence-validation wave; it's a step inside Wave 4). The 9-wave count buys observability.
- **X-008** (mode selection when both inputs present): V1 says "tasklist + completed-work artifact directory → post" (rule 4). Counter consideration: All five variants converge on "both present → post." This is consensus and the merge should adopt it. V1's specific phrasing (artifact dir as the trigger) is slightly more precise than V5's "post subsumes pre" and V4's "plan used as source-of-truth" — V1 names the *evidence* (artifact directory) rather than asserting a precedence.
- **X-010** (classification precedence explicitly defined): V1 says No (not stated). Counter consideration: V2 §10.5 says Yes ("Regression > Drift > Necessary > Authorized"); V3 says "default to Drift on ambiguity." This is a concession I already named — V2's precedence rule should be lifted into V1's Wave 2 step 4. The merge cost is one paragraph.
- **X-011** (eval rubric dimension count): V1 has 6. Counter consideration: V2/V3/V5 have 5; V4 has 7. V1's 6 hits the sweet spot — it adds "tier-decision correctness" (which V2/V3/V5 omit, leaving the rubric blind to whether the protocol routed correctly) without V4's overflow into "artifact contract compliance" (which is structurally tested by deterministic assertions, not by qualitative grading). V1's 6 dimensions map cleanly to 6 distinct failure modes.

## Closing Statement

Variant 1's strength is consistency with the proven sibling-skill pattern, not novelty. It does not invent new conventions where existing ones converge (memory keying, refs/ layout, fail-open policy, three-tier sc-adversarial guard sequence). It commits to the strictest defensible numeric thresholds (0.95 / 0.75) where laxer numbers would let single-agent verdicts ship on too-narrow grounding. It treats the asymmetric_flags block as a first-class downstream-routing contract rather than as decorative metadata.

The merge should take V1 as the base and lift the following additions:

- V2 §11 verbatim (Hallucination Guardrails + classification precedence rule + `[INFERRED]` tag without the drop-rule).
- V4 §16 (Testability Map) verbatim.
- V5 Wave 0 step 6 (env-var checks) verbatim.
- V3's Kill List discipline added to V1 §15.

Every other variant either weakens load-bearing structure (V2/V3/V5 coverage thresholds, V4 think_about_* declaration, V4 `unknown` deviation class) or adds ad-hoc surface area where V1's existing pattern already covers the case.
