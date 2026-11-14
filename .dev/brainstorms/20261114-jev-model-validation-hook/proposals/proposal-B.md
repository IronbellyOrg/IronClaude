# Version 1 model-policy hook: proposal B (chokepoint and evidence)

Lens: put enforcement at the fewest points, and state exactly what is seen, not seen, and why. Repository facts are cited as `path:line` only where I read the line. Claude Code hook behaviour comes from the enrichment file's docs facts (cited as "docs B1" and so on); I did not re-read those docs. Anything I could not confirm is marked UNVERIFIED.

## 1. Events and visibility

Enforcement has three points:

- **C1, launch helper.** One function in `src/superclaude/cli/model_policy.py` that every Python argv builder calls. Five builders append `--model` today: `src/superclaude/cli/pipeline/process.py:164`, `src/superclaude/cli/sprint/tmux.py:194`, `src/superclaude/cli/prd/models.py:283`, `src/superclaude/cli/sprint/summarizer.py:330`, and `src/superclaude/cli/reflect/runner.py:508` (string form). `src/superclaude/cli/reflect/commands.py:365` reads `ANTHROPIC_MODEL` as a default.
- **C2, thin hook.** One script, `model-policy-guard.sh`, dispatching on `hook_event_name`.
- **C3, native floor.** `availableModels` and `deniedModels` in user settings (docs B7). Lists from user, project and local settings concatenate, so they can only be a coarse floor, never the per-stage rule.

| # | How a model is chosen | Picked by | Visible to the hook? | Handling |
|---|---|---|---|---|
| 1 | Bash `claude` with literal `--model X` | `--model` beats settings and `ANTHROPIC_MODEL` (docs B6) | Yes: `tool_input.command` (docs B1) | C2 parses and checks |
| 2 | Bash `claude` with no flag | `ANTHROPIC_MODEL`, then settings `model` (their relative order UNVERIFIED) | Command text yes; settings file yes; hook env matches session env UNVERIFIED | C2 resolves; unresolved gives MP-03 |
| 3 | `bash launch.sh` whose file contains `--model` | File contents | No, only the path | C2 reads the file (up to 64 KB, one level); otherwise MP-03 |
| 4 | Python launcher argv (five sites above) | Caller or config value | No: no Claude Code hook fires for the launcher | C1 refuses before spawn |
| 5 | Child session started by a launcher | Child SessionStart input has `model` (docs B4) | In the child only | C2 records it; forbidden child calls are denied. A child that makes no tool call is not stopped (ceiling) |
| 6 | `claude --bare` child | Child skips all hooks (docs B8) | No, in the child | Parent command with `--bare` or `--settings` gives MP-05. No builder under `src/superclaude/cli` uses either (grep: no matches) |
| 7 | Agent tool `model` parameter | Alias only (docs B5) | Yes: `tool_input.model` | C2 canonicalises and checks |
| 8 | Agent tool, no parameter | Agent `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL` (default-only before v2.1.251), then main model (docs B5) | Frontmatter: C2 reads `~/.claude/agents/<type>.md`. Env: UNVERIFIED. Main model: SessionStart record, stale after `/model` (UNVERIFIED) | C2 resolves in the same order and checks the tier |
| 9 | Subagent `model:` frontmatter | At spawn; 11 sonnet, 2 opus, 3 gateway ids (enrichment D) | Only through the Agent call | Same as row 8. PreToolUse fires inside subagents (`src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:6`) |
| 10 | Skill `model:` frontmatter | At Skill call (1 skill, sonnet, per enrichment D) | `tool_input.skill` yes; C2 reads the SKILL.md | C2 |
| 11 | Command `model:` frontmatter | Slash command (none set in repo) | UserPromptSubmit `prompt` (docs B1, B3). Frontmatter effect on typed commands UNVERIFIED | C2 reads `~/.claude/commands/sc/<name>.md` |
| 12 | Alias env `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU,FABLE}_MODEL` | Alias redirect (docs B6) | Not in tool input; C2 reads env and settings `env` | C2 alias table; C3 covers redirects (docs B7) |
| 13 | `CLAUDE_CODE_SUBAGENT_MODEL` | Default unless `_FORCE=1` (docs B5) | Hook env only | C2 uses the documented order; C3 floor |
| 14 | `/model` typed by a person | Session model | UNVERIFIED whether UserPromptSubmit fires for built-ins (enrichment open question) | **Cannot see reliably.** C3 is the only layer covering it, and only coarsely |
| 15 | Installed mods with an `agent.spawn` hook (docs B5) | Mod code | No | **Cannot see.** Stated gap |
| 16 | Harness or managed settings, or a default changed by upgrade | Settings | Only if read | **Cannot see in general** |

