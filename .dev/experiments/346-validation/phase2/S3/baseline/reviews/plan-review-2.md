# Plan Review 2: refactor-plan.md (second adversarial review, after fix cycle 1)

Reviewer stance: the revision is assumed to contain mistakes. I did not edit the plan. Everything below was run, not guessed: bash 5.2.37, GNU sed 4.9, GNU tr 9.7, jq 1.7, git 2.47.3, in a throwaway directory under `/tmp` (two local bare repos, a stub `gh`; all removed at the end). Nothing inside the repository was changed.

## Verdict: FAIL

- Blocking findings: 8 (F-1 to F-8)
- Minor findings: 12 (m-1 to m-12)

The eight first-round findings are closed for the exact attacks the first review ran. The new canonical push form and the GET-only `gh api` rule are good ideas. But the word scan that decides whether the push rule even runs has holes, and four of them reach `main` in one line at the `worktree` level. All eight blocking items are narrow and cheap to fix; the exact replacement text is given for each.

## 1. First-round findings B-1 to B-8: did the fix close the original failure?

I re-ran the original attacks against the plan's new rules (the plan's own NM2 to NM6 pipeline copied into a script, the plan's push regex in bash `[[ =~ ]]`, the plan's H2 flag regex, and real git).

| Id | Original attack | Result against the new rules | Verdict |
|---|---|---|---|
| B-1 | ``git push origin a:b `echo c:main` `` | Raw-command regex does not match, so PUSHFORM; blocked at every level. Real git moved `main` for the old rule; not reachable now. | PASS (attack blocked). The AC-6 claim built on it is still false, see F-1, F-2, F-6, F-7. |
| B-2 | `git push origin a:b \` newline `c:main` | Regex does not match (inner newline), PUSHFORM. NM2 joins the lines (I confirmed `git push origin a:b   c:main`). | PASS for pushes. The join itself is wrong for an escaped backslash, see F-1. |
| B-3 | `/usr/lib/git-core/git-push origin main`, `git-push origin main` | Regex does not match, PUSHFORM. G0 reads `git-push` as `git push`; `$(git --exec-path)/git-push origin main` gives segments `$`, `git --exec-path` (UNKNOWN, no subcommand) and `/git-push origin main` (PUSH then PUSHFORM). | PASS |
| B-4 | `--method=POST`, `-XPOST`, `--raw-field=`, `-iXPOST`, `-Fbody=x`, `PUT contents/x -f branch=main` | H2 item 1 regex matches every one of these words (I ran all 15 listed in "Named regex cases"; plain words like `-q`, `--jq`, `-H`, `-i`, `--silent` do not match). | PASS for the spellings. FAIL for a flag the shell builds, see F-3. |
| B-5 | N3/N4 had no allowed tool; `tr` lost newlines | Named `sed -E` and `tr`. I ran NM2 to NM6 on the worked examples: the heredoc gives segments `[git commit -F -]`, `[fix: use git for hooks]`, `[EOF]`; the `gh api \` example gives one segment; `git push origin a:b 2>&1 \| tail -5` gives two segments. All match the plan text. | PASS. But NM4 has a new hole, see F-6. |
| B-6 | Background subagents not in TURN | Rewritten as an honest "not blocked, rests on harness wrapping (U4)" with O-17, R16, T-APR-10. The claim is now true as written. | PASS (honest). See m-6: item 5 is not a ship gate. |
| B-7 | AC-5 and a deleted session file | O-16, AC-5 limit text, section 13 sentence. | PASS for the wording of the limit. FAIL for the justification, which is false, see F-4. |
| B-8 | False claim about messages | G4 and "Departs from (2)" reworded for multi-line bodies. | PARTLY. The multi-line part is now true. The one-line part of the same sentence is still false for `gh pr create`, see F-8. |

## 2. Rules re-tested (at least eight)

| # | Rule | Accept examples run | Reject examples run | Result |
|---|---|---|---|---|
| 1 | Canonical push ERE (Change 11) | A1 to A13 style: `git push origin feature`, `-u`, `--set-upstream`, `3f2a9c1e:feature/x`, outer spaces, trailing newline, `refs/heads/heads/main` (dest `heads/main`) | backtick, continuation, dashed, `a:b c:main`, two commands on two lines, `;`, `2>&1`, tab-separated second refspec, `a:$B` | All as the plan says. **Defect:** a lone option word such as `--all`, `--mirror`, `-f`, `--force`, `--delete` after `origin` matches (F-2). |
| 2 | Destination check | `x:heads/main` gives `main` (PROTECTED) | 17 odd destinations run with `git push --dry-run`: `refs/heads/main/`, `refs/heads//main`, `./main`, `/main`, `refs/./heads/main`, `heads//main`, `main.`, `main^0`, `@` are all "invalid refspec" in git 2.47.3 | The plan's "git refuses these" claim is true. Note `@` can never reach the destination step because `@` is not in the character class (m-4). |
| 3 | gh flag regex H2 item 1 | all 15 GHWRITE words match | all 11 plain words do not match | True as stated. `-$X` and `--m$ethod` do not match (F-3). |
| 4 | NM2 to NM6 on a heredoc | worked example reproduced exactly | | PASS. |
| 5 | NM2 on a continuation | `gh api \` + `-X PATCH ...` is one segment | `\\` (escaped backslash) then newline is joined too, which the shell does not do (F-1) | Defect. |
| 6 | NM4 redirection removal | `2>&1`, `> /tmp/log 2>&1`, `< /dev/null` removed | `A=">" git push ...` loses the word `git` (F-6) | Defect. |
| 7 | Session id `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$` | 128 chars, UUID | empty, `.`, `..`, `x.ok`, `a/b`, `-lead`, 129 chars, `a b`, id with a trailing newline | PASS (matches T-BIND-14). |
| 8 | Marker: strict ERE and loose start test | 32 lowercase hex | uppercase, 33 hex, `v2`, `<nonce>`; loose: BOM, spaces, tab, newline in any order pass; `see [sc-launch:...]` does not | PASS. |
| 9 | Approval matcher | `approved`, `Approved.`, `  APPROVED!  `, `/task x`, `/task`, `/sc:implement`, `/sc:task y`, a leading blank line then `/task x` | `please approved`, `approved, but`, `approved?`, `approved` + newline + `please go`, `/tasks`, `/task-builder x`, `/sc:implement-protocol`, `/Task x`, a second-line `/task x`, `<task-notification>approved</task-notification>` | PASS. Note `/task` + newline + `rm -rf` approves (first line only); that is by design. |
| 10 | PreToolUse matcher (node regex) | `Bash`, `Task`, `Agent`, `SendMessage`, `CronCreate`, `ScheduleWakeup`, `mcp__github__merge_pull_request`, `mcp__github__push_files` | `Read`, `Grep`, `Glob`, `TaskCreate`, `TaskUpdate`, `TaskOutput`, `TaskStop`, `BashOutput`, `WebFetch`, `mcp__codegraph__codegraph_search`, `mcp__github__add_issue_comment` | PASS, matches T-REG-3 (R10 covers the unmatched issue-comment tool). |
| 11 | P5 field transport (`jq` `gsub`) | newline and NUL in a path become spaces | `gsub` on a missing field errors in jq 1.7 | Defect (m-1). |
| 12 | Speed of NM2 | normal 84 KB text 5 ms | 64 KB of `\` + newline lines: 0.79 s (quadratic loop) | Within the 5 s timeout, near the 1 s assert (m-5). |

## 3. Blocking findings

### F-1 (BLOCKING). A "later" git word is exempt from UNKNOWN, so an alias hides a commit or a push to `main`

Evidence, run on real git. Setup: a bare remote and a clone, `main` and `feature`.

- Command: `git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1`
- The plan's pipeline gives one segment `git rebase -x git -c alias.p=push p origin HEAD:main HEAD~1`. First git word: S = `rebase` (NONE). Second git word is "later"; its S = `p` is not on the allowlist, which is UNKNOWN for a first word but NONE for a later one (G4). No PUSH or COMMIT class is collected, so the push regex never runs.
- Real result: remote `main` moved from `681a2ef` to `d943c98`. This works at `W`, `WA`, `F` and `FS`.
- The plan's own G4 sentence says this nested form "is still caught". It is caught only when the inner command is a plain `git push`.
- A second route to the same hole, from NM2: `git status \\` (escaped backslash) newline `git -c alias.p=push p origin HEAD:main`. The shell runs two commands; NM2 joins them into one segment, so the second git word becomes "later". Same result.
- Aliases are listed in TH2 as a designed-against threat, and Change 10 says "aliases need no rule of their own". That is false for nested commands.

Replacement text, Change 10 G4:

> **G4.** A git word is *first* when no earlier word of its segment is a git word, and *later* otherwise. A later git word keeps every class. A later git word whose S is not on the allowlist is also UNKNOWN, except when the segment's first git word has S `commit`, `tag`, `log`, `show` or `stash` (their arguments are message or pattern text), or when a `gh` word comes earlier in the segment (the git word is message text, see F-8). So `git commit -m "fix git handling"` is allowed, and `git rebase -x 'git -c alias.p=push p origin HEAD:main' HEAD~1`, `git bisect run git ...` and `git grep -O 'git ...'` are UNKNOWN at every level. A multi-line message is still scanned line by line (NM5); a body line that starts with `git <word>` is UNKNOWN (R8).

Replacement text, Change 9 NM2 `sed` script (join only when the line ends in an odd number of backslashes; tested, `git status \\` stays two lines, `git status \` joins):

```bash
T=$(printf '%s\n' "$cmd" | sed -E -e ':a' -e '/(^|[^\\])(\\\\)*\\$/{' -e '$!N' -e 's/\\\n/ /' -e 'ta' -e '}' \
      -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e ':b' -e 's#/\./#/#' -e 'tb')
