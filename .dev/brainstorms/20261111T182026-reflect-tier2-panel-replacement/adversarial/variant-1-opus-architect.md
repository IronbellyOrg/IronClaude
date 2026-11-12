---
variant: 1
agent: opus:architect
generated: 2026-11-11T19:40:00Z
---

# Variant 1 (architect): a layered shared review kernel with reflect adapters

Paths are relative to `src/superclaude/` unless they start with `.dev/`. `path:line` cites are lines read in this session, or lines the enrichment file cites as read (marked "(enrichment)"). Everything marked PROPOSED is a new name, not an existing file, flag or function. Token figures are estimates unless a source is cited; the arithmetic is shown.

## Summary

Chosen architecture: **C, the Layered Review Kernel**. The panel's code becomes a shared kernel with four stable layers: panel resolution, dispatch adapters, a findings-v2 schema and a deterministic cluster merge. Reflect keeps its own policy layer on top: briefs, blind calibration, the evidence gate, the rubric and the contract builder.
Pre-execution moves to "panel dispatch, then deterministic merge, then evidence gate", and debates only disputed findings under `--depth deep`. Post-execution moves to panel dispatch but keeps the `/sc:adversarial` debate, because Regression/Drift class arbitration gates promotion and rollback.
Headline reason: one reviewer-identity and finding layer can be maintained for both commands without giving up any reflect grounding mechanism. The only part removed in pre-execution is the debate, which has separated nothing in recorded runs (convergence 1.0 in 4 of 5) and costs an estimated 25-35% of a T2 run.

## Candidate architectures

### A. Leave reflect as is

- **Changes:** nothing.
- **Keeps:** everything. That includes the hard-coded rotation table (refs/reviewer-spec.md:94-98), the debate (SKILL.md:633-651) and the two engines with diverging contract builders (cli/reflect/ensemble.py:787-832 emits `verification_ran: False` and `citations_dropped: 0` as constants).
- **Cost:** about 49-96k output tokens per pre-execution T2 run (estimate, see Cost model).
- **Risk:** low runtime risk, but maintenance risk rises. Two reviewer-pool definitions now exist (reflect's rotation and the panel's tier files, cli/review/data/review-tiers.default.json:4-11), and they will drift. Reviewer identity in the headless path comes from `T2Model0N` env vars (cli/swarm/lenses/reflect_review.py:59-64, enrichment) rather than a recorded, hashed resolution.
- **Verdict:** a valid fallback and the right answer if the first measurement fails. It does not meet the owner's "one shared review model" goal.

### B. Full replacement: reflect T2 becomes a spec-panel review loop

- **Changes:** reflect calls the panel end to end: `superclaude review panel resolve`, reviewers, `superclaude review merge` with ledger rounds (cap 3) and the reviser contract. The debate, the per-card calibrator and reflect's own merge are deleted. Ledger `confidence` single/overlap replaces calibrated confidence.
- **Keeps:** T1, the rubric, the evidence-validator.
- **Cost:** the spec-panel loop measured about 408k loop output tokens (.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19). Reflect has no revise step, so only the round-1 part applies. The default 4-reviewer panel with Haiku stand-ins writing 68k-108k each (LEDGER-RESULTS.md:66) is roughly 23k + 3 x 88k ≈ 290k for round 1 alone (midpoint arithmetic).
- **Risk:** high.
  - It drops blind calibration (SKILL.md:1172-1192) with no replacement of equal strength. Ledger confidence counts reviewers; it does not re-grade them blind.
  - The panel's measured gain comes from the ledger driving a revise loop on specs. Reflect never edits the plan (SKILL.md:342, "Findings never edit the tasklist"), so the mechanism that produced the gain is absent.
  - It breaks `merge_method` legal values (SKILL.md:789) and gate condition 9 (SKILL.md:1483).
- **Verdict:** rejected. It is the most expensive option, the gain does not transfer, and it violates the calibration constraint.

### C. Layered Review Kernel with reflect adapters (chosen)

- **Changes:** the panel code is generalized into four layers, each with a schema id:
  - **K1 Resolution:** `review-panel-resolution/1` plus a PROPOSED `exclusions` block and per-model `class`.
  - **K2 Dispatch adapters:** agent-session and swarm, both reading K1.
  - **K3 Findings:** PROPOSED `findings-v2`, a superset of findings-v1 with typed multi-file citations, deviation class, coverage rows and a calibrated-confidence slot.
  - **K4 Merge:** deterministic cluster plus an optional ledger. A single-pass mode is the reflect default.

  Reflect adds two adapters, pre and post, that sit on K1-K4 and keep briefs, calibration, the evidence gate, the rubric and the contract builder. Pre-execution: K4 merge replaces the debate, and the debate runs only on disputed clusters under `--depth deep`. Post-execution: K4 pre-clusters the cards and the debate still runs, so `merge_method: adversarial` keeps its meaning.
- **Keeps:** every reflect grounding mechanism, the 1.8.0 field names, and the post-execution contract semantics.
- **Cost:** pre about 34-66k (about 30% below A); post about the same as A.
- **Risk:** medium. A contract enum widening (`merge_method: panel`) needs a planned version change (see the mapping section). Multi-file dedupe is new code.
- **Verdict:** chosen.

### D. Panel as dispatcher only (thin adoption)

- **Changes:** reflect replaces only its rotation table with `superclaude review panel resolve`. Everything after dispatch is unchanged (cards, calibration, debate, validator).
- **Keeps:** everything else.
- **Cost:** the same as A.
- **Risk:** low.
- **Verdict:** this is Stage 1 of C, not a destination. It unifies reviewer identity but leaves two finding formats and two merges. That is the main maintenance cost the owner asked to remove.

### E. Debate-always hybrid

- **Changes:** as C, but the debate runs on every T2 run in both modes, with the K4 cluster map as an extra input.
- **Keeps:** the 1.8.0 contract with no version change at all.
- **Cost:** pre about 49-96k (no saving).
- **Risk:** low.
- **Verdict:** this is what C does for post-execution. For pre-execution it pays for a step that has not separated anything (enrichment section 4: convergence 1.0, 1.0, 1.0, 1.0, 0.97). Keep it as the rollback position for pre.

### Comparison

