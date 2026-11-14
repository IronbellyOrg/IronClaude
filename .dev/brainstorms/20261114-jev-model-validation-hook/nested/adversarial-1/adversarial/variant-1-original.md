# Version 1 proposal: layered model-policy hook (Lens A, architect)

Policy file, hook script, launcher helper and CLI are all new names. Nothing below exists yet.

## 0. Headline design

Three layers, each catching what the one above cannot see.

| Layer | Mechanism | Strength | Blind to |
|---|---|---|---|
| L0, floor | Native `availableModels` / `deniedModels` / `enforceAvailableModels` in settings | Covers every in-process choice: `/model`, `--model`, `ANTHROPIC_MODEL`, alias env redirects, agent/skill/command frontmatter, Agent `model` param (enrichment B7) | Per-stage rules (global, static); lists concatenate unless managed (B7) |
| L1, per-stage | New `PreToolUse` hook `enforce-model-policy.sh` (plus `SessionStart` and `UserPromptSubmit` entries) | Per-stage allow/deny, reads command text, scripts and frontmatter, gives a clear reason | Anything outside the Bash/Agent/Skill tool path (Python subprocesses, `--bare` children, `/model`) |
| L2, launcher | One Python function `check_launch(stage, model)` called before every `Popen` of `claude`, plus `superclaude model-policy check` for shell launchers | Sees the Python launchers L1 cannot (`pipeline/process.py:163-164`, `sprint/tmux.py:194`, `prd/models.py:283`, `reflect/runner.py:508`) | Code that does not call it |
| L3, detective (not a gate) | After a headless run, compare the observed model in the output JSON to the requested one | Catches silent substitution (the incident script already reads `.message.model` and `modelUsage`: `.dev/brainstorms/20261113-223124-panel-process-redesign/launch-variants.sh:35-36`) | Runs after the fact |

The hook never picks or rewrites a model. It allows, or blocks with a reason.

Plain statement of the v1 property: a launch is allowed only if the model it names resolves to a tier the session's stage allows. A launch that does not name a model is rejected when the stage requires an explicit pin.

## 1. Events and visibility

Hooks documentation facts used (enrichment B): PreToolUse input carries `session_id`, `cwd`, `tool_name`, `tool_input` (B1); exit 2 blocks and stderr goes to Claude (B2); `SubagentStart` has no model field (B4); non-2 failure exits fail open (B9); `claude --bare` children run no hooks (B8).

| # | Event | How it picks the model | Hook can see? | v1 handling |
|---|---|---|---|---|
| 1 | Bash `claude [-p] --model X` literal | Flag | Yes: `tool_input.command` | L1 tokenizer finds the `claude` word and its `--model` value, resolves tier, decides |
| 2 | Bash `claude` with no `--model` | Flag > `ANTHROPIC_MODEL` > settings `model` > default (B6; settings layering UNVERIFIED) | Partly: only the command text and the hook's own env | Stage with `require_explicit_model` blocks it (MP-NOT-PINNED), because inheriting is how an Opus session spawns Opus children |
| 3 | Bash `bash script.sh` / `./x.sh` / `source x.sh` containing `--model` | Flag inside the file | Only the path, unless the hook reads the file (enrichment D) | L1 reads shell scripts up to 256 KB and scans them (section 5). A `.py` file named in the command gets the same scan |
| 4 | Bash `superclaude sprint\|roadmap\|prd\|tasklist\|reflect\|cleanup-audit\|cli-portify\|eval ... --model X` | Flag to a nested launcher (`sprint/commands.py:95`, `roadmap/commands.py:71`, grep-seen) | Yes, command text | Same check as row 1; L2 checks again inside |
| 5 | Agent/Task `model` parameter | Alias only: sonnet, opus, haiku, fable (B5) | Yes: `tool_input.model` | Resolve alias through host env, decide |
| 6 | Agent/Task with no `model` | Agent frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main conversation's model (B5) | Frontmatter: yes, hook reads the agent file. Parent model: only if `SessionStart` supplied it (optional field, B4) | Read frontmatter by `subagent_type`; else check the recorded session model; MP-INHERIT if that tier is forbidden |
| 7 | Frontmatter `model:` of agents, skills, commands | Definition file | Only indirectly, at the Agent/Skill call that uses it | L1 reads the file at call time. A static lint (`superclaude model-policy lint`) checks all shipped definitions in CI. In-process use is also bounded by L0 |
| 8 | Skill tool call | Skill's frontmatter `model:` (1 skill sets one: `sc-bare-review/SKILL.md:5`) | Skill name yes; file read by the hook | Same as row 7 |
| 9 | Aliases and env: `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL(_FORCE)` | Redirects an alias to another id (B6) | In a command prefix or `export`: yes. Set in settings `env` or by the harness: no | Assignments in a command are rejected (MP-ENV-REDIRECT). Settings-file `env` is protected by the TAMPER class on writes. Harness-applied values: L0 only |
| 10 | `/model` typed by a person | Built-in client command | UNVERIFIED whether `UserPromptSubmit` fires | If it fires, the hook blocks or records. Either way L0 is the floor. Stated ceiling |
| 11 | Session's own model at start | `--model`, settings, env | `SessionStart.model` when present (optional, B4) | Recorded in a state file for row 6. Not rejected: the human's own session is not a launch event |
| 12 | Headless sessions from scripts (row 3) | Flag in file | See row 3 | L1 file scan plus L3 |
| 13 | Headless sessions from Python in `src/superclaude/cli/` | `cmd.extend(["--model", self.model])` (`pipeline/process.py:163-164`) | No, a subprocess outside the Bash tool | L2 helper; L0 as floor |
| 14 | `claude --bare` child | Same flags | Launch command: yes. Child's own events: no, no hooks run (B8) | Launch rejected for non-elevated stages (MP-BARE-CHILD) |
| 15 | Monitor tool commands | Same as Bash | Yes (`command` field; already in the guard matcher, `hooks.json:116`) | Same classifier |
| 16 | Mods with `agent.spawn` that replace the model (B5), Workflow tool scripts | Out-of-band | No | Stated ceiling; Workflow `tool_input` shape not verified |

