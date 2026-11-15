# Research Notes: Model and effort router, contracts and tests scope

**Date:** 2026-11-09
**Scenario:** A, scope discovery slice 4 only
**Depth Tier:** Deep parent research, bounded independent Tier1b discovery
**Status:** Scope discovery populated; awaiting parent independent review and acceptance
**Governing skeleton:** installed tech-research/SKILL.md A.4

---

## EXISTING_FILES
All paths below are relative to the issue-463 checkout unless absolute. This is focused discovery, not a runtime test result. Total sizes for the helper, documentation and test suites were measured with `wc -l`; only the cited source ranges were inspected, not every line of those files.

| File/subsystem | Purpose and integration surface | Evidence and size |
|---|---|---|
| `src/superclaude/skills/ccsession-tag/ccsession.env.example` | User proxy/auth file example, optional tier settings and permission timing caveat. Not a model registry or per-role default policy. | Lines 1-31; about 32 lines. |
| `src/superclaude/skills/ccsession-tag/ccsession-models.json` | Schema-2 data: profile IDs/windows/shim metadata, tier slot names, picker lists and display labels. Tier1b names environment slots, not fixed backend IDs. | Lines 1-19, 70-92, 122-173; about 174 lines. |
| `src/superclaude/skills/ccsession-tag/models.py` | Shared model-data loader, validation/cache, workspace export parser, identity/role rules, tier and model windows, aliases, compaction settings and CLI. Key functions: `validate`, `load`, `tier_env`, `user_access`, `tier_access`, `resolve_tiers`, `compact_settings`, `model_window`. | Lines 147-244, 325-420, 448-744; 1,111 lines total. Exact CLI and caller points follow below. |
| `src/superclaude/skills/ccsession-tag/README.md` | Operator contract for per-owner access, role matching, default selection, tier settings and advisory limits. | Lines 468-540; 772 lines total. |
| `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` | Tier placement rationale and external scores/prices; describes Coder defaults as external authority. Do not treat its current role layout as universal policy. | Lines 5-11, 25-42; 216 lines total. |
| `tests/unit/test_ccsession_tiers.py` | Helper, launcher and proxy regression suite, including safe parsing, role access, old/new policy compatibility, model windows and environment default precedence. | Lines 2999-3072, 3299-3376; 3,399 lines total. Test bodies were inspected, not executed. |
| `tests/unit/test_ccsession_tag.py` | Profile launches, package/install behavior, model-data refresh/cache validation, settings preservation and shim behavior. | Model-data bodies inspected at 1149-1245 and installer checks at 1068-1137; 4,823 lines total. |

Execution-tier evidence: startup identifies this session as `claude-gw-tier1b`. A search for this worker's unique tool descriptions identifies its own transcript as `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/da6e59ef-d491-4171-998c-177cd5be305e.jsonl`; an exact JSON model-field search shows backend `gpt-6.1-sol` in assistant records (lines 42 and 58). A live `printenv T1bModel01 T1bModel02 T1bModel03` on 2026-11-09 returned `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`, in that order. Thus the observed backend belongs to live Tier1b slot 2; this proves membership for this observed execution, not that every future request will select the same backend. No child agents or fallback sessions were launched.

## PATTERNS_AND_CONVENTIONS
### Existing contracts and real integration points

