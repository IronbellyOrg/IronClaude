---
title: "Launch-level enforcement hook: design"
issue: IronbellyOrg/IronClaude#394
type: architecture
format: spec
status: design draft, not implemented
review_status: "NOT REVIEWED after its last amendments (fix cycle 2 and the amendments from plan-review-3); the owner stopped review rounds on 2026-11-05"
adversarial_status: partial
convergence: "1.00 by the protocol rule (0.70 counting only identical verdicts)"
source: .dev/brainstorms/20261105-170229-launch-level-hook/
generated: 2026-11-05
---

# Launch-level enforcement hook: design

> **Not approved.** The final plan review (`plan-review-3.md`) failed with 10 blocking findings. Its reviewer tested the amendments on a copy of a prototype; no one re-reviewed them independently, and the owner decided on 2026-11-05 to stop review rounds. Every rule marked `[AMENDMENT ...]` (written `[B-n]` here) is unreviewed. Acceptance criteria AC-1, AC-2, AC-3, AC-5 and AC-6 were NOT MET by the plan as reviewed. Do not use the hook on real issues until the open decisions in section 15 are settled and the observed checks OB-H1 to OB-H3 pass.

Ids match `merged-requirements.md` ("MR"): FR-L-nn, IR-n, O-n, OD-..., R-n, U-n, LL-..., T-... "Proposed" means not built yet. DD-n marks a designer choice (section 17).

## 1. Purpose and scope

One script, `launch-level-guard.sh`, enforces the level that `/sc:issue --claim --pipeline <level>` gives a launched agent. Only sessions the claim script launched are governed; every other session is ordinary and never blocked.

| Level | Short | Allowed |
|---|---|---|
| worktree, before approval | `W` | planning only |
| worktree, after approval | `WA` | implement; no commit, push, publish |
| full | `F` | implement; no commit, push, publish |
| full with `--submit` | `FS` | commit, push a feature branch, open a PR |

No level allows a merge or a push to `master` or `main`. Targets: TH1 (an honest agent that drifts) and TH2 (one-step workarounds). Not TH3 (deliberate multi-step evasion). In scope: the script, two `hooks.json` entries, one `_FRESHNESS_SCRIPTS` entry, tests, IR-1 to IR-6. Out of scope: the claim feature, ccsession, issue #322, `pipeline.json`. Constraints: agent and hook are the same OS user; bash with `jq`, `sed`, `tr` only; exit 0 allows, exit 2 blocks; no `onFailure`.

## 2. Architecture and files

| File | Role | Change | Status |
|---|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | the only script; flat bash, `LC_ALL=C`, executable (FR-L-60) | new | proposed |
| `src/superclaude/hooks/hooks.json` | append two entries (section 13) | changed | exists |
| `src/superclaude/cli/install_hooks.py` `_FRESHNESS_SCRIPTS` | add `"launch-level-guard.sh"` | changed | exists |
| `Makefile` | none: `verify-sync` imports `_FRESHNESS_SCRIPTS` | unchanged | exists |
| `tests/hooks/test_launch_level_guard.py` | all automated cases | new | proposed |
| `tests/hooks/fixtures/launch_level/ob_h1/*.json` | OB-H1 payloads | new | proposed |
| `.claude/hooks/launch-level-guard.sh` | `make sync-dev` mirror, never staged | generated | proposed |
| `~/.claude/state/launch-level/pending/<nonce>` | launch record | runtime, claim script | proposed |
| `~/.claude/state/launch-level/sessions/<sid>`, `<sid>.ok` | level, approval | runtime, hook | proposed |

```
claim script --pipeline L          write pending/<nonce>; prompt "[sc-launch:v1:<nonce>] ..."  IR-1, IR-2
  v
first prompt (UserPromptSubmit)    mv pending/<nonce> sessions/<sid>, or "degraded"; else LL-NOBIND  FR-L-09
  v
each matched call (PreToolUse)     no bound id: exit 0 | jq -> level -> classes -> grid -> exit 0 or 2  FR-L-10
  v
typed prompt (UserPromptSubmit)    "approved" or /sc:implement /sc:task /task at W: touch <sid>.ok  FR-L-15
  v
release                            a person runs rm sessions/<sid> sessions/<sid>.ok  FR-L-07
```

Script layout (DD-1): settings (`LC_ALL=C`, `set -u -o pipefail`, `set -f`, `umask 077`); store path; messages; dispatch; prompt branch; fast paths; one `jq` read; classifiers adding classes; one `case` on `CLASS:LEVEL`; last line LL-BROKEN, exit 2. About 450 lines (NFR-L-03).

## 3. State and why the agent cannot edit it

Store: `$HOME/.claude/state/launch-level/`, built from three literal parts so the script text never holds `.claude/state` (FR-L-01, T-TAM-8).

| File | Content | Writer | Reader |
|---|---|---|---|
| `pending/<nonce>` | name `^[0-9a-f]{32}$`; one word `worktree`, `full`, `full-submit` | claim script; temp `.x` file then rename (IR-1) | hook, by `mv` or `rm -f` only |
| `sessions/<sid>` | one word; any word other than the three means `worktree` + LL-STATE (FR-L-03) | hook: `mv`, or `degraded` under `set -C` | `read -r level` |
| `sessions/<sid>.ok` | empty; existence is approval | hook: `touch` | file test |

Valid id: `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$` (FR-L-05). `mkdir -p` under `umask 077`; no pruning; no in-place edits (FR-L-06). Dispatch: raw input holds `"tool_name"` means tool branch, else prompt branch (FR-L-08).

