---
variant: 3
agent: haiku:backend
generated: 2026-11-11T18:33:00Z
---

## Summary

Use a shared, snapshot-bound review kernel with a reflect policy adapter and an adversarial compatibility finalizer.
Move slot resolution, dispatch accounting, typed findings, clustering and ledger storage into that kernel; keep calibration and evidence validation mandatory.
Migrate pre-execution first, single-pass and off by default; preserve return-contract 1.8.0 by retaining a real adversarial verdict.
Do not disguise deterministic agreement as adversarial convergence or import the specification panel's automatic revision loop.
Measure review quality and actual lane costs before increasing reviewer count or removing debate.

## Candidate architectures

All proposed names below are design proposals, not existing CLI capabilities. Source citations describe the inspected checkout; paths in citations are relative to the package source unless they begin with `.dev/`. Proposed installed instructions use installed locations, never repository-only package paths.

| Architecture | What changes | What it keeps | Estimated cost | Main risk | Verdict |
|---|---|---|---|---|---|
| Leave reflect as is | Nothing; collect measurements only | Existing reviewer rotation, two engines, blind calibration, adversarial merge, validator, contract | Published T2 design band: 35k–70k Claude tokens plus 10k–25k retrieval tokens | Duplicate machinery and headless accounting gaps remain | Safe control arm, not the desired shared model |
| Replace T2 with the full specification panel | Use default four-reviewer panel or seven-reviewer panel, deterministic merge, up to three reviews and two revisions | Reflect grounding and final policy gates, if explicitly adapted | Specification evidence is about 408k loop output tokens; not a reflect forecast | Single-document schema, missing calibration and executor exclusion; unauthorized plan revision; incompatible convergence semantics | Reject as a direct substitution |
| Shared kernel plus adversarial compatibility finalizer | Common resolver, dispatch interface, finding envelope and ledger; reflect retains real debate as a finalizer | 1.8.0 semantics, calibration, evidence gate, domain policy, single-pass behavior | Planning estimate 37k–53k output tokens for a three-reviewer pass; measurement required | Some debate cost remains; two engines need conformance tests | Choose |
| Shared deterministic kernel with versioned reflect contract | Same kernel, but replace debate with explicit adjudication states rather than an adversarial score | Calibration and validator; new major-version consumer semantics | Planning estimate 31k–43k output tokens for three reviewers | Broad consumer migration; no evidence that removal is quality-neutral | Possible later experiment, not initial shipment |

The existing panel is a resolver and document-review data path, not an already complete reflect executor. Its default template requests one fixed Tier 1b reviewer, one Tier 2 reviewer and two Tier 3 reviewers. The inspected merge command accepts one `--doc` and one round, then writes a merged report and ledger. Neither interface promises reflect's code-audit gates. Evidence: `cli/review/data/review-panel.default.json:5-11`; `cli/review/merge_cmd.py:21-71,99-118`.

## Chosen architecture and reasons

**Chosen architecture: snapshot-bound shared kernel with a reflect policy adapter and real adversarial finalization.** Share mechanics first; do not change the meaning of a shipping verdict while replacing the transport underneath it.

The kernel owns four things: a resolved execution manifest, immutable reviewer submissions, conservative finding grouping, and a ledger of processing outcomes. The reflect adapter owns requirement extraction, coverage denominators, grounding, deviation meaning, risk escalation, remediation and promotion. Calibration and evidence checking become reusable extension points, initially implemented through the existing installed agents. The specification panel can adopt the same finding envelope without adopting reflect's deviation taxonomy.

This separation follows the actual boundary: existing findings locate quote anchors within one document, while reflect's brief carries source ranges, verification artifacts and coverage slices. Combining documents into one giant synthetic document would erase source identities and make line citations fragile. Evidence: `cli/review/findings.py:276-359`; `skills/sc-reflect-protocol/refs/reviewer-spec.md:33-78`.

For 1.8.0, deterministic clustering is a **preparation step**, not the claimed merge method. The kernel's reflect profile invokes the installed adversarial protocol on all calibrated cards, including all cluster members and unresolved disagreements. It records a genuine adversarial result before the reflect adapter emits `merge_method: adversarial`. There is no substitute score derived from duplicate counts. The current stable enum explicitly disallows an inline merge and the promotion gate requires an actual merged adversarial verdict at T2. Evidence: `skills/sc-reflect-protocol/SKILL.md:659-666,784-793,1483`.

The backend priority is an honest result under failure. An empty submission, a transport success without valid findings, a schema failure, and a valid empty findings set are four different states. An interrupted merge must not appear as a clean audit. Replaying a run must not create additional reviewer votes, clear unresolved findings, or overwrite a newer plan. Those properties matter more than reducing one model call.

## Answers to Q1-Q7

### Q1 — What moves, what is missing, and what stays?

**Move review infrastructure; keep reflect's decisions.** The panel supplies reusable slot/tier data, deterministic selection, configuration hashes, document-finding parsing, grouping, ledger history and capture accounting. Parallel execution should be exposed through a shared runner interface; the inspected resolver itself does not launch reviewers. Reuse the existing swarm dispatch where applicable rather than inventing another scheduler.

