# Round 1: Advocate for Variant 2 (sonnet:refactorer)

## Position summary

Variant 2 is the smallest design that meets the 8 acceptance criteria: one flat script, one-word state files, two events, no layering. It is right on the facts that decide AC-4, AC-5 and AC-6 (X-004, X-006, X-007, X-010). I concede that it is too thin in a few places (X-001, X-008, Monitor/MCP coverage, speed numbers), and the best final spec is Variant 2's skeleton with a short list of small borrowings from Variant 1 and Variant 3.

## Steelman of Variant 1

The strongest case: this hook's worst failure is silent. If a launched agent ends up ungoverned, nothing tells anyone. So every ambiguous input should resolve toward governed, and Variant 1 does that consistently. A marker always binds (U-001), even with a lost, stale or reused record. Any unexpected end becomes exit 2 through traps. A corrupt session file drops to the strictest level instead of releasing. It also closes routes the others skip: `git pull`, git aliases, push to a non-`origin` remote, `gh pr create` without the right repo, MCP merge tools, Monitor commands, `curl` to a `/merge` URL (U-003, U-004). Its closed action-class list with a "grid is complete" test means a later level cannot be added with a hole. It has the most accurate repository reading of git hooks in a linked worktree (X-009: this worktree's `.git` is a file pointing at `/home/coder/workspaces/IronClaude/.git/worktrees/...`). Where it is right: X-001, X-008, C-008, C-012, C-013, U-001 and the part of U-003 that needs no new state.

## Steelman of Variant 3

The strongest case: a guard is only as good as the proof that it works, and the proof must be cheap to read. Variant 3 gives literal payloads and literal commands per acceptance criterion (T-W, T-F, T-S, T-ST, T-WR), pins a known over-match with a test so a change is deliberate, and orders the work so the hook is shown harmless to ordinary sessions (T-ISO-1, T-FO) before it governs anything. Its speed guard is the best of the three: the ordinary-path median must stay within 1.5 times `block-bare-python.sh` measured in the same run, over 100 runs, so CI noise cancels (U-009). It cross-checks the record's worktree path against `cwd` (U-008), adds `gh pr ready` (U-010), and names U8 as "the one item that can silently void the design". Where it is right: C-017, S-003 (literal commands), the harmless-first order, and the U8 warning.

## Strengths claimed (Variant 2)