- **CODE-VERIFIED: role policy is parameterized, not hardcoded Tier1b.** `models.py:527-545` describes username > first matching role > wildcard precedence; `models.py:568-624` implements selection and rejects malformed, undefined or disallowed start tiers. New `CCSESSION_TIER_RULES` replaces legacy `CCSESSION_ACCESS` when present (`models.py:550-567`). The CLI `default-tier` returns a matched start tier, otherwise configured default, otherwise warns and uses tier2 (`models.py:1007-1044`). Preserve this distinction when carrying #462 into synthesis.
- **CODE-VERIFIED: inherited named default can precede role-tier selection.** `ccsession:1201-1218` checks `ANTHROPIC_MODEL` only when no explicit model/tier choice exists, validates membership through `in-my-tiers`, then calls `model-resolve`; only the alternate path calls `default-tier` and `tier-resolve`. `models.py:890-901` checks names and picker aliases, accepts `[1m]`, and returns false on invalid input/policy. This is an important precedence question for #462, not proof that role defaults are universally applied before inherited defaults.
- **CODE-VERIFIED: workspace tier file is parsed as data.** `models.py:381-420` restricts export parsing; `models.py:459-471` prefers a present defaults file over shell tier values. `tests/unit/test_ccsession_tiers.py:145-180` explicitly excludes `ANTHROPIC_MODEL` from this parser and tests stale shell replacement. The launcher's inherited `ANTHROPIC_MODEL` and the helper's parsed tier-policy dictionary are separate input channels. Do not assume editing a model default in the file alone refreshes that inherited variable.
- **CODE-VERIFIED: schema and windows constrain new routes.** `models.py:147-214` validates model IDs, profile windows, tier slots and picker fields; `models.py:655-677` requires every tier slot, slot window and tier window. `models.py:681-716` builds per-model/tier compaction settings, shares picker aliases and merges canonical Claude spellings using the smaller window. `models.py:720-744` resolves tier aliases and individual windows. A future router must not merely replace a model string while leaving incompatible context/compaction settings.
- **CODE-VERIFIED: shell/helper boundary is a concrete API.** `models.py:916-935` and `models.py:945-989` emit `PROFILE_*` lines for tier/model choices; the caller consumes those fields at `ccsession:1224-1230`. Per-model compaction is requested at `ccsession:1253-1259`. These are integration points for later compatibility analysis, not a recommendation to add another resolver now.
- **CODE-VERIFIED: proxy shares the helper's policy.** The bounded caller inspection at `local-gateway-alias-proxy.py:190-220` reads `model_data.load`, `tier_env`, `tier_mode`, and `tier_access`; it filters offered tiers using the same access decision. It also obtains `CCSESSION_MODEL_ORDER` for picker order. This does not establish that display order changes backend failover order; slice 3 owns forwarding internals.
- **CODE-VERIFIED: cache and shim identity are separate concerns.** `models.py:233-244` chooses newest valid cached/bundled data, with a built-in minimum when neither is valid. `models.py:748-782` includes owner identity/roles, tier mode, timeout and cooldown settings in a session shim fingerprint, while a present normal defaults file is reread rather than embedding its contents. Any later effort-routing state needs analysis of session isolation and stale-shim reuse, not an assumed existing effort-key contract.

### Documentation status

| Documentation claim | Label | Code/test comparison |
|---|---|---|
| README username/role/wildcard precedence and advisory access (`README.md:475-512`) | CODE-VERIFIED for selection and advisory model; no gateway authorization claim | `models.py:568-624` implements precedence; owner/role values come from mutable process environment (`models.py:504-524`). This is not a server-side security boundary. |
| README workspace named default wins when eligible (`README.md:525-526`) | CODE-VERIFIED | `ccsession:1201-1218`; regression assertions at `tests/unit/test_ccsession_tiers.py:3302-3376`. |
| MODEL-TIERS says privileged roles start Tier1b and Members Tier2 (`MODEL-TIERS.md:27-30`) | UNVERIFIED as a universal/live Coder deployment statement | The helper reads policy, not a fixed role map. Existing role fixture tests intentionally start privileged roles on tier1a (`tests/unit/test_ccsession_tiers.py:2999-3013`). That is a fixture of arbitrary policy, not proof the live Coder release is wrong. Do not turn the page's layout into the #462 requirement. |
| MODEL-TIERS scores, prices and provider capabilities (`MODEL-TIERS.md:35-42`) | UNVERIFIED externally | This slice used no web and made no provider call. Tier JSON validates names/windows, not prices, intelligence, effort support or rankings. |
| Env example's user proxy/auth file and optional settings (`ccsession.env.example:1-31`) | UNVERIFIED here for full sourcing/permission timing; literal example contents verified | Launcher-init and launcher-selection slices own shell timing. No live secret file was opened. |
| Any assertion that existing helper/registry implements intelligent model-plus-effort selection | CODE-CONTRADICTED within this bounded scope | No effort/router fields appear in the helper or bundled registry; concrete selection examined above is explicit/inherited choice plus configured role/tier policy. Forwarding behavior outside this bound remains slice 3's responsibility. |

