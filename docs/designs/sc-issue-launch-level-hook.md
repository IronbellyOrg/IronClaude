---
title: "Launch-level enforcement hook: design"
issue: IronbellyOrg/IronClaude#394
type: architecture
format: spec
status: "built: L1 guard script, its two registrations, installer entry, claim IR-1, IR-2 and IR-4 to IR-7 detection (IR-3 documentation only; IR-4 refusal; IR-7 only warns, W-L2-ABSENT) and the scoped job identity foundation; pending: OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX and the L2 pre-push layer"
review_status: "one authorized simulated spec-panel iteration, followed by scoped identity implementation and per-task compliance checks; full enforcement not runtime-approved"
adversarial_status: partial
historical_convergence: "1.00 by the earlier protocol rule (0.70 identical verdicts); not this panel's score"
planning_status: "L1 built after the B-CTX evidence review (L1: PROCEED); L2 blocked on B-CTX (L2: BLOCKED); no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass (§7 U1: item 1 before full or --submit, item 5 before any level; OB-H2 and OB-H3: §11, §14)"
source: .dev/brainstorms/20261105-170229-launch-level-hook/
generated: 2026-11-05
---

# Launch-level enforcement hook: design

> **Full enforcement is not runtime-approved.** The authorized specification panel found the blocking actor-selection prerequisite B-CTX (§19.1). The owner subsequently authorized a narrowly scoped launcher/harness identity integration. That Bash job identity foundation is implemented separately (§19.7); isolated live CLI observations distinguish a rewritten governed call from an unchanged ordinary call. This does not build the main classifier, claim pipeline or production pre-push guard, and does not prove real `/clear`, Monitor or every lifecycle variant. O-22 remains accepted. The earlier blocked plan stays blocked; OB-H1 to OB-H3 and full enforcement integration remain required. The later implementation of issue #394 built the L1 guard and the claim-side checks; §19.8 lists what exists and what is still pending.

This updated design is authoritative for **new planning**. `merged-requirements.md` ("MR"), the Q1–Q4 debate outputs and the earlier plan reviews are historical/advisory inputs, not synchronized copies. Identifiers FR-L-nn, IR-n, O-n, OD-..., R-n, U-n, LL-..., T-... retain traceability; explicit changes here override older wording/expected results. `[B-n]` identifies an earlier amendment's provenance, not a current approval. The earlier failed verdicts remain historical in §12/§15.2. Panel findings, the full guard boundary table, quantity-flow analysis and the written document-change plan are in `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md`. No further panel or debate loop is selected.

## 1. Purpose and scope

One script, `launch-level-guard.sh`, enforces the level that `/sc:issue --claim --pipeline <level>` gives a launched agent. Only sessions the claim script launched are governed; every other session is ordinary and never blocked.

| Level | Short | Allowed |
|---|---|---|
| worktree, before approval | `W` | planning only |
| worktree, after approval | `WA` | implement; no commit, push, publish |
| full | `F` | implement; no commit, push, publish |
| full with `--submit` | `FS` | commit, push a feature branch, open a PR |

Policy intent: no level authorizes a merge or a push to `master` or `main`. Coverage is the explicitly checked routes, not universal prevention. Targets: TH1 (honest drift) and TH2 (specified one-step workarounds); not TH3 (deliberate evasion). Same-user guardrail, not a sandbox. A person's push from the **same** launched worktree must stay unrestricted by launch policy, even while an agent is active; deleting a marker is not a prerequisite for that right.

In scope: L1 text/skill hook, two Claude registrations, installer-list entry, tests, IR-1 to IR-7 and accepted O-22 L2 pre-push design (§19). L1 uses bash plus `jq`, `sed`, `tr`: exit 0 allows, exit 2 blocks, no `onFailure`. L2 is a separate Git hook with Git's nonzero-veto convention and necessarily uses Git's resolved update stream. Its process-context candidate is Linux-only until proven otherwise; its process reads are not part of the old L1 subprocess budget. No new runtime service, server policy, managed settings deployment, shell parser, forwarding framework or config migration is authorized. Claim launching and ccsession implementation are separate integration work; the claim code now implements IR-1, IR-2 and IR-4 to IR-7 (IR-7 as the warning W-L2-ABSENT), and IR-3 stays documentation only because no code writes `pipeline.json` (§19.8). Issue #322's source-write boundary and reading `pipeline.json` remain out of scope.

## 2. Architecture and files

| File | Role | Change | Status |
|---|---|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh` | L1 script; flat bash, `LC_ALL=C`, executable (FR-L-60) | new | proposed |
| shared Git `hooks/pre-push` | separate L2 artifact; owned install only, actor-selection gate (§19) | new | proposed, blocked by B-CTX |
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
first prompt (UserPromptSubmit)    consume nonce; publish sid without replacement, or degraded; else NOBIND
  v
each matched call (PreToolUse)     no bound id: exit 0 | jq -> level -> classes -> grid -> exit 0 or 2  FR-L-10
  v
typed prompt (UserPromptSubmit)    "approved" or /sc:implement /sc:task /task at W: touch <sid>.ok  FR-L-15
  v
release                            a person runs rm sessions/<sid> sessions/<sid>.ok  FR-L-07
```

Script layout (DD-1): settings (`LC_ALL=C`, `set -u -o pipefail`, `set -f`, `umask 077`); store path; messages; dispatch; prompt branch; fast paths; one `jq` read; classifiers adding classes; one `case` on `CLASS:LEVEL`; last line LL-BROKEN, exit 2. The earlier estimate was about 450 lines for L1 (NFR-L-03), not a measured size or a budget for L2. Keep added process-context handling separate and gated (§19).

