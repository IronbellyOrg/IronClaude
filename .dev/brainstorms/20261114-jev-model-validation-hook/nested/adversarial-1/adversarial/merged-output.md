---
title: Version 1 model-policy hook, merged design (enforce the requested or defined model)
date: 2026-11-14
issue: IronbellyOrg/IronClaude#546
scope: version 1, enforce the requested or defined model; no model-quality or cost routing
status: brainstorm output, not yet a design document
sources: proposal A (sonnet), B (haiku), C (sonnet); adversarial debate 2 rounds
---

# Version 1 model-policy hook: merged design

Tags. "Docs B1 to B9" are the Claude Code documentation facts in `enrichment/codebase-context.md` section B (read through context7 earlier, not re-read here): B1 PreToolUse input fields; B2 exit 2 blocks, stderr goes to Claude; B3 UserPromptSubmit can block with JSON; B4 SessionStart `model` is optional, SubagentStart has no model; B5 Agent model resolution order; B6 `--model`, alias env, `modelOverrides`; B7 native `availableModels` and `deniedModels`; B8 `claude --bare` children run no hooks; B9 a non-zero exit other than 2 does not block. "Verified" means an advocate or the Step 1 diff analysis read the line during the debate. UNVERIFIED means no step read it; section 10 gives the cheapest check. Every file, rule and command name below is new; nothing here exists yet.

## 0. Recommendation

Ship one deterministic hook, one in-process launcher helper and a small detective check, all reading one JSON policy and containing no Jev call, starting in observe mode except for a literal forbidden model, which is enforced from day one.

Decisions settled in the debate (tag = winning proposal):

- Four layers, each with a requirement and a file, including the native floor and the detective check that A named but never specified (A for the layer table, C-001; the requirements come from this merge because C-025 had no winner).
- The helper emits the value it checked, and a repository test fails when a raw `--model` appears in an argv builder outside the helper (B, C-002, C-003).
- Tiers are roles (`judge`, `work`, `light`) with exact ids and no prefix match (C, C-004, C-005). Stages are `default` and `blind-scoring`, chosen by `SC_MODEL_STAGE`; a command prefix may only narrow the stage (A, C-006, X-013).
- Failure paths: a pure-bash prefilter fails closed for launch-shaped input in any session, the hook converts its own timeout to exit 2 (A, C-013, X-002, X-011), and a missing or malformed policy blocks calls that choose a model (B, X-001).
- Scripts: scan shell scripts one level deep, resolve one literal assignment, deny every other dynamic value (C, C-009); a second flat pass for nested strings and a block on oversize input (A, X-004, X-005, C-010).
- Agent calls without `model` follow the documented order, re-record the session model on `/model`, and block when the model is unknown (B, C-011, C-012).
- No Jev code in v1; promotion needs at least 50 labelled code misses and precision 0.95 (B, X-010, C-020; A, C-021).
- Rollout by event class with a 100-script-event gate and one-edit rollback (C, S-005, C-015); one grant file per grant with a typed `yes` from `/dev/tty`, 2 h default, 24 h maximum (C, C-018, C-019; A, X-008).

## 1. Events and visibility

### 1.1 The property and the layers

Property: a launch is allowed only if the model it names resolves to a tier that the session's stage allows. The hook never picks or rewrites a model: it allows, or blocks with a reason. A launch that names no model is blocked when the stage requires an explicit pin.

| Layer | Mechanism | Strength | Blind to |
|---|---|---|---|
| L0, native floor | `superclaude model-policy native-floor` prints a settings snippet with `deniedModels` (B7) for tiers no stage allows | Covers every in-process choice, including `/model` and frontmatter | Global and static: cannot say "Opus for blind scoring only"; lists concatenate unless managed (B7) |
| L1, hook | `enforce-model-policy.sh` on PreToolUse, UserPromptSubmit, SessionStart | Per-stage rules; reads command text, scripts, frontmatter; gives a reason | Python subprocesses, `--bare` children, `/model` unless the prompt event fires |
| L2, helper | `model_policy.py`: `resolve`, `check`, `build_flag`, `ModelPolicyError`; CLI `model-policy check` for shell launchers | Sees the Python launchers; the checked value is the used value | Code that does not call it |
| L3, detective | `model-policy verify-run <output.json>` compares the observed model with the expected set | Catches silent substitution after a headless run | Runs after the event; not a gate |

### 1.2 What a hook sees

| # | How the model is chosen | What a hook sees | Doc fact | What the design does | Cannot see |
|---|---|---|---|---|---|
| 1 | Bash `claude [-p] --model X`, `--model=X`, `--fallback-model X` | Yes, `tool_input.command` | B1, B6 | Tokenizer (wrappers skipped) plus flat pass 2 find flag values; resolve tier; decide | Words assembled from pieces; `claude` renamed in a shell rc |
| 2 | Bash `claude` with no `--model` | Command text and the hook's own env | B6 (order of `ANTHROPIC_MODEL` and settings `model` UNVERIFIED) | Blocked MP-NOT-PINNED when the stage sets `require_explicit_model`; `--version`, `--help`, `mcp`, `doctor`, `update`, `plugin` exempt | The effective default is not resolved (C-008, A) |
| 3 | `bash x.sh`, `./x.sh`, `source x.sh` | Path only | B1 | Read the shell script (one level, `script_max_kb` 256) and a named `.py`; scan literals outside comments | Script calling a script; file built at run time; change between check and run |
| 4 | `superclaude <sub> ... --model X` | Yes | B1 | Same check as row 1; the helper checks again inside | Subcommands that read a default (reflect: only the helper sees it) |
| 5 | Agent or Task `model` parameter (alias only) | Yes, `tool_input.model` | B5 | Resolve alias through the host env value; decide | A same-family alias that resolves to the main session model (B5) |
| 6 | Agent or Task with no `model` | Frontmatter file: yes. `CLAUDE_CODE_SUBAGENT_MODEL`: hook env only. Main model: SessionStart record only | B4, B5 | Order: frontmatter (`inherit` checks the record), env (FORCE set and not allowed blocks), record; an unknown record blocks when `inherit_check` is true | Main model after a silent switch (picker, `--fallback-model`) |
| 7 | Frontmatter `model:` in agents, skills, commands | Only at the Agent or Skill call | B5 | Read the file at call time; `lint` checks all shipped files in CI | In-process use with no tool call (L0 only) |
| 8 | Skill tool call; typed `/sc:x` | Skill: yes. Typed command: only if UserPromptSubmit fires (UNVERIFIED) | B1, B3 | Read frontmatter; JSON block for a command naming a forbidden model | Typed commands if the event does not fire |
| 9 | Env: `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL(_FORCE)` | Prefix or `export` in a command: yes. Settings `env`, harness: no | B6, B7 | Prefix assignments blocked MP-ENV-REDIRECT; settings writes are TAMPER | Harness-set values; `modelOverrides` (B6) |
| 10 | `/model` typed by a person | UNVERIFIED whether UserPromptSubmit fires | B3, B7 | If it fires: block a non-allowed model and re-record. Otherwise L0 and L3 only | A `/model` with no prompt event; the picker |
| 11 | Session's own model at start | SessionStart `model`, optional | B4 | Record it for row 6; write a `policy-unreadable` lock when the policy cannot be read | Field omitted (for example after `/clear`); later changes |
| 12 | Python launchers: five argv builders plus the `reflect` default | No (not a Bash call) | enrichment D | Helper `build_flag`; a repo test forces new launchers through it | Code that builds argv without the helper |
| 13 | Child sessions: `--bare`, per-eval HOME children | Launch command: yes. Child's inner events: no | B8 | Launch blocked for `--bare` or `--settings` in a non-elevated stage; parent-side helper check for eval children | Inner calls of `--bare` and eval children (no hooks loaded is an inference, UNVERIFIED); a child with no tool call |
| 14 | Monitor and Workflow tools | Monitor: `command`, yes. Workflow: input shape UNVERIFIED | enrichment C | Monitor as Bash; Workflow serialised input scanned for model literals | Workflow scripts built at run time |
| 15 | Orca and ccsession launches (`worktree create --agent`, `agent launch`, `worker-start`) | Command text only; names no model | none | Listed as uncovered; the profile default model is used | The model such a session runs (default of `ccsession-orca` UNVERIFIED) |
| 16 | Mods with `agent.spawn`, managed or harness settings, upgrades, gateway failover | No | B5 | L0 floor; L3 compares observed and expected | Everything chosen there; what the gateway serves behind an id |