| | A as-is | B full loop | C kernel (chosen) | D dispatcher only | E debate-always |
|---|---|---|---|---|---|
| One reviewer-identity layer | no | yes | yes | yes | yes |
| One finding format | no | yes (lossy) | yes (findings-v2) | no | yes |
| Blind calibration kept | yes | **no** | yes | yes | yes |
| Evidence gate kept | yes | yes | yes, strengthened | yes | yes |
| Debate | always | never | post always, pre on disputes (deep only) | always | always |
| Contract change | none | major | 1.9.0 additive, then 2.0.0 enum widening, pre only | none | 1.9.0 additive |
| Pre T2 output tokens (est.) | 49-96k | about 290k+ | 34-66k | 49-96k | 49-96k |
| Transfers the measured panel gain | n/a | no (no revise step) | no claim made | no | no |
| Maintenance surface | 2 pools, 2 formats, 2 merges | 1 | 1 kernel + thin adapters | 1 pool, 2 formats | 1 kernel |

## Chosen architecture and reasons

**C, the Layered Review Kernel.** Reasons, in order of weight:

1. **The maintenance unit is the layer, not the command.** Today, reviewer identity lives in three places: the reflect rotation table (SKILL.md:604-608), the `T2Model0N` env pool (reflect_review lens), and the panel tier file (review-tiers.default.json:4-11). Finding shape lives in two places: reviewer card YAML and findings-v1 (findings.py:90-121). Merge lives in two places: `/sc:adversarial` and `merge_round` (ledger.py:200-298). C reduces each to one implementation with a schema id. Commands differ only in policy: brief, required finding fields, gates and contract.
2. **No grounding mechanism is weakened.**
   - Calibration (SKILL.md:1172-1192) stays per card.
   - The evidence-validator stays mandatory (SKILL.md:587). It gains a deterministic citation pre-check that typed citations make possible.
   - Executor-class exclusion (SKILL.md:600-610) becomes a hard K1 input instead of reflect-side table editing.
3. **The debate is removed only where evidence says it is idle and the stakes are advisory.** Pre-execution reflect is advisory: sc-workflow records only `reflect_status` and `reflect_report_path` and never changes the workflow status (skills/sc-workflow-protocol/SKILL.md:60-64, enrichment). Post-execution feeds promotion condition 9 (SKILL.md:1483) and the wrapper's degraded triggers 9-11b (cli/reflect/contract.py:290-326), so it keeps the debate.
4. **Extension scaffolding at low cost.** A third consumer (for example `/sc:auggie-review` or `/tdd`) would add a template, a brief and a contract mapping, and nothing else. No new merge code and no new reviewer pool.
5. **It does not claim the PN1 gain.** The spec-panel gain (15.7 vs 2.8 fixed defects, LEDGER-RESULTS.md:19) was measured with a revise loop on specs. C adopts the panel for maintainability and cost, not for a quality uplift. Quality is checked by the first measurement as non-inferiority.

## Answers to Q1-Q7

### Q1. What the panel takes over, what it lacks, what stays in reflect

**Direct answer:** the panel takes over the reviewer pool, model diversity, deterministic resolution, the dispatch description and telemetry, plus merge for pre-execution. It lacks hard executor exclusion, personas, blind calibration, an evidence gate, multi-file citations, deviation class and coverage rows. All reflect-specific judgement stays in reflect.

| Function | Today in reflect | Panel today | Owner in C |
|---|---|---|---|
| Reviewer pool, model rotation | rotation table (SKILL.md:604-608) | tier aliases + templates (review-tiers.default.json:4-11; review-panel.default.json:8-12) | **kernel K1** (reflect templates, PROPOSED) |
| Deterministic, recorded choice | none (agent-session) / env pool (swarm) | seeded by run id, template and tier hashes recorded (panel.py:455-459, 514-525) | **K1** |
| Model diversity | `_diversity.py` full/degraded (enrichment) | `distinct_across_slots`, soft (panel.py:405, 408 fall back to the full candidate list) | K1 computes it; reflect keeps `t2_*_diversity` emission |
| Executor-class exclusion | hard rule, N=2 floor (SKILL.md:600-610) | **lacks**: `exclude` is soft and ignored by `fixed` slots (panel.py:402-403) | **K1 PROPOSED `hard_exclude`**; reflect supplies the class |
| Personas | analyzer/qa/refactorer via brief (refs/reviewer-spec.md:94-98) | **lacks** | **reflect**: persona by resolution ordinal (no kernel change) |
| Parallel dispatch | Agent tool `reflect-reviewer` / swarm lens | `launch` alias map (review-tiers.default.json:29), no dispatcher | **K2 adapters** read K1 |
| Blind calibration | `confidence-calibrator` per card, disjoint class (SKILL.md:1172-1192) | **lacks** | **reflect** (writes into the K3 calibration sidecar) |
| Merge | `/sc:adversarial --compare` (SKILL.md:645-651) | `merge_round` cluster + ledger (ledger.py:200-298) | **K4** (pre); K4 pre-cluster + debate (post) |
| Evidence gate | evidence-validator, mandatory (SKILL.md:587) | **lacks** | **reflect**, with a PROPOSED K3 deterministic pre-check |
| Telemetry | §9.2 block (SKILL.md:892-921) | `review-telemetry/1` (enrichment: names only) | both: reflect §9.2 stays; K1/K4 append panel records |
| Grounding, coverage map, deviation taxonomy, rubric, remediation, promotion | reflect | n/a | **reflect** (constraint) |

### Q2. A finding format for both

**Direct answer:** findings-v2 (PROPOSED), a strict superset of findings-v1. `anchor` becomes optional when `citations[]` is present. Typed fields are added for deviation class, coverage rows, self-reported confidence and a calibrated confidence that reviewers may not set. Reflect's reviewer card keeps its prose. The machine part of the card *is* the findings-v2 block. Schema and dedupe key are in the Finding format section.

### Q3. Merge: debate, deterministic, or both

**Direct answer:** both, split by mode.

- **Pre-execution:** K4 deterministic merge is the default. A scoped debate on disputed clusters runs only with `--depth deep`.
- **Post-execution:** K4 pre-cluster plus the full debate. `merge_method: adversarial` and `adversarial_convergence_score` keep their 1.8.0 meaning.

What is lost without the debate:

- **Pre-execution.** Three things are lost:
  1. Arbitration when reviewers disagree on whether a plan gap is blocking. K4 takes the OR of blocking and the max severity (ledger.py:213-222), so disagreement turns into "blocking, single support". It is not resolved.
  2. The narrative synthesis of a merged verdict. REPORT.md is still written by reflect's Wave 5.
  3. A numeric convergence score. It is replaced by `panel_agreement_score` (definition below).

  The cost is small: pre findings are advisory, and every finding still passes the evidence gate. Recorded evidence is thin (6 runs) but shows the debate score never fell below 0.97.