Decision: C2 does not promise rows 14 to 16. The owner must accept that `/model` is covered only by the coarse C3 floor.

## 2. Machine-readable policy

Format: JSON. `jq` reads it in C2 and `json` reads it in C1, so no YAML parser is needed. Full example:

```json
{
  "version": 1,
  "mode": "observe",
  "tiers": {
    "opus":   {"ids": ["claude-opus-5-5"],   "aliases": ["opus", "claude-gw-tier1a"]},
    "sonnet": {"ids": ["claude-sonnet-5-5"], "aliases": ["sonnet", "claude-gw-tier1b"]},
    "haiku":  {"ids": ["claude-haiku-5-5"],  "aliases": ["haiku", "claude-gw-tier2"]}
  },
  "deny": [],
  "stages": {
    "blind-scoring":       {"allow": ["opus"]},
    "brainstorm-proposal": {"allow": ["sonnet", "haiku"]},
    "implement-worker":    {"allow": ["sonnet"]},
    "unscoped":            {"allow": ["sonnet", "haiku"]}
  },
  "escape_flags": ["--bare", "--settings"]
}
```

The gateway ids are the host values from enrichment D (not re-read here). The user-stated ids are `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`.

- **Canonicalisation.** Strip a trailing `[...]` suffix (for example `[1m]`), lowercase, then match against `ids` and `aliases`. A family alias (`opus`, `sonnet`, `haiku`, `fable`) resolves through `ANTHROPIC_DEFAULT_<FAMILY>_MODEL` when set. Anything else is `unmapped`, which is denied (MP-02).
- **Scope and precedence.** The user file `~/.claude/model-policy.json` is seeded from `src/superclaude/hooks/model-policy.example.json` by the existing seed mechanism (`src/superclaude/cli/install_hooks.py:104`), and is never overwritten. An optional project file at `<cwd>/.claude/model-policy.json` (cwd from docs B1) may only narrow: the effective deny list is the union, and the effective allow list for a stage is the intersection. A project stage that the user file lacks is ignored with a logged warning. In this repo `.claude/` is gitignored (CLAUDE.md), so the project file is per-checkout; the owner must choose whether IronClaude needs a versioned copy.
- **Stage declaration.** Env var `SC_MODEL_STAGE=<name>`. C1 sets it in the child environment; shell launchers prefix it. Missing or unknown stage means `unscoped`, so Opus needs a named stage.
- **Load.** C2 reads both files on each model-bearing event. There is no cache, so an edit applies at the next call.

**Missing or malformed policy, per event:**

| Event | Result | Reason |
|---|---|---|
| PreToolUse Bash, only when the command launches or names a model | Block, MP-04 | A model is chosen, so it must not pass unchecked |
| PreToolUse Agent, Task | Block, MP-04 | Every Agent call chooses a model |
| PreToolUse Skill | Block only if the skill file has `model:` | Otherwise the skill chooses nothing |
| PreToolUse Workflow, Monitor | Block | Inline scripts cannot be checked without the policy |
| UserPromptSubmit | Block only for `/model` and for `/sc:` commands with `model:` (JSON decision block) | Same rule as above |
| SessionStart | No block (docs B4 says a model cannot be rejected here); records `policy-unreadable` in session state, so later model-bearing calls in that session are blocked | Session lock |
| Edit, Write | Allowed; tamper check does not need the policy | |
| C1 Python | Raise `ModelPolicyError`, no spawn, non-zero exit | |
| `mode: observe` | Logs and exits 0 for every row above | Rollout only |