Stated plainly, the design checks the requested name, not the served model. `modelOverrides`, harness-set `env` redirects, gateway failover (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` names other models behind each gateway id; verified by the invariant probe, INV-034), `--fallback-model` switches, a `/model` the prompt event does not report, inner calls of `--bare` and eval children, and Orca or ccsession launches are outside L1. L0 and L3 narrow that list; they do not close it (A-001, QUALIFY).

## 2. Machine-readable policy

### 2.1 Format, storage, loading

JSON, read by `jq` in the hook and `json` in the helper. Template `model-policy.json.example` is copied to `~/.claude/model-policy.json` only when absent, through the existing seed list (`install_hooks.py:104-106`; seeds are never overwritten, even with `--force`; verified in Step 1). The hook re-reads the layers on every model-bearing event with one `jq` call per file; the helper re-reads on every launch. No cache. The log records `policy_sha8`.

### 2.2 Complete example (`~/.claude/model-policy.json`)

```json
{
  "version": 1,
  "table_date": "2026-11-14",
  "mode": {"bash_claude": "observe", "bash_script": "observe", "agent": "observe",
           "skill": "observe", "prompt_command": "observe"},
  "enforce_always": ["literal_flag", "agent_param"],
  "tiers": {
    "judge": {"restricted": true, "aliases": ["opus"], "alias_env": "ANTHROPIC_DEFAULT_OPUS_MODEL",
              "ids": ["claude-opus-5-5", "claude-gw-tier1a"]},
    "work":  {"aliases": ["sonnet"], "alias_env": "ANTHROPIC_DEFAULT_SONNET_MODEL",
              "ids": ["claude-sonnet-5-5", "claude-gw-tier1b"]},
    "light": {"aliases": ["haiku"], "alias_env": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
              "ids": ["claude-haiku-5-5", "claude-gw-tier2"]},
    "fable": {"restricted": true, "aliases": ["fable"], "alias_env": "ANTHROPIC_DEFAULT_FABLE_MODEL",
              "ids": []}
  },
  "id_prefix_match": false,
  "observed_ok": {"claude-gw-tier1a": ["claude-opus-5-5", "claude-sonnet-5-5"]},
  "stages": {
    "default":       {"allow": ["work", "light"], "require_explicit_model": true, "inherit_check": true},
    "blind-scoring": {"allow": ["judge", "work", "light"], "require_explicit_model": true, "inherit_check": false}
  },
  "unknown_model": "deny",
  "dynamic_model": "deny",
  "env_redirect": "deny",
  "bare_or_settings_child": "deny",
  "script_max_kb": 256,
  "command_max_kb": 64,
  "grant_default_hours": 2,
  "grant_max_hours": 24
}
```

- `enforce_always` lists the zero-ambiguity cases blocked even while their class observes: a non-allowed tier written as a literal in a `--model` flag, and one in the Agent `model` parameter (all three advocates qualified A-003 this way). `blind-scoring` also allows `work` and `light` so a Sonnet helper inside it is not blocked (probe INV-024).
- `claude-gw-tier3` is not listed, so it is unmapped and denied; observe logs will flag `issue-worker-t3`. `fable` has no ids yet and no stage allows it.
- `observed_ok` is read only by L3. Its one entry is the failover set for gateway tier 1a as quoted by the probe. An id with no entry reports `UNKNOWN_EXPECTATION`. Whether the output JSON reports these id strings is UNVERIFIED.
- Tier names are roles, not families, because what the gateway runs behind each id is UNVERIFIED (C-005).

### 2.3 Canonical tiers versus ids and aliases on this host

| Tier | Alias | Alias env on this host (enrichment D) | Listed ids | Note |
|---|---|---|---|---|
| judge | opus | `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]` | `claude-opus-5-5`, `claude-gw-tier1a` | Restricted |
| work | sonnet | `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b[1m]` | `claude-sonnet-5-5`, `claude-gw-tier1b` | |
| light | haiku | `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]` | `claude-haiku-5-5`, `claude-gw-tier2` | The probe (INV-035) read the host defaults file: the haiku alias resolves to a GLM model there, so `light` means gateway tier 2, not necessarily Haiku |
| fable | fable | unset in the observations | none | Restricted |

Canonicalisation, one rule set for hook and helper:

1. Lower-case and strip a trailing `[...]` suffix. A variable that is set but empty counts as unset (probe INV-010: `ANTHROPIC_MODEL` is empty on this host).
2. For an alias word, take the tier's `alias_env` value when set and non-empty, strip its suffix, and continue with that value; if unset, use the alias list.
3. Exact match against `ids`. No prefix, no glob (`id_prefix_match: false`: an id entry also permits later versions, B7). An unlisted id is already denied, so globs add nothing on the deny side (C-004).
4. Otherwise unmapped: MP-UNMAPPED when `unknown_model` is `deny`.

A prefix that redefines an alias is blocked (MP-ENV-REDIRECT) before step 2, so the table cannot be poisoned from inside a command.

### 2.4 Scoping and precedence

Three layers (C, X-003): managed `/etc/superclaude/model-policy.json` (root-owned, so a same-user model cannot edit it; absent on this host, verified), project `<project root>/.superclaude/model-policy.json` (walk up from `cwd`, at most 8 levels; gitignored here, so per checkout, verified in Step 1), user `~/.claude/model-policy.json`.

Merge rule (A's "tighten only", extended per probe INV-021): `tiers`, `stages` and every other key come from the managed layer if it exists, else the user layer. A project file can only intersect a stage's `allow`, make a class mode stricter, or lower a numeric cap (`script_max_kb`, `command_max_kb`, `grant_max_hours`); every other project key is ignored with a log line. A test path override for the managed file (`SC_MODEL_POLICY_MANAGED`, read by the hook only) makes that layer testable without `/etc/superclaude`.

### 2.5 Stage and requested model

The stage comes from the hook's environment variable `SC_MODEL_STAGE`, set by whoever starts the session (a person, Orca) or by the helper for the children it starts. The name is new: `SC_MODEL_STAGE` and `SC_STAGE` appear 0 times under `src/` (verified by advocate C), so no session carries one today. An unknown, empty or mis-cased value means `default` and logs `stage_unknown` (probe INV-023).

- A command prefix `SC_MODEL_STAGE=x claude ...`, or the same assignment in a scanned script, may only narrow: the declared stage's `allow` must be a subset of the session stage's, otherwise MP-STAGE-WIDEN. A model cannot claim `blind-scoring` for itself (X-013, A).
- Elevation needs a human grant (section 4) or a session a person started in the wider stage. A grant can bind to a script's sha256 so the human reviews the exact script holding the Opus literal (A-004).
- Grant lookup runs before the widen rule, and a prefix naming exactly the stage a valid grant unlocks is accepted (probe INV-029).

### 2.6 Modes

Each event class has a mode: `bash_claude`, `bash_script` (script scans and pass 2), `agent`, `skill`, `prompt_command`. The effective mode is the strictest across layers. Observe logs `would_block` and exits 0. Always enforced, whatever the mode: the `enforce_always` cases, MP-TAMPER, MP-POLICY-BROKEN for a call that chooses a model, and MP-INTERNAL on launch-shaped input (probe INV-028; otherwise a model could edit the policy through the whole observe window). If the policy cannot be read, the mode cannot be read either, so model-choosing events are treated as enforce; that is the one case where observe does not protect (probe INV-004). Default scope is all sessions, seeded in observe (C-026, A): the incident sessions were ordinary ones.

### 2.7 Missing or malformed policy, per event

Valid means: `version` 1; `tiers` non-empty, each with an `ids` array; `stages.default` with a non-empty `allow` of known tiers; every stage tier known; valid mode values. `{}`, `allow: []`, no `default` stage and an unknown tier are malformed (probe INV-022). Missing and malformed are treated alike.

| Event | Missing or malformed policy |
|---|---|
| Bash or Monitor with a positively detected `claude` launch (pinned or not) | Block MP-POLICY-BROKEN; tell the person to fix `~/.claude/model-policy.json` (B, X-001, narrowed) |
| Other Bash | Allow |
| Agent or Task naming a model (parameter or frontmatter) | Block MP-POLICY-BROKEN |
| Agent or Task with no model | Allow, log `no_policy_inherit`. Stated ceiling: this is the incident's inherit path and stays open while the policy is unreadable |
| Skill with `model:` in its file | Block; a skill without `model:` is allowed |
| Workflow | Block when its serialised input contains a model literal |
| UserPromptSubmit | Block only `/model` and `/sc:` commands whose file names a model (JSON decision) |
| SessionStart | No block (B4); write `policy-unreadable`; later model-bearing calls in that session are blocked |
| Edit, Write, NotebookEdit | Allow; tamper patterns are compiled into the script and need no policy |
| Helper (Python) | Raise `ModelPolicyError`, spawn nothing, non-zero exit |
| Internal error (`jq` or `awk` missing, scanner failure, own timeout) | Fail closed only if the pure-bash prefilter saw the word `claude` or `superclaude`, an assignment to `ANTHROPIC_` or `CLAUDE_CODE_`, or an Agent or Task call with `model`; otherwise allow. The prefilter matches command words and assignments, not substrings, and Edit or Write payloads are checked only by path (probe INV-027) |

Reason: failing open everywhere leaves the incident path open (the Orca hook fails open without `jq`; the launch guard fails closed only for governed sessions; both verified). Failing closed everywhere would break every Bash call on a host without `jq` (A, C-013, X-002).

## 3. Where Jev adds value in v1 versus plain code

### 3.1 Honest conclusion

**v1 needs no Jev call.** Every v1 decision is over a literal the code can read, a file the code can read, or a value the code can classify as dynamic and deny. Jev sees the same text the code sees; for a value that comes from outside the text its honest answer is "cannot tell", and Jev can only add a block, never allow. Under a deny default for dynamic values it adds nothing (B, X-010). The hook makes no network call and does not reference Jev (REQ-59).

### 3.2 Code decides

Literal `--model` and `--model=` through any wrapper; alias or id to tier; the Agent `model` parameter and frontmatter; env redirects, `--bare`, `--settings`; one top-level literal assignment followed by `--model "$M"`; `$`, `$(...)` and backticks in the flag value (dynamic, denied); size caps; tamper paths; expired grants; malformed policy. C estimated that about 95 percent of launches fall here (an estimate, UNVERIFIED until the observe log exists).

### 3.3 Residue

| Class | Example | Handling |
|---|---|---|
| (a) Value built at run time | `--model "$1"`, an inherited env var, a file read, a table-driven array (the `SPECS` launcher of the redesign brainstorm) | Code blocks MP-DYNAMIC; allowed only by a grant bound to the script's sha256 or by rewriting to a literal. Jev would add nothing |
| (b) Launch in a file the hook cannot read | Deeper nesting, `uv run python x.py` that builds argv | Ceiling, not a judgment problem; Jev fails on multi-hop judgments over large input (enrichment E) |
| (c) Natural-language "use Opus" to a subagent | No model field is set | Not a model-selection event |

### 3.4 Measured-need rule and spike

Jev enters only if the offline replay (3.6) shows at least 50 labelled launches where code said ALLOW and the label says BLOCK, and a spike then reaches precision of at least 0.95 at p of at least 0.7 with at most 1 percent false blocks on the OK set (A, C-021; B's "any miss" trigger was too loose, and its class (b) trigger contradicted its own text). Given 3.1, Jev is expected to stay off.

If the spike runs, the narrow question is one Choice call (B, C-020), input capped at 2 KB:

- Q-J1: "This shell text starts a model-using process. Which best describes its model? (A) a tier the policy forbids for stage S, (B) a tier the policy allows for stage S, (C) cannot tell from the text."
- Option C is the "none" option: Jev flags 0 of 30 out-of-scope inputs unless one exists (enrichment E).
- Code adds a block only on answer A with p at least 0.7. Jev never allows. The forbidden list is passed as vocabulary only; policy stays in code.
- Only the redacted excerpt leaves the machine. Key `JEV_API_KEY` from env only; the endpoint setting is UNVERIFIED.

### 3.5 Thresholds, latency, cost, failure behaviour

| Number | Value | Reliability |
|---|---|---|
| Block threshold | p at least 0.7 | Design choice from the Jev note (enrichment E) |
| Promotion gate | 50 labelled misses; precision 0.95; 1 percent false blocks | Design choice, untested |
| Latency | 70 to 500 ms per call, reported | Company-adjacent; outside tests find vendor claims 5 to 6x smaller at the median (enrichment E); not measured for this task: low |
| Cost | about $0.000025 per call (2,011 pair calls, $0.051, 0 failed) | Measured once, on short pair inputs of another task: moderate for those inputs. A 2 KB excerpt may cost 2 to 5 times more (A's estimate, UNVERIFIED) |
| Call timeout | 1 s inside a 3 s registration, no retry | Design choice; the p15 adapter retries once and a hook cannot afford it |
| Hook latency | section 6 | Estimates, UNVERIFIED until REQ-60 and REQ-61 |

Failure behaviour per event (spike only; v1 makes no call): for a Bash or Monitor launch with a dynamic value, an unreachable Jev, 429, 5xx, timeout or bad key adds no block and the code result stands (code already denies). Agent, Task, Skill, UserPromptSubmit, SessionStart, Edit, Write and the helper never call Jev. A failed call is never an answer: Jev only adds, so its absence must equal the code default.

### 3.6 Offline test plan on labelled historical calls

Data sources (counts are from searches in the earlier session):

1. Launcher scripts under `.dev/` with a literal `--model`: 17 files contain the Opus literal (C's search), 20 contain any literal (B's search); recount at step 1. Named by the proposals: `launch-implement.sh:18` and `launch-designs.sh:22` (Opus, violations), `launch-slack.sh:31` and `launch-override.sh:27` (Sonnet, compliant), `launch-implement-2.sh:8,28` (single variable), `launch-variants.sh` (table-driven), `run-proposals.sh:17` (function argument). Their line numbers are UNVERIFIED: the debate did not open `.dev/eval-workspaces/`.
2. Session transcripts under `~/.claude/projects/-home-coder-workspaces-IronClaude/`: 503 `*.jsonl` files (B's glob); `--model` appears 470 times in 94 files, including discussion text. Keep only `tool_use` inputs of Bash, Agent, Skill, Workflow, Monitor. The record's model key is UNVERIFIED: read one raw line first.
3. Output JSON of headless runs with `.message.model` and `modelUsage` (named by A at `launch-variants.sh:35-36`; key names UNVERIFIED by the debate).
4. The five argv builders in dry-run mode, and the issue's violation list (enrichment A) as known positives.

Labelling (A, C-022, with B's controls): ground truth is the observed model in the run's output JSON, mapped to a tier by the policy table; VIOLATION if outside the stage's allow list, else OK. Join a launch to its output file by the redirect path on the same line; hand-label cases with no output file. The author labels all cases, a second reader labels a random 20 percent from the written rule only, disagreements change the written rule first, and labels are frozen before the hook runs. Synthetic mutants (`M=...; --model "$M"`, `"${M:-...}"`, `bash -c`, heredoc, array) are labelled by construction and reported separately.

Replay: a script in `tests/hooks/` feeds each recorded `tool_input` with its recorded `cwd` on stdin; no network, no `claude` process. Frontmatter comes from a frozen copy of the agent and skill trees (mapping a transcript date to a commit is UNVERIFIED; if it fails the report says the current tree was used). Output: a confusion matrix per event type and a list of misses. Metrics: literal and single-assignment cases 100 percent recall and no false block on OK scripts; dynamic cases as precision and recall; read-only mentions (grep, echo, commit text) zero false blocks; Jev AUC and precision at p of at least 0.7 over the residue only, and not enabled below 50 labelled items.

## 4. Rejection and override

### 4.1 Message the model sees (stderr, exit 2)

Shape from `launch-level-guard.sh:126` (`Blocked:` / `Why:` / `You can:`). The text is built from variables at run time; shipped scripts hold no model-id literal (REQ-58).

```
Model policy: blocked [MP-FORBIDDEN-TIER] (event ev-20261114T135012-9f3a)
Blocked: claude -p --model claude-opus-5-5 resolves to tier judge on this host.
Why: stage "default" allows tiers work, light (policy ~/.claude/model-policy.json, stages.default.allow). The requested model must be the model used, and this one is not allowed here. Do not edit the policy, the grants or the hook.
You can: re-run with a model from an allowed tier, for example --model sonnet (the hook never changes the model for you). For an approved run of a restricted tier, ask the person to run in their own terminal: superclaude model-policy allow --stage blind-scoring --for 2h --reason "<why>"
```

Rule ids: MP-FORBIDDEN-TIER, MP-UNMAPPED, MP-NOT-PINNED, MP-INHERIT, MP-DYNAMIC, MP-ENV-REDIRECT, MP-ESCAPE-FLAG (`--bare`, `--settings`), MP-STAGE-WIDEN, MP-SCRIPT-UNREADABLE, MP-BIG, MP-TAMPER, MP-POLICY-BROKEN, MP-INTERNAL. The event id ties a block to its log row (A, C-017).

### 4.2 Exit codes and output

| Event | Result |
|---|---|
| PreToolUse block | Exit 2, message on stderr (B2). Never exit 1 (non-blocking, B9) |
| UserPromptSubmit block | Exit 0 and `{"decision":"block","reason":"..."}` on stdout; the reason is shown to the user (B3). Exit 2 for a prompt is UNVERIFIED against the docs |
| SessionStart | Exit 0 always; records state |
| Observe | Exit 0, one `would_block` line |
| Helper | `ModelPolicyError`, no spawn; CLI `model-policy check`: 0 allow, 2 deny, 1 usage error |

### 4.3 What the user sees

Claude Code shows the blocked call; whether hook stderr is shown to the user is UNVERIFIED. The same facts go to `~/.claude/state/model-policy/decisions.jsonl` (A, C-016): `ts, sid, event, tool, stage, class, mode, decision, rule, model_raw, tier, origin, policy_sha8, grant_id, ms`. `origin` is `hook` or `helper`, so a gate counts hook events once (probe INV-030). Raw command text is never logged, only the extracted model tokens (C, U-016). `superclaude model-policy log --tail 20` prints it.

### 4.4 Human override record

One file per grant, `~/.claude/state/model-policy/grants/<id>.json` (C, C-018):

```json
{"id": "g-20261114T140000-3b7e", "created_at": "2026-11-14T14:00:00Z",
 "expires_at": "2026-11-14T16:00:00Z", "expires_epoch": 1794672000,
 "stage": "blind-scoring", "allow": ["judge"],
 "scope": {"script_sha256": "<64 hex characters>"},
 "reason": "owner-approved blind scoring run", "created_by": "human-tty", "uid": 1000}