- **Post-execution.** Arbitration of deviation *class* (Necessary vs Drift vs Regression) would be lost. That class drives `deviation_count_by_class`, `regression_present`, TurnLedger rollback (SKILL.md:930), promotion condition 4 (SKILL.md:1472) and the wrapper's halted triggers (contract.py:369-381). A deterministic merge cannot decide between two classes; it can only take the worst. That would over-report Regression and block promotions that should pass. This is why post keeps the debate.

**Judge class.** The debate keeps the rule that the judge is a different class from the debaters (refs/reviewer-spec.md:112-116). K1 now records reviewer classes, so reflect can pass them to sc-adversarial. A recorded `judge_class_collision: true` (enrichment section 4, snippet only, UNVERIFIED) shows that delegation alone does not enforce the rule. Whether sc-adversarial accepts a judge-exclusion input is UNVERIFIED. If it does not, reflect records `judge_class_collision` and emits `calibrator_diversity`-style degraded telemetry. Fable and Tier 0 are never a judge.

### Q4. Engine

**Direct answer:** both engines, one identity source. The K1 resolution JSON is the only place reviewer models are chosen. Two K2 adapters read it:

- **Agent-session adapter** (interactive skill; this is the pre-execution path, because sc-workflow invokes reflect inside an agent session). It spawns `~/.claude/agents/reflect-reviewer.md` once per resolved reviewer and passes the K1 `launch` value as the model override. In anthropic-only, `launch` maps model ids to `sonnet`, `haiku` and `opus` (review-tiers.default.json:29). In gateway, `launch` is empty and "dispatch mechanism per model not defined yet" (review-tiers.default.json:20). The adapter then uses the tier alias (for example `claude-gw-tier2[1m]`, review-tiers.default.json:7) as a ccsession model alias. Whether the Agent tool accepts that alias as a model override is UNVERIFIED and is a Stage 1 exit check.
- **Swarm adapter** (headless post path, cli/reflect/ensemble.py). The `reflect-review` lens takes worker models from a PROPOSED `--panel-resolution <file>` input instead of `T2Model0N` env vars. `T2Model0N` stays as the fallback when no resolution file is given, so existing runs are unaffected.

**Model-class rotation versus T2Model slots.** Reflect's rotation becomes packaged K1 templates (PROPOSED `review-panel.reflect-pre.json` and `review-panel.reflect-post.json`, loadable as `@reflect-pre` per panel.py:327-334):

```json
{"schema": "review-panel/1", "template_id": "reflect-pre", "version": "1.0.0",
 "distinct_across_slots": true, "apply_to": ["first"],
 "slots": [
   {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
   {"slot_id": "t4",  "tier": "tier4",  "count": 1, "strategy": "random"},
   {"slot_id": "t2",  "tier": "tier2",  "count": 1, "strategy": "random"}]}
```

- **anthropic-only:** resolves to Sonnet, Haiku, Haiku (stand-ins, review-tiers.default.json:28). That is 2 distinct ids, so model diversity is `full` under the 2-distinct rule (`_diversity.py`, enrichment) and vendor diversity is single, the same as today.
- **Side effect worth stating:** today's default third reviewer in anthropic-only is Opus (SKILL.md:607). The calibrator's disjoint set {opus, sonnet, haiku, qwen, kimi, deepseek} minus reviewers is then empty of available classes, which forces `calibrator_diversity: degraded` (SKILL.md:1180-1185). With the reflect-pre template, the disjoint set is {opus}, so the calibrator is Opus and `calibrator_diversity` becomes `full`. **Opus is used here, and only here, because the disjoint-set rule requires a class no reviewer uses.** Calibrator output is a short re-grade (est. 1-2k tokens per card).
- **gateway:** resolves to Sonnet or another tier1b model, a tier4 model (gpt-6-luna, haiku or grok) and a tier2 model. Vendor diversity can become multi. The calibrator can then be a non-reviewer tier2 or tier3 model rather than Opus (PROPOSED calibrator selection from K1 classes).
- `--strategy enterprise` (SKILL.md:608) maps to a PROPOSED `@reflect-enterprise` template whose third slot is `tier1a`. That means an Opus reviewer: opt-in only, and stated as such.

Fable and Tier 0 are never listed. `claude-fable-5-1` appears in the anthropic-only `available` list (review-tiers.default.json:27), but no reflect template references a tier that resolves to it. The PROPOSED kernel validation for reflect templates rejects any resolution whose model id is `claude-fable-*`.

### Q5. Pre-execution migration end to end

**Direct answer:** the flow below. It is detailed in the Adapter sketches section.

- **Input:** plan plus source spec (`--spec <pkg>/source.md --tasklist <pkg>/<id>.md`, enrichment).
- **Reviewers:** from K1 `@reflect-pre`, with the executor class hard-excluded. Each gets a three-section brief that is unchanged (refs/reviewer-spec.md:31-74). The qa ordinal receives the spec body (refs/reviewer-spec.md:55).
- **Findings:** each reviewer card ends with a `## Findings block` fenced `findings-v2` block, citing `plan` and `spec` roles.
- **Calibration:** per card, blind, and written to a sidecar.
- **Merge:** K4 single-pass, two documents.
- **Evidence gate:** deterministic pre-check, then the evidence-validator agent.
- **Contract:** `merge_method: panel` (contract 2.0.0, pre only), `adversarial_convergence_score: null`, plus `panel_agreement_score`. All coverage fields are unchanged.

### Q6. Rounds, ledger, revise loop

**Direct answer:** reflect stays single-pass. It never revises the artifact it reviews (SKILL.md:342), so rounds 2-3 would have nothing to verify. K4 runs one round with `--cap 1`. The ledger file is still written, because it is the on-disk merged record that EV-1 can check (replacing `merged-verdict.yaml` for pre). The ledger's `decision` (PASS/REVISE/ESCALATE) is recorded and ignored by reflect.

**Extension point, not built:** sc-workflow's Phase B "refactor" loop re-runs Phase A into a new package (SKILL.md:342). A future ledger keyed on the workflow id could carry findings across those packages. That is deferred and named only so the K4 ledger id is not tied to one reflect run id.

### Q7. Cost before and after; when a full panel is not worth calling

**Direct answer:**

