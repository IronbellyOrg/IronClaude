# Research Notes: Model and effort router launcher initialization

**Date:** 2026-11-09
**Scenario:** A, focused scope discovery
**Depth Tier:** Deep (parent research); bounded discovery slice only
**Scope:** Launcher lines 1-950, setup/config/environment and relevant caller discovery
**Status:** Complete (assigned discovery slice only; parent independent review pending)

---

## EXISTING_FILES
### Bounded inventory

Counts measured with `wc -l`; paths below are repository-relative. Eleven core source/test files were counted across three groups: launcher configuration, lifecycle/install callers, and test entry points. Other slices own complete proxy/model-contract/test inventories.

| File | Lines | Purpose and discovery coverage |
|---|---:|---|
| `src/superclaude/skills/ccsession-tag/ccsession` | 1975 | Bash launcher. Read lines 1-950 only, including setup, label helpers, argument collection, environment loading, tier activation and start of shim identity check. Remainder deliberately delegated. |
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | 249 | Orca front door; targeted caller reads only. Restarts call `--orca-tab-reopen` then exec the launcher with `--shim --claude-args` at lines 174-189; normal handoff does the same at lines 240-249. |
| `src/superclaude/skills/ccsession-tag/models.py` | 1111 | Model helper boundary, symbol discovery only. Launcher calls `tier-mode` and `tiers`; resolution/access/default semantics are delegated to the contract slice. |
| `src/superclaude/skills/ccsession-tag/ccsession.env.example` | 31 | Public proxy/auth and optional tier configuration documentation, read in full; not live defaults. |
| `src/superclaude/skills/ccsession-tag/install.sh` | 172 | Standalone installation integration; bounded follow-on entry, not executed. |
| `src/superclaude/skills/ccsession-tag/hooks/session-start.sh` | 47 | Hook entry point; target for lifecycle-preservation investigation. |
| `src/superclaude/skills/ccsession-tag/hooks/session-name.sh` | 217 | Hook caller locations identified; targeted body read is recorded below. |
| `src/superclaude/cli/install_ccsession.py` | 133 | `wire_ccsession(home: Path | None = None) -> tuple[bool, str]` at line 11. Locates installed launcher, Orca wrapper, hook and example at lines 12-18; rejects unsafe file/symlink shapes before wiring at lines 19-37. Targeted first 55 lines read. |
| `tests/unit/test_ccsession_tag.py` | 4823 | Launcher/name/profile/environment test discovery only; tests not executed. |
| `tests/unit/test_ccsession_tiers.py` | 3399 | Tier/default/model/permission test discovery only; tests not executed. |
| `tests/unit/test_install_ccsession.py` | 323 | Installer regression test lead; tests not executed. |

### Regression anchors (discovered, not executed)

- `tests/unit/test_ccsession_tag.py:225-249`: private profile can suppress env/model and refuse shim; other-writable add-on is ignored. Read actual assertions.
- `tests/unit/test_ccsession_tag.py:1574-1624`: env-file permission opt-in does not change flags; a launched fake Claude sees only the original shell permission value. Read actual assertions; this is source evidence, not an observed test pass.
- `tests/unit/test_ccsession_tag.py:1659-1672`: invalid permission values stop a launch and help with exit 2. Read actual assertions.
- `tests/unit/test_ccsession_tiers.py:598-642`: permission opt-in preserves tier model/settings/base URL in fixtures; profiles/bad tiers are rejected in tier mode; non-tier model flags remain intact. Actual assertions were read, no live gateway was exercised.
- Additional name-only search leads for the test slice: `test_default_tier_sets_model_and_tier_window`, `test_orca_relaunch_reopens_the_tabs_session_on_the_default_tier`, `test_orca_launch_with_a_prompt_in_tier_mode_is_auto_named_and_goes_through_the_shim`, `test_named_tier_checks_definition_and_owner` in `tests/unit/test_ccsession_tiers.py`. Bodies deliberately deferred.

Additional confirmed config/document surfaces: `src/superclaude/skills/ccsession-tag/ccsession-models.json` (Tier1b slot mapping at lines 85-91), `src/superclaude/skills/ccsession-tag/README.md` (targeted claims below). No source, tests, installed configuration or generated mirrors were modified.

## PATTERNS_AND_CONVENTIONS
### Initialization and selection boundary [CODE-VERIFIED]

All launcher references below are to `src/superclaude/skills/ccsession-tag/ccsession`.