The shared model needs additions before reflect can use it: hard executor-class exclusion, persona assignment, actual model-class metadata, independent blind calibration, multi-file citations and coverage references, a mandatory evidence-validation stage, and explicit incomplete-run states. Existing `distinct_across_slots` is not a hard independence guarantee: random and round-robin selection fall back to the full candidate list when exclusions exhaust it. Fixed selection takes the first candidate. Evidence: `cli/review/panel.py:380-418,479-512`.

Reflect retains all code grounding; parsed and inferred requirement extraction; task-to-hunk mapping; four-class deviation classification; tier-decision rubric; verification and reachability logic; remediation offers; and promotion. The shared ledger must not convert a no-spec correctness warning into Regression. That channel is explicitly advisory in `agents/reflect-reviewer.md:30,101-115`.

Share telemetry vocabulary and per-slot accounting, but preserve command-specific fields. Existing telemetry integration details are UNVERIFIED beyond the schema/function inventory recorded in the enrichment. The design does not assume an existing universal telemetry writer.

### Q2 — How do findings carry reflect content?

**Introduce a versioned envelope around a common finding core, with a reflect extension and multiple typed evidence locations.** Keep the current `findings-v1` parser unchanged for existing panel consumers. Normalize its output into the new internal envelope through a lossless adapter; do not silently feed new fields into a parser that cannot interpret them.

A reviewer submission contains an explicit completeness declaration, its card-level calibration record, findings and coverage observations. Each finding carries independent calibrated confidence provenance, even when it inherits the card's calibration. Preserve the distinction between a card score and a separately graded finding; never manufacture finer precision from a card score. Requirement/task rows exist independently of findings so a clean review can still show which obligations were checked.

The existing ledger's `confidence: single|overlap` becomes `agreement_label` internally, not numeric confidence. Repeated reports from the same actual model class can increase reviewer overlap but not model-class diversity. Evidence: `cli/review/ledger.py:86-90`; `skills/sc-reflect-protocol/SKILL.md:1172-1192`.

### Q3 — Deterministic matching, debate, or both?

**Use both initially: deterministic matching for storage and navigation, real debate for semantic adjudication and the 1.8.0 score.** Keep every source claim available to the debate. A cluster is a candidate group, not proof that its members identify the same defect or deserve the same class.

Deterministic grouping does not decide whether a departure is authorized, necessary, drift or regression. It also cannot decide whether a plan's alternate implementation satisfies a requirement. The current matcher can group by shared section and references or nearby spans, which is useful for document reviews but too permissive as the sole decision rule for a multi-file audit. Evidence: `cli/review/findings.py:367-407`.

For **pre-execution**, removing debate would lose explicit reconciliation of competing interpretations, such as a claimed coverage gap versus an intentionally deferred requirement. A blind evidence-grounded adjudicator might replace that work eventually. The six recorded runs do not establish this: four of five T2 scores were 1.0 and the fifth 0.97, but those are agreement observations, not defect-recall measurements.

For **post-execution**, removal additionally risks accepting the wrong deviation class and triggering or suppressing remediation, rollback or promotion. This is higher consequence. Retain debate until an independent post-execution trial demonstrates that a proposed replacement resolves classification conflicts at least as reliably.

Do not force a different-class judge by silently reusing the executor. Resolve a judge disjoint from reviewers when available, record actual identity and collisions, and retain existing degradation behavior where the pool cannot supply separation. Opus is permitted only when its stronger independent calibration or contested semantic adjudication is needed and no suitable lower-tier disjoint choice is available; it is not the routine reviewer anchor. No forbidden model or Tier 0 may be selected by primary, fallback, calibrator or judge resolution.

### Q4 — Which engine and how are aliases mapped?

**Support agent sessions and swarm behind one execution contract, not two audit semantics.** Use restricted agent sessions first for pre-execution migration; preserve swarm as the headless transport and migrate it after parity tests. The CLI already dispatches and normalizes swarm workers and calls a separate adversarial scorer: `cli/reflect/ensemble.py:333-440`.

Panel tiers describe capability pools. Reflect T2 describes an audit escalation level. `T2Model` slots describe existing transport configuration. These are three namespaces, not interchangeable labels. Resolve capability pool to an actual model and class, then bind that immutable selection to the engine's launch alias. Record requested tier, selected class, actual class, vendor, alias, fallback history and persona separately.

The current panel resolution includes tier, alias, model, fallback candidates and launcher; it has no executor-class input. Tier files also include environment stand-ins. Therefore filter every primary and fallback candidate through reflect's policy **before dispatch**, and check the actual completion identity afterward. Merely relabeling multiple Haiku stand-ins as distinct panel tiers does not satisfy heterogeneous review. Evidence: `cli/review/panel.py:427-525`; `cli/review/data/review-tiers.default.json:18-30`.

