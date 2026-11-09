# Round 1, Advocate 1: Variant 1 (opus:architect)

## Position summary

Variant 1 is the right base because it is the only design that keeps a launched agent governed when the launch record is lost, stale or stolen (U-001, X-001), blocks the settings-edit route that switches the hook off (X-006), and closes the master/main push routes through HEAD, `--all` and `--mirror` (X-007). Its layered script (classifiers, one policy block, one message block) makes the next level, tool or action a data row plus a test row. It should absorb four specific improvements from Variants 2 and 3, listed under Concessions.

## Steelman of Variant 2

Variant 2's strongest argument is that every line of a guard is a line that can be wrong, and that the #357 awk hook (300 lines, three review rounds, nine ceilings, `codebase-context.md` section 2) proves it. So it cuts to about 150 lines, two events, one-word state files, and a narrow PreToolUse matcher (`Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Cron.*|Schedule.*`), and it writes down exactly what each cut leaves open (its section 2 table). It gets several things right that Variant 1 should take: the store name is assembled from two parts so the guard's own source does not trip its tamper rule, tamper tokens are tested in both `/` and `\/` forms (U-005); approval prompts carrying `agent_id` are ignored (U-006, N1); the claim script refuses to launch without `jq` (U-007); `gh <group> create` is gated, not only `gh pr create`; and U1 is treated as a ship gate, not a design branch. It is also right on the repository fact in X-010: `_FRESHNESS_SCRIPTS` lives only in `src/superclaude/cli/install_hooks.py` (line 42), and the Makefile only imports it (Makefile line 309).

## Steelman of Variant 3

Variant 3's strongest argument is that a guard nobody can prove is a guard nobody can trust, so every rule is written as a literal JSON payload with an expected exit code and message id. Its order of work proves the hook harmless first (T-ISO-1 and T-FO before any governing rule), which is exactly the right fear for a hook that runs on every tool call on every machine. Its relative speed guard (ordinary median at most 1.5 times `block-bare-python.sh` in the same run, U-009) is the best answer to CI noise of the three. Its binding cross-check of `worktree_real_path` against `cwd` (U-008) blocks a replayed marker from another directory. It pins the documented over-match (`echo "git commit"`) as a blocked test so a change is deliberate, and it names U8 as "the one item that can silently void the design".

## Strengths claimed

1. **A marker always governs (U-001, X-001).** Variant 1 section 4 step 4: if the record is "absent, unreadable, over 30 minutes old or of unknown version, the hook still creates the session file, with `degraded: true` and level `worktree`." Variant 2 binds only "if `pending/<nonce>` exists" and admits "A session never bound looks like an ordinary one"; Variant 3 says "Any mismatch: no binding, exit 0." Under Variants 2 and 3 a lost pending file, a race, a clock-skewed claim, or an agent that reads and consumes its own nonce leaves the launched agent with no limits at all. The marker exists only in claim-launched prompts, so the false-positive cost of governing on the marker alone is a person who deliberately types a marker.

2. **Settings and hook tamper blocked (X-006).** Variant 1 section 5 blocks Edit/Write on `.claude/settings*` and `.claude/hooks/` and the Bash token `disableAllHooks`. V11 (VERIFIED) says `disableAllHooks` switches non-managed hooks off. Variant 3 protects only the store path and claims the settings route "reduce[s] to the script-file residual", which the diff analysis shows is false. Variant 1 also adds `.gitconfig`, `.git/config` and `git config alias.` (U-003), which Variant 2 lists as not covered.

3. **Protected-push detection is the most precise (X-007, C-009).** Variant 1 section 8 step 4 checks words after `push` (`master`, `main`, `--all`, `--mirror`, `:main`, `refs/heads/main` suffixes) and runs `symbolic-ref` only when no branch word follows; failure or detached HEAD blocks. Variant 3 allows `git push origin HEAD` and `--all` at FS, breaking AC-6. Variant 2 catches the same cases but with a whole-command regex that also fires on `git push origin feature/main` (`/` is not in its excluded character class `[^A-Za-z0-9._-]`) and on a chained commit message containing the word `main`, so it blocks legitimate submit-level pushes.

4. **The tokenizer covers more git option forms (C-007).** Variant 1 skips the value after `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`, `--config-env`. Variant 2 skips only `-C` and `-c`, so `git --git-dir x push` reads `x` as the subcommand and misses the push. Variant 3 relies on a named wrapper list; any wrapper not on it (for example `stdbuf` or `flock`) is a gap, while Variant 1 checks every word with basename `git` regardless of position.