Fail-closed applies to model-bearing events only. Ordinary tool calls are never blocked by a bad policy.

## 3. Where Jev adds value

**Conclusion: v1 needs no Jev call.** Every v1 decision is either over a literal value the hook can resolve, or over a file it can read. Anything else is blocked by code, not judged.

**Code decides:** rows 1, 2, 3 (one level), 4, 6, 7, 8, 9, 10, 12 and 13 in section 1; escape flags; tamper paths; unmapped ids; override expiry; malformed policy.

**Residue code cannot decide:**
- (a) Model value built by expansion (`--model "$M"`, `--model $(cat f)`). Code blocks (MP-03) in every mode. Jev could only add a block, and code already blocks, so Jev adds nothing.
- (b) A launch inside a file the hook cannot read: deeper nesting, interpreter scripts, `uv run python x.py`. Code cannot see it. This is a ceiling, not a judgment problem. Jev reads only short text, and the enrichment reports it fails on multi-hop judgments over large documents (enrichment E).
- (c) A subagent told in natural language to "use Opus". No model field is set, so this is not a model-selection event.

**Measured-need rule.** Jev enters v1.1 only if the replay below shows either at least 3 labelled misses in residue class (b) per 300 model-bearing events, or any labelled miss where code said ALLOW and the label says BLOCK for a launch that code could see. Otherwise Jev stays out.

**If the spike happens,** the question is Choice, not Noul, because the answer has three outcomes:
- Q-J1: "This shell text starts a model-using process. Which best describes its model? A: a tier the policy forbids for stage S. B: a tier the policy allows for stage S. C: cannot tell from the text."
- Input capped at 2 KB. Option C is the "none" option. The enrichment warns that Jev flags 0 of 30 out-of-scope inputs unless such an option exists (enrichment E).
- Block only on answer A with p at least 0.7. Never allow on B.
- Latency: 70 to 500 ms, reported by a vendor-adjacent source, not measured here (UNVERIFIED on this host). Per-call timeout 1 s inside a 3 s registration.
- Cost: about $0.000025 per call, from one run of 2,011 calls costing $0.051 (enrichment E; single run, not re-read here).
- **Failure behaviour: fail open for the Jev layer only.** If Jev is unreachable, returns 429/5xx or times out, no extra block is added and the code decision stands. This is safe because Jev can only add blocks, and the code fail-closed rules (MP-03, MP-04) do not depend on Jev.

**Offline replay test plan (needed in v1 regardless).**

Data sources:
1. Session transcripts under `/home/coder/.claude/projects/-home-coder-workspaces-IronClaude/`. Glob found 503 `*.jsonl` files. A text search finds `--model` in 470 places across 94 files, but that includes discussion text. Keep only `tool_use` inputs for Bash, Agent, Skill, Workflow and Monitor. The JSON key for the model on a record is UNVERIFIED: a search for `"model":"claude-` returned no match in a sample file, so read one raw line before writing the parser.
2. Incident launchers in `.dev/`. Grep found 20 `.sh` files with a literal `--model <id>`, for example `.dev/brainstorms/20261113-163248-panel-collaboration/launch-debate.sh`.
3. The five C1 argv builders in dry-run mode: build argv, do not spawn.

Labelling: each `tool_use` input containing a model-bearing token becomes one case. The label is the decision the rule in force on that date requires, with its rule id. The author labels all cases. A second reader, given only the policy and rule text (not hook output), labels a random 20 percent. Disagreements change the written rule first, then the case. Labels are frozen before the hook runs.

Replay: a script in `tests/hooks/` feeds each recorded `tool_input` on stdin with its recorded `cwd`, with no network and no `claude` process. Agent and Skill frontmatter comes from a frozen copy of the agent and skill trees. Mapping transcript time to a git commit is UNVERIFIED; if it fails, use the current tree and say so in the report. Output: a confusion matrix per event type and a list of misses.