- **Pre-execution:** T2 drops from about 49-96k to about 34-66k output tokens (about 30%), entirely by removing the debate.
- **Post-execution:** about unchanged.
- **A full panel (default 4 slots, or live7) is not worth calling for reflect:**
  - In anthropic-only, every extra slot is another Haiku stand-in. That adds tokens without new model classes. The 1S+6H vs 1S+3H gain was about 3 defects on one spec (docs/reference/review-panel-live7.md:19-26, enrichment).
  - Reflect has no revise step to turn extra findings into fixes.
  - Pre is advisory.

  Arithmetic is in the Cost model section.

## Finding format

PROPOSED schema `findings-v2`. It is JSON lines in a fenced block with info string `findings-v2` under the heading `## Findings block`, the same container rules as v1 (findings.py:124-196). A v1 line is valid v2 by construction.

| Field | Type | v1? | Set by | Rule |
|---|---|---|---|---|
| `id` | str `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` | yes | reviewer | unique per block (findings.py:91-95) |
| `severity` | CRITICAL/MAJOR/MINOR | yes | reviewer | MINOR cannot block (findings.py:100-101) |
| `blocking` | bool | yes | reviewer | |
| `category` | v1 enum + PROPOSED `coverage-gap`, `deviation`, `best-practice`, `grounding` | extended | reviewer | v1 values unchanged (findings.py:15-22) |
| `claim` | str ≤300 | yes | reviewer | |
| `refs` | ≤8 str | yes | reviewer | requirement ids such as `REQ-014`, `INF-003`, task ids |
| `anchor`, `anchor2` | quote 12-200 chars | yes | reviewer | **required only if `citations` is absent** |
| `citations` | list 1..8 of `{role, path, line_start, line_end, quote}` | NEW | reviewer | `role` ∈ `plan` `spec` `source` `test` `diff` `artifact`; `path` repo-relative; `quote` 12-200 chars copied from those lines |
| `deviation_class` | `authorized` `necessary` `drift` `regression` `none` | NEW | reviewer | required when `lens` is `reflect-post`; optional in pre (plan-vs-spec gaps map to `none` or a coverage category) |
| `coverage_rows` | list of requirement/task ids | NEW | reviewer | must be ids present in the reviewer's Coverage slice |
| `self_confidence` | float 0-1 | NEW | reviewer | self-report; never routes anything |
| `lens` | `spec` `reflect-pre` `reflect-post` | NEW | brief | selects the required-field profile |
| `calibrated_confidence` | float 0-1 | NEW | **calibrator sidecar only** | a reviewer line that sets it is rejected (keeps calibration blind and separate) |
| `validator_status` | `kept` `dropped` `inferred` | NEW | evidence gate sidecar only | |

**How reflect card content and panel findings coexist.** The reflect card stays a document. Its prose sections and the persona's narrative are what the debate reads in post and what the report quotes. The `findings-v2` block is the machine part.

The calibrator writes a PROPOSED sidecar `<output>/panel/calibration.json`: `{reviewer_id: {calibrated_confidence, dims[5], calibrator_model, calibrator_class}}`. The evidence gate writes `<output>/panel/validation.json`: `{reviewer_id/fid: {status, citation_results[]}}`. K4 reads all three. Reviewer output is never mutated, matching the reflect-reviewer read-only constraint (refs/reviewer-spec.md:11-15).

**Dedupe key for multi-file citations (K4 v2 matcher, PROPOSED).**

1. Annotate each citation, not each finding. `span = (line_start-1, line_end)` on the file at `path`. `section` is the nearest heading for markdown roles (reuse `section_of`, findings.py:307-318), or the nearest enclosing `def`/`class`/function line for code roles (deterministic regex fallback; codegraph enclosing-symbol when `index_state=fresh`). The quote is checked with `locate` against those lines (findings.py:276-304), which gives `anchor_status`.
2. The **primary citation** is the first citation whose `role` is the reviewed artifact: `plan` in pre, `source` or `diff` in post. If there is none, it is the first citation.
3. **Fingerprint v2** = sha256(`"v2|" + role + "|" + path + "|" + section + "|" + ",".join(refs_norm) + "|" + (deviation_class or "-")`)[:16]. This mirrors v1 (findings.py:340-343) with path and class added.
4. **same_defect_v2(a, b)** is true when:
   - (a) the fingerprints are equal and `refs_norm` is non-empty (v1 rule, findings.py:371-372); or
   - (b) the deviation classes are compatible (equal, or either null or `none`), the `refs_norm` sets intersect or are both empty, and **some** citation of a and **some** citation of b have the same `role` and `path` with spans within ±3 lines (v1 tolerance, findings.py:377).

   Cross-file citations therefore merge only through a shared file. Two findings that cite the same spec requirement from different plan tasks merge through the `spec` citation plus a shared REQ ref. Two findings with no shared file do not merge.
5. Clusters use the existing union-find (findings.py:382-407).

**`panel_agreement_score` (PROPOSED).** For each blocking cluster c, support(c) = Σ calibrated_confidence of member reviewers / Σ calibrated_confidence of all reviewers that returned a valid block. Then panel_agreement_score = mean(support(c)) over blocking clusters, or 1.0 when there is no blocking cluster and at least 2 valid blocks. A cluster is **disputed** if support(c) < 0.5, if its members disagree on `blocking`, or if they disagree on a non-null `deviation_class`.

## Adapter sketches

### Pre-execution adapter (agent-session engine)

**Inputs:** `--spec`, `--tasklist`, `--executor-model` (optional), PROPOSED `--t2-engine legacy|shadow|panel` (default `legacy`).