## SOLUTION_RESEARCH
N/A: pure scope investigation, not implementation. No router architecture, dependency, provider, or deployment change was selected. No external candidate was fetched or executed.

### Inspected test contracts, not test-run results

| Contract | Inspected evidence | Later compatibility question |
|---|---|---|
| Explicit choices override the inherited default | `tests/unit/test_ccsession_tiers.py:3318-3328` | Does a candidate router preserve explicit model and tier choices rather than silently replacing them? |
| Eligible inherited model uses its own window and picker entry | `tests/unit/test_ccsession_tiers.py:3302-3315` | Does any role-default correction retain the resolved model's context, compaction and picker metadata? |
| Invalid, unknown and disallowed inherited models fall back | `tests/unit/test_ccsession_tiers.py:3331-3368` | Does a candidate preserve access filtering and the configured fallback rather than impose Tier1b? |
| Non-tier launches ignore this inherited-model path | `tests/unit/test_ccsession_tiers.py:3371-3376` | Is behavior outside tier mode deliberately unchanged? |
| User effort setting passes through as supplied | `tests/unit/test_ccsession_tiers.py:2485-2498` asserts the trailing user settings argument containing `effortLevel: high` remains untouched | This proves a launcher argument-preservation test exists, not that a gateway honors it or that effort is selected automatically. Later research must trace effective precedence and provider translation. |
| Shipped registry validates and refresh uses conditional caching | `tests/unit/test_ccsession_tag.py:1156-1159,1212-1228` | Can candidate metadata coexist with existing validation and cache behavior? |
| Bad and older registry downloads are rejected | `tests/unit/test_ccsession_tag.py:1231-1245` | Any proposed data extension needs version/validation analysis; do not bypass the current boundary. |

These bodies were read, not run. Existing tests are evidence of asserted contracts, not proof that this checkout passes them today. Additional installer evidence was inspected at `tests/unit/test_ccsession_tag.py:1068-1114`: it asserts private env-file permissions and preservation of an edited sentinel on reinstall. The narrowly owned migration in `unseed-env.py:29-49` skips symlinks and user-edited files, and only resets the exact legacy installer shape. Neither discovery authorizes changes to real user secrets.

### Negative evidence and limits

- Exact case-sensitive content searches for `effort|reasoning|Jev|cliproxy|router` returned no matches in `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/skills/ccsession-tag/ccsession-models.json`. Combined with the inspected resolver, policy and registry code, this did not reveal an intelligent effort-selection contract in those two files. It is not a repository-wide or semantic proof of absence.
- The same focused search in `tests/unit/test_ccsession_tag.py` found `cliproxyapi` at line 619, not evidence identifying Jev or integrating the supplied effort-router candidate. That test location was not followed into a router investigation. Effort-setting preservation is instead positively evidenced in the tier suite above.
- No candidate-source, provider-documentation, live Coder role-policy, price, or benchmark verification was performed. Jev's identity and the supplied candidate's actual capabilities remain UNVERIFIED, not rejected or selected.
- Deep launcher initialization, session reuse, forwarding, failover and streaming analysis remain owned by slices 1-3. Only bounded helper callers were read here. No global settings or live secret file was opened.
- The first environment probe for Orca/session variables returned no values; the later multi-variable tier probe returned the three slots but exited nonzero because other requested names were unset. Transcript identification was narrowed using worker-specific tool descriptions before checking backend model fields. This records observed membership, not guaranteed backend pinning.

### External questions for later research

1. What project/person/product does Jev identify, and what primary source establishes it? Retain the unresolved identity if reliable evidence cannot identify it.
2. What does the supplied router actually classify or rewrite: initial model, per-request model, provider effort, or all three? Check source and a pinned revision before treating its README as implementation evidence.
3. Which supported providers accept which effort/thinking controls, and what happens to unsupported settings, tool calls, streamed responses and conversation state when a route changes? Documentation and source evidence are needed; no capability is inferred from a model label.
4. Where does the deployed Coder role-dependent default originate, and when does a new terminal inherit it? Correlate authorized deployment evidence with the launcher slices, without reading credentials or treating arbitrary test fixtures as live policy.

