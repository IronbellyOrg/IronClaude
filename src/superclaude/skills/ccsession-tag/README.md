# ccsession + model shim

Two small tools for Claude Code that work together:

1. **ccsession** gives your Claude sessions names, so you can leave one and come
   back to it later by typing its name instead of hunting through a list of
   random IDs.
2. **The shim** makes the other models on your LiteLLM gateway (GPT, Grok, Kimi,
   GLM, Qwen) show up in Claude Code's own model picker, which normally refuses
   to list them.

Neither one changes anything on your gateway. Both run entirely on your machine.

---

## What is in this package

| File | What it is |
|---|---|
| `ccsession` | The `ccsession` shell command |
| `ccsession-orca` | Orca's Claude command: asks for a session name only when Claude starts with no task, no name and no resume (a new session without a name is auto-named, except in print mode, with `CCSESSION_AUTOSTART=0`, and for launches that start no session), then runs ccsession |
| `local-gateway-alias-proxy.py` | The shim, a small local proxy |
| `ccsession-models.json` | Profiles and the curated model list (data only) |
| `models.py` | Checks for, validates, and caches the latest model data |
| `install.sh` | Standalone fallback when you only have this skill folder |
| `ccsession.env.example` | Template for your gateway address and key |
| `hooks/session-start.sh` | Records each session's ID so names can resume it |
| `hooks/session-name.sh` | Copies a name given with Claude Code's `/rename` into ccsession's list |
| `SKILL.md` | Marks this folder as a skill so it installs; the old `/ccsession-tag` command is retired (use `/rename`) |
| `README.md` | This file |

---

## Before you install

- macOS or Linux only. The optional gateway shim uses `python3`, `curl`, and `lsof`.
- Claude Code already installed and working.
- `~/.local/bin` on your `PATH`.
- The shim part only matters if you have a LiteLLM gateway. Session naming works
  fine without one.

---

## Install from IronClaude

Install IronClaude normally (or update it from a checkout):

```bash
superclaude install
# In an IronClaude checkout, ./update.sh also refreshes ccsession.
```

This installs the skill, links `~/.local/bin/ccsession` and
`~/.local/bin/ccsession-orca`, seeds
`~/.claude/ccsession.env` if absent, and registers its SessionStart,
UserPromptSubmit and SessionEnd hooks.
`superclaude update` and `./update.sh` refresh the packaged files without
overwriting your env file. No gateway is required for session naming.

**Standalone fallback:** If you copied only this skill folder, run its
`./install.sh` from inside that folder. You do not need it after
`superclaude install`.

Then check it:

```bash
ccsession --help
```

---

## Set up your gateway

Only needed if you want the extra models. Session naming works without it.

**1. Find your gateway address.** This is your own LiteLLM server, not
Anthropic. Take its address and port, then add `/cli` on the end:

```
http://192.168.1.50:4000/cli
```

That `/cli` suffix is required. Leave it off and every request fails with what
looks like an authentication error.

**2. Get your key.** It is the key your LiteLLM server issues, usually starting
with `sk-`. If you did not set up that server, ask whoever did.

**3. Put both in your settings file.** Open `~/.claude/ccsession.env` (the
installer created it) and set these two lines:

```bash
export ANTHROPIC_BASE_URL=http://your-gateway:4000/cli
export ANTHROPIC_AUTH_TOKEN=sk-your-key
```

**4. Check it before opening a session:**

```bash
set -a; . ~/.claude/ccsession.env; set +a
curl -s -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" "$ANTHROPIC_BASE_URL/v1/models" | head -c 300
```

A list of model names means you are done. An error means the address or the key
is wrong. Nothing else in this tool will work until that command returns models.

**5. Start a session with the models available:**

```bash
ccsession notes --shim
```

Then run `/model` inside Claude. Your gateway's models should be in the list.

Keep `~/.claude/ccsession.env` private. It holds a real credential, it is never
part of this package, and it belongs in no git repository.

---

## Everyday use

```bash
ccsession notes              # start or resume the session named "notes"
ccsession notes --shim       # same, but with the extra gateway models available
ccsession --list             # every named session on this machine
ccsession --here             # named sessions of this worktree (and of removed ones)
ccsession --here --all       # named sessions of every worktree of this repo
ccsession --rm notes         # forget the name (the conversation itself is kept)
ccsession notes --claude-args "fix it"
                             # everything after --claude-args goes to Claude Code
                             # as given, never read as a name or a ccsession option
```

### One name, given either way

A session has one name, shown in ccsession's list, in Claude Code's prompt box
and `/resume` picker, and on the Orca tab:

- **`ccsession <name>`** starts or resumes the session with that name, and
  gives Claude Code the same name (`--name`).
- **`/rename <name>`** inside Claude Code names a session you started without
  one, or renames it. It is a built-in command, so it costs no tokens. The
  name joins ccsession's list (the old one leaves it) and `ccsession <name>`
  reopens it. Claude Code runs no hook at a rename itself, so the list and the
  Orca tab pick it up at your next message, or when you quit.