```

Add tests `T-GIT-14 test_nested_alias_push_blocked` (the rebase command above, the `\\` pair above, `git bisect run git -c alias.c=commit c`: UNKNOWN at every level) and extend `T-NRM-5` with the `\\` case.

### F-2 (BLOCKING). The push regex accepts a lone option word, so `git push origin --all` reaches `main` at `full --submit`

Evidence: the character class `[A-Za-z0-9._/-]+` starts with any of those characters, including `-`. Ran the plan's ERE:

- MATCH with destination = the option word: `git push origin --all`, `--mirror`, `--tags`, `--prune`, `--force`, `-f`, `--delete`, `--force-with-lease`, `--follow-tags`, `--no-verify`, `--atomic`, `--receive-pack`, `--exec`. Also `git push origin ..`, `./x`, `.`.
- The destination is never `main`, so the call keeps class PUSH only and is allowed at `FS`.
- Real git: local `main` was one commit ahead of remote `main`; `git push origin --all` printed `c4864c4..654a4ee main -> main`. `git push origin --mirror` printed `- [deleted] other`, a remote branch removal.
- The plan's Consequences paragraph says `--all`, `--mirror` and force pushes "are PUSHFORM". That is true for `git push --all origin` (option before the remote) and false for the option after `origin`.

Replacement text, Change 11 item 1 (refspec and destination must start with a letter, digit or `_`; capture numbers unchanged; tested: all the option words above no longer match, A1 to A13 style cases still match):

```
^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9_][A-Za-z0-9._/-]*)(:([A-Za-z0-9_][A-Za-z0-9._/-]*))?[[:space:]]*$
```

Reword "one refspec made only of letters, digits, `.`, `_`, `/` and `-`" to "one refspec that starts with a letter, digit or `_` and continues with letters, digits, `.`, `_`, `/` and `-`". Add accept/reject cases to T-PSH-11 and T-PSH-12: reject R24 `git push origin --all`, R25 `git push origin --mirror`, R26 `git push origin -f`, R27 `git push origin x:--all`. Delete the dead word "`@`" from item 3 (m-4).

### F-3 (BLOCKING). GET-only `gh api` still lets the shell build the method flag (variable inside a word, or a backtick)

Evidence, with a stub `gh` that prints its arguments:

- `X=X; gh api repos/o/r/git/refs/heads/main -$X DELETE`: gh receives `[-X] [DELETE]`. In the plan, the word `-$X` fails item 1 (`-` is followed by `$`, which is neither a letter nor X/f/F) and item 3 (the word starts with `-`, not `$`). The endpoint is not `graphql`, `/merge` or `/merges`. Class NONE at every level. DELETE of `refs/heads/main` removes the branch.
- ``gh api repos/o/r/git/refs/heads/main `echo -e '\055X'` DELETE``: gh receives `[-X] [DELETE]`. NM2 deletes the backslash so the text shows `055X`, no `-X` word; NM5 puts the backtick contents in another segment, so the `gh api` segment has no `$` word. Class NONE at every level.
- Change 12's revision-log row says "a flag hidden in a backtick, `$(...)` or variable is caught". True only when the flag is spelled out literally (`echo -XPATCH`) or the word starts with `$`.

Replacement text, Change 12 H2 item 3:

> 3. the raw command `cmd` contains a backtick, or some word after `api` in its segment starts with `$`, or starts with `-` and contains `$`.

Words like `repos/$REPO/commits/x` (the `/sc:pr-submit` form) do not start with `-` or `$` and stay allowed (checked on the line from `conflict-mechanical.md:146`). Add `T-GH-11 test_gh_api_shell_built_flag`: the two commands above are LL-GH-WRITE at every level; `gh api repos/${REPO}/commits/x/check-runs --jq .total_count` stays allowed.

### F-4 (BLOCKING). The justification for O-16 and R3 ("reaching the delete needs a command that names a tamper token") is false; `rm -rf ~/.claude/state` is allowed

Evidence: ran the plan's NM2/NM3 text T through the token list and the "word ends with `.claude`" rule:

| Command | Tamper token hit | Word ends `.claude` |
|---|---|---|
| `rm -rf ~/.claude/state` | none | no |
| `cd ~/.claude/state && rm -rf launch-level` | none | no |
| `find /home/u/.claude/state -delete` | none | no |
| `mv ~/.claude/state ~/.claude/s2` | none | no |
| `rm -rf ~/.claude/state/launch-level` | yes | no |

The token in Change 17 is the long form `.claude/state/launch-level`, so deleting or moving the parent directory is allowed in one natural command. That releases the session (and its `.ok`). The text in R3, O-16's "Why the default", and the INV-037 note all say "only an obfuscated shell command or a script can do it". That is not true, and TH2 lists "editing the guard's state" as designed against. The AC-5 limit is therefore not honest as written.

Replacement text, Change 17 item 1: replace the first token with `.claude/state` (still built from two literal parts, Change 4 item 1). Replace the sentence in R3, O-16 ("Why the default") and the INV-037 note with:

> Reaching the delete from inside the session needs a command that names `.claude/state` (blocked), so only a glob, a variable, a relative path from another subdirectory of `~/.claude` (`cd ~/.claude/skills && : > ../hooks/x.sh`), or a script can do it.

Add to R8: any governed-session command that names `~/.claude/state` is blocked, including reads of the other hooks' state files (the freshness hooks keep files there; the agent does not need them). Add the four commands above to T-TAM-1.

### F-5 (BLOCKING). `$GIT push origin main` is a pinned gap with no residual statement, and R1/O-7 claim inline wrappers are covered

Evidence: row 33 of the decision table pins `$GIT push origin main` as ALLOW at every level and says "(Change 32)". Change 32 has no residual for it (R1 is about a script file and programs; R9 is about plumbing). R1 and O-7 say AC-6's wrapper clause "is met only for wrappers written inline in the command". A variable that holds `git` is written inline. `g=git; $g push origin main` leaves no git word (`$` is kept, `{`/`}` are spaces), so no class is collected and the push to `main` goes through at `W`. The same hole hides `gh`: `GH=gh; $GH pr merge 5`.

Replacement text, R1 (append) and O-7 (default):

> A command word that is a variable or the result of a substitution (`$GIT push origin main`, `g=git; $g push ...`, `GH=gh; $GH pr merge 5`) is not a git or gh word, so inline wrappers that build the command name from a variable are not covered. AC-6's wrapper clause is met for wrappers whose text contains the word git or gh (`bash -c`, `sh -c`, `env`, `sudo`, `xargs`, `eval` with a literal string, a quoted or escaped name, a dashed built-in), not for a variable command name.

Optional cheap rule that closes it: a segment whose first non-assignment word starts with `$` is UNKNOWN. I tested the shape (`$` is a first word for `$GIT push` and `${g}t push`); `REPO="$(git ...)"` and `foo $(bar)` start with a name, so they are not affected. If the owner takes the rule, move row 33's first example to UNKNOWN and add it to T-GIT-2.

### F-6 (BLOCKING). NM4 deletes the word after a quoted `<` or `>`, so the git word disappears: `A=">" git push origin HEAD:main`

Evidence: NM2 deletes quotes first, so a quoted `>` becomes a redirection operator for NM4. The plan's NM4 also deletes "its target word". Pipeline output for `A=">" git push origin HEAD:main`: `seg0=[A= push origin HEAD:main]`, no git word, no class. Real git: remote `main` moved from `654a4ee` to `32e2a87`. The same line with `git commit -m x` hides the commit. It also eats gh flags: `gh api repos/o/r/git/refs/heads/main --jq ".a >" -X DELETE` loses `-X` (the word `-X` is taken as the redirection target).

Replacement text, Change 9 NM4 (remove only the operator, keep the target word; every word stays visible, and a misread subcommand can only fail toward UNKNOWN):

```bash
    | sed -E -e 's/[0-9]*[<>]&([0-9]+|-)/ /g' \
             -e 's/[0-9]*(&>>|&>|>>|>\||>&|<&|<<<|<<-|<<|>|<)/ /g' \