1. Permission policy is captured from the calling shell before env-file loading: `_cc_permissions` accepts empty or `default`, otherwise exits 2; default flags include Grep and normally skip-permissions, while explicit `CC_CLAUDE_FLAGS` overrides the defaults (`ccsession:134-143`). A router must not treat model selection as authorization to alter those flags.
2. Helper location follows the real launcher symlink target, not the current project: resolve links into `CCSESSION_DIR`, then `CCSESSION_MODELS=$CCSESSION_DIR/models.py` (`ccsession:148-160`). Shim script defaults separately to the installed skill path; port defaults to 4010 (`ccsession:145-147`).
3. Wrapper parsing captures name, shim, profile, tier and model choices. `--claude-args` stops wrapper parsing and saves the rest unchanged (`ccsession:729-800`); model token spelling and position are saved (`ccsession:801-814`). Explicit model flags inside the pass-through payload therefore are not visible to this parser. Precedence must be traced at the later launch boundary before assigning any new default.
4. A selected local profile loads owner-controlled non-group/other-writable `.sh` add-ons, normalizes the profile function name, resets profile values, runs the matching function and can reject a shim (`ccsession:824-858`). These add-ons execute shell code, not declarative model metadata. Do not rewrite their location or relax their ownership checks.
5. Next, source the configurable user env file unless the profile disables it; restore/unset `CCSESSION_PERMISSIONS` to its captured shell value (`ccsession:861-874`). The implementation restores this variable, not every variable the sourced shell file could alter. No live secret file was opened for this discovery.
6. Tier enablement delegates to `models.py tier-mode`; a recognized private add-on profile bypasses it. Tier mode rejects any nonempty profile and forces the shim (`ccsession:880-891`). Available tiers from `models.py tiers` selectively set the Opus/Sonnet/Haiku alias env variables; an unavailable tier leaves its inherited alias unchanged (`ccsession:892-898`). This is alias compatibility, not proof that the user's default tier is Tier1b.

### Product constraint, not a discovered implementation

The dispatch fixes related issue #462's requirement as **the user's Coder-role default**, while Tier1b is only this research execution tier. Whether current default resolution fully implements that requirement is UNVERIFIED in this slice and belongs to the model-contract researcher. Do not derive a universal Tier1b product default from this session.

## SOLUTION_RESEARCH
N/A: focused discovery only, not implementation or candidate selection. No web research performed.

### Existing integration surfaces [CODE-VERIFIED]

- Outside tier mode, captured model tokens are reinserted at their original argument position (`src/superclaude/skills/ccsession-tag/ccsession:902-906`). A launch-level router must preserve explicit choices and the `--claude-args` boundary, not assume the first parser sees every Claude model flag.
- Auth setup copies `LITELLM_API_KEY` only when neither Anthropic auth variable is set, and removes the token only when it duplicates the API key (`src/superclaude/skills/ccsession-tag/ccsession:909-919`). The private-profile skip flag skips this whole block. Candidate compatibility must be established without copying live keys into research files.
- Shim listener identification is `shim_listener_pid()` at line 922; health checking begins `shim_health_status()` at line 936, fetching the local identity endpoint and parsing JSON (`src/superclaude/skills/ccsession-tag/ccsession:922-950`). The success/mismatch comparison and process decisions lie beyond this slice. A pre-existing listener is not itself evidence of matching configuration.
- Lifecycle hooks resolve the sibling or installed launcher and invoke `--sync-name`, `--orca-tab-session`, `--orca-tab-clear` (`src/superclaude/skills/ccsession-tag/hooks/session-name.sh:183-214`). Router work should stay off these hook fast paths and must not turn name synchronization into a model decision.

### Documentation cross-check ledger

| Documentation claim | Status | Evidence / disposition |
|---|---|---|
| Env template says the wrapper sources the selected user env before launch (`ccsession.env.example:10-12`) | CODE-VERIFIED, for normal configuration-loading path | Launcher `ccsession:861-866` does so conditionally; hook/name fast paths intentionally skip it. This is not a claim that every invocation reads secrets. |
| README permission option is read from the calling shell before env-file sourcing (`README.md:540-541`) | CODE-VERIFIED for initialization and restore behavior | Launcher `ccsession:134-141` and `ccsession:868-874`; actual final Claude arguments and nested execution still require the remainder slice. |
| README gives model/tier/user/role precedence and a defaults-file path (`README.md:525-532`) | UNVERIFIED in this slice | Direct launcher calls delegate to `models.py`; assign exact precedence, owner-role interpretation and the defaults-file claim to the contract researcher. |
| README says cooldown, first-byte timeout, port fingerprinting and nested gateway unwrapping work (`README.md:535-539`) | UNVERIFIED in this slice | Most implementation is beyond launcher line 950 or in proxy/model helper; delegate rather than treat prose as runtime proof. |

No CODE-CONTRADICTED claim established in the inspected documentation subset. This is not a clean bill for the full README; deferred claims remain listed in Gaps and Questions.

