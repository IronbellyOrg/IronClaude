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
| `local-gateway-alias-proxy.py` | The shim, a small local proxy |
| `install.sh` | Installer. Run this once |
| `ccsession.env.example` | Template for your gateway address and key |
| `hooks/session-start.sh` | Records each session's ID so names can resume it |
| `SKILL.md` | The `/ccsession-tag` command used inside Claude |
| `README.md` | This file |

---

## Before you install

- macOS or Linux, with `python3`, `curl`, and `lsof` available.
- Claude Code already installed and working.
- `~/.local/bin` on your `PATH`.
- The shim part only matters if you have a LiteLLM gateway. Session naming works
  fine without one.

---

## Install from IronClaude

Install or update the packaged skill, then run its local installer:

```bash
superclaude install-skill ccsession-tag --force
~/.claude/skills/ccsession-tag/install.sh
```

The first command copies this complete package out of IronClaude. The second
creates the `ccsession` command, creates `~/.claude/ccsession.env` without
putting a key in the repository, and registers the SessionStart hook. It is
safe to run again and leaves an existing environment file untouched.

If you are working from an IronClaude source checkout, you can install directly:

```bash
cd src/superclaude/skills/ccsession-tag
./install.sh
```

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
ccsession --here             # named sessions for this folder only
ccsession --rm notes         # forget the name (the conversation itself is kept)
```

Inside a running Claude session you can name it after the fact:

```
/ccsession-tag notes
```

Names are per folder. The same name in two different projects points at two
different conversations, which is what you usually want.

---

## Profiles

A profile decides which model a session starts on and how much conversation it
holds before Claude Code trims it.

```bash
ccsession notes --profile gpt1 --shim
```

| Profile | Starts on | Holds | Needs `--shim` |
|---|---|---|---|
| `claude` | Opus 5, large-window version | 1,000,000 | no |
| `gpt` | GPT 5.6 Sol | 850,000 | yes |
| `gpt1` | GPT 6 Astra | 850,000 | yes |
| `grok` | Grok 4.6 | 500,000 | yes |

Older names `1mm`, `372k`, and `500k` still work and mean `claude`, `gpt`, and
`grok`. With `--shim`, ccsession saves the complete curated model list before
Claude Code starts, so every profile shows the same gateway models in `/model`.

To add your own, copy a block in the `apply_profile` section of `ccsession` and
change the name, the model, and the two numbers.

---

## Choosing which models appear

Every gateway model not listed in `REMOVE` shows up on its own. Editing these
lists controls the curated model picker shipped for the team. All of it lives near the top of `local-gateway-alias-proxy.py`, and
you always use the model's real gateway name such as `gpt-6-astra`, never the
`claude-gw-` version you see in the picker.

| Goal | Where to put it |
|---|---|
| Hide a model | `REMOVE` |
| Move it to the top | `PINNED` |
| Give it a nicer name | `DISPLAY_OVERRIDES` |
| Let it hold a million tokens | `ONE_MILLION_CONTEXT` |

---

## About conversation size

There are exactly two controls, and it helps to know which one you are reaching
for.

**Per model.** A model listed in `ONE_MILLION_CONTEXT` is offered to Claude Code
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

Restart it and clear the saved list, then open a new session:

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

---

## If something is wrong

| Symptom | Cause |
|---|---|
| `ccsession: command not found` | `~/.local/bin` is not on your `PATH` |
| Gateway models missing from the picker | Started without `--shim`, or the session predates your last shim restart |
| A model shows 200,000 tokens | It is not in `ONE_MILLION_CONTEXT`, and the session has no profile |
| "input exceeds the context window" | The size you set is larger than the model truly accepts. Lower the profile number |
| Image errors on some models | Certain models accept text only. Use a different model for conversations containing screenshots |
| A named session says it cannot be found | The conversation was deleted. `ccsession --rm <name>` clears the stale name |

---

## Moving to another computer

Copy `~/.claude/skills/ccsession-tag/`, your `~/.claude/ccsession.env`, and, if
you want your existing conversations to come with you, the matching `.jsonl`
files under `~/.claude/projects/`. Those transcripts live in folders named after
the full path of the project, so keep your username and project paths the same
or the names will not line up.

---

## Storage layout

- Label pointers live at `~/.claude/projects/<workspace-slug>/topics/<label>.txt`.
- The `.cwd` file beside them records the real workspace path for listings.
- Claude Code owns the conversation transcripts in the neighboring `.jsonl`
  files. ccsession resumes them but does not modify their contents.

## Uninstall

```bash
rm ~/.local/bin/ccsession
rm -rf ~/.claude/skills/ccsession-tag
```

Optionally remove `~/.claude/ccsession.env` and the ccsession SessionStart hook
from `~/.claude/settings.json`. Removing a label or uninstalling ccsession does
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
