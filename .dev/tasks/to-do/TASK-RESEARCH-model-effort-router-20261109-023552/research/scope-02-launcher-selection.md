# Research Notes: Model and effort router, launcher selection slice

**Date:** 2026-11-09
**Scenario:** A
**Depth Tier:** Deep
**Status:** Complete (assigned discovery slice only; independent parent review pending)
**Scope:** Independent Stage A discovery slice 2, launcher lines 951-1975 and direct selection/invocation callers. No implementation or web research.

---

## EXISTING_FILES
### Primary launcher and direct dependencies

Sizes are observed `wc -l` counts, not inferred from a repository map.

| File | Lines | Purpose and scoped entry points |
|---|---:|---|
| `src/superclaude/skills/ccsession-tag/ccsession` | 1975 | Bash launcher. Entire assigned range 951-1975 read. Relevant functions: `setup_shim()`, `apply_profile()`, `apply_tier_selection()`, `export_selection(what)`; top-level selection followed by untagged/new named/resumed named invocation. The same range also holds session-location/listing/name-prompt helpers, which were read but do not select effort. |
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | 249 | Immediate Orca caller. Focused scanner and final handoff reads only, not a second broad launcher-initialization investigation. Passes Claude arguments through the launcher. |
| `src/superclaude/skills/ccsession-tag/models.py` | 1111 | Launcher's helper-command boundary: `in-my-tiers`, `model-resolve`, `default-tier`, `tier-resolve`, `compact-settings`, refresh, shim-port/digest commands. Text discovery located this boundary; deep role/registry policy reading is delegated to the adjacent owner, not duplicated here. |
| `src/superclaude/skills/ccsession-tag/README.md` | 772 | User-facing selection/default/permission documentation. Only focused relevant claims cross-checked below. |
| `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` | Not measured | Tier/role policy documentation; focused lines 18-41 read. Deployed policy is not established by this document. |

### Related tests and fixtures [CODE-VERIFIED as existing test code, NOT test passes]

| File and location | What the read assertions establish | Follow-on use |
|---|---|---|
| `tests/unit/test_ccsession_tiers.py` (3399 lines), `:308-393` | `_launch(tmp_path, *args, defaults=..., **extra)` executes the actual launcher with a fake Claude binary and a fake running shim. The recorder captures argument vector, settings, context/compaction, custom model, base URL, and auth variables under a temporary home. | Reuse this fixture for launch-boundary assertions instead of creating a second harness. Its synthetic gateway and model IDs are not live service evidence. |
| Same file, `:3302-3315` | An allowed workspace default, including its `[1m]` spelling, is handed to Claude with its own model window. | Preserve configured user-default behavior. |
| Same file, `:3318-3328` | Explicit tier and explicit model beat the workspace default. | Test any router's precedence against deliberate user choices. |
| Same file, `:3331-3368` | Empty/unknown/bad/unavailable workspace-default models retain the tier fallback; username-limited access changes acceptance. | Preserve authorization before choosing defaults; do not treat silent fallback as a universal tier mandate. |
| Same file, `:3371-3399` | Non-tier launch does not add the workspace-default model; `in-my-tiers` is silent and communicates via exit code. | Preserve non-tier behavior and the shell/helper contract. |
| `tests/unit/test_ccsession_tag.py` (4823 lines), `:1510-1524` | Permission-default launches drop the bypass while retaining model/resume presence. | Keep the permission choice independent from model/effort selection. |
| Same file, `:1745-1769` | Passthrough after `--claude-args` and Claude's own `--` survive without being reinterpreted as labels/options. | Include dash-led prompt text, unknown CLI flags, and explicit effort values in later compatibility checks. |

Additional test names were located, not deeply reviewed or run: profile model/window launch, profile cache warm-up/failure, Orca relaunch on default tier, native picker settings, tier role rules, and compaction overrides. The contracts/tests slice owns exhaustive coverage and execution.

## PATTERNS_AND_CONVENTIONS
### Selection and export flow [CODE-VERIFIED]

All short `ccsession` citations below refer to `src/superclaude/skills/ccsession-tag/ccsession`.