1. **Smallest state surface (C-003, C-006).** Session file is one word, approval is an empty `.ok` file (Variant 2 section 4 table). Reading the level needs no `jq` and cannot hit a bad-JSON state. Variant 3's approval is a read-modify-write of the governing JSON (C-006), which can corrupt the file that decides everything. Variant 1 needs `v`, `degraded`, nonce and age fields plus an LL-STATE note to handle states that a one-word file cannot be in.
2. **Fewest unverified dependencies for approval (C-005).** Variant 2 approves from the UserPromptSubmit `prompt` text only, which rests on V6 (verified: typed slash lines arrive as typed). Variants 1 and 3 add UserPromptExpansion with a `command_name` match; its form is unverified (Variant 1's own U9), and Variant 3 does no stripping of `/` or `sc:`, so a differently-formed name would silently approve nothing. The plain `approved` reply works in every variant, so the failure of the typed route is loud (Variant 2 section 6).
3. **Matcher keeps ordinary traffic out of the hook (C-011).** `hooks.json` already uses tool matchers (`Edit|Write`, `Bash`, `mcp__auggie__.*|...`). Variant 2's matcher means Read, Grep, Glob and most MCP calls never spawn the script. Variants 1 and 3 run bash for every tool call in every session. AC-4 and AC-8 both reward not touching ordinary calls.
4. **Best tamper design (C-004, X-005, X-006, U-005).** Governed-only, covers `.claude/settings` and `.claude/hooks` (the likeliest workaround, V11 verified), and assembles the store name from two parts so the guard's own source and tests do not trip it. Variant 1's substring list includes `launch-level-guard`; in a governed session working on this very issue, any Bash naming `src/superclaude/hooks/scripts/launch-level-guard.sh` is blocked. That is an unwanted block Variant 1 does not list.
5. **Right on the fact-checked contradictions.** X-004 (a person's own subagents must not be governed), X-006 (settings edits must be blocked), X-007 (`git push origin HEAD` on `master`, `--all`, `--mirror` must be blocked), X-010. For X-010 I re-checked the repo: `_FRESHNESS_SCRIPTS` is defined only at `src/superclaude/cli/install_hooks.py:42`; `Makefile:309` imports it. There is no Makefile list to edit (Variants 1 and 3 say there is).
6. **Default-deny once governed, with an install-time guard (C-015, X-002).** Variant 2 asks the claim script to refuse to launch when `jq` is missing, which removes the situation Variant 3 chooses to live with.
7. **Tokens, not a sub-parser (C-007).** One `jq`, one character-class sweep, no command-position logic. Ignoring position means wrappers (`bash -c`, `env`, `command`, `xargs`, `sudo`) need no list. Variant 3 builds a wrapper list (`timeout N`, `env -u X`, a four-word lookahead, `-c` re-scan) after citing the #357 parser's nine ceilings as the reason to avoid one. That recreates the problem.
8. **Every cut is priced (S-002).** The cut table says what each deletion leaves open and lists seven owner decisions, so the owner can buy any cut back.

## Weaknesses identified in Variants 1 and 3

**Variant 1**

1. **Scale beyond the task.** 12 action classes, 13 message ids, five named layers, three events, and a `--classify` argument that exists only for tests. "A new level, tool or action is a data row" prices an extension nobody asked for (scope discipline). A production hook that runs on every tool call carries a test-only mode.
2. **Inconsistent on clocks.** It rejects approval expiry because it "would add a clock edge case" (section 6) but adds a 30-minute stale-record rule at binding (section 4 step 4).
3. **"A marker always governs" has a cost it does not price.** A human who pastes a marker as the first prompt of an ordinary session is governed, with only `rm` to undo it. This needs the "starts with" rule, which fails if Orca prepends text (A-007).
4. **Fast path 2 reads `session_id` by regex on raw JSON.** If a harness puts `tool_input` before `session_id` (key order is not in V1 to V14), a command containing `"session_id":"x"` could point the lookup at another id. Variant 2 reads it with `jq` on the main path.
5. **Possible ERR trap gap.** Bash does not inherit an ERR trap into functions unless `set -E` is set. Variant 1 puts everything in functions and relies on ERR plus EXIT traps and does not mention `set -E`. This is general bash behaviour, not something I checked in this repo; the EXIT trap may cover it.
6. **Over-blocks:** `claude`/`ccsession` followed by any dash word blocks `grep claude -rn docs/` in a repo named superclaude; it accepts blocking `cat ~/.claude/settings.json` (its own A12).

**Variant 3**

1. **Three verified errors against acceptance criteria:** X-004 (always-on fallback governs a person's own subagent session, AC-4), X-006 (the settings edit passes, AC-5), X-007 (`git push origin HEAD` from `master`, `--all`, `--mirror` pass at submit, AC-6). Each is stated in the diff analysis with its fact check; I re-derived X-006 from Variant 3's own text: the Edit check is only for the store path, and "basename `claude`" does not match a path ending `settings.json`.
2. **Fail-open in a governed session (X-002, C-015).** Variant 3 cites V8 ("a crash does not block anyway"), but V8 says nothing about a script choosing exit 2 on its own check. `block-bare-python.sh` fails open on missing `jq` (lines 11, 67-68) because it guards a style rule; this guard's whole job is a boundary.
3. **Blocks any command word `claude` or `orca`, including read-only calls.** `grep claude`, `orca worktree current`, and any Orca worker call (heartbeats, ask, worker_done in the orchestration skill) are blocked. If U7 resolves toward "launched sessions are workers", this breaks them.
4. **Hard-codes `IronbellyOrg/IronClaude` (O-1 default yes).** The script is installed to every user's `~/.claude/hooks` by `superclaude install` (Makefile line 314: "end-user 'superclaude install' will skip it"). A hard-coded repo name is wrong for every other project.
5. **Binding needs `cwd` equality (U-008).** A launch from a subdirectory or a symlinked path fails to bind, and a failed bind is silent (A-007, A-008). It adds a new fail-open path to a hook that wants none.
6. **Bind is write then delete, not one `mv`.** A crash between the steps leaves a live pending record plus an active file; the single-use claim is not atomic.
7. **`@pytest.mark.manual` placeholders fail collection.** `pyproject.toml` sets `--strict-markers` (line 114) and I found no `manual` marker in `pyproject.toml`, `tests/conftest.py` or `pytest_plugin.py`.
8. **Internal contradictions (X-005):** "blocked in every session" against "ordinary sessions are never blocked" and T-ISO-1.

## Concessions

- **X-001, U-001:** a lost, stale or reused nonce leaves my session ungoverned. Variant 1 is right. Adopt "marker with no usable record binds at `worktree`" (see C-001 for the guard against the paste case).
- **X-008:** `git pull` can create a merge commit; I gate it nowhere. Add `pull` to the merge list.
- **C-012, C-013:** Monitor runs a shell command, so `git push` inside Monitor passes my matcher. MCP merge tools pass too. My cuts are real gaps, not only owner choices.
- **C-007:** I skip values after `-C` and `-c` only; `git --git-dir x push` makes `x` the subcommand and slips through. Variant 1's longer option list is correct.
- **C-017:** I give no measured numbers. Variant 3's relative guard is better.
- **X-003:** blocking every matched call on a bad session file is heavy-handed; Variant 1's strictest-level degrade is more usable and equally closed.
- **C-015:** "default-deny" needs a mechanism. `set -u` aborts with exit 1, which does not block (V8), so I need Variant 1's EXIT trap.
- **C-009:** my `symbolic-ref` check runs on every submit-level push, so a push of a named feature ref from a `master` HEAD is wrongly blocked. Rare, but Variant 1's "only when no branch word follows" is more precise.
- **C-001, C-005:** no UserPromptExpansion means typed-command approval depends on V6 and the `approved` fallback (U5).
- **C-002:** U1 as a ship gate means a redesign if OB-H1 fails. That is a schedule risk, not a correctness risk.
- U-003's remote check and my lack of issue numbers in messages are real gaps; I accept the first as optional.

## Shared assumptions

| ID | Verdict | Reason |
|---|---|---|
| A-001 | QUALIFY | Holds only if OB-H1 observes that subagent and nested ids equal the parent's, before any real `full` launch. If it fails, redesign; an always-on cwd fallback is not safe (X-004). |
| A-002 | QUALIFY | True for slash commands (V5) and for agent tool calls, but V6 gives no origin field on prompts. It holds only while scheduling tools and `orca terminal send` stay blocked, and prompts carrying `agent_id` are ignored (N1). |
| A-003 | QUALIFY | Acceptable only if the claim script checks the guard is installed (script file present and executable, and registered in the settings the launch reads) before it writes a pending record. No variant does this; a silent unbound launch is the worst case. |
| A-004 | ACCEPT | Same OS user means no file is truly unwritable, so HMAC, mode bits and a root directory add no protection; this is why all three use a deny rule and `rm` as release. |
| A-005 | QUALIFY | Only if the claim script refuses to launch without `jq` and the hook blocks governed calls when `jq` disappears (not fail-open, X-002). |
| A-006 | QUALIFY | Holds only if the claim script and the launched session resolve the same `$HOME`. Unit tests use a temporary `HOME` and cannot catch a mismatch, so OB-H2 (bound before the first tool call) must be recorded as the check for it. |
| A-007 | QUALIFY | The marker reaching `prompt` unaltered is acceptable; "starts with" is not. Match the first marker anywhere in the first prompt, and record the real prompt text (any Orca preamble, U7) in OB-H2. |
| A-008 | QUALIFY | Use `cwd` only for the `symbolic-ref` lookup, with failure meaning block. Add tests for `cd sub && git push` and `git -C /elsewhere push`; a push with an explicit `master` or `main` word is still caught by the raw-command regex. |

## Per-point verdicts

| Point | Superior approach | Confidence % | One-sentence evidence |
|---|---|---|---|
| S-001 | Variant 1 | 55 | Front matter plus a title identify the spec; Variant 2's file starts at "## 1. Position summary" with no title, and adding one costs nothing. |
| S-002 | Merge | 55 | Variant 2's cut table ties each deletion to what it leaves open; Variant 1's R-numbers make each residual citable. |
| S-003 | Merge | 65 | Variant 2 states the table is the test data (no drift) and Variant 3's literal commands such as `git push origin HEAD` make each row directly runnable. |
| S-004 | Variant 2 | 60 | 16 rows do not need five layers and a `--classify` mode; a test-only argument in a hook that runs on every tool call is surface for no acceptance criterion. |
| S-005 | Merge | 70 | All three keep U1 to U8; take Variant 1's U9 to U13, Variant 2's N1 to N5, and Variant 3's per-item Test column. |
| S-006 | Variant 2 | 50 | Message families with one fixed three-line shape pass AC-7, while Variant 3's MSG-SELF has no next step. |
| C-001 | Merge | 60 | Take Variant 2's atomic `mv` and anywhere-match (A-007) plus Variant 1's degraded bind for a marker with no usable record; Variant 3's `cwd` equality adds a silent fail-open path. |
| C-002 | Variant 2 | 65 | A fallback that is always on governs a person's own subagent session (X-004); a ship gate on OB-H1 costs only schedule, and Variant 1's off-by-default design is a fair second. |
| C-003 | Variant 2 | 75 | One-word files remove the bad-JSON and read-modify-write states that Variants 1 and 3 must then handle. |
| C-004 | Variant 2 | 70 | Governed-only scope (not Variant 3's every session), settings and hooks tokens, and a two-part store name that avoids tripping on its own source. |
| C-005 | Variant 2 | 65 | Prompt-text approval rests on verified V6; the `command_name` form in Variants 1 and 3 is unverified (U9) and Variant 3 does no prefix stripping. |
| C-006 | Variant 2 | 60 | An empty `.ok` file written only at `worktree` has no read-modify-write; Variant 3 rewrites the governing JSON, Variant 1 writes at levels where approval means nothing. |
| C-007 | Merge | 65 | Variant 2's single-pass tokens plus Variant 1's longer skip list (`--git-dir`, `--work-tree`, `--namespace`, `--config-env`); Variant 3's wrapper list is a sub-parser. |
| C-008 | Variant 1 | 60 | `pull` can merge and an alias can hide `push`, both one-line rules; its remote check is optional. |
| C-009 | Variant 2 | 55 | One regex over the raw command plus `symbolic-ref` catches `HEAD`, `--all`, `--mirror` and `:main`; Variant 1 is more precise on bare pushes, Variant 3 fails AC-6 (X-007). |
| C-010 | Merge | 60 | Block `gh pr merge`, `gh api .../merge` and `gh <group> create` below submit (Variant 2); require a `--repo` word on `gh pr create` with no hard-coded name, since Variant 3's hard-coded repo is wrong for other users. |
| C-011 | Variant 2 | 55 | A matcher in the style `hooks.json` already uses keeps Read, Grep, Glob out of the hook; extend it with Monitor and the MCP names from C-013. |
| C-012 | Variant 1 | 65 | Monitor runs a shell command, so scanning it like Bash closes a plain `git push` route that Variant 2 leaves open. |
| C-013 | Merge | 60 | Use Variant 1's name rule, but put it in the matcher (`mcp__.*(merge|push|commit|create_pull_request).*`) so other MCP calls never spawn the hook. |
| C-014 | Variant 2 | 55 | A fixed flag list blocks fewer innocent commands than Variant 1's "any dash word"; Variant 3's blanket `claude`/`orca` word block breaks `grep claude` and read-only Orca calls. |
| C-015 | Merge | 65 | Variant 2's default-deny posture is right, but only Variant 1 names the mechanism (EXIT trap), needed because `set -u` aborts with exit 1, which does not block (V8). |
| C-016 | Variant 2 | 55 | `compgen -G` then one `jq` is exact and fast enough; Variant 1's regex on raw JSON depends on key order, Variant 3 spawns `jq` on every call. |
| C-017 | Variant 3 | 60 | A median relative to `block-bare-python.sh` over 100 runs cancels CI noise, and Variant 2 gives no numbers at all. |
| C-018 | Variant 2 | 55 | Fixed "Blocked / Why / You can" lines satisfy AC-7 without needing an issue number in state; Variant 3's MSG-SELF has no next step. |
| C-019 | Merge | 65 | Generate cases from the one decision table (Variant 2), use literal commands (Variant 3), add Variant 1's "every id has text" test; skip `@pytest.mark.manual` unless registered. |
| C-020 | Variant 2 | 55 | OB-H1 first, because U1 and U2 can change the design; Variant 3 puts observed checks last, and Variant 3's harmless-first skeleton is worth keeping. |
| X-001 | Variant 1 | 80 | A lost or stolen nonce must not release the launched agent; Variant 2's "A session never bound looks like an ordinary one" is the gap. |
| X-002 | Variant 2 | 70 | Block governed calls when `jq` is missing and refuse launch without it; V8 does not force fail-open, and `block-bare-python.sh` (lines 11, 67-68) fails open only because it guards style. |
| X-003 | Variant 1 | 60 | Degrading to the strictest level keeps `git status` and plan edits working; my block-everything is also closed but stalls the session. |
| X-004 | Variant 2 | 90 | V4 only says a subagent carries `agent_id`; a person's own session that starts a subagent sends the same shape, so Variant 3's rule 2 governs it. |
| X-005 | Variant 2 | 85 | Governed-only tamper scope; Variant 3 contradicts its own "ordinary sessions ... never blocked" and T-ISO-1. |
| X-006 | Variant 2 | 85 | V11 verifies `disableAllHooks`; Variant 3's Edit check covers only the store path and "basename `claude`" does not match `settings.json`, so the edit passes. |
| X-007 | Variant 2 | 75 | Raw-command regex plus `symbolic-ref` blocks `HEAD`, `--all`, `--mirror`; Variant 1 reaches the same outcome and Variant 3 allows `git push origin HEAD` at submit. |
| X-008 | Variant 1 | 65 | A pull can create a merge commit, so AC-6's "never a merge" is not met with `pull` allowed. |
| X-009 | Variant 1 | 90 | This worktree's `.git` file points at the main checkout's `worktrees/` directory, so Variant 3's ".git/hooks sits inside the worktree" is wrong; the decision to reject git hooks stands. |
| X-010 | Variant 2 | 90 | `_FRESHNESS_SCRIPTS` is defined at `install_hooks.py:42` and only imported by `Makefile:309`; `--strict-markers` is set at `pyproject.toml:114` with no `manual` marker found. |
