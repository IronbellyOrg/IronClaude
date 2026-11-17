# Research: Shared review CLI package (scope slice 2 of 5)
**Scope:** `src/superclaude/cli/review/` (all `.py` files and `data/*.json`) and `tests/review/`
**Status:** Complete
**Date:** 2026-11-14
**Branch:** ironbelly/shadow-runs (master = d2d8a2d16 contains reflect Stage 0-2 merge)
---

Method: line counts by `wc -l`; origin of each file by `git log --diff-filter=A` (first-add commit). `git log d2d8a2d16..HEAD -- src/superclaude/cli/review tests/review` is empty, so the package on this branch equals d2d8a2d16 (master). The local `master` ref in this worktree is stale (80f361804); d2d8a2d16 is an ancestor of HEAD. codegraph MCP tools were not available to this agent; Grep/Read/Bash were used.

Origin keys: **#346** = added by 9163bd1c7 (2026-11-11, "Merge 346Claude-integration into master (#346 review loop, @live7 panel ...)"). **reflect** = added by d2d8a2d16 (2026-11-12, "feat(reflect): Stage 0-2 of the Tier 2 review panel ... (#519)"). **#346+reflect** = added by #346, then extended by d2d8a2d16 (`git diff --stat 9163bd1c7 d2d8a2d16`: `__init__.py` +3, `panel.py` +206/-15 (total for the 4 files: 248+/15-), `panel_cmd.py` +48, `review-tiers.default.json` +6).

## 1. Module inventory

| Path (under `src/superclaude/cli/review/`) | Lines | Origin | Purpose | Public functions / CLI commands | Imports from this package | Imported by |
|---|---|---|---|---|---|---|
| `__init__.py` | 36 | #346+reflect | `review` click group; optional subcommand loader | `review_group` :15; loads `panel_cmd, merge_cmd, ledger_cmd, telemetry_cmd, lint_cmd, estimate_cmd, cluster_cmd, verify_cmd, manifest_cmd` (:19-29), swallowing `ModuleNotFoundError` only for the exact module name (:30-35). Reflect added the last three names. | dynamic import of `*_cmd` | `cli/main.py:568-570` (`main.add_command(review_group, name="review")`) |
| `findings.py` | 457 | #346 | findings-v1 parser, fixmap-v1 parser, anchor locate, section naming, refs normalisation, fingerprint, v1 clustering, diff span mapping | `parse_block` :124, `parse_fixmap` :205, `flat` :272, `locate` :276, `section_of` :307, `refs_norm` :321, `fingerprint` :340, `annotate` :346, `same_defect` :367, `cluster` :382, `opcodes` :413, `map_span` :430, `hunks_touch` :442; constants `SEVERITIES` :14, `CATEGORIES` :15-22, `PRIOR_STATUSES` :23, `ACTIONS` :24; private `_ID` :26, `_REF_TOKEN` :29, `_HEAD_FINDINGS` :31, `_blocks_after` :38, `_check_flat` :79, `_check_finding` :90 | none | `ledger`, `ledger_cmd`, `findings_v2`, `card_convert`, `cluster` |
| `ledger.py` | 494 | #346 | review-ledger/1 store: merge a round of reviewer reports into rows, revision mapping, defer, verdict, capture matrix, merged report | `LedgerError` :29, `sha256_text` :33, `new_ledger` :37, `load` :41, `save` :52, `merge_round` :107, `apply_revision` :301, `defer` :350, `verdict` :363, `capture` :375, `render_merged_report` :408 | `findings` (:15) | `merge_cmd`, `ledger_cmd` |
| `merge_cmd.py` | 118 | #346 | `superclaude review merge` | `command` :21/:71 (ledger, doc, round, reports, resolution, out, cap) | `ledger` | `__init__` |
| `ledger_cmd.py` | 137 | #346 | `superclaude review ledger {revise,defer,verdict,capture}` | `revise_cmd` :36/:61, `defer_cmd` :74/:83, `verdict_cmd` :94/:101 (exit PASS 0 / REVISE 10 / ESCALATE 11, `EXIT_BY_DECISION` :13), `capture_cmd` :112/:126 | `findings`, `ledger` | `__init__` |
| `panel.py` | 707 | #346+reflect | panel template + tier file validation; resolve reviewer slots to model ids | `NoModelAvailable` :49, `ExclusionExhausted` :57 (reflect), `validate_reflect_profile` :80 (reflect), `validate_panel` :160, `validate_tiers` :258, `find_path` :397, `packaged_panel` :430, `load_panel` :447, `load_tiers` :470, `select_env` :485, `resolve_slot` :500, `sha256_json` :559, `resolve` :565 | none | `panel_cmd`; `scripts/reflect_shadow_exit.py:52` |
| `panel_cmd.py` | 129 | #346+reflect | `superclaude review panel {resolve,validate}` | `resolve_cmd` :18/:64 (reflect added `--hard-exclude-class` repeatable, expanded through the tier file `classes` map, case-insensitive, unknown class = UsageError; and `--strict-distinct`; `ExclusionExhausted` surfaces as ClickException with its type name), `validate_cmd` :111/:116 | `panel` | `__init__` |
| `telemetry.py` | 447 | #346 | review-telemetry/1 JSONL records + SQLite load | `new_record_id` :118, `now_utc` :122, `task_variables` :142, `validate_record` :196, `append_record` :287, `load` :382 | none | `telemetry_cmd` |
| `telemetry_cmd.py` | 98 | #346 | `superclaude review telemetry {taskvars,append,load}`; default dir `.dev/benchmarks/review-telemetry` (:12) | `taskvars_cmd` :20/:30, `append_cmd` :41/:56, `load_cmd` :73/:84 | `telemetry` | `__init__` |
| `findings_v2.py` | 304 | reflect | findings-v2 contract: v1 container + citations, lens, deviation_class, reflect_category, coverage_rows, self_confidence, channel; completion states | `check_finding` :84, `channel_of` :190, `coverage_context` :196, `parse_block` :215; constants `INFO` :24, `V1_FIELDS` :25-34, `ROLES` :35, `LENSES` :36, `CHANNELS` :37, `DEVIATION_CLASSES` :38, `COMPLETION_STATES` :40, `REFLECT_CATEGORIES` :41-48; private `_check_citation` :59 | `findings` (`_HEAD_FINDINGS, _ID, CATEGORIES, SEVERITIES, _blocks_after, _check_flat`, :15-22) | `card_convert`, `cluster`, `cluster_cmd`, `verify_cmd` |
| `card_convert.py` | 517 | reflect | converts legacy reflect reviewer cards (shapes `yaml-blocking-minor`, `yaml-other-severity`, `markdown-table`, `unlisted`, :65) into findings-v2 lines | `convert_card` :333, `snapshot_paths` :451, `convert_card_file` :474, `summarize` :496; `MAX_REF_TEXT=200` :85, `MAX_CLAIM=300` :86 | `findings` (`_ID, flat`, :57), `findings_v2` (:58+) | `cluster_cmd`; `scripts/reflect_stage0a_replay.py:65` |
| `cluster.py` | 487 | reflect | v2 path-aware clustering (K4 `cluster_v2`) + `cluster_agreement` telemetry value; second pass over validator-kept findings | `annotate` :126, `same_defect_v2` :161, `cluster_v2` :381, `clusters_kept` :447; `PRIMARY_ROLES` :67 | `findings` (`refs_norm`, :64), `findings_v2` (`_check_citation`, :65) | `cluster_cmd` (lazy import :136, calls :166/:169); `scripts/reflect_stage0a_replay.py:66` |
| `cluster_cmd.py` | 197 | reflect | `superclaude review cluster <cards> --snapshot --calibration --coverage --kept --out`; writes `clusters.json` or `panel/clusters_kept.json` | `command` :96/:133 | `card_convert`, `findings_v2`, `cluster` (lazy) | `__init__`, `verify_cmd` |
| `verify_cmd.py` | 184 | reflect | `superclaude review verify-citations` (schema `review-precheck/1`, :25): flags citations to re-read; drops nothing | `command` :76/:113 (cards, snapshot, root, coverage, out) | `cluster_cmd`, `findings_v2` | `__init__` |
| `manifest.py` | 534 | reflect | reflect run manifest: staged pipeline state, hashes, attempts, resume, publish/commit | `ManifestError` :67, `Conflict` :71, `OutOfOrder` :75, `NotCommitted` :79, `Invalid` :83, `sha256_json` :87, `sha256_file` :93, `policy_sha256` :97, `new_manifest` :111, `save` :156, `load` :166, `read_committed` :176, `validate` :192, `advance_stage` :277, `record_attempt` :331, `fail` :389, `reusable_stages` :402, `resume` :422, `publish_files` :476, `commit_published` :521, `hash_published_files` :527 | none | `manifest_cmd`; `scripts/reflect_shadow_exit.py:51` |
| `manifest_cmd.py` | 240 | reflect | `superclaude review manifest {init,advance,validate}` | `init_cmd` :53/:79, `advance_cmd` :137/:160, `validate_cmd` :218/:225 | `manifest` | `__init__` |