1. **Wave 0 / 0.5b (unchanged).** Resolve aliases and the executor class (SKILL.md:600-602).
2. **Waves 1-2 (unchanged).** Grounding, the coverage map with the two-pass extraction, T1 card, Wave 1D calibration, rubric (SKILL.md:354-382). If the rubric stops at T1, the adapter never runs.
3. **K1 resolve.** `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --kind first --exclude-class <executor class>` (`--exclude-class` is PROPOSED; `--template`, `--run-id` and `--kind` exist per panel_cmd.py:18-53, option names not all read, UNVERIFIED). Write `<output>/panel/resolution.json`. If hard exclusion leaves fewer than 2 reviewers, emit `executor_exclusion_degraded: true` and degrade to T1 (SKILL.md:600, unchanged semantics).
4. **Brief (unchanged shape).** Three sections (refs/reviewer-spec.md:31-74). Persona by resolution ordinal: 1 analyzer, 2 qa, 3 refactorer. qa gets the spec body hunks (refs/reviewer-spec.md:55). One added instruction line in the T1-card section of the brief: "End your card with a `## Findings block` fenced `findings-v2` block, `lens: reflect-pre`, citations with roles `plan` and `spec`." This is an instruction inside an existing section, not a fourth section.
5. **K2 dispatch.** Parallel Agent calls to `reflect-reviewer` (`~/.claude/agents/reflect-reviewer.md`), one per resolution entry, with model = `launch` value (anthropic-only) or tier alias (gateway, UNVERIFIED). Cards go to `<output>/reviewer-cards/reviewer-<n>-card.md`.
6. **Blind calibration (unchanged mechanism, SKILL.md:1192).** One `confidence-calibrator` per card (`~/.claude/agents/confidence-calibrator.md`), in a class disjoint from K1's reviewer classes. Results go to `<output>/panel/calibration.json`.
7. **Deterministic citation pre-check (PROPOSED `superclaude review verify-citations`).** For every citation, check that the file exists at `input_tree_snapshot_path`'s hash, that the line range exists, and that the flattened quote occurs inside the range. A failure marks the citation `dropped-precheck`. This is script work, 0 model tokens.
8. **Evidence-validator (unchanged, mandatory, SKILL.md:587).** It re-Reads every citation that survived the pre-check. Pre-check drops are added to its drop count, never subtracted. Results go to `validation.json`, and `citations_total`, `citations_revalidated` and `citations_dropped` follow §9.1 definitions. **Grounding strength:** the agent gate is unchanged and the pre-check only adds rejections, so grounding is at least as strong as today.
9. **K4 merge.** `superclaude review merge --schema findings-v2 --doc plan=<tasklist> --doc spec=<spec> --round 1 --cap 1 --report r1=... --resolution panel/resolution.json --calibration panel/calibration.json --validation panel/validation.json --ledger panel/ledger.json --out panel/merged-report.md`. `--schema`, role-qualified `--doc`, `--calibration` and `--validation` are PROPOSED; `--round`, `--cap`, `--report`, `--resolution`, `--ledger` and `--out` exist (merge_cmd.py:21-70). Only validator-kept findings enter clusters. Output: clusters, `panel_agreement_score`, disputed list.
10. **Disputes.** Default: disputed clusters are reported in REPORT.md as "single-support" with their calibrated confidence, and no debate runs. With `--depth deep` and at least one disputed cluster: `Skill sc-adversarial-protocol --compare` on the disputed clusters' source cards only, with the judge class excluded from K1 classes. The result goes to the PROPOSED field `dispute_debate_convergence`. `adversarial_convergence_score` stays null.
11. **EV-1 for the panel path (PROPOSED wording).** Wave 4 is complete when `panel/ledger.json` and `panel/merged-report.md` exist on disk, `ledger.rounds[0].reviewers` has at least 2 entries with valid blocks, and `reviewer-cards/` holds that many cards and `calibration.json` that many entries. If `merge_round` refuses the round because no valid block exists (enrichment gap 3), take the F2 path: `merge_method: single-reviewer-fallback` using the highest-calibrated card (SKILL.md:313).
12. **Contract.** As in the mapping table. REPORT.md renders clusters as findings with plan/spec citations.

**Shadow mode (`--t2-engine shadow`).** Steps 3-9 run with K1 replaced by the legacy rotation expressed as a resolution (so the cards are identical), and the legacy debate runs too. The debate result is authoritative. The panel artifacts and telemetry are written for the measurement.

### Post-execution adapter (both engines)

**Inputs:** `--spec`, `--tasklist`, `--task-log`, `--diff`, `--executor-model`, `--t2-engine`.

1. Waves 0-2 unchanged, including §6.1 verification steps 5/5.5 run by the orchestrator. Reviewers never execute (refs/reviewer-spec.md:14).
2. K1 resolve with `--template @reflect-post` (same slots as pre; `@reflect-enterprise` adds a tier1a slot) and the executor class hard-excluded.
3. Brief unchanged. The qa ordinal gets the verification and runtime-surface hunks (refs/reviewer-spec.md:53, 57). Findings use `lens: reflect-post`, so `deviation_class` is required and citations use roles `source`, `test`, `diff`, `artifact`, `spec`.
4. K2 dispatch:
   - Agent-session: as in pre.
   - Headless: `superclaude reflect` → ensemble → swarm `reflect-review` lens with PROPOSED `--panel-resolution`. The bounded fallback ladder stays (cli/reflect/fallback.py, body UNVERIFIED) and walks K1's `fallbacks` list (panel.py:417) instead of the env pool.
5. Blind calibration per card (unchanged).
6. Citation pre-check, then the evidence-validator (unchanged). **Headless gap closed (separate work item):** today the headless builder hard-codes `citations_dropped: 0` and `verification_ran: False` (ensemble.py:808-817). With K3 typed citations, the headless path can run the same pre-check and report a real `citations_dropped`. The agent validator stays the authority where it runs.
7. K4 pre-cluster (no verdict authority): the cluster map with class agreement per cluster goes to `panel/clusters.json`.
8. **Debate (kept).** `Skill sc-adversarial-protocol --compare <calibrated cards> ...` as today (SKILL.md:645-651), plus `panel/clusters.json` as an extra input (PROPOSED; whether `--compare` accepts a non-card context file is UNVERIFIED, otherwise the cluster map is appended to each card). Writes `adversarial/merged-verdict.yaml` (EV-1 unchanged, SKILL.md:666).
9. Contract: `merge_method: adversarial`, `adversarial_convergence_score` from the debate. The 1.8.0 semantics are unchanged. The panel fields are additive.
10. Promotion, remediation and the `reflect_post` write-back are unchanged.

## Staged migration

