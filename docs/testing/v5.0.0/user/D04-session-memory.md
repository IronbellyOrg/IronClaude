# E2E Test Guide — `Session memory in .superclaude/memory/` (`5.0.0`)

- **Capability:** `/sc:save`, `/sc:load`, `/sc:pm` and the PM agent keep project memory as plain markdown files in `<project>/.superclaude/memory/`, one store per worktree. The first save creates `<project>/.superclaude/.gitignore` containing `*`. For 5.0.0 only, `/sc:load` also reads an old `.serena/memories/<key>.md` when the matching new file is absent, never writes there and says that folder is read-only history.
- **Audience:** end user
- **Source of truth:** `src/superclaude/commands/save.md:22,28,42-45`; `src/superclaude/commands/load.md:42-43,52-53`; `src/superclaude/commands/pm.md:16,47,51-52`; `src/superclaude/agents/pm-agent.md:19-35`; `src/superclaude/skills/sc-pm-protocol/SKILL.md:23-32,45-54`; `CHANGELOG.md:98,105`; `docs/releases/v5.0.0.md` (Breaking Changes, Change 1)
- **Est. time:** `Tier A: 1 minute. Tier B: 2 minutes. Tier C: 20-30 minutes in interactive Claude Code sessions.`

## Preconditions

- IronClaude 5.0.0 installed for your user (`superclaude install` done): `superclaude --version` prints `SuperClaude, version 5.0.0`.
- `git` and the `claude` CLI on your `PATH`, and a Claude Code login for Tier C (each Tier C step uses API tokens).
- `/tmp/d04` does not exist (`[ ! -e /tmp/d04 ] && echo OK` prints `OK`). Every file this guide creates is under `/tmp/d04`. No step installs, registers or edits anything under `~/.claude`, but the Tier C sessions still write there: Claude Code saves each session's history, the freshness hooks that `superclaude install` registers write state and log files under `~/.claude/state/` and `~/.claude/logs/` at session start and on each prompt (`src/superclaude/hooks/hooks.json:18,49`; `src/superclaude/hooks/scripts/freshness-session-start.sh:8-9`, `freshness-user-prompt.sh:8-10`), and `auggie-flag-clear.sh` writes there after auggie tool calls (`hooks.json:104`; `auggie-flag-clear.sh:10-12`).
- Claude Code may ask permission before writing files under `/tmp/d04/...`; allow it for these sessions.
- Do not confuse this feature with Claude Code's own memory (files Claude Code keeps under `~/.claude/projects/`). This guide checks only `<project>/.superclaude/memory/`.
- The behaviour under test is carried out by Claude following the command files; there is no script behind it. So every expected result below checks files on disk or one distinctive marker string, never the exact wording of Claude's reply.

## What you're verifying

- `/sc:save` writes markdown files into `<git top-level>/.superclaude/memory/`, creates `.superclaude/.gitignore` with the single line `*` so `git status` stays clean, overwrites single-owner keys and adds a new `checkpoint-<session-or-timestamp>.md` file for each checkpoint.
- `/sc:load` in a new session reads that store, reports the saved content and ends with a line telling you to type `/sc:graph status`, without running it.
- In a project that only has the old `.serena/memories/`, `/sc:load` reads it, calls it read-only history and leaves `.serena/` byte-for-byte unchanged; a file in the new store takes precedence over its `.serena` twin.
- A second worktree of the same repository has its own separate store.
- `/sc:pm` reads and writes the same store.

---

## Steps

### Tier A — free smoke on your machine (read-only)

#### Step 1 — The installed commands describe the file store `[FREE]`

**Do:**

```bash
superclaude --version
for f in commands/sc/save.md commands/sc/load.md commands/sc/pm.md agents/pm-agent.md skills/sc-pm-protocol/SKILL.md; do
  printf '%s ' "$f"; grep -c '\.superclaude/memory' ~/.claude/"$f"
done
grep -n -i serena ~/.claude/commands/sc/load.md
grep -c -i serena ~/.claude/commands/sc/save.md ~/.claude/commands/sc/pm.md ~/.claude/agents/pm-agent.md
```

