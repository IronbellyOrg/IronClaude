# Research: Run recording: manifest, telemetry and audits

**Investigation type:** Code Tracer
**Scope:** `src/superclaude/cli/review/manifest.py`, `src/superclaude/cli/review/manifest_cmd.py`, `src/superclaude/cli/review/telemetry.py`, `src/superclaude/cli/review/telemetry_cmd.py`, `src/superclaude/cli/review/merge_cmd.py` (:71-118), `src/superclaude/skills/sc-reflect-protocol/SKILL.md` §9.2 (:940-989), E2 per-run records (`meta.json`, `cost.json`, `fallback.log`, `tools/run-reviewer.sh`) at commit 4a22d742, E2 audits A and D (`summary.md`, `audit.py`), `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py`, `scripts/reflect_shadow_exit.py`
**Status:** Complete
**Date:** 2026-11-13

Effort tags: [E1] = reflect Tier 2 panel kernel, shadow mode and model-combination experiment (branch ironbelly/shadow-runs); [E2] = tasklist review-panel evaluation study at commit 4a22d74213f93837d00c2c314075dd967b9a98e3; [E3] = #346 review loop on master (findings-v1, ledger, review merge/ledger/panel/telemetry CLI).

---

## 1. `src/superclaude/cli/review/manifest.py` (534 lines) [E1]

Origin: reflect (scope slice 02, section 1). Imports only stdlib (`hashlib, json, os, re, pathlib, typing`, :31-36). Imported by `manifest_cmd.py:16` and `scripts/reflect_shadow_exit.py` (checked in section 9).

### 1.1 Data model (schema `review-panel-manifest/1`, :38)

File location: `<out>/panel/manifest.json` (module docstring :1; `manifest_cmd._path` :19-20).

Top-level keys written by `new_manifest` (:111-150):

| Key | Meaning | Source line |
|---|---|---|
| `schema` | `"review-panel-manifest/1"` | :122 |
| `run_id` | caller-supplied string | :123 |
| `invocation` | integer, starts at 1, +1 on each resume with changed inputs | :124, :466 |
| `history` | list of earlier invocations `{invocation, input_tree_sha256, policy_sha256, state}` | :125, :451-459 |
| `t2_engine_requested`, `t2_engine_effective` | one of `legacy`, `shadow`, `panel` (`ENGINES` :51) | :126-127 |
| `frozen` | the seven `FROZEN_FIELDS` (:55-63): `snapshot_ref`, `snapshot_sha256`, `input_tree_sha256`, `template_sha256`, `tiers_sha256`, `brief_template_sha256`, `schema_ids` | :128 |
| `input_tree_sha256` | copy of `frozen.input_tree_sha256` | :129 |
| `policy_sha256` | sha256 of canonical JSON of `{template_sha256, tiers_sha256, brief_template_sha256, schema_ids}` (`policy_sha256` :97-108) | :130 |
| `state` | one of the nine `STATES` (:39-49) or `failed` (:50) | :131 |
| `stages` | map stage -> `{payload_sha256, outputs{name: sha256}, deps{prev, input_tree_sha256, policy_sha256}, invocation}` | :132-141, :317-326 |
| `attempts` | list of `{stage, reviewer_id, attempt_id, completion, payload_sha256, [superseded_by]}` | :142, :348-354, :383 |
| `reviewers_requested`, `reviewers_resolved` | null until `resolved` stage | :143-144, :307-316 |
| `reviewers_complete` | count of reviewers whose latest `collected` attempt is `complete` | :145, `_recount` :269-274 |
| `failure_reason` | set by `fail` | :396 |

Canonical hashing: `sha256_json` = sha256 of `json.dumps(sort_keys=True, separators=(",",":"))` (:87-90); `sha256_file` = sha256 of raw bytes (:93-94).

### 1.2 Stages

Linear pipeline `frozen -> resolved -> dispatched -> collected -> calibrated -> clustered -> debated -> validated -> published` (`STATES` :39-49) plus terminal `failed` (:50). `PER_REVIEWER_STAGES = ("dispatched", "collected", "calibrated")` (:53) are the only stages that take per-reviewer attempts. `advance_stage` (:277-328):
- rejects `frozen` and unknown stages (:280-281);
- requires `payload.outputs` to map names to 64-hex sha256 (:284-291);
- identical replay of an already-committed stage returns `False` (:293-296), different payload raises `Conflict` (:297-299) — note the replay check runs **before** the `failed` check (:300), so an identical replay on a failed run still returns `False` without error;
- enforces strict next-stage order via `_next_state` (:302-306); no stage can be skipped;
- the `resolved` payload must carry `reviewers_requested`/`reviewers_resolved` as non-negative ints with resolved <= requested (:307-316);
- writes `deps.prev` = previous stage's `payload_sha256` (`_prev_hash` :265-266), forming a hash chain.

`validate` (:192-253) checks schema, non-empty run_id, engines, the four 64-hex frozen hashes, `snapshot_ref`, non-empty `schema_ids`, `input_tree_sha256` and `policy_sha256` consistency, state membership, that every stage up to the current state is present (:239-243), count types, and `attempts` is a list. It does **not** re-check `deps.prev` chain integrity or that `reviewers_complete` matches the attempts (only `reusable_stages` checks the chain).

### 1.3 Attempts (`record_attempt` :331-386)

- Valid only for an **open** per-reviewer stage: the stage must not yet be committed and must be the next stage (`:371-372`). So attempts for `collected` can only be recorded while the state is `dispatched`.
- `completion` must be one of `complete, truncated, invalid, failed, timed_out` (`COMPLETIONS` :52; check :344-345).
- Identity inside the run is `(stage, reviewer_id, attempt_id)` (:355-368); identical replay -> `False`, different payload -> `Conflict`.
- A new attempt after a `complete` attempt of the same reviewer in the same stage raises `Conflict` ("would add a vote", :378-381). An earlier incomplete attempt gets `superseded_by` (:382-383).
- **What an attempt stores:** only `payload_sha256` = sha256 of `{"completion": ..., **payload}` (:353). The payload itself (model, tokens, cost, wall time, error) is **not stored**; only its hash. So the manifest proves *that* an attempt happened and its outcome class, but carries no model identity, cost or timing.
- `_recount` (:269-274) counts only `collected` attempts, latest per reviewer.

### 1.4 Resume (`reusable_stages` :402-419, `resume` :422-470)

- `resume` compares freshly computed frozen fields with stored ones: same `input_tree_sha256`, same `policy_sha256`, same `(engine_requested, engine_effective)` -> returns the same manifest, `False` (:443-450). Any change -> a **new** manifest at `frozen` with `invocation+1` and the old invocation summarised in `history` (:451-470). The new manifest does **not** carry over stages or attempts.
- A different `run_id` raises `Conflict` (:436-439).
- `reusable_stages` returns the prefix of committed stages whose `deps` still match (:405-418). It is a pure helper; nothing in `manifest.py` or `manifest_cmd.py` calls it (callers checked in section 9).
- Edge case: a run that reached `failed` and is re-inited with the same inputs comes back as `reused` with state `failed` (`resume` returns `m` unchanged, :449-450; `manifest_cmd.init_cmd` does not save on `reused`, :121-122). Every later `advance` raises `OutOfOrder` (:300-301, :369-370). So a failed run cannot be retried in the same output directory under the same inputs and run id; a different run id raises `Conflict`. A retry needs a new `--out`.

### 1.5 Publish (`publish_files` :476-518, `commit_published` :521-524, `hash_published_files` :527-534)

- `PUBLISH_FILES = ("REPORT.md", "return-contract.yaml", "audit.log")` (:54). `publish_files` requires exactly these (:491-492), refuses in shadow mode (:496-500), accepts an identical replay when already published (:501-504), requires state `validated` (:505-508), writes temporaries then `os.replace` (:509-516), then commits (:517).
- Crash window: files renamed but `published` not committed -> `read_committed` (:176-186) refuses the manifest. Recovery is by re-running publish (identical-replay path needs state `published`, so a crashed run in state `validated` simply re-publishes; overwrite is safe because contents are identical).
- Shadow mode: `hash_published_files` hashes the files the legacy writers wrote and they are recorded via `advance published` (`manifest_cmd.advance_cmd` :200-203).

