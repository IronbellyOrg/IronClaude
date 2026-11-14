# Version 1 proposal: model-policy guard (Lens C: policy and operations)

Name: `model-policy-guard.sh`. It is one script that reads one JSON policy and decides by plain code. It never picks or rewrites a model. "Enforce" below means the hook exits 2 with a message.

Facts from the enrichment file are cited as "enrichment B5" and so on. Repository lines are cited only where I read them in this session. Anything else is marked UNVERIFIED.

## 1. Events and visibility

| # | Event | How the model is picked | Visible to a hook? | Design for v1 |
|---|---|---|---|---|
| E1 | Bash `claude` / `claude -p` with `--model X` or `--model=X` | The flag. Without it: inline `ANTHROPIC_MODEL=`, then session env, then settings `model` (enrichment B6) | Yes. PreToolUse sees `tool_input.command` (enrichment B1) | Hook check. Read the flag value, resolve it to a tier, compare with the stage. No flag: resolve the effective default and check that. |
| E2 | `bash script.sh` or `./script.sh` where the file contains `--model` | The literal inside the file (for example `.dev/brainstorms/20261113-163248-panel-collaboration/launch-debate.sh:12` has `claude -p --model claude-opus-5-5`) | Only the path, not the content | Hook reads the file (depth 1, at most 256 KB) and checks every `--model` and `ANTHROPIC_MODEL=` literal. Scripts that call other scripts are a stated ceiling (E2b). |
| E3 | Agent/Task tool `model` parameter | Alias only: sonnet, opus, haiku, fable (enrichment B5) | Yes, in `tool_input`. The matcher already covers `Agent` and `Task` (`hooks.json:116`) | Hook check on the alias, resolved through env at check time. |
| E4 | Agent call without a `model` parameter | Agent frontmatter `model:`, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main conversation's model (enrichment B5) | Partly. The hook can read the agent file and the env. It cannot see the main model after a `/model` switch (UNVERIFIED that any hook input carries the current model) | Hook computes the effective model in the documented order. Main-model inheritance uses the model recorded at SessionStart (enrichment B4). A mid-session switch is a stated ceiling. |
| E5 | `model:` frontmatter in skills and commands | Frontmatter. Today 1 skill sets `sonnet` and no command sets a model (enrichment D) | Skill: yes, through the `Skill` tool call (matcher at `hooks.json:116`). Typed `/sc:x`: only if UserPromptSubmit fires for it (UNVERIFIED) | Hook reads the frontmatter on Skill calls and on UserPromptSubmit prompts that start with `/`. A CI lint test checks all shipped frontmatter against the template policy (section 8). |
| E6 | Aliases and env: `ANTHROPIC_DEFAULT_*_MODEL`, `ANTHROPIC_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL` | Env redirects an alias to another id (enrichment B6, D) | Inline in a Bash command: yes. Set in settings or the parent process env: the hook sees only its own inherited env (UNVERIFIED that it equals the session env) | Hook resolves aliases through its env and blocks when an alias points at a different tier (MP-05). Inline redefinition counts as tamper. |
| E7 | `/model` switch | Person types it | Unknown. UserPromptSubmit may not fire for built-ins (enrichment B3, UNVERIFIED) | Cannot see: state it. Native layer: `availableModels` / `deniedModels` (enrichment B7) generated from the same policy. |
| E8 | Headless sessions started by Python, such as `src/superclaude/cli/sprint/tmux.py:193-194` (`cmd.extend(["--model", config.model])`) | The launcher's config | No. Not a Bash tool call (enrichment D) | Launcher-side check: each launcher calls the same hook script in `--check` mode before it starts the child. Launchers not yet wired are listed as uncovered. |
| E9 | `claude --bare` children | Any | No: bare sessions run no hooks (enrichment B8) | Block `--bare` and `--settings` on a launch in enforce stages (MP-06). A bare child started by a Python launcher is a stated ceiling. |

E2b ceiling: a script run by a script, `eval`, command words built from pieces. The ceilings in `require-orca-worktree-agent.sh:39-61` apply equally here.

## 2. Machine-readable policy

**Format: JSON.** The hook runs jq and no Python (the precedent at `require-orca-worktree-agent.sh:14`), and bash has no YAML parser.

