# Refactoring Plan: Merge into Base (Variant 1)

## Overview

- Base: Variant 1 (`variant-1-opus-architect.md`, opus:architect), selected in `base-selection.md` by the debate tiebreaker (7 points to 4).
- Incorporating strengths from: Variant 2 (`variant-2-sonnet-refactorer.md`, sonnet:refactorer), Variant 3 (`variant-3-haiku-qa.md`, haiku:qa), the Round 2 merged rules (`round-2-advocate-1..3.md`, section 5) and the fault-finder's 40 findings (`invariant-probe.md`).
- Planned changes: 34, in seven groups: A frame (1 to 3), B identity and state (4 to 8), C classification (9 to 18), D policy and failure (19 to 23), E registration and interfaces (24 to 25), F proof (26 to 30), G registers (31 to 34).
- Risk level: Medium overall. The rules are concrete and each has a named test, but four facts stay unverified until the observed checks run (U1 subagent identity, U8 first-prompt timing, U7 worker preamble, anchored matcher behaviour).

### How the merge executor uses this plan

1. Each change states the **Final rule** in testable words. Write the spec section from that text. Do not reopen a variant to fill a gap; if a detail is missing here, the rule is "not in v1".
2. Each fact, token list, regex, file name, message id and exit code appears in exactly one change. Other changes refer to it by change number. Keep that single-statement property in the spec: write it once, cite it elsewhere.
3. The spec keeps Variant 1's 16-section skeleton (Change 1). The "Target" field of each change names the section.
4. Selection criterion used for every residual split and every conflict between a probe resolution and a debated rule: **fewest edge cases and fewest unwanted blocks that still meets AC-1 to AC-8 of issue #394.** Where this plan departs from a Round 2 consensus rule or from a probe's suggested resolution, the change says so under "Departs from".
5. Plain words, no em dashes, in the spec as in this plan.

### Repository facts re-checked while drafting (2026-11-05)

- `src/superclaude/hooks/hooks.json` registers commands as `~/.claude/hooks/<name>.sh`; UserPromptSubmit entries carry no matcher; the existing Bash guard uses timeout 3.
- `_FRESHNESS_SCRIPTS` is defined only in `src/superclaude/cli/install_hooks.py` (line 42); the `Makefile` `install` target runs `uv pip install -e ".[dev]"` and does not run `superclaude install`.
- `/sc:implement` (skill `sc-implement-protocol`) runs `git stash`, `read-tree`, `add`, `write-tree`, `update-ref` on `refs/superclaude/implement/...` (sometimes through a shell variable, `refs/retry.md` line 371), `rev-parse`, `diff`, `show`, `cat-file`, `for-each-ref`, `show-ref`, `ls-tree`, `restore`, `checkout`, `grep`, `gc`; no `commit`, `push`, `merge` or `pull`.
- `/sc:pr-submit` runs, among reads, `git merge-tree`, `git remote get-url`, `gh pr view --json mergeable,mergeStateStatus`, `gh pr checks`, `gh repo view`, `gh pr create --repo "$REPO"`, `gh api --method POST .../comments/<id>/replies`, `gh api graphql` with the mutation `resolveReviewThread`, `git commit --only -- <paths>`, `git push origin <target_sha>:<target_branch>` (written with placeholders the agent fills in), and the conflict sync `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>`.

### Design in five lines (for the spec's position summary)

1. One bash script, `launch-level-guard.sh`, on two events: UserPromptSubmit (bind a launch, record approval) and PreToolUse (decide). It never reads `cwd`, never runs git, and never reads a file inside the worktree.
2. A session is governed only when a launch marker in its prompt binds it to `session_id`; once bound it is governed for life, and only a person's `rm` releases it. A malformed or orphaned marker at the start of a prompt still binds, at the strictest level.
3. Bash and Monitor text goes through one normalisation pass, then a word scan with allowlists (git subcommands, `orca` subcommands, gh read actions) instead of growing denylists. No shell parser.
4. Approval comes only from a typed prompt and unlocks implementation only. No level allows a merge or a push to `master`/`main`; at `full --submit` a push must be written `git push origin <source>:<branch>`.
5. In a governed session every failure blocks with a plain three-line message; ordinary sessions are never blocked and pay one directory test per call.

## Planned Changes

### Group A: frame

### Change 1: Spec frame, skeleton and defined terms (from Variant 1, with the Variant 3 title line)
- **Source**: Variant 1 front matter and section list; Variant 3 H1 and persona line.
- **Target**: Base, front matter and all section headings (restructure).
- **Settles**: S-001; scoring note L4 (terms used before definition).
- **Final rule**:
  1. YAML front matter: `issue: IronbellyOrg/IronClaude#394`, `status: design only, nothing implemented`, `base: variant 1`, `merged_from: variants 1, 2, 3; round 2; invariant probe`, `created: <ISO date of the merge>`.
  2. H1: `Launch-level guard for /sc:issue --claim --pipeline (issue #394)`.
  3. Sections, in this order: 1 Position summary; 2 Threat model; 3 Components and files; 4 Session identity and state; 5 Decision table; 6 Human approval; 7 Subagents; 8 Bash, Monitor and git classification; 9 Other tools and escape routes; 10 Fail-closed rules and speed; 11 Block messages; 12 Test plan; 13 Acceptance criteria map; 14 Order of work; 15 Open decisions for the owner; 16 Unverified items; 17 Residual risks; 18 Rejected alternatives.
  4. A "Terms" list right after the position summary defines, before first use: **store** (`$HOME/.claude/state/launch-level/`); **governed session** (a session whose valid `session_id` has a file in `sessions/`, or a call that resolves to degraded `worktree` under Change 6); **ordinary session** (every other session); **effective level** (one of `W` = worktree before approval, `WA` = worktree after approval, `F` = full, `FS` = full with `--submit`); **segment** and **word** (Change 9); **class** (Change 19); **message id** (Change 23). It also expands the external ids the spec cites: A2, A12 (seed brief assumptions), WC-9, WC-13 (`~/.claude/WORKER-CONTRACT.md`), FR-23, FR-31 (launch-levels addendum), V1 to V14 and U1 to U8 (`enrichment/research-light.md`).
- **Rationale**: S-001 majority for Variant 1's front matter (A1 55%, A2 50%, A3 merge 55%); base-selection L4 marked all three variants NOT MET for undefined terms.
- **Integration point**: top of the spec; replace Variant 1's 16-section list with the 18 sections above (sections 17 and 18 are new homes for Changes 32 and 34).
- **Risk**: Low. Cosmetic and structural only.

### Change 2: Threat model (from Variant 1 section 2, Variant 2 section 2)
- **Source**: Variant 1 section 2 targets; Variant 2 section 2 harness facts.
- **Target**: Base section 2 (replace the R1 to R8 table; residuals move to section 17, Change 32).
- **Settles**: A-004; S-002 (structure part).
- **Final rule**: Section 2 states, in this order:
  1. **T1**: an honest agent that drifts from `launch-prompt.md` and runs `/sc:implement`, `git commit`, `git push` or `/sc:pr-submit` anyway. Primary target.
  2. **T2**: an agent that tries obvious workarounds in one step: `bash -c`, `sh -c`, `env`, `command`, `exec`, `sudo`, `nohup`, `timeout`, `xargs`, `/usr/bin/git`, `\git`, quote splicing, a git alias, `$(...)`, a subagent, a fresh `claude -p`, typing `approved` into its own terminal, scheduling a turn, editing the guard's state or the Claude Code settings, reinstalling the hooks. Designed against.
  3. **T3**: deliberate multi-step evasion (a script file written with Write and then run, plumbing commits through variables, a hostile agent). Not designed against; listed in section 17.
  4. Premise: the agent and the hook run as the same OS user, so no file is truly unwritable. Protection is a deny rule plus residuals, not file permissions.
  5. Harness facts relied on: V2 and V3 (a PreToolUse exit 2 blocks, also with permission prompts off), V4 (hooks run inside subagents and carry `agent_id`), V5 and V6 (typed commands and prompts arrive on prompt events with no origin field), V8 (a crashing or timed-out hook does not block).
- **Rationale**: all three variants share T1 to T3 (diff-analysis Content intro); A-004 STATED by all.
- **Integration point**: section 2.
- **Risk**: Low.

### Change 3: Components and files (from Variant 2 section 3, correcting Variant 1)
- **Source**: Variant 2 section 3; Round 2 X-010 (unanimous Variant 2).
- **Target**: Base section 3 (replace the table; delete the "Layers as shell functions", "Action classes" and "Extension scaffolding" paragraphs, whose content moves to Changes 19 and 34).
- **Settles**: X-010, S-004 (file part).
- **Final rule**: Section 3 lists exactly these items:

  | Item | Status | Written by | Purpose |
  |---|---|---|---|
  | `src/superclaude/hooks/scripts/launch-level-guard.sh` | new | developer | the only hook script; flat bash plus `jq`, no awk, no Python, no layers, no command-line arguments |
  | `src/superclaude/hooks/hooks.json` | existing, 2 new entries | developer | registration (Change 24) |
  | `src/superclaude/cli/install_hooks.py`, list `_FRESHNESS_SCRIPTS` | existing, 1 new string | developer | `"launch-level-guard.sh"`, so `superclaude install` deploys it and `make verify-sync` passes. No `Makefile` line exists to add; the Makefile imports this list |
  | `tests/hooks/test_launch_level_guard.py` | new | developer | all automated cases (Changes 26, 27) |
  | `tests/hooks/fixtures/launch_level/ob_h1/*.json` | new | OB-H1 run | real payloads captured by OB-H1 (Change 29) |
  | `~/.claude/state/launch-level/pending/<nonce>` | runtime | claim script | launch record (Change 4) |
  | `~/.claude/state/launch-level/sessions/<sid>`, `sessions/<sid>.ok` | runtime | hook | bound level and approval (Change 4) |

  `.claude/` mirrors produced by `make sync-dev` are never staged. The claim feature's files (`orca_worktree.py`, `launch-prompt.md`, `pipeline.json`) are out of scope; the hook never reads `pipeline.json` (Change 25).
- **Rationale**: X-010 fact check (`install_hooks.py:42` defines the list, `Makefile:309` imports it); all advocates conceded.
- **Integration point**: section 3.
- **Risk**: Low.

### Group B: identity and state

### Change 4: Store layout and file formats (from Variant 2 section 4, with probe fixes)
- **Source**: Variant 2 section 4 file table; Round 2 C-003 (majority Variant 2), C-006 (unanimous Variant 2); INV-019.
- **Target**: Base section 4, "where state lives" (replace the JSON record and `.approved` file).
- **Settles**: C-003, C-006 (file part), INV-006, INV-019.
- **Final rule**:
  1. Store: `$HOME/.claude/state/launch-level/`. The script builds this path from two literal parts (`$HOME/.claude/state/` and `launch-level`), so its own source never contains the joined text that the tamper rule (Change 17) looks for.
  2. `pending/<nonce>`: written only by the claim script. File name matches `^[0-9a-f]{32}$`. Content: one line holding one word, `worktree`, `full` or `full-submit`.
  3. `sessions/<sid>`: written only by the hook, by `mv` of a pending file (normal bind) or by writing the word `degraded` (degraded bind, Change 5). Read with `read -r level < file`. The words `worktree`, `full`, `full-submit` set the level; any other content (including `degraded`, an empty file, an unreadable file) means level `worktree` plus the LL-STATE note (Change 23).
  4. `sessions/<sid>.ok`: empty file written only by the hook; its existence is approval (Change 8).
  5. A `session_id` is valid only if it matches `^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$`. No dots are allowed, so `.`, `..` and names ending in `.ok` can never be a session file name.
  6. The hook creates `sessions/` with `mkdir -p` under `umask 077`. It never writes `pending/` except to remove a consumed record (Change 5), never prunes, and never edits a file in place (no JSON, no read-modify-write).
  7. Release: a person runs `rm "$HOME/.claude/state/launch-level/sessions/<sid>" "$HOME/.claude/state/launch-level/sessions/<sid>.ok"` in their own terminal. LL-TAMPER prints this command with the real `<sid>`.
- **Rationale**: one word needs no `jq` and has no bad-JSON state (C-003); `touch` never rewrites the file that holds the level (C-006); the no-dot id rule removes the `sessions/..` and `x.ok` collisions in one rule (INV-019); an empty file left by a crash reads as the strictest level (INV-006).
- **Departs from**: Advocate 1's Round 2 line `level repo issue`. Nothing reads `repo` (Change 12 compares no repo name) or `issue` (Change 23 names the level only), so the one-word form wins on fewer states.
- **Integration point**: section 4, subsection "State".
- **Risk**: Low.

### Change 5: Launch marker detection and binding on UserPromptSubmit (merge of Variants 1 and 2, probe fixes)
- **Source**: Variant 1 section 4 steps 3 to 5 ("a marker always governs"); Variant 2 section 4 binding (marker anywhere, `mv`); Round 2 C-001 and X-001 (unanimous); INV-001, INV-004, INV-014, INV-015.
- **Target**: Base section 4, "Binding" (replace steps 1 to 5).
- **Settles**: C-001, X-001, U-001, A-007; INV-001, INV-004, INV-014, INV-015.
- **Final rule** (the UserPromptSubmit branch, step by step):
  - **U1.** Read all of stdin into `raw`.
  - **U2.** If `raw` does not contain the text `[sc-launch:`: exit 0 when `sessions/` holds no file, or when the prefilter of Change 6 step P3 finds no bound id (nothing to bind, nothing to approve).
  - **U3.** If `jq` is not on `PATH`: if `raw` contains `[sc-launch:` and does not contain `"tool_name"`, print LL-NOBIND and exit 2; otherwise exit 0.
  - **U4.** One `jq` call reads `session_id`, `agent_id` and `prompt`. If `jq` fails (input is not JSON), act as in U3.
  - **U5.** If `agent_id` is a non-empty string, exit 0. Prompts from inside a subagent never bind and never approve.
  - **U6.** Marker detection on `prompt`. **Strict**: the first match anywhere of `\[sc-launch:v1:([0-9a-f]{32})\]` gives nonce `N`. **Loose**: after removing leading spaces, tabs, carriage returns, newlines and one leading UTF-8 byte-order mark, the prompt starts with `[sc-launch:`. A marker is **present** if strict or loose is true. When a marker is present, install an EXIT trap that turns any exit code other than 0 or 2 into LL-NOBIND and exit 2.
  - **U7.** If `session_id` is not valid (Change 4 item 5): marker present, print LL-NOBIND and exit 2; no marker, exit 0.
  - **U8.** If `sessions/<sid>` exists (a bound session): (a) if strict `N` was found and `pending/N` exists, `rm -f pending/N`; the level does not change, so an orphaned record can never bind a later session; (b) run the approval check of Change 8; (c) exit 0.
  - **U9.** Unbound session with no marker: exit 0.
  - **U10.** `mkdir -p sessions` (umask 077).
  - **U11.** If strict `N` was found and `pending/N` exists, `mv pending/N sessions/<sid>`. The `mv` is atomic, so one nonce binds at most one session.
  - **U12.** If `sessions/<sid>` still does not exist and loose is true, write the word `degraded` without overwriting: `(set -C; printf 'degraded\n' > sessions/<sid>)`.
  - **U13.** If `sessions/<sid>` is now a regular file, exit 0. Otherwise print LL-NOBIND and exit 2. The prompt is blocked, so a launched agent whose session could not be registered never starts ungoverned.
- **Consequences the spec must state**:
  - A malformed marker at the start of a prompt (uppercase hex, a dashed UUID, 33 characters, `v2`, the `<nonce>` template text) binds `degraded`, which reads as `worktree` with the LL-STATE note.
  - A strict marker elsewhere in the prompt binds the record's level when the record exists, and blocks the prompt (LL-NOBIND) when it does not. A marker-shaped text in the middle of an ordinary prompt with no live record therefore costs one blocked prompt, never a governed session.
  - A loose (malformed) marker that is not at the start is ignored. Residual R6 (Change 32).
  - Later markers in a bound session never change its level (U8).
  - There is no age check on records and no pruning.
- **Rationale**: X-001 unanimous Variant 1 (a lost, stale or used nonce must not release the agent); C-001 unanimous merge (strict marker anywhere with a record, degraded bind at the start without one); INV-001 (a failed `mv` or write must not leave the agent ungoverned, and V6 lets UserPromptSubmit block); INV-014 and INV-015 (malformed or whitespace-prefixed markers).
- **Departs from**: (1) the Round 2 C-001 text "a marker at the very start" is widened to allow leading whitespace and a byte-order mark (INV-015); (2) INV-015's "match anywhere in the first line or first 512 characters" for the loose form is not taken, because a loose match in the middle of a line governs a person who quotes the marker; (3) INV-014's "any prompt whose first line contains `[sc-launch:`" is narrowed to "starts with", for the same reason. All three choices pick fewer unwanted governed sessions.
- **Integration point**: section 4, subsection "Binding".
- **Risk**: Medium. Depends on U8 (UserPromptSubmit fires before the first model call) and A-006 (same `$HOME`), both checked by OB-H2.