| Stage | What ships | Entry criteria | Exit criteria | Rollback |
|---|---|---|---|---|
| **0. Measure offline** | findings-v2 schema + parser, card→findings-v2 converter for existing cards, v2 matcher, `panel_agreement_score`; **no runtime change** | design accepted | replay of the 5 recorded T2 runs (enrichment section 4) produces cluster maps; first measurement (below) designed and costed | delete the code; nothing consumed it |
| **1. Kernel extensions** | K1 `class` map + `hard_exclude` (also applied to `fixed` slots), `@reflect-pre`/`@reflect-post` templates, Fable-rejecting validation; K4 `--schema findings-v2`, multi-`--doc`, `--calibration`, `--validation`; `verify-citations` | Stage 0 exit | unit tests: hard exclusion of the fixed anchor; v1 reports merge byte-identically with and without `--schema` (no spec-panel regression); Agent-tool alias override checked for gateway (UNVERIFIED item) | revert the kernel commits; spec-panel paths untouched by construction (new flags off by default) |
| **2. Pre shadow** (`--t2-engine shadow`, off by default) | pre adapter steps 3-9 alongside the legacy debate; contract **1.9.0 additive** fields (below); telemetry rows | Stage 1 exit | first measurement run and **passed**; ≥20 shadow runs with zero MALFORMED and an EV-1 failure rate no higher than legacy | set flag default to `legacy` (it already is); the 1.9.0 fields are additive and read-and-ignore (SKILL.md:970) |
| **3. Pre panel opt-in** (`--t2-engine panel`, off by default) | panel merge authoritative in pre; `merge_method: panel` → contract **2.0.0** | every consumer in the 2.0.0 list (mapping section) updated and released; grep shows no `contract_version == "1.8.0"` equality check remains (UNVERIFIED today) | ≥30 opt-in workflow runs: `reflect_status` distribution no worse than shadow, zero MALFORMED, token mean ≤75% of legacy | flag back to legacy; legacy runs emit 2.0.0 with `merge_method: adversarial`, which 2.0.0 consumers already accept |
| **4. Pre default flip** | sc-workflow's Wave 4 call gets the panel engine by default | Stage 3 exit + owner sign-off | 2 release cycles with no regression in workflow `reflect_status: failed` rate | one-line default change back to `legacy` |
| **5. Post panel dispatch** (`--t2-engine panel` for post) | post adapter: K1/K2/K3, K4 pre-cluster, debate kept; headless contract builder reports real `citations_dropped` | Stage 4 exit; a separate post measurement (seeded deviations, class accuracy) designed | wrapper verdict distribution (contract.py) on ≥20 paired post runs: no new `degraded`/`halted` reasons caused by dispatch alone | flag back to legacy rotation; contract fields unchanged for post |
| **6. Optional: post deterministic merge for non-gating clusters** | debate only on clusters whose class affects gates | a post measurement showing class arbitration is preserved | | not planned until data exists |

## Return-contract 1.8.0 mapping

**Versioning plan.**

- **1.9.0 (Stage 2), purely additive** per §9.4 (SKILL.md:952). New fields:
  - `merge_engine: legacy | panel`
  - `panel_resolution_path`
  - `panel_ledger_path`
  - `panel_agreement_score: <float> | null`
  - `panel_disputed_clusters: <int> | null`
  - `dispute_debate_ran: <bool>`
  - `dispute_debate_convergence: <float> | null`
  - `findings_schema: reviewer-card | findings-v2`
  - `citations_dropped_precheck: <int>` (a component of `citations_dropped`, which stays authoritative)
- **2.0.0 (Stage 3):** `merge_method` legal values widen from {adversarial, single-reviewer-fallback} (SKILL.md:789) to add `panel`, legal **only** when `mode: pre`. Widening a legal-value set changes EV-2 semantics, so under §9.4 it is a major change (SKILL.md:953: "semantic change ... Breaking"). The consumers below must update before it ships. No field is renamed or removed.

| Contract field | Source in new design | Status |
|---|---|---|
| `merge_method` | pre panel: `panel`; pre panel F2: `single-reviewer-fallback`; pre with legacy/shadow and all post: `adversarial` from the debate | values widened in 2.0.0 (pre only) |
| `adversarial_convergence_score` | debate score where the debate is the merge (legacy, shadow, post); **null by construction** when `merge_method: panel` | unchanged field; new null case |
| `adversarial_unavailable` | true only on the F3 path, as today (SKILL.md:314); `false` on a panel merge (the merge is available, it is just not adversarial) | unchanged |
| `adversarial_artifacts_dir` | debate dir when it ran; null for panel-only | unchanged |
| `reviewer_cards` | card paths (unchanged location) | unchanged |
| `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity` | computed from K1 resolution models | unchanged semantics |
| `calibrator_diversity` | from K1 classes vs calibrator class | unchanged semantics (often improves to `full`, see Q4) |
| `citations_total/revalidated/dropped` | validator + pre-check union | unchanged semantics (pre-check can only add drops) |
| `evidence_validator_ran` | true (mandatory) | unchanged |
| `confidence_calibrated`, coverage fields, deviation fields, promotion fields | reflect waves, unchanged | unchanged |
| `status` | unchanged derivation; `citations_dropped > 0` forces partial (SKILL.md:777) | unchanged |
| new 1.9.0 fields | K1/K4 artifacts | additive |

**Null-score rules (extended).** The existing rule "route on `merge_method` FIRST" (SKILL.md:661) extends by one branch: if `merge_method == panel`, then `adversarial_convergence_score` is inapplicable and `panel_agreement_score` is the routing input. A null `panel_agreement_score` with `merge_method: panel` is MALFORMED (EV-2 extended). The undefined-comparison guard (SKILL.md:662) applies to both scores.

**Gate condition 9 (SKILL.md:1483).** Promotion is UC-2 only (`promotion_gate_passed` is null when `mode == pre`, SKILL.md:837), and `panel` is legal only in pre. So condition 9 is unchanged in every stage up to 5. Its wording "a Tier 2 run with no merged adversarial verdict MUST NOT promote" stays literally true for post. If Stage 6 ever ships, condition 9 would need a second clause (`merge_method == panel` AND an on-disk ledger AND non-null `panel_agreement_score`). That would be another major change and is explicitly out of scope.

**`reflect_post` frontmatter (cli/reflect/runner.py:103-133).** Its fields are verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at and three `*_verified` booleans. None is a merge field. The wrapper writes it for post runs on a tasklist. **Unchanged in every stage.** In Stage 5, an optional `merge_engine` key may be appended at the end, following the FX7 append-at-end precedent (runner.py:127-129). It is not required.

**Consumer by consumer.**

- **sc-workflow Wave 4** reads `reflect_status`/`reflect_report_path` only (enrichment: skills/sc-workflow-protocol/SKILL.md:60-64): no change.
- **Wrapper verdict map** (cli/reflect/contract.py):
  - Trigger 10 compares only `single-reviewer-fallback` (contract.py:295), so `panel` passes through.
  - Trigger 11 (null convergence at T2, contract.py:299-300) **would mis-fire on a pre panel run**, and trigger 11b (contract.py:317-326) skips null. 2.0.0 change: guard triggers 11 and 11b with `merge_method != "panel"`, and add an equivalent `panel_agreement_score` null/NaN check for `panel`.
  - In practice the wrapper is post-only (ensemble.py:797 hard-codes `"mode": "post"`). The guard is defensive.