## 2. Machine-readable policy

### File and scoping

- Format: JSON. The hook already needs `jq` (`require-orca-worktree-agent.sh:11-15`); Python reads it with the standard library. No YAML parser in the hook.
- User file: `~/.claude/model-policy.json`, seeded from a template through the existing seed mechanism (`install_hooks.py:104-106`: deployed only when absent, never overwritten).
- Project file (optional): the nearest `.claude/model-policy.json` found by walking up from `cwd` (at most 8 levels, pure bash).
- Precedence: a project file can only tighten. `deny` is the union of layers. `allow` is the intersection of layers that define one. `mode`: enforce beats observe. A model-written project file therefore cannot loosen anything.
- The user file may loosen. Only a person edits it, because Edit/Write to it is a TAMPER class (section 5).

### Requested model and stage declaration

- A launch's requested model is the `--model` / `model` value it carries. The defined model is what the stage and the agent definition allow. The hook checks requested against defined.
- Stage comes from the session environment variable `SC_MODEL_STAGE` (default `default`). It is set by whoever starts the session (a person, Orca, or the L2 helper), not by the model.
- A command prefix `SC_MODEL_STAGE=x claude ...` may only narrow: the declared stage's `allow` must be a subset of the session stage's `allow`, otherwise MP-STAGE-WIDEN. This stops the model from claiming `blind-scoring` for itself.
- Elevation (Opus from a `default` session) needs a human grant (section 4), which can bind to a script's sha256.

### Example (`~/.claude/model-policy.json`)

```json
{
  "schema": 1,
  "mode": "observe",
  "event_mode": {"bash_launch": "enforce", "agent": "enforce", "script_scan": "observe"},
  "tiers": {
    "opus":   {"aliases": ["opus"],   "ids": ["claude-opus-*"],   "host_env": "ANTHROPIC_DEFAULT_OPUS_MODEL"},
    "sonnet": {"aliases": ["sonnet"], "ids": ["claude-sonnet-*"], "host_env": "ANTHROPIC_DEFAULT_SONNET_MODEL"},
    "haiku":  {"aliases": ["haiku"],  "ids": ["claude-haiku-*"],  "host_env": "ANTHROPIC_DEFAULT_HAIKU_MODEL"},
    "fable":  {"aliases": ["fable"],  "ids": ["claude-fable-*"],  "host_env": "ANTHROPIC_DEFAULT_FABLE_MODEL"}
  },
  "host_ids": {"claude-gw-tier1a": "opus", "claude-gw-tier1b": "sonnet", "claude-gw-tier2": "haiku"},
  "stages": {
    "default": {
      "allow": ["sonnet", "haiku"], "deny": ["opus", "fable"],
      "unclassified": "deny", "require_explicit_model": true, "inherit_check": true,
      "env_redirect": "deny", "bare_child": "deny", "settings_flag": "deny",
      "dynamic_model": "closed_world_then_deny", "script_max_kb": 256
    },
    "blind-scoring": {
      "allow": ["opus", "sonnet", "haiku"], "deny": [],
      "unclassified": "deny", "require_explicit_model": true, "inherit_check": false,
      "env_redirect": "deny", "bare_child": "deny", "settings_flag": "deny",
      "dynamic_model": "closed_world_then_deny", "script_max_kb": 256
    }
  },
  "jev": {"enabled": false}
}
```