## 3. State and why the agent cannot edit it

Store: `$HOME/.claude/state/launch-level/`, built from three literal parts so the script text never holds `.claude/state` (FR-L-01, T-TAM-8).

| File | Content | Writer | Reader |
|---|---|---|---|
| `pending/<nonce>` | name `^[0-9a-f]{32}$`; one word `worktree`, `full`, `full-submit` | claim script; complete atomic publication (IR-1) | hook: consume once; never replace a bound sid |
| `sessions/<sid>` | exactly one allowed word plus optional terminal newline; malformed, empty or unreadable means `worktree` + LL-STATE on a block (FR-L-03) | hook: atomic create-without-replacement; first binding retained | bounded exact record read |
| `sessions/<sid>.ok` | empty; existence is approval | hook: `touch` | file test |

Valid id: a **top-level JSON string** matching `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$` (FR-L-05); never coerce numbers/objects or replace control characters to manufacture an id. `mkdir -p` under `umask 077`; no pruning or in-place edits. Pending/session/approval records must be regular nonsymlink files in owned directories; an invalid object at a positively bound path is state failure, never a valid level/approval. This is integrity hygiene, not same-user access control. Dispatch (FR-L-08) uses parsed top-level `hook_event_name`, exactly UserPromptSubmit or PreToolUse; prompt text or nested `tool_name` keys cannot select the branch. Unknown/inconsistent event shape uses the identity-loss rule below.