Names may contain spaces and any other characters except tabs, newlines and
other control characters, up to 245 bytes, where each `/` or `%` (and a
leading `.`) counts as 3: 245 letters of plain English text, or about 81
characters of Chinese or Japanese. A longer `/rename` name is not listed. Quote a name with spaces in the shell: `ccsession "my work"`; the
session-name question needs no quotes. A name that starts with `-` would be
read as an option, so reopen it with `ccsession --name -wip` (`--name` takes
any name). A name another saved session already has gets `-2` (then `-3`...)
in ccsession's list. Claude Code's automatic names are not listed; only names
someone gave.

`superclaude install` also adds, once, the names given with `/rename` before
ccsession kept them. The old `/ccsession-tag` command is retired: use
`/rename`.

Names are per repo. Every worktree, branch and copy of a repo (same `origin`)
shares one list, so a session named in one worktree resumes from any other,
and a fresh copy of the repo still sees its names. The same name in two
different repos points at two different conversations. A folder that is not a
git repo keeps its own list, as before.

The list you see follows the worktree, like Claude Code's own `/resume`
picker. Claude Code continues a resumed conversation in the folder you start
it in, so a session that was working in another worktree would make its edits
and commits in this one. `ccsession --here` and the session-name question
therefore show:

- the sessions that were started in this worktree;
- under "Sessions whose worktree was removed", the sessions whose worktree no
  longer exists, with the folder they were started in: they have nowhere else
  to go, so they are listed in every worktree;
- a count of the sessions that were started in another worktree (or copy of
  the repo) that still exists. `ccsession --here --all`, or `*` at the
  question, lists them.

A session's folder is the one it was started in, which Claude Code names its
transcript folder after (`~/.claude/projects/<folder with every character
other than a letter or digit as ->`), as its own picker does. The working
folders the transcript records follow the session's shell when it changes
directory, so they are not used alone. A session from another worktree still
resumes by name from anywhere, and ccsession then warns which worktree it was
started in.

