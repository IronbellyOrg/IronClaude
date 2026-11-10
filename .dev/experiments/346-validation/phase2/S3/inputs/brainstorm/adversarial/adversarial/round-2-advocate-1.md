---
round: 2
advocate: 1
variant: variant-1-opus-architect.md
status: design debate, nothing implemented
---

# Round 2, Advocate 1: Variant 1 (opus:architect), rebuttals

Variant 1 stays the right base for the decision rules and the failure posture, and both other advocates now say so (Advocate 3: "The decision rules must come from V1's stricter table"). Round 2 is mostly about cutting Variant 1's excess. I concede nine of the criticisms in full, two in part, and rebut two. I also propose one new rule (push destinations must be named) that removes Variant 1's only subprocess.

## 1. Response to criticisms

Steelman first: Advocates 2 and 3 share one strong argument. Every line in a hook that runs on every tool call can be wrong, and the #357 hook shows how that cost grows. Each answer below applies that test.

| # | Criticism (who) | Answer |
|---|---|---|
| 1 | Too big: 12 classes, 13 ids, five layers, a test-only `--classify` mode (A2 weakness 1, A3 weakness 1) | **Partly conceded.** Cut `--classify` and the ERR trap (row 5). Keep the literal `CLASS LEVEL DECISION MSGID` block and a test that reads that block from the script and checks that every class has a row for every level. No other variant has a mechanism that stops a fifth level from shipping with a gap. The "layers" are about seven shell functions, not a framework. |
| 2 | The clock rules are inconsistent: approval expiry is rejected, but a 30-minute stale-record rule is added (A2 weakness 2) | **Conceded.** A nonce works once (`mv`), so the record's age adds nothing. Drop the age check and the O-9 prune. |
| 3 | The cost of "a marker always governs" is not counted: a pasted marker governs a person's session (A2 weakness 3, A3 weakness 2) | **Partly rebutted.** Adopting Variant 2's strict pattern `\[sc-launch:v1:([0-9a-f]{32})\]` means a pasted template with `<nonce>` never matches. The only marker in the repository today is that placeholder form, in the brainstorm files (grep for `sc-launch`). Only a real launch prompt pasted at the very start binds, at degraded `worktree`. I add this as residual R9. |
| 4 | Fast path 2 reads `session_id` from the raw JSON with a regex, so key order matters (A2 weakness 4) | **Conceded, with a sharper reason.** Inside a JSON string every `"` is escaped, so a command's text cannot forge the key. But a nested object key can: an MCP tool argument named `session_id` would match. Fix: use `jq` on the main path, as all six existing scripts do (for example `freshness-pre-edit.sh:18`). Use the regex only when `jq` is missing. In that case a call exits 0 only if none of the matched ids has a session file, which can only fail toward governing. |
| 5 | The ERR trap is not inherited by functions without `set -E` (A2 weakness 5) | **Conceded; checked in a shell.** With no `set -E`, `trap ERR` did not fire for `false` inside a function. An EXIT trap did turn a `set -u` abort inside a function into exit 2. The real gap is a command that fails without ending the script and falls through to ALLOW. Fix: use Variant 2's default-deny structure. The last line is `exit 2`, allowing takes an explicit `exit 0` on a named path, and an EXIT trap maps any other code to 2. Drop the ERR trap. |
| 6 | A `claude` word followed by any dash word over-blocks `grep claude -rn docs/` (A2 weakness 6) | **Conceded.** Variant 2's fixed flag list has the same fault, because it contains `-r`. Rule: `claude` or `ccsession*` followed by `-p`, `--print`, `--resume`, `--continue`, `--bare`, `--settings` or `--dangerously-skip-permissions`, without `-r`. |
| 7 | The `launch-level-guard` token blocks work on this very issue (A2 strength 4) | **Conceded.** Drop that token. The installed copy lives in `~/.claude/hooks/` (`install_hooks.py` line 4), which the `.claude/hooks` token already covers. Build the store name from two parts, as Variant 2 does. |
| 8 | With no matcher, every Read in every session starts the script (A2 strength 3) | **Conceded** (already conceded in Round 1). The merged matcher is in C-011 below. |
| 9 | The `command_name` form for UserPromptExpansion is unverified (A2 strength 2) | **Rebutted.** That event fires only for typed commands (V5). An unexpected form gives no approval and leaves the UserPromptSubmit route in place, so it can never approve the wrong thing. Cutting it ties typed approval to one reading of V6, which Advocate 2 conceded. |
| 10 | Approval is written at levels where it means nothing (A2 C-006) | **Conceded.** Write `.ok` only at `worktree`. Ignore any prompt payload that carries `agent_id` (N1). |
| 11 | The JSON record brings bad-JSON states (A2 C-003, A3 C-003) | **Partly conceded.** Store one line, `level repo issue`, read with `read -r`. It needs no `jq` and cannot be bad JSON. It still carries `repo` for LL-REPO, which must not be hard-coded, and `issue` for AC-7. An unknown level reads as `worktree` with an LL-STATE note. |
| 12 | With `jq` missing, the governed session is stuck, and reading `tool_name` without `jq` is fragile (A3 weakness 3) | **Rebutted, with one adjustment.** The merged matcher keeps Read, Grep and Glob from reaching the hook, so LL-BROKEN can block every call that does reach it without reading `tool_name`. Having no fix inside the session is deliberate: the guard fails closed. The claim script's `jq` check (Variant 2) makes the case rare. |
| 13 | O-5 states U7's answer as fact (A3 weakness 4) | **Conceded.** O-5 is open and OB-H3 decides it. |
| 14 | Medians over 30 runs, with no relative guard (A3 weakness 5) | **Conceded.** Adopt T-SPD-3: over 100 runs, the ordinary-path median is at most 1.5 times `block-bare-python.sh` measured in the same run, plus p95 limits. Keep Variant 1's absolute limits as a second check. |

