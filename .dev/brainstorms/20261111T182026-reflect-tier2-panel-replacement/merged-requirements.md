---
title: "Replacing /sc:reflect Tier 2 with the shared review panel: a layered kernel design"
generated: 2026-11-11T19:58:00Z
base: variant-1-opus-architect
checkout_sha: ec259f1b718ccdb9f08bba0237bfa47b2b7601a2
method: adversarial Mode B merge
status: draft-for-owner-review
adversarial_convergence: 0.882
adversarial_status: partial   # score is above the 0.75 threshold, but the invariant gate blocked (5 HIGH unaddressed at Round 2.5, no Round 3 at standard depth); the merge plan resolves all 20, no second probe was run
independent_check: "verification/merged-output-check.md: FAIL on 1 blocking finding (cost contradiction) and 11 minor; all 12 fixed afterwards; the fixes were confirmed by grep only, not by a second independent review"
---

<!-- Provenance: produced by /sc:adversarial (Mode B). Base: Variant 1 (opus:architect). Incorporated from: Variant 2 (sonnet:analyzer), Variant 3 (haiku:backend). Plan: refactor-plan.md (46 changes). Merge date: 2026-11-11. Cross-references of the form "Change N" in the plan text were converted to section names so the document is self-contained; "Change #n" inside these HTML provenance comments refers to the numbered changes of refactor-plan.md (external to this document). -->

# Replacing /sc:reflect Tier 2 with the shared review panel: a layered kernel design

<!-- Source: Variant 2 (sonnet:analyzer), opening paragraph - merged per Change #13; Base (original, modified) - keeps the "(enrichment)" marker -->
Paths are relative to `src/superclaude/` unless they start with `.dev/`. `path:line` cites are lines read in the drafting or verification sessions; "(enrichment)" marks a line taken from the enrichment file; "(plan-verified)" marks a line the refactor plan re-read. PROPOSED = a new name, not an existing file, flag, function or schema. UNVERIFIED = not read. Token figures are estimates unless a source is cited; units are named. Installed primitives are named by installed path (`~/.claude/...`) or the `superclaude` CLI, never by `src/superclaude/...` (CLAUDE.md rule); a `src/superclaude/` or `cli/...` path in this document is a citation of package code that was read, never an instruction for an installed primitive. `<out>` abbreviates the reflect output directory. Ids such as INV-nnn, S-/C-/X-/U-/A-nnn and O-n are labels from this adversarial run's invariant-probe.md and diff-analysis.md (external to this document), except O-n, which are defined in "Open items".

## Summary

<!-- Source: Base (original, modified) - rewritten per Change #40, #6, #18 -->
Chosen architecture: **C, the Layered Review Kernel with reflect adapters and a retained adversarial finalizer.** The kernel generalizes panel resolution, dispatch adapters, findings-v2 and deterministic clustering; reflect keeps briefs, blind calibration, the evidence gate, the rubric, the debate and the contract builder. Contract 1.8.0 is unchanged in Stages 0-4. Pre-execution first, behind `--t2-engine` (default `legacy`).