**Expected result:** `SuperClaude, version 5.0.0`; then the counts `commands/sc/save.md 8`, `commands/sc/load.md 8`, `commands/sc/pm.md 2`, `agents/pm-agent.md 25`, `skills/sc-pm-protocol/SKILL.md 15`; then exactly one Serena line, line 43 of `load.md` (the legacy fallback); then `:0` for `save.md`, `pm.md` and `pm-agent.md`. Only `/sc:load` still mentions Serena, and only to read it. (source: the installed files are byte copies of `src/superclaude/commands/save.md`, `load.md`, `pm.md`, `src/superclaude/agents/pm-agent.md` and `src/superclaude/skills/sc-pm-protocol/SKILL.md`; counts taken from those files at tag v5.0.0; fallback line `src/superclaude/commands/load.md:43`; Serena removal `CHANGELOG.md:104-105`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier B — local writes under /tmp/d04

#### Step 2 — Create the fixtures `[LOCAL-WRITE]`

**Do:** (bash; keep this terminal open, Tier C uses a second one)

```bash
[ ! -e /tmp/d04 ] || { echo "remove /tmp/d04 first"; false; }
mkdir -p /tmp/d04/repo /tmp/d04/legacy/.serena/memories
cd /tmp/d04/repo && git init -q . && printf '# d04 fixture\n' > README.md
git add -A && git -c user.name=d04 -c user.email=d04@example.invalid commit -qm fixture
git worktree add -q /tmp/d04/wt2 -b d04-wt2
cd /tmp/d04/legacy && git init -q . && printf '# legacy fixture\n' > README.md
git add README.md && git -c user.name=d04 -c user.email=d04@example.invalid commit -qm fixture
cat > .serena/memories/last_session.md <<'EOF'
# Last session

Finished: SERENA-MARKER-D04, the migration of the config loader.
EOF
find .serena -type f -exec cksum {} + | sort > /tmp/d04/serena.before
ls -A /tmp/d04/repo; ls -A /tmp/d04/wt2; ls -A /tmp/d04/legacy; cat /tmp/d04/serena.before
```

**Expected result:** `/tmp/d04/repo` holds `.git` and `README.md`; `/tmp/d04/wt2` holds `.git` (a file, because it is a linked worktree) and `README.md`; `/tmp/d04/legacy` holds `.git`, `.serena` and `README.md` and no `.superclaude`. `/tmp/d04/serena.before` has one line ending in `.serena/memories/last_session.md`. This gives a main checkout, a second worktree of it, and a project that only has old Serena memories with no `.superclaude/memory/last_session.md` twin, which is the case the fallback covers (`src/superclaude/commands/load.md:43`).

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

### Tier C — interactive Claude Code sessions

Run these in a second terminal. Start each session with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` so the codegraph session-start hook does not add a `.codegraph/` folder to the fixtures (that switch turns off the hook only, `src/superclaude/hooks/scripts/codegraph-session-start.sh:11`). Type each `/sc:` line at the Claude Code prompt exactly as shown. Exit each session with `/exit` before running the shell checks, unless the step says otherwise.

#### Step 3 — `/sc:save` writes the store and its `.gitignore` `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d04/repo && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
For this project, remember: the release codename is BLUE-HERON-D04 and the next action is to write the parser tests.
/sc:save
/exit
```

Then, in the shell:

```bash
cd /tmp/d04/repo
ls -A .superclaude; cat .superclaude/.gitignore; ls .superclaude/memory
grep -rl BLUE-HERON-D04 .superclaude/memory
git status --porcelain --untracked-files=all
[ ! -e .serena ] && echo no-serena
```

**Expected result:** `.superclaude` holds `.gitignore` and `memory`; `.gitignore` is exactly one line, `*`; `memory/` holds one or more `.md` files (names are chosen by Claude; single-owner keys such as `last_session.md` or `next_actions.md` are typical); `grep -rl` prints at least one of those files; `git status --porcelain` prints nothing, because `*` also ignores the `.gitignore` itself; `no-serena` is printed. (source: store location and per-worktree root `src/superclaude/commands/save.md:42`; first-write `.gitignore` `save.md:43`; markdown files `save.md:28,35`; key names `save.md:44-45`)

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 4 — Checkpoints add files; single-owner keys never get a suffix `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d04/repo && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:save --checkpoint
```

In the first terminal, record the checkpoint files:

```bash
cd /tmp/d04/repo && ls .superclaude/memory | grep '^checkpoint-' | tee /tmp/d04/cp.before
find .superclaude/memory -name 'checkpoint-*' -exec cksum {} + | sort > /tmp/d04/cp.cksum
```

Back in the session:

```text
/sc:save --checkpoint
/exit
```

Then:

```bash
cd /tmp/d04/repo
ls .superclaude/memory | grep '^checkpoint-' | wc -l; wc -l < /tmp/d04/cp.before
find .superclaude/memory -name 'checkpoint-*' -exec cksum {} + | sort | grep -cxF -f /tmp/d04/cp.cksum; wc -l < /tmp/d04/cp.cksum
ls .superclaude/memory | grep -E '^(pm_context|last_session|next_actions|current_plan)-'
```

**Expected result:** After the first `--checkpoint`, `/tmp/d04/cp.before` lists one or more `checkpoint-<session-or-timestamp>.md` names. After the second, the checkpoint count is one higher than `wc -l < /tmp/d04/cp.before`. The two `cksum` counts are equal: every earlier checkpoint file is still there, byte-for-byte unchanged. The last command prints nothing: single-owner keys are always overwritten as `<key>.md`, never written with a suffix. (source: `--checkpoint` flag `src/superclaude/commands/save.md:22`; parallel keys written as `<key>-<session-or-timestamp>.md` and never edited in place `save.md:45`; single-owner keys overwritten whole `save.md:44`; `current_plan` as a single-owner key `src/superclaude/agents/pm-agent.md:21`). If the first `--checkpoint` produced no `checkpoint-*` file at all, mark FAIL and note the file names it wrote instead.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 5 — `/sc:load` in a new session reads the store `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d04/repo && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:load
```

**Expected result:** Claude reads files under `/tmp/d04/repo/.superclaude/memory/` (the tool calls shown in the session name that folder) and its summary mentions `BLUE-HERON-D04` and the parser-tests next action. The summary ends with one line telling you to type `/sc:graph status` to see whether the code-graph index is ready. Claude does not run `/sc:graph` itself: no `sc:graph-protocol` skill load and no `codegraph` command appear in the session. Exit the session, then `[ ! -e /tmp/d04/repo/.serena ] && echo no-serena` prints `no-serena`. (source: store and root `src/superclaude/commands/load.md:42`; Glob and Read of the store `load.md:49-50`; `/sc:graph status` line and "never runs `/sc:graph` itself" `load.md:53`). UNVERIFIED: the wording of the summary and of the `/sc:graph status` line is chosen by Claude; judge PASS on the marker and on the presence of a line naming `/sc:graph status`.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 6 — `/sc:load` reads `.serena/memories/` read-only `[CLAUDE-SESSION]`

**Do:**

```bash
cd /tmp/d04/legacy && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:load
/exit
```

Then:

```bash
cd /tmp/d04/legacy
find .serena -type f -exec cksum {} + | sort | diff /tmp/d04/serena.before - && echo serena-unchanged
find .serena -newer /tmp/d04/serena.before
```

**Expected result:** The summary reports `SERENA-MARKER-D04` (the config-loader migration) as the last session and tells you that `.serena/memories/` is read-only history. In the shell, `serena-unchanged` is printed and the `find -newer` command prints nothing: no file in `.serena/` was changed or added. If Claude saved anything during `/sc:load`, it is under `/tmp/d04/legacy/.superclaude/memory/`, never under `.serena/`. (source: fallback only when `.superclaude/memory/<key>.md` is absent, never writes there, tells the user it is read-only history `src/superclaude/commands/load.md:43`; `CHANGELOG.md:105`; the fallback ends in the next release, `docs/releases/v5.0.0.md` Breaking Changes, Change 1). UNVERIFIED: the exact read-only wording; judge PASS on the marker, a statement that the folder is read-only, and the unchanged checksums.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 7 — A new-store file takes precedence over its `.serena` twin `[CLAUDE-SESSION]`

**Do:** first, in the first terminal:

```bash
cd /tmp/d04/legacy && mkdir -p .superclaude/memory
printf '# Last session\n\nFinished: NEW-STORE-MARKER-D04, the parser tests.\n' > .superclaude/memory/last_session.md
```

Then:

```bash
cd /tmp/d04/legacy && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:load
/exit
```

Then `cd /tmp/d04/legacy && find .serena -type f -exec cksum {} + | sort | diff /tmp/d04/serena.before - && echo serena-unchanged`.

**Expected result:** The summary reports `NEW-STORE-MARKER-D04` (the parser tests) as the last session, not `SERENA-MARKER-D04`: `.serena/memories/last_session.md` is not used because `.superclaude/memory/last_session.md` now exists. `serena-unchanged` is printed. (source: "reads `.serena/memories/<key>.md` only when `.superclaude/memory/<key>.md` is absent" `src/superclaude/commands/load.md:43`). UNVERIFIED: whether Claude also mentions the shadowed `.serena` file is up to Claude; FAIL only if it reports the Serena marker as the last session.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 8 — A second worktree has its own store `[CLAUDE-SESSION]`

**Do:**

```bash
ls -A /tmp/d04/wt2
cd /tmp/d04/wt2 && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:load
For this worktree, remember: the worktree codename is WT2-ONLY-D04.
/sc:save
/exit
```

Then:

```bash
cat /tmp/d04/wt2/.superclaude/.gitignore
grep -rl WT2-ONLY-D04 /tmp/d04/wt2/.superclaude/memory
grep -rl WT2-ONLY-D04 /tmp/d04/repo/.superclaude/memory || echo not-in-main
grep -rl BLUE-HERON-D04 /tmp/d04/wt2/.superclaude || echo main-not-in-wt2
git -C /tmp/d04/wt2 status --porcelain --untracked-files=all
```

**Expected result:** Before the session, `/tmp/d04/wt2` holds only `.git` and `README.md`: the main checkout's store is ignored by git, so it never reaches the worktree. `/sc:load` reports no saved project memory for this worktree and does not mention `BLUE-HERON-D04`. After the session: `.gitignore` is `*`; the first `grep` prints at least one file under `/tmp/d04/wt2/.superclaude/memory/`; then `not-in-main` and `main-not-in-wt2`; `git status` prints nothing. (source: `<project>` is the git top-level of the current directory, one store per worktree `src/superclaude/commands/save.md:42` and `src/superclaude/commands/load.md:42`; `.gitignore` `save.md:43`). UNVERIFIED: how Claude words "no saved memory"; FAIL only if it reports `BLUE-HERON-D04` or any file from `/tmp/d04/repo`.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

#### Step 9 — `/sc:pm` reads and writes the same store `[CLAUDE-SESSION]`

**Do:**

```bash
touch /tmp/d04/pm.mark
cd /tmp/d04/repo && SUPERCLAUDE_CODEGRAPH_AUTOINIT=0 claude
```

```text
/sc:pm "Where did we leave off on this project? Then wrap up this session and save its state."
/exit
```

Then:

```bash
cd /tmp/d04/repo
find .superclaude/memory -newer /tmp/d04/pm.mark -name '*.md'
find /tmp/d04/repo -path '*/.serena*' | head -n 1
git status --porcelain --untracked-files=all -- .superclaude
```

**Expected result:** Claude loads the `sc:pm-protocol` skill, reads files under `/tmp/d04/repo/.superclaude/memory/` (Glob, then Read of `pm_context.md`, `current_plan.md`, `last_session.md`, `next_actions.md` where they exist) and its report mentions `BLUE-HERON-D04`. On wrap-up it writes into the same folder: the first `find` lists one or more of `last_session.md`, `next_actions.md` and `pm_context.md`. The second `find` prints nothing (no `.serena` anywhere) and `git status` prints nothing for `.superclaude`. Files the PM agent may also create outside the store, such as `docs/temp/`, `docs/patterns/` or `docs/mistakes/`, are allowed and not a failure. (source: `/sc:pm` restores context from `.superclaude/memory/` `src/superclaude/commands/pm.md:16,47`; skill invocation `pm.md:51-52`; restore and report `src/superclaude/skills/sc-pm-protocol/SKILL.md:27-38`; session end writes `SKILL.md:52-54`; same rules in `src/superclaude/agents/pm-agent.md:19-35`; docs folders `SKILL.md:48,53`). UNVERIFIED: the report format (Previous / Progress / Next / Blockers) and which of the three files Claude writes; FAIL if none of them is newer than `/tmp/d04/pm.mark` or if anything is written to `.serena`.

**Pass/Fail:** ☐ PASS ☐ FAIL — notes: `______`

---

## Edge cases (optional but recommended)

| Try this | Expected behavior | Source | Pass/Fail |
|---|---|---|---|
| `[CLAUDE-SESSION]` `mkdir -p /tmp/d04/repo/sub`, start `claude` in `/tmp/d04/repo/sub`, tell it a fact with marker `SUBDIR-D04`, `/sc:save` | The marker lands in `/tmp/d04/repo/.superclaude/memory/` (git top-level); no `/tmp/d04/repo/sub/.superclaude` is created | `src/superclaude/commands/save.md:42` | ☐ |
| `[CLAUDE-SESSION]` `mkdir /tmp/d04/nogit`, start `claude` there (not a git repository), tell it a fact with marker `NOGIT-D04`, `/sc:save` | Files under `/tmp/d04/nogit/.superclaude/memory/` and `/tmp/d04/nogit/.superclaude/.gitignore` = `*` (outside git the current directory is the project) | `src/superclaude/commands/save.md:42-43` | ☐ |
| `[CLAUDE-SESSION]` `git init -q /tmp/d04/own && mkdir /tmp/d04/own/.superclaude && printf '# mine\n*\n' > /tmp/d04/own/.superclaude/.gitignore`, then `/sc:save` in `/tmp/d04/own` | The existing `.gitignore` is kept unchanged (`cat` still shows `# mine` and `*`); memory files appear next to it | "if `<project>/.superclaude/.gitignore` is absent, create it" `src/superclaude/commands/save.md:43` | ☐ |
| `[CLAUDE-SESSION]` In `/tmp/d04/legacy`, tell Claude a fact with marker `LEGACY-SAVE-D04`, then `/sc:save` | The marker lands under `/tmp/d04/legacy/.superclaude/memory/`; the `.serena` checksum check of Step 6 still prints `serena-unchanged` | `src/superclaude/commands/save.md:28,42`; `src/superclaude/commands/load.md:43` ("never writes there") | ☐ |

## Cleanup

```bash
cd /tmp && rm -rf /tmp/d04
```

This removes both repositories, the linked worktree `/tmp/d04/wt2` (its metadata lives inside `/tmp/d04/repo/.git`), every memory store the steps created and the checksum files. No step changed your `~/.claude` setup. The Claude Code sessions of Tier C stay in Claude Code's own session history, like any session.

## Overall result

☐ **PASS** — capability works as documented for `5.0.0`
☐ **FAIL** — see failing step(s) above

**Tester:** `<name>`  **Date:** `<date>`  **Build:** `5.0.0 (tag v5.0.0, commit d953b983)`