PROPOSED launch binding: the adapter maps the resolved reviewer list to the existing swarm slot transport factory rather than independently re-resolving `T2Model0N` values. A mismatch is a configuration error or visible diversity degradation, never a second hidden selection. Agent launches use the restricted installed `reflect-reviewer` definition, with persona supplied in the brief; they do not use an all-tools persona agent. Engine restrictions for external providers must be verified, not inferred from the agent definition.

### Q5 — What is the pre-execution path?

**Keep existing T1 and coverage work, replace only the T2 infrastructure, and produce the same advisory return contract.** Snapshot plan and spec, extract requirements, ground the coverage map, apply the existing tier rubric, resolve eligible reviewers, dispatch independent briefs, calibrate cards, group findings, obtain a real adversarial verdict, synthesize and evidence-check the report, then serialize 1.8.0.

Reviewers inspect both plan and source spec, plus relevant code where the plan makes implementation assumptions. Assumption A-3 must not be read as permission to remove code grounding. The QA reviewer receives the full spec body, sectioned when necessary, to catch requirements absent from the matrix. This is existing behavior, not an optional cost optimization: `skills/sc-reflect-protocol/refs/reviewer-spec.md:55`.

The return includes both parsed-only and union coverage; unmapped requirements; calibrated confidence; status; report and audit paths; citation statistics; input integrity; reviewer cards; adversarial artifacts and score; diversity; and unchanged non-applicable post/promotion values. Workflow records advisory status and report path without turning reflect into a plan-revision gate. The workflow behavior is established in the supplied enrichment at lines 35-40, citing its already-read workflow sources.

### Q6 — Are rounds and revision loops needed?

**Single pass per reflect invocation; one ledger round for traceability, no automatic revise loop.** Retries of malformed or failed work are attempts within that round, not fresh opportunities to clear findings. A revised plan is a new input snapshot and a new invocation.

The panel's rounds and ledger are useful storage concepts. Its `REVISE` decision is not permission for reflect to edit the plan or code. The existing ledger expects strictly increasing rounds, and its revision machinery can mark touched rows `resolved_check`, later clearing them when absent. That lifecycle is inappropriate for an advisory audit unless an explicit revision workflow owns it. Evidence: `cli/review/ledger.py:114-121,254-258,301-347`.

Reuse capture accounting and immutable membership history; disable automatic clearing in the reflect profile. Keep remediation opt-in through reflect's current handoff. A subsequent remediation audit may link prior finding IDs, but it must validate the changed source anew.

### Q7 — What does it cost, and when should it not run?

**A small shared-kernel pass can be cost-comparable to T2; a full document-review loop is not justified by current reflect evidence.** Infrastructure sharing alone does not save model tokens. The savings hypothesis is shorter structured outputs and fewer repeated summaries, not extra cheap reviewers.

The published T2 design band is 35k–70k Claude tokens plus 10k–25k retrieval tokens, 480–900 seconds. Those are not established output-only measurements. Specification-panel evidence is about 408k loop output tokens; it cannot be substituted for reflect costs. The cost section separates these units and gives explicit lane estimates.

Do not call a full panel for every workflow plan simply because workflow calls reflect. Preserve the T1 stop rubric, budget routing, grounding requirements and explicit T2 escalation. Use three reviewers by default when T2 is justified, two when independence constraints permit only two, never seven by default. Large scope alone does not prove seven reviewers are worth the cost. A low-stakes plan with clear coverage and no escalation signal stays at T1; missing evidence must not be hidden as a clean cheap pass.

## Finding format

**PROPOSED schemas:** `review-submission/2`, `review-finding/2`, and a snapshot-aware ledger envelope. These are internal review APIs, not additions to reflect's stable return contract.

Submission fields:

- `schema`, `run_id`, `round`, `reviewer_id`, `attempt_id`, `input_tree_sha256`, `brief_sha256`, `policy_sha256`.
- `resolution`: requested capability tier; selected and actual model class; vendor; launch alias; persona; executor-exclusion result; fallback attempts.
- `completion`: `complete|truncated|invalid|failed|timed_out`, parse errors, output hash, observed token counts and duration. Only `complete` plus valid schema is eligible to count toward review quorum.
- `card`: original card path/hash; proposed confidence; blind-calibrated confidence; rubric identity; calibrator class; calibration result/path/hash; diversity label. No reviewer formation transcript is sent to the calibrator.
- `findings`: ordered array, valid empty array allowed.
- `coverage_observations`: independent rows with requirement/task IDs, checked state, evidence IDs and missing-evidence explanation. Every assigned row must receive an observation or an explicit unverified marker.

Finding core:

