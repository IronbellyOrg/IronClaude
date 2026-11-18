# Proposal B: the central panel targets the gateway, with launch adapters and dated tier data, for C03

Side: B. Conflict: C03 (`model-tier-config`), status UNDECIDED-BY-EVIDENCE in `synthesis/synth-04-options-conflicts.md` (block C-03, lines 164-226). Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`.

Evidence tags used below: `[CODE]` = I read the file in this session; `[RES]` = taken from a research file and not re-read in code by me (the research file is named); `[E2@4a22d74]` = read with `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>` only; `[EXT]` = external source with URL; `[UNVERIFIED]` = decides nothing. Paths under `research/` are relative to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`. Model-behaviour evidence carries its date.

## Design

**One sentence.** Make the gateway a first-class environment in the shared tier file: every model it serves gets a real launch entry (`<adapter>:<argument>`), the tier lists carry their date and source, and every consumer other than reflect's Stage 3 gate resolves against the gateway by default. `anthropic-only` stays in the file and stays reflect's gate, so B contains Option A's cell and adds to it.

**What B decides that the provisional Option C does not.** C (synth-04 lines 200-212) makes environments data and says it "does not by itself say which environment the first central consumers use". B names it: the gateway. B does not decide O-2 for reflect's own gate; it decides it for the shared core and for new consumers (tasklist review, spec review, PR review, rf-qa).

### Core: `src/superclaude/cli/review/` (`panel.py`, `panel_cmd.py`, `data/review-tiers.default.json`)

