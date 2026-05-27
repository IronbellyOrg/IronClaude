# Round 1 — Advocate for Variant 2

## Position Summary

Variant 2 is the only proposal that treats reflection as a *hallucination-control*
problem first and a *workflow* problem second. It ships a dedicated
Hallucination Guardrails section (§11) with five enumerated structural
guards, an explicit `Grounded` / `[INFERRED]` binary on every claim, a
precedence rule for the deviation taxonomy (Regression > Drift > Necessary
> Authorized, §10.5), and a zero-drop evidence-validator pass treated as
an *audit flag* rather than a green light.

These are the load-bearing mechanisms that distinguish a reflection skill
from a generic verification skill — and V2 is the only variant where they
are first-class architectural elements, not byproducts of other waves. The
other four variants distribute these mechanisms across Serena, Wave 5, and
Boundaries sections, which means a future edit can silently weaken them
without anyone noticing.

## Steelmen of Opposing Variants

### Variant 1 (strongest argument)

V1's strongest move is the **inline embedding of the tier rubric inside
Wave Architecture as Wave 2.5** (V1 §4 "Wave 2.5 — Tier Decision Gate"),
combined with a 9-row signal table and *retroactive escalation* on
calibrated confidence <0.85.

The retro-escalation rule is in V1 §4 Wave 3 step 4: "If calibrated
confidence < 0.85 AND `tier_planned == 1` AND `--no-escalate` not set →
upgrade `tier_planned` to 2; record `retro_escalation: confidence_below_floor`."
This is genuinely better than V2's purely-forward rubric in one specific
case: when a T1 card looks scope-safe on paper (scope ≤ 5, density ≤ 0.05)
but the reviewer self-reports low confidence after the actual evidence pass,
V1 can salvage with a retro-upgrade where V2 would ship a low-confidence
T1 verdict.

V1's `asymmetric_flags` sub-block in the return contract (V1 §5
"asymmetric_flags: blocked_by_low_confidence, spec_is_wrong,
user_decision_required") is also a real downstream-automation feature V2
doesn't match — those flags let `/sc:task` and `/sc:pm` short-circuit
without parsing prose. The `spec_is_wrong` flag is particularly valuable:
it surfaces the "the code is right, the spec doesn't match reality" case
that V2 §10 conflates with "necessary deviation."

V1 also has the largest cross-skill integration table (V1 §8 with 14 rows)
which makes the orchestration boundaries the most explicit of any variant.

### Variant 3 (strongest argument)

V3's strongest move is **radical minimalism backed by a dedicated Kill List**
(V3 §13 with 5 enumerated exclusions and justifications: coverage-mapper
agent, deviation-classifier agent, streaming dialogue, knowledge graph,
T1 multi-model).

The Kill List is not just shorter — it is *defensive against scope creep*
in a way V2 isn't, because every "we deliberately did NOT build this"
entry has a paragraph of rationale that future contributors have to refute
before re-adding the feature. V3 §13 row 5 is exemplary: "Multi-model
fan-out in T1 — T1 is intentionally single-agent and cheap. Heterogeneous
multi-model review is a T2/T3 feature. Running parallel models at T1 would
violate the 'quick first' contract that makes sc:troubleshoot's T1
effective."

V3 also has the leanest refs footprint (2 refs total: `coverage-map-template.md`,
`report-template.md` per V3 §14) and the strongest single sentence on why:
"every piece of logic that could be inline IS inline; only structural
templates that would bloat the SKILL.md are externalized" (V3 §14). That
discipline directly addresses the SKILL.md size band that all variants
reference but only V3 enforces by construction.

V3's tier rubric (V3 §4) is also genuinely simpler — 4 signals, not V2's
5 dimensions × 4 structural signals. For a v1 release where eval data is
scarce, a simpler rubric is easier to validate.

### Variant 4 (strongest argument)

V4's strongest move is the **Testability Map (§16) requiring every protocol
decision to map to a deterministic or qualitative eval assertion**.