**Canonical tiers.** The policy is written against tier names (`judge`, `work`, `light`). Each tier lists its aliases and concrete ids. On this host, `opus` resolves to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b` and `haiku` to `claude-gw-tier2` (enrichment D).

```json
{
  "version": 1,
  "mode": {
    "bash_claude": "observe", "bash_script": "observe", "agent": "observe",
    "skill": "observe", "prompt_command": "observe"
  },
  "tiers": {
    "judge": {"restricted": true, "aliases": ["opus"],
              "ids": ["claude-opus-5-5", "claude-gw-tier1a"]},
    "work":  {"aliases": ["sonnet"], "ids": ["claude-sonnet-5-5", "claude-gw-tier1b"]},
    "light": {"aliases": ["haiku"],  "ids": ["claude-haiku-5-5", "claude-gw-tier2"]}
  },
  "id_prefix_match": false,
  "stages": {
    "default":       {"allow": ["work", "light"]},
    "proposal":      {"allow": ["work", "light"]},
    "implement":     {"allow": ["work"]},
    "blind-scoring": {"allow": ["judge"], "declared_by": "human"}
  },
  "bindings": [
    {"match": {"script_glob": "*/blind-score*.sh"}, "stage": "blind-scoring"}
  ],
  "unknown_model": "deny",
  "dynamic_model": "deny",
  "bare_or_settings_child": "deny",
  "grant_max_hours": 24,
  "jev": {"shadow": false}
}
```

- `claude-gw-tier3` is deliberately not listed. Its family is UNVERIFIED, so it resolves to "unknown" and `unknown_model: deny` flags it in observe logs.
- `id_prefix_match: false` matters because the docs say an id entry also permits later versions (enrichment B7).
- On day one, observe mode will flag the two `opus` agents (`auggie-reviewer`, `eval-suite-author`) and `issue-worker-t1`. `issue-worker-t1` uses `claude-gw-tier1a`, which is the `opus` alias target on this host (enrichment D, mapping UNVERIFIED for the worker). The owner decides: change the frontmatter, or add a binding.

**How the requested model is declared.** The requested model is a stage name. A stage names the tiers that may be used.

1. `SC_STAGE=<name>` in the hook's environment. A launcher or a person sets it before the session starts.
2. `SC_STAGE=<name>` as an inline prefix on the Bash command. This is only accepted for stages that do not have `declared_by: human`. The model can write inline text, so it must not be able to pick `blind-scoring`.
3. A `bindings` entry in the policy that maps a script glob, an agent name or a skill name to a stage.
4. A grant record (section 4).
5. Otherwise the `default` stage applies.

The `judge` tier is `restricted`. It is allowed only through sources 1, 3 or 4, never through inline text.

Mismatch rule: if the declared stage allows tier X and the text uses tier Y, the call is rejected (MP-02). This is the literal "requested equals used" check.

**Scoping and precedence.** Three layers:

1. Managed: `/etc/superclaude/model-policy.json`. Root-owned, so a same-user model cannot edit it.
2. Project: `<project root>/.superclaude/model-policy.json`. The hook walks up from `cwd` at most 8 levels.
3. User: `~/.claude/model-policy.json`, seeded from the template.

Rules:
- Deny wins across layers. An allow needs every present layer to allow, so a lower layer can only tighten.
- The effective `mode` per event class is the strictest of the layers (enforce > observe > off).
- The tier table comes from the highest layer that defines it.

**Storage and loading.** The template ships as `src/superclaude/hooks/model-policy.json.example`. The installer copies it to `~/.claude/model-policy.json` only when absent, through `_SEED_FILES` (`install_hooks.py:104-106`, comment `:100-103`). User edits therefore survive `--force`. The hook loads each layer with one `jq` call per file and checks `version`, `tiers`, `stages` and the mode keys.

**Missing or malformed policy, per event.**

| Case | Ordinary Bash, prompts, non-launch tools | A positively detected model-choosing event (E1-E5, E8) |
|---|---|---|
| No policy in any layer | Allow, silent. Write one log line. | Allow, log `no_policy`. |
| Malformed (bad JSON, unknown `version`, missing required keys) in observe mode | Allow | Allow, log `MP-08` |
| Malformed in enforce mode | Allow. Never brick the session, because the fix itself runs through Bash. | Deny with MP-08 (reason: the guard cannot prove the model) |
| Session governed (`SC_STAGE` in the hook env), any internal error | Deny, as `launch-level-guard.sh:147-163` does for governed sessions | Deny |
| `jq` or `awk` missing | Fail open, as `require-orca-worktree-agent.sh:11-13` does. Log it, and add `superclaude doctor` warning text. | Same |

## 3. Where Jev adds value in v1 versus plain code

**Code decides (about 95 percent, expected, UNVERIFIED until the observe log exists):**
- Literal `--model` or `--model=` on a `claude` command.
- Inline `ANTHROPIC_MODEL=` and the alias env redirects.
- The Agent `model` parameter.
- Frontmatter in agents, skills and commands.
- Literal flags inside a script that is run by path.
- A single in-file assignment, `M=claude-opus-5-5 ... --model "$M"`, resolved by one regex over the same file.

**Residue code cannot decide:** the flag value is built at run time (`--model "$(pick)"`, `--model "$M"` where `M` comes from a file, an argument or a loop). Code classifies it `dynamic` and applies `dynamic_model` (default `deny` in enforce).

**Is Jev needed in v1?** No, not in the blocking path. The question "what does `$M` evaluate to" is a multi-hop judgment, and Jev is poor at those (enrichment E). Code is better for it: it knows what it could not resolve and applies the policy. Jev can only add a block, and `dynamic_model: deny` already blocks everything that cannot be resolved.

**Optional shadow call (default off, `jev.shadow: true`).** The shadow runs as a separate async registration (the `"async": true` pattern at `hooks.json:144`). It is logged and never decides anything.
- Input: only commands that code already classified `claude-launch` and `model-unresolved`.
- Question (Choice): "Does this command start a Claude session whose model is set by something the text does not show?" Options: `dynamic`, `static`, `not-a-launch`, `none`. The `none` option is needed because Jev answers out-of-scope input when no option fits (enrichment E: 0 of 30 flagged without one).
- Threshold: log `jev_dynamic` when the `dynamic` probability is above 0.7.
- If it ever became blocking it could only add a block, never allow, and only after the offline test below passes.
- Cost: about $0.000025 per call, measured over 2,011 pair calls in one run on a different task (enrichment E), so moderately reliable. 1,000 shadow calls cost about $0.03.
- Latency: 70 to 500 ms reported by the vendor; outside tests report a different median, 5 to 6 times off from the vendor claim (enrichment E). Not measured by us for this task. Treat it as unreliable and budget 2.5 s.
- Failure when Jev is unreachable: do nothing. The code decision stands. A shadow that cannot answer changes no outcome, so there is no fail-open or fail-closed choice to make.

**Offline test plan.**

| Source | What it gives | Status |
|---|---|---|
| The 17 `.dev/**/*.sh` files that contain `--model claude-opus-5-5` (counted by search, for example `launch-debate.sh:12`) | Static launches that must be flagged as `judge` | verified present |
| Session transcripts under `~/.claude/projects/` | Real Bash commands containing `claude` | UNVERIFIED: not opened by me |
| `src/superclaude/cli/**` launchers (`tmux.py:193-194`) | Launches built from config | verified for one line |
| Issue #546 violation list (enrichment A) | Known positives | from the enrichment file |

Labelling method:
1. A small extraction script pulls every Bash `command` containing a `claude` word.
2. A deterministic pass labels literal tiers.
3. A human labels the remainder as `dynamic`, `static`, `not-a-launch`.
4. The labelled set is stored under `tests/hooks/fixtures/model_policy/` and replayed in CI.

Pass criteria for any Jev promotion: precision of at least 0.95 at p above 0.7 on at least 100 residue items, and zero Jev-added blocks on the `not-a-launch` and `static` items.

**What would change this conclusion:** observe logs showing dynamic flags above about 5 percent of launches, or a repeated pattern that the file scan cannot resolve.

## 4. Rejection and override

**What the model sees** (stderr, exit 2). It uses the format of the launch-level guard (`launch-level-guard.sh:126`, `Blocked:` / `Why:` / `You can:`):

```
Model-policy guard:
Blocked: starting `claude -p --model claude-opus-5-5` in stage "proposal" (rule MP-01).
Why: policy line stages.proposal.allow = [work, light]; claude-opus-5-5 is tier "judge", which is restricted. The model that was requested must be the model used.
You can: use --model sonnet (tier work), or ask the person to run: superclaude model-policy grant --stage blind-scoring --expires 4h
Policy: /home/coder/.claude/model-policy.json (layer: user), rule id MP-01.
```

Rule ids and meaning:

| Id | Meaning |
|---|---|
| MP-01 | Tier not allowed in the stage |
| MP-02 | Declared stage and written model disagree |
| MP-03 | Model resolves to no known tier |
| MP-04 | Model flag is dynamic |
| MP-05 | Alias env redirects to another tier |
| MP-06 | `--bare` or `--settings` on a child launch |
| MP-07 | Tamper with policy, grants or hook |
| MP-08 | Policy broken |
| MP-09 | Command over 64 KB (`launch-level-guard.sh:102-105`, cap at `:422-423`) |

**What the user sees.** Claude Code shows the rejected tool call. The exact display of hook stderr to the user is UNVERIFIED. The same facts go to the decision log, which the user can read: `~/.claude/state/model-policy/decisions.jsonl`. Fields: `ts`, `session_id`, `event`, `rule`, `tier`, `stage`, `mode`, `action` (`observe` or `deny`). Raw command text is not logged, only the extracted model tokens.

**Exit code.** Exit 2 plus stderr only. Never exit 1. No JSON output in v1, matching the precedents (`require-orca-worktree-agent.sh:10-12`).

**Human override record.** A grant is one file: `~/.claude/state/model-policy/grants/<id>.json`.

| Field | Meaning |
|---|---|
| `id` | unique id |
| `created_at`, `expires_at` | Expiry is required and capped by `grant_max_hours` (24 in the example) |
| `stage` | The stage it unlocks |
| `allow` | Tiers or ids allowed |
| `scope` | One of `session_id`, a `cwd` glob, or `command_sha256` |
| `reason` | Required text |
| `created_by` | `human-tty` |
| `uid` | Creator's user id |

Creation: `superclaude model-policy grant ...`. The command refuses to run unless stdin is a TTY and it reads a typed `yes` from `/dev/tty`. The Bash tool runs without a TTY (UNVERIFIED), so the model cannot confirm.

The guard also blocks these as MP-07, the same pattern as TAMPER at `launch-level-guard.sh:94-97`, with the matching check near `:706`:
- Bash text naming `model-policy grant` or the state directory.
- Edit, Write and NotebookEdit on the policy, grant or state paths.

Ceiling: a same-user process that is not seen by the hook (a Python subprocess, a hand-made file) can still write a grant. Putting the policy in the managed layer closes that for the policy file, not for grants. Honest ceiling: grants are protected against the model's normal tools, not against a determined same-user process.

## 5. Bypass resistance

| Attack | Result |
|---|---|
| Wrapper words (`sudo`, `nohup`, `env`, `timeout`, `time`) | Blocked. The word scan finds `claude` by basename in any segment (`launch-level-guard.sh:454`). |
| `bash -c "claude ..."`, `eval`, `ssh host '...'`, `xargs claude` | Ceiling, same as `require-orca-worktree-agent.sh:39-45`. Mitigation: detection. A command with a `claude` word anywhere in the text and no resolvable flag is logged as `claude-mention` and treated as dynamic (MP-04). |
| Script written then run | Blocked at run time, because the hook reads the file when it is run by path. Not covered when the script is built and fed to a shell on stdin (`cat <<EOF \| bash`, ceiling at `require-orca-worktree-agent.sh:43-45`). |
| Heredoc or here-string body | Scanned as text, since the check works on the whole command. |
| Variables and command substitution in the flag value (`--model "$M"`) | Detected: any word with `$` is dynamic (MP-04). One in-file assignment is resolved. |
| Env override inline (`ANTHROPIC_MODEL=opus claude`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-opus-5-5`) | Blocked or flagged (MP-01, MP-05). |
| Env override in settings or the parent process | Hook sees its own env only: partly covered. Native `availableModels` / `deniedModels` is the backstop (enrichment B7). |
| `--settings` or `--bare` on the child | Blocked in enforce stages (MP-06). Child `claude --bare` started by a Python launcher: ceiling (enrichment B8). |
| Editing the hook, policy, grants or `settings.json` | Blocked for Bash, Edit, Write and NotebookEdit by path and text (MP-07). Ceiling: non-tool writes. Recommend the managed policy layer. |
| Other tools (Monitor, Workflow, RemoteTrigger) | Monitor: same Bash scan (the matcher at `hooks.json:116` lists it). Other tools: ceiling in v1. |
| Subagents | PreToolUse hooks fire inside subagents, so their Bash and Agent calls are checked (`require-orca-worktree-agent.sh:5-6`). |
| `/model` switch and a changed main model | Ceiling, see E7. |
| Hook timeout | Platform treats non-exit-2 as non-blocking (enrichment B9), so a timeout fails open. Mitigation: the script wraps its own scan in `timeout 2` and converts a self-timeout to exit 2 for governed sessions. |

## 6. Time cost per event

All numbers are estimates, not measured (UNVERIFIED). Step 1 of the plan measures them on this host, with a target of p95 at or below 50 ms on the non-matching path.

| Event | Typical (ms) | Worst (ms) | Recommended `timeout` (s) |
|---|---|---|---|
| Ordinary Bash, no `claude` word (prefilter exit) | 10 | 40 | 5 |
| Bash with literal `--model` | 25 | 80 | 5 |
| Bash running a script (scan up to 256 KB) | 30 | 120 | 5 |
| Agent / Task | 20 | 60 | 5 |
| Skill | 20 | 60 | 5 |
| UserPromptSubmit, ordinary prompt | 8 | 30 | 3 |
| UserPromptSubmit, `/command` with frontmatter read | 20 | 60 | 3 |
| SessionStart record | 10 | 30 | 2 |
| Launcher-side check from Python (spawn) | 40 | 100 | not a hook |
| Jev shadow (async, off by default) | 150 | 2,500 | 5, async |

The 5 s Bash timeout matches `launch-level-guard.sh` (`hooks.json:121`). The 3 s UserPromptSubmit value matches `freshness-user-prompt.sh` (`hooks.json:50`).

## 7. Test plan and requirements

Test files in `tests/hooks/` (existing names include `test_launch_level_guard.py` and `test_require_orca_worktree_agent.py`):
- `test_model_policy_guard.py` (events)
- `test_model_policy_policy.py` (precedence, malformed)
- `test_model_policy_grants.py`
- `test_model_policy_install.py` (list, registration, seed)
- `test_model_policy_replay.py` (labelled fixtures)

Run with `uv run pytest tests/hooks/ -v`.

- REQ-01: A Bash `claude -p --model claude-opus-5-5` in the default stage is denied with exit 2 and rule MP-01 in enforce mode. [unit test]
- REQ-02: The same command in observe mode exits 0 and writes one `observe` line to the decision log. [unit test]
- REQ-03: `claude -p --model=claude-sonnet-5-5` is allowed in the default stage. [unit test]
- REQ-04: `--model opus` is resolved through `ANTHROPIC_DEFAULT_OPUS_MODEL` before comparing. [unit test]
- REQ-05: A bracket suffix (`claude-gw-tier1a[1m]`) is ignored when resolving a tier. [unit test]
- REQ-06: An alias whose env value points at another tier is denied with MP-05. [unit test]
- REQ-07: A `claude` launch with no `--model` is checked against the effective default model. [unit test]
- REQ-08: `bash script.sh` is denied when the file contains `--model claude-opus-5-5` and the stage does not allow `judge`. [fixture replay with `launch-debate.sh`-style fixture]
- REQ-09: A script larger than 256 KB is not scanned and is logged `scan_skipped`. [unit test]
- REQ-10: A flag value containing `$` is classified `dynamic` and denied with MP-04 under `dynamic_model: deny`. [unit test]
- REQ-11: A single in-file assignment `M=claude-sonnet-5-5` followed by `--model "$M"` resolves and is allowed. [unit test]
- REQ-12: An Agent call with `model: "opus"` is denied in a stage that does not allow `judge`. [unit test]
- REQ-13: An Agent call without `model` takes the model from the agent file's frontmatter. [unit test]
- REQ-14: An Agent call with neither a `model` parameter nor frontmatter uses `CLAUDE_CODE_SUBAGENT_MODEL`, then the SessionStart model. [unit test]
- REQ-15: A Skill call whose frontmatter names a forbidden tier is denied. [unit test]
- REQ-16: A UserPromptSubmit prompt `/cmd` whose command file names a forbidden tier is denied. [unit test; real firing UNVERIFIED, manual check]
- REQ-17: An inline `SC_STAGE=blind-scoring` prefix is ignored for a stage marked `declared_by: human`. [unit test]
- REQ-18: `SC_STAGE=blind-scoring` in the hook env allows `judge` in that session only. [unit test]
- REQ-19: A declared stage that disagrees with the written model is denied with MP-02. [unit test]
- REQ-20: The project layer cannot widen what the user layer denies. [unit test]
- REQ-21: The effective mode is the strictest across layers. [unit test]
- REQ-22: A malformed policy in enforce mode denies a launch with MP-08 and still allows `ls`. [unit test]
- REQ-23: Missing policy allows everything and writes a `no_policy` log line. [unit test]
- REQ-24: A governed session fails closed on any internal error. [unit test]
- REQ-25: With `jq` missing the hook exits 0. [unit test with PATH stripped]
- REQ-26: The rejection message contains the rule id, the policy line, the policy path and a `You can:` line. [unit test]
- REQ-27: The hook never exits 1 and never writes JSON to stdout. [unit test over all fixtures]
- REQ-28: An expired grant is ignored; a valid grant allows only its scope. [unit test]
- REQ-29: `superclaude model-policy grant` refuses to run without a TTY. [integration test]
- REQ-30: A Bash command naming `model-policy grant` or the state directory is denied with MP-07. [unit test]
- REQ-31: An Edit or Write on the policy file is denied with MP-07. [unit test]
- REQ-32: `--bare` or `--settings` on a child launch is denied with MP-06 in enforce stages. [unit test]
- REQ-33: A command over 64 KB is denied with MP-09. [unit test]
- REQ-34: The non-matching Bash path has p95 at or below 50 ms over 200 runs. [integration test, timing]
- REQ-35: `model-policy-guard.sh` is in `_FRESHNESS_SCRIPTS` and `make verify-sync` reports no drift. [integration test]
- REQ-36: The hooks.json registration for the script exists on PreToolUse, UserPromptSubmit and SessionStart with the timeouts in section 6. [unit test]
- REQ-37: A reinstall with `--force` does not overwrite an edited `~/.claude/model-policy.json`. [integration test]
- REQ-38: Every shipped agent, skill and command frontmatter model resolves to an allowed tier or to a listed exception. [unit test over `src/superclaude/{agents,skills,commands}`]
- REQ-39: The Python launcher helper returns exit 2 for a forbidden stage/model pair and 0 for an allowed one. [unit test]
- REQ-40: The replay of the labelled fixture set gives zero false denials on `static` and `not-a-launch` items. [fixture replay]

## 8. Implementation plan

**Files.**
- Add `src/superclaude/hooks/scripts/model-policy-guard.sh`. One dispatch on `hook_event_name`, like `launch-level-guard.sh:182-205`. It reuses the normalisation block (`launch-level-guard.sh:431-437`) and copies it in, because installed hooks are standalone.
- Add `src/superclaude/hooks/model-policy.json.example`: the template.
- Change `src/superclaude/hooks/hooks.json`: three registrations (below).
- Change `src/superclaude/cli/install_hooks.py`: one entry in `_FRESHNESS_SCRIPTS` (`:42-97`) and one in `_SEED_FILES` (`:104-106`):

```python
    "model-policy-guard.sh",            # PreToolUse/UserPromptSubmit/SessionStart model-policy guard
    ("model-policy.json.example", "model-policy.json"),   # in _SEED_FILES
```

- Add a new click command module under `src/superclaude/cli/` for `superclaude model-policy grant|list|revoke|check`, registered in the CLI entry (file not verified).
- Add the launcher helper that runs `model-policy-guard.sh --check <stage> <model>`. Wire it into the sprint, roadmap, eval and reflect launchers (the files in enrichment D). Unwired launchers stay on the uncovered list.
- Add tests listed in section 7 and fixtures under `tests/hooks/fixtures/model_policy/`.

**Registration JSON** (same command string for all events, as `launch-level-guard.sh` has at `hooks.json:67` and `:120`):

```json
"PreToolUse": [
  {"matcher": "Bash|Agent|Task|Skill|Monitor",
   "hooks": [{"type": "command",
              "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 5}]}
],
"UserPromptSubmit": [
  {"hooks": [{"type": "command",
              "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 3}]}
],
"SessionStart": [
  {"hooks": [{"type": "command",
              "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 2}]}
]
```

**Sync.** Edit only `src/superclaude/hooks/scripts/`. Run `make sync-dev`, which copies `src/superclaude/hooks/scripts/*.sh` to `.claude/hooks/` (`Makefile:137-142`). Run `make verify-sync`, which diffs the two (`Makefile:255-262`) and requires every script to be a member of `_FRESHNESS_SCRIPTS` (`Makefile:308-311`). Never edit `.claude/` by hand. The installed script and its message text never name a `src/superclaude/` path: they name `~/.claude/model-policy.json` and `~/.claude/hooks/...`.

**Order of work (8 steps).**
1. Resolver and policy loader as jq filters with fixture tests. Measure the non-matching path time.
2. Hook script: dispatch, prefilter, Bash `claude` parse, decision log, message, observe and enforce.
3. Agent, Skill and UserPromptSubmit frontmatter resolution, plus the SessionStart record.
4. Script scan (depth 1) and the `dynamic` classification.
5. Grant CLI and the MP-07 tamper class.
6. Installer list, seed, registration, `verify-sync`, and the CI frontmatter lint (REQ-38).
7. Launcher-side helper and wiring into the four launcher families.
8. Rollout.

**Rollout.**
- **Week 0:** ship with every event class at `observe`. Nothing is blocked. The log fills.
- **Review:** read `decisions.jsonl`. Check false-positive count per rule and the dynamic share. Resolve the day-one flags (the two opus agents, `issue-worker-t1`).
- **Enforce, first:** `bash_claude` and `agent` (literal and parameter checks have the lowest false-positive risk).
- **Enforce, second:** `skill`, `prompt_command`, then `bash_script` once the scan has run clean for at least 100 script events.
- **Rollback:** set the event class back to `observe` in the user policy file. No reinstall needed.

## 9. Room for version 2

- A `routing: dynamic` marker in an agent, skill or command frontmatter would exempt it from the fixed-model check and name a v2 router.
- The router would pick a model from facet answers mapped by a code table (Jev item 7, enrichment E), with the retry-ledger data it needs.
- The decision log fields (`tier`, `stage`, `rule`) are the data the router would learn from.
- v1 never rewrites a model. v2 must keep that, or use `updatedInput` only with its own explicit mode (enrichment B2).
- Native `availableModels` generation from the policy is left as a v2 task.
- Jev as a blocking residue classifier stays off until the offline test passes.

## 10. Risks and recommendation

- A hook cannot see Python launchers, `/model`, scripts that call scripts, `bash -c`, or bare children. Section 1 lists each. The launcher helper and native `availableModels` are the only coverage for some of them.
- The same-user model can create grants or edit files through paths the hook does not see. The managed layer protects the policy only.
- A hook timeout fails open (enrichment B9). The self-timeout reduces this for governed sessions only.
- `bindings` by glob can be satisfied by a model that creates a script with a matching name. Optional `sha256` pins reduce this.
- The tier mapping for `claude-gw-tier3` and the family of `issue-worker-t1` are UNVERIFIED and need the owner.
- Latency figures are estimates until step 1.
- UserPromptSubmit firing for `/command` and for `/model` is UNVERIFIED.

**Version 1 recommendation: ship one deterministic, JSON-policy-driven guard with no Jev in the blocking path, observe-only first, and enforce each event class after the decision log shows it is clean.**

| Status | Result |
|---|---|
| DONE | Wrote the 10-section version 1 proposal. |
| NEXT | None. |

Not checked: the installer ownership merge body (`install_hooks.py:301` onward), the Python CLI entry file, and any real timing. I did not open any session transcript.