Notes on the example:

- `host_ids` mirrors this host's alias env (enrichment D: `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]`, sonnet `claude-gw-tier1b[1m]`, haiku `claude-gw-tier2[1m]`).
- `claude-gw-tier3` is deliberately unlisted. What the gateway runs behind each id is UNVERIFIED.
- With this table, `issue-worker-t1` (`model: claude-gw-tier1a`, `agents/issue-worker-t1.md:6`) resolves to the Opus tier and would trip `default.deny`. The first observe run will show whether the owner wants that.

### Canonicalisation (one rule set, both implementations)

1. Lower-case the value and strip a `[...]` suffix such as `[1m]`.
2. Exact match in `host_ids`.
3. Exact alias match.
4. Equal to a tier's `host_env` value (read from the hook's own environment, suffix stripped).
5. Glob match in `ids`.
6. Otherwise the tier is `unclassified`.

A prefix that redirects an alias is rejected before step 4, so the table cannot be poisoned from inside a command.

### Loading

- The hook merges user + project policy in one `jq` call. It hashes the file (`sha8`) for the decision log.
- Alias env values come from the hook's own environment (UNVERIFIED that hooks inherit the session env on this host; very likely, as they are child processes).

### Missing or malformed policy, per event

| Situation | Launch events (Bash claude, Agent with model, Skill/Agent frontmatter) | Other events |
|---|---|---|
| No policy file at all | Allow, log `no_policy`. Deliberate delete; `superclaude doctor` should flag it (not designed here) | Allow |
| Malformed JSON, `schema` not 1, unknown tier named, invalid `mode` | Block, MP-POLICY-BROKEN (fail closed), message: "ask the person to fix `~/.claude/model-policy.json`" | Allow |
| Policy valid, but `mode: observe` | Log `would_block`, exit 0 | Allow |
| Internal error (jq or awk missing, scanner failure, timeout) | Fail closed only if a pure-bash prefilter on the raw input saw `claude`, `superclaude`, `ANTHROPIC_`, `CLAUDE_CODE_`, or an Agent/Task call with `model`; else allow | Allow |

Reason for the split: fail-open everywhere would leave the exact incident path open. Fail-closed everywhere would break every Bash call on a host without jq. This mirrors the precedents (`require-orca-worktree-agent.sh:10-15` fails open; `launch-level-guard.sh:147-163` fails closed for governed sessions). Note that a platform timeout is a non-blocking error (B9), so the script wraps its own work in `timeout 4` and converts expiry to exit 2 for launch events.

Default enforcement scope is all sessions (the incident sessions were ordinary ones), but the seeded template starts in `observe`.

## 3. Where Jev adds value in v1 versus plain code

### Code decides these (the great majority)

- Literal `--model` in a command, any wrapper (`sudo`, `env`, `nohup`, `timeout` are skipped by the copied tokenizer, `require-orca-worktree-agent.sh:21-25`).
- Alias or id to tier.
- Agent `model` parameter and frontmatter.
- Env redirects, `--bare`, `--settings`.
- Single-assignment variables: `MODEL=claude-sonnet-5-5` at line 8 then `--model "$MODEL"` at line 28 (`.dev/eval-workspaces/tasklist-review-panel/20261113-collab/launch-implement-2.sh:8,28`).
- Closed-world table case: `launch-variants.sh` takes the model from a `SPECS` array (lines 11-13), reads it at line 16 and uses it at line 31. Rule: if the variable is assigned only from in-file text, and every non-comment model-shaped literal in the file is allowed, the dynamic argument is bounded and allowed. The comment on line 3 that mentions Opus is stripped first.

### The residue

- A `--model` value that comes from outside the file: `"$1"`, an inherited env var such as `SWEEPER_MODEL` (named in the usage line at `r2-idle-shift-sweeper/bin/launch-panel.sh:3`), a file read, a command substitution.
- In-file flows where the closed-world rule is unsound or the file mentions a forbidden literal.