```yaml
schema: review-finding/2                 # PROPOSED
id: reviewer-local-id
channel: defect                         # defect | grounding-gap | advisory
claim: one precise failed obligation
severity: MAJOR                         # retain panel vocabulary
blocking: true
category: missing-requirement
obligation_refs: [REQ-014]
subject_citation_id: plan-location
citations:
  - id: plan-location
    input_id: plan
    path: plan.md                       # relative to declared grounding root
    revision: snapshot-sha256
    start_line: 40                      # 1-based, inclusive
    end_line: 44
    quote: exact source excerpt
    role: subject                       # subject | requirement | baseline | verification
  - id: spec-location
    input_id: source-spec
    path: source.md
    revision: snapshot-sha256
    start_line: 80
    end_line: 85
    quote: exact source excerpt
    role: requirement
confidence:
  calibrated: 0.86                     # example, not a measured result
  source: card                         # card | finding
  calibration_ref: card-calibration-id
reflect:
  mode: pre
  deviation_class: null                # authorized | necessary | drift | regression in post
  classification_rationale: null
  coverage_row_ids: [REQ-014]
  inferred: false
  modifier: null
```

`blocking` and severity remain reviewer claims until reflect adjudication; they cannot override the four-class taxonomy. A grounding gap has no invented fifth deviation class. Advisory no-spec correctness findings remain non-gating regardless of severity. Post findings preserve original HIGH/MEDIUM/LOW labels in the reflect extension; a display mapping to panel severity is not an automatic classification or routing rule.

**Dedupe key:** compute an exact identity from schema version, input snapshot identity, channel, category, sorted obligation refs, normalized claim text, and the sorted set of `(input_id, revision, normalized_path, role, quote_hash)` tuples. Do not include reviewer ID. This catches identical claims across reviewers while retaining distinct claims at the same location. Line ranges are validated locators, not the sole identity.

Non-identical keys may be suggested as related if the same subject location and obligation overlap. They are not automatically collapsed, especially when classifications differ. Cross-file findings retain their full citation sets. Duplicate quotes in different files are never interchangeable. Ambiguous repeated quotes within one file require the declared range to disambiguate; failed resolution becomes a grounding gap, not the first match.

For panel `findings-v1`, derive input identity from `--doc`, carry `anchor` and `anchor2` as document citations, and retain original report bytes. No numeric calibration is invented for panel reports. Existing `refs`, claim, category, severity and blocking fields survive. Deterministic legacy matching remains available for legacy schema runs; the new reflect profile uses conservative multi-file matching.

The ledger stores every source member, calibration reference and validator outcome. Counts of deviations are computed once per adjudicated issue, not once per reviewer or citation. Group disagreements remain visible and cannot be resolved by taking the maximum severity alone.

## Adapter sketches

### Pre-execution adapter

1. **Freeze inputs.** Hash plan, source spec and all grounding inputs; materialize the existing input snapshot. Pin the panel template, tier file, policy and prompt hashes. Record executor identity and source. Unknown executor remains the existing fail-open warning, not an invented precondition stop.
2. **Run existing T1.** Build parsed and inferred coverage; preserve both denominators. Ground proposed component assumptions. Apply the current escalation rubric unchanged. If T1 stops, the panel is not invoked.
3. **Resolve reviewer slots.** PROPOSED reflect-specific three-slot template: one Tier 1b-capability anchor and two eligible independent slots from lower allowed pools, with analyzer, QA and structural lenses. Resolve class exclusions first; reserve independent calibration capacity. Replace an ineligible anchor before resolution, not after launching it. If two distinct eligible classes cannot be supplied, use the existing T1 degradation path.
4. **Materialize and dispatch.** Keep exactly `T1 card excerpt`, `Grounding hunks`, `Coverage slice` in each brief. Put schema instructions and run metadata inside those sections rather than adding a fourth. Dispatch through the shared engine interface, agent sessions first. Existing CLI surface is `superclaude review panel resolve`; a reflect-policy-aware extension to it is PROPOSED, not currently available.
5. **Normalize and calibrate.** Validate schemas and input identity. Persist immutable cards. Run separate blind `confidence-calibrator` instances per card, using installed definitions with project-agent precedence. Preserve actual disjointness/degradation metadata.
6. **Merge without losing evidence.** Build conservative clusters and round-1 ledger. Invoke the installed adversarial protocol, retaining all cards as inputs. A multi-input extension of `superclaude review merge` is PROPOSED; today's single-document command cannot directly process this envelope.
7. **Final evidence gate.** Reflect synthesizes the verdict; `evidence-validator` re-Reads cited sources under the existing citation-budget policy. Validate quotes, file versions and claim support; feed drops and inferred-row changes back into coverage. Compare current input hashes again. Validator failure uses the existing partial inline fallback.
8. **Publish advisory outputs.** Atomically publish the finished report, audit log and 1.8.0 contract only after their referenced artifacts exist and validate. Workflow receives its unchanged advisory fields. No pre-execution `reflect_post` write and no plan revision.

### Post-execution adapter, later