V4 §16 is explicit: "A protocol step that cannot map to at least one
deterministic or qualitative eval assertion should be simplified or
removed." This is a structural forcing function V2 does not have — V2's
eval rubric in §12 lists dimensions and thresholds, but it does not
require *every section of the SKILL.md* to be assertable.

V4's §11 also gives a concrete Python implementation sketch of
`citation_resolves` with fixture-root remapping (V4 §11 lines 451-468),
which is more buildable than V2's §12.3 which only names the new assertion
types.

V4 is also the only variant that surfaces an iteration-3 "held-out
hardening" pass with *seeded traps* (V4 §9.4: "12-15 cases with seeded
false citations, authorized deviation, regression, missing tests, and
recommendation-scrutiny traps"). That is exactly the kind of eval design
that catches the hallucination V2 is trying to prevent — and V4 builds
the harness to test it where V2 only specifies the policy.

V4's 7-dimension eval rubric (vs V2's 5) adds Tier-routing correctness
and Artifact contract compliance as first-class dimensions. Tier-routing
is mechanically the most testable property of the whole skill; making it
a graded dimension is the right call.

### Variant 5 (strongest argument)

V5's strongest move is the **dedicated Ops Integration section (§9)
covering Makefile targets, PreToolUse hook awareness, sync-dev/verify-sync
compliance, and CI cadence**.

V5 §9.1 proposes `make reflect-eval`, `make reflect-eval-quick`,
`make eval-skill SKILL=...` as new and reused targets. V5 §9.3 explicitly
names the PreToolUse hook redirect to `.dev/eval-workspaces/<skill-name>/`.
V5 §9.4 enumerates the 6-step build workflow including "Stage ONLY `src/`
and `.dev/` paths. NEVER stage `.claude/` paths."