- **Headless ensemble contract builder** (ensemble.py:772-773): it sets `adversarial` for ≥2 reviewers. It is post-only, so there is no 2.0.0 change. Stage 5 makes `citations_dropped` real, which can newly trip trigger 13 (contract.py:347-352). That is intended and honest, but it is a behavior change, called out at Stage 5 entry.
- **Sprint executor TurnLedger** (SKILL.md:930) reads `status` and `per_task_verdicts`: post-only, unchanged.
- **sc-troubleshoot, sc-task, task-builder, sc-workflow T3 handoff** (SKILL.md:929, 931, 937-938) read no merge fields: no change.
- **sc:roadmap, sc:tasklist gates** (SKILL.md:932-933) read coverage fields: no change.
- **Wave 7 promotion** (SKILL.md:939): post-only, no change (see condition 9).
- **CI grader** (`make reflect-eval`, SKILL.md:940): whether grader.py asserts `merge_method` values is UNVERIFIED. The 2.0.0 entry criterion is to grep it and add `panel` for pre cases.
- **Meta-eval aggregator** (SKILL.md:941) reads `convergence_score`: it must route on `merge_method` first and aggregate `panel_agreement_score` separately (2.0.0 change).
- **Reflect SKILL.md** EV-1 (SKILL.md:666) and EV-2 (SKILL.md:789): add the panel-path on-disk check and the widened legal set (2.0.0 change, in `~/.claude/skills/sc-reflect-protocol/SKILL.md` after install).

## Cost model

All figures are **output tokens**, following assumption A-5, and are estimates. The only measured anchors:

- cost-profile T2 35k-70k Claude tokens plus 10k-25k auggie (refs/cost-profile.yaml:46-70, enrichment);
- recorded T2 artifact sizes 221,405-371,507 bytes, about 55k-93k tokens at 4 bytes per token (221,405/4 ≈ 55k; 371,507/4 ≈ 93k);
- PN1 lanes (LEDGER-RESULTS.md:59-64).

Artifact bytes include copied input hunks, so they overstate output somewhat.

**Before: pre-execution T2 today (3 reviewers), per lane (estimates).**

| Lane | Work | Estimate | Arithmetic |
|---|---|---|---|
| primary | T1 card, coverage map, 3 briefs, REPORT | 12-20k | assumption |
| parallel | 3 reviewer cards | 15-30k | 3 x 5-10k |
| calibrator | 1 T1 + 3 T2 re-grades | 4-8k | 4 x 1-2k |
| merge | `/sc:adversarial --compare --depth standard` | 15-30k | assumption: multi-step advocates, scoring and merge over 3 cards |
| validator | evidence-validator re-Reads | 3-8k | assumption |
| **total** | | **49-96k** | 12+15+4+15+3 = 49; 20+30+8+30+8 = 96 |

That range brackets the observed 55k-93k artifact estimate, which is the only sanity check available.

**After: pre panel (`@reflect-pre`, 3 reviewers).**

| Lane | Change | Estimate |
|---|---|---|
| primary | unchanged | 12-20k |
| parallel | +findings-v2 block, about 0.5k per card | 16.5-31.5k (15+1.5; 30+1.5) |
| calibrator | unchanged | 4-8k |
| merge | K4 script | 0 model tokens |
| dispute debate | default 0; `--depth deep` with disputes about 5-10k | 0 (default) |
| validator | pre-check removes obviously bad citations first; assume 0-20% less agent work | 2.4-8k |
| **total (default)** | | **about 35-68k** (12+16.5+4+0+2.4 ≈ 35; 20+31.5+8+0+8 ≈ 68) |

Saving: about 14-28k per run (the debate lane minus the added blocks), about 28-30% of the before range.

**Post (Stage 5):** the debate is kept, so the cost is about the same as before (+1.5k for blocks, +0 for K4). The value is maintenance and an honest headless `citations_dropped`, not tokens.

**What a full panel would cost in reflect (why not to call it).** Using the default 4-slot panel in anthropic-only with spec-panel-style verbosity: Sonnet about 23k plus 3 Haiku stand-ins at 68k-108k (LEDGER-RESULTS.md:66) gives 23 + 204 to 23 + 324 = **about 227k-347k for the parallel lane alone**, 4-7x the whole current T2 run. Reflect briefs are persona-scoped (refs/reviewer-spec.md:37-43), so reflect cards should be far shorter than spec-panel reports, but that is UNVERIFIED for Haiku stand-ins.

**When a full panel (more than 3 slots) is not worth calling:**

1. **Always in anthropic-only.** Extra slots are more Haiku copies. They add no model class (diversity stays 2 distinct ids) and leave vendor diversity single.
2. **Always in pre-execution.** It is advisory, has no revise step to turn findings into fixes, and the measured panel gain depended on the revise loop.
3. **When the rubric would stop at T1 anyway** (SKILL.md:362-366: `--tier 1`, `--depth quick`). The kernel is never called.

The only candidate case is gateway post-execution with `--depth deep`, where extra *vendors* could add independent class judgements. That is unmeasured and left for Stage 6 data.

## Risks

1. **The debate turns out to matter in pre.** The six recorded runs are a tiny sample, and convergence 1.0 may reflect correlated single-vendor reviewers rather than "nothing to arbitrate". *Mitigation:* the shadow stage and the first measurement compare both merges on identical cards; the flag default stays legacy until that passes; architecture E is the rollback.
2. **Contract 2.0.0 breaks a consumer nobody listed.** *Mitigation:* `panel` is only legal in pre; there is a grep entry criterion for `merge_method`, `contract_version` and `convergence` readers across `src/` and `tests/`; legacy runs under 2.0.0 emit only 1.8.0 values.
3. **Multi-file dedupe is wrong.** False merges hide a second defect; false splits inflate counts. *Mitigation:* Stage 0 replays recorded cards and hand-labels cluster correctness on a 50-pair sample. The ±3-line tolerance and the shared-file requirement are conservative toward splitting. A split costs a duplicate report line, not a lost finding.
4. **Executor exclusion silently weakened.** `distinct_across_slots` is soft (panel.py:405, 408) and fixed slots ignore exclusion (panel.py:402-403). *Mitigation:* `hard_exclude` raises instead of falling back and also covers fixed slots, with a unit test that excludes the fixed anchor's model.
5. **Reviewer format non-compliance.** An invalid findings-v2 block makes the reviewer non-clearing (enrichment gap 3), and a round with zero valid blocks is refused. *Mitigation:* one bounded re-ask per reviewer for the block only; then the F2 single-reviewer fallback. The `findings_schema` telemetry tracks the compliance rate per model.
6. **Gateway dispatch through the Agent tool is undefined** (review-tiers.default.json:20). *Mitigation:* the Stage 1 exit check; anthropic-only works today through `launch`; gateway agent-session stays on legacy until verified.
7. **Opus creep.** *Mitigation:* Opus appears only as the calibrator when the disjoint-set rule leaves nothing else (anthropic-only), and as a reviewer only via opt-in `@reflect-enterprise`. Kernel validation rejects Fable and Tier 0 ids.
8. **Two engines drift again.** *Mitigation:* both adapters consume the same resolution file and the same K3/K4 code. The contract builder for both should be one function (Stage 5 work item).