### Honest conclusion: v1 needs no Jev call

For the truly external case Jev sees the same text the code sees, so it cannot know the value either. Its best honest answer is "cannot tell". Code can already do the safe thing: `dynamic_model: closed_world_then_deny` blocks, and the message tells the author to pin a literal or call the launcher-side check first. Jev can only add blocks, never allow, so under a deny default it adds nothing.

What would change this: a measured residue where code is wrong. Gate for enabling `jev.enabled`: at least 50 labelled in-file indirect launches where code's closed-world rule misses a forbidden model, and Jev reaches precision of at least 0.95 at p of at least 0.7 with at most 1% false blocks. Until then, ship it off.

### Spec if enabled (default off, mode `allow_log` for dynamic cases)

- Trigger: only when code returns UNRESOLVED and the stage sets `"dynamic_model": "jev_then_log"`.
- Input: at most 2 KB, 60 lines: the claude line plus every line that assigns or loops over the variable. Comments kept (they carry the intent) but secrets redacted. Sent to an external model, so only this excerpt leaves the machine.
- Question (Choice, one call): "In this shell excerpt, which best describes the value of the `--model` argument at the claude call? (a) a literal name from the forbidden list, (b) a literal name not on the list, (c) taken from a list or table that includes a name from the forbidden list, (d) cannot be told from this excerpt."
- The forbidden list is passed as a vocabulary only (aliases and ids of the denied tiers). Policy stays in code.
- Option (d) exists on purpose: Jev flags 0 of 30 out-of-scope inputs unless a "none" option exists (enrichment E).
- Decision: code adds a block (MP-DYNAMIC-LIKELY) only when p(a or c) is at least 0.70. Jev can never turn a code block into an allow.
- Cost: measured $0.000025 per call, from 2,011 duplicate-pair calls (AB-RESULTS.md as quoted in enrichment E). That was short pair inputs, so a 2 KB excerpt could cost 2 to 5 times more (my estimate, UNVERIFIED). Reliability of that figure: high for what was measured, weak for this task.
- Latency: reported 70 to 500 ms (company-adjacent); outside tests find the vendor claims 5 to 6 times smaller at the median (E). Not measured on this task. Budget: 2 s call timeout, no retry (a hook cannot afford one; the p15 adapter retries once, E).
- Unreachable (timeout, 429, 5xx, bad key): no added block, so the code result stands (allow-and-log for `jev_then_log`). A failed call is never an answer (E). Reason: Jev only adds, so its absence must equal the code default.
- Key: `JEV_API_KEY` from env only; endpoint setting UNVERIFIED (not found in what I read).

### Offline test plan

Data sources on this machine:

- Incident scripts under `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/`:
  - violations: `launch-implement.sh:18` and `launch-designs.sh:22` (`--model claude-opus-5-5`);
  - compliant literal: `launch-slack.sh:31`, `launch-override.sh:27` (`claude-sonnet-5-5`);
  - single variable: `launch-implement-2.sh:28`;
  - table-driven: `launch-variants.sh:31` (redesign brainstorm);
  - function argument: `run-proposals.sh:17` (this brainstorm).
- Session transcripts under `~/.claude/projects/` (Bash `tool_use` inputs). I did not read any, so their shape is UNVERIFIED.
- Output JSON of headless runs (`session.json`) with `modelUsage` keys (`launch-variants.sh:35-36`).

Labelling method: ground truth is the observed model in the run's output JSON, mapped to a tier by the policy table. Label VIOLATION if that tier is outside the stage allow list, else OK. Join launch command to output file by the redirect path in the same line (for example `$D/implement-report/session.json`). Hand-label cases with no output file.

Plus synthetic mutants, labelled by construction: take each literal launch and rewrite it as `M=...; claude --model "$M"`, `"${M:-...}"`, `bash -c`, heredoc, array-literal. Report mutants separately, because they are not real data.

Metrics:

- Literal and single-variable cases: 100% recall, 0 false blocks on the OK scripts.
- Closed-world cases: report precision and recall.
- Jev: AUC and precision at p of at least 0.7, over the residue only. If the real residue has fewer than 50 labelled items, do not enable Jev.

## 4. Rejection and override

### Message the model sees (stderr, exit 2; same contract as `require-orca-worktree-agent.sh:10-15`)

