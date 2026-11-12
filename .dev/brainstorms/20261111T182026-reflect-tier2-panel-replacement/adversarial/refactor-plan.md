# Refactoring Plan: Merge into Base (Variant 1)

Paths are relative to `src/superclaude/` unless they start with `.dev/` or name the adversarial folder. `path:line` cites below are lines I read while drafting this plan (panel.py, panel_cmd.py, merge_cmd.py, ledger.py, findings.py, review-tiers.default.json, contract.py, ensemble.py, _diversity.py, runner.py, sc-reflect-protocol SKILL.md and refs, reflect-reviewer.md, sc-workflow-protocol SKILL.md, sc-adversarial-protocol SKILL.md excerpts, one recorded reviewer card, and a count over `.dev/reflect/`). Anything I did not read is marked UNVERIFIED. "PROPOSED" marks a name that does not exist today. Point ids: S- structural, C- content, X- contradiction, U- unique, A- shared assumption (diff-analysis.md); INV- (invariant-probe.md); R1/R2 = debate rounds; the percentage is the confidence in the Scoring Matrix of debate-transcript.md.

## Overview

- Base: Variant 1 (opus:architect), kept as the skeleton: Layered Review Kernel (K1 resolution, K2 dispatch adapters, K3 findings-v2, K4 clustering), five candidates with verdicts, the 13-row finding table, command-level adapter steps, the stage table with What ships / Entry / Exit / Rollback, the consumer-by-consumer change list, the validator-legal template, the PROPOSED-names inventory (base-selection.md "Strengths to preserve" 1-11).
- Incorporating strengths from: Variant 3 (manifest state machine, completion states, contract stays 1.8.0 with `merge_method: adversarial`, executor exclusion by filtering before dispatch, judge collision accounting, honest cost units, embedded calibration, separate documents, no automatic quote rejection, `channel`, measurement hygiene) and Variant 2 (three-arm measurement with a T1 arm, pre debate kept until measured, `launch` null/non-null rule, 15-point gate, real-card evidence, Fable filter, ablation, `reflect_category`, conventions).
- Planned changes: **46** (13 incorporations, 10 corrections, 10 invariant resolutions covering all 20 UNADDRESSED invariants, 5 unresolved-point dispositions, 1 depth-by-tier policy section requested by the coordinator, 7 consistency edits).
- Overall risk: **Medium**. The merge changes the base's central decision (deterministic merge in pre, `merge_method: panel`, contract 2.0.0) into "debate kept, contract 1.8.0 unchanged, clustering as telemetry". That touches Summary, candidates, Q1/Q3/Q5/Q6, adapters, stages, contract mapping, cost and measurement; every one of those is rewritten here with full text so the executor invents nothing.

### Design decisions that govern the whole merge (the executor must keep them consistent everywhere)

1. **No contract change in Stages 0-4.** `contract_version` stays `1.8.0`, `merge_method` stays in `{adversarial, single-reviewer-fallback}`, the score stays the real `sc-adversarial` child score. Deterministic agreement is telemetry named `cluster_agreement`. A deterministic authoritative merge is a deferred major version with a named consumer list (Change 15). Basis: C-015 98%, C-016 98%, X-005 98%, X-004 98%; verified `SKILL.md:789` (legal set), `SKILL.md:666` EV-1 (merged-verdict.yaml with `merge_method: adversarial`), `SKILL.md:953` (semantic change is major).
2. **The debate is kept in pre and post.** Cards (calibrated, embedded calibration) are the debate's inputs exactly as `SKILL.md:645-651`. The K4 cluster map is telemetry only until a measurement shows it helps. Basis: C-006 90% (3 of 3), X-006 90%, A-008 80%, A-001 98%.
3. **First shipment is parity, not redesign.** In anthropic-only the `@reflect-pre` template reproduces today's rotation classes (sonnet anchor, haiku, opus as the third), because `t2_model_class_diversity: full` means three distinct classes (`SKILL.md:233-239`) and wrapper trigger 7 reads that field (`contract.py:281-284`). V1's lite template (sonnet, haiku, haiku; Opus moves to the calibrator) becomes a measured variant arm, not the default (Changes 19, 23, 28).
4. **Executor exclusion fails closed in the kernel and degrades in the adapter.** The kernel raises when exclusion exhausts a slot; reflect catches it per slot and applies `SKILL.md:600`. Reconciles V1 "raises" with V3 "degrade, do not raise" (Change 24).
5. **Identity of a dispatched reviewer is the pinned request until a spike proves read-back.** Today's cards already record the requested class (`model_class: sonnet` at the top of the recorded card) and nothing reads identity back; the design does not weaken that and adds a probe (Change 26).
6. **Pre never goes headless.** The headless builder is post-only (`ensemble.py:797`); the interactive skill emits contract 1.8.0 (37 of 42 recorded pre contracts under `.dev/reflect/pre-*` carry `contract_version: "1.8.0"`); the headless builder emits `"1.0"` (`ensemble.py:74,788`).
7. **Opus uses, named (full list in Change 19):** (a) blind calibrator when SKILL.md:1181 picks it; (b) third reviewer exactly where today's rotation uses it (`SKILL.md:607`, backfill `reviewer-spec.md:108`); (c) `--strategy enterprise` reviewer (`SKILL.md:608`); (d) judge selection stays inside `sc-adversarial-protocol` and reflect never pins Opus. No new Opus use is introduced. Fable and Tier 0 are never selected anywhere.

## Planned Changes

### Group A. Incorporations from Variant 2 and Variant 3

### Change 1: Execution contract block (manifest state machine, idempotency, atomic publish) (from Variant 3)
- **Source**: Variant 3, "Adapter sketches" final block ("Operational execution contract, both adapters"), S-008.
- **Target**: Base, new subsection `### Execution contract (both adapters)` after "Adapter sketches" (insert).
- **Rationale**: S-008 L3 V3 98%; C-011 V3 98% (R1 and R2, 3 of 3: attempts are not votes); U-014 High; U-017 (merge_cmd writes the report before saving the ledger, `merge_cmd.py:113-116`, so the pair is not a transaction). Base has no failure/resume model (diff S-008 "None" for V1).
- **Integration point**: insert this text verbatim:

  > **Execution contract (both adapters).** A coordinator-owned manifest `<output>/panel/manifest.json` (PROPOSED) carries run state `frozen -> resolved -> dispatched -> collected -> calibrated -> clustered -> debated -> validated -> published`, plus terminal `failed`. One coordinator writes it; reviewer agents only return data. `frozen` records the reference to `<output>/artifacts/input-snapshot.yaml` and its `input_tree_sha256` (the existing multi-file hash, `SKILL.md:217-229`), the template sha256, tiers sha256, brief-template sha256, schema ids, `run_id`. Each later state records the hashes of the outputs it committed. **Idempotency identity:** `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`. A repeated submission with the same payload hash is a no-op; a different payload under the same identity is rejected. An attempt supersedes an earlier failed attempt of the same reviewer but never adds a vote and never clears a finding. **Resume:** reuse a completed stage only when all its dependency hashes still match; a changed plan or spec hash starts a new invocation. **Publish:** write `REPORT.md`, `return-contract.yaml` and `audit.log` to same-directory temporaries, rename them, then commit `published` in the manifest; a reader accepts only a committed manifest. One total deadline across stages (the ensemble already captures a shared deadline before dispatch, `ensemble.py` per V3, UNVERIFIED line); failed attempts never restart the whole panel.
- **Risk**: Medium. New artifact and a new reader rule. Rollback: delete the block and `panel/manifest.json`; the legacy path never reads it.

### Change 2: Completion states, quorum, and finding `channel` (from Variant 3)
- **Source**: Variant 3, "Finding format" (`completion`, `channel`), C-024, U-015, U-016.
- **Target**: Base, Finding format (append a subsection `Completion and channel`) and Risk list (replace Risk 5 mitigation).
- **Rationale**: C-024 V3 98% (R2 3 of 3); U-015 High; U-016 Medium (advisory no-spec gaps must never become Regression, `agents/reflect-reviewer.md:30`); closes the hole behind INV-010 (already addressed by `ledger.py:150-157`) and informs INV-011/INV-017.
- **Integration point**: append:

  > **Completion states** (per reviewer attempt, recorded in the manifest): `complete`, `truncated`, `invalid` (no parsable findings-v2 block or schema failure), `failed` (transport), `timed_out`. Only `complete` with a valid block counts toward quorum. A valid empty findings array is `complete` only when the card also carries its coverage observations for every assigned row; otherwise it is `invalid`, never "clean". The N=2 floor of `SKILL.md:600` counts `complete` reviewers of distinct classes (Change 30). **Channel** (optional v2 field, default `defect`): `defect | grounding-gap | advisory`. An `advisory` finding is never counted in `deviation_count_by_class` and never maps to Regression.
- **Risk**: Low. Optional fields; v1 lines stay valid.

### Change 3: Judge identity and collision accounting (from Variant 3)
- **Source**: Variant 3, Q3 last paragraph; C-021.
- **Target**: Base, Q3 "Judge class" paragraph (replace).
- **Rationale**: C-021 V3 98%. Verified: `SKILL.md:612` and `reviewer-spec.md:112-116` say sc-adversarial owns judge selection and reflect only delegates disjointness. Base's "pass K1 classes to sc-adversarial if it accepts" is UNVERIFIED and stays UNVERIFIED.
- **Integration point**: replace with: "Reflect does not pin a judge (`SKILL.md:612`). After the debate returns, the adapter records `judge_identity` (as reported by `sc-adversarial-protocol` in its return contract, UNVERIFIED which field) and sets `judge_class_collision: true` when the judge class equals a reviewer class or the executor class; a collision is telemetry plus a REPORT.md note, never a silent pass. Whether `--compare` accepts a judge-exclusion input is UNVERIFIED; if it does not, the collision is recorded, not prevented. Fable and Tier 0 are never a judge: the adapter asserts the recorded judge model id is not `claude-fable-*` and not a `tier0` alias."
- **Risk**: Low.