### Change 6: Session resolution on PreToolUse and the fast paths (from Variants 1 and 2, probe fixes)
- **Source**: Variant 1 section 10 fast paths; Variant 2 section 10; Round 2 C-016 (majority merge); INV-002, INV-024.
- **Target**: Base section 4, new subsection "Resolution", and section 10 (replace "Fast path 1" and "Fast path 2").
- **Settles**: C-016, A-008 (statement part), INV-002, INV-024.
- **Final rule** (the PreToolUse branch up to classification):
  - **P1.** Read all of stdin into `raw`.
  - **P2.** If `compgen -G "$store/sessions/*"` finds nothing, exit 0. No `jq`, no subprocess. This is the usual case on a machine with no governed session.
  - **P3.** Prefilter: collect every value `V` in `raw` that matches `"session_id"[[:space:]]*:[[:space:]]*"([A-Za-z0-9][A-Za-z0-9_-]{0,127})"`. If at least one `V` was found and none has a file `sessions/V`, exit 0. This is safe in both directions: the real top-level `session_id` is always among the matches, so a governed call never exits here; a forged nested `session_id` key can only send an ordinary call on to step P5, where `jq` reads the real key.
  - **P4.** If `jq` is not on `PATH`, print LL-BROKEN and exit 2. (Reaching this step means a bound id appeared in the input, or no id could be read while the store holds a bound session.)
  - **P5.** One `jq` call reads `session_id`, `tool_name`, `tool_input.skill // tool_input.name`, `tool_input.command`, `tool_input.file_path // tool_input.notebook_path`, `tool_input.isolation`, `tool_input.run_in_background`. NUL characters inside these strings are replaced by spaces in `jq`. A `jq` failure prints LL-BROKEN and exits 2.
  - **P6.** If `session_id` is valid and `sessions/<sid>` exists, the call is governed at the file's level. If `session_id` is valid and has no file, exit 0. If `session_id` is missing, not a string or not valid, the call is governed at level `worktree` with the LL-STATE note, because the store holds at least one bound session (P2).
  - **P7.** Install the EXIT trap of Change 21, then classify (Changes 9 to 18) and decide (Change 19).
  - The hook never reads `cwd` or `agent_id` on PreToolUse.
- **Rationale**: C-016 merge (`compgen -G` first); INV-002 (with sessions never pruned, one governed launch would otherwise put `jq` on every later ordinary call); INV-024 (a payload without a readable id must not be waved through while governed sessions exist).
- **Departs from**: the C-016 consensus ran `jq` before the regex and used the regex only without `jq`. This plan runs the regex first in every case. It is one code path instead of two, it keeps `jq` off the ordinary path, and the "exit 0 only if no matched id is bound" condition, which all three Round 2 tables accepted for the no-`jq` case, is what makes it safe.
- **Integration point**: section 4 "Resolution"; section 10 "Fast paths".
- **Risk**: Medium. A wrong regex would let a governed call through; T-ISO and T-FC tests (Change 27) cover both directions.

### Change 7: Subagents and the U1 ship gate (from Variant 2 section 7, Variant 1 section 7)
- **Source**: Variant 2 section 7 ("U1 is a ship gate"); Variant 1 section 7 (enforce at the leaf); Round 2 C-002 (majority), X-004 (unanimous Variant 2).
- **Target**: Base section 7 (replace) and section 4 (delete "Cwd fallback (designed, off unless an observed check fails)").
- **Settles**: C-002, X-004, A-001, U3.
- **Final rule**:
  1. Identity is `session_id` only (Change 6). If a subagent and a nested subagent carry the parent's `session_id` (U1), every rule applies to them with no extra code.
  2. The Agent or Task call itself is allowed, except `isolation: "remote"` (Change 15). The Agent `prompt` is never scanned; what a subagent tries is checked when it tries it.
  3. Tool names `Agent` and `Task` are handled the same (U3). `TaskCreate`, `TaskUpdate` and similar names never reach the hook (anchored matcher, Change 24).
  4. Prompt payloads that carry `agent_id` never bind or approve (Change 5 step U5).
  5. **Ship gate**: no claim with `--pipeline full` or `--submit` runs on a real issue until OB-H1 (Change 29) shows that a subagent's and a nested subagent's PreToolUse payloads carry the parent's `session_id`.
  6. No `cwd` fallback is built. If OB-H1 fails, work stops and the owner decides (O-9, Change 33). The spec records the reserve design for that decision only as text: store the launch worktree path as a second line of the session file; treat a call that carries `agent_id`, has an unbound `session_id`, and whose `cwd` is that path or below it as governed. Its known wrong case: a person's own session in the same worktree that starts a subagent (X-004).