1. Freeze spec, tasklist, task log, base/head identities, diff, verification outputs and all grounded sources; retain existing snapshot/isolation rules.
2. Reflect performs code grounding, coverage, deviation candidates, verification, reuse and reachability work. No kernel worker executes tests or mutates the audit target.
3. Resolve eligible restricted reviewers with existing personas, plus QA's verification and ledger hunks; dispatch through either conforming engine.
4. Normalize citations against both baseline and reviewed versions; calibrate cards; cluster conservatively. Debate every disputed class using all underlying evidence, then synthesize the four-class register and separate grounding gaps.
5. Run final evidence validation and input-drift checks. Never copy the current headless builder's constant zero citation-drop count into the new path without validation. That constant is visible in `cli/reflect/ensemble.py:808-819`.
6. Produce the same 1.8.0 contract and derive the existing wrapper verdict. Let the existing wrapper own `reflect_post` writeback. Remediation and promotion remain separate reflect stages; rerun promotion evidence checks when remediation ran.

**Operational execution contract, both adapters:** use a coordinator-owned manifest with state `resolved → dispatched → collected → calibrated → merged → validated → published`, plus terminal failure. This manifest is PROPOSED, stored within the normal reflect output directory. Each stage records input hashes and committed output hashes. One coordinator writes it; reviewer workers only return data.

The idempotency identity is `(run_id, snapshot_hash, policy_hash, stage, reviewer_id, attempt_id)`. A repeated submission with the same hash is a no-op; a different payload under the same identity is rejected. An attempt supersedes its earlier failed attempt but never adds another vote. A duplicate merge request returns the committed result when its input hash matches; otherwise it fails without modifying the ledger. On resume, reuse only completed stages whose complete dependency hashes match. A new plan hash starts a new invocation, not a continuation.

Use same-directory temporary output and atomic replacement for publication, with a manifest commit marking the complete artifact set. Existing ledger saves are atomic, but the current merge command writes its report separately before saving the ledger; that pair is not a transaction. A reader of the new path accepts only a committed manifest. Evidence: `cli/review/ledger.py:52-67`; `cli/review/merge_cmd.py:113-118`.

Use one total deadline and bounded fallback budget across stages. The existing ensemble captures a shared deadline before dispatch; retain that principle. Do not multiply timeouts by restarting the entire panel after each missing reviewer. Exclude forbidden and executor-colliding classes throughout the fallback chain, and report each failed attempt. Preserve existing bounded malformed-merge retries and corroborated loud fallbacks rather than silently publishing partial artifacts as success.

## Staged migration

| Stage | Entry criteria | Exit criteria | Rollback |
|---|---|---|---|
| 0: freeze baseline | Design accepted for an experiment; no default behavior change | Snapshot fixtures, actual consumer inventory, model availability and lane metrics captured | No production change to undo |
| 1: build shared data seam | Legacy findings-v1 and 1.8.0 fixtures available | Lossless round trips; multi-file negative tests; retry/idempotency tests; no forbidden model resolution; spec-panel unchanged | Keep new schema dormant; retain old serializers |
| 2: shadow pre-execution | PROPOSED `--review-backend shared` flag implemented, off by default; agent runner conforms | First measurement passes; new outputs isolated from authoritative old outputs; crash paths produce honest partial/failed results | Disable flag; old path remains authoritative |
| 3: opt-in authoritative pre | Shadow quality and budget criteria pass | Workflow advisory behavior unchanged; complete artifacts and contracts validated on real plans; operator approval for default change | Select legacy backend for new invocations; retain all artifacts for diagnosis |
| 4: pre default, headless parity | Explicit default-change approval; both engines independently tested | Equivalent findings/calibration/evidence semantics, actual identity accounting and failure handling | Revert default; unfinished shared runs remain resumable or explicitly abandoned |
| 5: post opt-in | Pre stable; post-specific verification, taxonomy, writeback and promotion tests pass | Blinded post study passes with no false promotion; wrapper frontmatter and sidecar behavior preserved | Turn off shared post flag; legacy post remains default |

Post default is a separate decision, not implied by successful pre adoption. Every rollback changes only future routing; it does not delete or reinterpret existing reports. Flag changes must not splice a legacy merge into a partially completed shared run. Complete it with its pinned policy or start a new run.

Compatibility tests include T1 stop, two-of-three completion, no survivors, wrong schema, empty valid findings, truncated findings, unknown executor, exhausted disjoint pool, alias drift, validator failure, dropped citations, changed input, missing adversarial artifacts, null/non-finite convergence, and stale frontmatter. The new path must preserve existing consumer semantics; fixing unrelated legacy behavior requires a separately reviewed contract change.

## Return-contract 1.8.0 mapping

**No stable field is added, removed, renamed, retyped or repurposed.** New manifest and schema data live in referenced artifacts and non-stable telemetry. Contract changes are unnecessary because the chosen architecture retains real adversarial finalization.

