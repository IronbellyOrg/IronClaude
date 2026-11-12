---
variant: 2
agent: sonnet:analyzer
generated: 2026-11-11T19:00:00Z
---

# Variant 2 (analyzer): panel-fed Tier 2 for /sc:reflect

Conventions. `path:line` cites are lines I read in this session. Paths are relative to `src/superclaude/` unless they start with `.dev/`. `<sr1>` abbreviates `.dev/research/346-review-loop-experiments/exp346/.dev/experiments/346-validation/phase5/final-bundle/builds/stoprule/brainstorm/workflow-report/nested/reflect-1`, one recorded pre-execution reflect run. "PROPOSED" marks a name or behaviour that does not exist today. "UNVERIFIED" marks anything I did not read. In the proposed design, installed primitives are named by installed path or by the `superclaude` CLI only.

## Summary

- Chosen: **stage-gated panel-fed T2**. The panel supplies reviewer resolution (tiers, deterministic slots, a new executor-exclusion filter), a shared finding carrier and deterministic clustering. Reflect keeps grounding, briefs, blind calibration, the evidence-validator gate, the tier rubric, remediation and promotion.
- The `/sc:adversarial` debate stays in 1.8.0 form but runs over the clustered table, not raw cards. It is removed only after a measurement, and that needs a versioned 1.9.0 contract.
- Headline reason: the panel does resolution and clustering, not dispatch, calibration or an evidence gate (`cli/review/panel_cmd.py:18-69`). Its measured gain is on specs with a reviser loop. Reflect T2 has no measured benefit and no reviser, so a full swap is not justified. A narrow swap is cost-neutral and gets cleaner reviewer composition.
- Pre-execution goes first, behind an off-by-default flag. Post-execution waits, because its deviation-class disputes feed promotion condition 4.
- The first experiment measures whether T2 beats T1 at all. The recorded runs cannot answer that.

## Candidate architectures

### A. Leave reflect as is
- Changes: nothing.
- Keeps: everything, including contract 1.8.0.
- Cost: 35k-70k Claude tokens per T2 run (cost-profile figure as quoted in the seed brief; I did not open the profile file).
- Risk, found in the recorded runs:
  - Vendor diversity was `single` in 5 of 5 T2 runs.
  - Model-class diversity was `degraded` in 2 of 5.
  - Convergence was 1.0 in 4 of 5 and 0.97 in the fifth.
  - Reviewer cards are not uniform: card 1 uses `severity: blocking|minor` with categories such as `ordering` (`<sr1>/reviewer-cards/reviewer-1-card.yaml:7-31`), while a card from another run uses `class: Drift`, `severity: HIGH` and a single `citation` (diffgate `reviewer-2-card.yaml:6-18`). Nothing deterministic clusters them, so the debate has to do all the matching.
- Verdict: the safe default and the baseline arm. It leaves known structural weaknesses (inconsistent cards, hand-rolled rotation, no deterministic overlap signal).

### B. Thin adoption: panel for resolution and telemetry only
- Changes: a reflect panel template plus tier file replace the hand-written rotation table (`skills/sc-reflect-protocol/SKILL.md:604-610`). `superclaude review panel resolve` picks reviewers and calibrator. Executor exclusion is added to `resolve` (PROPOSED).
- Keeps: reflect cards, the calibrator, `/sc:adversarial`, the validator, contract 1.8.0 with no value changes.
- Cost: about neutral. Resolution is a CLI call with no LLM tokens.
- Risk: low. It adds only a dependency on tier files and a changed seed rule.
- Verdict: justified by current evidence. It is stage 1 of the chosen path.

### C. Panel-fed T2 (chosen target)
- Changes: B, plus a shared finding carrier (`reflect-finding/1`, PROPOSED), reviewer output as a fenced findings block, `superclaude review merge` clustering, and the debate run over the cluster table.
- Keeps: grounding, coverage, blind calibration, evidence-validator, tier rubric, remediation, promotion, contract 1.8.0 values.
- Cost: reviewers +about 1k output tokens each for the block. The debate input shrinks. Net about neutral, between 5k saved and 3k added (see Cost model).
- Risk: medium. Clustering may undercount overlap on citation-heavy plan findings. Reviewers must emit a strict block.
- Verdict: chosen target, gated on the first measurement.

### D. Full replacement by the spec-panel review model
- Changes: findings-v1 everywhere, ledger rounds, a revise loop, no calibrator, no debate, no evidence-validator.
- Keeps: little of reflect's own mechanism.
- Cost: panel-shaped. The seed brief puts a 4-reviewer first review at about 314k tokens, which is 4.5x to 9x a T2 run (314/70 = 4.5; 314/35 = 9.0).
- Risk: high.
  - The PN1 gain (15.7 of 44 ledger defects fixed vs 2.8 for baseline) is a loop gain over specs with a reviser (`.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19`).
  - Reflect is advisory and never edits the plan (`<sr1>/REPORT.md:21`).
  - The panel has no evidence gate and no calibration, so dropping reflect's gates fails the hard constraint.
- Verdict: rejected.

### Comparison