- The top-level launch refreshes model data unless disabled or using an external profile, then calls `apply_tier_selection()` in tier mode or `apply_profile()` for a selected profile. Only afterwards does it choose a shim port and call `setup_shim()` (`ccsession:1834-1851`). Refresh failure is tolerated, whereas a failing selection exits.
- `apply_tier_selection()` clears inherited context/compaction/custom-picker overrides. With neither explicit model nor explicit tier, `ANTHROPIC_MODEL` becomes the named selection only if `models.py in-my-tiers` succeeds; an absent or disallowed workspace model leaves the default-tier path (`ccsession:1191-1207`). This is an allowed-workspace-default preference, not a fixed Tier1b default.
- An explicit or accepted default model goes through `models.py model-resolve`, labels the session profile `model:<name>`, and enables a custom picker option. The alternative goes through `default-tier` when necessary and then `tier-resolve`; both resolver failures exit 2 (`ccsession:1208-1232`). The launcher does not itself parse Coder roles here: authorization and role/default policy sit behind the helper commands.
- `apply_profile()` resolves validated built-in data unless an external profile was selected, reads model/context/compaction/shim requirements, refuses a shim-required profile without a shim, then uses the same exporter (`ccsession:1157-1188`). Preserve this non-tier launch surface in later compatibility research; do not replace every launch with a tier selection.
- `export_selection(what)` applies optional `CCSESSION_COMPACT_WINDOW`, exports maximum context, obtains per-model settings with `compact-settings` in tier mode unless compaction was pinned, falls back to the compaction environment variable, and honors `CCSESSION_COMPACT_PCT`. It exports `CCSESSION_PROFILE` and optionally custom picker fields (`ccsession:1235-1271`). A future effort setting must not overwrite these settings or conflate reasoning effort with token-window/compaction tuning.
- Launch authentication adaptation is conditional: a shim launch with an API key and no bearer token converts that key to the bearer-token variable and unsets the API-key variable (`ccsession:1852-1859`). This is a compatibility boundary to retain, not authorization to inspect or disclose credentials.

### Invocation and direct caller boundaries [CODE-VERIFIED]

- The immediate Orca wrapper is `src/superclaude/skills/ccsession-tag/ccsession-orca`. Its scanner treats `--model`, `--settings`, `--permission-mode`, `--fallback-model`, and `--effort` as options taking a value rather than task/name text (`ccsession-orca:104-108`). Recognizing `--effort` is not evidence that the wrapper chooses effort.
- Wrapper relaunches hand off via `exec "$CCSESSION" --name ... --shim --claude-args "$@"` or the untagged equivalent with `--resume` appended (`ccsession-orca:174-189`). Ordinary named and untagged starts also use `--shim --claude-args "$@"` (`ccsession-orca:244-249`). Thus later research must trace the launcher parser on both sides of `--claude-args`, not assume the wrapper directly executes Claude Code.
- Untagged launch: append stored passthrough arguments, clear inherited labels, set the title, then `exec` the Claude binary with permission flags, generated settings, and an optional selected `--model` before remaining arguments (`ccsession:1896-1907`).
- Named launch: validate the name, append passthrough arguments, maintain the label store and launch-folder marker, then choose saved-session resume or new session. The saved-session path checks for a transcript and warns before continuing another existing worktree's conversation in this worktree (`ccsession:1910-1961`). A routing addition must not move these operations or inadvertently create a differently named session.
- Resume and new named launches both have model and no-model variants; each preserves permission flags, generated settings, name, and remaining arguments, and resume adds the saved session identifier (`ccsession:1963-1974`). Launch-time selection therefore applies to resume as well as new conversations. Whether a resumed CLI conversation honors every selected parameter is a downstream-runtime question, not established by these `exec` calls.
- There are six final `exec` sites (three launch forms multiplied by presence/absence of a selected model), not one universal final command. A launch-only router would need parity across all six or a deliberately proven shared selection step before them. No implementation approach is selected here.

### Picker/settings integration [CODE-VERIFIED]

- `setup_shim()` exports the original gateway separately, changes the session base URL to the shim, and enables gateway discovery (`ccsession:1060-1065`). Later code reads `/v1/models?limit=1000`, drops invalid IDs, keeps display-name/description strings, refuses an empty result, and atomically replaces a restricted-permission cache (`ccsession:1099-1130`). This is discovery/cache plumbing, not a router choosing a model from prompt complexity.
- In tier mode the warm-up reads existing generated settings, adds `modelPicker`, sends the combined JSON on a separate file descriptor, and replaces the launch settings arguments only on a nonempty successful handoff. A failure emits a warning rather than aborting (`ccsession:1132-1153`). An added effort-setting path must merge rather than replace the per-model compaction and picker settings.