| Contract field or family | Source in new design | Compatibility |
|---|---|---|
| `contract_version` | Constant `1.8.0` | Unchanged |
| `status`, `mode`, `tier_reached` | Existing reflect reduction of validated observations and actual stages reached | Unchanged meanings; not panel PASS/FAIL |
| `report_path`, `audit_log_path` | Committed output artifacts | Unchanged |
| `confidence_calibrated` | Existing rubric over blind-calibrated cards and validated evidence | Unchanged; never reviewer overlap |
| `coverage_pct`, `unmapped_requirements` | Parsed-only requirement map, recomputed after evidence drops | Unchanged |
| `coverage_pct_union`, `coverage_degraded`, `unmapped_requirements_union`, `coverage_undefined` | Existing parsed-plus-inferred extraction and map | Unchanged |
| `best_practice_grade`, implementation coverage | Reflect's existing grounded analyses | Unchanged |
| `reviewer_cards` | Persisted calibrated cards with shared-envelope provenance | Unchanged path list; readable card content retained |
| `merge_method` | Real adversarial finalizer or corroborated legal fallback | Only `adversarial` or `single-reviewer-fallback` |
| `adversarial_convergence_score` | Real child `convergence_score` | Unchanged numeric meaning or null |
| `adversarial_artifacts_dir` | Mechanical remap of child `artifacts_dir` | Unchanged |
| `adversarial_unavailable` | Existing loud fallback outcome | Unchanged |
| Diversity fields | Actual reviewer classes/vendors and calibrator class | Unchanged meanings; aliases do not count as classes |
| Citation fields and `evidence_validator_ran` | Actual validator results under existing sample/full policy | Unchanged, not fabricated defaults |
| Input integrity fields | Original snapshot and final current-source comparison | Unchanged |
| Deviation counters, asymmetric flags, per-task verdicts | Reflect's post adapter after evidence/class adjudication | Unchanged four classes and routing |
| Verification, runtime surface, reachability, reuse fields | Existing reflect domain stages | Unchanged; no panel-generated substitutes |
| Remediation and promotion fields | Existing opt-in handoff and nine-condition promotion gate | Unchanged; pre remains non-promoting |

**Null-score rules:** at T1, the score is inapplicable/null. At T2, an unavailable adversarial result stays null, forces the documented partial/halt routing, and blocks promotion. For a legal single-reviewer fallback, route on merge method first and use calibrated confidence where the existing fallback semantics require it; never compare null numerically. No synthetic 0, 0.5 or 1.0 is emitted. Deterministic agreement is internal telemetry only. The wrapper's stricter below-0.80 degradation threshold remains unchanged even though skill-level score routing uses other thresholds. Evidence: `skills/sc-reflect-protocol/SKILL.md:655-666`; `cli/reflect/contract.py:290-326`.

**Gate condition 9:** retain `tier_reached == 2` requiring a non-null genuine merged adversarial result. Internally, read the stable `adversarial_convergence_score` into the gate's local `convergence_score`; this is a local name mapping, not a new stable alias. Other promotion conditions still apply, particularly evidence drops, grounding gaps and input drift. Evidence: `skills/sc-reflect-protocol/SKILL.md:1465-1487`.

**`reflect_post`:** keep the existing wrapper-owned mapping exactly: verdict, status, run identity, tier, report/contract/reason, four deviation counters, head, review time and the three honest-accounting verification siblings. Do not add kernel/ledger fields to frontmatter or let reviewers write it. Preserve byte-splice behavior, the compare-before-write guard, missing-frontmatter behavior and the sidecar failure path. The implementation normalizes CRLF to LF; do not promise byte preservation of line endings. Evidence: `cli/reflect/runner.py:103-155,157-204`.

Consumer-by-consumer commitment:

- Workflow's pre advisory consumer continues reading only `reflect_status` and `reflect_report_path`; no plan status gate or auto-reviser is added.
- The sprint/wrapper verdict map retains blocked → degraded → halted → pass ordering, actual diversity, unavailable merge, fallback, null/bad/low convergence and dropped-citation handling. No deterministic-only success is slipped past that map.
- Sprint's per-task ledger retains status, validation strength, deviation class and budget downgrade semantics.
- Troubleshoot and task end hooks retain status/confidence/deviation/human-decision routing. Auggie-review's post invocation remains unchanged; its precise additional parsing is UNVERIFIED beyond the enrichment.
- Roadmap and tasklist retain parsed-only coverage semantics. Advisory union coverage remains optional.
- Workflow remediation and task-builder retain report, deviation register and grounding-gap references, preserving human-decision visibility.
- Promotion adapters retain all nine gate inputs, score null handling, post-remediation revalidation and rollback behavior.
- CI graders retain per-task, evidence-validator and audit fields. Meta-eval retains score and diversity meanings; new engine labels are telemetry only.
- Implement does not acquire a new reflect dependency. The complete consumer inventory must be checked again before implementation because inspected protocol documentation is not proof of every runtime caller.

These commitments follow `skills/sc-reflect-protocol/SKILL.md:923-970` and the supplied enrichment's consumer inventory. Any later deterministic-only shipping path needs a major-version design and migration of every consumer above, not a new enum hidden inside 1.8.0.

## Cost model

Separate estimates, artifact sizes and provider usage. The published profile is 35k–70k Claude tokens, plus 10k–25k retrieval, with 480–900 seconds; it does not establish output-only lane costs. Its hard kill is 1.25 times the midpoint, not the maximum: `(35 + 70) / 2 × 1.25 = 65.625k` Claude tokens. Do not alter that preflight contract as part of this infrastructure migration. Evidence: `skills/sc-reflect-protocol/refs/cost-profile.yaml:46-70`.