```

- Scope is one of `session_id`, a `cwd` glob, `script_sha256` or `command_sha256`. Expiry is required: default 2 h, maximum 24 h (A, X-008). The hook compares the integer `expires_epoch`, reads grants only when it is about to block, and reads at most the newest 50 files.
- Created only by `superclaude model-policy allow ... --for <dur> --reason <text>` (name from A, X-006). It refuses unless stdin is a TTY and reads a typed `yes` from `/dev/tty` (C, C-019). It does not rely on `CLAUDECODE`: `pipeline/process.py:178-180` removes it from launcher children (verified), and the Bash tool had no TTY when observed once on this host (X-014, A).
- `list` shows grants; `revoke` deletes one file. Each use writes `grant_id` to the decision log, and grant frequency is counted because the premise that Opus runs are rare is UNVERIFIED (A-004).
- Against self-creation: any Bash or Monitor text naming `model-policy allow`, or any Edit, Write, NotebookEdit or Bash write touching the policy, the grants, the state directory, `settings*`, the hook or `install_hooks`, is MP-TAMPER and always enforced (A, C-014; precedent `launch-level-guard.sh:94-97, 706`).
- Ceiling: a same-user process with a pty, or a write the hook does not see, can still forge a grant or edit the policy. Only the managed layer protects the policy from that, and it does not protect grants. A run longer than its grant fails at its next launch; the maximum is 24 h (probe INV-006, open).

## 5. Bypass resistance

The scanner runs two passes. Pass 1 is the structured tokenizer, copied from `require-orca-worktree-agent.sh` because installed hooks are standalone, with a parity test. Pass 2 is a flat over-approximate scan that can only add blocks. It runs only when the command contains a nesting construct (`bash -c`, `sh -c`, `eval`, `ssh`, `xargs`, `find -exec`, a heredoc piped to a shell) and the word `claude` or `superclaude`, so a `grep`, `echo` or commit text that mentions a launch passes (probe INV-009). Its false-block rate is UNVERIFIED, so it starts in observe under `bash_script`.

| Vector | Result | Note |
|---|---|---|
| Wrappers `sudo`, `env`, `nohup`, `timeout`, `time`, `command`, `exec` | Blocked | Skipped by the tokenizer |
| `bash -c`, `sh -c`, `eval`, `ssh host '...'`, `xargs`, `find -exec`, heredoc piped to a shell | Blocked | Pass 2; the Orca hook lists these as ceilings (`:39-45`) |
| Heredoc writing a script, then running it in the same command | Blocked | The body is in the command text |
| Script written by Write, then `bash x.sh` | Blocked at run time | Ceiling: file changed between check and run |
| Script sourcing another, or generating the flag from a downloaded file | Ceiling | L3 detects after the run |
| Command over 64 KB, script over `script_max_kb` | Blocked MP-BIG | Command cap only for launch-shaped commands; an oversize script is decided by a streaming grep for launch-shaped words (this merge, probe INV-016) |
| `--model "$M"`, `$(...)`, backticks, assembled words in the flag | Resolved only for one top-level literal assignment; else blocked MP-DYNAMIC | Table-driven launchers are blocked until pinned or granted. Words assembled into `claude` itself: ceiling |
| Env prefix or `export` of the redirect variables | Blocked MP-ENV-REDIRECT | Settings `env` and harness values: settings writes are TAMPER, harness values L0 only |
| `--settings` with `model`, `availableModels` or `env`; `--bare` | Blocked MP-ESCAPE-FLAG | Inner events of a `--bare` child: ceiling |
| `--fallback-model` | Value checked like `--model` | `--agents` and `--agent`: model key UNVERIFIED, section 10 |
| Tampering: policy, grants, state dir, `settings*`, hook, `disableAllHooks`, `install_hooks` | Blocked MP-TAMPER, always | Same-user pty: ceiling. Editing settings by Bash: ceiling |
| Python script that spawns `claude` | Named file: flat scan. Five package builders: helper | Fully dynamic Python: L0 and L3 only |
| Monitor; subagents | Blocked | Same scanner; PreToolUse fires inside subagents (`require-orca-worktree-agent.sh:5-6`, verified) |
| Workflow, MCP tools, mods | Workflow: scanned (shape UNVERIFIED). MCP and mods: ceiling | |
| `/model` by a person | Blocked if the prompt event fires; else ceiling | |
| Eval children (per-eval HOME) | Launch checked in the parent; inner calls ceiling | `claude_process.py:238-241` verified: the isolated HOME wins in the child env (A-002, REJECT of "every child sees the operator's hooks") |
| Gateway failover, `modelOverrides`; a child with no tool call | Ceiling | L3 compares observed and expected; only the parent launch is checked |
| Prompt text saying "use opus" | Out of scope | Policy is the written intent |

## 6. Time cost per event

All numbers are estimates from A and B, not measured on this host (UNVERIFIED until REQ-60 and REQ-61). What the platform does when a hook times out is UNVERIFIED (B9 covers only non-zero exits other than 2), so the hook runs its own `timeout` and converts expiry to exit 2 for launch-shaped input; that is safe either way (X-011, A). The internal limit is the registration timeout minus 1 s, and 0.5 s for the 1 s registration (probe INV-015).

| Event | Typical ms | Worst ms | Registration timeout | Internal limit |
|---|---|---|---|---|
| Bash, not a launch (prefilter exit) | 10 to 25 | 80 | 3 s | 2 s |
| Bash `claude` literal | 25 to 45 | 120 | 3 s | 2 s |
| Bash running a script (scan up to 256 KB) | 40 to 90 | 400 | 3 s | 2 s |
| Agent or Task with `model` | 15 to 30 | 80 | 3 s | 2 s |
| Agent or Task without `model` | 25 to 50 | 120 | 3 s | 2 s |
| Skill; Monitor; Workflow | 20 to 40 | 100 | 3 s | 2 s |
| Edit, Write, NotebookEdit (tamper path check) | 5 to 20 | 60 | 1 s | 0.5 s |
| UserPromptSubmit; SessionStart | 10 to 30 | 80 | 3 s | 2 s |
| Helper per launch (in-process) | 5 | 30 | none | none |
| Jev spike (not in v1) | 150 to 600 | 2,000 | none | 1 s call timeout |

Bash already runs four PreToolUse registrations (`hooks.json:96, 106, 116, 126`); this hook is a fifth process on every Bash call, so the non-matching path is the cost that matters (REQ-60: p95 at most 50 ms over 200 runs, automated; X-012, C).

## 7. Test plan and requirements

### 7.1 Test plan

- Tests live in `tests/hooks/` and `tests/cli/` (pytest, `uv run pytest tests/hooks/ -v`). Method: replay JSON fixtures on stdin and assert exit code and stderr, as the existing guard tests do (`test_launch_level_guard*.py`, `test_require_orca_worktree_agent*.py`).
- One shared `tests/hooks/fixtures/model_policy/vectors.json` runs against both hook and helper so they cannot drift (REQ-48). The labelled replay corpus of 3.6 lives in the same directory and is replayed in CI.
- Methods: [unit], [integration], [fixture replay], [parity], [manual] (B, S-003).
- Dropped because the debate rejected them: closed-world scan, allow on an unknown session model, the manual 100 ms and 150 ms benchmark, dormant or shadow Jev, allow on a missing policy, allow on an oversize script, fail-open without `jq`, inline non-human stage, the `CLAUDECODE` guard, the hash-chained journal.

### 7.2 Requirements

- REQ-01: In stage `default` with `bash_claude` set to enforce, `claude -p --model <id of tier judge>` exits 2 and names MP-FORBIDDEN-TIER. [unit]
- REQ-02: The same command with an allowed tier, and with the `--model=<value>` form, exits 0. [unit]
- REQ-03: `--model opus` resolves to the tier of `ANTHROPIC_DEFAULT_OPUS_MODEL` when that is set and non-empty, and to the alias list when it is unset or empty. [unit]
- REQ-04: A `[1m]` suffix and upper case resolve like the plain id; an unlisted id (including a newer id of a listed family) is MP-UNMAPPED even in `blind-scoring`; an alias env value found in no tier's `ids` is unmapped. [unit]
- REQ-05: `claude -p` with no `--model` exits 2 MP-NOT-PINNED when `require_explicit_model` is true; `claude --version`, `--help`, `mcp`, `doctor`, `update`, `plugin` exit 0. [unit]
- REQ-06: Wrappers (`sudo`, `env`, `nohup`, `timeout`, `time`, `command`, `exec`) do not hide a launch. [unit]
- REQ-07: `bash -c`, `sh -c`, `eval`, `ssh h '...'`, `xargs claude`, `find -exec` and a heredoc piped to a shell, each holding a launch of a non-allowed tier, exit 2 through pass 2. [unit]
- REQ-08: `grep`, `echo`, `git commit -m` and `gh issue create --body` commands that only mention `claude --model <judge id>` exit 0. [unit]
- REQ-09: `superclaude sprint run x --model <judge id>` is checked like `claude`. [unit]
- REQ-10: A `--fallback-model` value is checked like `--model`. [unit]
- REQ-11: `bash launch-implement.sh` (fixture copy of an incident script with a literal Opus id) exits 2; a fixture with only allowed literals exits 0. [fixture replay]
- REQ-12: A script with one top-level literal `M=<allowed id>` on a line before `--model "$M"` exits 0; with a judge id it exits 2; an assignment using `${`, `$(`, `export` or a second assignment is dynamic. [unit]
- REQ-13: A `--model` value from `"$1"`, an inherited env var, a file read, an array loop or a substitution exits 2 MP-DYNAMIC; the same script passes with a valid `script_sha256` grant. [unit]
- REQ-14: Comments are stripped before the literal scan: a judge id only in a comment passes, and a usage comment holding a full launch line does not block. [unit]
- REQ-15: A `.py` file named in the command is scanned flat for model literals. [unit]
- REQ-16: Sizes count bytes with KB = 1024: a launch-shaped command of 65536 bytes passes the size rule and 65537 bytes exits 2 MP-BIG; a non-launch command of 100 KB passes; a script of 262144 bytes is scanned and one of 262145 bytes is decided by the streaming grep (match: MP-BIG; no match: allow). [unit]
- REQ-17: An `SC_MODEL_STAGE=` assignment inside a scanned script follows the narrow-only rule. [unit]
- REQ-18: Agent `model: "opus"` in `default` exits 2; `model: "sonnet"` exits 0. [unit]
- REQ-19: Agent with no `model` uses the named agent's frontmatter first (`opus` exits 2, `sonnet` exits 0); frontmatter `inherit` checks the session record. [fixture replay]
- REQ-20: With no `model` and no frontmatter, `CLAUDE_CODE_SUBAGENT_MODEL` is next (empty counts as unset), then the SessionStart record; with `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` set and a non-allowed value in the hook env the call exits 2. [unit]
- REQ-21: With `inherit_check` true and no or unknown session record the call exits 2 MP-INHERIT and logs `no_session_model`; with `inherit_check` false it exits 0. [unit]
- REQ-22: A Skill whose SKILL.md names a non-allowed model exits 2; a skill without `model:` exits 0. [unit]
- REQ-23: A prompt `/sc:<cmd>` whose command file names a non-allowed model returns `{"decision":"block","reason":...}` with exit 0. [unit]
- REQ-24: A prompt `/model <non-allowed>` returns a block decision, and any `/model` prompt re-records the session model. [unit]
- REQ-25: A person types `/model` and a `/sc:` command in a throwaway session with a logging hook; the report records whether UserPromptSubmit fired for each. [manual]
- REQ-26: SessionStart records the reported model; with an unreadable policy it writes `policy-unreadable`, and later model-bearing calls in that session exit 2. [integration]
- REQ-27: A prefix or `export` of `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL(_FORCE)` or `ANTHROPIC_BASE_URL` exits 2 MP-ENV-REDIRECT. [unit]
- REQ-28: `--bare`, or `--settings` carrying `model`, `availableModels` or `env`, in a launch of a non-elevated stage exits 2 MP-ESCAPE-FLAG. [unit]
- REQ-29: An unknown, empty or mis-cased `SC_MODEL_STAGE` maps to `default` and logs `stage_unknown`. [unit]
- REQ-30: A prefix stage wider than the session stage exits 2 MP-STAGE-WIDEN; a prefix naming exactly the stage a valid grant unlocks is accepted. [unit]
- REQ-31: Merge: tiers and caps come from managed else user; a project file only intersects `allow`, strengthens a mode or lowers a cap; any other project key is ignored. [unit]
- REQ-32: A managed policy at the test path override beats a more permissive user file. [unit]
- REQ-33: `{}`, `stages: {}`, no `default` stage, `allow: []`, a stage naming an unknown tier, a tier with no `ids` array, an invalid mode and `version` other than 1 are MP-POLICY-BROKEN. [unit]
- REQ-34: With no readable policy, a `claude` launch and an Agent call naming a model exit 2, `ls` exits 0, and an Agent call with no model exits 0 and logs `no_policy_inherit`. [unit]
- REQ-35: In an observe class, rule decisions exit 0 and log `would_block`; the `enforce_always` cases, MP-TAMPER, MP-POLICY-BROKEN and MP-INTERNAL exit 2 in observe. [unit]
- REQ-36: Flipping one class to enforce changes only that class, and flipping it back needs no reinstall. [unit]
- REQ-37: With `jq` removed from PATH, a launch-shaped Bash command exits 2 MP-INTERNAL, while `ls` and an Edit on a path containing `/.claude/` exit 0. [integration]
- REQ-38: For every registration in `hooks.json` the internal timeout is at most the registration timeout minus 1 s (0.5 s for a 1 s registration), and expiry on launch-shaped input exits 2. [unit]
- REQ-39: The hook never exits 1, never emits `updatedInput`, and writes JSON only for UserPromptSubmit. [unit]
- REQ-40: Every block message has `Blocked:`, `Why:`, `You can:`, the rule id, the event id, the resolved tier, the policy path and key, and the "do not edit" line, and names no `src/superclaude/` path. [unit]
- REQ-41: Every decision appends one line with the fields of 4.3, and the file never holds raw command text. [unit]
- REQ-42: `model-policy allow` refuses without a TTY and requires a typed `yes` read from `/dev/tty`. [integration]
- REQ-43: A valid grant passes only its scope; an expired one is ignored; a changed `script_sha256` fails; 24 h is accepted while 24 h plus 1 s, zero and negative are refused; `revoke` deletes the file; at most the newest 50 files are read. [unit]
- REQ-44: Edit, Write, NotebookEdit, and Bash redirect, `tee`, `sed -i`, `rm`, `mv` or `cp` naming the policy, grants, state directory, `settings*`, the hook, `install_hooks` or `disableAllHooks`, and Bash naming `model-policy allow`, exit 2 MP-TAMPER in every mode. [unit]
- REQ-45: `build_flag` returns the flag value it checked, and each of the five argv builders refuses a non-allowed model before spawning. [integration]
- REQ-46: A repository test fails if a literal `"--model"` appears in an argv builder outside the helper module. [unit]
- REQ-47: The `reflect` default model goes through `build_flag`. [unit]
- REQ-48: Hook and helper return identical decisions for every case in `vectors.json`. [parity]
- REQ-49: The helper re-reads the policy on each launch: a mode flip inside a loop is seen. [unit]
- REQ-50: The helper with no policy raises `ModelPolicyError` and spawns nothing; tests and CI pass an explicit `policy_path`. [unit]
- REQ-51: `model-policy native-floor` prints settings JSON with `deniedModels` listing the ids of tiers no stage allows (`--restricted`: all restricted tiers), and never `availableModels`. [unit]
- REQ-52: `model-policy verify-run <output.json>` compares the observed model with `observed_ok` for the requested id, prints OK, MISMATCH or UNKNOWN_EXPECTATION, and appends a decision line. [unit]
- REQ-53: `model-policy lint` fails when a shipped agent, skill or command `model:` is outside the policy; `--live` warns when an alias env value is in no tier's `ids`. [unit]
- REQ-54: Install copies the script, merges one script across four registrations once, seeds the policy only when absent, and a `--force` reinstall keeps an edited policy. [integration]
- REQ-55: `hooks.json` holds the registrations and timeouts of section 8. [unit]
- REQ-56: `make verify-sync` passes after `make sync-dev` and fails if the script is missing from `_FRESHNESS_SCRIPTS`. [integration]
- REQ-57: `git status` shows no staged `.claude/` path other than `settings.json`. [manual]
- REQ-58: The shipped script and module hold no `claude-opus-`, `claude-sonnet-` or `claude-gw-tier` literal outside the policy template, and the existing literal-check tests pass (they scan `cli`, `hooks`, `core`, per `docs/reference/model-aliases.md:10-12`). [integration]
- REQ-59: The hook makes no network call and does not reference Jev. [unit]
- REQ-60: The non-matching Bash path has p95 at most 50 ms over 200 runs. [integration]
- REQ-61: Launch, script-scan and Agent path timings are measured on this host and recorded in the test report; they set the final timeouts. [manual]
- REQ-62: On the labelled replay no BLOCK-labelled case is allowed in enforce mode and no `static` or `not-a-launch` case is denied. [fixture replay]
- REQ-63: A Workflow input fixture, captured from one real call at step 1, containing a non-allowed model literal exits 2. [fixture replay]

## 8. Implementation plan in the IronClaude layout

### 8.1 Files

Add:

- `src/superclaude/hooks/scripts/enforce-model-policy.sh`: one script dispatching on `hook_event_name`; tokenizer copied from `require-orca-worktree-agent.sh`; names only `~/.claude/...` paths.
- `src/superclaude/hooks/model-policy.json.example`: the template of 2.2, placed beside the existing seed example for `auggie-projects.txt` (its directory is UNVERIFIED; use the same one).
- `src/superclaude/cli/model_policy.py`: loader, `resolve`, `check`, `build_flag`, `ModelPolicyError`, and the click group `model-policy` with `check`, `allow`, `list`, `revoke`, `log`, `lint`, `native-floor`, `verify-run`. The file that registers the group is not verified.
- Tests: `tests/hooks/test_enforce_model_policy.py` (events), `..._policy.py` (precedence, malformed), `..._grants.py`, `..._install.py`, `..._replay.py`, `tests/cli/test_model_policy.py`, and `tests/hooks/fixtures/model_policy/` (`vectors.json`, replay corpus).

Change:

- `src/superclaude/hooks/hooks.json`, appended:

```json
"PreToolUse": [
  {"matcher": "^(Bash|Monitor|Agent|Task|Skill|Workflow)$",
   "hooks": [{"type": "command", "command": "~/.claude/hooks/enforce-model-policy.sh", "timeout": 3}]},
  {"matcher": "^(Edit|Write|NotebookEdit)$",
   "hooks": [{"type": "command", "command": "~/.claude/hooks/enforce-model-policy.sh", "timeout": 1}]}
],
"UserPromptSubmit": [
  {"hooks": [{"type": "command", "command": "~/.claude/hooks/enforce-model-policy.sh", "timeout": 3}]}
],
"SessionStart": [
  {"matcher": "*", "hooks": [{"type": "command", "command": "~/.claude/hooks/enforce-model-policy.sh", "timeout": 3}]}
]
```

  Edit and Write already run `freshness-pre-edit.sh` at 1 s, and the existing wide matcher lists NotebookEdit, Monitor and Workflow (`hooks.json:86-91, 115-123`, verified), so the split follows precedent (B, C-023).
- `src/superclaude/cli/install_hooks.py`: add `"enforce-model-policy.sh"` to `_FRESHNESS_SCRIPTS` (list at `:42`; the comment near `:64` requires every `hooks/scripts/*.sh` to be a member) and `("model-policy.json.example", "model-policy.json")` to `_SEED_FILES` (`:104`). How the ownership merge handles one command in four registrations is UNVERIFIED (B says it matches by command path); REQ-54 covers it.
- The five argv sites (`pipeline/process.py:163-164`, `sprint/tmux.py:194`, `prd/models.py:283`, `sprint/summarizer.py:330`, `reflect/runner.py:508`) and the `reflect/commands.py:365` default: route through `build_flag`. `eval/claude_process.py` builds `ClaudeProcess(model=...)` in the parent, so the argv-site check covers it.
- `tests/cli/test_install_hooks.py` and `tests/cli/test_verify_sync_hooks.py`: extend for the new script and seed.

### 8.2 Sync and ownership rules

Edit only under `src/superclaude/`. `make sync-dev` copies `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/` and sets the execute bit (`Makefile:136-143`); `make verify-sync` diffs them (`:254-263`) and requires every script to be in `_FRESHNESS_SCRIPTS` (`:306-326`). Never edit `.claude/` by hand and never stage a `.claude/` path other than `settings.json`. Installed script text and messages name `~/.claude/...` paths and the `superclaude` CLI, never `src/superclaude/`. `src/superclaude/hooks/README.md` is stale (it still says to edit `plugins/superclaude/hooks/`); do not rely on it and do not change it in this work. Python runs through `uv`.

### 8.3 Order of work (8 steps)

1. Spike the open facts of section 10 that block design (transcript model key, one output JSON, one Workflow input, prompt event for `/model`, hook env). Then fix the policy schema, the template and `vectors.json`.
2. `model_policy.py`: resolver, `build_flag`, `lint`, `native-floor`, `verify-run`, with unit tests against the vectors.
3. Route the five argv sites and the reflect default through `build_flag`; add the REQ-46 repository test.
4. Hook, Bash and Monitor path: prefilter, tokenizer, pass 2, env and escape rules, decision, log, message, modes, TAMPER.
5. Hook, Agent, Skill, Workflow, UserPromptSubmit and SessionStart paths; script scan and the single-assignment resolver.
6. Grant CLI (`allow`, `list`, `revoke`, `log`, `check`) and grant reading.
7. Wiring (`hooks.json`, `install_hooks.py`, seed, `make sync-dev`, `make verify-sync`); replay harness, labelled corpus, latency (REQ-60, REQ-61, REQ-62).
8. Roll out as below.

### 8.4 Rollout (observe, then enforce)

Owner: the owner of issue #546 flips each class by editing the user policy and writes the date of each flip in the issue (C, S-005, C-015; A-003 was qualified by all three advocates: a named owner, exit evidence, and day-one enforcement of the zero-ambiguity cases). The durations below are this merge's numbers, not debate results.

| Stage | Enforced | Exit evidence for the next stage |
|---|---|---|
| Day one | `enforce_always` cases, MP-TAMPER, MP-POLICY-BROKEN, MP-INTERNAL; everything else observes | Install verified (REQ-54); first decision rows logged |
| Review, 7 days after install | none new | Every `would_block` row is classed as a true violation, a fixed false positive, or an accepted case with a grant. Day-one flags: `auggie-reviewer` and `eval-suite-author` (frontmatter Opus), `issue-worker-t1` (gateway tier 1a), `issue-worker-t3` (unmapped), the reflect default |
| Enforce 1 | `bash_claude`, `agent` | Zero unexplained false positives over 7 days |
| Enforce 2 | `skill`, `prompt_command` | One more week clean |
| Enforce 3 | `bash_script` (script scan, pass 2) | At least 100 script events and zero unexplained false positives; if 100 is not reached in 4 weeks the owner decides in writing |
| Rollback | Set a class to `observe` in the user policy; no reinstall | The always-enforced rules cannot be rolled back this way |

## 9. Room for version 2

- A `routing: dynamic` field in agent, skill or command frontmatter exempts that item from the fixed-model check only if it names a `router:`; v1 treats it as unpinned (B, C-024).
- Each stage gains a `candidates` list. The router's output is a request: the hook checks it against the same `allow` list, so v1 still bounds it.
- The decision log keeps a `routing` field, null in v1 (A).
- v1 never rewrites a model; v2 may use `updatedInput` only under an explicit mode (C).
- Jev returns only as a Choice router under the same block-only rule; the v1 replay corpus becomes the v2 evaluation set.
- Quality and cost judgment stays out of v1: no scoring of "best model" anywhere.

## 10. Risks and open questions

Risks that remain after the design:

- A same-user model with a pty can forge a grant or edit the policy; only the managed layer helps, and it is absent here.
- While the policy is unreadable, an Agent call with no model passes (the incident's inherit path).
- Two implementations (bash and Python) can drift; REQ-46 and REQ-48 are the controls.
- A mid-session `/model` the prompt event does not report leaves the session record stale (probe INV-002). The seeded tier table can drift after the seed is written (probe INV-003); `lint --live` warns. A grant shorter than a run fails mid-run (probe INV-006).

UNVERIFIED items that no debate step verified, with the cheapest check:

| Item | Cheapest check |
|---|---|
| UserPromptSubmit fires for `/model` and typed `/sc:` commands | REQ-25: a logging hook in a throwaway session |
| Hook env equals session env (alias values, `SC_MODEL_STAGE`) | A throwaway hook dumps `ANTHROPIC_*`; compare with `printenv` in the same session |
| Platform behaviour when a hook times out | A throwaway hook that sleeps past its timeout |
| Exit 2 blocks a UserPromptSubmit prompt (design uses the JSON form of B3) | Same throwaway session |
| Hook stderr is shown to the user | Watch one blocked call in the terminal |
| The Bash tool never has a TTY (observed once on this host) | Run a TTY test several times through Bash and Monitor |
| Transcript model key; transcript date to commit mapping | Read one raw transcript line (step 1) |
| Output JSON keys `.message.model`, `modelUsage` | Read one `session.json` |
| Incident script line numbers; 17 versus 20 launcher counts | Re-grep and read the scripts at step 1 |
| Workflow tool input shape | Capture one real call (REQ-63) |
| What the gateway serves behind each id, including `claude-gw-tier3` | One headless call per gateway id, then `verify-run` |
| `availableModels` or `deniedModels` injected per child through `--settings`, additive | One throwaway headless run with the flag and a forbidden `--model` |
| `/etc/superclaude` can be deployed (absent here) | Ask the host owner; test with the path override (REQ-32) |
| False-block rates of pass 2 and the script scan | The observe log, under `bash_script` |
| All latency estimates (section 6) | REQ-60 and REQ-61 |
| Jev endpoint, 2 KB cost, latency on this task | Only if the 3.4 gate is met |
| Installer merge of one command across four registrations | REQ-54 |
| File that registers the `model-policy` click group; directory of the existing seed example | Read the CLI entry and `install_hooks.py:100-106` at step 1 |
| Existing literal-check tests scan `.json.example` | Run them with the template present (REQ-58) |
| `modelOverrides` effect; model key inside `--agents`; which repeated `--model` wins | Read the docs page; one throwaway call each |
| An eval child loads no operator hooks (inference from the HOME override) | One eval run with a logging hook |
| Default model of `ccsession-orca` launches | Read the ccsession profile list (`MODEL-TIERS.md:39`) and watch one launch |
| Whether `reflect` gets a `--model` option so its only override is not blocked (probe INV-031) | Owner decision at step 3; until then the reflect default Opus is flagged in observe |
| Rollout durations of 8.4 (7 days, 100 events, 4 weeks) | Owner confirms or edits them when opening the rollout issue |

## 11. Provenance

From `debate/tally-round2.json` (votes in the order A, B, C advocates; all 50 points agreed). The 25 most consequential points:

| Point | Topic | Votes | Winner |
|---|---|---|---|
| C-001 | Enforcement layers | A, B, A | A |
| C-002 | Python launcher coverage | B, B, B | B |
| C-003 | Guard new launchers | B, B, B | B |
| C-004 | Id and alias canonicalisation | C, C, C | C |
| C-005 | Tier vocabulary | C, C, C | C |
| C-006 | Stage and seeded stages | A, A, A | A |
| C-007 | Observe and enforce granularity | C, C, C | C |
| C-008 | `claude` with no `--model` | A, A, A | A |
| C-009 | Run-time `--model` value | C, C, C | C |
| C-011 | Agent call without `model` | B, B, B | B |
| C-013 | Internal-error handling | A, A, A | A |
| C-015 | Rollout order and rollback | C, C, C | C |
| C-018 | Override record design | C, C, C | C |
| C-021 | Gate to promote Jev | A, A, A | A |
| C-025 | Native `availableModels` floor | NONE, NONE, NONE | NONE (resolved by this merge: generator only, REQ-51) |
| X-001 | Policy file missing | B, B, B | B |
| X-002 | `jq` or `awk` missing | A, A, A | A |
| X-004 | Nested launches | A, A, A | A (narrowed by this merge, REQ-08) |
| X-005 | Oversize script or command | A, A, A | A |
| X-010 | Jev code in the v1 deliverable | B, B, B | B |
| X-013 | Stage named in a command text | A, A, A | A |
| A-001 | Name equals served model | QUALIFY, QUALIFY, QUALIFY | QUALIFY |
| A-002 | Every child sees operator hooks | REJECT, REJECT, REJECT | REJECT |
| A-003 | Observe-first exposure window accepted | QUALIFY, QUALIFY, QUALIFY | QUALIFY |
| A-004 | Legitimate Opus runs are rare | QUALIFY, QUALIFY, QUALIFY | QUALIFY |