5. **Repo and remote checks without hard-coding (U-003, C-010).** LL-REPO compares against the record's `repo`; Variant 3 hard-codes `IronbellyOrg/IronClaude` in a hook that `superclaude install` copies to `~/.claude/hooks/` and runs in other projects, where that repo name is wrong; reading it from the record keeps the hook project-neutral. LL-REMOTE enforces "origin only", which is the fork rule in the project CLAUDE.md. Variant 2 has no repo check at all (its O-3 default is no), so at FS a `gh pr create` with no `--repo` can land on the upstream parent, the exact incident the CLAUDE.md fork rule records.

6. **Indirect routes covered (U-004, C-012, C-013).** V1 (VERIFIED) says PreToolUse fires for MCP tools and `Workflow`. Variant 1 blocks MCP names containing `merge` at every level and `push`, `commit`, `create_pull_request` below submit; any word ending `/merge` catches `curl` to the GitHub API; Monitor commands are scanned as Bash. Variants 2 and 3 leave a GitHub MCP `merge_pull_request` call open, which is a direct AC-6 miss.

7. **Corrupt state degrades instead of freezing (X-003).** Variant 1 falls to `worktree` with an LL-STATE note; approval is a separate file, so it survives a corrupt record. Variant 2 blocks every matched call, including `git status` and plan edits, which stops the agent from even writing the plan. Variant 3 drops an existing approval because approval lives inside the same JSON it treats as corrupt.

8. **Extension scaffolding (S-004, U-002).** A closed action-class list, one `CLASS LEVEL DECISION MSGID` block, a message block, and tests asserting every class has a row for every level and every id has text. Adding `sc:task` to IMPL (O-8) is one row. Versioned record and marker (`v: 1`, `sc-launch:v1`) let v2 sit beside v1; an unknown version fails closed. `--classify` lets classifier tests run apart from policy tests and changes no decision because the harness passes no arguments.

9. **Cheapest fast path (C-016).** Fast path 1 is a `compgen -G` on an empty store with no `jq`; fast path 2 reads `session_id` with a bash regex. Variant 3 runs `jq` on every call in every session. `block-bare-python.sh` shows the cost profile Variant 1 matches: no `jq` work before the cheap exits.

10. **Approval routes cover both unknowns (C-005).** UserPromptExpansion is the only harness signal V5 names for typed commands; UserPromptSubmit first-line `/sc:implement` covers the mid-turn case (U5). Stripping `/` and `sc:` tolerates U9. Variant 2 drops UserPromptExpansion entirely, so it depends on the V6 reading being right; Variant 3 has no slash route on UserPromptSubmit.

## Weaknesses identified in Variants 2 and 3

1. **Variant 3's always-on cwd fallback governs a person's own subagents (X-004).** Its rule 2 claims "top-level sessions do not" carry `agent_id` (V4), but a person's own session in the same worktree that spawns a subagent sends `agent_id` with an unbound `session_id`. That breaks AC-4.
2. **Variant 3 contradicts itself on the tamper rule (X-005).** "Blocked in every session" against "ordinary sessions ... are never blocked" and T-ISO-1. It would also block a person releasing a session from their own Claude session.
3. **Variant 3 fails open in a governed session (X-002, C-015).** "`jq` missing or stdin not JSON: exit 0 everywhere (V8...)". V8 does not force this; a script can test `command -v jq` and exit 2, as `block-bare-python.sh` line 67 already tests (it chooses exit 0 because it is not a governance hook).
4. **Variant 3's repository claims are wrong (X-009, X-010).** Git hooks for this linked worktree live in the main checkout's common dir, not in the worktree; `@pytest.mark.manual` is not registered and `pyproject.toml` sets `--strict-markers` (line 114), so its placeholders fail collection; `session-init.sh` has no `state` reference.
5. **Variant 3 blocks every `orca` command (C-014),** including read-only ones such as `orca worktree current`, and allows every Agent spawn including remote isolation.
6. **Variant 2 lets a missing record release the agent (X-001)** and allows `git pull` at every level (X-008), which can create a merge commit.
7. **Variant 2's narrow matcher leaves MCP, Monitor, Workflow and RemoteTrigger unmatched (C-011, C-012)** with no repo check at submit (C-010).
8. **Variant 2's F1 blocks every matched call on bad state (X-003),** which is the opposite of "fewest unwanted behaviour": a corrupt file stops planning, not only gated actions.