```

Tested with the NM2 fix above: `A=">" git push origin HEAD:main` gives `[A=  git push origin HEAD:main]`; `git commit -m x > /tmp/log 2>&1` gives `[git commit -m x   /tmp/log  ]`; `git status 2>&1 | tail -5` gives two segments; the `gh api ... ".a >" -X DELETE` example keeps `-X`. T-NRM-2 still passes. Change the NM4 prose to "removes redirection operators; the target word stays as an ordinary word". Update the worked example ("redirection target kept in T and in W"). Add `T-NRM-7 test_quoted_redirect_char_keeps_git_word` (`A=">" git commit -m x` is LL-COMMIT at F; `A=">" git push origin HEAD:main` is LL-PUSH-FORM at FS and LL-PUSH below).

### F-7 (BLOCKING). Deleting quotes lets a quoted option value shift the subcommand: `git -c "x.y=a status" push origin HEAD:main`

Evidence: after NM2 the words are `git -c x.y=a status push origin HEAD:main`. G1 makes `-c` consume `x.y=a` and reads S = `status` (NONE). No PUSH class, no regex. Real git: remote `main` moved from `32e2a87` to `4085071`. Same shape with `-C "a b"`, `--git-dir "a b"`, `-c x="a status"`, `-c x='a status'`, `-c core.x=a\ status`. The plan's note that `-C "/dir with space" push` "now fails closed" holds only when the misread word is not an allowlisted subcommand.

Replacement text, Change 10 G1 (add as G1b):

> **G1b.** If the raw `cmd` matches the ERE below, the call gets class UNKNOWN at every level (an option value that contains a space or an escaped space can shift the subcommand after quotes are deleted):
> `(^|[[:space:]])(-c|-C|--git-dir|--work-tree|--namespace|--config-env|--attr-source)[[:space:]]+[^[:space:]'"\\]*(["'][^"']*[[:space:]]|\\[[:space:]])`

Tested: flags `git -c "x.y=a status" push ...`, `git -c x='a status' push`, `git -c x="a status" push`, `git -C 'a b' push`, `git -c core.x=a\ status push`; does not flag `git -C "/dir" status`, `git -C /tmp/x status`, or `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit` (the `/sc:pr-submit` form). Add `T-GIT-15 test_quoted_option_value_blocked`.

### F-8 (BLOCKING). False claim: "one-line ... PR titles that mention git are not blocked"

Evidence: Change 10 "Departs from (2)" says UNKNOWN on the first git word only means "one-line commit messages and PR titles that mention git are not blocked". True for `git commit -m "fix git handling"` (a real git word comes first). False for the command `/sc:pr-submit` issues in Wave 0: `gh pr create --repo "$REPO" --base master --head f --title "docs: explain git hooks" --body "x"`. There is no earlier git word, so the first git word is inside the title, S = `hooks`, UNKNOWN, blocked at every level (pipeline output: one segment, git word inside the title). The same happens for any `gh issue comment` or `--body` text on one line.

Replacement text, Change 10 "Departs from (2)": "INV-011 applied the allowlist to every git word; this plan applies UNKNOWN to the first git word of each segment only, and not to a git word that follows a `gh` word in the same segment (G4). So a one-line commit message and a one-line `gh pr create --title/--body` that mention git are not blocked. A multi-line message or heredoc is scanned line by line, so a body line that starts with `git <word>` is UNKNOWN (G4, R8)." This is satisfied by the G4 text in F-1. Add `gh pr create --repo "$REPO" --title "docs: explain git hooks"` to row 21 of the decision table (allowed at FS) and to T-GH-4.

## 4. Regression hunt (task 3)

### 4.1 `/sc:pr-submit` at `full --submit`: every git and gh command it issues

Read `~/.claude/skills/sc-pr-submit-protocol/SKILL.md`, all of `refs/`, and the script names. Scripts run as `bash`/path calls with `--repo "$REPO"` and are class NONE (not inspected, R1). Inline commands:

| Command (source) | Class under the plan | Passes at FS? |
|---|---|---|
| `REPO="$(git remote get-url origin \| sed -E 's#...##')"` (SKILL.md:274) | NONE (checked with the pipeline; `.git$` and `git@` are not git words) | yes |
| `gh repo view "$REPO" --json defaultBranchRef -q ...`, `gh pr view N --repo "$REPO" --json ...`, `gh pr checks`, `gh run view --log-failed` | NONE | yes |
| `git remote -v`, `git fetch origin <base>`, `git rev-parse`, `git rev-list --parents -n 1`, `git merge-base --is-ancestor`, `git diff --name-only`, `git checkout --ours -- uv.lock`, `git add -- <paths>`, `git rm -- <paths>` | NONE (allowlist) | yes |
| `gh api "repos/${REPO}/commits/<sha>/check-runs" --jq '...'` (conflict-mechanical.md:146) and `gh api repos/<r>/commits/<sha>/check-runs --jq .total_count` (ci-poll.md:61) | NONE (verified with the pipeline; no flag word matches, no `$`-leading word) | yes |
| `gh pr create --repo "$REPO" --base --head --title "..." --body "..."` | SUBMIT, allowed at FS | yes, **unless** title or body contains `git <non-allowlisted word>` (F-8) |
| `git commit --only -- <paths>` (Wave 6) | COMMIT, allowed at FS | yes for a one-line message; a multi-line message with a body line starting `git ...` is UNKNOWN (R8, LL-TEXT names `-F`) |
| `git push origin <target_sha>:<HEAD_BRANCH>` (conflict-mechanical.md:194, SKILL.md Wave 6) | PUSH, canonical form | yes, **if** the values are written out and the push is its own call (O-18); `"$SHA:$BRANCH"` or `2>&1` or `&&` makes it PUSHFORM |
| `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <sha>` | MERGE | **blocked** (O-10, stated) |
| `git merge --abort` (conflict-mechanical.md:226) | MERGE | **blocked, and not stated** (m-9) |
| `git revert -m 1 <merge_sha>` | COMMIT | yes |
| `refs/ci-poll`, `augment-poll` lines `gh api ... --method GET -F per_page=100` | GHWRITE if issued inline | blocked, but these are inside the poll scripts (R1, O-19) |
| Scripts: `reply-resolve-thread.sh`, `retrigger-review.sh`, `finish-merge.sh`, `poll-*.sh`, `probe-merge.sh`, `collect-conflict-evidence.sh` | NONE | yes (invisible to the hook) |
| Skills `sc:pr-submit-protocol`, `sc:troubleshoot-protocol`, local `Agent` calls | SUBMIT allowed at FS; others NONE | yes |

Result: `/sc:pr-submit` is not made unusable by the new push and gh rules once F-8 is fixed. The conflict-sync path is knowingly blocked. The `git merge --abort` consequence should be added to O-10 and the AC-2 limit (m-9).

### 4.2 Internal consistency

Checked, no contradiction: class count 17 and the table of 17 rows; precedence list names all 16 non-NONE classes; every class has a message id; message ids LL-BROKEN and LL-NOBIND exist; LL-STATE and LL-TEXT are notes, not ids, and T-MSG-6 treats them as notes; timeout 5 s is stated once for both registrations; the 65,536-byte cap matches "64 KB" in LL-BIG; capture numbers in Change 11 match the ERE; every test id named in Change 28 exists in Change 27; O-1 to O-19 all have rows; U1 to U20 and R1 to R16 are complete; no stale `PUSHNAME`, `symbolic-ref` (only in rejected-alternatives text), or `Change 5 U<n>` references remain.

Contradictions found:

- Row 33 of Change 20 cites Change 32 for the `$GIT` gap; Change 32 has no such residual (F-5).
- R3, O-16 and INV-037 give a false reason (F-4).
- Change 10 "Departs from (2)" versus row 31 and the pipeline (F-8).
- Row 36 ("input not JSON: BLOCK LL-BROKEN at every level") reads against Change 21's table ("exit 0 when the store is empty or the text names only unbound ids"). Context (governed session) reconciles them, but the row should say "when the text names a bound id or the store holds a bound session" (m-8).
- Change 1 says each id family is used for one thing only and lists G1 to G4; Change 10 also defines G0 (m-10).

### 4.3 Owner decisions and residual list

O-16 to O-19 agree with the rules (O-17 default matches Change 16 item 3, O-18 matches Change 11, O-19 matches Change 12 H2). The residual list is not consistent with the claims in two places: R1/O-7 (F-5) and R3/O-16 (F-4). R16 and U4 are honest about the unverified Monitor and background-subagent notice shape.

## 5. Acceptance criteria, rule by rule

| AC | Satisfied by the plan as written? | Why | Caveat honest? |
|---|---|---|---|
| AC-1 | No | A commit, push or `/sc:pr-submit` is reachable at `W` through F-1, F-6, F-7 (git word hidden or reclassified). IMPL gating by skill name is sound (T1 names checked). | The limit text (framework scripts, command level) is honest; the evasions are not stated. |
| AC-2 | No | Same holes at `F` (commit) and `FS` (push to `main`). Compound push and conflict merge limits are stated (O-18, O-10). | Honest for the stated limits; `git merge --abort` missing (m-9). |
| AC-3 | Yes, conditionally | Whole-prompt approval and `agent_id` filtering are sound (rules 9 above). Self-started turns rely on harness wrapping that is unverified for Monitor and background subagents. | Yes (U4, R16, O-17). See m-6. |
| AC-4 | Yes, conditionally on OB-H1 item 1 | Matcher and session-id gate behave as stated. | Yes. |
| AC-5 | No as justified | Deleting `~/.claude/state` releases a session in one command (F-4). The tamper test cases cover only the long token. Rename and re-claim are sound. | No. The reason given for accepting the deleted-file gap is false. |
| AC-6 | No | `git push origin --all` (F-2), alias nested in `rebase -x` (F-1), `A=">" git push ...` (F-6), `git -c "x=a status" push ...` (F-7), `gh api ... -$X DELETE` (F-3), `$GIT push origin main` (F-5). | No. R1/O-7 overstate inline-wrapper coverage; the revision log says "closed". |
| AC-7 | Yes | Every class reaches a message; precedence is total; T-MSG-2 checks reachability. | Yes. |
| AC-8 | Partly | Case coverage is broad, but no test covers the eight holes above (T-GIT-14, T-GIT-15, T-PSH-12 additions, T-GH-11, T-NRM-7, T-TAM-1 additions are new). | n/a |

## 6. Size discipline

I estimate the script at 500 to 600 lines of bash, not 400: the 18-message table with notes (60 lines), the policy `case` grid (25), binding B1 to B13 with loose and strict markers (70), resolution P1 to P7 (45), git classifier G0 to G4 plus `update-ref`, `remote`, `config`, `worktree` read forms and the allowlist (70), gh H1 to H5 (55), escape rules with the `orca` pair allowlist (35), tamper (25), MCP and Skill normalisation (30), decision with precedence (30), and dispatch, trap and helpers (30). Reaching about 450 is possible only if messages are a data table printed by one function and the `orca` pairs are one string.

Costliest mechanisms, in order of cost against what they return:

1. The 18 message texts plus LL-STATE and LL-TEXT notes (required by AC-7; keep, but keep as data).
2. Binding: strict and loose marker, BOM and whitespace handling, degraded bind, nonce consumption in a bound session (about 70 lines). The degraded bind is the part to question.
3. The git classifier with dashed built-ins, option skipping, `update-ref` rules and the three read-only forms. Fixes F-1, F-6, F-7 add about 10 lines.
4. The 11-pair `orca` allowlist and the `claude` flag list.
5. Three-tier MCP rule (Change 13). One rule would do: block every matched MCP tool whose name does not start with a read prefix.

The fixes in this review are small (a regex, a sed line, a token, a sentence of rule text each) and keep the plan one script.

## 7. Minor findings

- **m-1** Change 6 P5: `gsub` on a missing field fails in jq 1.7 (`null cannot be matched`), which would print LL-BROKEN on every Edit, Skill and Agent call. Say `(.tool_input.skill // .tool_input.name // "" | tostring | gsub(...))` for each field. T-GRID rows 2 to 4 would catch it.
- **m-2** Change 5 B4: the field order and transport for `session_id`, `agent_id` and the multi-line `prompt` are not stated (P5 has them; B4 does not). Say: two fields one per line, `prompt` last, read with `read -r -d ''`.
- **m-3** Change 6 P3: "collect every value V" has no stated method, and Change 22 item 3 does not allow a subprocess for it. State a pure-bash loop (`[[ =~ ]]` then strip the matched prefix) and cap the loop at the number of matches that fit in a 1 MB payload (the first review measured 16 ms).
- **m-4** Change 11 item 3: "Destination `HEAD` or `@`" has a dead branch, `@` cannot match the character class, so `x:@` is PUSHFORM by form, not by destination. Row 15 and T-PSH-2 list `x:@` correctly; only item 3 needs the word removed.
- **m-5** NM2 is quadratic on lines ending in `\`: a 64 KB command of `\` and newline lines took 0.79 s here. Add one governed stress case to T-SPD-5 (continuation lines at the cap) so a slow CI host does not cross the 5 s timeout and fail open (V8).
- **m-6** The ship gate (Change 7 item 5, Change 29) names only OB-H1 item 1. AC-3's default depends on item 5 (the Monitor and background-subagent prompt shape) as well. Add "item 5 must show a wrapped prompt, otherwise O-17 flips to block" to the same gate.
- **m-7** Tamper by a relative path: `cd ~/.claude/skills && : > ../hooks/x.sh` and `.../state/../settings.json` name no token and no word ends in `.claude`. The token `hooks/launch-level-guard` (INV-009) does not match the repository source path `hooks/scripts/launch-level-guard.sh`, so it could be restored at no cost. At least name the case in R3 (included in F-4's text).
- **m-8** Row 36 wording (see 4.2).
- **m-9** Add to O-10 and the AC-2 limit: `git merge --abort` is MERGE and is blocked too, so after a blocked sync merge the skill has nothing to abort.
- **m-10** Change 1 id families list "G1 to G4" but Change 10 defines G0 (and F-7 adds G1b); list "G0 to G4".
- **m-11** T-PSH-8 and R11 mention only `remote.origin.push`; say once that `push.default` and `branch.*.merge` do not matter for a push with an explicit refspec (I checked: they apply only when no refspec is given), so the reader does not wonder.
- **m-12** M-5b of the first review (a quoted strict marker with no record blocks the prompt) was skipped with a reason. Keep it as a named owner decision (O-20) so the choice is visible, since it blocks people who quote an example marker, which AC-4 says should stay unaffected.

## 8. Required fixes (order)

1. F-6 NM4 and F-1 NM2 and G4 (the segment text must show every word before any rule runs).
2. F-2 push regex.
3. F-7 G1b.
4. F-3 H2 item 3.
5. F-4 tamper token and the R3/O-16/INV-037 sentence.
6. F-5 R1/O-7 and row 33.
7. F-8 "Departs from (2)".
8. Add tests T-GIT-14, T-GIT-15, T-PSH-12 additions, T-GH-11, T-NRM-7, T-TAM-1 additions; then the minors.

None of the fixes changes the design. After they are applied I expect a third pass to be short.

## Self-Audit

What I actively checked: I read refactor-plan.md in full (all 34 changes, coverage index, A-001 to A-008, probe table, O-1 to O-19, not-made table, risk summary, revision log), plan-review.md in full, the first 100 lines of invariant-probe.md (consensus and finding table) and its resolution list, and the issue's AC-1 to AC-8. I read `sc-pr-submit-protocol/SKILL.md` (the relevant waves) and every `git` and `gh` command in its `refs/` files, and the script names. I ran: the plan's NM2 to NM6 pipeline on 14 commands, its push ERE on about 55 strings, its H2 regex on 30 words, the session-id, marker, approval and PreToolUse matcher rules, 17 push destinations with `git push --dry-run`, and five real-git attacks against local bare repositories (rebase -x with alias, `--all` and `--mirror`, `A=">" git push`, `git -c "x.y=a status" push`, plus a stub `gh` for the flag attacks). I timed NM2 on 64 KB inputs and tested three proposed fixes (NM2 odd-backslash join, NM4 operator-only removal, the G1b ERE, the new push ERE) before writing them as replacements.

What I did not check: I did not read the three round-2 advocate files, the round-1 files, the variants, `diff-analysis.md` or `base-selection.md` in detail, so a mismatch inside those documents could have escaped me. I did not run `gh` against GitHub; the gh flag behaviour rests on the stub receiving the arguments the shell built and on gh's flag library accepting the forms (taken from the first review's reading of `gh api --help`). I did not run BSD `sed`. I did not verify any Claude Code harness behaviour (V1 to V14, U1 to U20) and treat them as the plan states them. I did not test every orca, claude, MCP and tamper-word case, only the tamper tokens and the MCP matcher. I did not implement the full classifier, so the claim that "no other path reaches `main`" is not made: I only claim the eight holes above are real and that the replacements close the cases I ran. Other holes of the same family (an exec-carrying option on an allowlisted git subcommand, for example `git grep -O`) are covered by the G4 replacement for the alias case but I did not run `git grep -O` itself.

Cleanup: the `/tmp` working directory (two bare repos, clones, the stub `gh`, helper scripts) is removed at the end of this run.