No other variant ties the skill build to the repo's mechanical gates with
this concreteness. V5 §9.5 also commits to a specific CI runtime budget
("`reflect-eval-quick` target (3 pilot cases) runs in < 30s. The full
`reflect-eval` runs in < 2 min"), which is the kind of empirical claim
that disciplines design choices V2 leaves abstract.

The env-var awareness in V5 §4 Wave 0 step 6 ("Validate model aliases:
check env vars `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`,
`ANTHROPIC_DEFAULT_HAIKU_MODEL` are set. If missing, WARN and degrade
gracefully") is also a real gap V2 silently inherits — V2 §7.1's reviewer
composition assumes the aliases resolve, never checks.

V5's tier-decision composite-score formula (V5 §8 with 4 weighted scores
summing to ≤1.0 + bonus cap) is also a single mathematical signal that is
easier to log and replay than V2's 8-row priority-rule decision table.

## Strengths of Variant 2 (with evidence)

**S2-1. Dedicated Hallucination Guardrails section with 5 enumerated
structural guards (U-002 unique to V2).**

V2 §11 enumerates: §11.1 Grounded vs `[INFERRED]` binary; §11.2
evidence-validator as final gate with zero-drop-flag; §11.3 blind
calibration anti-anchoring; §11.4 heterogeneous reviewer ensemble; §11.5
citation re-Read window; §11.6 inferred-claim audit threshold.

Per diff-analysis §5 row U-002, **V2 is the only variant** that exposes
these guards as a first-class architectural element with a numbered
subsection per guard. V1, V3, V4, V5 all distribute these mechanisms
across Serena, Wave 5, and Boundaries sections — making them harder to
audit and easier to silently weaken in future edits.

This matters specifically because the *failure mode* of a reflection
skill is not that any one guard breaks, but that several weaken together
in subsequent revisions. Having all five in one section means a reviewer
on a future PR sees them collectively and notices when one drops out.

**S2-2. Zero-drop evidence-validator pass is an audit FLAG, not a clean
signal (U-005 unique to V2).**

V2 §11.2 states: "0 dropped → `status: success`, but **audit-log a
`zero-drop-flag: true` marker** so meta-eval can spot-check."

This single decision flips the failure mode of evidence validation: every
other variant treats zero drops as the happy path. Per diff-analysis U-005,
**V2 alone** internalizes the citation directly: "a pass that drops zero
items is suspect" — quoting the actual `evidence-validator.md:21`
contract. This is the load-bearing anti-confirmation mechanism for the
whole skill: when a reflection report ships with no dropped citations,
the *real* signal is "either the work is unusually clean OR the validator
is rubber-stamping." V2's audit flag forces meta-eval to distinguish the
two; the other variants conflate them.

**S2-3. `[INFERRED]` as a first-class claim category with binary contract
(U-004 unique to V2).**

V2 §11.1: "Every claim in the report carries one of two tags: **Grounded**
... or **`[INFERRED]`** ... There is no third bucket. Findings the
reviewer could not tag either way are *dropped* before Wave 5 synthesis."

Per diff-analysis U-004, this binary is unique to V2. V1 and V3 talk
about "grounded citations" but allow ungrounded claims to remain as
prose; V4 has citation-resolves as an assertion but no claim-tagging
contract; V5 treats unverified claims as a side effect of evidence
validation (V5 §1: "marked `unverified`; they are never silently promoted
to verdict facts") but does not enforce the binary at synthesis time.

The V2 binary forces every reviewer to choose-or-drop, eliminating the
prose-confidence smuggling problem where speculative language ("this
appears to be...", "the implementation may not...") survives evidence
validation because it doesn't cite a file:line.

**S2-4. Classification precedence rule for the deviation taxonomy (U-003
unique to V2).**

V2 §10.5: "Regression > Drift > Necessary > Authorized. A diff hunk that
contradicts a spec criterion but has an inline TODO rationale is still a
**Regression** — rationale does not authorise contradiction."

Per diff-analysis U-003 and X-010, **only V2 and V3** state an explicit
precedence rule, and V2's is stricter. V3 §1.5 only specifies "Default to
Drift on ambiguity"; V4 escapes via a 5th `unknown` class (X-009); V1 and
V5 leave multi-signal classification undefined.

The asymmetric cost of misclassification is the reason precedence
matters: misclassifying a Regression as a Necessary deviation lets a
spec-violation ship; misclassifying a Necessary deviation as a Regression
generates a noisy false-positive that wastes a remediation cycle. The
correct posture is conservative — over-flag Regression — and V2's
precedence rule encodes that posture deterministically.

**S2-5. Inferred-claim audit threshold as a soft signal (U-006 unique to
V2).**

V2 §11.6: "A reviewer that produces a report with `citations_total > 20`
AND `citations_inferred > citations_total / 2` triggers an automatic WARN
in chat: 'Reflection is more inference than evidence.'"

Per diff-analysis U-006, this is a unique meta-gate that catches *reports
that ship clean but are mostly speculation*. The other variants' eval
rubrics catch low citation accuracy after the fact (during grading); V2's
audit threshold catches it at synthesis time, before the report reaches
the user. The threshold (>50% inferred for reports with >20 citations) is
empirically calibrated to "the report is more speculation than evidence"
rather than to a fixed cap.

**S2-6. Reviewer-composition rules tie model-class rotation to research
citations (V2 §7.1).** V2 §7.1 names the underlying papers in-line ("per
Topic 2 research, Wisdom of Silicon Crowd, LLM-TOPLA") and pins judge
selection to Khan et al. ICML 2024 Oral. V5 talks about heterogeneity but
doesn't enumerate the rotation; V1's matrix in §4 Wave 4 is the closest
comparable but doesn't cite the supporting research at the composition
table. V2's tighter coupling between mechanism and citation makes the
design defensible against future "let's just use 3x sonnet" edits.

**S2-7. Per-card blind calibration at Tier 2 with parallel calibrator
instances (V2 §6.4 + §11.3).** V2 §11.3 explicitly says
"sc-adversarial-protocol's debate is weighted by calibrated confidence,
not self-reported." V1 does parallel calibration too (V1 §4 Wave 4 step
4) but does not wire calibrated scores into the merge weighting; V3 §3
step 2 calibrates independently but does not feed the merge. V2 ties the
calibration directly to the merge math.

## Weaknesses of Opposing Variants (with evidence)

### V1 weaknesses

**W-V1-1. Wave 2.5 fractional numbering breaks linear audit trace
(diff-analysis S-005).** V1's "Wave 2.5" embedded between Wave 2 and Wave
3 makes `wave_durations_ms.wave_2_5` a string key that breaks naive
integer comparisons across waves. V2's linear Wave 0-6 numbering is
mechanically cleaner. V4 and V5 inherit the same weakness; V2 and V3 do
not.

**W-V1-2. V1 §4 Wave 2.5 sets the T1 coverage floor at `coverage_pct ≥
0.95`.** Per diff X-001, V1 alone uses 0.95 while V2/V5 use 0.90 and V3
uses 0.85. In practice, 0.95 turns T1 from a "fast path" into a "rare
path" because real specs almost always have ≥1 partially-covered item
that legitimately doesn't need T2. The 0.95 floor pushes work into T2
unnecessarily, exactly the cost V2 §5.4 explicitly justifies avoiding.

### V3 weaknesses

**W-V3-1. V3's 4-signal tier rubric drops blast-radius and multi-domain
signals (V3 §4).** V3's table covers `coverage_pct`, `scope breadth`,
`spec complexity`, `--depth deep` — but no explicit multi-domain trigger.
V2 §5.3 rule 4 ("`S_domains ≥ 3` → ESCALATE") catches the exact failure
mode V3 misses: a 3-file diff that touches code+infra+docs *looks* small
but spans representational frames a single reviewer cannot adjudicate.
V1 §4 Wave 2.5 has a multi-domain row too; V3 alone misses this.

**W-V3-2. V3 §6 declares think_about_* "Zero references" and eliminates
them entirely.** Per diff X-005, this contradicts the Topic 1 research
finding (referenced by V2 §6 and V1 §7) that the tools are CURRENT (not
deprecated). V3's elimination throws away the cheap 200-token
scripted-nudge benefit that V2 §6.4 captures by wiring them as
audit-logged checkpoints — trading a real (small) value for definitional
purity.

### V4 weaknesses

**W-V4-1. V4 lists `mcp__serena__think_about_*` tools in `allowed-tools`
frontmatter (V4 line 7, diff-analysis X-006).** V4 is the only variant
that does this. Frontmatter `allowed-tools` is the *permission surface*,
not the usage commitment — listing think_about_* there elevates them from
"scripted nudge" (V2's stance, §6.4) to "load-bearing surface the user
expects." If a future edit removes them from allowed-tools, V4's protocol
breaks silently; V2's does not, because V2 treats them as nudges layered
on top of an evidence chain that uses none of the three tools.

**W-V4-2. V4 introduces a 5th `unknown` deviation class (diff-analysis
X-009).** This escape hatch defeats the point of having a taxonomy:
reviewers will route ambiguous cases to `unknown` rather than reasoning
through precedence (V2 §10.5 forces them to decide). The asymmetric cost
of misclassified-as-Drift vs misclassified-as-Regression vs
misclassified-as-Unknown is dramatically different; only V2's precedence
rule + 4-class set forces the reviewer to face the cost.

### V5 weaknesses

**W-V5-1. V5 §4 Wave 5 sets adversarial convergence PASS at 0.65**
(diff-analysis X-003), 10 points below sc-adversarial's 0.75 default. V2
§5.4 + §6 pin to 0.75 because that is the documented default — using 0.65
makes V5's merges look passing that sc-adversarial itself would consider
partial. The caller (sc:reflect) should not silently override the called
skill's threshold; if 0.65 is right for reflect, the fix is to argue it
in sc-adversarial's docs, not override at the caller.

**W-V5-2. V5's 864-line SKILL.md is the largest variant by ~30%**
(diff-analysis S-002: V5=864 vs V1=658 vs V2=650 vs V4=586 vs V3=569). The
Ops Integration content is genuinely valuable (U-001) but wiring it into
SKILL.md violates the lazy-loading discipline V2 §16 enforces. Makefile
targets and PreToolUse hook awareness should live in a ref, not the
every-session-loaded SKILL.md body.

## Concessions (genuine V2 weaknesses)

**C-1. V2 has no retroactive escalation rule comparable to V1's
`confidence-below-floor → upgrade tier_planned to 2`.** V1 §4 Wave 3 step
4 catches the case where T1 starts looking safe but calibration drops the
score; V2 §5.3 only escalates forward at Wave 2. This is a genuine V1
advantage worth absorbing.

**C-2. V2's return contract has no `asymmetric_flags` sub-block matching
V1's surface.** V1 §5 surfaces `blocked_by_low_confidence`, `spec_is_wrong`,
`user_decision_required` as explicit booleans for downstream automation.
V2 §9.1 has `cannot_validate_without_user_input`, `regression_present`,
`unauthorized_deviation_present` (which are similar in spirit) but does
NOT have `spec_is_wrong` — the "the code is right, the spec is wrong"
signal V1 surfaces. This is the most actionable single missing field for
/sc:task and /sc:pm composability.

**C-3. V2 has no Ops Integration section (Makefile + CI cadence + hook
awareness).** V5 §9 is genuinely valuable and V2 §13 only references
CLAUDE.md plugin override without enumerating the mechanical gates. If
the round-2 merge keeps V2's structural guards, it should absorb V5's
Ops Integration as a new section or appendix — ideally pushed to a ref
to preserve V2's lazy-load discipline.

**C-4. V2 has no Testability Map.** V4 §16 forces every protocol decision
to map to an assertion. V2 §12 lists eval dimensions but does not enforce
per-decision mapping. A future V2 revision should add a §17 Testability
Map per V4's pattern — it's an additive change that does not contradict
V2's other structural choices.

**C-5. V2 does not validate ANTHROPIC_DEFAULT_* env-var aliases in Wave 0.**
V5 §4 Wave 0 step 6 catches missing aliases and degrades gracefully. V2
assumes the aliases resolve when Wave 3A composes the reviewer model
rotation. Round-2 should absorb V5's env-var check.

## Shared Assumption Responses

- **A-001 (user reads 400-700 line SKILL.md)**: QUALIFY — V2 §16
  explicitly addresses this by lazy-loading refs ("Refs loaded by the
  wave that needs them; never pre-loaded. Session-start footprint:
  SKILL.md only ~50 tokens via Claude Code skill loader"). The 650-line
  SKILL.md is loaded *by the skill runner*, not by the user — the user
  reads chat output. The assumption mis-states the failure mode: the
  cost is per-session token weight, which V2 minimizes via deferred ref
  loading. The user-facing surface is the REPORT.md template (V2 §10.6)
  and the chat summary.

- **A-002 (ANTHROPIC_DEFAULT_* env vars remain set)**: ACCEPT as a
  genuine gap for V2 specifically. V5 §4 Wave 0 step 6 is the right
  pattern: validate env vars in Wave 0, degrade gracefully if missing,
  never abort. V2 should absorb this in the round-2 merge. Concrete fix:
  add a Wave 0 step that checks the three aliases and, if any are
  missing, drops the reviewer count or reroutes the persona table per
  the available models.

- **A-003 (`.dev/reflect/` parent path is right)**: QUALIFY — V2 §3.1
  uses `.dev/reflect/<mode>-<slug>-<YYYYMMDDHHMMSS>/` per the existing
  `.dev/` convention documented in CLAUDE.md and project README. The
  bikeshed between `.dev/reflect/` vs `.dev/reflections/` vs
  `.dev/sc-reflect/` is below the threshold worth debating; the
  load-bearing rule is "not under `.claude/`" (CLAUDE.md ABSOLUTE RULE),
  which V2 §3.3 + §14 enforce.

- **A-004 (60/40 train/test split fits reflect's eval domain)**:
  QUALIFY — V2 §12.2 uses 60/40 per skill-creator default and per
  sc-brainstorm precedent. The right justification (which V2 should
  add) is: reflect's eval matrix is small at v1 (3 pilot → 9-12
  expansion); 60/40 is a defensible default for small-N, and the
  alternative (80/20) leaves too few held-out cases for variance
  estimation. The assumption is acceptable but should be made explicit
  in §12.

- **A-005 (single-repo/single-project scope)**: ACCEPT as a v1 scope
  boundary. Multi-repo reflection is a genuine future feature but its
  requirements (cross-project memory keying, repo identity
  disambiguation, fork-vs-upstream awareness) are large enough to be a
  separate v2 design. V2 §6.3 keys memory by `pwd` basename which is
  single-project; absorbing multi-repo would require its own KEY format
  and is out of v1 scope.

## Per-Point Position on Key Contradictions

- **X-001 (T1 coverage floor)**: V2 says ≥0.90 (V2 §5.3 rule 1: "`C ≥
  0.90` AND `S_scope ≤ 5 files` AND `S_domains == 1` AND `S_dev_density
  ≤ 0.05`"). Counter consideration: V1's 0.95 is defensibly stricter for
  high-stakes work but pushes too much into T2 in practice; V3's 0.85 is
  too lenient because it lets a 5/6 coverage map STOP without any
  structural pressure. V2's 0.90 matches CLAUDE.md global rule 3 ("≥90%
  confidence to proceed without alternatives") — the rubric and the
  global rule should agree, which they do only at 0.90. **HOLD at 0.90.**

- **X-003 (convergence PASS)**: V2 says 0.75 (V2 §5.4 + §8 invocation
  example). Counter: V3 and V5 use 0.65, which makes more verdicts PASS
  at the cost of accepting weaker consensus. The argument for 0.75:
  sc-adversarial-protocol itself defaults to 0.75; using a different
  threshold in the caller silently overrides the called skill's
  documented behavior, which violates the V2 §8 boundary
  ("Reflect does NOT re-implement debate"). **HOLD at 0.75.**

- **X-005 (think_about_* status)**: V2's position: CURRENT (not
  deprecated) per Topic 1 research; wired as **mandatory scripted
  nudges** with audit-log capture, NOT load-bearing (V2 §6.4). Counter:
  V3 eliminates them (loses the 200-token nudge benefit); V4 elevates
  them to allowed-tools (over-commits the permission surface); V5 makes
  them "mandatory checkpoint gates" (closer to V2 but doesn't preserve
  the not-load-bearing framing). V2's position is the right middle:
  capture the cheap benefit, never gate on them, audit-log every
  invocation so meta-eval can verify they were called. **HOLD V2's
  position.**

- **X-009 (deviation-taxonomy completeness — V2 owns the 4-cat
  taxonomy)**: V2 §10 specifies all 4 categories with full definitions,
  detection signals, gold-standard references, and default remediation
  per category (diff-analysis C-015 marks V2 as the most complete
  spec). Counter: V4 hedges with a 5th `unknown` class to absorb
  ambiguity. The V2 counter to V4: the 4 classes + the §10.5 precedence
  rule (Regression > Drift > Necessary > Authorized) is exhaustive *if*
  the precedence is enforced. An `unknown` class is an admission that
  the precedence is not being applied. Reviewers always have enough
  signal to choose under V2's precedence rule because the rule resolves
  ambiguity deterministically (contradiction → Regression; no mapping +
  no rationale → Drift; rationale → Necessary; pre-authorized →
  Authorized). **HOLD 4 classes + enforce precedence.**

- **X-012 (T2 reviewer agent set, UC-2 default)**: V2 says rf-qa +
  rf-qa-qualitative + root-cause-analyst (V2 §7 table), with the
  confidence-calibrator pass running per-card in Wave 3C rather than as
  a reviewer. Counter: V3 uses confidence-calibrator AS a reviewer
  (X-012 calls this out: "CALIBRATOR-AS-REVIEWER"); V4 has a 5-role
  topology adding quality-engineer/auggie-reviewer. V2's choice keeps
  calibrator strictly post-card (so calibration is downstream pressure,
  not upstream framing) and keeps the 3-reviewer count tight. V4's
  5-role topology bloats agent coordination cost without changing the
  failure mode being addressed. **HOLD V2's 3-reviewer rf-qa +
  rf-qa-qualitative + root-cause-analyst, calibrator post-card.**