### Change 4: Cost model restructure with honest units (from Variant 3)
- **Source**: Variant 3, Cost model; C-012, X-012, X-013, X-014, X-015, A-005, S-011.
- **Target**: Base, "Cost model" (restructure) and Q7 numbers.
- **Rationale**: X-012 V3 98%, X-013 V3 98% (V1's before-high 96k and after-high 68k exceed the kill line), X-014 80%, X-015 90%, A-005 98%. Verified: `cost-profile.yaml:42,50-51,54` ("1 turn ≈ 1k claude tokens", T2 35000-70000, turn midpoint 52), `cost-profile.yaml:70` (1.25 hard kill), `SKILL.md:269-270` (N >= 65 means no constraint, 52 x 1.25 = 65).
- **Integration point**: rewrite the section as three separated bases, never summed:
  1. **Published profile (claude-orchestration tokens, turn-budget unit):** T1 3k-8k plus 2k-5k auggie; T2 35k-70k plus 10k-25k auggie; hard kill about 65k (`cost-profile.yaml:36-39,46-51,70`; 52 x 1.25 = 65, or 65.6k from the 52.5k arithmetic midpoint). The panel does not change `cost_profile_version`.
  2. **Output-token planning estimate for a T2 run reaching T2 (3 reviewers), lane by lane** (V3's table, adopted as the planning basis): legacy 42k-66k (`10+21+3+6+2` to `16+30+6+10+4`); panel-parity with the debate kept 37k-56k (`8+18+3+6+2` to `12+24+6+10+4`), midpoint 54k to 46.5k, about 14% saving, labelled **hypothesis, not a result**. The debate lane is 6k-10k in both. V3's 37k-53k "target" assumes a 6k-7k debate; 37k-56k is the allowance; say so in one sentence (X-014). Parity differs from legacy only by +0.5k per card for the findings block (+1.5k) plus the possibly shorter cards; do not claim the saving.
  3. **Recorded artifact sizes (bytes/4)** 55k-93k are a sanity bracket only; they include copied input and are not provider usage.
  V1's 49k-96k legacy estimate is kept as a footnote: its high end exceeds both the profile's 70k band top and the 65k kill line, so it is not used for any threshold (X-013). PN1 figures (408k loop, 23k + 3 x 68k-108k first review, `LEDGER-RESULTS.md:19,66`) stay a comparison only.
  Deterministic-merge variant (deferred candidate E'): legacy debate lane removed, 31k-46k (V3: 37k-56k minus 6k-10k), not production behavior.
  Add the rule: panel T2 must stay inside the existing 35k-70k profile band and below the 65k kill line at p95 (a measurement criterion, Change 28).
- **Risk**: Medium. Numbers are estimates; the section must not present any as measured.

### Change 5: Embedded calibration; remove the findings-only sidecar (from Variant 3)
- **Source**: Variant 3, Q2 and `submission.card`; X-008, X-009, A-004.
- **Target**: Base, Finding format table rows `calibrated_confidence` and `validator_status`, the paragraph "The calibrator writes a PROPOSED sidecar...", Q1 row "Blind calibration", adapter pre step 6 and 8, post step 5-6.
- **Rationale**: X-009 V3 98% (intra-V1 gap: post step 8 passes `--compare <calibrated cards>` while the sidecar keeps calibration out of cards); X-008 V3 90%; A-004 REJECT 3 of 3. Verified on the recorded card: calibration is an embedded `calibration:` block with `calibrator_model_class`, five `dimensions`, `C`, and `per_finding` entries with `finding_confidence` and `reason` (stoprule `reviewer-1-card.yaml:82-103`). `ledger.py:86-90` carries no calibration, so the card is the only carrier.
- **Integration point**: delete `panel/calibration.json` and `panel/validation.json`. State: "The calibrator appends the existing `calibration:` block to the card, exactly as today. The findings-v2 block does not carry calibrated confidence; reflect joins `calibration.per_finding[id]` to findings by (reviewer_id, finding id). A reviewer line that sets `calibrated_confidence` is rejected. The evidence validator's results stay where Wave 5 writes them today." Remove "reviewer output is never mutated" (it was true only of the sidecar design; today's card is mutated by the calibrator).
- **Risk**: Low.

### Change 6: Keep the debate in pre and post; removal becomes a gated later experiment (from Variant 2, Variant 3)
- **Source**: Variant 2, Q3 and Stage 5 (C2); Variant 3, Q3; C-006, X-006, A-008, X-005.
- **Target**: Base, Summary paragraph 2, Candidate C "Changes", Q3, Chosen-architecture reason 3, candidate E, comparison matrix rows "Debate" and "Contract change" (restructure).
- **Rationale**: C-006 V2 90% (R1 V2 3 of 3; V1 moved in R2); X-006 V2 90%; A-001 V2 98%; A-008 V3 80%. EV-2 forbids a self-built merge (`SKILL.md:789`), so keeping the debate is the only legal choice today (INV-025 ADDRESSED).
- **Integration point**: Q3 "Direct answer" becomes: "The debate stays in both modes. K4 clustering runs as deterministic preparation and telemetry; it is not the merge. Removing the pre debate is a later, versioned experiment (candidate E') that needs its own T1-armed measurement and a major contract version." Remove every sentence that says the debate is removed in pre by default, runs only on disputes under `--depth deep`, or emits `panel_agreement_score`. Keep the lost-without-debate analysis (arbitration of blocking disagreements, narrative synthesis, numeric score) as the reason it is kept; keep the post analysis (class arbitration drives `deviation_count_by_class`, `regression_present`, TurnLedger rollback `SKILL.md:930`, condition 4 `SKILL.md:1472`).
- **Risk**: Medium. It reverses the base's headline; all dependent paragraphs are listed in Changes 40-44.

### Change 7: Engine rule by `launch`, pin before freeze, gateway not claimed for pre (from Variant 2 and Variant 3; resolves X-010 and part of C-008)
- **Source**: Variant 2 Q4 rule; Variant 3 Q4 "PROPOSED launch binding"; C-008 V2 75%, X-010 UNRESOLVED, A-011 STATED.
- **Target**: Base, Q4 (replace the "Agent-session adapter" bullet and the gateway sentence).
- **Rationale**: Verified false in base: "Whether the Agent tool accepts the tier alias as a model override is UNVERIFIED". The Agent tool's `model` parameter in this harness accepts only `sonnet | opus | haiku | fable`; `claude-gw-tier2[1m]` is not in that set. `review-tiers.default.json:20` says gateway dispatch is "not defined yet" and `launch` is `{}` (line 23). The headless swarm lens is post-only (`ensemble.py:797`). `reflect-reviewer.md:6` has `model: sonnet` in frontmatter, so omitting the override runs Sonnet for every reviewer.
- **Integration point**: replace the bullet with:

  > **Agent-session adapter (pre-execution).** For each reviewer in the K1 resolution: if `launch` is non-null and in the whitelist `{sonnet, opus, haiku}`, spawn `~/.claude/agents/reflect-reviewer.md` (project `.claude/agents/` first) with the Agent-tool `model` set explicitly to that value. The adapter must pass `model` on every dispatch (omitting it would run the agent's frontmatter default, Sonnet, for all reviewers); a conformance check asserts one explicit `model` per reviewer before dispatch. If `launch` is null (every gateway model today) the resolution is **refused for pre-execution**: the run uses the legacy rotation and records `panel_fallback_reason: no-launch-alias`. No swarm dispatch is claimed for pre-execution; the swarm lens stays post-only. The resolution is pinned (hashed template, tiers, seeds, executor-class exclusion result) before any reviewer is dispatched and is never re-resolved mid-run. Gateway agent-session dispatch is an open item (O-4); the first stage that supports it needs its own conformance run.

  Delete "the adapter then uses the tier alias ... as a ccsession model alias" and the Stage-1 exit check about the alias (it is answered, not pending).
- **Risk**: Medium. It narrows pre-execution support to anthropic-only. Safe default is legacy for any unsupported cell.

### Change 8: Forbidden-model filter, Tier 0, and the `launch` whitelist (from Variant 2; corrects X-020)
- **Source**: Variant 2 U-013 and Risk 7; X-020 V2 98%.
- **Target**: Base, Q4 last paragraph "Fable and Tier 0 are never listed" and Risk 7 (replace).
- **Rationale**: Verified: `review-tiers.default.json:14,27,29` list `claude-fable-5-1` in `names`, in the anthropic-only `available`, and in `launch` (`"fable"`). `panel.py:30` `_TIER = ^tier[0-9]{1,2}[a-z]?$` accepts `tier0`; nothing in `cli/review` mentions Fable (grep over `cli/review`, only the tier json). Base said `launch` maps to sonnet, haiku, opus only.
- **Integration point**: replace with: "The tier file maps four ids in `launch`, including `claude-fable-5-1` to `fable`. Reflect profile validation (PROPOSED, in the kernel, applied to every `reflect-*` template and to every resolution): (1) reject any resolved model id matching `claude-fable-*`; (2) reject any template slot whose tier is `tier0` or whose alias list contains a Tier 0 model; (3) reject a `launch` value outside `{sonnet, opus, haiku}` at dispatch. The same filter applies to the calibrator pick and to the recorded judge identity (Change 3)." Risk 7 becomes the corresponding probability/impact line (Change 21).
- **Risk**: Low.

### Change 9: Reviewer-count cap and the 15-point gate (from Variant 2; resolves INV-016)
- **Source**: Variant 2 Q7 rule and First measurement; C-013 V2 75% (V3 dissents); INV-016 MEDIUM.
- **Target**: Base, Q7 "A full panel is not worth calling" list and Risks (append) (insert).
- **Rationale**: `panel.py:142` allows 1..8 reviewers; `SKILL.md:86` limits reflect to 2-3. A numeric gate alone does not stop a 7-slot template from running 7 reviewers against the 65k kill.
- **Integration point**: add: "**Code-level cap (hard):** reflect-profile validation rejects any `reflect-*` template or resolution with more than 3 reviewers, whatever the user template says (the generic panel keeps 1..8 for `/sc:spec-panel`). `N_eff = min(--reviewers (default 3), alias-derived count from SKILL.md:233-239, 3)`; a fixed anchor is never dropped; trailing random slots are dropped first. **Raising the cap** to 4+ needs (PROPOSED, labelled as such because V3 dissents) a measurement showing T2 recall beats T1 recall by at least 15 percentage points and the larger panel beats T2 by a margin the owner accepts. Larger panels are never an automatic response to `--depth deep` (V2 Q7 allowed 4+ on `--depth deep`; rejected: `--depth deep` forces T2 and routes remediation, `SKILL.md:89,365`, and says nothing about reviewer count)."
- **Risk**: Low.

### Change 10: Real-card evidence for the calibrator and validator, and the card format facts (from Variant 2)
- **Source**: Variant 2, Candidate B/C reasons 2; U-009 High; A-003.
- **Target**: Base, Chosen architecture reason 2 (append) and Finding format (insert a paragraph "What a recorded card looks like").
- **Rationale**: U-009 High. Verified on the stoprule card: findings are YAML with `severity: blocking|minor`, categories `ordering|acceptance|deviation|coverage|risk`, `evidence: [plan:57, source.md:62, src/...:451-462]` (line refs, no quotes), orchestrator-written `model_class: sonnet`, `persona`, `plan:` and `spec:` paths; the calibrator scored F1-F3 at 0.60, 0.50, 0.55 ("fit major better than blocking"); the final gate dropped `source.md:143` (a heading) which a "quote locates" check would pass (per V2, `REPORT.md:130-132`, not re-read by me).
- **Integration point**: append: "Evidence that the gates carry load: [the three facts above]. Consequence for the design: a deterministic locate check cannot replace the semantic re-read (Change 31), and the recorded card gives line references, so findings-v2 `citations[]` are built from `path:line` refs with `quote` optional (Change 37)."
- **Risk**: Low.

### Change 11: Ablation arm, per-source section layout, and `reflect_category` (from Variant 2)
- **Source**: Variant 2 U-012, U-011, U-010.
- **Target**: Base, First measurement (append arm D), Finding format (extend `category` row and add a mapping table), Adapter post step 3 (insert layout note).
- **Rationale**: U-012 Medium (2 reviewers plus an Opus calibrator versus 3 with Haiku stand-ins); U-011 Medium used only as a per-source section layout, not as a concatenated identity store (X-007 V3 75%); U-010 Low. Base's `category` row extends the v1 enum by four values but the recorded card uses `ordering`, `acceptance`, `risk`, `coverage`, which the extension lacks.
- **Integration point**: (1) `category` row: "v1 six-value enum unchanged; reflect's original label is preserved in `reflect_category`; mapping: `ordering`->`other`, `acceptance`->`unpassable-check`, `coverage`->`missing-requirement`, `contradiction`->`contradiction`, `risk`->`safety` or `other`, `deviation`->`other` with `deviation_class` set. Severity mapping: `blocking` -> MAJOR or CRITICAL with `blocking: true`, `minor` -> MINOR." (2) Measurement arm D = panel-lite template (sonnet, haiku, calibrator Opus) run on the pilot only (Change 28). (3) Post audit bundle: each grounding hunk is an H3 `path:start-end` heading in the reviewer's brief (the shape reviewers already receive, `reviewer-spec.md:45`); it is a per-source layout inside the brief, never a concatenated document that identities are computed against.
- **Risk**: Low.

### Change 12: Answers in place for Q5 and Q7 (from Variant 3)
- **Source**: Variant 3 Q5, Q7; S-005 V3 90%.
- **Target**: Base, Q5 and Q7 (restructure: keep the forward pointer but state the answer first).
- **Rationale**: S-005 L2 V3 90%: answers available in place; base Q5 and Q7 only point forward.
- **Integration point**: Q5 gets a 6-line in-place answer (inputs plan+spec; Wave 0-2 unchanged; resolve with executor exclusion; dispatch; per-card blind calibration; debate on cards; evidence gate; contract 1.8.0 unchanged; the T1-stop rule and flag order from Change 39), Q7 gets the 4-line answer of Change 4 and Change 9. The step-by-step flow stays in "Adapter sketches".
- **Risk**: Low.

### Change 13: Conventions paragraph (from Variant 2)
- **Source**: Variant 2 opening paragraph; S-003 V2 75% (V1 dissent: separates enrichment provenance from lines read).
- **Target**: Base, opening paragraph (replace).
- **Rationale**: S-003 keeps citations auditable. Keep V1's "(enrichment)" provenance marker too, because it records which lines V1 did not read itself.
- **Integration point**: new text: "Paths are relative to `src/superclaude/` unless they start with `.dev/`. `path:line` cites are lines read in the drafting or verification sessions; "(enrichment)" marks a line taken from the enrichment file; "(plan-verified)" marks a line the refactor plan re-read. PROPOSED = a new name, not an existing file, flag, function or schema. UNVERIFIED = not read. Token figures are estimates unless a source is cited; units are named. Installed primitives are named by installed path (`~/.claude/...`) or the `superclaude` CLI, never by `src/superclaude/...` (CLAUDE.md rule). `<out>` abbreviates the reflect output directory."
- **Risk**: Low.

### Group B. Corrections of base claims

### Change 14: Contract-version facts (X-003) and the wrapper's major-version gate
- **Source**: Verification; diff X-003 (verified false in all three variants).
- **Target**: Base, "Return-contract 1.8.0 mapping" opening and "Consumer by consumer" (replace the Headless contract builder bullet and the wrapper bullet).
- **Rationale**: X-003 UNRESOLVED (50) in the matrix only because all three misread it. Verified: `ensemble.py:74` `REFLECT_CONTRACT_VERSION = "1.0"`, written at `ensemble.py:788`, with `"mode": "post"` at `:797`. The recorded interactive pre contracts say `contract_version: "1.8.0"` (37 of 42 under `.dev/reflect/pre-*`; others 1.0, 1.2.0, 1.3.0, 1.5.0, 1.7.0). **New fact the base missed:** `contract.py:187-194` makes the wrapper return BLOCKED `unknown-major-version` for any `contract_version` whose major is not `1`. Base's 2.0.0 plan said "legacy runs emit 2.0.0 values" and only listed triggers 11/11b; under that plan the wrapper would BLOCK every 2.0.0 contract it reads (fixture `tests/cli/reflect/fixtures/blocked_unknown_major.yaml` exists, per grep). Also verified: the only other `contract_version` equality in `src/` is `sc-implement-protocol/scripts/archive_workspace.py:327` (`!= "1.1"`), a different contract.
- **Integration point**: replace with: "Two producers exist: the interactive skill (1.8.0, pre and post) and the headless ensemble builder (`ensemble.py:788`, constant `"1.0"`, post only). The wrapper accepts any major `1` and BLOCKS any other major (`contract.py:187-194`), then applies degraded/halted triggers 1-14. No change to any of these is needed while the contract stays 1.8.0. Any future major version (Change 15, deferred candidate) must first change `contract.py:187-194`."
- **Risk**: Low (text correction).

### Change 15: Rewrite the versioning plan and the contract mapping (X-004, X-005, C-015, C-016)
- **Source**: Variant 3 "Return-contract 1.8.0 mapping" (adopted table); Variant 1 consumer list (kept and moved to the deferred path).
- **Target**: Base, "Return-contract 1.8.0 mapping" in full (restructure).
- **Rationale**: C-015 V3 98%, C-016 V3 98%, X-005 V3 98% (`merge_method: panel` violates the exact legal set `SKILL.md:789` and EV-1 `SKILL.md:666`); X-004 V1 98% (a widened legal set is a major change, `SKILL.md:952-953`). Both V1 and V2 labelled the new value additive 1.9.0 or required a 2.0.0 that breaks the wrapper (Change 14).
- **Integration point**: replace the section with the following.

  > **Versioning plan.** Stages 0-4 change no stable field: `contract_version` stays `1.8.0` for interactive runs; no field is added to the stable block; panel data lives in referenced artifacts (`<out>/panel/*`) and in the non-stable telemetry block (`SKILL.md` two-block contract). **Bump rule (applies to every later proposal):** a new top-level stable field = minor (`SKILL.md:952`); a new legal value of an existing field, a changed meaning, a gate-text change = major (`SKILL.md:953`); a new telemetry-only field = no bump. A contract lint test (Change 27) enforces this on panel runs.
  >
  > | Contract field or family | Source in the panel path | Status |
  > |---|---|---|
  > | `contract_version` | constant `1.8.0` (interactive builder); headless builder constant `"1.0"` untouched | unchanged |
  > | `status`, `mode`, `tier_reached` | existing reduction; `tier_reached` is 2 only when the floor of Change 30 holds | unchanged meaning |
  > | `merge_method` | `adversarial` from the real `sc-adversarial` run; `single-reviewer-fallback` via the F2 path | unchanged legal set |
  > | `adversarial_convergence_score` | the child's `convergence_score` or null; never synthesized | unchanged |
  > | `adversarial_unavailable`, `adversarial_artifacts_dir` | F3 path as today; mechanical remap `artifacts_dir` -> `adversarial_artifacts_dir` (`SKILL.md:657`) | unchanged |
  > | `reviewer_cards` | calibrated card paths (cards carry the findings-v2 block and the embedded `calibration:`) | unchanged |
  > | `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `calibrator_diversity` | computed with the same rules as the legacy path from the resolved classes (parity template, Change 23) | unchanged semantics; values asserted equal on matching inputs by the lint test |
  > | `citations_total/revalidated/dropped`, `evidence_validator_ran` | validator results; pre-check only flags (Change 31) | unchanged semantics |
  > | coverage, deviation, verification, reachability, promotion, remediation fields | reflect waves | unchanged |
  > | `panel_*`, `cluster_agreement`, `manifest_path`, `t2_engine_requested/effective`, `identity_source` | telemetry block / artifacts | non-stable, no bump |
  >
  > **Null-score rules.** Route on `merge_method` first (`SKILL.md:661`). `adversarial_convergence_score` is a real child score or null; null enters only on the F3 path, a skipped debate (Change 33) or a failed child; no synthetic 0, 0.5 or 1.0. A null at T2 stays `status: partial` and blocks promotion (`SKILL.md:659-664`; wrapper trigger 11 `contract.py:299-300`). `cluster_agreement` is never compared with the convergence thresholds and never routes anything.
  >
  > **Deferred versioned change (candidate E', not scheduled).** A deterministic authoritative merge in pre would add `merge_method` value `panel` (pre only), which is a major version, `2.0.0`. Every consumer that must change first: (1) `contract.py:187-194` major gate; (2) `contract.py:295-300,317-326` triggers 10, 11, 11b (guard on `merge_method`); (3) `ensemble.py:74,772-773,788,806` builder constant and merge-method derivation; (4) reflect `SKILL.md` EV-1 (`:666`), EV-2 (`:789`), the §9.4 note, and promotion condition 9 text (`:1483`); (5) `task-builder` SKILL.md EV-4 (line 2242: requires `merge_method: adversarial` on disk for post); (6) `refs/ops-integration.md:239` (`adversarial.merge_method` PromQL label values); (7) the meta-eval aggregator that reads `convergence_score` (`SKILL.md:941`); (8) the sprint executor routing named at `SKILL.md:664` and `:930` (executor code UNVERIFIED); (9) `tests/cli/reflect` (31 fixture files carry `merge_method`; `test_ensemble_unit.py`, `test_ensemble_stub_integration.py`, `test_verdict_mapping.py`, `test_contract_fallback_metadata.py`); (10) `sc-workflow` Wave 4 reads only `reflect_status` and `reflect_report_path` (`sc-workflow-protocol/SKILL.md:60`), no change. The CI grader `.dev/eval-workspaces/sc-reflect/grader.py` has no match for `merge_method`, `contract_version` or `convergence` (grep), so it needs no change today.
  >
  > **Promotion gate condition 9 (`SKILL.md:1483`).** Unchanged in every planned stage: the retained debate keeps a real merged adversarial verdict on every T2 run. The condition's operative test is `tier_reached == 2 AND adversarial_unavailable == true` (blocked), and its `convergence_score` is the prose name of `adversarial_convergence_score` (A-015); both stay as written. Promotion is UC-2 only (`promotion_gate_passed` is null when `mode == pre`, `SKILL.md:837` per V1, UNVERIFIED line).
  >
  > **`reflect_post` frontmatter** (`cli/reflect/runner.py:103-133`): unchanged in every stage. Fields are verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at and the three `*_verified` booleans, in a fixed order; no merge field. The wrapper writes it for post runs on a tasklist only; the pre adapter never writes it. Do not add panel fields to it.
  >
  > **Consumers.** [keep V1's consumer bullets for sc-workflow Wave 4, sprint TurnLedger, troubleshoot/task/task-builder/workflow T3, roadmap/tasklist gates, Wave 7 promotion, CI grader, meta-eval, each with the statement "no change while the contract stays 1.8.0"; delete the "2.0.0 change" annotations and move them to the deferred list above.]
- **Risk**: High. It is the most consequential rewrite; mitigated by the lint test and by keeping the deferred list explicit.

### Change 16: Gate-9 and EV-1 wording check
- **Source**: Verification of `SKILL.md:666,1483`.
- **Target**: Base, "Gate condition 9" paragraph and adapter pre step 11 "EV-1 for the panel path" (replace).
- **Rationale**: Base step 11 proposed "PROPOSED wording" for EV-1 on `panel/ledger.json`; with the debate kept, EV-1 is unchanged: `merged-verdict.yaml` with `merge_method: adversarial` plus at least the resolved `--reviewers` count of calibrated cards, or a corroborated F2/F3 fallback (`SKILL.md:666`). Base's sentence that cond. 9 "stays literally true" is correct but cites the wrong operative test.
- **Integration point**: replace step 11 with: "EV-1 is unchanged. The count it compares is the resolved reviewer count of the K1 resolution after exclusion (the manifest records requested, resolved and complete counts separately, Change 30)." The gate-9 paragraph is the text in Change 15.
- **Risk**: Low.

### Change 17: Ledger role, `--cap 1`, and ledger line cites (X-017, X-018)
- **Source**: Verification of `ledger.py:93-96,107,114-118,150-157,184-203,213-222`; X-017 V3 90%; X-018 V2 90%.
- **Target**: Base, Q3 pre bullet 1, Q6, Staged table, Risks (replace statements that cite or use the ledger).
- **Rationale**: Verified: `_decision` returns `REVISE if n < cap else ESCALATE` (`ledger.py:93-96`), so with `--cap 1` every blocking round records `ESCALATE` (base listed this UNVERIFIED). `merge_round` starts at `ledger.py:107`; the OR of `blocking` and `severity_max` for a new row is at `:187-190` (not `:213-222`, which is the re-found branch where the current report decides blocking); `merge_round` spans `:107-298` (not `:200-298`). A ledger stores a bare `span` per row (`:196-197`) and one `doc_sha256` per round (`:278-279`).
- **Integration point**: Q6 becomes: "Reflect is single-pass (`SKILL.md:342`). **The panel ledger is not used for reflect in Stages 0-4:** the merge is the `sc-adversarial` debate; K4 clustering writes `panel/clusters.json` and needs no rounds, no REVISE/ESCALATE decision and no `doc_sha256`. If a later stage uses the ledger, run it with `--cap 1` knowing every blocking round records `ESCALATE` (`ledger.py:93-96`), reflect must ignore `decision`, and telemetry must not surface it as an escalation. Each merge attempt gets its own ledger path (Change 29)." Fix the cites to `ledger.py:187-190` and `:107-298` wherever V1 states them.
- **Risk**: Low.

### Change 18: Recorded convergence evidence (X-006) corrected
- **Source**: Verification of local recorded contracts; X-006 V2 90%.
- **Target**: Base, Summary sentence "has separated nothing in recorded runs (convergence 1.0 in 4 of 5)", Q3, candidate E verdict, Risk 1 (replace).
- **Rationale**: Base claims the debate "separated nothing". The base's five-run sample is a subset. Grep over `.dev/reflect/pre-*/return-contract.yaml` finds 42 `adversarial_convergence_score` lines: 21 equal 1.0, 14 are below 1.0 (0.40, 0.76, 0.80, 0.852, 0.88, 0.885, 0.8889, 0.889, 0.92, 0.94, 0.947, 0.95, 0.9583, 0.9615), 7 are null; contract versions are mixed (1.0 to 1.8.0), merge methods include 5 `single-reviewer-fallback` and several pre-EV-2 illegal values (`adversarial-inline`, `inline-orchestrator`, `none`). Agreement is not recall (V3, R1); the debate produced non-unanimous scores in 14 of 35 numeric recorded runs.
- **Integration point**: replace the claim with: "Recorded pre contracts under `.dev/reflect/` show a convergence score of 1.0 in 21 of 35 numeric cases and below 1.0 in 14 (0.40 to 0.9615); 7 are null (mixed contract versions, 5 `single-reviewer-fallback`). These are agreement observations, not defect-recall measurements, and vendor diversity was single in the recorded T2 runs the enrichment cites. They do not show the debate is idle." Keep "advisory" for pre.
- **Risk**: Low.

### Change 19: Opus-use list and the calibrator/diversity claim (X-016, C-018, U-005)
- **Source**: Variant 1 Q4 "Side effect" paragraph; Variant 3 Q3 Opus rule; X-016 V1 90%, C-018 V1 90%.
- **Target**: Base, Q4 "Side effect worth stating" and Risk 7 (replace); add a section `Opus uses` after Q4.
- **Rationale**: Base says Opus is used "only here" (calibrator) while also listing `@reflect-enterprise` with an Opus reviewer: not "only here". `SKILL.md:1181` already selects the highest-capability disjoint class, so an Opus calibrator is today's rule (V1 R2, V2 R2 side with V1; V3 reads "sparingly" as a reason to avoid it, conceded as a policy change). `SKILL.md:607` and `reviewer-spec.md:97,108` already use Opus as the third reviewer or backfill. U-005's claim (calibrator diversity improves to `full`) holds only for the lite template (Opus is not a reviewer); for the parity template the disjoint set is empty and `calibrator_diversity` stays `degraded`, as in the recorded card (`calibrator_model_class: opus`, `calibrator_diversity: degraded`).
- **Integration point**: add:

  > **Opus uses (complete list; the owner's ceiling is "Opus only sparingly").** (1) Blind calibrator, chosen by the unchanged rule of `SKILL.md:1181-1186` (highest capability from the set disjoint from reviewers, else the class used by fewest reviewers, with `calibrator_diversity: degraded`). (2) Third reviewer in the anthropic-only parity template, exactly where today's rotation puts it (`SKILL.md:607`), and as backfill when the executor class is removed (`reviewer-spec.md:108`). (3) Reviewer in the opt-in `--strategy enterprise` template (`SKILL.md:608`). (4) Never as a judge pinned by reflect (`SKILL.md:612`). No use is new relative to today. The lite template (variant arm only) moves use (2) to use (1): its calibrator diversity becomes `full`, its model-class diversity falls from three classes to two, which the interactive skill labels `degraded` (`SKILL.md:237-239`). That value change is why lite is a measured arm and not the first shipment. Fable and Tier 0 are never used.
- **Risk**: Low.

### Change 20: Internal-consistency fixes (IC items in scoring-quant.md)
- **Source**: scoring-quant.md contradiction list; base-selection "IC items".
- **Target**: Base, candidate C Cost line, Q7, Cost model, comparison matrix.
- **Rationale**: Two IC items: pre cost "34-66k" (candidate C) versus "35-68k" (cost model); candidate E "no contract version change" versus the comparison row "1.9.0 additive".
- **Integration point**: candidate C cost becomes "37k-56k output-token planning estimate with the debate kept (Change 4), inside the profile's 35k-70k band"; delete every "34-66k" and "35-68k". The comparison matrix row "Contract change" reads: A none, B major, C (chosen) none (1.8.0), D none, E' major (2.0.0, deferred). No "1.9.0 additive" appears anywhere.
- **Risk**: Low.

### Change 21: Risks with probability and impact (RISK-1)
- **Source**: base-selection (V1 RISK-1 NOT MET in both passes).
- **Target**: Base, "Risks" (restructure: replace the list with a table).
- **Rationale**: no per-risk probability; all three variants lacked it.
- **Integration point**: replace with this table (probability = my estimate with the basis stated; impact = consequence; mitigation = design element):

  | # | Risk | Prob. | Impact | Mitigation |
  |---|---|---|---|---|
  | 1 | The debate matters and clustering cannot replace it | n/a (debate kept) | Medium | kept; E' needs its own measurement and a major version |
  | 2 | Panel-fed T2 is worse than legacy T2 | Medium: reviewer classes match (parity) but format, brief line and dispatch plumbing differ | High | Stage 2 shadow, first measurement NI test (Change 28), legacy default |
  | 3 | Executor exclusion fails open or empties the anchor | Medium: `panel.py:402-409` silent paths are real | High | kernel hard exclusion, per-slot skip, post-resolve assertion, tests (Change 24) |
  | 4 | Reviewer identity not what was requested | Low-Medium: the tool pins `model`, but omitting it runs Sonnet (`reflect-reviewer.md:6`) | High | explicit `model` check, probe spike (Change 26) |
  | 5 | Format non-compliance (invalid findings block) | Medium for Haiku-class reviewers (card format varies today) | Medium | one bounded re-ask; legacy card body still reaches the debate; compliance rate in telemetry |
  | 6 | Consumer or test relies on a 1.8.0 value that shifts | Low (grep shows no `contract_version == 1.8.0` check, no grader match) | High | lint test, consumer grep gate, parity (Change 27) |
  | 7 | Multi-file clustering merges unrelated findings | Low (path-aware, conservative) / split risk Medium | Low: telemetry only | Change 25, 50-pair hand label at Stage 0 |
  | 8 | Opus creep | Low: no new use | Medium | the Opus list (Change 19) |
  | 9 | Two engines drift again | Medium | Medium | one resolution file, one contract-lint, one builder function for post at Stage 5 |
  | 10 | Pre T2 exceeds the 65k kill | Medium at the legacy high end | Medium | p95 criterion, cap of 3 reviewers (Changes 4, 9) |
  | 11 | Interactive and wrapper disagree on a 2-of-3 run | High (exists today: `SKILL.md:666` calls it MALFORMED, `ensemble.py:765-770` records benign `reviewer-shortfall`) | Low-Medium | preserved, counted at Stage 2 (Change 30) |
  | 12 | Gateway cell silently routed through an unsupported path | Low | High | refusal rule (Change 7) |
- **Risk**: Low.

### Change 22: Assumptions and UNVERIFIED inventory update
- **Source**: Verification.
- **Target**: Base, "Assumptions and UNVERIFIED items" (replace the affected bullets).
- **Rationale**: Base listed items I verified or can now answer.
- **Integration point**: move to VERIFIED with cites: (a) `superclaude review panel resolve` options are `--template`, `--tiers`, `--env`, `--run-id`, `--kind first|re-review`, `--seed`, `--sequence` (`panel_cmd.py:18-52`); `--exclude-class` and `--strict-distinct` do not exist (PROPOSED); (b) `validate_panel` rejects unknown slot keys (`panel.py:109-111`, `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}` at `panel.py:46`), so exclusion cannot be a template key and must be a resolve-time parameter; (c) `_decision` with `--cap 1` (Change 17); (d) no `contract_version == "1.8.0"` equality in `src/` (Change 14); (e) the CI grader has no `merge_method` match; (f) `A-7` (wrapper post-only) is verified at `ensemble.py:797`; (g) `refs/reviewer-spec.md:31-74,55,94-98,112-116` and `cost-profile.yaml` cites are re-read and correct. Keep as UNVERIFIED: `sc-adversarial` judge-exclusion input; how `sc-adversarial` scores a skipped debate (`SKILL.md:409,951,439,457` says skip when variants differ by under 10% and score is "null if debate not reached"); the Agent-tool reply carrying a model id; `cli/reflect/fallback.py` body; `review-telemetry/1` schema; sprint executor code; `refs/report-template.md`; whether the `reflect-reviewer` tools allowlist survives a `model` override (Change 30, INV-009).
- **Risk**: Low.

### Change 23: Template set, validity, and the parity template (corrects the base template and resolves C-009/X-001 consistently)
- **Source**: Variant 1 Q4 JSON; X-001 V1 90%; C-009 V1 90%.
- **Target**: Base, Q4 "Model-class rotation versus T2Model slots" (replace the JSON block and the bullets after it).
- **Rationale**: V1's template is the only validator-legal one (one fixed slot, `panel.py:140-141`; slot ids match `^[a-z0-9]{1,8}$` `:31`; keys within `_SLOT_KEYS` `:46`). But it changes the anthropic-only reviewer set to sonnet, haiku, haiku and Opus to the calibrator, which changes `t2_model_class_diversity` (Change 19). Parity requires a third slot on `tier1a` (`review-tiers.default.json:5`: opus, sonnet).
- **Integration point**: replace with this template set (all packaged as `review-panel.<name>.json`, loadable as `@<name>` per `panel.py:327-334`; each has exactly one `fixed` slot; none lists a tier-0 or Fable tier):

  ```json
  {"schema": "review-panel/1", "template_id": "reflect-pre", "version": "1.0.0",
   "distinct_across_slots": true, "apply_to": ["first"],
   "slots": [
     {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
     {"slot_id": "t4",  "tier": "tier4",  "count": 1, "strategy": "random"},
     {"slot_id": "t1a", "tier": "tier1a", "count": 1, "strategy": "random"}]}
  ```
  `@reflect-pre` (parity, default). Anthropic-only resolves to sonnet, haiku, opus under strict distinctness (Change 24): tier1b -> sonnet; tier4 -> haiku (stand-in list `review-tiers.default.json:28`); tier1a minus {sonnet, haiku} -> opus. Persona by resolution order: fixed first, then slot order: analyzer, qa, refactorer (matches `reviewer-spec.md:97`).
  - `@reflect-pre-x2` (anchor replacement when tier1b is exhausted by the executor, i.e. executor `sonnet` in anthropic-only, where tier1b has only Sonnet and no stand-in, `review-tiers.default.json:6,28`): fixed `t4` anchor plus random `t1a`. Resolves haiku, opus (2 reviewers, analyzer and qa), matching `reviewer-spec.md:102,109`.
  - `@reflect-enterprise`: same slots; third persona `architect`; opt-in for `--strategy enterprise`.
  - `@reflect-lite` (variant arm only): V1's original three slots t1b, t4, t2; resolves sonnet, haiku, haiku (soft) or sonnet, haiku (strict, third slot skipped).
  - Post templates `@reflect-post` and `@reflect-post-x2` mirror pre. Gateway templates are not defined (O-4).
  Delete the claims that anthropic-only "resolves to Sonnet, Haiku, Haiku" as the default and that diversity is full under a 2-distinct rule (the 2-distinct rule is the headless helper's, `_diversity.py:8-15`, which returns `insufficient`, not `degraded`, a vocabulary mismatch with `SKILL.md:790` recorded as O-9).
- **Risk**: Medium. Template files and a second template are new; mitigated by the validator test in Stage 1.

### Group C. Invariant resolutions

Coverage table (all 20 UNADDRESSED): INV-005 -> Change 24; INV-015 -> 25; INV-022 -> 26; INV-023 -> 27; INV-024 -> 28; INV-001, INV-002, INV-003 -> 29; INV-006, INV-007, INV-009, INV-011 -> 30; INV-012, INV-013 -> 31; INV-014, INV-018, INV-019, INV-021 -> 32; INV-020 -> 33; INV-016 -> 9. INV-004, 008, 010, 017, 025 stay ADDRESSED.

### Change 24: INV-005 (HIGH) executor-class exclusion cannot fail open
- **Source**: invariant-probe INV-005; Variant 3 Q4 and C-017/X-002 (filter before dispatch, replace the anchor, degrade not raise); Variant 1 `hard_exclude` and `--exclude-class`; A-006 class map.
- **Target**: Base, Q1 table row "Executor-class exclusion", Q4 text, Pre adapter step 3, Staged table Stage 1, Risk 4 (replace).
- **Rationale**: C-017 V3 90% (3 of 3), X-002 V3 90%, A-006 V1 90%. Verified failure modes: a `fixed` slot returns `candidates[0]` and ignores `exclude` (`panel.py:402-403`); `random` and `round_robin` use `[m for m in candidates if m not in set(exclude)] or candidates` and so re-admit an excluded model when the pool empties (`panel.py:405,408`); `exclude` today carries only models chosen earlier in this panel (`panel.py:479`); `NoModelAvailable` is raised only when no candidate and no stand-in exists (`panel.py:396-401`); the anthropic-only stand-in map has no `tier1b` (`review-tiers.default.json:28`); `review-tiers.default.json:6` lists three tier1b models but only Sonnet is in the anthropic-only `available` (`:27`).
- **Integration point**: replace with the following full text.

  > **K1 hard exclusion contract (PROPOSED code; generic panel behavior unchanged).**
  > 1. `resolve_slot` and `resolve` gain two keyword-only parameters with defaults that reproduce today's behavior byte for byte: `hard_exclude: Sequence[str] = ()` (model ids) and `strict_distinct: bool = False`. They are resolve-time parameters, not template keys (`validate_panel` rejects unknown slot keys, `panel.py:109-111`).
  > 2. Filtering is applied to the **candidate list itself**, before the strategy runs, for all strategies including `fixed`: `candidates = [m for m in candidates if m not in hard]` where `hard = set(hard_exclude) | (set(chosen) if strict_distinct else set())`. Fallbacks (`panel.py:417`) are derived from the filtered list, so no primary or fallback can be an excluded model. The silent `or candidates` re-admission is **not** taken when `hard` is non-empty.
  > 3. If the filtered list is empty and the stand-in list has not yet been tried, try `stand_ins` filtered the same way; if still empty raise a new `ExclusionExhausted(tier)` (a subclass of `NoModelAvailable`). With `hard_exclude == ()` and `strict_distinct == False` the code path, output and hashes are identical to today (asserted by a spec-panel byte-identity test, A-014 98%).
  > 4. `resolve` records `skipped_slots: [{slot_id, reason}]` and `excluded: {models, classes}` as additive keys in the `review-panel-resolution/1` JSON; `merge_cmd.py:76-79` reads only `reviewers[*].reviewer_id/model`, so existing consumers are unaffected. A non-fixed slot that raises `ExclusionExhausted` is **skipped** (recorded), not fatal; the fixed anchor raising is fatal at kernel level.
  > 5. **Class map (A-006).** The tier file gains a `classes` object mapping every model id to a class string in the vocabulary of `SKILL.md:1180` where one exists (`claude-opus-5-5: opus`, `claude-sonnet-5-5: sonnet`, `claude-haiku-5-5: haiku`) and a vendor family otherwise (`gpt-*: gpt`, `glm-*: glm`, `grok-*: grok`, `Qwen*: qwen`, `muse-*: muse`). A model id with no entry is **not eligible** in any `reflect-*` template (fail closed at validation). `--hard-exclude-class <class>` (PROPOSED CLI flag on `superclaude review panel resolve`) expands the class to ids through this map and compares case-insensitively with the executor value resolved by `SKILL.md:600-602` (flag, `EXECUTOR_MODEL_CLASS`, or log hint; headless wrapper also reads frontmatter `executor_model_class`, `cli/reflect/config.py:53-56,351-355`). The gateway classes `gpt|glm|grok|muse` are outside the `SKILL.md:1180` calibrator vocabulary; gateway is out of scope until O-4.
  > 6. **Adapter (reflect side) applies the policy, the kernel only enforces:** (a) resolve with `@reflect-pre`, `strict_distinct=True`, `hard_exclude` = ids of the executor class. (b) If the fixed anchor raises `ExclusionExhausted`, re-resolve once with the anchor-replacement template (`@reflect-pre-x2`) before any dispatch; the replacement is recorded (`anchor_replaced: true`). (c) After resolution assert: no resolved model class equals the executor class; no model id repeats; at least 2 distinct classes. (d) Failure of (c), or a second exhaustion, is the `SKILL.md:600` path: `executor_exclusion_degraded: true`, WARN with the text of `SKILL.md:600`, degrade to T1 for rubric-driven escalation. For a pinned `--depth deep` or `--tier 2` run the degrade is never silent: see Change 39 rule D3.
  > 7. **Unknown executor** (`executor_class_source: unknown`): unchanged fail-open of `SKILL.md:602` (`executor_class_resolved: false`, loud WARN); the panel runs without `hard_exclude`. This is the main consumer path today: `sc-workflow` Wave 4 passes only defaults (`sc-workflow-protocol/SKILL.md:60`) and a recorded workflow-driven pre run has `executor_class_source: unknown` (`.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/return-contract.yaml:96-97`). Exclusion therefore rarely fires in the main consumer path; see O-6.
  > 8. **Tests (Stage 1 exit):** excluded model is the fixed anchor; pool empties for random and round_robin slots and the excluded model is not re-admitted; executor `sonnet` in anthropic-only yields `ExclusionExhausted` for `tier1b` and the adapter lands on `@reflect-pre-x2` with 2 reviewers; executor `haiku` skips the `t4` slot; executor `opus` under strict distinctness yields sonnet, haiku and no duplicate; unmapped model id rejected; `hard_exclude == ()` is byte-identical to the current resolution for the default and live7 templates.
- **Risk**: High. It modifies shared kernel code; mitigated by default-off parameters and the byte-identity test.

### Change 25: INV-015 (HIGH) multi-file identity without concatenation and without the ledger
- **Source**: invariant-probe INV-015; Variant 1 dedupe key v2; X-007, C-023, Variant 3 "separate documents".
- **Target**: Base, "Dedupe key for multi-file citations" (replace), pre adapter step 9 (replace), Risk 3 (replace).
- **Rationale**: X-007 V3 75% (single `--doc`: `merge_cmd.py:29-34`; concatenation erases identity); C-023 V1 90%; C-005 V1 75% with the primary-citation fix, V3 dissent. Verified problems in today's code: the ledger row stores a bare `span` list with no path (`ledger.py:196-197`) and each round one `doc_sha256` (`:278-279`); `findings._spans` returns spans without a path and `same_defect` compares any two spans within 3 lines (`findings.py:363-379`), so two findings at line 10 of different files merge; clustering is transitive (`findings.py:382-407`). V1's role-qualified multi `--doc` does not exist and would still feed that path-blind row.
- **Integration point**: replace with:

  > **Multi-file identity (PROPOSED K4 `cluster_v2`).** Reflect does not use `review merge` or the ledger in Stages 0-4 (the merge is the debate), so no path-blind row exists. K4 is a pure function `cluster_v2(findings_v2_blocks, snapshot_file_list) -> clusters` exposed as `superclaude review cluster` (PROPOSED), writing `<out>/panel/clusters.json`.
  > 1. **Citation tuple.** Each citation is `(role, path, line_start, line_end)` with `path` repo-relative and verified against `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), whose `file_list` gives each file's sha256. A citation whose path is not in the snapshot file list is `unresolved` and never joins a cluster by span. Spans are 1-based inclusive line ranges taken from the citation itself (no `locate` call needed; `quote` is optional, Change 37).
  > 2. **Primary citation** = the first citation whose `role` is the reviewed artifact (`plan` in pre; `source` or `diff` in post), else the first citation.
  > 3. **`same_defect_v2(a, b)`** is true only if (i) deviation classes are compatible (equal, or either null or `none`), **and** (ii) the `refs_norm` sets intersect or are both empty (same normalization as `findings.py:321-337`), **and** (iii) some citation of `a` and some citation of `b` have the **same `path`** and spans within 3 lines (`a.start <= b.end + 3 and b.start <= a.end + 3`, the tolerance of `findings.py:377`). Equal fingerprints (`sha256("v2|" + role + "|" + path + "|" + section + "|" + refs + "|" + class)`) with non-empty refs also match, as in `findings.py:371-372`. **Two findings that cite different paths never match by span.** Two findings that cite the same spec requirement from different plan tasks match only through a shared `spec` path span plus a shared requirement ref.
  > 4. **Transitivity guard.** Clusters are union-find components (as `findings.py:382-407`); each cluster is marked `chained: true` when it contains two members that do not match pairwise. `chained` clusters list their members and are never treated as one issue for counting (INV-014, Change 32).
  > 5. **Per-source identity.** The brief carries each source as its own H3 `path:start-end` hunk (`reviewer-spec.md:45`); there is no concatenated review document and no `review-doc.md`.
  > 6. **Tests (Stage 0 exit, positive and negative):** two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines and equal refs do cluster; a three-member chain A-B-C with A and C pairwise unequal is `chained`; v1 reports through the unchanged `review merge` produce byte-identical output with and without the new module imported (A-014).
  > 7. **If the ledger is used later** (not planned), rows need `citations[]` (path-aware) and a `ledger/2` schema; that is a separate change, recorded as O-5.
- **Risk**: Medium. New clustering code, but it is telemetry-only while the debate decides.

### Change 26: INV-022 (HIGH) executor exclusion is enough only if eight gates hold, including identity read-back
- **Source**: invariant-probe INV-022 gate list; X-002, X-010, A-006.
- **Target**: Base, new subsection `### Executor-exclusion gates` after Q4 and Pre adapter step 3/5 (insert).
- **Rationale**: The probe says the consensus orders gates 3, 7, 8 but never shows gate 7 (true model identity from an agent-session reply). Verified: the card's top-level `model_class: sonnet` is orchestrator-written, so today identity is the request; the Agent tool schema exposes no model-id in a reply (UNVERIFIED for the reply body); `reflect-reviewer.md:6` defaults to Sonnet when no override is passed; the recorded workflow pre run has an unknown executor.
- **Integration point**: insert this table and text:

  > | Gate | Decision | Evidence or test | If it fails |
  > |---|---|---|---|
  > | 1 executor class resolved (flag, env, log; `SKILL.md:600-602`) | unchanged; `unknown` stays fail-open and is reported as `executor_class_resolved: false` | recorded run `return-contract.yaml:96-97` | no exclusion, loud WARN |
  > | 2 per-model class map | `classes` in the tier file; unmapped ids ineligible | Change 24.5 | template invalid, legacy rotation |
  > | 3 candidate filter | kernel `hard_exclude` on primary, fallback and fixed (Change 24) | tests in 24.8 | degrade per 24.6 |
  > | 4 `resolve_slot` pick | no `or candidates` re-admission under `hard` | `panel.py:405,408` fixed by 24.2 | `ExclusionExhausted` |
  > | 5 tier1b stand-in | none exists (`review-tiers.default.json:28`); anchor replacement template | `@reflect-pre-x2` | degrade |
  > | 6 dispatch via `launch` | whitelist `{sonnet, opus, haiku}`; null refused for pre; explicit `model` on every call | Change 7 | legacy rotation |
  > | 7 actual identity | **identity_source = `requested-pinned`** (the Agent tool pins `model`); the card header records `model_class` from the request, as today; each reviewer card must also carry a one-line self-report `reviewer_model_self_report` (advisory); a mismatch with the pin sets `identity_mismatch_suspected: true`, degrades diversity telemetry and never upgrades trust | **Spike S-ID, Stage 1 exit:** dispatch three probe reviewers (`model: haiku`, `sonnet`, `opus`) with a probe brief; check (a) the self-report matches the pin in 3 of 3 and (b) whether the tool result or transcript exposes a model id. If (b) is yes, switch `identity_source` to `observed` and assert it; if no, the pinned identity stays and is stated as an unverified assumption | UNVERIFIED until the spike runs |
  > | 8 N=2 floor on distinct classes | counts `complete` reviewers of **distinct** classes (Change 30) | test: two reviewers of one class do not reach T2 | T1 degrade (`SKILL.md:600`) |

  Safe default if S-ID is not run: pinned identity, `identity_source: requested-pinned` in telemetry, and no claim of verified independence in REPORT.md.
- **Risk**: High. Gate 7 is genuinely unknowable now; the design makes it an explicit spike with a stated default.

### Change 27: INV-023 (HIGH) a field mapping without a version change must be proven, not trusted
- **Source**: invariant-probe INV-023; A-009 V1 90%; X-003.
- **Target**: Base, Staged table Stage 1 and Stage 3 entry/exit (replace), new subsection `### Contract compatibility gate` in the Return-contract section (insert).
- **Rationale**: The wrapper's triggers 6-14 read fields (`contract.py:277-356`) and the interactive pre path assembles the same fields by prose, not code; `SKILL.md:923-940` (the §9.3 consumer map) does not list the wrapper or the headless builder at all. A-009 REJECT 3 of 3. Verified grep inventory at plan time (counts, not proof of completeness): `merge_method|adversarial_convergence_score|convergence_score` appears in `cli/reflect/contract.py` (3), `cli/reflect/ensemble.py` (22), `contracts/__init__.py` (1), `tests/cli/reflect/*` (fixtures: 31 files; `test_ensemble_unit.py` 23, `test_ensemble_stub_integration.py` 16, `test_verdict_mapping.py` 5), `task-builder` SKILL.md (4, EV-4 at `:2242`), reflect `SKILL.md` (9), `refs/ops-integration.md:239`; roadmap files match the same words for the roadmap pipeline's own merge (different contract). `.dev/eval-workspaces/sc-reflect/grader.py` has no match.
- **Integration point**: insert:

  > **Contract compatibility gate (PROPOSED, a hard stage-entry criterion for Stages 3, 4 and 5).**
  > 1. **Inventory.** Re-run a repository-wide grep for `merge_method`, `adversarial_convergence_score`, `convergence_score`, `contract_version`, `t2_model_class_diversity`, `t2_vendor_diversity`, `calibrator_diversity`, `reviewer_cards`, `citations_dropped` over `src/`, `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/` and the installed skill and command primitives. **Producers:** the interactive skill prose (`SKILL.md` §9.1 and Wave 5, plus `refs/report-template.md`, UNVERIFIED), the headless builder (`ensemble.py:787-832`). **Validators:** `contract.py` (`derive_verdict`, `contract.py:138`; `_degraded_reason`, `:263`). **Consumers:** the §9.3 map plus `task-builder` EV-4, the PromQL label list, the meta-eval aggregator, the sprint executor (UNVERIFIED code). The result is stored as `.dev/` evidence and attached to the stage's exit record.
  > 2. **Per-field source table** for the five fields whose producer changes in panel mode (the diversity trio, `calibrator_diversity`, `reviewer_cards`): each is computed by the same rule as the legacy path from the resolved classes; for the parity template in anthropic-only the expected values equal the legacy values (sonnet, haiku, opus: three distinct classes, vendor `single`, calibrator `degraded`).
  > 3. **Contract lint test** (PROPOSED `tests/cli/reflect/test_panel_contract_lint.py`; the reflect tests already live in that directory): feeds a panel-run contract and its output directory to a checker that asserts: `contract_version == "1.8.0"`; every top-level key is in the 1.8.0 stable field list or in the telemetry block; `merge_method` in `{adversarial, single-reviewer-fallback}`; `adversarial_convergence_score` is a float or null; `adversarial_unavailable`, `regression_present` and the other `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`) are real booleans; EV-1 holds on disk (`merged-verdict.yaml`, cards count); the five fields above equal the legacy values on the matched fixture.
  > 4. **Verdict replay.** Feed every recorded 1.8.0 pre contract and the Stage 2 shadow contracts through `derive_verdict` (`contract.py:138`) offline and diff the verdicts between legacy and shadow outputs; any new degraded reason is a stage-exit failure. (The wrapper is post-only in production; this replay is a test, not a runtime path.)
  > 5. **Bump rule check:** the lint fails if a panel run emits a stable key outside the list or a legal value outside EV-2; that is the machine form of "no change".
- **Risk**: Medium. It adds test work but removes the largest silent-break risk.

### Change 28: INV-024 (HIGH) first measurement with a power calculation and one margin per hypothesis
- **Source**: invariant-probe INV-024; Variant 2 three-arm design and sample-size section; Variant 1 shared-card idea (U-002) and seeded defects (U-003); Variant 3 hygiene (U-018); A-012; C-020 V2 98%.
- **Target**: Base, "First measurement" (replace in full) and Stage 0/2 exit criteria (cross-reference).
- **Rationale**: Base had three incompatible margins (10, 15 and 5 points across variants) and no power calculation; at n = 60 defects an unpaired recall CI is about +-0.12 (probe). Debate: C-020 V2 98%, A-001 98%, A-012 90%, X-011 90%.
- **Integration point**: replace with:

  > **Hypotheses and thresholds (one margin each).**
  > - **H-A (worth):** T2 recall beats T1 recall by at least **15 percentage points** on seeded defects (superiority). If not, record that the T2 spend does not buy recall on plans, and the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8). This is not an automatic veto of the migration, which is justified by maintenance as well.
  > - **H-B (non-inferiority):** panel-parity T2 recall is within **10 percentage points** of legacy T2 recall (one-sided 95% bound), and precision likewise. **The 5-point margin (V3) and the 15-point margin as an NI bound (V2) are dropped:** 5 points is not resolvable at feasible n (below), and 15 points is the H-A threshold, a different hypothesis.
  > - **H-C (cost):** median panel-T2 tokens <= 1.05 x legacy median and p95 <= 65k in the profile unit (Change 4). A saving is reported, not required.
  > - **Safety (fails regardless of savings):** a forbidden model or executor-class collision dispatched when the executor is known; a MALFORMED contract; an unsupported citation certified; any repository write by a reviewer; a T1 or `--depth quick` run that calls the panel.
  >
  > **Arms** (same plans, hidden arm identity for graders): A = T1 only (a `--tier 1` pin; flag semantics `SKILL.md:362`); B = legacy T2; C = panel-parity T2 (`--t2-engine panel`, debate kept); D = panel-lite (pilot subset only, Change 11) to price the Opus-moves ablation (U-012).
  >
  > **Ground truth.** Seeded defects (scripted, not derived from reviewer output; ordering, missing acceptance, spec-uncovered requirement, wrong file path, cross-task contradiction) plus a **union ledger** of natural findings from all arms scored by a blinded grader (A-012 QUALIFY; the ledger circularity caveat `LEDGER-RESULTS.md:49` applies).
  >
  > **Sample size (formula and numbers).** Paired by defect, with discordance d = share of defects found by exactly one arm. Standard error of the paired recall difference is about sqrt(d/n). One-sided 95% non-inferiority with 80% power at true difference 0 needs `n = d x (1.645 + 0.842)^2 / M^2 = 6.185 x d / M^2`. For M = 0.10: **n = 618 x d** defects (d = 0.10 -> 62; d = 0.20 -> 124; d = 0.30 -> 185). For H-A with M = 0.15: **n = 275 x d** (d = 0.35 -> 96). Multiply by 1.3 for clustering of defects within plans. At the pilot size of 60 defects the power is about 79% when d = 0.10 but only about 54% when d = 0.20 (SE 0.058, bound 0.095): the pilot therefore estimates d; it does not decide H-B.
  >
  > **Phasing.** Pilot: 12 plan+spec pairs x 5 seeded defects = 60 defects, arms A, B, C (arm D on 6 of them), plus 6 repeats of arm B to estimate the within-arm noise discordance d0 (if d0 is at least 0.8 x d between arms, the arms are indistinguishable from noise). Confirmatory: `n_plans = ceil(1.3 x max(618 x d_BC, 275 x d_AB) / 5)` from the pilot's observed d; the owner approves the spend before it runs. Cost units are the profile's: per plan arms A+B+C = 3k-8k + 35k-70k + 35k-70k = 73k-148k claude tokens; pilot (12 plans) 0.9M-1.8M; a confirmatory run of 33 plans (d = 0.20) 2.4M-4.9M; arm D adds 6 x 35k-70k. Retrieval tokens are reported separately and not summed.
  >
  > **Strata (required reporting).** Results are reported **split by `--depth` and by escalation path**, never only pooled: strata are (standard, escalated by the parsed-sparse pre-filter), (standard, escalated by rule 4, 5 or 6 without the pre-filter), (`--depth deep`), (`--tier 2` pin). Quota: at least 25% of plans whose source carries labelled requirement ids (non-sparse), because 34 of 38 recorded pre decisions were parsed-sparse (Change 39); if not obtainable, the report states it measured sparse-labelled plans only. Each stratum reports n, recall, precision, tokens and a CI; a pooled headline is shown only if a heterogeneity check across strata is not significant.
  >
  > **Stage 0a (zero dispatch, descriptive).** Convert the recorded cards (42 `reviewer-cards/` directories under `.dev/reflect/pre-*`, 33 with `adversarial/merged-verdict.yaml`) to findings-v2 (line refs to citations, Change 37), run `cluster_v2`, report cluster counts and agreement with the recorded merged verdict; report the share of findings that convert with an unambiguous `(path, line)` (the gate for A-003: at least 90%). Unseeded, not a pass/fail input.
  >
  > **Inconclusive is not a pass.** If the confirmatory interval crosses the margin, H-B is inconclusive and Stage 3 does not proceed; Stages 0-2 still ship.
- **Risk**: High. Cost and run-time are large; mitigated by the pilot-then-confirm rule and an explicit owner approval step.

### Change 29: INV-001, INV-002, INV-003 (state variables)
- **Source**: invariant-probe INV-001, INV-002, INV-003.
- **Target**: Base, Execution contract (Change 1), Q6, Pre adapter step 3 and 9.
- **Rationale**: INV-001 LOW: round_robin slots seed from `date.today().toordinal()` when no `sequence` is passed (`panel.py:471-476`), so a resume after midnight re-resolves; random slots hash `run_id` (`:455-459`) and are stable. INV-002 MEDIUM: the ledger records one `doc_sha256` (`ledger.py:278-279`, `merge_cmd.py:29-34`). INV-003 MEDIUM: `merge_cmd.py:113-116` writes the report before the ledger and `ledger.py:114-118` refuses a re-merge of round 1.
- **Integration point**: add to the Execution contract: "(1) `@reflect-*` templates use only `fixed` and `random` strategies; reflect-profile validation rejects `round_robin` unless `--sequence` is supplied and recorded in the manifest. (2) The plan and spec (and every grounding file) are covered by the existing `input_tree_sha256` and per-file sha256 list of `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), re-read and recomputed before Wave 5 and before promotion (`SKILL.md:227`); the manifest references that file by hash; no single-document hash is used and `doc_sha256` of the ledger is not relied on. (3) Reflect uses no ledger in Stages 0-4. If a ledger is ever used, each merge attempt writes to its own path `<out>/panel/attempt-<n>/ledger.json` and `merged.md`, and only the attempt named by the committed manifest is read."
- **Risk**: Low.

### Change 30: INV-006, INV-007, INV-009, INV-011 (guards and counts)
- **Source**: invariant-probe INV-006, 007, 009, 011; C-024 98%; Change 2.
- **Target**: Base, Q4 end, Execution contract, Risks (append), Staged table Stage 1/2 exit.
- **Rationale**: INV-006: unknown executor still gives a normal T2 (`SKILL.md:602` fail-open). INV-007: `panel.py:142` allows a template of 1..8 and `:405,408` can repeat models, and `ensemble.py:772` sets `tier_reached = 2` on `reviewer_count >= 2` without checking models differ. INV-009: reviewers must stay read-only whichever engine launches them; `reflect-reviewer.md:5-8` gives `tools` (Read, Grep, Glob and read-only search MCP tools, no Bash/Edit/Write), `permissionMode: plan`. INV-011: EV-1 compares the resolved `--reviewers` count (`SKILL.md:666`), the wrapper records a 2-of-3 as benign `reviewer-shortfall` (`ensemble.py:765-770`; halt set only auggie, env-aliases, evidence-validator, `contract.py:31-33`).
- **Integration point**: add: "**INV-006:** an unknown executor keeps the fail-open path and the T2 report states `executor_class_resolved: false`; the T2 label is allowed but REPORT.md must not claim anti-self-confirmation; the Stage 2 telemetry counts how many runs have it (O-6). **INV-007:** the N=2 floor is enforced on **distinct classes among `complete` reviewers**, in the adapter (strict distinctness, Change 24) and as a post-resolution assertion; the headless builder's `tier_reached` rule is a Stage 5 work item (add a distinct-model check at `ensemble.py:772`). **INV-009:** pre reviewers are only launched through the `reflect-reviewer` agent with an explicit `model` override; the tools allowlist is expected to survive the override (UNVERIFIED, part of spike S-ID: the probe reviewers are given a write attempt that must fail); a `launch: null` model is never dispatched (Change 7), so no swarm path exists for pre; the post swarm path keeps its existing isolation telemetry (`ensemble.py:825-831`). **INV-011:** the manifest records three counts, `reviewers_requested`, `reviewers_resolved`, `reviewers_complete`; EV-1 compares calibrated cards with `reviewers_resolved` (unchanged); a short run is MALFORMED under EV-1, remediated by the existing bounded re-dispatch, then the F2 fallback. The 2-of-3 mismatch between EV-1 and the wrapper pre-exists and is preserved; Stage 2 counts it."
- **Risk**: Medium (INV-009 rests on a spike).

### Change 31: INV-012 and INV-013 (citation counts and thresholds), plus C-019, C-022, A-010
- **Source**: invariant-probe INV-012, INV-013; Variant 1 verify-citations; A-010 REJECT 3 of 3; C-019 V1 75%; C-022 V1 80%.
- **Target**: Base, Pre adapter step 7-8, Post step 6, Return-contract null-score paragraph (append).
- **Rationale**: INV-012 MEDIUM: `SKILL.md:1210-1214` defines `citations_dropped` as the count among the re-read sample, gate 6a requires 0 and trigger 13 degrades on any value above 0 (`contract.py:347-352`); base's pre-check "adds drops" over **every** citation would change the field from a sample count to a mixed count and would tighten a gate, a semantic change (major, `SKILL.md:953`). INV-013 MEDIUM: `contract.py:317-326` degrades a T2 score below 0.80, while `SKILL.md:655` routes 0.75 and above to PASS; one recorded pre run scored 0.76 (Change 18), inside that gap.
- **Integration point**: replace the pre-check wording: "**The deterministic pre-check never drops a citation.** `superclaude review verify-citations` (PROPOSED, 0 model tokens) writes `panel/precheck.json` with, per citation, `missing-file`, `out-of-range`, or `quote-not-found` (advisory; a failed locate is not proof of an unfounded citation, A-010). Every flagged citation is added to the evidence-validator's re-read set even when the sampling policy (`SKILL.md:1204-1208`) would have skipped it. The validator alone decides drops, so `citations_dropped` keeps its sample-count meaning and gate 6a and trigger 13 are unchanged. Grounding is at least as strong as today because flagged citations are always re-read." **Headless gap (`ensemble.py:808-819`, `citations_dropped: 0`, `verification_ran: False`):** a Stage 5 work item runs the same pre-check headless and reports the validator-confirmed count; this moves the field toward its documented meaning, can newly trip trigger 13, and is announced at Stage 5 entry as a behavior change, not a contract version event. **Thresholds (INV-013):** no change to either. Pre runs route by `SKILL.md:655` (>=0.75 PASS, >=0.60 PARTIAL); the wrapper's 0.80 line applies to post contracts only; the first measurement reports both bands per run so the owner can see how many pre runs would degrade under 0.80.
- **Risk**: Medium.

### Change 32: INV-014, INV-018, INV-019, INV-021 (clustering semantics and score names)
- **Source**: invariant-probe INV-014, 018, 019, 021; U-006 (disputed cluster definition).
- **Target**: Base, "`panel_agreement_score` (PROPOSED)" paragraph (replace), Finding format footer, PROPOSED names.
- **Rationale**: `findings.py:382-407` chains transitively and `:377` links spans within 3 lines; `ledger.py:182-199` copies claim, anchor and category from the first member and ORs blocking before any validator drop; `contract.py:299` and `SKILL.md:663,1711` use two score names (A-015).
- **Integration point**: replace with: "**`cluster_agreement` (telemetry only; the name `panel_agreement_score` is deleted).** For each cluster c, `support(c)` = sum of the calibrated confidences (`calibration.per_finding[id].finding_confidence` joined from each member's card) of the distinct reviewers in c divided by the sum of calibrated confidences of all `complete` reviewers; `cluster_agreement` = mean support over blocking clusters, or 1.0 when none and at least 2 valid blocks. A cluster is **disputed** when support < 0.5, members disagree on `blocking`, or disagree on a non-null `deviation_class`. **Owner of a cluster's score:** the cluster carries the list of member calibrated scores, no scalar; its representative claim text and `blocking_any`/`blocking_all` come from the member with the highest calibrated confidence (ties: resolution order), not from the first reviewer (INV-018). **Order (INV-019):** clusters are computed on raw cards for telemetry; a second pass `clusters_kept` recomputes over findings the evidence validator kept, and only `clusters_kept` is used in measurements; the raw `overlap` label never routes anything. **Chaining (INV-014):** `chained` clusters are excluded from agreement counts and listed. **Names (INV-021):** stable field `adversarial_convergence_score`; prose name `convergence_score` (`SKILL.md:663,1483`); telemetry `cluster_agreement`. No other score name is introduced."
- **Risk**: Low.

### Change 33: INV-020 clustering plus a kept debate still needs a numeric score
- **Source**: invariant-probe INV-020; sc-adversarial `SKILL.md:404-411,438-460,944-952`.
- **Target**: Base, Pre adapter step 10 and Null-score rules (append).
- **Rationale**: Verified in `sc-adversarial-protocol/SKILL.md`: variants differing by under 10% skip the debate (`:407-410`, `:948-951`) and `convergence_score` is "null if debate not reached" (`:439,457`). A unanimous clean run can therefore return null today, which the wrapper degrades at T2 (`contract.py:299-300`) and promotion blocks (`SKILL.md:663`). Recorded pre contracts include 7 null scores (Change 18); their cause (skipped debate versus F2/F3) is UNVERIFIED.
- **Integration point**: add: "The debate input is unchanged (the calibrated cards, not the cluster table), so clustering cannot change whether sc-adversarial considers the variants 'substantially identical'. If the child returns a null score without `adversarial_unavailable`, the adapter keeps the real null (no synthetic 1.0), sets `debate_skipped_similar: true` in telemetry when the child's log says so, and the existing null routing applies (`SKILL.md:659-664`). Stage 0a classifies the 7 recorded nulls by cause; if skipped-similar is a frequent cause, a separate decision (not this design) is needed on whether a skipped debate should return a score."
- **Risk**: Low (no behavior change).

### Group D. Resolution of the 8 unresolved debate points

### Change 34: S-001, S-004, C-025 (style and naming: no-op decisions)
- **Source**: debate-transcript Scoring Matrix, all three UNRESOLVED 50.
- **Target**: Base, section order, Q-heading style, names.
- **Rationale**: S-001 (same order in all variants), S-004 (heading punctuation) and C-025 (names) carry no design content; V3: "names do not establish behavior".
- **Integration point**: keep V1's section order and `### Qn.` plus bold "Direct answer:" style, then add the owner-required sections where absent (Change 46). Names: keep `findings-v2` and the flag `--t2-engine legacy|shadow|panel`; replace `panel_agreement_score` with `cluster_agreement` (INV-021, Change 32). `V2`'s `reflect-finding/1`, `--panel-resolve/-merge/-post` and V3's `review-submission/2`, `--review-backend shared` are not adopted; their field content is (Changes 2, 11).
- **Risk**: Low.

### Change 35: C-007 (post debate input: pre-cluster map) decided as "not fed in the first shipment"
- **Source**: C-007 UNRESOLVED (V1 votes V1; V2, V3 vote NONE: all keep the post debate); A-008.
- **Target**: Base, Post adapter step 8 and Q3 post bullet (replace).
- **Rationale**: no evidence that a cluster map helps the debate; a non-card context file may not be accepted by `--compare` (UNVERIFIED); the base's step 8 itself says so. Feeding it changes the debate's inputs and the similarity check (Change 33).
- **Integration point**: replace with: "Post step 8: `Skill sc-adversarial-protocol --compare <calibrated cards>` exactly as `SKILL.md:645-651`. The K4 cluster map is written to `panel/clusters.json` for the Stage 5 post measurement; it is not an input to the debate until that measurement shows an effect (O-3). Replacing or narrowing the post debate needs its own post trial with seeded deviations and class accuracy (A-008)."
- **Risk**: Low.

### Change 36: A-002 (Haiku stand-ins transfer to the gateway) decided as an environment gate
- **Source**: A-002 UNRESOLVED (V1, V2 QUALIFY; V3 REJECT).
- **Target**: Base, Assumptions and Staged table Stage 3 entry.
- **Rationale**: no variant plans a gateway run; `review-tiers.default.json:20` says gateway dispatch is not defined; Change 7 already refuses `launch: null` for pre.
- **Integration point**: add to Stage 3 entry: "Stage 3 and later run only in an environment whose resolved models all have a non-null `launch` alias (today: anthropic-only). Haiku-stand-in runs certify mechanics and anthropic-only behavior, not gateway quality. A gateway default needs its own run of the first measurement (not planned; O-4)."
- **Risk**: Low.

### Change 37: A-003 (quote-anchor model) decided: `quote` optional when path and line range exist
- **Source**: A-003 UNRESOLVED (all three REJECT); diff A-003 CONTRADICTED by the recorded card.
- **Target**: Base, Finding format table rows `anchor`, `anchor2`, `citations` (replace) and Stage 0a.
- **Rationale**: the recorded card cites line references only (`evidence: [plan:57, source.md:62, src/...:451-462]`, stoprule `reviewer-1-card.yaml:12-30`). A `quote` of 12-200 characters per citation would be an unmet requirement for existing reviewer behavior.
- **Integration point**: rows become: `citations` list 1..8 of `{role, path, line_start, line_end, quote?}`, `quote` **optional** (12-200 chars copied from those lines when present); `anchor`/`anchor2` **required only if `citations` is absent**; a finding with neither is invalid. Conversion rule for recorded cards (deterministic, no quote): `plan:N` -> `(plan, <card plan path>, N, N)`; `source.md:N` or `spec:N` -> `(spec, <card spec path>, N, N)`; `path:A-B` -> `(source, path, A, B)`; unresolvable refs stay as `unresolved` citations and are counted. **Lossless conversion is not claimed**: Stage 0a reports the share converted unambiguously, with a gate of at least 90% before the parser change ships (the open part of A-003, O-7). `quote-not-found` is advisory only (Change 31).
- **Risk**: Medium. The 90% gate is a measured unknown.

### Change 38: Open items section (new) recording every residual tension
- **Source**: the 8 unresolved points and residual disputes (debate-transcript "Open disputes").
- **Target**: Base, new final section `## Open items` (insert before Assumptions).
- **Rationale**: the task requires either a position or an explicit open item for the 8 points; these items are the ones a position cannot settle today.
- **Integration point**: insert: **O-1** C-002 and C-014 (V3 holds its verdict/completion policy should be the base and prefers resolution-only first): resolved as V1 skeleton plus V3 policy; Stage 3 is the first stage that changes reviewers and it is effectively resolution-plus-format-only, so V3's concern is met without a separate stage; V3 dissent recorded. **O-2** C-005 (exact key versus primary-citation proximity): `cluster_v2` is telemetry only, so under-merging is cheap; revisit if clusters ever become authoritative. **O-3** C-007: post debate input (Change 35). **O-4** gateway dispatch for pre and post and gateway templates (X-010, A-002): undefined; refused. **O-5** path-aware ledger (`ledger/2`) if a ledger is ever used. **O-6** unknown executor is the default in the workflow path (Change 24.7): consider having `sc-workflow` Wave 4 pass `--executor-model` when known (a sc-workflow change, out of scope here). **O-7** A-003 conversion gate (Change 37). **O-8** the cheaper lever may be the rubric: 34 of 38 recorded pre decisions escalated because of the parsed-sparse pre-filter, not plan risk (Change 39); decide after H-A. **O-9** `_diversity.py:15` returns `insufficient` while `SKILL.md:790` allows only `full | degraded` (pre-existing vocabulary mismatch). **O-10** X-003: resolved in Change 14 as a text correction, no residual. **O-11** `--depth quick --tier 2` precedence and whether pins override the budget downgrade are not stated in the rows I read (UNVERIFIED).
- **Risk**: Low.

### Group E. Depth and tier call policy (coordinator addition)

### Change 39: New section "When the panel is called (depth x tier path)"
- **Source**: coordinator requirement; `SKILL.md:84-91,231-239,262-273,358-402,598`; `refs/cost-profile.yaml`; Variant 1 (`--depth` appears at base lines 14, 46, 123, 248, 353, 367, 381, 383), Variant 2 (lines 234, 338); recorded tier decisions.
- **Target**: Base, new top-level section after "Chosen architecture and reasons" and before "Answers to Q1-Q7" (insert); references from Q5, Q7, Staged migration and First measurement.
- **Rationale and reconciliation of the existing depth material.** (1) V1's "scoped debate only under `--depth deep`" (V1 lines 14, 46, 123, 248) and V2's "4+ reviewers on `--depth deep`" (V2 line 338) misuse reflect's `--depth`; reflect's `--depth` is Tier-1-only / Tier-1-then-rubric / force-Tier-2 (`SKILL.md:84`), and `--depth standard` at V2 line 234 and in `SKILL.md:648` belongs to `sc-adversarial`, a different flag. With the debate kept (Change 6), the first use disappears; the second is rejected (Change 9). (2) V1's "the kernel is never called when the rubric stops at T1 (`--tier 1`, `--depth quick`)" (V1 lines 367, 381) is correct and becomes rule D1. (3) V1 line 383 "gateway post with `--depth deep`" stays an open candidate (O-4). Evidence for the default-depth behavior: of 38 recorded pre tier decisions under `.dev/reflect/pre-*/artifacts/tier_decision.yaml`, 37 selected tier 2 and 1 selected tier 1 (a `--tier 1` user pin); 34 carry `coverage_degraded: parsed-sparse`; 21 are sc-workflow packages; 2 were forced by `--depth deep`; 0 stopped at T1 on the rubric. The cause is the table-wide pre-filter of `SKILL.md:400`: when `coverage_degraded` is set no STOP row may fire; sc-workflow plan sources carry no labelled requirement ids ("inferred 10 > parsed 0"), and rule 4 (`S_domains >= 3`) and rule 6 (`C < 0.85`) also fire in the recorded reasons.
- **Integration point**: insert this text in full:

  > ## When the panel is called (depth x tier path)
  >
  > The panel is a Tier-2 mechanism. It is called only after the **final** tier is 2. Order of decisions, unchanged from `SKILL.md`: (1) Wave 0 alias routing (`:231-239`: 1 alias -> T1 only; 2 aliases -> 2 reviewers; 3+ -> 3) and executor class (`:600-602`); (2) budget pre-flight (`:262-273`); (3) Waves 1-2: T1 card, coverage map, blind calibration of the T1 card, rubric (`:354-402`); (4) **only now** the T2 engine flag `--t2-engine` is read, at the start of Wave 3. The effective engine and the requested engine are both written to `tier_decision.yaml` and the manifest.
  >
  > **Rules.** D1: a `--depth quick`, `--tier 1`, `--no-escalate` or rubric-stopped T1 run **never** calls the panel and never reads `--t2-engine`. D2: the staged-migration flag is checked after the depth, pin, budget and rubric decisions, never before. D3: a run pinned to T2 (`--depth deep` or `--tier 2`) whose panel yields fewer than 2 distinct eligible classes does **not** silently run T1 or one reviewer: it emits the `SKILL.md:600` WARN and `executor_exclusion_degraded: true` (if exclusion caused it), `t2_floor_unmet` in `degraded_components` (a benign token, not in `contract.py:31-33`), forces `status: partial`, and REPORT.md opens with a banner naming the unmet floor; a rubric-driven escalation keeps the existing silent-safe T1 degrade of `SKILL.md:600` with the WARN. N=2 is the minimum in every case (`SKILL.md:610`; `reviewer-spec.md:102`). D4: unsupported cells (gateway, null `launch`, unmapped model) run the legacy rotation and record `panel_fallback_reason`. D5: `N_eff = min(--reviewers, alias count, 3)` (`SKILL.md:86`, clamp rule by depth is unstated in the rows I read and stays UNVERIFIED), anchor never dropped.
  >
  > | Depth / pin / modifier | Tier path | Panel called? | Template and reviewers | Stages that run | Expected cost (profile unit; planning) | Notes |
  > |---|---|---|---|---|---|---|
  > | `--depth quick` | T1 only (`:364`) | No | none | Waves 0-2 including the T1 card's blind calibration; no Wave 3-4 | 3k-8k claude + 2k-5k auggie (`cost-profile.yaml:36-39`) | `--t2-engine` ignored |
  > | `--tier 1`, `--no-escalate` | T1 (`:362,366`) | No | none | as above | as above | `--no-escalate` warns if C < 0.85 |
  > | `--depth standard` (default, `:323`), rubric stops | T1 | No | none | as above | as above | recorded: 0 of 38 |
  > | `--depth standard`, rubric escalates (rows 3-7, parsed-sparse pre-filter) | T1 work then T2 | Yes if engine is `panel` or `shadow` | `@reflect-pre`, 3 reviewers (2 if 2 aliases); `@reflect-enterprise` if `--strategy enterprise` | Wave 3 resolve + dispatch; per-card blind calibration; Wave 4 `sc-adversarial` debate on cards (not a deterministic merge); Wave 5 synthesis; evidence-validator; K4 clustering and pre-check as telemetry | planning 37k-56k output (legacy 42k-66k); profile band 35k-70k claude + 10k-25k auggie (`:46-51`) | the typical `/sc:workflow` plan: recorded 37 of 38 |
  > | `--depth deep` | forced T2 (`:365`) | Yes | same templates and count; no extra reviewers | as above plus the deep-only behavior of `--remediate` (task-builder route, `:89`) and optional tech-research in Wave 1B (`:637`) | as T2; deep extras unmeasured (no deep row in the profile) | D3 applies; 2 of 38 recorded |
  > | `--tier 2` | forced T2 (`:363`) | Yes | same | as T2 | as T2 | D3 applies |
  > | `--budget-remaining N`, N < 5 | STOP (`:267`) | No | none | none | none | |
  > | N = 5 | T1 forced (`:268`) | No | none | T1 | T1 | `budget_forced_tier_downgrade: true` |
  > | 6 <= N < 65 | T2 downgraded to T1 with WARN when the rubric asks for T2 (`:269`) | No | none | T1 | T1 | band 52 <= N < 65 has no row label in the table I read (UNVERIFIED how implemented); safe default: treat as downgrade |
  > | N >= 65 or unset | as the rubric directs (`:270-271`) | per rows above | per rows above | per rows above | the panel's p95 must stay <= 65k (`cost-profile.yaml:70`; 52 x 1.25) | panel adds no budget logic |
  > | executor class collides with the pool | N=2 floor then T1 degrade (`:600`) | only if >= 2 distinct eligible classes remain | `@reflect-pre-x2` etc. (Change 24) | as T2, or T1 | as T2, or T1 | D3 for pins |
  > | `--unattended` | unchanged | per rows above | per rows above | per rows above | unchanged | |
  > | headless `superclaude reflect` | post only (`ensemble.py:797`) | Stage 5 only | `@reflect-post` | existing ensemble, swarm lens | post planning unchanged | pre is never headless |
  >
  > **What a default-depth `/sc:workflow` run triggers.** Wave 4 of `sc-workflow` invokes `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with defaults for every other flag (`sc-workflow-protocol/SKILL.md:60`): depth standard, tier auto, no `--reviewers`, no `--budget-remaining` (budget check skipped), executor class unknown. So it runs T1 first, then the rubric, which in the recorded history escalated to T2 in 37 of 38 pre runs (34 by the parsed-sparse pre-filter because workflow sources carry no labelled requirement ids, others by rule 4, 5 or 6). With the engine at `panel`, every such run calls the panel; with the default `legacy` it never does. This is why the T2 cost, not the T1 cost, is the typical per-plan cost, and why the rubric's parsed-sparse behavior (O-8) deserves its own look after H-A.
- **Risk**: Medium. New section; the recorded-history figures are counts over `.dev/reflect/`, a single repository's sample.

### Group F. Consistency edits

### Change 40: Summary, candidates, and comparison matrix
- **Source**: Base Summary, "Candidate architectures", "Comparison".
- **Target**: Base, those sections (replace text, keep structure).
- **Rationale**: owner-required content: at least three candidates including "leave reflect as is", chosen architecture with reasons; consistency with Changes 6, 15, 19, 20.
- **Integration point**: Summary: "Chosen architecture: **C, the Layered Review Kernel with reflect adapters and a retained adversarial finalizer.** The kernel generalizes panel resolution, dispatch adapters, findings-v2 and deterministic clustering; reflect keeps briefs, blind calibration, the evidence gate, the rubric, the debate and the contract builder. Contract 1.8.0 is unchanged in Stages 0-4. Pre-execution first, behind `--t2-engine` (default `legacy`). Headline reason: one reviewer-identity layer and one finding format can serve two commands without weakening any reflect grounding mechanism; the first measurement decides whether the panel-fed T2 holds quality, and whether T2 beats T1 at all." Candidates (five, each with Changes/Keeps/Cost/Risk/Verdict): **A** leave as is (valid fallback, control arm); **B** full replacement by the spec-panel loop (rejected: drops calibration and the evidence gate, gain depends on a revise loop, breaks EV-2); **C** layered kernel with retained debate (chosen); **D** panel as dispatcher only (stage 1-3 of C, not a destination); **E'** layered kernel with deterministic pre merge and a major contract version (deferred; needs its own measurement and the consumer list of Change 15). Comparison matrix rows: one reviewer-identity layer; one finding format; blind calibration kept; evidence gate kept; debate (A always, B never, C always, D always, E' pre on disputes only); contract change (none, major, none, none, major 2.0.0); pre T2 output tokens (42k-66k legacy, about 290k+, 37k-56k, 42k-66k, 31k-46k); transfers the measured panel gain (no claim for all); maintenance surface.
- **Risk**: Medium.

### Change 41: Chosen-architecture reasons
- **Source**: Base "Chosen architecture and reasons" 1-5.
- **Target**: Base, those reasons (edit 3 and 5, append 6).
- **Rationale**: Changes 6, 18, 19.
- **Integration point**: reason 3 becomes "The debate is kept: EV-2 forbids a self-built merge, the debate's value is unmeasured and not shown idle (Change 18), and the post debate feeds promotion and rollback." Reason 5 stays (does not claim the PN1 gain). Add reason 6: "The first shipment changes no contract and no reviewer class: it is parity plus a format and dispatch layer, so the measurement can attribute any difference."
- **Risk**: Low.

### Change 42: Q1, Q2, Q3, Q5, Q6 answers synchronized
- **Source**: Base Q1-Q7.
- **Target**: Base, Q1 table rows, Q2, Q3, Q5, Q6 (edit).
- **Rationale**: consistency with Changes 5, 6, 10, 17, 24, 25.
- **Integration point**: Q1 table: "Blind calibration | `confidence-calibrator` per card (embedded block) | reflect"; "Merge | `/sc:adversarial --compare` | K4 clustering as telemetry; debate stays"; "Executor-class exclusion | kernel hard exclusion (Change 24), reflect supplies the class and the policy"; "Evidence gate | evidence-validator, with a deterministic flagging pre-check". Q2: findings-v2 is a superset of findings-v1; calibration is not carried in the block. Q3: Change 6. Q5: in-place answer (Change 12). Q6: Change 17.
- **Risk**: Low.

### Change 43: Staged migration table (replace)
- **Source**: Base "Staged migration" (V1 S-009 98%, C-014 75%); Variant 3 table; Variant 2 stage gating.
- **Target**: Base, the table (replace rows; keep columns What ships / Entry / Exit / Rollback).
- **Rationale**: C-014 V1 75% (shadow stage and byte-identity exit), V3 dissent (resolution-only first) answered in O-1; contract rows from Change 15; gates from Changes 24-28.
- **Integration point**: replace with:

  | Stage | What ships | Entry | Exit | Rollback |
  |---|---|---|---|---|
  | **0. Measure offline** | findings-v2 schema and parser, card converter, `cluster_v2`, Stage 0a replay on the recorded cards, consumer inventory and the lint test design | design accepted | 50-pair hand-labelled cluster check; conversion share >= 90% (Change 37); consumer grep result stored (Change 27); pilot designed and costed | delete the code; nothing consumes it |
  | **1. Kernel extensions, dormant** | K1 `classes`, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, Fable and tier0 rejection, `@reflect-pre`, `-x2`, `-enterprise`, `-lite`; `review cluster`; `verify-citations` | Stage 0 exit | Change 24.8 tests; spec-panel byte-identity (default and live7 templates, A-014); template validity; spike S-ID run (Change 26) | revert the commits; new parameters default off |
  | **2. Pre shadow** (`--t2-engine shadow`, default `legacy`, read only after the final tier, Change 39) | the panel resolution is written next to the legacy rotation and asserted identical (parity), findings-v2 block instruction in the brief, clusters, pre-check, manifest; legacy debate authoritative; contract 1.8.0 | Stage 1 exit; contract compatibility gate (Change 27) passed | 20 shadow runs: zero MALFORMED, EV-1 failure rate no higher than legacy, parity assertion holds, lint and verdict replay pass | flag default is `legacy`; delete `<out>/panel/` |
  | **3. Pre panel opt-in** (`--t2-engine panel`) | reviewers chosen by the template; debate on cards authoritative; contract 1.8.0 | **first measurement passed (H-B, H-C, safety)** and the environment gate (Change 36) | 30 opt-in workflow runs: `reflect_status` distribution no worse than shadow, zero MALFORMED, median tokens <= 1.05 x legacy | flag to `legacy` |
  | **4. Pre default** | sc-workflow's Wave 4 gets `panel` by default | Stage 3 exit plus owner sign-off | two release cycles with no rise in workflow `reflect_status: failed` | one-line default change |
  | **5. Post panel dispatch** | post adapter: K1/K2/K3, K4 telemetry, debate kept; headless `citations_dropped` made real (Change 31) with the `ensemble.py:772` distinct-model check | Stage 4 exit; a separate post measurement (seeded deviations, class accuracy) | wrapper verdict distribution on >= 20 paired post runs: no new `degraded` or `halted` reason from dispatch alone | flag to legacy rotation |
  | **6. Deferred candidate E'** | deterministic pre merge, `merge_method` value `panel`, contract 2.0.0 | a measurement that the debate adds nothing plus every consumer of Change 15 updated | not planned | not planned |
- **Risk**: Medium.

### Change 44: Adapter sketches (full replacement text)
- **Source**: Base "Adapter sketches" (V1 S-007 90%, C-010 75%); V3 pre steps 1, 7, 8; V2 step 8.
- **Target**: Base, "Adapter sketches" (replace pre steps 1-12 and post steps 1-10).
- **Rationale**: the base's merge step (`review merge --ledger ...`), the sidecars, the EV-1 wording and the dispute debate all go (Changes 5, 6, 16, 17); V3's input-drift recheck (C-010) and atomic publish (Change 1) are added.
- **Integration point**: replace with:

  > ### Pre-execution adapter (agent-session engine)
  > Inputs: `--spec`, `--tasklist`, `--executor-model` (optional), PROPOSED `--t2-engine legacy|shadow|panel` (default `legacy`).
  > 1. **Wave 0 and Waves 1-2 unchanged**: alias resolution, executor class (`SKILL.md:600-602`), budget pre-flight, grounding, coverage map (two-pass extraction), T1 card, blind calibration of the T1 card, rubric. If the final tier is 1 the adapter never runs and `--t2-engine` is not read (Change 39, D1, D2).
  > 2. **Engine decision.** `t2_engine_effective = requested` only if the final tier is 2 and the environment gate holds (Change 36); else `legacy` with `panel_fallback_reason`. Write both into `tier_decision.yaml`.
  > 3. **Freeze** (manifest `frozen`, Change 1): reference `artifacts/input-snapshot.yaml` by hash, pin template, tiers and brief-template hashes.
  > 4. **Resolve**: `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct` (`--template`, `--run-id`, `--kind`, `--env` exist, `panel_cmd.py:18-52`; the last two flags are PROPOSED). On `ExclusionExhausted` for the anchor, re-resolve with `@reflect-pre-x2`; assert the invariants of Change 24.6; write `<out>/panel/resolution.json`. Below the floor: Change 39 D3 or the `SKILL.md:600` degrade.
  > 5. **Briefs**: exactly three sections (`reviewer-spec.md:31-74`), persona by resolution order (analyzer, qa, refactorer), qa gets the spec body (`:55`). One added instruction line inside the T1-card section: "End your card with a `## Findings block` fenced `findings-v2` block, `lens: reflect-pre`, citations with roles `plan` and `spec`." Not a fourth section.
  > 6. **Dispatch**: parallel Agent calls to `reflect-reviewer` with the explicit `model` of Change 7, cards to `<out>/reviewer-cards/reviewer-<n>-card.md` (or `.yaml` as today). Attempts and completion states go to the manifest (Change 2).
  > 7. **Normalize**: parse each card's findings-v2 block (convert line refs, Change 37); an invalid block gets one bounded re-ask for the block only; the card body still reaches the debate.
  > 8. **Blind calibration** (unchanged mechanism, `SKILL.md:1192`): one `confidence-calibrator` per card, class chosen by `SKILL.md:1181-1186`, result embedded in the card.
  > 9. **K4 clustering and pre-check (telemetry and flagging only)**: `superclaude review cluster` writes `panel/clusters.json`; `superclaude review verify-citations` writes `panel/precheck.json`; neither drops anything and neither feeds the debate.
  > 10. **Debate (unchanged)**: `Skill sc-adversarial-protocol --compare <calibrated cards> --depth standard --focus correctness,coverage,deviation-classification --output <out>/adversarial/` (`SKILL.md:645-651`; under `--unattended`, `SKILL.md:653`). Remap `artifacts_dir` (`:657`). Record judge identity and collisions (Change 3). EV-1 unchanged (`:666`).
  > 11. **Wave 5 synthesis and evidence-validator (unchanged, mandatory, `SKILL.md:587`)** with the pre-check flags added to the re-read set (Change 31); recompute `input_tree_sha256` before synthesis (`:227`).
  > 12. **Publish** atomically (Change 1) and emit contract 1.8.0 by the legacy rules; lint (Change 27) in tests.
  >
  > **Shadow mode** (`--t2-engine shadow`): steps 4-9 run with the legacy rotation expressed as the resolution (identical reviewers); the assertion "panel resolution == legacy rotation" is recorded; the debate result is authoritative; panel artifacts and telemetry are written for the measurement.
  >
  > ### Post-execution adapter (Stage 5; both engines)
  > Inputs: `--spec`, `--tasklist`, `--task-log`, `--diff`, `--executor-model`, `--t2-engine`.
  > 1. Waves 0-2 unchanged, including the §6.1 verification run by the orchestrator (reviewers never execute, `reflect-reviewer.md` Safety Constraint).
  > 2. Resolve with `@reflect-post` (same slots; `@reflect-post-x2` for anchor replacement) and the executor class hard-excluded and strict distinctness; this matters most here (self-confirmation, `SKILL.md:600`).
  > 3. Briefs unchanged; each grounding hunk is an H3 `path:start-end` (`reviewer-spec.md:45`); `lens: reflect-post`, `deviation_class` required; no-spec gaps use `channel: advisory`.
  > 4. Dispatch: agent-session as pre; headless `superclaude reflect` -> ensemble -> swarm `reflect-review` lens, unchanged in Stage 5 except that it may read the K1 resolution through a PROPOSED `--panel-resolution` input with `T2Model0N` as the fallback.
  > 5. Blind calibration per card (embedded); pre-check flags; evidence-validator (unchanged).
  > 6. K4 clustering to `panel/clusters.json` (telemetry).
  > 7. **Debate (kept)**: `--compare <calibrated cards>` as `SKILL.md:645-651`; cluster map not an input (Change 35). Writes `adversarial/merged-verdict.yaml`.
  > 8. Contract: `merge_method: adversarial`, the child's score; 1.8.0 semantics unchanged. Promotion, remediation and the `reflect_post` write-back are unchanged.
- **Risk**: High. This is the executable core; every step names its source change so a reviewer can trace it.

### Change 45: PROPOSED-names inventory and header block
- **Source**: Base "PROPOSED names introduced" (S-012 V1 98%).
- **Target**: Base, the last inventory (replace).
- **Rationale**: remove names that no longer exist (`panel_agreement_score`, `merge_method: panel` as a shipped value, `merge_engine`, `panel_ledger_path`, `dispute_debate_*`, `calibration.json`, `validation.json`, `--calibration`, `--validation`, role-qualified `--doc`); add the new ones.
- **Integration point**: inventory: templates `review-panel.reflect-pre.json`, `reflect-pre-x2`, `reflect-post`, `reflect-post-x2`, `reflect-enterprise`, `reflect-lite`; K1 `classes` in the tier file, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, `skipped_slots`, `excluded` (additive resolution keys), CLI `--hard-exclude-class` and `--strict-distinct`; K3 `findings-v2` and its fields (`citations`, `deviation_class`, `coverage_rows`, `self_confidence`, `lens`, `channel`, `reflect_category`); K4 `superclaude review cluster`, `cluster_v2`, `cluster_agreement`; `superclaude review verify-citations`; manifest `panel/manifest.json`, `panel/resolution.json`, `panel/clusters.json`, `panel/precheck.json`; reflect flag `--t2-engine legacy|shadow|panel`; telemetry `t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `t2_floor_unmet`; swarm lens input `--panel-resolution` (Stage 5); test `test_panel_contract_lint.py`. Contract: none.
- **Risk**: Low.

### Change 46: Owner-required-content map (appendix) and final cross-reference pass
- **Source**: the owner's list of required content; Plan sections.
- **Target**: Base, new last section `## Required-content map` (insert) plus a consistency pass.
- **Rationale**: the owner required these items in the final design; a map makes omissions detectable.
- **Integration point**: insert a table with these rows and targets: candidates >= 3 including leave-as-is (Candidates); chosen architecture and reasons (Chosen architecture); Q1-Q7 (Answers); finding-format section (Finding format); pre and post adapter sketches (Adapter sketches); staged migration with pre behind a flag first (Staged migration: Stage 2 `shadow`, Stage 3 `panel`, default `legacy`); mapping onto contract 1.8.0 including `merge_method`, convergence score, null-score rules, gate condition 9, `reflect_post` frontmatter and every consumer (Return-contract section, Change 15; versioned-change consumer list for the deferred path); cost model (Cost model); main risks (Risks); first measurement (First measurement); depth x tier (When the panel is called). Consistency pass for the executor: (a) grep the merged file for `panel_agreement_score`, `merge_method: panel`, `2.0.0`, `1.9.0`, `calibration.json`, `validation.json`, `--ledger panel`, `review-doc.md`, `dispute_debate`, `--depth deep` and `hard_exclude raises`; each remaining hit must be inside the deferred-candidate text or removed; (b) every `path:line` cite is a line listed in this plan or carries UNVERIFIED; (c) no `src/superclaude/` path appears as an instruction to an installed primitive (the plan's own `cli/...` cites are descriptive citations of package code, allowed by CLAUDE.md); (d) Fable and Tier 0 never appear except in the rejection rules; (e) every Opus mention points to the Opus-use list.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base (or the merged position) |
|---|---|---|
| C-002 / C-003 / C-010 (V3 votes V3) | V3 as the base: policy first, interfaces imported | V1 is the only variant with a checkable template, a command-level pre flow and a stage table with rollback (C-009 90%, X-001 90%, C-010 75%, S-009 98%); V3's policy is incorporated (Changes 1-3, 15, 30). Recorded as O-1. |
| C-014 (V3 for V2) | resolution-only as a separate first stage | V1's shadow stage changes no reviewer and has the byte-identity exit (C-014 75%, A-014 98%); Stage 3 is effectively resolution plus format, so V3's minimal-mutation concern is met. |
| C-005 (V3) | exact-identity key with related groups only | `cluster_v2` is telemetry only, so the under-merge cost the key avoids is not at stake; the primary-citation, path-aware matcher with a chain guard (Change 25) is kept (C-005 V1 75%, 2 of 3). Recorded as O-2. |
| C-004 (V2, V3) | `reflect-finding/1` reusing the `findings-v1` info string; `review-submission/2` YAML envelope | V1's superset `findings-v2` keeps one parser for spec-panel (C-004 V1 90%, 3 of 3); V3's completion state and `channel` are added (Change 2); V2's category map is added (Change 11). |
| C-006 / C-016 / C-015 in V1's form | debate removed in pre, `merge_method: panel`, 2.0.0 | EV-2 and EV-1 forbid it (X-005 98%); the wrapper blocks major 2 (Change 14); debate value unmeasured and not idle (Change 18). Moved to deferred candidate E'. |
| X-007 (V2) | one concatenated `review-doc.md` | identity loss, single `--doc` (`merge_cmd.py:29-34`); X-007 V3 75%; V2 conceded in R1. Per-source layout only (Change 11). |
| C-019 (V1) | pre-check that drops missing-file or out-of-range citations | it changes `citations_dropped` semantics and tightens a gate (INV-012; `SKILL.md:953`); replaced by "flag and force into the validator" (Change 31); A-010 REJECT 3 of 3. |
| C-018 (V1 vs V3) | cheaper non-Opus calibrator | `SKILL.md:1181` already selects the highest-capability disjoint class; V3 conceded it is a policy change (C-018 V1 90%, X-016 90%); unchanged and listed (Change 19). |
| C-022 (V1 vs V3) | headless pre-check fully closes `citations_dropped: 0` | rule without a mechanism is not enough (V1, V2 R2); Stage 5 work item with an announced behavior change instead of a claim (Change 31). |
| C-013 (V2 as a gate for 4+) | 15-point gate as the policy for larger panels | V3 dissent (no unsupported automatic expansion); the hard cap of 3 stands and the gate is a PROPOSED precondition to raise it (Change 9). |
| V2 stage 5 "additive 1.9.0" `panel-deterministic` | new `merge_method` value labelled additive | X-004 98%: a widened legal set is major (`SKILL.md:953`); also contradicts V2's own EV-2 edit; moved to E'. |
| V3 post adapter "later", V2 swarm path for `launch` null | swarm for gateway models in pre | the swarm lens is post-only (`ensemble.py:797`); gateway dispatch is undefined (`review-tiers.default.json:20`); X-010 (Change 7). |
| V1 sidecars `calibration.json`, `validation.json` | findings-only reduction | A-004 REJECT 3 of 3; X-009 98% (Change 5). |
| V1 `panel_agreement_score` as a routing input | numeric substitute for convergence | V3 C-016 98%: no substitute score; INV-021 (Change 32). |
| V1 first measurement (K4 vs debate on shared cards, 20 pairs, margin 0.10) | as the first measurement | the merged design keeps the debate, so the K4-vs-debate question is not the gate; shared-card is kept only for the Stage 0a replay (Change 28). V1's margin 0.10 and seeded-defect idea are kept. |
| V3 first measurement (24 cases x 2 repeats x 2 arms, margin 5 points) | as the first measurement | no T1 arm (A-001 98%); 5 points is unresolvable at that n (Change 28); V3's hygiene (blinding, stop rule, pilot label) kept. |
| V2 first measurement margin 15 points as NI bound | single bound | separated into H-A (15, superiority) and H-B (10, NI) (Change 28). |
| V3 "Opus only if no lower disjoint choice" | stricter Opus rule | would change existing policy (`SKILL.md:1181`, `:607`); Opus list keeps today's uses (Change 19). |
| V1's `@reflect-pre` (sonnet, haiku, haiku) as default | lite template as the first shipment | changes `t2_model_class_diversity` from three classes to two (`SKILL.md:233-239`); kept as the measured arm D (Changes 19, 23, 28). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | resume and publish rules unclear; stage 2 manifest unusable | remove the block and `panel/manifest.json`; legacy never reads it |
| 2, 3, 5, 8, 10-13, 16-18, 20, 22, 29, 32-38, 41, 42, 45, 46 | Low | wording or telemetry only | revert the text |
| 4 | Medium | cost numbers read as results | restore units text; keep hypothesis labels |
| 6 | Medium | headline reversal leaves stale sentences | the Change 46 grep list |
| 7 | Medium | pre limited to anthropic-only | legacy rotation (default) |
| 9 | Low | cap too tight | raise through the 15-point precondition |
| 14 | Low | text correction | none needed |
| 15 | High | contract plan wrong breaks a consumer | the lint test plus deferred list; contract unchanged by default |
| 19 | Low | Opus list wrong | revert to the base statement |
| 21 | Low | probabilities are estimates | revise after Stage 2 telemetry |
| 23 | Medium | template mistakes fail validation | Stage 1 validator test; legacy rotation |
| 24 | High | kernel change affects spec-panel | default-off parameters; byte-identity test |
| 25 | Medium | clusters wrong | telemetry only; Stage 0 hand labels |
| 26 | High | identity read-back unknowable | pinned default; spike S-ID; no verified-independence claim |
| 27 | Medium | gate adds work | none; removing it removes the protection |
| 28 | High | cost and run time of the measurement | pilot first; owner approval before the confirmatory run |
| 30 | Medium | INV-009 rests on a spike | read-only probe; legacy default |
| 31 | Medium | pre-check semantics misread | flagging only; validator decides |
| 39 | Medium | counts come from one repository's `.dev/reflect` history | restate with fresh data after Stage 2 |
| 40, 43, 44 | Medium / Medium / High | stale sections or unexecutable steps | Change 46 consistency pass; trace each step to its change |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-11T19:19:46Z