**Key Takeaways**
- [E1] The manifest is a strict, hash-chained, append-only stage ledger with idempotent replays, conflict detection and a commit point (`published`). It is the only run-state record of the three efforts with resume semantics.
- [E1] It records outcome classes and hashes, **not** reviewer model, served model, tokens, cost or wall time: per-attempt payloads are reduced to `payload_sha256` (:353). A unified run record must add these fields or link to a sidecar.
- [E1] Gaps: `validate` does not re-verify the hash chain or `reviewers_complete`; `reusable_stages` has no in-package caller; a failed run cannot be retried in place.
- The stage list is reflect-shaped (`calibrated`, `debated`, `validated`); a tasklist or spec panel [E2]/[E3] has no calibration or debate stage, so a shared manifest needs optional or per-profile stages.

---

## 2. `src/superclaude/cli/review/manifest_cmd.py` (240 lines) [E1]

CLI group `superclaude review manifest` (:48-50), registered through the `review` group loader (scope slice 02, `__init__.py:19-29`). Imports `click`, `yaml`, and `manifest as mf` (:13-16).

| Subcommand | Lines | Behaviour |
|---|---|---|
| `init` | :53-134 | Options `--out`, `--run-id`, `--snapshot` (must exist), `--template-sha256`, `--tiers-sha256`, `--brief-template-sha256`, repeatable `--schema-id`, `--t2-engine-requested`, `--t2-engine-effective` (choices = `mf.ENGINES`). Builds `frozen` with `snapshot_sha256 = sha256_file(snapshot)` and `input_tree_sha256` read from the snapshot YAML, top-level or under `input_snapshot` (`_tree_sha` :37-45). Creates, resumes (`mf.resume`) or reuses; saves only when not `reused` (:121-122). Prints `{"result": created|reused|new-invocation, "state", "invocation"}` (:125-134). |
| `advance` | :137-215 | `--stage` choice = `STATES[1:] + failed` (:139). Three modes: `--stage failed --reason` -> `mf.fail` (:174-175); `--reviewer-id/--attempt-id/--completion` (all three required together, :176-180) -> `mf.record_attempt` with the `--payload` JSON as payload (:181-183); `--stage published --publish-from DIR` -> `mf.publish_files` (:184-199); otherwise `mf.advance_stage`, and for `published` without an `outputs` map the three files already in `--out` are hashed (shadow path, :200-203). Prints `{"result": advanced|noop, "state"}`. |
| `validate` | :218-240 | Loads and validates; `--require-published` adds the reader check; exits 1 on any error (:233-239). |

Observations:
- `--template-sha256`, `--tiers-sha256` and `--brief-template-sha256` are **caller-computed**; the CLI does not hash the template, tier file or brief itself, so the policy hash is only as honest as the caller (:67-69, :96-98). The manifest's `validate` checks only the hex shape (manifest.py:208-217).
- The `--payload` file for an attempt is reduced to a hash (manifest.py:353), so whatever the coordinator puts there (model, tokens) is not readable later from the manifest.
- `advance` on `failed` with no `--reason` writes `"unspecified"` (:175).
- An `OSError` (for example a missing publish file) becomes a `ClickException` (:208-209).

**Key Takeaways**
- [E1] The CLI is a thin wrapper; all rules live in `manifest.py`. The only content it computes itself is `snapshot_sha256` and the extraction of `input_tree_sha256` from the snapshot YAML.
- [E1] For a shared core, the hashes of template/tiers/brief should be computed by the CLI from the actual files, not passed in, so the policy hash is self-verifying.

---

## 3. `src/superclaude/cli/review/telemetry.py` (447 lines) [E3]

Origin #346 (scope slice 02, section 1). Stdlib only (:8-15); module docstring promises "No document text, quote, anchor or claim ever enters a record" (:3).

### 3.1 Record kinds and schema `review-telemetry/1` (:17)

There are two record kinds, decided by the `kind` key in `validate_record` (:196-281): `reviewer_run` (:204-255) and `outcome` (:256-264); anything else is rejected (:265-266).

**Naming trap:** the module constant `KINDS = ("first", "re-review", "audit")` (:19) is **not** the record kind. It is the review kind, used only as the `--kind` choice of `telemetry taskvars` (`telemetry_cmd.py:23-29`) and written into `task.review_kind` by `task_variables` (:189). `validate_record` never checks `task.review_kind` against `KINDS`.

`reviewer_run` record = top keys `REVIEWER_TOP` (:82-91: `schema_version, kind, record_id, ts_utc, run_id, step, round, reviewer_id`) + six required groups `REVIEWER_GROUPS` (:30-81) + `context`, with optional `supersedes` and `stratum` (:205-206). Unknown keys at top or group level are errors (:210-225).

| Group | Keys (:line) | Notes |
|---|---|---|
| `panel` | `template_id, template_version, template_sha256, tiers_version, tiers_sha256, environment, panel_size` (:31-39) | the policy identity, same idea as the manifest's `frozen` hashes [E1] |
| `slot` | `slot_id, tier, alias, strategy, seed, fallback_depth, stand_in` (:40-48) | `fallback_depth` and `stand_in` record a fallback hop as a number/flag, not the hop chain |
| `model` | `resolved, launch, observed` (:49) | three identities: model chosen by resolution, model actually launched, model observed in the transcript. This is the only schema of the three efforts that separates intended from served model at the record level. |
| `task` | `doc_sha256 ... review_kind` (:50-65) | produced by `task_variables` (:142-190): doc hash, bytes, lines, language guess, format, sections, heading depth, tables, table rows, ids defined, cross refs, RFC 2119 words |
| `output` | `block_ok, findings, blocking, by_severity, verdict, verdict_mismatch` (:66-73) | `by_severity` must hold CRITICAL, MAJOR, MINOR (:226-237). No dropped-finding count. |
| `cost` | `tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s` (:74-80) | tokens and wall seconds; **no money field** |

`context` values must be short labels or numbers matching `^[A-Za-z0-9._-]{1,64}$` (`_RUN_ID` :21, check :238-251) so no text can ride in. `round` must be an int (:252-255).

`outcome` record = `OUTCOME_KEYS` (:92-109): `reviewer_record_id` (link to a reviewer_run), `truth_basis` in `catalog-v1, theme-v1, adjudicated-v1` (`TRUTH_BASES` :18; :263-264), `confirmed_tp, false_pos, unconfirmed, unique_tp, overlap_mean_jaccard, recall_vs_confirmed, precision, cost_per_confirmed_tp, supersedes`, plus optional `stratum` (:110, :261).

Shared checks (:267-280): `stratum`, `ts_utc` shape `YYYY-MM-DDTHH:MM:SSZ` (`_TS` :22), `run_id` shape, non-empty `record_id`.

### 3.2 D15: strata fixed to sonnet/haiku [CODE-VERIFIED]

`STRATA = ("sonnet", "haiku")` (:112-115, comment "owner decision D3 ... strata are never pooled"). `validate_record` rejects any other non-null stratum with "stratum must be 'sonnet' or 'haiku'" (:267-268). `append_record` raises `ValueError` on any error (:289-291), and `load` skips the line and reports only its first error (:411-414).

What breaks with gateway tiers: a record tagged with a gateway class (for example `claude-gw-tier1a`, `luna`, `ember`, `opus`) as its stratum cannot be appended; the only way to store it is `stratum: null`, which puts it outside every stratum cohort. `model.observed`/`resolved`/`launch` are free-form (no validation beyond key presence), so gateway ids are accepted there. The `model_scores` view (:362-379) groups by `model_observed, slot_tier, slot_stand_in, stratum, truth_basis`, so null-stratum records form their own group; `stratum_conflicts` (:438-443) counts outcomes whose stratum differs from their reviewer run's.