Older versions kept one list per folder. The first run of this version copies
those names into their repo's list, once per old list (`ccsession
--migrate-names`, which every install also runs, retrying only lists that
failed). The old files stay but drop out of `--list`, nothing is overwritten,
the most recently used folder keeps a shared name, and another session with
the same name is copied as `<name>-<folder>` (then `-2`, `-3`). Labels saved
with a leading `.` (hidden files before this version) are moved to the new
file name first, and copied to their repo's list too when their old list was
already copied.

A labeled session's name, and its Orca tab, belong only to the Claude Code
that ccsession started, in that folder, including the conversations `/clear`
starts in it. A `claude` started inside it inherits its environment (for
example a pipeline's `claude -p`, in that folder or another worktree) but
never takes the name or the tab over: ccsession replaces itself with Claude
Code, so its process id (the start of `CCSESSION_LAUNCH_ID`) is that Claude
Code's, and the hooks check which Claude Code runs them. A `ccsession` run
from inside Claude Code (its Bash tool) leaves the Orca tab alone, and an
untagged one does not take the session's label either.

---

## Claude launched from Orca

When you pick Claude directly in Orca (the + button, a new workspace or branch
with Claude, the agent picker), Orca runs plain `claude`, which skips
ccsession. To route those launches through ccsession, set Orca's
**Settings > Agents > Claude > Command** to the absolute path of the link, for
example:

```
/home/coder/.local/bin/ccsession-orca
```

Orca accepts one executable there, with no arguments. Each Orca launch then
runs through the shim and passes Orca's own arguments (its prompt,
`--prefill <text>`, resume flags) to Claude Code unchanged, after ccsession's
`--claude-args`, so a prompt is never read as a session name.

### Orca session launches

For a new ccsession-backed Claude session, choose **Claude (CLI)**, never **New Terminal**.
Load the version-matched `orca-cli` guide before choosing commands. Use `agent launch`
in an existing worktree or `worktree create --agent` for a new checkout; request
`--surface terminal` when a CLI session is required. `terminal create` is for shells,
not agent sessions. This requires the `ccsession-orca` Claude command configuration above;
choosing an agent does not configure ccsession automatically.
For supervised workers, keep `worker-start` and the dispatch preamble authoritative;
this rule does not replace supervised dispatch or commands' internal Agent-tool subagents.

Every Orca worktree gets an agent: create it with `worktree create --agent` (supervised workers
use `worker-start`, and a supervised worker follows its worker contract, which forbids it from
creating worktrees), and never create a worktree for your own use. The session that creates a
worktree becomes its orchestrator, or a coordinator under another orchestrator, and
owns its agent(s). A hook blocks `orca worktree create` without `--agent`.

#### The one question rule

The session-name question is asked **only when Claude starts with no task, no
name and no resume**, and someone can answer it (stdin, stdout and standard
error are all a terminal, and `CCSESSION_AUTOSTART` is not `0`). The question lists this
worktree's saved sessions (as `ccsession --here` does; `*` lists every
worktree's) and reads:

```
Session name (Enter = auto-named, Ctrl+C = cancel; auto-named after 30s):
```

- **A name** starts or resumes the session of that name. Spaces are fine, and
  a name starting with `-` is passed on as `--name`.
- **Enter**, or no answer within the time limit, starts the session under an
  automatic name (below), so with the default limit the tab does not wait at
  the prompt for ever.
- **Ctrl+C** cancels: `ccsession-orca` exits with status 130 and Claude is not
  started, so you are back at the shell.
- **Text that cannot be a name** is not an error and not a name. A line that
  holds a control character (a tab) among other text (a line of only spaces
  or tabs is a blank answer, like Enter), is too long to save as a name (more than
  245 bytes of file name, where each `/` or `%`, and a leading `.`, count as 3
  bytes), or is several lines pasted (the first line not blank) becomes
  Claude's first message (after `--` when it starts with `-`), and the session
  is auto-named from its first words. A normal line, spaces included, stays a
  name.

What each launch does:

| Launch | Question | Name Claude gets |
|---|---|---|
| The Claude button, a plain relaunch of a new tab | Asked | The name typed; an automatic name on Enter, on the time limit, or on keys typed ahead (no question then) |
| A prompt, `--prefill <text>`, or `--session-id <id>` (an agent or worktree launch) | No | An automatic name made from the prompt's first words (from the folder and a stamp alone when there is no prompt text, as with `--session-id`); Orca's arguments reach Claude unchanged and in their own order |
| `CCSESSION_NAME=<name>` in the environment (a worker start) | No | That name (see below) |
| Claude's own `--name`, `-n` or `--name=` | No | Left for Claude as given; nothing is added |
| `--resume`, `-r`, `--continue`, `-c`, `--fork-session`, `--from-pr` | No | None: the session names itself |
| A tab Orca relaunches after a restart, with a recorded session | No | The tab's own session is reopened (below) |
| No terminal and no task or name (a worker start with nothing given) | No (nobody to ask) | An automatic name |
| `-p` / `--print` (print mode) | No | None: the run is untagged |
| `CCSESSION_AUTOSTART=0` | No | None: the launch is untagged |
| `--version`, `--help`, and Claude's own subcommands (`mcp`, `doctor`, `update`...) | No | None: they start no session |

The rows above describe a launch with no `CCSESSION_NAME`. A valid
`CCSESSION_NAME` is an explicit instruction. It is passed as `--name` even with
`-p`, `--version`, a subcommand or `CCSESSION_AUTOSTART=0`, so set it only on a
launch that starts a new session. Do not combine it with a resume option (with
`--resume <id>` and a name that is also a saved label, Claude would get two
`--resume` arguments) or with Claude's own `--name` (Claude would get two
`--name` arguments).

`--fork-session` and `--from-pr` are resume options like `--resume`, so they
skip the question and get no name. `--session-id` starts a new session under an
id you choose: it carries a task, so it skips the question and is auto-named.

#### Automatic names

A launch that needs a name and was given none gets one from
`ccsession --auto-name [<task text>]`:
`<folder>-<up to four words of the task>-<MMDD-HHMMSS>-<4 hex digits>`, for
example `my-repo-fix-the-login-bug-1105-091530-3a7f`. The folder is cut to 20
characters and each word to 12, and only letters, digits and hyphens are kept,
so whatever the text holds (quotes, `$(...)`, a path, control characters) the
label is one safe, valid name, well under the 245-byte limit. It is checked
against the names already saved for this repo (a saved name resumes its
session), and the stamp ends in a random part, so launches do not share one in
practice: a label that matches a saved name gets `-2`, then `-3`. A name is
saved only when the session starts, so two launches in the same second rely on
the random part. If the name list
cannot be written, no name is made and Claude starts untagged: a launch never
stops here. The name is Claude Code's name for the session too, and joins
`ccsession --here` once the session has started and the hooks have recorded it.

#### Time limit

The question gives up after 30 seconds (the time runs again after a `*`, which
lists every worktree's sessions and asks again). Orca fails a supervised worker whose
Claude is not ready within 60 seconds, so a worker that was started with
neither a task nor a name still starts. Change the limit with
`CCSESSION_ASK_TIMEOUT=<seconds>` (`0` waits for ever, and the hint then drops
the time). The limit lives inside the question itself (`ccsession --ask`), so
every caller of `--ask` has it, not only `ccsession-orca`. `ccsession-orca`
removes both this limit and `CCSESSION_NAME` from the environment it starts
Claude Code with; a plain `ccsession` run leaves its environment as it is.

#### `CCSESSION_NAME`: how an orchestrator names a session

Set `CCSESSION_NAME=<name>` in the launch environment to name a session
without a prompt. A valid name (the rules above) is used as the session's name
and nothing is asked. An invalid one (a control character, or too long to save) is dropped with a
warning on standard error, and the launch is then handled as if none was
given: Claude still starts. A name equal to a saved label of this repo resumes
that session, with a visible `Resuming '<name>'` line, while its conversation
is still saved; if the conversation is gone, a new session starts under that
name. A launch with a valid
`CCSESSION_NAME` is never treated as a relaunch to reopen.

**Orchestrators should always pass the task or a name in the launch** (a prompt
argument, or `CCSESSION_NAME`). Without either, on a terminal the worker waits
for the question until the time limit; with no terminal it is auto-named at
once.

#### Known exception

Claude Agent Teams starts its teammates from inside Claude Code, without
running `ccsession-orca`, so ccsession cannot name those sessions or ask about
them. This is the one launch path this command does not cover. It is listed as
a follow-up to issue 315.

### Reopening a tab after a restart

After a workspace restart Orca relaunches each Claude tab by running this
command again, with only its own options (for example
`--dangerously-skip-permissions`) and nothing that says which session the tab
ran. So the tab reopens its own session instead of asking:

- The hooks remember, for each Orca tab (its `ORCA_PANE_KEY`, which Orca keeps
  across restarts), the session the Claude Code that ccsession launched there
  runs, with the folder and the terminal it ran in. They update it at every
  session start and message, so `/clear` and `/resume` move it along. The
  record is `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/<pane key>`,
  with each `:` of the pane key written as `+` (for example `tab-1+leaf-1`).
- When `ccsession-orca` would ask the question, Orca passed only options, and
  the tab's recorded session is still saved, was started in this same folder
  and ran in another terminal (Orca relaunched the tab), it resumes that
  session: by its name when it has one in this repo's list, else by its id.
- The reopen runs first, before the question and before any automatic name.
  Everything else follows the one question rule above. A new tab or split pane
  has no record and is asked. A launch with a prompt, `--prefill`, a name
  (`CCSESSION_NAME` or Claude's `--name`) or a session choice (`--resume`,
  `--continue`, `--session-id`, `--fork-session`, `--from-pr`) never reopens:
  it is named, or resumed, as described above. Running `ccsession-orca` again
  by hand in the same terminal is asked. A session whose conversation was
  deleted, or that was started in another folder, falls back to the question.
- A session belongs to one tab: when another tab opens it, the first tab
  forgets it, so two tabs never reopen the same session.

ccsession prints its own status lines (`[ccsession] ...`) on standard error, so
standard output carries only Claude's output and the results of commands such as
`--ask`, `--auto-name` and `--list`; on a terminal both streams look the same.

The question itself is `ccsession --ask [<hint>]`: it prints the list and the
question on the terminal and only the answer on standard output. A `@LIMIT@`
in the hint becomes the time limit in seconds. When there is no limit, the hint
is cut at the first `; ` that has `@LIMIT@` after it; a hint without such a
`; ` keeps `@LIMIT@` as written. Without a hint the question reads
`Session name (Enter = untagged, Ctrl+C = plain shell; gives up after 30s):`,
for callers where an empty answer means an untagged session. Exit status:

- `0`: a name, or an empty line for a blank answer (Enter);
- `1`: it did not ask (no terminal, or keys already waiting), got no answer
  within `CCSESSION_ASK_TIMEOUT` seconds (default `30`; `0` or a value that is
  not a whole number of seconds, such as `1.5` or `30s`: no limit), or input
  ended;
- `3`: the typed text cannot be a name (a control character among other text,
  over 245 bytes, or several lines pasted after a first line that is not
  blank; the 245-byte rule is the one above; a line of only spaces or tabs is a
  blank answer, status `0`, and so is a pasted block that starts with a blank
  line). It is printed as
  typed, as a first message for Claude;
- `130`: Ctrl+C.

`ccsession --check-name <name>` exits 0 when the name is valid, else 1.

### Tab title in Orca

In any Orca terminal (`ORCA_PANE_KEY` set), ccsession sets the tab title to
`<label> · Claude Code`, or `Claude Code` for an untagged session, and starts
Claude Code with `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` so it keeps that title.
Orca's web and mobile server treats a pane as running Claude only while its
title contains the word "claude"; Claude Code's own title is its AI
conversation name, so without this a resumed session dropped out of the Orca
Web sidebar and the phone. Other terminals keep Claude Code's own titles.

Because Claude Code's own title is off, a `/rename` reaches the tab through
Orca: at your next message the hook sets the tab title to
`<new name> · Claude Code` (`orca terminal rename`). When you leave Claude Code
(or, after a crash, at the next ccsession launch in that tab) ccsession takes
that title off again, but only while the tab still shows it: a name you typed
into Orca since is kept. Renaming the tab in Orca still works, but only
changes the tab: Claude Code and ccsession never see that name, so use
`/rename` to rename a session.

---

## Tiers (Coder workspaces)

In a Coder workspace whose env file defines tier windows (`T<N>_WINDOW`),
ccsession runs in tier mode. The workspace env file
(`/etc/aidev02/aienv.d/defaults.sh`) names each tier's models in order and
their context windows; ccsession reads it on every launch, so a changed file
applies to the next launch in any terminal or in Orca, with no new shell.

```bash
ccsession notes                       # default tier (CCSESSION_DEFAULT_TIER)
ccsession notes --tier tier1a         # a specific tier (tier1a and 1a both work)
ccsession notes --model gpt-6-astra   # start on this model; fallback within its tier
```

| | What happens |
|---|---|
| Picker (`/model`) | Shows the tiers (Tier 0, Tier 1a, ...), each with its models; with `+models` in the owner's rule, also each model on its own, in `CCSESSION_MODEL_ORDER` order |
| Failover | Out-of-usage errors on the existing switch list (`are cooling down`, `auth_unavailable`, `usage_limit_reached`, billing, overloaded, retired or unrouted model, outdated provider login) switch immediately. Other 408, 429, 500, 502, 503 and 504 replies and cut-off error replies count per model across the shim's sessions: the first two go back for Claude Code to retry; the third switches the same request to the next model. Malformed requests and main-model context errors never count or switch. An unreachable gateway never switches |
| Cooldown | Out of usage: `Retry-After`, else 1 hour. Repeated server errors: 5, 10, 20, 40, then 60 minutes (cap). Each expiry permits another try; a success resets the count and growing duration. A streamed request with no start of a reply in 5 minutes switches immediately and uses the same growing park |
| Context | The tier window (`T<N>_WINDOW`) for the whole session; a backup smaller than that is never used |
| `--model <name>` | Window from the tier slot that holds that model (a `[1m]` suffix is accepted); for a model in no tier, 1M if it is on the `one_million_context` list, else 200K, with a warning |
| `--profile` | Not used in tier mode (refused with a pointer to `--tier` and `--model`) |
| Shim | Always on |

A named model starts with the requested model, then falls back within the allowed
tier where it holds the best list position (ties go to the higher tier). It
skips backups with a smaller context window than the requested model and shares
failure counts and cooldowns with tier requests. A model outside all allowed
tiers, or outside tier mode, keeps plain forwarding with no fallback. Successful
HTTP replies stream immediately, pings and error events included: there is no
look-ahead, event buffering, mid-stream switch or new reply-body timeout.

Admin options: `/model <name>` inside a session switches to any model by
name. `CCSESSION_SHOW_ALL_MODELS=1 ccsession notes` also lists every tier
model one by one in `/model`; that session gets its own shim so other
sessions' pickers do not change. `CCSESSION_TIERS=0` turns tier mode off,
`CCSESSION_COOLDOWN_SECONDS` changes the out-of-usage cooldown.
`CCSESSION_FAILS_BEFORE_SWITCH` (default 3) controls the server-error threshold;
`CCSESSION_PARK_SECONDS` (300) and `CCSESSION_PARK_MAX_SECONDS` (3600) control the
starting and maximum growing park. These are process environment settings read
when the shim starts, not tier settings in the workspace defaults file.
`GW_PROXY_LOGFILE` overrides the default `${XDG_CACHE_HOME:-$HOME/.cache}/ccsession/proxy.log`.
The log rotates at 5 MB with one older copy and records routing, error kind,
counts and parks, never credentials or request/reply bodies (except gateway
error messages, with credential redaction). An unwritable log does not stop requests.
`CCSESSION_COMPACT_WINDOW` / `CCSESSION_COMPACT_PCT` still override the
auto-compact settings. `ccsession --models-status` shows whether tier mode is
on and where its settings came from.

A tier is named by a number with an optional letter (`tier0`, `tier1a`,
`tier1b`, `tier12`); its env names follow (`T1a_WINDOW`, `T1aModel01`).

**Per-user tiers.** `CCSESSION_TIER_RULES` in the same workspace env file sets
the tier each person starts on, the tiers they are offered, and whether the
picker also lists each model:

```bash
export CCSESSION_TIER_RULES="role:owner=tier1a+models role:auditor=tier1a+models *=tier2:tier2,tier3,tier4"
export CCSESSION_MODEL_ORDER="claude-fable-5-1 claude-opus-5-5 ... Qwen3.8-max"
```

Entries are space-separated `<who>=<start tier>[:<tier>,<tier>,...][+models]`.
`<who>` is a Coder username, `role:<coder role>` for everyone holding that
site-wide Coder role (`owner`, `user-admin`, `template-admin`, `auditor`; a
plain member holds only `member`), or `*` for everyone else, including a terminal that does not know
its owner. A username entry wins, then the first matching role entry, then
`*`. No tier list means every tier (`tier2` and `2` both work, and names match
without regard to case). `+models` also lists each model of those tiers in
`/model`, ordered by `CCSESSION_MODEL_ORDER` (models not named there follow in
tier order). With no matching entry, the user starts on
`CCSESSION_DEFAULT_TIER` with every tier. The owner comes from
`CODER_WORKSPACE_OWNER_NAME` and their roles from
`CODER_WORKSPACE_OWNER_ROLES`, both set by the Coder template. For a limited
user, `--help` and `/model` show only their tiers, `--tier` and `--model`
refuse anything outside them, and the shim refuses requests for other tiers.
A broken or repeated entry that applies to this user stops their launch with
the reason, rather than opening every tier. Set it on one line with a literal
value, `export CCSESSION_TIER_RULES="..."`, and do not name it on any other
line of the file, comments included. Another line naming it, a `${...}`
value, or a piece of the value that is not a `who=...` entry (for example from
a stray space) stops ccsession for every Coder user until it is fixed. Because
ccsession re-reads the file on every launch and every request, a pushed change
applies without a restart. `ccsession --models-status` shows the owner's
access.

`CCSESSION_ACCESS` is the older form of the same setting, read when there is no
`CCSESSION_TIER_RULES` line. Keep it in the file for workspaces still running an
older ccsession, with the same one-line rule. Older copies ignore
`CCSESSION_TIER_RULES` and understand only username entries in
`CCSESSION_ACCESS`: a `role:` or `*` entry there stops them for every named
owner, so put those in `CCSESSION_TIER_RULES` only.

The limit is advisory. It sets what ccsession offers by default, and the
workspace owner can undo it from their own environment
(`CODER_WORKSPACE_OWNER_NAME`, `CODER_WORKSPACE_OWNER_ROLES`, `AIDEV_AI_DEFAULTS_PATH`, `CCSESSION_TIERS=0`)
or call a model directly with their gateway key. Only a gateway key limited to
those models enforces it. ccsession reads the file without running it, so a
setting whose name is deliberately assembled from pieces (for example across
two lines) is not seen; the central file is changed only through review.

No time limit ever applies once a model has started answering: a reply may
think or stream for hours. The only ccsession timer is, for streamed tier
requests and named-model fallback requests, a 5-minute wait for the gateway to accept the request (it normally
sends its "starting" header within 2 seconds, before the model thinks). A
gateway that cannot be reached at all is reported and never treated as a model
failure.

| Setting | Effect |
|---|---|
| `T<N>_WINDOW` (workspace env) | Tier context window; its presence turns tier mode on (`<N>` is a number with an optional letter, such as `1a`) |
| `T<N>Model0M`, `T<N>Model0M_WINDOW` (workspace env) | Tier models in order, and each model's own window (a backup smaller than the tier window is never used) |
| `ANTHROPIC_MODEL` (workspace env) | Default model when no `--tier` or `--model` is given, if it is a model of a tier you may use (same launch as `--model <that model>`); otherwise ignored and `CCSESSION_DEFAULT_TIER` applies |
| `CCSESSION_DEFAULT_TIER` (workspace env) | Tier used when no `--tier` or `--model` is given and `ANTHROPIC_MODEL` does not apply (`tier2` if unset) |
| `CCSESSION_TIER_RULES` (workspace env) | Per Coder username, Coder role, or everyone else: start tier, tiers offered, and `+models` (see Per-user tiers above) |
| `CCSESSION_MODEL_ORDER` (workspace env) | Order of the individual models in `/model` for a `+models` rule |
| `CCSESSION_ACCESS` (workspace env) | Older per-username form, read only when there is no `CCSESSION_TIER_RULES` line |
| `CODER_WORKSPACE_OWNER_NAME` | Workspace owner's Coder username (set by the Coder agent); picks a username entry |
| `CODER_WORKSPACE_OWNER_ROLES` | Workspace owner's Coder roles, comma-separated (set by the Coder template); picks `role:` entries |
| `AIDEV_AI_DEFAULTS_PATH` | Workspace env file read on every launch (default `/etc/aidev02/aienv.d/defaults.sh`); the shell environment is used only when the file is absent |
| `CCSESSION_TIERS=0` | Turn tier mode off |
| `CCSESSION_SHOW_ALL_MODELS=1` | Also list every tier model in `/model` (own shim) |
| `CCSESSION_COOLDOWN_SECONDS` | Out-of-usage cooldown when no `Retry-After` is given (default 3600) |
| `CCSESSION_FAILS_BEFORE_SWITCH` | Consecutive server errors before switching (default 3) |
| `CCSESSION_PARK_SECONDS`, `CCSESSION_PARK_MAX_SECONDS` | First and maximum temporary park in seconds (defaults 300 and 3600) |
| `CCSESSION_FIRST_BYTE_TIMEOUT` | Wait for a streamed tier or named-model fallback reply to start before switching (default 300) |
| `GW_PROXY_LOGFILE` | Override the kept log path (default cache `ccsession/proxy.log`, 5 MB plus one rotated copy) |
| `CC_SHIM_PORT` | Base shim port (default 4010). Show-all, a non-standard env file, tier settings from the shell, or a workspace owner name or roles (every Coder session) get base + an offset; an explicitly set port is used as-is |
| `CCSESSION_COMPACT_WINDOW`, `CCSESSION_COMPACT_PCT` | Override the auto-compact window or percentage, in tier mode too |
| `CCSESSION_GATEWAY_URL`, `CCSESSION_SHIM_URL` | Set by ccsession, not by you: a shim session exports the gateway its shim forwards to and the shim's own address. A `ccsession` started inside that session finds `ANTHROPIC_BASE_URL` equal to `CCSESSION_SHIM_URL` and forwards to `CCSESSION_GATEWAY_URL` instead, so one shim never forwards to another |
| `CCSESSION_PERMISSIONS=default` | Start Claude without `--dangerously-skip-permissions`: only `--allowedTools=Grep` is added, so Grep and Glob stay available. The shim and tier-model routing are unchanged. Set it in the shell environment that starts `ccsession`; it is read before `~/.claude/ccsession.env` is sourced, so it cannot be set from that file (a value exported there is undone, so Claude and a nested `ccsession` see what the shell set). It stays exported to nested launches. Any other non-empty value exits with status 2 on every `ccsession` call, `--help` included (under a bad value, and only when `CCSESSION_NAME` is set, `ccsession-orca` also prints its "CCSESSION_NAME is not a valid session name; ignoring it" warning before the exit). A non-empty `CC_CLAUDE_FLAGS`, from the shell or the env file, still wins; flags the caller passes (such as Orca's default `--dangerously-skip-permissions` option) still apply. Unset or empty: no change |
| `CC_CLAUDE_FLAGS` | Replaces the flags `ccsession` adds to every Claude it starts (default `--dangerously-skip-permissions --allowedTools=Grep`, or `--allowedTools=Grep` with `CCSESSION_PERMISSIONS=default`). An empty value takes the default |

---

## Profiles (when not in tier mode)

A profile decides which model a session starts on and how much conversation it
holds before Claude Code trims it.

```bash
ccsession notes --profile gpt --shim
```

| Profile | Starts on | Holds | Needs `--shim` |
|---|---|---|---|
| `claude` | Opus 5.5, large-window version | 1,000,000 | no |
| `gpt` | GPT 6.1 Sol | 850,000 | yes |
| `grok` | Grok 4.7 | 500,000 | yes |
| `muse` | Muse Spark 1.3 | 950,000 | yes |
| `wonderfull` | Muse Wonder Full 1.0 | 1,000,000 | yes |
| `wonder` | Muse Wonder 1.0 | 1,000,000 | yes |
| `qwen` | Qwen 3.8 Max | 1,000,000 | yes |
| `glm` | GLM 5.3 | 1,000,000 | yes |

Which model sits in which tier, and the scores and prices behind it, are in
[MODEL-TIERS.md](MODEL-TIERS.md).

`ccsession --help` shows the list from the last download (or the copy shipped
with the skill) without going online; run `ccsession --refresh-models` to fetch
the latest first. With `--shim`, ccsession saves the complete curated model list before
Claude Code starts, so every profile shows the same gateway models in `/model`.

To add your own without editing ccsession, put a file in
`~/.config/ccsession/profiles.d/` (for example `mine.sh`, readable and writable
only by you) that defines a function named `ccsession_profile_<name>`. Reinstalling
ccsession never touches this folder, and nothing in it is ever shared.

```bash
ccsession_profile_mine() {
  PROFILE_MODEL="claude-opus-5-5[1m]"   # empty: let Claude Code choose
  PROFILE_CONTEXT="1000000"              # empty: no context override
  PROFILE_COMPACT_WINDOW="1000000"
  PROFILE_REQUIRES_SHIM=0
  # Optional: CCSESSION_SKIP_ENV_FILE=1 to ignore ~/.claude/ccsession.env,
  # CCSESSION_REFUSE_SHIM=1 to refuse --shim for this profile.
}
```

Then run `ccsession --profile mine`. Labels work the same across every profile.

---

## Keeping profiles and models current

Profiles and the curated picker live in `ccsession-models.json`. Every
`ccsession` launch asks IronClaude on GitHub whether a newer copy exists. When
nothing changed GitHub answers "not modified", which adds roughly a tenth of a
second; a newer copy is validated, cached in `~/.cache/ccsession/`, and used
by that same launch, with one line saying what changed. Without a network the
check gives up after about 2 seconds and the cached or shipped copy is used.
A running shim picks up new data on its next model-list request. After an
upgrade, new sessions start a new shim on another port; a shim still used by
older sessions keeps running until you stop it (`pkill -f
local-gateway-alias-proxy.py` when no session uses it).

| Command or setting | What it does |
|---|---|
| `ccsession --refresh-models` | Check right now and report the result |
| `ccsession --models-status` | Show which copy is in use and when it was last checked |
| `CCSESSION_MODELS_REFRESH=0` | Skip the check (uses the cached or shipped copy) |
| `CCSESSION_MODELS_URL=<url>` | Read the data from a different address |

## Choosing which models appear

Edit `ccsession-models.json` in IronClaude and merge it; every install picks it
up on its next launch. Always use the model's real gateway name such as
`gpt-6-astra`, never the `claude-gw-` version you see in the picker. Outside
tier mode the picker shows exactly the models in `picker.show`, in that order,
that the gateway still serves; a new gateway model stays hidden until it is
added there. Tier models and their order come from the workspace env file, not
from this file.

| Goal | Where to put it |
|---|---|
| Add or change a profile | `profiles` |
| Show a model, or change the order | `picker.show` |
| Give it a nicer name | `picker.display_overrides` |
| Let it hold a million tokens | `picker.one_million_context` |
| Change which env variables make up a tier | `tiers` |

Raise `version` (for example `2026-10-02.1`) with every change: installs keep
whichever copy has the newest version.

---

## About conversation size

There are exactly two controls, and it helps to know which one you are reaching
for.

**Per model.** A model listed in `picker.one_million_context` is offered to Claude Code
with a `[1m]` tag on its name, and Claude Code then treats it as holding a
million tokens. One million is the only size this method supports. There is no
way to tag a model as 500,000 or 372,000.

**Per session.** A profile sets one size for the whole session. It cannot give
two models different sizes, so if you switch models mid-session, every model
either uses its own million-token tag or falls back to the session's number.

Anything with no tag and no profile is treated as 200,000 tokens.

One caution: tagging a model as a million tokens does not make it one. If the
model actually stops accepting input earlier, Claude Code will not trim the
conversation in time and the model will start rejecting your messages. Set the
profile's number to something the model can really handle.

---

## After you edit the shim

Restart it and clear the saved list, then open a new session. This recipe is
for the base port (a Mac with default settings). In a Coder workspace the port
depends on the workspace owner and the settings, so use the simpler
alternative below.

```bash
(
  set -e
  CC_SHIM_PORT="${CC_SHIM_PORT:-4010}"
  CC_SHIM_SCRIPT="$HOME/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py"
  SHIM_PID=$(lsof -ti "tcp:$CC_SHIM_PORT" -s TCP:LISTEN | head -n 1 || true)
  if [ -n "$SHIM_PID" ]; then
    ps -p "$SHIM_PID" -o command= | grep -Fq -- "$CC_SHIM_SCRIPT" || {
      echo "Port $CC_SHIM_PORT belongs to another service; refusing to stop it." >&2
      exit 1
    }
    kill "$SHIM_PID"
  fi
  set -a; . "$HOME/.claude/ccsession.env"; set +a
  GW_PROXY_UPSTREAM="$ANTHROPIC_BASE_URL" GW_PROXY_PORT="$CC_SHIM_PORT" \
    nohup python3 "$CC_SHIM_SCRIPT" >/dev/null 2>&1 &
  rm -f "$HOME/.claude/cache/gateway-models.json"
)
```

Sessions that are already open keep the old list until they restart.

Simpler alternative: stop every running shim (`pkill -f local-gateway-alias-proxy.py`)
and start a new session; ccsession starts the right shim on the right port
(show-all and other offset ports included). ccsession never stops a running
shim by itself, because other sessions may be using it.

---

## If something is wrong

| Symptom | Cause |
|---|---|
| `ccsession: command not found` | `~/.local/bin` is not on your `PATH` |
| Gateway models missing from the picker | Started without `--shim`, or the session predates your last shim restart |
| A model shows 200,000 tokens | It is not in `picker.one_million_context`, and the session has no profile |
| A new model or profile has not appeared | Run `ccsession --models-status`; `ccsession --refresh-models` checks immediately |
| "input exceeds the context window" | The size you set is larger than the model truly accepts. Lower the profile number |
| Image errors on some models | Certain models accept text only. Use a different model for conversations containing screenshots |
| A named session says it cannot be found | The conversation was deleted. `ccsession --rm <name>` clears the stale name |
| `API Error: 502 ccsession: gateway unreachable at http://127.0.0.1:<port>` | The shim's upstream is another shim's address, saved in `~/.claude/ccsession.env` or `~/.env` (older installers saved the shell's `ANTHROPIC_BASE_URL`, which inside a session is the shim). Set `ANTHROPIC_BASE_URL` there to the gateway, stop the broken shim (`curl -s http://127.0.0.1:<port>/__ccsession_shim` shows its `pid`), and start a new session. ccsession now refuses such an address before starting a shim |
| `ccsession: gateway unreachable at <gateway>` | The gateway itself refused or dropped the connection: check that it is up on that host and port (a ping only proves the host is up) |