### Documentation cross-check

| Documentation claim | Classification | Direct comparison |
|---|---|---|
| The workspace default model is preferred only without an explicit model/tier and only within permitted tiers (`src/superclaude/skills/ccsession-tag/README.md:525`). | [CODE-VERIFIED] | `ccsession:1201-1210` performs exactly this conditional preference. |
| If the workspace default does not apply, the default-tier policy is used (`README.md:526`, same directory). | [CODE-VERIFIED] for the fallback call; [UNVERIFIED] here for the exact policy result and unset-value default | `ccsession:1215-1218` calls the helper; role/default precedence and the `tier2` unset claim require the helper-policy investigation owned by the adjacent slice. |
| Roles above Member start on Tier1b and Members start on Tier2 (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md:27-30`). | [UNVERIFIED] as deployed Coder policy; [CODE-CONTRADICTED] if interpreted as an unconditional launcher default | The launcher prefers an allowed `ANTHROPIC_MODEL` before `default-tier` (`ccsession:1201-1218`); it contains no unconditional Tier1b start. The deployed role table is not verified by this slice. Do not turn the research worker's mandated Tier1b into product policy. |
| The source comment attributes the picker timing issue to Claude Code 2.1.269 (`ccsession:1067-1069`). | [UNVERIFIED] upstream-version behavior | The local workaround is real (`ccsession:1099-1153`), but no installed-version check or upstream reproduction ran. |

## SOLUTION_RESEARCH
Scope discovery only. No router is selected, built, downloaded, or exercised. The product requirement remains the user's Coder-role-dependent default with explicit choices and permissions preserved; the worker execution requirement is Tier1b only.

### Existing integration surfaces worth investigating

1. **Before launch:** the existing shared selection/export functions are an available boundary for choosing launch parameters. This would select for a session/start, not automatically for every later prompt or tool cycle. Investigate whether this granularity can meet the requested product behavior before proposing a design.
2. **At request forwarding:** the shim is already the launcher's selected upstream endpoint. Request-time effort/model transformation belongs to the proxy investigation, not to a new claim that the shell launcher currently does it.
3. **Explicit CLI settings:** existing test code passes `{"effortLevel":"high"}` as a user `--settings` value (`tests/unit/test_ccsession_tiers.py:1215-1216`, `:2485-2498`). The latter explicitly asserts that the user's settings remain the last two arguments while generated model settings also exist. This proves argument preservation in the test's intended contract, not how the real CLI merges repeated settings or converts effort into provider requests. Later provider/CLI investigation must verify that behavior.
4. **Shim isolation:** the launcher recovers the original gateway for nested launches, rejects shim-as-upstream, fingerprints settings/code, and reuses only matching shims; it leaves other sessions' shims running (`src/superclaude/skills/ccsession-tag/ccsession:974-1024`). A future policy that changes request behavior needs an explicit decision about per-session versus shared state and how existing isolation observes it. Do not stop/restart live shims as part of this research.

### Negative evidence and limits of discovery

- `codegraph_search("apply_tier_selection")` returned no results despite a fresh status (0 changed files). The shell function exists by direct Read. This is an index-coverage gap (`graph:empty`), not evidence of a missing function or missing callers; used Grep/Read thereafter.
- A content search of the complete launcher for `effort|Jev|jev|router|classif|complexity|reasoning` found only the unrelated word `best-effort` in a workspace-name comment. The assigned 951-1975 range was read directly. No dedicated effort chooser, prompt-complexity classifier, or Jev integration was observed in that range. This does not establish absence elsewhere in the repository or in the upstream CLI.
- Searching both `tests/unit/test_ccsession*.py` files for effort/Jev/provider-effort names found the two user-settings examples above, not a demonstrated automatic effort router. Do not claim that no effort-related tests exist; these settings-preservation examples do exist.
- A broader source search for `ccsession-orca` found installer, doctor, issue-preflight, hook, and documentation references. Those are discovery leads, not fully traced runtime callers. The immediate wrapper-to-launcher and launcher-to-Claude handoffs were read directly; unrelated consumers remain outside this slice.
- The first environment query printed only the base URL and exited 1 because optional queried variables were absent; a narrower slot query returned all three Tier1b values. Missing optional environment variables were not treated as a missing model.
- The first report Edit was refused because the freshness hook required an explicit Read even after Write. Read the assigned stub and retried through Edit successfully; no alternate mutation tool bypassed the hook.

### Runtime model provenance

At this run's 2026-11-09 scope-discovery checkpoint, startup declared `claude-gw-tier1b`. Live environment values were `T1bModel01=claude-sonnet-5-5`, `T1bModel02=gpt-6.1-sol`, and `T1bModel03=muse-wonder-full-1.0` (read directly with `printenv`, no credentials read). A bounded JSON parser matched this dispatch context in the user message of `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/bbb8a6ff-255a-43d2-ba5d-6b6fb9be329a.jsonl` and counted 39 assistant records, all with `message.model=gpt-6.1-sol`. That recorded backend matches the second live Tier1b slot; this is positive consistency evidence, not proof of the external provider's physical serving model. No model switch, fallback launch, child agent, or paid experiment ran.

### Gaps and Questions

- **[UNVERIFIED] Deployed Coder default/role policy:** the exact current user-default origin, role precedence, helper authorization results, and unset-default behavior are assigned to the launcher-initialization/policy owner. The static role-to-start-tier text is not a universal product requirement; interpreting it that way is [CODE-CONTRADICTED] by the launcher's conditional model preference described above.
- **[UNVERIFIED] Real CLI effort contract:** supported effort names, flags, environment/settings precedence, repeated `--settings` merge behavior, model switching, and resume semantics need official current documentation plus direct CLI/source evidence where available. The local wrapper's scanner and local fake-Claude tests alone cannot establish them.
- **[UNVERIFIED] External candidates:** identify Jev from authoritative sources or explicitly retain unresolved identity; examine the user-supplied cliproxy-effort-router candidate only in the later authorized external-research stage. No external identity, capabilities, installation method, or compatibility is assumed.
- **[UNVERIFIED] Model/provider boundaries:** whether effort survives gateway translation for every allowed model, how incompatible effort values fail, and whether request-time routing preserves streaming/tools/caching belong to the provider/proxy investigators.
- **[UNVERIFIED] Version/timing and measurements:** the picker comment's cited CLI version behavior is not reproduced; cost, latency, quality, and actual live proxy compatibility remain unmeasured. No test suite or live routing experiment ran in this discovery slice.

## RECOMMENDED_OUTPUTS
Task root for every relative path in this section: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`.

- **Existing, assigned deliverable:** `research/scope-02-launcher-selection.md` (this file). Stage A scope-discovery input for the parent's research notes, not the final research report or an implementation plan.
- **Existing, parent-owned:** `research/research-notes.md`. Consolidate this slice with launcher initialization, proxy, and contracts/tests slices; this worker does not edit it.
- **Proposed later investigation output:** `research/launcher-routing-investigation.md`. Precise selection/invocation matrix, explicit-choice preservation, settings-composition findings, and launch-only feasibility.
- **Proposed later external-contract output:** `research/cli-effort-contract-investigation.md`. Current CLI/provider effort surface with authoritative documentation, verified precedence, and unsupported cases.
- **Proposed synthesis output:** `research/routing-compatibility-synthesis.md`. Map launcher findings against proxy, user-default/role policy, test-contract, and external-candidate findings; distinguish code-proven compatibility from untested feasibility. These three proposed files do not exist as a result of this slice and are suggestions for the parent's task builder, not extra worker assignments already launched.

No final-report filename or task-checklist structure is invented here; the parent research workflow owns those template-governed outputs.

## SUGGESTED_PHASES
These are concrete investigation assignments for later parent planning, not instructions to spawn children now. Every proposed output below is relative to `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`.

| Proposed investigator | Investigation and files | Required result and external questions | Output and synthesis mapping |
|---|---|---|---|
| Launcher-selection investigator | `src/superclaude/skills/ccsession-tag/ccsession:1157-1281,1830-1975`; `ccsession-orca:75-121,174-189,215-249`; parser boundary from the initialization owner's findings | Enumerate tier/profile/non-tier paths crossed with new/untagged/resume and explicit/default model; account for every final argument vector, generated settings, later passthrough settings, and permissions. Determine whether launch-only routing can satisfy the intended request granularity without changing user choices. No web needed for this local flow. | `research/launcher-routing-investigation.md` -> launch/precedence section of `research/routing-compatibility-synthesis.md`. |
| CLI/provider-contract investigator | The launcher's generated settings and effort pass-through evidence; official current Claude Code docs and installed CLI inspection where permitted | Establish `--effort` and `effortLevel` support, valid values, duplicate-settings precedence, session/model-switch/resume behavior, and provider translation. Separate documentation claims from observed runtime; do not install tools or make paid calls without authorization. | `research/cli-effort-contract-investigation.md` -> effort/schema/precedence section of compatibility synthesis. |
| Existing initialization/policy owner (cross-slice request, not duplicate work) | `src/superclaude/skills/ccsession-tag/models.py`: `tier_env`, `tier_access`, `in_my_tiers`, and `main` helper subcommands; launcher argument parsing and environment origin | Return exact configured Coder-user-default origin and role restrictions; trace explicit model/tier inputs across `--claude-args`. Resolve the documentation-policy gap without universalizing the worker's Tier1b requirement. No deep reread by this slice. | Consume that owner's assigned scope and later research outputs into default/authorization section of compatibility synthesis. |
| Existing proxy owner (cross-slice request) | `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` and its registry/helper contracts | Determine request-time versus launch-time feasibility, aliases, model/effort rewriting, stream/tool/cache integrity, and per-session isolation. External candidate inspection only after local scope discovery and authorized web stage. | Consume that owner's assigned output into proxy-boundary and failure-mode sections of compatibility synthesis. |
| Existing contracts/tests owner (cross-slice request) | `tests/unit/test_ccsession_tiers.py`, `tests/unit/test_ccsession_tag.py`; fixture `_launch/_launch_env`; default/permission/passthrough tests located above | Build an evidence matrix from existing tests; distinguish fake-CLI argument preservation from real CLI/provider behavior. Include explicit effort in user settings, repeated settings, tier switch, and named-model/default paths as investigation gaps, not invented regressions. | Consume that owner's assigned output into coverage/validation section of compatibility synthesis. |
| Parent's external-candidate researcher | User-supplied cliproxy-effort-router reference and unresolved Jev identity from the original issue, then other source-backed candidates | Identify candidate entry points, routing granularity, supported effort schemas, data sent to classifiers, cost/latency evidence, and permission/default preservation. Do not assume Jev's identity or select an architecture before evidence. | Parent-defined external research artifact -> candidate comparison section of compatibility synthesis. |

Suggested sequence: complete and independently check local scope slices; build the research task; then run local-flow and external-contract/candidate investigations in the parent's authorized execution stage; finally synthesize options and unresolved evidence before any separate implementation decision.

## TEMPLATE_NOTES
Structure derives directly from installed `tech-research/SKILL.md` A.4 (read lines 265-305): metadata plus EXISTING_FILES, PATTERNS_AND_CONVENTIONS, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, and AMBIGUITIES_FOR_USER. The instruction calls these six categories but shows seven headings; preserved all seven rather than dropping one. Header/skeleton was written before findings, then populated in place.

For the parent's later research task, Template 02 is appropriate for the explicitly selected tech-research workflow's discovery, separate investigations, synthesis, and independent gates. This is not a decision to use that task format for subsequent product implementation. No template contents beyond the governing A.4 skeleton were required or fabricated by this scoped researcher.

## AMBIGUITIES_FOR_USER
None. Intent is clear: investigate compatibility and options without implementing or selecting a router. Jev identity and external/CLI behavior are research questions for later investigation, not reasons to ask the user now. User-default means the user's Coder-role-dependent default, not a universal Tier1b.

## Summary and handoff state

- This slice's assigned source discovery is complete: the full launcher range was read, direct selection/export/invocation and immediate wrapper calls were mapped, related test assertions and documentation claims were distinguished from runtime proof, and concrete later research assignments were recorded.
- No source, tests, configuration, installed primitives, or other assigned artifacts changed. No web research, installs, child agents, model fallback, GitHub writes, commits, push, PR, merge, or live routing/model experiments ran. Only this report was authored.
- No test-pass claim is made; tests were inspected, not executed. This producer did not run or claim an independent quality gate. Parent must consume the file from disk and apply its independent scope-sufficiency/review gates before treating the overall research stage as complete.
- Operational evidence shows the recorded backend is in the live Tier1b slots; unresolved external behavior, physical provider identity, deployed role configuration, and cost/latency/quality remain explicitly unverified.