The following is an **output-token planning estimate**, not observed reflect billing. It includes T1/common work for a run reaching T2 and excludes input tokens, retries and retrieval tokens. Lane allocations must be measured before capacity decisions.

| Lane | Legacy three-reviewer estimate | Shared-kernel three-reviewer estimate | Why |
|---|---:|---:|---|
| Primary/coordinator, T1, grounding summaries, report | 10k–16k | 8k–12k | Less repeated prose; same grounding scope |
| Parallel reviewer cards | `3 × 7k–10k = 21k–30k` | `3 × 6k–8k = 18k–24k` | Bounded typed findings and coverage, not less required reading |
| Blind calibrators | `3 × 1k–2k = 3k–6k` | `3 × 1k–2k = 3k–6k` | Preserved per-card independence |
| Debate/finalizer, including judge | 6k–10k | 6k–10k | Real debate retained; no assumed free convergence |
| Evidence validator | 2k–4k | 2k–4k | Existing citation policy retained |
| Total | `10+21+3+6+2` to `16+30+6+10+4` = **42k–66k** | `8+18+3+6+2` to `12+24+6+10+4` = **37k–56k** | Hypothesized savings, not established |

The candidate table's 37k–53k target assumes the finalizer is held to 6k–7k; the broader operational planning band above allows 10k. This distinction is a target versus allowance, not two measured results. At midpoints, legacy is 54k and shared is 46.5k: proposed savings `7.5 / 54 ≈ 14%`. Infrastructure overhead is deterministic CPU/storage and small, but no numeric latency claim is made.

Two-reviewer shared estimate: primary 8–12k + reviewers 12–16k + calibration 2–4k + finalizer 6–10k + validator 2–4k = **30k–46k**. Do not choose it solely to save tokens when the requested independent coverage cannot be delivered. A hypothetical debate-free three-reviewer experiment subtracts 6–10k from the shared band, yielding **31k–46k**, but it is not contract-compatible production behavior.

For comparison only, PN1's specification loop measured about 408k output tokens: approximately 106,357 primary + 290,600 parallel + 11,359 adjudication = 408,316. That last historical adjudicator is forbidden in this design; its replacement cost is unknown. The parallel share is `290,600 / 408,316 ≈ 71%`. The observed first-review arithmetic was roughly 23k + `3 × (68k–108k)` = **227k–347k**, including a reported example around 314k. None is evidence that reflect needs those prompts or those budgets. Provenance is the supplied enrichment at lines 59-63, citing the already-read experiment records.

The panel's measured gain was 15.7 fixed defects versus 2.8 baseline on a 44-defect specification ledger; it is not a reflect gain. Moving from one Sonnet plus three Haiku reviewers to one Sonnet plus six Haiku reviewers gained about three fixed defects on one specification. Adding three reviewer lanes would cost approximately `3 × (6k–8k) + 3 × (1k–2k) = 21k–30k` more under this proposed reflect budget, before larger merge/validation work. Do not buy that expansion without reflect-specific benefit.

Capture input, output, cached input where available, retries and elapsed time separately for each actual class and stage. Currency estimates require verified current routing prices and are UNVERIFIED here. A byte-to-token conversion of report artifacts is not provider usage. Keep retrieval tokens separate from output tokens, and do not claim output-token savings automatically imply lower latency or bills.

## Risks

1. **False clean result from missing data.** Empty valid findings require a complete coverage observation set; schema/transport failure is incomplete, not clean. Keep original outputs and rejected records for diagnosis.
2. **Wrong deduplication suppresses defects.** Exact keys include source identity and claim; related clusters do not delete members. Disputed class or claim remains a separate adjudication input.
3. **Alias diversity disguises class collision.** Record actual class and vendor, enforce exclusion on all fallback candidates, and compare completion identity to resolution. Unknown identity is explicit degradation, not invented diversity.
4. **Calibrator anchoring.** Give each calibrator only the card and required rubric, never the review conversation, other reviewer cards, agreement counts or merged verdict. Preserve independent instances and disjointness metadata.
5. **Citation validity changes mid-run.** Pin snapshots; validate final current-source identity; preserve input-drift routing. A snapshot citation alone is insufficient for promotion after source changes.
6. **Partial publication after crash.** Publish a committed manifest after validating every referenced artifact. Resume by hashes; retries cannot add votes. Do not treat the existing report-plus-ledger write sequence as transactional.
7. **Engine parity is overstated.** Swarm currently reports snapshot isolation as children-only because text workers can read the live tasklist; its builder also lacks the full verification/evidence stages. Keep headless migration separate until grounding and gate semantics are demonstrated. Evidence: `cli/reflect/ensemble.py:490-498,808-819`.
8. **Review infrastructure acquires mutation authority.** Restricted reviewers cannot revise plans, execute tests or archive work. Existing wrapper and promotion code remain the only owners of their respective writes.
9. **Scope grows into a generic workflow platform.** Implement the common envelope, resolver policy seam and single-pass ledger only. No new scheduler, daemon, database, remote service or automatic revision engine is required.