---

## Moving to another computer

Copy `~/.claude/skills/ccsession-tag/`, your `~/.claude/ccsession.env`, and, if
you want your existing conversations to come with you, the matching `.jsonl`
files under `~/.claude/projects/`. Those transcripts live in folders named after
the full path of the project, so keep your username and project paths the same
or the names will not line up.

---

## Storage layout

- Label pointers live at `~/.claude/projects/<key>/topics/<label>.txt`. The key
  is the repo's network `origin` as host and path with `/` turned into `-`
  (for example `github.com-IronbellyOrg-IronClaude`; credentials, port, query
  and host case ignored). Without a network origin (none, or a local path such
  as a clone made with `git clone /path/repo`), the main worktree's folder
  (for a separate or bare git folder, that folder); outside a git repo, the
  current folder. `ccsession --key` prints it. In the file name, `%`, `/` and
  a leading `.` are written `%25`, `%2F` and `%2E`.
- The `.cwd` file beside them records the folder last used, for listings.
- `.ccsession-lock` beside them is locked (`flock`) while a name is saved, so
  two sessions saving at once take turns. The lock goes with the process that
  held it, so a killed run never leaves the list locked.
- `~/.cache/ccsession/orca-titles/` (or under `$XDG_CACHE_HOME`) holds, per
  Orca tab, the exact title ccsession set on it, so only that title is ever
  taken off.
