# Research: Reflect-side consumer of the Review Panel (scope slice 3 of 5)

**Scope:** src/superclaude/skills/sc-reflect-protocol/SKILL.md (sections 3.1, 4 Wave 0 step 0.5, 4.3a, 5.4, 7.1, 9.1, 9.2, 11.3) and refs/reviewer-spec.md; src/superclaude/agents/reflect-reviewer.md and confidence-calibrator.md; src/superclaude/cli/reflect/panel_lint.py; scripts/reflect_*.py; tests/cli/reflect/ panel/shadow tests; git diff master..HEAD -- src tests.
**Status:** Complete
**Date:** 2026-11-13
**Branch:** ironbelly/shadow-runs (HEAD 792cf8c52)

**Baseline note.** The local `master` ref is stale: `git log master..HEAD` lists many merged PRs. The branch is 3 commits ahead of `origin/master` (`git log origin/master..HEAD`: 792cf8c52, c2e3347d3, 9874d63fb). Commit d2d8a2d16 (#519, Stage 0-2 of the reflect panel) is already on `origin/master`, so the whole panel kernel used by reflect (`cli/review/{findings_v2,card_convert,cluster,cluster_cmd,manifest,manifest_cmd,verify_cmd}.py`, the six `review-panel.reflect-*.json` templates, `cli/reflect/panel_lint.py`, `scripts/reflect_*.py`) is master code, not branch code.

---

## 1. Inventory

R = reflect-specific; U = reusable by any panel consumer as is; U* = reusable after removing reflect assumptions.

| Path | Lines | Purpose | R / U |
|---|---|---|---|
| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` | 2033 | The reflect protocol. Panel-relevant parts: §3.1 `--t2-engine` flag (:87), §4 Wave 0 step 0.5 alias routing (:232-246), §4.3 Step 3B.0 brief materialization (:303-307), §4.3a engine selection rules D1-D5 + shadow steps 1-10 (:309-349), §5.4 `tier_decision.yaml` engine keys (:447-471), §7.1 rotation + executor exclusion (:644-660), §9.1 stable contract 1.8.0 (:724+), §9.2 telemetry incl. `telemetry:` panel block (:940-989), §11.3 calibrator disjoint-set rule (:1240-1262) | R (protocol). The shadow steps are the only written "panel consumer recipe" and are a template for other consumers (U*) |
| `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` | 116 | Brief template (exactly three sections: T1 card excerpt, Grounding hunks, Coverage slice) and rotation table; holds the shadow findings-v2 instruction line (:39) | R; the findings-v2 instruction line is U* (lens and roles are reflect-pre-specific) |
| `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md` | 177 | Calibrator 5-dimension rubric and the disjoint-set pseudocode (:133-169) | R |
| `src/superclaude/agents/reflect-reviewer.md` | 151 | Read-only reviewer agent (tools: Read, Grep, Glob, auggie, 4 codegraph tools; `model: sonnet`, `permissionMode: plan`) (:1-9); 4-class deviation taxonomy (:21-26); markdown Deviations table output with HIGH/MEDIUM/LOW (:69-99); advisory Correctness-gaps channel (:101-115) | R (taxonomy, UC-2 wording); the read-only allowlist pattern is U |
| `src/superclaude/agents/confidence-calibrator.md` | 159 | Blind re-grader; frontmatter tools: Read only, `model: sonnet` (:1-9). Written for sc:troubleshoot (6-dimension rubric, `rubric_path` = `refs/escalation-rubric.md`) (:3, :15, :48) | U* (generic by design, :16 "Delegable by any other skill"); reflect reuses it with a different rubric |
| `src/superclaude/agents/evidence-validator.md` | 150 | Final gate that re-Reads every file:line citation. Body NOT read in this slice (UNVERIFIED beyond the agent listing description) | U (per its own description) |
| `src/superclaude/cli/reflect/panel_lint.py` | 366 | Read-only lint of a panel run dir against frozen 1.8.0: L0 parse, L1 version, L2 unknown top-level keys, L3 `merge_method` legal values, L4 convergence-score type, L5 load-bearing booleans, L6 EV-1 merge gate on disk, L7 parity with matched legacy contract, B bump rule (:302-366). `STABLE_FIELDS_1_8_0` (110 keys) and `TELEMETRY_FIELDS` (27 keys) are copied from SKILL.md §9.1/§9.2 (:33-185) | R (bound to the reflect contract) |
| `src/superclaude/cli/review/findings_v2.py` | 304 | findings-v2 = findings-v1 container + optional `citations`, `lens`, `deviation_class`, `reflect_category`, `coverage_rows`, `self_confidence`, `channel` (:24-48, :84-187) | U (lens enum already includes `spec`) |
| `src/superclaude/cli/review/card_convert.py` | 517 | Converts recorded reflect cards (YAML or markdown table) to findings-v2 with a deterministic word map (:1-47) | R (reflect card shapes only) |
| `src/superclaude/cli/review/cluster.py`, `cluster_cmd.py` | 487, 197 | `review cluster`: cross-reviewer clustering (`same_defect_v2`), `cluster_agreement`, `calibrated_findings n/m`, `--kept` pass. Internals not read here (UNVERIFIED; another slice) | U |
| `src/superclaude/cli/review/manifest.py`, `manifest_cmd.py` | 534, 240 | `review manifest init/advance`: stage machine resolved..published with per-reviewer attempts and output hashes. Only seen via `test_the_skills_manifest_recipe_runs_as_written` | U |
| `src/superclaude/cli/review/verify_cmd.py` | 184 | `review verify-citations`: citation pre-check against the snapshot (flags only, drops nothing). Not read here | U |
| `src/superclaude/cli/review/panel.py` | 707 | Template resolution; reflect additions: `ExclusionExhausted` (:57), Fable/tier0 validation for reflect templates (:76-150), `hard_exclude`/`strict_distinct` (:508-534, :574-705) | U (the reflect checks are template-scoped) |
| `src/superclaude/cli/review/data/review-panel.reflect-{pre,pre-x2,post,post-x2,enterprise,lite}.json` | 12-13 each | Reflect panel templates, all `distinct_across_slots: true`, `apply_to: ["first"]`. `reflect-pre` = t1b fixed + t4 random + t1a random | R (data) |
| `scripts/reflect_cluster_pairs.py` | 559 | Stage 0 exit: writes a 50-pair human check sheet of cluster_v2 merged/apart verdicts from recorded pre-* cards (`sample`) and scores the owner-filled sheet (`score`). Inputs `.dev/reflect/pre-*/reviewer-cards`, snapshot. Reads files only (:1-35) | R (study tool) |
| `scripts/reflect_consumer_inventory.py` | 535 | Contract compatibility gate item 1: counts contract words (`merge_method`, `contract_version`, diversity fields, `reviewer_cards`, `citations_dropped`, ...) in src/tests/scripts/eval-workspaces/docs and classifies each hit file as producer/validator/consumer (:1-35). Output `consumer-inventory.md` | R |
| `scripts/reflect_stage0a_replay.py` | 896 | Stage 0a: converts recorded pre-* cards to findings-v2, clusters them, reports conversion share (descriptive since 2026-11-12, reference 0.90, gates nothing), agreement with merged verdict, causes of null convergence scores (:1-40) | R |
| `scripts/reflect_verdict_replay.py` | 184 | Stage 2 entry check: replays recorded 1.8.0 pre contracts through `contract.derive_verdict(expected_tier=2, child_rc=0, both allow_single_vendor)`; exit 1 on any new degraded reason in the shadow set (:1-35). Writes nothing | R |
| `scripts/reflect_shadow_exit.py` | 410 | Stage 2 exit aggregator: needs 20 published shadow manifests; per run recomputed parity, MALFORMED audit rows = 0, `panel_lint`, verdict replay; aggregate EV-1 rate no higher than legacy. Exit 0 PASS / 1 FAIL / 3 INSUFFICIENT-RUNS / 2 usage (:1-35) | R |
| `tests/cli/reflect/test_shadow_skill_contract.py` | 307 | Pins the shadow text: §9.1 block byte-identical to HEAD (:42-49); working-tree SKILL.md diffs vs HEAD only in §3.1/§4.3a/§5.4/§9.2 (:52-75); no new `src/superclaude` hits in the skill dir (:78-98); manifest recipe runs as written (:104-140); brief has exactly 3 sections and the shadow line sits inside T1 excerpt (:146-165); header fields + legacy authority wording (:168-180); calibrator line is shadow-only and parseable by `cluster_cmd._embedded_calibration` (:183-196); brief line carries the schema and its example parses with `findings_v2.parse_block` (:199-218); shadow steps pin header model / merged-verdict.yaml / first-pass metric (:221-238); fixture parity recompute (:243-307) | R |
| `tests/cli/reflect/test_panel_contract_lint.py` | 409 | Pins `STABLE_FIELDS_1_8_0`/`TELEMETRY_FIELDS` to SKILL.md §9.1/§9.2 in order (:90-104), sizes 110/27 (:107-114), pass/fail cases P1-P9, F1-F20 | R |
| `tests/cli/reflect/test_shadow_exit_script.py` | 319 | Aggregator cases (20 clean pass, malformed fails, 12 insufficient, parity record vs recompute, frozen tier file, EV-1 rate, exit codes); the branch changed the live-repo test to "reports without crashing" (:292-300) | R |
| `tests/cli/reflect/test_verdict_replay_script.py` | 190 | Self-replay zero diffs, new degraded reason exits 1, documented `derive_verdict` args | R |
| `tests/cli/reflect/test_reviewer_brief_constraints.py` | 70 | `## Constraints (READ-ONLY)` in reviewer-spec; live-exec prohibition in Step 3B.0; `reflect-reviewer` named in BOTH §7.1 and reviewer-spec Composition (:35-70) | R |
| `tests/cli/reflect/test_reviewer_readonly_tools.py`, `test_reviewer_finding_parity.py` | 115, ~100 | `reflect-reviewer` tools line excludes all mutators; restricted toolset reaches seeded surfaces (test names only read) | R (pattern U) |
| `tests/review/test_review_panel_reflect_profile.py`, `test_review_reflect_templates.py`, `test_review_card_convert.py`, `test_review_findings_v2.py`, `test_review_cluster*.py`, `test_review_manifest.py`, `test_review_verify_citations.py`, `test_reflect_{cluster_pairs,consumer_inventory,stage0a_replay}.py` | see #519 stat | Kernel and template tests (names from `git show --stat d2d8a2d16`; contents NOT read, UNVERIFIED) | mixed |

### 1.1 What the two skill-fix commits changed (`git diff 9874d63fb~1..c2e3347d3 -- src tests`)

Only 4 files: SKILL.md (all hunks inside §4.3a shadow steps 2, 4, 7, 10 and the §9.2 `findings_block_compliance_rate` comment), `refs/reviewer-spec.md` (the shadow instruction line, :39), `tests/cli/reflect/test_shadow_exit_script.py`, `tests/cli/reflect/test_shadow_skill_contract.py`.
- Step 2: card header `model:` is the pin copied from `panel/resolution.json` `reviewers[N].model`; the harness-reported model goes on a separate `model_observed:` line (SKILL.md:341).
- Step 4: `findings_block_compliance_rate` is measured on the first parse, before the re-ask; the orchestrator never edits or remaps findings (SKILL.md:343).
- Step 7: the orchestrator writes `<output>/adversarial/merged-verdict.yaml` (EV-1 reads that exact path; `adversarial/adversarial/` copies do not count) (SKILL.md:346).
- Step 10: confirm `reviewer_personas`/`reviewer_models` are present and no non-stable top-level key exists (SKILL.md:349).
- reviewer-spec.md:39: the brief line now spells out the full findings-v2 schema, the exact heading `## Findings block` and an example line.
- Tests: two new pins (`test_the_reviewer_brief_line_carries_the_schema_and_its_example_parses`, `test_shadow_steps_pin_the_header_model_the_verdict_file_and_the_first_pass_metric`) and the live-repo shadow-exit test relaxed to any documented exit code.

### 1.2 Current Stage 2 state (ran `uv run python scripts/reflect_shadow_exit.py`, read-only, 2026-11-13)

`OVERALL: FAIL (shadow runs 13 of 20)`, exit 1. 42 legacy runs in the baseline, 0 new degraded reasons. Mean findings-block compliance 0.704 over 9 runs; `cluster_agreement` min/median/max 1.000; 9 runs with unknown executor class; 0 two-of-three shortfalls. Failures: EV-1 rate above legacy; parity fails in 6 runs; lint/manifest problems in 9 runs (examples: shadow07 has top-level keys `memory_status`, `notes`, `zero_drop_flag` outside 1.8.0; shadow05/07 have neither `adversarial/merged-verdict.yaml` nor a loud fallback; shadow08/09 have no contract). Which runs predate the two fix commits is UNVERIFIED.

---

## 2. The reflect Tier 2 pipeline today

All citations are `src/superclaude/skills/sc-reflect-protocol/SKILL.md` unless another file is named. This is a protocol executed by the orchestrating model; the only code in the loop is the `superclaude review ...` CLI (shadow only), `panel_lint.py` and the replay scripts (offline). There is no Python orchestrator for UC-1 Tier 2 [CODE-VERIFIED by absence: `cli/reflect/` holds config/runner/ensemble/contract/fallback/models/_diversity/panel_lint; `ensemble.py` is the headless builder named by `reflect_consumer_inventory.py:32`, its relation to the in-session Wave 3 NOT read, UNVERIFIED].

### 2.1 Order of decisions before Tier 2

1. Wave 0 step 0.5: count distinct models named by `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` (unset = built-in alias); 1 -> T1 only, 2 -> 2 reviewers, 3+ -> 3 reviewers (:232-240). Step 0.5b resolves executor class (flag / env / log heuristic / unknown) (:648).
2. Step 0.9 budget pre-flight (:264-274).
3. Waves 1-2: T1 card (`<output>/t1-card.md`, reviewer-spec.md:39), coverage map, blind calibration of the T1 card (Wave 1D), rubric (§5.3), `tier_decision.yaml` (:447-467).
4. Only then `--t2-engine` is read, at the start of Wave 3 (:313; rules D1, D2 :317-318).

### 2.2 Legacy mode (`--t2-engine legacy`, the default; authoritative in every mode)

| Step | Role / who | Input | Output / file | Cite |
|---|---|---|---|---|
| 3A compose | Orchestrator | rotation table x alias count x executor exclusion | N reviewers (2-3), each = `reflect-reviewer` agent + model class + persona (analyzer, qa, refactorer / architect) | §7.1 :644-658; reviewer-spec.md:92-110 |
| 3B.0 briefs | Orchestrator | T1 card slice, Wave 1A grounding hunks, coverage slice, codegraph run state | `<output>/reviewer-briefs/reviewer-<N>.md` (exactly 3 sections) | :303-307; reviewer-spec.md:21-78 |
| 3B dispatch | Reviewers: `reflect-reviewer` (read-only tools, `permissionMode: plan`) | its brief (no live-exec instructions, L4) | Returned markdown Deviations table + Adherence summary + optional Correctness gaps; orchestrator persists to `<output>/reviewer-cards/reviewer-<N>-card.yaml` (the Wave 4 call names `.yaml` cards, :695) | `agents/reflect-reviewer.md:48-115`; :305 |
| 3C calibrate | Calibrator: `confidence-calibrator`, one per card, in parallel; class chosen by disjoint-set rule | the card only (stripped of formation context) + `refs/reflection-rubric.md` (5 dims) | card-level calibrated confidence `C`; `calibrator_diversity`; fallback `calibration: inline-fallback` | §11.3 :1240-1262; §7 :631; reflection-rubric.md:9-13, :133-169; error row :1469 |
| 3D distill | Orchestrator | calibrated cards | candidate verdicts | :160 (one-line wave map only; detail NOT found in the read ranges, UNVERIFIED) |
| 4 merge | Debate judge: `sc-adversarial-protocol` Mode A `--compare` of the card files, `--depth standard --focus correctness,coverage,deviation-classification`; judge model chosen by sc-adversarial, not pinned by reflect | the reviewer card files | `<output>/adversarial/` incl. `merged-verdict.yaml`; `convergence_score` routing >=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL; `artifacts_dir` renamed to `adversarial_artifacts_dir` | §8 :681-705; :660 |
| 4 exit EV-1 | Orchestrator, on disk | `merged-verdict.yaml` with `merge_method: adversarial` AND `reviewer-cards/` count >= resolved reviewers (min 2), OR a corroborated F2/F3 fallback | MALFORMED audit row + up to 2 retries of Waves 3-4 | :714; lint L6 `panel_lint.py:246-299` |
| 5.0 probe | Orchestrator | `Skill('sc-adversarial-protocol', '--help')` | F1 retry, F2 `merge_method: single-reviewer-fallback` (highest-calibrated single reviewer), F3 `adversarial_unavailable: true` | :353-359 |
| 5 gate | Evidence validator: `evidence-validator` agent | every cited file:line of the draft (sampled under the §11.5 budget policy) | drops; `citations_dropped` >0 forces `status: partial`; zero drops audit-logged as suspect | §11.2 :1227-1238 |
| 5 publish | Orchestrator (legacy writers) | everything above | `REPORT.md`, `return-contract.yaml` (1.8.0), `audit.log` | §9 :718-724 |

### 2.3 Shadow mode (`--t2-engine shadow`, UC-1 only; accepted and ignored in UC-2 until Stage 5) (:311)

Shadow runs **next to** the legacy steps above; it changes no verdict, no stable field, no `merge_method`; every panel file goes under `<output>/panel/` and every field under `telemetry:` (:338, :349). Each step ends with `superclaude review manifest advance --out <output> --stage <stage>` (:338).

| # | Step | Command / action | Files written | Manifest stage | Cite |
|---|---|---|---|---|---|
| 1 | Resolve and freeze | `review panel resolve --template @reflect-pre --run-id <id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct`; on anchor `ExclusionExhausted` retry once with `@reflect-pre-x2` (`anchor_replaced: true`); then `review manifest init ... --schema-id review-panel/1 --schema-id findings-v2 --t2-engine-requested shadow --t2-engine-effective shadow` | `panel/resolution.json` (verbatim stdout), `panel/manifest.json` | `resolved` (payload `reviewers_requested`, `reviewers_resolved`) | :340 |
| 2 | Parity | compare ordered (persona, class) of resolution vs legacy rotation as run; orchestrator writes card headers `persona:`, `model_class:`, `model:` (= pin), optional `model_observed:` | (recorded) `panel_parity` | - | :341 |
| 3 | Briefs and dispatch | legacy briefs + one findings-v2 instruction line (reviewer-spec.md:39); legacy dispatch | per-attempt manifest records | `dispatched`, `collected` | :342 |
| 4 | Normalize | parse each card's `## Findings block`; first-parse compliance rate; one bounded re-ask; no orchestrator remapping | `panel/notes.md` (valid count after re-ask) | - | :343 |
| 5 | Calibration | legacy Wave 3C + one appended calibrator line asking a `calibration: per_finding:` map; Fable / Tier 0 never picked as calibrator | `panel/cards/reviewer-<N>.md` = headers + findings block + `calibration.per_finding` yaml | `calibrated` | :344 |
| 6 | Cluster + citation pre-check | optional `panel/coverage.json`; `review cluster panel/cards --snapshot ...` and `review verify-citations --cards ... --root ...` (flag only; flagged citations join the validator re-read set) | `clusters.json` etc. (names per kernel, UNVERIFIED), `cluster_agreement`, `calibration_coverage n/m` | `clustered` | :345 |
| 7 | Debate (legacy, unchanged) | then write `adversarial/merged-verdict.yaml` from the debate output; record `debate_skipped_similar`, `judge_identity` (or `unknown`), `judge_class_collision` | `adversarial/merged-verdict.yaml`, `panel/notes.md` | `debated` | :346 |
| 8 | After evidence validator | kept ids as `reviewer-<N>:<id>`; `review cluster ... --kept panel/kept-ids.txt` (clusters_kept pass) | `panel/kept-ids.txt` | `validated` | :347 |
| 9 | Identity | `identity_source: observed | requested-pinned`; compare `reviewer_model_self_report` with the pin | `identity_mismatch_suspected` in telemetry and `panel/notes.md` | - | :348 |
| 10 | Publish | confirm stable keys; after legacy writers, `manifest advance --stage published` records hashes | (none rewritten) | `published` | :349 |

Engine values are also written to `tier_decision.yaml` (`t2_engine_requested`, `t2_engine_effective`, `panel_fallback_reason`; audit keys, not contract fields) (:464-469). Telemetry fields: §9.2 `telemetry:` block (:969-988), 19 keys.

### 2.4 Roles summary (who plays each role today)

| Role | Legacy | Shadow addition | Reusable? |
|---|---|---|---|
| Reviewers | `reflect-reviewer` agent x 2-3, model class by rotation, persona by brief | same dispatch; model pin from `resolution.json`; findings-v2 block appended | agent is reflect-specific (taxonomy, UC-2 wording); read-only allowlist pattern reusable |
| Calibrator | `confidence-calibrator` per card, disjoint-set class rule, card-level `C` | adds `per_finding` confidences | agent generic (built for troubleshoot); rubric reflect-specific |
| Debate judge | `sc-adversarial-protocol` Mode A, judge not pinned | records judge identity (often `unknown`) | already a shared skill |
| Evidence validator | `evidence-validator`, final gate, decides drops | gets the `verify-citations` flagged set added | already shared |
| Orchestrator | the main session following SKILL.md | runs `superclaude review` CLI steps, manifest | recipe reflect-specific; CLI reusable |
| Clustering / merge script | none (the debate merges) | `review cluster` (telemetry only, never routes) | reusable kernel |

---

## 3. Reflect finding shapes and their mapping to findings-v1 / findings-v2

### 3.1 Shapes that exist today

| Shape | Where | Fields | Cite |
|---|---|---|---|
| Legacy reviewer card (UC-2 audit) | returned by `reflect-reviewer`, persisted as `reviewer-cards/reviewer-<N>-card.yaml` | markdown table `# / Category / Location / What diverged / Evidence (file:line) / Severity`; Category = one of 4 deviation classes; Severity HIGH (regression or load-bearing invariant break), MEDIUM (unjustified drift with real impact), LOW (cosmetic / minor drift); Adherence summary counts; separate advisory `Correctness gaps` table (never gates) | `agents/reflect-reviewer.md:69-115` |
| Recorded card variants | `.dev/reflect/pre-*/reviewer-cards/` | 4 observed shapes: yaml-blocking-minor, yaml-other-severity (medium/low/should-fix/P1-P3, optional `deviation_class`), markdown-table, unlisted. So recorded cards do NOT follow one schema | `cli/review/card_convert.py:3-13` |
| Grounding gaps | `grounding-gaps.yaml` (§10.6) | evidence-insufficient findings, not a 5th class | SKILL.md:1044, :1137 heading (body not read, UNVERIFIED detail) |
| Contract-level deviation output | §9.1 | `deviation_count_by_class {authorized, necessary, drift, regression}`, `per_task_verdicts[].deviation_class: authorized|necessary|drift|regression|none`, flags `regression_present`, `unauthorized_deviation_present` | SKILL.md:755-759, :860-867, :851-858 |
| Shadow findings-v2 block (UC-1 pre only) | end of each card after the exact heading `## Findings block` | `id`, `severity` CRITICAL/MAJOR/MINOR, `blocking` bool (MINOR never blocking), `category` (contradiction, data-loss, missing-requirement, other, safety, unpassable-check), `lens: "reflect-pre"`, `claim` <=300, `refs`, `citations` 1-8 `{role plan|spec, path, line_start, line_end, quote?}`; then a `reviewer_model_self_report` line | `refs/reviewer-spec.md:39` |
| Per-finding calibration (shadow) | `panel/cards/reviewer-<N>.md` | fenced yaml `calibration: per_finding: {F1: 0.85}`; never inside the finding line (`calibrated_confidence` is rejected in a findings-v2 line) | SKILL.md:344; `findings_v2.py:96-97` |

### 3.2 What findings-v2 already carries for reflect (code, `src/superclaude/cli/review/findings_v2.py`)

- Container = findings-v1 container with fence info `findings-v2`; a findings-v1 line with only V1 keys passes unchanged (:1-7, :24-34). [CODE-VERIFIED]
- `citations` may replace `anchor` (a finding needs one or the other) (:122-134); roles `plan, spec, source, test, diff, artifact` (:35).
- `lens` in `spec, reflect-pre, reflect-post` (:36, :140-145). The `spec` lens is the hook for spec review.
- `deviation_class` in `authorized, necessary, drift, regression, none`; required only when lens is `reflect-post` (:38, :147-153).
- `reflect_category` in `ordering, acceptance, coverage, contradiction, risk, deviation`, each tied to allowed v1 categories (`deviation` and `ordering` map to `other`, `risk` to `safety|other`) (:41-48, :155-164). With `reflect_category` set, `blocking` must equal `severity != MINOR` (:161-162); `deviation` needs `deviation_class` (:163-164).
- `channel` in `defect, grounding-gap, advisory` (absent = defect) (:37, :184-193). This is where reflect's Grounding Gaps and advisory Correctness gaps fit.
- `coverage_rows` checked against the reviewer's assigned Coverage slice (:166-176); `self_confidence` 0-1 (:178-182).

### 3.3 Mapping and where it fails

| Reflect concept | findings-v1 | findings-v2 | Status |
|---|---|---|---|
| Deviation class (4 + none) | no field; would collapse to `category: other` | `deviation_class` | v1: lost. v2: carried |
| "Authorized expansion" / "Necessary deviation" words in recorded cards | n/a | `card_convert` matches only the single words `authorized`/`necessary` (`_word` lowercases the whole string, `card_convert.py:103-104`, match at :203); the two-word labels the agent is told to use (`reflect-reviewer.md:23-24`) are NOT matched, so those rows get no `deviation_class`. `drift`/`regression` match | Mapping gap [CODE-VERIFIED] |
| HIGH | severity MAJOR + blocking (via converter) | same | maps (`card_convert.py:36-37`) |
| MEDIUM ("unjustified drift with real impact") | MINOR, not blocking (converter) | same | **Verdict-changing**: reflect treats unjustified Drift as `unauthorized_deviation_present` (load-bearing bool, `contract.py:47-53`), but the converter makes it non-blocking. The hand-off merge risk "HIGH/MEDIUM/LOW is not a gate" is confirmed |
| LOW | MINOR | MINOR | maps |
| Regression | category `other` (or `safety`/`data-loss` by judgement) | `deviation_class: regression`; blocking per reviewer | v2 keeps it; no rule forces Regression to be blocking |
| Grounding Gap | no place (would be dropped or mis-filed) | `channel: grounding-gap` | v2 only |
| Correctness gap (advisory, never gates) | no place | `channel: advisory` | v2 only; no rule yet that advisory implies `blocking: false` (not in `check_finding`) [CODE-VERIFIED by reading :84-187] |
| Evidence `file:line` | `anchor` (12-200 chars, exact-substring locate) | `citations` with line ranges; `review verify-citations` flags but never drops | v1 anchor check is replaced, not kept; the evidence-validator stays the only dropper (SKILL.md:345) |
| Card-level calibrated confidence `C` | none | none in the line; per-finding map is a card sidecar | v1: none; v2: separate block |
| UC-1 coverage findings (unmapped requirement) | `missing-requirement` | `missing-requirement` + `coverage_rows` | maps |
| Rubric deviation vocabulary | - | - | `refs/reflection-rubric.md:39` uses `{Aligned, Refinement, Drift, Regression}`, a different 4-word set from SKILL.md §10 and the agent. Internal inconsistency to resolve before any mapping is frozen |

Conclusion for Q2: findings-v2 (not v1) is the format reflect can live on; it already has `deviation_class`, `lens`, `channel` and `citations`. What is missing is a written **blocking rule per lens**: for `reflect-post`, which deviation classes are blocking (Regression and Drift, by the contract's two load-bearing flags) and that `authorized`/`necessary` and `channel: advisory` are never blocking. Today that rule exists only in prose and in the contract builder, not in the parser or the merge.

---

## 4. Answers to the hand-off questions 2-5

**Q2. Finding format and mapping from the 4 deviation categories to findings-v1 categories.** See section 3. findings-v1 has no field for the deviation class; the only v1 category that fits Drift / Authorized / Necessary is `other`, and Regression fits `other`, `safety` or `data-loss` by judgement. findings-v2 already carries `deviation_class` (required under `lens: reflect-post`) (`findings_v2.py:147-153`) and `reflect_category: deviation -> category other` (:41-48). The unified panel should use findings-v2, with a lens-specific blocking rule. Two converter defects must not be imported: MEDIUM -> non-blocking (`card_convert.py:36-37`) and two-word deviation labels not recognised (:203).

**Q3. Calibrator scope; class disjointness vs `distinct_across_slots`.**
- Scope: legacy calibrates the **whole card** (one `C` per card from 5 dimensions; card is its only input) (SKILL.md:1242, :1260; reflection-rubric.md:11). Shadow adds a per-finding map keyed by the card's findings-v2 ids (SKILL.md:344), which `review cluster` reads (`calibrated_findings n/m`, :345). It never applies to findings-v1 anchors or to ledger rows. Stage 2 evidence: mean compliance 0.704 and the calibration-id mismatch text in step 6 (:345) show the per-finding map is fragile.
- Disjointness: reflect's rule is by **model class** across three pools: executor not in reviewers (§7.1 :648), calibrator not in reviewers (§11.3 :1244-1256), pairwise disjoint executor/reviewers/calibrator (:1258). Panel `distinct_across_slots` is by **model id** among reviewer slots only (`panel.py:633`; `strict_distinct` turns the exclude set into a hard exclude, :515-519) plus `--hard-exclude-class` for the executor (SKILL.md:340; `panel.py:700-705`). The panel code selects **no calibrator** (no `calibrat` hit in `panel.py`; hits only in manifest/cluster/findings_v2). So they do not conflict in code, but they measure different things: two ids of one class (`gpt-6.1-sol` and `gpt-6-luna`, both class `gpt`, `review-tiers.default.json` classes) pass `distinct_across_slots` and fail reflect's class rule.
- Practical conflict: in `anthropic-only`, `@reflect-pre` resolves to sonnet, haiku, opus (template description, `review-panel.reflect-pre.json`), so the calibrator disjoint set `{opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewers` = `{qwen, kimi, deepseek}`, none launchable (`launch` lists only opus/sonnet/haiku/fable). The calibrator is therefore always `degraded` (reflection-rubric.md:157 Example C), and Fable is banned as calibrator in shadow (SKILL.md:344). The §11.3 class list also does not match the tier file classes (`kimi`, `deepseek` absent from the tier file; `gpt`, `muse`, `glm`, `grok` absent from §11.3).

**Q4. What reflect gives reviewers for the driving spec (D8).** The brief has exactly three sections (reviewer-spec.md:31-33, pinned by `test_the_brief_template_has_exactly_three_sections`). In UC-1 the **spec body itself** is injected as `## Grounding hunks` entries with `file:line-range` H3 refs: whole file when <=400 lines, else one hunk per top-level section covering 100% of the spec, **for the `qa` persona only** (reviewer-spec.md:55). Other personas get the T1 card slice, their grounding hunks and their coverage slice. The `reflect-reviewer` agent definition also lists `spec_path`, `tasklist_path`, `diff_scope` as Task inputs (`reflect-reviewer.md:50-57`) and has Read, so it can open the spec from its grounding root; whether the orchestrator passes those paths in the Task prompt in UC-1 is UNVERIFIED (the brief template does not name them). Reuse: the "inject the driving document as cited hunks" mechanism is reusable and stronger than a bare `{{CANDIDATE}}` placeholder, because the hunks carry line refs the evidence-validator re-reads; for a panel it should go to every reviewer, not only `qa`.

**Q5. Is the rotation table (sonnet / haiku / qwen|kimi|deepseek else opus) still valid?** The table text is stale, but the effective behaviour already avoids Qwen:
- Qwen is chosen only when one of the three `ANTHROPIC_DEFAULT_*_MODEL` aliases names a Qwen model (§7.1 :655; vendor by alias-name heuristic, step 0.6 :260). Coder workspaces no longer set these variables, so they resolve to Claude built-ins (:232) and the third slot is opus.
- The panel template `@reflect-pre` (and `-post`, `-enterprise`) uses tier1b/tier4/tier1a, none of which lists `Qwen3.8-max` (`review-tiers.default.json` aliases). Only `@reflect-lite` (variant arm) uses `tier2`, which does list Qwen3.8-max.
- So: remove `qwen | kimi | deepseek` from §7.1, reviewer-spec.md:97 and the §11.3 calibrator class list, and let the panel template be the single rotation source. Any edit to §7.1 must keep `reflect-reviewer` named there and in reviewer-spec `## Composition` (`test_reflect_reviewer_repointed_in_both_rotation_tables`). That Qwen was disqualified is the hand-off's claim and is not re-verified here.

---

## 5. Constraints the unified design must respect

| # | Constraint | Enforced by | Cite |
|---|---|---|---|
| C1 | §9.1 stable contract block is byte-identical and `contract_version: "1.8.0"` | `test_stable_contract_block_and_version_are_byte_identical_to_head` (compares the working tree with **HEAD**, so it guards uncommitted edits; once a change is committed it no longer compares against master) | `tests/cli/reflect/test_shadow_skill_contract.py:42-49` |
| C2 | No top-level contract key outside the 110 stable + 27 telemetry names; all panel fields nested under `telemetry:` | `panel_lint` L2 + B bump rule; constants pinned in order to SKILL.md | `panel_lint.py:316-321, :360-365`; `test_panel_contract_lint.py:90-114`; SKILL.md:349 |
| C3 | `merge_method` legal values exactly `adversarial`, `single-reviewer-fallback` (EV-2). A panel/script merge needs a new value, which means a contract version bump; `--t2-engine panel` is explicitly deferred to "Stage 3" | `panel_lint.py:184, :328-334`; SKILL.md:837, :87 |
| C4 | EV-1: Wave 4 is complete only with `adversarial/merged-verdict.yaml` (`merge_method: adversarial`) + enough `reviewer-cards/`, or a corroborated loud fallback | SKILL.md:714; `panel_lint.py:246-299`; testability map SKILL.md:1955 |
| C5 | Legacy engine stays default and authoritative; with `legacy` the panel code is never called; shadow is UC-1 only until Stage 5 | SKILL.md:87, :311, :338 |
| C6 | Working-tree SKILL.md edits (vs HEAD) only under §3.1 (lines must contain `--t2-engine`), §4.3a, §5.4, §9.2 | `test_skill_changes_are_confined_to_the_allowed_sections` (`test_shadow_skill_contract.py:52-75`). A unified design that edits §7.1, §11.3 or §8 must change or retire this test in the same change |
| C7 | Brief has exactly three sections; shadow line lives inside `## T1 card excerpt`; legacy briefs unchanged | `test_shadow_skill_contract.py:146-165`; reviewer-spec.md:31-39 |
| C8 | Shadow text needles pinned (header fields, "authoritative and unchanged", `kept-ids.txt`, `judge_class_collision: unknown`, calibrator line once, brief-line schema words + parseable example, merged-verdict path, first-parse metric, `reviewer_personas`/`reviewer_models`) | `test_shadow_skill_contract.py:168-238` |
| C9 | `reflect-reviewer` keeps a mutator-free `tools:` line and stays named in both rotation tables | `test_reviewer_readonly_tools.py`; `test_reviewer_brief_constraints.py:58-70` |
| C10 | Verdict replay: zero new degraded reasons vs the 42-run legacy baseline; Stage 2 exit needs 20 clean shadow runs (today FAIL, 13 of 20) | `scripts/reflect_verdict_replay.py`, `scripts/reflect_shadow_exit.py`; section 1.2 |
| C11 | Reflect templates may not use Fable models or tier0, max 3 reviewers | `panel.py:76-150` |
| C12 | Only `anthropic-only` can launch; `gateway` has `launch: {}` so every gateway cell is rule D4 fallback | `review-tiers.default.json` environments; SKILL.md:320 |
| C13 | Source of truth is `src/superclaude/`; `.claude/` is sync output, never staged | CLAUDE.md (project) |
| C14 | Installed primitives must not reference `src/superclaude/...`; skill dir may not gain new hits | CLAUDE.md; `test_no_new_src_superclaude_hit_in_the_skill_directory` (`test_shadow_skill_contract.py:78-98`) |
| C15 | Reviewers stay read-only (L1 allowlist, L4 no live-exec instructions in briefs); verification only via orchestrator hunks | SKILL.md:305; `reflect-reviewer.md:36-40` |
| C16 | Contract consumers outside reflect (wrapper `derive_verdict`, sprint routing, promotion gate condition 9 on null convergence) read `merge_method` first | SKILL.md:707-712; `contract.py:138`; `reflect_consumer_inventory.py` |

---

## 6. Suggested Phase 2 deep-investigation assignments

1. **Blocking rule per lens.** Read `cli/reflect/contract.py` (`derive_verdict`, `_degraded_reason`, load-bearing bools) and SKILL.md §10.1-10.7 + `refs/deviation-taxonomy.md`; write the exact rule that turns findings-v2 (`deviation_class`, `channel`, severity) into reflect's `regression_present` / `unauthorized_deviation_present` and into a panel `blocking`. Include the MEDIUM-drift case and the two-word label gap in `card_convert.py`.
2. **Calibrator as a panel role.** Read `agents/confidence-calibrator.md` fully, `refs/reflection-rubric.md`, and `cli/review/cluster.py` calibration handling; decide whether calibration becomes a panel step (per finding, class-disjoint, chosen by the tier file) and how §11.3's class list maps to tier-file classes. Quantify fragility from recorded `panel/cards/*` (`calibration_coverage` values).
3. **Merge path: debate vs script.** Compare `sc-adversarial-protocol` Mode A outputs in recorded runs (`.dev/reflect/pre-*-shadow*/adversarial/`) with `review cluster` clusters (cluster_agreement 1.000 in all 9 runs); decide whether Stage 3 `panel` replaces the debate (needs a `merge_method` value and a contract bump, C3) or keeps it as the judge.
4. **Why Stage 2 fails today.** Per failing shadow run (section 1.2), classify each failure as harness defect, skill-text defect fixed by 9874d63fb/c2e3347d3, or real panel defect. Owner of these runs is this session; evidence in commit 792cf8c52.
5. **Driving-document delivery (D8) as a shared mechanism.** Trace how the orchestrator actually passes `spec_path` to `reflect-reviewer` in UC-1 runs (recorded `reviewer-briefs/`), and design one brief placeholder plus grounding-hunk injection that tasklist review and spec review can share.
6. **UC-2 / `reflect-post` readiness.** `review-panel.reflect-post*.json` exist but SKILL.md ignores the engine in UC-2 until Stage 5; check `findings_v2` `reflect-post` requirements against what `reflect-reviewer` actually returns (markdown table) and the recorded post-* cards.
7. **Test-pin migration plan.** List every test in section 5 that a unified panel would break, and the replacement assertion (especially C1 and C6, which compare against HEAD).

---

## 7. Gaps and questions

- **UNVERIFIED** Wave 3D "distill candidate verdicts" detail; only the one-line wave map (SKILL.md:160) was read.
- **UNVERIFIED** `evidence-validator.md` body, `cluster.py`, `manifest.py`, `verify_cmd.py`, `ensemble.py` internals; and the `tests/review/*` reflect test contents.
- **Inconsistency [CODE-CONTRADICTED within docs]:** the §7 delegation-map row says `reflect-reviewer` is a UC-2 reviewer (SKILL.md:640) and the agent's Triggers say "UC-2 post-execution deviation audit" (`reflect-reviewer.md:15`), yet §7.1 says all Tier 2 reviewers are `reflect-reviewer` (:646) and shadow mode is UC-1 only. In UC-1 the agent is told to classify deviations of completed work that does not exist yet.
- **Inconsistency:** the calibrator agent is written for troubleshoot (6-dimension rubric, `refs/escalation-rubric.md`, `confidence-calibrator.md:3, :48`) while reflect uses a 5-dimension rubric (SKILL.md:631; reflection-rubric.md:9-13). How the reflect orchestrator overrides `rubric_path` is not stated in the read ranges.
- **Inconsistency:** rubric dimension 3 uses `{Aligned, Refinement, Drift, Regression}` (reflection-rubric.md:39) vs the 4-class taxonomy.
- **Inconsistency:** legacy cards are named `.yaml` in the Wave 4 call (SKILL.md:695) while the agent returns a markdown table (`reflect-reviewer.md:73-99`); recorded runs show 4 shapes (`card_convert.py:3-13`). There is no single legacy card schema.
- **Question:** does Stage 3 keep `sc-adversarial-protocol` as the merge judge (no contract bump) or replace it with a script merge (bump to a new contract version)?
- **Question:** should the tier file (`review-tiers.default.json`) become the only model source for reflect, retiring the `ANTHROPIC_DEFAULT_*` alias count of Wave 0 step 0.5 for Tier 2? Today both exist and can disagree (`panel_parity` false in 6 recorded runs).
- **Question:** who owns `cli/review/` going forward: the #346 review-loop owners or the reflect panel work? Both extended it (`panel.py` +206 lines in #519).
- **Risk:** C1 and C6 compare against HEAD, not master, so they do not protect the contract across commits; only `panel_lint` constants + `test_pinned_field_lists_match_skill_md` do.

---

## Summary

Reflect is already a partial consumer of the shared `superclaude review` kernel: in shadow mode (UC-1 only) it resolves a panel from `@reflect-pre`, collects findings-v2 blocks, calibrates per finding, clusters and pre-checks citations, all as telemetry next to the authoritative legacy path (`reflect-reviewer` x 2-3 by alias rotation, card-level blind calibrator, `sc-adversarial-protocol` debate, evidence-validator gate). findings-v2 already has the fields reflect needs (`deviation_class`, `lens`, `channel`, `citations`); what is missing is a written blocking rule per lens, a calibrator role inside the panel, and agreement on the merge path. The 1.8.0 contract, the EV-1/EV-2 rules and several HEAD-relative test pins constrain any change; Stage 2 currently reports FAIL (13 of 20 runs, parity and lint failures).