| Option | Contract 1.8.0 | Cost vs today | Evidence for it | Main risk | Verdict |
|---|---|---|---|---|---|
| A. Leave as is | stable | 0 | none needed | known weaknesses stay | baseline arm |
| B. Resolution only | stable | about 0 | composition rule gaps are real (executor exclusion absent in panel, `cli/review/panel.py:380-427`) | tier files carry gateway-only dispatch gaps | stage 1 |
| C. Panel-fed + debate over clusters | stable | -5k to +3k | cards are non-uniform; the debate score was flat | overlap undercount, block compliance | chosen target, gated |
| C2. C without debate | needs 1.9.0 | -8k to -15k more | debate score never separated runs (1.0 in 4 of 5) | post-exec class disputes unresolved | optional later |
| D. Full replacement | breaks gates | 4.5x-9x | panel gain is spec-only | drops calibration and evidence gate | rejected |

## Chosen architecture and reasons

Name: **stage-gated panel-fed T2** (B now, C after measurement, C2 only on evidence).

**Reason 1: the panel gives resolution and clustering, not a pipeline.**
- `superclaude review panel` has only `resolve` and `validate` (`cli/review/panel_cmd.py:18, 69`). `superclaude review merge` takes one `--doc`, reviewer reports and a ledger (`cli/review/merge_cmd.py:21-71`).
- Neither dispatches agents. Dispatch lives in the coordinator prompt. Reflect already has dispatch: agent sessions, and a swarm lens that is post-only (see Q4).
- So the panel can take over composition and matching, and nothing else.