```
Model policy: blocked [MP-FORBIDDEN-TIER] (event ev-20261114T135012-9f3a)
Blocked: claude -p --model claude-opus-5-5 resolves to tier opus on this host.
Why: stage "default" allows tiers sonnet, haiku and denies opus (policy ~/.claude/model-policy.json, stages.default.deny). Opus is reserved for blind scoring.
You can: re-run with a model from an allowed tier, for example --model claude-sonnet-5-5 (the hook never changes the model for you). For an approved Opus stage, ask the person to run in their own terminal: superclaude model-policy allow --tier opus --for 2h --reason "<why>"
```

This follows the `Blocked: / Why: / You can:` shape (`launch-level-guard.sh:126`). The message names the rule id and policy line. Rule ids:

- MP-FORBIDDEN-TIER
- MP-UNCLASSIFIED
- MP-NOT-PINNED
- MP-INHERIT
- MP-DYNAMIC
- MP-ENV-REDIRECT
- MP-BARE-CHILD
- MP-SETTINGS-FLAG
- MP-STAGE-WIDEN
- MP-SCRIPT-UNREADABLE
- MP-BIG
- MP-TAMPER
- MP-POLICY-BROKEN

For `/model` blocked via `UserPromptSubmit`, the JSON is `{"decision":"block","reason":...}` (B3), shown to the user.

### What the user sees

- The tool call appears blocked, with the stderr text (display format UNVERIFIED).
- Every decision, including `would_block` in observe mode, is appended to `~/.claude/state/model-policy/decisions.jsonl`: `ts, sid, event, tool, stage, decision, rule, model_raw, tier, source, policy_sha8, ms`.
- `superclaude model-policy log --tail 20` prints it.

### Human override

- Command: `superclaude model-policy allow --tier <t> [--stage <s>] [--session <id> | --project <dir> | --script <path>] --for <dur> --reason <text>`.
- Record: one line appended to `~/.claude/state/model-policy/overrides.jsonl`: `{id, created, expires, uid, tty, scope:{tier, stage, session|project|script_sha256}, reason}`.
- Default expiry 2 h, maximum 24 h. A `--script` grant binds to the file's sha256, so the human reviews the exact script that contains the Opus literal.
- Who may create it: the CLI refuses unless stdin is a TTY and `CLAUDECODE` is unset. The Bash tool has no TTY.
- Defence against the model creating it itself: any Bash/Monitor command naming `model-policy` with `allow`/`grant`, or any Edit/Write/Bash touching the state directory or policy file, is class MP-TAMPER and blocked (precedent: `launch-level-guard.sh:706`).
- Ceiling: a same-user process with a pty could still write the file. A root-owned managed settings file is the only stronger layer (availability on this workspace UNVERIFIED).
- The hook reads the last 200 override lines only when it is about to block, so the allow path pays nothing.

## 5. Bypass resistance

The command scanner runs two passes. Pass 1 is the structured tokenizer (copied, as installed hooks are standalone, `require-orca-worktree-agent.sh:24-25`). Pass 2 is a flat over-approximate scan: normalise quotes, backslashes and commas as the guard does (`launch-level-guard.sh:431`), then look for any `--model X` pair or env redirect anywhere in the text whenever the word `claude` or `superclaude` appears. Pass 2 can only add blocks.

| Vector | Result |
|---|---|
| Wrappers: `sudo`, `env`, `nohup`, `timeout` | Blocked (tokenizer skips them) |
| `bash -c "claude --model opus"`, `eval`, `ssh host '...'`, `xargs`, `find -exec`, heredoc piped to a shell | Blocked by pass 2. These are exactly the ceilings of the Orca hook (`require-orca-worktree-agent.sh:39-61`), which does not do pass 2 |
| Heredoc writing a script and running it in the same command | Blocked by pass 2 (body is in the command text) |
| Script written by Write, then `bash x.sh` | Blocked at run time by file read. Ceiling: file changed between check and run (small time-of-check window) |
| Script sourcing another script, or generating the flag from a downloaded file | Ceiling, stated; L3 detects after the run |
| Command text over 64 KB or script over 256 KB | MP-BIG (as in `launch-level-guard.sh:102-105`, `:422`) |
| Variables: `--model "$M"` | Resolved by single-assignment and closed-world rules; else MP-DYNAMIC |
| Command substitution `$(...)`, backticks, assembled words (`--mo$x`) | Treated as dynamic → MP-DYNAMIC. Words assembled into `claude` itself: ceiling (same as Orca hook) |
| Env: prefix or `export` of `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL(_FORCE)`, `ANTHROPIC_BASE_URL` | Blocked (MP-ENV-REDIRECT) |
| Env set in settings `env` or by the harness | Settings writes: TAMPER. Harness: L0 only |
| `--settings <json>` carrying `model`, `availableModels` or `env` | Blocked (MP-SETTINGS-FLAG) |
| `--bare` child | Launch blocked (MP-BARE-CHILD). Child's inner events unseen; stated ceiling |
| Tampering with hook, policy, state dir, `settings*`, `disableAllHooks`, `install_hooks` | Blocked: TAMPER class, Edit/Write/NotebookEdit included (precedent `launch-level-guard.sh:443-451,706`). Same-user pty process: ceiling |
| Python script that spawns `claude` | `uv run python x.py` reads x.py with the flat scan. Fully dynamic Python: L2 if it uses the helper, else L0 and L3 |
| Other tools than Bash: Monitor | Covered |
| Other tools than Bash: Workflow scripts, MCP, mods | Ceiling, not verified |
| Subagents | PreToolUse hooks fire inside subagents (`require-orca-worktree-agent.sh:5-6`), so their Bash and Agent calls are checked under the session stage |
| Prompt text saying "use opus" | Out of scope; policy is the written intent |
| Model claims a wider stage in a prefix | Blocked (MP-STAGE-WIDEN) |