## First measurement

**First experiment: paired shadow pre-execution non-inferiority and cost trial, with debate held constant.** Isolate infrastructure substitution before asking whether debate itself is useful.

Use 24 frozen plan/spec cases: eight real plans across different domains, eight deliberately incomplete coverage cases, and eight cases with contradictory or ambiguous implementation assumptions. Independently author the expected defect/coverage ledger before generating either output. Include known citation pathology and executor-collision cases across these groups. Keep cases disjoint from prompt-development examples.

Run each case twice per arm with matched candidate model classes and matched budgets: legacy T2 versus shared-kernel T2, both with blind calibration, genuine adversarial finalization and the same evidence policy. Arithmetic: `24 cases × 2 repeats × 2 arms = 96 runs`. Repeat because one stochastic review per plan cannot distinguish transport/prompt changes from run variation. Randomize arm order and hide arm identity from graders. The estimated total shared/legacy output budget at planning midpoints is `48 × (46.5k + 54k) = 4.824 million` tokens, excluding retrieval/input/retries; obtain experiment-budget approval before execution.

Primary metric: case-level recall of independently validated material defects, with a paired difference and case-clustered uncertainty interval. Secondary metrics: false-positive rate, coverage-map accuracy, unsupported citations retained, calibration quality, actual class independence, malformed completion rate, total tokens by lane and wall time. Do not score success using convergence alone or count a duplicated finding twice.

**Pass for wider opt-in:** shared recall is within five percentage points of legacy on the observed aggregate; no HIGH-stakes seeded defect caught by legacy is missed by shared; no unsupported citation or incomplete-run result is certified clean; no forbidden/executor-colliding class is dispatched; no unintended repository write; median total provider output tokens at most 90% of legacy; p95 elapsed time at most 125% of legacy. A safety failure fails the trial regardless of savings. An uncertainty interval extending below the five-point margin makes the result inconclusive, not a quality pass.

Twenty-four cases is a feasibility sample, not a powered proof of non-inferiority: paired variance and baseline reflect recall are unknown. Estimate them from this pilot and determine the next sample before changing defaults. If quality passes but cost does not, sharing may still reduce maintenance duplication, but the owner must explicitly approve that tradeoff. Do not claim the migration is a cost win.

A debate-removal ablation belongs after this first result and must be separate for pre and post. The first experiment intentionally does not change convergence semantics, reviewer count and execution engine simultaneously.

## Assumptions and UNVERIFIED items

- A-1 accepted: this is a design and measurement recommendation, not approval to ship. Only this variant file is created.
- A-2 refined: one shared finding envelope, resolver/dispatch interface and ledger model; command-specific policy profiles and finalizers. Sharing does not require every command to use the same merge decision rule.
- A-3 qualified: pre reviews plan plus source spec and may cite grounded code when judging implementation assumptions. Multi-document support is necessary even without a code diff.
- A-4 retained without false precision: preserve per-card calibration and carry a calibration reference on each finding. A card-derived finding score is labeled as such; it is not a fresh per-finding judgment.
- A-5 applies only to experimental output-token figures and proposed lane estimates. The published reflect profile does not identify an equivalent output-only measurement basis.
- A-6 accepted for drafting only: owner approval remains necessary for experiment spending, default routing and eventual post adoption.
- Timestamp metadata uses the brief's available ISO timestamp as a coarse generation marker; wall-clock time was not queried because this assignment permits no shell operations.
- All schema names, state-machine details, idempotency keys, reflect-specific panel templates, multi-input merge support and `--review-backend shared` are PROPOSED. Existing `superclaude review panel resolve` and `superclaude review merge` were read; no new flag is claimed available.
- Installed implementation instructions must resolve agents from project `.claude/agents/` first, then `~/.claude/agents/`; skills from `~/.claude/skills/` first, then project `.claude/skills/`. The relevant installed endpoints are the reflect protocol, adversarial protocol, restricted reviewer, calibrator and evidence-validator; no primitive should point at a source checkout path.
- The restricted reviewer currently describes post-execution triggers. Its pre-execution brief support and shared-envelope output are proposed changes, not existing verified behavior.
- The exact swarm transport-factory alias mapping, actual gateway availability, provider model-class metadata, fallback implementation internals and external tool restrictions remain UNVERIFIED. No candidate model IDs or unverified provider versions are prescribed.
- The complete telemetry writer, every runtime consumer and the installed calibrator/validator implementations were not read in full. The design preserves their documented contracts and requires implementation-time verification.
- Six recorded pre runs and the specification experiments are inherited evidence explicitly marked read in the supplied enrichment, not new measurements in this variant. Artifact byte sizes and convergence scores do not measure accuracy or billing.
- No post-execution quality, safety, cost or debate-removal equivalence is established. Post migration stays gated on its own study and promotion tests.
