# Reviewer 3 brief (refactorer)

## T1 card excerpt

# Tier 1 reflection card (UC-1 pre-execution)

- Plan: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md
- Spec (real, pointed to by source.md): .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md sha256 54a8dce2...c4e45
- Prior T1 pass by the plan author (unvalidated, not independent): .dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203500/REPORT.md
- coverage_degraded: parsed-sparse (source.md carries no labelled requirement ids; spec has none either, headings are the only structure)

## Leads for reviewers (unverified suspicions, each needs a citation or must be dropped)

- L1: Task 10 acceptance names an `@reflect-pre` resolve that only works after Task 11 ("once Task 11 lands"), so Task 10 cannot be closed on its own acceptance.
- L2: Task 14 acceptance asks for "a clean git status for the probe window" in a worktree that is already dirty (staged and untracked package files).
- L3: Task 19 records `judge_identity` and `judge_class_collision` after the debate; the spec lists the judge-exclusion input and the contract field that carries judge identity as UNVERIFIED (lines 584-585) and no task verifies it.
- L4: Spec Cost model (474-501) and Risks (502-521) may hold Stage 0-2 requirements with no task.
- L5: Task 4 expects 7 null convergence scores; confirm the number exists in the spec or the recorded data.
- L6: Prior pass R-5: Task 19 does not say what shadow does when `panel_parity` is false.
- L7: Task 9 relies on a `launch` field and a `round_robin` strategy and `--sequence`; confirm they exist in `panel.py` and the tiers file; confirm cited line numbers (panel.py 380, 427; panel_cmd.py 18-52; contract.py 47-57, 138; findings.py 90-196, 321-337).
- L8: Task 15 puts a checker into `src/superclaude/cli/reflect/panel_lint.py`; spec names only the test file.



## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-11T20:36:38Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md:1-30