## 6. Time cost per event

All numbers are my estimates, not measured on this host (UNVERIFIED). REQ-24 makes measuring them a gate. Costs: bash start about 3 ms, `jq` about 5 to 10 ms per spawn, `awk` about 3 ms.

| Event | Typical ms | Worst ms | Notes |
|---|---|---|---|
| Bash, not a launch | 12 to 25 | 80 | prefilter + one jq parse, early exit |
| Bash `claude` literal | 25 to 45 | 120 | tokenizer + policy jq |
| Bash `bash x.sh`, file read | 40 to 90 | 400 | 256 KB cap, flat scan |
| Agent/Task with `model` | 15 to 30 | 80 | |
| Agent without `model` (frontmatter + session record) | 25 to 50 | 120 | |
| Skill (frontmatter) | 20 to 40 | 100 | |
| Edit/Write (tamper path check) | 10 to 20 | 60 | |
| UserPromptSubmit | 10 to 20 | 60 | `^/model` check only |
| SessionStart (record) | 15 to 30 | 80 | one file write |
| Jev residue (off by default) | +150 to 600 | +2,000 | call timeout |

Recommended timeouts (the existing Bash hooks use 3 s, `hooks.json:101,113`; the guard uses 5 s, `hooks.json:122`):

- PreToolUse: 5 s. Internal `timeout 4`; Jev call at most 2 s.
- UserPromptSubmit: 3 s.
- SessionStart: 3 s.

## 7. Test plan and requirements

Tests live in `tests/hooks/` (existing pytest style, run with `uv run pytest tests/hooks/ -v`). Method: replay JSON fixtures on stdin, assert exit code and stderr, as the existing guard tests do. A shared `vectors.json` is run against both the hook and the Python module so they cannot drift.

