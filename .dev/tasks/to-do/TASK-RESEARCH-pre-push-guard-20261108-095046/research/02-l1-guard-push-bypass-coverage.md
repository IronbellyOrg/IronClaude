# Research: L1 guard coverage of push spellings and bypasses
**Investigation type:** Code Tracer
**Scope:** src/superclaude/hooks/scripts/launch-level-guard.sh
**Status:** Complete
**Date:** 2026-11-08
---

Method: static reading only. The guard was not run and no candidate command was executed. Every verdict below comes from the regexes and branches quoted verbatim with their file:line in `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines, read in slices 1-300, 300-469 and 470-747).

## 1. How a refusal is produced (messages, `ll_say`, `ll_deny`)

- `ll_say` (lines 36-133) maps a message id to three strings: `b` (Blocked), `w` (Why), `y` (You can). It prints a level header (lines 115-125), then `printf '%s\n' "Blocked: $b" "Why: $w" "You can: $y" >&2` (line 126), plus optional notes: the invalid-record note (lines 127-129) and the quoted-text note (lines 130-132, when `LL_NOTE_TEXT=1`).
- `ll_deny` (lines 135-139) sets `LL_DENIED=1`, calls `ll_say "$1"`, then `exit 2`. The header comment says "Exit 0 allows; exit 2 blocks with a message on stderr; never exit 1" (lines 4-5) [CODE-VERIFIED lines 135-139, 147-163].
- The EXIT trap `ll_on_exit` (lines 147-163) turns any other non-zero exit into `LL-BROKEN` (tool branch) or `LL-NOBIND` (prompt branch) with exit 2, but only when `LL_GOVERNED=1`; an ungoverned session exits 0 on internal failure (lines 153-155).
- **Line 59** is the `b=` string of `LL-PROTECTED`: `b='a push to master or main.'`, with `w='No launch level may change the main branch.'` (line 60) and `y='Push the feature branch by name, then merge it through a reviewed pull request.'` (line 61). It is printed only when `ll_deny LL-PROTECTED` runs (section 5 gives the branch that calls it).
- Push-related message ids:
  - `LL-PUSH` (lines 50-53): "a git push." Only `full --submit` may push.
  - `LL-PUSH-FORM` (lines 54-57): "a push that is not one plain git push command, or a command that names git and push together." Its Why text (line 56) states the allowed shape: `git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it`. That claim is checked against the classifier in section 5.
  - `LL-PROTECTED` (lines 58-61).
  - `LL-UNKNOWN` (lines 78-81): unknown git/gh subcommand, alias definition, variable-built subcommand, or a backslash-newline inside a word.
  - `LL-GH-WRITE` (lines 66-69): non-plain `gh api`, or "a direct call to the GitHub API".
  - `LL-TAMPER` (lines 94-97): "touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks." The message names "a git configuration file" but not git hook files; section 6 checks what the code covers.

### Governance gate (who is checked at all)

- Fast exit when there is no store and no launch marker: lines 168-173 (`[ ! -d "$LL_STORE/sessions" ]` then `exit 0` unless the input contains `[sc-launch:`).
- A session is governed only when its `session_id` has a record file: lines 257-273. The level comes from the file text (`worktree`, `full`, `full-submit`); anything else is worktree with a note (line 268).
- Tool branch: `[ "$LL_GOVERNED" = 1 ] || exit 0` (line 394). So **every verdict in this file applies only to a governed session** (one started by `/sc:issue --claim`). An ordinary session is never checked [CODE-VERIFIED line 394; header comment lines 6-7].
- Only `Bash` and `Monitor` tool calls are command-classified (line 417); the command comes from `tool_input.command` via jq (line 195).

**Key Takeaways**
- A refusal is `ll_deny <ID>` -> stderr text -> `exit 2`. Line 59 is a message string, not a check.
- L1 governs only claimed sessions, and inspects only Bash/Monitor command text, Skill names, Edit/Write paths, Agent/Task isolation and tool names.

## 2. Tokenization of the command line (normalise block, lines 421-438)

The guard does not parse shell. It builds three derived strings from the raw command `cmd=$LL_TEXT` (line 421):

| Name | Line | Exact construction (verbatim) | Effect |
|---|---|---|---|
| size cap | 422-423 | `if [ "${#cmd}" -gt 65536 ]; then` / `LL_CLASSES+='BIG '` | Over 64 KB: only class BIG, nothing else is checked. |
| NM1a | 428-429 | `LL_RE_NM1A=$'[^[:space:]\\\\]\\\\\n'` ; `[[ $cmd =~ $LL_RE_NM1A ]] && LL_CLASSES+='UNKNOWN '` | A backslash-newline right after a non-space character (continuation inside a word) adds UNKNOWN. |
| T | 431 | ``T=$(printf '%s\n' "$cmd" \| sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g')`` | `$'` / `$"` lose the `$`; every `'`, `"` and `\` is deleted (quoting is erased: `'gi't` -> `git`, `"push"` -> `push`); `/` runs squeezed; `/./` collapsed; each backtick becomes ` $;`. |
| G | 433 | `G=" $(printf '%s\n%s\n' "$cmd" "$T" \| tr 'A-Z' 'a-z' \| tr -c 'a-z0-9._/~$@+:-' ' ') "` | Raw cmd and T, lower-cased, every char outside `a-z0-9._/~$@+:-` made a space, one space at each end. Used for whole-command word tests. `=` is NOT in G's set, so `core.hooksPath=/dev/null` becomes `core.hookspath` and `/dev/null`. |
| W | 435 | `W=$(printf '%s\n' "$T" \| tr '\n;&\|()' ';;;;;;' \| tr -c 'A-Za-z0-9._/=:@+~$;-' ' ')` | Newline, `;`, `&`, `\|`, `(`, `)` become `;` (segment separators); chars outside `A-Za-z0-9._/=:@+~$;-` become spaces; case kept; `=` kept. `_` is NOT in the set (comment lines 440-441: "W has no `_`"), so `GIT_DIR=/x` becomes the two words `GIT` and `DIR=/x`. |
| segs | 437 | `IFS=';' read -r -a segs <<<"$W"` | Segments split on `;`. Words are `ws=($seg)` (line 446) under `set -f` (line 15, no globbing). |
| basename | 436 comment, 450 | `b=${w##*/}` | `/usr/lib/git-core/git` -> `git`. |

Consequences for push spellings:
- **Quoting** is erased in T and W before matching (line 431), so `g'i't push`, `"git" "push"` and `\git push` all reach the classifier as `git push`.
- **Compound commands** (`;`, `&&`, `||`, `|`, subshell parens, newlines) become separate segments in W (line 435), but G (line 433) sees the whole command at once.
- **Env prefixes** are not stripped by the normaliser; they stay as words in the segment (section 4 shows how the git classifier treats them).
- The comment at lines 418-420 says "No ${s//...} substitution runs over the text (fact T5); one sed and four tr." [CODE-VERIFIED lines 431, 433, 435: one `sed`, four `tr`].

**Key Takeaways**
- Matching is on text after quote/backslash deletion, so quoting tricks do not hide `git` or `push` words.
- Segment checks (W) and whole-command checks (G) differ: a check on G cannot be dodged by splitting across `;` or `|`.

## 3. Whole-command git/gh detection on G (lines 483-534)

All regexes run on G (lower-cased, see section 2) unless stated.

| Purpose | Line | Regex / test (verbatim) | Class |
|---|---|---|---|
| A git word anywhere | 486-488 | `LL_RE='( \|/)git(-[a-z][a-z-]*)? '` ; `[[ $G =~ $LL_RE ]] && LL_GIT=1` | sets `LL_GIT=1` (gate for lines 525-534) |
| A gh word anywhere | 489-491 | `LL_RE='( \|/)gh '` | sets `LL_GH=1` |
| URL hint | 494 | `case $G in *repos/* \| *api.github.com* \| *uploads.github.com*) LL_URL=1 ;; esac` | sets `LL_URL=1` (gate for H5) |
| H2 gh api | 495-524 | gate `[ "$LL_GH" = 1 ] && [[ $G == *' api '* ]]`; plain-GET form on raw cmd `LL_RE='^[[:space:]]*gh api( +[A-Za-z0-9._/:=,@%+-]+)+[[:space:]]*$'`; write-word test `LL_RE_W='^(-[A-Za-z]*[XfF].*\|--method.*\|--field.*\|--raw-field.*\|--input.*)$'`; endpoint `case ${LL_EP,,} in '' \| graphql \| */merge \| */merges) LL_OK=0` | `GHWRITE` unless one plain GET |
| merge/pull | 526-527 | `LL_RE='( \|/git-\| git-)(merge\|pull) '` | `MERGE` |
| **push** | 528-529 | `LL_RE='( \|/git-\| git-)(push\|send-pack\|http-push) '` | `PUSH` |
| commit | 530-531 | `LL_RE='( \|/git-\| git-)(commit\|cherry-pick\|am\|commit-tree) '` | `COMMIT` |
| **config-rewrite tokens** | 532-533 | `LL_RE='alias\.\|pushurl\|insteadof\|hookspath\| (remote\|url\|include\|includeif)\.\| set-url '` | `UNKNOWN` |

Notes from the code:
- The push regex's first alternative is a bare space, so ` push `, ` send-pack ` or ` http-push ` as a whole word **anywhere** in the command (including inside a commit message or a search pattern) gives `PUSH` when a git word is also present. The LL-PUSH-FORM message (line 55) and the LL-TEXT note (line 131) say exactly this [CODE-VERIFIED lines 528-529, 716-718].
- A word is "push" only when a space precedes it in G. `.push` (Python method call), `pre-push`, `--push-option`, `x70ush` (ANSI-C escaped) do not match.
- The `hookspath`, `alias.`, `pushurl`, `insteadof` tokens are substrings, matched anywhere in G, but only when `LL_GIT=1` (line 525). A command that touches git config text without a git word (section 6) is not checked by line 532.
- `LL_GIT` needs `git` preceded by a space or `/` and followed by a space or `-[a-z]...` then a space. `.git/config` and `.git/hooks/pre-push` do not set it (the char before `git` is `.`); `https://github.com/o/r.git/git-receive-pack ` does (`/git-receive-pack `).

**Key Takeaways**
- Push detection is lexical: the words `push`, `send-pack`, `http-push` plus any git word. It is broad (false positives on text) but blind to spellings that avoid those words.
- Config-rewrite detection (line 532) covers `core.hooksPath`, aliases, `pushurl`, `insteadOf`, `remote.*`, `url.*`, `include*` and `set-url`, but only in a command that also has a git word.

## 4. Per-segment git/gh word classifier (lines 535-657)

Runs when `"$LL_GIT$LL_GH$LL_URL" != 000` (line 535), once per segment of W.

**Command position (CP) and env-prefix handling, lines 541-558.** For each segment, words are skipped until the command-position word:
- options `-*` skipped (line 546);
- wrappers by basename (line 549, verbatim): `env | sudo | nohup | exec | command | builtin | timeout | xargs | setsid | time | nice | stdbuf | ionice | doas | unbuffer | eval | if | then | else | elif | do | while | until | coproc) continue ;;`
- `bash | sh | zsh | dash | ksh` followed by a `-c`-style flag (`^-[a-z]*c$`, line 551) skip both words;
- assignments and numbers: `LL_RE_NAME='^[A-Za-z_][A-Za-z0-9_]*='` (line 536) and `LL_RE_NUM='^[0-9]+(\.[0-9]+)?[smhd]?$'` (line 537), tested at line 556;
- the first word that is none of these becomes `LL_CP` (line 557).

**Defect found (static): underscore env names.** W is built with `tr -c 'A-Za-z0-9._/=:@+~$;-' ' '` (line 435), which has no `_` (the comment at lines 440-441 confirms "W has no `_`"). So `GIT_DIR=/x git ...` reaches the CP loop as the words `GIT`, `DIR=/x`, `git`. `GIT` does not match `LL_RE_NAME` (no `=`), so `LL_CP` is set to `GIT` (index 0), and the real `git` word is **not** in command position. `LL_RE_NAME` allows `_` but never sees one. Any assignment whose name contains `_` (for example `GIT_DIR=`, `GIT_CONFIG_COUNT=`, `A_B=1`) therefore moves CP off the git word. The same happens for any wrapper not in the line 549 list (`chrt`, `taskset`, `flock`, `strace`, `find ... -exec`, `uv run`, and so on).

**git word resolution, lines 611-636.**
- `case $b in git) ;; git-*) [[ $b =~ $LL_RE_DASH ]] || continue ;; *) continue ;; esac` (line 611) with `LL_RE_DASH='^git-[a-z][a-z-]*$'` (line 538). So `git`, `/usr/bin/git`, `git-push`, `/usr/lib/git-core/git-push` all resolve (basename at line 567).
- Dashed form: subcommand `LL_S=${b#git-}` (line 615).
- Plain form: options that take a value are skipped with their value (line 620, verbatim): `-C | -c | --git-dir | --work-tree | --namespace | --config-env | --attr-source)`; other `-*` skipped (line 628); the first other word is the subcommand (line 629). A value option at the end of the segment sets `LL_DG=1` (lines 621-623).
- G4, every git word, any position (lines 634-636): `if [ "$LL_DG" = 1 ] || [[ $LL_S == *'$'* ]]; then LL_CLASSES+='UNKNOWN '`. So a subcommand built from `$var`, `${var}` or `$(...)` is UNKNOWN even off command position.
- `[ "$LL_CP" = "$i" ] || continue` (line 637): **the subcommand table (G3) runs only for the git word in command position.**
- G3 table (lines 640-654): `push) LL_CLASSES+='PUSH '` (line 648); `remote) case $LL_NX in '' | -v | --verbose | get-url | show) ;; *) LL_CLASSES+='UNKNOWN '` (line 650); `config) case $LL_NX in --get | --get-all | --get-regexp | --list | -l | get | list) ;; *) LL_CLASSES+='UNKNOWN '` (line 651); read-only and local subcommands allowed (line 649, includes `fetch`, `rebase`, `reset`, `branch`, `tag`); `update-ref` with `HEAD`, `--stdin` or `refs/heads/*` is COMMIT (lines 643-646); everything else, including `send-pack`, `http-push`, `remote-https`, `bundle`, `pack-objects` and alias names, is `*) LL_CLASSES+='UNKNOWN '` (line 653).

**gh word resolution (H1, H3, H4), lines 568-610.** Group and action are the first two non-option words after `gh`, skipping `-R`/`--repo` values (lines 571-584). `'api '*) ;;` (line 589) defers to H2. Unrecognised group/action is UNKNOWN only in command position (line 596: `*) [ "$LL_CP" != "$i" ] || LL_CLASSES+='UNKNOWN '`).

**H5, lines 559-566, 656.** In segments with no gh word, any word with `repos/` ending `/merge(s)` is MERGE, and any word containing `api.github.com` or `uploads.github.com` is GHWRITE (`case $LL_LW in *api.github.com* | *uploads.github.com*) LL_H5+='GHWRITE '`, line 565).

**Key Takeaways**
- G3 (unknown subcommand, alias call, remote-helper call) is command-position-only, and an underscore env prefix or an unlisted wrapper moves command position off `git`. This is the main L1 hole for push spellings that avoid the literal word `push`.
- G4 (`$` in the subcommand) and the G-level regexes (section 3) do not depend on command position, so they still fire behind such prefixes.

## 5. Canonical push check and the PROTECTED refusal (lines 658-669, 720-742)

Verbatim (lines 659-669):

```bash
case $LL_CLASSES in
*' PUSH '*)
    LL_RE='^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$'
    if [[ $cmd =~ $LL_RE ]]; then
        LL_D=${BASH_REMATCH[5]:-${BASH_REMATCH[3]}}
        case $LL_D in refs/heads/*) LL_D=${LL_D#refs/heads/} ;; heads/*) LL_D=${LL_D#heads/} ;; esac
        case $LL_D in master | main) LL_CLASSES+='PROTECTED ' ;; HEAD) LL_CLASSES+='PUSHFORM ' ;; esac
    else
        LL_CLASSES+='PUSHFORM '
    fi ;;
esac
```

- It runs only when `PUSH` is already in the class list (from line 529 or line 648). A push spelled so that neither fires never reaches this check.
- It matches the **raw** `cmd`, not T: quotes, backslashes, a path to git (`/usr/bin/git`), a dashed `git-push`, any prefix (env, `-C`, `-c`, `--git-dir`), any option other than `-u`/`--set-upstream`, a second refspec, a trailing comment, a doubled space or a tab between words, or a second line all fail the regex and give `PUSHFORM`.
- Destination: group 5 (`<dst>` after `:`) or else group 3 (`<src>`); one leading `refs/heads/` or `heads/` is stripped; then an exact, case-sensitive compare with `master | main` gives `PROTECTED`; `HEAD` gives `PUSHFORM`.
- Decision (lines 722-741): classes are taken in the order `BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL` (line 722); first blocked class wins.
  - `PROTECTED:W | PROTECTED:WA | PROTECTED:F | PROTECTED:FS) ll_deny LL-PROTECTED ;;` (line 732) -> prints the line 59 text. PROTECTED precedes PUSH in the order, so even at W/WA/F a push to main shows LL-PROTECTED, not LL-PUSH.
  - `PUSHFORM:W | PUSHFORM:WA | PUSHFORM:F | PUSHFORM:FS) ll_deny LL-PUSH-FORM ;;` (line 731).
  - `PUSH:FS` is allowed (line 726); `PUSH:W | PUSH:WA | PUSH:F` deny LL-PUSH (line 729).
- So at **full --submit**, the only push L1 lets through is `git push [-u|--set-upstream] origin <name>[:<name>]` whose destination, after stripping `refs/heads/` or `heads/`, is not exactly `master`, `main` or `HEAD`.
- The LL-PUSH-FORM Why text (line 56) describes this form as `git push [-u] origin <branch> (or <source>:<branch>)` [CODE-VERIFIED line 661; the regex also accepts `--set-upstream`, which the message does not mention].

**What the canonical form cannot see (destination resolved outside the text).** git docs (git-scm.com/docs/git-push, fetched 2026-11-08): "`<src>` without a `:<dst>` means to update the same ref as the `<src>`, unless the `remote.<repository>.push` configuration specifies a different `<dst>`." So a canonical `git push origin feature` reaches `refs/heads/main` if `remote.origin.push` maps it there, and it reaches whatever URL `remote.origin.url`/`pushurl`/`url.*.pushInsteadOf` resolve to. L1 refuses *setting* these through git (line 532, line 650-651) but reads no existing configuration. The canonical check also does not know which repository the current directory is: `cd` persists between Bash calls, so the same text pushes from whatever checkout the session last moved to.

**Key Takeaways**
- The PROTECTED refusal is a literal test of the refspec text; it covers `main`, `master`, `HEAD:main`, `x:refs/heads/main`, `x:heads/main`.
- Every non-canonical push text is refused at every level (PUSHFORM), so `--no-verify`, `--force`, `--mirror`, `--all`, `--tags`, `--delete`, `:main`, `+main` and all env/`-c`/`-C`/`--git-dir` prefixes are refused as long as the command contains a git word and the word `push`.
- A destination chosen by existing git configuration, not by the text, is invisible to L1.

## 6. Tamper tokens and git hook files (lines 439-452, 672-680, 703-714)

- `LL_TT` is T for Bash/Monitor (line 442) or the edit path EPATH for Edit/Write/NotebookEdit (lines 674-679; EPATH is the path with `/` runs squeezed and `/./` collapsed, line 676). File **contents** written by Edit/Write are never read (comment line 678: "the tamper check only; contents are never read") [CODE-VERIFIED lines 672-680].
- Token list (line 706, verbatim): `*"$LL_S1/$LL_S2"* | *.claude/settings* | *.claude/hooks* | *disableAllHooks* | *.gitconfig* | *.git/config* | *.config/git*) LL_CLASSES+='TAMPER '`.
- Extra Bash-only tokens: `case $T in *install_hooks*) LL_CLASSES+='TAMPER '` (line 443); a word ending `.claude` or `.claude/` (line 451); `install` after a `superclaude` word in the same segment (line 452).
- Edit path with `/../` or ending `/..` is TAMPER (line 680).
- Store-path dot/slash tricks (lines 712-714) with the in-code admission at lines 710-711: "shortcut: text only; variables and quoting tricks still pass, so the real fix is the L2 layer." [CODE-VERIFIED: the comment describes the code it sits on; it also confirms the authors treat L1 as text-only].

**There is no `.git/hooks` token.** Line 706 has no `hooks/pre-push`, `.git/hooks` or `git-path hooks` pattern, and `.git/hooks/...` does not set `LL_GIT` (section 3). So, statically:
- Write/Edit tool to `<repo>/.git/hooks/pre-push` or to the common-dir `<main checkout>/.git/hooks/pre-push`: EPATH has no token -> no class -> exit 0 (line 743). **ALLOWED** at every level.
- Bash `rm`, `mv`, `chmod -x`, `ln -sf /bin/true`, `cp /dev/null`, `printf ... >` on `.git/hooks/pre-push`: no git word, no token -> **ALLOWED**.
- Exception: a command that resolves the hooks path through git (for example `git rev-parse --git-path hooks`) has a git word; `rev-parse` is allowed in G3 (line 649), so it is still ALLOWED unless another token fires.
- The LL-TAMPER message (line 95) says it covers "the Claude Code settings or hooks, a git configuration file". "hooks" there means Claude Code hooks (`.claude/hooks`); git hooks are not covered [CODE-VERIFIED line 706: no git-hooks token].

**git configuration file coverage is partial.**
- Covered by text token: any T or edit path that contains the contiguous text `.gitconfig`, `.git/config` or `.config/git` (line 706).
- Not covered: a command that never spells the joined path, for example `cd /path/to/main/.git && printf '...' >> config` (T has `.git` and `config` apart; no git word; no token). Also not covered: `<common>/.git/worktrees/<id>/config.worktree` (contains `.git/worktrees`, not `.git/config`; it is read only when `extensions.worktreeConfig` is true [UNVERIFIED for this repo]), and `/etc/gitconfig` (no leading `.` before `gitconfig`; needs root).
- Through such a write an agent can set `core.hooksPath`, `alias.<x>`, `remote.origin.push`, `remote.origin.pushurl` or `url.<x>.pushInsteadOf` without any of the line 532 tokens being checked (line 532 runs only when `LL_GIT=1`).

**Integration opportunities (for an L2 tamper token).**
- Add `*.git/hooks*`, `*hooks/pre-push*` and `*config.worktree*` to the line 706 `case`, so they apply to both Bash T and the edit path through the shared `LL_TT`.
- If L2 is installed through `core.hooksPath` pointing under `~/.claude/hooks/...`, the existing `*.claude/hooks*` token (line 706) already protects the hook files from Edit/Write and from Bash text that spells the path; `hookspath` (line 532) already refuses changing `core.hooksPath` through git.
- Add a `hookspath` / `alias.` scan that does not depend on `LL_GIT` (move those tokens out of the `if [ "$LL_GIT" = 1 ]` block at line 525) so a config write without a git word is caught.

**Key Takeaways**
- L1 does not protect `.git/hooks/pre-push` at all: write, chmod, rm, mv and ln on it are allowed in every governed session.
- git config protection depends on the path being spelled contiguously; `cd .git && ... >> config` and `config.worktree` escape it.

## 7. Pushes by tools that do not run `git push`

| Tool form | Trace | Result |
|---|---|---|
| `curl -X POST https://github.com/o/r.git/git-receive-pack --data-binary @pack` (also `--data`) | G has `/git-receive-pack ` -> `LL_GIT=1` (line 486). No ` push `/` send-pack `/` http-push ` (line 528). No `repos/`, `api.github.com` (line 494) -> `LL_URL=0`. Segment CP is `curl`; the URL word's basename `git-receive-pack` passes `LL_RE_DASH` but is not CP (line 637). No class. | **ALLOWED** (exit 0, line 743). |
| `curl ... https://api.github.com/repos/o/r/git/refs/heads/main` (PATCH/POST/DELETE) | `*api.github.com*` -> `LL_URL=1` (line 494); H5 `*api.github.com*) LL_H5+='GHWRITE '` (line 565); added when the segment has no gh word (line 656). | **REFUSED** (LL-GH-WRITE, line 734), any method, any level. |
| same with the host hidden (`https://api.$H/...`, an IP, a proxy host, `--resolve`, GitHub Enterprise host) | `repos/` still sets `LL_URL=1` but H5 needs `/merge(s)` or the literal `api.github.com`/`uploads.github.com` (lines 562-565). | **ALLOWED** (no class). |
| `gh api -X PATCH repos/o/r/git/refs/heads/main -f sha=...` | `LL_GH=1`, ` api ` in G (line 495); word `-X` matches `LL_RE_W` `^(-[A-Za-z]*[XfF].*\|--method.*\|...)$` (line 500) -> `LL_OK=0`. | **REFUSED** (GHWRITE -> LL-GH-WRITE, lines 523, 734). |
| `gh api --method POST repos/o/r/git/refs -f ref=refs/heads/main -f sha=...` | `--method` matches `LL_RE_W` (line 500). | **REFUSED** (LL-GH-WRITE). |
| `gh api` with the word `api` hidden (`gh $'\x61pi' -X PATCH ...`) | T turns `$'\x61pi'` into `x61pi`, so ` api ` is absent and H2 does not run (line 495). H3: group `x61pi` hits `*) [ "$LL_CP" != "$i" ] \|\| LL_CLASSES+='UNKNOWN '` (line 596): refused in command position, **not** refused behind an underscore env prefix (section 4). | **PARTIAL**. |
| MCP tool `mcp__<srv>__push_files`, `create_ref`, `update_ref`, `create_or_update_file`, `create_branch` | lines 688-699: name contains `*push*`, `*create_ref*`, `*update_ref*` and so on, not prefixed `list_`/`get_`/`search_`/`read_` -> `MCP`; `*merge*` -> MERGE. | **REFUSED** (LL-MCP line 736, LL-MERGE line 733). |
| `uv run python -c "...dulwich... porcelain.push(...)"` or `pygit2 ... remote.push([...])` | Python attribute calls give `.push` (the char before `push` is `.`, so line 528 does not match); `dulwich`/`pygit2` are not git words. If the text also has ` git ` and ` push ` as words (for example `subprocess.run(['git','push',...])`), PUSH fires and the canonical check fails -> PUSHFORM. | **PARTIAL**: typical library calls ALLOWED; a subprocess call spelling `git` and `push` REFUSED. |
| `uv run python <script>` where the script (written with Write) pushes | The command text names only the script; Write contents are never read (line 678). | **ALLOWED**. |

Whether pygit2/libgit2, dulwich or GitPython run the client-side pre-push hook is outside this file [UNVERIFIED; belongs to the L2 hook-semantics research].

**Key Takeaways**
- L1 stops GitHub REST/GraphQL writes only when the literal host `api.github.com` (or `uploads.github.com`) or a `gh api` write flag appears. The smart-HTTP `git-receive-pack` endpoint on `github.com` is not covered.
- Library-based pushes and pushes from script files pass L1; none of them run `git push`, so a pre-push hook may not see them either.

## 8. Coverage table (candidates as written)

Verdict is for a governed session at **full --submit** (FS), the only level where a plain push is allowed. At worktree, worktree (approved) and full, every text that gets `PUSH` is refused anyway (`PUSH:W | PUSH:WA | PUSH:F` -> LL-PUSH, line 729); an ALLOWED verdict below that comes from "no class at all" holds at every level. PUSHFORM means: the line 661 regex failed, `LL_CLASSES+='PUSHFORM '` (line 667), `ll_deny LL-PUSH-FORM` (line 731).

| Candidate | Verdict | Deciding regex or branch | file:line |
|---|---|---|---|
| `git push --no-verify origin <b>` (any position of `--no-verify`) | REFUSED | `push` word -> PUSH (`( \|/git-\| git-)(push\|send-pack\|http-push) `); canonical `^[[:space:]]*git push( (-u\|--set-upstream))? origin (...)...$` fails on `--no-verify` -> PUSHFORM | launch-level-guard.sh:528-529, 661, 667, 731 |
| `git -c core.hooksPath=/dev/null push ...` | REFUSED | `alias\.\|pushurl\|insteadof\|hookspath\|...` matches `hookspath` -> UNKNOWN (wins over PUSHFORM by order) | :532-533, 722, 735 |
| `git -c core.hooksPath=<other dir> push ...` | REFUSED | same `hookspath` token; also PUSHFORM | :532-533, 667, 735 |
| `git config core.hooksPath <dir>` (also `--global`, `--file`, `set`) | REFUSED | `hookspath` token; G3 `config) case $LL_NX in --get \| --get-all \| --get-regexp \| --list \| -l \| get \| list) ;; *) LL_CLASSES+='UNKNOWN '` | :532, 651, 735 |
| persistent `core.hooksPath` by writing the config file directly | PARTIAL | refused when T/edit path contains `.gitconfig`, `.git/config` or `.config/git` (`*.gitconfig* \| *.git/config* \| *.config/git*`); allowed when the path is not spelled contiguously (`cd .../.git && ... >> config`) or is `config.worktree` | :706, 738 |
| `git send-pack ...` / `git-send-pack` | REFUSED | `send-pack` in push regex -> PUSH; G3 `*) LL_CLASSES+='UNKNOWN '` in command position -> LL-UNKNOWN | :528-529, 653, 735 |
| `git http-push ...` / `git-http-push` | REFUSED | `http-push` in push regex; G3 UNKNOWN | :528-529, 653, 735 |
| `git-push origin <b>` | REFUSED | `( \|/)git(-[a-z][a-z-]*)? ` sets LL_GIT; ` git-push ` -> PUSH; canonical needs literal `git push` -> PUSHFORM | :486-488, 528-529, 661, 667 |
| `/usr/lib/git-core/git-push origin <b>` | REFUSED | `/git-push ` -> PUSH; PUSHFORM | :528-529, 661, 667 |
| `GIT_DIR=<path> git push ...` | REFUSED | canonical regex anchored `^[[:space:]]*git push` -> PUSHFORM | :661, 667, 731 |
| `git --git-dir=<path> push ...` | REFUSED | PUSHFORM (G3 still finds `push`, line 628-629, 648) | :648, 661, 667 |
| `git -C <dir> push ...` | REFUSED | PUSHFORM | :661, 667 |
| `cd <dir>` in one call, then a canonical `git push origin <b>` | ALLOWED (non-main `<b>`) | the push text is canonical; L1 has no notion of which repository the cwd is | :661-665, 726 |
| edit `.git/hooks/pre-push` with Write/Edit | ALLOWED | no token in `*"$LL_S1/$LL_S2"* \| *.claude/settings* \| *.claude/hooks* \| *disableAllHooks* \| *.gitconfig* \| *.git/config* \| *.config/git*` | :679, 706, 743 |
| `rm` / `mv` / `chmod -x` / `ln -sf` / `printf >` on `.git/hooks/pre-push` (repo or common dir) | ALLOWED | no git word (`.git/` fails `( \|/)git...`), no tamper token | :486, 706, 743 |
| `git config alias.<x> ...` / `git -c alias.<x>=... <x>` | REFUSED | `alias\.` token; config non-read G3 | :532, 651, 735 |
| alias defined by a direct file write, then `<VAR_WITH_UNDERSCORE>=1 git <x> origin main` | ALLOWED | write: no git word, no contiguous token; call: CP moves to the env name (W has no `_`), G3 skipped by `[ "$LL_CP" = "$i" ] \|\| continue`, no ` push ` word | :435, 556-557, 637, 706 |
| `git config remote.origin.pushurl ...` | REFUSED | `pushurl` and ` remote.` tokens | :532, 735 |
| `git config url.<x>.insteadOf` / `pushInsteadOf` | REFUSED | `insteadof` and ` url.` tokens | :532, 735 |
| `git push origin HEAD:main` | REFUSED | canonical matches; `LL_D=${BASH_REMATCH[5]:-${BASH_REMATCH[3]}}` = `main` -> `master \| main) LL_CLASSES+='PROTECTED '` -> LL-PROTECTED (line 59 text) | :661-665, 732 |
| `git push origin main` / `x:refs/heads/main` / `x:heads/main` | REFUSED | same PROTECTED path after `refs/heads/` / `heads/` strip | :663-665, 732 |
| `git push origin +main` | REFUSED | `+` not allowed by `([A-Za-z0-9_][A-Za-z0-9._/-]*)` -> PUSHFORM | :661, 667 |
| `git push origin :main` | REFUSED | group 3 needs at least one char before `:` -> PUSHFORM | :661, 667 |
| `git push origin --delete main` / `-d` | REFUSED | PUSHFORM | :661, 667 |
| `git push --mirror` / `--all` / `--tags` | REFUSED | PUSHFORM | :661, 667 |
| `HOME=<dir> git push ...` | REFUSED | PUSHFORM (anchored regex) | :661, 667 |
| `env -i git push ...` | REFUSED | PUSHFORM | :661, 667 |
| `env -u HOME git push ...` | REFUSED | PUSHFORM | :661, 667 |
| `PATH=<dir without uv> git push ...` | REFUSED | PUSHFORM | :661, 667 |
| `curl -X POST` / `--data` to `https://github.com/<o>/<r>.git/git-receive-pack` | ALLOWED | sets LL_GIT via `/git-receive-pack `, but no push word, no `api.github.com`, basename `git-receive-pack` not in command position | :486, 494, 528, 637, 743 |
| `curl` to `https://api.github.com/repos/<o>/<r>/git/refs...` | REFUSED (PARTIAL if host is hidden) | H5 `*api.github.com* \| *uploads.github.com*) LL_H5+='GHWRITE '` | :494, 565, 656, 734 |
| `gh api -X PATCH repos/<o>/<r>/git/refs/heads/main` | REFUSED | `LL_RE_W='^(-[A-Za-z]*[XfF].*\|--method.*\|--field.*\|--raw-field.*\|--input.*)$'` | :499-523, 734 |
| `gh api --method POST .../git/refs` | REFUSED | same `--method.*` | :500, 523, 734 |
| `uv run python -c` with pygit2/dulwich/GitPython | PARTIAL | `.push(` is not a ` push ` word; only a text that also spells ` git ` and ` push ` as words gets PUSH -> PUSHFORM | :486, 528, 661, 667 |
| `uv run python <script>` that pushes | ALLOWED | command text has no push word; Write contents never read | :678, 743 |

**Key Takeaways**
- Every literal `git push` spelling in the candidate list that is not exactly canonical is refused (PUSHFORM), and every canonical push to `main`/`master` is refused (PROTECTED).
- The ALLOWED rows share one cause: the command never contains a git word together with the word `push` (hook-file edits, smart-HTTP `curl`, scripts), or command position is moved off `git` so G3 never looks at an alias or helper name.

## 9. L1 evasions found by static reading (not executed)

These were derived only from the regexes; none was run. Each is a gap the L2 design should assume exists.

| Spelling | Why L1 passes it | file:line |
|---|---|---|
| `A_B=1 git $'\x70ush' --no-verify origin main` | T turns `$'\x70ush'` into `x70ush` (sed at line 431), so G has no ` push ` word (line 528); W drops `_` (line 435), so CP lands on `A` (line 556-557) and G3 never sees subcommand `x70ush` (line 637); G4 needs `$` in the subcommand (line 634), which T removed. No class -> exit 0 at **every** level. Without the `A_B=1` prefix, G3 refuses it as UNKNOWN (line 653). | :431, 435, 528, 556-557, 634-637, 743 |
| `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=$'core.hooks\x50ath' GIT_CONFIG_VALUE_0=/dev/null` before such a call | the `hookspath` token (line 532) is matched as text; `hooks\x50ath` becomes `hooksx50ath` in T. Combined with the row above it removes the pre-push hook for that call. | :431, 532 |
| `cd <common-dir>/.git && printf '[remote "origin"]\n\tpush = refs/heads/<b>:refs/heads/main\n' >> config`, later the canonical `git push origin <b>` | the write has no git word and no contiguous `.git/config`; the later push is canonical with a non-main destination, so it passes at FS, and git maps it to `refs/heads/main` through `remote.origin.push` (git-push docs, see section 5) | :486, 525, 661-665, 706, 726 |
| an unlisted wrapper before `git` (`chrt 0 git ...`, `taskset 1 git ...`, `find . -exec git ... \;`) | the wrapper word becomes CP (line 557) | :549, 557, 637 |

**Key Takeaways**
- L1 is a text classifier with a known, self-declared limit (lines 710-711). A governed agent that tries to evade it can reach `refs/heads/main` without the word `push`, and can disable the pre-push hook through config it writes without a git word.
- For L2, this means the pre-push hook must not rely on L1 to stop `--no-verify`, `core.hooksPath` overrides or hook-file edits. Those three remove a client-side hook entirely, so only server-side protection or a hook-tamper token in L1 can cover them.

## Gaps and Questions

1. **No git-hooks tamper token** (line 706): Write/Edit/rm/chmod/mv/ln on `.git/hooks/pre-push` and the common-dir hooks are ALLOWED. Proposed: add `*.git/hooks*` and `*hooks/pre-push*` to line 706.
2. **Underscore env prefix moves command position** (lines 435, 556-557, 637): `LL_RE_NAME` allows `_` but W has already turned `_` into a space. G3's unknown-subcommand and alias refusal is therefore skipped behind `GIT_*=` style prefixes. This contradicts the LL-UNKNOWN Why text (line 80) [CODE-CONTRADICTED, see Stale Documentation].
3. **Config-rewrite tokens need a git word** (line 525, 532): a direct file write to `.git/config` that does not spell the joined path sets `core.hooksPath`, `alias.*`, `remote.origin.push`, `pushurl` or `insteadOf` without refusal.
4. **Destination from existing configuration is invisible**: a canonical `git push origin <b>` can land on `refs/heads/main` through `remote.origin.push` (git-push docs). L1 reads no git configuration.
5. **Smart-HTTP `git-receive-pack` on `github.com`** (not `api.github.com`) is not refused (lines 494, 565). Same for any GitHub API call whose host is not the literal `api.github.com`/`uploads.github.com`.
6. **Library and script pushes** pass L1. Whether pygit2/libgit2, dulwich or GitPython run the client-side pre-push hook [UNVERIFIED; out of this file's scope]. Routed to Phase 4 web-01 in the Gate 1 cycle 0 fix, together with JGit: see the "ROUTE web-01: (b) other tools" line in 04 Gaps and Questions. No local test was possible (none of these libraries is installed offline).
7. **Repository identity**: L1 does not know which checkout the cwd is. That `cd` persists between Bash calls in a governed session is taken from the Bash tool description, not from code [UNVERIFIED].
8. **Case of the branch name**: the PROTECTED compare is case-sensitive (`master | main`, line 665). Whether GitHub treats `Main` as the protected `main` [UNVERIFIED].
9. **Refname normalisation**: a destination such as `refs//heads/main` passes the regex and is not stripped (line 664), so it is not PROTECTED. Whether git accepts or normalises it on push [UNVERIFIED; git-check-ref-format forbids consecutive slashes, so git probably rejects it].
10. **`config.worktree`** is not a token; whether `extensions.worktreeConfig` is enabled in this repo [UNVERIFIED].
11. **`remote.<name>.mirror`**: git-push docs say `--mirror` "is the default if the configuration option `remote.<remote>.mirror` is set". How that interacts with an explicit refspec in a canonical push [UNVERIFIED].
12. **Shell profile changes**: whether a governed session's Bash calls pick up a mid-session edit to `~/.bashrc` (for example an exported `GIT_CONFIG_PARAMETERS`) [UNVERIFIED]; `~/.bashrc` is not a tamper token (line 706).
13. The section 9 evasions are static readings; none was executed (task safety rule). They should be confirmed by the L1 test suite, not by running the guard here.
14. Local-path remotes only: `git --git-dir=<bare remote> fetch ...` or `git -C <bare remote> update-ref refs/heads/main ...` (COMMIT, allowed at FS, lines 643-646) can change a remote that is a local directory. Not relevant to a GitHub remote.

## Stale Documentation Found

- **[STALE DOC] / [CODE-CONTRADICTED]** LL-UNKNOWN Why, line 80: "only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge." The code refuses unknown subcommands only for the git word in command position (line 637), and an underscore env prefix or an unlisted wrapper moves command position off `git` (lines 435, 549, 556-557). An alias call such as `A_B=1 git p ...` is not refused.
- **[CODE-CONTRADICTED] (partial)** LL-TAMPER Blocked text, line 95: "touching ... a git configuration file". Code covers only paths that contain `.gitconfig`, `.git/config` or `.config/git` as contiguous text (line 706); `cd .git && ... >> config`, `config.worktree` and `/etc/gitconfig` are not covered.
- **Minor, not stale:** LL-PUSH-FORM Why, line 56, describes `git push [-u] origin <branch>`; the regex at line 661 also accepts `--set-upstream` [CODE-VERIFIED with this addition].
- **[CODE-VERIFIED]** header line 3 names `docs/designs/sc-issue-launch-level-hook.md`; the file exists (Glob). Its content was not compared with the code in this file.
- **[CODE-VERIFIED]** comments at lines 418-420 (one sed, four tr), 440-441 (W has no `_`), 483-485 (which checks read G vs segments), 658 (only one plain git push to origin passes), 678 (edit contents never read), 710-711 (text-only shortcut; real fix is L2).

## Summary

L1 refuses every literal `git push` that is not exactly `git push [-u|--set-upstream] origin <name>[:<name>]` (LL-PUSH-FORM, lines 661/667/731), and refuses a canonical push whose destination, after stripping `refs/heads/` or `heads/`, is `main` or `master` (LL-PROTECTED, lines 663-665/732, text at line 59); so `--no-verify`, `-c core.hooksPath`, `send-pack`, `http-push`, dashed and path spellings, env/`-C`/`--git-dir` prefixes, `+main`, `:main`, `--delete`, `--mirror`, `--all`, `--tags`, `gh api` writes and literal `api.github.com` calls are all refused. It does not protect `.git/hooks/pre-push` at all (no token at line 706), it misses a smart-HTTP `curl` to `git-receive-pack`, library and script pushes, and config written without a git word or a contiguous `.git/config` path. A static reading also shows that an underscore env prefix moves command position off `git` (W drops `_`, line 435), so an obfuscated subcommand such as `$'\x70ush'` or an alias passes L1 at every level; together with `--no-verify` or a `core.hooksPath` override that defeats a client-side pre-push hook as well. The L2 design should therefore treat L1 as advisory, add a `.git/hooks` tamper token to line 706, and rely on server-side protection for `refs/heads/main` and `refs/heads/master`.