## First measurement

**Question:** in pre-execution, is the deterministic K4 merge non-inferior to the `/sc:adversarial` debate on the same reviewer cards, at lower cost?

**Design: paired, seeded, shared-card.**

- **Corpus:** 20 plan+spec pairs. Take real sc-workflow packages (`source.md` + `<id>.md`). Into each, inject 3 known defects with a script, so defects are known in advance and not derived from reviewer output (this avoids the ledger circularity noted at LEDGER-RESULTS.md:49):
  1. delete the task that covers one parsed requirement (coverage gap);
  2. add one out-of-scope task (scope creep);
  3. change one task's acceptance criterion so it contradicts the spec (contradiction).

  That gives 60 seeded defects.
- **Run:** reflect pre with `--tier 2 --t2-engine shadow` once per pair. Reviewers and calibrators run **once**, and both merges consume the identical calibrated cards. This isolates the merge, halves the cost and removes reviewer sampling noise from the comparison.
- **Metrics:**
  - **Recall:** the share of seeded defects present among validator-kept findings in the final merged output (debate merged verdict vs K4 clusters). This is the primary metric.
  - **Precision:** the share of final blocking findings that the evidence-validator kept and a blind Sonnet grader judges real. The grader sees only finding + citations, not the arm.
  - **Cost:** merge-lane output tokens.
  - **Agreement:** `reflect_status` equality between arms.
- **Sample-size reasoning:** paired binary outcomes per defect (found by arm X or not). With n = 60 and an assumed discordant-pair rate of about 10%, the standard error of the paired recall difference is about sqrt(0.10/60) ≈ 0.041. The one-sided 95% bound is 1.645 x 0.041 ≈ 0.067, which is inside a 0.10 non-inferiority margin. If the observed discordance exceeds about 20%, the SE rises to about sqrt(0.2/60) ≈ 0.058 and the bound to about 0.095, which is still inside the margin. Above that, extend to 30 pairs.
- **Cost of the experiment (estimate):** 20 x (about 49-96k legacy run + about 1.5k blocks + 0 K4) ≈ 1.0-1.95M output tokens.
- **Pass:** all four must hold:
  1. K4 recall ≥ debate recall − 0.10 (one-sided 95% bound);
  2. K4 precision ≥ debate precision − 0.10;
  3. merge-lane tokens cut by ≥ 80%;
  4. `reflect_status` agrees in ≥ 18 of 20 pairs.
- **Fail:** any bound crosses its margin. Then pre stays on the debate (architecture E for pre), and Stages 0-1 still ship for maintenance (dispatch unification), because they do not depend on this result.
- **Stage 0a, zero-dispatch first look:** convert the 5 recorded T2 runs' cards (enrichment section 4) to findings-v2 and run K4. Report cluster counts and agreement with their recorded merged verdicts. This is descriptive only and not a pass/fail input (n = 5, unseeded).

## Assumptions and UNVERIFIED items

**Assumptions (from the seed brief):** A-1 (design, measure first is acceptable), A-2 (shared model = one schema, one dispatch, one merge layer), A-3 (pre cites plan and spec, post cites source), A-4 (calibrated confidence stays per finding/card), A-5 (output tokens only), A-6 (no owner decision needed).

**Assumptions added here:**

- **A-7:** the wrapper (`cli/reflect/contract.py`, `runner.py`) is used only for post-execution. Basis: ensemble.py:797 hard-codes `"mode": "post"`. Other callers were not read.
- **A-8:** sc-workflow invokes reflect inside an agent session, so pre uses the agent-session engine (enrichment: skills/sc-workflow-protocol/SKILL.md:60-64).
- **A-9:** persona-scoped reflect cards stay far shorter than spec-panel reports. This drives the "full panel not worth it" estimate only as a lower bound.

**UNVERIFIED:**

- the exact option names of `superclaude review panel resolve` beyond `--run-id` (panel_cmd.py:39 read; other option lines not read) and whether `validate_panel` rejects unknown slot keys;
- `_decision` behavior with `--cap 1` (ledger.py `_decision` not read; reflect ignores it anyway);
- whether sc-adversarial accepts a judge-class exclusion or an extra context file with `--compare`;
- the body of `cli/reflect/fallback.py` and `cli/review/telemetry.py` (`review-telemetry/1` fields);
- whether grader.py or any test asserts `merge_method` values or a `contract_version` equality;
- whether the Agent tool accepts a ccsession tier alias (`claude-gw-tier2[1m]`) as a model override;
- the `judge_class_collision: true` record and the July `proxy_error` record (enrichment snippets only);
- the `reflect-reviewer` agent frontmatter (`model: sonnet`, `maxTurns: 50`, read-only tools) is taken from the enrichment file, not re-read here;
- `refs/cost-profile.yaml:46-70` and `docs/reference/review-panel-live7.md:19-26` are taken from enrichment, not re-read;
- every per-lane token split in the Cost model is an estimate; only the totals' bracket is checked against recorded artifact sizes.

**PROPOSED names introduced** (none exist today):

- templates: `review-panel.reflect-pre.json`, `review-panel.reflect-post.json`, `@reflect-enterprise`;
- K1: the tier-file `class` map, `hard_exclude`, `--exclude-class`;
- K3: `findings-v2` and its new fields;
- K4: `superclaude review merge --schema/--doc role=path/--calibration/--validation`;
- `superclaude review verify-citations`;
- the swarm lens input `--panel-resolution`;
- the reflect flag `--t2-engine legacy|shadow|panel`;
- contract fields `merge_engine`, `panel_resolution_path`, `panel_ledger_path`, `panel_agreement_score`, `panel_disputed_clusters`, `dispute_debate_ran`, `dispute_debate_convergence`, `findings_schema`, `citations_dropped_precheck`;
- the `merge_method` value `panel`;
- sidecars `panel/calibration.json` and `panel/validation.json`.