| ID | Requirement | Verification |
|---|---|---|
| REQ-01 | A Bash command `claude -p --model claude-opus-5-5` in stage `default` exits 2 with rule MP-FORBIDDEN-TIER | [unit test, fixture replay] |
| REQ-02 | The same command with `--model claude-sonnet-5-5` exits 0 | [unit test] |
| REQ-03 | Aliases resolve through host env: `--model opus` is the Opus tier when `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a[1m]` | [unit test] |
| REQ-04 | A `[1m]` suffix and upper-case ids resolve to the same tier as the plain id | [unit test] |
| REQ-05 | A model that matches no tier is `unclassified` and blocked when the stage says deny | [unit test] |
| REQ-06 | `claude -p` with no `--model` is blocked MP-NOT-PINNED when `require_explicit_model` is true | [unit test] |
| REQ-07 | `timeout 60 claude -p --model opus` and `sudo env X=1 claude ...` are detected through wrappers | [unit test] |
| REQ-08 | `bash -c "claude --model opus"`, `eval`, `ssh h 'claude --model opus'` and heredoc piped to `bash` are blocked by the flat scan | [unit test] |
| REQ-09 | `bash launch-implement.sh` (fixture copy of the real script, `claude-opus-5-5` literal) is blocked; `launch-slack.sh` is allowed | [fixture replay] |
| REQ-10 | A script with `MODEL=claude-sonnet-5-5` then `--model "$MODEL"` is allowed; with `MODEL=claude-opus-5-5` it is blocked | [unit test] |
| REQ-11 | A script whose model-shaped literals are all allowed, with an Opus word only in a comment, is allowed (closed-world rule) | [unit test] |
| REQ-12 | A script whose `--model` comes from `"$1"` or an inherited env var is blocked MP-DYNAMIC under `closed_world_then_deny` | [unit test] |
| REQ-13 | A script over `script_max_kb` or a command over 64 KB is blocked MP-BIG | [unit test] |
| REQ-14 | `superclaude sprint run x --model opus` is checked like `claude` | [unit test] |
| REQ-15 | Agent `model: "opus"` in stage `default` exits 2; `model: "sonnet"` exits 0 | [unit test] |
| REQ-16 | Agent with no `model` and an agent file with frontmatter `opus` is blocked; with `sonnet` it is allowed | [unit test] |
| REQ-17 | Agent with no `model` and no frontmatter is blocked MP-INHERIT when the recorded session model is Opus-tier, and allowed when it is unknown | [unit test] |
| REQ-18 | A Skill whose SKILL.md has a forbidden `model:` is blocked | [unit test] |
| REQ-19 | A command prefix assigning `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL`, `CLAUDE_CODE_SUBAGENT_MODEL` or `ANTHROPIC_BASE_URL` is blocked MP-ENV-REDIRECT | [unit test] |
| REQ-20 | `--bare` and `--settings` containing `model`, `availableModels` or `env` are blocked in a non-elevated stage | [unit test] |
| REQ-21 | A declared `SC_MODEL_STAGE` wider than the session stage is blocked MP-STAGE-WIDEN | [unit test] |
| REQ-22 | Missing policy: launch allowed and `no_policy` logged. Malformed policy: launch blocked MP-POLICY-BROKEN; a non-launch Bash command still passes | [unit test] |
| REQ-23 | With jq absent, a command containing `claude` fails closed and a command without it passes | [integration test with PATH stub] |
| REQ-24 | On this host, p95 hook time is at most 100 ms for a non-launch Bash command and at most 150 ms for a launch, over 200 runs | [manual benchmark] |
| REQ-25 | Observe mode never exits 2 and writes `would_block` to `decisions.jsonl` with all listed fields | [unit test] |
| REQ-26 | The blocking message contains the rule id, the resolved tier, the policy path, and a "You can" line that names no `src/superclaude/` path | [unit test] |
| REQ-27 | `model-policy allow` refuses without a TTY or when `CLAUDECODE` is set | [unit test] |
| REQ-28 | A valid override makes the same blocked command pass until `expires`; an expired one does not; a `--script` grant fails if the file's sha256 changed | [unit test] |
| REQ-29 | A Bash or Write call touching the policy file, the state directory, `.claude/settings*` or running `model-policy allow` is blocked MP-TAMPER | [unit test] |
| REQ-30 | `check_launch()` raises before `Popen` for a forbidden tier in `ClaudeProcess` and the other four launchers, and passes for an allowed one | [unit test] |
| REQ-31 | The Python resolver and the hook agree on every case in `vectors.json` | [unit test] |
| REQ-32 | `superclaude model-policy lint` fails when a shipped agent, skill or command has a `model:` outside the policy | [unit test, CI] |
| REQ-33 | Installing adds `enforce-model-policy.sh` to `~/.claude/hooks/` and the three registrations to settings.json, and re-install keeps a user-edited `~/.claude/model-policy.json` | [integration test] |
| REQ-34 | `make verify-sync` passes after `make sync-dev`, and fails if the script is missing from the installer list | [integration test] |
| REQ-35 | With `jev.enabled` false, no network call is made; with it true and an unreachable endpoint, the code decision stands | [unit test with stub] |

## 8. Implementation plan (IronClaude layout)

Files to add:

- `src/superclaude/hooks/scripts/enforce-model-policy.sh`: one script, dispatching on `hook_event_name` (PreToolUse, SessionStart, UserPromptSubmit).
- `src/superclaude/hooks/model-policy.json.example`: the template above.
- `src/superclaude/cli/model_policy.py`: loader, resolver, `check_launch`, and the `model-policy` click group (`check`, `allow`, `log`, `lint`). Where the click group is registered: file not verified.
- `tests/hooks/test_enforce_model_policy*.py` (events, policy loading, override, registration) and `tests/hooks/fixtures/model_policy/` with `vectors.json` and the replay corpus.

Files to change:

