# Round 2.5 invariant probe (raw fault-finder output), slot C-07 dispatch-and-launch-mechanism

Fault-finder: independent, not an advocate. Consensus probed: the gated hybrid (H-gated per A, V2-bound per B), ship-now set S1-S6.
Code state: HEAD 50d4d2b9d on `ironbelly/shadow-runs`. Read-only. Tags used inside EVIDENCE: [READ] = file:line read this round; [RAN] = in-memory run of the repo's own `panel.py` (`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src uv run --no-project python`, deep copy of the packaged tiers, nothing written; the explicit environment "ws" is B's S5 example: available = opus, sonnet, gpt-6.1-sol; stand_ins tier4 and tier2 = gpt-6.1-sol; launch one word per model); [RESULTS] = `jq` over `.dev/eval-workspaces/shadow-model-combos/results.jsonl` (15 rows). Nothing was run against a gateway model id.

## Findings

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: A class-word binding written as data (S5 `launch` map, `note`) stays true for the whole run, because the binding it describes (`ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`) is set once before the session starts and the map is a static file. The consensus treats a mismatch as something the recorder finds after the fact (A-002), not something checked before dispatch.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The binding is a tier alias, not a model: `docs/reference/model-aliases.md:26-38` (haiku = `claude-gw-tier2`; outside a tier workspace the launcher sets none of the three). The combo runs used five different bindings, and the pin disagreed with what was served in 11 of 15 runs (`identity_mismatch_suspected: true` for A-r1, A-r2, B-r1..r3, D-r1..r3, E-r1..r3) [RESULTS]; word `haiku` was served `gpt-6.1-sol` in A and B, `claude-haiku-5-5` in C and D, `gpt-6-luna` in E. A `launch` map is model-to-one-word (`panel.py:364-368`), so a session that binds two words to one model (comboE: opus and haiku both to `gpt-6-luna`) cannot be written down at all. Nothing in S1-S6 compares the binding to the file before the first Agent call; the S3 reader only records. `SKILL.md:348` (step 9) shows the record stays "requested-pinned" until a transcript read exists.

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: S5/S6 can keep the explicit tier file correct as the packaged tiers and templates evolve; B adds "one reference file of this shape ... as a test fixture under tests/review/".
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: A tier file given by path replaces the packaged one whole (`panel.py:470-482`; `panel_cmd.py:26-32` "whole-file replacement"). A fixture or workspace file is therefore a copy of `aliases`, `classes`, `names` and the `anthropic-only` environment. S6 run on a static copy tests the copy's aliases, not the packaged ones, so it cannot catch a packaged tier reorder or new model. Only a fixture built at test time by overlaying the new environment on `pnl.load_tiers()` (what the probe in this round did) stays in step. Neither advocate says which.

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: Either form of S5 is safe to ship: A's override through `find_path` (`$SUPERCLAUDE_REVIEW_TIERS`, `<project>/.superclaude/review-tiers.json`, `~/.superclaude/review-tiers.json`) or B's `panel resolve --tiers <file> --env <name>`. The consensus lists both as S5 without choosing.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Shadow step 1 passes no `--tiers` and `--env anthropic-only` literally (`SKILL.md:340`), and `reflect_shadow_exit.py:205-207` calls `pnl.load_tiers()` with no path. Both reach `find_path` (`panel.py:397-419`). A project or user file therefore silently replaces the packaged tiers for every shadow resolve and for the exit script: a file that lacks an `anthropic-only` environment makes `resolve` raise "unknown environment" (`panel.py:583-587`) and every shadow run falls back to legacy with `panel_fallback_reason`; a file that carries a copy changes `tiers_sha256` (`panel.py:694`) and every earlier run becomes "not proven" (`reflect_shadow_exit.py:128-132`). B's `--tiers` form does not have this effect (NB4/NB5), but the consensus text keeps A's form open. No override file exists in this checkout or in `~` today (`ls` of both paths: absent), so the failure would be introduced by the first workspace that follows S5 as A states it.

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: S1's clause "`launch: null` is a dispatch error, not a fallback" is consistent with the packaged rules and reachable.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `SKILL.md:320` (D4) says a null `launch` runs the legacy rotation and records `panel_fallback_reason`: that is a fallback, the opposite word. For any `reflect-*` template a null `launch` never reaches dispatch, because `_check_reflect_resolution` raises at resolve (`panel.py:153-156`, called at `panel.py:682-687`). The S1 clause can fire only for a generic template (`review-panel.default.json`, `live7`), where nothing validates `launch` at all. So the clause is dead for the only consumer and contradicts D4 for the others; precedence between "dispatch error" and "D4 fallback" is not stated.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: S1's precondition (every reviewer Agent call carries a `model` word) and the replay prediction "flags A-r3 and no other" cover the omission the combo run showed.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Reviewer rows have a null requested word only in A-r3 [RESULTS], so the prediction holds if the detector reads reviewer rows only. But the calibrator Agent calls carry a null word in six runs, not one: A-r3 (3 of 3), B-r3 (4 of 4), C-r1 and C-r2 (1 of 4 each), E-r1 and E-r2 (4 of 4) [RESULTS: `calibrator_requested_served`]. S1 as worded ("every core reviewer ... the `launch` word from `panel resolve`") does not govern calibrators, which are not in the resolution at all. A replay that reads every Agent row would flag six runs and falsify the prediction; a replay scoped to reviewers leaves calibrator collapse (every calibrator served `claude-sonnet-5-5` in B-r3 and `claude-haiku-5-5` in E-r1/E-r2) with no guard.

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: S4 (brief tells a `reflect-reviewer` to run a shell command and write a file; pass if no Bash/Edit/Write call in the sidechain transcript and `git status` unchanged) produces dynamic evidence that tool enforcement, not model compliance, keeps the reviewer read-only.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `reflect-reviewer.md:38,59` tell the agent it has no write/Bash tool and that a brief must not instruct it to run anything; a model can decline in prose and the transcript then has no Bash call, so the test passes without showing the tool is absent. A discriminating pass needs either the subagent's effective tool list or an observed denied attempt; A put the tool list into G2 for `claude-p` (init event) but S4 on the Agent path has no such source (a sidechain transcript has no init event; unverified). `git status unchanged` proves nothing if the requested file path is outside the tree. The static test only reads the agent file (`test_reviewer_readonly_tools.py:25,69-103`). Also, `permissionMode: plan` (`reflect-reviewer.md:8`) means a Write attempt could be blocked by mode rather than by the allowlist, so a pass cannot be attributed to the allowlist.

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: The gated `claude-p` reviewer, launched with `--restricted --tools Read,Grep,Glob --strict-mcp-config --mcp-config <grounding>`, can do the same audit as an agent-file reviewer; G2's pass criteria (no Bash/Edit/Write, `git status` unchanged, tool list has the grounding tools) establish that.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `claude --help` (2.1.325) for `--restricted`: "confines the file tools to the working directories (--add-dir included)" and ignores user/project/local settings [READ via `claude --help`, lines 195-208]. A reviewer reads `spec_path`, `tasklist_path` and the diff from absolute paths and is grounded in a snapshot root (`reflect-reviewer.md:50-58`); a path outside the child's cwd/`--add-dir` is unreadable, so a child can satisfy every G2 criterion and still be unable to read its inputs. `--tools` lists built-in tools only (help lines 255-259), so the six MCP tools of `reflect-reviewer.md:5` depend on `--mcp-config` plus an allow rule that the ignored settings files normally carry (A's N5, unrun). G2 has no "reads spec_path and diff inputs and produces a valid findings block" criterion, so a different (tool-starved) reviewer could pass the gate and enter a panel as a model-diversity data point.

ID: INV-008
CATEGORY: guard_conditions
ASSUMPTION: A second `adapters` map per environment (Variant 1's additive key) can ship without touching the validator.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `validate_tiers` rejects any environment key outside `available, stand_ins, launch, note` (`panel.py:371-373`) and `load_tiers` raises on any error (`panel.py:477-481`). Both advocates dropped the key in Round 2 (r2A N1, r2B 3(b)); the consensus keeps one `launch` vocabulary. Handled.

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: Three reviewers on three class words (the cap equals the word count, A-004) is a workable panel for the contract that follows: blind calibration with a class disjoint from the reviewer classes.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `SKILL.md:1248`: `calibrator_model_class ∈ {opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewer_model_classes`. With reviewers on all of sonnet, haiku, opus the disjoint set is empty for the Agent-reachable words (Fable is excluded, `panel.py:76-77`). In the combo results `calibrator_diversity` is "degraded" in 14 of 15 runs; the only "full" is A-r3, the run where every word was null, so no reviewer class existed to collide with [RESULTS]. So the contract's "full" value is a by-product of the collapse, and S1-S6 neither change how that field is computed nor give the calibrator a word outside the three. The cap/word-count coincidence that makes B's reach claim work is the same coincidence that makes the disjoint-calibrator rule unsatisfiable.

ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: S6 holds: under the explicit environment every packaged `reflect-*` template resolves, passes `_check_reflect_resolution`, prints pairwise distinct words under strict distinctness, and prints the same panel for any run id.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: [RAN] over 300 run ids with the "ws" environment: `reflect-pre`, `reflect-post` and `reflect-enterprise` give one panel (sonnet/`sonnet`, gpt-6.1-sol/`haiku`, opus/`opus`). `reflect-pre-x2` and `reflect-post-x2` give two panels (163 and 137 of 300: gpt-6.1-sol with sonnet, or with opus), because slot `t1a` is `random` over {opus, sonnet}; the "same panel for any run id" property is false for the x2 templates (both panels are valid, but the property as written would fail). `reflect-lite` prints gpt-6.1-sol with word `haiku` twice under soft distinctness and a 2-reviewer panel under `--strict-distinct`. The shadow step uses `--strict-distinct --hard-exclude-class <executor>` (`SKILL.md:340`); with that, [RAN] `reflect-pre` gives 3 reviewers only for executor class `haiku` and 2 for opus, sonnet and gpt, and `reflect-pre-x2` with executor class `gpt` raises `ExclusionExhausted` on the fixed anchor. The floor is N=2 (`SKILL.md:319`, D3), so there is no slack, and S6 as written tests none of the exclusion paths.

ID: INV-011
CATEGORY: count_divergence
ASSUMPTION: S3's reader emits one row per reviewer (so `model_observed` can be joined to a resolved reviewer, and "distinct served" can be counted).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: comboE-r1 has seven `reviewer_requested_served` rows for a three-reviewer panel; E-r2 and E-r3 have three [RESULTS]. Those are attempts, not reviewers, and `reviewer_distinct_served` (2) is computed across them. The reader's key is not stated (reviewer id, attempt id). C-03's quorum is `min(2, requested)` over `complete` reports (C-03 result, point 4), and independence is "requested, not served" until `model_observed` exists (point 5); a per-attempt row set joined naively to reviewers double-counts. The shadow manifest already has `--reviewer-id` and `--attempt-id` (`SKILL.md:342`), so the key exists but S3 does not say it uses it.

ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: A launch word is always available when the dispatcher needs one for a reviewer other than the primary pick (a retry or fallback).
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `resolve` prints `fallbacks` as model ids only (`panel.py:555`, `:678`) and `launch` for the primary only (`panel.py:679`). `_check_reflect_resolution` validates `launch` for the primary and class/Fable status for the fallbacks, not a word for each fallback (`panel.py:147-156`). `validate_tiers` does not require `launch` keys to be a subset of, or to cover, `available` (`panel.py:364-368`); an environment with `available: "all"` and a three-entry `launch` (the shape of the packaged `gateway` if filled) has fallbacks with no word. Under S1 a retry onto such a model is a dispatch error. Low today because B says nothing in the core acts on fallbacks and the ws example has `launch` keys equal to `available`; S6 should assert `set(launch) == set(available)` for the fixture, to make it a rule rather than a property of one example.

ID: INV-013
CATEGORY: collection_boundaries
ASSUMPTION: A packaged class-word fill of `gateway.launch` is correct for the packaged random slots.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Both advocates withdrew the packaged fill: `reflect-pre` slot `t4` picks among three models by seed and the session binds three words to tier aliases (r2A N3, r2B section 0 item 1; `panel.py:545`, `review-tiers.default.json:10`). Consistent with [RAN]: under the ws environment `t4` is the stand-in and the panel is constant. `gateway.launch` stays `{}` (S2) and `tiers_sha256` is unchanged. Handled.

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: Executor-class exclusion (anti-self-confirmation) still works when words are bound to non-Claude models by S5.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The executor class comes from `--executor-model <class>`, `EXECUTOR_MODEL_CLASS` or a log heuristic (SKILL.md section 7.1, "Executor-class exclusion rule"), and `--hard-exclude-class` expands through the tier file's `classes`, which is keyed by model id (`panel_cmd.py:82-92`). In a binding where `haiku` is `gpt-6.1-sol`, an executor that ran as the `haiku` alias has class `gpt` in the tier file, not `haiku`. [RAN] with the ws environment, `reflect-pre`, executor class `haiku`: nothing is excluded and the panel contains (gpt-6.1-sol, word `haiku`), i.e. the executor's own served model reviews its own work. The same word-versus-class gap exists in the legacy rotation (all combos); S5 gives it a second, data-defined place to occur and S1-S6 add no check.

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: S1 (the resolved `launch` word is the Agent `model` argument) and the shadow fence (shadow changes no verdict, INV-L) can both hold.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Shadow step 3: "Dispatch is the legacy dispatch" and the legacy briefs are unchanged (`SKILL.md:338,342`); card `model:` is the resolution pin, never what ran (`SKILL.md:341`). The reviewers that actually launch in shadow come from the legacy rotation (`SKILL.md:655-656`), and the resolution used for the pin comes from `--env anthropic-only`. If S1 is applied to shadow dispatch, the launched models become the anthropic-only words instead of the legacy rotation and shadow stops being shadow (and `panel_parity` is trivially true). If S1 is applied only where the effective engine is `panel`, that engine "ships in Stage 3" (`SKILL.md:319`) and S1 has no consumer today. Either reading fits the text; the consensus does not say which.

ID: INV-016
CATEGORY: interaction_effects
ASSUMPTION: After G1-G3, widening `_REFLECT_LAUNCH` by one value (`claude-p`) is "the reviewed edit" that keeps INV-G; and S5's workspace files stay within what G2 proved.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `_check_reflect_resolution` tests membership of the value (`panel.py:153-156`), not the model it applies to. Once `claude-p` is in `_REFLECT_LAUNCH`, any tier file S5 allows (`find_path` or `--tiers`) may map any model id to `claude-p` and pass the reflect check; G2 ran one gateway id plus `sonnet`. The static read-only pin (`test_reviewer_readonly_tools.py:25`) reads only `src/superclaude/agents/reflect-reviewer.md`; a `claude-p` reviewer's tool surface lives in launcher argv, which has no static test, and `ClaudeProcess` reviewer_profile passes no allowlist (`process.py:145-154`). The interaction of S5 (data anywhere) with the one-value ceiling widening is not covered; the safe form needs a per-model gate or a static test on the launcher's argv builder.

ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: The ship-now set S1-S6 closes the collapse failure of run A-r3 (all three reviewers and all calibrators served `claude-sonnet-5-5` because the orchestrator passed no class).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Enumeration of what lies between the S1 fix site and the observed failure. (a) Dispatch path: in shadow the dispatch is legacy (`SKILL.md:342`) and A-r3 is a run of the shadow-model-combos experiment (`FINDINGS.md:9`); S1 is a rule about the `launch` word printed by `panel resolve`, so it does not govern the legacy Wave 3B Task spawn or the calibrator spawns unless the legacy dispatch text is edited too (INV-005, INV-015). (b) Calibrators: null requested word in six of 15 runs [RESULTS]; no S item covers them. (c) Mechanism: A-r3's cause was an omitted optional argument; the Agent tool's schema in this session says an omitted `model` falls back to the agent definition's model, which is `model: sonnet` (`reflect-reviewer.md:6`), exactly what was served. S1 restates a rule in prose; the only mechanical guard is S7 (a PreToolUse check), which is "not built", its payload is unverified, and the hook would see presence only, not the resolved set, because it holds no run state (`launch-level-guard.sh:182-205` reads `tool_input.isolation` only). (d) The replay detector reads recorded runs after the votes, so it detects and does not prevent. (e) The contract field that mislabelled A-r3 ("full" diversity) is unchanged (INV-009). Falsifiers: any future run whose orchestrator drops `model` on a legacy-path or calibrator spawn; a replay that reads calibrator rows. What the set does close: detection of a reviewer-row omission after the fact, if the S3 reader is built, plus a written rule.

ID: INV-018
CATEGORY: sufficiency_challenge
ASSUMPTION: The ship-now set closes the `--env gateway` refusal (C-S6): a gateway workspace can get a class-word panel.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The packaged `gateway` environment is unchanged by design (`review-tiers.default.json:25-30`, `launch: {}`), so `--env gateway` still raises "launch None is not one of sonnet, opus, haiku" for any reflect template (`panel.py:153-156`). It is the default environment whenever `T3Model01` is set (`select_env`, `panel.py:485-494`; it is set in this very workspace, value `glm-5.3`), and D4 still routes "gateway" to legacy (`SKILL.md:320`). S5 offers an opt-in alternative environment, but no S item makes any caller pass `--tiers <file> --env <name>`: shadow step 1 hardcodes `--env anthropic-only` (`SKILL.md:340`) and the Stage 3 edit that would call it has no owner (A-005 in the diff analysis). Net effect in a gateway workspace: no behavior change, and shadow pins remain wrong by construction (INV-001: 11 of 15 mismatch). Falsifier: any caller of `panel resolve` without an explicit `--env` in a gateway workspace.

ID: INV-019
CATEGORY: sufficiency_challenge
ASSUMPTION: S3 (one transcript reader fed first by the Agent sidechain transcript via SubagentStop `agent_transcript_path`) supplies `model_observed` for gateway-served subagents, which is what C-03's independence claim and S1's replay both consume.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Named as unresolved (spike: one reviewer, check `message.model` in the sidechain transcript). Repo state: the only `SubagentStop` hook is the freshness counter (`src/superclaude/hooks/hooks.json:179-190`, async); `model_observed` exists only as a SQL column (`telemetry.py:364,378`); the contract already carries `identity_source: observed | requested-pinned` (`SKILL.md:974`, step 9 at `:348`). Downstream conditions that would falsify the dependence: transcript absent or not flushed when the hook fires, or `message.model` holding the tier alias (the usage table is keyed `claude-gw-tier3[1m]` etc. [RESULTS]) rather than the served model, in which case `model_observed` stays "requested-pinned" and C-03's "requested, not served" (C-03 result, point 5) stays. The consensus has the spike but no stated fallback if it fails; the existing orchestrator self-report path (`SKILL.md:341,348`) is the implied one.

## Summary

- Total findings: 19. ADDRESSED: 3 (INV-008 LOW, INV-013 MEDIUM, INV-019 MEDIUM). UNADDRESSED: 16.
- UNADDRESSED by severity: HIGH 1 (INV-017), MEDIUM 12 (INV-001, 003, 005, 006, 007, 009, 010, 011, 014, 015, 016, 018), LOW 3 (INV-002, 004, 012).
- By category: state_variables 3, guard_conditions 5, count_divergence 3, collection_boundaries 2, interaction_effects 3, sufficiency_challenge 3.
