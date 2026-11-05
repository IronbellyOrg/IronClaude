---
round: 2
advocate: 2
variant: variant-2-sonnet-refactorer.md
status: design debate, nothing implemented
---

# Round 2, Advocate 2: Variant 2 (sonnet:refactorer), rebuttals

Of the 14 criticisms below I concede 9 in full and 2 in part (rows 11 and 12), and rebut 3 (rows 10, 13, 14). I also report three defects in my own variant that nobody raised (the matcher, the tamper scope, `git -c alias.`). The final design is still Variant 2's flat script and one-word state files, with these repairs. Steelman of the attack: a guard that fails silently is worse than a bigger guard. A hook that frees the launched agent when one file is missing, or never sees Monitor, protects nobody when it matters. I apply that test to every row below.

## 1. Response to criticisms

| # | Criticism (who) | Answer |
|---|---|---|
| 1 | A lost, stale or used nonce leaves the agent ungoverned (X-001; A1, A3) | **Conceded.** Rule: the first `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere in an unbound session's prompt, with `pending/<nonce>` present, is moved by `mv`. A marker at the very start with no pending file writes `worktree` (with `set -C`, so it cannot overwrite). Later markers are ignored. No age check. A pasted `<nonce>` template never matches 32 hex characters. Residual: a person pasting a real, used launch prompt as a first prompt is governed at `worktree`, released by `rm`. |
| 2 | `git pull` allowed (X-008; A1, A3) | **Conceded.** `pull` is M2 at every level. Checked: `git pull` appears once in `src/superclaude`, in an operator-facing message (`git pull --ff-only`, `sc-pr-submit-protocol/SKILL.md:275`), and no agent step runs it. The project rule is fetch then rebase. So the block costs no framework flow. Message: "use `git fetch`, then `git rebase`". |
| 3 | Monitor, Workflow, RemoteTrigger, MCP not matched (C-012, C-013; A1, A3) | **Conceded.** Monitor in this harness takes `command` (or `ws`, which has no shell), so its `command` is scanned like Bash. Workflow and RemoteTrigger join Cron and Schedule as E3: their internals are unknown, and one matcher word is the fewest-edge-case answer. MCP: merge names only (section 2). |
| 4 | Speed plan loose (C-017; A1, A3) | **Conceded.** Adopt T-SPD-3: 100 runs, ordinary median at most 1.5 times `block-bare-python.sh` in the same run, plus p95 limits. The helper `time.monotonic()` already exists in `test_block_bare_python.py:37`. |
| 5 | Option skip list too short (C-007; A1) | **Conceded, and it is worse.** I ran `git -c alias.ci=commit ci --allow-empty -m x` in a temporary repo: it made a commit. My scanner skips the `-c` value, reads `ci` as the subcommand and allows it. Fix: skip values of `-C -c --git-dir --work-tree --namespace --config-env`, and treat any token starting `alias.` in a git segment as tamper (T1). |
| 6 | Push regex blocks `feature/main` and a commit message containing `main` (A1 N-5) | **Conceded, verified.** I ran my regex: it matched `git push origin feature/main` and `git commit -m 'move main menu'; git push origin x`. Replaced by the destination rule (section 2). |
| 7 | F1 blocks every matched call on bad state (X-003; A1) | **Conceded.** An unreadable or unknown word reads as `worktree`, and the first block message adds "launch record unreadable". Approval is a separate file, so it survives. |
| 8 | "Default-deny" had no mechanism (C-015; A1) | **Conceded and verified.** In a shell, a `set -u` abort inside a function ended with exit 2 under `trap 'rc=$?; [ $rc -ne 0 ] && [ $rc -ne 2 ] && exit 2' EXIT`. Install the trap only after the session is known governed, so ordinary sessions never meet it. |
| 9 | `claude` flag list contains `-r`, which over-blocks `grep claude -r docs/` (A1) | **Conceded.** Drop `-r`; keep `--resume`. Also compare the basename (`${w##*/}`) for `claude`, `gh`, `orca`, `ccsession`, so `/usr/local/bin/claude -p` is covered. My text only did this for `git`. |
| 10 | Cutting UserPromptExpansion hangs typed approval on one reading of V6 (C-005; A3, A1) | **Rebutted with documentation.** The hooks page says UserPromptSubmit receives a typed skill command "as you typed it rather than the expanded skill content", and sends you to UserPromptExpansion only to match on name or arguments. The documented UserPromptExpansion example shows `command_name: "example-skill"` with a separate `command_source`, so whether `sc:implement` arrives as `sc:implement` or `implement` is unknown (U9). Submit-side prefix matching needs no such parse. Conditional buy-back: if OB-H1 shows the typed line does not reach UserPromptSubmit, add the event. Mid-turn queuing is "not stated" for both events, so `approved` stays. |
| 11 | No repo check on `gh pr create` (C-010; A1, A3) | **Partly conceded.** Require an explicit `--repo`, `--repo=` or `-R` word on `gh pr create` at submit, with no name compared. That stops the recorded incident (a bare `gh pr create` going to the parent repo). A literal name check would block the skill's own command form: `sc-pr-submit-protocol/SKILL.md:274` writes `gh pr create --repo "$REPO"`. |
| 12 | Messages lack the issue number (C-018; A1) | **Rebutted in part.** AC-7 needs what, why, next step. Add the level name to the header at no state cost. An issue number needs a second field and validation, so no. |
| 13 | Binding should cross-check `cwd` (U-008; A3) | **Rebutted.** The nonce is single use, and with a degraded bind a failed check no longer frees anyone. The check adds real-path and symlink edge cases and protects only against a copied marker landing in another session first. Cut. |
| 14 | One-word state cannot carry `repo` or `issue` (C-003; A1) | **Rebutted.** With row 11 as written, nothing needs them. |

## 2. Updated assessment

**Take from Variant 1:** degraded bind; `pull`; the `alias.` rule; Monitor scanning; Workflow and RemoteTrigger blocked; the fuller git option list; remote isolation blocked; tamper tokens `.gitconfig` and `.git/config` on edit paths.

**Take from Variant 3:** T-SPD-3 with p95; harmless-first order of work (T-ISO-1 and T-FO pass before any rule); literal payload fixtures; the pinned over-match test; OB-H2 mandatory before any real governed launch.

**Take from Advocate 1's N-2, with my edits (this replaces my regex and the `symbolic-ref` call).** At submit a push is allowed only if: the first non-option word is `origin`; none of `--all`, `--mirror`, `--repo`, `--receive-pack`, `--exec` appears; the segment has no `$` or backtick; at least one refspec follows; and each refspec destination (leading `+` removed, text after the last `:`, `refs/heads/` removed) is not `master`, `main`, `HEAD`, `@` or empty. Skip the word after `-o` or `--push-option`. No subprocess, no `cwd`, no `-C`, no `push.default` gap. I do not ban `--force`: no acceptance criterion names it, and pr-submit already forbids it. Cost: `git push origin HEAD` and a bare `git push` are blocked at submit with "push the branch by name". I accept that, and OB-H3 will show how often the agent hits it.

**Merged matcher (anchored, see E1):** `^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*merge`. In the script, unknown tool names that reach the hook exit 0 on an explicit allow path; MCP names whose last segment starts with `list_`, `get_`, `search_` or `read_` are allowed.

**Tamper scope (E2):** governed sessions only; tokens are the store path built from two parts, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `alias.` in a git segment; checked on the decoded Bash or Monitor `command` and on Edit, Write and NotebookEdit path fields, never on file content, Agent prompts or Skill arguments. Decoding makes my `\/` double test unnecessary (N5 closes).

**My cuts that stand:** source-edit gating at `worktree`; approval expiry or plan binding; locking and clean-up; HMAC and mode bits; the always-on `cwd` fallback (U1 stays a ship gate, reserve fallback needs `agent_id`); `--force` rules; `gh pr ready` (no use in `src/superclaude`, grep count 0; I only add it to the below-submit `gh` list with `create`).

**Variant 1 rules that cost more edge cases than they save:** a self-reading policy block with a grid test (the test then checks the script against itself; an independent table in the test file is a better oracle, and a fifth level is not asked for); literal repo-name matching (row 11); MCP substring rules for `commit` and `push` (they would block read-only `list_commits` and `get_commit`); the 30-minute age rule and prune (Advocate 1 has cut them).

## 3. New evidence

- **E1, my matcher is wrong.** The hooks page: a matcher containing any character beyond letters, digits, `_`, `-`, space, `,` and `|` is a JavaScript regular expression, "unanchored"; "`Edit.*` matches both `Edit` and `NotebookEdit`". My matcher contains `.` and `*`, so it becomes an unanchored regex: `Task` matches `TaskCreate`, `TaskUpdate`, `TaskList`, and so on, spawning the script on all of them. The existing `Edit|Write` and `Bash` entries in `hooks.json` are exact lists; only the auggie entry is a regex. Advocate 1's proposed merged matcher has the same flaw. Fix: `^(...)$` as above.
- **E2, my tamper rule over-blocks.** I wrote "any matched call whose raw input contains a guard-surface token". Raw input of Write includes file content, so writing a plan or doc that mentions `.claude/hooks` is blocked. The project `CLAUDE.md` has 6 such lines. Variant 1 checks paths for Edit and Write; that is right. Fixed above.
- **E3, documentation.** Lifecycle order is UserPromptSubmit, then UserPromptExpansion. `hook_event_name` appears in the documented UserPromptExpansion payload, so event dispatch can use it.
- **E4, static checks.** `sc-implement-protocol` has no `git commit|push|merge|pull`. Its Q0 snapshot (`SKILL.md:110-115`) uses `read-tree`, a private-index `add`, `write-tree`, `stash create` and `update-ref`; none is gated, which settles N4 statically (U10 still needs OB-H3). Advocate 1's N-3 holds: pr-submit's Tier 2 sync runs `git merge --no-commit --no-ff` (`refs/conflict-mechanical.md:76`), and AC-6 reads "No level permits a merge". Keep M2 and add a conflicting PR to OB-H3. Say so in the M2 text: "a person syncs the branch".
- **E5, tool keys.** In this session's tool definitions: Skill takes `skill`, Monitor takes `command` or `ws`, Agent takes `isolation` with value `remote`, Edit and Write take `file_path`, NotebookEdit takes `notebook_path`. This lowers U2, U11 and U13, but a hook payload was not observed, so OB-H1 still decides.
- **E6, still open after checking.** `git -C "/path with space" push` is misread (the sweep leaves `with` as the subcommand); `g""it` and `$GIT` stay uncovered. Worktree paths here have no spaces. Residual, named test `test_known_gaps`. Implementation traps worth a test each: a `\` placed inside the sweep's character class keeps backslashes (I hit this), so `\git` needs its own case; and multi-line commands must be read with `jq -r`, not `@tsv`, which turns a newline into a literal `\n`.
- UNVERIFIED: what `git push --repo`, `--receive-pack` and `--exec` do (taken from Advocate 1, not re-checked); the real MCP tool names on any host.

## 4. Changed answers on A-001 to A-008

- **A-007 changed.** Marker anywhere binds only when a pending record exists; with none, only a marker at the very start binds (degraded).
- **A-008 changed to moot.** Under the destination rule no push decision reads `cwd`. It is used only by the reserve fallback, which stays off.
- **A-003 made concrete (verdict unchanged).** The claim script refuses to launch unless `~/.claude/hooks/launch-level-guard.sh` is executable and `~/.claude/settings.json` registers it (`install_hooks.py` merges registrations there, per its docstring). That the Orca-launched session reads that file is UNVERIFIED; OB-H2 decides.
- A-001, A-002, A-004, A-005, A-006 unchanged.

## 5. Per-point verdicts, final form

| Point | Superior approach | Confidence % | Changed since Round 1? | One-sentence evidence |
|---|---|---|---|---|
| S-001 | Variant 1 | 50 | no | Front matter and a title cost nothing and identify the file. |
| S-002 | Merge | 60 | no | Variant 1's numbered residuals plus Variant 2's "what each cut leaves open" column. |
| S-003 | Merge | 70 | no | Variant 3's literal commands as rows, kept as the test's own table so it is an independent oracle. |
| S-004 | Variant 2 | 60 | no | Flat script; Advocate 1 dropped `--classify` and the ERR trap, and a policy block that the test reads back checks the script against itself. |
| S-005 | Merge | 75 | no | Variant 1's U9 to U13, my N1 to N5 and Variant 3's Test column each found unknowns the others missed. |
| S-006 | Merge | 55 | yes | Variant 2's families and Blocked/Why/You can lines, with the level name in the header. |
| C-001 | Merge | 80 | no | Rule: marker anywhere plus pending file moves by `mv`; marker at the start with no file writes `worktree` under `set -C`; later markers ignored; no age check. |
| C-002 | Variant 2 | 75 | no | U1 is a ship gate; the reserve fallback stays off and needs `agent_id` (X-004). |
| C-003 | Variant 2 | 65 | no | One word per file needs no JSON parse and no read-modify-write; nothing needs `repo` once row 11 is as written. |
| C-004 | Merge | 75 | yes | Rule: governed only; tokens store (two-part), `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `alias.`; decoded command and path fields only, never content or Agent prompts. |
| C-005 | Variant 2 | 60 | no | Docs say UserPromptSubmit gets the typed slash line as typed; UserPromptExpansion's `command_name` form is unknown; add it only if OB-H1 fails. |
| C-006 | Variant 2 | 70 | no | `touch` of `.ok` only at `worktree`, ignoring prompts with `agent_id`, never rewrites the level file. |
| C-007 | Merge | 80 | no | Rule: character sweep, basename compare for git, gh, claude, orca, ccsession, skip values of `-C -c --git-dir --work-tree --namespace --config-env`; Variant 3's wrapper list is a sub-parser. |
| C-008 | Variant 1 | 75 | no | `pull` is a merge path, and `-c alias.ci=commit ci` made a commit in my test. |
| C-009 | Merge | 75 | yes | Destination rule (section 2): origin only, named branch, none of master, main, HEAD, @, no `--all`, `--mirror`, `$`; no subprocess. |
| C-010 | Merge | 65 | no | Block `gh pr merge`, any `gh api` path ending `/merge`, and `gh <group> create` or `ready` below submit; at submit require an explicit `--repo`/`-R` word, no name compared. |
| C-011 | Merge | 70 | yes | Anchored matcher `^(Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|Cron[A-Za-z]*\|Schedule[A-Za-z]*)$\|^mcp__.*merge`; an unanchored one fires on `TaskCreate`. |
| C-012 | Variant 1 | 70 | no | Monitor `command` scanned like Bash; Workflow, RemoteTrigger, Cron, Schedule blocked. |
| C-013 | Merge | 55 | no | Rule: only MCP names containing `merge`, minus `list_`, `get_`, `search_`, `read_`; `commit` and `push` substrings would block read-only calls. |
| C-014 | Variant 2 | 65 | no | A fixed `orca` subcommand list and a `claude` flag list without `-r` block fewer innocent commands; remote isolation blocked via `isolation`. |
| C-015 | Merge | 85 | no | Rule: last line `exit 2`, allow only on a named path, EXIT trap (installed after governed) maps any code but 0 and 2 to 2; verified in a shell. |
| C-016 | Variant 2 | 70 | no | `compgen -G`, then `jq` (the repo's convention); regex only when `jq` is missing, and then exit 0 only if no matched id is bound. |
| C-017 | Variant 3 | 70 | no | Relative guard against `block-bare-python.sh` over 100 runs with p95, plus Variant 1's absolute limits as a second check. |
| C-018 | Merge | 60 | yes | Variant 1's id coverage in Variant 2's three-line wording, level in the header, no issue number. |
| C-019 | Merge | 70 | no | Cases from the table, literal payloads, "every id has text" test, pinned over-match, no unregistered `manual` marker. |
| C-020 | Merge | 65 | yes | OB-H1 first (Variant 2), OB-H2 mandatory before use (Variant 3), a conflicting-PR case in OB-H3 (Advocate 1's N-3). |
| X-001 | Variant 1 | 85 | no | Only a degraded bind keeps a lost or used nonce from freeing the agent. |
| X-002 | Variant 2 | 70 | no | Governed calls block when `jq` is missing and the claim script refuses to launch without it; V8 forces nothing. |
| X-003 | Variant 1 | 70 | no | Degrading to `worktree` keeps planning and approval working. |
| X-004 | Variant 2 | 90 | no | A person's own subagent sends `agent_id` with an unbound id, so an always-on `cwd` fallback governs that person. |
| X-005 | Variant 2 | 85 | no | Governed-only scope; Variant 3 contradicts its own T-ISO-1. |
| X-006 | Merge | 85 | yes | V11 makes `disableAllHooks` real; Variant 1's path check on Edit and Write is more precise than my raw-input check, which also blocks file content. |
| X-007 | Merge | 75 | yes | The destination rule blocks `HEAD`, bare push, `--all`, `--mirror`, `+main` with no subprocess and no `cwd`. |
| X-008 | Variant 1 | 75 | no | `pull` can create a merge commit and appears in no agent flow (one operator message). |
| X-009 | Variant 1 | 90 | no | The worktree `.git` file points to the main checkout's git directory. |
| X-010 | Variant 2 | 90 | no | `_FRESHNESS_SCRIPTS` is defined only at `install_hooks.py:42`; the Makefile imports it. |