- `src/superclaude/hooks/hooks.json`:

```json
{ "matcher": "^(Bash|Monitor|Agent|Task|Skill|Edit|Write|NotebookEdit)$",
  "hooks": [{"type":"command","command":"~/.claude/hooks/enforce-model-policy.sh","timeout":5}] }
```

  (appended to PreToolUse). Add `{"matcher":"*","hooks":[{"type":"command","command":"~/.claude/hooks/enforce-model-policy.sh","timeout":3}]}` to SessionStart and `{"hooks":[{"type":"command","command":"~/.claude/hooks/enforce-model-policy.sh","timeout":3}]}` to UserPromptSubmit.
- `src/superclaude/cli/install_hooks.py`: append `"enforce-model-policy.sh"` to `_FRESHNESS_SCRIPTS` (after line 96) and add `("model-policy.json.example", "model-policy.json")` to `_SEED_FILES` (line 104). How the managed-command set for the ownership merge is built from hooks.json: not verified; REQ-33 covers it.
- `src/superclaude/cli/pipeline/process.py` (before line 164) and the other launchers (`prd/models.py:283`, `sprint/summarizer.py:330`, `reflect/runner.py:508`; `eval/claude_process.py` not read): call `check_launch` first.

Sync: edit only under `src/superclaude/`. `make sync-dev` copies `hooks/scripts/*.sh` to `.claude/hooks/` and sets the execute bit (`Makefile:138-143`). `make verify-sync` diffs them and checks `_FRESHNESS_SCRIPTS` lists every script (`Makefile:307-325`, seen via search, not read in full). Never hand-edit `.claude/`. Installed text names `~/.claude/...` paths and the `superclaude` CLI only. `src/superclaude/hooks/README.md` is stale; do not use it.

Order of work:

1. Policy schema, template, and `vectors.json` (resolver rules fixed first).
2. `model_policy.py` resolver and `lint`, tested against the vectors.
3. Hook: Bash/Monitor path (tokenizer, flat scan, env rules, decision jq, log).
4. Hook: Agent/Skill frontmatter, SessionStart recorder, UserPromptSubmit, tamper class.
5. Script file read and closed-world rule.
6. `allow` / `log` CLI and override reading.
7. Launcher calls and installer/hooks.json/sync wiring.
8. Replay the incident scripts and transcripts offline; measure latency.

Rollout:

- Phase 0, observe: seed `mode: observe`; read `decisions.jsonl` for about a week.
- Phase 1, enforce `bash_launch` and `agent` (literal and param cases only).
- Phase 2, enforce script scan and inherit checks after the observe log shows no false blocks.
- Phase 3, optional Jev, only if the section 3 gate is met.

## 9. Room for version 2

- Reserve a `routing: dynamic` marker in agent, skill and command frontmatter. v1 treats it as "unpinned": the hook exempts it from `require_explicit_model` only if a named router exists in policy.
- A router is `superclaude model-policy route --stage <s> --facets <json>` and must return a model inside the stage `allow` set, so v1 still bounds it.
- Facets (task size, risk, need for reasoning) are answered by Jev Choice questions and mapped to a tier by a code table; escalation on failure needs retry-ledger data (enrichment E, item 7).
- `decisions.jsonl` keeps a `routing` field now, null in v1.
- Quality and cost judgment stays out of v1: no scoring of "best model" anywhere.

## 10. Risks and recommendation

- Two implementations (bash/jq and Python) can drift; mitigated by the shared `vectors.json` test (REQ-31).
- A model that can run a pty can still forge an override or rewrite the policy; only root-owned managed settings (availability UNVERIFIED) is stronger.
- Observed false-block risk: the seeded `default.deny` includes Opus, and `claude-gw-tier1a` resolves to Opus on this host, so `issue-worker-t1` is flagged. The observe phase exists to surface exactly this.
- `/model` and the main session's own model are not rejected: L0 and L3 only; whether `UserPromptSubmit` fires is UNVERIFIED.
- Whether `availableModels` can be injected per child via `--settings` is UNVERIFIED, so L0 stays a global ceiling, not a per-stage tool.
- **Version 1 recommendation: ship a deterministic hook, a Python launcher check and the native allowlist floor with no Jev call, starting in observe mode, because the incident was a model name written in a command, an agent parameter or a script, and plain code can read all three.**
- Not checked: session transcript shape, the Jev endpoint, `eval/claude_process.py`, and any measured latency; those are marked UNVERIFIED where they matter.
