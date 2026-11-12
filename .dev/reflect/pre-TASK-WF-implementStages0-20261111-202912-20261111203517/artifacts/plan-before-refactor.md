---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementStages0-20261111-202912
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Reflect Tier 2 review panel: Stages 0 to 2 (offline measurement, dormant kernel, pre shadow mode)

Source: ./source.md
Goal: The shared review kernel gains findings-v2, path-aware clustering, hard executor exclusion, reflect templates and citation pre-check, all dormant or telemetry-only; `/sc:reflect` pre-execution accepts `--t2-engine legacy|shadow` (default `legacy`) and, in shadow, writes panel artifacts next to an unchanged legacy run, with the tooling to judge the Stage 2 exit.

## Constraints

- Requirement text lives in `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (sha256 recorded in `./source.md`). Section names below refer to that file. Items it marks PROPOSED are new names to create; items it marks UNVERIFIED must be checked in code before relying on them.
- Return contract stays `1.8.0` with no new stable field and no new legal value (`merge_method` stays `adversarial` or `single-reviewer-fallback`). Panel data lives only in `<out>/panel/*` and the non-stable telemetry block.
- The `/sc:adversarial` debate stays authoritative in pre-execution. K4 clustering, the citation pre-check and the findings block never drop a citation, never feed the debate and never route anything.
- Default behavior of every existing command is unchanged: with no new flag, `superclaude review panel resolve`, `review merge`, `review ledger` and the spec-panel loop produce byte-identical output.
- Plan decision: in Stage 2 the flag accepts only `legacy` and `shadow`; the value `panel` is rejected with a plain message saying it ships in Stage 3. The post-execution path, the swarm lens, `--panel-resolution` and the headless `citations_dropped` change are Stage 5 and are not touched.
- Plan decision: the prose coordinator of the reflect skill cannot import Python, so the manifest gets a minimal `superclaude review manifest` CLI (init, advance, validate) instead of hand-written JSON.
- Edit installed primitives only under `src/superclaude/` and run `make sync-dev` afterwards. Never edit or add files under `.claude/` by hand. Installed primitives reference other primitives by installed path or the `superclaude` CLI, never by a `src/superclaude/...` path.
- All Python runs through `uv run`. Never use Opus, Fable or Tier 0 in any new template; Fable and Tier 0 are rejected by validation.
- Human-supplied inputs are not fabricated: the 50-pair cluster labels (Task 5) and the 20 real shadow runs (Task 20) are produced by the owner and by normal use after merge. The tasks deliver the sheets, scorers and aggregators that judge them.
- Task-owned evidence goes under `./artifacts/` in this package.

## Phase 1: Stage 0, offline measurement (findings-v2, converter, cluster_v2, replay)

## Task 1: Add the findings-v2 schema and parser

Create `src/superclaude/cli/review/findings_v2.py` and `tests/review/test_review_findings_v2.py`. Read `src/superclaude/cli/review/findings.py` (v1 parser `parse_block`, `_check_finding`, id and severity rules at lines 90-196) and follow its container rules. Implement the "Finding format" table of the source: a JSON-lines fenced block with info string `findings-v2` under `## Findings block`; fields `id`, `severity`, `blocking`, `category` (v1 six-value enum unchanged), `reflect_category`, `claim`, `refs`, `anchor`/`anchor2` (required only when `citations` is absent), `citations` (1..8 of `{role, path, line_start, line_end, quote?}` with role in plan, spec, source, test, diff, artifact), `deviation_class` (required when `lens` is `reflect-post`), `coverage_rows`, `self_confidence` (0-1), `lens` (spec, reflect-pre, reflect-post), `channel` (defect, grounding-gap, advisory; default defect). Apply the category and severity mapping paragraph (ordering to other, acceptance to unpassable-check, coverage to missing-requirement, contradiction to contradiction, risk to safety or other, deviation to other with deviation_class). Reject a line that sets `calibrated_confidence`. Expose completion states `complete`, `truncated`, `invalid`, `failed`, `timed_out`, where a valid empty array counts as `complete` only when the card also carries coverage observations for every assigned row.

Acceptance criteria:
- Every valid v1 block in the existing tests also parses as v2 with the same findings.
- Tests cover: finding with neither `anchor` nor `citations` is invalid; MINOR cannot block; duplicate ids rejected; `calibrated_confidence` rejected; `deviation_class` required for `reflect-post`; empty valid array without coverage observations is `invalid`, with them is `complete`; `quote` optional and, when present, 12-200 chars.
- `uv run pytest tests/review -q` passes, including the untouched v1 tests.

## Task 2: Add the recorded-card converter

Depends on: Task 1

Create `src/superclaude/cli/review/card_convert.py` and `tests/review/test_review_card_convert.py`. Convert a recorded reflect reviewer card (YAML findings with `severity: blocking|minor`, categories ordering, acceptance, deviation, coverage, risk, and `evidence` line refs, as in "What a recorded card looks like") to findings-v2 using the deterministic, quote-free rule: `plan:N` becomes a `plan` citation on the card's plan path, lines N-N; `source.md:N` or `spec:N` becomes a `spec` citation on the card's spec path; `path:A-B` becomes a `source` citation; unresolvable refs become `unresolved` citations and are counted. Return the converted findings plus per-card counts (converted unambiguously, unresolved). Use real cards from `.dev/reflect/pre-*/reviewer-cards/` (copy two or three small ones to `tests/review/fixtures/reflect_cards/`).

Acceptance criteria:
- A fixture card with refs `plan:57`, `source.md:62`, `src/x.py:451-462` converts to three citations with the roles and paths above and no quote.
- A ref that cannot be resolved is kept as an `unresolved` citation and counted, never dropped.
- Tests assert the unambiguous-conversion share is reported per card and in total.

## Task 3: Implement cluster_v2 (path-aware, with the chained guard)

Depends on: Task 1

Create `src/superclaude/cli/review/cluster.py` and `tests/review/test_review_cluster.py`. Implement the pure function `cluster_v2(findings_v2_blocks, snapshot_file_list) -> clusters` exactly as "Multi-file identity (K4 cluster_v2)": citation tuple `(role, path, line_start, line_end)` verified against the snapshot file list (a path not in the list is `unresolved` and never joins a cluster by span); primary citation rule; `same_defect_v2` (deviation classes compatible, `refs_norm` sets intersect or both empty using the normalization of `findings.py:321-337`, and some citation of each on the same path with spans within 3 lines; equal `sha256("v2|"+role+"|"+path+"|"+section+"|"+refs+"|"+class)` fingerprints with non-empty refs also match); union-find components with `chained: true` for any cluster holding two members that do not match pairwise. Implement `cluster_agreement` and the `disputed` flag per "`cluster_agreement` and clustering semantics": support from calibrated confidences joined from `calibration.per_finding[id].finding_confidence`, representative claim from the highest-confidence member (ties by resolution order), `chained` clusters excluded from agreement counts and listed, and a second pass `clusters_kept` over findings the evidence validator kept. Do not import or alter `findings.cluster`.

Acceptance criteria:
- Tests (positive and negative): two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines with equal refs cluster; a chain A-B-C with A and C unequal is `chained`; an unresolved path never clusters by span.
- A test proves `review merge` output on v1 reports is byte-identical with and without importing the new module.
- `cluster_agreement` is 1.0 when there are no blocking clusters and at least 2 valid blocks; the field is named `cluster_agreement` everywhere and `panel_agreement_score` appears nowhere.

## Task 4: Build the Stage 0a replay on the recorded cards

Depends on: Task 2, Task 3

Create `scripts/reflect_stage0a_replay.py` (run with `uv run python scripts/reflect_stage0a_replay.py`). It reads the 42 recorded `reviewer-cards/` directories under `.dev/reflect/pre-*` (33 have `adversarial/merged-verdict.yaml`), converts them with `card_convert`, runs `cluster_v2`, and writes `./artifacts/stage0a-report.md` containing: cluster counts, agreement with the recorded merged verdict, the share of findings that convert with an unambiguous `(path, line)` against the 90% gate (O-7), and a classification of the 7 recorded null convergence scores by cause (skipped-similar debate, single-reviewer-fallback, illegal merge_method value, other), read from each run's `adversarial/` log and `return-contract.yaml`. It dispatches no model.

Acceptance criteria:
- `./artifacts/stage0a-report.md` exists with the conversion share stated as a number and a PASS or FAIL against 90%.
- The report lists each of the 7 null-score runs with its cause, or states for which the cause could not be determined and why.
- If the share is below 90%, the report says the findings-v2 parser change must not ship and the plan stops at this task for owner review.

## Task 5: Produce the 50-pair cluster check sheet and its scorer

Depends on: Task 3

Create `scripts/reflect_cluster_pairs.py` and `tests/review/test_reflect_cluster_pairs.py`. The script samples 50 finding pairs from the converted recorded cards (25 that `cluster_v2` merges, 25 it keeps apart, drawn with a fixed seed, mixing same-file and cross-file pairs), writes `./artifacts/cluster-pairs-50.csv` with blank `human_same_defect` column, and has a `score` mode that reads the filled sheet and reports precision, recall and the confusion counts of `cluster_v2` against the labels.

Acceptance criteria:
- `./artifacts/cluster-pairs-50.csv` exists with exactly 50 rows, each carrying both claims, both citations and the `cluster_v2` verdict; the label column is empty for the owner.
- A unit test fills a synthetic sheet and checks the score output; scoring an unfilled sheet fails with a message naming the missing labels.

## Task 6: Add the consumer inventory script and store the first result

Create `scripts/reflect_consumer_inventory.py` and `./artifacts/consumer-inventory.md`. The script greps `merge_method`, `adversarial_convergence_score`, `convergence_score`, `contract_version`, `t2_model_class_diversity`, `t2_vendor_diversity`, `calibrator_diversity`, `reviewer_cards`, `citations_dropped` over `src/`, `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/` and the installed skill and command primitives under `src/superclaude/{skills,commands}`, classifies each hit as producer, validator or consumer (producers: reflect `SKILL.md` section 9.1 and Wave 5, `refs/report-template.md`, `cli/reflect/ensemble.py`; validators: `cli/reflect/contract.py`; consumers: the section 9.3 map, `task-builder` EV-4, `refs/ops-integration.md`, the meta-eval aggregator, the sprint executor), and writes a markdown table with counts per file. It must be rerunnable with `--out <file>`.

Acceptance criteria:
- `./artifacts/consumer-inventory.md` lists every hit file with its role and counts, and flags files that match the words for an unrelated pipeline (roadmap) as not in scope.
- The report states that no `contract_version == "1.8.0"` equality exists in `src/` and that `.dev/eval-workspaces/sc-reflect/grader.py` has no match, or states the contradicting hit with its path.
- Running the script twice on an unchanged tree yields identical output.

## Task 7: Design and cost the first-measurement pilot

Depends on: Task 4

Write `./artifacts/pilot-design.md` from "First measurement": hypotheses H-A, H-B, H-C and the safety list; arms A (T1 pin), B (legacy T2), C (panel-parity T2), D (lite, 6 plans); ground truth (scripted seeded defects of the five kinds plus the union ledger with a blinded grader); the pilot of 12 plan+spec pairs x 5 seeded defects with 6 repeats of arm B to estimate d0; the sample-size formulas (n = 618 x d for margin 0.10, n = 275 x d for margin 0.15, times 1.3) with the worked numbers; the strata and the 25% non-sparse quota; the cost per plan and for the pilot in the profile's claude-token unit (arms A+B+C = 73k-148k per plan, pilot 0.9M-1.8M), with retrieval tokens listed separately; the stop rule; the statement that the pilot estimates d and does not decide H-B; and the "inconclusive is not a pass" rule. Use the Stage 0a numbers from Task 4 where they replace estimates.

Acceptance criteria:
- The document states every threshold once and the arithmetic reproduces the cost figures above.
- It names the owner approval needed before the confirmatory run and marks the pilot as a pilot.
- Stage 0 exit checklist at the end lists the five exit items (50-pair check, conversion share, consumer inventory stored, pilot designed and costed) with the artifact that answers each.

## Phase 2: Stage 1a, kernel resolution extensions (dormant)

## Task 8: Add hard exclusion and strict distinctness to panel resolution

Depends on: Task 7

Edit `src/superclaude/cli/review/panel.py` per "K1 hard exclusion contract" items 1-4. Add keyword-only `hard_exclude: Sequence[str] = ()` and `strict_distinct: bool = False` to `resolve_slot` (line 380) and `resolve` (line 427); filter the candidate list before the strategy runs for every strategy including `fixed`, derive fallbacks from the filtered list, and skip the silent `or candidates` re-admission when `hard` is non-empty. When the filtered list is empty try stand-ins filtered the same way, else raise new `ExclusionExhausted(tier)` (subclass of `NoModelAvailable`). In `resolve`, a non-fixed slot that raises `ExclusionExhausted` is skipped and recorded; the fixed anchor raising is fatal. Add additive keys `skipped_slots: [{slot_id, reason}]` and `excluded: {models, classes}` to the `review-panel-resolution/1` JSON only when exclusion arguments are used. Do not add template keys (`_SLOT_KEYS` stays). Create `tests/review/test_review_panel_exclusion.py`.

Acceptance criteria:
- With `hard_exclude == ()` and `strict_distinct == False` the resolution output and hashes are byte-identical to today for the packaged default and live7 templates (asserted by a test that compares against a stored golden).
- Tests: excluded model is the fixed anchor; random and round_robin pools that empty do not re-admit the excluded model; a stand-in is used only after filtering; `ExclusionExhausted` is raised when nothing remains.
- `uv run pytest tests/review -q` passes.

## Task 9: Add the class map, Fable and Tier 0 rejection and the reviewer cap

Depends on: Task 8

Edit `src/superclaude/cli/review/data/review-tiers.default.json` to add a `classes` object mapping every model id to a class string (`claude-opus-5-5` to opus, `claude-sonnet-5-5` to sonnet, `claude-haiku-5-5` to haiku, and vendor families gpt, glm, grok, qwen, muse for the gateway models) and let `validate_tiers` in `panel.py` accept it. Add a reflect-profile validator in `panel.py` applied to every template whose name starts with `reflect-` and to every resolution made from one: reject a model id with no `classes` entry; reject any resolved id matching `claude-fable-*`; reject a slot on `tier0` or whose alias list holds a Tier 0 model; reject a `launch` value outside `{sonnet, opus, haiku}`; reject more than 3 reviewers; reject `round_robin` slots unless a recorded `--sequence` is supplied. Generic panels keep their 1..8 range.

Acceptance criteria:
- Tests in `tests/review/test_review_panel_exclusion.py` (or a new `test_review_panel_reflect_profile.py`) cover each rejection above, and show a generic non-reflect panel with 4 reviewers is still valid.
- An unmapped model id makes a `reflect-*` template invalid and leaves non-reflect templates valid.
- The existing tier-file tests still pass without edits.

## Task 10: Add the CLI flags to `review panel resolve`

Depends on: Task 8, Task 9

Edit `src/superclaude/cli/review/panel_cmd.py` (`resolve_cmd`, options at lines 18-52) to add `--hard-exclude-class <class>` (repeatable; expands through `classes`, compares case-insensitively with the executor class) and `--strict-distinct`. Wire them to `hard_exclude` and `strict_distinct`, write `skipped_slots` and `excluded` into the JSON, and exit non-zero with the exception name on `ExclusionExhausted`. Extend `tests/review/test_review_cli.py`.

Acceptance criteria:
- `superclaude review panel resolve --template @reflect-pre --run-id r1 --kind first --env anthropic-only --hard-exclude-class sonnet --strict-distinct` exits non-zero naming `ExclusionExhausted` for tier1b once Task 11 lands; without the new flags the existing CLI tests pass unchanged.
- An unknown class name is a usage error that lists the known classes.

## Task 11: Ship the reflect panel templates

Depends on: Task 10

Create in `src/superclaude/cli/review/data/`: `review-panel.reflect-pre.json` (the JSON in "Template set": slots t1b fixed on tier1b, t4 random on tier4, t1a random on tier1a, distinct_across_slots true, apply_to first), `review-panel.reflect-pre-x2.json` (fixed t4 anchor plus random t1a), `review-panel.reflect-enterprise.json` (same slots as reflect-pre), `review-panel.reflect-lite.json` (t1b, t4, t2), `review-panel.reflect-post.json` and `review-panel.reflect-post-x2.json` (mirror pre). Confirm tier ids exist in `review-tiers.default.json` and that each file passes `validate_panel` and the Task 9 reflect profile. Create `tests/review/test_review_reflect_templates.py` covering the Task 8 scenarios from "K1 hard exclusion contract" item 8.

Acceptance criteria:
- `@reflect-pre` resolves in anthropic-only to sonnet, haiku, opus with three distinct classes; `@reflect-pre-x2` resolves to haiku and opus.
- Executor sonnet raises `ExclusionExhausted` for tier1b and the adapter-style fallback to `@reflect-pre-x2` yields 2 reviewers; executor haiku skips the t4 slot; executor opus with strict distinctness yields sonnet and haiku with no duplicate.
- No template names Fable, tier0 or a gateway model; `uv run pytest tests/review -q` passes.

## Phase 3: Stage 1b, clustering and citation tooling, identity spike

## Task 12: Add `superclaude review cluster`

Depends on: Task 3, Task 11

Create `src/superclaude/cli/review/cluster_cmd.py` exposing a click `command` named `cluster` and add `"cluster_cmd"` to the module tuple in `src/superclaude/cli/review/__init__.py`. Inputs: a directory of calibrated reviewer cards (findings-v2 block plus embedded `calibration:` block), `--snapshot <input-snapshot.yaml>`, optional `--kept <validator kept-ids file>`, `--out <dir>`. It writes `<out>/panel/clusters.json` with raw clusters, `clusters_kept`, `cluster_agreement`, `disputed` and `chained` flags. It never modifies a card and never writes anything but `clusters.json`. Create `tests/review/test_review_cluster_cmd.py`.

Acceptance criteria:
- A fixture directory of two cards produces `clusters.json` containing both passes and the agreement value; running twice is byte-identical.
- A card with an invalid findings-v2 block is reported as `invalid` in the output and excluded from agreement, not a crash.
- `superclaude review --help` lists `cluster`.

## Task 13: Add `superclaude review verify-citations`

Depends on: Task 1, Task 12

Create `src/superclaude/cli/review/verify_cmd.py` (command `verify-citations`, registered in `__init__.py`) per "Evidence gate and citation pre-check". For every findings-v2 citation it reads the file from the snapshot-verified path and records `missing-file`, `out-of-range` or `quote-not-found` (advisory) in `<out>/panel/precheck.json`, plus a `reread_set` listing every flagged citation. It spends zero model tokens, drops nothing, and never changes `citations_dropped` semantics. Create `tests/review/test_review_verify_citations.py`.

Acceptance criteria:
- Tests: a nonexistent path yields `missing-file`; a line range past end of file yields `out-of-range`; a quote absent from the cited lines yields `quote-not-found` and is marked advisory; a correct citation yields no flag.
- The output has no field named `dropped` and the command never deletes or rewrites a finding.
- `superclaude review --help` lists `verify-citations`.

## Task 14: Run the identity spike S-ID and record the result

Depends on: Task 11

Write `./artifacts/s-id-runbook.md` and run it. Dispatch three probe reviewers through the `reflect-reviewer` agent with the Agent tool `model` set to `haiku`, `sonnet` and `opus`, each given a probe brief asking it to state its model in one line (`reviewer_model_self_report`) and to attempt one repository write that must fail. Record in `./artifacts/s-id-results.md`: whether the self-report matches the pin in 3 of 3; whether the tool result or transcript exposes a model id; whether the read-only tool allowlist of `reflect-reviewer` survives the `model` override (write attempts blocked); and the decision for `identity_source` (`observed` if a model id is exposed, else `requested-pinned` stated as an unverified assumption). If a probe cannot be dispatched, record that and keep `requested-pinned`.

Acceptance criteria:
- `./artifacts/s-id-results.md` has one row per probe with pin, self-report, write-attempt outcome and any exposed model id.
- It ends with the explicit `identity_source` decision and the three Stage 1 exit facts: allowlist survives or not, self-report match count, model-id exposure yes or no.
- No file in the repository was modified by a probe (the document records a clean `git status` for the probe window).

## Phase 4: Stage 2 entry, contract compatibility gate

## Task 15: Add the panel contract lint and its per-field source table

Depends on: Task 6

Create `src/superclaude/cli/reflect/panel_lint.py` and `tests/cli/reflect/test_panel_contract_lint.py` per "Contract compatibility gate" item 3 and 5. The checker takes a panel-run contract and its output directory and asserts: `contract_version == "1.8.0"`; every top-level key is in the 1.8.0 stable field list (derive the list from `src/superclaude/skills/sc-reflect-protocol/SKILL.md` section 9.1) or the telemetry block; `merge_method` in `{adversarial, single-reviewer-fallback}`; `adversarial_convergence_score` is float or null; `adversarial_unavailable`, `regression_present` and the other `_LOAD_BEARING_BOOL_FIELDS` (`src/superclaude/cli/reflect/contract.py:47-57`) are real booleans; EV-1 on disk (`adversarial/merged-verdict.yaml`, card count equals `reviewers_resolved`); and the five fields whose producer changes (the diversity trio, `calibrator_diversity`, `reviewer_cards`) equal the legacy values on a matched fixture. Copy one recorded 1.8.0 pre contract and its directory structure to `tests/cli/reflect/fixtures/` as the matched fixture. Write `./artifacts/per-field-source-table.md` giving, for those five fields, the rule and the expected anthropic-only parity values (three distinct classes, vendor single, calibrator degraded).

Acceptance criteria:
- The lint passes on the legacy fixture and on a copy with a `panel/` directory added; it fails, with the offending key named, on a copy with an extra stable key or `merge_method: panel`.
- `uv run pytest tests/cli/reflect -q` passes.

## Task 16: Add the verdict replay and refresh the inventory

Depends on: Task 6, Task 15

Create `scripts/reflect_verdict_replay.py`. It feeds every recorded 1.8.0 pre contract under `.dev/reflect/pre-*` and, optionally, a second directory of shadow contracts through `derive_verdict` (`src/superclaude/cli/reflect/contract.py:138`) offline and prints a diff of verdicts and degraded reasons between legacy and shadow, exiting non-zero on any new degraded reason. Create `tests/cli/reflect/test_verdict_replay_script.py`. Re-run `scripts/reflect_consumer_inventory.py --out ./artifacts/stage2-entry-inventory.md` and diff it against `./artifacts/consumer-inventory.md`.

Acceptance criteria:
- Replaying the recorded contracts against themselves reports zero differences; a synthetic shadow contract with a new degraded reason makes the script exit non-zero.
- `./artifacts/stage2-entry-inventory.md` exists and the diff against the Task 6 inventory is either empty or lists each new file with its producer, validator or consumer role.

## Phase 5: Stage 2, pre-execution shadow mode in the reflect skill

## Task 17: Add the panel manifest module and CLI

Depends on: Task 11

Create `src/superclaude/cli/review/manifest.py`, `src/superclaude/cli/review/manifest_cmd.py` (command `manifest` with `init`, `advance`, `validate`, registered in `__init__.py`) and `tests/review/test_review_manifest.py` per "Execution contract (both adapters)". The manifest `<out>/panel/manifest.json` carries states `frozen`, `resolved`, `dispatched`, `collected`, `calibrated`, `clustered`, `debated`, `validated`, `published` and terminal `failed`; `frozen` records the reference to `artifacts/input-snapshot.yaml` with `input_tree_sha256`, template, tiers and brief-template sha256, schema ids and `run_id`; each later state records the hashes of its outputs. Idempotency identity is `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`: the same payload hash is a no-op, a different payload under the same identity is rejected, a new attempt supersedes a failed one without adding a vote. Record the counts `reviewers_requested`, `reviewers_resolved`, `reviewers_complete` and per-attempt completion states. Resume reuses a stage only when dependency hashes match. Publish writes REPORT.md, return-contract.yaml and audit.log to same-directory temporaries, renames them, then commits `published`.

Acceptance criteria:
- Tests: replaying an identical `advance` is a no-op; a conflicting payload is rejected; an out-of-order state is rejected; a changed plan hash on resume starts a new invocation; a crash between rename and commit leaves a manifest that readers refuse (no `published`).
- `superclaude review manifest --help` lists the three subcommands.

## Task 18: Add `--t2-engine` and the engine-decision rules to the reflect skill

Depends on: Task 14, Task 16, Task 17

Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (never `.claude/`). In section 3.1 add the flag `--t2-engine legacy|shadow` (default `legacy`; `panel` rejected with a message that it ships in Stage 3). Add a subsection after section 4.3 "T2 engine selection" holding rules D1-D5 from "When the panel is called (depth x tier path)": the flag is read only at the start of Wave 3 and only after the final tier is 2 (D1, D2: `--depth quick`, `--tier 1`, `--no-escalate` and rubric-stopped runs never read it); D3 for runs pinned to T2 with fewer than 2 distinct eligible classes (WARN of the section 7.1 text, `executor_exclusion_degraded`, `t2_floor_unmet` in `degraded_components`, `status: partial`, REPORT.md banner); D4 unsupported cells run the legacy rotation and record `panel_fallback_reason`; D5 `N_eff = min(--reviewers, alias count, 3)` with the anchor never dropped. Extend the `tier_decision.yaml` description in section 5.4 with `t2_engine_requested`, `t2_engine_effective` and `panel_fallback_reason`. Add the depth x tier path table to the skill. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- The skill states in plain text that with the default `legacy` the panel code is never called and that contract 1.8.0 is unchanged.
- `grep -n "src/superclaude" ` over the edited skill shows no new hit; existing skill tests pass: `uv run pytest tests/skills tests/cli/reflect -q`.
- `make verify-sync` passes and `git status` shows no staged or modified path under `.claude/` other than synced, gitignored copies.

## Task 19: Write the shadow-mode steps, brief line and telemetry into the reflect skill

Depends on: Task 12, Task 13, Task 18

Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`. Under the new T2 engine subsection add the "Pre-execution adapter" steps 3-9 and 11-12 for `--t2-engine shadow` as given in "Adapter sketches" and the "Shadow mode" paragraph: freeze via `superclaude review manifest init`; resolve with `superclaude review panel resolve --template @reflect-pre ... --hard-exclude-class <executor class> --strict-distinct` (re-resolve with `@reflect-pre-x2` on `ExclusionExhausted` of the anchor, record `anchor_replaced`), express the legacy rotation as the resolution and record `panel_parity: true|false`, with executor-unknown keeping the fail-open path and `executor_class_resolved: false`; add to the brief, inside the T1-card section of `refs/reviewer-spec.md` and not as a fourth section, the one line instructing each reviewer to end its card with a `## Findings block` fenced `findings-v2` block (`lens: reflect-pre`, citations with roles plan and spec) and a `reviewer_model_self_report` line; normalize cards with one bounded re-ask of the block only; run `superclaude review cluster` and `superclaude review verify-citations` as telemetry and flagging (flagged citations join the evidence-validator re-read set, the validator alone decides drops); record `judge_identity`, `judge_class_collision`, `debate_skipped_similar` after the debate; record `identity_source` from Task 14. State that the legacy debate, calibration, evidence gate and contract builder are authoritative and unchanged, and that panel artifacts go to `<out>/panel/`. Add the non-stable telemetry fields (`t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `cluster_agreement`, `manifest_path`, the three reviewer counts, the Stage 2 counts of 2-of-3 shortfalls and of `executor_class_resolved: false`, and the findings-block compliance rate) to section 9.2 only; leave section 9.1 and the contract version untouched. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- Section 9.1 and `contract_version: 1.8.0` are byte-identical to before; a diff of the skill shows additions only in the flag line, section 4.3a, section 5.4, section 9.2 and `refs/reviewer-spec.md`.
- The brief template still has exactly three sections.
- `grep -rn 'src/superclaude' src/superclaude/skills/sc-reflect-protocol` shows no hit that was not there before.
- `uv run pytest tests/skills tests/cli/reflect tests/review -q` and `make verify-sync` pass.

## Phase 6: Stage 2 exit tooling

## Task 20: Add the Stage 2 shadow-exit aggregator

Depends on: Task 16, Task 19

Create `scripts/reflect_shadow_exit.py` and `tests/cli/reflect/test_shadow_exit_script.py`. It scans `.dev/reflect/pre-*/panel/manifest.json` for runs with `t2_engine_effective: shadow`, joins each with its `return-contract.yaml` and `adversarial/merged-verdict.yaml`, and writes a report with: run count against the 20 required; MALFORMED count (must be zero); EV-1 failure rate compared with the rate over recorded legacy pre runs (must be no higher); the parity assertion result per run; verdict-replay diffs through `scripts/reflect_verdict_replay.py` (any new degraded reason fails); the Stage 2 counts (2-of-3 shortfalls, unknown executor, findings-block compliance rate, `cluster_agreement` distribution); and an overall PASS, FAIL or INSUFFICIENT-RUNS line.

Acceptance criteria:
- Tests with synthetic shadow run directories: 20 clean runs report PASS; one MALFORMED run reports FAIL; 12 clean runs report INSUFFICIENT-RUNS; a parity failure reports FAIL.
- Running it on the current repository (no shadow runs yet) prints INSUFFICIENT-RUNS with run count 0 and exits with a documented non-zero code.