**Binding (FR-L-09, revised B1–B13).** Read and parse once. No marker and no session records permits the empty-store fast exit. A strict marker is the first `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere; a loose marker starts the prompt after whitespace/BOM with `[sc-launch:`. No `jq`/parseable envelope means no inferred binding; a recognizable launch-marker prompt fails LL-NOBIND rather than launching ungoverned. A nonempty string `agent_id` ignores the prompt. Invalid session id with a marker is LL-NOBIND; without one, apply identity-loss behavior. Already bound: preserve the level, optionally consume a newly supplied pending nonce, and run approval. Unbound with no marker: allow. Otherwise create the store, consume one pending nonce once and publish the level **atomically without replacing an existing binding**. Racing publishers must preserve the first binding and re-read it; no check-then-overwriting `mv`. A missing/used nonce with a leading loose marker publishes `degraded` under the same no-replacement discipline. A strict marker only in the middle without a usable record gives LL-NOBIND (O-20). Failure to obtain a valid binding gives LL-NOBIND. The implementer must test concurrent consumption and publication; exact shell primitive is an implementation choice, not permission to overwrite a winner.

**Resolution (FR-L-10, revised P1–P7).** Empty session store: allow. Otherwise use one `jq` extraction of the actual top-level fields; **remove the fixed-64 raw-id early-allow loop**. Nested/duplicate-looking strings do not establish ordinary status. Extract session id, event, tool name and typed tool fields, preserving command as a string. `skill` is used if present/non-null, otherwise `name`; an explicit empty string stays empty (SKILL), not an alternate-name escape. File-path fallback uses the same missing/null rule. Nonstring tool fields or embedded NUL are input errors, not silently converted commands. Valid unbound id: allow silently. Valid bound id: read its exact level and apply policy. Positively identified governed input errors/internal failures block LL-BROKEN; unreadable/malformed bound level becomes W, approval may still yield WA. L1 tool resolution does not infer authority from `cwd`, git/worktree files, `agent_id` or `pipeline.json`.

**Identity loss (panel F2/F3).** A nonempty store alone never proves this caller is governed. Missing/invalid id or an unparseable envelope without independent positive binding evidence cannot be assigned W or blocked merely because another session exists: allow without claiming enforcement. This replaces the old P6 missing-id fallback and its MR test expectations. It is a declared fail-open limit, not proof of safe operation. OB-H1/OB-H2 must show a valid top-level string id and consistent event shape on every supported governed call; otherwise deployment stops. If fail-closed behavior under identity loss is needed, it requires the independently proven process context of B-CTX (§19.1), not a worktree-wide fallback. No raw substring match or environment variable counts as that proof.

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
| 4 | Skill `sc:implement`, `sc:implement-protocol`, `task`, `sc:task-protocol`, `sc:improve`, `sc:cleanup`, `sc:spawn`, `sc:build` [O-13] | IMPL | IMPL | A | A | A |
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
| 37 | bad positively bound session file | failure | W + LL-STATE on block | WA if valid `.ok` | n/a | n/a |
| panel F2 | missing/invalid id with unrelated nonempty store | identity loss | allow, no enforcement claim | allow | allow | allow |

## 5. Rules by tool

### 5.1 Bash and Monitor (FR-L-22 to FR-L-39, FR-L-44, FR-L-47 to FR-L-50)

`cmd` is the decoded `tool_input.command` of a Bash (foreground or background) or Monitor call. Monitor with only `ws`: NONE. No `${s//...}` over the text (fact T5).

**Normalisation, in order.** NM1: over 65,536 bytes gives BIG, stop. NM1a [B-1]: `[[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]` gives UNKNOWN. (Note: that printed test never matches, because a quoted `$'...'` on the right of `=~` is matched as literal text; the implemented script holds the pattern in a variable, `LL_RE_NM1A`, and tests `[[ $cmd =~ $LL_RE_NM1A ]]`.) NM2 and NM3 [B-2] give T. NM4 gives G (never split). NM5 and NM6 give W. Segments [B-6]: always `IFS=';' read -r -a segs <<< "$W"`; words `ws=($seg)` under `set -f`. NM7: basename is the text after the last `/`.

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

A git word outside command position gets no G3 class. **G4:** compute S with the same option/value skipping after **each** git-word occurrence in its segment, even outside command position; if that S contains `$`, add UNKNOWN. Reset S/options for every occurrence and segment. A value-taking Git/gh option with no following value adds UNKNOWN; help/version does not excuse a dangling required value. This is lexical classification, not shell execution or a promise to reconstruct quoted argument boundaries; B-10's explicit last-value-dollar exception remains.

**Canonical push (FR-L-33, FR-L-34).** Any call with PUSH, at every level, tests the raw `cmd`:

```
^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$
```

No match: PUSHFORM. Match: destination is capture 5, else 3, minus one `refs/heads/` or else `heads/`; `master` or `main` gives PROTECTED; `HEAD` gives PUSHFORM. Accept: PA1 `git push origin feature`, PA4 `git push origin 3f2a9c1e:feature/x`, PA6 `git push origin feature/main:feature/main`. Reject: PR1 backtick, PR3 `git-push`, PR6 `--force`, PR13 `upstream`, PR15 `cd x && ...`, PR24 `origin --all`; PD1 `git push origin main` (PROTECTED). Full lists in MR.

**gh (FR-L-35 to FR-L-39).** H1: group is the first non-option word after a gh word (skip `-R`, `--repo` values); action the next. H2: G holds a gh word and `api`: GHWRITE unless (1) raw `cmd` matches `^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$`, (2) no word after `api` matches `^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$`, (3) the endpoint exists, is not `graphql`, and does not end `/merge` or `/merges`. H3, first match wins: `api` no class; no group with `--version`/`--help` NONE; action `merge`, `update-branch`, `sync` MERGE anywhere [B-3]; group `alias`, `extension` or `$` in group or action UNKNOWN anywhere [B-3]; group `search status auth browse help completion` or action `view list status diff checks watch checkout` NONE; `pr create|edit|comment|ready`, `issue create|edit|comment` SUBMIT anywhere; else UNKNOWN in command position. H4: for each recognized `pr create` occurrence, require a nonempty operand after `-R`/`--repo`, or nonempty suffix in `--repo=<value>`, in that occurrence's segment; otherwise add REPO. A detached operand must not be another option. This replaces the anywhere-presence test, but normalization still loses quoted argument boundaries: option-looking title/body text can collide. That is a stated lexical limit, not validated repository selection; O-12 still does not compare the value to origin. H5: no gh word in the segment and a word with `repos/` ending `/merge(s)`: MERGE; a word with `api.github.com` or `uploads.github.com`: GHWRITE [B-7].

**Tamper (FR-L-49 to FR-L-51).** T, or an edit path after the same `/` squeeze, contains `.claude/state`, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config` or `.config/git` [B-4]. Bash only: a word ending `.claude` or `.claude/`; a `superclaude` or `superclaude.*` word followed later in the segment by `install` [B-9]; a word containing `install_hooks`. Edit tools only: a `/../` segment or trailing `/..`. Contents, prompts and arguments are never checked.

**Escape (FR-L-47, FR-L-48).** `orca`: NONE if the segment ends `--help` or `-h`, w1 is `status`, `help`, `--version`, or w1 w2 is `worktree current|list|show`, `terminal list|show|read`, `orchestration check|inbox|run-current|task-list|worker-show`; else ESCAPE. `ccsession*`: ESCAPE. `claude`/`claude-code` (basename cut at `@`) [B-8] with any word in the whole command among `-p --print --continue --resume --bare --settings --dangerously-skip-permissions --fork-session --session-id --permission-mode`: ESCAPE. `tmux screen xdotool ydotool`: ESCAPE.

### 5.2 Other tools

- **Skill (FR-L-40):** name `skill`, else `name`; strip leading space, keep the first word, lower-case, drop one `/`, keep text after the last `:`, drop one leading `sc-` and one trailing `-protocol`. `implement`, `task`, `improve`, `cleanup`, `spawn`, `build`: IMPL (the last four by owner decision O-13, 2026-11-06; exact match after normalising, so `cleanup-audit` and `task-builder` stay NONE). `pr-submit`: SUBMIT. `issue`: ESCAPE. Empty: SKILL. Else NONE (`task-builder`).
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
| `jq` missing or input not JSON | independently proven governed: LL-BROKEN; recognizable launch-marker prompt: LL-NOBIND; otherwise identity-loss allow (§3), no enforcement claim |
| positively bound session file bad word, empty, unreadable, wrong file kind | `worktree` + LL-STATE on block |
| id missing or invalid, even with nonempty store | identity-loss allow (§3); stop deployment if observed on supported governed calls |
| Skill name unreadable / command over 64 KB | SKILL / BIG |
| `sed`, `tr` or internal error | LL-BROKEN |
| bind failure | LL-NOBIND |
| hook killed at timeout | call goes ahead (V8, R2) |
| session file deleted | ordinary (R3, O-16) |

Empty-store fast path: one directory test. With state present, one typed `jq` parse replaces the unsafe raw-id prefilter; ordinary sessions may therefore cost more than before and must be rebenchmarked. Timeout: 5 s, both entries (FR-L-58). Command cap: 65,536 bytes, governed only. L1 normalization uses one `sed` and four `tr`; one `sed` for an edit path; no git, network, Python or awk on ordinary L1 classification. Bind-time process-context probing, if B-CTX succeeds, is a separately measured L2 integration cost.

The command cap does **not** bound input-envelope size, initial stdin ingestion or jq work. Performance claims apply only to measured fixtures; add a large noncommand-field envelope stress case and report time/memory or a timeout as an explicit result. No arbitrary new wire-size limit is implied. The numbers below are **acceptance targets**, not observed results here; 'reported' means collect/report, not already measured. A failing asserted target cannot be waived silently.

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
| LL-IMPL | starting /sc:implement, /task, /sc:improve, /sc:cleanup, /sc:spawn or /sc:build (or their skills). | At the worktree level the agent stops at a plan until a person approves it. | Read the plan, then type /sc:implement or /task, or reply approved, in this session. |
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

- **LL-STATE** (positively bound level record invalid/unreadable): `Note: the launch record was invalid or unreadable, so the strictest level (worktree) applies.` Attach notes only to a block; an allowed call remains silent. Missing/invalid identity without positive binding is not LL-STATE authority (§3).
- **LL-TEXT** (class came from Bash or Monitor text): `Note: the guard does not tell quoted text from commands. Any command that names git together with the word commit, push, merge or pull, or gh together with the word api, counts as that action, even if the words are only in a message, a title, a PR body or a search pattern. If that is the case here, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>, or reword the search or title.`

## 10. Edge-case table

| Case | Decision | Rule |
|---|---|---|
| ordinary payload with a forged nested bound id | allow | P3, P6, T-ISO-6 |
| person's own session or subagent in the worktree | allow | FR-L-11, T-ISO-4 |
| id missing, store non-empty, no independent positive binding | allow, no enforcement claim; observed governed occurrence stops deployment | revised P6, panel F2 |
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

**Corpus.** Preserve MR section 8 (8.3/8.4) case inputs and historical outcomes as baseline provenance, but do not copy obsolete expected results unchanged (revised DD-2). Explicit overrides here: top-level typed JSON dispatch, identity-loss ordinary allowance instead of store-wide W, removal of the 64-id early allow, exact/no-replacement state publication, nonempty PR repo operands, and combined L2 protected-destination checks. Add panel F1–F8 regression cases and maintain a hand-written current oracle; report each intentional override rather than claiming MR was synchronized. Categories: push routes (T-ATK-1, 13, 25, 29, 50); aliases and variable subcommands (T-ATK-10, 35, 42); `gh api` writes (T-ATK-6, 18, 47); merges (T-ATK-48, 49, 51); tamper and escape (T-ATK-21, 55, 60); accepted leaks pinned `allow` (T-ATK-26 to 28, N-ATK-7, 31, 36); benign (T-OK-1 to 36); pinned over-blocks (T-OVR-1 to 6); amendment attacks (N-ATK-1 to 39). T-COR-2 replays the rows MR marks "real" on a temporary bare remote.

**Observed checks.**

- **OB-H1** (first; log-only hook). Records: (1) subagent and nested-subagent `session_id`, `agent_id`, `agent_type` (U1); (2) Skill keys, name form (U2); (3) Agent name, `isolation` (U3, U13); (4) typed `/sc:implement x` (O-4); (5) exact `prompt` of a Monitor line `approved` and of background-Bash and background-subagent notices (U4, O-17); (6) `TaskCreate` versus the anchored matcher (U15); (7) SendMessage, MCP names (U12); (8) `claude` without `-p` (U14); (9) Bash, Edit, Write, Skill names (U21).
- **OB-H2** (after the claim feature ships). Session file before the first tool call (U8); exact first prompt and marker position (U7); hook `HOME` and `CLAUDE_CONFIG_DIR`; IR-4 refusals; LL-NOBIND visibility (U20).
- **OB-H3** (test issue, each level, after all prior gates). `W` stops and unlocks by both routes; `F` logs git commands (U10); `FS` runs one authorized `/sc:pr-submit --monitor 3` cycle logging pushes and inline `gh api` (O-18, O-19) and a conflict (O-10). Protected-push/merge refusal tests use disposable repositories, never an actual protected branch on the fork. L2 observation follows §19.5. Count LL-PUSH-FORM, LL-GH-WRITE, LL-TEXT and NM1a/G2 UNKNOWN; separately count **am-only blocked first attempts and retries** before any O-21 reconsideration. Record Orca preamble (O-11), one live message (AC-7), timing, and exact harness/config versions. A skipped observation remains pending, not passed.
- **OB-CTX** is the first blocking feasibility check described in §19.1. Extend OB-H1/H2 capture to valid top-level event/id types on every supported governed leaf call. No probe or observation in this specification has been executed by this panel.

## 12. Acceptance criteria map

**Historical matrix only:** these verdicts belong to `plan-review-3.md` before this panel, not to the current refined design. Its reviewer tested an amended prototype; this panel reviewed/refined the design without rerunning executable behavior. No current AC has a runtime pass here. The earlier wording 'unreviewed' below records that historical review boundary.

| AC | Historical verdict | Earlier amendments (then unreviewed) | Historical remaining issues |
|---|---|---|---|
| AC-1 | NOT MET | B-1, B-2, B-3 close one-line commit, merge, push routes | built names (R1), R9, O-8 |
| AC-2 | NOT MET | B-3 redirect keys, B-4 `.config/git`, B-10 retry block | O-10, O-18, O-19, O-21 |
| AC-3 | NOT MET | B-1 makes `tm\`, `or\` spellings UNKNOWN | U4, O-17, R16 |
| AC-4 | MET WITH CAVEAT | none (U21 added) | OB-H1 item 1, else O-9 |
| AC-5 | NOT MET | B-1, B-2 close N-ATK-29, 30, 32, 33; B-9 reinstall | R3, O-16, N-ATK-31 |
| AC-6 | NOT MET | B-1 to B-4, B-7; copy blocked 35 of 38 | R1, R11; O-22 |
| AC-7 | MET | B-1, B-7 wording | none |
| AC-8 | MET WITH CAVEAT | amendment corpus added | only corpus routes shown; speed untimed |

**Current acceptance additions (all pending execution):** AC-4 requires concurrent governed/ordinary actors in the same worktree, including a human terminal, with no marker-removal workaround. AC-5 requires no-replacement binding, exact state reads and ordinary isolation under identity loss, with that fail-open limit stated. AC-6 requires actual field-3 L2 checks only after B-CTX; scripts/aliases using ordinary Git push are covered only if actor selection demonstrably follows them. AC-8 adds F1–F8 boundary regressions and all §19.5 lifecycle/fixture checks. Acceptance is limited to tested routes; local hooks do not establish universal no-merge/no-main-write protection. B-CTX blocks declaring the complete feature ready, independently of any old MET label.

## 13. Registration, install and claim-feature interface requests

Append to `UserPromptSubmit` and to `PreToolUse` in `src/superclaude/hooks/hooks.json`; existing entries, such as Bash `block-bare-python.sh`, stay.

```json
{ "hooks": [ { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 } ] }
{ "matcher": "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)",
  "hooks": [ { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 } ] }
```

No UserPromptExpansion, SessionStart or `onFailure` (FR-L-63). Anchors are U15; the script re-checks names (FR-L-66). Add `"launch-level-guard.sh"` to `_FRESHNESS_SCRIPTS` (not the Makefile). For later implementation, run `make sync-dev` and `make verify-sync`; stage canonical source/tests and all `.dev/tasks/` packages, never generated `.claude/` mirrors. This panel does not run sync or change executable files.

- **IR-1** Before `orca agent launch`, write `pending/<nonce>` (one word) atomically; nothing for `--pipeline none`.
- **IR-2** Nonce `secrets.token_hex(16)`; prompt starts `[sc-launch:v1:<nonce>] `.
- **IR-3** `pipeline.json` is documentation only; amend FR-31.
- **IR-4** Refuse a governed launch unless jq exists, the expected installed script/version is executable, and the effective configuration actually enables both registrations (not merely matching text in an ignored/disabled settings file). This increment supports `$HOME/.claude` for hook commands and state. An effective `CLAUDE_CONFIG_DIR` resolving elsewhere is unsupported and must refuse the governed launch, not inspect one directory while executing another. Do not edit global configuration to force compliance. OB-H2 must observe actual hook execution and bind-before-first-tool order.
- **IR-5** Re-claim: new session, new nonce, never `--resume`.
- **IR-6** Claim output says how to release a session and states active L1/L2 status. Release invalidates both layers' session membership; it does not require a person to remove a worktree marker to push ordinarily.
- **IR-7** Claim integration must verify owned/effective L2 installation and the proven B-CTX context contract before a governed pipeline starts. Conflict/absence preserves foreign hooks, reports W-L2-ABSENT and refuses that governed launch. No-pipeline claims stay unaffected. This is a requested interface, not existing claim capability.

## 14. Order of work

0. **B-CTX / OB-CTX feasibility gate (§19.1).** Validate the process-context candidate and same-worktree concurrent human isolation with a log-only bounded probe. If it cannot distinguish required lifecycle cases, stop the enforcement implementation and report the exact missing launcher/harness integration. Do not weaken isolation, add infrastructure or start another review loop. This is the first required task in downstream workflow planning.
1. **OB-H1.** Validate U1, typed top-level identity/event fields and turn wrapping. Gate: item 1 fails, stop (O-9); item 5 bare, apply O-17 alternative. Identity loss on a supported governed call stops deployment.
2. Skeleton (dispatch, store, binding, resolution, trap, printer). Proves harmless: T-ISO-1, 5, 6, T-FC-*, T-BIND-*.
3. Normalisation and classifiers: T-NRM, T-GIT, T-PSH, T-GH, T-MCP, T-SKL, T-ESC, T-TRN, T-TAM, T-COR.
4. Policy and messages: T-GRID, T-MSG.
5. Approval: T-APR.
6. Registration: T-REG, T-SPD.
7. Hand IR-1 to IR-7 to the claim feature. Build L2 only after B-CTX passes, using §19 rather than superseded MR 11.3 alternatives. Preserve foreign hooks and implement the isolated temporary-remote suite before any real launch.
8. **OB-H2**, then **OB-H3**. Gate: no real governed launch until both pass.

## 15. Open decisions

### 15.1 Owner decisions O-1 to O-22 (default is in force)

Decided by the owner on 2026-11-06: **O-22 yes**, **O-21 retain the default**, and **O-13 yes**. O-22 keeps the structural git-level guard alongside text checks. Human pushes from the same worktree must remain unrestricted by the launch-level guard; worktree membership alone must not activate it. A trustworthy way to distinguish governed pushes from human pushes remains a design prerequisite, not an implemented capability. O-21 keeps `am` in the broad scan and records `am`-only interruptions during OB-H3 before considering its removal. See the advisory debate at `.dev/brainstorms/20261105-170229-launch-level-hook/o21-o22-debate.md`. Every other decision keeps its default.

| Id | Question | Default | Alternative |
|---|---|---|---|
| O-22 | add a structural git-level layer (L2, `pre-push` refusing governed updates to `main`, `master`)? | **DECIDED yes (owner, 2026-11-06)**: step 7a, text layer kept; human pushes in the same worktree remain unrestricted. Before building: trustworthy governed-push selection, install place (U28), hook chaining, removal, tests. Local hooks do not guarantee AC-6. | text classifier only (R1), not selected |
| O-21 | quoted-text over-match | **DECIDED retain default (owner, 2026-11-06)**: accept; LL-TEXT; retain global `am`; OB-H3 counts `am`-only blocks and retries separately | drop only global `am` after measurement and a new owner decision; keep command-position `git am` gated |
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
| O-13 | more IMPL skills | **DECIDED yes (owner, 2026-11-06)**: `sc:improve`, `sc:cleanup`, `sc:spawn`, `sc:build` join the IMPL set; approval unlocks them like `/sc:implement` | no (the earlier default) |
| O-14 | MCP writes at `FS` | blocked | allow non-`main` |
| O-15 | old state files | person removes | prune on re-claim |
| O-16 | deleted file is ordinary | accept | read `transcript_path` (U27) |
| O-17 | self-started turns | allowed | block at `W` |
| O-18 | compound push at `FS` | blocked | widen form |
| O-19 | non-canonical `gh api` | blocked | admit GET variants |
| O-20 | strict marker, no record | block prompt | ignore |

### 15.2 Blocking findings of the three plan reviews

Historical status copied from MR 11.2, which names the confirming review. 'OPEN (amended, not re-reviewed)' means open at that earlier review boundary, not that the 2026-11-06 panel did not read it. This panel is one simulated design review, not an independent runtime confirmation; no historical experiment is rerun or relabelled closed. Current requirements and blockers are in §3, §12 and §19.

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
| DD-2 | preserve MR inputs as historical baseline; current hand-written expectations follow this design's explicit overrides (§11) | no false synchronization claim |
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

Historical corpus, debate record and reviews: `.dev/brainstorms/20261105-170229-launch-level-hook/` (`merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review*.md`, `refactor-plan.md`). These files have not been synchronized to this refinement.

## 19. L2 structural pre-push layer: conditional integration contract

### 19.1 Actor selection and blocking prerequisite B-CTX

**Invariant:** an ordinary human push in the same worktree is never restricted by launch policy. Git's documented pre-push inputs are remote name/location and ref-update records; Git does not supply a Claude session id. A worktree marker is only an installation/eligibility hint. An inherited environment value, `CCSESSION_LAUNCH_ID`, `CLAUDECODE`, pane key, branch or path is never sufficient authority to select a governed push.

**Historical controller-process candidate, not the implemented identity contract:** the panel proposed associating a bound session with its Claude ancestor and inspecting ancestry at pre-push. The subsequent scoped integration instead binds each accepted Bash job independently (§19.7); do not implement the controller-only design below as if it solved session resets. The historical candidate remains here to explain the original feasibility blocker.

Historical candidate steps, not adopted as an implementation contract:

1. On successful main-session binding, identify the actual firing Claude ancestor from the hook process tree on Linux. Record `(session_id, pid, process-start identity)` outside the worktree in the launch store. Include kernel boot identity or an equivalent lifetime discriminator so a PID reused after exit/reboot cannot authorize a push. Record only after matching the real supported executable/wrapper topology observed by OB-CTX; do not assume the nearest non-shell process is Claude. Environment values may aid diagnosis but cannot supply authority.
2. Pre-push walks a **bounded** actual parent chain. Select governed only when an ancestor's PID and start identity match a live registered process and the associated session's level record still exists. A human terminal sharing an Orca ancestor is not a descendant of Claude and is not selected. Script/alias/subprocess pushes under the registered Claude ancestor are selected regardless of command spelling. No global environment toggle is consulted.
3. Release invalidates the membership when the session record is removed. Dead/reused PID records are inert; no destructive pruning needed. Resuming in a new Claude process must re-establish membership from the existing bound session, not trust an inherited label. A new ordinary session in the same process must not inherit the old session's restriction.
4. Unknown/unreadable ancestry cannot be called 'trusted human' and cannot justify blocking a human on the basis of the worktree marker. This is an unsupported coverage case until the gate below is resolved. If safe distinction is unavailable, stop deployment; do not substitute a marker-wide block or silently advertise enforcement.

**OB-CTX / B-CTX completion evidence (not observed here):** a log-only probe must capture the actual main/subagent/nested/background Bash/Monitor-to-Git and hook process trees, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, launch wrapper, process exit/PID reuse, resume in a new process, /clear/fork, and release while a job remains alive. Establish the needed ancestry bound from that evidence, with an explicit exhaustion rule. In particular, prove how an ordinary new session in a reused Claude process and an old governed background child can be distinguished at the same time. Kernel ancestry alone may not supply that distinction. No single PID-label lookup is accepted as a solution to it.

**Current full-enforcement verdict:** B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. The claim code now launches governed pipelines and refuses one when the L1 guard is not effective (§19.8); the L2 layer this section selects for is not built. Keep production activation conditional on the actual supported execution surfaces and their required observations, without a root service or weakening human isolation. O-22/O-21/O-13 are not reopened.

### 19.2 Placement and coexistence (Q1/Q2, narrowed)

The current run-4 merged artifacts prefer one owned shared `hooks/pre-push` plus a private-worktree marker, no config change, and no push-hook forwarding. Adopt this as the **conditional placement**, not the actor selector. Resolve common/private Git paths using Git, never assume `.git` is a directory. Existing `pre-commit`, `commit-msg` and other hook names remain untouched.

Install only if effective hooks lookup is the supported default, there is no foreign pre-push, and publication/self-test succeeds. Publish a complete executable without replacing an existing file, including a concurrent foreign install; recheck exact owned version/content before reuse. A header alone is not sufficient ownership proof. Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow foreign hooks, generate name-only stubs, or buffer/replay someone else's push hook in this increment.

Conflict or unsupported lookup: preserve all existing files/configuration; report `W-L2-ABSENT` with the reason. Unlike Q1/Q2's advisory 'continue claim', **do not launch a governed pipeline advertised as protected** when accepted L2 is absent. An ordinary/no-pipeline claim is unaffected. This preserves safety without silently treating a warning as O-22 compliance. A later request for coexistence beyond this boundary requires its own scoped design, not an automatic review loop.

### 19.3 Update stream and limits

After positive actor selection, read every record as `<local-ref> <local-oid> <remote-ref> <remote-oid>`. Refuse the **entire push**, with a plain diagnostic and nonzero status, if field 3 is exactly `refs/heads/main` or `refs/heads/master`, including create/update/delete and force forms. Zero OIDs and `(delete)` are ordinary Git control values, not exemptions. Empty stream allows. A malformed governed stream (missing/extra fields) refuses with a distinct malformed-input diagnostic. Stream until EOF; do not truncate after a fixed ref count or infer ref count from the user's original command. No hardcoded SHA-1 length is necessary for destination selection. Unselected ordinary pushes are allowed without launch-policy output or stream inspection.

`refs/tags/main`, `refs/heads/mainline`, `refs/heads/ma` and `refs/heads/feature/main` are not protected by this rule. A source-only refspec configured to resolve to protected heads is protected because field 3 is authoritative. L2 adds no local commit/merge restriction and does not know the correct remote repository. `--no-verify`, per-process hooksPath overrides, direct send-pack and API/programmatic ref writes can bypass local pre-push; visible forms remain checked by L1. Same-user modification and deliberate detachment remain limitations unless the observation gate establishes the specified coverage. Neither layer guarantees universal AC-6 or a hostile-agent sandbox.

### 19.4 Release and removal (Q3, narrowed)

Private-worktree eligibility data may disappear with Git worktree removal; Q artifacts report that Git behavior in disposable repositories. Actual Orca removal remains unverified. The shared hook file may remain installed and inert for launch policy; do not claim **all** L2 files disappear with one worktree.

Deleting a session's level/approval files is still the person's release route and must invalidate that session's L2 process membership. Retaining a worktree marker after release must not retain a restriction on human pushes. No marker-lift command is required for ordinary humans and no config-unset command is introduced. Re-add/rename, stale records and concurrent sessions must be in the lifecycle tests; renames must not switch the bound session's identity. No whole shared-hook deletion during a single-session release.

### 19.5 Tests and observed checks (Q4, constrained to safe target)

Use production installation and real Git in a pytest temporary bare remote, clone and linked worktrees. Assert hook evidence **and before/after remote refs**, not merely exit status. Cover create, update, delete, forced update, plus refspec, mapped source-only refspec, mixed protected/unprotected updates (protected last), empty stream, SHA-format-independent destination handling, exact-name edges and known bypasses. Synthetic direct-hook inputs are only for malformed/padded records Git does not normally send. Seed existing protected refs where deletion/update requires them.

Actor cases: agent and human concurrent in the **same** eligible worktree; ordinary Claude session there; main checkout; sibling; nested subagent; release/resume/clear; stale or reused process id; unreadable ancestry and bound exhaustion. Mark expected text-layer leaks separately from combined L1+L2 results: historical allow pins for hidden ordinary Git pushes do not mean L2 should also allow a governed protected destination.

OB-H3 L2 observation uses a real claim's installation and a **disposable local bare destination**, never a real origin protected branch or a scratch push to the fork. Check effective hook presence/executable ownership and process membership. Use fixture refs that actually reach pre-push (not up-to-date/nonfastforward rejection), and require the hook's own diagnostic. A dry-run can supplement the fixture test, not replace ref-state assertions. Official Git documents dry-run as not sending updates; Q artifacts report local hook invocation, not this panel's runtime verification. No transport-specific proof for the real fork is claimed.

### 19.6 Provenance and evidence limits

Read-only source fallback: Auggie unavailable; codegraph/native tools used. Current advisory outputs and their sibling `adversarial/return-contract.yaml` files:

- `.dev/brainstorms/20261106-l2-prepush-decisions/q1-install-place/run-4/merged-answer.md`: partial, marker-only isolation insufficient.
- `.dev/brainstorms/20261106-l2-prepush-decisions/q2-chaining/run-4/merged-q2-answer.md`: partial; use shared-path branch only, no forwarding/stubs.
- `.dev/brainstorms/20261106-l2-prepush-decisions/q3-removal/run-4/merged-answer.md`: partial; worktree cleanup useful, retained human restriction rejected.
- `.dev/brainstorms/20261106-l2-prepush-decisions/q4-testing/run-4/answer-merged.md`: success label with unresolved items; choose local fixture target to avoid real-remote ambiguity.

Their measurements remain their authors' historical observations. This panel did not rerun them. Official interface references: [Git hooks](https://git-scm.com/docs/githooks), [Git push](https://git-scm.com/docs/git-push), [Git core config](https://raw.githubusercontent.com/git/git/master/Documentation/config/core.adoc), [Claude Code hooks](https://code.claude.com/docs/en/hooks). These establish protocol semantics, not runtime proof of B-CTX.

### 19.7 Implemented scoped job identity foundation

The owner's subsequent authorization covers the missing launcher/harness identity integration, not the complete enforcement feature. The implementation is `src/superclaude/hooks/scripts/launch-job-identity.sh`, with a byte-identical plugin mirror and executable installer distribution. Its stdlib Python body runs through UV on Linux; this is a narrowly authorized exception to this component's earlier bash-only design. No new dependency package or service is added. Tests live in `tests/hooks/test_launch_job_identity.py`; installer coverage is in `tests/cli/test_install_hooks.py`.

**Execution binding:** the Bash PreToolUse adapter reads the actual event's top-level `session_id`. Only a positively governed private `sessions/<id>` record with an exact supported level triggers adaptation. It copies the entire `tool_input`, changes only `command`, and returns `updatedInput` without `permissionDecision: allow`. Timeout, background flag, description and other input fields are retained. Ordinary and non-Bash events are unchanged. No long-lived Claude PID, worktree marker or inherited environment label supplies actor authority.

**Permission boundary:** PreToolUse creates no launch ticket. It emits a shell-quoted invocation of `execute SESSION TOOL_ID_OR_EMPTY COMMAND`. Only when normal permission evaluation allows that invocation to start does `execute` create and immediately consume its private single-use request through the runner. A denied or canceled-before-start rewrite creates no request to replay. The standalone launcher interfaces `prepare SESSION COMMAND [TOOL_USE_ID]` and `run TOKEN` remain explicit caller APIs, not proof that a person approved a command.

**Job lifetime:** each supervisor owns a separate Linux process session, records its actual kernel session/PID/start ticks/boot identity and immutable originating logical session, and waits for the main shell plus ordinary live descendants in that kernel session. The subreaper retains/reaps ordinary orphan descendants after an intermediate shell exits. The main shell's stdout, stderr, stdin, environment, initial cwd and exit status are preserved. A new ordinary tool event from the same controller is not assigned to the old job. The supervisor remains live while ordinary background descendants remain; command completion therefore waits for them deliberately.

**Selector contract:** `identify [PID]` inspects actual kernel process-session membership and validates a live supervisor's PID/start/boot identity plus the origin's current governed record. It emits `governed` with the original session ID, `ordinary` for no registered job or explicit release, and `unknown` for malformed/stale/unreadable registered identity. `unknown` is not a trusted-human verdict. Deleting the origin's level record releases its live jobs without changing another session. Starting a new logical session does not relabel an old job. State location is the configured HOME's launch-level store; callers must preserve that execution context. Arbitrary state relocation or hostile same-user modification is not an isolation guarantee.

**Known execution changes:** wrapped commands run in a fresh Bash shell. An internal `cd` does not persist to later Bash tool calls; use an explicit working directory in each governed call. This adapter is not a transparent replacement for every interactive Bash workflow. Deliberate `setsid`/daemonization escapes kernel-session selection; supervisor killing leaves stale/unknown state for surviving registered jobs. Monitor, other shell tools, remote jobs and unmatched execution mechanisms are not silently supported. No universal hostile-agent protection is claimed.

**Runtime preflight:** UV, the supported Linux process/pidfd/subreaper interfaces, Bash and valid private state must exist for governed execution. With UV absent, jq may establish an exact positively bound session and block it plainly; ordinary unbound calls remain silent. If neither runtime nor parser can establish binding, adaptation is unavailable with no rewrite, not proven human identity or active protection. The future governed launcher must check these prerequisites instead of advertising protection on a host that cannot adapt its jobs.

**Observed versus simulated:** isolated actual CLI PreToolUse/PostToolUse records show one governed call rewritten without a permission-approval decision and reporting the same origin UUID from the executed selector; its ordinary counterpart is not rewritten and reports ordinary. Both actual CLI runs exited 0. The managed identity package `TASK-WF-authorizedNarrow-20261106-214325` retains the redacted `artifacts/live-harness-events.jsonl`. Controlled subprocess tests exercise old-background/new-ordinary overlap, release, stale process data, quoting, startup failure and signal behavior; they are not observations of real `/clear` or resume. Actual persistent-cwd tracking, background scheduling, `/clear`, resume, Monitor, auto mode, concurrent-hook composition and nested-subagent payload variants remain unobserved unless later evidence explicitly adds them.

**Next integration:** a future claim launcher must create the private governed level record for the actual logical session, validate effective adapter/runtime availability and install the separately designed production pre-push policy. That policy may use this selector only on the tested local Bash surface; it must retain an explicit unsupported path for unknown or unadapted execution. This increment does not implement the claim pipeline, the full text classifier, automatic session binding from a claim marker or the production pre-push install/release policy. The earlier blocked workflow remains historical and immutable, not retroactively compliant. §19.8 records what the later issue #394 implementation added.

### 19.8 Implementation status (issue #394)

**Built:**

- The L1 guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (bash, `jq`, `sed`, `tr`; exit 0 allows, exit 2 blocks), with a byte-identical plugin copy.
- Its two registrations, on `UserPromptSubmit` and on `PreToolUse` with the §13 matcher, in `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json`.
- The installer entry `"launch-level-guard.sh"` in `_FRESHNESS_SCRIPTS` of `src/superclaude/cli/install_hooks.py`.
- Claim-side detection in `orca_worktree.py`: IR-1 and IR-2 (pending launch record and prompt mark), IR-4 (a read-only preflight that refuses the governed launch with `W-ENFORCEMENT-ABSENT` when `jq`, `uv`, the commands the guard calls (`cat`, `sed`, `tr`, `mkdir`, `mv`, `ln`, `rm`), the installed guard, its effective registrations or the job identity registration is missing or not effective, as seen from the claim process only (its HOME, PATH, environment and the user and worktree settings files; enterprise-managed settings and what Claude Code really runs are not seen); no agent starts and no record is written), IR-5 (new session and nonce per claim), IR-6 (release instruction and L1/L2 status lines) and IR-7 as the warning `W-L2-ABSENT` (the launch continues; the owner had not answered whether it should refuse). IR-3 stays documentation only: no code writes `pipeline.json`.

**Pending, none run:** OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX, and the L2 pre-push layer of §19.2 to §19.5, which needs its own plan after B-CTX. No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed. §7 U1 requires item 1 before a `full` or `--submit` claim and OB-H1 item 5 (self-started turns wrapped) before a claim at any level; OB-H2 and OB-H3 are defined in §11 and gated in §14.

Pending launch records are not pruned: a person removes old state files (owner decision O-15).