The `/sc:adversarial` debate stays in both pre- and post-execution. K4 clustering runs as deterministic preparation and telemetry (`cluster_agreement`); it is not the merge. Removing the pre debate is a later, versioned experiment (candidate E') that needs its own measurement and a major contract version.

Headline reason: one reviewer-identity layer and one finding format can serve two commands without weakening any reflect grounding mechanism. The first measurement decides whether the panel-fed T2 holds quality, and whether T2 beats T1 at all.

## Candidate architectures

### A. Leave reflect as is

<!-- Source: Base (original, modified) - cost figure restated per Change #4, #20 -->
- **Changes:** nothing.
- **Keeps:** everything. That includes the hard-coded rotation table (refs/reviewer-spec.md:94-98), the debate (SKILL.md:633-651) and the two engines with diverging contract builders (cli/reflect/ensemble.py:787-832 emits `verification_ran: False` and `citations_dropped: 0` as constants).
- **Cost:** about 42k-66k output tokens per pre-execution T2 run (planning estimate, see Cost model). The earlier 49k-96k estimate is a footnote there only.
- **Risk:** low runtime risk, but maintenance risk rises. Two reviewer-pool definitions now exist (reflect's rotation and the panel's tier files, cli/review/data/review-tiers.default.json:4-11), and they will drift. Reviewer identity in the headless path comes from `T2Model0N` env vars (cli/swarm/lenses/reflect_review.py:14, cli/swarm/config.py:59) rather than a recorded, hashed resolution.
- **Verdict:** a valid fallback, the control arm of the first measurement, and the right answer if that measurement fails. It does not meet the owner's "one shared review model" goal.

### B. Full replacement: reflect T2 becomes a spec-panel review loop

<!-- Source: Base (original) -->
- **Changes:** reflect calls the panel end to end: `superclaude review panel resolve`, reviewers, `superclaude review merge` with ledger rounds (cap 3) and the reviser contract. The debate, the per-card calibrator and reflect's own merge are deleted. Ledger `confidence` single/overlap replaces calibrated confidence.
- **Keeps:** T1, the rubric, the evidence-validator.
- **Cost:** the spec-panel loop measured about 408k loop output tokens (.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19). Reflect has no revise step, so only the round-1 part applies. The default 4-reviewer panel with Haiku stand-ins writing 68k-108k each (LEDGER-RESULTS.md:66) is roughly 23k + 3 x 88k ≈ 290k for round 1 alone (midpoint arithmetic).
- **Risk:** high.
  - It drops blind calibration (SKILL.md:1172-1192) with no replacement of equal strength. Ledger confidence counts reviewers; it does not re-grade them blind.
  - The panel's measured gain comes from the ledger driving a revise loop on specs. Reflect never edits the plan (SKILL.md:342, "Findings never edit the tasklist"), so the mechanism that produced the gain is absent.
  - It breaks `merge_method` legal values (SKILL.md:789) and gate condition 9 (SKILL.md:1483).
- **Verdict:** rejected. It is the most expensive option, the gain does not transfer, and it violates the calibration constraint. <!-- fix M1 -->

### C. Layered Review Kernel with reflect adapters and a retained debate (chosen)

<!-- Source: Base (original, modified) - debate kept, contract unchanged, cost restated per Change #6, #20, #40 -->
- **Changes:** the panel code is generalized into four layers, each with a schema id:
  - **K1 Resolution:** `review-panel-resolution/1` plus PROPOSED hard exclusion, per-model `classes` and additive `skipped_slots` / `excluded` keys.
  - **K2 Dispatch adapters:** agent-session (pre) and swarm (post only), both reading K1.
  - **K3 Findings:** PROPOSED `findings-v2`, a superset of findings-v1 with typed multi-file citations, deviation class, coverage rows, completion states and `channel`.
  - **K4 Clustering:** deterministic `cluster_v2` as telemetry (`cluster_agreement`); it is not the merge.

  Reflect adds two adapters, pre and post, that sit on K1-K4 and keep briefs, per-card blind calibration, the `/sc:adversarial` debate, the evidence gate, the rubric and the contract builder.
- **Keeps:** every reflect grounding mechanism, the 1.8.0 contract and its field names and legal values, and the post-execution contract semantics.
- **Cost:** 43k-67k output-token planning estimate with the debate kept (legacy plus about 1.5k, see Cost model), inside the profile's 35k-70k band. A possible 37k-56k if cards turn out shorter is a hypothesis. Parity with legacy, no saving claimed. <!-- fix B1 item 3 -->
- **Risk:** medium. Multi-file clustering and the hard-exclusion kernel change are new code; both are default-off or telemetry-only.
- **Verdict:** chosen.

### D. Panel as dispatcher only (thin adoption)

<!-- Source: Base (original) -->
- **Changes:** reflect replaces only its rotation table with `superclaude review panel resolve`. Everything after dispatch is unchanged (cards, calibration, debate, validator).
- **Keeps:** everything else.
- **Cost:** the same as A.
- **Risk:** low.
- **Verdict:** this is Stages 1-3 of C, not a destination. It unifies reviewer identity but leaves two finding formats. That is the main maintenance cost the owner asked to remove.

### E'. Deterministic pre merge with a major contract version (deferred)

<!-- Source: Base (original, modified) - former candidate E "debate-always hybrid" re-cast as the deferred deterministic-merge candidate per Change #6, #15, #40; Variant 3, Cost model - merged per Change #4 -->
- **Changes:** as C, but in pre-execution the debate is removed and K4 clusters are the authoritative merge (disputes debated only on request). The `merge_method` legal set gains the value `panel` (pre only).
- **Keeps:** the post debate.
- **Cost:** 33k-61k output-token planning estimate (corrected parity total 43k-67k minus the debate lane 6k-10k). Not production behavior. <!-- fix B1 item 4 -->
- **Risk:** high. It is a major contract version (2.0.0), and the wrapper blocks any major other than 1 (see Return-contract mapping). Every consumer in the deferred list must change first.
- **Verdict:** deferred and not scheduled. It needs its own T1-armed measurement showing the debate adds nothing, plus the consumer list in "Deferred versioned change". C is its rollback position.

### Comparison

<!-- Source: Base (original, modified) - matrix rows restated per Change #40, #20 -->
| | A as-is | B full loop | C kernel (chosen) | D dispatcher only | E' deterministic pre (deferred) |
|---|---|---|---|---|---|
| One reviewer-identity layer | no | yes | yes | yes | yes |
| One finding format | no | yes (lossy) | yes (findings-v2) | no | yes |
| Blind calibration kept | yes | **no** | yes | yes | yes |
| Evidence gate kept | yes | yes | yes, strengthened (flags) | yes | yes |
| Debate | always | never | always (pre and post) | always | pre on disputes only |
| Contract change | none | major | none (1.8.0) | none | major (2.0.0, deferred) |
| Pre T2 output tokens (planning est.) | 42k-66k | about 290k+ | 43k-67k (legacy plus about 1.5k; a possible 37k-56k if cards turn out shorter is a hypothesis) | 42k-66k | 33k-61k |
| Transfers the measured panel gain | no claim | no (no revise step) | no claim | no claim | no claim |
| Maintenance surface | 2 pools, 2 formats, 2 merges | 1 | 1 kernel + thin adapters | 1 pool, 2 formats | 1 kernel |

## Chosen architecture and reasons

<!-- Source: Base (original, modified) - reasons 2, 3 edited and reason 6 added per Change #10, #41, #17, #31 -->
**C, the Layered Review Kernel.** Reasons, in order of weight:

1. **The maintenance unit is the layer, not the command.** Today, reviewer identity lives in three places: the reflect rotation table (SKILL.md:604-608), the `T2Model0N` env pool (reflect_review lens), and the panel tier file (review-tiers.default.json:4-11). Finding shape lives in two places: reviewer card YAML and findings-v1 (findings.py:90-121). Merge lives in two places: `/sc:adversarial` and `merge_round` (ledger.py:107-298). C reduces identity and finding shape to one implementation each, with a schema id. Commands differ only in policy: brief, required finding fields, gates and contract.
2. **No grounding mechanism is weakened.**
   - Calibration (SKILL.md:1172-1192) stays per card, embedded in the card as today.
   - The evidence-validator stays mandatory (SKILL.md:587). It gains a deterministic citation pre-check that only flags citations for re-read.
   - Executor-class exclusion (SKILL.md:600-610) becomes a hard K1 input instead of reflect-side table editing.

   Evidence that the gates carry load (recorded stoprule card, `reviewer-1-card.yaml`, plan-verified): findings are YAML with `severity: blocking|minor`, categories `ordering|acceptance|deviation|coverage|risk`, `evidence: [plan:57, source.md:62, src/...:451-462]` (line refs, no quotes), an orchestrator-written `model_class: sonnet`, `persona`, and `plan:`/`spec:` paths; the calibrator scored F1-F3 at 0.60, 0.50, 0.55 ("fit major better than blocking"); the final gate dropped `source.md:143` (a heading) which a "quote locates" check would pass (per V2, `REPORT.md:130-132`, not re-read by the plan). Consequence for the design: a deterministic locate check cannot replace the semantic re-read (see "Evidence gate and citation pre-check"), and the recorded card gives line references, so findings-v2 `citations[]` are built from `path:line` refs with `quote` optional (see Finding format).
3. **The debate is kept.** EV-2 forbids a self-built merge, the debate's value is unmeasured and not shown idle (recorded pre contracts show convergence below 1.0 in 14 of 35 numeric cases, see Return-contract mapping), and the post debate feeds promotion and rollback. Pre-execution reflect is advisory: sc-workflow records only `reflect_status` and `reflect_report_path` and never changes the workflow status (skills/sc-workflow-protocol/SKILL.md:60-64, enrichment). Post-execution feeds promotion condition 9 (SKILL.md:1483) and the wrapper's degraded triggers 9-11b (cli/reflect/contract.py:290-326).
4. **Extension scaffolding at low cost.** A third consumer (for example `/sc:auggie-review` or `/tdd`) would add a template, a brief and a contract mapping, and nothing else. No new merge code and no new reviewer pool.
5. **It does not claim the PN1 gain.** The spec-panel gain (15.7 vs 2.8 fixed defects, LEDGER-RESULTS.md:19) was measured with a revise loop on specs. C adopts the panel for maintainability, not for a quality uplift. Quality is checked by the first measurement as non-inferiority.
6. **The first shipment changes no contract and no reviewer class.** It is parity plus a format and dispatch layer, so the measurement can attribute any difference.

## When the panel is called (depth x tier path)

<!-- Source: Base (original, modified) - new section merged per Change #39 (coordinator requirement); Base mentions of --depth reconciled -->
The panel is a Tier-2 mechanism. It is called only after the **final** tier is 2. Order of decisions, unchanged from `SKILL.md`: (1) Wave 0 alias routing (`:231-239`: 1 alias -> T1 only; 2 aliases -> 2 reviewers; 3+ -> 3) and executor class (`:600-602`); (2) budget pre-flight (`:262-273`); (3) Waves 1-2: T1 card, coverage map, blind calibration of the T1 card, rubric (`:354-402`); (4) **only now** the T2 engine flag `--t2-engine` is read, at the start of Wave 3. The effective engine and the requested engine are both written to `tier_decision.yaml` and the manifest.

**Rules.** D1: a `--depth quick`, `--tier 1`, `--no-escalate` or rubric-stopped T1 run **never** calls the panel and never reads `--t2-engine`. D2: the staged-migration flag is checked after the depth, pin, budget and rubric decisions, never before. D3: a run pinned to T2 (`--depth deep` or `--tier 2`) whose panel yields fewer than 2 distinct eligible classes does **not** silently run T1 or one reviewer: it emits the `SKILL.md:600` WARN and `executor_exclusion_degraded: true` (if exclusion caused it), `t2_floor_unmet` in `degraded_components` (a benign token, not in `contract.py:31-33`), forces `status: partial`, and REPORT.md opens with a banner naming the unmet floor; a rubric-driven escalation keeps the existing silent-safe T1 degrade of `SKILL.md:600` with the WARN. N=2 is the minimum in every case (`SKILL.md:610`; `reviewer-spec.md:102`). D4: unsupported cells (gateway, null `launch`, unmapped model) run the legacy rotation and record `panel_fallback_reason`. D5: `N_eff = min(--reviewers, alias count, 3)` (`SKILL.md:86`, clamp rule by depth is unstated in the rows I read and stays UNVERIFIED), anchor never dropped.

Reflect's `--depth` is Tier-1-only / Tier-1-then-rubric / force-Tier-2 (`SKILL.md:84`). The flag `--depth standard` that appears in the debate command (`SKILL.md:648`) belongs to `sc-adversarial`, a different flag. `--depth deep` never means "more reviewers" and never means "debate only on disputes".

| Depth / pin / modifier | Tier path | Panel called? | Template and reviewers | Stages that run | Expected cost (profile unit; planning) | Notes |
|---|---|---|---|---|---|---|
| `--depth quick` | T1 only (`:364`) | No | none | Waves 0-2 including the T1 card's blind calibration; no Wave 3-4 | 3k-8k claude + 2k-5k auggie (`cost-profile.yaml:36-39`) | `--t2-engine` ignored |
| `--tier 1`, `--no-escalate` | T1 (`:362,366`) | No | none | as above | as above | `--no-escalate` warns if C < 0.85 |
| `--depth standard` (default implied by `--tier auto`, `:84-85`; UNVERIFIED as a stated default), rubric stops | T1 | No | none | as above | as above | recorded: 0 of 38 |
| `--depth standard`, rubric escalates (rows 3-7, parsed-sparse pre-filter) | T1 work then T2 | Yes if engine is `panel` or `shadow` | `@reflect-pre`, 3 reviewers (2 if 2 aliases); `@reflect-enterprise` if `--strategy enterprise` | Wave 3 resolve + dispatch; per-card blind calibration; Wave 4 `sc-adversarial` debate on cards (not a deterministic merge); Wave 5 synthesis; evidence-validator; K4 clustering and pre-check as telemetry | planning 43k-67k output (legacy 42k-66k); profile band 35k-70k claude + 10k-25k auggie (`:46-51`) | the typical `/sc:workflow` plan: recorded 37 of 38 |
| `--depth deep` | forced T2 (`:365`) | Yes | same templates and count; no extra reviewers | as above plus the deep-only behavior of `--remediate` (task-builder route, `:89`) and optional tech-research in Wave 1B (`:637`) | as T2; deep extras unmeasured (no deep row in the profile) | D3 applies; 2 of 38 recorded |
| `--tier 2` | forced T2 (`:363`) | Yes | same | as T2 | as T2 | D3 applies |
| `--budget-remaining N`, N < 5 | STOP (`:267`) | No | none | none | none | |
| N = 5 | T1 forced (`:268`) | No | none | T1 | T1 | `budget_forced_tier_downgrade: true` |
| 6 <= N < 65 | T2 downgraded to T1 with WARN when the rubric asks for T2 (`:269`) | No | none | T1 | T1 | band 52 <= N < 65 has no row label in the table I read (UNVERIFIED how implemented); safe default: treat as downgrade |
| N >= 65 or unset | as the rubric directs (`:270-271`) | per rows above | per rows above | per rows above | the panel's p95 must stay <= 65k (`cost-profile.yaml:70`; 52 x 1.25) | panel adds no budget logic |
| executor class collides with the pool | N=2 floor then T1 degrade (`:600`) | only if >= 2 distinct eligible classes remain | `@reflect-pre-x2` etc. (see "K1 hard exclusion contract") | as T2, or T1 | as T2, or T1 | D3 for pins |
| `--unattended` | unchanged | per rows above | per rows above | per rows above | unchanged | |
| headless `superclaude reflect` | post only (`ensemble.py:797`) | Stage 5 only | `@reflect-post` | existing ensemble, swarm lens | post planning unchanged | pre is never headless |

**What a default-depth `/sc:workflow` run triggers.** Wave 4 of `sc-workflow` invokes `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with defaults for every other flag (`sc-workflow-protocol/SKILL.md:60`): depth standard, tier auto, no `--reviewers`, no `--budget-remaining` (budget check skipped), executor class unknown. So it runs T1 first, then the rubric, which in the recorded history escalated to T2 in 37 of 38 pre runs (34 by the parsed-sparse pre-filter because workflow sources carry no labelled requirement ids, others by rule 4, 5 or 6). Recorded evidence: of 38 recorded pre tier decisions under `.dev/reflect/pre-*/artifacts/tier_decision.yaml`, 37 selected tier 2 and 1 selected tier 1 (a `--tier 1` user pin); 34 carry `coverage_degraded: parsed-sparse`; 21 are sc-workflow packages; 2 were forced by `--depth deep`; 0 stopped at T1 on the rubric. The cause is the table-wide pre-filter of `SKILL.md:400`: when `coverage_degraded` is set no STOP row may fire; sc-workflow plan sources carry no labelled requirement ids ("inferred 10 > parsed 0"), and rule 4 (`S_domains >= 3`) and rule 6 (`C < 0.85`) also fire in the recorded reasons. With the engine at `panel`, every such run calls the panel; with the default `legacy` it never does. This is why the T2 cost, not the T1 cost, is the typical per-plan cost, and why the rubric's parsed-sparse behavior (O-8) deserves its own look after H-A. These figures are counts over one repository's `.dev/reflect/` history.

## Answers to Q1-Q7

### Q1. What the panel takes over, what it lacks, what stays in reflect

<!-- Source: Base (original, modified) - rows restated per Change #42, #5, #24 -->
**Direct answer:** the panel takes over the reviewer pool, model diversity, deterministic resolution, the dispatch description and telemetry. It lacks hard executor exclusion, personas, blind calibration, an evidence gate, multi-file citations, deviation class and coverage rows. All reflect-specific judgement stays in reflect, including the merge, which remains the `/sc:adversarial` debate.

| Function | Today in reflect | Panel today | Owner in C |
|---|---|---|---|
| Reviewer pool, model rotation | rotation table (SKILL.md:604-608) | tier aliases + templates (review-tiers.default.json:4-11; review-panel.default.json:8-12) | **kernel K1** (reflect templates, PROPOSED) |
| Deterministic, recorded choice | none (agent-session) / env pool (swarm) | seeded by run id, template and tier hashes recorded (panel.py:455-459, 514-525) | **K1** |
| Model diversity | `_diversity.py` full/degraded (enrichment) | `distinct_across_slots`, soft (panel.py:405, 408 fall back to the full candidate list) | K1 computes it; reflect keeps `t2_*_diversity` emission |
| Executor-class exclusion | hard rule, N=2 floor (SKILL.md:600-610) | **lacks**: `exclude` is soft and ignored by `fixed` slots (panel.py:402-403) | **kernel hard exclusion** (see "K1 hard exclusion contract"); reflect supplies the class and the policy |
| Personas | analyzer/qa/refactorer via brief (refs/reviewer-spec.md:94-98) | **lacks** | **reflect**: persona by resolution ordinal (no kernel change) |
| Parallel dispatch | Agent tool `reflect-reviewer` / swarm lens | `launch` alias map (review-tiers.default.json:29), no dispatcher | **K2 adapters** read K1 |
| Blind calibration | `confidence-calibrator` per card (embedded block), disjoint class (SKILL.md:1172-1192) | **lacks** | **reflect** |
| Merge | `/sc:adversarial --compare` (SKILL.md:645-651) | `merge_round` cluster + ledger (ledger.py:107-298) | **`/sc:adversarial` stays the merge**; K4 clustering as telemetry |
| Evidence gate | evidence-validator, mandatory (SKILL.md:587) | **lacks** | **reflect**, with a deterministic flagging pre-check |
| Telemetry | §9.2 block (SKILL.md:892-921) | `review-telemetry/1` (enrichment: names only) | both: reflect §9.2 stays; K1/K4 append panel records |
| Grounding, coverage map, deviation taxonomy, rubric, remediation, promotion | reflect | n/a | **reflect** (constraint) |

### Q2. A finding format for both

<!-- Source: Base (original, modified) - calibration no longer carried in the block per Change #5, #42 -->
**Direct answer:** findings-v2 (PROPOSED), a strict superset of findings-v1. `anchor` becomes optional when `citations[]` is present. Typed fields are added for deviation class, coverage rows, self-reported confidence, completion state and channel. Calibration is not carried in the block: it stays in the card's embedded `calibration:` block. Reflect's reviewer card keeps its prose. The machine part of the card *is* the findings-v2 block. Schema and dedupe key are in the Finding format section.

### Q3. Merge: debate, deterministic, or both

<!-- Source: Variant 2 (sonnet:analyzer), Q3 and Stage 5; Variant 3 (haiku:backend), Q3 - merged per Change #6; Base (original, modified) -->
**Direct answer:** the debate stays in both modes. K4 clustering runs as deterministic preparation and telemetry; it is not the merge. Removing the pre debate is a later, versioned experiment (candidate E') that needs its own T1-armed measurement and a major contract version. EV-2 forbids a self-built merge (`SKILL.md:789`), so keeping the debate is the only legal choice today.

What the debate provides that clustering cannot, and why it is kept:

- **Pre-execution.**
  1. Arbitration when reviewers disagree on whether a plan gap is blocking. A deterministic merge takes the OR of blocking and the max severity (ledger.py:187-190), so disagreement turns into "blocking, single support". It is not resolved.
  2. The narrative synthesis of a merged verdict (the `merged-verdict.yaml` that EV-1 checks, `SKILL.md:666`).
  3. A real numeric convergence score, `adversarial_convergence_score`. No substitute score is introduced.
- **Post-execution.** Arbitration of deviation *class* (Necessary vs Drift vs Regression) drives `deviation_count_by_class`, `regression_present`, TurnLedger rollback (SKILL.md:930), promotion condition 4 (SKILL.md:1472) and the wrapper's halted triggers (contract.py:369-381). A deterministic merge cannot decide between two classes; it can only take the worst. That would over-report Regression and block promotions that should pass.

The cards (calibrated, with embedded calibration) are the debate's inputs exactly as `SKILL.md:645-651`. The K4 cluster map is telemetry only until a measurement shows it helps; it is not an input to the debate.

**Judge identity.** Reflect does not pin a judge (`SKILL.md:612`; `reviewer-spec.md:112-116` says sc-adversarial owns judge selection and reflect only delegates disjointness). After the debate returns, the adapter records `judge_identity` (as reported by `sc-adversarial-protocol` in its return contract, UNVERIFIED which field) and sets `judge_class_collision: true` when the judge class equals a reviewer class or the executor class; a collision is telemetry plus a REPORT.md note, never a silent pass. Whether `--compare` accepts a judge-exclusion input is UNVERIFIED; if it does not, the collision is recorded, not prevented. Fable and Tier 0 are never a judge: the adapter asserts the recorded judge model id is not `claude-fable-*` and not a `tier0` alias.

### Q4. Engine

<!-- Source: Base (original, modified) - agent-session bullet replaced per Change #7; Variant 2 (sonnet:analyzer) Q4 rule and Variant 3 (haiku:backend) Q4 launch binding -->
**Direct answer:** the pre-execution path uses the agent-session engine only, with one identity source. The K1 resolution JSON is the only place reviewer models are chosen. The swarm engine stays post-only (Stage 5).

**Agent-session adapter (pre-execution).** For each reviewer in the K1 resolution: if `launch` is non-null and in the whitelist `{sonnet, opus, haiku}`, spawn `~/.claude/agents/reflect-reviewer.md` (project `.claude/agents/` first) with the Agent-tool `model` set explicitly to that value. The adapter must pass `model` on every dispatch (omitting it would run the agent's frontmatter default, Sonnet, for all reviewers; `reflect-reviewer.md:6` has `model: sonnet`); a conformance check asserts one explicit `model` per reviewer before dispatch. The Agent tool's `model` parameter in this harness accepts only `sonnet | opus | haiku | fable`; a gateway tier alias such as `claude-gw-tier2[1m]` is not in that set. If `launch` is null (every gateway model today, `review-tiers.default.json:20,23`) the resolution is **refused for pre-execution**: the run uses the legacy rotation and records `panel_fallback_reason: no-launch-alias`. No swarm dispatch is claimed for pre-execution; the swarm lens stays post-only (`ensemble.py:797`). The resolution is pinned (hashed template, tiers, seeds, executor-class exclusion result) before any reviewer is dispatched and is never re-resolved mid-run. Gateway agent-session dispatch is an open item (O-4); the first stage that supports it needs its own conformance run.

**Swarm adapter (headless post path, Stage 5, cli/reflect/ensemble.py).** The `reflect-review` lens may take worker models from a PROPOSED `--panel-resolution <file>` input instead of `T2Model0N` env vars. `T2Model0N` stays as the fallback when no resolution file is given, so existing runs are unaffected.

#### Template set

<!-- Source: Base (original, modified) - template JSON replaced per Change #23 -->
Reflect's rotation becomes packaged K1 templates, all `review-panel.<name>.json`, loadable as `@<name>` (panel.py:327-334); each has exactly one `fixed` slot; none lists a tier-0 or Fable tier. V1's original template is the only validator-legal shape (one fixed slot, `panel.py:140-141`; slot ids match `^[a-z0-9]{1,8}$` `:31`; keys within `_SLOT_KEYS` `:46`), but its three slots change the anthropic-only reviewer set to sonnet, haiku, haiku and move Opus to the calibrator, which changes `t2_model_class_diversity`. Parity therefore needs a third slot on `tier1a` (`review-tiers.default.json:5`: opus, sonnet).

```json
{"schema": "review-panel/1", "template_id": "reflect-pre", "version": "1.0.0",
 "distinct_across_slots": true, "apply_to": ["first"],
 "slots": [
   {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
   {"slot_id": "t4",  "tier": "tier4",  "count": 1, "strategy": "random"},
   {"slot_id": "t1a", "tier": "tier1a", "count": 1, "strategy": "random"}]}
```

- `@reflect-pre` (parity, default). Anthropic-only resolves to sonnet, haiku, opus under strict distinctness: tier1b -> sonnet; tier4 -> haiku (a direct tier4 member and in the anthropic-only `available` list, `review-tiers.default.json:10,27`); tier1a minus {sonnet, haiku} -> opus. Persona by resolution order: fixed first, then slot order: analyzer, qa, refactorer (matches `reviewer-spec.md:97`). Parity matters because `t2_model_class_diversity: full` means three distinct classes (`SKILL.md:233-239`) and wrapper trigger 7 reads that field (`contract.py:281-284`).
- `@reflect-pre-x2` (anchor replacement when tier1b is exhausted by the executor, i.e. executor `sonnet` in anthropic-only, where tier1b has only Sonnet and no stand-in, `review-tiers.default.json:6,28`): fixed `t4` anchor plus random `t1a`. Resolves haiku, opus (2 reviewers, analyzer and qa), matching `reviewer-spec.md:102,109`.
- `@reflect-enterprise`: same slots as `@reflect-pre`; third persona `architect`; opt-in for `--strategy enterprise` (`SKILL.md:608`).
- `@reflect-lite` (variant arm only): V1's original three slots t1b, t4, t2; resolves sonnet, haiku, haiku (soft) or sonnet, haiku (strict, third slot skipped).
- Post templates `@reflect-post` and `@reflect-post-x2` mirror pre. Gateway templates are not defined (O-4).

The 2-distinct diversity rule is the headless helper's (`_diversity.py:8-15`), which returns `insufficient`, not `degraded`, a vocabulary mismatch with `SKILL.md:790` recorded as O-9. The claim that anthropic-only "resolves to Sonnet, Haiku, Haiku" by default is withdrawn.

#### K1 hard exclusion contract

<!-- Source: Base (original, modified) - hard_exclude semantics replaced per Change #24 (INV-005); Variant 3 (haiku:backend) Q4 filter-before-dispatch merged -->
**K1 hard exclusion contract (PROPOSED code; generic panel behavior unchanged).** Verified failure modes today: a `fixed` slot returns `candidates[0]` and ignores `exclude` (`panel.py:402-403`); `random` and `round_robin` use `[m for m in candidates if m not in set(exclude)] or candidates` and so re-admit an excluded model when the pool empties (`panel.py:405,408`); `exclude` today carries only models chosen earlier in this panel (`panel.py:479`); `NoModelAvailable` is raised only when no candidate and no stand-in exists (`panel.py:396-401`); the anthropic-only stand-in map has no `tier1b` (`review-tiers.default.json:28`); `review-tiers.default.json:6` lists three tier1b models but only Sonnet is in the anthropic-only `available` (`:27`).

1. `resolve_slot` and `resolve` gain two keyword-only parameters with defaults that reproduce today's behavior byte for byte: `hard_exclude: Sequence[str] = ()` (model ids) and `strict_distinct: bool = False`. They are resolve-time parameters, not template keys (`validate_panel` rejects unknown slot keys, `panel.py:109-111`).
2. Filtering is applied to the **candidate list itself**, before the strategy runs, for all strategies including `fixed`: `candidates = [m for m in candidates if m not in hard]` where `hard = set(hard_exclude) | (set(chosen) if strict_distinct else set())`. Fallbacks (`panel.py:417`) are derived from the filtered list, so no primary or fallback can be an excluded model. The silent `or candidates` re-admission is **not** taken when `hard` is non-empty.
3. If the filtered list is empty and the stand-in list has not yet been tried, try `stand_ins` filtered the same way; if still empty raise a new `ExclusionExhausted(tier)` (a subclass of `NoModelAvailable`). With `hard_exclude == ()` and `strict_distinct == False` the code path, output and hashes are identical to today (asserted by a spec-panel byte-identity test).
4. `resolve` records `skipped_slots: [{slot_id, reason}]` and `excluded: {models, classes}` as additive keys in the `review-panel-resolution/1` JSON; `merge_cmd.py:76-79` reads only `reviewers[*].reviewer_id/model`, so existing consumers are unaffected. A non-fixed slot that raises `ExclusionExhausted` is **skipped** (recorded), not fatal; the fixed anchor raising is fatal at kernel level. (The kernel fails closed; the reflect adapter catches the exception per slot and applies `SKILL.md:600`, below.)
5. **Class map.** The tier file gains a `classes` object mapping every model id to a class string in the vocabulary of `SKILL.md:1180` where one exists (`claude-opus-5-5: opus`, `claude-sonnet-5-5: sonnet`, `claude-haiku-5-5: haiku`) and a vendor family otherwise (`gpt-*: gpt`, `glm-*: glm`, `grok-*: grok`, `Qwen*: qwen`, `muse-*: muse`). A model id with no entry is **not eligible** in any `reflect-*` template (fail closed at validation). `--hard-exclude-class <class>` (PROPOSED CLI flag on `superclaude review panel resolve`) expands the class to ids through this map and compares case-insensitively with the executor value resolved by `SKILL.md:600-602` (flag, `EXECUTOR_MODEL_CLASS`, or log hint; headless wrapper also reads frontmatter `executor_model_class`, `cli/reflect/config.py:53-56,351-355`). The gateway classes `gpt|glm|grok|muse` are outside the `SKILL.md:1180` calibrator vocabulary; gateway is out of scope until O-4.
6. **Adapter (reflect side) applies the policy, the kernel only enforces:** (a) resolve with `@reflect-pre`, `strict_distinct=True`, `hard_exclude` = ids of the executor class. (b) If the fixed anchor raises `ExclusionExhausted`, re-resolve once with the anchor-replacement template (`@reflect-pre-x2`) before any dispatch; the replacement is recorded (`anchor_replaced: true`). (c) After resolution assert: no resolved model class equals the executor class; no model id repeats; at least 2 distinct classes. (d) Failure of (c), or a second exhaustion, is the `SKILL.md:600` path: `executor_exclusion_degraded: true`, WARN with the text of `SKILL.md:600`, degrade to T1 for rubric-driven escalation. For a pinned `--depth deep` or `--tier 2` run the degrade is never silent: see rule D3 of "When the panel is called".
7. **Unknown executor** (`executor_class_source: unknown`): unchanged fail-open of `SKILL.md:602` (`executor_class_resolved: false`, loud WARN); the panel runs without `hard_exclude`. This is the main consumer path today: `sc-workflow` Wave 4 passes only defaults (`sc-workflow-protocol/SKILL.md:60`) and a recorded workflow-driven pre run has `executor_class_source: unknown` (`.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/return-contract.yaml:96-97`). Exclusion therefore rarely fires in the main consumer path; see O-6.
8. **Tests (Stage 1 exit):** excluded model is the fixed anchor; pool empties for random and round_robin slots and the excluded model is not re-admitted; executor `sonnet` in anthropic-only yields `ExclusionExhausted` for `tier1b` and the adapter lands on `@reflect-pre-x2` with 2 reviewers; executor `haiku` skips the `t4` slot; executor `opus` under strict distinctness yields sonnet, haiku and no duplicate; unmapped model id rejected; `hard_exclude == ()` is byte-identical to the current resolution for the default and live7 templates.

#### Opus uses

<!-- Source: Base (original, modified) - "Opus only here" claim replaced per Change #19; Variant 3 (haiku:backend) Q3 Opus rule -->
**Opus uses (complete list; the owner's ceiling is "Opus only sparingly").** (1) Blind calibrator, chosen by the unchanged rule of `SKILL.md:1181-1186` (highest capability from the set disjoint from reviewers, else the class used by fewest reviewers, with `calibrator_diversity: degraded`). (2) Third reviewer in the anthropic-only parity template, exactly where today's rotation puts it (`SKILL.md:607`), and as backfill when the executor class is removed (`reviewer-spec.md:108`). (3) Reviewer in the opt-in `--strategy enterprise` template (`SKILL.md:608`). (4) Never as a judge pinned by reflect (`SKILL.md:612`). No use is new relative to today. The calibrator for the parity template stays `degraded` (the disjoint set is empty; recorded card: `calibrator_model_class: opus`, `calibrator_diversity: degraded`). The lite template (variant arm only) moves use (2) to use (1): its calibrator diversity becomes `full`, its model-class diversity falls from three classes to two, which the interactive skill labels `degraded` (`SKILL.md:237-239`). That value change is why lite is a measured arm and not the first shipment. Fable and Tier 0 are never used. Every Opus mention elsewhere in this document points here.

#### Forbidden models: Fable and Tier 0

<!-- Source: Variant 2 (sonnet:analyzer), U-013 and Risk 7 - merged per Change #8 -->
The tier file maps four ids in `launch`, including `claude-fable-5-1` to `fable` (`review-tiers.default.json:14,27,29`); `panel.py:30` `_TIER = ^tier[0-9]{1,2}[a-z]?$` accepts `tier0`; nothing in `cli/review` mentions Fable (grep over `cli/review`, only the tier json). Reflect profile validation (PROPOSED, in the kernel, applied to every `reflect-*` template and to every resolution): (1) reject any resolved model id matching `claude-fable-*`; (2) reject any template slot whose tier is `tier0` or whose alias list contains a Tier 0 model; (3) reject a `launch` value outside `{sonnet, opus, haiku}` at dispatch. The same filter applies to the calibrator pick and to the recorded judge identity.

#### Executor-exclusion gates

<!-- Source: Base (original, modified) - new subsection merged per Change #26 (INV-022) -->
Executor exclusion is enough only if eight gates hold, including identity read-back. The card's top-level `model_class: sonnet` is orchestrator-written, so today identity is the request; the Agent tool schema exposes no model-id in a reply (UNVERIFIED for the reply body); `reflect-reviewer.md:6` defaults to Sonnet when no override is passed; the recorded workflow pre run has an unknown executor.

| Gate | Decision | Evidence or test | If it fails |
|---|---|---|---|
| 1 executor class resolved (flag, env, log; `SKILL.md:600-602`) | unchanged; `unknown` stays fail-open and is reported as `executor_class_resolved: false` | recorded run `return-contract.yaml:96-97` | no exclusion, loud WARN |
| 2 per-model class map | `classes` in the tier file; unmapped ids ineligible | K1 contract item 5 | template invalid, legacy rotation |
| 3 candidate filter | kernel `hard_exclude` on primary, fallback and fixed | tests in K1 contract item 8 | degrade per K1 contract item 6 |
| 4 `resolve_slot` pick | no `or candidates` re-admission under `hard` | `panel.py:405,408` fixed by K1 contract item 2 | `ExclusionExhausted` |
| 5 tier1b stand-in | none exists (`review-tiers.default.json:28`); anchor replacement template | `@reflect-pre-x2` | degrade |
| 6 dispatch via `launch` | whitelist `{sonnet, opus, haiku}`; null refused for pre; explicit `model` on every call | Agent-session adapter above | legacy rotation |
| 7 actual identity | **identity_source = `requested-pinned`** (the Agent tool pins `model`); the card header records `model_class` from the request, as today; each reviewer card must also carry a one-line self-report `reviewer_model_self_report` (advisory); a mismatch with the pin sets `identity_mismatch_suspected: true`, degrades diversity telemetry and never upgrades trust | **Spike S-ID, Stage 1 exit:** dispatch three probe reviewers (`model: haiku`, `sonnet`, `opus`) with a probe brief; check (a) the self-report matches the pin in 3 of 3 and (b) whether the tool result or transcript exposes a model id. If (b) is yes, switch `identity_source` to `observed` and assert it; if no, the pinned identity stays and is stated as an unverified assumption | UNVERIFIED until the spike runs |
| 8 N=2 floor on distinct classes | counts `complete` reviewers of **distinct** classes (see "Completion and channel") | test: two reviewers of one class do not reach T2 | T1 degrade (`SKILL.md:600`) |

Safe default if S-ID is not run: pinned identity, `identity_source: requested-pinned` in telemetry, and no claim of verified independence in REPORT.md.

#### Guards and counts

<!-- Source: Base (original, modified) - new guards merged per Change #30 (INV-006, 007, 009, 011) -->
**INV-006:** an unknown executor keeps the fail-open path and the T2 report states `executor_class_resolved: false`; the T2 label is allowed but REPORT.md must not claim anti-self-confirmation; the Stage 2 telemetry counts how many runs have it (O-6). **INV-007:** the N=2 floor is enforced on **distinct classes among `complete` reviewers**, in the adapter (strict distinctness) and as a post-resolution assertion; the headless builder's `tier_reached` rule (`ensemble.py:772` sets `tier_reached = 2` on `reviewer_count >= 2` without checking models differ) is a Stage 5 work item (add a distinct-model check there). **INV-009:** pre reviewers are only launched through the `reflect-reviewer` agent with an explicit `model` override; `reflect-reviewer.md:5-8` gives `tools` (Read, Grep, Glob and read-only search MCP tools, no Bash/Edit/Write) and `permissionMode: plan`; the allowlist is expected to survive the override (UNVERIFIED, part of spike S-ID: the probe reviewers are given a write attempt that must fail); a `launch: null` model is never dispatched, so no swarm path exists for pre; the post swarm path keeps its existing isolation telemetry (`ensemble.py:825-831`). **INV-011:** the manifest records three counts, `reviewers_requested`, `reviewers_resolved`, `reviewers_complete`; EV-1 compares calibrated cards with `reviewers_resolved` (unchanged); a short run is MALFORMED under EV-1, remediated by the existing bounded re-dispatch, then the F2 fallback. The 2-of-3 mismatch between EV-1 (`SKILL.md:666` calls it MALFORMED) and the wrapper (`ensemble.py:765-770` records a benign `reviewer-shortfall`; halt set only auggie, env-aliases, evidence-validator, `contract.py:31-33`) pre-exists and is preserved; Stage 2 counts it.

### Q5. Pre-execution migration end to end

<!-- Source: Variant 3 (haiku:backend), Q5 - merged per Change #12 (answer in place); Base (original, modified) -->
**Direct answer:** inputs are plan plus source spec (`--spec <pkg>/source.md --tasklist <pkg>/<id>.md`, enrichment). Waves 0-2 are unchanged and decide the tier; the panel runs only if the final tier is 2 and `--t2-engine` is not `legacy` (rules D1-D5 of "When the panel is called"). Then: resolve the reviewers with executor exclusion; dispatch them through the agent-session adapter; blind-calibrate each card; run the `/sc:adversarial` debate on the calibrated cards; run the evidence gate; emit contract 1.8.0 unchanged. Flag order: depth, pin, budget and rubric first, `--t2-engine` after. The step-by-step flow is in "Adapter sketches".

### Q6. Rounds, ledger, revise loop

<!-- Source: Base (original, modified) - ledger not used for reflect per Change #17, #29 -->
**Direct answer:** reflect is single-pass (`SKILL.md:342`; it never revises the artifact it reviews, so rounds 2-3 would have nothing to verify). **The panel ledger is not used for reflect in Stages 0-4:** the merge is the `sc-adversarial` debate; K4 clustering writes `panel/clusters.json` and needs no rounds, no REVISE/ESCALATE decision and no `doc_sha256`. If a later stage uses the ledger, run it with `--cap 1` knowing every blocking round records `ESCALATE` (`_decision` returns `REVISE if n < cap else ESCALATE`, `ledger.py:93-96`), reflect must ignore `decision`, and telemetry must not surface it as an escalation. Each merge attempt gets its own ledger path (see "Execution contract"). A ledger row stores a bare `span` per row (`ledger.py:196-197`) and one `doc_sha256` per round (`:278-279`), which is why it is path-blind (see "Multi-file identity").

**Extension point, not built:** sc-workflow's Phase B "refactor" loop re-runs Phase A into a new package (SKILL.md:342). A future ledger keyed on the workflow id could carry findings across those packages. That is deferred and named only so a future ledger id is not tied to one reflect run id.

### Q7. Cost before and after; when a full panel is not worth calling

<!-- Source: Variant 3 (haiku:backend), Q7 - merged per Change #12, #4; Variant 2 (sonnet:analyzer), Q7 rule - merged per Change #9; Base (original, modified) -->
**Direct answer:**

- **Pre-execution:** the first shipment is parity. The panel-parity T2 planning estimate is 43k-67k output tokens (legacy plus about 1.5k for the findings block) against 42k-66k for legacy; a possible 37k-56k if cards turn out shorter is a hypothesis; no saving is claimed. Panel T2 must stay inside the existing 35k-70k profile band and below the 65k kill line at p95 (a measurement criterion, see First measurement). The arithmetic and units are in "Cost model".
- **Post-execution:** about unchanged (the debate is kept; +1.5k for the findings blocks).
- **A full panel (default 4 slots, or live7) is not worth calling for reflect:**
  - In anthropic-only, every extra slot is another Haiku stand-in. That adds tokens without new model classes. The 1S+6H vs 1S+3H gain was about 3 defects on one spec (docs/reference/review-panel-live7.md:19-26, enrichment).
  - Reflect has no revise step to turn extra findings into fixes.
  - Pre is advisory.

**Code-level cap (hard):** reflect-profile validation rejects any `reflect-*` template or resolution with more than 3 reviewers, whatever the user template says (the generic panel keeps 1..8 for `/sc:spec-panel`, `panel.py:142`; reflect is limited to 2-3, `SKILL.md:86`). `N_eff = min(--reviewers (default 3), alias-derived count from SKILL.md:233-239, 3)`; a fixed anchor is never dropped; trailing random slots are dropped first. **Raising the cap** to 4+ needs (PROPOSED, labelled as such because V3 dissents) a measurement showing T2 recall beats T1 recall by at least 15 percentage points and the larger panel beats T2 by a margin the owner accepts. Larger panels are never an automatic response to `--depth deep` (V2 Q7 allowed 4+ on `--depth deep`; rejected: `--depth deep` forces T2 and routes remediation, `SKILL.md:89,365`, and says nothing about reviewer count).

## Finding format

<!-- Source: Base (original, modified) - table rows restated per Change #5, #11, #37, #2 -->
PROPOSED schema `findings-v2`. It is JSON lines in a fenced block with info string `findings-v2` under the heading `## Findings block`, the same container rules as v1 (findings.py:124-196). A v1 line is valid v2 by construction.

| Field | Type | v1? | Set by | Rule |
|---|---|---|---|---|
| `id` | str `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` | yes | reviewer | unique per block (findings.py:91-95) |
| `severity` | CRITICAL/MAJOR/MINOR | yes | reviewer | MINOR cannot block (findings.py:100-101) |
| `blocking` | bool | yes | reviewer | |
| `category` | v1 six-value enum, unchanged (findings.py:15-22) | yes | reviewer | reflect's original label is preserved in `reflect_category` (mapping below) |
| `reflect_category` | `ordering` `acceptance` `coverage` `contradiction` `risk` `deviation` | NEW | reviewer | original reflect label, never routes anything |
| `claim` | str ≤300 | yes | reviewer | |
| `refs` | ≤8 str | yes | reviewer | requirement ids such as `REQ-014`, `INF-003`, task ids |
| `anchor`, `anchor2` | quote 12-200 chars | yes | reviewer | **required only if `citations` is absent**; a finding with neither is invalid |
| `citations` | list 1..8 of `{role, path, line_start, line_end, quote?}` | NEW | reviewer | `role` ∈ `plan` `spec` `source` `test` `diff` `artifact`; `path` repo-relative; `quote` **optional** (12-200 chars copied from those lines when present) |
| `deviation_class` | `authorized` `necessary` `drift` `regression` `none` | NEW | reviewer | required when `lens` is `reflect-post`; optional in pre (plan-vs-spec gaps map to `none` or a coverage category) |
| `coverage_rows` | list of requirement/task ids | NEW | reviewer | must be ids present in the reviewer's Coverage slice |
| `self_confidence` | float 0-1 | NEW | reviewer | self-report; never routes anything |
| `lens` | `spec` `reflect-pre` `reflect-post` | NEW | brief | selects the required-field profile |
| `channel` | `defect` `grounding-gap` `advisory` | NEW | reviewer | optional, default `defect` (see "Completion and channel") |

**Category and severity mapping** (v1 six-value enum unchanged; reflect's original label is kept in `reflect_category`): `ordering` -> `other`; `acceptance` -> `unpassable-check`; `coverage` -> `missing-requirement`; `contradiction` -> `contradiction`; `risk` -> `safety` or `other`; `deviation` -> `other` with `deviation_class` set. Severity: `blocking` -> MAJOR or CRITICAL with `blocking: true`; `minor` -> MINOR.

**Calibration is not carried in the block.** The calibrator appends the existing `calibration:` block to the card, exactly as today (recorded card: `calibrator_model_class`, five `dimensions`, `C`, and `per_finding` entries with `finding_confidence` and `reason`, stoprule `reviewer-1-card.yaml:82-103`). The findings-v2 block does not carry calibrated confidence; reflect joins `calibration.per_finding[id]` to findings by (reviewer_id, finding id). A reviewer line that sets `calibrated_confidence` is rejected. The evidence validator's results stay where Wave 5 writes them today. The ledger carries no calibration (`ledger.py:86-90`), so the card is the only carrier. (The earlier findings-only sidecar files `panel/calibration.json` and `panel/validation.json` are not part of this design: today's card is mutated by the calibrator, and a sidecar would leave the debate's calibrated-card input without calibration.)

**How reflect card content and panel findings coexist.** The reflect card stays a document. Its prose sections and the persona's narrative are what the debate reads and what the report quotes. The `findings-v2` block is the machine part.

### What a recorded card looks like

<!-- Source: Variant 2 (sonnet:analyzer), Candidate B/C reasons 2 - merged per Change #10 -->
Findings in the recorded stoprule card are YAML with `severity: blocking|minor`, categories `ordering|acceptance|deviation|coverage|risk`, `evidence: [plan:57, source.md:62, src/...:451-462]` (line refs, no quotes), an orchestrator-written `model_class: sonnet`, and `plan:`/`spec:` paths. Conversion rule for recorded cards (deterministic, no quote): `plan:N` -> `(plan, <card plan path>, N, N)`; `source.md:N` or `spec:N` -> `(spec, <card spec path>, N, N)`; `path:A-B` -> `(source, path, A, B)`; unresolvable refs stay as `unresolved` citations and are counted. **Lossless conversion is not claimed**: Stage 0a reports the share converted unambiguously, with a gate of at least 90% before the parser change ships (O-7). `quote-not-found` is advisory only. In the post audit bundle, each grounding hunk is an H3 `path:start-end` heading in the reviewer's brief (the shape reviewers already receive, `reviewer-spec.md:45`); it is a per-source layout inside the brief, never a concatenated document that identities are computed against.

### Completion and channel

<!-- Source: Variant 3 (haiku:backend), Finding format (completion, channel) - merged per Change #2 -->
**Completion states** (per reviewer attempt, recorded in the manifest): `complete`, `truncated`, `invalid` (no parsable findings-v2 block or schema failure), `failed` (transport), `timed_out`. Only `complete` with a valid block counts toward quorum. A valid empty findings array is `complete` only when the card also carries its coverage observations for every assigned row; otherwise it is `invalid`, never "clean". The N=2 floor of `SKILL.md:600` counts `complete` reviewers of distinct classes (see "Guards and counts"). **Channel** (optional v2 field, default `defect`): `defect | grounding-gap | advisory`. An `advisory` finding is never counted in `deviation_count_by_class` and never maps to Regression (advisory no-spec gaps must never become Regression, `agents/reflect-reviewer.md:30`). Optional fields; v1 lines stay valid. A ledger-level hole (a reviewer with an empty valid block counted as clean) is already closed by `ledger.py:150-157`.

### Multi-file identity (K4 `cluster_v2`)

<!-- Source: Base (original, modified) - dedupe key replaced per Change #25 (INV-015); Variant 3 (haiku:backend) separate-documents -->
Verified problems in today's code: the ledger row stores a bare `span` list with no path (`ledger.py:196-197`) and each round one `doc_sha256` (`:278-279`); `merge_cmd` takes a single `--doc` (`merge_cmd.py:29-34`), so concatenating documents erases identity; `findings._spans` returns spans without a path and `same_defect` compares any two spans within 3 lines (`findings.py:363-379`), so two findings at line 10 of different files merge; clustering is transitive (`findings.py:382-407`).

**Multi-file identity (PROPOSED K4 `cluster_v2`).** Reflect does not use `review merge` or the ledger in Stages 0-4 (the merge is the debate), so no path-blind row exists. K4 is a pure function `cluster_v2(findings_v2_blocks, snapshot_file_list) -> clusters` exposed as `superclaude review cluster` (PROPOSED), writing `<out>/panel/clusters.json`.

1. **Citation tuple.** Each citation is `(role, path, line_start, line_end)` with `path` repo-relative and verified against `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), whose `file_list` gives each file's sha256. A citation whose path is not in the snapshot file list is `unresolved` and never joins a cluster by span. Spans are 1-based inclusive line ranges taken from the citation itself (no `locate` call needed; `quote` is optional).
2. **Primary citation** = the first citation whose `role` is the reviewed artifact (`plan` in pre; `source` or `diff` in post), else the first citation.
3. **`same_defect_v2(a, b)`** is true only if (i) deviation classes are compatible (equal, or either null or `none`), **and** (ii) the `refs_norm` sets intersect or are both empty (same normalization as `findings.py:321-337`), **and** (iii) some citation of `a` and some citation of `b` have the **same `path`** and spans within 3 lines (`a.start <= b.end + 3 and b.start <= a.end + 3`, the tolerance of `findings.py:377`). Equal fingerprints (`sha256("v2|" + role + "|" + path + "|" + section + "|" + refs + "|" + class)`) with non-empty refs also match, as in `findings.py:371-372`. **Two findings that cite different paths never match by span.** Two findings that cite the same spec requirement from different plan tasks match only through a shared `spec` path span plus a shared requirement ref.
4. **Transitivity guard.** Clusters are union-find components (as `findings.py:382-407`); each cluster is marked `chained: true` when it contains two members that do not match pairwise. `chained` clusters list their members and are never treated as one issue for counting.
5. **Per-source identity.** The brief carries each source as its own H3 `path:start-end` hunk (`reviewer-spec.md:45`); there is no concatenated review document and no `review-doc.md`.
6. **Tests (Stage 0 exit, positive and negative):** two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines and equal refs do cluster; a three-member chain A-B-C with A and C pairwise unequal is `chained`; v1 reports through the unchanged `review merge` produce byte-identical output with and without the new module imported.
7. **If the ledger is used later** (not planned), rows need `citations[]` (path-aware) and a `ledger/2` schema; that is a separate change, recorded as O-5.

### `cluster_agreement` and clustering semantics

<!-- Source: Base (original, modified) - panel_agreement_score replaced per Change #32 (INV-014, 018, 019, 021) -->
**`cluster_agreement` (telemetry only; the name `panel_agreement_score` is not used).** For each cluster c, `support(c)` = sum of the calibrated confidences (`calibration.per_finding[id].finding_confidence` joined from each member's card) of the distinct reviewers in c divided by the sum of calibrated confidences of all `complete` reviewers; `cluster_agreement` = mean support over blocking clusters, or 1.0 when none and at least 2 valid blocks. A cluster is **disputed** when support < 0.5, members disagree on `blocking`, or disagree on a non-null `deviation_class`. **Owner of a cluster's score:** the cluster carries the list of member calibrated scores, no scalar; its representative claim text and `blocking_any`/`blocking_all` come from the member with the highest calibrated confidence (ties: resolution order), not from the first reviewer (a ledger copies claim, anchor and category from the first member and ORs blocking before any validator drop, `ledger.py:182-199`). **Order:** clusters are computed on raw cards for telemetry; a second pass `clusters_kept` recomputes over findings the evidence validator kept, and only `clusters_kept` is used in measurements; the raw `overlap` label never routes anything. **Chaining:** `chained` clusters are excluded from agreement counts and listed. **Names:** stable field `adversarial_convergence_score`; prose name `convergence_score` (`SKILL.md:663,1483`); telemetry `cluster_agreement`. No other score name is introduced. `cluster_agreement` is never compared with the convergence thresholds and never routes anything.

### Evidence gate and citation pre-check

<!-- Source: Base (original, modified) - pre-check semantics replaced per Change #31 (INV-012, INV-013) -->
**The deterministic pre-check never drops a citation.** `superclaude review verify-citations` (PROPOSED, 0 model tokens) writes `panel/precheck.json` with, per citation, `missing-file`, `out-of-range`, or `quote-not-found` (advisory; a failed locate is not proof of an unfounded citation). Every flagged citation is added to the evidence-validator's re-read set even when the sampling policy (`SKILL.md:1204-1208`) would have skipped it. The validator alone decides drops, so `citations_dropped` keeps its sample-count meaning (`SKILL.md:1210-1214`: the count among the re-read sample; gate 6a requires 0 and trigger 13 degrades on any value above 0, `contract.py:347-352`) and gate 6a and trigger 13 are unchanged. Grounding is at least as strong as today because flagged citations are always re-read. A pre-check that dropped citations over every citation would change the field from a sample count to a mixed count and tighten a gate, a semantic change (major, `SKILL.md:953`); that variant is not adopted.

**Headless gap** (`ensemble.py:808-819`, `citations_dropped: 0`, `verification_ran: False`): a Stage 5 work item runs the same pre-check headless and reports the validator-confirmed count; this moves the field toward its documented meaning, can newly trip trigger 13, and is announced at Stage 5 entry as a behavior change, not a contract version event.

**Thresholds:** no change to either. Pre runs route by `SKILL.md:655` (>=0.75 PASS, >=0.60 PARTIAL); the wrapper's 0.80 line (`contract.py:317-326`) applies to post contracts only; the first measurement reports both bands per run so the owner can see how many pre runs would degrade under 0.80 (one recorded pre run scored 0.76, inside that gap).

## Adapter sketches

### Execution contract (both adapters)

<!-- Source: Variant 3 (haiku:backend), Adapter sketches final block ("Operational execution contract, both adapters") - merged per Change #1; additions per Change #29 -->
**Execution contract (both adapters).** A coordinator-owned manifest `<output>/panel/manifest.json` (PROPOSED) carries run state `frozen -> resolved -> dispatched -> collected -> calibrated -> clustered -> debated -> validated -> published`, plus terminal `failed`. One coordinator writes it; reviewer agents only return data. `frozen` records the reference to `<output>/artifacts/input-snapshot.yaml` and its `input_tree_sha256` (the existing multi-file hash, `SKILL.md:217-229`), the template sha256, tiers sha256, brief-template sha256, schema ids, `run_id`. Each later state records the hashes of the outputs it committed. **Idempotency identity:** `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`. A repeated submission with the same payload hash is a no-op; a different payload under the same identity is rejected. An attempt supersedes an earlier failed attempt of the same reviewer but never adds a vote and never clears a finding. **Resume:** reuse a completed stage only when all its dependency hashes still match; a changed plan or spec hash starts a new invocation. **Publish:** write `REPORT.md`, `return-contract.yaml` and `audit.log` to same-directory temporaries, rename them, then commit `published` in the manifest; a reader accepts only a committed manifest (a non-atomic pair is a real risk: `merge_cmd.py:113-116` writes the report before saving the ledger). One total deadline across stages (the ensemble already captures a shared deadline before dispatch, `ensemble.py` per V3, UNVERIFIED line); failed attempts never restart the whole panel.

State variables (INV-001, INV-002, INV-003): (1) `@reflect-*` templates use only `fixed` and `random` strategies; reflect-profile validation rejects `round_robin` unless `--sequence` is supplied and recorded in the manifest (round_robin slots seed from `date.today().toordinal()` when no `sequence` is passed, `panel.py:471-476`, so a resume after midnight re-resolves; random slots hash `run_id`, `:455-459`, and are stable). (2) The plan and spec (and every grounding file) are covered by the existing `input_tree_sha256` and per-file sha256 list of `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), re-read and recomputed before Wave 5 and before promotion (`SKILL.md:227`); the manifest references that file by hash; no single-document hash is used and `doc_sha256` of the ledger is not relied on. (3) Reflect uses no ledger in Stages 0-4. If a ledger is ever used, each merge attempt writes to its own path `<out>/panel/attempt-<n>/ledger.json` and `merged.md`, and only the attempt named by the committed manifest is read (`ledger.py:114-118` refuses a re-merge of round 1).

### Pre-execution adapter (agent-session engine)

<!-- Source: Base (original, modified) - steps 1-12 replaced per Change #44; Variant 3 (haiku:backend) pre steps 1, 7, 8 and input-drift recheck; Variant 2 (sonnet:analyzer) step 8 -->
Inputs: `--spec`, `--tasklist`, `--executor-model` (optional), PROPOSED `--t2-engine legacy|shadow|panel` (default `legacy`).

1. **Wave 0 and Waves 1-2 unchanged**: alias resolution, executor class (`SKILL.md:600-602`), budget pre-flight, grounding, coverage map (two-pass extraction), T1 card, blind calibration of the T1 card, rubric. If the final tier is 1 the adapter never runs and `--t2-engine` is not read (rules D1, D2 of "When the panel is called").
2. **Engine decision.** `t2_engine_effective = requested` only if the final tier is 2 and the environment gate holds (Stage 3 entry); else `legacy` with `panel_fallback_reason`. Write both into `tier_decision.yaml`.
3. **Freeze** (manifest `frozen`, see "Execution contract"): reference `artifacts/input-snapshot.yaml` by hash, pin template, tiers and brief-template hashes.
4. **Resolve**: `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct` (`--template`, `--run-id`, `--kind`, `--env` exist, `panel_cmd.py:18-52`; the last two flags are PROPOSED; `--exclude-class` does not exist). On `ExclusionExhausted` for the anchor, re-resolve with `@reflect-pre-x2`; assert the invariants of K1 contract item 6; write `<out>/panel/resolution.json`. Below the floor: rule D3 or the `SKILL.md:600` degrade.
5. **Briefs**: exactly three sections (`reviewer-spec.md:31-74`), persona by resolution order (analyzer, qa, refactorer), qa gets the spec body (`:55`). One added instruction line inside the T1-card section: "End your card with a `## Findings block` fenced `findings-v2` block, `lens: reflect-pre`, citations with roles `plan` and `spec`." Not a fourth section.
6. **Dispatch**: parallel Agent calls to `reflect-reviewer` with the explicit `model` of the Agent-session adapter rule, cards to `<out>/reviewer-cards/reviewer-<n>-card.md` (or `.yaml` as today). Attempts and completion states go to the manifest (see "Completion and channel").
7. **Normalize**: parse each card's findings-v2 block (convert line refs, see "What a recorded card looks like"); an invalid block gets one bounded re-ask for the block only; the card body still reaches the debate.
8. **Blind calibration** (unchanged mechanism, `SKILL.md:1192`): one `confidence-calibrator` per card, class chosen by `SKILL.md:1181-1186`, result embedded in the card as the existing `calibration:` block.
9. **K4 clustering and pre-check (telemetry and flagging only)**: `superclaude review cluster` writes `panel/clusters.json`; `superclaude review verify-citations` writes `panel/precheck.json`; neither drops anything and neither feeds the debate.
10. **Debate (unchanged)**: `Skill sc-adversarial-protocol --compare <calibrated cards> --depth standard --focus correctness,coverage,deviation-classification --output <out>/adversarial/` (`SKILL.md:645-651`; under `--unattended`, `SKILL.md:653`). Remap `artifacts_dir` to `adversarial_artifacts_dir` (`:657`). Record judge identity and collisions (see Q3). The debate input is unchanged (the calibrated cards, not the cluster table), so clustering cannot change whether sc-adversarial considers the variants "substantially identical". If the child returns a null score without `adversarial_unavailable`, the adapter keeps the real null (no synthetic 1.0), sets `debate_skipped_similar: true` in telemetry when the child's log says so, and the existing null routing applies (`SKILL.md:659-664`). EV-1 is unchanged (`:666`): `merged-verdict.yaml` with `merge_method: adversarial` plus at least the resolved `--reviewers` count of calibrated cards, or a corroborated F2/F3 fallback; the count it compares is the resolved reviewer count after exclusion (the manifest records requested, resolved and complete counts separately).
11. **Wave 5 synthesis and evidence-validator (unchanged, mandatory, `SKILL.md:587`)** with the pre-check flags added to the re-read set (see "Evidence gate and citation pre-check"); recompute `input_tree_sha256` before synthesis (`:227`).
12. **Publish** atomically (see "Execution contract") and emit contract 1.8.0 by the legacy rules; lint (see "Contract compatibility gate") in tests.

**Shadow mode** (`--t2-engine shadow`): steps 4-9 run with the legacy rotation expressed as the resolution (identical reviewers); the assertion "panel resolution == legacy rotation" is recorded; the debate result is authoritative; panel artifacts and telemetry are written for the measurement.

### Post-execution adapter (Stage 5; both engines)

<!-- Source: Base (original, modified) - steps 1-10 replaced per Change #44, #35 -->
Inputs: `--spec`, `--tasklist`, `--task-log`, `--diff`, `--executor-model`, `--t2-engine`.

1. Waves 0-2 unchanged, including the §6.1 verification run by the orchestrator (reviewers never execute, `reflect-reviewer.md` Safety Constraint; refs/reviewer-spec.md:14).
2. Resolve with `@reflect-post` (same slots; `@reflect-post-x2` for anchor replacement) and the executor class hard-excluded and strict distinctness; this matters most here (self-confirmation, `SKILL.md:600`).
3. Briefs unchanged; each grounding hunk is an H3 `path:start-end` (`reviewer-spec.md:45`); the qa ordinal gets the verification and runtime-surface hunks (`reviewer-spec.md:53,57`); `lens: reflect-post`, `deviation_class` required; no-spec gaps use `channel: advisory`.
4. Dispatch: agent-session as pre; headless `superclaude reflect` -> ensemble -> swarm `reflect-review` lens, unchanged in Stage 5 except that it may read the K1 resolution through a PROPOSED `--panel-resolution` input with `T2Model0N` as the fallback. The bounded fallback ladder stays (cli/reflect/fallback.py, body UNVERIFIED).
5. Blind calibration per card (embedded); pre-check flags; evidence-validator (unchanged).
6. K4 clustering to `panel/clusters.json` (telemetry).
7. **Debate (kept)**: `Skill sc-adversarial-protocol --compare <calibrated cards>` exactly as `SKILL.md:645-651`. The K4 cluster map is written to `panel/clusters.json` for the Stage 5 post measurement; it is not an input to the debate until that measurement shows an effect (O-3). Replacing or narrowing the post debate needs its own post trial with seeded deviations and class accuracy. Writes `adversarial/merged-verdict.yaml`.
8. Contract: `merge_method: adversarial`, the child's score; 1.8.0 semantics unchanged. Promotion, remediation and the `reflect_post` write-back are unchanged.

## Staged migration

<!-- Source: Base (original, modified) - rows replaced per Change #43, #36 -->
Pre-execution ships behind an off-by-default flag first: `--t2-engine` defaults to `legacy` in every stage until Stage 4.

| Stage | What ships | Entry | Exit | Rollback |
|---|---|---|---|---|
| **0. Measure offline** | findings-v2 schema and parser, card converter, `cluster_v2`, Stage 0a replay on the recorded cards, consumer inventory and the lint test design | design accepted | 50-pair hand-labelled cluster check; conversion share >= 90% (see "What a recorded card looks like"); consumer grep result stored (see "Contract compatibility gate"); pilot designed and costed | delete the code; nothing consumes it |
| **1. Kernel extensions, dormant** | K1 `classes`, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, Fable and tier0 rejection, `@reflect-pre`, `-x2`, `-enterprise`, `-lite`; `review cluster`; `verify-citations` | Stage 0 exit | the K1 contract item 8 tests; spec-panel byte-identity (default and live7 templates); template validity; spike S-ID run (see "Executor-exclusion gates") | revert the commits; new parameters default off |
| **2. Pre shadow** (`--t2-engine shadow`, default `legacy`, read only after the final tier) | the panel resolution is written next to the legacy rotation and asserted identical (parity), findings-v2 block instruction in the brief, clusters, pre-check, manifest; legacy debate authoritative; contract 1.8.0 | Stage 1 exit; contract compatibility gate passed | 20 shadow runs: zero MALFORMED, EV-1 failure rate no higher than legacy, parity assertion holds, lint and verdict replay pass | flag default is `legacy`; delete `<out>/panel/` |
| **3. Pre panel opt-in** (`--t2-engine panel`) | reviewers chosen by the template; debate on cards authoritative; contract 1.8.0 | **first measurement passed (H-B, H-C, safety)** and the environment gate: Stage 3 and later run only in an environment whose resolved models all have a non-null `launch` alias (today: anthropic-only); Haiku-stand-in runs certify mechanics and anthropic-only behavior, not gateway quality; a gateway default needs its own run of the first measurement (not planned; O-4) | 30 opt-in workflow runs: `reflect_status` distribution no worse than shadow, zero MALFORMED, median tokens <= 1.05 x legacy | flag to `legacy` |
| **4. Pre default** | sc-workflow's Wave 4 gets `panel` by default | Stage 3 exit plus owner sign-off | two release cycles with no rise in workflow `reflect_status: failed` | one-line default change |
| **5. Post panel dispatch** | post adapter: K1/K2/K3, K4 telemetry, debate kept; headless `citations_dropped` made real with the `ensemble.py:772` distinct-model check | Stage 4 exit; a separate post measurement (seeded deviations, class accuracy) | wrapper verdict distribution on >= 20 paired post runs: no new `degraded` or `halted` reason from dispatch alone | flag to legacy rotation |
| **6. Deferred candidate E'** | deterministic pre merge, `merge_method` value `panel`, contract 2.0.0 | a measurement that the debate adds nothing plus every consumer in "Deferred versioned change" updated | not planned | not planned |

## Return-contract 1.8.0 mapping

<!-- Source: Variant 3 (haiku:backend), "Return-contract 1.8.0 mapping" (adopted table) - merged per Change #15; Base (original, modified) - consumer list kept and moved to the deferred path; corrected per Change #14, #16 -->
**Producers and the wrapper.** Two producers exist: the interactive skill (1.8.0, pre and post) and the headless ensemble builder (`ensemble.py:788`, constant `REFLECT_CONTRACT_VERSION = "1.0"` at `ensemble.py:74`, post only: `"mode": "post"` at `:797`). Recorded interactive pre contracts say `contract_version: "1.8.0"` (37 of 62 under `.dev/reflect/pre-*`; others 1.0, 1.2.0, 1.3.0, 1.5.0, 1.7.0). The wrapper accepts any major `1` and BLOCKS any other major (`contract.py:187-194`, `unknown-major-version`; fixture `tests/cli/reflect/fixtures/blocked_unknown_major.yaml`), then applies degraded/halted triggers 1-14. No change to any of these is needed while the contract stays 1.8.0. Any future major version must first change `contract.py:187-194`. The only other `contract_version` equality in `src/` is `sc-implement-protocol/scripts/archive_workspace.py:327` (`!= "1.1"`), a different contract.

**Versioning plan.** Stages 0-4 change no stable field: `contract_version` stays `1.8.0` for interactive runs; no field is added to the stable block; panel data lives in referenced artifacts (`<out>/panel/*`) and in the non-stable telemetry block (`SKILL.md` two-block contract). **Bump rule (applies to every later proposal):** a new top-level stable field = minor (`SKILL.md:952`); a new legal value of an existing field, a changed meaning, a gate-text change = major (`SKILL.md:953`); a new telemetry-only field = no bump. A contract lint test (see "Contract compatibility gate") enforces this on panel runs. `merge_method` stays in `{adversarial, single-reviewer-fallback}` (`SKILL.md:789`, EV-2; EV-1 at `SKILL.md:666` requires `merged-verdict.yaml` with `merge_method: adversarial`).

| Contract field or family | Source in the panel path | Status |
|---|---|---|
| `contract_version` | constant `1.8.0` (interactive builder); headless builder constant `"1.0"` untouched | unchanged |
| `status`, `mode`, `tier_reached` | existing reduction; `tier_reached` is 2 only when the N=2 floor of distinct `complete` classes holds | unchanged meaning |
| `merge_method` | `adversarial` from the real `sc-adversarial` run; `single-reviewer-fallback` via the F2 path | unchanged legal set |
| `adversarial_convergence_score` | the child's `convergence_score` or null; never synthesized | unchanged |
| `adversarial_unavailable`, `adversarial_artifacts_dir` | F3 path as today; mechanical remap `artifacts_dir` -> `adversarial_artifacts_dir` (`SKILL.md:657`) | unchanged |
| `reviewer_cards` | calibrated card paths (cards carry the findings-v2 block and the embedded `calibration:`) | unchanged |
| `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `calibrator_diversity` | computed with the same rules as the legacy path from the resolved classes (parity template, see "Template set") | unchanged semantics; values asserted equal on matching inputs by the lint test |
| `citations_total/revalidated/dropped`, `evidence_validator_ran` | validator results; pre-check only flags | unchanged semantics |
| coverage, deviation, verification, reachability, promotion, remediation fields | reflect waves | unchanged |
| `panel_*`, `cluster_agreement`, `manifest_path`, `t2_engine_requested/effective`, `identity_source` | telemetry block / artifacts | non-stable, no bump |

**Null-score rules.** Route on `merge_method` first (`SKILL.md:661`). `adversarial_convergence_score` is a real child score or null; null enters only on the F3 path, a skipped debate or a failed child; no synthetic 0, 0.5 or 1.0. A null at T2 stays `status: partial` and blocks promotion (`SKILL.md:659-664`; wrapper trigger 11 `contract.py:299-300`). `cluster_agreement` is never compared with the convergence thresholds and never routes anything. In `sc-adversarial-protocol/SKILL.md`, variants differing by under 10% skip the debate (`:407-410`, `:948-951`) and `convergence_score` is "null if debate not reached" (`:439,457`); a unanimous clean run can therefore return null today, which the wrapper degrades at T2 and promotion blocks (`SKILL.md:663`). Recorded pre contracts include 7 null scores; their cause (skipped debate versus F2/F3) is UNVERIFIED. Stage 0a classifies the 7 recorded nulls by cause; if skipped-similar is a frequent cause, a separate decision (not this design) is needed on whether a skipped debate should return a score.

**Recorded convergence evidence.** Recorded pre contracts under `.dev/reflect/` show a convergence score of 1.0 in 21 of 35 numeric cases and below 1.0 in 14 (0.40 to 0.9615); 7 T2-reached contracts have a null score (2 `single-reviewer-fallback`, 3 illegal values such as `none` and `inline-orchestrator`, 1 `adversarial` with a null score, 1 `sc-adversarial-protocol-mode-a`); 5 `single-reviewer-fallback` contracts exist in all. These are agreement observations, not defect-recall measurements, and vendor diversity was single in the recorded T2 runs the enrichment cites. They do not show the debate is idle. The debate stays advisory in pre.

**Promotion gate condition 9 (`SKILL.md:1483`).** Unchanged in every planned stage: the retained debate keeps a real merged adversarial verdict on every T2 run. The condition's operative test is `tier_reached == 2 AND adversarial_unavailable == true` (blocked), and its `convergence_score` is the prose name of `adversarial_convergence_score`; both stay as written. Promotion is UC-2 only (`promotion_gate_passed` is null when `mode == pre`, `SKILL.md:837`).

**`reflect_post` frontmatter** (`cli/reflect/runner.py:103-133`): unchanged in every stage. Fields are verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at and the three `*_verified` booleans, in a fixed order; no merge field. The wrapper writes it for post runs on a tasklist only; the pre adapter never writes it. Do not add panel fields to it.

**Consumer by consumer** (each: no change while the contract stays 1.8.0).

- **sc-workflow Wave 4** reads `reflect_status` and `reflect_report_path` only (`sc-workflow-protocol/SKILL.md:60`): no change.
- **Wrapper verdict map** (cli/reflect/contract.py): triggers 10, 11 and 11b read `merge_method` and the convergence score exactly as before: no change.
- **Headless ensemble contract builder** (`ensemble.py:772-773`): post-only, no change in Stages 0-4; Stage 5 makes `citations_dropped` real (announced behavior change).
- **Sprint executor TurnLedger** (`SKILL.md:930`) reads `status` and `per_task_verdicts`: post-only, unchanged (executor code UNVERIFIED).
- **sc-troubleshoot, sc-task, task-builder, sc-workflow T3 handoff** (`SKILL.md:929, 931, 937-938`) read no merge fields; `task-builder` EV-4 (line 2242) requires `merge_method: adversarial` on disk for post, which still holds.
- **sc:roadmap, sc:tasklist gates** (`SKILL.md:932-933`) read coverage fields: no change.
- **Wave 7 promotion** (`SKILL.md:939`): post-only, see condition 9.
- **CI grader** (`make reflect-eval`, `SKILL.md:940`): `.dev/eval-workspaces/sc-reflect/grader.py` has no match for `merge_method`, `contract_version` or `convergence` (grep), so it needs no change today.
- **Meta-eval aggregator** (`SKILL.md:941`) reads `convergence_score`: no change.
- **Reflect SKILL.md** EV-1 (`:666`) and EV-2 (`:789`): no change (installed as `~/.claude/skills/sc-reflect-protocol/SKILL.md`).

### Deferred versioned change (candidate E', not scheduled)

A deterministic authoritative merge in pre would add `merge_method` value `panel` (pre only), which is a major version, `2.0.0`. Every consumer that must change first: (1) `contract.py:187-194` major gate; (2) `contract.py:295-300,317-326` triggers 10, 11, 11b (guard on `merge_method`; trigger 11 would mis-fire on a null score from a panel merge); (3) `ensemble.py:74,772-773,788,806` builder constant and merge-method derivation; (4) reflect `SKILL.md` EV-1 (`:666`), EV-2 (`:789`), the §9.4 note, and promotion condition 9 text (`:1483`); (5) `task-builder` SKILL.md EV-4 (line 2242: requires `merge_method: adversarial` on disk for post); (6) `refs/ops-integration.md:239` (`adversarial.merge_method` PromQL label values); (7) the meta-eval aggregator that reads `convergence_score` (`SKILL.md:941`); (8) the sprint executor routing named at `SKILL.md:664` and `:930` (executor code UNVERIFIED); (9) `tests/cli/reflect` (25 fixture files carry `merge_method`; `test_ensemble_unit.py`, `test_ensemble_stub_integration.py`, `test_verdict_mapping.py`, `test_contract_fallback_metadata.py`); (10) `sc-workflow` Wave 4 reads only `reflect_status` and `reflect_report_path` (`sc-workflow-protocol/SKILL.md:60`), no change. The CI grader has no match (above), so it needs no change today.

### Contract compatibility gate

<!-- Source: Base (original, modified) - new subsection merged per Change #27 (INV-023) -->
The wrapper's triggers 6-14 read fields (`contract.py:277-356`) and the interactive pre path assembles the same fields by prose, not code; `SKILL.md:923-940` (the §9.3 consumer map) does not list the wrapper or the headless builder at all. Grep inventory at plan time (counts, not proof of completeness): `merge_method|adversarial_convergence_score|convergence_score` appears in `cli/reflect/contract.py` (3), `cli/reflect/ensemble.py` (22), `contracts/__init__.py` (1), `tests/cli/reflect/*` (fixtures: 25 files; `test_ensemble_unit.py` 23, `test_ensemble_stub_integration.py` 16, `test_verdict_mapping.py` 5), `task-builder` SKILL.md (4, EV-4 at `:2242`), reflect `SKILL.md` (25), `refs/ops-integration.md:239`; roadmap files match the same words for the roadmap pipeline's own merge (different contract).

**Contract compatibility gate (PROPOSED, a hard stage-entry criterion for Stages 2, 3, 4 and 5; the Stage 2 entry needs items 1-3, its exit adds item 4).**

1. **Inventory.** Re-run a repository-wide grep for `merge_method`, `adversarial_convergence_score`, `convergence_score`, `contract_version`, `t2_model_class_diversity`, `t2_vendor_diversity`, `calibrator_diversity`, `reviewer_cards`, `citations_dropped` over `src/`, `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/` and the installed skill and command primitives. **Producers:** the interactive skill prose (`SKILL.md` §9.1 and Wave 5, plus `refs/report-template.md`, UNVERIFIED), the headless builder (`ensemble.py:787-832`). **Validators:** `contract.py` (`derive_verdict`, `contract.py:138`; `_degraded_reason`, `:263`). **Consumers:** the §9.3 map plus `task-builder` EV-4, the PromQL label list, the meta-eval aggregator, the sprint executor (UNVERIFIED code). The result is stored as `.dev/` evidence and attached to the stage's exit record.
2. **Per-field source table** for the five fields whose producer changes in panel mode (the diversity trio, `calibrator_diversity`, `reviewer_cards`): each is computed by the same rule as the legacy path from the resolved classes; for the parity template in anthropic-only the expected values equal the legacy values (sonnet, haiku, opus: three distinct classes, vendor `single`, calibrator `degraded`).
3. **Contract lint test** (PROPOSED `tests/cli/reflect/test_panel_contract_lint.py`; the reflect tests already live in that directory): feeds a panel-run contract and its output directory to a checker that asserts: `contract_version == "1.8.0"`; every top-level key is in the 1.8.0 stable field list or in the telemetry block; `merge_method` in `{adversarial, single-reviewer-fallback}`; `adversarial_convergence_score` is a float or null; `adversarial_unavailable`, `regression_present` and the other `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`) are real booleans; EV-1 holds on disk (`merged-verdict.yaml`, cards count); the five fields above equal the legacy values on the matched fixture.
4. **Verdict replay.** Feed every recorded 1.8.0 pre contract and the Stage 2 shadow contracts through `derive_verdict` (`contract.py:138`) offline and diff the verdicts between legacy and shadow outputs; any new degraded reason is a stage-exit failure. (The wrapper is post-only in production; this replay is a test, not a runtime path.)
5. **Bump rule check:** the lint fails if a panel run emits a stable key outside the list or a legal value outside EV-2; that is the machine form of "no change".

## Cost model

<!-- Source: Variant 3 (haiku:backend), Cost model - merged per Change #4; Base (original, modified) - 49k-96k estimate demoted to a footnote -->
Three separated bases, never summed. All token figures are estimates and are labelled with their unit.

1. **Published profile (claude-orchestration tokens, turn-budget unit).** T1 3k-8k plus 2k-5k auggie; T2 35k-70k plus 10k-25k auggie; hard kill about 65k (`cost-profile.yaml:36-39,46-51,70`; "1 turn ≈ 1k claude tokens", turn midpoint 52, 52 x 1.25 = 65, or 65.6k from the 52.5k arithmetic midpoint; `SKILL.md:269-270`: N >= 65 means no constraint). The panel does not change `cost_profile_version`.
2. **Output-token planning estimate for a T2 run reaching T2 (3 reviewers), lane by lane** (V3's table, adopted as the planning basis, in k output tokens):

   | Lane | Legacy | Panel-parity, debate kept (legacy lanes plus the findings block) |
   |---|---|---|
   | primary (T1 card, coverage map, briefs, REPORT) | 10-16 | 10-16 |
   | parallel (3 reviewer cards) | 21-30 | 22-31 |
   | calibrator (3 per-card re-grades, 1k-2k each) | 3-6 | 3-6 |
   | debate (`/sc:adversarial --compare`) | 6-10 | 6-10 |
   | validator | 2-4 | 2-4 |
   | **total** | **42-66** (`10+21+3+6+2` to `16+30+6+10+4`) | **43-67** (`10+22+3+6+2` to `16+31+6+10+4`; 43.5-67.5 before rounding) |

   Midpoint 54k to about 55.5k: parity costs about 1.5k more, not less. The earlier lane-table saving (37k-56k, about 14%) came from an assumed shorter-card effect that this design does not contain and no data supports; it is kept only as the unproven arm-C hypothesis that the first measurement may test (H-C reports it, does not require it). <!-- fix B1 -->
3. **Recorded artifact sizes (bytes/4)** 55k-93k (221,405-371,507 bytes) are a sanity bracket only; they include copied input and are not provider usage.

V1's earlier 49k-96k legacy estimate is kept as a footnote: its high end exceeds both the profile's 70k band top and the 65k kill line, so it is not used for any threshold. PN1 figures (408k loop, 23k + 3 x 68k-108k first review, `LEDGER-RESULTS.md:19,66`) stay a comparison only: the default 4-slot panel in anthropic-only with spec-panel-style verbosity would cost about 227k-347k for the parallel lane alone (23 + 204 to 23 + 324), 4-7x the whole current T2 run (reflect briefs are persona-scoped, so reflect cards should be shorter, UNVERIFIED for Haiku stand-ins).

Deterministic-merge variant (deferred candidate E'): corrected parity total 43-67 minus the debate lane 6-10 = 33k-61k, not production behavior. <!-- fix B1 item 4, M7 -->

**Rule:** panel T2 must stay inside the existing 35k-70k profile band and below the 65k kill line at p95 (a measurement criterion, see First measurement). **Post (Stage 5):** the debate is kept, so the cost is about the same as legacy (+1.5k for blocks, +0 for K4). The value is maintenance and an honest headless `citations_dropped`, not tokens.

**When a full panel (more than 3 slots) is not worth calling:** (1) always in anthropic-only: extra slots are more Haiku copies, they add no model class and leave vendor diversity single; (2) always in pre-execution: advisory, no revise step; (3) when the rubric would stop at T1 anyway (`SKILL.md:362-366`, rule D1): the kernel is never called. The only candidate case is gateway post-execution with extra *vendors*, unmeasured and left for Stage 5 data; raising the cap needs the gate in Q7.

## Risks

<!-- Source: Base (original, modified) - list replaced by a table per Change #21 -->
Probability is an estimate with its basis stated; impact is the consequence; mitigation names the design element.

| # | Risk | Prob. | Impact | Mitigation |
|---|---|---|---|---|
| 1 | The debate matters and clustering cannot replace it | n/a (debate kept) | Medium | kept; E' needs its own measurement and a major version |
| 2 | Panel-fed T2 is worse than legacy T2 | Medium: reviewer classes match (parity) but format, brief line and dispatch plumbing differ | High | Stage 2 shadow, first measurement NI test, legacy default |
| 3 | Executor exclusion fails open or empties the anchor | Medium: `panel.py:402-409` silent paths are real | High | kernel hard exclusion, per-slot skip, post-resolve assertion, tests (K1 contract) |
| 4 | Reviewer identity not what was requested | Low-Medium: the tool pins `model`, but omitting it runs Sonnet (`reflect-reviewer.md:6`) | High | explicit `model` check, probe spike S-ID |
| 5 | Format non-compliance (invalid findings block) | Medium for Haiku-class reviewers (card format varies today) | Medium | one bounded re-ask; legacy card body still reaches the debate; compliance rate in telemetry |
| 6 | Consumer or test relies on a 1.8.0 value that shifts | Low (grep shows no `contract_version == 1.8.0` check, no grader match) | High | lint test, consumer grep gate, parity |
| 7 | Multi-file clustering merges unrelated findings | Low (path-aware, conservative) / split risk Medium | Low: telemetry only | `cluster_v2`, 50-pair hand label at Stage 0 |
| 8 | Opus creep | Low: no new use | Medium | the Opus-use list; Fable and Tier 0 rejected in the kernel (`launch` whitelist) |
| 9 | Two engines drift again | Medium | Medium | one resolution file, one contract-lint, one builder function for post at Stage 5 |
| 10 | Pre T2 exceeds the 65k kill | Medium at the legacy high end | Medium | p95 criterion, cap of 3 reviewers |
| 11 | Interactive and wrapper disagree on a 2-of-3 run | High (exists today: `SKILL.md:666` calls it MALFORMED, `ensemble.py:765-770` records benign `reviewer-shortfall`) | Low-Medium | preserved, counted at Stage 2 |
| 12 | Gateway cell silently routed through an unsupported path | Low | High | refusal rule (Agent-session adapter, rule D4) |

## First measurement

<!-- Source: Base (original, modified) - replaced per Change #28 (INV-024); Variant 2 (sonnet:analyzer) three-arm design and sample-size section; Variant 3 (haiku:backend) hygiene -->
**Hypotheses and thresholds (one margin each).**

- **H-A (worth):** T2 recall beats T1 recall by at least **15 percentage points** on seeded defects (superiority). If not, record that the T2 spend does not buy recall on plans, and the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8). This is not an automatic veto of the migration, which is justified by maintenance as well.
- **H-B (non-inferiority):** panel-parity T2 recall is within **10 percentage points** of legacy T2 recall (one-sided 95% bound), and precision likewise. **The 5-point margin (V3) and the 15-point margin as an NI bound (V2) are dropped:** 5 points is not resolvable at feasible n (below), and 15 points is the H-A threshold, a different hypothesis.
- **H-C (cost):** median panel-T2 tokens <= 1.05 x legacy median and p95 <= 65k in the profile unit (see Cost model). A saving is reported, not required.
- **Safety (fails regardless of savings):** a forbidden model or executor-class collision dispatched when the executor is known; a MALFORMED contract; an unsupported citation certified; any repository write by a reviewer; a T1 or `--depth quick` run that calls the panel.

**Arms** (same plans, hidden arm identity for graders): A = T1 only (a `--tier 1` pin; flag semantics `SKILL.md:362`); B = legacy T2; C = panel-parity T2 (a development-build `--t2-engine panel`, or the `shadow` run with the parity assertion; the measurement runs on a development build and Stage 3 ships the same code to users; debate kept) <!-- fix M8 -->; D = panel-lite (the `@reflect-lite` template: sonnet, haiku, Opus calibrator; pilot subset only) to price the Opus-moves ablation.

**Ground truth.** Seeded defects (scripted, not derived from reviewer output; ordering, missing acceptance, spec-uncovered requirement, wrong file path, cross-task contradiction) plus a **union ledger** of natural findings from all arms scored by a blinded grader (the ledger circularity caveat `LEDGER-RESULTS.md:49` applies).

**Sample size (formula and numbers).** Paired by defect, with discordance d = share of defects found by exactly one arm. Standard error of the paired recall difference is about sqrt(d/n). One-sided 95% non-inferiority with 80% power at true difference 0 needs `n = d x (1.645 + 0.842)^2 / M^2 = 6.185 x d / M^2`. For M = 0.10: **n = 618 x d** defects (d = 0.10 -> 62; d = 0.20 -> 124; d = 0.30 -> 185). For H-A with M = 0.15: **n = 275 x d** (d = 0.35 -> 96). Multiply by 1.3 for clustering of defects within plans. At the pilot size of 60 defects the power is about 79% when d = 0.10 but only about 54% when d = 0.20 (SE 0.058, bound 0.095): the pilot therefore estimates d; it does not decide H-B.

**Phasing.** Pilot: 12 plan+spec pairs x 5 seeded defects = 60 defects, arms A, B, C (arm D on 6 of them), plus 6 repeats of arm B to estimate the within-arm noise discordance d0 (if d0 is at least 0.8 x d between arms, the arms are indistinguishable from noise). Confirmatory: `n_plans = ceil(1.3 x max(618 x d_BC, 275 x d_AB) / 5)` from the pilot's observed d; the owner approves the spend before it runs. Cost units are the profile's: per plan arms A+B+C = 3k-8k + 35k-70k + 35k-70k = 73k-148k claude tokens; pilot (12 plans) 0.9M-1.8M; a confirmatory run of 33 plans (d = 0.20) 2.4M-4.9M; arm D adds 6 x 35k-70k. Retrieval tokens are reported separately and not summed. Hygiene: blinded arm identity, a stop rule, and the pilot labelled as a pilot.

**Strata (required reporting).** Results are reported **split by `--depth` and by escalation path**, never only pooled: strata are (standard, escalated by the parsed-sparse pre-filter), (standard, escalated by rule 4, 5 or 6 without the pre-filter), (`--depth deep`), (`--tier 2` pin). Quota: at least 25% of plans whose source carries labelled requirement ids (non-sparse), because 34 of 38 recorded pre decisions were parsed-sparse (see "When the panel is called"); if not obtainable, the report states it measured sparse-labelled plans only. Each stratum reports n, recall, precision, tokens and a CI; a pooled headline is shown only if a heterogeneity check across strata is not significant.

**Stage 0a (zero dispatch, descriptive).** Convert the recorded cards (42 `reviewer-cards/` directories under `.dev/reflect/pre-*`, 33 with `adversarial/merged-verdict.yaml`) to findings-v2 (line refs to citations), run `cluster_v2`, report cluster counts and agreement with the recorded merged verdict; report the share of findings that convert with an unambiguous `(path, line)` (the gate: at least 90%). Unseeded, not a pass/fail input.

**Inconclusive is not a pass.** If the confirmatory interval crosses the margin, H-B is inconclusive and Stage 3 does not proceed; Stages 0-2 still ship.

## Open items

<!-- Source: Base (original, modified) - new section merged per Change #38 -->
- **O-1** (C-002, C-014; V3 holds its verdict/completion policy should be the base and prefers resolution-only first): resolved as V1 skeleton plus V3 policy; Stage 3 is the first stage that changes reviewers and it is effectively resolution-plus-format-only, so V3's concern is met without a separate stage; V3 dissent recorded.
- **O-2** (C-005, exact key versus primary-citation proximity): `cluster_v2` is telemetry only, so under-merging is cheap; revisit if clusters ever become authoritative.
- **O-3** (C-007): post debate input; the cluster map is not fed to the post debate in the first shipment (see Post-execution adapter, step 7).
- **O-4** gateway dispatch for pre and post and gateway templates (X-010, A-002): undefined; refused.
- **O-5** path-aware ledger (`ledger/2`) if a ledger is ever used.
- **O-6** unknown executor is the default in the workflow path (see K1 contract item 7): consider having `sc-workflow` Wave 4 pass `--executor-model` when known (a sc-workflow change, out of scope here).
- **O-7** A-003 conversion gate (at least 90% unambiguous conversion).
- **O-8** the cheaper lever may be the rubric: 34 of 38 recorded pre decisions escalated because of the parsed-sparse pre-filter, not plan risk; decide after H-A.
- **O-9** `_diversity.py:15` returns `insufficient` while `SKILL.md:790` allows only `full | degraded` (pre-existing vocabulary mismatch).
- **O-10** X-003 (contract-version facts): resolved as a text correction (see Return-contract mapping), no residual.
- **O-11** `--depth quick --tier 2` precedence and whether pins override the budget downgrade are not stated in the rows I read (UNVERIFIED).

## Assumptions and UNVERIFIED items

<!-- Source: Base (original, modified) - verified items moved and bullets replaced per Change #22, #36 -->
**Assumptions (from the seed brief):** A-1 (design, measure first is acceptable), A-2 (shared model = one schema, one dispatch, one merge layer), A-3 (pre cites plan and spec, post cites source; the quote-anchor part is decided: `quote` is optional), A-4 (calibrated confidence stays per finding/card, embedded in the card), A-5 (output tokens only; the profile unit is named wherever it is used), A-6 (no owner decision needed).

**Assumptions added here:**

- **A-8:** sc-workflow invokes reflect inside an agent session, so pre uses the agent-session engine (enrichment: skills/sc-workflow-protocol/SKILL.md:60-64).
- **A-9:** persona-scoped reflect cards stay far shorter than spec-panel reports. This drives the "full panel not worth it" estimate only as a lower bound.
- **A-10:** Haiku-stand-in runs certify mechanics and anthropic-only behavior, not gateway quality. Stage 3 and later run only where every resolved model has a non-null `launch` alias; a gateway default needs its own run of the first measurement (not planned; O-4).

**VERIFIED (moved from UNVERIFIED, with cites):**

- (a) `superclaude review panel resolve` options are `--template`, `--tiers`, `--env`, `--run-id`, `--kind first|re-review`, `--seed`, `--sequence` (`panel_cmd.py:18-52`); `--exclude-class` and `--strict-distinct` do not exist (PROPOSED).
- (b) `validate_panel` rejects unknown slot keys (`panel.py:109-111`, `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}` at `panel.py:46`), so exclusion cannot be a template key and must be a resolve-time parameter.
- (c) `_decision` with `--cap 1` records `ESCALATE` on every blocking round (`ledger.py:93-96`).
- (d) No `contract_version == "1.8.0"` equality in `src/`.
- (e) The CI grader has no `merge_method` match.
- (f) The wrapper and headless builder are post-only (previously an assumption, A-7; verified at `ensemble.py:797`; other callers were not read).
- (g) `refs/reviewer-spec.md:31-74,55,94-98,112-116` and `cost-profile.yaml` cites were re-read and are correct.

**UNVERIFIED (kept):**

- the `sc-adversarial` judge-exclusion input, and which return-contract field carries the judge identity;
- how `sc-adversarial` scores a skipped debate (`SKILL.md:409,951,439,457` says skip when variants differ by under 10% and score is "null if debate not reached");
- whether the Agent-tool reply carries a model id;
- the body of `cli/reflect/fallback.py` and the `review-telemetry/1` schema (`cli/review/telemetry.py`);
- the sprint executor code, and `refs/report-template.md`;
- whether the `reflect-reviewer` tools allowlist survives a `model` override (part of spike S-ID);
- the `judge_class_collision: true` record and the July `proxy_error` record (enrichment snippets only);
- `docs/reference/review-panel-live7.md:19-26` and the `REPORT.md:130-132` stoprule facts (taken from enrichment or V2, not re-read);
- every per-lane token split in the Cost model is an estimate; only the totals' bracket is checked against recorded artifact sizes.

**PROPOSED names introduced** (none exist today):

- templates: `review-panel.reflect-pre.json`, `reflect-pre-x2`, `reflect-post`, `reflect-post-x2`, `reflect-enterprise`, `reflect-lite`;
- K1: `classes` in the tier file, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, `skipped_slots`, `excluded` (additive resolution keys), CLI `--hard-exclude-class` and `--strict-distinct`;
- K3: `findings-v2` and its fields (`citations`, `deviation_class`, `coverage_rows`, `self_confidence`, `lens`, `channel`, `reflect_category`);
- K4: `superclaude review cluster`, `cluster_v2`, `cluster_agreement`; `superclaude review verify-citations`;
- artifacts: `panel/manifest.json`, `panel/resolution.json`, `panel/clusters.json`, `panel/precheck.json`;
- the reflect flag `--t2-engine legacy|shadow|panel`;
- telemetry: `t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `t2_floor_unmet`;
- the swarm lens input `--panel-resolution` (Stage 5);
- the test `test_panel_contract_lint.py`;
- contract: none.

## Required-content map

<!-- Source: Base (original, modified) - new appendix merged per Change #46 -->
| Required content | Where |
|---|---|
| At least 3 candidate architectures including leave-as-is | Candidate architectures (A-D and E') |
| Chosen architecture and reasons | Chosen architecture and reasons |
| Answers to Q1-Q7 | Answers to Q1-Q7 |
| Finding format | Finding format |
| Pre and post adapter sketches | Adapter sketches |
| Staged migration with pre behind an off-by-default flag first | Staged migration (Stage 2 `shadow`, Stage 3 `panel`, default `legacy`) |
| Mapping onto contract 1.8.0: `merge_method`, convergence score, null-score rules, gate condition 9, `reflect_post` frontmatter, every consumer | Return-contract 1.8.0 mapping (and "Deferred versioned change" for the consumer list of the deferred path) |
| Cost model with the depth table | Cost model; When the panel is called (depth x tier path) |
| Main risks | Risks |
| First measurement | First measurement |
| Depth x tier call policy | When the panel is called (depth x tier path) |