## RECOMMENDED_OUTPUTS
Existing assigned deliverable: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/scope-01-launcher-init.md` (this file).

Proposed later outputs, not created by this worker; all under `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`:

| Planned relative path | Purpose |
|---|---|
| `research/launcher-selection-trace.md` | Exact argument/env/default-to-final-exec trace, including Orca pass-through. |
| `research/owner-default-precedence.md` | Model-contract owner's resolved Coder-role/default precedence and permitted explicit overrides. |
| `research/router-candidate-compatibility.md` | Source-backed external candidate comparison, including Jev identity and authentication/effort compatibility. |
| `research/launcher-regression-map.md` | Test owner's evidence map; distinguish mocked tests, live checks and untested paths. |
| `synthesis/launcher-constraints.md` | Merge initialization, permission, profile and lifecycle constraints from this slice and the remainder trace. |
| `synthesis/routing-compatibility.md` | Merge launcher constraints, contracts, proxy findings and external candidate evidence without selecting architecture prematurely. |

Parent owns final report path and synthesis naming. These names are concrete proposed assignments, not claims that files already exist; reuse parent-selected equivalents to avoid duplicate research.

## SUGGESTED_PHASES
These are later investigation assignments for the parent, not agents launched here. Reuse the current slice owners for remainder, contracts/proxy and tests rather than duplicating their work. Proposed output paths are under the same parent package as this artifact.

1. **Code tracer: final launch and explicit-choice precedence.** Input: this file's argument/environment boundary, launcher remainder lines 951-1975 and `ccsession-orca` call sites. Resolve how `CLAUDE_PASSTHROUGH`, `MODEL_ARG`, `TIER_ARG`, env defaults and resume choices reach each final exec; identify exact point(s) where a prospective router could receive the task and where it must abstain for an explicit choice. Confirm whether normal Orca `--model` flags after `--claude-args` override or are overridden by tier settings. Output `research/launcher-selection-trace.md`; synthesis `synthesis/launcher-constraints.md`. No web needed.
2. **Contract tracer: user default and permitted model set.** Input: `models.py` call boundaries `tier-mode` and `tiers`, and README claims at 525-532. Trace `defaults_path`, `read_defaults_file`, `tier_env`, `tier_mode`, `owner_name`, `owner_roles`, `user_access` and downstream resolution as selected by that slice's own discovery. Resolve file-vs-shell precedence, per-user/per-role selection, missing/invalid rules, allowed aliases and context windows; retain issue #462's user-default requirement. Output `research/owner-default-precedence.md`; synthesis `synthesis/routing-compatibility.md`. External question: what exactly does the deployed Coder template guarantee about owner/roles/defaults delivery? Obtain the actual template/config source later, not an inference from README.
3. **Integration mapper: candidate router and transport constraints.** Input: this file plus proxy owner's request/rewrite/failover evidence; later inspect the user-provided effort-router example and identify Jev. Establish whether each candidate decides once per launch or per request, understands explicit overrides, emits provider-appropriate effort settings, preserves streaming/tool-call/auth behavior and avoids a second shim/proxy loop. Output `research/router-candidate-compatibility.md`; synthesis `synthesis/routing-compatibility.md`. Web is explicitly deferred until the parent's external-research stage; obtain upstream candidate source and official provider effort support then.
4. **Test/pattern investigator: initialization regression matrix.** Input: the test anchors above, installation caller and profile/permission/env boundaries. Map existing assertions to shell-vs-file permissions, local profile skip/refusal, non-tier model pass-through, unavailable tier aliases, Orca pass-through and hook fast paths; report missing coverage rather than adding tests during research. Output `research/launcher-regression-map.md`; synthesis `synthesis/launcher-constraints.md`. No web needed; running tests requires separate authorization/scope from the parent.

Follow-on scopes deliberately excluded here: complete shim identity/start/restart and gateway-unwrapping decisions; proxy request rewriting, streaming and failover; complete model registry/access/default contract; test execution or new tests. They have dedicated owners.

## TEMPLATE_NOTES
Structure derives from installed `tech-research/SKILL.md` A.4's research-notes skeleton, retaining all seven named headings even though its prose calls them six categories. Added the researcher's required gaps, negative evidence, execution provenance and summary subsections. Stub was created before source investigation, then populated through incremental Edit calls. A.4 notes that the parent research task commonly uses Template 02; this slice neither selects a new executor nor builds an MDTM task, implementation plan or product design.

## AMBIGUITIES_FOR_USER
None requiring a user decision for this bounded discovery. Intent is fixed by the dispatch: discover before design; preserve the user's Coder-role default and explicit choices; execute research on Tier1b only. Jev's identity is a factual research gap, not permission to invent a component or choose a design.

### Gaps and Questions
- **UNVERIFIED: default/role precedence.** README's model, tier, rules, access, owner roles and defaults-file assertions need the model-contract owner's source trace; launcher initialization alone proves delegation, not the answer. Do not replace the owner's default with this worker's Tier1b execution selector.
- **UNVERIFIED: final argument precedence.** Orca forwards Claude flags after `--claude-args`; initialization stops parsing there. Remainder owner must show final argv and resolve precedence before any integration point is selected.
- **UNVERIFIED: full shim matching and lifecycle.** This slice ends inside `shim_health_status`; success/stale comparison, restart policy, nested gateway unwrapping, cooldown and timeouts are unverified here. README claims about these remain deferred to remainder/proxy/contract owners.
- **UNVERIFIED: Jev and candidate compatibility.** External identity, capability, licensing, maintained versions and provider effort mappings are not established. Later source research must resolve these; this slice performs no web lookup and endorses no candidate.
- **UNVERIFIED: deployed Coder template contract.** No live template or role-delivery source was opened. Compare actual deployment inputs with the helper's parser in a separately scoped investigation.
- **UNVERIFIED: runtime coverage.** Assertions were read but no tests, launches or gateway requests were run. Parent must distinguish source evidence from measured behavior and obtain independent review of the slice before synthesis acceptance.
- No confirmed code/document contradiction in this bounded subset. If later owners contradict a scoped claim, reconcile against exact source before synthesis; do not silently choose a version.

### Negative evidence and limits
- Searched launcher text with `effort|Jev|router|decision` (bounded 40 matches): the only hit was the unrelated phrase `best-effort` after this slice. No matching decision-router/effort token was found within lines 1-950, and direct reading of those lines found no dedicated effort parser. This does not prove absence elsewhere or preclude opaque pass-through of a Claude effort flag.
- `models.py` symbol search was capped at 40 lines and test name searches at 40 lines; these are deliberately incomplete location leads, not full inventories or absence evidence. The proxy and model helper bodies were not researched here.
- Codegraph reports indexed Python/JavaScript/TypeScript/YAML/Liquid, but not Bash; no claim of zero Bash callers derives from graph edges. Relevant callers were located by text search and selectively read.
- The session exposes no `mcp__auggie__codebase-retrieval` tool, so it was unavailable. No source edits required it; no remote code-search substitute or upstream interaction was attempted. Local bounded Read/Grep/Glob was used.
- Initial combined `printenv` inspections exited 1 because some optional Orca/model/graph environment names were unset; this was not treated as a launcher failure. `TERM_PROGRAM=Orca` plus executable lookup resolved the managed Orca CLI, whose guide and coordination commands succeeded.
- No web, live private env-file read, candidate checkout, install, config edit, source edit, test run, native/nested agent, GitHub operation, commit, push, PR or merge. Installer code was read only. Only the assigned report is written and staged.
- Parent's independent review has not run in this worker. Self-inspection of headings/placeholders is structural completion only, not an independent quality verdict.

### Execution provenance
- Execution checked at 2026-11-09T02:39:53Z. Startup selector is `claude-gw-tier1b`; selector alone was not accepted as backend proof.
- Found this worker's transcript by searching the exact assigned task ID: `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/05e3d544-bb69-498a-9835-2d82ca7ea210.jsonl`. Bounded model-field extraction shows selector `claude-gw-tier1b` at record line 30 and actual assistant backend `gpt-6.1-sol` at lines 38-40 and 65. Only model fields were emitted.
- Live `printenv T1bModel01 T1bModel02 T1bModel03` returned `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`. Installed registry `/home/coder/.claude/skills/ccsession-tag/ccsession-models.json:85-91` binds Tier1b to those slots. Actual backend therefore belongs to a live Tier1b slot. No model change, fallback launch or nested agent occurred.
- Codegraph reported 0 changed indexed files for this worktree; Bash was not among its reported indexed languages, so bounded direct Read/Grep supplied launcher evidence. No index mutation was performed.
- Governing sources read: installed rf-task-researcher definition (including staleness labels and incremental writing), installed tech-research A.3-A.4, supplied global/project instructions, installed routing guide and codegraph rules. Independent review is reserved for the parent.
- Initial Edit after stub creation was blocked because the freshness hook requires an explicit Read, not merely Write. Read the assigned artifact and retried through Edit; no bypass or alternate writer was used.

### Summary
Scope-discovery slice 1 is populated: launcher initialization lines 1-950, selected configuration/install/lifecycle callers, documentation checks and regression-test leads are recorded above. The key follow-on questions are final explicit-choice precedence after Orca pass-through, the user's Coder-role default contract, complete shim/proxy behavior, and external candidate identity/effort compatibility; each has an assigned investigation boundary and proposed synthesis destination.

This is a discovery input, not a router design, implementation, runtime test result or independent acceptance. The parent must read this file, combine it with the other slices and obtain the required independent review before accepting synthesis; this worker launches no further investigators.