```markdown
1	---
2	schema: workflow-plan/1.2
3	source: ./source.md
4	strategy: systematic
5	depth: standard
6	slug: TASK-WF-implementStages0-20261111-202912
7	version: "1"
8	priority: Medium
9	created_date: "2026-11-11"
10	---
11	
12	# Reflect Tier 2 review panel: Stages 0 to 2 (offline measurement, dormant kernel, pre shadow mode)
13	
14	Source: ./source.md
15	Goal: The shared review kernel gains findings-v2, path-aware clustering, hard executor exclusion, reflect templates and citation pre-check, all dormant or telemetry-only; `/sc:reflect` pre-execution accepts `--t2-engine legacy|shadow` (default `legacy`) and, in shadow, writes panel artifacts next to an unchanged legacy run, with the tooling to judge the Stage 2 exit.
16	
17	## Constraints
18	
19	- Requirement text lives in `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md` (sha256 recorded in `./source.md`). Section names below refer to that file. Items it marks PROPOSED are new names to create; items it marks UNVERIFIED must be checked in code before relying on them.
20	- Return contract stays `1.8.0` with no new stable field and no new legal value (`merge_method` stays `adversarial` or `single-reviewer-fallback`). Panel data lives only in `<out>/panel/*` and the non-stable telemetry block.
21	- The `/sc:adversarial` debate stays authoritative in pre-execution. K4 clustering, the citation pre-check and the findings block never drop a citation, never feed the debate and never route anything.
22	- Default behavior of every existing command is unchanged: with no new flag, `superclaude review panel resolve`, `review merge`, `review ledger` and the spec-panel loop produce byte-identical output.
23	- Plan decision: in Stage 2 the flag accepts only `legacy` and `shadow`; the value `panel` is rejected with a plain message saying it ships in Stage 3. The post-execution path, the swarm lens, `--panel-resolution` and the headless `citations_dropped` change are Stage 5 and are not touched.
24	- Plan decision: the prose coordinator of the reflect skill cannot import Python, so the manifest gets a minimal `superclaude review manifest` CLI (init, advance, validate) instead of hand-written JSON.
25	- Edit installed primitives only under `src/superclaude/` and run `make sync-dev` afterwards. Never edit or add files under `.claude/` by hand. Installed primitives reference other primitives by installed path or the `superclaude` CLI, never by a `src/superclaude/...` path.
26	- All Python runs through `uv run`. Never use Opus, Fable or Tier 0 in any new template; Fable and Tier 0 are rejected by validation.
27	- Human-supplied inputs are not fabricated: the 50-pair cluster labels (Task 5) and the 20 real shadow runs (Task 20) are produced by the owner and by normal use after merge. The tasks deliver the sheets, scorers and aggregators that judge them.
28	- Task-owned evidence goes under `./artifacts/` in this package.
29	
30	## Phase 1: Stage 0, offline measurement (findings-v2, converter, cluster_v2, replay)
```

### .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md:149-251

```markdown
149	## Phase 3: Stage 1b, clustering and citation tooling, identity spike
150	
151	## Task 12: Add `superclaude review cluster`
152	
153	Depends on: Task 3, Task 11
154	
155	Create `src/superclaude/cli/review/cluster_cmd.py` exposing a click `command` named `cluster` and add `"cluster_cmd"` to the module tuple in `src/superclaude/cli/review/__init__.py`. Inputs: a directory of calibrated reviewer cards (findings-v2 block plus embedded `calibration:` block), `--snapshot <input-snapshot.yaml>`, optional `--kept <validator kept-ids file>`, `--out <dir>`. It writes `<out>/panel/clusters.json` with raw clusters, `clusters_kept`, `cluster_agreement`, `disputed` and `chained` flags. It never modifies a card and never writes anything but `clusters.json`. Create `tests/review/test_review_cluster_cmd.py`.
156	
157	Acceptance criteria:
158	- A fixture directory of two cards produces `clusters.json` containing both passes and the agreement value; running twice is byte-identical.
159	- A card with an invalid findings-v2 block is reported as `invalid` in the output and excluded from agreement, not a crash.
160	- `superclaude review --help` lists `cluster`.
161	
162	## Task 13: Add `superclaude review verify-citations`
163	
164	Depends on: Task 1, Task 12
165	
166	Create `src/superclaude/cli/review/verify_cmd.py` (command `verify-citations`, registered in `__init__.py`) per "Evidence gate and citation pre-check". For every findings-v2 citation it reads the file from the snapshot-verified path and records `missing-file`, `out-of-range` or `quote-not-found` (advisory) in `<out>/panel/precheck.json`, plus a `reread_set` listing every flagged citation. It spends zero model tokens, drops nothing, and never changes `citations_dropped` semantics. Create `tests/review/test_review_verify_citations.py`.
167	
168	Acceptance criteria:
169	- Tests: a nonexistent path yields `missing-file`; a line range past end of file yields `out-of-range`; a quote absent from the cited lines yields `quote-not-found` and is marked advisory; a correct citation yields no flag.
170	- The output has no field named `dropped` and the command never deletes or rewrites a finding.
171	- `superclaude review --help` lists `verify-citations`.
172	
173	## Task 14: Run the identity spike S-ID and record the result
174	
175	Depends on: Task 11
176	
177	Write `./artifacts/s-id-runbook.md` and run it. Dispatch three probe reviewers through the `reflect-reviewer` agent with the Agent tool `model` set to `haiku`, `sonnet` and `opus`, each given a probe brief asking it to state its model in one line (`reviewer_model_self_report`) and to attempt one repository write that must fail. Record in `./artifacts/s-id-results.md`: whether the self-report matches the pin in 3 of 3; whether the tool result or transcript exposes a model id; whether the read-only tool allowlist of `reflect-reviewer` survives the `model` override (write attempts blocked); and the decision for `identity_source` (`observed` if a model id is exposed, else `requested-pinned` stated as an unverified assumption). If a probe cannot be dispatched, record that and keep `requested-pinned`.
178	
179	Acceptance criteria:
180	- `./artifacts/s-id-results.md` has one row per probe with pin, self-report, write-attempt outcome and any exposed model id.
181	- It ends with the explicit `identity_source` decision and the three Stage 1 exit facts: allowlist survives or not, self-report match count, model-id exposure yes or no.
182	- No file in the repository was modified by a probe (the document records a clean `git status` for the probe window).
183	
184	## Phase 4: Stage 2 entry, contract compatibility gate
185	
186	## Task 15: Add the panel contract lint and its per-field source table
187	
188	Depends on: Task 6
189	
190	Create `src/superclaude/cli/reflect/panel_lint.py` and `tests/cli/reflect/test_panel_contract_lint.py` per "Contract compatibility gate" item 3 and 5. The checker takes a panel-run contract and its output directory and asserts: `contract_version == "1.8.0"`; every top-level key is in the 1.8.0 stable field list (derive the list from `src/superclaude/skills/sc-reflect-protocol/SKILL.md` section 9.1) or the telemetry block; `merge_method` in `{adversarial, single-reviewer-fallback}`; `adversarial_convergence_score` is float or null; `adversarial_unavailable`, `regression_present` and the other `_LOAD_BEARING_BOOL_FIELDS` (`src/superclaude/cli/reflect/contract.py:47-57`) are real booleans; EV-1 on disk (`adversarial/merged-verdict.yaml`, card count equals `reviewers_resolved`); and the five fields whose producer changes (the diversity trio, `calibrator_diversity`, `reviewer_cards`) equal the legacy values on a matched fixture. Copy one recorded 1.8.0 pre contract and its directory structure to `tests/cli/reflect/fixtures/` as the matched fixture. Write `./artifacts/per-field-source-table.md` giving, for those five fields, the rule and the expected anthropic-only parity values (three distinct classes, vendor single, calibrator degraded).
191	
192	Acceptance criteria:
193	- The lint passes on the legacy fixture and on a copy with a `panel/` directory added; it fails, with the offending key named, on a copy with an extra stable key or `merge_method: panel`.
194	- `uv run pytest tests/cli/reflect -q` passes.
195	
196	## Task 16: Add the verdict replay and refresh the inventory
197	
198	Depends on: Task 6, Task 15
199	
200	Create `scripts/reflect_verdict_replay.py`. It feeds every recorded 1.8.0 pre contract under `.dev/reflect/pre-*` and, optionally, a second directory of shadow contracts through `derive_verdict` (`src/superclaude/cli/reflect/contract.py:138`) offline and prints a diff of verdicts and degraded reasons between legacy and shadow, exiting non-zero on any new degraded reason. Create `tests/cli/reflect/test_verdict_replay_script.py`. Re-run `scripts/reflect_consumer_inventory.py --out ./artifacts/stage2-entry-inventory.md` and diff it against `./artifacts/consumer-inventory.md`.
201	
202	Acceptance criteria:
203	- Replaying the recorded contracts against themselves reports zero differences; a synthetic shadow contract with a new degraded reason makes the script exit non-zero.
204	- `./artifacts/stage2-entry-inventory.md` exists and the diff against the Task 6 inventory is either empty or lists each new file with its producer, validator or consumer role.
205	
206	## Phase 5: Stage 2, pre-execution shadow mode in the reflect skill
207	
208	## Task 17: Add the panel manifest module and CLI
209	
210	Depends on: Task 11
211	
212	Create `src/superclaude/cli/review/manifest.py`, `src/superclaude/cli/review/manifest_cmd.py` (command `manifest` with `init`, `advance`, `validate`, registered in `__init__.py`) and `tests/review/test_review_manifest.py` per "Execution contract (both adapters)". The manifest `<out>/panel/manifest.json` carries states `frozen`, `resolved`, `dispatched`, `collected`, `calibrated`, `clustered`, `debated`, `validated`, `published` and terminal `failed`; `frozen` records the reference to `artifacts/input-snapshot.yaml` with `input_tree_sha256`, template, tiers and brief-template sha256, schema ids and `run_id`; each later state records the hashes of its outputs. Idempotency identity is `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`: the same payload hash is a no-op, a different payload under the same identity is rejected, a new attempt supersedes a failed one without adding a vote. Record the counts `reviewers_requested`, `reviewers_resolved`, `reviewers_complete` and per-attempt completion states. Resume reuses a stage only when dependency hashes match. Publish writes REPORT.md, return-contract.yaml and audit.log to same-directory temporaries, renames them, then commits `published`.
213	
214	Acceptance criteria:
215	- Tests: replaying an identical `advance` is a no-op; a conflicting payload is rejected; an out-of-order state is rejected; a changed plan hash on resume starts a new invocation; a crash between rename and commit leaves a manifest that readers refuse (no `published`).
216	- `superclaude review manifest --help` lists the three subcommands.
217	
218	## Task 18: Add `--t2-engine` and the engine-decision rules to the reflect skill
219	
220	Depends on: Task 14, Task 16, Task 17
221	
222	Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (never `.claude/`). In section 3.1 add the flag `--t2-engine legacy|shadow` (default `legacy`; `panel` rejected with a message that it ships in Stage 3). Add a subsection after section 4.3 "T2 engine selection" holding rules D1-D5 from "When the panel is called (depth x tier path)": the flag is read only at the start of Wave 3 and only after the final tier is 2 (D1, D2: `--depth quick`, `--tier 1`, `--no-escalate` and rubric-stopped runs never read it); D3 for runs pinned to T2 with fewer than 2 distinct eligible classes (WARN of the section 7.1 text, `executor_exclusion_degraded`, `t2_floor_unmet` in `degraded_components`, `status: partial`, REPORT.md banner); D4 unsupported cells run the legacy rotation and record `panel_fallback_reason`; D5 `N_eff = min(--reviewers, alias count, 3)` with the anchor never dropped. Extend the `tier_decision.yaml` description in section 5.4 with `t2_engine_requested`, `t2_engine_effective` and `panel_fallback_reason`. Add the depth x tier path table to the skill. Run `make sync-dev` and `make verify-sync`.
223	
224	Acceptance criteria:
225	- The skill states in plain text that with the default `legacy` the panel code is never called and that contract 1.8.0 is unchanged.
226	- `grep -n "src/superclaude" ` over the edited skill shows no new hit; existing skill tests pass: `uv run pytest tests/skills tests/cli/reflect -q`.
227	- `make verify-sync` passes and `git status` shows no staged or modified path under `.claude/` other than synced, gitignored copies.
228	
229	## Task 19: Write the shadow-mode steps, brief line and telemetry into the reflect skill
230	
231	Depends on: Task 12, Task 13, Task 18
232	
233	Edit `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`. Under the new T2 engine subsection add the "Pre-execution adapter" steps 3-9 and 11-12 for `--t2-engine shadow` as given in "Adapter sketches" and the "Shadow mode" paragraph: freeze via `superclaude review manifest init`; resolve with `superclaude review panel resolve --template @reflect-pre ... --hard-exclude-class <executor class> --strict-distinct` (re-resolve with `@reflect-pre-x2` on `ExclusionExhausted` of the anchor, record `anchor_replaced`), express the legacy rotation as the resolution and record `panel_parity: true|false`, with executor-unknown keeping the fail-open path and `executor_class_resolved: false`; add to the brief, inside the T1-card section of `refs/reviewer-spec.md` and not as a fourth section, the one line instructing each reviewer to end its card with a `## Findings block` fenced `findings-v2` block (`lens: reflect-pre`, citations with roles plan and spec) and a `reviewer_model_self_report` line; normalize cards with one bounded re-ask of the block only; run `superclaude review cluster` and `superclaude review verify-citations` as telemetry and flagging (flagged citations join the evidence-validator re-read set, the validator alone decides drops); record `judge_identity`, `judge_class_collision`, `debate_skipped_similar` after the debate; record `identity_source` from Task 14. State that the legacy debate, calibration, evidence gate and contract builder are authoritative and unchanged, and that panel artifacts go to `<out>/panel/`. Add the non-stable telemetry fields (`t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `cluster_agreement`, `manifest_path`, the three reviewer counts, the Stage 2 counts of 2-of-3 shortfalls and of `executor_class_resolved: false`, and the findings-block compliance rate) to section 9.2 only; leave section 9.1 and the contract version untouched. Run `make sync-dev` and `make verify-sync`.
234	
235	Acceptance criteria:
236	- Section 9.1 and `contract_version: 1.8.0` are byte-identical to before; a diff of the skill shows additions only in the flag line, section 4.3a, section 5.4, section 9.2 and `refs/reviewer-spec.md`.
237	- The brief template still has exactly three sections.
238	- `grep -rn 'src/superclaude' src/superclaude/skills/sc-reflect-protocol` shows no hit that was not there before.
239	- `uv run pytest tests/skills tests/cli/reflect tests/review -q` and `make verify-sync` pass.
240	
241	## Phase 6: Stage 2 exit tooling
242	
243	## Task 20: Add the Stage 2 shadow-exit aggregator
244	
245	Depends on: Task 16, Task 19
246	
247	Create `scripts/reflect_shadow_exit.py` and `tests/cli/reflect/test_shadow_exit_script.py`. It scans `.dev/reflect/pre-*/panel/manifest.json` for runs with `t2_engine_effective: shadow`, joins each with its `return-contract.yaml` and `adversarial/merged-verdict.yaml`, and writes a report with: run count against the 20 required; MALFORMED count (must be zero); EV-1 failure rate compared with the rate over recorded legacy pre runs (must be no higher); the parity assertion result per run; verdict-replay diffs through `scripts/reflect_verdict_replay.py` (any new degraded reason fails); the Stage 2 counts (2-of-3 shortfalls, unknown executor, findings-block compliance rate, `cluster_agreement` distribution); and an overall PASS, FAIL or INSUFFICIENT-RUNS line.
248	
249	Acceptance criteria:
250	- Tests with synthetic shadow run directories: 20 clean runs report PASS; one MALFORMED run reports FAIL; 12 clean runs report INSUFFICIENT-RUNS; a parity failure reports FAIL.
251	- Running it on the current repository (no shadow runs yet) prints INSUFFICIENT-RUNS with run count 0 and exits with a documented non-zero code.
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:358-400

```markdown
358	## Adapter sketches
359	
360	### Execution contract (both adapters)
361	
362	<!-- Source: Variant 3 (haiku:backend), Adapter sketches final block ("Operational execution contract, both adapters") - merged per Change #1; additions per Change #29 -->
363	**Execution contract (both adapters).** A coordinator-owned manifest `<output>/panel/manifest.json` (PROPOSED) carries run state `frozen -> resolved -> dispatched -> collected -> calibrated -> clustered -> debated -> validated -> published`, plus terminal `failed`. One coordinator writes it; reviewer agents only return data. `frozen` records the reference to `<output>/artifacts/input-snapshot.yaml` and its `input_tree_sha256` (the existing multi-file hash, `SKILL.md:217-229`), the template sha256, tiers sha256, brief-template sha256, schema ids, `run_id`. Each later state records the hashes of the outputs it committed. **Idempotency identity:** `(run_id, input_tree_sha256, policy_sha256, stage, reviewer_id, attempt_id)`. A repeated submission with the same payload hash is a no-op; a different payload under the same identity is rejected. An attempt supersedes an earlier failed attempt of the same reviewer but never adds a vote and never clears a finding. **Resume:** reuse a completed stage only when all its dependency hashes still match; a changed plan or spec hash starts a new invocation. **Publish:** write `REPORT.md`, `return-contract.yaml` and `audit.log` to same-directory temporaries, rename them, then commit `published` in the manifest; a reader accepts only a committed manifest (a non-atomic pair is a real risk: `merge_cmd.py:113-116` writes the report before saving the ledger). One total deadline across stages (the ensemble already captures a shared deadline before dispatch, `ensemble.py` per V3, UNVERIFIED line); failed attempts never restart the whole panel.
364	
365	State variables (INV-001, INV-002, INV-003): (1) `@reflect-*` templates use only `fixed` and `random` strategies; reflect-profile validation rejects `round_robin` unless `--sequence` is supplied and recorded in the manifest (round_robin slots seed from `date.today().toordinal()` when no `sequence` is passed, `panel.py:471-476`, so a resume after midnight re-resolves; random slots hash `run_id`, `:455-459`, and are stable). (2) The plan and spec (and every grounding file) are covered by the existing `input_tree_sha256` and per-file sha256 list of `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), re-read and recomputed before Wave 5 and before promotion (`SKILL.md:227`); the manifest references that file by hash; no single-document hash is used and `doc_sha256` of the ledger is not relied on. (3) Reflect uses no ledger in Stages 0-4. If a ledger is ever used, each merge attempt writes to its own path `<out>/panel/attempt-<n>/ledger.json` and `merged.md`, and only the attempt named by the committed manifest is read (`ledger.py:114-118` refuses a re-merge of round 1).
366	
367	### Pre-execution adapter (agent-session engine)
368	
369	<!-- Source: Base (original, modified) - steps 1-12 replaced per Change #44; Variant 3 (haiku:backend) pre steps 1, 7, 8 and input-drift recheck; Variant 2 (sonnet:analyzer) step 8 -->
370	Inputs: `--spec`, `--tasklist`, `--executor-model` (optional), PROPOSED `--t2-engine legacy|shadow|panel` (default `legacy`).
371	
372	1. **Wave 0 and Waves 1-2 unchanged**: alias resolution, executor class (`SKILL.md:600-602`), budget pre-flight, grounding, coverage map (two-pass extraction), T1 card, blind calibration of the T1 card, rubric. If the final tier is 1 the adapter never runs and `--t2-engine` is not read (rules D1, D2 of "When the panel is called").
373	2. **Engine decision.** `t2_engine_effective = requested` only if the final tier is 2 and the environment gate holds (Stage 3 entry); else `legacy` with `panel_fallback_reason`. Write both into `tier_decision.yaml`.
374	3. **Freeze** (manifest `frozen`, see "Execution contract"): reference `artifacts/input-snapshot.yaml` by hash, pin template, tiers and brief-template hashes.
375	4. **Resolve**: `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct` (`--template`, `--run-id`, `--kind`, `--env` exist, `panel_cmd.py:18-52`; the last two flags are PROPOSED; `--exclude-class` does not exist). On `ExclusionExhausted` for the anchor, re-resolve with `@reflect-pre-x2`; assert the invariants of K1 contract item 6; write `<out>/panel/resolution.json`. Below the floor: rule D3 or the `SKILL.md:600` degrade.
376	5. **Briefs**: exactly three sections (`reviewer-spec.md:31-74`), persona by resolution order (analyzer, qa, refactorer), qa gets the spec body (`:55`). One added instruction line inside the T1-card section: "End your card with a `## Findings block` fenced `findings-v2` block, `lens: reflect-pre`, citations with roles `plan` and `spec`." Not a fourth section.
377	6. **Dispatch**: parallel Agent calls to `reflect-reviewer` with the explicit `model` of the Agent-session adapter rule, cards to `<out>/reviewer-cards/reviewer-<n>-card.md` (or `.yaml` as today). Attempts and completion states go to the manifest (see "Completion and channel").
378	7. **Normalize**: parse each card's findings-v2 block (convert line refs, see "What a recorded card looks like"); an invalid block gets one bounded re-ask for the block only; the card body still reaches the debate.
379	8. **Blind calibration** (unchanged mechanism, `SKILL.md:1192`): one `confidence-calibrator` per card, class chosen by `SKILL.md:1181-1186`, result embedded in the card as the existing `calibration:` block.
380	9. **K4 clustering and pre-check (telemetry and flagging only)**: `superclaude review cluster` writes `panel/clusters.json`; `superclaude review verify-citations` writes `panel/precheck.json`; neither drops anything and neither feeds the debate.
381	10. **Debate (unchanged)**: `Skill sc-adversarial-protocol --compare <calibrated cards> --depth standard --focus correctness,coverage,deviation-classification --output <out>/adversarial/` (`SKILL.md:645-651`; under `--unattended`, `SKILL.md:653`). Remap `artifacts_dir` to `adversarial_artifacts_dir` (`:657`). Record judge identity and collisions (see Q3). The debate input is unchanged (the calibrated cards, not the cluster table), so clustering cannot change whether sc-adversarial considers the variants "substantially identical". If the child returns a null score without `adversarial_unavailable`, the adapter keeps the real null (no synthetic 1.0), sets `debate_skipped_similar: true` in telemetry when the child's log says so, and the existing null routing applies (`SKILL.md:659-664`). EV-1 is unchanged (`:666`): `merged-verdict.yaml` with `merge_method: adversarial` plus at least the resolved `--reviewers` count of calibrated cards, or a corroborated F2/F3 fallback; the count it compares is the resolved reviewer count after exclusion (the manifest records requested, resolved and complete counts separately).
382	11. **Wave 5 synthesis and evidence-validator (unchanged, mandatory, `SKILL.md:587`)** with the pre-check flags added to the re-read set (see "Evidence gate and citation pre-check"); recompute `input_tree_sha256` before synthesis (`:227`).
383	12. **Publish** atomically (see "Execution contract") and emit contract 1.8.0 by the legacy rules; lint (see "Contract compatibility gate") in tests.
384	
385	**Shadow mode** (`--t2-engine shadow`): steps 4-9 run with the legacy rotation expressed as the resolution (identical reviewers); the assertion "panel resolution == legacy rotation" is recorded; the debate result is authoritative; panel artifacts and telemetry are written for the measurement.
386	
387	### Post-execution adapter (Stage 5; both engines)
388	
389	<!-- Source: Base (original, modified) - steps 1-10 replaced per Change #44, #35 -->
390	Inputs: `--spec`, `--tasklist`, `--task-log`, `--diff`, `--executor-model`, `--t2-engine`.
391	
392	1. Waves 0-2 unchanged, including the §6.1 verification run by the orchestrator (reviewers never execute, `reflect-reviewer.md` Safety Constraint; refs/reviewer-spec.md:14).
393	2. Resolve with `@reflect-post` (same slots; `@reflect-post-x2` for anchor replacement) and the executor class hard-excluded and strict distinctness; this matters most here (self-confirmation, `SKILL.md:600`).
394	3. Briefs unchanged; each grounding hunk is an H3 `path:start-end` (`reviewer-spec.md:45`); the qa ordinal gets the verification and runtime-surface hunks (`reviewer-spec.md:53,57`); `lens: reflect-post`, `deviation_class` required; no-spec gaps use `channel: advisory`.
395	4. Dispatch: agent-session as pre; headless `superclaude reflect` -> ensemble -> swarm `reflect-review` lens, unchanged in Stage 5 except that it may read the K1 resolution through a PROPOSED `--panel-resolution` input with `T2Model0N` as the fallback. The bounded fallback ladder stays (cli/reflect/fallback.py, body UNVERIFIED).
396	5. Blind calibration per card (embedded); pre-check flags; evidence-validator (unchanged).
397	6. K4 clustering to `panel/clusters.json` (telemetry).
398	7. **Debate (kept)**: `Skill sc-adversarial-protocol --compare <calibrated cards>` exactly as `SKILL.md:645-651`. The K4 cluster map is written to `panel/clusters.json` for the Stage 5 post measurement; it is not an input to the debate until that measurement shows an effect (O-3). Replacing or narrowing the post debate needs its own post trial with seeded deviations and class accuracy. Writes `adversarial/merged-verdict.yaml`.
399	8. Contract: `merge_method: adversarial`, the child's score; 1.8.0 semantics unchanged. Promotion, remediation and the `reflect_post` write-back are unchanged.
400	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:416-521