## Concessions

1. **Makefile claim is wrong (X-010).** Variant 1 section 3 says a line is added to the Makefile `_FRESHNESS_SCRIPTS`; there is none. Only `install_hooks.py` changes.
2. **The cwd fallback as written is too broad (X-004).** Variant 1 section 4 matches "an unbound call whose `cwd` is inside a bound session's `worktree` (or a pending record under 30 minutes old)" with no `agent_id` condition. If switched on, that governs a person's own top-level session, worse than Variant 3's rule 2. Fix: require `agent_id`, keep it off, and treat U1 as a ship gate as Variant 2 does.
3. **Push checks have gaps.** `git push origin HEAD` while on `main` passes if `HEAD` counts as a branch word; `+main` (forced refspec) does not equal `main`; a bare `git push` with `push.default=upstream` from a feature branch tracking `origin/main` resolves to a feature branch name. Fix: treat `HEAD` and `@` as no branch word, strip a leading `+`, and for bare pushes also read `@{push}` via `git rev-parse --abbrev-ref @{push}`. Variant 2 shares the upstream gap.
4. **Starts-with marker matching is fragile (A-007).** If Orca prepends a preamble (U7), starts-with misses. Variant 2's search anywhere is more robust, but combined with "marker always governs" it would govern a person who pastes a log. Merge rule: marker anywhere plus a valid record binds normally; marker with no record binds degraded only at the start of the prompt.
5. **O-5 overreaches.** It asserts U7's answer; the WORKER-CONTRACT reading holds only if no preamble is sent, which is UNVERIFIED.
6. **No matcher on PreToolUse costs a process spawn on every Read in every session.** Merge: a matcher listing the gated tools plus `mcp__.*|Monitor|Workflow|RemoteTrigger`, excluding Read, Grep and Glob.
7. **Take from Variant 2:** two-part store name and `\/` token tests, `agent_id` prompts ignored, claim-side `jq` refusal, `gh <group> create`. **Take from Variant 3:** relative speed guard, harmless-first order, pinned over-match test, literal payload fixtures.
8. **Degraded messages** cannot name an issue number; the header must fall back to "an unknown issue".
9. **Size.** Variant 1 is larger than Variant 2; the layering earns its keep only if the grid-completeness test ships with it.

## Shared assumptions

| Id | Verdict | Reason |
|---|---|---|
| A-001 | QUALIFY | Holds only once OB-H1 logs a real subagent and nested-subagent payload; until then it is a ship gate for `full`, and the reserved fallback must require `agent_id`. |
| A-002 | QUALIFY | The V5/V6 split holds for top-level prompts; because prompt events inside subagents are UNVERIFIED (N1), any prompt payload carrying `agent_id` must be ignored for approval. |
| A-003 | QUALIFY | Holds only if the claim script checks, before launch, that the guard script exists and `~/.claude/settings.json` registers it; OB-H2 then confirms the session file exists before the first tool call. |
| A-004 | ACCEPT | One OS user runs both; this is why all three reject mode bits, HMAC and root-owned paths and rely on a deny rule. |
| A-005 | REJECT | The design must not assume `jq`: governed sessions block when it is missing (Variant 1 LL-BROKEN), and the claim script refuses to launch without it (Variant 2). |
| A-006 | QUALIFY | Holds if Orca and the ccsession shim keep the claim script's `HOME`; OB-H2 on a real Orca launch detects a mismatch, because the session file would be missing. |
| A-007 | QUALIFY | Holds only if the marker survives unaltered; bind with a record when the marker appears anywhere, and bind degraded without a record only when it is at the start. |
| A-008 | QUALIFY | `cwd` identifies the worktree reliably only at the first prompt; push checks must resolve HEAD in the `-C` directory when one is given, and any fallback should use prefix matching plus `agent_id`. |

## Per-point verdicts