## 4. Rejection and override

**Message the model sees** (PreToolUse exit 2, stderr; docs B2 says stderr is shown to Claude):

```
Model policy: blocked (rule MP-01, stage "brainstorm-proposal").
Blocked: claude -p with model claude-opus-5-5 (tier opus).
Why: stage brainstorm-proposal allows only sonnet and haiku (model-policy.json, stages.brainstorm-proposal).
You can: rerun with a sonnet or haiku model, or ask the person to record an override. Do not edit model-policy.json or the override file.
```

The format copies the `Blocked: / Why: / You can:` lines that `src/superclaude/hooks/scripts/launch-level-guard.sh:126` prints.

Rule ids: MP-01 tier forbidden for stage; MP-02 denied or unmapped id; MP-03 model not literal, or script unreadable or over 64 KB; MP-04 policy missing or malformed; MP-05 escape flag; MP-06 tamper path; MP-07 override command from inside a session.

**Exit codes and output:**
- PreToolUse: exit 2, stderr.
- UserPromptSubmit: `{"decision":"block","reason":"..."}` (docs B3; the reason shows to the user).
- C1: `ModelPolicyError`, non-zero exit.
- Every denial appends one line to `~/.claude/state/model-policy/denials.jsonl`.

**What the user sees.** For PreToolUse, the reason goes to Claude (docs B2). Whether the transcript shows hook stderr to the user is UNVERIFIED. So `superclaude model-policy report` prints the denials log as the user-visible record.

**Override record:**
- Created only by `superclaude model-policy override --stage S --model M --hours H --reason "..."`, run from a terminal. The CLI refuses when stdin is not a TTY or when `CLAUDECODE` is set. `src/superclaude/cli/pipeline/process.py:171` says child `claude` processes carry this variable, so it is a usable session marker.
- Stored in `~/.claude/state/model-policy/overrides.jsonl`, one object per line:

```json
{"id":"MPO-20261114-01","stage":"blind-scoring","model":"claude-opus-5-5","granted_by":"coder","created_at":"2026-11-14T10:00:00Z","expires_at":"2026-11-15T10:00:00Z","reason":"owner approved one-off Opus scoring run"}
```

- Fields: `id`, `stage`, `model` (canonical tier or id), `granted_by` (OS user), `created_at`, `expires_at` (default 24 h, maximum 168 h), `reason` (at least 20 characters). Expired rows are ignored. Each use appends to `overrides-used.jsonl` with the launch id.
- **Against self-creation:** C2 denies Bash that names `model-policy override` or the override path (MP-07) and denies Edit or Write to that path (MP-06). The CLI also writes a hash-chained line to a journal. `superclaude model-policy audit` reports override rows with no journal line. That is detection, not blocking (see section 5).

## 5. Bypass resistance

| Route | Status | Note |
|---|---|---|
| `sudo`, `nice`, `timeout`, `env`, `command`, `exec` wrappers | Blocked | Skipped by the tokenizer, as in `require-orca-worktree-agent.sh:23-25` |
| `bash -c "claude ..."`, `sh -c`, `eval` | Blocked | Scan the string one level, closing the case that require-orca leaves open (`:40-41`) |
| `--model $M` with `M` set earlier | Blocked (MP-03) | Unexpanded value in a model-bearing command |
| `--model $(cat f)` | Blocked (MP-03) | Command substitution |
| Script written, then run (`cat > x.sh <<EOF`; `bash x.sh`) | Blocked when the file exists at run time | Ceiling if the script is generated during the run |
| Heredoc piped to a shell | Ceiling | As `require-orca-worktree-agent.sh:43-44` |
| `python -c "subprocess..."` naming `claude` and `--model` | Blocked for literal text (MP-03); ceiling for constructed text | |
| `ANTHROPIC_MODEL` in settings `env` | Detected at next launch (settings read) | Harness-set env: ceiling |
| `--settings`, `--bare` | Blocked (MP-05) | |
| Edit or Write to the policy file | Blocked (MP-06) | Matcher `Edit\|Write` |
| Bash redirect, `tee` or `sed -i` naming the policy path | Blocked (MP-06) | Named-path rule |
| `cp` from elsewhere, or a `python` script writing the file | Ceiling; detected by `superclaude model-policy audit` (hash against install record) | Same OS user as the model |
| Removing the hook from settings, or `disableAllHooks` | Blocked when the text names `disableAllHooks` or `.claude/hooks` (enrichment C says launch-level-guard does this); otherwise detected by install verify | Editing settings.json by Bash: ceiling |
| `/model` typed by a person | Ceiling for C2; C3 floor only | |
| Monitor tool running `claude` | Blocked once Monitor is in the matcher | |
| Workflow tool inline script | Blocked (MP-03) when a model is not a literal | |
| Subagents | Blocked | PreToolUse fires inside subagents (`require-orca-worktree-agent.sh:6`) |
| Child with no tool call | Ceiling | Its answer is produced; only the parent launch is checked |
| Mod with `agent.spawn` changing the model (docs B5) | Ceiling | |