Two earlier concessions stand: the Makefile has no `_FRESHNESS_SCRIPTS` line (X-010), and the reserve cwd fallback must require `agent_id` (X-004).

## 2. Updated assessment

**Adopt from Variant 2:** the default-deny structure, the strict 32-hex nonce, the `mv` bind with a match anywhere when a record exists, the one-line state file, `.ok` written only at `worktree`, ignoring `agent_id` on prompts, the two-part store name with `/` and `\/` tests, the claim-side `jq` check, `gh <group> create`, its character sweep (see new evidence N-1), and treating U1 as a ship gate.

**Adopt from Variant 3:** T-SPD-3 with p95 over 100 runs, the "harmless first" order of work (T-ISO-1 and T-FO before any rule), literal payload fixtures, a test that pins the known over-match, OB-H2 as mandatory before any real governed launch, and `gh pr ready` as never allowed.

**Cut or soften in Variant 1:** `--classify`, the ERR trap, the 30-minute rule, the O-9 prune, the `launch-level-guard` token, "any dash word" after `claude`, the regex-first fast path 2, JSON state, and the `symbolic-ref` subprocess (replaced by the rule in N-2).

## 3. New evidence (not in Round 1)

- **N-1, a gap in Variant 1's tokenizer.** Variant 1 splits words on whitespace and `' " $ [ ] , =`, not on `\`. So `\git push origin main` gives the word `\git`, whose basename is not `git`, and the push is missed. Variant 2's sweep (any character outside `[A-Za-z0-9._/=:@+~-]` becomes a space) catches it, and Variant 2 lists `\git` as covered. Adopt the sweep and keep Variant 1's longer list of git options to skip.
- **N-2, pushes must name their destination.** `/sc:pr-submit` at L3 already pushes `git push origin <target_sha>:<target_branch>`, "never the repo's default/protected branch, never a force push" (`sc-pr-submit-protocol/SKILL.md` line 282). Proposed rule: at `full --submit`, a push is allowed only when (1) the remote is `origin`; (2) none of `--all`, `--mirror`, `--repo`, `--receive-pack`, `--exec` or `--force` appears, and no refspec starts with `+` (`--force-with-lease` stays allowed, O-4); and (3) at least one refspec follows and every destination is a branch other than `master`, `main`, `HEAD` or `@`. The destination is the text after `:`, or the whole word, with `refs/heads/` removed. Anything else is blocked with "push the feature branch by name". This removes the `symbolic-ref` call and its 2-second case, and with them the `cwd`, `-C`, `cd` and `push.default=upstream` gaps. The meanings of `--repo` and `-o` come from git's push documentation; I did not re-check them in this session (UNVERIFIED). `-o` and `--push-option` take a value, which the rule must skip.
- **N-3, every variant's merge rule blocks `/sc:pr-submit`'s conflict sync.** At L3 it runs `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>` (`refs/conflict-mechanical.md` line 76). All three variants block that at `full --submit`. How `/sc:pr-submit` reacts to the block is UNVERIFIED. New owner decision O-10: keep the block (my recommendation, because only people merge), and add a conflicting PR to OB-H3.
- **N-4.** `/sc:pr-submit` runs `gh pr create --repo "$REPO"` (SKILL.md line 274). If the agent sets `REPO` by command substitution, no word equals the record's repo, so LL-REPO blocks. The message tells the agent to name the repo literally. Add a test for this case.
- **N-5.** I ran Variant 2's pattern `(^|[^A-Za-z0-9._-])(master|main)($|[^A-Za-z0-9._-])` through `grep -E`. It matched both `git push origin feature/main` and a chained commit message containing `main`, so both would be wrongly blocked.
- **N-6, partial evidence for U10.** `src/superclaude/skills/sc-implement-protocol/` contains no `git commit|push|merge|pull`, and `*implement*` Python under `src/superclaude` has no quoted `commit`, `push` or `merge` argument. This supports, but does not prove, that `/sc:implement` makes no commits today.