1. **Launch grammar (schema stays `review-tiers/1`).** `environments.<env>.launch` stays a map of model id to string, so the validator at `panel.py:364-368` accepts it unchanged. A value is `<adapter>:<argument>`. Adapters: `agent-class` (in-session Agent tool, argument is a class), `cli-model` (headless `claude -p --model <raw id>`), `swarm` (in-process proxy transport). A value with no colon is the legacy form and means `agent-class:<value>`, so the current anthropic-only entries (`"claude-sonnet-5-5": "sonnet"`) are valid and mean what they meant. The three adapter names are the ones the decided C09 resolution already uses (synth-04 line 612).
2. **Real gateway entries.** `environments.gateway.launch` stops being `{}`. Every model reachable through an alias list gets `cli-model:<raw id>` (12 ids: opus, sonnet, haiku, sol, terra, luna, wonder-full, wonder, spark, glm, grok, qwen). `swarm:` is allowed by the grammar but not used by packaged data; it is there for the code-driven Tier 2 engine (C17) when that engine is replaced.
3. **Dated tier data.** Add one top-level `provenance` object: `tiers_as_of` (date), `gateway_observed_on` (date), `ccsession_models_version` (string), `evidence` (list of short dated notes, for example "E2 study 2026-11-12/13, one gateway"). `validate_tiers` (`panel.py:258-374`) has no check on unknown top-level keys, so this is additive. The resolution record gets one optional field, `tiers_as_of`, emitted only when `provenance` exists, so the frozen golden fixture stays byte-identical.
4. **Missing data added or declared out of scope.** `muse-ember-1.0` (E2's default panel member) and `tier0` (Fable, Astra) are in no tier list. B adds `tier0` so the reflect "no tier0" rule is no longer inert, and adds ember only in the same pull request that changes `ccsession-models.json` and the Coder env slots (see Risks). If the owner does not confirm ember, the proposal declares E2's ember panels out of scope in `provenance.evidence` instead of silently omitting them.
5. **D12 alias check outside the pure resolver.** `pnl.resolve` stays pure and deterministic. A new `check_required_env(panel, tiers, env, environ)` (called by the CLI, not by `resolve`) maps each tier a template uses to its Coder slot by the documented naming rule (`tier2b` to `T2bModel01`) and fails when the slot is unset in the gateway environment.
6. **Reflect profile reads the parsed launch.** `_check_reflect_resolution` (`panel.py:153-156`) tests the parsed adapter and argument instead of the raw string. For anthropic-only the outcome is identical. For gateway the error changes from `launch None is not one of sonnet, opus, haiku` to a message naming the adapter (`cli-model` is not allowed in a reflect resolution), which becomes the recorded `panel_fallback_reason` under rule D4.

### Consumers

| Module | What it does under B |
|---|---|
| Reflect Tier 2 panel (shadow, skill `sc-reflect-protocol`) | Keeps `--env anthropic-only` in §4.3a step 1 (the Stage 3 gate is unchanged). Adds a `panel verify` call (below) whose route warning is written into `panel_fallback_reason` per rule D4. Edits stay inside §4.3a and §9.2, the sections the C6 pin allows. |
| Document review loop (#346, `rules/prompts/document_review_loop_prompts.md:70`) | Prompt text unchanged. With `--env gateway`, `panel resolve` now returns a non-null `launch` for every reviewer, so the dispatcher (C09 Option C) can act on it. |
| Tasklist review (E2 pattern) | The bash ladder and raw ids in E2's `run-reviewer.sh` become `cli-model` entries plus the alias order already in the tier file. E2's exclusion default (`EXCLUDE_MODELS="glm-5.3 Qwen3.8-max"`) is recorded as a dated note, not encoded as a rule. |
| Code-driven Tier 2 engine (`cli/reflect/ensemble.py`) | Untouched. Its gateway-proxy launch becomes expressible as `swarm:` data when C17 replaces it. |
| Future consumers (PR review, rf-qa, spec panel) | Default environment is the gateway; each picks its adapter set; none needs a code branch for a model change. |

## How it works

### Data flow

1. **Tier change (owner, Coder).** One pull request updates the Coder env slots, `ccsession-models.json`, `MODEL-TIERS.md` and, new under B, `review-tiers.default.json` including `provenance`. A test pins that `provenance.ccsession_models_version` equals the `version` in `ccsession-models.json` and that list lengths match (the length check exists today).
2. **Preflight.** `superclaude review panel verify --env gateway --template @live7` reads the environment and the tier file, makes no model call, and prints JSON checks (below). Advisory by default; exit 1 when a check is `fail`.
3. **Resolve.** `superclaude review panel resolve --template @live7 --env gateway --run-id R` prints the existing `review-panel-resolution/1` record. Each reviewer's `launch` is now `cli-model:<raw id>` instead of `null`; the record carries `tiers_sha256` (existing) and `tiers_as_of` (new, optional).
4. **Dispatch (C09 Option C, not delivered by B).** The dispatcher splits `launch` at the first colon, runs the adapter with the pinned model, and writes the three identity fields per reviewer (`resolved`, `launch`, `observed`) into the telemetry `model` group that already exists (`telemetry.py:49`), as decided in C08.
5. **Reflect.** Step 1 stays `--env anthropic-only`. The `verify` result for the `agent-class` entries is stored with the run; a route warning becomes `panel_fallback_reason`.

### Contract fields

| Where | Field | Change |
|---|---|---|
| Tier file `review-tiers/1` | `environments.<env>.launch` values | grammar `<adapter>:<argument>`; bare string = `agent-class:<string>` |
| Tier file | `provenance` (`tiers_as_of`, `gateway_observed_on`, `ccsession_models_version`, `evidence[]`) | new, optional, validated when present |
| Tier file | `aliases.tier0`, `classes["gpt-6-astra"]`, `names` | new data; `muse-ember-1.0` only with owner confirmation |
| Resolution `review-panel-resolution/1` | `reviewers[].launch` | string in every environment that declares a complete launch table |
| Resolution | `tiers_as_of` | new, only when `provenance` exists |
| Telemetry `review-telemetry/1` | `model.launch` | receives the same string (field exists) |

No new environment key and no new template key are needed, so the closed key sets at `panel.py:37-46` and `:371-373` stay as they are.

### CLI surface

- `panel resolve`: no new flags. `--env` keeps its precedence (`--env`, `$SUPERCLAUDE_REVIEW_ENV`, `$T3Model01` set means gateway, else anthropic-only; `panel.py:485-494`). The D12 check runs in the command layer before `resolve`.
- `panel validate --kind tiers`: now also checks the adapter grammar and `provenance`.
- `panel verify` (new, read-only). Checks:
  - V1 launch completeness: every model reachable in the environment has a `launch` entry that parses; an unknown adapter is `fail`.
  - V2 alias existence: for each tier the template uses, the Coder slot (`T<N>[letter]Model01`) is set in the environment; unset is `fail` in the gateway environment.
  - V3 route check for `agent-class` entries: class, then `ANTHROPIC_DEFAULT_<CLASS>_MODEL`, then the tier whose `alias` equals that value, then that tier's first model, then its `classes` entry. If the class does not equal the launch class, `warn` with the expected served model. This is an expectation derived from data, not an observation.
  - V4 provenance: prints `tiers_as_of` and its age; `warn` when missing.

The environment read in V2 and V3 follows the repo's existing pattern (`cli/sprint/aienv.py:39-83` reads the three `ANTHROPIC_DEFAULT_*` slots and the numbered proxy slots from `os.environ`, with an injectable mapping for tests).

## Evidence

Each row: claim, research file, code location, tag. Dates are the dates of the observation, not of this proposal.

### A. The gateway is declared but empty, and the label on the other cell is not true here

| # | Claim | Research file | Code location | Tag |
|---|---|---|---|---|
| 1 | The gateway environment is `available: "all"`, `stand_ins: {}`, `launch: {}`, with the note "dispatch mechanism per model not defined yet". | `research/04-panel-resolution-identity.md` §4 | `src/superclaude/cli/review/data/review-tiers.default.json:25-30` | CODE |
| 2 | Each reviewer's `launch` is `launch.get(model)`, so every gateway reviewer carries `launch: null`; a test pins this as intended. | 04 §2, §4.1 | `panel.py:595`, `:679`; `tests/review/test_review_panel.py:303-308` (`test_gateway_resolution_prints_launch_null`) | CODE |
| 3 | No reflect template resolves in the gateway: `_check_reflect_resolution` rejects any launch outside sonnet, opus, haiku. Run 2026-11-13: `Error: invalid reflect resolution: t1b-1: launch None is not one of sonnet, opus, haiku`. | 04 §4.1 | `panel.py:137-157` (check at `:153-156`), raised at `:682-687` | CODE (check), RES (the run) |
| 4 | The anthropic-only label is not true at serving time on this machine. 2026-11-13 environment: `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, and tier2's first model is `gpt-6.1-sol`. Combo runs A1-A2 and B1-B3 served the "haiku" slot with `gpt-6.1-sol`; the panel record, card headers and `panel_parity` never showed it. | 04 §4.1, §7.2 (cites `.dev/eval-workspaces/shadow-model-combos/results.md:33-38`, `FINDINGS.md:15`) | tier2 list at `review-tiers.default.json:7` | CODE (tier list), RES (served model; routing is runtime behaviour) |
| 5 | In anthropic-only every tier has at most one available model, so every `fallbacks` list is empty. | 04 §4.1 | `review-tiers.default.json:33-34` (one stand-in per tier) | CODE |
| 6 | Option A therefore keeps reflect on a cell whose record cannot say what served, and keeps every other consumer without any dispatch instruction. | synth-04 C-03 Option A cons (line 184) | n/a | derived from rows 2-5 |

### B. The design already intends launch to be data, and three dispatch paths exist

| # | Claim | Research file | Code location | Tag |
|---|---|---|---|---|
| 7 | The module's stated design is that a model change is a data edit only. A test already adds a model family and a custom launcher string (`"acme-launcher"`) as data. | 04 §1 | `panel.py:1-9`; `tests/review/test_review_panel.py:243-259` (`test_adding_a_model_family_is_a_data_edit_only`) | CODE |
| 8 | The tier-file validator checks only that `launch` is a map of strings, so the adapter grammar is additive. | 04 §1 | `panel.py:364-368` | CODE |
| 9 | Three dispatch paths exist today: in-session Agent calls by class (reflect), one `claude -p --model <raw id>` per reviewer (E2), and in-process swarm calls over `T2Model0N` proxy models (master Tier 2 engine). | 04 §5, §6; `research/13-gap-fill-reflect-ensemble.md` §1.4, §1.5 | `ensemble.py:154-182`; E2 `run-reviewer.sh:48` | CODE (engine), E2@4a22d74 (runner), RES (reflect) |
| 10 | C09 is DECIDED: "The resolution `launch` names an adapter and an argument (`agent-class`, `cli-model`, `swarm`)", and its own cons line says "adapter default per consumer still depends on C03". | synth-04 C-09 Option C (lines 610-633) | n/a | RES |
| 11 | C08 is DECIDED: record requested, launch and served separately. The telemetry schema already has the `model` group `("resolved", "launch", "observed")`, which is only meaningful if `launch` is not null. | synth-04 C-08 (lines 546-570); 04 §6 | `src/superclaude/cli/review/telemetry.py:49` | CODE |
| 12 | The master Tier 2 engine launches gateway or proxy models directly. The reflect-side constraint "only `anthropic-only` launches; `gateway` launch `{}`" conflicts with it: applying it would remove the engine's reviewer pool. | 13 §9.2 (reflect constraints table, row C12, constraints from research 07 :395-412) | `ensemble.py:154-182` | CODE, RES |
| 13 | `claude --model` takes a model id, not a slot name (the repo's own comment). That is the argument the `cli-model` adapter needs. | none (code comment) | `src/superclaude/cli/sprint/aienv.py:101-105` | CODE |
| 14 | A raw-id `claude -p` route kept identity in the study's valid era: audit A reports 2 mismatches ("wonder" runs served terra) and "no other mismatches". The runner checks the observed top-level assistant model against the requested id. | 04 §5, §8 | E2 `COMBO-REPORT.md:295`; `tools/run-reviewer.sh:51-56` | E2@4a22d74. One gateway, 2026-11-11 to 2026-11-13. |

### C. Tier data decays, and the repo's own update checklist leaves this file out

| # | Claim | Research file | Code location | Tag |
|---|---|---|---|---|
| 15 | The tier file's only date is a note "owner decision 2026-11-10" and `version: 1.0.0`. `MODEL-TIERS.md` says tiers were last changed 2026-11-11, with a further owner change on 2026-11-12 (Haiku 5.5 confirmed in Tier 4; `issue-worker-t3` pinned to Tier 2b). `ccsession-models.json` has `"version": "2026-11-11.1"`. | 04 §4, §10 item 8 | `review-tiers.default.json:3`, `:32`; `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:5-10`; `ccsession-models.json` (`version`) | CODE |
| 16 | The update checklist says "when a tier changes, update all three together" (Coder env, `ccsession-models.json`, `MODEL-TIERS.md`). `review-tiers.default.json` is not one of the three. The only coupling test compares list lengths for tier2b, tier3, tier4 plus two first models. | 12 §5 (last bullet), Gaps (live7 coupling) | `MODEL-TIERS.md:11-14`, `:189-193`; `tests/review/test_review_panel_live7.py:92-106` | CODE |
| 17 | `muse-ember-1.0`, E2's default panel member, is in no alias, name or class of the tier file and in no file under `src/`. E2's runner comment says the gateway picker lists it as "Tier 04 Model 02", "being added" on 2026-11-12. | 04 §4, §8 | grep for `muse-ember` over `src/` returns no file; E2 `run-reviewer.sh:19-34` | CODE (absence), E2@4a22d74 |
| 18 | The packaged tier3 is exactly the two models E2's runner excludes by default. E2 comments that guard as added after a cyclic-ladder incident; the reason for excluding those two models is not stated in the lines I read. | 04 §8 | `review-tiers.default.json:9`; E2 `run-reviewer.sh:69` | CODE, E2@4a22d74 |
| 19 | Tier 0 exists in the repo's model documentation (Fable, GPT-6 Astra) and in `ccsession-models.json` (`T0Model01`, `T0Model02`), but the review tier file has no `tier0`, so reflect's "no tier0" rule (`panel.py:95-117`) is inert with packaged data. | 04 §4.3, Gap 4 | `MODEL-TIERS.md:40`; `ccsession-models.json` (`tiers.tier0`); `panel.py:95-117`, `:104-105` | CODE |
| 20 | `select_env` reads only `T3Model01`. `T2bModel01` is set in this environment (2026-11-13) but unread; `live7` needs `claude-gw-tier2b`; the only env-selection test pins the `T3Model01` key; D12 is listed as uncovered. | 04 §4.2; 12 §D12 row | `panel.py:485-494`; `review-panel.live7.json:5`; `tests/review/test_review_cli.py:83-88` | CODE |
| 21 | Slot names follow a documented rule: "Tier names match the Coder env slots (`T0Model01` is Tier 0, `T1aModel01` is Tier 1a)". | none | `MODEL-TIERS.md:28` | CODE |

### D. What the gateway side offers that anthropic-only cannot express

| # | Claim | Research file | Code location | Tag |
|---|---|---|---|---|
| 22 | Every panel E2 recommends mixes vendors; the final default is "ember + 2x luna", with "haiku + 2x luna" the best measured real-blocking panel (1.2/8). Luna is not in anthropic-only's `available` list. | 04 §8 | E2 `COMBO-REPORT.md:363-369`; `review-tiers.default.json:33` | E2@4a22d74. One gateway, valid era from 2026-11-12 13:02. |
| 23 | E2's own caveat: "All panels sit at about 2-2.5 of 14", model choice "cannot lift the ceiling past ~2.5/14"; the biggest levers are the anchor limit and naming `source.md`. | 04 §8 | E2 `COMBO-REPORT.md:371` (and the batch 11 section from line 421) | E2@4a22d74 |
| 24 | The #346 loop prompt calls `panel resolve`, so a null gateway `launch` already reaches a master consumer. | 04 §9 | `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` | RES (prompt text) |
| 25 | The default template resolved in gateway on 2026-11-13 gives sonnet, muse-spark-1.3, glm-5.3, Qwen3.8-max, all with `launch: null`. | 04 §4 (template table) | `review-panel.default.json:9-11` | RES (run) |

### E. External context

| # | Claim | URL | Tag |
|---|---|---|---|
| 26 | Frontier LLM evaluators show self-preference and self-recognition (tested on 2023-era models: GPT-4, GPT-3.5, Claude 2, Llama-2), which is the reason to want panel members from more than one family. | https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf (via `research/web-03-judge-calibration.md` §1.1) | EXT, peer reviewed, date caveat |
| 27 | A reanalysis finds about 89.6% of measured self-preference is explained by evaluator error on hard items, so family diversity alone is not sufficient. This limits how much B can claim from vendor mix. | https://arxiv.org/abs/2601.22548 (via web-03 §1.2) | EXT, preprint, summary-level figures |

Limits of this evidence: rows 14, 22 and 23 come from one gateway between 2026-11-11 and 2026-11-13 (synth-04 status line). I did not re-aggregate E2's raw score files. Row 4's served model is observed runtime behaviour, not code.

## Correctness argument

The argument is that B keeps every property the resolver has today, removes the one property that is false today (a launch label that does not match what serves), and does not depend on the open owner decision to be safe.

**P1. The resolver stays pure and deterministic.** `resolve` (`panel.py:565-707`) reads no environment. The new environment reads (D12 slot check, V3 route check) live in the command layer and in `verify`, where `select_env` already reads the environment (`panel.py:485-494`). Same inputs still give byte-identical output; the existing test `test_resolution_is_byte_identical_for_equal_inputs` (`test_review_panel.py:294-300`) covers it and does not change.

**P2. Backward compatibility is checkable.** A bare launch string parses as `agent-class:<string>`, and the anthropic-only table is unchanged. Therefore, for the packaged `default` and `live7` templates in anthropic-only, the new resolution differs from the old one only in `tiers_sha256` and the new `tiers_as_of`. A test can assert exactly that (resolve with the old and new tier file, delete those two keys, compare). The frozen-tier golden (`panel-golden-default-live7.json`) uses a tier file without `provenance`, so it stays byte-identical; only the packaged-tier golden regenerates, which its own docstring says is expected on any tier-file byte change (`test_review_panel_reflect_profile.py:3-6`, per research 12 §5).

**P3. Reflect's gate behaves as it does now.** `_check_reflect_resolution` accepts exactly the launches it accepts today in anthropic-only (parsed `agent-class` with sonnet, opus or haiku) and still rejects `fable` (`test_review_panel_reflect_profile.py:183-189`). In the gateway it still rejects, with a reason that names the adapter instead of `None`. Rule D4 (`SKILL.md:320`, "Unsupported cells (gateway, a null `launch`, an unmapped model) run the legacy rotation and record `panel_fallback_reason`") keeps working and gains a precise reason string.

**P4. Fail closed.** Under B an unknown adapter, a reachable model without a launch entry, a template tier whose Coder slot is unset in the gateway, and a malformed `provenance` are errors from `validate_tiers`, `verify` or the command layer. Today the same situations produce `launch: null`, or (D12) no signal at all (evidence rows 2, 20).

**P5. The label problem becomes visible.** For the 2026-11-13 failure (evidence row 4), V3 would compute: class `haiku`, `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]`, tier2 alias, first model `gpt-6.1-sol`, class `gpt`, which is not `haiku`, so `warn`. The inputs are exactly the values observed and recorded in research 04 §4.1. This is an expectation, not an observation; the observation is the job of the C08 identity fields, which B does not replace.

**P6. B is consistent with every decided conflict it touches.**
- C08 (three identity fields) needs `launch` to carry a value (telemetry `model.launch`, `telemetry.py:49`).
- C09 Option C names the three adapters and says the adapter default per consumer "follows the C03 decision" (synth-04 line 633). B supplies the schema half of that decision.
- C17 (fix the code-driven engine in place, replace it later at UC-2 Stage 5) leaves a consumer that launches gateway models directly (evidence row 12). Option A would leave that consumer outside the central data model; B gives it a `swarm:` slot to move into.

**P7. What B does not claim.** It does not claim the gateway is the right serving environment for reflect's gate; the evidence for the gateway's value (rows 14, 22, 23) is one gateway, 2026-11-11 to 2026-11-13, with a documented ceiling of about 2-2.5 of 14 for every panel. It also does not claim that the alias-serves-its-first-model rule holds generally: one instance is observed (row 4), and E2's manifest statement that aliases serve only the first model of a tier is [UNVERIFIED] in the research (research 04 §4.2). V3 therefore reports an expected served model and labels it as derived.

## Risks and mitigations

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | **Weakest point: the gateway launch entries describe a route that nothing executes yet.** The dispatcher that reads `cli-model:` is C09 Option C (effort L) and is not part of B. Until it exists, B repeats the defect research 04 §10 calls the highest-risk gap: a record that describes something that did not run. The evidence that favours the gateway is also narrow (one gateway, 2026-11-11 to 2026-11-13). | High likelihood for the gap window; Medium impact | Stage B so the first deliverable has standalone value (validation, `verify`, `provenance`, D12). Reflect stays on anthropic-only, so no live gate depends on an unimplemented adapter. `verify` gains a line listing which adapters have an implementation, and marks the rest `declared only`. Do not ship the gateway entries before the owner accepts that gap. |
| R2 | Alias routing is runtime behaviour and changes with Coder and ccsession configuration (G-33). Dated data can still be wrong the day after it is written. | High likelihood; Medium impact | `provenance` states the date and source and V4 prints its age. V3 reads the live environment each time. The observed served model (C08) remains the authority. No threshold for "too old" is set here; that is an owner policy choice. |
| R3 | In-session Agent calls cannot pass a raw gateway id (C09 Option A cons, synth-04 line 594). So a gateway panel with non-Claude members cannot run inside reflect's in-session dispatch. | Certain for that combination | The reflect profile rejects `cli-model` with a clear reason and D4 runs the legacy rotation. Non-Claude gateway panels are for consumers whose dispatcher can spawn `claude -p` (E2 pattern). |
| R4 | Adding `muse-ember-1.0` to tier4 changes list length from 3 to 4, which breaks the length coupling test against `ccsession-models.json` (`T4Model01`-`T4Model03` today) and, per `MODEL-TIERS.md:193`, ccsession stops when a listed slot is unset in the workspace env. `ccsession-models.json` is fetched live from master at launch (`research/12-test-pins-regression.md`, Gaps and Questions, last bullet), so a half-applied change can break launches. | Medium; High impact if mishandled | Ember is added only in one pull request that also changes `ccsession-models.json`, `MODEL-TIERS.md` and the Coder slot (Coder first), gated by the owner. Otherwise declare E2's ember panels out of scope in `provenance.evidence`. B does not depend on ember. |
| R5 | `review-tiers/1` stays the schema id although files gain `provenance`. A newer tier file in an older installed package is still accepted (`validate_tiers` ignores unknown top-level keys), but an older package would not enforce the grammar. A project or user tier file found by `find_path` (`panel.py:397-419`) could carry a stale grammar. | Low; Low | Additive change; old files remain valid under new code. If the owner wants a hard boundary, bump to `review-tiers/2` in the same change at the cost of touching `TIERS_SCHEMA` and fixtures. |
| R6 | Two goldens and one fixture family are coupled to the tier file bytes; any later tier edit regenerates them. | Certain; Low | Already true today. B adds the provenance-to-ccsession version test so the regeneration happens in the same PR as the data change, not later. |
| R7 | Slot-name derivation (`tier2b` to `T2bModel01`) rests on a documented naming rule (`MODEL-TIERS.md:28`), not on code. If Coder renames slots the check gives false failures. | Low; Low | The check is in `verify` and the command layer, not in `resolve`; a false failure blocks nothing but a preflight. Add one test that the derived names for tier2b, tier3 and tier4 equal the `models_env[0]` entries of `ccsession-models.json`. |
| R8 | Scope creep: B touches data, validator, CLI, goldens, docs and two skills' text. Synth-04 rates Option B effort L, risk High. | Medium; Medium | Four stages with independent value (Cost). The decision to ship the gateway entries is separate from the grammar and `verify`. |
| R9 | The external self-preference evidence is 2023-era and partly qualified by a 2026 reanalysis (evidence rows 26-27). Vendor mix is not shown to improve review quality; E2 itself found no panel significantly better and a low ceiling. | Medium; Low | B does not change any template or default panel composition and claims no quality gain. It makes cross-vendor panels expressible and their identity recordable; quality claims stay with the benchmark (C20). |

## Test coverage needed

### Existing tests that change

| Test | Why it changes | Change |
|---|---|---|
| `tests/review/test_review_panel.py:303-308` `test_gateway_resolution_prints_launch_null` | Pins the defect (`launch is None` for every gateway reviewer). | Rewrite: every gateway reviewer's `launch` parses as `cli-model:<id>` with `<id>` equal to `model`; keep the model and `stand_in` assertions. |
| `tests/review/test_review_panel_reflect_profile.py:74-90` `test_packaged_tiers_hash_and_resolutions_are_pinned`, fixture `tests/review/fixtures/panel-golden-packaged-tiers.json` | Any byte change to `review-tiers.default.json` changes `tiers_sha256`. | Regenerate the golden; no logic change. |
| `tests/review/test_review_panel_live7.py:92-106` `test_review_tier_lists_match_the_ccsession_slot_counts` | The coupling to `ccsession-models.json` is the only drift guard. | Extend: provenance version equals `ccsession-models.json` `version`; derived slot names for tier2b, tier3, tier4 equal `models_env[0]`. If ember is added, the tier4 length assertion moves in the same PR as `ccsession-models.json`. |
| `tests/review/test_review_panel_live7.py:109-125` (gateway live7) | Draws can move only if a tier list changes (ember). | Unchanged unless ember is added; then re-check `t4` distinctness only (the assertions at `:119-124` do not pin a specific t4 pair). |
| `tests/cli/reflect/test_shadow_skill_contract.py` (C8 needle tests, `:221-238`, `:283-299`) and the C6 section pin (`:52-75`) | §4.3a text gains the `verify` step and a new D4 reason. | Keep every pinned needle; edits stay in §4.3a and §9.2; add one needle for the `panel verify` call. |

### Existing tests that must stay green unchanged

`test_review_panel_reflect_profile.py:56-66` (every id in `names`, alias lists, `available` and stand-ins has a `classes` entry; it will exercise the new `tier0` ids, so `gpt-6-astra` and `names` entries must be added with `tier0`), `test_review_panel_exclusion.py:56-72` (frozen-tier golden, 16 cases; relies on `tiers_as_of` being absent without `provenance`), `test_review_panel.py:243-259` (custom launcher string as data), `:265-281` (anthropic-only resolution), `:294-300` (byte-identical output), `:332-341` (`select_env`), `test_review_panel_reflect_profile.py:183-189` (a bad launch value is rejected), `test_review_cli.py:83-88` (gateway selected by `T3Model01`), `test_review_reflect_templates.py:92,99,115-117` (reflect template model lists; research 12 §5).

### New tests

| Test | Asserts |
|---|---|
| `parse_launch` units | bare string is `agent-class`; `cli-model:x`, `swarm:x`, `agent-class:x` parse; empty argument, unknown adapter and a second-level colon in the adapter name are errors. |
| `validate_tiers` | accepts a launch table with the grammar; rejects an unknown adapter; accepts and rejects `provenance` shapes (missing date, non-string version). |
| Packaged-data completeness | for the packaged gateway environment, every model in every alias list has a `launch` entry that parses (the check that would have caught `launch: {}`). |
| Reflect profile in gateway | resolving `@reflect-pre --env gateway` fails with an error naming the adapter, not `None`. |
| Backward compatibility | for `default` and `live7` in anthropic-only, old and new tier files resolve identically after removing `tiers_sha256` and `tiers_as_of`. |
| `tiers_as_of` | present only when `provenance` exists. |
| `verify` V1-V4 | with an injected environment mapping (same seam as `aienv._load_aliases`): unset `T2bModel01` fails for `@live7` in gateway and passes for `@default`; `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]` yields the `warn` with expected served model `gpt-6.1-sol`; `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b[1m]` yields no warning for the sonnet class; missing `provenance` warns; no network or subprocess call is made. |
| D12 | the case research 12 lists as uncovered: `T2bModel01` unset with `tier2b` in the template gives an error; both set passes. |
| tier0 | with `tier0` in the file, a reflect template using it is rejected (`panel.py:104-105`) and a tier listing a tier0 model is rejected (`:116-117`); this rule has no positive test with packaged data today. |
| Skill text | reflect `SKILL.md` §4.3a names `panel verify`; the loop prompt still names `panel resolve` (`document_review_loop_prompts.md:70`). |

Not in this proposal's test scope: the dispatcher and its adapters (C09), identity observation (C08), and any quality measurement of gateway panels (C20).

## Cost

Effort rating: L overall (synth-04 rates Option B L, risk High). It splits into four stages, each shippable alone. Only the first two are needed to remove the defects in evidence rows 2, 3, 15, 16 and 20.

| Stage | Content | Size | Gate |
|---|---|---|---|
| B-1 | Launch grammar and `parse_launch`; reflect check reads the parse; `provenance` and `tiers_as_of`; gateway launch entries; `tier0`; golden regeneration; version-coupling test. Five existing test groups touched (table above), about ten new tests. | M | Owner accepts risk R1 (entries ahead of the dispatcher). |
| B-2 | `panel verify` (V1-V4), D12 check in the command layer, reflect §4.3a step and D4 reason; `MODEL-TIERS.md` checklist gains the fourth file. | S to M | B-1. |
| B-3 | `muse-ember-1.0` into tier4 together with `ccsession-models.json`, `MODEL-TIERS.md` and the Coder slot; or the out-of-scope note. | S in this repo; the Coder change is outside it | Owner decision and Coder first. |
| B-4 | Consumer wiring for new consumers (loop, tasklist review, PR review, rf-qa) to read `launch` through the dispatcher. | Counted under C09 Option C (L), not here | C09 dispatcher. |

Ongoing cost: each tier change now touches four artifacts instead of three, with a test that fails when they drift. Run-time cost: none in `resolve`; `verify` reads environment variables and one JSON file. Evidence cost avoided: no new model runs are needed to decide B; the open items are O-2 (target environment) and the ember status, both owner inputs.

Rollback: the gateway `launch` entries and `provenance` are data; removing them returns the file to today's behaviour (`launch: null`), and the grammar is a superset of the old values, so no stored anthropic-only resolution becomes invalid.