## 6. Time cost per event

Estimates, UNVERIFIED until REQ-31 measures them.

| Event (registration) | Typical ms | Worst ms | Timeout |
|---|---|---|---|
| PreToolUse Bash (fast path exits early when no model token is present) | 10 to 30 | 150 (64 KB script scan) | 3 s |
| PreToolUse Agent, Task, Skill, Workflow, Monitor | 10 to 20 | 60 | 3 s |
| PreToolUse Edit, Write | 5 | 10 | 1 s (as `freshness-pre-edit.sh`) |
| UserPromptSubmit | 5 to 15 | 40 | 3 s |
| SessionStart | 5 to 15 | 40 | 3 s |
| C1 helper per launch (in-process) | 5 | 30 | none |
| Jev (not in v1) | 70 to 500 (reported) | UNVERIFIED | 3 s |

Bash already runs four PreToolUse registrations (`src/superclaude/hooks/hooks.json:96`, `:106`, `:116` and `:126`). C2 makes five. If a timeout fires, the platform's behaviour is UNVERIFIED (docs B9 covers only non-zero, non-2 exits), so the design relies on the hook staying well under its timeout.

## 7. Test plan and numbered requirements

Verification methods: [unit], [integration], [fixture replay], [parity], [manual].

- **REQ-01** A Bash `claude` command with a literal `--model` for a forbidden tier exits 2 with MP-01. [unit]
- **REQ-02** The same command with an allowed tier exits 0. [unit]
- **REQ-03** A `claude` launch with no `--model` is checked against the resolved settings model. [unit, fixture settings]
- **REQ-04** An `ANTHROPIC_MODEL=` prefix or `export` in the same command is resolved and checked. [unit]
- **REQ-05** A model-bearing command with a shell expansion in the model value exits 2 with MP-03. [unit]
- **REQ-06** `bash x.sh` where `x.sh` contains a forbidden `--model` exits 2. [fixture replay]
- **REQ-07** `bash x.sh` where `x.sh` is over 64 KB or unreadable exits 2 with MP-03 in a model-bearing context. [unit]
- **REQ-08** `bash -c`, `sh -c` and `eval` strings containing a forbidden launch exit 2. [unit]
- **REQ-09** An Agent call with `model: opus` in a stage allowing only sonnet exits 2, and `sonnet` exits 0. [unit]
- **REQ-10** An Agent call with no model parameter resolves the named agent's frontmatter. [fixture replay]
- **REQ-11** An Agent call with no parameter and no frontmatter uses `CLAUDE_CODE_SUBAGENT_MODEL`, then the SessionStart record. [unit]
- **REQ-12** A Skill call whose skill frontmatter names a forbidden model exits 2. [unit]
- **REQ-13** A `/sc:<cmd>` prompt whose command file names a forbidden model returns a JSON block decision. [unit]
- **REQ-14** After SessionStart records a forbidden model, a later model-bearing call in that session exits 2. [integration]
- **REQ-15** A Workflow input containing a forbidden model literal exits 2. [unit]
- **REQ-16** An Edit or Write to the policy, override, or hook file exits 2 with MP-06. [unit]
- **REQ-17** An override command named in Bash exits 2 with MP-07, and the CLI refuses when `CLAUDECODE` is set or stdin is not a TTY. [unit]
- **REQ-18** `--bare` or `--settings` in a model-bearing launch exits 2 with MP-05. [unit]
- **REQ-19** A missing user policy blocks model-bearing events with MP-04 and allows other events. [unit]
- **REQ-20** Malformed JSON, a wrong version, or an unknown tier name follows the same per-event rules as REQ-19. [unit]
- **REQ-21** A project policy cannot allow a model the user policy denies. [unit]
- **REQ-22** An unmapped model id is denied (MP-02) even in the `unscoped` stage. [unit]
- **REQ-23** In `observe` mode a denial is logged and exits 0; in `enforce` mode it exits 2. [integration]
- **REQ-24** Every block message contains `Blocked:`, `Why:`, `You can:`, the rule id, the stage and the policy key path. [unit, golden text]
- **REQ-25** No block message names a path under `src/superclaude/`. [unit]
- **REQ-26** A valid unexpired override allows exactly its stage and model, and expired overrides are ignored. [unit]
- **REQ-27** Each override use appends one line to `overrides-used.jsonl`. [unit]
- **REQ-28** Each of the five C1 argv builders refuses a forbidden stage before spawning. [integration, dry-run argv]
- **REQ-29** A repository test fails if a literal `"--model"` appears in an argv builder outside the helper module. [unit, grep or AST]
- **REQ-30** The hook and the Python helper return identical decisions on a shared fixture table. [parity]
- **REQ-31** Bash p95 hook latency is at most 50 ms on the fixture corpus. [fixture replay, measured]
- **REQ-32** Install copies `model-policy-guard.sh` to `~/.claude/hooks/` and the seed file only when absent. [integration, `tests/cli/test_install_hooks.py`]
- **REQ-33** `make verify-sync` passes after `make sync-dev`, and no `.claude/` path is staged. [manual, `tests/cli/test_verify_sync_hooks.py`]
- **REQ-34** On the labelled replay, no case labelled BLOCK is allowed in enforce mode, and false positives are reported. [fixture replay]
- **REQ-35** The v1 hook makes no network call and does not reference Jev. [unit, grep]
- **REQ-36** The hook never returns `updatedInput`, so it never rewrites a model. [unit]