## RECOMMENDED_OUTPUTS
Only this assigned scope file was created by this worker. The following full paths are proposed later deliverables for the parent to reconcile with its actual plan; they are not existing files or extra work started here.

- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/scope-04-contracts-tests.md`: this discovery input, including contracts, test leads and bounded negative evidence.
- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/default-and-policy-contracts.md`: follow-on default-origin and precedence evidence, separating inherited named models from matched role-tier defaults.
- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/router-source-and-effort-contracts.md`: pinned external candidate evidence, Jev identity findings and provider effort-control questions.
- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/compatibility-test-matrix.md`: existing asserted behavior, coverage gaps and proposed checks, clearly separating inspected tests from observed runs.
- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/synthesis/contracts-and-compatibility.md`: merge this slice's contract evidence with launcher and proxy evidence from slices 1-3, without selecting an architecture prematurely.
- `/home/coder/workspaces/worktrees/IronClaude/issue-463/.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/RESEARCH-REPORT-model-effort-router.md`: proposed final report destination, subject to the parent's governing task. State verified findings, candidate comparisons, unresolved identity/capability gaps and any later decisions needed.

## SUGGESTED_PHASES
These are follow-on research assignments for the parent, not child agents launched by this worker. Each output filename below resolves to the full path listed above.

| Suggested assignment and investigation type | Topic and source scope | Research output | External gap | Synthesis mapping |
|---|---|---|---|---|
| 1. Code/deployment contract tracing | Start with `models.py` parser, identity, access and default CLI; compare default-model regressions in `tests/unit/test_ccsession_tiers.py`. Consume slices 1-2 for shell inheritance and explicit-option timing rather than redoing their deep trace. | `default-and-policy-contracts.md` | Authorized Coder default origin and role policy, including refresh/inheritance timing. | `contracts-and-compatibility.md`: default precedence and access invariants; final report: #462 boundary. |
| 2. External primary-source comparison | Supplied router candidate and independently discovered alternatives; identify Jev or retain explicit uncertainty. Compare effort input/output controls against the user-settings preservation assertion, not an assumed existing automatic selector. | `router-source-and-effort-contracts.md` | Candidate revision/license/maintenance, actual routing mechanism, provider-supported controls and state/stream compatibility. Web research begins only in the later authorized phase. | `contracts-and-compatibility.md`: candidate-to-contract compatibility; final report: source-backed comparison and unknowns. |
| 3. Code/test coverage analysis | `ccsession-models.json`, `models.py` validation, windows, aliases, fingerprint and cache; relevant tier/tag tests. Consume slice 3 for request rewrite, failover and streaming claims. | `compatibility-test-matrix.md` | Cross-provider effective effort behavior and state continuity need external evidence or separately authorized tests. | `contracts-and-compatibility.md`: coverage, gaps and proposed checks; final report: confidence and limitations. |

Proposed coverage rows: explicit model, explicit tier, eligible inherited model, disallowed/unknown inherited model, matched username/role/wildcard start, non-tier mode, supplied user effort, alias collisions, context/compaction windows, registry validation/versioning, and session settings isolation. This is an investigation checklist, not test code or a claim of executed coverage. Preserve the user's configured default according to their Coder role; do not rewrite it as a universal Tier1b default.

## TEMPLATE_NOTES
The seven actual headings in the installed tech-research A.4 skeleton govern this file, despite the surrounding prose calling them six categories. The file was stubbed before source findings and populated incrementally. This is an independently gathered Stage A scope input for the parent, not a final research report or an implementation task.

The installed skeleton suggests Template 02 for the parent's tech-research task. No task template was instantiated here, and this does not select the MDTM implementation workflow. Independent review and acceptance belong to the parent; no prohibited child reviewer was spawned. Test execution, web research and implementation remain outside this slice.

## AMBIGUITIES_FOR_USER
None: the requested scope and role-dependent default requirement are clear. Jev's identity, external router capabilities and the deployed Coder configuration are evidence gaps for later investigation, not a reason to ask the user to restate the requirement. Escalate only if later primary-source research cannot resolve an identity or product decision genuinely requires user input.