Packaged data (`data/`):

| File | Lines | Origin |
|---|---|---|
| `review-panel.default.json` | 13 | #346 |
| `review-panel.live7.json` | 15 | #346 |
| `review-panel.reflect-pre.json` | 13 | reflect |
| `review-panel.reflect-pre-x2.json` | 12 | reflect |
| `review-panel.reflect-post.json` | 13 | reflect |
| `review-panel.reflect-post-x2.json` | 12 | reflect |
| `review-panel.reflect-enterprise.json` | 13 | reflect |
| `review-panel.reflect-lite.json` | 13 | reflect |
| `review-tiers.default.json` | 38 | #346; reflect added the `classes` map (model id to class: opus, sonnet, haiku, fable, gpt, muse, glm, grok, qwen) |

Skill callers [CODE-VERIFIED by grep]: `sc-reflect-protocol/SKILL.md:345` runs `superclaude review cluster` and `superclaude review verify-citations`; `:347` runs the `--kept` pass. No skill calls `review merge`/`review ledger` in `src` (consistent with hand-off D14; not re-grepped beyond this package's callers).

Observations:
- Two parallel stacks share one package: **v1 stack** (`findings` -> `ledger` -> `merge_cmd`/`ledger_cmd`, plus `telemetry`) and **v2 stack** (`findings_v2` -> `card_convert`/`cluster` -> `cluster_cmd`/`verify_cmd`, plus `manifest`). Shared: `panel.py` (both), and the v1 primitives that v2 imports from `findings.py`.
- The v2 stack imports **private** v1 names (`_check_flat`, `_ID`, `_blocks_after`, `_HEAD_FINDINGS`, plus `refs_norm`, `flat`). Changing the v1 limits or the v1 heading/fence rules changes v2 too.
- There is no v2 ledger, no v2 verdict and no v2 merged report: the v2 stack is telemetry/flagging only ("Neither drops anything and neither feeds the debate", SKILL.md:345). Reflect's verdict still comes from sc-adversarial Mode A + evidence validator.

## 2. The two finding contracts side by side

All cells [CODE-VERIFIED] from `findings.py:14-196` and `findings_v2.py:1-304` (read in full for those ranges).

| Aspect | findings-v1 (`findings.py`) | findings-v2 (`findings_v2.py`) |
|---|---|---|
| Container | `## Findings block` heading (`_HEAD_FINDINGS` :31, any level 1-6, case-insensitive) then fenced block, info `findings-v1`, one JSON object per line (`parse_block` :124-196) | Same heading regex and same `_blocks_after` fence scanner imported from v1 (`findings_v2.py:15-22`); info `findings-v2` (:24) |
| Multiple blocks | last used, error "more than one" (:143-150) | same (:247-253) |
| Truncated (unclosed) block | `ok=False` + error (:151-158) | `state="truncated"` (:299-300) |
| Result shape | `{ok, findings, priors, errors}` | `{ok, state, findings, errors}`; `state` in `complete/truncated/invalid` (`COMPLETION_STATES` :40 also lists `failed`, `timed_out` for callers) |
| Bad line handling | line skipped, error `{line,msg}` appended, `ok=False` (:188-192). Other valid lines still returned. | line skipped, error appended, state becomes `invalid` (:284-287, :301-302). Other valid lines still returned. |
| Empty block | valid (`ok=True`, no findings) | **invalid** unless `assigned_rows` non-empty and every assigned row is in `observed_rows` (:291-298) |
| Prior lines (re-review) | `{"prior": id, "status": resolved/open/regressed}` (:175-187, `PRIOR_STATUSES` :23) | **rejected** (:279-283) — v2 has no re-review protocol |
| `id` | `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (:26, :92), unique | same `_ID` (:99-102), unique |
| `severity` | `CRITICAL/MAJOR/MINOR` (:14, :96) | same `SEVERITIES` (:103) |
| `blocking` | real bool; MINOR cannot be blocking (:98-101) | same (:105-108); **plus** when `reflect_category` is set: blocking must equal `severity != MINOR` (:161-162) |
| `category` | `contradiction, unpassable-check, data-loss, safety, missing-requirement, other` (:15-22) | same `CATEGORIES` (:109); optional `reflect_category` in `ordering, acceptance, coverage, contradiction, risk, deviation` mapped to allowed v1 categories (`REFLECT_CATEGORIES` :41-48, check :155-164) |
| `claim` | string, at most **300** chars after whitespace flattening (:118) | same, **300** (:111) |
| `anchor` | **required**, 12-**200** chars flattened (:104) | required **only if** `citations` absent (:123-126); if present alongside citations, still 12-200 (:131-132) |
| `anchor2` | optional, 12-**200** (:107-110) | optional, 12-**200** (:135-137) |
| `refs` | list of at most **8** strings (:111-117) | same (:114-120) |
| `citations` | n/a | optional list of **1-8** objects `{role, path, line_start, line_end, quote?}` (:128-130); `role` in `ROLES = plan, spec, source, test, diff, artifact` (:35); path repo-relative, no `..`, no drive/absolute (:64-75); `1 <= line_start <= line_end` (:76-78); `quote` optional 12-**200** (:79-80) |
| `lens` | n/a | `spec, reflect-pre, reflect-post` (`LENSES` :36); per-line lens must equal the block lens passed by caller (:140-145) |
| `deviation_class` | n/a | `authorized, necessary, drift, regression, none` (:38); **required** when lens is `reflect-post` (:147-149) and when `reflect_category == deviation` (:163-164) |
| `coverage_rows` | n/a | list of strings, each must be in caller-supplied `assigned_rows` (:166-176) |
| `self_confidence` | n/a (no confidence field at all) | optional number 0-1 (:178-182) |
| `calibrated_confidence` | n/a | **forbidden** in the reviewer line (:96-97): calibration is added downstream, never self-reported |
| `channel` | n/a | `defect, grounding-gap, advisory` (`CHANNELS` :37); absent or unknown = `defect` (`channel_of` :190-193) |
| Roles / lenses | none: reviewer identity comes from the merge command's `--resolution` (reviewer_id, model) | role is per **citation**, lens per block/line; reviewer id from card file name (cluster_cmd; UNVERIFIED detail) |
| Location model | **anchor**: exact text quote, located by whitespace-flattened substring in the candidate document (`locate` :276; `annotate` :346) | **citations** (file:line ranges across several documents) as the primary location; anchor optional |

Answers to the specific questions:
- **findings_v2 imports v1 limits:** YES [CODE-VERIFIED]. `findings_v2.py:15-22` imports `_HEAD_FINDINGS, _ID, CATEGORIES, SEVERITIES, _blocks_after, _check_flat`; the limits are passed literally at each call (`claim` 300 at :111, `anchor` 12-200 at :126/:132, `anchor2` at :136, citation `quote` 12-200 at :80). So the 200/300 numbers are **duplicated literals**, not shared constants; `_check_flat` (v1 :79-87) supplies only the flattening + compare logic.
- **Backward compatibility claim** (docstring :3): a v1-valid line whose keys are all in `V1_FIELDS` passes v2 unchanged. Not true for prior lines (rejected) and for an empty block (invalid without coverage).
- **card_convert truncates instead of rejecting** for legacy reflect cards: claim cut to 297 chars + `...` (`card_convert.py:199-201`); unresolved refs cut to 200 (`:108`). It does not emit `quote` or `anchor`, so it never hits the anchor limits. A card line with any unresolved citation is reported with reason "N unresolved citation(s)" and is not passed to `check_finding` (`:222-227`). Reviewers that write findings-v2 natively get **rejection**, not truncation (same as v1).

## 3. The two clustering paths

Sources [CODE-VERIFIED]: `findings.py:321-407`, `ledger.py:107-279` (partial: 107-163, 184-279), `cluster.py:1-56` (module docstring = the rules spec) and `cluster.py:161-181`; chaining/union-find lines located by grep (`cluster.py:306-316, 324, 370, 404, 422`). Rest of `cluster.py` (records validation, support maths at :184-447) UNVERIFIED by full read; the docstring is taken as its contract.

| Aspect | v1: `findings.cluster` (used by `ledger.merge_round`, `ledger.py:165`) | v2: `cluster.cluster_v2` (used by `cluster_cmd` :169, `clusters_kept` :447-485, `scripts/reflect_stage0a_replay.py`) |
|---|---|---|
| Input | annotated v1 findings of one round, all reviewers, in report order; annotation locates the anchor in **one** candidate document (`annotate` :346-360) | reviewer records `(reviewer_id, ordinal, findings_v2 block, calibration_map)` + snapshot file list; **no document text** (docstring :3-15, :28) |
| Invalid blocks | parsable findings of an invalid block are **kept and clustered** (`ledger.py:112, 135-138`) | findings of a block whose state is not `complete` are **not clustered**; that reviewer is not complete (docstring :9-11) |
| Location unit | anchor span (line range) in the candidate + optional `anchor2` span (`_spans` :363-364) | resolved citations `(role, path, line_start, line_end)`; a citation is resolved only if its path is in the snapshot list by exact string equality (docstring :21-23) |
| Fingerprint | `sha256("v1|" + section + "|" + refs)` (:340-343); section = nearest heading of the anchor (`section_of` :307) or `"none"` | `sha256("v2|" + role + "|" + path + "|" + section + "|" + refs + "|" + class)` over the primary citation; **section is always ""** (docstring :26-29) |
| Same-defect rule | equal fp **and** non-empty refs; else (refs intersect, or both empty) **and** spans within 3 lines (:367-379) | equal fp **and** non-empty refs; else deviation classes compatible **and** (refs intersect or both empty) **and** a resolved citation of each on the same path within `SPAN_TOLERANCE` lines (:161-181; docstring says 3) |
| Refs extraction | `refs_norm` with `_REF_TOKEN = [A-Z]{1,4}-digits(.digits)* | P[0-9]` (:29, :321-337) | **same `refs_norm`** imported from v1 (`cluster.py:64`) |
| Grouping | union-find, transitive (:382-407) | union-find, transitive (`cluster.py:306-316`) |
| Chaining | not detected | detected: `chained` = two members do not match pairwise (:324, :370); listed in output (:422); excluded from `cluster_agreement` (:404) |
| Representative / row fields | **first** member's `fp`, `category`, `anchor`, `claim` (`ledger.py:186, 191, 194, 199`) | member with the **highest calibrated confidence** (ties by resolution order) gives the claim (docstring :45-47) |
| Blocking | `any(m["blocking"])` (`ledger.py:187`; re-found rows use current round's `any`, :213-218) | `blocking_any` / `blocking_all`; cluster blocking when `blocking_any` (docstring :46-47); `disputed` flag when support <0.5, blocking disagreement, or two different deviation classes (:48-49) |
| Confidence | `single` / `overlap` by distinct reviewers per round (`ledger.py:86-90`); never used in the verdict | `support` = calibrated-confidence-weighted share of complete reviewers (docstring :35-44); `None` + `uncalibrated` list when calibration is missing |
| Output effect | creates/updates ledger rows that **drive the verdict** (`ledger.py:273-274`) | telemetry + flagging only (`cluster_agreement`, `clusters.json`); never routes or drops (SKILL.md:345) |

Differences that matter for unification:
- **Over-merge by fingerprint differs in kind.** v1 merges two findings in the same **section** with the same refs. v2 merges two findings whose primary citations are on the same **file** (same role) with the same refs, anywhere in that file, because section is always "" (docstring :28). For a tasklist where many findings cite `plan` + the same requirement id, v2's fp rule is coarser than v1's.
- **Chaining exists in both**; v2 only reports it (`chained`) and keeps it out of the agreement metric, it does not split the cluster.
- **Requirement-id regex is shared** (v2 imports `refs_norm`), so D7 (tasklist ids like `T01.02` not matched) applies to both.
- v1 needs the candidate text (anchors); v2 needs a snapshot file list (citations). A unified clusterer must accept either location type (anchor-only v1 lines are valid v2 lines when `citations` is absent, but `cluster_v2` then has nothing to match on [CODE-VERIFIED `cluster.py:126-154`]: with no `citations`, `primary` is None, `fp` is None (:143-147), and `same_defect_v2` needs either a fp or a resolved citation (:163-181), so an anchor-only finding is always a **singleton cluster**. The anchor text is used only as input to `refs_norm` (:138-141). Feeding v1-style reports through `cluster_v2` today would therefore produce zero cross-reviewer agreement.

## 4. panel.py: templates, tiers, environment, distinctness, reflect profile

Sources [CODE-VERIFIED]: `panel.py:60-137`, `:485-494` (grep), `:500-707`; all `data/*.json` printed in full; `panel_cmd.py` diff 9163bd1c7..d2d8a2d16.

### 4.1 Templates (`data/review-panel.*.json`, schema `review-panel/1`, all `distinct_across_slots: true`, `apply_to: ["first"]`)

| Template | Origin | Slots (slot_id: tier x count, strategy) | Reviewers | Notes from `description` |
|---|---|---|---|---|
| `default` | #346 | t1b: tier1b x1 fixed; t2: tier2 x1 random; t3: tier3 x2 random | 4 | "Production review panel"; t1b is the anchor |
| `live7` | #346 | t1b x1 fixed; t2 x1 random; t2b x1 random; t3 x2 random; t4 x2 random | 7 | anthropic-only = 1 Sonnet + 6 Haiku; gateway needs `claude-gw-tier2b` alias |
| `reflect-pre` | reflect | t1b: tier1b x1 fixed; t4: tier4 x1 random; t1a: tier1a x1 random | 3 | anthropic-only strict = sonnet, haiku, opus; personas by order: analyzer, qa, refactorer |
| `reflect-pre-x2` | reflect | t4: tier4 x1 **fixed**; t1a: tier1a x1 random | 2 | anchor replacement when tier1b is exhausted by the executor (executor sonnet) |
| `reflect-post` | reflect | same slots as reflect-pre | 3 | mirrors reflect-pre |
| `reflect-post-x2` | reflect | same as reflect-pre-x2 | 2 | mirrors reflect-pre-x2 |
| `reflect-enterprise` | reflect | same slots as reflect-pre | 3 | third persona is architect (`--strategy enterprise`) |
| `reflect-lite` | reflect | t1b x1 fixed; t4 x1 random; t2 x1 random | 3 | variant arm only; soft = sonnet, haiku, haiku; strict = sonnet, haiku |

Personas are NOT in the template; they are assigned by resolution order in the skill (description text only). Re-review (`review_kind` not in `apply_to`) resolves only the fixed slot(s), count 1 (`panel.py:600-605, 616`).

### 4.2 Tier file (`data/review-tiers.default.json`, schema `review-tiers/1`, version 1.0.0)
- `aliases` tier1a, tier1b, tier2, tier2b, tier3, tier4: `{alias: "claude-gw-<tier>[1m]", models: [...]}`; first model = default for `fixed`. Lists match hand-off 5.3 [CODE-VERIFIED]. No `tier0` alias exists in the file, though `validate_reflect_profile` checks for one (`panel.py:95-117`).
- `names` (display names), `classes` (reflect-added, model id -> class), `environments`:
  - `gateway`: `available: "all"`, no stand-ins, empty `launch`.
  - `anthropic-only`: available opus, sonnet, haiku, fable; stand-ins tier2/2b/3/4 = haiku; `launch` maps id -> `opus|sonnet|haiku|fable`.
- File path resolution: `find_path(kind, explicit, environ)` :397 — explicit path, then `SUPERCLAUDE_REVIEW_PANEL` / `SUPERCLAUDE_REVIEW_TIERS`, then a `review-panel.json` / `review-tiers.json` file (search locations UNVERIFIED, :414), then packaged data. `load_panel` also accepts a packaged name (`packaged_panel` :430; `@name` syntax UNVERIFIED by read).

### 4.3 Environment selection
`select_env` (:485-494): `--env`; else `$SUPERCLAUDE_REVIEW_ENV`; else `gateway` when `$T3Model01` is non-empty; else `anthropic-only`. `T2bModel01` does not occur in `cli/review` (grep rc=1).

### 4.4 Distinctness and exclusion (`resolve` :565-707, `resolve_slot` :500-556)
- Seeds: random slots use `"{slot.seed or base}|{slot_id}|{i}"`, `base` = `--seed` or first 8 hex of sha256(run_id) (:606-622); round_robin uses `--sequence` (or **today's date ordinal** when absent) + i - 1 (:623-628); fixed has no seed.
- `exclude` = models already chosen, when `distinct_across_slots` **or** `strict_distinct` (:631-635).
- **Soft distinctness** (`distinct_across_slots` only): `fixed` ignores `exclude` (takes `candidates[0]`, :536-537); random/round_robin drop excluded models, but if that empties the pool they **silently re-admit** all candidates (:539-543). No duplicate flag is written to the resolution.
- **`hard_exclude`** (reflect; CLI `--hard-exclude-class`, expanded via `classes`): filters candidates and stand-ins for every strategy (:519-529). Empty result -> `ExclusionExhausted` if exclusion caused it, else `NoModelAvailable` (:532-535).
- **`strict_distinct`** (reflect; CLI `--strict-distinct`): adds `exclude` to the hard set, so no re-admission (:519, :541-542). A **non-fixed** slot that is exhausted is skipped and listed in `skipped_slots`; the fixed anchor exhausting is fatal (:647-656). `skipped_slots` and `excluded` are written only when an exclusion option is used (:700-706).
- Resolution record per reviewer: reviewer_id `<slot_id>-<i>`, slot_id, tier, alias, strategy, seed, model, model_name, fallback_depth, stand_in, fallbacks, launch (:666-681); top level adds template/tiers versions and sha256, environment, run_id, review_kind (:688-699). Schema constant `RESOLUTION_SCHEMA` (value UNVERIFIED by read; hand-off says `review-panel-resolution/1`, and `panel_cmd` docstring says the same).

### 4.5 Reflect profile (`validate_reflect_profile` :80-134, `_check_reflect_resolution` :137+)
Applied when `template_id` starts with `reflect-` (:71, :588-592; also from `validate_panel` :254 when a tier file is given). Rules: no `tier0` slot; no tier listing a Tier 0 model; every model reachable from a slot (alias models + every environment's stand-ins) must have a `classes` entry and must not be Fable; at most **3** reviewers (`_REFLECT_MAX_REVIEWERS` :73); a round_robin slot needs `--sequence`. After resolution `_check_reflect_resolution` re-checks ids, fallbacks and `launch` values (`_REFLECT_LAUNCH = sonnet, opus, haiku` :72; body UNVERIFIED by read). Generic panels keep a 1..8 reviewer range (docstring :87).

## 5. Hand-off defects D1-D16 checked against the current code (d2d8a2d16 = this branch)

Verdict key: **CONFIRMED** = code at the cited place does what the hand-off says; **CONFIRMED (lines moved)** = behaviour holds, cited lines are stale; **PARTLY** = some of the claim holds; **OUT OF SLICE** = cites files outside this package (spot-checked only). "Reflect code shares it?" asks whether the reflect v2 stack (findings_v2, card_convert, cluster, cluster_cmd, verify_cmd, manifest, panel extensions) has the same defect.

| ID | Hand-off claim (short) | Current code | Verdict | Reflect code shares it? |
|---|---|---|---|---|
| D1 | anchor/anchor2 >200, claim >300 (also anchor <12, >8 refs, MINOR+blocking) reject the finding; only the first error is surfaced; dropped ids/count not stored | Limits `findings.py:104, 108, 118`; refs >8 :111-117; MINOR+blocking :100-101. Rejected line skipped (:188-192). `ledger.py:130-134` warns with `len(errors)` and only `errors[0]["msg"]`; `entries` store only `block_ok` (:141-149). | CONFIRMED (also note the warning does carry the error **count**, but not ids/reasons) | **YES for native v2 reviewers**: `findings_v2.check_finding` rejects with the same literals (claim 300 :111, anchor 12-200 :126/:132, anchor2 :136, refs 8 :114-120) plus new reject reasons (citation quote 12-200 :80, citations 1-8 :128-129, lens/deviation/coverage rules :140-186). Errors are returned per line in `parse_block` (:284-287) so they are not lost inside the parser; whether `cluster_cmd`/`verify_cmd` persist the per-line errors is UNVERIFIED. **NO for legacy cards via card_convert**: claim is truncated to 297+`...` (`card_convert.py:199-201`). Additionally v2 makes the **whole block** non-complete on any line error (`:301-302`), and `cluster_v2` then clusters **none** of that reviewer's findings (cluster.py docstring :9-11) — stricter loss than v1. |
| D2 | a `resolved_check` row becomes `resolved` when no cluster re-reports it, even if the re-reporting reviewer's block was invalid | `ledger.py:254-258` checks only `row["lid"] not in members_by_lid`; `block_ok` is not consulted. Docstring :112 says invalid reviewers are "skipped for clearing", which the code does not do. | CONFIRMED (code contradicts its own docstring) | N/A: v2 has no ledger/rounds. |
| D3 | merge fails only when no reviewer is valid; a round can PASS on one valid reviewer | `ledger.py:150-157` raises only when `not any(block_ok.values())`; verdict `FAIL if brief else PASS` (:273-274) | CONFIRMED | N/A for verdict (no v2 verdict). Analogue: `cluster_agreement` is None with <2 complete reviewers (docstring :50), so a 1-valid-reviewer run is visible as None, not as agreement. |
| D4 | one reviewer's `blocking` decides the row and verdict; `confidence` computed but unused | `ledger.py:187` `any(...)`; :213-218; `_confidence` :86-90; `_brief_ids` :99-104 uses only `blocking` + status; verdict :273-274 | CONFIRMED | PARTLY: `cluster_v2` cluster is blocking when `blocking_any` (docstring :46-47), but it also emits `support` (calibrated) and `disputed`. Nothing consumes them for a verdict yet (telemetry only). |
| D5 | missing anchors kept silently (`anchor_status "missing"`) | `findings.py:349-350` sets `anchor_status`, `span=None`, section `"none"` (:358); no warning appended in `merge_round` (warnings only at :132, :263) | CONFIRMED | Analogue: a citation whose path is not in the snapshot is `unresolved` (`cluster.py:115`) and a malformed one is counted (`citations.malformed`); findings are not dropped. `verify-citations` flags them for re-read (SKILL.md:345). So reflect surfaces it, but also does not drop. Line-range existence (line_end <= file length) is checked by verify_cmd? UNVERIFIED. |
| D6 | clustering over/under-merges; transitive union-find; row keeps first member's claim/category | `findings.py:367-407`; `ledger.py:186, 191, 194, 199` take `first[...]` | CONFIRMED | **YES, partly**: same transitive union-find (`cluster.py:306-316`). v2 **detects** chaining (`chained`, :324/:370/:422) and excludes chained clusters from agreement (:404), and picks the most-confident member as representative, but it does not split chains. v2 fp ignores line distance within a file (section always "", docstring :28), a new over-merge path. |
| D7 | ref-id regex needs letters-hyphen-digits; `T01.02` does not match | `findings.py:29` `_REF_TOKEN = \b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b`; same token in `telemetry.py:22` (`_ID_TOKEN`; hand-off said :23, which is `_ID_RE`) | CONFIRMED | **YES**: `cluster.py:64` imports `refs_norm` from v1. |
| D8 | reviewer brief never names the source document | OUT OF SLICE. Spot-check: `src/superclaude/rules/prompts/document_review_loop_prompts.md:17-21` placeholder list is CANDIDATE, BASELINE, PRIOR, N, IDS; first-review brief :32 names only `{{CANDIDATE}}` | CONFIRMED (spot-check) | Reflect brief lives in the skill (out of slice). findings-v2 has a `spec` / `source` citation **role** (`findings_v2.py:35`), so the contract can express source grounding; card_convert maps `source.md`/`spec` tokens to role `spec` (`card_convert.py:124-125`). |
| D9 | brief makes `missing-requirement` Medium, schema allows blocking | Schema side: `findings.py:15-22, 102-103` has no per-category blocking rule [CONFIRMED]; brief side OUT OF SLICE (prompt :31 is the grading-check line, not re-read in full) | PARTLY CONFIRMED | v2 with `reflect_category` set forces `blocking == (severity != MINOR)` (`findings_v2.py:161-162`): a different, explicit rule; `coverage` maps to `missing-requirement` (:44). |
| D10 | `unpassable-ac` rejected; only `unpassable-check` valid | `findings.py:17`; `grep -rn unpassable-ac src` returns nothing | CONFIRMED (fixed in eval only, as stated) | v2 uses the same `CATEGORIES`; reflect `acceptance` maps to `unpassable-check` (`findings_v2.py:43`). |
| D11 | `distinct_across_slots` silently allows duplicates when pool exhausted | `panel.py:539-543` (`pool = candidates` re-admission); `fixed` ignores `exclude` (:536-537); no duplicate flag in output (:666-699). Hand-off cited `panel.py:402-408` (pre-reflect lines). | CONFIRMED (lines moved) | Reflect **added the fix as opt-in**: `--strict-distinct` / `hard_exclude` (:519-543, :647-656) never re-admit and record `skipped_slots`. Default (`distinct_across_slots` only) still re-admits silently, for reflect templates too (`reflect-lite` description documents "sonnet, haiku, haiku under soft distinctness"). |
| D12 | env select keys on `$T3Model01`; `T2bModel01` never read | `panel.py:485-494`; grep for `T2bModel01` in `cli/review` rc=1. Hand-off cited :372 (stale). | CONFIRMED (lines moved) | Reflect uses the same `select_env`; `validate_reflect_profile` checks classes, Fable and tier0 but not alias existence. |
| D13 | `lint_cmd`, `estimate_cmd` registered but missing; error swallowed | `__init__.py:24-25` names them; `:30-35` swallows `ModuleNotFoundError` for the exact name; no `lint_cmd.py` / `estimate_cmd.py` in the package (file list, section 1) | CONFIRMED | Reflect appended `cluster_cmd, verify_cmd, manifest_cmd` to the same loader (:26-28): those files exist, but they share the risk that a deleted/renamed module silently disappears from the CLI. |
| D14 | no tasklist review step in sc-tasklist/sc-workflow; review loop only in spec-panel + prompts | `grep -rlE 'superclaude review|review_ledger|review panel resolve' src/superclaude/{skills,commands,core}` returns only `sc-reflect-protocol/SKILL.md`. So in `src`, **no** skill or command calls `review merge`, `review ledger` or `review panel resolve`; spec-panel.md does not contain the string `superclaude review` (UNVERIFIED how spec-panel.md:256-268 drives the loop) | CONFIRMED (stronger: the #346 merge/ledger CLI has no in-repo caller) | Reflect is the only in-repo caller of the package (`cluster`, `verify-citations`, and per its scripts `manifest`, `panel`). |
| D15 | telemetry strata only sonnet/haiku; merge and panel resolve write no telemetry | `telemetry.py:112-115` `STRATA = ("sonnet","haiku")`; `:267-268` rejects others; `merge_cmd.py:71-118` has no telemetry call | CONFIRMED | Reflect does not use `review telemetry` at all; it records `cluster_agreement`, `calibration_coverage` in its own run telemetry (SKILL.md:345; store UNVERIFIED). `manifest` records attempts (`record_attempt` :331). |
| D16 | round 4 accepted; `--cap` ignored on existing ledger; verify-only not a code mode | `ledger.py:114-118` only requires `n == len(rounds)+1` (no cap check); `_decision` :93-96 returns ESCALATE when `n >= cap` but merge still runs; `merge_cmd.py:102-104` uses `cap` only in `new_ledger` on round 1 | CONFIRMED | N/A (no rounds in v2). |

Summary for the reflect side: it **inherits** D1 (limits, for native v2 output), D6 (transitive union-find, partially mitigated by chain detection), D7 (shared regex), D11 (default soft mode), D12, D13 (same loader). It **avoids** D2, D3, D4, D16 only because the v2 stack has no ledger/verdict; adopting the v1 ledger as-is would import them.

## 6. tests/review inventory

`uv run pytest tests/review --collect-only -qq` -> **651 tests collected** (0.40 s). Per-file counts from the same collection; origin by first-add commit. Test names for ledger, exclusion and findings read via `grep '^def test_'`; other files' contents UNVERIFIED beyond file name and grep probes.

| File | Lines | Tests | Origin | Covers |
|---|---|---|---|---|
| `test_review_findings.py` | 317 | 23 | #346 | v1 parse (good, empty, unclosed, missing heading, bad JSON keeps good lines, MINOR+blocking, field validation, last-of-two blocks, prior lines), fixmap (block, table fallback, bad action), flat/locate, section_of, refs_norm, fingerprint stability, ambiguous anchor, same_defect 3-line rule, cluster determinism, map_span/hunks_touch, shared-fp-without-refs |
| `test_review_ledger.py` | 566 | 24 | #346 | round 1 rows, membership, revision, spans follow revision, cleared/refound/regressed, verdict+decision rounds 1-3, non-blocking never fails, priors never change status, no-valid-block refused, **one valid block is enough** (:376), merge order, defer, **missing anchor kept** (:408), capture, atomic save, merged report, ESCALATE prints FAIL, re-anchor, revision text mismatch, refound-nonblocking, late nonblocking cluster cannot mask |
| `test_review_cli.py` | 449 | 13 | #346 | click-level `review panel/merge/ledger/telemetry` (mentions `T3Model01`, `block_ok`, `strict-distinct`, `skipped_slots`) |
| `test_review_panel.py` | 409 | 41 | #346 (+reflect edits UNVERIFIED) | template/tier validation, resolve determinism, env selection (`T3Model01`) |
| `test_review_panel_live7.py` | 244 | 15 | #346 | @live7 shapes per environment |
| `test_review_rules_text.py` | 92 | 5 | #346 | pins insertions in the review prompt rules text, including "no source path" (`test_older_pins_still_hold_and_no_source_path`) |
| `test_review_telemetry.py` | 409 | 10 | #346 | record validation, append-only, no document text, task vars, loader idempotence, model_scores, stratum tag |
| `test_review_findings_v2.py` | 444 | 92 | reflect | v2 line/block rules incl. over-length (grep hit for 200/300 limits) |
| `test_review_card_convert.py` | 723 | 119 | reflect | 4 card shapes, citation resolution, category mapping (`unpassable-check`), fixtures `fixtures/reflect_cards/` (6 files: markdown-lines.md, markdown-table.md, synthetic-stoprule.yaml, yaml-blocking-minor.yaml, yaml-deviation-class.yaml, yaml-priority.yaml) |
| `test_review_cluster.py` | 795 | 113 | reflect | cluster_v2 rules, support, chained, clusters_kept |
| `test_reflect_cluster_pairs.py` | 522 | 32 | reflect | labelled pair cases for same_defect_v2 (chained) |
| `test_review_cluster_cmd.py` | 262 | 15 | reflect | `review cluster` CLI |
| `test_review_verify_citations.py` | 196 | 8 | reflect | each flag, coverage-linked finding, outside snapshot/root, re-read set, nothing dropped, byte-identical rerun, empty dir error, help lists command |
| `test_review_manifest.py` | 568 | 40 | reflect | manifest stages, attempts, resume, publish |
| `test_review_panel_exclusion.py` | 213 | 32 | reflect | hard_exclude / strict_distinct: golden byte-identity without exclusion, fixed-anchor exhaustion, no re-admission, stand-in after filtering, executor sonnet/haiku/opus cases, additive keys, class map, **soft distinct still repeats a model** (:208) |
| `test_review_panel_reflect_profile.py` | 230 | 17 | reflect | reflect profile rules |
| `test_review_reflect_templates.py` | 161 | 21 | reflect | the six reflect templates resolve to the documented shapes |
| `test_reflect_consumer_inventory.py` | 364 | 14 | reflect | (name suggests inventory of consumers of the reflect outputs; UNVERIFIED) |
| `test_reflect_stage0a_replay.py` | 440 | 17 | reflect | `scripts/reflect_stage0a_replay.py` |

Totals: #346 = 131 tests (7 files); reflect = 520 tests (12 files). Other fixtures: `clean.md`, `seeded.md`, `panel-golden-default-live7.json`, `panel-golden-packaged-tiers.json`, `review-tiers.frozen-1.0.0.json`.

Covered vs not covered (grep probes over `tests/review/*.py`):
- **Pinned as intended behaviour (a fix must change these tests):** D3 `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (ledger :376); D5 `test_missing_anchor_is_kept_without_a_span` (ledger :408); D11 `test_soft_distinct_without_exclusion_still_repeats_a_model` (exclusion :208); D8-adjacent `test_older_pins_still_hold_and_no_source_path` (rules_text).
- **Not covered (no grep hit):** `T2bModel01` (D12); `lint_cmd`/`estimate_cmd` (D13); tasklist-format ids like `T01.02` (D7); round 4 / cap on an existing ledger (D16); D2 (invalid reviewer's missing re-report clearing a `resolved_check` row): `resolved_check` appears only in ledger/cli tests whose names do not suggest the invalid-block case (UNVERIFIED by body read); `unpassable-check` accepted by **v1** `parse_block` (only card_convert tests mention it); a dropped-finding id/count being recorded (D1); a v1-to-v2 equivalence test (same report text with info string swapped) — not found by name; anchor-only finding through `cluster_v2` (singleton behaviour) — not found by name.
- **Shared-contract coupling not pinned:** no test asserts that v1 and v2 limits stay equal (they are separate literals).

## 7. Suggested Phase 2 deep-investigation assignments

1. **Finding-contract unification (findings.py + findings_v2.py + card_convert.py).** Decide one contract (v2 superset with v1 prior lines and empty-block rule reconciled). Read `findings.py:205-320` (fixmap, locate, section_of) and `card_convert.py:240-517` (shapes, summarize). Output: field-by-field mapping and the limit policy (truncate vs reject, counters) for D1.
2. **Ledger on v2 (ledger.py full read + merge_cmd/ledger_cmd).** Can `merge_round` take v2 findings with citations instead of anchors? What replaces `annotate(f, doc_text)` when a finding cites several files? Specify fixes for D2, D3, D4, D16 and list the tests in section 6 that pin the current behaviour.
3. **Clustering merge (findings.cluster vs cluster.cluster_v2).** Full read of `cluster.py:184-447` (support, chained, uncalibrated, clusters_kept). Design one clusterer accepting anchor spans and citations, keeping chain detection; evaluate the v2 "section always empty" over-merge and the shared D7 regex against real tasklist ids (`T01.02`, `AC-...`).
4. **Panel resolution policy (panel.py :160-500 not yet read + panel_cmd + tier file).** Make strict distinctness the default or flag duplicates (D11); environment detection beyond `T3Model01` (D12); tier list update from the tasklist study (hand-off 5.3); reconcile reflect's `classes`/Fable/3-reviewer profile with generic 1..8 panels; observed-model identity check (hand-off 6.5) — where it would live (no code today).
5. **CLI surface and callers.** `__init__` loader (D13), the absence of any in-repo caller of `review merge/ledger/panel resolve` (D14), how `spec-panel.md` and the installed `sc-review-ledger` skill drive the loop, and what `sc-workflow`/`sc-tasklist` would call. Includes `scripts/reflect_shadow_exit.py` and `scripts/reflect_stage0a_replay.py` as the reflect-side callers.
6. **Telemetry convergence (telemetry.py + manifest.py + reflect run telemetry).** Strata (D15), whether merge/resolve should append records, and how `cluster_agreement`/`calibration_coverage` and manifest attempts map into review-telemetry/1.
7. **Test migration plan.** Body-read the 131 #346 tests and the pinned tests listed in section 6; identify which become v2 contract tests and which golden fixtures (`panel-golden-*.json`, `review-tiers.frozen-1.0.0.json`) must be regenerated.

## 8. Gaps and questions

- [UNVERIFIED] `panel.py:137-400` (`_check_reflect_resolution` body, `validate_panel`, `validate_tiers`, `find_path` search order, `RESOLUTION_SCHEMA` value) not read in full.
- [UNVERIFIED] `cluster.py:184-487` beyond the docstring and the grep hits; `cluster_cmd.py` and `verify_cmd.py` bodies (whether per-line parse errors and invalid states are persisted in `clusters.json` / precheck output).
- [UNVERIFIED] `ledger.py:1-83, 163-183, 279-494` (row matching against existing rows, `apply_revision`, `render_merged_report`); `telemetry.py` beyond the cited lines; `manifest.py` bodies.
- [UNVERIFIED] how `spec-panel.md:256-268` drives the review loop without the string `superclaude review` (hand-off D14 claim); possibly via the installed `sc-review-ledger` skill's `review_ledger.py`, which is not in `src` (D14 says experiment copies only).
- [CODE-CONTRADICTED, minor] hand-off line numbers for D11 (`panel.py:402-408`), D12 (`panel.py:372`) and D7 (`telemetry.py:23`) are stale; current lines are `panel.py:536-543`, `panel.py:485-494`, `telemetry.py:22`. Behaviour unchanged.
- [CODE-CONTRADICTED] `ledger.merge_round` docstring (`ledger.py:112`) says an invalid reviewer "is skipped for clearing"; the clearing loop (:254-258) does not check `block_ok`. This is D2 and also a doc/code mismatch.
- [CODE-CONTRADICTED, minor] `findings_v2.py:3` says a v1-valid line with only V1 keys passes v2 unchanged; true per line, but a v1 block with prior lines or an empty v1 block is not valid v2.
- Question: should the unified contract keep **anchor** (exact-quote, single-document) as a first-class location, or require citations? `cluster_v2` ignores anchors entirely today.
- Question: should rejection become truncation for all reviewers (as `card_convert` already does for claims) or should the limits be removed? Both stacks share the literal limits but in separate places.
- Question: is the default panel distinctness for the unified panel soft (today's `distinct_across_slots`) or strict (reflect's `--strict-distinct`)? Tests currently pin soft re-admission.
- Question: `review-tiers.default.json` has no `tier0`, yet the reflect profile references it; is a `tier0` alias planned (ccsession config, UNVERIFIED)?

## Summary

The package holds two stacks on one CLI group: the #346 v1 stack (findings-v1, ledger, merge/ledger commands, telemetry; 131 tests) that produces verdicts, and the reflect v2 stack (findings-v2, card_convert, cluster_v2, cluster/verify-citations/manifest commands; 520 tests) that is telemetry/flagging only. `panel.py` is shared and carries reflect's opt-in `hard_exclude`/`strict_distinct` and the `reflect-*` profile. findings-v2 reuses v1's parser, regexes and `_check_flat` and repeats the 200/300 limits as literals, so D1 applies to native v2 output (and is harsher: one bad line makes the whole block non-complete and unclustered). All 16 hand-off defects that touch this package are confirmed at current code (D11, D12, D7 at moved lines); reflect shares D1, D6 (partly mitigated), D7, D11 (default mode), D12, D13, and avoids D2-D4/D16 only because it has no ledger. Three defects (D3, D5, D11) are pinned by current tests, so fixing them means changing tests on purpose.