## 8. Implementation plan

**Add:**
- `src/superclaude/hooks/scripts/model-policy-guard.sh`: thin hook; the tokenizer is copied from `require-orca-worktree-agent.sh`, with a parity test against it.
- `src/superclaude/hooks/model-policy.example.json`: the seed file from section 2.
- `src/superclaude/cli/model_policy.py`: helper with `resolve`, `check`, `build_flag`, `ModelPolicyError`, and the `override` and `audit` subcommands.
- `tests/hooks/test_model_policy_guard.py`, `tests/hooks/test_model_policy_guard_replay.py`, `tests/hooks/fixtures/model_policy/` (fixtures and replay cases), `tests/cli/test_model_policy.py`.

**Change:**
- `src/superclaude/hooks/hooks.json`: add the registrations below.
- `src/superclaude/cli/install_hooks.py`: add `"model-policy-guard.sh"` to `_FRESHNESS_SCRIPTS` (`:42`; the comment at `:62` to `:64` requires every `hooks/scripts/*.sh` to be listed) and `("model-policy.example.json", "model-policy.json")` to `_SEED_FILES` (`:104`).
- The five argv sites (`pipeline/process.py:164`, `sprint/tmux.py:194`, `prd/models.py:283`, `sprint/summarizer.py:330`, `reflect/runner.py:508`) and `reflect/commands.py:365`, routed through `model_policy.build_flag`.
- `tests/cli/test_install_hooks.py` and `tests/cli/test_verify_sync_hooks.py`: extended for the new script and seed.
- `src/superclaude/hooks/README.md`: the enrichment says it is stale (still names `plugins/superclaude/hooks/`); fix it in step 5.