```markdown
416	## Return-contract 1.8.0 mapping
417	
418	<!-- Source: Variant 3 (haiku:backend), "Return-contract 1.8.0 mapping" (adopted table) - merged per Change #15; Base (original, modified) - consumer list kept and moved to the deferred path; corrected per Change #14, #16 -->
419	**Producers and the wrapper.** Two producers exist: the interactive skill (1.8.0, pre and post) and the headless ensemble builder (`ensemble.py:788`, constant `REFLECT_CONTRACT_VERSION = "1.0"` at `ensemble.py:74`, post only: `"mode": "post"` at `:797`). Recorded interactive pre contracts say `contract_version: "1.8.0"` (37 of 62 under `.dev/reflect/pre-*`; others 1.0, 1.2.0, 1.3.0, 1.5.0, 1.7.0). The wrapper accepts any major `1` and BLOCKS any other major (`contract.py:187-194`, `unknown-major-version`; fixture `tests/cli/reflect/fixtures/blocked_unknown_major.yaml`), then applies degraded/halted triggers 1-14. No change to any of these is needed while the contract stays 1.8.0. Any future major version must first change `contract.py:187-194`. The only other `contract_version` equality in `src/` is `sc-implement-protocol/scripts/archive_workspace.py:327` (`!= "1.1"`), a different contract.
420	
421	**Versioning plan.** Stages 0-4 change no stable field: `contract_version` stays `1.8.0` for interactive runs; no field is added to the stable block; panel data lives in referenced artifacts (`<out>/panel/*`) and in the non-stable telemetry block (`SKILL.md` two-block contract). **Bump rule (applies to every later proposal):** a new top-level stable field = minor (`SKILL.md:952`); a new legal value of an existing field, a changed meaning, a gate-text change = major (`SKILL.md:953`); a new telemetry-only field = no bump. A contract lint test (see "Contract compatibility gate") enforces this on panel runs. `merge_method` stays in `{adversarial, single-reviewer-fallback}` (`SKILL.md:789`, EV-2; EV-1 at `SKILL.md:666` requires `merged-verdict.yaml` with `merge_method: adversarial`).
422	
423	| Contract field or family | Source in the panel path | Status |
424	|---|---|---|
425	| `contract_version` | constant `1.8.0` (interactive builder); headless builder constant `"1.0"` untouched | unchanged |
426	| `status`, `mode`, `tier_reached` | existing reduction; `tier_reached` is 2 only when the N=2 floor of distinct `complete` classes holds | unchanged meaning |
427	| `merge_method` | `adversarial` from the real `sc-adversarial` run; `single-reviewer-fallback` via the F2 path | unchanged legal set |
428	| `adversarial_convergence_score` | the child's `convergence_score` or null; never synthesized | unchanged |
429	| `adversarial_unavailable`, `adversarial_artifacts_dir` | F3 path as today; mechanical remap `artifacts_dir` -> `adversarial_artifacts_dir` (`SKILL.md:657`) | unchanged |
430	| `reviewer_cards` | calibrated card paths (cards carry the findings-v2 block and the embedded `calibration:`) | unchanged |
431	| `t2_model_class_diversity`, `t2_vendor_diversity`, `t2_effective_diversity`, `calibrator_diversity` | computed with the same rules as the legacy path from the resolved classes (parity template, see "Template set") | unchanged semantics; values asserted equal on matching inputs by the lint test |
432	| `citations_total/revalidated/dropped`, `evidence_validator_ran` | validator results; pre-check only flags | unchanged semantics |
433	| coverage, deviation, verification, reachability, promotion, remediation fields | reflect waves | unchanged |
434	| `panel_*`, `cluster_agreement`, `manifest_path`, `t2_engine_requested/effective`, `identity_source` | telemetry block / artifacts | non-stable, no bump |
435	
436	**Null-score rules.** Route on `merge_method` first (`SKILL.md:661`). `adversarial_convergence_score` is a real child score or null; null enters only on the F3 path, a skipped debate or a failed child; no synthetic 0, 0.5 or 1.0. A null at T2 stays `status: partial` and blocks promotion (`SKILL.md:659-664`; wrapper trigger 11 `contract.py:299-300`). `cluster_agreement` is never compared with the convergence thresholds and never routes anything. In `sc-adversarial-protocol/SKILL.md`, variants differing by under 10% skip the debate (`:407-410`, `:948-951`) and `convergence_score` is "null if debate not reached" (`:439,457`); a unanimous clean run can therefore return null today, which the wrapper degrades at T2 and promotion blocks (`SKILL.md:663`). Recorded pre contracts include 7 null scores; their cause (skipped debate versus F2/F3) is UNVERIFIED. Stage 0a classifies the 7 recorded nulls by cause; if skipped-similar is a frequent cause, a separate decision (not this design) is needed on whether a skipped debate should return a score.
437	
438	**Recorded convergence evidence.** Recorded pre contracts under `.dev/reflect/` show a convergence score of 1.0 in 21 of 35 numeric cases and below 1.0 in 14 (0.40 to 0.9615); 7 T2-reached contracts have a null score (2 `single-reviewer-fallback`, 3 illegal values such as `none` and `inline-orchestrator`, 1 `adversarial` with a null score, 1 `sc-adversarial-protocol-mode-a`); 5 `single-reviewer-fallback` contracts exist in all. These are agreement observations, not defect-recall measurements, and vendor diversity was single in the recorded T2 runs the enrichment cites. They do not show the debate is idle. The debate stays advisory in pre.
439	
440	**Promotion gate condition 9 (`SKILL.md:1483`).** Unchanged in every planned stage: the retained debate keeps a real merged adversarial verdict on every T2 run. The condition's operative test is `tier_reached == 2 AND adversarial_unavailable == true` (blocked), and its `convergence_score` is the prose name of `adversarial_convergence_score`; both stay as written. Promotion is UC-2 only (`promotion_gate_passed` is null when `mode == pre`, `SKILL.md:837`).
441	
442	**`reflect_post` frontmatter** (`cli/reflect/runner.py:103-133`): unchanged in every stage. Fields are verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at and the three `*_verified` booleans, in a fixed order; no merge field. The wrapper writes it for post runs on a tasklist only; the pre adapter never writes it. Do not add panel fields to it.
443	
444	**Consumer by consumer** (each: no change while the contract stays 1.8.0).
445	
446	- **sc-workflow Wave 4** reads `reflect_status` and `reflect_report_path` only (`sc-workflow-protocol/SKILL.md:60`): no change.
447	- **Wrapper verdict map** (cli/reflect/contract.py): triggers 10, 11 and 11b read `merge_method` and the convergence score exactly as before: no change.
448	- **Headless ensemble contract builder** (`ensemble.py:772-773`): post-only, no change in Stages 0-4; Stage 5 makes `citations_dropped` real (announced behavior change).
449	- **Sprint executor TurnLedger** (`SKILL.md:930`) reads `status` and `per_task_verdicts`: post-only, unchanged (executor code UNVERIFIED).
450	- **sc-troubleshoot, sc-task, task-builder, sc-workflow T3 handoff** (`SKILL.md:929, 931, 937-938`) read no merge fields; `task-builder` EV-4 (line 2242) requires `merge_method: adversarial` on disk for post, which still holds.
451	- **sc:roadmap, sc:tasklist gates** (`SKILL.md:932-933`) read coverage fields: no change.
452	- **Wave 7 promotion** (`SKILL.md:939`): post-only, see condition 9.
453	- **CI grader** (`make reflect-eval`, `SKILL.md:940`): `.dev/eval-workspaces/sc-reflect/grader.py` has no match for `merge_method`, `contract_version` or `convergence` (grep), so it needs no change today.
454	- **Meta-eval aggregator** (`SKILL.md:941`) reads `convergence_score`: no change.
455	- **Reflect SKILL.md** EV-1 (`:666`) and EV-2 (`:789`): no change (installed as `~/.claude/skills/sc-reflect-protocol/SKILL.md`).
456	
457	### Deferred versioned change (candidate E', not scheduled)
458	
459	A deterministic authoritative merge in pre would add `merge_method` value `panel` (pre only), which is a major version, `2.0.0`. Every consumer that must change first: (1) `contract.py:187-194` major gate; (2) `contract.py:295-300,317-326` triggers 10, 11, 11b (guard on `merge_method`; trigger 11 would mis-fire on a null score from a panel merge); (3) `ensemble.py:74,772-773,788,806` builder constant and merge-method derivation; (4) reflect `SKILL.md` EV-1 (`:666`), EV-2 (`:789`), the §9.4 note, and promotion condition 9 text (`:1483`); (5) `task-builder` SKILL.md EV-4 (line 2242: requires `merge_method: adversarial` on disk for post); (6) `refs/ops-integration.md:239` (`adversarial.merge_method` PromQL label values); (7) the meta-eval aggregator that reads `convergence_score` (`SKILL.md:941`); (8) the sprint executor routing named at `SKILL.md:664` and `:930` (executor code UNVERIFIED); (9) `tests/cli/reflect` (25 fixture files carry `merge_method`; `test_ensemble_unit.py`, `test_ensemble_stub_integration.py`, `test_verdict_mapping.py`, `test_contract_fallback_metadata.py`); (10) `sc-workflow` Wave 4 reads only `reflect_status` and `reflect_report_path` (`sc-workflow-protocol/SKILL.md:60`), no change. The CI grader has no match (above), so it needs no change today.
460	
461	### Contract compatibility gate
462	
463	<!-- Source: Base (original, modified) - new subsection merged per Change #27 (INV-023) -->
464	The wrapper's triggers 6-14 read fields (`contract.py:277-356`) and the interactive pre path assembles the same fields by prose, not code; `SKILL.md:923-940` (the §9.3 consumer map) does not list the wrapper or the headless builder at all. Grep inventory at plan time (counts, not proof of completeness): `merge_method|adversarial_convergence_score|convergence_score` appears in `cli/reflect/contract.py` (3), `cli/reflect/ensemble.py` (22), `contracts/__init__.py` (1), `tests/cli/reflect/*` (fixtures: 25 files; `test_ensemble_unit.py` 23, `test_ensemble_stub_integration.py` 16, `test_verdict_mapping.py` 5), `task-builder` SKILL.md (4, EV-4 at `:2242`), reflect `SKILL.md` (25), `refs/ops-integration.md:239`; roadmap files match the same words for the roadmap pipeline's own merge (different contract).
465	
466	**Contract compatibility gate (PROPOSED, a hard stage-entry criterion for Stages 2, 3, 4 and 5; the Stage 2 entry needs items 1-3, its exit adds item 4).**
467	
468	1. **Inventory.** Re-run a repository-wide grep for `merge_method`, `adversarial_convergence_score`, `convergence_score`, `contract_version`, `t2_model_class_diversity`, `t2_vendor_diversity`, `calibrator_diversity`, `reviewer_cards`, `citations_dropped` over `src/`, `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/` and the installed skill and command primitives. **Producers:** the interactive skill prose (`SKILL.md` §9.1 and Wave 5, plus `refs/report-template.md`, UNVERIFIED), the headless builder (`ensemble.py:787-832`). **Validators:** `contract.py` (`derive_verdict`, `contract.py:138`; `_degraded_reason`, `:263`). **Consumers:** the §9.3 map plus `task-builder` EV-4, the PromQL label list, the meta-eval aggregator, the sprint executor (UNVERIFIED code). The result is stored as `.dev/` evidence and attached to the stage's exit record.
469	2. **Per-field source table** for the five fields whose producer changes in panel mode (the diversity trio, `calibrator_diversity`, `reviewer_cards`): each is computed by the same rule as the legacy path from the resolved classes; for the parity template in anthropic-only the expected values equal the legacy values (sonnet, haiku, opus: three distinct classes, vendor `single`, calibrator `degraded`).
470	3. **Contract lint test** (PROPOSED `tests/cli/reflect/test_panel_contract_lint.py`; the reflect tests already live in that directory): feeds a panel-run contract and its output directory to a checker that asserts: `contract_version == "1.8.0"`; every top-level key is in the 1.8.0 stable field list or in the telemetry block; `merge_method` in `{adversarial, single-reviewer-fallback}`; `adversarial_convergence_score` is a float or null; `adversarial_unavailable`, `regression_present` and the other `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`) are real booleans; EV-1 holds on disk (`merged-verdict.yaml`, cards count); the five fields above equal the legacy values on the matched fixture.
471	4. **Verdict replay.** Feed every recorded 1.8.0 pre contract and the Stage 2 shadow contracts through `derive_verdict` (`contract.py:138`) offline and diff the verdicts between legacy and shadow outputs; any new degraded reason is a stage-exit failure. (The wrapper is post-only in production; this replay is a test, not a runtime path.)
472	5. **Bump rule check:** the lint fails if a panel run emits a stable key outside the list or a legal value outside EV-2; that is the machine form of "no change".
473	
474	## Cost model
475	
476	<!-- Source: Variant 3 (haiku:backend), Cost model - merged per Change #4; Base (original, modified) - 49k-96k estimate demoted to a footnote -->
477	Three separated bases, never summed. All token figures are estimates and are labelled with their unit.
478	
479	1. **Published profile (claude-orchestration tokens, turn-budget unit).** T1 3k-8k plus 2k-5k auggie; T2 35k-70k plus 10k-25k auggie; hard kill about 65k (`cost-profile.yaml:36-39,46-51,70`; "1 turn ≈ 1k claude tokens", turn midpoint 52, 52 x 1.25 = 65, or 65.6k from the 52.5k arithmetic midpoint; `SKILL.md:269-270`: N >= 65 means no constraint). The panel does not change `cost_profile_version`.
480	2. **Output-token planning estimate for a T2 run reaching T2 (3 reviewers), lane by lane** (V3's table, adopted as the planning basis, in k output tokens):
481	
482	   | Lane | Legacy | Panel-parity, debate kept (legacy lanes plus the findings block) |
483	   |---|---|---|
484	   | primary (T1 card, coverage map, briefs, REPORT) | 10-16 | 10-16 |
485	   | parallel (3 reviewer cards) | 21-30 | 22-31 |
486	   | calibrator (3 per-card re-grades, 1k-2k each) | 3-6 | 3-6 |
487	   | debate (`/sc:adversarial --compare`) | 6-10 | 6-10 |
488	   | validator | 2-4 | 2-4 |
489	   | **total** | **42-66** (`10+21+3+6+2` to `16+30+6+10+4`) | **43-67** (`10+22+3+6+2` to `16+31+6+10+4`; 43.5-67.5 before rounding) |
490	
491	   Midpoint 54k to about 55.5k: parity costs about 1.5k more, not less. The earlier lane-table saving (37k-56k, about 14%) came from an assumed shorter-card effect that this design does not contain and no data supports; it is kept only as the unproven arm-C hypothesis that the first measurement may test (H-C reports it, does not require it). <!-- fix B1 -->
492	3. **Recorded artifact sizes (bytes/4)** 55k-93k (221,405-371,507 bytes) are a sanity bracket only; they include copied input and are not provider usage.
493	
494	V1's earlier 49k-96k legacy estimate is kept as a footnote: its high end exceeds both the profile's 70k band top and the 65k kill line, so it is not used for any threshold. PN1 figures (408k loop, 23k + 3 x 68k-108k first review, `LEDGER-RESULTS.md:19,66`) stay a comparison only: the default 4-slot panel in anthropic-only with spec-panel-style verbosity would cost about 227k-347k for the parallel lane alone (23 + 204 to 23 + 324), 4-7x the whole current T2 run (reflect briefs are persona-scoped, so reflect cards should be shorter, UNVERIFIED for Haiku stand-ins).
495	
496	Deterministic-merge variant (deferred candidate E'): corrected parity total 43-67 minus the debate lane 6-10 = 33k-61k, not production behavior. <!-- fix B1 item 4, M7 -->
497	
498	**Rule:** panel T2 must stay inside the existing 35k-70k profile band and below the 65k kill line at p95 (a measurement criterion, see First measurement). **Post (Stage 5):** the debate is kept, so the cost is about the same as legacy (+1.5k for blocks, +0 for K4). The value is maintenance and an honest headless `citations_dropped`, not tokens.
499	
500	**When a full panel (more than 3 slots) is not worth calling:** (1) always in anthropic-only: extra slots are more Haiku copies, they add no model class and leave vendor diversity single; (2) always in pre-execution: advisory, no revise step; (3) when the rubric would stop at T1 anyway (`SKILL.md:362-366`, rule D1): the kernel is never called. The only candidate case is gateway post-execution with extra *vendors*, unmeasured and left for Stage 5 data; raising the cap needs the gate in Q7.
501	
502	## Risks
503	
504	<!-- Source: Base (original, modified) - list replaced by a table per Change #21 -->
505	Probability is an estimate with its basis stated; impact is the consequence; mitigation names the design element.
506	
507	| # | Risk | Prob. | Impact | Mitigation |
508	|---|---|---|---|---|
509	| 1 | The debate matters and clustering cannot replace it | n/a (debate kept) | Medium | kept; E' needs its own measurement and a major version |
510	| 2 | Panel-fed T2 is worse than legacy T2 | Medium: reviewer classes match (parity) but format, brief line and dispatch plumbing differ | High | Stage 2 shadow, first measurement NI test, legacy default |
511	| 3 | Executor exclusion fails open or empties the anchor | Medium: `panel.py:402-409` silent paths are real | High | kernel hard exclusion, per-slot skip, post-resolve assertion, tests (K1 contract) |
512	| 4 | Reviewer identity not what was requested | Low-Medium: the tool pins `model`, but omitting it runs Sonnet (`reflect-reviewer.md:6`) | High | explicit `model` check, probe spike S-ID |
513	| 5 | Format non-compliance (invalid findings block) | Medium for Haiku-class reviewers (card format varies today) | Medium | one bounded re-ask; legacy card body still reaches the debate; compliance rate in telemetry |
514	| 6 | Consumer or test relies on a 1.8.0 value that shifts | Low (grep shows no `contract_version == 1.8.0` check, no grader match) | High | lint test, consumer grep gate, parity |
515	| 7 | Multi-file clustering merges unrelated findings | Low (path-aware, conservative) / split risk Medium | Low: telemetry only | `cluster_v2`, 50-pair hand label at Stage 0 |
516	| 8 | Opus creep | Low: no new use | Medium | the Opus-use list; Fable and Tier 0 rejected in the kernel (`launch` whitelist) |
517	| 9 | Two engines drift again | Medium | Medium | one resolution file, one contract-lint, one builder function for post at Stage 5 |
518	| 10 | Pre T2 exceeds the 65k kill | Medium at the legacy high end | Medium | p95 criterion, cap of 3 reviewers |
519	| 11 | Interactive and wrapper disagree on a 2-of-3 run | High (exists today: `SKILL.md:666` calls it MALFORMED, `ensemble.py:765-770` records benign `reviewer-shortfall`) | Low-Medium | preserved, counted at Stage 2 |
520	| 12 | Gateway cell silently routed through an unsupported path | Low | High | refusal rule (Agent-session adapter, rule D4) |
521	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:546-606

```markdown
546	## Open items
547	
548	<!-- Source: Base (original, modified) - new section merged per Change #38 -->
549	- **O-1** (C-002, C-014; V3 holds its verdict/completion policy should be the base and prefers resolution-only first): resolved as V1 skeleton plus V3 policy; Stage 3 is the first stage that changes reviewers and it is effectively resolution-plus-format-only, so V3's concern is met without a separate stage; V3 dissent recorded.
550	- **O-2** (C-005, exact key versus primary-citation proximity): `cluster_v2` is telemetry only, so under-merging is cheap; revisit if clusters ever become authoritative.
551	- **O-3** (C-007): post debate input; the cluster map is not fed to the post debate in the first shipment (see Post-execution adapter, step 7).
552	- **O-4** gateway dispatch for pre and post and gateway templates (X-010, A-002): undefined; refused.
553	- **O-5** path-aware ledger (`ledger/2`) if a ledger is ever used.
554	- **O-6** unknown executor is the default in the workflow path (see K1 contract item 7): consider having `sc-workflow` Wave 4 pass `--executor-model` when known (a sc-workflow change, out of scope here).
555	- **O-7** A-003 conversion gate (at least 90% unambiguous conversion).
556	- **O-8** the cheaper lever may be the rubric: 34 of 38 recorded pre decisions escalated because of the parsed-sparse pre-filter, not plan risk; decide after H-A.
557	- **O-9** `_diversity.py:15` returns `insufficient` while `SKILL.md:790` allows only `full | degraded` (pre-existing vocabulary mismatch).
558	- **O-10** X-003 (contract-version facts): resolved as a text correction (see Return-contract mapping), no residual.
559	- **O-11** `--depth quick --tier 2` precedence and whether pins override the budget downgrade are not stated in the rows I read (UNVERIFIED).
560	
561	## Assumptions and UNVERIFIED items
562	
563	<!-- Source: Base (original, modified) - verified items moved and bullets replaced per Change #22, #36 -->
564	**Assumptions (from the seed brief):** A-1 (design, measure first is acceptable), A-2 (shared model = one schema, one dispatch, one merge layer), A-3 (pre cites plan and spec, post cites source; the quote-anchor part is decided: `quote` is optional), A-4 (calibrated confidence stays per finding/card, embedded in the card), A-5 (output tokens only; the profile unit is named wherever it is used), A-6 (no owner decision needed).
565	
566	**Assumptions added here:**
567	
568	- **A-8:** sc-workflow invokes reflect inside an agent session, so pre uses the agent-session engine (enrichment: skills/sc-workflow-protocol/SKILL.md:60-64).
569	- **A-9:** persona-scoped reflect cards stay far shorter than spec-panel reports. This drives the "full panel not worth it" estimate only as a lower bound.
570	- **A-10:** Haiku-stand-in runs certify mechanics and anthropic-only behavior, not gateway quality. Stage 3 and later run only where every resolved model has a non-null `launch` alias; a gateway default needs its own run of the first measurement (not planned; O-4).
571	
572	**VERIFIED (moved from UNVERIFIED, with cites):**
573	
574	- (a) `superclaude review panel resolve` options are `--template`, `--tiers`, `--env`, `--run-id`, `--kind first|re-review`, `--seed`, `--sequence` (`panel_cmd.py:18-52`); `--exclude-class` and `--strict-distinct` do not exist (PROPOSED).
575	- (b) `validate_panel` rejects unknown slot keys (`panel.py:109-111`, `_SLOT_KEYS = {slot_id, tier, count, strategy, seed}` at `panel.py:46`), so exclusion cannot be a template key and must be a resolve-time parameter.
576	- (c) `_decision` with `--cap 1` records `ESCALATE` on every blocking round (`ledger.py:93-96`).
577	- (d) No `contract_version == "1.8.0"` equality in `src/`.
578	- (e) The CI grader has no `merge_method` match.
579	- (f) The wrapper and headless builder are post-only (previously an assumption, A-7; verified at `ensemble.py:797`; other callers were not read).
580	- (g) `refs/reviewer-spec.md:31-74,55,94-98,112-116` and `cost-profile.yaml` cites were re-read and are correct.
581	
582	**UNVERIFIED (kept):**
583	
584	- the `sc-adversarial` judge-exclusion input, and which return-contract field carries the judge identity;
585	- how `sc-adversarial` scores a skipped debate (`SKILL.md:409,951,439,457` says skip when variants differ by under 10% and score is "null if debate not reached");
586	- whether the Agent-tool reply carries a model id;
587	- the body of `cli/reflect/fallback.py` and the `review-telemetry/1` schema (`cli/review/telemetry.py`);
588	- the sprint executor code, and `refs/report-template.md`;
589	- whether the `reflect-reviewer` tools allowlist survives a `model` override (part of spike S-ID);
590	- the `judge_class_collision: true` record and the July `proxy_error` record (enrichment snippets only);
591	- `docs/reference/review-panel-live7.md:19-26` and the `REPORT.md:130-132` stoprule facts (taken from enrichment or V2, not re-read);
592	- every per-lane token split in the Cost model is an estimate; only the totals' bracket is checked against recorded artifact sizes.
593	
594	**PROPOSED names introduced** (none exist today):
595	
596	- templates: `review-panel.reflect-pre.json`, `reflect-pre-x2`, `reflect-post`, `reflect-post-x2`, `reflect-enterprise`, `reflect-lite`;
597	- K1: `classes` in the tier file, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, `skipped_slots`, `excluded` (additive resolution keys), CLI `--hard-exclude-class` and `--strict-distinct`;
598	- K3: `findings-v2` and its fields (`citations`, `deviation_class`, `coverage_rows`, `self_confidence`, `lens`, `channel`, `reflect_category`);
599	- K4: `superclaude review cluster`, `cluster_v2`, `cluster_agreement`; `superclaude review verify-citations`;
600	- artifacts: `panel/manifest.json`, `panel/resolution.json`, `panel/clusters.json`, `panel/precheck.json`;
601	- the reflect flag `--t2-engine legacy|shadow|panel`;
602	- telemetry: `t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`, `identity_source`, `identity_mismatch_suspected`, `judge_class_collision`, `debate_skipped_similar`, `t2_floor_unmet`;
603	- the swarm lens input `--panel-resolution` (Stage 5);
604	- the test `test_panel_contract_lint.py`;
605	- contract: none.
606	
```

## Coverage slice

| Plan task | Plan line | Depends on | Spec span it answers |
|---|---|---|---|
| Task 12: Add `superclaude review cluster` | 151 | Task 3, Task 11 | K4 + cluster_agreement 344-348 |
| Task 13: Add `superclaude review verify-citations` | 162 | Task 1, Task 12 | Evidence gate and citation pre-check 349-357 |
| Task 14: Run the identity spike S-ID and record the result | 173 | Task 11 | Executor-exclusion gates 242-259 (S-ID); UNVERIFIED 587-589 |
| Task 15: Add the panel contract lint and its per-field source table | 186 | Task 6 | Contract gate items 2,3,5 469-472 |
| Task 16: Add the verdict replay and refresh the inventory | 196 | Task 6, Task 15 | Contract gate item 4 471 |
| Task 17: Add the panel manifest module and CLI | 208 | Task 11 | Execution contract 360-366 |
| Task 18: Add `--t2-engine` and the engine-decision rules to the reflect skill | 218 | Task 14, Task 16, Task 17 | When panel called D1-D5 120-123, table 126-140 |
| Task 19: Write the shadow-mode steps, brief line and telemetry into the reflect skill | 229 | Task 12, Task 13, Task 18 | Pre-execution adapter 367-386; Shadow mode |
| Task 20: Add the Stage 2 shadow-exit aggregator | 243 | Task 16, Task 19 | Staged migration Stage 2 exit 410 |