- Claude Code owns the conversation transcripts in the neighboring `.jsonl`
  files. ccsession resumes them but does not modify their contents.

## Uninstall

```bash
rm ~/.local/bin/ccsession ~/.local/bin/ccsession-orca
rm -rf ~/.claude/skills/ccsession-tag
```

Optionally remove `~/.claude/ccsession.env` and the ccsession SessionStart,
UserPromptSubmit and SessionEnd hooks from `~/.claude/settings.json`. Removing a label or uninstalling ccsession does
not delete a Claude Code transcript.

---

## Let an assistant set it up for you

Paste this into Claude Code, from inside the folder you unpacked:

> Set up the ccsession tool in this folder for me.
>
> 1. Run `./install.sh` and tell me what it reports.
> 2. Confirm `ccsession --help` works. If the command is not found, tell me
>    exactly what to add to my shell profile to put `~/.local/bin` on my PATH.
> 3. Ask me for my LiteLLM gateway address and key. Write them into
>    `~/.claude/ccsession.env` as `ANTHROPIC_BASE_URL` and
>    `ANTHROPIC_AUTH_TOKEN`, making sure the address ends in `/cli`, and set the
>    file to permissions 600. Never print my key back to me.
> 4. Verify the gateway by requesting `$ANTHROPIC_BASE_URL/v1/models` with that
>    key. If it fails, tell me whether the address or the key is the problem.
> 5. Show me the model names the gateway returned, and tell me how to start a
>    session with `ccsession <name> --shim`.
>
> Do not change any file outside `~/.claude/`. Stop and ask me if a step fails.