Line-number note: the task prompt and scope slice 02 cite `_ID_TOKEN` at :22. In the current file :22 is `_TS`; `_ID_TOKEN` is :23 and `_ID_RE` is :24. **[STALE DOC]** (scope slice 02 row D7 says "hand-off said :23, which is `_ID_RE`" — the hand-off's :23 was in fact correct).

### 3.3 Storage and loader

- `append_record` (:287-307): writes `<dir>/records/<YYYY>/<MM>/<run_id>.jsonl` (reviewer runs) or `<run_id>.outcomes.jsonl` (outcomes); reuses an existing file for that run id found anywhere under `records/*/*/` (:298-300), so a run that spans a month boundary stays in one file. Append-only, never rewrites (:305-306).
- `load` (:382-447): creates `reviewer_runs` and `outcomes` tables with `record_id` primary key, `INSERT OR IGNORE` (idempotent, :417-435), rebuilds view `model_scores` (:436-437). Supersession: superseded record ids are excluded from both sides of the view (:376-377). `cost_per_confirmed_tp` in the view uses **`tokens_out` only** (:371), not input or cache tokens.
- Context flattening keeps three named context keys as columns (`experiment, arm, replicate`, :327-329) plus `context_json`.

### 3.4 Callers

Grep over `src/superclaude` for `review telemetry|review-telemetry|benchmarks/review-telemetry` hits only `telemetry.py` and `telemetry_cmd.py` [CODE-VERIFIED]. No skill, command or other CLI module writes telemetry records. Tests: `tests/review/test_review_telemetry.py` and `tests/review/test_review_cli.py:386` build records by hand.

**Key Takeaways**
- [E3] review-telemetry/1 is the richest per-reviewer schema of the three efforts: three model identities, policy hashes, slot/fallback depth, document descriptors, output counts, tokens and wall time, plus a separate `outcome` record kind for scoring against a truth basis.
- [E3] It is dormant: nothing in `src` writes it. D15 is confirmed: strata are hard-coded to sonnet/haiku, which rejects every gateway class as a stratum.
- [E3] Missing for a unified record: money cost, dropped/rejected finding count and ids, attempt count, fallback hop chain, completion state (the manifest's `COMPLETIONS` [E1]), and a link to a run manifest.
- [E3] `KINDS` is a misleading name (review kind, not record kind).

---

## 4. `src/superclaude/cli/review/telemetry_cmd.py` (98 lines) [E3]

`superclaude review telemetry` group (:15-17) with `DEFAULT_DIR = ".dev/benchmarks/review-telemetry"` (:12), overridable by `--dir` or env `SUPERCLAUDE_REVIEW_TELEMETRY_DIR` (:42-47, :74-76).

| Subcommand | Lines | Behaviour |
|---|---|---|
| `taskvars DOC` | :20-38 | prints `task_variables(text, specialization, kind)`; `--kind` choice = `tel.KINDS` (:23-29) |
| `append --record FILE` | :41-70 | one record or a list; each validated and appended; first invalid record raises `ClickException` (:65-69) — records before it in the list are **already appended** (no all-or-nothing) |
| `load --db FILE` | :73-98 | prints `{reviewer_runs, outcomes, invalid, stratum_conflicts}`; invalid lines listed on stderr (:86-88) |

**Key Takeaways**
- [E3] The CLI exists and is tested but has no caller; a list append is not atomic.
- [E3] The record must be assembled entirely by the caller: the CLI does not derive `model.observed`, tokens or `output` counts from a transcript or report.

---

## 5. `src/superclaude/cli/review/merge_cmd.py` :71-118 [E3]

`command` (:71-118) reads an optional panel resolution to map `reviewer_id -> model` (:73-83), reads each `--report REVIEWER_ID=PATH` (:84-98), loads or creates the ledger (:100-108; `cap` used only on round 1, :104), runs `led.merge_round` and `render_merged_report` (:109-110), writes the merged report (:113-115), saves the ledger (:116) and prints the result keys not starting with `_` (:117-118).

D15 second half [CODE-VERIFIED]: there is no telemetry call and no import of `telemetry` in this file (imports :5-10 are `json, os, click, ledger`). The merge result (verdict, decision, brief ids, warnings) is printed to stdout only; nothing appends a `reviewer_run` or `outcome` record. Per scope slice 02 (D1) the ledger keeps per-reviewer `block_ok` but not dropped finding ids; the merge warning carries the error count and the first error message only (`ledger.py:130-134`, cited there, not re-read here).

Also: the reviewer's `model` comes only from the resolution file (:76-79), i.e. the **intended** model; no served model reaches the ledger.

**Key Takeaways**
- [E3] The merge is the natural point to emit per-reviewer `output` telemetry (block_ok, findings, blocking, rejected lines), but it emits none.
- [E3] The ledger records the intended model only; served identity would have to come from the runner.

---

## 6. Reflect run telemetry: `sc-reflect-protocol/SKILL.md` §9.2 (:940-989) [E1]

§9 is the "Output Contract (Versioned)" (:718). "Two-block contract: stable + telemetry. Written to `<output>/return-contract.yaml` AND returned inline" (:722). For the **skill path** this is a prompt instruction executed by the agent: no Python writer of the 1.8.0 contract with a `telemetry:` block exists [CODE-VERIFIED by absence, Phase 3 fix cycle 1: `research/13-gap-fill-reflect-ensemble.md` §4.1]. A Python writer of a **different** reflect contract at the same path does exist: `ensemble._emit_reflect_contract` (`src/superclaude/cli/reflect/ensemble.py:886-895`, called at :510) writes a 33-key, version-"1.0" contract with `yaml.safe_dump` and no `telemetry:` block, for the code-driven `superclaude reflect run` route that the tasklist post gate uses (`runner.py:538-545`) [CODE-VERIFIED]. So "no Python writer of `return-contract.yaml`" is [CODE-CONTRADICTED] in general and true only for the skill path. [E1] §9.2 is "non-stable" (:940).

**Contract and run-record writers in code (added in the Phase 3 fix cycle 1) [E1]:**

| Writer | File written | Schema / content | Evidence |
|---|---|---|---|
| `ensemble._emit_reflect_contract` | `<output>/return-contract.yaml` | reflect contract version "1.0", 33 keys incl. `adversarial_subrun_status`, `verification_verified`, `reviewers_verified`, `regression_verified`; deleted when 0 reviewers succeeded | `ensemble.py:74`, :786-834, :886-895 |
| swarm `reduce_wave3(..., emit_to_disk=True)` | `<output>/t2-swarm/return-contract.yaml` + `done` sentinel | swarm's own contract (key list [UNVERIFIED]; `swarm/reduce.py` not read) | `ensemble.py:404-421` |
| `runner.write_reflect_post` | `reflect_post:` block in the phase/tasklist frontmatter | `verdict`, `status`, `run_id`, `tier_reached`, `report`, `contract`, `reason`, `deviations{...}`, `head`, `reviewed_at`, three `*_verified` | `runner.py:103-204` |
| `runner.write_sidecar` | `<output>/wrapper-result.yaml` | verdict fields plus `child_exit_code` (always 0 on the ensemble route, `runner.py:545`), `write_status`, `fix_iterations`, isolation fields | `runner.py:207-268` |
| `commands._write_exit_sentinel` | `.reflect-exitcode` | the verdict exit code | `commands.py:505-510` (per research/13 §4.1) |
| skill-path orchestrator (agent) | `<output>/return-contract.yaml` (1.8.0 + `telemetry:`) | §9.1 + §9.2 | SKILL.md:722; no code writer |

None of these code writers writes telemetry in the E3 `review-telemetry/1` sense or a run manifest; the code route records no served model, tokens or cost per reviewer beyond the swarm worker `.meta.json` files (`ensemble.py:838-858`, file names only, contents not read here [UNVERIFIED]).

Legacy telemetry keys (:943-968): per-wave durations (`wave_durations_ms`) and estimated `token_usage` per wave, `reviewer_models`, `reviewer_personas`, `reviewer_vendors`, `degraded_components`, `fallback_path` (F1-F3), executor-class fields, `citations_dropped_extrapolated`, memory counters, verify-envelope fields, handoff fields, three constant-false fields kept for shape.

Stage 2 panel keys nested under `telemetry:` (:969-988, "never at the top level of the contract"):

| Key | Meaning (SKILL.md line) | Produced by code? |
|---|---|---|
| `t2_engine_requested/effective` | legacy or shadow (:970-971) | same values stored in the manifest (`manifest.py:126-127`, `ENGINES` :51 also allows `panel`) [CODE-VERIFIED for the manifest side] |
| `panel_fallback_reason`, `t2_floor_unmet` | (:972-973) | agent-written |
| `identity_source` | `observed` or `requested-pinned` (:974; step 9 at :348) | agent-written |
| `identity_mismatch_suspected` | self-report disagrees with the pin (:975) | agent-written |
| `judge_identity`, `judge_class_collision` | (:976-977) | agent-written |
| `debate_skipped_similar` | (:978) | agent-written |
| `cluster_agreement` | float 0-1 or null, telemetry only (:979) | printed by `review cluster` (`cluster_cmd.py:185-196`, value from `cluster.py:405-412`: null when fewer than 2 complete reviewers, 1.0 when no blocking cluster, else mean `support` over non-chained blocking clusters with a support value) [CODE-VERIFIED] |
| `calibration_coverage` | `"n/m"` (:980) | printed as `calibrated_findings` by `review cluster` (`cluster_cmd.py:174-178`, :190) and also written into `panel/clusters.json` as `calibration_coverage` (:179-184) [CODE-VERIFIED] |
| `panel_parity` | (:981; step 2 at :341) | agent-written; doc says the aggregator recomputes it from card headers and `panel/resolution.json` (checked in section 9) |
| `anchor_replaced` | (:982) | agent-written |
| `manifest_path` | `<output>/panel/manifest.json` (:983) | path matches `manifest_cmd._path` :19-20 [CODE-VERIFIED] |
| `reviewers_requested/resolved/complete` | (:984-986) | copies of manifest counts (`manifest.py:143-145`, :307-316, `_recount` :269-274) [CODE-VERIFIED for the manifest side] |
| `panel_shortfall_2_of_3` | (:987) | agent-written |
| `findings_block_compliance_rate` | valid-on-first-parse cards / reviewers dispatched (:988; step 4 at :343) | agent-written; the parse itself is `findings_v2.parse_block` (scope slice 02) |

Where stored: the `telemetry:` block lives inside `<output>/return-contract.yaml` (:722, :349), which the legacy writers produce; the manifest then records the file's sha256 in the `published` stage (`manifest.py:527-534`; SKILL.md:349). The manifest itself carries the reviewer counts; `panel/clusters.json` carries `cluster_agreement` and `calibration_coverage`; `panel/notes.md` carries the valid-block count after re-ask and identity notes (:343, :348).

Attempt recording in shadow mode: SKILL.md:342 records each attempt with `--completion <state>` and no payload, so the manifest gets outcome classes only, no model or cost.

**Key Takeaways**
- [E1] Reflect run data is spread over four places: `return-contract.yaml` `telemetry:` (agent-written YAML), `panel/manifest.json` (code), `panel/clusters*.json` (code), `panel/notes.md` (free text).
- [E1] Per-reviewer cost exists only as per-wave estimates (`token_usage`, `wave_durations_ms`), not per reviewer; per-reviewer model is a list (`reviewer_models`), with the served model only as an optional `model_observed:` card header line (:341).
- [E1] [E3] reflect does not use review-telemetry/1 at all; the two telemetry schemas share no keys except the reviewer counts concept.

---

## 7. E2 per-run records: `meta.json`, `cost.json`, `fallback.log` and `tools/run-reviewer.sh` [E2]

All paths below are `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`. Files read: `tools/run-reviewer.sh` (87 lines), `TASK-WF-design-20261108-041415/reviews/combos/h2-sonnet-luna2-ember2-r1/t1b-1.meta.json` and `t1b-1.cost.json`.

### 7.1 What is committed

`git ls-tree` at the commit: 1263 `*.meta.json` files under the study tree; **0** `*.fallback.log` files; **0** raw `*.attemptN.json` transcripts; **0** `*.attemptN.meta.json` files. Per run the commit holds `<rid>.md`, `<rid>.meta.json`, `<rid>.cost.json`, `<rid>.attemptN.md` and `<rid>.attemptN.err`. So the fallback-log format and the per-attempt meta are known only from the runner source, and audit A cannot be re-run from the commit (it reads `attemptN.json` and `attemptN.meta.json`, `audit-A/audit.py:53`, :65, :73).

### 7.2 Runner (`tools/run-reviewer.sh`)

- One fresh `claude -p --model $MODEL --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` per attempt in `/tmp/evalsb/repo`, timeout 3000 s (:48). Raw stream to `$OUT/$RID.attemptN.json`, stderr to `.err`.
- Derived per attempt (:49-57): wall seconds `W` from `date +%s` (:47, :49); report text = first `result` record (:50); `OBS` = unique `message.model` of top-level assistant turns (`parent_tool_use_id==null`), comma-joined (:51); `TOK` = `result.usage.output_tokens` (:52); `TOKALL` = sum of `result.modelUsage[*].outputTokens` (:53); `APIERR` if the report contains `API Error` (:54); `MODEL_OK` when OBS is non-empty, not `<synthetic>`, and equals the requested model case-insensitively or `<requested>-build` (:55-56); `BLOCK_OK` when the report contains a line starting with ```` ```findings-v1 ```` (:57).
- Per-attempt meta written at :58; success = `MODEL_OK && BLOCK_OK && !APIERR` (:59). Up to 2 attempts per model (:61-64).
- Fallback ladder (:23-43 map, :66-83 loop): only when the primary failed and `NOFALLBACK` is unset; `EXCLUDE_MODELS` default `glm-5.3 Qwen3.8-max` (:69); never revisit (:70-71); each hop appends one line `FALLBACK <model> -> <next> (HH:MM:SS)` to `$OUT/$RID.fallback.log` (:75).
- Final = last attempt: `.md` and `.meta.json` copied from `attempt$attempt` (:85). `cost.json` = `jq -s` over `$RID.attempt*.meta.json`: `{attempts: length, total_wall_s, total_output_tokens_all}` (:87).

### 7.3 Record formats

`meta.json` sample (`h2-sonnet-luna2-ember2-r1/t1b-1.meta.json`, full file): `reviewer_id`, `expected_model` (`claude-sonnet-5-5`), `observed_model` (`claude-sonnet-5-5`), `model_ok` true, `findings_block` true, `attempt` 1, `wall_s` 220, `output_tokens_main` 25685, `output_tokens_all` 26495, `exit` 0. Matches the jq template at `run-reviewer.sh:58`.

`cost.json` sample (`t1b-1.cost.json`): `attempts` 1, `total_wall_s` 220, `total_output_tokens_all` 26495.

`fallback.log`: one text line per hop (`run-reviewer.sh:75`); no committed sample exists, and audit A reports "fallback.log present: 0 runs" (`audit-A/summary.md:12`).

### 7.4 Intended versus served model

- `expected_model` is `$MODEL` at write time (:58), and the ladder overwrites `MODEL="$NEXT"` (:76). After a fallback the meta's `expected_model` is the **fallback** model, not the intended one; the intended model survives only in the first `fallback.log` line. `MODEL_LADDER` is built (:44, :76) but never written to any file. (Scope slice 01 gap 6 says the same; CODE-VERIFIED here at :58/:76.)
- `attempt=0` is reset per hop (:76) so the fallback model's attempt files reuse the names `attempt1/attempt2` and overwrite the earlier model's files; `cost.json` (:87) then sums only the surviving files. Audit A names this "the known overwrite flaw" (`audit-A/summary.md:12`).
- The reverse case also exists: stale `attemptN` files left from an earlier run in the same directory are summed into `cost.json`, inflating 5 runs (`audit-A/summary.md:15-16`).
- Served model is the transcript's top-level `message.model` (:51). Auxiliary calls (for example a `claude-gw-tier2[1m]` `web_fetch_apply` call) are excluded from `observed_model` but **included** in `output_tokens_all` via `modelUsage` (:53; audit-A/summary.md:22).
- Intended model for the study is kept outside the run record, in `combos/<row>/<pkg>/resolution.json` (read by `audit-A/audit.py:28-31`), or derived from the row name when no resolution exists (`audit.py:129-135`).

### 7.5 Cost and time fields

Output tokens only (main turn and all models) and wall seconds per attempt; no input tokens, no cache tokens, no money, no start timestamp. Wall time includes CLI start-up (the `claude -p` subprocess, :47-49).

**Key Takeaways**
- [E2] The runner is the only one of the three efforts that measures served identity from the transcript per run and gates on it; it writes a compact per-run record (`meta.json`) and a per-run cost sum (`cost.json`).
- [E2] Its records are lossy: intended model overwritten on fallback, ladder not stored, attempt files overwritten across hops or left stale, fallback log only as free text, no per-attempt files or transcripts committed.
- [E2] [E3] The E2 `meta.json` fields map onto review-telemetry/1: `expected_model`->`model.launch`, `observed_model`->`model.observed`, `findings_block`->`output.block_ok`, `wall_s`->`cost.wall_s`, `output_tokens_*`->`cost.tokens_out`; `model.resolved` (intended) has no E2 counterpart in the record.

---

## 8. E2 audits A and D [E2]

Only `audit-A/summary.md` and `audit-D/summary.md` exist; audits B, C, E, F hold scripts and outputs but no summary file (confirmed by the `git ls-tree` listing of `analysis/audits/audit-A/` and `audit-D/`, and by scope slice 01 section 1.5).

### 8.1 Audit A: model identity and attempts (`audit-A/summary.md`, 34 lines; `audit-A/audit.py`, 171 lines)

Snapshot "2026-11-13 ~01:12 UTC" over 890 runs (`summary.md:1-3`). Model-behaviour evidence below is dated to that snapshot.

Checks implemented in `audit.py` (per run, rows with `contaminated/superseded/quarantine` skipped, :4, :25):

| Check | Code | What it does |
|---|---|---|
| 1 intended == expected == observed | :42-48 | intended from `resolution.json`; `ok_eq` allows `-build` suffix (:10-11) |
| 1b name-derived intended | :129-137 | when no resolution, derive allowed models from row-name tokens |
| 2 fallback present | :49-50 | flags any `fallback.log` as EXCLUDE |
| 3 bad observed | :51-52 | empty, `<synthetic>` or comma-joined |
| 4 identity re-derivation | :61-72 | final `.md` byte-equal to `attempt{n}.md` (`cmp`), then re-derive top-level `message.model` from raw `attempt{n}.json` and compare with meta and intended |
| 5 cost consistency | :77-84 | `cost.attempts` equals attempt-file count; token and wall sums equal |
| 5 stale attempts | :56-60 | attempt files numbered above `meta.attempt` |
| 5 retry/outage | :85-92 | outage = "native binary not installed" or exit 127 with 0 tokens and 0 wall |
| 6 misrouting | :94-104 | zero tokens with `model_ok`; under 400 tokens; stderr other than `unrecognized_model` |
| E1/E2/E3/E9 | :107-128 | init model vs observed, extra `modelUsage` keys, subagent models, init model varying across attempts |
| E4/E4b, E5 | :139-144 | `model_ok`/`findings_block` not true; earlier attempt on another model |
| E6 duplicate report | :148-149, :161-164 | identical final report sha across runs |
| E7, E8 | :151-155 | empty / `API Error` report; self-identification regex |
| E10, E11, R1 | :35-36, :156-160 | same slot uses the same model across packages; run missing in a package; resolution reviewer with no output |

Results (`summary.md`): 2 runs EXCLUDE (b4-muse-luna2 t2b-1 asked muse-wonder-1.0, served gpt-6.1-terra, :6-8); check 1 0 mismatches over 828 resolved runs (:11); 0 fallback logs (:12); check 4 0 differences (:14); 5 stale-attempt runs with inflated cost (:15-16); 59 runs with extra `modelUsage` keys, 57 of them an auxiliary `claude-gw-tier2[1m]` call (:22).

Anomalies in the script: `audit.py:33` increments `stats[fam]` in the no-resolution branch before `fam` is assigned in this iteration (:38), so it uses the previous row's family or raises `NameError` on the first row. Paths are hard-coded to another worktree and `/tmp/audit-A` (:2, :165, :168), matching scope slice 01 gap 5.

### 8.2 Audit D: merge and ledger integrity (`audit-D/summary.md`, 90 lines; `audit-D/audit.py`, 239 lines)

Scope 264 `merged-1.md` over 89 rows x 3 packages, round 1 only (`summary.md:3`). The study tree also holds `audit2.py`, `mk.py`, `anch.py`, `bok.py` (listing), which were not read; the summary names `audit.py, audit2.py, mk.py` as its scripts (:2).

Checks implemented in `audit.py` (per merged row and reviewer):

| Check | Code | What it does |
|---|---|---|
| 1 panel/paths | :54-62, :70-76, :83-84 | reviewers listed in `merged-1.md` (regex over the `- <id>: report <path>, block ok <bool>` lines, :55) equal the resolution panel; report path equals the current final path and exists; reviewer present in ledger |
| 2 block ok | :95-98 | `block ok false` -> EXCLUDE; block true but no block found -> WARN |
| 3 conservation (dropped-finding counter) | :85-103, :105-109 | audit's own lenient `parse_block` (:17-31, takes the **last** findings-v1 fence, counts JSON-unparsable lines) vs ledger members of that reviewer; `>50%` dropped -> EXCLUDE, any drop -> WARN; id-level raw-only/ledger-only ids |
| 4 blocking consistency | :111-118, :134-156 | raw vs ledger blocking per finding; row blocking == any member; markdown table == ledger; verdict == FAIL iff any blocking row (stdout and md) |
| 5 stale / doc sha | :77-82, :158-168 | report mtime newer than merge; **report sha256 vs ledger `report_sha256`**; ledger `doc_sha256` vs candidate sha; rounds == [1]; `stale-r1` dirs |
| 6 model | :120-132 | resolution model == meta `expected_model`; observed == expected; tier/alias present |
| extras | :171-219 | same-reviewer multi-member rows, mixed categories, mixed blocking, rows without span, merge warnings, identical ledger sha across rows, merged vs resolution mtime gap, reviewer order |

Ledger side, current product code [E3] [CODE-VERIFIED]: per reviewer per round the ledger stores `reviewer_id, model, report, report_sha256, block_ok` (`ledger.py:141-149`), per round `doc_sha256` (:279) and returns `block_ok` and `warnings` (:295-296). The warning carries the error count and only the first message (:130-134). So the sha check of audit D can be done against the ledger as shipped; the conservation check cannot, because dropped ids are not stored.

Results (`summary.md`): C2 80 reviewer-level EXCLUDE (:7); C3 10 EXCLUDE and 78 WARN, 49 dropped findings were blocking (:8); C5 16 EXCLUDE stale (report sha differs from ledger `report_sha256`), ledger doc sha matched in all 264 (:10); drop reasons by replaying `_check_finding`: anchor >200 56, anchor2 >200 18, claim >300 14, bad severity 3, refs 1 (:15-16); per model drops (:17); 3 verdict flips named (:20); 45 merges without `merge-stdout.txt` (:26).

Chain size (X1, `summary.md:29`): 195 chained rows among 1398 ledger rows in total, 144 span >60 lines, 83 rows have >=8 members or >=4 sections. This replay is **not** in `audit.py` (which only counts mixed categories and same-reviewer members, :183-195); it is in `analysis/audits/audit-D/audit2.py:139-155` [CODE-VERIFIED, `git show 4a22d742...`]: `rows_total` is incremented at :140 for every ledger row before the `< 3 members` filter at :145, and `chain_total` at :154 only for rows with >=3 members and at least one non-directly-same pair, so 1398 is all rows. The `summary.md:29` wording "195 of 1398 rows with >=3 members" is [CODE-CONTRADICTED] (also file 03 :288).

### 8.3 How each check could become a built-in run check

| Audit check | Built-in form | Where it would hook | Evidence the product lacks it today |
|---|---|---|---|
| A-1/A-4 identity re-derivation [E2] | runner records `model.resolved` (intended), `model.launch`, `model.observed` (from the transcript top-level turns), and a `model_ok` flag; the run record fails a reviewer whose observed != launch | at collection, beside `record_attempt` [E1]; fields already exist in review-telemetry/1 `model` group [E3] | manifest attempts hold only a hash (`manifest.py:353`); reflect uses self-report or `requested-pinned` (SKILL.md:348) |
| A-2 fallback hops [E2] | store the hop list (`[model, attempt, completion, reason]`) per reviewer instead of a text log; never overwrite attempt files (key by `(model, attempt)`) | manifest `attempts` already allow multiple attempts per reviewer with `superseded_by` (`manifest.py:373-383`) | runner overwrites `expected_model` (`run-reviewer.sh:58`, :76) and attempt files |
| A-5 cost consistency [E2] | compute run cost from per-attempt records only; one aggregator | telemetry `cost` group [E3] per attempt | E2 `cost.json` drifts on stale/overwritten files (`audit-A/summary.md:12`, :15-16) |
| D-3 dropped-finding counter [E2] | the merge/cluster step stores per reviewer `findings_raw`, `findings_kept`, and each rejected line's id and reason; non-zero drop of a blocking finding becomes a run warning | `ledger.merge_round` entries (`ledger.py:141-149`) and `findings_v2.parse_block` errors (scope slice 02 D1) | ledger stores `block_ok` and a first-error warning only (`ledger.py:130-134`, :147) |
| D-5 report sha vs ledger [E2] | at merge, re-hash each reviewer report and compare with the sha recorded at collection; at publish, re-hash before commit | manifest `collected` stage outputs map (`manifest.py:284-291`, :317-326) can hold per-report sha256; ledger already stores `report_sha256` (`ledger.py:146`) | nothing compares the two today |
| D-1 panel/path equality [E2] | merged reviewer set == resolved reviewer set == collected attempts with completion `complete` | manifest counts (`reviewers_resolved`, `reviewers_complete`) [E1] | `merge_cmd` accepts any `--report` list (`merge_cmd.py:84-98`) |
| D X1 chain size [E2] | cluster step reports chained clusters and member/section counts; flag above a threshold | `cluster_v2` already marks `chained` (`cluster.py:422`) [E1]; v1 `findings.cluster` does not (scope slice 02 D6) | v1 ledger rows keep the first member only |
| D-4 blocking/verdict consistency [E2] | assert inside the ledger writer (row blocking == any member, verdict == FAIL iff blocking row) | `ledger.py` verdict code (scope slice 02 D4) | holds today (0 violations, `summary.md:33`), so only a regression guard |

**Key Takeaways**
- [E2] Audits A and D are after-the-fact scripts with hard-coded paths (`audit-A/audit.py:2`, `audit-D/audit.py:2`, output in `/tmp`), run once by the orchestrating session; they found real defects (49 dropped blocking findings, 16 stale merges, 2 misrouted runs).
- [E1] [E3] Most of their checks need only data the product already has or nearly has: ledger `report_sha256`/`doc_sha256` [E3], manifest attempts/counts [E1], cluster `chained` [E1], telemetry `model` group [E3]. The missing pieces are stored rejected-line ids, served model from transcripts, and per-attempt cost.

---

## 9. `scripts/reflect_shadow_exit.py` (410 lines) [E1]

Stage 2 shadow-exit aggregator; reads files only (docstring :4-5). Imports `superclaude.cli.reflect.panel_lint`, `review.manifest`, `review.panel` (:50-52) and loads `reflect_verdict_replay.py` by path (:62-71).

Run selection (`collect` :203-263): every `<runs-root>/pre-*/panel/manifest.json` with `t2_engine_effective == "shadow"` (:209-216); `failed` -> listed as failure (:218-220); any state other than `published` -> incomplete, not counted (:221-223). Default runs root `.dev/reflect` (:392), default required 20 (:55).

Keys read per counted run:

| Key | Source | Line |
|---|---|---|
| `t2_engine_effective`, `state` | manifest | :215-217 |
| manifest structural errors | `mf.validate(manifest)` | :232 |
| `reviewers_resolved == 3 and reviewers_complete == 2` -> `shortfall` | manifest | :244-245 |
| `panel_parity` (recorded, compared with recomputed) | contract `telemetry:` via `tele` (:90-95) | :226, :237 |
| `reviewer_personas`, `reviewer_models` | contract (stable block or telemetry) | :155-156 |
| `executor_class_resolved` | contract | :246 |
| `findings_block_compliance_rate` | contract | :247 |
| `cluster_agreement` | contract | :248 |
| `tier_reached` | contract | :191 |
| `panel/resolution.json` reviewers and `tiers_sha256`; `panel/cards/reviewer-<N>.md` headers | files | :125-153 |
| MALFORMED rows | `audit.log` | :180-186 |

Not aggregated: `calibration_coverage`, `identity_source`, `identity_mismatch_suspected`, `judge_identity`, `panel_shortfall_2_of_3` (recomputed from the manifest instead), any cost or duration field. Parity is recomputed and the recorded boolean is not trusted (docstring :13-18; `recompute_parity` :117-177), which confirms the SKILL.md:341 claim "The Stage 2 aggregator recomputes parity from the card headers and `panel/resolution.json`" [CODE-VERIFIED]. A run whose resolution `tiers_sha256` differs from today's tier file is "not proven" (:128-132), so a tier-file change invalidates parity proofs for older runs.

Manifest helpers used: only `mf.validate`. `reusable_stages`, `read_committed`, `record_attempt`, `publish_files` have no caller outside `manifest.py`, `manifest_cmd.py` and `tests/review/test_review_manifest.py` (Grep over `*.py`) [CODE-VERIFIED]; so `reusable_stages` and `read_committed` are exercised only by tests.

**Key Takeaways**
- [E1] The exit aggregator is effectively E1's built-in run check set: parity recompute, MALFORMED rows, contract lint, manifest validation, EV-1 rate versus legacy, verdict replay. It already does what E2's audits do for identity-by-pin (not by served model) and for record consistency.
- [E1] It ignores cost and time completely, and reads served identity nowhere.

---

## 10. `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py` (193 lines) [E1]

Builds one record per experiment run (5 combinations x 3 repeats, :23-25) into `results.jsonl` and `results.md` (:172-189). Sources: `return-contract.yaml`, `adversarial/merged-verdict.yaml` (or the nested copy), `panel/manifest.json`, `panel/clusters.json`, `logs/<run>.time`, `logs/<run>.jsonl`, and the stdout of `scripts/reflect_shadow_exit.py` (docstring :4-5; :84-88; :111-128).

Fields extracted per run (`record` :147-164): `state` (manifest), `status`, `merge_method`, `confidence_calibrated` (contract), `minutes` (from `.time` start/end, :126-128), `verdict`, `blocking/medium/minor_findings`, `convergence_score` (merged verdict), `findings_clustered` (sum of cluster members, :145), `compliance_first_pass` = telemetry `findings_block_compliance_rate`, `reviewers_complete` (manifest), `calibrator_diversity`, `identity_mismatch_suspected`, `judge_identity`, parity/lint from the exit script, `reviewer_requested_served` and `calibrator_requested_served` (pairs), `reviewer_distinct_served`, `cost_usd`, `out_tokens`, per-model `usage`, card `reviewer_model_self_report` lines, and a `leak` flag (report text mentions `.dev/tasks/done/<ID>`, :135-141).

Served model and cost come from the outer session's stream-json log (`stream` :42-81): served model per sub-agent call = most common `message.model` of assistant events whose `parent_tool_use_id` is that `Task`/`Agent` tool-use id (:54-62, :66-69); requested = the tool call's `input.model`; cost = `total_cost_usd` of the costliest `result` event (:63-65, :77); per-model usage = `modelUsage` with `inputTokens`, `outputTokens`, `costUSD` (:70-73).

Sample (first line of `results.jsonl`, file dated 2026-11-13; model behaviour on that gateway at that date): run `comboA-r1`, 63.9 minutes, `cost_usd` 24.6, `out_tokens` 220817; `usage` keyed by **gateway tier aliases** (`claude-gw-tier3[1m]` 15.73 USD, `claude-gw-tier1a[1m]` 7.09, `claude-gw-tier1b[1m]` 1.3, `claude-gw-tier2[1m]` 0.47); `reviewer_requested_served` `[["sonnet","claude-sonnet-5-5"],["haiku","gpt-6.1-sol"],["opus","claude-opus-5-5"]]` — a reviewer requested as `haiku` was served by `gpt-6.1-sol`. The same run's `panel/manifest.json` is `published`, invocation 1, 3/3/3 reviewers, 6 attempts (`dispatched` and `collected` per reviewer), the first attempt being `{attempt_id "1", completion "complete", payload_sha256 ..., reviewer_id "t1b-1", stage "dispatched"}` with no model or cost.

Anomalies: `extract.py` runs the exit script with `sys.executable` (:85-88), not `uv run`; `"cur" in dir()` (:106) relies on a local name existing from an earlier loop iteration.

**Key Takeaways**
- [E1] E1's per-run cost and served identity exist only in the experiment's analysis script, derived from the outer session log; the product run (manifest + contract) holds neither.
- [E1] Cost is per run and per gateway alias, not per reviewer: `modelUsage` keys are tier aliases while served ids are real model ids, so a reviewer's cost cannot be separated when two reviewers share an alias. Wall time is per run (`.time` file), not per reviewer.
- [E1] [E2] Both E1 (`extract.py` :54-62) and E2 (`run-reviewer.sh:51`) derive served identity the same way: top-level (or per-parent) assistant `message.model` from a stream-json transcript. This is one shared method for the core.

---

## 11. Cross-effort comparison of run records

### 11.1 Record formats side by side

| Concern | [E1] reflect panel | [E2] tasklist study | [E3] #346 review loop |
|---|---|---|---|
| Run-state record | `panel/manifest.json`, `review-panel-manifest/1`, 9 stages + failed, hash chain (`manifest.py:38-50`, :317-326) | none (directory layout per row and package) | ledger `review-ledger/1` per document across rounds (scope slice 02); no stage state |
| Resume | yes: same frozen inputs reuse, changed inputs new invocation with history (`manifest.py:422-470`) | no (rerun by hand, quarantine dirs) | ledger rounds `n == len(rounds)+1` (scope slice 02 D16) |
| Policy identity | `frozen` template/tiers/brief sha256 + schema ids, `policy_sha256` (`manifest.py:55-63`, :97-108) | `resolution.json` per row (read by audits) | telemetry `panel` group hashes (`telemetry.py:31-39`), unwritten |
| Input identity | `input_tree_sha256`, `snapshot_sha256` (`manifest_cmd.py:92-100`) | candidate sha in the brief (`run-reviewer.sh:12-15`) | ledger `doc_sha256` per round (`ledger.py:279`); telemetry `task.doc_sha256` |
| Per-reviewer attempt | `attempts[]` with completion class and payload hash only (`manifest.py:348-354`) | `meta.json` per final attempt; attempt files on disk (`run-reviewer.sh:58`, :85) | ledger entry `reviewer_id, model, report, report_sha256, block_ok` (`ledger.py:141-149`); telemetry `reviewer_run` unwritten |
| Intended model | `panel/resolution.json` + card `model:` header (SKILL.md:340-341) | `resolution.json` outside the record; `expected_model` overwritten on fallback (`run-reviewer.sh:58`, :76) | ledger `model` from resolution (`merge_cmd.py:73-83`); telemetry `model.resolved` |
| Served model | optional card `model_observed:` line, `identity_source`, self-report check (SKILL.md:341, :348); real served id only in `extract.py` (:54-69) | `observed_model` from transcript, `model_ok` gate (`run-reviewer.sh:51-56`) | telemetry `model.observed` (unwritten) |
| Fallback | `panel_fallback_reason` (engine level, SKILL.md:972); no per-reviewer hops | `fallback.log` text, ladder not stored (`run-reviewer.sh:44`, :75-76) | telemetry `slot.fallback_depth`, `slot.stand_in` |
| Cost | per-wave `token_usage` estimate, `wave_durations_ms` (SKILL.md:943-944); real USD only in `extract.py` per run per alias (:63-77) | output tokens and wall per attempt; `cost.json` sum (`run-reviewer.sh:58`, :87) | telemetry `cost` tokens in/cache/out + `wall_s` (`telemetry.py:74-80`), unwritten |
| Output quality counters | `findings_block_compliance_rate`, `cluster_agreement`, `calibration_coverage` (SKILL.md:979-988; `cluster_cmd.py:174-196`) | `findings_block` boolean; drops measured only by audit D | ledger `block_ok`, first-error warning (`ledger.py:130-134`); telemetry `output` group |
| Truth / outcome scoring | none in product (verdict replay vs legacy in exit script) | blind judge `score.json` per row (study) | telemetry `outcome` kind with truth basis (`telemetry.py:92-110`) |
| Integrity checks | built-in exit aggregator (`reflect_shadow_exit.py:203-387`) | six after-the-fact audits (A, D read here) | none |
| Writer | CLI (manifest, cluster) + agent-written YAML (contract telemetry) | bash runner | CLI (ledger); telemetry CLI with no caller |

### 11.2 Cost and time per reviewer (question 6)

- [E1] Not recorded per reviewer in the product. The contract has per-wave durations and token estimates (SKILL.md:943-944). The experiment derives per-run USD, per-alias tokens/USD and run minutes (`extract.py:63-77`, :126-128); per-reviewer split is impossible when reviewers share a tier alias.
- [E2] Per reviewer, per attempt: `wall_s`, `output_tokens_main`, `output_tokens_all`; summed in `cost.json` (`run-reviewer.sh:58`, :87). No input/cache tokens, no USD. Sums are wrong when attempt files are overwritten or stale (`audit-A/summary.md:12`, :15-16).
- [E3] Schema supports per reviewer `tokens_in`, `tokens_cache_read`, `tokens_cache_write`, `tokens_out`, `wall_s` (`telemetry.py:74-80`) and a `cost_per_confirmed_tp` from `tokens_out` (:371), but nothing writes it.

### 11.3 Design input for one run record (question 7)

Derived from the gaps above; each point names the code it extends.

1. **One manifest per run, profile-specific stage list.** Keep `review-panel-manifest/1` semantics (hash chain, idempotent replay, Conflict, commit point, resume) [E1], but let the profile declare its stages (a tasklist or spec panel [E2]/[E3] has `resolved -> dispatched -> collected -> merged -> published`; reflect keeps calibration and debate). Today `STATES` is a fixed tuple (`manifest.py:39-49`).
2. **Store attempt payloads, not only their hash.** Each attempt carries the review-telemetry/1 `model` (resolved, launch, observed), `slot` (tier, alias, fallback_depth, stand_in) and `cost` groups [E3], plus `exit`, `started_utc`, `wall_s`, `usd` and the transcript-derived served id [E2]/[E1 extract]. The hash stays for idempotency (`manifest.py:353`).
3. **Fallback as attempts.** Each fallback hop is a new attempt with its own model; `superseded_by` already links them (`manifest.py:382-383`). This replaces `fallback.log` and fixes the expected-model overwrite [E2].
4. **Per-reviewer output counters at collection/merge.** `findings_raw`, `findings_kept`, `rejected[{id, reason}]`, `blocking_rejected`, `block_ok_first_parse`, `report_sha256`. Sources: `findings_v2.parse_block` per-line errors (scope slice 02 D1), `ledger.py:141-149` [E3], audit D conservation [E2].
5. **Built-in run checks evaluated before `published`.** From audit A and D [E2] and the exit aggregator [E1]: observed == launch for every complete attempt; merged reviewer set == resolved set; each report sha at merge == sha at collection; no blocking finding rejected silently (warn or fail by profile); chain-size flag from the cluster step [E1 `cluster.py:422`]; cost sum == sum of attempt costs. Store the check results in the `validated` or `published` stage payload.
6. **Telemetry as a projection of the manifest.** Emit review-telemetry `reviewer_run` records from the committed manifest (one per reviewer's final attempt) instead of a separate hand-built record, and lift the `stratum` restriction to a data-driven class list (the tier file `classes` map) [E3] [E1]. Keep `outcome` records for judge/ground-truth scoring [E3] [E2].
7. **Reflect `telemetry:` block** keeps its consumer-facing summary fields, but `reviewers_*`, `cluster_agreement`, `calibration_coverage`, `findings_block_compliance_rate` should be copied from code outputs (manifest, `clusters.json`) by a CLI, not typed by the agent [E1].
8. **Policy hashes computed by the CLI** from the template, tiers and brief files, not passed in (`manifest_cmd.py:67-69`) [E1].
9. **Retry in place after failure**: allow a new invocation after `failed` with the same inputs (today it is stuck, `manifest.py:449-450`, :300-301) [E1].

**Key Takeaways**
- [E1] [E2] [E3] Each effort records a different third of a run: E1 state and hashes, E2 served identity and per-attempt cost, E3 a full per-reviewer schema and outcome scoring that nothing writes.
- The cheapest unification is: the E1 manifest as the single record, attempt payloads in E3's telemetry groups, E2's transcript identity method and audit checks as built-in validators.

---

## 12. Doc-sourced claims and their verification status

| Claim (source) | Tag | Evidence |
|---|---|---|
| Manifest stages, idempotency identity, superseding, counts, resume and publish rules (manifest.py docstring :1-26) | [CODE-VERIFIED] | `manifest.py:39-53`, :277-386, :402-470, :476-534 |
| "`advance published` records their hashes and rewrites nothing" in shadow mode (SKILL.md:349) | [CODE-VERIFIED] | `manifest_cmd.py:200-203`, `manifest.py:527-534`, `publish_files` refuses shadow :496-500 |
| Attempts recorded with `--stage dispatched/collected --completion` (SKILL.md:342) | [CODE-VERIFIED] | `manifest_cmd.py:176-183`, `manifest.py:331-386` |
| `review cluster` prints `cluster_agreement` and `calibrated_findings` n/m (SKILL.md:345, :979-980) | [CODE-VERIFIED] | `cluster_cmd.py:174-196`, `cluster.py:405-412` |
| Aggregator recomputes parity and does not trust the boolean (SKILL.md:341, :981) | [CODE-VERIFIED] | `reflect_shadow_exit.py:117-177`, :225-237 |
| Contract with `telemetry:` block "Written to `<output>/return-contract.yaml`" (SKILL.md:722) | Skill path: agent-executed, no code writer of the 1.8.0 contract [CODE-VERIFIED by absence]; general claim "no Python writer of `return-contract.yaml`" [CODE-CONTRADICTED] | `ensemble.py:886-895` writes a version-"1.0" reflect contract at the same path for `superclaude reflect run` (section 6 writer table; research/13 §4) |
| `manifest_path` = `<output>/panel/manifest.json` (SKILL.md:983) | [CODE-VERIFIED] | `manifest_cmd.py:19-20` |
| D15: strata only sonnet/haiku; merge and panel resolve write no telemetry (hand-off, scope slice 02 row D15) | [CODE-VERIFIED] for strata and merge (`telemetry.py:112-115`, :267-268; `merge_cmd.py:5-10`, :71-118); panel resolve not re-read in this slice [UNVERIFIED for `panel_cmd.py`] | |
| `_ID_TOKEN` at `telemetry.py:22` (task prompt; scope slice 02 D7) | [CODE-CONTRADICTED] | `_ID_TOKEN` is :23; :22 is `_TS` |
| "Six independent read-only audits ... (summaries in `summary.md`)" (hand-off 2.6, HANDOFF:139) | [CODE-CONTRADICTED] | only `audit-A/summary.md` and `audit-D/summary.md` exist at the commit (git ls-tree) |
| `meta.json` fields "expected/observed model, model_ok, findings_block, attempts, wall, output tokens" (hand-off 5.4) | [CODE-VERIFIED] with one correction | template `run-reviewer.sh:58`: the key is `attempt` (final attempt number), plus `exit`, `output_tokens_main`, `output_tokens_all`; "attempts" is in `cost.json` (:87) |
| Audit A is "repeatable: `uv run --no-project python -I audit.py`" (`audit-A/summary.md:2`) | [CODE-CONTRADICTED] for re-running from the commit | `audit.py` reads `attemptN.json` and `attemptN.meta.json` (:53, :65, :73), and 0 of those files are committed; paths hard-coded to another worktree (:2) |
| Audit D chain replay (195 chained rows among 1398 ledger rows in total, 83 mega-rows) (`audit-D/summary.md:29`) | [CODE-VERIFIED] script; wording "rows with >=3 members" [CODE-CONTRADICTED] | `audit-D/audit2.py:139-155` (`rows_total` :140 before the `< 3` filter :145; `chain_total` :154); not in `audit.py` |
| Audit D drop reasons by replaying `_check_finding` (`audit-D/summary.md:15-16`) | [UNVERIFIED] as to which script | `audit-D/audit.py` uses its own lenient parser (:17-31), not `_check_finding` |

---

## Gaps and Questions

1. [E1] `manifest.validate` does not check the `deps.prev` hash chain or that `reviewers_complete` equals the recount; only `reusable_stages` checks the chain, and it has no caller outside tests.
2. [E1] A run in state `failed` cannot be retried in the same `--out` with the same inputs and run id (`manifest.py:449-450`, :300-301; `manifest_cmd.py:121-122`). Is a new output directory the intended recovery?
3. [E1] Attempt payloads are stored only as a hash (`manifest.py:353`); in shadow mode they are recorded with no payload at all (SKILL.md:342). No product record holds per-reviewer model, tokens, cost or wall time.
4. [E1] Per-reviewer cost cannot be derived from E1 logs when reviewers share a gateway alias (`extract.py:70-73` keys usage by alias). Is per-reviewer cost needed for the core, and if so must the dispatcher record it per Agent call?
5. [E1] The reflect `telemetry:` block is agent-written on the skill path (SKILL.md:722; no code writer of the 1.8.0 contract, confirmed by absence in the Phase 3 fix cycle 1; the only code writer of a reflect contract is `ensemble.py:886-895`, version "1.0", no `telemetry:` block); values like `cluster_agreement` and `reviewers_*` are copies of code outputs and can drift. `reflect_shadow_exit.py` already distrusts `panel_parity`; the others are trusted.
6. [E3] review-telemetry/1 has no caller in `src` (Grep); D15 strata restriction rejects every gateway class. Who decides the replacement stratum list (owner decision "D3" per `telemetry.py:115`)?
7. [E3] `KINDS` (`telemetry.py:19`) is the review kind, not the record kind, and `task.review_kind` is never validated against it.
8. [E3] `telemetry append` with a list is not atomic (`telemetry_cmd.py:65-70`).
9. [E3] `merge_cmd` writes no telemetry and the ledger stores only the intended model (`merge_cmd.py:73-83`); dropped finding ids are not stored (`ledger.py:130-134`, :141-149).
10. [E2] No `fallback.log`, `attemptN.json` or `attemptN.meta.json` is committed, so the fallback format is known from `run-reviewer.sh:75` only and audit A cannot be re-run from the commit.
11. [E2] `expected_model` overwrite on fallback (`run-reviewer.sh:58`, :76), attempt-file overwrite across hops and stale attempt files make `cost.json` unreliable (`audit-A/summary.md:12`, :15-16).
12. [E2] `audit-A/audit.py:33` uses `fam` before assignment in the no-resolution branch.
13. [E2] The chain replay is `audit-D/audit2.py:139-155` (resolved in the Phase 3 fix cycle 1; its "of 1398" denominator is all ledger rows). Which script implements the `_check_finding` drop-reason replay remains [UNVERIFIED] (`mk.py`, `anch.py`, `bok.py` not read).
14. `panel_cmd.py` / `panel resolve` writing no telemetry (second half of D15) was not re-read in this slice [UNVERIFIED].
15. Resolved in the Phase 3 fix cycle 1: the SKILL.md `return-contract.yaml` writer claim (:722) has no code writer for the skill's 1.8.0 contract; a code writer of a different, version-"1.0" reflect contract exists at the same path (`ensemble.py:886-895`, section 6 writer table). Open: two reflect contract schemas share one file name and one reader (`contract.py`); which one a unified run record keeps is a design decision. [E1]
16. [CODE-CONTRADICTED] items to carry into the report: hand-off 2.6 "summaries in summary.md" for six audits (only A and D); `_ID_TOKEN` line (:23, not :22); audit A "repeatable" from the committed tree.
17. Question for the core design: should the built-in checks fail a run (verdict-affecting) or only warn? E2's audits marked EXCLUDE; E1's exit aggregator FAILs the stage exit but not the individual reflect run.

## Stale Documentation Found

- **[STALE DOC]** Task prompt and scope slice 02 (row D7): `_ID_TOKEN` cited at `telemetry.py:22`; it is at :23 (:22 is `_TS`). Scope slice 02's remark that the hand-off's :23 was `_ID_RE` is itself wrong (`_ID_RE` is :24).
- **[STALE DOC]** Hand-off 2.6 (HANDOFF:139): "summaries in `summary.md`" for all six audits; only A and D have one (already noted by scope slice 01 gap 1).
- **[STALE DOC]** Hand-off 5.4: `meta.json` "attempts" field; the runner writes `attempt` (final attempt number) in `meta.json` and `attempts` in `cost.json` (`run-reviewer.sh:58`, :87).
- **[STALE DOC]** `audit-A/summary.md:2` and `audit-D/summary.md:2` reference `/tmp/audit-*` script paths and call audit A repeatable; the inputs it needs are not in the commit.
- `ledger.py` docstring vs code mismatch (D2) is covered by scope slice 02, not re-checked here.

## Summary

The three efforts record a panel run three incompatible ways: [E1] a strict, hash-chained stage manifest (`review-panel-manifest/1`) with resume and a publish commit point, plus agent-written `telemetry:` fields in `return-contract.yaml` and code-written `panel/clusters.json`; [E2] a bash runner that writes per-run `meta.json` (with transcript-derived served model and a `model_ok` gate) and `cost.json`, a free-text `fallback.log`, and six after-the-fact audits of which A (identity, attempts, cost consistency) and D (dropped findings, report sha vs ledger, panel/path equality, blocking consistency) have summaries; and [E3] a rich review-telemetry/1 schema (three model identities, policy hashes, slot/fallback depth, document descriptors, output counts, tokens and wall time, plus outcome scoring) that nothing in `src` writes and whose strata are hard-coded to sonnet/haiku (D15 confirmed). None of the product records stores served model, per-reviewer cost or the ids of rejected findings: the manifest keeps attempt payloads only as hashes, the ledger keeps the intended model and a first-error warning, and E2's records lose the intended model and miscount cost on fallback. Per-reviewer cost is recorded only by E2 (output tokens and wall), while E1's experiment derives per-run USD per gateway alias from session logs. The recommended single run record is the E1 manifest with profile-specific stages, attempt payloads in E3's telemetry groups (resolved/launch/observed model, tokens, wall, USD), fallback hops as superseding attempts, per-reviewer kept/rejected counters, and audits A/D plus the shadow-exit checks turned into built-in checks evaluated before `published`, with telemetry records emitted as a projection of the committed manifest.