- **Rationale**: X-004 fact check (V4 says only that subagent payloads carry `agent_id`; a person's own subagent sends the same shape); all three Round 2 tables keep the fallback off.
- **Integration point**: section 7; remove the fallback paragraph from section 4.
- **Risk**: Medium. If U1 is false, governance of subagents fails until the owner acts; the ship gate keeps that from reaching a real issue.

### Change 8: Human approval (from Variant 2 section 6, Variant 1 section 6)
- **Source**: Variant 2 section 6; Variant 1 section 6 item 2; Round 2 C-005 (residual split), C-006, U-006; INV-008.
- **Target**: Base section 6 (replace items 1 and 2 and the "touches `sessions/<id>.approved`" line).
- **Settles**: C-005, C-006 (rule part), U-006, A-002, INV-008.
- **Final rule**:
  1. Approval is written only by the UserPromptSubmit branch, in a bound session, from a payload without `agent_id` (Change 5 steps U5 and U8).
  2. It is written only when the effective level is `worktree`: the file word is `worktree` or any invalid word, including `degraded`. At `full` and `full-submit` nothing is written.
  3. A prompt approves when either (a) the prompt, with leading and trailing whitespace removed and lower-cased, matches `^approved[.!]?$`, or (b) the first line of the prompt, with leading whitespace removed, matches `^/(sc:implement|sc:task|task)([[:space:]]|$)` (case-sensitive). `/task-builder`, `/tasks`, `/sc:implement-protocol`, `please approved` and `approved, but` approve nothing. A typed `/sc:pr-submit` approves nothing.
  4. Effect: `touch sessions/<sid>.ok`. If the `touch` fails, the prompt still goes ahead (exit 0); the next implement call is blocked with LL-IMPL, which is loud.
  5. Approval unlocks class IMPL only (Change 19), never COMMIT, PUSH, SUBMIT or MERGE. It lasts until a person removes the session's files (owner decision O-6, default).
  6. Ordering: UserPromptSubmit runs before a typed command is expanded, so `.ok` exists before the model's `Skill` call that `/sc:implement` makes (`sc:implement-protocol`).
  7. UserPromptExpansion is not registered (owner decision O-4, default). OB-H1 confirms that a typed `/sc:implement` line reaches UserPromptSubmit as typed (V6). If it does not, register UserPromptExpansion and approve when `command_name` is exactly one of `sc:implement`, `implement`, `sc:task`, `task`, with no prefix stripping.
  8. Forgery: the agent cannot produce a prompt event; turn-starting tools are blocked before approval (Change 16) and input-injection tools always (Change 15); a harness-wrapped notification never equals the whole word `approved`.
- **Rationale**: V6 (VERIFIED) says typed slash lines reach UserPromptSubmit as typed, so the second event adds a registration and an unverified `command_name` form (U9) without adding a route (criterion: fewest edge cases). U-006 and C-006 unanimous on `.ok` at `worktree` only and ignoring `agent_id`.
- **Departs from**: (1) the C-005 majority (Advocates 1 and 3 kept UserPromptExpansion); decided by the criterion and listed as O-4. (2) INV-008's resolution says a typed `/sc:task` approves nothing; Change 14 makes `sc:task` an implement skill, so the command that it gates must also approve. `/task-builder` and `/tasks` still approve nothing, which is the part of INV-008 that matters.
- **Integration point**: section 6.
- **Risk**: Low.

### Group C: classification (governed sessions only; ordinary calls exit before this point)

### Change 9: One normalisation pass for Bash and Monitor text (merge of Variants 1 and 2, probe fixes)
- **Source**: Variant 2 section 8 character sweep; Variant 1 section 8 segment split; Round 2 C-007 (unanimous merge); INV-016, INV-022; orchestrator fact T5.
- **Target**: Base section 8, steps 1 and 2 (replace).
- **Settles**: C-007 (normalisation part), INV-016 (method part), INV-022.
- **Final rule**: the decoded `tool_input.command` of a Bash call (foreground or background) or a Monitor call is normalised once, in this order:
  - **N1.** If the command is longer than 65,536 bytes, the call gets class BIG and nothing else is checked (Change 22).
  - **N2.** Delete every `'`, `"` and `\` character. This mirrors how the shell joins quoted pieces: `g""it` becomes `git`, `\git` becomes `git`, `'feature:ma''in'` becomes `feature:main`, `feature:ma\in` becomes `feature:main`.
  - **N3.** Replace each run of `/` with one `/` and each `/./` with `/`. The result is text **T**, used by the tamper rule (Change 17).
  - **N4.** Remove redirections: an optional run of digits, then one of `&>>`, `&>`, `>>`, `>|`, `>&`, `<&`, `<<<`, `<<-`, `<<`, `>`, `<` (longest first). If the operator is followed by `&` plus digits or `-`, or ends in `&` and is followed by digits or `-` (as in `2>&1`, `>&2`, `>&-`), remove those too; otherwise also remove the next word (the file target, here-string or heredoc delimiter). Heredoc body lines stay and are scanned.
  - **N5.** Split into **segments** at newline, `;`, `&`, `|`, `(`, `)` and backtick.
  - **N6.** In each segment, replace every character outside `A-Za-z0-9._/=:@+~$-` with a space; the space-separated pieces are the segment's **words**, in order. `$` is kept, so a word such as `$cmd` can never equal a known subcommand.
  - **N7.** A word's **basename** is the text after its last `/`.
  - N5 and N6 run as `tr` calls over the whole text, never as bash pattern substitution (`${s//...}` took about 1.6 s on a 100 KB command, against 4 ms for `tr`; fact T5).
- **Rationale**: one deletion pass replaces Variant 1's word split on quotes (which missed `\git`, N-1) and INV-022's suggestion of scanning two forms; deletion matches shell semantics, so one form is enough. Redirection removal keeps `2>&1` and `> log` from being read as push refspecs, which would block the common `git push origin a:b 2>&1` at `full --submit`.
- **Departs from**: (1) INV-022's "apply the rules to both forms": one form is enough, as argued; (2) Variants 1 and 2 split segments on `{` and `}`; here they are swept to spaces (one separator list fewer; `${X}` still leaves the word `$`).
- **Integration point**: section 8, subsection "Normalisation".
- **Risk**: Medium. Redirection removal is the one step with real string handling; T-NRM cases (Change 27) pin it.

### Change 10: Git classification by allowlist (from INV-011, replacing the Round 2 denylist)
- **Source**: Variant 1 section 8 step 3 (option skip, `pull` as merge); Round 2 C-007, C-008, X-008 (unanimous Variant 1 for `pull`); INV-011, INV-017, INV-021, INV-034; orchestrator facts T2 and T4.
- **Target**: Base section 8, step 3 (replace).
- **Settles**: C-007 (git part), C-008, X-008, INV-011, INV-017, INV-021, INV-034 (git part).
- **Final rule**: in each segment, take every word whose basename is `git`, in order. The first such word in the segment is **first**; later ones are **later**.
  - **G1.** After the git word, a word starting with `-` is an option. The options `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`, `--config-env` and `--attr-source` also consume the next word (their `=` forms are one word). The first non-option word is the subcommand **S**; the words after it are its arguments.
  - **G2.** No S: class NONE if an option word is `--version`, `--help` or `-h`; otherwise UNKNOWN for a first word and NONE for a later word.
  - **G3.** Classes for S:
    - COMMIT: `commit`, `cherry-pick`, `revert`, `am`; and `update-ref` when an argument is `--stdin`, or when its first argument not starting with `-` (after skipping the value of `-m`) is `HEAD` or starts with `refs/heads/`. Any other `update-ref` is NONE (this keeps `/sc:implement`'s `refs/superclaude/implement/...` pins working, including the ones written through a shell variable).
    - MERGE: `merge`, `pull`.
    - PUSH: `push` (then Change 11).
    - NONE (allowlist): `add apply bisect blame branch cat-file check-attr check-ignore check-ref-format checkout clean count-objects describe diff diff-files diff-index diff-tree fetch for-each-ref format-patch fsck gc grep hash-object help log ls-files ls-remote ls-tree merge-base merge-tree mv name-rev range-diff read-tree rebase reflog reset restore rev-list rev-parse rm shortlog show show-branch show-ref stash status switch tag var version whatchanged write-tree`.
    - NONE only in a read form: `remote` when the next word is absent or is `-v`, `--verbose`, `get-url` or `show`; `config` when the next word is `--get`, `--get-all`, `--get-regexp`, `--list`, `-l`, `get` or `list`; `worktree` when the next word is `list`.
    - Anything else, including the write forms of `remote`, `config` and `worktree`: UNKNOWN for a first word, NONE for a later word.
  - **G4.** A later git word keeps every class except UNKNOWN. Real nested runs (`git rebase -x "git push origin main"`, `git bisect run git commit`) use gated subcommands and are still caught; prose inside a message (`git commit -m "fix git handling"`) is not blocked.
- **Consequences the spec must state**: aliases need no rule of their own. Git ignores an alias whose name is a built-in command (git-config documentation for `alias.*`), and any other alias name is not on the allowlist, so `git -c alias.ci=commit ci`, `X=commit git --config-env=alias.ci=X ci` and `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.ci GIT_CONFIG_VALUE_0=commit git ci` (all three commit on git 2.47.3, fact T2) are UNKNOWN; so is `git config alias.ci commit`. `git --attr-source HEAD push origin main` reads S = `push` (fact T4). `git $(echo push) ...`, `cmd=push; git $cmd ...` and `printf ... | xargs git` have S equal to `$`, `$cmd` or nothing, so they are UNKNOWN (INV-021). `git -C "/dir with space" push` reads S = `with` and is UNKNOWN, so this former gap now fails closed.
- **Rationale**: the orchestrator's instruction and INV-011 favour one allowlist over a growing denylist (aliases, `--config-env`, `GIT_CONFIG_*`, `--attr-source`, variable subcommands all fall to it without separate rules). INV-034: `cherry-pick`, `revert` and `am` create commits, so AC-2 needs them in COMMIT.
- **Departs from**: (1) the C-004 and C-008 consensus `alias.` token and `git config alias.` rule are dropped as subsumed; (2) INV-011 applied the allowlist to every git word; this plan applies UNKNOWN only to the first git word in a segment, to avoid blocking commit messages and PR bodies that mention git (criterion: fewer unwanted blocks, no AC lost because gated subcommands still classify everywhere); (3) INV-012's "block `-c`, `--config-env` and `GIT_CONFIG_` words in a push segment" is not taken, because Change 11's explicit-destination rule already defeats a configured push refspec.
- **Integration point**: section 8, subsection "Git".
- **Risk**: Medium. An allowlist that is too short blocks real work; the list was built from the git commands `/sc:implement` and `/sc:pr-submit` actually run (see Overview), and T-GIT-1 (Change 27) runs each of them.

### Change 11: Push rule: named destinations only (from Advocate 1 N-2 with Advocate 2 edits, INV-012)
- **Source**: Round 2 C-009 and X-007 (unanimous merge, rule N-2); Advocate 2 Round 2 section 2 edits; INV-012; orchestrator fact T3.
- **Target**: Base section 8, step 4 (replace, including the `symbolic-ref` subprocess).
- **Settles**: C-009, X-007, U-003 (remote part), A-008 (push part), INV-012.
- **Final rule**: for every PUSH from Change 10, at every level:
  1. Read the push arguments: words starting with `-` are options; `-o` and `--push-option` also consume the next word. The first non-option word is the **remote**; the remaining non-option words are **refspecs**.
  2. **Destination** of a refspec: remove one leading `+`; take the text after the last `:` if there is one, otherwise the whole word; remove one leading `refs/heads/` or `heads/`.
  3. Class PROTECTED if an option is `--all` or `--mirror`, or any destination is `master` or `main`.
  4. Class PUSHNAME if any of these holds: the remote is missing or is not exactly `origin`; there is no refspec; a refspec has no `:`; a destination is empty, `HEAD` or `@`; any push argument contains `$`; an option is `--repo`, `--receive-pack` or `--exec`, or starts with `--repo=`, `--receive-pack=` or `--exec=`.
  5. `--force`, `-f`, `--force-with-lease` and a leading `+` have no rule of their own (owner decision O-2).
  6. The hook never reads `cwd`, HEAD, `push.default` or configured refspecs, and runs no subprocess.
- **Consequences**: allowed at `full --submit`: `git push origin <sha>:<branch>` (the `/sc:pr-submit` form), `git push -u origin feature:feature`, `git push origin feature/main:feature/main`, `git push origin a:b 2>&1 | tail -5`. Blocked: a bare `git push`, `git push origin HEAD`, `git push origin feature` (no colon, so a configured `remote.origin.push` cannot redirect it, fact T3), `git push upstream a:b`, `git push origin a:$B`.
- **Rationale**: N-2 removes the `symbolic-ref` subprocess and every `cwd`, `-C` and `push.default` gap; NE-2 shows it admits the framework's only real submit push; T3 shows a no-colon refspec can land on `main`.
- **Departs from**: the Round 2 rule took the whole word as the destination when no `:` is present; INV-012 requires an explicit `:<destination>`, adopted here because it closes the configured-refspec route with no extra rule.
- **Integration point**: section 8, subsection "Push".
- **Risk**: Low. Cost: the agent must write pushes in one form; LL-PUSHNAME says which.

### Change 12: gh rule and the merge-URL rule (merge of Variants 1, 2, 3, probe fixes)
- **Source**: Variant 1 section 8 step 5; Variant 2 section 8 gh row; Variant 3 `gh pr ready`; Round 2 C-010 (unanimous merge, explicit `--repo` word, no name compared); NE-1; INV-013.
- **Target**: Base section 8, step 5 (replace).
- **Settles**: C-010, U-010, INV-013 (gh and URL part).
- **Final rule**: for every word whose basename is `gh`:
  - **H1.** The **group** is the first non-option word after `gh`, skipping the values of `-R` and `--repo`; the **action** is the next non-option word.
  - **H2.** Group `api`. The **path** is the first non-option word after `api`, skipping the values of `-X`, `--method`, `-H`, `--header`, `-f`, `-F`, `--field`, `--raw-field`, `--input`, `-q`, `--jq`, `-t`, `--template`, `--hostname`, `-p`, `--preview`, `--cache`. The call is a **write** when: for path `graphql`, some word, lower-cased, contains `mutation`; for any other path, a `-X` or `--method` value other than `GET` (any case) is given, or no method is given and one of `-f`, `-F`, `--field`, `--raw-field`, `--input` appears. A write is MERGE if some word, lower-cased, contains `merge`, `git/refs`, `updateref`, `createref`, `deleteref` or `createcommitonbranch`; any other write is SUBMIT; a read is NONE.
  - **H3.** Other groups. Action `merge`: MERGE. No group, with an option word `--version` or `--help`: NONE. No group otherwise, or a group not in {`pr`, `issue`, `repo`, `run`, `workflow`, `release`, `gist`, `label`, `search`, `status`, `auth`, `browse`, `secret`, `variable`, `cache`, `project`, `ruleset`, `org`, `codespace`, `attestation`, `ssh-key`, `gpg-key`, `config`, `completion`, `help`}: UNKNOWN (this covers `gh alias`, `gh extension` and every alias or extension command). Group `search`, `status`, `auth`, `browse`, `help` or `completion`, or action `view`, `list`, `status`, `diff`, `checks`, `watch` or `checkout`: NONE. Anything else: SUBMIT (this includes `gh pr create`, `gh pr edit`, `gh pr comment`, `gh pr ready`, `gh issue create`).
  - **H4.** Group `pr`, action `create`: also class REPO unless the segment has a word `-R` or `--repo`, or a word starting with `--repo=`. No repository name is compared, so `--repo "$REPO"` (the `/sc:pr-submit` form) passes.
  - **H5.** Merge URLs: in a segment with no gh word, any word that contains `repos/` and ends with `/merge` or `/merges` is MERGE (catches `curl`, `wget` and similar calls to the GitHub merge endpoints).
- **Consequences**: `gh pr view <N> --json mergeable,mergeStateStatus` and a GraphQL query that reads `mergeStateStatus` are reads (NONE); `resolveReviewThread` and REST comment replies are SUBMIT (allowed at `full --submit`); `gh api -X POST repos/o/r/merges`, `gh api graphql -f query='mutation{mergePullRequest(...)}'`, `enablePullRequestAutoMerge` and `gh api -X PATCH repos/o/r/git/refs/heads/main` are MERGE at every level.
- **Rationale**: NE-1 (name equality would block the skill's own `--repo "$REPO"`); INV-013 (`/merges`, GraphQL merge mutations and ref writes were open); `gh pr ready` in the submit class per Advocates 2 and 3 Round 2 (owner decision O-3).
- **Departs from**: INV-013 suggested "graphql whose body contains `merge`"; reads such as `mergeStateStatus` would then block `/sc:pr-submit`, so the merge words apply only to writes (mutations).
- **Integration point**: section 8, subsection "gh and GitHub URLs".
- **Risk**: Medium. A gh write the list does not foresee falls to SUBMIT (blocked below submit, allowed at submit), which is the safe side for every level except `full --submit`.

### Change 13: MCP tools (from Variant 1 section 9, narrowed per Advocates 2 and 3, INV-013)
- **Source**: Variant 1 section 9 MCP row; Round 2 C-013 (unanimous merge); INV-013.
- **Target**: Base section 9, MCP row (replace).
- **Settles**: C-013, U-004 (MCP part), INV-013 (MCP part).
- **Final rule**: for a tool whose name starts with `mcp__`, let N be the text after the last `__`, lower-cased.
  1. If N contains none of `merge`, `push`, `commit`, `pull_request`, `create_or_update_file`, `delete_file`, `update_ref`, `create_ref`, `create_branch`: NONE (explicit allow, in case the matcher lets other names through).
  2. If N starts with `list_`, `get_`, `search_` or `read_`: NONE.
  3. If N contains `merge`: MERGE.
  4. Otherwise: class MCP, blocked at every level (owner decision O-14). The agent uses `git` and `gh`, which the guard can check.
- **Rationale**: the read-prefix exception keeps `list_commits` and `get_commit` open (Advocates 2 and 3); blocking MCP writes at every level avoids parsing `branch` and `base` arguments, whose names are unverified (U12).
- **Departs from**: INV-013's "allow MCP writes at submit unless `branch` or `base` is `main`/`master`": argument parsing on unverified tool shapes adds edge cases; `/sc:pr-submit` does not use MCP.
- **Integration point**: section 9.
- **Risk**: Low.

### Change 14: Skill classification by normalised name (from INV-007, INV-033)
- **Source**: Variant 1 section 9 Skill row; Variant 2 section 9; INV-007, INV-033; orchestrator fact T1.
- **Target**: Base section 5 rows for Skill and section 9 Skill row (replace the literal name lists).
- **Settles**: INV-007, INV-033 (name part), U2, owner question O-8 of Variant 1 (`sc:task`).
- **Final rule**:
  1. Name = `tool_input.skill`, else `tool_input.name`. Absent or empty: class SKILL.
  2. Normalise: keep the text before the first whitespace; lower-case; remove one leading `/`; remove one leading `sc:` or `sc-`; remove one trailing `-protocol`.
  3. `implement` or `task`: IMPL. `pr-submit`: SUBMIT. `issue`: ESCAPE (a launched agent may not claim or launch another agent; WORKER-CONTRACT lists `/sc:issue` as never-as-worker). Anything else: NONE.
  4. So IMPL covers `sc:implement`, `sc:implement-protocol` (the name `/sc:implement` itself calls), `sc-implement-protocol`, `task`, `sc:task` and `sc:task-protocol`; SUBMIT covers `sc:pr-submit` and `sc:pr-submit-protocol`; `task-builder` and `sc:tasklist-protocol` stay NONE.
- **Rationale**: fact T1: the real skill names are `sc:implement-protocol`, `sc:pr-submit-protocol`, `task`, `sc:task-protocol`, so the variants' literal lists missed the name the model actually calls.
- **Integration point**: section 9, subsection "Skill".
- **Risk**: Low.

### Change 15: Escape routes (merge of Variants 1 and 2, probe allowlists)
- **Source**: Variant 1 section 8 step 6 and section 9; Variant 2 section 8 orca and claude rows; Round 2 C-014 (majority merge), U-002 part; INV-025, INV-026, INV-032.
- **Target**: Base section 8 step 6 and section 9 escape rows (replace).
- **Settles**: C-014, INV-025, INV-026, INV-032.
- **Final rule**: class ESCAPE for:
  1. Tools: `Agent` or `Task` whose `tool_input.isolation` is `remote`; `Workflow`; `RemoteTrigger`; `SendMessage`.
  2. Bash or Monitor words, by basename, in any segment:
     - `orca`: let w1 and w2 be the next two non-option words. NONE when the segment has a word `--help` or `-h`, or w1 is `status`, `help` or `--version`, or the pair w1 w2 is one of `worktree current`, `worktree list`, `worktree show`, `terminal list`, `terminal show`, `terminal read`, `orchestration check`, `orchestration inbox`, `orchestration run-current`, `orchestration task-list`, `orchestration worker-show`. Every other `orca` call is ESCAPE (this covers `agent launch`, `terminal send`, `computer type-text`, `automations run`, `orchestration send`, `orchestration dispatch`, `worktree create`).
     - a basename starting with `ccsession`: ESCAPE.
     - `claude` or `claude-code`: ESCAPE when a later word in the segment is one of `-p`, `--print`, `--continue`, `--resume`, `--bare`, `--settings`, `--dangerously-skip-permissions`, `--fork-session`, `--session-id`, `--permission-mode`.
     - `tmux`, `screen`, `xdotool`, `ydotool`: ESCAPE (they start terminal sessions or type into one).
  3. Local subagents (Agent or Task without `isolation: remote`) are allowed (Change 7).
- **Rationale**: allowlists for `orca` (INV-026: `computer type-text`, `automations run`, `orchestration send` were open under both blocklists) follow the same one-mechanism rule as git; `SendMessage` reaches other local sessions, which are ordinary (INV-032); `claude-code` covers `npx @anthropic-ai/claude-code -p` (INV-025); terminal tools close `tmux send-keys` and a flagless `claude` started inside tmux.
- **Departs from**: INV-025 asked for `-c` and `-r` in command position. A command-position rule is a parser fragment; `-c` and `-r` alone over-block `grep claude -c` and `grep claude -r`. An interactive `claude` without `-p` needs a terminal, which the Bash tool does not provide (UNVERIFIED, U14 in Change 31), and the terminal tools are blocked. Residual R5 (Change 32).
- **Integration point**: section 9, subsection "Escape routes".
- **Risk**: Low. Over-blocks: any `orca` write subcommand an Orca worker would need (owner decision O-11), and `grep tmux`-style mentions.

### Change 16: Turn starters (from Variant 1 section 9, INV-027, INV-028)
- **Source**: Variant 1 section 9 (Cron, ScheduleWakeup, Monitor scanned); Round 2 C-012 (unanimous Variant 1); INV-027, INV-028.
- **Target**: Base section 9 rows for CronCreate, ScheduleWakeup and Monitor (replace).
- **Settles**: C-012, INV-027, INV-028.
- **Final rule**:
  1. Class TURN: a tool whose name matches `^Cron[A-Za-z]*$` or `^Schedule[A-Za-z]*$`; the tool `Monitor` (any input); a `Bash` call whose `tool_input.run_in_background` is `true`.
  2. TURN is blocked only at `W` (worktree before approval), where an approval can still be forged; it is allowed at `WA`, `F` and `FS` (Change 19).
  3. The `command` of a Monitor call and of a background Bash call is always normalised and classified like a foreground Bash command (Changes 9 to 17). A Monitor call with only `ws` has no text to scan.
  4. `RemoteTrigger` and `Workflow` are ESCAPE at every level (Change 15), not TURN.
- **Rationale**: INV-027 (each Monitor line and each background-task notice starts a turn whose text the agent chose; whether it is wrapped is U4); INV-028 (approval exists only at `worktree`, and `/sc:pr-submit --monitor` at `full --submit` needs a wait tool).
- **Departs from**: the C-012 consensus blocked Cron and Schedule at every level; narrowed to `W` because blocking them elsewhere protects nothing and breaks the submit flow.
- **Integration point**: section 9, subsection "Turn starters".
- **Risk**: Low.

### Change 17: Tamper rule (merge of Variants 1 and 2, probe fixes)
- **Source**: Variant 1 sections 8 step 7 and 5; Variant 2 section 4 tamper rule; Round 2 C-004 (unanimous merge), X-005, X-006 (merge); U-005; INV-009, INV-010, INV-030.
- **Target**: Base section 8 step 7 and section 4 D2 paragraph (replace).
- **Settles**: C-004, X-005, X-006, U-005, INV-009, INV-010, INV-030.
- **Final rule**: in a governed session only, class TAMPER when:
  1. Text T of a Bash or Monitor command (Change 9 N3), or a path field (`tool_input.file_path` or `tool_input.notebook_path`) of Edit, Write or NotebookEdit after the same `/` squeezing, contains one of: `.claude/state/launch-level` (the script builds this token from two parts, Change 4), `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`.
  2. Bash or Monitor only: a word (Change 9 N6) that ends with `.claude` or `.claude/`; a segment that has a word `superclaude` followed later by a word `install`; any word containing `install_hooks`.
  3. Edit, Write or NotebookEdit only: a path that contains a `/../` segment or ends in `/..` (these tools take absolute paths, so a real edit never needs one).
  4. Never checked: Write or Edit content, Agent prompts, Skill arguments, MCP inputs. Values are decoded by `jq`, so JSON `\/` escapes need no rule.
  5. Ordinary sessions never reach this rule.
- **Consequences**: blocked in a governed session: an Edit of `~/.claude/settings.json` (V11 `disableAllHooks` route), `rm -rf ~/.claude/state/launch-level`, `cd ~/.claude && : > hooks/launch-level-guard.sh`, `/home/u/.claude//settings.json`, `uv run superclaude install` (which copies hook scripts to `~/.claude/hooks/` and merges registrations into `~/.claude/settings.json`, `install_hooks.py` docstring). Allowed: a Bash or Edit naming `src/superclaude/hooks/scripts/launch-level-guard.sh` or a worktree path containing `hook-launch-level-394`; a Write whose content quotes `CLAUDE.md` lines about `.claude/hooks`. Accepted over-block: `git add .claude/settings.json` and an Edit of the tracked project `.claude/settings.json` in a governed session (R8).
- **Rationale**: X-006 (V11 makes the settings edit a real route); X-005 (governed-only, or a person releasing a session from their own Claude session is blocked); INV-009 (`//` paths and a `cd` split); INV-010 (reinstalling the guard).
- **Departs from**: (1) the `launch-level-guard` token (Variant 1) is not used, per A1 Round 2 concession 7; (2) INV-009 suggested also the token `hooks/launch-level-guard` and `realpath -m`; the "word ends with `.claude`" rule covers the `cd` split, and blocking `..` segments replaces `realpath` (not on every host); (3) the `alias.` token of C-004 is subsumed by Change 10.
- **Integration point**: section 8, subsection "Tamper", and a short pointer from section 4.
- **Risk**: Low.

### Change 18: Coverage of the remaining tools (from Variant 1 section 9)
- **Source**: Variant 1 section 9 table; Variant 2 section 9; Variant 3 section 9.
- **Target**: Base section 9, rows for Edit, Write, NotebookEdit and read tools (replace).
- **Settles**: D5 rows not covered by Changes 13 to 16; INV-033 (statement part).
- **Final rule**:
  1. Read, Grep, Glob, WebFetch, WebSearch, TodoWrite, the `Task*` family other than `Task`, and every tool name outside the matcher (Change 24) never start the hook.
  2. Edit, Write, NotebookEdit: only the tamper check (Change 17). Source edits at `worktree` are not gated (owner decision O-8; the write boundary is issue #322). The spec states in section 6: "AC-1's stop at an approved plan is enforced at the command level (`/sc:implement`, `/task`, `/sc:task` and their skills), not at the file level."
  3. A tool name that reaches the hook and no rule in Changes 10 to 17 classifies gets class NONE on an explicit allow path.
  4. `@file` mentions start no tool call (V12); reading is never gated.
- **Rationale**: all three variants allow source edits at `worktree`; INV-033 asks the spec to say that the plan stop is command-level.
- **Integration point**: section 9.
- **Risk**: Low.

### Group D: policy and failure

### Change 19: Classes, policy table and precedence (Variant 1 closed list, Variant 2 flat script, Variant 3 oracle)
- **Source**: Variant 1 section 3 (closed class list, literal policy block), section 5 (precedence line); Variant 2 section 5 ("the table is the test data"); Round 2 S-004 (majority merge), S-003 (unanimous merge); U-002; INV-039 (order part).
- **Target**: Base section 3 "Action classes" and section 5 precedence line (replace).
- **Settles**: S-004, U-002, INV-039 (precedence part).
- **Final rule**:
  1. Closed class list: NONE, IMPL, SUBMIT, REPO, COMMIT, PUSH, PUSHNAME, PROTECTED, MERGE, UNKNOWN, MCP, ESCAPE, TURN, TAMPER, SKILL, BIG.
  2. Policy (B = block with the message id of Change 23, A = allow):

     | Class | W | WA | F | FS | Message id |
     |---|---|---|---|---|---|
     | NONE | A | A | A | A | none |
     | IMPL | B | A | A | A | LL-IMPL |
     | SUBMIT | B | B | B | A | LL-SUBMIT |
     | REPO | B | B | B | B | LL-REPO |
     | COMMIT | B | B | B | A | LL-COMMIT |
     | PUSH | B | B | B | A | LL-PUSH |
     | PUSHNAME | B | B | B | B | LL-PUSHNAME |
     | PROTECTED | B | B | B | B | LL-PROTECTED |
     | MERGE | B | B | B | B | LL-MERGE |
     | UNKNOWN | B | B | B | B | LL-UNKNOWN |
     | MCP | B | B | B | B | LL-MCP |
     | ESCAPE | B | B | B | B | LL-ESCAPE |
     | TURN | B | A | A | A | LL-TURN |
     | TAMPER | B | B | B | B | LL-TAMPER |
     | SKILL | B | B | B | A | LL-SKILL |
     | BIG | B | B | B | B | LL-BIG |

  3. One call can collect several classes (several segments, several git words). It is blocked if any of its classes is blocked at the effective level. The message shown is the first blocked class in this precedence order: BIG, TAMPER, MERGE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHNAME, COMMIT, TURN, IMPL, SKILL. (SUBMIT before REPO and PUSH before PUSHNAME, so below `full --submit` the agent reads "needs --submit", not "fix the form".)
  4. The script holds the policy as one literal `case` table on `CLASS:LEVEL`. It has no `--classify` argument, no ERR trap and no layers; it is one flat file.
  5. The test file holds its own independent copy of this grid as the expected result (the oracle) and a test that every class has a cell for every level (Change 26). The test never reads the grid from the script.
- **Rationale**: S-004 majority (flat script, policy as literal data, independent oracle, no `--classify`, no ERR trap); Variant 1's precedence line, which the merged Round 2 rules did not restate (INV-039).
- **Integration point**: section 5 (policy and precedence) and section 3 (one line pointing to section 5).
- **Risk**: Low.

### Change 20: The decision table (merge of the three variants' tables)
- **Source**: Variant 1 section 5; Variant 2 section 5 (failure row); Variant 3 section 5 (literal commands, over-match row); Round 2 S-003 (unanimous merge).
- **Target**: Base section 5, the table (replace).
- **Settles**: S-003; the "decision table" deliverable; AC-1, AC-2, AC-6 rows.
- **Final rule**: section 5 carries this table. Columns: `W` worktree before approval, `WA` worktree after approval, `F` full, `FS` full with `--submit`. Every row applies to a governed session; in an ordinary session every row is ALLOW with no output (exit 0).

  | # | Tool call pattern (literal examples) | Class | W | WA | F | FS |
  |---|---|---|---|---|---|---|
  | 1 | Read, Grep, Glob, WebFetch, TodoWrite, TaskCreate (not matched) | n/a | ALLOW | ALLOW | ALLOW | ALLOW |
  | 2 | Edit, Write, NotebookEdit on an ordinary path (`/repo/src/x.py`, `/repo/.dev/tasks/plan.md`) | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 3 | Edit, Write, NotebookEdit on `~/.claude/settings.json`, `~/.claude/hooks/x.sh`, the store, `~/.gitconfig`, `/repo/.git/config`, or a path with a `..` segment | TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER |
  | 4 | Skill `sc:implement`, `sc:implement-protocol`, `sc-implement-protocol`, `task`, `sc:task`, `sc:task-protocol` | IMPL | BLOCK LL-IMPL | ALLOW | ALLOW | ALLOW |
  | 5 | Skill `sc:pr-submit`, `sc:pr-submit-protocol` | SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
  | 6 | Skill `sc:issue`, `sc:issue-protocol` | ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
  | 7 | Skill call with neither `skill` nor `name` | SKILL | BLOCK LL-SKILL | BLOCK LL-SKILL | BLOCK LL-SKILL | ALLOW |
  | 8 | Other Skill (`sc:workflow`, `sc:load`, `task-builder`) | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 9 | Agent or Task, local (`isolation` absent or `worktree`) | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 10 | Agent or Task with `isolation: "remote"`; Workflow; RemoteTrigger; SendMessage | ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
  | 11 | CronCreate, CronDelete, CronList, ScheduleWakeup; Monitor; Bash with `run_in_background: true` | TURN (plus the scan of any command) | BLOCK LL-TURN | ALLOW, command scanned | ALLOW, command scanned | ALLOW, command scanned |
  | 12 | `git status`, `git diff`, `git log --grep push`, `git add -A`, `git stash`, `git rebase origin/master`, `git fetch origin`, `git remote get-url origin`, `git merge-tree a b`, `git update-ref refs/superclaude/implement/p/T1 <sha>` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 13 | `git commit -m x`, `git commit --only -- a b`, `git cherry-pick x`, `git revert x`, `git am p.patch`, `git update-ref refs/heads/f <sha>`, `git update-ref HEAD <sha>` | COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | ALLOW |
  | 14 | `git push origin <sha>:feature`, `git push -u origin feature:feature`, `git push origin a:b 2>&1` | PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | ALLOW |
  | 15 | `git push`, `git push origin`, `git push origin feature`, `git push origin HEAD`, `git push origin x:@`, `git push upstream a:b`, `git push --repo=x a:b`, `git push origin a:$B`, `--receive-pack`, `--exec` | PUSH, PUSHNAME | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSHNAME |
  | 16 | `git push origin main`, `x:main`, `x:refs/heads/master`, `x:heads/main`, `+main`, `:main`, `--all`, `--mirror`, `git --attr-source HEAD push origin main` | PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED |
  | 17 | `git merge x`, `git pull`, `git -c merge.conflictStyle=zdiff3 merge --no-commit --no-ff <sha>`, `gh pr merge 5`, `gh api -X POST repos/o/r/merges`, `gh api graphql -f query='mutation{mergePullRequest(...)}'`, `gh api -X PATCH repos/o/r/git/refs/heads/main`, `curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge`, MCP `merge_pull_request` | MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE |
  | 18 | `git ci`, `git -c alias.ci=commit ci`, `X=commit git --config-env=alias.ci=X ci`, `git $(echo push) origin a:b`, `cmd=push; git $cmd`, `printf x \| xargs git`, `git notes add`, `git worktree add`, `git remote set-url origin u`, `git config alias.ci commit`, `git commit-tree t`, `gh alias set co 'pr merge'`, `gh co 5` | UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN |
  | 19 | `gh pr view 5 --json mergeable`, `gh issue view 5`, `gh pr checks 5`, `gh repo view`, `gh api repos/o/r/pulls/5`, `gh api graphql -f query='query{...mergeStateStatus...}'` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 20 | `gh issue create`, `gh pr comment 5`, `gh pr edit 5`, `gh pr ready 5`, `gh api --method POST repos/o/r/pulls/5/comments/1/replies -f body=x`, `gh api graphql -f query='mutation{resolveReviewThread(...)}'` | SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
  | 21 | `gh pr create --repo "$REPO" --base master --head f`, `gh pr create -R o/r ...` | SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
  | 22 | `gh pr create --title x` (no `--repo` or `-R`) | SUBMIT, REPO | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-REPO |
  | 23 | MCP `push_files`, `create_or_update_file`, `create_pull_request` | MCP | BLOCK LL-MCP | BLOCK LL-MCP | BLOCK LL-MCP | BLOCK LL-MCP |
  | 24 | MCP `list_commits`, `get_commit` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 25 | `claude -p x`, `/usr/local/bin/claude --print x`, `npx @anthropic-ai/claude-code -p x`, `ccsession-orca x`, `orca agent launch ...`, `orca terminal send ...`, `orca computer type-text approved`, `tmux send-keys approved Enter`, `screen -X stuff x`, `xdotool type approved` | ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
  | 26 | `orca worktree current`, `orca status`, `orca terminal read`, `grep -rn claude docs/`, `grep claude -rn docs/` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 27 | `cat ~/.claude/state/launch-level/sessions/x`, `rm -rf ~/.claude/state/launch-level`, `echo '{"disableAllHooks":true}' > ~/.claude/settings.json`, `cd ~/.claude && : > hooks/x.sh`, `uv run superclaude install`, `cat ~/.gitconfig` | TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER | BLOCK LL-TAMPER |
  | 28 | Bash or Monitor command longer than 65,536 bytes | BIG | BLOCK LL-BIG | BLOCK LL-BIG | BLOCK LL-BIG | BLOCK LL-BIG |
  | 29 | Other Bash (`make test`, `uv run pytest`, `ls -la`) | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 30 | Pinned over-match: `echo "git commit"` | COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | ALLOW |
  | 31 | Pinned over-match: `echo "use git for x"`, `grep -rn "git worktree" docs/` | UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN |
  | 32 | Pinned over-match: `git commit -m "explain git push"` | COMMIT, PUSH, PUSHNAME | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSHNAME |
  | 33 | Pinned gaps (Change 32): `$GIT push origin main`; `bash ./push.sh` where `push.sh` was written with Write | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 34 | Prompt typed by a person: `approved`, `/sc:implement x`, `/sc:task x`, `/task x` | prompt event | ALLOW, writes `.ok` | ALLOW | ALLOW, writes nothing | ALLOW, writes nothing |
  | 35 | Prompt with a launch marker in an unbound session | prompt event | binds the record's level, or `degraded`; on failure BLOCK LL-NOBIND (Change 5) | n/a | n/a | n/a |
  | 36 | `jq` missing; input not JSON | failure | BLOCK LL-BROKEN | BLOCK LL-BROKEN | BLOCK LL-BROKEN | BLOCK LL-BROKEN |
  | 37 | Session file empty, unreadable, `degraded` or an unknown word; `session_id` missing or invalid while the store holds a session | failure | the W column, plus the LL-STATE note | (WA if `.ok` exists) | n/a | n/a |
  | 38 | Internal error (a failed `tr`, an unexpected exit code) | failure | BLOCK LL-BROKEN | BLOCK LL-BROKEN | BLOCK LL-BROKEN | BLOCK LL-BROKEN |

- **Rationale**: one row per AC-relevant pattern with literal commands (Variant 3), generic rows and failure rows (Variants 1 and 2), the pinned over-match (U-010). The test oracle (Change 26) is this table, copied, not read.
- **Integration point**: section 5.
- **Risk**: Low. The table is derived from Changes 9 to 19; T-GRID checks that the script agrees with it.

### Change 21: Fail-closed rules (from Variants 1 and 2, INV-031)
- **Source**: Variant 1 section 10 failure table; Variant 2 section 10 default deny; Round 2 C-015 (unanimous merge), X-002 (majority merge), X-003 (unanimous Variant 1); INV-031.
- **Target**: Base section 10, "Governed path" and failure table (replace).
- **Settles**: C-015, X-002, X-003, A-005 (hook part), INV-031.
- **Final rule**:
  1. Ordinary sessions are never blocked by a failure: every failure before identity is known exits 0, except where a bound id or a launch marker is seen (Change 5 U3, Change 6 P4).
  2. Default deny once governed: the script's last line prints LL-BROKEN and exits 2. Allowing takes an explicit `exit 0` on a named path.
  3. After a call is known to be governed (Change 6 P7), and in the prompt branch once a marker is present (Change 5 U6), an EXIT trap turns any exit code other than 0 or 2 into a printed LL-BROKEN (LL-NOBIND in the prompt branch) and exit 2. The script uses `set -u` and `set -o pipefail`, not `set -e`, and no ERR trap.
  4. The exit status of every `jq` and `tr` call is checked; a failure prints LL-BROKEN and exits 2.
  5. Failure table (governed session unless stated):

     | Failure | Result |
     |---|---|
     | `jq` missing, ordinary session | exit 0 (Change 6 P3) |
     | `jq` missing, bound id in the input | BLOCK LL-BROKEN on every matched call; Read, Grep and Glob are never matched, so reading still works |
     | `jq` missing, launch marker in a prompt | BLOCK LL-NOBIND |
     | input not JSON | ordinary exit 0; governed BLOCK LL-BROKEN |
     | session file empty, unreadable, `degraded`, unknown word | level `worktree` plus LL-STATE; `.ok` still counts |
     | `session_id` missing or invalid while the store holds a session | level `worktree` plus LL-STATE |
     | Skill name unreadable | class SKILL |
     | command over 65,536 bytes | class BIG |
     | `tr` failure or other internal error | BLOCK LL-BROKEN |
     | bind failure (`mkdir`, `mv`, write) | BLOCK LL-NOBIND on the prompt |
     | hook killed at its timeout | the call goes ahead (V8); residual R2 |
     | session file deleted | the session reads as ordinary; this is also the release route; residual R3 |

  6. `onFailure: "block"` is not set on either registration: it would block ordinary sessions whenever the hook breaks (V8).
- **Rationale**: X-002 (V8 does not force fail-open; a governance hook that exits 0 when it cannot judge is silent non-enforcement); X-003 (degrading to `worktree` keeps planning and approval working); INV-031 (the trap and the default-deny line must print a message, or AC-7 fails).
- **Integration point**: section 10.
- **Risk**: Low.

### Change 22: Command size cap, timeout and speed budget (from Variant 3 section 10, Variant 1 section 10, probe fixes)
- **Source**: Variant 3 section 10 (p95, 100 runs, ratio guard); Variant 1 section 10 absolute limits; Round 2 C-017 (majority Variant 3); U-009; INV-016, INV-018, INV-040.
- **Target**: Base section 10, "Budget" paragraph (replace).
- **Settles**: C-017, U-009, INV-016 (cap), INV-018, INV-040 (speed part).
- **Final rule**:
  1. Size cap: in a governed session a Bash or Monitor command longer than 65,536 bytes is class BIG (Change 9 N1). Ordinary sessions have no cap.
  2. Timeout: 5 seconds on both registrations (Change 24). One value, stated once.
  3. Subprocesses: at most one `jq` per call that passes the prefilter, `tr` only for Bash and Monitor text in governed sessions, and `mkdir`, `mv`, `touch`, `rm` only on prompt events. No git, no network, no Python.
  4. Budget, measured by the T-SPD cases of Change 27 with 100 real subprocess runs each (helper `time.monotonic()`, as in `tests/hooks/test_block_bare_python.py`); every test prints its measured numbers:
     - ordinary session, empty store: median at most 20 ms, p95 at most 50 ms;
     - ordinary session, store holding 1,000 session files and 50 pending files: the same limits;
     - ordinary median at most 1.5 times the median of `block-bare-python.sh` on the same Bash payload in the same run;
     - governed allow (`git status`) and governed block (`git commit -m x` at `F`): p95 at most 60 ms;
     - governed 65,536-byte realistic command (heredoc-like text with git words) and a 1 MB command: every run under 1 second, one fifth of the timeout.
- **Rationale**: T-SPD-3's same-run ratio catches regressions that absolute limits miss on fast CI (all three advocates); INV-002 and INV-016 require the stale-store and large-command cases; INV-018 requires one fixed timeout.
- **Departs from**: INV-018 suggested 3 s. 5 s gives slow hosts more margin before V8 lets a governed call through, and the 1 s assertion keeps the real cost far below either value.
- **Integration point**: section 10, subsection "Speed".
- **Risk**: Medium. Absolute millisecond limits can be flaky on loaded CI; the ratio test is the regression guard, the absolute limits are the second check.

### Change 23: Block messages (Variant 1 coverage in Variant 2's three-line shape)
- **Source**: Variant 1 section 11 ids; Variant 2 section 11 three-line wording; Round 2 C-018 (merge, residual split on the issue number), S-006 (merge); INV-031, INV-039.
- **Target**: Base section 11 (replace).
- **Settles**: C-018, S-006, INV-039, AC-7.
- **Final rule**:
  1. Every block prints to stderr, then exits 2. Shape:
     ```
     Launch-level guard: this session was started by /sc:issue --claim at level {level}.
     Blocked: <what>
     Why: <why>
     You can: <next step>
     [Note: ...]   (zero, one or two lines)
     ```
     `{level}` renders as `worktree`, `worktree (approved)`, `full` or `full --submit`. LL-NOBIND and LL-BROKEN use the first line `Launch-level guard:` with no level when the level is unknown. No issue number (owner decision O-5).
  2. Messages (the only template variables are `{level}`, `{store}` and `{sid}`; text in angle brackets is literal instruction text):

     | Id | Blocked: | Why: | You can: |
     |---|---|---|---|
     | LL-IMPL | starting /sc:implement or /task (or their skills). | At the worktree level the agent stops at a plan until a person approves it. | Read the plan, then type /sc:implement or /task, or reply approved, in this session. |
     | LL-COMMIT | creating a commit (git commit, cherry-pick, revert, am, or moving a branch with update-ref). | Only a launch with --pipeline full --submit lets the agent commit. | Review the changes and commit them yourself, or claim the issue again with --pipeline full --submit. |
     | LL-PUSH | a git push. | Only a launch with --pipeline full --submit lets the agent push. | Push the branch yourself after review, or claim the issue again with --pipeline full --submit. |
     | LL-PUSHNAME | a push that is not written as git push origin <source>:<branch>. | At this level the agent may push only a named feature branch to origin; other forms can reach another remote or the main branch. | Retry as git push origin <source>:<feature-branch>, with both names written out (no variables). |
     | LL-PROTECTED | a push to master or main, or a push of every branch (--all, --mirror). | No launch level may change the main branch. | Push the feature branch by name, then merge it through a reviewed pull request. |
     | LL-MERGE | a merge (git merge, git pull, gh pr merge, a GitHub merge or branch-write API call, or an MCP merge tool). | No launch level may merge; only a person reviews and merges. | Leave the merge to a person. To update the branch, run git fetch, then git rebase. |
     | LL-SUBMIT | /sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue, or a gh api write). | Publishing work needs a launch with --pipeline full --submit. | Run it yourself in your own session, or claim the issue again with --pipeline full --submit. |
     | LL-REPO | gh pr create without --repo. | Without --repo, gh can open the pull request on the parent repository of a fork. | Retry with --repo <owner>/<name> (or -R). |
     | LL-UNKNOWN | a git or gh command the guard does not recognise. | In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge. | Use the standard command (for example git status, git diff, git add), or ask the person to run it. |
     | LL-MCP | a GitHub write through an MCP tool. | The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh. | Use git or gh for this step. |
     | LL-ESCAPE | starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool). | That work would run outside this session's launch level. | Do the work here (local subagents are allowed), or ask the person to start it. |
     | LL-TURN | scheduling a turn, or starting a background task or monitor, before the plan is approved. | Its output arrives as a new turn and could look like a person replying approved. | Run the command in the foreground, or wait until the person approves the plan. |
     | LL-TAMPER | touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks. | The session must not change its own limits. | Ask the person. To release this session they run, in their own terminal: rm "{store}/sessions/{sid}" "{store}/sessions/{sid}.ok" |
     | LL-SKILL | a skill call whose name the guard cannot read. | The guard cannot tell whether the skill is allowed at this level. | Report it (the hook input format may have changed); the person can release the session. |
     | LL-BIG | a command longer than 64 KB. | The guard cannot check a command that long in time. | Write the content to a file with the Write tool, then run a short command. |
     | LL-BROKEN | this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error). | In a launched session the guard fails closed. | Install jq, or ask the person to release the session by deleting its files in {store}/sessions/. |
     | LL-NOBIND | this launch prompt. | The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced. | Check that jq is installed and {store} is writable, then claim the issue again. |

     When `{sid}` is not a valid id (Change 6 P6), LL-TAMPER uses the LL-BROKEN wording "deleting its files in {store}/sessions/".
  3. Notes, appended after "You can:":
     - **LL-STATE**: `Note: the launch record was missing or unreadable, so the strictest level (worktree) applies.` Added to every block in a session whose level came from an invalid word or an invalid `session_id` (Change 4 item 3, Change 6 P6).
     - **LL-TEXT**: `Note: the guard reads command text. If the command only mentions this action inside a message, write the text to a file and pass it with -F <file> or --body-file <file>.` Added to every block whose class came from Bash or Monitor text.
  4. Which message is shown when several classes block: Change 19 item 3.
- **Rationale**: AC-7; Variant 1 covers more cases, Variant 2's three labelled lines are the clearest; INV-039 (messages may use only data the one-word state holds; LL-REPO no longer needs a stored repo); INV-031 (the trap path prints LL-BROKEN). LL-TEXT is the documented way around the accepted over-match (A12), so no message parser is needed.
- **Departs from**: Advocate 1 wanted the issue number in the header (C-018 residual split); the one-word state does not carry it (owner decision O-5).
- **Integration point**: section 11.
- **Risk**: Low.

### Group E: registration and interfaces

### Change 24: Registration (from Variant 2 section 3, anchored per Advocate 2 E1)
- **Source**: Variant 1 section 3 (three events, timeout 5); Variant 2 section 3 (matcher, two events); Round 2 C-011 (unanimous merge, anchored matcher); NE-4; INV-018, INV-032, INV-036.
- **Target**: Base section 3, `hooks.json` row, and a new subsection "Registration" in section 3.
- **Settles**: C-011, INV-018 (value), INV-032 (matcher part), INV-036 (matcher part).
- **Final rule**:
  1. Append to the `UserPromptSubmit` array of `src/superclaude/hooks/hooks.json`:
     ```json
     {
       "hooks": [
         { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 }
       ]
     }
     ```
  2. Append to the `PreToolUse` array:
     ```json
     {
       "matcher": "^(Bash|Skill|Agent|Task|Edit|Write|NotebookEdit|Monitor|Workflow|RemoteTrigger|SendMessage|Cron[A-Za-z]*|Schedule[A-Za-z]*)$|^mcp__.*(merge|push|commit|pull_request|create_or_update_file|delete_file|update_ref|create_ref|create_branch)",
       "hooks": [
         { "type": "command", "command": "~/.claude/hooks/launch-level-guard.sh", "timeout": 5 }
       ]
     }
     ```
  3. No UserPromptExpansion entry (owner decision O-4), no SessionStart entry, no `onFailure` key.
  4. Add the string `"launch-level-guard.sh"` to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py`. The script file is executable, like the other scripts in `src/superclaude/hooks/scripts/`.
  5. Run `make sync-dev`, then `make verify-sync`. Stage only `src/` and `tests/` files; never stage `.claude/` mirrors.
  6. Event dispatch inside the script: if the raw input contains the text `"tool_name"` (a JSON key; inside a JSON string every `"` is escaped, so prompt text cannot fake it), run the PreToolUse branch (Change 6); otherwise run the UserPromptSubmit branch (Change 5). Nothing depends on `hook_event_name`.
  7. The script re-checks every tool name itself (Changes 13 and 18), so if the harness ignored the anchors the only cost would be speed, never a wrong decision.
- **Rationale**: an unanchored regex matcher would match `TaskCreate`, `TaskUpdate` and every other name containing a listed word (Advocate 2 E1); `SendMessage` reaches other local sessions (INV-032); one timeout value (INV-018).
- **Integration point**: section 3.
- **Risk**: Medium. That the harness honours `^` and `$` inside a matcher is unverified (U15); OB-H1 item 6 checks it.

### Change 25: Interface requests to the claim feature (from Variant 2 C1 to C3, Variant 1 R1 to R3, probe fixes)
- **Source**: Variant 2 section 3 (C1 to C3, claim refuses without `jq`); Variant 1 section 4 (R1, R2); seed brief R1 to R4; Round 2 A-003 (made concrete by Advocate 2); INV-004, INV-005.
- **Target**: Base section 3, new subsection "Interface requests to the claim feature" (replace the R1 to R3 mentions in sections 4 and 14; the ids CL-1 to CL-6 replace R1 to R3, so they no longer collide with residual ids).
- **Settles**: A-003, A-005 (claim part), A-006, U-007, INV-004 (interface part), INV-005.
- **Final rule** (requests only; the claim feature builds them in its own sprint):
  - **CL-1** Before `orca agent launch`, write `$HOME/.claude/state/launch-level/pending/<nonce>` holding one line with one word: `worktree`, `full` or `full-submit`. `--pipeline none` writes nothing. Write atomically: `umask 077`, `mkdir -p`, write a temporary file in `pending/` whose name starts with `.`, then rename it.
  - **CL-2** The nonce is `secrets.token_hex(16)` (32 lowercase hex characters), new for every launch. The launch `--prompt` begins with `[sc-launch:v1:<nonce>]`, one space, then the existing instruction sentence (FR-23 forbids only a leading `/`).
  - **CL-3** `pipeline.json` stays documentation only; the hook never reads it. Amend FR-31 to say so.
  - **CL-4** Refuse to launch, and write no record, unless all three hold: `jq` is on `PATH`; `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable; the settings file the launched session will load, `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json`, registers that script under both `UserPromptSubmit` and `PreToolUse`. The refusal names what is missing and says to run `superclaude install`.
  - **CL-5** A re-claim always starts a new session with a new nonce. It never uses `--resume` on a governed session to change its level.
  - **CL-6** The claim output tells the person that the session is released by deleting its files in `$HOME/.claude/state/launch-level/sessions/` (block messages print the exact command).
- **Rationale**: A-003 (a launch whose guard is not installed runs ungoverned with no warning); INV-005 (another config dir loads different settings); INV-004 (a resumed session would ignore the new marker); A-006 (the claim script and the hook must agree on `$HOME`; a mismatch makes the record invisible, which Change 5 turns into a degraded bind rather than an ungoverned one).
- **Integration point**: section 3, after "Registration".
- **Risk**: Low for this spec; the claim feature owns delivery.

### Group F: proof

### Change 26: Test harness, oracle and fixtures (Variant 3 literal payloads, Variant 2 table-as-data)
- **Source**: Variant 3 section 12; Variant 2 section 12; Variant 1 section 12 fixtures; Round 2 C-019 (unanimous merge), X-010 (`manual` marker); INV-040.
- **Target**: Base section 12, first paragraph (replace).
- **Settles**: C-019, X-010 (marker part), INV-040 (fixture part).
- **Final rule**:
  1. One file, `tests/hooks/test_launch_level_guard.py`. Every case runs the real script `src/superclaude/hooks/scripts/launch-level-guard.sh` with `subprocess.run(["bash", HOOK], input=<json bytes>, env={"HOME": str(tmp_path), "PATH": <controlled>})` and asserts the exit code and stderr text, as `tests/hooks/test_block_bare_python.py` does.
  2. Helpers: `bind(home, sid, word)` writes `sessions/<sid>` directly; `launch(home, sid, word)` writes `pending/<nonce>` and sends the marker prompt through the script; `approve(home, sid)` sends `approved`; `pre(tool_name, tool_input, sid, **extra)` and `prompt(text, sid, agent_id=None)` build payloads; `path_without(name)` builds a temporary `PATH` directory of symlinks to `bash` and the coreutils the script uses, minus `jq` or minus `tr`; `ob_h1(name)` loads a captured payload.
  3. Oracle: a literal table `EXPECTED` in the test file, one entry per row of the Change 20 table with literal JSON payloads and the expected exit code and message id per level. It is written by hand from the spec, never read from the script.
  4. Observed checks appear as tests whose body is `pytest.skip("observed check OB-H<n>: see spec section 12")`. No `@pytest.mark.manual`: `pyproject.toml` sets `--strict-markers` and registers no such marker.
  5. Captured OB-H1 payloads live in `tests/hooks/fixtures/launch_level/ob_h1/`, with tokens and personal paths removed. Subagent and nested-subagent tests (T-ISO-7, T-ISO-8) load them; until OB-H1 runs, they use hand-written shapes and say "pending OB-H1" in their docstring.
- **Rationale**: Variant 3's literal payloads and Variant 2's "the table is the test data", with Advocate 2's point that a test must not read its expected values from the code it checks.
- **Integration point**: section 12, "Harness".
- **Risk**: Low.

### Change 27: Named test cases (all variants, probe cases added)
- **Source**: Variant 1 section 12 groups; Variant 3 T-* ids; Advocate 3 Round 2 named cases; the "Test" suggestions of every INV finding.
- **Target**: Base section 12, the group table (replace).
- **Settles**: C-019 (case list), INV-035, INV-037 (test part), every INV row's test (see the probe disposition table).
- **Final rule**: section 12 lists these cases. Each name is a pytest function; a range like `T-SPD-1..5` is one function per id.

  | Id | Function | Asserts |
  |---|---|---|
  | T-ISO-1 | `test_ordinary_session_never_blocked` | every oracle payload with an unbound id exits 0 with empty stderr, with an empty store and with a store holding other sessions |
  | T-ISO-2 | `test_two_sessions_isolated` | ids A (`worktree`) and B (`full-submit`) get their own result for the same payload |
  | T-ISO-3 | `test_same_worktree_other_session_ordinary` | a second session in the same `cwd`, no `agent_id`, exits 0 |
  | T-ISO-4 | `test_person_subagent_not_governed` | unbound id plus `agent_id` plus the `cwd` of a bound session's worktree exits 0 (X-004) |
  | T-ISO-5 | `test_fail_open_shapes_ordinary` | not-JSON input, empty `tool_input`, unknown tool, no `jq`: unbound session exits 0 |
  | T-ISO-6 | `test_forged_nested_session_id` | an ordinary payload whose `tool_input` holds a bound `session_id` exits 0; a governed payload whose `tool_input` holds an unbound one stays governed |
  | T-ISO-7 | `test_subagent_governed` | parent id plus `agent_id` (OB-H1 payload) is governed |
  | T-ISO-8 | `test_nested_subagent_governed` | nested shape with `agent_type` (OB-H1 payload) is governed |
  | T-ISO-9 | `test_agent_and_task_names` | `Agent` and `Task` get the same decisions |
  | T-BIND-1 | `test_marker_with_record_binds_level` | for each of the three words; the record is gone afterwards |
  | T-BIND-2 | `test_marker_at_start_without_record_binds_degraded` | file holds `degraded`; next gated call shows LL-STATE |
  | T-BIND-3 | `test_malformed_marker_at_start_binds_degraded` | uppercase hex, dashed UUID, 33 hex, `v2`, `<nonce>` |
  | T-BIND-4 | `test_marker_after_whitespace_or_bom_binds` | leading spaces, newline, BOM |
  | T-BIND-5 | `test_strict_marker_mid_prompt_with_record_binds` | preamble text, then the marker |
  | T-BIND-6 | `test_strict_marker_mid_prompt_without_record_blocks_prompt` | exit 2, LL-NOBIND, no session file |
  | T-BIND-7 | `test_bind_failure_blocks_prompt` | read-only `sessions/`: exit 2, LL-NOBIND |
  | T-BIND-8 | `test_sessions_dir_created` | no `sessions/` directory yet: bind succeeds |
  | T-BIND-9 | `test_nonce_single_use` | a second session sending the same marker binds `degraded`, not the record's level |
  | T-BIND-10 | `test_later_marker_consumes_record_keeps_level` | bound `worktree` session plus a new marker with record: level unchanged, record removed |
  | T-BIND-11 | `test_resume_same_id_governed` | a later prompt and call with the same id stay governed |
  | T-BIND-12 | `test_rename_still_governed` | different `cwd` on later calls: still governed |
  | T-BIND-13 | `test_reclaim_new_session_new_level` | old id keeps its level; new id gets the new record's level |
  | T-BIND-14 | `test_invalid_session_ids` | `.`, `..`, `x.ok`, `a/b`, empty, 129 characters: marker prompt gives LL-NOBIND; PreToolUse with a non-empty store gives the `W` column plus LL-STATE |
  | T-BIND-15 | `test_marker_prompt_with_agent_id_ignored` | exit 0, nothing bound |
  | T-BIND-16 | `test_jq_missing_marker_prompt_blocked` | exit 2, LL-NOBIND |
  | T-BIND-17 | `test_loose_marker_mid_prompt_ignored` | `see [sc-launch:v2:x]` in an ordinary prompt: exit 0, nothing bound |
  | T-APR-1 | `test_approve_by_reply` | `approved`, `Approved.`, `  APPROVED!  ` |
  | T-APR-2 | `test_approve_by_typed_command` | `/sc:implement x`, `/task`, `/sc:task y` |
  | T-APR-3 | `test_approve_ignored_with_agent_id` | no `.ok` |
  | T-APR-4 | `test_approve_needs_exact_form` | `please approved`, `approved, but`, `/task-builder x`, `/tasks`, `/sc:implement-protocol`, `/sc:pr-submit` approve nothing |
  | T-APR-5 | `test_approval_never_unlocks_commit_push_submit` | after approval at `W`: COMMIT, PUSH, SUBMIT still blocked |
  | T-APR-6 | `test_ok_written_only_at_worktree` | `full` and `full-submit` sessions get no `.ok` |
  | T-APR-7 | `test_unbound_session_cannot_approve` | no file written |
  | T-APR-8 | `test_degraded_session_can_approve` | `.ok` written; IMPL allowed |
  | T-APR-9 | `test_typed_implement_then_skill_call_allowed` | prompt `/sc:implement x`, then Skill `sc:implement-protocol`: exit 0 |
  | T-GRID-1 | `test_policy_grid` | every oracle row at every level |
  | T-GRID-2 | `test_grid_complete` | every class of Change 19 has W, WA, F, FS entries in the oracle |
  | T-GRID-3 | `test_worktree_stops_at_plan` | at `W`: IMPL, COMMIT, PUSH, SUBMIT blocked; Write of `.dev/tasks/x/plan.md` and Skill `sc:workflow` allowed |
  | T-GRID-4 | `test_full_implements_without_submitting` | at `F`: IMPL allowed; COMMIT, PUSH, SUBMIT blocked |
  | T-GRID-5 | `test_full_submit_allows_commit_push_prsubmit` | at `FS`: commit, named push, `sc:pr-submit`, `gh pr create --repo "$REPO"` allowed |
  | T-SKL-1 | `test_impl_name_spellings` | the six IMPL spellings of Change 14, plus `SC:IMPLEMENT` and `/sc:implement args` |
  | T-SKL-2 | `test_submit_name_spellings` | `sc:pr-submit`, `sc:pr-submit-protocol` |
  | T-SKL-3 | `test_skill_name_keys` | name under `skill`, then under `name` |
  | T-SKL-4 | `test_skill_without_name` | LL-SKILL at W, WA, F; allowed at FS |
  | T-SKL-5 | `test_issue_skill_escape` | `sc:issue`, `sc:issue-protocol`: LL-ESCAPE |
  | T-NRM-1 | `test_quote_and_backslash_splicing` | `g""it push origin main`, `\git push origin main`, `git push origin 'feature:ma''in'`, `git push origin feature:ma\in`: LL-PROTECTED |
  | T-NRM-2 | `test_redirections_removed` | at FS allowed: `git push origin a:b 2>&1 \| tail -5`, `git push origin a:b > /tmp/log 2>&1`, `git commit -m x < /dev/null` |
  | T-NRM-3 | `test_segment_separators` | `;`, `&&`, `\|\|`, `\|`, newline, `$( )`, backtick each start a new segment |
  | T-NRM-4 | `test_json_escaped_slash_decoded` | a payload with `\/` escapes in a tamper path is blocked |
  | T-GIT-1 | `test_framework_git_commands_allowed` | every `/sc:implement` and `/sc:pr-submit` read or local git command listed in the Overview, at `F` |
  | T-GIT-2 | `test_unknown_or_missing_subcommand_blocked` | row 18 of Change 20 |
  | T-GIT-3 | `test_alias_routes_blocked` | the three alias forms of fact T2 |
  | T-GIT-4 | `test_alias_cannot_shadow_builtin` | in a temporary repo, real `git -c alias.status=commit status` makes no commit (checks the git behaviour Change 10 relies on) |
  | T-GIT-5 | `test_attr_source_value_skipped` | `git --attr-source HEAD push origin main`: LL-PROTECTED at every level; `git --attr-source HEAD status`: allowed |
  | T-GIT-6 | `test_commit_class_variants` | row 13 of Change 20: blocked at F, allowed at FS |
  | T-GIT-7 | `test_update_ref_rules` | `refs/superclaude/...` and `"$ref"` allowed; `HEAD`, `refs/heads/x`, `--stdin` are COMMIT |
  | T-GIT-8 | `test_later_git_word_rules` | `git commit -m "fix git handling"` allowed at FS; `git rebase -x "git push origin main" main` LL-PROTECTED; `git bisect run git commit` LL-COMMIT at F |
  | T-GIT-9 | `test_wrappers_every_level` | `bash -c`, `sh -c`, `env`, `command`, `exec`, `sudo`, `nohup`, `timeout 30`, `xargs`, `/usr/bin/git`, `git -C /x`, `NAME=x git`, a `python -c "subprocess.run(['git','push','origin','main'])"` one-liner: same class as the bare command |
  | T-GIT-10 | `test_pull_is_merge` | `git pull`, `git pull --rebase`: LL-MERGE at every level |
  | T-GIT-11 | `test_space_in_C_path_blocked` | `git -C "/dir with space" push`: LL-UNKNOWN |
  | T-PSH-1 | `test_named_push_allowed_at_submit` | `git push origin <sha>:<branch>` |
  | T-PSH-2 | `test_unnamed_push_blocked_at_submit` | bare, `origin`, `origin feature`, `origin HEAD`, `origin x:@`: LL-PUSHNAME |
  | T-PSH-3 | `test_push_all_mirror_protected` | every level |
  | T-PSH-4 | `test_push_main_destinations_protected` | `main`, `x:main`, `x:refs/heads/master`, `x:heads/main`, `+main`, `:main`, every level |
  | T-PSH-5 | `test_push_other_remote_or_options_blocked` | `upstream a:b`, `--repo=x`, `--receive-pack=x`, `--exec=x` at FS |
  | T-PSH-6 | `test_push_option_value_skipped` | `git push -o ci.skip origin a:b` allowed at FS |
  | T-PSH-7 | `test_push_variable_blocked` | `git push origin a:$B` at FS |
  | T-PSH-8 | `test_configured_refspec_cannot_redirect` | fact T3 replayed: `git -c remote.origin.push=refs/heads/feature:refs/heads/main push origin feature` LL-PUSHNAME; with `feature:feature` allowed |
  | T-PSH-9 | `test_feature_slash_main_allowed` | `git push origin feature/main:feature/main` at FS |
  | T-PSH-10 | `test_force_options_have_no_rule` | `--force`, `--force-with-lease`, `+a:b` allowed at FS (O-2) |
  | T-GH-1 | `test_gh_pr_merge_every_level` | LL-MERGE |
  | T-GH-2 | `test_gh_api_merge_and_ref_writes` | `/merges` POST, GraphQL `mergePullRequest`, `enablePullRequestAutoMerge`, `git/refs/heads/main` PATCH: LL-MERGE at every level |
  | T-GH-3 | `test_gh_pr_create_without_repo` | LL-REPO at FS; LL-SUBMIT below |
  | T-GH-4 | `test_gh_pr_create_repo_forms` | `--repo "$REPO"`, `-R o/r`, `--repo=o/r` allowed at FS |
  | T-GH-5 | `test_gh_writes_need_submit` | row 20 of Change 20 |
  | T-GH-6 | `test_gh_pr_ready_submit_class` | blocked below FS, allowed at FS (O-3) |
  | T-GH-7 | `test_gh_reads_every_level` | row 19 of Change 20 |
  | T-GH-8 | `test_merge_url_suffix` | `curl` to `.../pulls/5/merge` and `.../merges`: LL-MERGE; `gh api repos/o/r/pulls/5/merge` (a GET) is not caught by H5 |
  | T-GH-9 | `test_gh_unknown_group` | `gh alias set co 'pr merge'`, `gh co 5`, `gh extension install x`: LL-UNKNOWN |
  | T-MCP-1 | `test_mcp_merge_every_level` | `mcp__github__merge_pull_request` |
  | T-MCP-2 | `test_mcp_writes_blocked` | `push_files`, `create_or_update_file`, `create_pull_request`: LL-MCP at every level |
  | T-MCP-3 | `test_mcp_reads_allowed` | `list_commits`, `get_commit` |
  | T-MCP-4 | `test_mcp_ordinary_session_allowed` | exit 0 |
  | T-ESC-1 | `test_claude_launch_flags` | row 25 claude forms blocked; `grep -rn claude docs/`, `grep claude -rn docs/` allowed |
  | T-ESC-2 | `test_orca_allowlist` | the allowed `orca` pairs pass; `agent launch`, `terminal send`, `computer type-text`, `automations run`, `orchestration send`, `orchestration dispatch`, `worktree create` blocked |
  | T-ESC-3 | `test_remote_isolation_blocked` | every level |
  | T-ESC-4 | `test_workflow_remotetrigger_sendmessage_blocked` | every level |
  | T-ESC-5 | `test_terminal_tools_blocked` | `tmux send-keys approved Enter`, `tmux new-session -d 'claude "x"'`, `screen -X stuff x`, `xdotool type approved`, `ydotool type x` |
  | T-ESC-6 | `test_ccsession_any_form` | `ccsession`, `ccsession-orca 'x'`, `/usr/local/bin/ccsession -h` |
  | T-TRN-1 | `test_turn_starters_blocked_before_approval` | CronCreate, ScheduleWakeup, Monitor, background Bash at `W` |
  | T-TRN-2 | `test_turn_starters_allowed_later` | same calls at WA, F, FS (with harmless commands) |
  | T-TRN-3 | `test_monitor_and_background_commands_scanned` | Monitor `git push origin main` at FS: LL-PROTECTED; background `git commit -m x` at F: LL-COMMIT |
  | T-TRN-4 | `test_turn_and_input_route_table` | every turn-starting or input-injecting route (Cron*, Schedule*, Monitor, background Bash, `orca terminal send`, `orca computer type-text`, `tmux send-keys`, `screen -X stuff`, `xdotool`, SendMessage) is blocked at `W` |
  | T-TAM-1 | `test_tamper_tokens_in_bash` | row 27 of Change 20 |
  | T-TAM-2 | `test_tamper_paths` | Edit, Write and NotebookEdit on each token path, a `//` path, a `/./` path and a `..` path |
  | T-TAM-3 | `test_tamper_ignores_content` | a Write whose content quotes `.claude/hooks` and `disableAllHooks` is allowed |
  | T-TAM-4 | `test_guard_source_path_not_tamper` | `cat src/superclaude/hooks/scripts/launch-level-guard.sh`, an Edit of that file, a path containing `hook-launch-level-394` |
  | T-TAM-5 | `test_cd_split_blocked` | `cd ~/.claude && : > hooks/launch-level-guard.sh` |
  | T-TAM-6 | `test_reinstall_blocked` | `uv run superclaude install`, `uv run python -c "import superclaude.cli.install_hooks"` |
  | T-TAM-7 | `test_tamper_in_ordinary_session_allowed` | exit 0 (X-005) |
  | T-TAM-8 | `test_script_source_has_no_joined_store_token` | the script text does not contain `.claude/state/launch-level` |
  | T-FC-1 | `test_jq_missing` | governed: LL-BROKEN; ordinary: exit 0 |
  | T-FC-2 | `test_bad_state_degrades_to_worktree` | empty file, garbage word, `degraded`, mode 000: `W` column plus LL-STATE; an existing `.ok` still counts |
  | T-FC-3 | `test_internal_error_prints_broken` | `PATH` without `tr`, governed Bash: exit 2, stderr has the header and `Blocked:` |
  | T-FC-4 | `test_script_ends_in_default_deny` | the script's last command prints LL-BROKEN and exits 2 |
  | T-FC-5 | `test_not_json_governed` | raw text holding a bound id but invalid JSON: LL-BROKEN |
  | T-FC-6 | `test_missing_session_id_with_store` | no `session_id` key while the store holds a session: `W` column plus LL-STATE |
  | T-FC-7 | `test_big_command` | 65,537 bytes governed: LL-BIG; ordinary: exit 0 |
  | T-MSG-1 | `test_every_message_has_header_and_three_lines` | first line header, then lines starting `Blocked:`, `Why:`, `You can:` |
  | T-MSG-2 | `test_every_message_id_reachable` | one oracle payload per id produces it |
  | T-MSG-3 | `test_no_unresolved_template_variables` | no `{level}`, `{store}` or `{sid}` in any output |
  | T-MSG-4 | `test_precedence_order` | TAMPER over MERGE; SUBMIT over REPO below FS; PUSH over PUSHNAME below FS; PROTECTED over PUSH |
  | T-MSG-5 | `test_level_rendered_in_header` | the four renderings |
  | T-MSG-6 | `test_state_and_text_notes` | LL-STATE on degraded sessions; LL-TEXT on Bash-derived blocks only |
  | T-SPD-1..5 | `test_speed_empty_store`, `test_speed_stale_store`, `test_speed_ratio_to_block_bare_python`, `test_speed_governed`, `test_speed_large_commands` | the five budget lines of Change 22, in that order |
  | T-REG-1 | `test_hooks_json_entries` | the two entries of Change 24, exact matcher, command and timeout; no UserPromptExpansion entry |
  | T-REG-2 | `test_freshness_scripts_lists_guard` | `"launch-level-guard.sh"` is in `_FRESHNESS_SCRIPTS` |
  | T-REG-3 | `test_matcher_selects_intended_tools` | Python `re.search` of the matcher: matches `Bash`, `Task`, `SendMessage`, `CronCreate`, `mcp__github__merge_pull_request`; does not match `Read`, `Grep`, `Glob`, `TaskCreate`, `TaskUpdate`, `mcp__codegraph__codegraph_search` |
  | T-GAP-1 | `test_known_gaps_pinned` | row 33 of Change 20 stays ALLOW, so closing a gap is a deliberate change |
- **Rationale**: every merged rule and every probe finding gets a named case (Advocate 3 Round 2; INV "Test" suggestions).
- **Integration point**: section 12, "Named cases".
- **Risk**: Low.

### Change 28: Acceptance criteria map (all variants, rewritten to the merged rules)
- **Source**: section 13 of all three variants.
- **Target**: Base section 13 (replace).
- **Settles**: success criterion "every AC maps to a row and a named test".
- **Final rule**: section 13 carries this table.

  | AC | Rules (changes) | Automated cases (at least two) | Observed |
  |---|---|---|---|
  | AC-1 worktree stops at plan; blocks implement, task, commit, push, pr-submit | 8, 14, 18, 19, 20 | T-GRID-3, T-SKL-1, T-APR-5, T-APR-9 | OB-H3 |
  | AC-2 full implements, blocks submission; full --submit allows it | 10, 11, 12, 19, 20 | T-GRID-4, T-GRID-5, T-GIT-6, T-PSH-1, T-GH-4 | OB-H3 |
  | AC-3 approval by typing or `approved`; human versus agent | 5, 8, 15, 16 | T-APR-1, T-APR-2, T-APR-3, T-APR-4, T-TRN-1, T-TRN-4 | OB-H1 item 4 |
  | AC-4 claim sessions only; Bash, Skill, Task; nested subagents | 6, 7, 14, 24 | T-ISO-1, T-ISO-4, T-ISO-7, T-ISO-8, T-ISO-9, T-REG-3 | OB-H1 items 1 and 6, OB-H2 |
  | AC-5 uneditable state, fail closed, tamper, rename, re-claim | 4, 5, 17, 21, 25 | T-BIND-2, T-BIND-7, T-BIND-12, T-BIND-13, T-TAM-1, T-TAM-2, T-FC-1, T-FC-2 | OB-H2 |
  | AC-6 no merge or main push at any level, including wrappers | 9, 10, 11, 12, 13 | T-PSH-3, T-PSH-4, T-GIT-9, T-NRM-1, T-GH-1, T-GH-2, T-MCP-1 | OB-H3; limit: owner decision O-7 |
  | AC-7 plain-words explanation for every block | 21, 23 | T-MSG-1, T-MSG-2, T-MSG-3, T-FC-3 | OB-H3 (one live message read) |
  | AC-8 tests per level, approval, isolation, nested, missing state, wrappers, edges; speed | 22, 26, 27 | T-GRID-1, T-SPD-1..5, plus every group above | OB-H3 timing |
- **Integration point**: section 13.
- **Risk**: Low.

### Change 29: Observed checks OB-H1 to OB-H3 (merge of all variants)
- **Source**: Variant 1 section 12 "Observed"; Variant 2 OB-H1 to OB-H5; Variant 3 OB-H2 mandatory; Round 2 C-020 (unanimous merge), NE-3, NE-4; INV-005, INV-015, INV-027, INV-028, INV-036, INV-040.
- **Target**: Base section 12, "Observed" paragraph (replace).
- **Settles**: C-020 (content), INV-040 (observation part).
- **Final rule**:
  - **OB-H1** (first; needs no claim feature). A throwaway log-only hook, registered on PreToolUse with matcher `*`, on PreToolUse with a copy of the Change 24 matcher, and on UserPromptSubmit, appends each payload to a log. It records: (1) a subagent Bash call and a nested-subagent Bash call: `session_id` against the parent's, `agent_id`, `agent_type` (U1); (2) a model Skill call: `tool_input` keys and the name form (U2); (3) an Agent call: tool name and the `isolation` key (U3, U13); (4) a typed `/sc:implement x` line on UserPromptSubmit (V6 reading, O-4 contingency); (5) a Monitor call's `tool_input`, and the UserPromptSubmit payload, if any, of a Monitor-delivered line and of a background-Bash completion notice (U4, U11, INV-027); (6) whether a `TaskCreate` call reaches the anchored-matcher copy (U15); (7) the names of SendMessage and any team or cross-session tool, and the GitHub MCP tool names if a server is configured (U12, INV-032); (8) whether `claude` without `-p` starts from the Bash tool with no terminal (U14). Payloads are saved to `tests/hooks/fixtures/launch_level/ob_h1/` with secrets removed. Ship gate: item 1 must show the parent's `session_id` (Change 7).
  - **OB-H2** (after the claim feature ships; once per Orca account and config directory in use). Launch a real claim at `worktree` and record: the session file exists before the first tool call (U8); the exact first prompt text, including any Orca preamble and the marker's position (A-007, U7); the hook process's `HOME` and `CLAUDE_CONFIG_DIR` (A-006, INV-005); the claim script refuses to launch without `jq` and without the registration (CL-4). Mandatory before any real governed launch.
  - **OB-H3** (after OB-H2, on a test issue; one run per level). `W`: the session stops at the plan; in separate runs a typed `/sc:implement` and a reply `approved` each unlock implementation; commit stays blocked. `F`: implementation runs with no commit or push; record every git command `/sc:implement` runs (U10). `FS`: commit, `git push origin <sha>:<branch>`, and `/sc:pr-submit --monitor 3` opens a pull request on the fork and completes one poll cycle (INV-028); a deliberately conflicting pull request shows the conflict-sync merge blocked and how `/sc:pr-submit` reacts (O-10). At every level: one attempt to push to `main` and one to merge, both blocked; record how often LL-PUSHNAME and LL-TEXT fire; record whether the session carries an Orca worker preamble (U7, O-11); read one live block message for wording (AC-7); record the hook's timing from the session debug log.
- **Rationale**: Variant 2's OB-H4 (wording) and OB-H5 (timing) fold into OB-H3 so the list stays at three; Variant 3's rule that OB-H2 gates real use is kept.
- **Integration point**: section 12, "Observed".
- **Risk**: Medium. These are manual and need the claim feature for OB-H2 and OB-H3.

### Change 30: Order of work (Variant 2 OB-H1 first, Variant 3 harmless first)
- **Source**: Variant 1 section 14; Variant 2 section 14; Variant 3 section 14; Round 2 C-020 (unanimous merge).
- **Target**: Base section 14 (replace).
- **Settles**: C-020 (order), U-009 (order part).
- **Final rule**:
  1. OB-H1 with the log-only hook. If item 1 fails, stop and take owner decision O-9.
  2. Skeleton: event dispatch, store, binding (Change 5), resolution and fast paths (Change 6), default deny and the EXIT trap (Change 21), message printer (Change 23). T-ISO-1, T-ISO-5, T-ISO-6, T-FC-* and T-BIND-* pass before any classification rule exists, so the hook is shown harmless to ordinary sessions first.
  3. Normalisation and classifiers (Changes 9 to 18): T-NRM, T-GIT, T-PSH, T-GH, T-MCP, T-SKL, T-ESC, T-TRN, T-TAM.
  4. Policy and messages (Changes 19, 20, 23): T-GRID, T-MSG.
  5. Approval (Change 8): T-APR.
  6. Registration (Change 24): `hooks.json`, `_FRESHNESS_SCRIPTS`, `make sync-dev`, `make verify-sync`; T-REG, T-SPD.
  7. Hand CL-1 to CL-6 (Change 25) to the claim feature; amend FR-31.
  8. OB-H2, then OB-H3, once claim launches exist. Until both pass, `--pipeline full` and `--submit` are not used on real issues (launch-levels addendum section 9).
- **Integration point**: section 14.
- **Risk**: Low.

### Group G: registers

### Change 31: Unverified register (merge of U1 to U13, N1 to N5, Variant 3's test column)
- **Source**: Variant 1 section 16 (U9 to U13); Variant 2 section 16 (N1 to N5); Variant 3 section 16 (Test column); Round 2 S-005 (unanimous merge).
- **Target**: Base section 16 (replace).
- **Settles**: S-005.
- **Final rule**: section 16 carries one table with columns Item, Question, Tolerance, Check. Rows:

  | Item | Question | Tolerance | Check |
  |---|---|---|---|
  | U1 | Subagent and nested-subagent `session_id` equal the parent's | Ship gate (Change 7); no fallback built | OB-H1 item 1, T-ISO-7, T-ISO-8 |
  | U2 | Skill payload key | Read `skill`, then `name`; neither gives SKILL | OB-H1 item 2, T-SKL-3 |
  | U3 | `Agent` also named `Task` | Both handled | OB-H1 item 3, T-ISO-9 |
  | U4 | `!cmd`, Monitor lines, cron turns via UserPromptSubmit | Whole-prompt approval; TURN blocked at `W` | OB-H1 item 5, T-TRN-1 |
  | U5 | UserPromptSubmit for a typed command queued mid-turn | The reply `approved` always works | OB-H3 |
  | U6 | Hooks under `claude --bare` or `--settings` | Human-chosen; residual R4; the agent's launch flags are ESCAPE | T-ESC-1 |
  | U7 | Orca worker preamble on launched sessions (WC-9 versus `--submit`) | Owner decision O-11; the hook never reads the preamble | OB-H2, OB-H3 |
  | U8 | UserPromptSubmit fires before the first model call for a command-line prompt | If it does not fire, nothing binds and the session is ordinary; OB-H2 is mandatory before real use | OB-H2 |
  | U9 | `command_name` form on UserPromptExpansion | Moot while the event is not registered; contingency in Change 8 | OB-H1 item 4 |
  | U10 | Git commands `/sc:implement` runs | Static check: no `commit`, `push`, `merge`, `pull` (Overview); its `update-ref` targets are allowed | OB-H3, T-GIT-1 |
  | U11 | Monitor input fields | `command` scanned; `ws` has nothing to scan | OB-H1 item 5 |
  | U12 | GitHub MCP tool names | Keyword matcher plus read prefixes (Change 13); unmatched names are residual R10 | OB-H1 item 7 |
  | U13 | Agent `isolation` key in the hook payload | This session's tool definitions show `isolation: "remote"`; if the key is absent, ESCAPE never fires for it | OB-H1 item 3, T-ESC-3 |
  | N1 | UserPromptSubmit inside subagents | Payloads with `agent_id` are ignored | T-APR-3, T-BIND-15 |
  | N3 | `/clear` gives a new `session_id` | Residual R4 | none |
  | N5 | Payload escapes `/` | Moot: `jq` decodes values | T-NRM-4 |
  | U14 | `claude` without `-p` can start from the Bash tool with no terminal | Residual R5; terminal tools are ESCAPE | OB-H1 item 8 |
  | U15 | The harness honours `^` and `$` inside a matcher | The script re-checks names (Change 24 item 7) | OB-H1 item 6, T-REG-3 |
  | U16 | What `git push --repo`, `--receive-pack`, `--exec` do (taken from Advocate 1, not re-checked) | All three are PUSHNAME at every level | T-PSH-5 |

  N2 and N4 are merged into U13 and U10. The git behaviour "an alias cannot shadow a built-in" is not listed: T-GIT-4 checks it on every test run.
- **Integration point**: section 16.
- **Risk**: Low.

### Change 32: Residual risks (Variant 1 numbering, Variant 2 "what it leaves open")
- **Source**: Variant 1 section 2 R1 to R8; Variant 2 section 2 cut table; Variant 3 section 2; Round 2 S-002 (unanimous merge); INV-003, INV-023, INV-030; diff-analysis closing note on shell startup files.
- **Target**: new section 17 (Change 1).
- **Settles**: S-002, INV-003, INV-023, INV-030; residual statements for A-004, A-006, A-007.
- **Final rule**: section 17 lists these plain statements, each with "why accepted":
  - **R1** A file written with Write or any other tool and then run (`bash push.sh`, a `make` target, `uv run python x.py`), and programs that start git or Claude internally (the claim script, `superclaude sprint run` and similar runners), are not inspected. AC-6's "including through shell wrappers around git" is therefore met only for wrappers written inline in the command (owner decision O-7). Why: scanning file content would block every plan that mentions a push.
  - **R2** A hook that times out or crashes lets the call go ahead (V8). Why: `onFailure: "block"` would also block ordinary sessions.
  - **R3** The store reached indirectly (a glob such as `~/.cl*`, a variable, a script) or deleted from another terminal turns the session ordinary. Why: the token rule catches direct names only, and deletion is also the release route.
  - **R4** Human-chosen bypasses: `claude --bare`, `--settings`, a person setting `disableAllHooks`, `--fork-session` and `/clear` (new ids), or a person launching under another `CLAUDE_CONFIG_DIR` (CL-4 refuses this only for claim launches). Why: they are a person's choice.
  - **R5** An interactive `claude`, `claude -c` or `claude -r` started some way other than tmux or screen, and input-injection tools not on the ESCAPE list (UNVERIFIED U14). Why: a command-position parser would be needed.
  - **R6** A malformed marker that is not at the start of the prompt (for example after an Orca preamble), with no usable record, leaves the session ordinary. OB-H2 records the real first prompt. Why: matching loose markers anywhere would govern people who quote the marker.
  - **R7** A shell alias or function defined in `~/.bashrc` or another startup file the Bash tool loads can hide `git` from the scan; whether a mid-session edit takes effect is unverified; edits to startup files are not tamper. Why: no variant protects them, and adding them over-blocks ordinary dotfile work.
  - **R8** Accepted over-blocks in governed sessions: prose that mentions git, gh, `orca` or the claude family inside a Bash command (LL-TEXT names the way around); the tracked project `.claude/settings.json`; `orca` worker subcommands (O-11); variables in pushes. Why: governed sessions only, plain message, cheap retry.
  - **R9** Local plumbing commits through variables (`git update-ref "$ref" ...`, `git reset --hard <stash commit>`) are not COMMIT. Why: `/sc:implement` writes refs through variables; a push still needs the named form.
  - **R10** GitHub writes outside the checked routes: `curl` with a token to endpoints other than merge URLs, MCP tools whose names lack the matcher keywords (for example issue comments). Why: no acceptance criterion names them; merge routes are covered.
  - **R11** Fork rule at `full --submit`: `gh pr create --repo <upstream>` passes (no name compared, O-12), and `-c url.<x>.pushInsteadOf` or `-c remote.origin.pushurl` can send an `origin` push to another URL (feature branches only; `main` stays protected by name). Why: the hook is installed in every project and cannot know the right repository.
  - **R12** A hostile agent (T3) running as the same user can defeat any same-user guard. Why: out of scope (A-004).
  - **R13** A person who pastes a launch prompt at the start of their own first prompt is governed at `worktree` until they `rm` the session file. Why: the price of "a marker always governs" (X-001).
  - **R14** If U1, U8 or A-006 is false and the observed checks are skipped, the guard silently does nothing for that case; tests use a temporary `HOME` and synthetic payloads and cannot see it. Why: only OB-H1 and OB-H2 can; they are gates (Change 30).
  - **R15** Another person's session typing `approved` into the governed terminal (for example `orca terminal send` from an ordinary session) is indistinguishable from the person (V6, no origin field). Why: the governed agent itself cannot do it (Change 15).
- **Integration point**: section 17.
- **Risk**: Low.

### Change 33: Open decisions for the owner (all variants, residual splits added)
- **Source**: section 15 of all variants; Round 2 residual splits (INV-020).
- **Target**: Base section 15 (replace).
- **Settles**: INV-020; the residual splits on the `cwd` cross-check, `--force`, `gh pr ready`, UserPromptExpansion and the issue number.
- **Final rule**: section 15 copies the table in this plan's section "Open decisions for the owner", ids O-1 to O-15, with the default and the alternative for each. The spec states each default as the rule in force.
- **Integration point**: section 15.
- **Risk**: Low.

### Change 34: Rejected alternatives (from all variants, X-009 reason corrected)
- **Source**: rejections in Variant 1 sections 4, 8, 10; Variant 2 sections 2, 4, 8; Variant 3 sections 4, 8; Round 2 cuts.
- **Target**: new section 18 (Change 1); remove the scattered "Rejected:" lines from sections 4, 6, 8 and 10.
- **Settles**: X-009; the design-alternative rows of this plan's "Changes NOT Being Made" table.
- **Final rule**: section 18 lists, with a one-line reason each, every row of this plan's "Changes NOT Being Made" table whose subject is a design alternative (rows marked "alternative"). For git-level hooks the reason is: "a linked worktree's hooks live in the main checkout's common git directory (this worktree's `.git` file points to `/home/coder/workspaces/IronClaude/.git/worktrees/hook-launch-level-394`), so they also run for the person's own pushes; git cannot tell which session called; `--no-verify` skips them". Variant 3's reason ("`.git/hooks` sits inside the worktree") is not used.
- **Integration point**: section 18.
- **Risk**: Low.

## Coverage index: diff points S-, C-, X-

One row per diff point. "Round 2" is the tally status from `convergence-tally.md`; "Final rule" is the one-line summary of the rule stated in full in the named change.

| Point | Round 2 | Final rule (summary) | Change |
|---|---|---|---|
| S-001 | majority V1 | YAML front matter plus an H1 title and a Terms list | 1 |
| S-002 | unanimous merge | Numbered residuals R1 to R15, each with "why accepted" | 2, 32 |
| S-003 | unanimous merge | Decision table of literal commands with class column and failure rows; the test oracle is a hand copy | 20, 26 |
| S-004 | majority merge | One flat script; policy as a literal `case` table; independent oracle in the test file; no `--classify`, no ERR trap | 3, 19 |
| S-005 | unanimous merge | One unverified register U1 to U16 with Tolerance and Check columns | 31 |
| S-006 | unanimous merge | `LL-*` ids in the header plus Blocked, Why, You can shape | 23 |
| C-001 | unanimous merge | Strict marker anywhere with a record binds by `mv`; a marker at the start (after whitespace or BOM) with no record binds `degraded`; a strict marker elsewhere with no record blocks the prompt; later markers never change the level; no age check; no `cwd` cross-check (O-1) | 5 |
| C-002 | majority merge | U1 is a ship gate; no fallback built; reserve design recorded for O-9 | 7 |
| C-003 | majority V2 | One word per file; approval is a separate empty file | 4 |
| C-004 | unanimous merge | Governed only; tokens on normalised command text and path fields, never content; `..` paths; `.claude` word ending; reinstall rule | 17 |
| C-005 | majority merge (split) | UserPromptSubmit only; whole-prompt `approved` or a first line `/sc:implement`, `/sc:task`, `/task`; `agent_id` ignored; UserPromptExpansion not registered (O-4) | 8 |
| C-006 | unanimous V2 | `touch sessions/<sid>.ok` only at `worktree` | 4, 8 |
| C-007 | unanimous merge | One normalisation pass (quote deletion, `tr` sweep keeping `$`), option skip list including `--attr-source`, git allowlist | 9, 10 |
| C-008 | unanimous V1 | `pull` is MERGE; non-`origin` push blocked; aliases fall to the allowlist | 10, 11 |
| C-009 | unanimous merge | Named destination rule with explicit `:`; no subprocess; `--force` has no rule (O-2) | 11 |
| C-010 | unanimous merge | `gh pr merge` and gh api merge or ref writes always MERGE; gh writes are SUBMIT; `gh pr create` needs an explicit `--repo`/`-R` word at submit; `gh pr ready` is SUBMIT (O-3); merge URLs for `curl` | 12 |
| C-011 | unanimous merge | Two events; anchored PreToolUse matcher with `SendMessage` and MCP keywords; timeout 5 | 24 |
| C-012 | unanimous V1 | Monitor and background Bash commands scanned like Bash; Cron, Schedule, Monitor, background Bash blocked only at `W`; Workflow and RemoteTrigger always ESCAPE | 15, 16 |
| C-013 | unanimous merge | MCP: read prefixes allowed, `merge` names MERGE, other matched writes MCP at every level (O-14) | 13 |
| C-014 | majority merge | `orca` read allowlist; `ccsession*` always; `claude`/`claude-code` with launch flags; terminal tools; remote isolation; SendMessage; Skill `issue` | 14, 15 |
| C-015 | unanimous merge | Default deny last line; EXIT trap printing LL-BROKEN; checked `jq` and `tr` status | 21 |
| C-016 | majority merge | `compgen -G` on `sessions/`, then the `session_id` regex prefilter, then `jq` | 6 |
| C-017 | majority V3 | 100-run medians and p95, ratio to `block-bare-python.sh`, stale-store and large-command cases | 22 |
| C-018 | unanimous merge (split on issue number) | Header names the level, no issue number (O-5) | 23 |
| C-019 | unanimous merge | Literal payload oracle, grid completeness, every id reachable, pinned over-matches and gaps, no `manual` marker | 26, 27 |
| C-020 | unanimous merge | OB-H1 first; OB-H2 mandatory before real use; OB-H3 includes a conflicting PR and a pr-submit poll cycle | 29, 30 |
| X-001 | unanimous V1 | A marker without a usable record never leaves the agent ungoverned | 5 |
| X-002 | majority merge | `jq` missing blocks governed calls; claim refuses to launch without it | 21, 25 |
| X-003 | unanimous V1 | Bad state degrades to `worktree` with LL-STATE; `.ok` survives | 4, 21 |
| X-004 | unanimous V2 | No always-on `cwd` fallback | 7 |
| X-005 | majority merge | Tamper rule in governed sessions only | 17 |
| X-006 | unanimous merge | Settings and hooks paths blocked on Edit, Write, NotebookEdit and in Bash; `disableAllHooks` token | 17 |
| X-007 | unanimous merge | HEAD, bare push, `--all`, `--mirror`, `+main`, `:main` blocked without reading HEAD | 11 |
| X-008 | unanimous V1 | `git pull` is MERGE at every level | 10 |
| X-009 | unanimous V1 | Git-level hooks rejected with the corrected reason | 34 |
| X-010 | unanimous V2 | `_FRESHNESS_SCRIPTS` lives in `install_hooks.py`; no Makefile line; no `manual` marker | 3, 26 |

Unique contributions: U-001 (Change 5), U-002 (Change 19), U-003 (Changes 11, 12; repo-name check dropped per NE-1), U-004 (Changes 12, 13, 16), U-005 (Changes 4, 17), U-006 (Change 8), U-007 (Changes 12, 25), U-008 (not taken, O-1), U-009 (Changes 22, 30), U-010 (Changes 12, 20).

## Shared assumptions A-001 to A-008

| Id | Assumption | Resolved condition (what the spec states or tests) | Changes |
|---|---|---|---|
| A-001 | A subagent's and a nested subagent's `session_id` equal the parent's | The spec states it as UNVERIFIED (U1) and makes it a ship gate: OB-H1 item 1 must pass before any real `full` or `--submit` launch. T-ISO-7 and T-ISO-8 run on the captured payloads. If it fails, O-9. | 7, 29, 30 |
| A-002 | Typed commands and agent actions are distinguishable, and a subagent cannot produce an approving prompt | Approval only from UserPromptSubmit without `agent_id`; every agent route to start a turn (TURN at `W`) or type into a terminal (ESCAPE) is blocked; T-APR-3, T-TRN-4 | 8, 15, 16 |
| A-003 | The launched session actually loads the guard | CL-4: the claim script refuses to launch unless the script is installed and registered in the settings the session will load; OB-H2 confirms the session file exists before the first tool call | 25, 29 |
| A-004 | Agent and hook run as one OS user | Stated in section 2; nothing is truly unwritable; protection is the tamper rule plus residuals R3, R12 | 2, 17, 32 |
| A-005 | `jq` is present on governed hosts | The claim script refuses to launch without `jq` (CL-4); the hook blocks governed calls with LL-BROKEN and marker prompts with LL-NOBIND when it is missing; ordinary sessions exit 0; T-FC-1, T-BIND-16 | 5, 6, 21, 25 |
| A-006 | Claim script, launched session and hooks resolve the same `$HOME` and config directory | Store fixed at `$HOME/.claude/state/launch-level`. A `$HOME` mismatch makes the record invisible, so the session binds `degraded` or its prompt is blocked, never ungoverned. A config-directory mismatch is refused by CL-4 and recorded by OB-H2 once per Orca account. The spec states that temporary-`HOME` tests cannot see this (R14). | 5, 25, 29, 32 |
| A-007 | The marker reaches the prompt unaltered and at a known place | Strict marker anywhere with a record binds; a marker at the start (after whitespace or BOM) without a record binds `degraded`; a strict marker elsewhere without a record blocks the prompt; OB-H2 records the real first prompt; residual R6 | 5, 29, 32 |
| A-008 | The payload `cwd` identifies the worktree acted on | Moot: the spec states "the hook never reads `cwd`". Push decisions read only the command words (Change 11); there is no fallback or cross-check | 6, 11 |

## Probe disposition (INV-001 to INV-040)

Every finding has one disposition. "Conflict" names where the probe's suggested resolution differs from the rule adopted, and why (criterion: fewest edge cases and unwanted blocks that still meet AC-1 to AC-8).

| INV | Disposition | Test | Note or sentence the spec carries |
|---|---|---|---|
| INV-001 | Planned change #5 (U10, U13) | T-BIND-7, T-BIND-8 | `mkdir -p sessions`; any bind failure blocks the prompt with LL-NOBIND |
| INV-002 | Planned change #6 (P2, P3), #22 | T-SPD-2 | Prefilter keeps `jq` off ordinary calls; speed measured with 1,000 stale session files |
| INV-003 | Accepted residual R4 (Change 32) | none | "A new `session_id` from `--fork-session` or `/clear` is a person's choice and makes the session ordinary." |
| INV-004 | Planned change #5 (U8a), #25 (CL-5) | T-BIND-10 | Conflict: the probe also asked for a one-line note; not taken (a UserPromptSubmit note is not shown to the person reliably) |
| INV-005 | Planned change #25 (CL-4), #29 (OB-H2 per account) | OB-H2 | Residual R4 for launches outside the claim script |
| INV-006 | Planned change #4 (item 3) | T-FC-2 | An empty file reads as `worktree` plus LL-STATE |
| INV-007 | Planned change #14 | T-SKL-1, T-SKL-2 | Name normalisation |
| INV-008 | Planned change #8 | T-APR-4 | Conflict: typed `/sc:task` approves, because Change 14 makes `sc:task` an implement skill; `/task-builder` and `/tasks` approve nothing as the probe asked |
| INV-009 | Planned change #17 | T-TAM-2, T-TAM-5 | Conflict: `..` paths are blocked instead of resolved with `realpath -m`; the word-ending `.claude` rule replaces the `hooks/launch-level-guard` token |
| INV-010 | Planned change #17 (item 2) | T-TAM-6 | `superclaude ... install` and `install_hooks` are TAMPER |
| INV-011 | Planned change #10 | T-GIT-2, T-GIT-3, T-GIT-4 | Conflict: UNKNOWN applies to the first git word in a segment only, so commit messages that mention git are not blocked; no separate `alias.` or `GIT_CONFIG_` rule (subsumed) |
| INV-012 | Planned change #11 | T-PSH-8 | Explicit `:<destination>` required; conflict: `-c`, `--config-env` and `GIT_CONFIG_` words are not banned in push segments (the explicit destination already defeats configured refspecs); `remote` and `config` writes are UNKNOWN via Change 10 |
| INV-013 | Planned change #12, #13 | T-GH-2, T-GH-8, T-MCP-1, T-MCP-2 | Conflict: merge words apply only to gh api writes, so reads of `mergeStateStatus` pass; MCP writes are blocked at every level instead of parsing `branch` arguments |
| INV-014 | Planned change #5 (U6 loose form) | T-BIND-3 | Conflict: loose markers bind only at the start of the prompt, not anywhere in the first line |
| INV-015 | Planned change #5 (U6), #29 (OB-H2) | T-BIND-4 | Leading whitespace and BOM accepted; conflict: no "first 512 characters" window; residual R6 |
| INV-016 | Planned change #9 (`tr`), #22 (cap) | T-SPD-5, T-FC-7 | 65,536-byte cap; `tr`, never `${s//...}` |
| INV-017 | Planned change #10 (G1 skip list and allowlist) | T-GIT-5 | `--attr-source` consumes a value |
| INV-018 | Planned change #22, #24 | T-REG-1, T-SPD-5 | Conflict: 5 s, not 3 s; every governed run asserted under 1 s |
| INV-019 | Planned change #4 (item 5) | T-BIND-14 | No dots in ids; invalid ids degrade to `worktree` while the store holds a session |
| INV-020 | Planned change #33 and this plan's coverage index | none | One rule per point; residual splits are O-1 to O-5 |
| INV-021 | Planned change #9 (`$` kept), #10 | T-GIT-2 | Variable, missing or substituted subcommands are UNKNOWN |
| INV-022 | Planned change #9 (N2) | T-NRM-1 | Conflict: one deletion form instead of scanning two forms |
| INV-023 | Accepted residual R1 plus owner decision O-7 | T-GAP-1 | "A script file or a program that runs git internally is not inspected; AC-6's wrapper clause is met for inline wrappers only." |
| INV-024 | Planned change #6 (P6) | T-FC-6 | Missing or invalid `session_id` with a non-empty store governs at `worktree` |
| INV-025 | Planned change #15, plus accepted residual R5 | T-ESC-1, T-ESC-5 | Conflict: no command-position rule; `claude-code`, `ccsession*` and terminal tools added instead. Sentence: "`claude -c`, `claude -r` and an interactive `claude` started other than through tmux or screen are not blocked (UNVERIFIED U14)." |
| INV-026 | Planned change #15 | T-ESC-2, T-ESC-5 | `orca` read allowlist; tmux, screen, xdotool, ydotool |
| INV-027 | Planned change #16 | T-TRN-1, T-TRN-3 | Conflict: "ignore approval while a monitor is live" not taken (needs state); TURN is blocked before approval instead |
| INV-028 | Planned change #16 | T-TRN-2, OB-H3 | TURN blocked at `W` only |
| INV-029 | Planned change #10 (remote and config writes UNKNOWN), plus owner decision O-12 and residual R11 | T-GIT-2 | Literal `--repo` not compared with origin by default |
| INV-030 | Accepted residual R8 | T-TAM-1 | "In a governed session, commands and edits that name `.claude/settings.json` are blocked, including the tracked project file." |
| INV-031 | Planned change #21, #23 | T-FC-3, T-FC-4 | The trap and the default-deny line print LL-BROKEN |
| INV-032 | Planned change #15, #24 | T-ESC-4, T-REG-3 | `SendMessage` is ESCAPE and in the matcher |
| INV-033 | Planned change #14, #18 (item 2), plus owner decision O-8 | T-SKL-1, T-GRID-3 | "AC-1's plan stop is command-level; direct edits stay allowed." |
| INV-034 | Planned change #10 (COMMIT list), #12, #13, plus residual R9 | T-GIT-6, T-GIT-7 | `cherry-pick`, `revert`, `am`, branch `update-ref` are COMMIT |
| INV-035 | Planned change #8, #15, #16 | T-TRN-4 | One test table lists every turn-starting or input route |
| INV-036 | Planned change #15, #24, #25, #29 | T-REG-3, OB-H1 item 6 | Anchors checked by OB-H1 |
| INV-037 | Planned change #5, #17 | T-BIND-3, T-BIND-7, T-TAM-5, T-TAM-6 | All four falsifiers have cases |
| INV-038 | Planned changes #9 to #13 and #22, plus owner decision O-7 | T-NRM-1, T-GIT-5, T-PSH-8, T-GH-2, T-SPD-5 | Each falsifier closed except script wrappers (R1) |
| INV-039 | Planned change #19 (precedence), #23 | T-MSG-2, T-MSG-3, T-MSG-4 | Messages use only `{level}`, `{store}`, `{sid}` |
| INV-040 | Planned change #22, #26, #29 | T-SPD-2, T-SPD-5, T-ISO-7 | Subagent tests driven by captured OB-H1 payloads; R14 for what tests cannot see |

## Open decisions for the owner

The default is the rule written into the spec. O-1 to O-5 are the Round 2 residual splits (INV-020), decided by the criterion; O-7 is the AC-6 limit the owner must accept explicitly.

| Id | Question | Default (rule in force) | Alternative | Why the default |
|---|---|---|---|---|
| O-1 | Cross-check the record's worktree path against `cwd` at bind? | No | Record stores the launch path; a mismatch binds `degraded` and keeps the record (Advocate 3) | The nonce is single use and a failed bind can no longer free anyone; the check adds real-path and symlink cases |
| O-2 | `--force` at `full --submit` | No rule | Block `--force`, `-f` and `+` refspecs; allow `--force-with-lease` (Advocate 1) | No AC names it; `/sc:pr-submit` never force pushes; `main` is protected by name either way |
| O-3 | `gh pr ready` | SUBMIT class (allowed at submit) | Never allowed (Variant 3) | Marking a draft ready is publishing, which `--submit` governs |
| O-4 | Register UserPromptExpansion for approval? | No | Register it with exact `command_name` matching (Advocates 1, 3) | V6 already delivers the typed line; the event adds an unverified field form |
| O-5 | Issue number in the block header | No | Store `level issue` in the session file and print it | AC-7 needs what, why, next step; the one-word state has no parse states |
| O-6 | Approval lifetime | Whole session | Expire or bind to a plan | No clock or plan identity to manage |
| O-7 | AC-6 "including through shell wrappers around git": accept that only inline wrappers are covered (R1)? | Accept | Add a second layer (for example a git `pre-push` hook) later | Scanning script files would block every plan that mentions a push |
| O-8 | Gate direct source edits at `worktree` | No (#322 owns the write boundary) | Allow writes only under `.dev/` before approval | The agent writes plans and notes legitimately |
| O-9 | If OB-H1 shows subagents get a different `session_id` | Stop; build nothing until decided | Build the reserve `cwd` fallback of Change 7 item 6, accepting its wrong case | X-004 |
| O-10 | `/sc:pr-submit`'s conflict-sync merge at `full --submit` | Stays blocked (only people merge) | Allow `merge --no-commit` at submit | AC-6 says no level permits a merge |
| O-11 | Launched sessions that carry an Orca worker preamble (WC-9) and need `orca orchestration` report commands | OB-H3 decides; none allowed now | Add the worker-report subcommands to the `orca` allowlist; if the session is a worker, `--submit` is unreachable | U7 unverified |
| O-12 | Compare a literal `--repo` value with `origin` at submit | No | Read `owner/name` at bind time and block other literal values | The hook is installed in every project; no AC names the fork rule |
| O-13 | More implement skills (`sc:improve`, `sc:cleanup`, `sc:spawn`, `sc:build`) | No | Add names to the IMPL set (one word each) | The issue names `/sc:implement` and `/task` |
| O-14 | MCP writes at `full --submit` | Blocked at every level | Allow at submit unless `branch` is `main`/`master` | MCP argument names are unverified (U12); `/sc:pr-submit` uses gh |
| O-15 | Old state files | A person removes them; the hook never prunes | The claim script prunes on re-claim | No clean-up state to get wrong |

## Changes NOT Being Made (with rationale)

Rows marked "alternative" are design alternatives that the spec lists in section 18 (Change 34); the other rows are base content dropped in the merge.

| Diff point | Approach not taken | Rationale (debate evidence) | Kind |
|---|---|---|---|
| D2 | HMAC over the state | The key is readable by the same user (A-004); no gain against T2 | alternative |
| D2 | Read-only mode bits | The agent can `chmod`; release gets harder | alternative |
| D2 | Root-owned directory | Install needs root | alternative |
| D4, C-007 | A real shell parser (reuse the #357 awk scanner) | 300 lines, three review rounds, nine ceilings (codebase-context section 2) | alternative |
| D4 | PATH shim for `git` | Absolute paths bypass it; needs a launch-environment change | alternative |
| D4, X-009 | Git-level hooks (`pre-push`, `reference-transaction`) | Shared with the person's own pushes via the common git directory; cannot tell which session called; `--no-verify` skips them | alternative |
| D1 | Environment variable from the shim | Shim out of scope; reach into hook processes unchecked; inherited by every child | alternative |
| D1 | Record keyed by worktree path or branch | Breaks on rename; governs a person's own session in that worktree (AC-4) | alternative |
| C-002, X-004 | Always-on `cwd` fallback (Variant 3) | Governs a person's own subagents (all three Round 2 tables) | alternative |
| C-015 | `onFailure: "block"` | Blocks ordinary sessions when the hook breaks (V8) | alternative |
| D5, O-8 | Source-edit gating at `worktree` | Plans are files; #322 owns the write boundary | alternative |
| D3 | Approval only by relaunch (seed A10) | Fails AC-3 | alternative |
| D3 | Approval read from PreToolUse(Skill) | The agent controls it | alternative |
| D3, O-6 | Approval expiry or plan binding | Adds clock and plan-identity states | alternative |
| C-005, O-4 | UserPromptExpansion registration | V6 suffices; unverified `command_name` form | alternative |
| C-001, O-1 | `cwd` cross-check at bind (Variant 3, Advocate 3 Round 2) | Single-use nonce plus degraded bind already prevent release | alternative |
| C-010, U-003 | Repo name equality (record `repo` or hard-coded `IronbellyOrg/IronClaude`) | Blocks the skill's own `--repo "$REPO"` (NE-1); wrong in other projects | alternative |
| C-009 | `git symbolic-ref` lookup of HEAD (Variants 1, 2) | Subprocess, `cwd` and `-C` gaps; replaced by named destinations (N-2) | base dropped |
| C-009 | Whole-command `master|main` regex (Variant 2) | Blocks `feature/main` and commit messages (N-5) | alternative |
| C-009 | Word list after `push` only (Variant 3) | Misses HEAD, `--all`, `--mirror` (X-007) | alternative |
| C-008 | `alias.` token and `git config alias.` rule | Subsumed by the git allowlist (Change 10) | base dropped |
| C-007 | Variant 3 wrapper list and four-word lookahead | A sub-parser; position-free words need no wrapper list | alternative |
| C-007 | Splitting words on `' " $ [ ] , =` (Variant 1) | Misses `\git` (N-1); replaced by quote deletion plus sweep | base dropped |
| INV-022 | Scanning two normalised forms | Deletion matches shell joining, so one form suffices | alternative |
| INV-025 | Command-position rule for `claude -c`/`-r` | Parser fragment; `-c`/`-r` alone over-block `grep` | alternative |
| C-013 | MCP `commit`/`push` substring block below submit only (Variant 1) | Would block `list_commits`; replaced by read prefixes plus block-at-every-level | base dropped |
| C-014 | Blanket `claude`/`orca` word block (Variant 3) | Blocks read-only `orca worktree current` and `grep claude` | alternative |
| C-014 | `claude` followed by any dash word (Variant 1); `-r` in the flag list (Variant 2) | Over-blocks `grep claude -rn docs/` | base dropped |
| C-012 | Monitor always blocked (Variant 3); Cron and Schedule blocked at every level | Breaks `/sc:pr-submit` waits at submit (INV-028); only `W` has an approval to forge | alternative |
| C-012 | Monitor, Workflow, RemoteTrigger unmatched (Variant 2) | Leaves a plain `git push` route and outside-hook routes open | alternative |
| S-004 | `--classify` argument, ERR trap, five named layers | Test-only surface; ERR not inherited by functions without `set -E` | base dropped |
| S-004 | Test that reads the policy block from the script | Checks the script against itself; the oracle lives in the test file | base dropped |
| C-001 | 30-minute record age check and the O-9 prune (Variant 1) | A single-use nonce makes age meaningless; clock edge case | base dropped |
| C-003 | JSON session record with `v`, `degraded`, nonce, repo, issue | Bad-JSON states; nothing reads the extra fields | base dropped |
| C-004 | `launch-level-guard` tamper token | Blocks work on this issue's own source | base dropped |
| C-016 | Regex-only identity read as the main path (Variant 1 fast path 2) | Forgeable as the sole read; kept only as the prefilter whose exit 0 needs every match unbound | base dropped |
| X-002 | Fail open when `jq` is missing (Variant 3) | Silent non-enforcement; V8 does not force it | alternative |
| X-003 | Block every matched call on bad state (Variant 2 F1) | Stops planning; degrading keeps work and approval | alternative |
| X-005 | Tamper rule in every session (Variant 3) | Blocks a person releasing a session from their own Claude session | alternative |
| X-010 | `Makefile` `_FRESHNESS_SCRIPTS` line; `@pytest.mark.manual` placeholders | No such Makefile list; `--strict-markers` fails collection | base dropped |
| A1 | SessionStart housekeeping, `flock`, clean-up | No state needing them (one-word files, atomic `mv` and `touch`) | alternative |
| D5 | Scanning the Agent `prompt` | Blocks wording, not actions; subagent calls are checked at the leaf | alternative |
| (new) | Skipping message text after `-m`/`--body` | Heredoc bodies defeat it and `git rebase -m` collides; LL-TEXT names `-F`/`--body-file` instead | alternative |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 1, 2, 3 | Low | Cosmetic or file-list errors | Revert to base sections 1 to 3 |
| 4 | Low | State format mismatch with the claim feature | Revert to base section 4 state paragraph; update CL-1 |
| 5 | Medium | A launch binds wrongly or not at all (depends on U8, A-006) | Revert to base section 4 binding steps; OB-H2 detects |
| 6 | Medium | A governed call exits early, or ordinary calls slow down | Revert to the C-016 consensus (`jq` first, regex only without `jq`) |
| 7 | Medium | Subagents ungoverned if U1 is false | Ship gate holds; owner decision O-9 |
| 8 | Low | Typed approval not seen | Register UserPromptExpansion (Change 8 item 7 contingency) |
| 9 | Medium | Redirection removal misreads a command | Drop N4; accept over-blocks on `2>&1` pushes |
| 10 | Medium | Allowlist blocks a needed git command | Add the subcommand to the list (one word) |
| 11 | Low | Agent cannot find the allowed push form | LL-PUSHNAME names it; OB-H3 measures |
| 12 | Medium | An unforeseen gh write behaves as SUBMIT | Add an action to the read list or the merge words |
| 13, 14 | Low | MCP or skill name mismatch | Adjust the keyword or name set |
| 15 | Low | Orca worker commands blocked | Owner decision O-11 |
| 16 | Low | Wait tools blocked where needed | Restore Change 16 item 2 per level |
| 17 | Low | Over-block on `.claude` paths | Narrow the word-ending rule |
| 18 | Low | None expected | Revert to base section 9 |
| 19, 20 | Low | Table and script disagree | T-GRID fails; fix whichever is wrong |
| 21 | Low | A failure path allows | T-FC cases fail; restore default deny |
| 22 | Medium | Flaky absolute timing on CI | Keep the ratio test; widen absolute limits |
| 23 | Low | Wording unclear | Edit message text only |
| 24 | Medium | Anchors ignored (U15) | Script re-checks names; only speed suffers |
| 25 | Low | Claim feature does not deliver CL-1 to CL-6 | Hook still binds `degraded` from any marker |
| 26 to 30 | Low to Medium | Observed checks delayed | `full` and `--submit` stay off real issues |
| 31 to 34 | Low | Register or decision list incomplete | Additive; amend the list |

## Review Status

- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-05T21:30:00Z