**Registration JSON** (new entries in `hooks.json`):

```json
"PreToolUse": [
  {"matcher": "^(Bash|Agent|Task|Skill|Workflow|Monitor)$",
   "hooks": [{"type": "command", "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 3}]},
  {"matcher": "Edit|Write",
   "hooks": [{"type": "command", "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 1}]}
],
"UserPromptSubmit": [
  {"hooks": [{"type": "command", "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 3}]}
],
"SessionStart": [
  {"matcher": "*", "hooks": [{"type": "command", "command": "~/.claude/hooks/model-policy-guard.sh", "timeout": 3}]}
]
```

The installer's ownership check matches by command path (`install_hooks.py:126`, `:301`), so one script across four registrations merges cleanly.

**Sync rules.** Edit only `src/superclaude/`, then run `make sync-dev` and `make verify-sync`. Never edit `.claude/` by hand. The hook and policy text name only `~/.claude/...` paths, never `src/superclaude/`. The Python helper is package code, so it may name package paths.

**Order of work (8 steps):**
1. Fix the tier table and write the example policy and fixture table. Read one raw transcript line to confirm the model key.
2. Build `model_policy.py` (resolve, check, build_flag) with unit tests.
3. Route the five argv sites and `reflect/commands.py:365` through the helper; add the REQ-29 grep test.
4. Build `model-policy-guard.sh` with the copied tokenizer.
5. Register in `hooks.json`, `install_hooks.py`, seed file; run `make sync-dev` and `make verify-sync`; fix the README.
6. Build the replay harness, label the corpus, and measure latency (REQ-31, REQ-34).
7. Run in observe mode for two weeks, or until 200 model-bearing live events are logged, with the false-positive count reviewed.
8. Flip to `enforce`, add the override CLI, and write the owner-facing guide.

**Rollout:** the seed ships with `"mode": "observe"`. The owner flips it to `enforce` by hand, after reviewing the denials log and the replay result. The model cannot flip it, because MP-06 blocks writes to the policy file.

## 9. Room for version 2

- A `routing: dynamic` field in an agent, skill or command exempts it from the fixed-model check only, and must name a router (`router: <name>`).
- Each stage gains a `candidates` list. A router chooses from it, and the hook still checks the chosen model against the same `allow` list, so router output is a request, not an allow.
- The C3 native list stays as the global floor.
- Jev returns in v2 only as a Choice router, under the same block-only rule.
- The v1 replay corpus becomes the v2 evaluation set.

## 10. Risks and recommendation

1. `/model` is invisible to C2 (UNVERIFIED whether UserPromptSubmit sees it); only the coarse C3 floor covers it.
2. The recorded main model goes stale after `/model`; mitigate by re-recording on any `/model` prompt.
3. Bash gains a fifth PreToolUse process per call; measure before enforce.
4. The copied tokenizer can drift from require-orca; a parity test is required.
5. The helper and the hook both read the JSON; REQ-30 keeps them aligned.
6. The model runs as the same OS user, so an indirect write to the policy or override file is detected, not blocked.
7. Malformed policy blocks all Agent calls until fixed; the seed and `superclaude model-policy audit` make that visible.
8. The project policy sits in gitignored `.claude/`; the owner must choose a versioned path.

**Version 1 recommendation:** build one thin Claude Code hook and one Python launch helper that both read one JSON policy and fail closed on any model-bearing event they cannot resolve, with no Jev call, rolled out in observe mode first.

**Not checked:** the docs facts (docs B1 to B9) are from the enrichment file, not re-read; the gateway ids and the transcript model key are unverified; no latency was measured.

| Status | Result |
|---|---|
| DONE | Wrote the version 1 proposal from the brief, the enrichment file, the hook registry, the installer, the precedent hooks, and the `--model` call sites. |
| DONE | Confirmed by grep that no launcher under `src/superclaude/cli` uses `--bare` or `--settings`. |
| NEXT | Owner decides the project policy location and whether `/model` is accepted as C3-only coverage. |
