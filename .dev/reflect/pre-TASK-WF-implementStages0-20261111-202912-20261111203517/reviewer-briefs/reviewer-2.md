# Reviewer 2 brief (qa)

## T1 card excerpt

# Tier 1 reflection card (UC-1 pre-execution)

- Plan: .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md
- Spec (real, pointed to by source.md): .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md sha256 54a8dce2...c4e45
- Prior T1 pass by the plan author (unvalidated, not independent): .dev/reflect/pre-TASK-WF-implementStages0-20261111-202912-20261111203500/REPORT.md
- coverage_degraded: parsed-sparse (source.md carries no labelled requirement ids; spec has none either, headings are the only structure)

## Coverage matrix (spec heading span -> plan task)

| Spec span (merged-requirements.md) | Plan task(s) | Status |
|---|---|---|
| Finding format 291-357 | 1, 2, 3, 12, 13 | covered |
| Q4 Engine, K1 contract, templates, forbidden models 187-264 | 8, 9, 10, 11 | covered |
| When the panel is called D1-D5 117-143 | 18 | covered |
| Adapter sketches: Execution contract, Pre adapter, Shadow 358-386 | 17, 19 | covered |
| Staged migration 401-415 (Stages 0-2 exit rows) | 1-20 (exit tooling 5, 20; exit facts 14, 16) | covered, exits need human data |
| Return-contract mapping 416-456 | constraint (1.8.0 unchanged), 15 | covered by constraint only |
| Contract compatibility gate 461-473 | 6, 15, 16 | covered |
| First measurement 522-545 | 4, 7 | covered (design only) |
| Cost model 474-501 | none | unmapped (check if any Stage 0-2 requirement) |
| Risks 502-521 | none | unmapped (check if any Stage 0-2 requirement) |
| Open items 546-560, UNVERIFIED 582-593 | 14 (S-ID only) | partial |



## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-11T20:36:38Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md:1-251

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
31	
32	## Task 1: Add the findings-v2 schema and parser
33	
34	Create `src/superclaude/cli/review/findings_v2.py` and `tests/review/test_review_findings_v2.py`. Read `src/superclaude/cli/review/findings.py` (v1 parser `parse_block`, `_check_finding`, id and severity rules at lines 90-196) and follow its container rules. Implement the "Finding format" table of the source: a JSON-lines fenced block with info string `findings-v2` under `## Findings block`; fields `id`, `severity`, `blocking`, `category` (v1 six-value enum unchanged), `reflect_category`, `claim`, `refs`, `anchor`/`anchor2` (required only when `citations` is absent), `citations` (1..8 of `{role, path, line_start, line_end, quote?}` with role in plan, spec, source, test, diff, artifact), `deviation_class` (required when `lens` is `reflect-post`), `coverage_rows`, `self_confidence` (0-1), `lens` (spec, reflect-pre, reflect-post), `channel` (defect, grounding-gap, advisory; default defect). Apply the category and severity mapping paragraph (ordering to other, acceptance to unpassable-check, coverage to missing-requirement, contradiction to contradiction, risk to safety or other, deviation to other with deviation_class). Reject a line that sets `calibrated_confidence`. Expose completion states `complete`, `truncated`, `invalid`, `failed`, `timed_out`, where a valid empty array counts as `complete` only when the card also carries coverage observations for every assigned row.
35	
36	Acceptance criteria:
37	- Every valid v1 block in the existing tests also parses as v2 with the same findings.
38	- Tests cover: finding with neither `anchor` nor `citations` is invalid; MINOR cannot block; duplicate ids rejected; `calibrated_confidence` rejected; `deviation_class` required for `reflect-post`; empty valid array without coverage observations is `invalid`, with them is `complete`; `quote` optional and, when present, 12-200 chars.
39	- `uv run pytest tests/review -q` passes, including the untouched v1 tests.
40	
41	## Task 2: Add the recorded-card converter
42	
43	Depends on: Task 1
44	
45	Create `src/superclaude/cli/review/card_convert.py` and `tests/review/test_review_card_convert.py`. Convert a recorded reflect reviewer card (YAML findings with `severity: blocking|minor`, categories ordering, acceptance, deviation, coverage, risk, and `evidence` line refs, as in "What a recorded card looks like") to findings-v2 using the deterministic, quote-free rule: `plan:N` becomes a `plan` citation on the card's plan path, lines N-N; `source.md:N` or `spec:N` becomes a `spec` citation on the card's spec path; `path:A-B` becomes a `source` citation; unresolvable refs become `unresolved` citations and are counted. Return the converted findings plus per-card counts (converted unambiguously, unresolved). Use real cards from `.dev/reflect/pre-*/reviewer-cards/` (copy two or three small ones to `tests/review/fixtures/reflect_cards/`).
46	
47	Acceptance criteria:
48	- A fixture card with refs `plan:57`, `source.md:62`, `src/x.py:451-462` converts to three citations with the roles and paths above and no quote.
49	- A ref that cannot be resolved is kept as an `unresolved` citation and counted, never dropped.
50	- Tests assert the unambiguous-conversion share is reported per card and in total.
51	
52	## Task 3: Implement cluster_v2 (path-aware, with the chained guard)
53	
54	Depends on: Task 1
55	
56	Create `src/superclaude/cli/review/cluster.py` and `tests/review/test_review_cluster.py`. Implement the pure function `cluster_v2(findings_v2_blocks, snapshot_file_list) -> clusters` exactly as "Multi-file identity (K4 cluster_v2)": citation tuple `(role, path, line_start, line_end)` verified against the snapshot file list (a path not in the list is `unresolved` and never joins a cluster by span); primary citation rule; `same_defect_v2` (deviation classes compatible, `refs_norm` sets intersect or both empty using the normalization of `findings.py:321-337`, and some citation of each on the same path with spans within 3 lines; equal `sha256("v2|"+role+"|"+path+"|"+section+"|"+refs+"|"+class)` fingerprints with non-empty refs also match); union-find components with `chained: true` for any cluster holding two members that do not match pairwise. Implement `cluster_agreement` and the `disputed` flag per "`cluster_agreement` and clustering semantics": support from calibrated confidences joined from `calibration.per_finding[id].finding_confidence`, representative claim from the highest-confidence member (ties by resolution order), `chained` clusters excluded from agreement counts and listed, and a second pass `clusters_kept` over findings the evidence validator kept. Do not import or alter `findings.cluster`.
57	
58	Acceptance criteria:
59	- Tests (positive and negative): two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines with equal refs cluster; a chain A-B-C with A and C unequal is `chained`; an unresolved path never clusters by span.
60	- A test proves `review merge` output on v1 reports is byte-identical with and without importing the new module.
61	- `cluster_agreement` is 1.0 when there are no blocking clusters and at least 2 valid blocks; the field is named `cluster_agreement` everywhere and `panel_agreement_score` appears nowhere.
62	
63	## Task 4: Build the Stage 0a replay on the recorded cards
64	
65	Depends on: Task 2, Task 3
66	
67	Create `scripts/reflect_stage0a_replay.py` (run with `uv run python scripts/reflect_stage0a_replay.py`). It reads the 42 recorded `reviewer-cards/` directories under `.dev/reflect/pre-*` (33 have `adversarial/merged-verdict.yaml`), converts them with `card_convert`, runs `cluster_v2`, and writes `./artifacts/stage0a-report.md` containing: cluster counts, agreement with the recorded merged verdict, the share of findings that convert with an unambiguous `(path, line)` against the 90% gate (O-7), and a classification of the 7 recorded null convergence scores by cause (skipped-similar debate, single-reviewer-fallback, illegal merge_method value, other), read from each run's `adversarial/` log and `return-contract.yaml`. It dispatches no model.
68	
69	Acceptance criteria:
70	- `./artifacts/stage0a-report.md` exists with the conversion share stated as a number and a PASS or FAIL against 90%.
71	- The report lists each of the 7 null-score runs with its cause, or states for which the cause could not be determined and why.
72	- If the share is below 90%, the report says the findings-v2 parser change must not ship and the plan stops at this task for owner review.
73	
74	## Task 5: Produce the 50-pair cluster check sheet and its scorer
75	
76	Depends on: Task 3
77	
78	Create `scripts/reflect_cluster_pairs.py` and `tests/review/test_reflect_cluster_pairs.py`. The script samples 50 finding pairs from the converted recorded cards (25 that `cluster_v2` merges, 25 it keeps apart, drawn with a fixed seed, mixing same-file and cross-file pairs), writes `./artifacts/cluster-pairs-50.csv` with blank `human_same_defect` column, and has a `score` mode that reads the filled sheet and reports precision, recall and the confusion counts of `cluster_v2` against the labels.
79	
80	Acceptance criteria:
81	- `./artifacts/cluster-pairs-50.csv` exists with exactly 50 rows, each carrying both claims, both citations and the `cluster_v2` verdict; the label column is empty for the owner.
82	- A unit test fills a synthetic sheet and checks the score output; scoring an unfilled sheet fails with a message naming the missing labels.
83	
84	## Task 6: Add the consumer inventory script and store the first result
85	
86	Create `scripts/reflect_consumer_inventory.py` and `./artifacts/consumer-inventory.md`. The script greps `merge_method`, `adversarial_convergence_score`, `convergence_score`, `contract_version`, `t2_model_class_diversity`, `t2_vendor_diversity`, `calibrator_diversity`, `reviewer_cards`, `citations_dropped` over `src/`, `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/` and the installed skill and command primitives under `src/superclaude/{skills,commands}`, classifies each hit as producer, validator or consumer (producers: reflect `SKILL.md` section 9.1 and Wave 5, `refs/report-template.md`, `cli/reflect/ensemble.py`; validators: `cli/reflect/contract.py`; consumers: the section 9.3 map, `task-builder` EV-4, `refs/ops-integration.md`, the meta-eval aggregator, the sprint executor), and writes a markdown table with counts per file. It must be rerunnable with `--out <file>`.
87	
88	Acceptance criteria:
89	- `./artifacts/consumer-inventory.md` lists every hit file with its role and counts, and flags files that match the words for an unrelated pipeline (roadmap) as not in scope.
90	- The report states that no `contract_version == "1.8.0"` equality exists in `src/` and that `.dev/eval-workspaces/sc-reflect/grader.py` has no match, or states the contradicting hit with its path.
91	- Running the script twice on an unchanged tree yields identical output.
92	
93	## Task 7: Design and cost the first-measurement pilot
94	
95	Depends on: Task 4
96	
97	Write `./artifacts/pilot-design.md` from "First measurement": hypotheses H-A, H-B, H-C and the safety list; arms A (T1 pin), B (legacy T2), C (panel-parity T2), D (lite, 6 plans); ground truth (scripted seeded defects of the five kinds plus the union ledger with a blinded grader); the pilot of 12 plan+spec pairs x 5 seeded defects with 6 repeats of arm B to estimate d0; the sample-size formulas (n = 618 x d for margin 0.10, n = 275 x d for margin 0.15, times 1.3) with the worked numbers; the strata and the 25% non-sparse quota; the cost per plan and for the pilot in the profile's claude-token unit (arms A+B+C = 73k-148k per plan, pilot 0.9M-1.8M), with retrieval tokens listed separately; the stop rule; the statement that the pilot estimates d and does not decide H-B; and the "inconclusive is not a pass" rule. Use the Stage 0a numbers from Task 4 where they replace estimates.
98	
99	Acceptance criteria:
100	- The document states every threshold once and the arithmetic reproduces the cost figures above.
101	- It names the owner approval needed before the confirmatory run and marks the pilot as a pilot.
102	- Stage 0 exit checklist at the end lists the five exit items (50-pair check, conversion share, consumer inventory stored, pilot designed and costed) with the artifact that answers each.
103	
104	## Phase 2: Stage 1a, kernel resolution extensions (dormant)
105	
106	## Task 8: Add hard exclusion and strict distinctness to panel resolution
107	
108	Depends on: Task 7
109	
110	Edit `src/superclaude/cli/review/panel.py` per "K1 hard exclusion contract" items 1-4. Add keyword-only `hard_exclude: Sequence[str] = ()` and `strict_distinct: bool = False` to `resolve_slot` (line 380) and `resolve` (line 427); filter the candidate list before the strategy runs for every strategy including `fixed`, derive fallbacks from the filtered list, and skip the silent `or candidates` re-admission when `hard` is non-empty. When the filtered list is empty try stand-ins filtered the same way, else raise new `ExclusionExhausted(tier)` (subclass of `NoModelAvailable`). In `resolve`, a non-fixed slot that raises `ExclusionExhausted` is skipped and recorded; the fixed anchor raising is fatal. Add additive keys `skipped_slots: [{slot_id, reason}]` and `excluded: {models, classes}` to the `review-panel-resolution/1` JSON only when exclusion arguments are used. Do not add template keys (`_SLOT_KEYS` stays). Create `tests/review/test_review_panel_exclusion.py`.
111	
112	Acceptance criteria:
113	- With `hard_exclude == ()` and `strict_distinct == False` the resolution output and hashes are byte-identical to today for the packaged default and live7 templates (asserted by a test that compares against a stored golden).
114	- Tests: excluded model is the fixed anchor; random and round_robin pools that empty do not re-admit the excluded model; a stand-in is used only after filtering; `ExclusionExhausted` is raised when nothing remains.
115	- `uv run pytest tests/review -q` passes.
116	
117	## Task 9: Add the class map, Fable and Tier 0 rejection and the reviewer cap
118	
119	Depends on: Task 8
120	
121	Edit `src/superclaude/cli/review/data/review-tiers.default.json` to add a `classes` object mapping every model id to a class string (`claude-opus-5-5` to opus, `claude-sonnet-5-5` to sonnet, `claude-haiku-5-5` to haiku, and vendor families gpt, glm, grok, qwen, muse for the gateway models) and let `validate_tiers` in `panel.py` accept it. Add a reflect-profile validator in `panel.py` applied to every template whose name starts with `reflect-` and to every resolution made from one: reject a model id with no `classes` entry; reject any resolved id matching `claude-fable-*`; reject a slot on `tier0` or whose alias list holds a Tier 0 model; reject a `launch` value outside `{sonnet, opus, haiku}`; reject more than 3 reviewers; reject `round_robin` slots unless a recorded `--sequence` is supplied. Generic panels keep their 1..8 range.
122	
123	Acceptance criteria:
124	- Tests in `tests/review/test_review_panel_exclusion.py` (or a new `test_review_panel_reflect_profile.py`) cover each rejection above, and show a generic non-reflect panel with 4 reviewers is still valid.
125	- An unmapped model id makes a `reflect-*` template invalid and leaves non-reflect templates valid.
126	- The existing tier-file tests still pass without edits.
127	
128	## Task 10: Add the CLI flags to `review panel resolve`
129	
130	Depends on: Task 8, Task 9
131	
132	Edit `src/superclaude/cli/review/panel_cmd.py` (`resolve_cmd`, options at lines 18-52) to add `--hard-exclude-class <class>` (repeatable; expands through `classes`, compares case-insensitively with the executor class) and `--strict-distinct`. Wire them to `hard_exclude` and `strict_distinct`, write `skipped_slots` and `excluded` into the JSON, and exit non-zero with the exception name on `ExclusionExhausted`. Extend `tests/review/test_review_cli.py`.
133	
134	Acceptance criteria:
135	- `superclaude review panel resolve --template @reflect-pre --run-id r1 --kind first --env anthropic-only --hard-exclude-class sonnet --strict-distinct` exits non-zero naming `ExclusionExhausted` for tier1b once Task 11 lands; without the new flags the existing CLI tests pass unchanged.
136	- An unknown class name is a usage error that lists the known classes.
137	
138	## Task 11: Ship the reflect panel templates
139	
140	Depends on: Task 10
141	
142	Create in `src/superclaude/cli/review/data/`: `review-panel.reflect-pre.json` (the JSON in "Template set": slots t1b fixed on tier1b, t4 random on tier4, t1a random on tier1a, distinct_across_slots true, apply_to first), `review-panel.reflect-pre-x2.json` (fixed t4 anchor plus random t1a), `review-panel.reflect-enterprise.json` (same slots as reflect-pre), `review-panel.reflect-lite.json` (t1b, t4, t2), `review-panel.reflect-post.json` and `review-panel.reflect-post-x2.json` (mirror pre). Confirm tier ids exist in `review-tiers.default.json` and that each file passes `validate_panel` and the Task 9 reflect profile. Create `tests/review/test_review_reflect_templates.py` covering the Task 8 scenarios from "K1 hard exclusion contract" item 8.
143	
144	Acceptance criteria:
145	- `@reflect-pre` resolves in anthropic-only to sonnet, haiku, opus with three distinct classes; `@reflect-pre-x2` resolves to haiku and opus.
146	- Executor sonnet raises `ExclusionExhausted` for tier1b and the adapter-style fallback to `@reflect-pre-x2` yields 2 reviewers; executor haiku skips the t4 slot; executor opus with strict distinctness yields sonnet and haiku with no duplicate.
147	- No template names Fable, tier0 or a gateway model; `uv run pytest tests/review -q` passes.
148	
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

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:1-19

