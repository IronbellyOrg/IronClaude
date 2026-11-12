# Reviewer 1 brief (analyzer)

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

### .dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/TASK-WF-implementStages0-20261111-202912.md:31-148

```markdown
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

### .dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md:187-264

```markdown
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