**Binding (FR-L-09).** B1 read stdin. B2 no `[sc-launch:` and no bound id seen (P2, P3 tests): exit 0. B3 no `jq`: marker text and no `"tool_name"` gives LL-NOBIND, else exit 0. B4 one `jq` prints `session_id`, `agent_id` (each `// "" | tostring | gsub("[\r\n\u0000]"; " ")`), then `prompt`; `jq` failure as B3. B5 `agent_id` set: exit 0. B6 strict marker: first `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere gives N; loose: prompt starts with `[sc-launch:` after leading space, tab, CR, LF and BOM; either present: EXIT trap to LL-NOBIND. B7 invalid id: marker gives LL-NOBIND, else exit 0. B8 already bound: `rm -f pending/N` if strict and present (level kept), run approval (section 6), exit 0. B9 unbound, no marker: exit 0. B10 `mkdir -p sessions`. B11 strict and `pending/N` exists: `mv pending/N sessions/<sid>` (atomic, single use). B12 still none and loose: `(set -C; printf 'degraded\n' > sessions/<sid>)`. B13 regular file exists: exit 0; else LL-NOBIND, exit 2.

**Resolution (FR-L-10).** P1 read stdin. P2 `compgen -G "$store/sessions/*"` empty: exit 0. P3 pure-bash loop over up to 64 `"session_id"\s*:\s*"<valid id>"` values; some found, none bound: exit 0. P4 EXIT trap; no `jq`: LL-BROKEN. P5 one `jq` prints `session_id`, `tool_name`, `skill // name`, `file_path // notebook_path`, `isolation`, then `command` last; failure LL-BROKEN. P6 bound id: that level; valid unbound id: exit 0; missing or invalid id: `worktree` + LL-STATE. P7 classify. Never read: `cwd`, `agent_id`, git, worktree files, `pipeline.json` (FR-L-11).

**Lifecycle.** No pruning (O-15). Release: `rm` both files (FR-L-07). Re-claim: new nonce and session (IR-5). `--resume` and renames stay governed (V14); `/clear` and `--fork-session` are ordinary (R4); so is a deleted file (R3).

**"Cannot edit" is a deny rule, not a wall.** The agent runs as the same OS user and could write every file. In a governed session, any Bash, Monitor, Edit, Write or NotebookEdit call that names the store, Claude Code settings or hooks, a git config file, or a reinstall is TAMPER at every level. Globs, brace expansion, variables, relative paths from another `~/.claude` folder and scripts are not caught (R1, R3).

## 4. Decision table

**Policy grid (FR-L-20).** A allow, B block. Held as one literal `case` in the script and as an independent hand-written oracle in the tests.

| Classes | W | WA | F | FS |
|---|---|---|---|---|
| NONE | A | A | A | A |
| IMPL, TURN | B | A | A | A |
| SUBMIT, COMMIT, PUSH, SKILL | B | B | B | A |
| REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG | B | B | B | B |

Message id is `LL-<class>`; PUSHFORM gives LL-PUSH-FORM, GHWRITE gives LL-GH-WRITE. Any blocked class blocks the call. Message precedence: BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL.

**Patterns (MR 6.2 rows).** Governed sessions; ordinary sessions always allow silently. Cells give A or the id without `LL-`. Full examples: MR 6.2 (DD-7).

| MR row | Examples | Class | W | WA | F | FS |
|---|---|---|---|---|---|---|
| 1 | Read, Grep, Glob, TaskCreate (unmatched) | n/a | A | A | A | A |
| 2, 8, 9, 11a, 12, 19, 24, 26, 29, 30 | Edit `/repo/src/x.py`; Skill `sc:workflow`; local Agent; Monitor `tail -f log`; `git status`; `git -C "$(git rev-parse --show-toplevel)" status` [B-10]; `gh api repos/o/r/pulls/5`; `orca worktree current` | NONE | A | A | A | A |
| 4 | Skill `sc:implement`, `sc:implement-protocol`, `task`, `sc:task-protocol` | IMPL | IMPL | A | A | A |
| 11 | CronCreate, ScheduleWakeup | TURN | TURN | A | A | A |
| 5, 20, 21 | Skill `sc:pr-submit`; `gh pr comment 5`; `gh pr ready 5`; `gh pr create --repo "$REPO" ...` | SUBMIT | SUBMIT | SUBMIT | SUBMIT | A |
| 22 | `gh pr create --title x` | SUBMIT, REPO | SUBMIT | SUBMIT | SUBMIT | REPO |
| 7 | Skill with no name | SKILL | SKILL | SKILL | SKILL | A |
| 13 | `git commit -m x`; `git revert x`; `sh -c "git commit -m x"`; ``git$'' commit -m x`` [B-2]; `git status && echo "I am done"` | COMMIT | COMMIT | COMMIT | COMMIT | A |
| 14 | `git push -u origin feature`; `git push origin <sha>:feature` | PUSH | PUSH | PUSH | PUSH | A |
| 15, 32 | `git push`; `git push --force origin f`; `cd x && git push origin a:b`; `bash -c "git push origin main"`; `timeout -s KILL 30 git send-pack <R> HEAD:refs/heads/main` [B-3]; `git log --grep push` | PUSH, PUSHFORM | PUSH | PUSH | PUSH | PUSH-FORM |
| 16 | `git push origin main`; `git push -u origin feature:main` | PROTECTED | PROTECTED | PROTECTED | PROTECTED | PROTECTED |
| 17, 32a | `git merge x`; `git pull`; `gh pr merge 5`; `gh repo sync` [B-3]; MCP `merge_pull_request`; `git log --grep merge` | MERGE | MERGE | MERGE | MERGE | MERGE |
| 17a, 32a | `gh api -X POST repos/o/r/merges`; `gh api graphql ...`; `gh api "repos/$REPO/pulls"`; `curl -X PATCH https://api.github.com/...` [B-7]; `gh pr create --repo o/r --title "fix api docs"` | GHWRITE | GH-WRITE | GH-WRITE | GH-WRITE | GH-WRITE |
| 18, 31 | `git -c alias.ci=commit ci`; `git $(echo push)`; `git worktree add`; `gh alias set co 'pr merge'`; `gi\` newline `t push ...` [B-1]; `if true; then git send-pack ...; fi` [B-3]; `git config --get-regexp alias.` | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| 23 | MCP `push_files`, `create_pull_request` | MCP | MCP | MCP | MCP | MCP |
| 6, 10, 25 | Skill `sc:issue`; Agent `isolation: "remote"`; Workflow; RemoteTrigger; SendMessage; `claude -p x`; `npx -y @anthropic-ai/claude-code@latest -p x` [B-8]; `orca terminal send`; `tmux send-keys approved Enter` | ESCAPE | ESCAPE | ESCAPE | ESCAPE | ESCAPE |
| 3, 27 | Edit `~/.claude/settings.json`; Write `~/.config/git/config` [B-4]; a `..` path; `rm -rf ~/.claude/state`; ``rm -rf ~/.cla$''ude/state`` [B-2]; `uv run python -m superclaude.cli.main install` [B-9] | TAMPER | TAMPER | TAMPER | TAMPER | TAMPER |
| 28 | Bash or Monitor over 65,536 bytes | BIG | BIG | BIG | BIG | BIG |
| 33 | pinned gaps: `G=gi; ${G}t push origin main`; `/usr/bin/gi[t] push origin main` [B-5]; `bash ./push.sh` | NONE | A | A | A | A |
| 34 | typed `approved`, `/sc:implement x` | prompt | A, writes `.ok` | A | A, no write | A, no write |
| 35 | marker prompt, unbound session | prompt | binds, or NOBIND | n/a | n/a | n/a |
| 36, 38 | `jq` missing or bad JSON with a bound id; internal error | failure | BROKEN | BROKEN | BROKEN | BROKEN |
| 37 | bad session file; bad id with non-empty store | failure | W + LL-STATE | WA if `.ok` | n/a | n/a |

## 5. Rules by tool

### 5.1 Bash and Monitor (FR-L-22 to FR-L-39, FR-L-44, FR-L-47 to FR-L-50)

`cmd` is the decoded `tool_input.command` of a Bash (foreground or background) or Monitor call. Monitor with only `ws`: NONE. No `${s//...}` over the text (fact T5).

**Normalisation, in order.** NM1: over 65,536 bytes gives BIG, stop. NM1a [B-1]: `[[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]` gives UNKNOWN. NM2 and NM3 [B-2] give T. NM4 gives G (never split). NM5 and NM6 give W. Segments [B-6]: always `IFS=';' read -r -a segs <<< "$W"`; words `ws=($seg)` under `set -f`. NM7: basename is the text after the last `/`.

```bash
T=$(printf '%s\n' "$cmd" | sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g')
G=" $(printf '%s\n%s\n' "$cmd" "$T" | tr 'A-Z' 'a-z' | tr -c 'a-z0-9._/~$@+:-' ' ') "
W=$(printf '%s\n' "$T" | tr '\n;&|()' ';;;;;;' | tr -c 'A-Za-z0-9._/=:@+~$;-' ' ')
```

**G0 words.** Git word: basename `git` or `^git-[a-z][a-z-]*$`. Gh word: basename `gh`. Gated: COMMIT `commit cherry-pick am commit-tree`; PUSH `push send-pack http-push` [B-3]; MERGE `merge pull`; `<name>` in `git-<name>` counts.

**G1, the global rule.** If G holds a git word, every gated word anywhere in G adds its class. Quoting, position and segments are ignored. Tests on G: `( |/)git(-[a-z][a-z-]*)? `, then `( |/git-| git-)(merge|pull) `, `( |/git-| git-)(push|send-pack|http-push) `, `( |/git-| git-)(commit|cherry-pick|am|commit-tree) `.

**G2 [B-3].** G holds a git word and a word containing `alias.`, `pushurl`, `insteadof`, `hookspath`, or starting `remote.`, `url.`, `include.`, `includeif.`, or equal to `set-url`: UNKNOWN.

**G3, command position.** The first word of a segment that is not: `NAME=...`; `-...`; `^[0-9]+(\.[0-9]+)?[smhd]?$`; a wrapper (`env sudo nohup exec command builtin timeout xargs setsid time nice stdbuf ionice doas unbuffer eval`); a shell (`bash sh zsh dash ksh`) plus `^-[a-z]*c$`; a reserved word (`if then else elif do while until coproc`) [B-3]. For a git word there, S is the first non-option word; `-C -c --git-dir --work-tree --namespace --config-env --attr-source` take a value.

| S | Class |
|---|---|
| none, with `--version`, `--help` or `-h`, or last value word `$` [B-10] | NONE |
| none, otherwise | UNKNOWN |
| `commit cherry-pick revert am commit-tree`; `update-ref` with later `HEAD`, `--stdin` or `refs/heads/...` | COMMIT |
| `merge pull`; `push` | MERGE; PUSH |
| `add apply bisect blame branch cat-file check-attr check-ignore check-ref-format checkout clean count-objects describe diff diff-files diff-index diff-tree fetch for-each-ref format-patch fsck gc grep hash-object help log ls-files ls-remote ls-tree merge-base merge-tree mv name-rev range-diff read-tree rebase reflog reset restore rev-list rev-parse rm shortlog show show-branch show-ref stash status switch tag var version whatchanged write-tree`, other `update-ref` | NONE |
| `remote` (next none, `-v`, `--verbose`, `get-url`, `show`); `config` (next `--get --get-all --get-regexp --list -l get list`); `worktree list` | NONE |
| anything else, `send-pack` included | UNKNOWN |

A git word outside command position gets no G3 class. **G4:** a git word anywhere whose S contains `$`: UNKNOWN.

**Canonical push (FR-L-33, FR-L-34).** Any call with PUSH, at every level, tests the raw `cmd`:

```
^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$
```

No match: PUSHFORM. Match: destination is capture 5, else 3, minus one `refs/heads/` or else `heads/`; `master` or `main` gives PROTECTED; `HEAD` gives PUSHFORM. Accept: PA1 `git push origin feature`, PA4 `git push origin 3f2a9c1e:feature/x`, PA6 `git push origin feature/main:feature/main`. Reject: PR1 backtick, PR3 `git-push`, PR6 `--force`, PR13 `upstream`, PR15 `cd x && ...`, PR24 `origin --all`; PD1 `git push origin main` (PROTECTED). Full lists in MR.

**gh (FR-L-35 to FR-L-39).** H1: group is the first non-option word after a gh word (skip `-R`, `--repo` values); action the next. H2: G holds a gh word and `api`: GHWRITE unless (1) raw `cmd` matches `^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$`, (2) no word after `api` matches `^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$`, (3) the endpoint exists, is not `graphql`, and does not end `/merge` or `/merges`. H3, first match wins: `api` no class; no group with `--version`/`--help` NONE; action `merge`, `update-branch`, `sync` MERGE anywhere [B-3]; group `alias`, `extension` or `$` in group or action UNKNOWN anywhere [B-3]; group `search status auth browse help completion` or action `view list status diff checks watch checkout` NONE; `pr create|edit|comment|ready`, `issue create|edit|comment` SUBMIT anywhere; else UNKNOWN in command position. H4: `pr create` with no `-R`, `--repo` or `--repo=` word anywhere adds REPO. H5: no gh word in the segment and a word with `repos/` ending `/merge(s)`: MERGE; a word with `api.github.com` or `uploads.github.com`: GHWRITE [B-7].

**Tamper (FR-L-49 to FR-L-51).** T, or an edit path after the same `/` squeeze, contains `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config` or `.config/git` [B-4]. Bash only: a word ending `.claude` or `.claude/`; a `superclaude` or `superclaude.*` word followed later in the segment by `install` [B-9]; a word containing `install_hooks`. Edit tools only: a `/../` segment or trailing `/..`. Contents, prompts and arguments are never checked.

**Escape (FR-L-47, FR-L-48).** `orca`: NONE if the segment ends `--help` or `-h`, w1 is `status`, `help`, `--version`, or w1 w2 is `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; else ESCAPE. `ccsession*`: ESCAPE. `claude`/`claude-code` (basename cut at `@`) [B-8] with any word in the whole command among `-p --print --continue --resume --bare --settings --dangerously-skip-permissions --fork-session --session-id --permission-mode`: ESCAPE. `tmux screen xdotool ydotool`: ESCAPE.

### 5.2 Other tools

- **Skill (FR-L-40):** name `skill`, else `name`; strip leading space, keep the first word, lower-case, drop one `/`, keep text after the last `:`, drop one leading `sc-` and one trailing `-protocol`. `implement`, `task`: IMPL. `pr-submit`: SUBMIT. `issue`: ESCAPE. Empty: SKILL. Else NONE (`task-builder`).
- **Agent, Task (FR-L-41):** same decisions; NONE, background or not, unless `isolation` is `remote` (ESCAPE). Prompt never scanned.
- **Edit, Write, NotebookEdit (FR-L-42):** tamper check only; source edits not gated (O-8).
- **Cron\*, Schedule\* (FR-L-43):** TURN. RemoteTrigger, Workflow, SendMessage: ESCAPE (FR-L-46).
- **MCP (FR-L-45):** N = text after the last `__`, lower-cased. No keyword (`merge push commit pull_request create_or_update_file delete_file update_ref create_ref create_branch`): NONE. Prefix `list_ get_ search_ read_`: NONE. Holds `merge`: MERGE. Else MCP.
- **Anything else matched (FR-L-52):** NONE on an explicit allow path.

## 6. Human approval and human versus agent

- **Event:** UserPromptSubmit only (O-4).
- **Match (FR-L-16):** whole prompt trimmed and lower-cased matches `^approved[.!]?$`, or first line matches `^/(sc:implement|sc:task|task)([[:space:]]|$)`. `/task-builder`, `/tasks`, `/sc:implement-protocol`, `please approved`, `approved, but`, `/sc:pr-submit` do not.
- **Where (FR-L-15):** bound session, no `agent_id`, level `worktree` (or invalid word). Nothing at `F`, `FS`.
- **Effect (FR-L-17):** `touch .ok`; `W` becomes `WA`. It unlocks IMPL (the grid also allows TURN at `WA`), never COMMIT, PUSH, SUBMIT or MERGE. A failed `touch` shows later as LL-IMPL. Lasts until a person deletes the files (O-6).
- **Order (FR-L-18):** the prompt event runs before expansion, so `.ok` exists before Skill `sc:implement-protocol`. OB-H1 item 4 checks; fallback is UserPromptExpansion with exact `command_name`.
- **Why the agent cannot fake it:** it cannot type a prompt; `agent_id` prompts are ignored; TURN is blocked at `W`; terminal and messaging tools are ESCAPE; in-word continuations are UNKNOWN [B-1]; self-started turns arrive wrapped, so never exactly `approved` (FR-L-19).
- **Rests on UNVERIFIED facts:** U4 (wrapping seen for background-task notices only), U5, U8, U17, U20, U26; prompts carry no origin field (V6), so another session typing `approved` counts as the person (R15).

## 7. Subagents and nested subagents

1. Identity is `session_id` only. If U1 holds, subagents are governed with no extra code.
2. `agent_id` is not read on PreToolUse; on prompts it means exit 0 (B5).
3. The Agent call is allowed (except `isolation: "remote"`); each later subagent call is checked.
4. **Ship gate U1 (FR-L-13):** no `full` or `--submit` claim on a real issue until OB-H1 item 1 shows the parent's `session_id` in subagent and nested-subagent payloads; no claim at any level until item 5 shows self-started turns wrapped.
5. **Reserve fallback off (FR-L-14):** no `cwd` fallback is built. If item 1 fails, stop and take O-9.

## 8. Fail-closed rules and speed

Ordinary sessions are never blocked by a failure (FR-L-53). Governed: default deny last line; EXIT trap maps other exit codes to LL-BROKEN (LL-NOBIND in the prompt branch); `set -u -o pipefail`, no `set -e`, no ERR trap; every `jq`, `sed`, `tr` status checked; no `onFailure` (FR-L-54 to FR-L-57).

| Failure (FR-L-56) | Decision |
|---|---|
| `jq` missing: ordinary / bound id / marker prompt | exit 0 / LL-BROKEN / LL-NOBIND |
| input not JSON | exit 0 if no bound id seen; else LL-BROKEN |
| session file bad word, empty, unreadable | `worktree` + LL-STATE |
| id missing or invalid, store non-empty | `worktree` + LL-STATE |
| Skill name unreadable / command over 64 KB | SKILL / BIG |
| `sed`, `tr` or internal error | LL-BROKEN |
| bind failure | LL-NOBIND |
| hook killed at timeout | call goes ahead (V8, R2) |
| session file deleted | ordinary (R3, O-16) |

Fast path: P2 is one `compgen`, P3 pure bash. Timeout: 5 s, both entries (FR-L-58). Cap: 65,536 bytes, governed only. Subprocesses: one `jq` per call past the prefilter; one `sed` and four `tr` for Bash text; one `sed` for an edit path; no git, network, Python, awk (FR-L-59).

| Budget (NFR-L-01; 100 runs, `time.monotonic()`) | Limit | Asserted |
|---|---|---|
| T-SPD-1, T-SPD-2 ordinary, empty and 1,050-file store | median 20 ms, p95 50 ms | reported |
| T-SPD-3 ordinary median against `block-bare-python.sh`, same run | 1.5 times | yes |
| T-SPD-4 governed allow and block | p95 60 ms | reported |
| T-SPD-5 governed 64 KB texts and 1 MB | under 1 s each | yes |

## 9. Block messages

To stderr, then exit 2. Header: `Launch-level guard: this session was started by /sc:issue --claim at level {level}.` then `Blocked:`, `Why:`, `You can:` lines and zero to two `Note:` lines. `{level}`: `worktree`, `worktree (approved)`, `full`, `full --submit`; LL-NOBIND and LL-BROKEN print `Launch-level guard:` alone when the level is unknown. Variables: `{level}`, `{store}`, `{sid}` only. Amendment marks are not printed (DD-3).

| Id | Blocked: | Why: | You can: |
|---|---|---|---|
| LL-IMPL | starting /sc:implement or /task (or their skills). | At the worktree level the agent stops at a plan until a person approves it. | Read the plan, then type /sc:implement or /task, or reply approved, in this session. |
| LL-COMMIT | creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref). | Only a launch with --pipeline full --submit lets the agent commit. | Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit. |
| LL-PUSH | a git push. | Only a launch with --pipeline full --submit lets the agent push. | Push the branch yourself after review, or claim the issue again with --pipeline full --submit. |
| LL-PUSH-FORM | a push that is not one plain git push command, or a command that names git and push together. | The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch. | Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out. |
| LL-PROTECTED | a push to master or main. | No launch level may change the main branch. | Push the feature branch by name, then merge it through a reviewed pull request. |
| LL-MERGE | a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool). | No launch level may merge; only a person reviews and merges. | Leave the merge to a person. To update the branch, run git fetch, then git rebase. |
| LL-GH-WRITE | a gh api call that is not one plain read command (it sets a method, a field or an input, calls graphql or a merge endpoint, or uses variables, quotes, pipes or other commands around it), or a gh command whose text mentions api, or a direct call to the GitHub API [B-7]. | In a launched session gh api may only read, and only in a form the guard can check: a gh api write can merge, comment or change the main branch. | Run the read as one plain command with every value written out, for example gh api repos/o/r/pulls/5 --jq .state, or use a gh command for the step (gh pr view --json, gh pr comment, gh pr create --repo ...) at a level that allows it, or ask the person. |
| LL-SUBMIT | /sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue). | Publishing work needs a launch with --pipeline full --submit. | Run it yourself in your own session, or claim the issue again with --pipeline full --submit. |
| LL-REPO | gh pr create without --repo. | Without --repo, gh can open the pull request on the parent repository of a fork. | Retry with --repo <owner>/<name> (or -R). |
| LL-UNKNOWN | a git or gh command the guard does not recognise (an unknown subcommand, a git alias definition, or a subcommand built from a variable or a substitution), or a line continuation inside a word [B-1]. | In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge. | Use the standard command written out (for example git status, git diff, git add), or ask the person to run it. Write the command on one line [B-1]. |
| LL-MCP | a GitHub write through an MCP tool. | The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh. | Use git or gh for this step. |
| LL-ESCAPE | starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool). | That work would run outside this session's launch level. | Do the work here (local subagents are allowed), or ask the person to start it. |
| LL-TURN | scheduling a turn (a cron job or a wake-up) before the plan is approved. | Its prompt text arrives later as a new turn and could look like a person replying approved. | Wait until the person approves the plan, or use a background task or a monitor instead. |
| LL-TAMPER | touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks. | The session must not change its own limits. | Ask the person. To release this session they run, in their own terminal: rm "{store}/sessions/{sid}" "{store}/sessions/{sid}.ok" |
| LL-SKILL | a skill call whose name the guard cannot read. | The guard cannot tell whether the skill is allowed at this level. | Report it (the hook input format may have changed); the person can release the session. |
| LL-BIG | a command longer than 64 KB. | The guard cannot check a command that long in time. | Write the content to a file with the Write tool, then run a short command. |
| LL-BROKEN | this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error). | In a launched session the guard fails closed. | Install jq, or ask the person to release the session by deleting its files in {store}/sessions/. |
| LL-NOBIND | this launch prompt. | The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced. | Check that jq is installed and {store} is writable, then claim the issue again. |

With an invalid `{sid}`, LL-TAMPER uses the LL-BROKEN wording. Notes, LL-STATE first (DD-4):

- **LL-STATE** (level came from an invalid word or id): `Note: the launch record was missing or unreadable, so the strictest level (worktree) applies.`
- **LL-TEXT** (class came from Bash or Monitor text): `Note: the guard does not tell quoted text from commands. Any command that names git together with the word commit, push, merge or pull, or gh together with the word api, counts as that action, even if the words are only in a message, a title, a PR body or a search pattern. If that is the case here, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>, or reword the search or title.`

## 10. Edge-case table

| Case | Decision | Rule |
|---|---|---|
| ordinary payload with a forged nested bound id | allow | P3, P6, T-ISO-6 |
| person's own session or subagent in the worktree | allow | FR-L-11, T-ISO-4 |
| id missing, store non-empty | `W` + LL-STATE | P6 |
| invalid id in a marker prompt | LL-NOBIND | B7 |
| malformed marker at start | binds `degraded` | B12 |
| strict marker mid-prompt, no record | LL-NOBIND | B13, O-20 |
| malformed marker mid-prompt | ignored | R6 |
| nonce reused by a second session | `degraded` | B11, T-BIND-9 |
| new marker in a bound session | record removed, level kept | B8 |
| `sessions/` read-only | LL-NOBIND | T-BIND-7 |
| `--resume`; worktree renamed | still governed | V14 |
| `/clear`, `--fork-session` | ordinary | R4 |
| session file deleted elsewhere | ordinary | R3, O-16 |
| `approved` at `F` | allow, no write | FR-L-15 |
| `approved` from a subagent | ignored | B5 |
| typed `/sc:implement`, then Skill call | allow | T-APR-9 |
| PR title "docs: explain git hooks" at `FS` | allow | T-GH-12 |
| PR body naming "pull request" and "git" | MERGE + LL-TEXT | O-21 |
| `git stash push -m wip` | PUSH, PUSHFORM at `FS`; use `git stash -u -m x` | R8 |
| `git push origin f 2>&1 \| tail -5` at `FS` | LL-PUSH-FORM | O-18 |
| `git push origin x:refs/heads//main` at `FS` | allow; git rejects it | FR-L-34 |
| `git -c remote.origin.push=... push origin f` | LL-UNKNOWN by precedence | DD-5 |
| `git config --get remote.origin.url` | LL-UNKNOWN | R8 (d) |
| heredoc line `all:\` | LL-UNKNOWN; use Write | R8 (h) |
| `orca \` newline `worktree list` | ESCAPE | FR-L-47 |
| commit scope `fix(ccsession): x` | ESCAPE | R8 (e) |
| `git add src/superclaude/cli/install_hooks.py` | TAMPER | R8 (f) |
| Write content quoting `.claude/hooks` | allow | FR-L-51 |
| Monitor with only `ws` | NONE | FR-L-22 |
| Bash named `mcp__<server>__<word>_Bash` | unmatched, allow | U21 |
| 65,537 bytes of multi-byte text | BIG | T-FC-7 |

## 11. Test plan

`tests/hooks/test_launch_level_guard.py` (proposed) runs the real script with `subprocess.run`, a temporary `HOME` and a controlled `PATH`, like `test_block_bare_python.py`. Oracle `EXPECTED` is hand-written from section 4. Observed checks are `pytest.skip(...)` bodies. Run `uv run pytest tests/hooks/ -v`. Every T- id of MR 8.2 is built; minimum per AC:

| AC | Cases |
|---|---|
| AC-1 | T-GRID-3, T-SKL-1, T-APR-5, T-APR-9, T-NRM-8, T-GIT-18 |
| AC-2 | T-GRID-4, T-GRID-5, T-GIT-17, T-PSH-8, T-PSH-11, T-GH-12 |
| AC-3 | T-APR-1 to T-APR-4, T-APR-10, T-TRN-1, T-TRN-4 |
| AC-4 | T-ISO-1, T-ISO-4, T-ISO-7, T-ISO-8, T-ISO-9, T-REG-3 |
| AC-5 | T-BIND-2, T-BIND-7, T-BIND-13, T-TAM-1, T-TAM-2, T-TAM-6, T-FC-2 |
| AC-6 | T-PSH-4, T-PSH-12, T-GIT-9, T-GIT-14, T-NRM-1, T-GH-2, T-GH-11, T-GH-14, T-MCP-1, T-COR-2 |
| AC-7 | T-MSG-1, T-MSG-2, T-MSG-3, T-FC-3 |
| AC-8 | T-GRID-1, T-GRID-2, T-SPD-1..5, T-COR-1, T-GAP-1 |

**Corpus.** The implementer copies the full corpus from MR section 8 (8.3 and 8.4) unchanged (DD-2). Categories: push routes (T-ATK-1, 13, 25, 29, 50); aliases and variable subcommands (T-ATK-10, 35, 42); `gh api` writes (T-ATK-6, 18, 47); merges (T-ATK-48, 49, 51); tamper and escape (T-ATK-21, 55, 60); accepted leaks pinned `allow` (T-ATK-26 to 28, N-ATK-7, 31, 36); benign (T-OK-1 to 36); pinned over-blocks (T-OVR-1 to 6); amendment attacks (N-ATK-1 to 39). T-COR-2 replays the rows MR marks "real" on a temporary bare remote.

**Observed checks.**

- **OB-H1** (first; log-only hook). Records: (1) subagent and nested-subagent `session_id`, `agent_id`, `agent_type` (U1); (2) Skill keys, name form (U2); (3) Agent name, `isolation` (U3, U13); (4) typed `/sc:implement x` (O-4); (5) exact `prompt` of a Monitor line `approved` and of background-Bash and background-subagent notices (U4, O-17); (6) `TaskCreate` versus the anchored matcher (U15); (7) SendMessage, MCP names (U12); (8) `claude` without `-p` (U14); (9) Bash, Edit, Write, Skill names (U21).
- **OB-H2** (after the claim feature ships). Session file before the first tool call (U8); exact first prompt and marker position (U7); hook `HOME` and `CLAUDE_CONFIG_DIR`; IR-4 refusals; LL-NOBIND visibility (U20).
- **OB-H3** (test issue, each level). `W` stops and unlocks by both routes; `F` logs git commands (U10); `FS` runs one `/sc:pr-submit --monitor 3` cycle logging pushes and inline `gh api` (O-18, O-19) and a conflict (O-10); a `main` push and a merge blocked; counts of LL-PUSH-FORM, LL-GH-WRITE, LL-TEXT and NM1a or G2 UNKNOWN (O-21); Orca preamble (O-11); a live message (AC-7); timing.

## 12. Acceptance criteria map

Verdicts are the final review's, of the plan as reviewed. No review checked the amendments, so no verdict changed.

| AC | Verdict | Amendments meant to change (unreviewed) | Still open |
|---|---|---|---|
| AC-1 | NOT MET | B-1, B-2, B-3 close one-line commit, merge, push routes | built names (R1), R9, O-8 |
| AC-2 | NOT MET | B-3 redirect keys, B-4 `.config/git`, B-10 retry block | O-10, O-18, O-19, O-21 |
| AC-3 | NOT MET | B-1 makes `tm\`, `or\` spellings UNKNOWN | U4, O-17, R16 |
| AC-4 | MET WITH CAVEAT | none (U21 added) | OB-H1 item 1, else O-9 |
| AC-5 | NOT MET | B-1, B-2 close N-ATK-29, 30, 32, 33; B-9 reinstall | R3, O-16, N-ATK-31 |
| AC-6 | NOT MET | B-1 to B-4, B-7; copy blocked 35 of 38 | R1, R11; O-22 |
| AC-7 | MET | B-1, B-7 wording | none |
| AC-8 | MET WITH CAVEAT | amendment corpus added | only corpus routes shown; speed untimed |

## 13. Registration, install and claim-feature interface requests

Append to `UserPromptSubmit` and to `PreToolUse` in `src/superclaude/hooks/hooks.json`; existing entries, such as Bash `block-bare-python.sh`, stay.

```json
{ "hooks": [ { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 } ] }
{ "matcher": "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)",
  "hooks": [ { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 } ] }
```

No UserPromptExpansion, SessionStart or `onFailure` (FR-L-63). Anchors are U15; the script re-checks names (FR-L-66). Add `"launch-level-guard.sh"` to `_FRESHNESS_SCRIPTS` (not the Makefile). Run `make sync-dev`, `make verify-sync`; stage `src/` and `tests/` only.

- **IR-1** Before `orca agent launch`, write `pending/<nonce>` (one word) atomically; nothing for `--pipeline none`.
- **IR-2** Nonce `secrets.token_hex(16)`; prompt starts `[sc-launch:v1:<nonce>] `.
- **IR-3** `pipeline.json` is documentation only; amend FR-31.
- **IR-4** Refuse to launch unless `jq` exists, the installed script is executable, and `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json` registers it on both events.
- **IR-5** Re-claim: new session, new nonce, never `--resume`.
- **IR-6** Claim output says how to release a session.

## 14. Order of work

1. **OB-H1.** Proves U1 and turn wrapping. Gate: item 1 fails, stop (O-9); item 5 bare, apply O-17 alternative.
2. Skeleton (dispatch, store, binding, resolution, trap, printer). Proves harmless: T-ISO-1, 5, 6, T-FC-*, T-BIND-*.
3. Normalisation and classifiers: T-NRM, T-GIT, T-PSH, T-GH, T-MCP, T-SKL, T-ESC, T-TRN, T-TAM, T-COR.
4. Policy and messages: T-GRID, T-MSG.
5. Approval: T-APR.
6. Registration: T-REG, T-SPD.
7. Hand IR-1 to IR-6 to the claim feature. 7a. Only if the owner confirms O-22: the git-level layer.
8. **OB-H2**, then **OB-H3**. Gate: no real governed launch until both pass.

## 15. Open decisions

### 15.1 Owner decisions O-1 to O-22 (default is in force)

| Id | Question | Default | Alternative |
|---|---|---|---|
| O-22 | add a structural git-level layer (L2, `pre-push` per worktree refusing `main`, `master`)? | orchestrator: yes as step 7a, text layer kept; owner decides; open: install place (U28), hook chaining, removal, tests | text classifier only (R1) |
| O-21 | quoted-text over-match | accept; LL-TEXT; OB-H3 counts | drop `am` after OB-H3 |
| O-1 | `cwd` check at bind | no | mismatch binds `degraded` |
| O-2 | `--force` at `FS` | blocked | admit `--force-with-lease` |
| O-3 | `gh pr ready` | SUBMIT | never |
| O-4 | UserPromptExpansion | no | exact `command_name` |
| O-5 | issue number in header | no | store it |
| O-6 | approval lifetime | session | expire or bind to plan |
| O-7 | built names and scripts uncovered | accept | `$` in command position is UNKNOWN; or O-22 |
| O-8 | gate source edits at `W` | no | `.dev/` only |
| O-9 | subagent id differs | stop | reserve `cwd` fallback |
| O-10 | sync merge at `FS` | blocked | allow `--no-commit`, `--abort` |
| O-11 | Orca worker commands | none | allowlist them |
| O-12 | compare `--repo` to `origin` | no | read at bind |
| O-13 | more IMPL skills | no | add names |
| O-14 | MCP writes at `FS` | blocked | allow non-`main` |
| O-15 | old state files | person removes | prune on re-claim |
| O-16 | deleted file is ordinary | accept | read `transcript_path` (U27) |
| O-17 | self-started turns | allowed | block at `W` |
| O-18 | compound push at `FS` | blocked | widen form |
| O-19 | non-canonical `gh api` | blocked | admit GET variants |
| O-20 | strict marker, no record | block prompt | ignore |

### 15.2 Blocking findings of the three plan reviews

Status as in MR 11.2 (which names the confirming review). Default for all: keep the rule now in force.

| Id | Finding | Rule now | Status | Alternative |
|---|---|---|---|---|
| OD-R1-B1 | backtick hid a refspec to `main` | FR-L-33 | closed | reopen if T-PSH-12 fails |
| OD-R1-B2 | backslash-newline split a push | FR-L-33, FR-L-25 | closed | reopen if T-NRM-5 fails |
| OD-R1-B3 | dashed built-ins unseen | FR-L-28 | closed | reopen if T-GIT-12 fails |
| OD-R1-B4 | `gh api` writes read as reads | FR-L-36 | closed | O-19 |
| OD-R1-B5 | normalisation unnamed, boundaries lost | FR-L-25 to 27 | closed | none |
| OD-R1-B6 | background subagent turns uncovered | FR-L-19, O-17 | closed | O-17 alternative |
| OD-R1-B7 | deleted file ordinary, unstated | FR-L-56, R3 | closed | O-16 alternative |
| OD-R1-B8 | false "messages pass" claim | FR-L-29, R8 | closed | O-21 alternative |
| OD-R2-F1 | nested alias pushed to `main` | G1, G2, G4 | closed | none |
| OD-R2-F2 | option after `origin` moved `main` | FR-L-33 | closed | none |
| OD-R2-F3 | shell-built `gh api` flag | FR-L-36 | closed | O-19 |
| OD-R2-F4 | `rm -rf ~/.claude/state` allowed | FR-L-49, R3 | fixed in a fix cycle but NOT confirmed by any later review | O-16 alternative |
| OD-R2-F5 | `$GIT push` gap unstated | R1, O-7 | fixed in a fix cycle but NOT confirmed by any later review | O-7 (a), O-22 |
| OD-R2-F6 | quoted `>` deleted git word | FR-L-26, 27 | closed | none |
| OD-R2-F7 | quoted value shifted subcommand | G1 | closed | none |
| OD-R2-F8 | PR title blocked as git | FR-L-31, 37 | closed | none |
| OD-R3-B1 | in-word continuation hides names | FR-L-24 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B2 | `$''` splices hide words | FR-L-25 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B3 | hidden command position, `send-pack`, redirects, gh merges | FR-L-28 to 31, 37 | OPEN (amended, not re-reviewed) | drop; O-22 |
| OD-R3-B4 | `~/.config/git/config` redirect | FR-L-49 | OPEN (amended, not re-reviewed) | drop; R11 |
| OD-R3-B5 | glob and brace spellings unlisted | R1, R3, T-GAP-1 | OPEN (amended, not re-reviewed) | O-22 (push part) |
| OD-R3-B6 | segment split skipped | FR-L-27 | OPEN (amended, not re-reviewed) | none |
| OD-R3-B7 | `curl` PATCH moves `main` | FR-L-39 | OPEN (amended, not re-reviewed) | drop; R10 |
| OD-R3-B8 | versioned `npx` Claude Code | FR-L-48 | OPEN (amended, not re-reviewed) | drop; R5 |
| OD-R3-B9 | reinstall by module name | FR-L-50 | OPEN (amended, not re-reviewed) | drop; residual |
| OD-R3-B10 | `/sc:implement` retry block UNKNOWN | FR-L-31 | OPEN (amended, not re-reviewed) | drop; AC-2 breaks |

Counts: 26; 14 closed, 2 fixed but not confirmed, 10 open.

## 16. Residual risks and UNVERIFIED items

| R | Not stopped | Tolerated by |
|---|---|---|
| R1 | scripts; names from variables, escapes, globs | pinned allow; O-7, O-22 |
| R2 | timeout or crash allows | 1 s budget at 5 s |
| R3 | indirect store delete | direct names TAMPER; O-16 |
| R4 | person's bypass flags | person's choice; IR-4 |
| R5 | `claude` started without tmux | terminal tools ESCAPE |
| R6 | malformed late marker | OB-H2 |
| R7 | startup-file alias | accepted |
| R8 | over-blocks (a) to (i) | LL-TEXT; O-21 |
| R9 | local plumbing commits | local only |
| R10 | GitHub writes by programs, unmatched MCP | `curl` GHWRITE |
| R11 | pre-set push config | agent cannot set one |
| R12 | hostile agent | out of scope |
| R13 | person pastes a marker | `rm` releases |
| R14 | U1 or U8 false, checks skipped | OB gates |
| R15 | other session types `approved` | agent cannot |
| R16 | bare self-started turn | OB-H1 5; O-17 |
| R17 | aliases from non-tamper config | needs setup first |

UNVERIFIED (MR 12): U1 subagent id (ship gate); U2 Skill key; U3 `Task` name; U4 turn wrapping; U5 queued prompt; U6 `--bare`; U7 Orca preamble; U8 bind timing (OB-H2 mandatory); U9 `command_name` (moot); U10 `/sc:implement` git use; U11 Monitor fields; U12 MCP names; U13 `isolation` key; U14 `claude` without `-p`; U15 matcher anchors (names re-checked); U16 push options (moot); U17 subagent prompts (ignored); U18 `/clear` id; U19 `/` escapes (moot); U20 blocked prompt visible; U21 tool names; U22 BSD tools (T-NRM-6); U23 `send-pack` https (moot); U24 gh alias (R17); U25 `orca -h`; U26 tmux pane; U27 `transcript_path`; U28 Orca hooks (O-22).

## 17. Design decisions taken by the designer

| Id | Decision | Reason |
|---|---|---|
| DD-1 | fixed ten-part script layout (section 2) | follows MR 4 and NFR-L-03 order |
| DD-2 | tests copy MR 8.3 as one text block and MR 8.4 as tuples | one source, diffable |
| DD-3 | `[B-n]` marks in messages are not printed | they mark provenance |
| DD-4 | LL-STATE prints before LL-TEXT | MR gives no order |
| DD-5 | oracle expects LL-UNKNOWN for PR8, PR9; T-PSH-12 still accepts either | precedence is fixed; MR tolerance kept |
| DD-6 | OB-H1 fixtures named `item<n>-<shape>.json` | tests load by item |
| DD-7 | sections 4, 11 show representative examples | size limit; MR has full lists |
| DD-8 | grid and pattern rows with equal cells are grouped | shorter; T-GRID-2 checks each class |

## 18. Traceability

| MR | Here |
|---|---|
| FR-L-01 to 11 | 3 |
| FR-L-12 to 14 | 7 |
| FR-L-15 to 19 | 6 |
| FR-L-20, 21; MR 6, 7 | 4, 9 |
| FR-L-22 to 52 | 5 |
| FR-L-53 to 59, NFR-L-01, 02 | 8 |
| FR-L-60 to 66, IR-1 to 6 | 13 |
| MR 8, 9, 10 | 11, 12, 14 |
| O, OD, MR 13 | 15 |
| R, U | 16 |

Full corpus, debate record and reviews: `.dev/brainstorms/20261105-170229-launch-level-hook/` (`merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review*.md`, `refactor-plan.md`).