```markdown
1	---
2	title: "Replacing /sc:reflect Tier 2 with the shared review panel: a layered kernel design"
3	generated: 2026-11-11T19:58:00Z
4	base: variant-1-opus-architect
5	checkout_sha: ec259f1b718ccdb9f08bba0237bfa47b2b7601a2
6	method: adversarial Mode B merge
7	status: draft-for-owner-review
8	adversarial_convergence: 0.882
9	adversarial_status: partial   # score is above the 0.75 threshold, but the invariant gate blocked (5 HIGH unaddressed at Round 2.5, no Round 3 at standard depth); the merge plan resolves all 20, no second probe was run
10	independent_check: "verification/merged-output-check.md: FAIL on 1 blocking finding (cost contradiction) and 11 minor; all 12 fixed afterwards; the fixes were confirmed by grep only, not by a second independent review"
11	---
12	
13	<!-- Provenance: produced by /sc:adversarial (Mode B). Base: Variant 1 (opus:architect). Incorporated from: Variant 2 (sonnet:analyzer), Variant 3 (haiku:backend). Plan: refactor-plan.md (46 changes). Merge date: 2026-11-11. Cross-references of the form "Change N" in the plan text were converted to section names so the document is self-contained; "Change #n" inside these HTML provenance comments refers to the numbered changes of refactor-plan.md (external to this document). -->
14	
15	# Replacing /sc:reflect Tier 2 with the shared review panel: a layered kernel design
16	
17	<!-- Source: Variant 2 (sonnet:analyzer), opening paragraph - merged per Change #13; Base (original, modified) - keeps the "(enrichment)" marker -->
18	Paths are relative to `src/superclaude/` unless they start with `.dev/`. `path:line` cites are lines read in the drafting or verification sessions; "(enrichment)" marks a line taken from the enrichment file; "(plan-verified)" marks a line the refactor plan re-read. PROPOSED = a new name, not an existing file, flag, function or schema. UNVERIFIED = not read. Token figures are estimates unless a source is cited; units are named. Installed primitives are named by installed path (`~/.claude/...`) or the `superclaude` CLI, never by `src/superclaude/...` (CLAUDE.md rule); a `src/superclaude/` or `cli/...` path in this document is a citation of package code that was read, never an instruction for an installed primitive. `<out>` abbreviates the reflect output directory. Ids such as INV-nnn, S-/C-/X-/U-/A-nnn and O-n are labels from this adversarial run's invariant-probe.md and diff-analysis.md (external to this document), except O-n, which are defined in "Open items".
19	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:20-28

```markdown
20	## Summary
21	
22	<!-- Source: Base (original, modified) - rewritten per Change #40, #6, #18 -->
23	Chosen architecture: **C, the Layered Review Kernel with reflect adapters and a retained adversarial finalizer.** The kernel generalizes panel resolution, dispatch adapters, findings-v2 and deterministic clustering; reflect keeps briefs, blind calibration, the evidence gate, the rubric, the debate and the contract builder. Contract 1.8.0 is unchanged in Stages 0-4. Pre-execution first, behind `--t2-engine` (default `legacy`).
24	
25	The `/sc:adversarial` debate stays in both pre- and post-execution. K4 clustering runs as deterministic preparation and telemetry (`cluster_agreement`); it is not the merge. Removing the pre debate is a later, versioned experiment (candidate E') that needs its own measurement and a major contract version.
26	
27	Headline reason: one reviewer-identity layer and one finding format can serve two commands without weakening any reflect grounding mechanism. The first measurement decides whether the panel-fed T2 holds quality, and whether T2 beats T1 at all.
28	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:29-99

```markdown
29	## Candidate architectures
30	
31	### A. Leave reflect as is
32	
33	<!-- Source: Base (original, modified) - cost figure restated per Change #4, #20 -->
34	- **Changes:** nothing.
35	- **Keeps:** everything. That includes the hard-coded rotation table (refs/reviewer-spec.md:94-98), the debate (SKILL.md:633-651) and the two engines with diverging contract builders (cli/reflect/ensemble.py:787-832 emits `verification_ran: False` and `citations_dropped: 0` as constants).
36	- **Cost:** about 42k-66k output tokens per pre-execution T2 run (planning estimate, see Cost model). The earlier 49k-96k estimate is a footnote there only.
37	- **Risk:** low runtime risk, but maintenance risk rises. Two reviewer-pool definitions now exist (reflect's rotation and the panel's tier files, cli/review/data/review-tiers.default.json:4-11), and they will drift. Reviewer identity in the headless path comes from `T2Model0N` env vars (cli/swarm/lenses/reflect_review.py:14, cli/swarm/config.py:59) rather than a recorded, hashed resolution.
38	- **Verdict:** a valid fallback, the control arm of the first measurement, and the right answer if that measurement fails. It does not meet the owner's "one shared review model" goal.
39	
40	### B. Full replacement: reflect T2 becomes a spec-panel review loop
41	
42	<!-- Source: Base (original) -->
43	- **Changes:** reflect calls the panel end to end: `superclaude review panel resolve`, reviewers, `superclaude review merge` with ledger rounds (cap 3) and the reviser contract. The debate, the per-card calibrator and reflect's own merge are deleted. Ledger `confidence` single/overlap replaces calibrated confidence.
44	- **Keeps:** T1, the rubric, the evidence-validator.
45	- **Cost:** the spec-panel loop measured about 408k loop output tokens (.dev/research/346-review-loop-experiments/p17/LEDGER-RESULTS.md:19). Reflect has no revise step, so only the round-1 part applies. The default 4-reviewer panel with Haiku stand-ins writing 68k-108k each (LEDGER-RESULTS.md:66) is roughly 23k + 3 x 88k ≈ 290k for round 1 alone (midpoint arithmetic).
46	- **Risk:** high.
47	  - It drops blind calibration (SKILL.md:1172-1192) with no replacement of equal strength. Ledger confidence counts reviewers; it does not re-grade them blind.
48	  - The panel's measured gain comes from the ledger driving a revise loop on specs. Reflect never edits the plan (SKILL.md:342, "Findings never edit the tasklist"), so the mechanism that produced the gain is absent.
49	  - It breaks `merge_method` legal values (SKILL.md:789) and gate condition 9 (SKILL.md:1483).
50	- **Verdict:** rejected. It is the most expensive option, the gain does not transfer, and it violates the calibration constraint. <!-- fix M1 -->
51	
52	### C. Layered Review Kernel with reflect adapters and a retained debate (chosen)
53	
54	<!-- Source: Base (original, modified) - debate kept, contract unchanged, cost restated per Change #6, #20, #40 -->
55	- **Changes:** the panel code is generalized into four layers, each with a schema id:
56	  - **K1 Resolution:** `review-panel-resolution/1` plus PROPOSED hard exclusion, per-model `classes` and additive `skipped_slots` / `excluded` keys.
57	  - **K2 Dispatch adapters:** agent-session (pre) and swarm (post only), both reading K1.
58	  - **K3 Findings:** PROPOSED `findings-v2`, a superset of findings-v1 with typed multi-file citations, deviation class, coverage rows, completion states and `channel`.
59	  - **K4 Clustering:** deterministic `cluster_v2` as telemetry (`cluster_agreement`); it is not the merge.
60	
61	  Reflect adds two adapters, pre and post, that sit on K1-K4 and keep briefs, per-card blind calibration, the `/sc:adversarial` debate, the evidence gate, the rubric and the contract builder.
62	- **Keeps:** every reflect grounding mechanism, the 1.8.0 contract and its field names and legal values, and the post-execution contract semantics.
63	- **Cost:** 43k-67k output-token planning estimate with the debate kept (legacy plus about 1.5k, see Cost model), inside the profile's 35k-70k band. A possible 37k-56k if cards turn out shorter is a hypothesis. Parity with legacy, no saving claimed. <!-- fix B1 item 3 -->
64	- **Risk:** medium. Multi-file clustering and the hard-exclusion kernel change are new code; both are default-off or telemetry-only.
65	- **Verdict:** chosen.
66	
67	### D. Panel as dispatcher only (thin adoption)
68	
69	<!-- Source: Base (original) -->
70	- **Changes:** reflect replaces only its rotation table with `superclaude review panel resolve`. Everything after dispatch is unchanged (cards, calibration, debate, validator).
71	- **Keeps:** everything else.
72	- **Cost:** the same as A.
73	- **Risk:** low.
74	- **Verdict:** this is Stages 1-3 of C, not a destination. It unifies reviewer identity but leaves two finding formats. That is the main maintenance cost the owner asked to remove.
75	
76	### E'. Deterministic pre merge with a major contract version (deferred)
77	
78	<!-- Source: Base (original, modified) - former candidate E "debate-always hybrid" re-cast as the deferred deterministic-merge candidate per Change #6, #15, #40; Variant 3, Cost model - merged per Change #4 -->
79	- **Changes:** as C, but in pre-execution the debate is removed and K4 clusters are the authoritative merge (disputes debated only on request). The `merge_method` legal set gains the value `panel` (pre only).
80	- **Keeps:** the post debate.
81	- **Cost:** 33k-61k output-token planning estimate (corrected parity total 43k-67k minus the debate lane 6k-10k). Not production behavior. <!-- fix B1 item 4 -->
82	- **Risk:** high. It is a major contract version (2.0.0), and the wrapper blocks any major other than 1 (see Return-contract mapping). Every consumer in the deferred list must change first.
83	- **Verdict:** deferred and not scheduled. It needs its own T1-armed measurement showing the debate adds nothing, plus the consumer list in "Deferred versioned change". C is its rollback position.
84	
85	### Comparison
86	
87	<!-- Source: Base (original, modified) - matrix rows restated per Change #40, #20 -->
88	| | A as-is | B full loop | C kernel (chosen) | D dispatcher only | E' deterministic pre (deferred) |
89	|---|---|---|---|---|---|
90	| One reviewer-identity layer | no | yes | yes | yes | yes |
91	| One finding format | no | yes (lossy) | yes (findings-v2) | no | yes |
92	| Blind calibration kept | yes | **no** | yes | yes | yes |
93	| Evidence gate kept | yes | yes | yes, strengthened (flags) | yes | yes |
94	| Debate | always | never | always (pre and post) | always | pre on disputes only |
95	| Contract change | none | major | none (1.8.0) | none | major (2.0.0, deferred) |
96	| Pre T2 output tokens (planning est.) | 42k-66k | about 290k+ | 43k-67k (legacy plus about 1.5k; a possible 37k-56k if cards turn out shorter is a hypothesis) | 42k-66k | 33k-61k |
97	| Transfers the measured panel gain | no claim | no (no revise step) | no claim | no claim | no claim |
98	| Maintenance surface | 2 pools, 2 formats, 2 merges | 1 | 1 kernel + thin adapters | 1 pool, 2 formats | 1 kernel |
99	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:100-116

```markdown
100	## Chosen architecture and reasons
101	
102	<!-- Source: Base (original, modified) - reasons 2, 3 edited and reason 6 added per Change #10, #41, #17, #31 -->
103	**C, the Layered Review Kernel.** Reasons, in order of weight:
104	
105	1. **The maintenance unit is the layer, not the command.** Today, reviewer identity lives in three places: the reflect rotation table (SKILL.md:604-608), the `T2Model0N` env pool (reflect_review lens), and the panel tier file (review-tiers.default.json:4-11). Finding shape lives in two places: reviewer card YAML and findings-v1 (findings.py:90-121). Merge lives in two places: `/sc:adversarial` and `merge_round` (ledger.py:107-298). C reduces identity and finding shape to one implementation each, with a schema id. Commands differ only in policy: brief, required finding fields, gates and contract.
106	2. **No grounding mechanism is weakened.**
107	   - Calibration (SKILL.md:1172-1192) stays per card, embedded in the card as today.
108	   - The evidence-validator stays mandatory (SKILL.md:587). It gains a deterministic citation pre-check that only flags citations for re-read.
109	   - Executor-class exclusion (SKILL.md:600-610) becomes a hard K1 input instead of reflect-side table editing.
110	
111	   Evidence that the gates carry load (recorded stoprule card, `reviewer-1-card.yaml`, plan-verified): findings are YAML with `severity: blocking|minor`, categories `ordering|acceptance|deviation|coverage|risk`, `evidence: [plan:57, source.md:62, src/...:451-462]` (line refs, no quotes), an orchestrator-written `model_class: sonnet`, `persona`, and `plan:`/`spec:` paths; the calibrator scored F1-F3 at 0.60, 0.50, 0.55 ("fit major better than blocking"); the final gate dropped `source.md:143` (a heading) which a "quote locates" check would pass (per V2, `REPORT.md:130-132`, not re-read by the plan). Consequence for the design: a deterministic locate check cannot replace the semantic re-read (see "Evidence gate and citation pre-check"), and the recorded card gives line references, so findings-v2 `citations[]` are built from `path:line` refs with `quote` optional (see Finding format).
112	3. **The debate is kept.** EV-2 forbids a self-built merge, the debate's value is unmeasured and not shown idle (recorded pre contracts show convergence below 1.0 in 14 of 35 numeric cases, see Return-contract mapping), and the post debate feeds promotion and rollback. Pre-execution reflect is advisory: sc-workflow records only `reflect_status` and `reflect_report_path` and never changes the workflow status (skills/sc-workflow-protocol/SKILL.md:60-64, enrichment). Post-execution feeds promotion condition 9 (SKILL.md:1483) and the wrapper's degraded triggers 9-11b (cli/reflect/contract.py:290-326).
113	4. **Extension scaffolding at low cost.** A third consumer (for example `/sc:auggie-review` or `/tdd`) would add a template, a brief and a contract mapping, and nothing else. No new merge code and no new reviewer pool.
114	5. **It does not claim the PN1 gain.** The spec-panel gain (15.7 vs 2.8 fixed defects, LEDGER-RESULTS.md:19) was measured with a revise loop on specs. C adopts the panel for maintainability, not for a quality uplift. Quality is checked by the first measurement as non-inferiority.
115	6. **The first shipment changes no contract and no reviewer class.** It is parity plus a format and dispatch layer, so the measurement can attribute any difference.
116	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:117-143

```markdown
117	## When the panel is called (depth x tier path)
118	
119	<!-- Source: Base (original, modified) - new section merged per Change #39 (coordinator requirement); Base mentions of --depth reconciled -->
120	The panel is a Tier-2 mechanism. It is called only after the **final** tier is 2. Order of decisions, unchanged from `SKILL.md`: (1) Wave 0 alias routing (`:231-239`: 1 alias -> T1 only; 2 aliases -> 2 reviewers; 3+ -> 3) and executor class (`:600-602`); (2) budget pre-flight (`:262-273`); (3) Waves 1-2: T1 card, coverage map, blind calibration of the T1 card, rubric (`:354-402`); (4) **only now** the T2 engine flag `--t2-engine` is read, at the start of Wave 3. The effective engine and the requested engine are both written to `tier_decision.yaml` and the manifest.
121	
122	**Rules.** D1: a `--depth quick`, `--tier 1`, `--no-escalate` or rubric-stopped T1 run **never** calls the panel and never reads `--t2-engine`. D2: the staged-migration flag is checked after the depth, pin, budget and rubric decisions, never before. D3: a run pinned to T2 (`--depth deep` or `--tier 2`) whose panel yields fewer than 2 distinct eligible classes does **not** silently run T1 or one reviewer: it emits the `SKILL.md:600` WARN and `executor_exclusion_degraded: true` (if exclusion caused it), `t2_floor_unmet` in `degraded_components` (a benign token, not in `contract.py:31-33`), forces `status: partial`, and REPORT.md opens with a banner naming the unmet floor; a rubric-driven escalation keeps the existing silent-safe T1 degrade of `SKILL.md:600` with the WARN. N=2 is the minimum in every case (`SKILL.md:610`; `reviewer-spec.md:102`). D4: unsupported cells (gateway, null `launch`, unmapped model) run the legacy rotation and record `panel_fallback_reason`. D5: `N_eff = min(--reviewers, alias count, 3)` (`SKILL.md:86`, clamp rule by depth is unstated in the rows I read and stays UNVERIFIED), anchor never dropped.
123	
124	Reflect's `--depth` is Tier-1-only / Tier-1-then-rubric / force-Tier-2 (`SKILL.md:84`). The flag `--depth standard` that appears in the debate command (`SKILL.md:648`) belongs to `sc-adversarial`, a different flag. `--depth deep` never means "more reviewers" and never means "debate only on disputes".
125	
126	| Depth / pin / modifier | Tier path | Panel called? | Template and reviewers | Stages that run | Expected cost (profile unit; planning) | Notes |
127	|---|---|---|---|---|---|---|
128	| `--depth quick` | T1 only (`:364`) | No | none | Waves 0-2 including the T1 card's blind calibration; no Wave 3-4 | 3k-8k claude + 2k-5k auggie (`cost-profile.yaml:36-39`) | `--t2-engine` ignored |
129	| `--tier 1`, `--no-escalate` | T1 (`:362,366`) | No | none | as above | as above | `--no-escalate` warns if C < 0.85 |
130	| `--depth standard` (default implied by `--tier auto`, `:84-85`; UNVERIFIED as a stated default), rubric stops | T1 | No | none | as above | as above | recorded: 0 of 38 |
131	| `--depth standard`, rubric escalates (rows 3-7, parsed-sparse pre-filter) | T1 work then T2 | Yes if engine is `panel` or `shadow` | `@reflect-pre`, 3 reviewers (2 if 2 aliases); `@reflect-enterprise` if `--strategy enterprise` | Wave 3 resolve + dispatch; per-card blind calibration; Wave 4 `sc-adversarial` debate on cards (not a deterministic merge); Wave 5 synthesis; evidence-validator; K4 clustering and pre-check as telemetry | planning 43k-67k output (legacy 42k-66k); profile band 35k-70k claude + 10k-25k auggie (`:46-51`) | the typical `/sc:workflow` plan: recorded 37 of 38 |
132	| `--depth deep` | forced T2 (`:365`) | Yes | same templates and count; no extra reviewers | as above plus the deep-only behavior of `--remediate` (task-builder route, `:89`) and optional tech-research in Wave 1B (`:637`) | as T2; deep extras unmeasured (no deep row in the profile) | D3 applies; 2 of 38 recorded |
133	| `--tier 2` | forced T2 (`:363`) | Yes | same | as T2 | as T2 | D3 applies |
134	| `--budget-remaining N`, N < 5 | STOP (`:267`) | No | none | none | none | |
135	| N = 5 | T1 forced (`:268`) | No | none | T1 | T1 | `budget_forced_tier_downgrade: true` |
136	| 6 <= N < 65 | T2 downgraded to T1 with WARN when the rubric asks for T2 (`:269`) | No | none | T1 | T1 | band 52 <= N < 65 has no row label in the table I read (UNVERIFIED how implemented); safe default: treat as downgrade |
137	| N >= 65 or unset | as the rubric directs (`:270-271`) | per rows above | per rows above | per rows above | the panel's p95 must stay <= 65k (`cost-profile.yaml:70`; 52 x 1.25) | panel adds no budget logic |
138	| executor class collides with the pool | N=2 floor then T1 degrade (`:600`) | only if >= 2 distinct eligible classes remain | `@reflect-pre-x2` etc. (see "K1 hard exclusion contract") | as T2, or T1 | as T2, or T1 | D3 for pins |
139	| `--unattended` | unchanged | per rows above | per rows above | per rows above | unchanged | |
140	| headless `superclaude reflect` | post only (`ensemble.py:797`) | Stage 5 only | `@reflect-post` | existing ensemble, swarm lens | post planning unchanged | pre is never headless |
141	
142	**What a default-depth `/sc:workflow` run triggers.** Wave 4 of `sc-workflow` invokes `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with defaults for every other flag (`sc-workflow-protocol/SKILL.md:60`): depth standard, tier auto, no `--reviewers`, no `--budget-remaining` (budget check skipped), executor class unknown. So it runs T1 first, then the rubric, which in the recorded history escalated to T2 in 37 of 38 pre runs (34 by the parsed-sparse pre-filter because workflow sources carry no labelled requirement ids, others by rule 4, 5 or 6). Recorded evidence: of 38 recorded pre tier decisions under `.dev/reflect/pre-*/artifacts/tier_decision.yaml`, 37 selected tier 2 and 1 selected tier 1 (a `--tier 1` user pin); 34 carry `coverage_degraded: parsed-sparse`; 21 are sc-workflow packages; 2 were forced by `--depth deep`; 0 stopped at T1 on the rubric. The cause is the table-wide pre-filter of `SKILL.md:400`: when `coverage_degraded` is set no STOP row may fire; sc-workflow plan sources carry no labelled requirement ids ("inferred 10 > parsed 0"), and rule 4 (`S_domains >= 3`) and rule 6 (`C < 0.85`) also fire in the recorded reasons. With the engine at `panel`, every such run calls the panel; with the default `legacy` it never does. This is why the T2 cost, not the T1 cost, is the typical per-plan cost, and why the rubric's parsed-sparse behavior (O-8) deserves its own look after H-A. These figures are counts over one repository's `.dev/reflect/` history.
143	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:144-290

```markdown
144	## Answers to Q1-Q7
145	
146	### Q1. What the panel takes over, what it lacks, what stays in reflect
147	
148	<!-- Source: Base (original, modified) - rows restated per Change #42, #5, #24 -->
149	**Direct answer:** the panel takes over the reviewer pool, model diversity, deterministic resolution, the dispatch description and telemetry. It lacks hard executor exclusion, personas, blind calibration, an evidence gate, multi-file citations, deviation class and coverage rows. All reflect-specific judgement stays in reflect, including the merge, which remains the `/sc:adversarial` debate.
150	
151	| Function | Today in reflect | Panel today | Owner in C |
152	|---|---|---|---|
153	| Reviewer pool, model rotation | rotation table (SKILL.md:604-608) | tier aliases + templates (review-tiers.default.json:4-11; review-panel.default.json:8-12) | **kernel K1** (reflect templates, PROPOSED) |
154	| Deterministic, recorded choice | none (agent-session) / env pool (swarm) | seeded by run id, template and tier hashes recorded (panel.py:455-459, 514-525) | **K1** |
155	| Model diversity | `_diversity.py` full/degraded (enrichment) | `distinct_across_slots`, soft (panel.py:405, 408 fall back to the full candidate list) | K1 computes it; reflect keeps `t2_*_diversity` emission |
156	| Executor-class exclusion | hard rule, N=2 floor (SKILL.md:600-610) | **lacks**: `exclude` is soft and ignored by `fixed` slots (panel.py:402-403) | **kernel hard exclusion** (see "K1 hard exclusion contract"); reflect supplies the class and the policy |
157	| Personas | analyzer/qa/refactorer via brief (refs/reviewer-spec.md:94-98) | **lacks** | **reflect**: persona by resolution ordinal (no kernel change) |
158	| Parallel dispatch | Agent tool `reflect-reviewer` / swarm lens | `launch` alias map (review-tiers.default.json:29), no dispatcher | **K2 adapters** read K1 |
159	| Blind calibration | `confidence-calibrator` per card (embedded block), disjoint class (SKILL.md:1172-1192) | **lacks** | **reflect** |
160	| Merge | `/sc:adversarial --compare` (SKILL.md:645-651) | `merge_round` cluster + ledger (ledger.py:107-298) | **`/sc:adversarial` stays the merge**; K4 clustering as telemetry |
161	| Evidence gate | evidence-validator, mandatory (SKILL.md:587) | **lacks** | **reflect**, with a deterministic flagging pre-check |
162	| Telemetry | §9.2 block (SKILL.md:892-921) | `review-telemetry/1` (enrichment: names only) | both: reflect §9.2 stays; K1/K4 append panel records |
163	| Grounding, coverage map, deviation taxonomy, rubric, remediation, promotion | reflect | n/a | **reflect** (constraint) |
164	
165	### Q2. A finding format for both
166	
167	<!-- Source: Base (original, modified) - calibration no longer carried in the block per Change #5, #42 -->
168	**Direct answer:** findings-v2 (PROPOSED), a strict superset of findings-v1. `anchor` becomes optional when `citations[]` is present. Typed fields are added for deviation class, coverage rows, self-reported confidence, completion state and channel. Calibration is not carried in the block: it stays in the card's embedded `calibration:` block. Reflect's reviewer card keeps its prose. The machine part of the card *is* the findings-v2 block. Schema and dedupe key are in the Finding format section.
169	
170	### Q3. Merge: debate, deterministic, or both
171	
172	<!-- Source: Variant 2 (sonnet:analyzer), Q3 and Stage 5; Variant 3 (haiku:backend), Q3 - merged per Change #6; Base (original, modified) -->
173	**Direct answer:** the debate stays in both modes. K4 clustering runs as deterministic preparation and telemetry; it is not the merge. Removing the pre debate is a later, versioned experiment (candidate E') that needs its own T1-armed measurement and a major contract version. EV-2 forbids a self-built merge (`SKILL.md:789`), so keeping the debate is the only legal choice today.
174	
175	What the debate provides that clustering cannot, and why it is kept:
176	
177	- **Pre-execution.**
178	  1. Arbitration when reviewers disagree on whether a plan gap is blocking. A deterministic merge takes the OR of blocking and the max severity (ledger.py:187-190), so disagreement turns into "blocking, single support". It is not resolved.
179	  2. The narrative synthesis of a merged verdict (the `merged-verdict.yaml` that EV-1 checks, `SKILL.md:666`).
180	  3. A real numeric convergence score, `adversarial_convergence_score`. No substitute score is introduced.
181	- **Post-execution.** Arbitration of deviation *class* (Necessary vs Drift vs Regression) drives `deviation_count_by_class`, `regression_present`, TurnLedger rollback (SKILL.md:930), promotion condition 4 (SKILL.md:1472) and the wrapper's halted triggers (contract.py:369-381). A deterministic merge cannot decide between two classes; it can only take the worst. That would over-report Regression and block promotions that should pass.
182	
183	The cards (calibrated, with embedded calibration) are the debate's inputs exactly as `SKILL.md:645-651`. The K4 cluster map is telemetry only until a measurement shows it helps; it is not an input to the debate.
184	
185	**Judge identity.** Reflect does not pin a judge (`SKILL.md:612`; `reviewer-spec.md:112-116` says sc-adversarial owns judge selection and reflect only delegates disjointness). After the debate returns, the adapter records `judge_identity` (as reported by `sc-adversarial-protocol` in its return contract, UNVERIFIED which field) and sets `judge_class_collision: true` when the judge class equals a reviewer class or the executor class; a collision is telemetry plus a REPORT.md note, never a silent pass. Whether `--compare` accepts a judge-exclusion input is UNVERIFIED; if it does not, the collision is recorded, not prevented. Fable and Tier 0 are never a judge: the adapter asserts the recorded judge model id is not `claude-fable-*` and not a `tier0` alias.
186	
187	### Q4. Engine
188	
189	<!-- Source: Base (original, modified) - agent-session bullet replaced per Change #7; Variant 2 (sonnet:analyzer) Q4 rule and Variant 3 (haiku:backend) Q4 launch binding -->
190	**Direct answer:** the pre-execution path uses the agent-session engine only, with one identity source. The K1 resolution JSON is the only place reviewer models are chosen. The swarm engine stays post-only (Stage 5).
191	
192	**Agent-session adapter (pre-execution).** For each reviewer in the K1 resolution: if `launch` is non-null and in the whitelist `{sonnet, opus, haiku}`, spawn `~/.claude/agents/reflect-reviewer.md` (project `.claude/agents/` first) with the Agent-tool `model` set explicitly to that value. The adapter must pass `model` on every dispatch (omitting it would run the agent's frontmatter default, Sonnet, for all reviewers; `reflect-reviewer.md:6` has `model: sonnet`); a conformance check asserts one explicit `model` per reviewer before dispatch. The Agent tool's `model` parameter in this harness accepts only `sonnet | opus | haiku | fable`; a gateway tier alias such as `claude-gw-tier2[1m]` is not in that set. If `launch` is null (every gateway model today, `review-tiers.default.json:20,23`) the resolution is **refused for pre-execution**: the run uses the legacy rotation and records `panel_fallback_reason: no-launch-alias`. No swarm dispatch is claimed for pre-execution; the swarm lens stays post-only (`ensemble.py:797`). The resolution is pinned (hashed template, tiers, seeds, executor-class exclusion result) before any reviewer is dispatched and is never re-resolved mid-run. Gateway agent-session dispatch is an open item (O-4); the first stage that supports it needs its own conformance run.
193	
194	**Swarm adapter (headless post path, Stage 5, cli/reflect/ensemble.py).** The `reflect-review` lens may take worker models from a PROPOSED `--panel-resolution <file>` input instead of `T2Model0N` env vars. `T2Model0N` stays as the fallback when no resolution file is given, so existing runs are unaffected.
195	
196	#### Template set
197	
198	<!-- Source: Base (original, modified) - template JSON replaced per Change #23 -->
199	Reflect's rotation becomes packaged K1 templates, all `review-panel.<name>.json`, loadable as `@<name>` (panel.py:327-334); each has exactly one `fixed` slot; none lists a tier-0 or Fable tier. V1's original template is the only validator-legal shape (one fixed slot, `panel.py:140-141`; slot ids match `^[a-z0-9]{1,8}$` `:31`; keys within `_SLOT_KEYS` `:46`), but its three slots change the anthropic-only reviewer set to sonnet, haiku, haiku and move Opus to the calibrator, which changes `t2_model_class_diversity`. Parity therefore needs a third slot on `tier1a` (`review-tiers.default.json:5`: opus, sonnet).
200	
201	```json
202	{"schema": "review-panel/1", "template_id": "reflect-pre", "version": "1.0.0",
203	 "distinct_across_slots": true, "apply_to": ["first"],
204	 "slots": [
205	   {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
206	   {"slot_id": "t4",  "tier": "tier4",  "count": 1, "strategy": "random"},
207	   {"slot_id": "t1a", "tier": "tier1a", "count": 1, "strategy": "random"}]}
208	```
209	
210	- `@reflect-pre` (parity, default). Anthropic-only resolves to sonnet, haiku, opus under strict distinctness: tier1b -> sonnet; tier4 -> haiku (a direct tier4 member and in the anthropic-only `available` list, `review-tiers.default.json:10,27`); tier1a minus {sonnet, haiku} -> opus. Persona by resolution order: fixed first, then slot order: analyzer, qa, refactorer (matches `reviewer-spec.md:97`). Parity matters because `t2_model_class_diversity: full` means three distinct classes (`SKILL.md:233-239`) and wrapper trigger 7 reads that field (`contract.py:281-284`).
211	- `@reflect-pre-x2` (anchor replacement when tier1b is exhausted by the executor, i.e. executor `sonnet` in anthropic-only, where tier1b has only Sonnet and no stand-in, `review-tiers.default.json:6,28`): fixed `t4` anchor plus random `t1a`. Resolves haiku, opus (2 reviewers, analyzer and qa), matching `reviewer-spec.md:102,109`.
212	- `@reflect-enterprise`: same slots as `@reflect-pre`; third persona `architect`; opt-in for `--strategy enterprise` (`SKILL.md:608`).
213	- `@reflect-lite` (variant arm only): V1's original three slots t1b, t4, t2; resolves sonnet, haiku, haiku (soft) or sonnet, haiku (strict, third slot skipped).
214	- Post templates `@reflect-post` and `@reflect-post-x2` mirror pre. Gateway templates are not defined (O-4).
215	
216	The 2-distinct diversity rule is the headless helper's (`_diversity.py:8-15`), which returns `insufficient`, not `degraded`, a vocabulary mismatch with `SKILL.md:790` recorded as O-9. The claim that anthropic-only "resolves to Sonnet, Haiku, Haiku" by default is withdrawn.
217	
218	#### K1 hard exclusion contract
219	
220	<!-- Source: Base (original, modified) - hard_exclude semantics replaced per Change #24 (INV-005); Variant 3 (haiku:backend) Q4 filter-before-dispatch merged -->
221	**K1 hard exclusion contract (PROPOSED code; generic panel behavior unchanged).** Verified failure modes today: a `fixed` slot returns `candidates[0]` and ignores `exclude` (`panel.py:402-403`); `random` and `round_robin` use `[m for m in candidates if m not in set(exclude)] or candidates` and so re-admit an excluded model when the pool empties (`panel.py:405,408`); `exclude` today carries only models chosen earlier in this panel (`panel.py:479`); `NoModelAvailable` is raised only when no candidate and no stand-in exists (`panel.py:396-401`); the anthropic-only stand-in map has no `tier1b` (`review-tiers.default.json:28`); `review-tiers.default.json:6` lists three tier1b models but only Sonnet is in the anthropic-only `available` (`:27`).
222	
223	1. `resolve_slot` and `resolve` gain two keyword-only parameters with defaults that reproduce today's behavior byte for byte: `hard_exclude: Sequence[str] = ()` (model ids) and `strict_distinct: bool = False`. They are resolve-time parameters, not template keys (`validate_panel` rejects unknown slot keys, `panel.py:109-111`).
224	2. Filtering is applied to the **candidate list itself**, before the strategy runs, for all strategies including `fixed`: `candidates = [m for m in candidates if m not in hard]` where `hard = set(hard_exclude) | (set(chosen) if strict_distinct else set())`. Fallbacks (`panel.py:417`) are derived from the filtered list, so no primary or fallback can be an excluded model. The silent `or candidates` re-admission is **not** taken when `hard` is non-empty.
225	3. If the filtered list is empty and the stand-in list has not yet been tried, try `stand_ins` filtered the same way; if still empty raise a new `ExclusionExhausted(tier)` (a subclass of `NoModelAvailable`). With `hard_exclude == ()` and `strict_distinct == False` the code path, output and hashes are identical to today (asserted by a spec-panel byte-identity test).
226	4. `resolve` records `skipped_slots: [{slot_id, reason}]` and `excluded: {models, classes}` as additive keys in the `review-panel-resolution/1` JSON; `merge_cmd.py:76-79` reads only `reviewers[*].reviewer_id/model`, so existing consumers are unaffected. A non-fixed slot that raises `ExclusionExhausted` is **skipped** (recorded), not fatal; the fixed anchor raising is fatal at kernel level. (The kernel fails closed; the reflect adapter catches the exception per slot and applies `SKILL.md:600`, below.)
227	5. **Class map.** The tier file gains a `classes` object mapping every model id to a class string in the vocabulary of `SKILL.md:1180` where one exists (`claude-opus-5-5: opus`, `claude-sonnet-5-5: sonnet`, `claude-haiku-5-5: haiku`) and a vendor family otherwise (`gpt-*: gpt`, `glm-*: glm`, `grok-*: grok`, `Qwen*: qwen`, `muse-*: muse`). A model id with no entry is **not eligible** in any `reflect-*` template (fail closed at validation). `--hard-exclude-class <class>` (PROPOSED CLI flag on `superclaude review panel resolve`) expands the class to ids through this map and compares case-insensitively with the executor value resolved by `SKILL.md:600-602` (flag, `EXECUTOR_MODEL_CLASS`, or log hint; headless wrapper also reads frontmatter `executor_model_class`, `cli/reflect/config.py:53-56,351-355`). The gateway classes `gpt|glm|grok|muse` are outside the `SKILL.md:1180` calibrator vocabulary; gateway is out of scope until O-4.
228	6. **Adapter (reflect side) applies the policy, the kernel only enforces:** (a) resolve with `@reflect-pre`, `strict_distinct=True`, `hard_exclude` = ids of the executor class. (b) If the fixed anchor raises `ExclusionExhausted`, re-resolve once with the anchor-replacement template (`@reflect-pre-x2`) before any dispatch; the replacement is recorded (`anchor_replaced: true`). (c) After resolution assert: no resolved model class equals the executor class; no model id repeats; at least 2 distinct classes. (d) Failure of (c), or a second exhaustion, is the `SKILL.md:600` path: `executor_exclusion_degraded: true`, WARN with the text of `SKILL.md:600`, degrade to T1 for rubric-driven escalation. For a pinned `--depth deep` or `--tier 2` run the degrade is never silent: see rule D3 of "When the panel is called".
229	7. **Unknown executor** (`executor_class_source: unknown`): unchanged fail-open of `SKILL.md:602` (`executor_class_resolved: false`, loud WARN); the panel runs without `hard_exclude`. This is the main consumer path today: `sc-workflow` Wave 4 passes only defaults (`sc-workflow-protocol/SKILL.md:60`) and a recorded workflow-driven pre run has `executor_class_source: unknown` (`.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/return-contract.yaml:96-97`). Exclusion therefore rarely fires in the main consumer path; see O-6.
230	8. **Tests (Stage 1 exit):** excluded model is the fixed anchor; pool empties for random and round_robin slots and the excluded model is not re-admitted; executor `sonnet` in anthropic-only yields `ExclusionExhausted` for `tier1b` and the adapter lands on `@reflect-pre-x2` with 2 reviewers; executor `haiku` skips the `t4` slot; executor `opus` under strict distinctness yields sonnet, haiku and no duplicate; unmapped model id rejected; `hard_exclude == ()` is byte-identical to the current resolution for the default and live7 templates.
231	
232	#### Opus uses
233	
234	<!-- Source: Base (original, modified) - "Opus only here" claim replaced per Change #19; Variant 3 (haiku:backend) Q3 Opus rule -->
235	**Opus uses (complete list; the owner's ceiling is "Opus only sparingly").** (1) Blind calibrator, chosen by the unchanged rule of `SKILL.md:1181-1186` (highest capability from the set disjoint from reviewers, else the class used by fewest reviewers, with `calibrator_diversity: degraded`). (2) Third reviewer in the anthropic-only parity template, exactly where today's rotation puts it (`SKILL.md:607`), and as backfill when the executor class is removed (`reviewer-spec.md:108`). (3) Reviewer in the opt-in `--strategy enterprise` template (`SKILL.md:608`). (4) Never as a judge pinned by reflect (`SKILL.md:612`). No use is new relative to today. The calibrator for the parity template stays `degraded` (the disjoint set is empty; recorded card: `calibrator_model_class: opus`, `calibrator_diversity: degraded`). The lite template (variant arm only) moves use (2) to use (1): its calibrator diversity becomes `full`, its model-class diversity falls from three classes to two, which the interactive skill labels `degraded` (`SKILL.md:237-239`). That value change is why lite is a measured arm and not the first shipment. Fable and Tier 0 are never used. Every Opus mention elsewhere in this document points here.
236	
237	#### Forbidden models: Fable and Tier 0
238	
239	<!-- Source: Variant 2 (sonnet:analyzer), U-013 and Risk 7 - merged per Change #8 -->
240	The tier file maps four ids in `launch`, including `claude-fable-5-1` to `fable` (`review-tiers.default.json:14,27,29`); `panel.py:30` `_TIER = ^tier[0-9]{1,2}[a-z]?$` accepts `tier0`; nothing in `cli/review` mentions Fable (grep over `cli/review`, only the tier json). Reflect profile validation (PROPOSED, in the kernel, applied to every `reflect-*` template and to every resolution): (1) reject any resolved model id matching `claude-fable-*`; (2) reject any template slot whose tier is `tier0` or whose alias list contains a Tier 0 model; (3) reject a `launch` value outside `{sonnet, opus, haiku}` at dispatch. The same filter applies to the calibrator pick and to the recorded judge identity.
241	
242	#### Executor-exclusion gates
243	
244	<!-- Source: Base (original, modified) - new subsection merged per Change #26 (INV-022) -->
245	Executor exclusion is enough only if eight gates hold, including identity read-back. The card's top-level `model_class: sonnet` is orchestrator-written, so today identity is the request; the Agent tool schema exposes no model-id in a reply (UNVERIFIED for the reply body); `reflect-reviewer.md:6` defaults to Sonnet when no override is passed; the recorded workflow pre run has an unknown executor.
246	
247	| Gate | Decision | Evidence or test | If it fails |
248	|---|---|---|---|
249	| 1 executor class resolved (flag, env, log; `SKILL.md:600-602`) | unchanged; `unknown` stays fail-open and is reported as `executor_class_resolved: false` | recorded run `return-contract.yaml:96-97` | no exclusion, loud WARN |
250	| 2 per-model class map | `classes` in the tier file; unmapped ids ineligible | K1 contract item 5 | template invalid, legacy rotation |
251	| 3 candidate filter | kernel `hard_exclude` on primary, fallback and fixed | tests in K1 contract item 8 | degrade per K1 contract item 6 |
252	| 4 `resolve_slot` pick | no `or candidates` re-admission under `hard` | `panel.py:405,408` fixed by K1 contract item 2 | `ExclusionExhausted` |
253	| 5 tier1b stand-in | none exists (`review-tiers.default.json:28`); anchor replacement template | `@reflect-pre-x2` | degrade |
254	| 6 dispatch via `launch` | whitelist `{sonnet, opus, haiku}`; null refused for pre; explicit `model` on every call | Agent-session adapter above | legacy rotation |
255	| 7 actual identity | **identity_source = `requested-pinned`** (the Agent tool pins `model`); the card header records `model_class` from the request, as today; each reviewer card must also carry a one-line self-report `reviewer_model_self_report` (advisory); a mismatch with the pin sets `identity_mismatch_suspected: true`, degrades diversity telemetry and never upgrades trust | **Spike S-ID, Stage 1 exit:** dispatch three probe reviewers (`model: haiku`, `sonnet`, `opus`) with a probe brief; check (a) the self-report matches the pin in 3 of 3 and (b) whether the tool result or transcript exposes a model id. If (b) is yes, switch `identity_source` to `observed` and assert it; if no, the pinned identity stays and is stated as an unverified assumption | UNVERIFIED until the spike runs |
256	| 8 N=2 floor on distinct classes | counts `complete` reviewers of **distinct** classes (see "Completion and channel") | test: two reviewers of one class do not reach T2 | T1 degrade (`SKILL.md:600`) |
257	
258	Safe default if S-ID is not run: pinned identity, `identity_source: requested-pinned` in telemetry, and no claim of verified independence in REPORT.md.
259	
260	#### Guards and counts
261	
262	<!-- Source: Base (original, modified) - new guards merged per Change #30 (INV-006, 007, 009, 011) -->
263	**INV-006:** an unknown executor keeps the fail-open path and the T2 report states `executor_class_resolved: false`; the T2 label is allowed but REPORT.md must not claim anti-self-confirmation; the Stage 2 telemetry counts how many runs have it (O-6). **INV-007:** the N=2 floor is enforced on **distinct classes among `complete` reviewers**, in the adapter (strict distinctness) and as a post-resolution assertion; the headless builder's `tier_reached` rule (`ensemble.py:772` sets `tier_reached = 2` on `reviewer_count >= 2` without checking models differ) is a Stage 5 work item (add a distinct-model check there). **INV-009:** pre reviewers are only launched through the `reflect-reviewer` agent with an explicit `model` override; `reflect-reviewer.md:5-8` gives `tools` (Read, Grep, Glob and read-only search MCP tools, no Bash/Edit/Write) and `permissionMode: plan`; the allowlist is expected to survive the override (UNVERIFIED, part of spike S-ID: the probe reviewers are given a write attempt that must fail); a `launch: null` model is never dispatched, so no swarm path exists for pre; the post swarm path keeps its existing isolation telemetry (`ensemble.py:825-831`). **INV-011:** the manifest records three counts, `reviewers_requested`, `reviewers_resolved`, `reviewers_complete`; EV-1 compares calibrated cards with `reviewers_resolved` (unchanged); a short run is MALFORMED under EV-1, remediated by the existing bounded re-dispatch, then the F2 fallback. The 2-of-3 mismatch between EV-1 (`SKILL.md:666` calls it MALFORMED) and the wrapper (`ensemble.py:765-770` records a benign `reviewer-shortfall`; halt set only auggie, env-aliases, evidence-validator, `contract.py:31-33`) pre-exists and is preserved; Stage 2 counts it.
264	
265	### Q5. Pre-execution migration end to end
266	
267	<!-- Source: Variant 3 (haiku:backend), Q5 - merged per Change #12 (answer in place); Base (original, modified) -->
268	**Direct answer:** inputs are plan plus source spec (`--spec <pkg>/source.md --tasklist <pkg>/<id>.md`, enrichment). Waves 0-2 are unchanged and decide the tier; the panel runs only if the final tier is 2 and `--t2-engine` is not `legacy` (rules D1-D5 of "When the panel is called"). Then: resolve the reviewers with executor exclusion; dispatch them through the agent-session adapter; blind-calibrate each card; run the `/sc:adversarial` debate on the calibrated cards; run the evidence gate; emit contract 1.8.0 unchanged. Flag order: depth, pin, budget and rubric first, `--t2-engine` after. The step-by-step flow is in "Adapter sketches".
269	
270	### Q6. Rounds, ledger, revise loop
271	
272	<!-- Source: Base (original, modified) - ledger not used for reflect per Change #17, #29 -->
273	**Direct answer:** reflect is single-pass (`SKILL.md:342`; it never revises the artifact it reviews, so rounds 2-3 would have nothing to verify). **The panel ledger is not used for reflect in Stages 0-4:** the merge is the `sc-adversarial` debate; K4 clustering writes `panel/clusters.json` and needs no rounds, no REVISE/ESCALATE decision and no `doc_sha256`. If a later stage uses the ledger, run it with `--cap 1` knowing every blocking round records `ESCALATE` (`_decision` returns `REVISE if n < cap else ESCALATE`, `ledger.py:93-96`), reflect must ignore `decision`, and telemetry must not surface it as an escalation. Each merge attempt gets its own ledger path (see "Execution contract"). A ledger row stores a bare `span` per row (`ledger.py:196-197`) and one `doc_sha256` per round (`:278-279`), which is why it is path-blind (see "Multi-file identity").
274	
275	**Extension point, not built:** sc-workflow's Phase B "refactor" loop re-runs Phase A into a new package (SKILL.md:342). A future ledger keyed on the workflow id could carry findings across those packages. That is deferred and named only so a future ledger id is not tied to one reflect run id.
276	
277	### Q7. Cost before and after; when a full panel is not worth calling
278	
279	<!-- Source: Variant 3 (haiku:backend), Q7 - merged per Change #12, #4; Variant 2 (sonnet:analyzer), Q7 rule - merged per Change #9; Base (original, modified) -->
280	**Direct answer:**
281	
282	- **Pre-execution:** the first shipment is parity. The panel-parity T2 planning estimate is 43k-67k output tokens (legacy plus about 1.5k for the findings block) against 42k-66k for legacy; a possible 37k-56k if cards turn out shorter is a hypothesis; no saving is claimed. Panel T2 must stay inside the existing 35k-70k profile band and below the 65k kill line at p95 (a measurement criterion, see First measurement). The arithmetic and units are in "Cost model".
283	- **Post-execution:** about unchanged (the debate is kept; +1.5k for the findings blocks).
284	- **A full panel (default 4 slots, or live7) is not worth calling for reflect:**
285	  - In anthropic-only, every extra slot is another Haiku stand-in. That adds tokens without new model classes. The 1S+6H vs 1S+3H gain was about 3 defects on one spec (docs/reference/review-panel-live7.md:19-26, enrichment).
286	  - Reflect has no revise step to turn extra findings into fixes.
287	  - Pre is advisory.
288	
289	**Code-level cap (hard):** reflect-profile validation rejects any `reflect-*` template or resolution with more than 3 reviewers, whatever the user template says (the generic panel keeps 1..8 for `/sc:spec-panel`, `panel.py:142`; reflect is limited to 2-3, `SKILL.md:86`). `N_eff = min(--reviewers (default 3), alias-derived count from SKILL.md:233-239, 3)`; a fixed anchor is never dropped; trailing random slots are dropped first. **Raising the cap** to 4+ needs (PROPOSED, labelled as such because V3 dissents) a measurement showing T2 recall beats T1 recall by at least 15 percentage points and the larger panel beats T2 by a margin the owner accepts. Larger panels are never an automatic response to `--depth deep` (V2 Q7 allowed 4+ on `--depth deep`; rejected: `--depth deep` forces T2 and routes remediation, `SKILL.md:89,365`, and says nothing about reviewer count).
290	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:291-357

```markdown
291	## Finding format
292	
293	<!-- Source: Base (original, modified) - table rows restated per Change #5, #11, #37, #2 -->
294	PROPOSED schema `findings-v2`. It is JSON lines in a fenced block with info string `findings-v2` under the heading `## Findings block`, the same container rules as v1 (findings.py:124-196). A v1 line is valid v2 by construction.
295	
296	| Field | Type | v1? | Set by | Rule |
297	|---|---|---|---|---|
298	| `id` | str `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` | yes | reviewer | unique per block (findings.py:91-95) |
299	| `severity` | CRITICAL/MAJOR/MINOR | yes | reviewer | MINOR cannot block (findings.py:100-101) |
300	| `blocking` | bool | yes | reviewer | |
301	| `category` | v1 six-value enum, unchanged (findings.py:15-22) | yes | reviewer | reflect's original label is preserved in `reflect_category` (mapping below) |
302	| `reflect_category` | `ordering` `acceptance` `coverage` `contradiction` `risk` `deviation` | NEW | reviewer | original reflect label, never routes anything |
303	| `claim` | str ≤300 | yes | reviewer | |
304	| `refs` | ≤8 str | yes | reviewer | requirement ids such as `REQ-014`, `INF-003`, task ids |
305	| `anchor`, `anchor2` | quote 12-200 chars | yes | reviewer | **required only if `citations` is absent**; a finding with neither is invalid |
306	| `citations` | list 1..8 of `{role, path, line_start, line_end, quote?}` | NEW | reviewer | `role` ∈ `plan` `spec` `source` `test` `diff` `artifact`; `path` repo-relative; `quote` **optional** (12-200 chars copied from those lines when present) |
307	| `deviation_class` | `authorized` `necessary` `drift` `regression` `none` | NEW | reviewer | required when `lens` is `reflect-post`; optional in pre (plan-vs-spec gaps map to `none` or a coverage category) |
308	| `coverage_rows` | list of requirement/task ids | NEW | reviewer | must be ids present in the reviewer's Coverage slice |
309	| `self_confidence` | float 0-1 | NEW | reviewer | self-report; never routes anything |
310	| `lens` | `spec` `reflect-pre` `reflect-post` | NEW | brief | selects the required-field profile |
311	| `channel` | `defect` `grounding-gap` `advisory` | NEW | reviewer | optional, default `defect` (see "Completion and channel") |
312	
313	**Category and severity mapping** (v1 six-value enum unchanged; reflect's original label is kept in `reflect_category`): `ordering` -> `other`; `acceptance` -> `unpassable-check`; `coverage` -> `missing-requirement`; `contradiction` -> `contradiction`; `risk` -> `safety` or `other`; `deviation` -> `other` with `deviation_class` set. Severity: `blocking` -> MAJOR or CRITICAL with `blocking: true`; `minor` -> MINOR.
314	
315	**Calibration is not carried in the block.** The calibrator appends the existing `calibration:` block to the card, exactly as today (recorded card: `calibrator_model_class`, five `dimensions`, `C`, and `per_finding` entries with `finding_confidence` and `reason`, stoprule `reviewer-1-card.yaml:82-103`). The findings-v2 block does not carry calibrated confidence; reflect joins `calibration.per_finding[id]` to findings by (reviewer_id, finding id). A reviewer line that sets `calibrated_confidence` is rejected. The evidence validator's results stay where Wave 5 writes them today. The ledger carries no calibration (`ledger.py:86-90`), so the card is the only carrier. (The earlier findings-only sidecar files `panel/calibration.json` and `panel/validation.json` are not part of this design: today's card is mutated by the calibrator, and a sidecar would leave the debate's calibrated-card input without calibration.)
316	
317	**How reflect card content and panel findings coexist.** The reflect card stays a document. Its prose sections and the persona's narrative are what the debate reads and what the report quotes. The `findings-v2` block is the machine part.
318	
319	### What a recorded card looks like
320	
321	<!-- Source: Variant 2 (sonnet:analyzer), Candidate B/C reasons 2 - merged per Change #10 -->
322	Findings in the recorded stoprule card are YAML with `severity: blocking|minor`, categories `ordering|acceptance|deviation|coverage|risk`, `evidence: [plan:57, source.md:62, src/...:451-462]` (line refs, no quotes), an orchestrator-written `model_class: sonnet`, and `plan:`/`spec:` paths. Conversion rule for recorded cards (deterministic, no quote): `plan:N` -> `(plan, <card plan path>, N, N)`; `source.md:N` or `spec:N` -> `(spec, <card spec path>, N, N)`; `path:A-B` -> `(source, path, A, B)`; unresolvable refs stay as `unresolved` citations and are counted. **Lossless conversion is not claimed**: Stage 0a reports the share converted unambiguously, with a gate of at least 90% before the parser change ships (O-7). `quote-not-found` is advisory only. In the post audit bundle, each grounding hunk is an H3 `path:start-end` heading in the reviewer's brief (the shape reviewers already receive, `reviewer-spec.md:45`); it is a per-source layout inside the brief, never a concatenated document that identities are computed against.
323	
324	### Completion and channel
325	
326	<!-- Source: Variant 3 (haiku:backend), Finding format (completion, channel) - merged per Change #2 -->
327	**Completion states** (per reviewer attempt, recorded in the manifest): `complete`, `truncated`, `invalid` (no parsable findings-v2 block or schema failure), `failed` (transport), `timed_out`. Only `complete` with a valid block counts toward quorum. A valid empty findings array is `complete` only when the card also carries its coverage observations for every assigned row; otherwise it is `invalid`, never "clean". The N=2 floor of `SKILL.md:600` counts `complete` reviewers of distinct classes (see "Guards and counts"). **Channel** (optional v2 field, default `defect`): `defect | grounding-gap | advisory`. An `advisory` finding is never counted in `deviation_count_by_class` and never maps to Regression (advisory no-spec gaps must never become Regression, `agents/reflect-reviewer.md:30`). Optional fields; v1 lines stay valid. A ledger-level hole (a reviewer with an empty valid block counted as clean) is already closed by `ledger.py:150-157`.
328	
329	### Multi-file identity (K4 `cluster_v2`)
330	
331	<!-- Source: Base (original, modified) - dedupe key replaced per Change #25 (INV-015); Variant 3 (haiku:backend) separate-documents -->
332	Verified problems in today's code: the ledger row stores a bare `span` list with no path (`ledger.py:196-197`) and each round one `doc_sha256` (`:278-279`); `merge_cmd` takes a single `--doc` (`merge_cmd.py:29-34`), so concatenating documents erases identity; `findings._spans` returns spans without a path and `same_defect` compares any two spans within 3 lines (`findings.py:363-379`), so two findings at line 10 of different files merge; clustering is transitive (`findings.py:382-407`).
333	
334	**Multi-file identity (PROPOSED K4 `cluster_v2`).** Reflect does not use `review merge` or the ledger in Stages 0-4 (the merge is the debate), so no path-blind row exists. K4 is a pure function `cluster_v2(findings_v2_blocks, snapshot_file_list) -> clusters` exposed as `superclaude review cluster` (PROPOSED), writing `<out>/panel/clusters.json`.
335	
336	1. **Citation tuple.** Each citation is `(role, path, line_start, line_end)` with `path` repo-relative and verified against `artifacts/input-snapshot.yaml` (`SKILL.md:217-229`), whose `file_list` gives each file's sha256. A citation whose path is not in the snapshot file list is `unresolved` and never joins a cluster by span. Spans are 1-based inclusive line ranges taken from the citation itself (no `locate` call needed; `quote` is optional).
337	2. **Primary citation** = the first citation whose `role` is the reviewed artifact (`plan` in pre; `source` or `diff` in post), else the first citation.
338	3. **`same_defect_v2(a, b)`** is true only if (i) deviation classes are compatible (equal, or either null or `none`), **and** (ii) the `refs_norm` sets intersect or are both empty (same normalization as `findings.py:321-337`), **and** (iii) some citation of `a` and some citation of `b` have the **same `path`** and spans within 3 lines (`a.start <= b.end + 3 and b.start <= a.end + 3`, the tolerance of `findings.py:377`). Equal fingerprints (`sha256("v2|" + role + "|" + path + "|" + section + "|" + refs + "|" + class)`) with non-empty refs also match, as in `findings.py:371-372`. **Two findings that cite different paths never match by span.** Two findings that cite the same spec requirement from different plan tasks match only through a shared `spec` path span plus a shared requirement ref.
339	4. **Transitivity guard.** Clusters are union-find components (as `findings.py:382-407`); each cluster is marked `chained: true` when it contains two members that do not match pairwise. `chained` clusters list their members and are never treated as one issue for counting.
340	5. **Per-source identity.** The brief carries each source as its own H3 `path:start-end` hunk (`reviewer-spec.md:45`); there is no concatenated review document and no `review-doc.md`.
341	6. **Tests (Stage 0 exit, positive and negative):** two findings at line 10 of two different files do not cluster; two findings on the same file within 3 lines and equal refs do cluster; a three-member chain A-B-C with A and C pairwise unequal is `chained`; v1 reports through the unchanged `review merge` produce byte-identical output with and without the new module imported.
342	7. **If the ledger is used later** (not planned), rows need `citations[]` (path-aware) and a `ledger/2` schema; that is a separate change, recorded as O-5.
343	
344	### `cluster_agreement` and clustering semantics
345	
346	<!-- Source: Base (original, modified) - panel_agreement_score replaced per Change #32 (INV-014, 018, 019, 021) -->
347	**`cluster_agreement` (telemetry only; the name `panel_agreement_score` is not used).** For each cluster c, `support(c)` = sum of the calibrated confidences (`calibration.per_finding[id].finding_confidence` joined from each member's card) of the distinct reviewers in c divided by the sum of calibrated confidences of all `complete` reviewers; `cluster_agreement` = mean support over blocking clusters, or 1.0 when none and at least 2 valid blocks. A cluster is **disputed** when support < 0.5, members disagree on `blocking`, or disagree on a non-null `deviation_class`. **Owner of a cluster's score:** the cluster carries the list of member calibrated scores, no scalar; its representative claim text and `blocking_any`/`blocking_all` come from the member with the highest calibrated confidence (ties: resolution order), not from the first reviewer (a ledger copies claim, anchor and category from the first member and ORs blocking before any validator drop, `ledger.py:182-199`). **Order:** clusters are computed on raw cards for telemetry; a second pass `clusters_kept` recomputes over findings the evidence validator kept, and only `clusters_kept` is used in measurements; the raw `overlap` label never routes anything. **Chaining:** `chained` clusters are excluded from agreement counts and listed. **Names:** stable field `adversarial_convergence_score`; prose name `convergence_score` (`SKILL.md:663,1483`); telemetry `cluster_agreement`. No other score name is introduced. `cluster_agreement` is never compared with the convergence thresholds and never routes anything.
348	
349	### Evidence gate and citation pre-check
350	
351	<!-- Source: Base (original, modified) - pre-check semantics replaced per Change #31 (INV-012, INV-013) -->
352	**The deterministic pre-check never drops a citation.** `superclaude review verify-citations` (PROPOSED, 0 model tokens) writes `panel/precheck.json` with, per citation, `missing-file`, `out-of-range`, or `quote-not-found` (advisory; a failed locate is not proof of an unfounded citation). Every flagged citation is added to the evidence-validator's re-read set even when the sampling policy (`SKILL.md:1204-1208`) would have skipped it. The validator alone decides drops, so `citations_dropped` keeps its sample-count meaning (`SKILL.md:1210-1214`: the count among the re-read sample; gate 6a requires 0 and trigger 13 degrades on any value above 0, `contract.py:347-352`) and gate 6a and trigger 13 are unchanged. Grounding is at least as strong as today because flagged citations are always re-read. A pre-check that dropped citations over every citation would change the field from a sample count to a mixed count and tighten a gate, a semantic change (major, `SKILL.md:953`); that variant is not adopted.
353	
354	**Headless gap** (`ensemble.py:808-819`, `citations_dropped: 0`, `verification_ran: False`): a Stage 5 work item runs the same pre-check headless and reports the validator-confirmed count; this moves the field toward its documented meaning, can newly trip trigger 13, and is announced at Stage 5 entry as a behavior change, not a contract version event.
355	
356	**Thresholds:** no change to either. Pre runs route by `SKILL.md:655` (>=0.75 PASS, >=0.60 PARTIAL); the wrapper's 0.80 line (`contract.py:317-326`) applies to post contracts only; the first measurement reports both bands per run so the owner can see how many pre runs would degrade under 0.80 (one recorded pre run scored 0.76, inside that gap).
357	
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

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:401-415

```markdown
401	## Staged migration
402	
403	<!-- Source: Base (original, modified) - rows replaced per Change #43, #36 -->
404	Pre-execution ships behind an off-by-default flag first: `--t2-engine` defaults to `legacy` in every stage until Stage 4.
405	
406	| Stage | What ships | Entry | Exit | Rollback |
407	|---|---|---|---|---|
408	| **0. Measure offline** | findings-v2 schema and parser, card converter, `cluster_v2`, Stage 0a replay on the recorded cards, consumer inventory and the lint test design | design accepted | 50-pair hand-labelled cluster check; conversion share >= 90% (see "What a recorded card looks like"); consumer grep result stored (see "Contract compatibility gate"); pilot designed and costed | delete the code; nothing consumes it |
409	| **1. Kernel extensions, dormant** | K1 `classes`, `hard_exclude`, `strict_distinct`, `ExclusionExhausted`, Fable and tier0 rejection, `@reflect-pre`, `-x2`, `-enterprise`, `-lite`; `review cluster`; `verify-citations` | Stage 0 exit | the K1 contract item 8 tests; spec-panel byte-identity (default and live7 templates); template validity; spike S-ID run (see "Executor-exclusion gates") | revert the commits; new parameters default off |
410	| **2. Pre shadow** (`--t2-engine shadow`, default `legacy`, read only after the final tier) | the panel resolution is written next to the legacy rotation and asserted identical (parity), findings-v2 block instruction in the brief, clusters, pre-check, manifest; legacy debate authoritative; contract 1.8.0 | Stage 1 exit; contract compatibility gate passed | 20 shadow runs: zero MALFORMED, EV-1 failure rate no higher than legacy, parity assertion holds, lint and verdict replay pass | flag default is `legacy`; delete `<out>/panel/` |
411	| **3. Pre panel opt-in** (`--t2-engine panel`) | reviewers chosen by the template; debate on cards authoritative; contract 1.8.0 | **first measurement passed (H-B, H-C, safety)** and the environment gate: Stage 3 and later run only in an environment whose resolved models all have a non-null `launch` alias (today: anthropic-only); Haiku-stand-in runs certify mechanics and anthropic-only behavior, not gateway quality; a gateway default needs its own run of the first measurement (not planned; O-4) | 30 opt-in workflow runs: `reflect_status` distribution no worse than shadow, zero MALFORMED, median tokens <= 1.05 x legacy | flag to `legacy` |
412	| **4. Pre default** | sc-workflow's Wave 4 gets `panel` by default | Stage 3 exit plus owner sign-off | two release cycles with no rise in workflow `reflect_status: failed` | one-line default change |
413	| **5. Post panel dispatch** | post adapter: K1/K2/K3, K4 telemetry, debate kept; headless `citations_dropped` made real with the `ensemble.py:772` distinct-model check | Stage 4 exit; a separate post measurement (seeded deviations, class accuracy) | wrapper verdict distribution on >= 20 paired post runs: no new `degraded` or `halted` reason from dispatch alone | flag to legacy rotation |
414	| **6. Deferred candidate E'** | deterministic pre merge, `merge_method` value `panel`, contract 2.0.0 | a measurement that the debate adds nothing plus every consumer in "Deferred versioned change" updated | not planned | not planned |
415	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:416-473

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
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:474-501

```markdown
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
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:502-521

```markdown
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

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:522-545

```markdown
522	## First measurement
523	
524	<!-- Source: Base (original, modified) - replaced per Change #28 (INV-024); Variant 2 (sonnet:analyzer) three-arm design and sample-size section; Variant 3 (haiku:backend) hygiene -->
525	**Hypotheses and thresholds (one margin each).**
526	
527	- **H-A (worth):** T2 recall beats T1 recall by at least **15 percentage points** on seeded defects (superiority). If not, record that the T2 spend does not buy recall on plans, and the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8). This is not an automatic veto of the migration, which is justified by maintenance as well.
528	- **H-B (non-inferiority):** panel-parity T2 recall is within **10 percentage points** of legacy T2 recall (one-sided 95% bound), and precision likewise. **The 5-point margin (V3) and the 15-point margin as an NI bound (V2) are dropped:** 5 points is not resolvable at feasible n (below), and 15 points is the H-A threshold, a different hypothesis.
529	- **H-C (cost):** median panel-T2 tokens <= 1.05 x legacy median and p95 <= 65k in the profile unit (see Cost model). A saving is reported, not required.
530	- **Safety (fails regardless of savings):** a forbidden model or executor-class collision dispatched when the executor is known; a MALFORMED contract; an unsupported citation certified; any repository write by a reviewer; a T1 or `--depth quick` run that calls the panel.
531	
532	**Arms** (same plans, hidden arm identity for graders): A = T1 only (a `--tier 1` pin; flag semantics `SKILL.md:362`); B = legacy T2; C = panel-parity T2 (a development-build `--t2-engine panel`, or the `shadow` run with the parity assertion; the measurement runs on a development build and Stage 3 ships the same code to users; debate kept) <!-- fix M8 -->; D = panel-lite (the `@reflect-lite` template: sonnet, haiku, Opus calibrator; pilot subset only) to price the Opus-moves ablation.
533	
534	**Ground truth.** Seeded defects (scripted, not derived from reviewer output; ordering, missing acceptance, spec-uncovered requirement, wrong file path, cross-task contradiction) plus a **union ledger** of natural findings from all arms scored by a blinded grader (the ledger circularity caveat `LEDGER-RESULTS.md:49` applies).
535	
536	**Sample size (formula and numbers).** Paired by defect, with discordance d = share of defects found by exactly one arm. Standard error of the paired recall difference is about sqrt(d/n). One-sided 95% non-inferiority with 80% power at true difference 0 needs `n = d x (1.645 + 0.842)^2 / M^2 = 6.185 x d / M^2`. For M = 0.10: **n = 618 x d** defects (d = 0.10 -> 62; d = 0.20 -> 124; d = 0.30 -> 185). For H-A with M = 0.15: **n = 275 x d** (d = 0.35 -> 96). Multiply by 1.3 for clustering of defects within plans. At the pilot size of 60 defects the power is about 79% when d = 0.10 but only about 54% when d = 0.20 (SE 0.058, bound 0.095): the pilot therefore estimates d; it does not decide H-B.
537	
538	**Phasing.** Pilot: 12 plan+spec pairs x 5 seeded defects = 60 defects, arms A, B, C (arm D on 6 of them), plus 6 repeats of arm B to estimate the within-arm noise discordance d0 (if d0 is at least 0.8 x d between arms, the arms are indistinguishable from noise). Confirmatory: `n_plans = ceil(1.3 x max(618 x d_BC, 275 x d_AB) / 5)` from the pilot's observed d; the owner approves the spend before it runs. Cost units are the profile's: per plan arms A+B+C = 3k-8k + 35k-70k + 35k-70k = 73k-148k claude tokens; pilot (12 plans) 0.9M-1.8M; a confirmatory run of 33 plans (d = 0.20) 2.4M-4.9M; arm D adds 6 x 35k-70k. Retrieval tokens are reported separately and not summed. Hygiene: blinded arm identity, a stop rule, and the pilot labelled as a pilot.
539	
540	**Strata (required reporting).** Results are reported **split by `--depth` and by escalation path**, never only pooled: strata are (standard, escalated by the parsed-sparse pre-filter), (standard, escalated by rule 4, 5 or 6 without the pre-filter), (`--depth deep`), (`--tier 2` pin). Quota: at least 25% of plans whose source carries labelled requirement ids (non-sparse), because 34 of 38 recorded pre decisions were parsed-sparse (see "When the panel is called"); if not obtainable, the report states it measured sparse-labelled plans only. Each stratum reports n, recall, precision, tokens and a CI; a pooled headline is shown only if a heterogeneity check across strata is not significant.
541	
542	**Stage 0a (zero dispatch, descriptive).** Convert the recorded cards (42 `reviewer-cards/` directories under `.dev/reflect/pre-*`, 33 with `adversarial/merged-verdict.yaml`) to findings-v2 (line refs to citations), run `cluster_v2`, report cluster counts and agreement with the recorded merged verdict; report the share of findings that convert with an unambiguous `(path, line)` (the gate: at least 90%). Unseeded, not a pass/fail input.
543	
544	**Inconclusive is not a pass.** If the confirmatory interval crosses the margin, H-B is inconclusive and Stage 3 does not proceed; Stages 0-2 still ship.
545	
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:546-560

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
```

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:561-606

```markdown
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

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:607-625

```markdown
607	## Required-content map
608	
609	<!-- Source: Base (original, modified) - new appendix merged per Change #46 -->
610	| Required content | Where |
611	|---|---|
612	| At least 3 candidate architectures including leave-as-is | Candidate architectures (A-D and E') |
613	| Chosen architecture and reasons | Chosen architecture and reasons |
614	| Answers to Q1-Q7 | Answers to Q1-Q7 |
615	| Finding format | Finding format |
616	| Pre and post adapter sketches | Adapter sketches |
617	| Staged migration with pre behind an off-by-default flag first | Staged migration (Stage 2 `shadow`, Stage 3 `panel`, default `legacy`) |
618	| Mapping onto contract 1.8.0: `merge_method`, convergence score, null-score rules, gate condition 9, `reflect_post` frontmatter, every consumer | Return-contract 1.8.0 mapping (and "Deferred versioned change" for the consumer list of the deferred path) |
619	| Cost model with the depth table | Cost model; When the panel is called (depth x tier path) |
620	| Main risks | Risks |
621	| First measurement | First measurement |
622	| Depth x tier call policy | When the panel is called (depth x tier path) |
623	
624	
625	
```

## Coverage slice

| Plan task | Plan line | Depends on | Spec span it answers |
|---|---|---|---|
| Task 1: Add the findings-v2 schema and parser | 32 | none | Finding format 291-357 (schema, completion) |
| Task 2: Add the recorded-card converter | 41 | Task 1 | Finding format 319-323 (recorded card) + O-7 gate |
| Task 3: Implement cluster_v2 (path-aware, with the chained guard) | 52 | Task 1 | Multi-file identity 329-348 (K4) |
| Task 4: Build the Stage 0a replay on the recorded cards | 63 | Task 2, Task 3 | First measurement Stage 0a 542; Staged migration 408 |
| Task 5: Produce the 50-pair cluster check sheet and its scorer | 74 | Task 3 | Staged migration Stage 0 exit 408 (50-pair check) |
| Task 6: Add the consumer inventory script and store the first result | 84 | none | Contract gate item 1 466-468 |
| Task 7: Design and cost the first-measurement pilot | 93 | Task 4 | First measurement 522-544 |
| Task 8: Add hard exclusion and strict distinctness to panel resolution | 106 | Task 7 | K1 contract 218-231 |
| Task 9: Add the class map, Fable and Tier 0 rejection and the reviewer cap | 117 | Task 8 | K1 + Forbidden models 237-241 + Template set 196-217 |
| Task 10: Add the CLI flags to `review panel resolve` | 128 | Task 8, Task 9 | K1 CLI flags 574-575 (PROPOSED) |
| Task 11: Ship the reflect panel templates | 138 | Task 10 | Template set 196-217; K1 item 8 |
| Task 12: Add `superclaude review cluster` | 151 | Task 3, Task 11 | K4 + cluster_agreement 344-348 |
| Task 13: Add `superclaude review verify-citations` | 162 | Task 1, Task 12 | Evidence gate and citation pre-check 349-357 |
| Task 14: Run the identity spike S-ID and record the result | 173 | Task 11 | Executor-exclusion gates 242-259 (S-ID); UNVERIFIED 587-589 |
| Task 15: Add the panel contract lint and its per-field source table | 186 | Task 6 | Contract gate items 2,3,5 469-472 |
| Task 16: Add the verdict replay and refresh the inventory | 196 | Task 6, Task 15 | Contract gate item 4 471 |
| Task 17: Add the panel manifest module and CLI | 208 | Task 11 | Execution contract 360-366 |
| Task 18: Add `--t2-engine` and the engine-decision rules to the reflect skill | 218 | Task 14, Task 16, Task 17 | When panel called D1-D5 120-123, table 126-140 |
| Task 19: Write the shadow-mode steps, brief line and telemetry into the reflect skill | 229 | Task 12, Task 13, Task 18 | Pre-execution adapter 367-386; Shadow mode |
| Task 20: Add the Stage 2 shadow-exit aggregator | 243 | Task 16, Task 19 | Staged migration Stage 2 exit 410 |

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.