| Point | Superior approach | Confidence % | One-sentence evidence |
|---|---|---|---|
| S-001 | Variant 1 | 55 | Front matter with `status: design only` states provenance; low impact either way. |
| S-002 | Merge | 65 | Variant 1's numbered residuals are citable, Variant 2's cut table shows what each deletion opens; use both columns. |
| S-003 | Merge | 70 | Variant 1's generic rows plus Variant 3's literal commands and over-match row make the table both complete and testable. |
| S-004 | Variant 1 | 75 | Policy and message blocks with a grid-completeness test make a new class or level one data row. |
| S-005 | Variant 1 | 65 | U9 to U13 name real unknowns (`command_name` form, `isolation` key, Monitor field) that drive concrete tolerances. |
| S-006 | Merge | 60 | Variant 1's ids cover more cases; Variant 2's Blocked/Why/You can lines are the clearest wording. |
| C-001 | Merge | 75 | Variant 1's degraded binding plus Variant 2's marker-anywhere search when a record exists, per A-007. |
| C-002 | Merge | 75 | Variant 2's ship gate with Variant 1's reserved fallback, corrected to require `agent_id` (X-004). |
| C-003 | Variant 1 | 70 | JSON record carries `repo` and issue for LL-REPO and AC-7 messages; separate approval file avoids Variant 3's read-modify-write. |
| C-004 | Merge | 80 | Variant 1's wider surface (gitconfig, alias) plus Variant 2's two-part name and `\/` tests. |
| C-005 | Variant 1 | 75 | Both events, prefix stripping for U9, and a first-line slash route for U5. |
| C-006 | Variant 2 | 60 | Writing approval only at `worktree` and ignoring `agent_id` prompts is tidier; outcome is the same. |
| C-007 | Variant 1 | 75 | Skips `--git-dir` and `--work-tree` values that Variant 2 misreads as the subcommand, and is position-free unlike Variant 3. |
| C-008 | Variant 1 | 70 | `git pull` can create a merge commit, and origin-only push matches the CLAUDE.md fork rule. |
| C-009 | Variant 1 | 70 | Word-after-push avoids Variant 2's `feature/main` false block; needs the `HEAD`, `+main` and `@{push}` fixes conceded above. |
| C-010 | Merge | 75 | Variant 1's record-based LL-REPO plus Variant 2's `gh <group> create` gate. |
| C-011 | Merge | 70 | Variant 1's three events with a matcher that adds MCP, Monitor, Workflow, RemoteTrigger but excludes read tools. |
| C-012 | Variant 1 | 70 | V1 says Workflow fires PreToolUse; blocking RemoteTrigger and Workflow and scanning Monitor closes self-start routes. |
| C-013 | Variant 1 | 75 | A GitHub MCP merge tool is an AC-6 route that Variants 2 and 3 leave open. |
| C-014 | Variant 1 | 65 | Subcommand-specific `orca` blocking avoids Variant 3's read-only over-block and keeps the remote-isolation rule. |
| C-015 | Merge | 70 | Variant 2's default-deny structure with Variant 1's traps both guarantee exit 2 on internal error. |
| C-016 | Variant 1 | 70 | No `jq` before the two cheap exits; Variant 3 runs `jq` on every call everywhere. |
| C-017 | Merge | 75 | Variant 1's absolute ceilings plus Variant 3's relative guard against `block-bare-python.sh`. |
| C-018 | Variant 1 | 65 | Naming issue and level meets AC-7 best; needs a degraded fallback text. |
| C-019 | Merge | 70 | Variant 1's layer groups and grid test plus Variant 3's literal payloads. |
| C-020 | Variant 2 | 60 | OB-H1 first decides the fallback; OB-H4 and OB-H5 add live wording and timing checks. |
| X-001 | Variant 1 | 85 | Only Variant 1 keeps a launched agent governed when the record is missing, stale or consumed. |
| X-002 | Merge | 80 | Variant 1's governed block plus Variant 2's claim-side refusal; V8 does not force Variant 3's fail-open. |
| X-003 | Variant 1 | 70 | Degrading to `worktree` keeps planning possible and keeps approval in its own file. |
| X-004 | Variant 2 | 80 | Variant 3's rule 2 governs a person's own subagents; Variant 1's reserved fallback needs the same correction. |
| X-005 | Variant 1 | 75 | Governed-only tamper keeps T-ISO-1 true and lets a person release a session from their own Claude session. |
| X-006 | Merge | 85 | Variants 1 and 2 both block settings edits per V11; Variant 3's claim is false. |
| X-007 | Variant 1 | 75 | Word checks plus `symbolic-ref` close HEAD, `--all`, `--mirror`; Variant 3 breaks AC-6. |
| X-008 | Variant 1 | 65 | A pull can merge into the branch; blocking it matches "only people merge". |
| X-009 | Variant 1 | 85 | The worktree's `.git` file points to the main checkout's common dir, where hooks live. |
| X-010 | Variant 2 | 90 | `_FRESHNESS_SCRIPTS` is defined at `install_hooks.py:42` and only imported by Makefile line 309. |