**Reason 2: calibration and the evidence gate carry load the panel cannot replace.**
- Card 1 shows calibration working. Reviewer 1 marked F1-F3 `blocking`. The blind calibrator scored them 0.60, 0.50 and 0.55 and noted "F1-F3 fit major better than blocking" (`<sr1>/reviewer-cards/reviewer-1-card.yaml:88-90, 101`).
- The final gate dropped `source.md:143` because the line was a section heading that did not support the claim (`<sr1>/REPORT.md:130-132`).
- A deterministic "quote locates" test (the panel's `locate`/`annotate`, `cli/review/findings.py:276-360`) would pass that citation, since the line exists. Only a semantic re-read catches it. So the validator stays and the anchor check is added in front of it, not instead of it.

**Reason 3: the debate's contribution is not evidenced.**
- Convergence was 1.0 in 4 of 5 T2 runs and 0.97 in one (seed brief; return contracts show 0.97 at `<sr1>/../return-contract.yaml`, grep line 40).
- In the same stoprule run the debate settled items as not-a-defect (C-007, C-017, C-019, `<sr1>/REPORT.md:84-87`). That is one run of anecdotal value. A deterministic merge would not reclassify.
- Without evidence either way, the safe step is to keep the debate and shrink its input. Removal waits for the measurement.

**Reason 4: the panel does not fix the vendor problem in an Anthropic-only environment.** There every non-Sonnet tier resolves to a Haiku stand-in (`cli/review/data/review-tiers.default.json:25-29`). Single-vendor stays single-vendor. The gain shows only in the gateway environment (`review-tiers.default.json:19-24`).

**Reason 5: it respects every hard constraint.** Contract 1.8.0 values do not change in stages 1-2. Calibration and the validator stay. No Fable. Opus is used in exactly one place, the calibrator.

## Answers to Q1-Q7

### Q1. What the panel can take over, lacks, and what stays in reflect

**Direct answer.** The panel can take over reviewer composition and deterministic clustering. It cannot take over dispatch (it has none), calibration, the evidence gate, executor exclusion or multi-document anchors. Those stay in reflect or must be added.

| Piece | Panel today | Verdict |
|---|---|---|
| Reviewer pool, model diversity | tiers, slots, `distinct_across_slots`, stand-ins per environment (`cli/review/panel.py:380-524`) | take over |
| Deterministic reproducibility | resolution records `template_sha256`, `tiers_sha256`, seeds (`panel.py:514-524`) | take over; feeds telemetry |
| Parallel dispatch | none; the panel only prints a resolution (`panel_cmd.py:53-66`) | stays in reflect (agent spawn / swarm) |
| Merge | clustering by whitespace-flattened quote, section, refs, span overlap (`findings.py:276-407`) | take over, as the first stage of merge |
| Telemetry | `review-telemetry/1` (function names only, `cli/review/telemetry_cmd.py:15-77`; schema body UNVERIFIED) | adopt in stage 2 |
| Executor-class exclusion | absent; `exclude` is only the models already chosen in this panel (`panel.py:479`) | add (PROPOSED), reflect keeps the rule and the degrade |
| Personas | absent | stay in reflect briefs |
| Blind calibration | absent | stays in reflect |
| Evidence-validator gate | absent | stays in reflect |
| Per-finding confidence, deviation class, coverage rows | absent from findings-v1 (`findings.py:90-121`) | carried by the finding format below |
| Multi-document citations | one document per merge (`merge_cmd.py:29-34`) | handled by the finding format and an audit bundle |

Must stay in reflect, per the hard constraints: code grounding, coverage mapping, deviation classification, the tier-decision rubric, remediation, promotion, executor-class resolution (flag, env var, log heuristic, `SKILL.md:600-602`), brief materialization (`refs/reviewer-spec.md:33-78`), blind calibration and the evidence-validator.

One implementation gap matters. `resolve_slot` for a `fixed` slot returns `candidates[0]` and ignores `exclude` (`panel.py:402-403`). For `random` and `round_robin` slots it falls back to all candidates if the pool empties (`panel.py:405, 409`). So an exclusion extension must filter candidates before the strategy runs, and must report a collision, not hide it.

### Q2. Finding format

**Direct answer.** Use a superset of findings-v1, `reflect-finding/1` (PROPOSED). The panel's required fields are unchanged so `parse_block` accepts it. Reflect fields ride in the same JSON line. The full per-finding content is also kept in a sidecar card keyed by `(reviewer_id, fid)`. See "Finding format" below.

The superset works because `_check_finding` validates only the panel's own keys and leaves other keys alone (`findings.py:90-121`), and `parse_block` returns the parsed object (`findings.py:188-195`). One limit: ledger rows keep only a fixed set of fields (`cli/review/ledger.py:184-203`), and members keep only `round`, `reviewer_id`, `fid`, `blocking` (`ledger.py:172-179`). Extra fields do not survive into the ledger. So reflect joins its sidecar through the ledger's member records.

### Q3. Merge: debate, deterministic merge, or both

**Direct answer.** Both, in sequence. Deterministic clustering runs first. The debate then runs over the cluster table (stage 2, contract unchanged). A conflict-only or no-debate merge (C2) is a later, versioned step, taken only if the first measurement shows the debate adds nothing.

What clustering gives that the debate does not: a reproducible overlap signal (`single` or `overlap`, `ledger.py:86-90`) and stable identity across reviewers. What it lacks: a judge, reclassification and invariant probing.

Lost without the debate, pre-execution:
- Settlement of disputed items (three not-a-defect settlements in one run, `<sr1>/REPORT.md:84-87`).
- Consolidated claim text, with several findings merged into one row (C-004 in that report carries three combined claims).
- A judge of a different class than the reviewers (`SKILL.md:612`).
- Mitigating fact: the pre-execution report is advisory and never edits the plan (`<sr1>/REPORT.md:21`), and `sc-workflow` reads only `reflect_status` and `reflect_report_path` (seed brief). A false positive costs a reader's minute, not a bad edit.

Lost without the debate, post-execution:
- Class disagreements (one reviewer says Drift, another Necessary) feed promotion condition 4 (`SKILL.md:1472`). Clustering can detect a conflict but cannot resolve it. A judge is needed, so the debate stays for conflict clusters at minimum.
- A recorded post run shows `convergence_score: 0.836` with `judge_class_collision: true`. This is a search snippet that I did not read (UNVERIFIED), but it shows post-execution disputes are real.

### Q4. Engine: agent sessions, swarm, or both

**Direct answer.** Both, chosen per reviewer by the resolution's `launch` field. Pre-execution uses agent sessions, because the headless ensemble is post-only. The swarm is used for gateway models that agent sessions cannot launch.

Facts I read:
- The headless contract builder hard-codes `"mode": "post"` (`cli/reflect/ensemble.py:797`). The swarm `reflect-review` lens and `run_tier2_ensemble` serve post-execution only.
- Pre-execution T2 runs as a skill with `reflect-reviewer` agents (`SKILL.md:592, 633`), launched by `sc-workflow` Wave 4 (seed brief).
- Tier file `launch` is populated only in the Anthropic-only environment: `{"claude-opus-5-5": "opus", "claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", ...}` (`review-tiers.default.json:29`). In the gateway environment `launch` is `{}` and the note says "dispatch mechanism per model not defined yet" (`review-tiers.default.json:20`).

Rule (PROPOSED):
- `launch` non-null: spawn the read-only `reflect-reviewer` agent session with that model alias.
- `launch` null (gateway models): run a swarm worker. The adapter exports the resolved ids as the `T2Model01..03` pool the lens already reads (lens facts from the enrichment file; invocation details UNVERIFIED), then collects the report.
- Explicit `T2ModelNN` env values stay the override and win over the resolution. This preserves today's behaviour.

How tiers relate to reflect's rotation (PROPOSED mapping):

| Reflect rotation entry | Panel slot |
|---|---|
| sonnet (anchor) | `t1b`, fixed, head of tier1b = Sonnet (`review-tiers.default.json:6`) |
| haiku | `t3`/`t4` slot; in Anthropic-only the Haiku stand-in |
| qwen / kimi / deepseek, else opus | `t2` slot in gateway (list at `review-tiers.default.json:7`); a second Haiku stand-in in Anthropic-only, with degraded diversity flagged |
| calibrator (class disjoint) | fixed `cal` slot, tier1a, head = Opus (`review-tiers.default.json:5`) |

Slot order helps. Fixed slots resolve first (`panel.py:447-448`), so the calibrator is chosen first and the reviewers exclude its model when `distinct_across_slots` is true (`panel.py:479`). That enforces calibrator-vs-reviewer disjointness mechanically, where today it is a prose rule (`SKILL.md:583, 600`). The adapter must still re-check disjointness after resolution, because the `or candidates` fallback can collide silently (`panel.py:405`).

### Q5. Pre-execution migration, end to end

**Direct answer.** The plan and its source spec go in. Reflect's Wave 0-2 are untouched (T1, grounding, coverage). Reviewers come from `reflect-pre` resolution, each emits a findings block plus a card, `superclaude review merge` clusters them against the plan, a blind calibrator grades each card, the debate runs over the cluster table, and the evidence-validator gates the result. The return contract is produced as today. The numbered flow is under "Adapter sketches".

Return-contract fields produced: all of the 1.8.0 stable block. See the mapping table. The only additions are telemetry fields.

### Q6. Rounds, ledger and revise loop

**Direct answer.** Reflect stays single-pass. It uses the ledger machinery for one round only, to get clusters and the overlap label.

Reasons:
- There is no reviser. Reflect never edits the plan (`<sr1>/REPORT.md:21`). The loop's measured gain comes from find, fix and re-verify (`LEDGER-RESULTS.md:41-43`), so it does not transfer.
- `merge_round` computes a PASS/FAIL verdict on blocking rows and a REVISE/ESCALATE decision with cap 3 (`ledger.py:93-96, 274-285`). Reflect ignores both. Its verdict comes from the tier rubric and the contract.
- Ledger value across runs (finding identity when the plan regenerates, or when post-execution re-audits after remediation) is real but unmeasured. Mark it optional and later.
- `merge_round` raises when no reviewer has a valid block (`ledger.py:150-157`). That maps onto reflect's existing loud-fallback path (F2/F3), so it is compatible.

### Q7. Cost, and when a full panel is not worth calling

**Direct answer.** The chosen design costs about the same as today (see Cost model). A full panel (4-7 reviewers, rounds) is not worth calling for pre-execution advisory review by default. The call rule is in the Cost model section.

## Finding format

Name: `reflect-finding/1` (PROPOSED). One JSON object per line inside a fenced block with info string `findings-v1` under the heading `## Findings block`. The reuse of the info string is deliberate: it lets `parse_block` run unchanged (`findings.py:31, 124-196`). A reflect-only consumer reads `schema` to tell the variants apart.

Panel-required fields, unchanged (`findings.py:90-121`):

| Field | Rule | Reflect mapping |
|---|---|---|
| `id` | `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, unique | card finding id (F1, QA-001) |
| `severity` | CRITICAL / MAJOR / MINOR | `blocking`->CRITICAL or MAJOR; `HIGH`->MAJOR; `MEDIUM`/`minor`->MINOR (graded by consequence, not by reflect's old label) |
| `blocking` | boolean; MINOR cannot be blocking | card's blocking flag |
| `category` | closed set of 6 (`findings.py:15-22`) | nearest map: `ordering`->`other`; `acceptance`->`unpassable-check`; `coverage`->`missing-requirement`; `contradiction`->`contradiction`; `risk`->`safety` or `other`. Original kept in `reflect_category`. |
| `anchor` | 12-200 chars, quoted from the document under review | quote from the plan (pre) or the audit bundle (post) |
| `anchor2` | optional, same rule | quote from the second cited document or file |
| `refs` | at most 8 strings | coverage-row ids (INF-007, C-018), requirement ids, section numbers |
| `claim` | at most 300 chars | card `claim`/`finding` text, shortened |

Reflect additions, extra keys that `parse_block` leaves alone:

| Field | Meaning | Source |
|---|---|---|
| `schema` | `"reflect-finding/1"` | constant |
| `mode` | `pre` or `post` | run |
| `doc` | `plan`, `bundle` | which document `anchor` quotes |
| `cites` | list of `{path, start, end, role}`; `role` = `anchor` or `evidence`; any number of files | card `evidence` / `citation` |
| `deviation_class` | authorized, necessary, drift, regression, none | card (`SKILL.md:816`); `none` in pre mode unless the pre taxonomy applies |
| `reflect_category` | original category label | card |
| `coverage_rows` | ids of coverage rows touched | coverage slice |
| `persona` | analyzer, qa, refactorer | brief |
| `recommendation` | reviewer fix text | card |

**Calibrated confidence is not in the reviewer line.** The blind calibrator must not see other reviewers' output and must not be steered by the panel's `single`/`overlap` label. It writes `finding_confidence` (per finding) and the card-level calibrated number to a sidecar `calibration/<reviewer_id>.yaml`, as it does now (`<sr1>/reviewer-cards/reviewer-1-card.yaml:82-103`). The adapter joins sidecar rows to clusters afterwards. A cluster reports both its panel label and the member finding confidences, and never merges them into one number.

**Dedupe key.** The key is the panel fingerprint, `sha256("v1|" + section + "|" + refs_norm)[:16]` (`findings.py:340-343`), plus span overlap within 3 lines on either anchor span (`findings.py:363-379`).
- `section` is the nearest heading of the `anchor` quote (`findings.py:307-318`).
- `refs_norm` uppercases ids that match `[A-Z]{1,4}-[0-9]+` or `P[0-9]` (`findings.py:29, 321-337`). Reflect's coverage ids `INF-nnn` and finding ids `C-nnn` match this pattern, so reviewers must put them in `refs`.
- A shared fingerprint matches only when `refs_norm` is non-empty (`findings.py:371`). With no refs it falls back to span overlap (`findings.py:374-379`).

How multi-file citations fit:
- **Pre-execution.** The anchor document is the plan. Spec lines go into `anchor2` (a quote from the spec) and `cites`. `merge_round` annotates `anchor2` against the same document text, so a spec quote only yields a span if the text appears in the plan. The adapter handles this by concatenating the plan and the spec into one numbered review document `review-doc.md`, with H2 sections `## PLAN` and `## SPEC`. Both anchors then locate, with sections that differ by document.
- **Post-execution.** The adapter builds `audit-bundle.md`: each grounding hunk as an H3 `path:start-end` heading with its fenced code, which reviewers already receive in this shape (`refs/reviewer-spec.md:45`). The slug of that heading becomes the section, so two reviewers citing the same hunk share a section. A defect that spans two files uses `anchor` and `anchor2`. A third file or more goes only into `cites`, and the evidence gate validates it (anchor matching never sees it).

## Adapter sketches

### Pre-execution adapter (stage 1-3)

Inputs: tasklist `<pkg>/<id>.md`, source spec `<pkg>/source.md`, optional `--executor-model`. This is the call `sc-workflow` Wave 4 makes today (seed brief): `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`.

1. Wave 0-2 as today: T1 card, grounding, coverage map (the Step 1B.0 two-pass extraction), tier rubric. Stop if the rubric says T1.
2. Resolve (PROPOSED flags): `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --exclude-model <executor class models>`. Capture `resolution.json` with the template and tier hashes. If the exclusion cannot satisfy N=2, emit `executor_exclusion_degraded: true` and degrade to T1, as today (`SKILL.md:600`).
3. Build `review-doc.md` (plan, then spec, as above) and one brief per reviewer. The brief keeps exactly three sections (`refs/reviewer-spec.md:31-78`), plus one added instruction: end the report with a `## Findings block`, using the schema above.
4. Dispatch, per reviewer by `launch`: agent session (`reflect-reviewer`) or swarm worker. The persona comes from a reflect-owned slot-to-persona map (analyzer, qa, refactorer), so the panel schema is unchanged.
5. Collect reports. Run `superclaude review merge --ledger <out>/ledger.json --doc <out>/review-doc.md --round 1 --report <rid>=<path> ... --resolution resolution.json --out <out>/merged.md`. Keep only the clusters, not the PASS/FAIL verdict.
6. Blind calibration: one `confidence-calibrator` per card, with a model from the `cal` slot. Each calibrator sees one card and the grounding, never the other cards or the cluster labels.
7. Debate: `Skill sc-adversarial-protocol --compare` over the cluster table (merged cards plus labels) with `--depth standard`, the same call shape as `SKILL.md:645-651`. Read the `artifacts_dir` remap rule (`SKILL.md:657`) as today. EV-1 on-disk check unchanged (`SKILL.md:666`).
8. Evidence gate, first mechanical then semantic:
   - Deterministic pre-check: for each finding, `annotate` reports `anchor_status` found or missing (`findings.py:346-360`); every `cites` path exists and the line range is inside the file. Missing items are dropped or flagged before the validator runs.
   - Then the `evidence-validator` agent re-Reads every cited file:line as today (`SKILL.md:587`, final gate).
9. Write REPORT.md and `return-contract.yaml` (see the mapping). `reflect_report_path` and `reflect_status` are what `sc-workflow` records.

### Post-execution adapter (stage 4)

Inputs: spec, tasklist, task log, diff, optional `--executor-model`.

1. Wave 0-2 as today (grounding, verification run, deviation candidates).
2. Resolve with the executor exclusion. This matters more here, because self-confirmation is the mechanism the exclusion rule defends (`SKILL.md:600`).
3. Build `audit-bundle.md` (hunks as H3 `path:range`), briefs and the findings block instruction.
4. Dispatch as above. The swarm path (`cli/reflect/ensemble.py:296-511`) remains for headless runs. The wrapper contract builder stays.
5. `superclaude review merge` clusters on the bundle.
6. Blind calibration per card.
7. Debate on clusters whose members disagree on `deviation_class` or `blocking`, and on any single-source blocking cluster. Stage 4 keeps the full cluster-table debate; C2 later narrows it.
8. Evidence gate as in pre-execution, including the verification-results hunk (`refs/reviewer-spec.md:53`).
9. Deviation counters (`deviation_count_by_class`) come from adjudicated clusters. Promotion gate, remediation (Wave 6) and promotion (Wave 7) are untouched.

## Staged migration

| Stage | What changes | Entry | Exit | Rollback |
|---|---|---|---|---|
| 0. Measure | nothing ships; run the first measurement | this design accepted | result decides whether stage 1 proceeds | none needed |
| 1. Resolution only, pre-exec, flag `--panel-resolve` (PROPOSED, off by default) | `reflect-pre` template, tier lookup, `--exclude-model`; reviewers dispatched as today; cards and debate as today | stage 0 shows panel-fed arm not worse than current | 20 consecutive pre-execution runs with identical contract field sets and no new wrapper degrade reason | flag off; the hand-written rotation still exists |
| 2. Carrier plus clustering, flag `--panel-merge` (PROPOSED) | `reflect-finding/1` blocks, `review merge` clusters, debate over cluster table | stage 1 exit | 30 runs; overlap undercount below 20% against a manual spot-check of 10 runs; block compliance at least 95% | flag off |
| 3. Default on for pre-exec | flags default true | stage 2 exit plus owner approval | one release of clean runs | flag flip back |
| 4. Post-exec adapter, flag `--panel-post` (PROPOSED) | bundle, executor exclusion, class-conflict adjudication | stage 3 plus a separate post-exec measurement | agreement of promotion decisions with the current mechanism on at least 20 recorded audits | flag off |
| 5. Optional C2 | conflict-only or no debate; contract 1.9.0 | measurement shows debate adds nothing | consumer updates merged (see mapping) | restore 1.8.0 path |

Stage 5 needs a versioned change because EV-2 makes any `merge_method` other than `adversarial` or `single-reviewer-fallback` MALFORMED (`SKILL.md:666, 789`).

## Return-contract 1.8.0 mapping

Stages 1-4 keep every 1.8.0 field name, type and legal value. Stage 5 would be an additive 1.9.0.

| Field | Source in new design | Stages 1-4 | Stage 5 (1.9.0) |
|---|---|---|---|
| `contract_version` | constant | "1.8.0" | "1.9.0" |
| `status`, `mode`, `tier_reached`, `report_path`, `audit_log_path` | reflect | unchanged | unchanged |
| `confidence_calibrated` | mean of calibrated card values (as in `<sr1>/REPORT.md:25`) | unchanged | unchanged |
| `reviewer_cards` | card paths; each card also has a findings block | unchanged | unchanged |
| `adversarial_artifacts_dir` | debate output dir, remapped from `artifacts_dir` (`SKILL.md:657`) | unchanged | null when no debate ran |
| `adversarial_convergence_score` | debate over the cluster table | unchanged (still a debate number) | null when no debate ran; see null rules |
| `adversarial_unavailable` | F3 path | unchanged | unchanged |
| `merge_method` | `adversarial` or `single-reviewer-fallback` | unchanged | adds `panel-deterministic` (EV-2 edited) |
| `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity` | computed from resolved model ids with the same helpers (`cli/reflect/_diversity.py`, seed brief) | unchanged | unchanged |
| `calibrator_diversity` | from resolution; disjointness re-checked after resolve | unchanged | unchanged |
| `citations_total`, `citations_revalidated`, `citations_dropped`, `evidence_validator_ran` | validator, now after a deterministic pre-check | unchanged | unchanged |
| `deviation_count_by_class`, `regression_present`, `unauthorized_deviation_present` | reflect; post-exec from adjudicated clusters | unchanged | unchanged |
| new telemetry (non-stable block): `panel_template_id`, `panel_template_sha256`, `panel_tiers_sha256`, `panel_env`, `clusters_total`, `clusters_overlap`, `clusters_conflict` | resolution and clustering | added, telemetry only | stable `merge_agreement_score` (PROPOSED) |

Null-score rules:
- Stages 1-4: unchanged. A T2 run with `adversarial_unavailable: true` has null convergence, routes on `merge_method` first, and blocks promotion (`SKILL.md:659-664`).
- Stage 5: a deterministic merge has no debate score. Add `merge_agreement_score` (the share of clusters with no member conflict; PROPOSED, 0.0-1.0). Consumers route on `merge_method` first. `panel-deterministic` uses the agreement score; `adversarial` uses the convergence score. A null convergence with `merge_method: panel-deterministic` is then not an error.

Promotion gate condition 9 (`SKILL.md:1483`, maps to `gate_evaluation.adversarial_result_present`):
- Stages 1-4: unchanged text.
- Stage 5: reword to "a Tier 2 run needs a merged verdict, either adversarial or panel-deterministic". The gate key keeps its name.

Consumers, one by one:
- **`sc-workflow` Wave 4**: reads only `reflect_status` and `reflect_report_path` (seed brief). Unaffected at every stage.
- **Wrapper and sprint verdict map** (`cli/reflect/contract.py:224-358`): reads `merge_method`, `adversarial_convergence_score`, diversity fields, `citations_dropped`. Stages 1-4 unchanged. For stage 5, change trigger 10 (`merge_method == single-reviewer-fallback`, `contract.py:295`) and triggers 11 and 11b (null or below 0.80, `contract.py:299, 317-326`) so they apply only when `merge_method == adversarial`. Otherwise a deterministic-merge run is degraded for having no debate score.
- **Headless builder** (`cli/reflect/ensemble.py:772-773, 806-807`): sets `merge_method` from the reviewer count. Update for stage 5.
- **Skill text**: EV-1, EV-2 (`SKILL.md:666, 789`), the field comment, and `refs/report-template.md` (not read).
- **Sprint executor routing**: `SKILL.md:664` says null convergence routes to `status: partial` and `next_action: halt-phase-for-review`. The executor code was not read (UNVERIFIED); it must be checked in stage 5.
- **Troubleshoot and auggie-review**: consume `reflect_status` and `reflect_report_path` only (enrichment file); unaffected.

`reflect_post` frontmatter: the wrapper writes it from a `ReflectResult` and replaces only the `reflect_post:` block of the tasklist (`cli/reflect/runner.py:103-175`, builder and writer read; the middle of `_build_reflect_post_value`, lines 110-133, only partly). This design adds no `ReflectResult` fields, so the block is unchanged through stage 4. Stage 5 adds `merge_method` visibility only if an owner asks; I have not verified whether `reflect_post` carries `merge_method` (UNVERIFIED), so check it before stage 5. It is written only after post-execution runs and is not touched by the pre-execution adapter.

## Cost model

All token figures are output-token estimates in the manner of the 346 experiments (assumption A-5). The before total is the cost profile's 35k-70k Claude tokens for T2 as quoted in the seed brief (the profile file itself was not opened). The lane split below is **my assumption**, chosen so the lanes sum to the profile total.

Before (3 reviewers, today):

| Lane | Low | High | Arithmetic |
|---|---|---|---|
| Primary: anchor reviewer (Sonnet) plus other reviewers | 18k | 36k | 3 reviewers x 6k-12k |
| Calibrator (Opus today, one per card) | 6k | 12k | 3 x 2k-4k |
| Debate / merge (`/sc:adversarial`) | 8k | 15k | assumed |
| Evidence-validator | 3k | 7k | assumed |
| Total | 35k | 70k | 18+6+8+3 = 35; 36+12+15+7 = 70 |

After stage 2 (3 reviewers, chosen design):

| Lane | Low | High | Change from before |
|---|---|---|---|
| Reviewers, plus findings block | 21k | 39k | +1k each x 3 |
| Deterministic merge | 0 | 0 | CLI, no LLM tokens |
| Calibrator | 6k | 12k | unchanged (blind, kept) |
| Debate over cluster table | 5k | 10k | assumed smaller input; between 60% and 70% of before |
| Evidence-validator (after deterministic pre-check) | 3k | 7k | unchanged; the pre-check is free |
| Total | 35k | 68k | 21+6+5+3 = 35; 39+12+10+7 = 68 |

Net: 0 to -2k. The assumption on debate size is the weak point. If the debate does not shrink, the cost is +3k (the findings blocks). The migration's argument is composition and consistency, not savings.

After stage 5 (no debate on agreement, conflict-only adjudication of about 0-3 clusters at about 2k each, 0-6k): total 30k-63k (21+6+0+3 = 30; 39+12+6+7 = 64, rounded; treat as about 30k-64k). Saving against stage 2 is 5k-4k, so small. This is why C2 is optional.

For reference, the panel: the first review of 4 reviewers measured about 314k (Sonnet 23k + 3 Haiku at 68k-108k each, seed brief); PN1 loop total 408,316 output tokens, with 71% in the Haiku stand-in lane (`LEDGER-RESULTS.md:55-66`). Haiku stand-ins wrote far more than the Sonnet reviewer, so reflect's reviewer lane could also grow if its stand-in model is verbose. That is a risk to the +1k figure, not a measured number.

When a full panel is not worth calling:
- Pre-execution runs on every `/sc:workflow` plan as an advisory step. A 4-reviewer panel at about 314k is 4.5x to 9x a T2 run (314/70, 314/35), for a benefit that is unmeasured and with no reviser to use the findings.
- Rule (PROPOSED): keep T1 when the rubric says T1. Use the 3-reviewer T2 when the rubric says T2. Offer a 4-plus reviewer panel only on an explicit `--depth deep` request, and only after the first measurement shows T2 recall beats T1 by at least 15 percentage points and the larger panel beats T2 by a further margin the owner accepts. The 1S+6H vs 1S+3H result (about 3 extra fixed defects on one spec, `docs/reference/review-panel-live7.md`, not re-read this session) is thin evidence for scaling reviewers.
- In an Anthropic-only environment, prefer 2 reviewers plus an Opus calibrator, which is fully disjoint, over 3 reviewers with two Haiku stand-ins. That cuts the reviewer lane by one third (6k-12k) and the calibrator lane by one third (2k-4k). The first measurement tests this as an ablation.

## Risks

1. **Overlap undercount in clustering.** Plan findings cite many lines; two reviewers may anchor the same defect in different tasks, so no span overlap occurs and no overlap is recorded. Mitigation: require coverage-row and finding ids in `refs` (fingerprint match, `findings.py:371`), use `anchor2`, and spot-check 10 runs by hand before stage 3. In specs with no labelled requirement ids the stoprule run had zero (`<sr1>/REPORT.md:23`), so matching leans on span overlap.
2. **Block compliance.** Today cards are YAML and vary by reviewer (see candidate A). A strict JSON-lines block is a new burden, and a Haiku-class reviewer may truncate. `merge_round` skips an invalid-block reviewer for clearing but keeps its parsable findings (`ledger.py:111-112`). Mitigation: count only valid-block reviewers toward the N=2 floor, and add the loud fallback when none is valid.
3. **Blind calibration leakage.** If cluster labels reach the calibrator it stops being blind. Mitigation: calibrators run before the debate and receive only their own card.
4. **Evidence gate coverage.** New fields (`cites`, `anchor2`) must be inside the validator's scope, or the gate gets weaker. Mitigation: the validator reads `cites` and `anchor2` quotes; the pre-check is added in front, not instead.
5. **Closed category set.** Reflect's categories map lossily onto six values. Mitigation: `reflect_category` is kept in the line and the sidecar.
6. **Gateway dispatch undefined.** `launch` is `{}` for gateway models (`review-tiers.default.json:20`). Mitigation: swarm path for null `launch`; in a first release restrict the flag to environments where every resolved model has a launch alias.
7. **Forbidden models in tier data.** The Anthropic-only environment lists a Fable model in `available` and `names` (`review-tiers.default.json:14, 27`), and no tier alias lists it. Mitigation: add a forbidden-model filter to `resolve` (PROPOSED) and never pass `fable` to an agent model override.
8. **Evidence does not transfer.** The panel's gain is on specs with a reviser; reflect has neither. Mitigation: first measurement; stage 1 gated on it.
9. **Existing headless gap.** The headless builder hard-codes `verification_ran: false` and `citations_dropped: 0` (`cli/reflect/ensemble.py:808-817`), so the wrapper's citation trigger (`contract.py:347-352`) cannot fire there. The migration does not fix this. Flag it for a separate task.
10. **Executor exclusion can empty a fixed slot.** With Sonnet excluded in the Anthropic-only environment, tier1b has no model, and there is no tier1b stand-in (`review-tiers.default.json:28`). `resolve_slot` would raise `NoModelAvailable` (`panel.py:396-401`). The exclusion extension must drop the slot and report, not raise.

## First measurement

**Question.** Does T2 beat T1 on plans, and does the panel-fed T2 hold that benefit at equal or lower cost? Neither is known today. Six recorded runs show agreement, not quality.

**Design.** Three arms over the same plans: T1 only; current T2; panel-fed T2 (stage 2 design, debate kept).
- Plans: 12 plan-plus-spec pairs. The 5 recorded pre-execution plan packages are reusable (recorded under the phase5 bundle); add 7 fresh plans from `/sc:workflow` runs.
- Ground truth, two sources:
  1. Seeded defects: inject 5 known defects per plan, one each of ordering, missing acceptance, spec-uncovered requirement, wrong file path and cross-task contradiction. This gives 60 defect instances per arm with known truth.
  2. A union ledger of natural findings, scored as in the 346 method (Sonnet scorer, Opus agreement 96% on 264 judgements, `LEDGER-RESULTS.md:53`). That method's circularity caveat applies (`LEDGER-RESULTS.md:49`).

**Metrics.**
- Seeded-defect recall per arm.
- Validator-confirmed false-positive rate: dropped citations / total citations.
- Output tokens per run, by lane.
- Overlap undercount (manual spot-check of clusters).
- Calibration quality: correlation of `finding_confidence` with scorer-confirmed truth.

**Sample size reasoning (arithmetic, illustrative).** 12 plans x 5 seeded defects = 60 paired instances. If the arms disagree on about 25% of instances (15 discordant pairs) and the panel-fed arm wins 12 of them, an exact McNemar test gives a one-sided p of about (455 + 105 + 15 + 1) / 32768 = 576 / 32768 = 0.018, so about 0.035 two-sided. That detects roughly a 15-point recall gap (9 net wins of 60). It cannot detect smaller gaps. If the discordance is lower, the test is weaker; say so in the result.

**Pass/fail thresholds (PROPOSED).**
- Stage 1 proceeds only if panel-fed T2 recall is within 5 points of current T2 (non-inferiority), the validator-confirmed false-positive rate is not higher, and cost is at most 1.1x current T2.
- T2 itself is worth its cost on pre-execution only if T2 recall beats T1 by at least 15 points. If not, record that the 35k-70k are not buying recall on plans, and shrink T2 to 2 reviewers instead of migrating.
- C2 (stage 5) proceeds only if the debate arm's seeded recall is not better than the no-debate arm's by more than 5 points and the debate arm is at least 8k tokens dearer.

## Assumptions and UNVERIFIED items

Assumptions (from the seed brief, A-1 to A-6, restated where I rely on them):
- A-1: a design, not a ship decision; "measure first" is acceptable.
- A-2: "shared review model" means one finding schema, one resolution layer and one clustering layer, with reflect-specific briefs and gates on top.
- A-3: pre-execution findings cite plan lines and spec lines (two documents); post-execution findings cite source files and hunks.
- A-4: calibrated confidence stays per finding and per card.
- A-5: token cost is output tokens.

My additional assumptions:
- The lane split of the 35k-70k T2 total in the Cost model is my own. Only the total is from the profile.
- The debate over cluster tables is 60% to 70% of today's debate cost. No measurement.
- Reviewers add about 1k tokens for the findings block.
- The adapter can concatenate plan and spec into one review document without harming reviewers' ability to cite real files.

UNVERIFIED (not read this session):
- Cost-profile file `refs/cost-profile.yaml` (figures quoted from the seed brief).
- SKILL.md section 9.4 (additive-only rule for minor versions) and `refs/report-template.md`; whether new telemetry fields are allowed in the telemetry block without a version bump.
- The body of `cli/reflect/runner.py` beyond lines 103-175, and whether `reflect_post` carries `merge_method`.
- `cli/reflect/fallback.py` (fallback ladder) and the swarm lens invocation details (`T2Model0N` handling is from the enrichment file).
- Sprint executor routing code (`SKILL.md:664` names `executor.py`, I did not open it).
- The `/sc:adversarial` judge selection and how it computes convergence; the post-execution recorded verdict (`convergence_score: 0.836`, `judge_class_collision: true`) is a search snippet only.
- The `review-telemetry/1` schema body (`cli/review/telemetry_cmd.py` read by option list only).
- `docs/reference/review-panel-live7.md` (the 1S+6H vs 1S+3H figure is from the seed brief).
- Model identifiers in tier files are as read in `review-tiers.default.json`; the design uses tier names (tier1a, tier1b, tier2, tier3) and does not rely on any id.
- Whether `evidence-validator` can re-Read `anchor2` quotes in the combined `review-doc.md`; stage 1 must confirm it.