## 4. Changed answers on A-001 to A-008

Only **A-008** changes. In Round 1 I wanted push checks to resolve HEAD in the `-C` directory. Under N-2 no push decision reads `cwd` or HEAD. `cwd` is now used only by the reserve fallback, which stays off by default and needs `agent_id`. A-001 to A-007 are unchanged: the A-005 rejection stands, and the A-007 binding rule is the one in C-001 below.

## 5. Per-point verdicts, final form

| Point | Superior approach | Confidence % | Changed since Round 1? | One-sentence evidence |
|---|---|---|---|---|
| S-001 | Variant 1 | 55 | no | Front matter with `status: design only` records where the file came from at no cost. |
| S-002 | Merge | 65 | no | Variant 1's numbered R1 to R9 can be cited, and Variant 2's cut table prices each deletion. |
| S-003 | Merge | 70 | no | Variant 2's "the table is the test data", filled with Variant 3's literal commands and its over-match row. |
| S-004 | Merge | 65 | yes | Rule: one flat file in Variant 2's style, plus Variant 1's literal policy block and a test that reads it and checks the grid is complete; no `--classify`, no ERR trap. |
| S-005 | Merge | 75 | yes | Variant 1's U9 to U13, Variant 2's N1 to N5 and Variant 3's Test column each name unknowns the others missed. |
| S-006 | Merge | 60 | no | Variant 1's id coverage written in Variant 2's Blocked/Why/You can lines. |
| C-001 | Merge | 80 | no | Rule: the first `\[sc-launch:v1:([0-9a-f]{32})\]` anywhere in an unbound session's prompt `mv`s an existing record; a marker at the start with no record binds degraded `worktree`; no age check; later markers are ignored. |
| C-002 | Merge | 75 | no | U1 is a ship gate (Variant 2); the reserve fallback stays off and requires `agent_id` plus a `cwd` prefix match (X-004). |
| C-003 | Merge | 70 | yes | Rule: `sessions/<sid>` holds one line, `level repo issue`, read with `read -r`, and `<sid>.ok` holds approval, so there is no JSON parsing and no read-modify-write. |
| C-004 | Merge | 80 | no | Rule: governed sessions only; tokens are the store path (built from two parts), `.claude/settings`, `.claude/hooks`, `disableAllHooks`, plus `.gitconfig`/`.git/config` on edits and `git config alias.`, each tested in `/` and `\/` forms, with no `launch-level-guard` token. |
| C-005 | Merge | 75 | yes | Variant 1's two events with prefix stripping, plus Variant 2's rule to ignore `agent_id`; an unexpected `command_name` approves nothing. |
| C-006 | Variant 2 | 70 | no | `touch` of `.ok` only at `worktree` is atomic and never rewrites the file that holds the level. |
| C-007 | Merge | 75 | yes | Variant 1 misses `\git` (N-1); use Variant 2's sweep with Variant 1's option list (`-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`, `--config-env`). |
| C-008 | Variant 1 | 70 | no | `pull` can create a merge commit, and pushing only to `origin` is the CLAUDE.md fork rule. |
| C-009 | Merge | 75 | yes | Rule N-2: at submit every refspec must name a destination branch other than `master`/`main`/`HEAD`/`@`, with no `--all`/`--mirror`/`--repo`/`--force`/`+`; this matches pr-submit's own `<sha>:<branch>` push and needs no subprocess. |
| C-010 | Merge | 75 | no | Variant 1's LL-REPO read from the record, plus Variant 2's `gh <group> create` gate and Variant 3's `gh pr ready`, with a test for the `"$REPO"` case (N-4). |
| C-011 | Merge | 75 | no | Rule: PreToolUse matcher `Bash\|Skill\|Agent\|Task\|Edit\|Write\|NotebookEdit\|Monitor\|Workflow\|RemoteTrigger\|Cron.*\|Schedule.*\|mcp__.*(merge\|push\|commit\|create_pull_request).*`, in the style of `hooks.json` line 110. |
| C-012 | Variant 1 | 70 | no | V1 says Workflow fires PreToolUse; scanning Monitor like Bash closes a plain `git push` route. |
| C-013 | Merge | 70 | yes | Variant 1's name rule, placed in the matcher so that other MCP calls never start the script. |
| C-014 | Merge | 70 | yes | Variant 1's `orca` subcommand list and remote-isolation block, plus Variant 2's `claude` flag list without `-r`. |
| C-015 | Merge | 80 | no | Checked in a shell: ERR does not reach functions, but EXIT does; rule: default deny (last line `exit 2`) and an EXIT trap that maps anything other than 0 or 2 to 2. |
| C-016 | Merge | 70 | yes | `compgen -G` on an empty store, then `jq` for `session_id` (the repo's six-script convention); the regex only when `jq` is missing, and it exits 0 only if no matched id is bound. |
| C-017 | Merge | 75 | no | Variant 3's T-SPD-3 with p95 over 100 runs, plus Variant 1's absolute limits; the 2-second push case is gone under N-2. |
| C-018 | Merge | 65 | yes | Variant 1's header naming the issue and level ("an unknown issue" when degraded) over Variant 2's three-line body. |
| C-019 | Merge | 70 | no | Cases generated from the table with literal payloads, a grid-completeness test, a test that every id has text, and the pinned over-match. |
| C-020 | Merge | 65 | yes | Variant 2's OB-H1 to OB-H5 with OB-H1 first, Variant 3's OB-H2 required before any real governed launch, and a conflict-sync case in OB-H3 (N-3). |
| X-001 | Variant 1 | 85 | no | Only a degraded bind stops a lost or used-up nonce from leaving the launched agent ungoverned, and both other advocates concede it. |
| X-002 | Merge | 80 | no | Block governed calls when `jq` is missing and refuse to launch without it; V8 does not require failing open. |
| X-003 | Variant 1 | 70 | no | Falling back to `worktree` keeps `git status` and plan edits working, and the separate `.ok` file keeps approval. |
| X-004 | Variant 2 | 85 | no | A person's own subagent sends `agent_id` with an unbound id, so any always-on `cwd` fallback governs that person. |
| X-005 | Merge | 80 | yes | Variants 1 and 2 both scope tamper rules to governed sessions; the merged token set and two-part name are in C-004. |
| X-006 | Merge | 85 | no | V11 makes `disableAllHooks` a real route, and Variants 1 and 2 both block settings edits. |
| X-007 | Merge | 80 | yes | Rule N-2 blocks `HEAD`, a bare push, `--all`, `--mirror` and `+main` without reading HEAD, which Variant 3's word list and Variant 1's `symbolic-ref` each handled only in part. |
| X-008 | Variant 1 | 65 | no | A pull can create a merge commit; N-3 shows that the merge rule also stops pr-submit's sync merge, which is left to owner decision O-10. |
| X-009 | Variant 1 | 85 | no | This worktree's `.git` file points to the main checkout's common git directory, where hooks live. |
| X-010 | Variant 2 | 90 | no | `_FRESHNESS_SCRIPTS` is defined only in `install_hooks.py` (line 42), and the Makefile imports it. |
