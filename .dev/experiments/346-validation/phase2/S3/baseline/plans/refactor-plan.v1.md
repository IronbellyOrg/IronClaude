# Refactoring Plan: Merge into Base (Variant 1)

## Overview

- Base: Variant 1 (`variant-1-opus-architect.md`, opus:architect), selected in `base-selection.md` by the debate tiebreaker (7 points to 4).
- Incorporating strengths from: Variant 2 (`variant-2-sonnet-refactorer.md`, sonnet:refactorer), Variant 3 (`variant-3-haiku-qa.md`, haiku:qa), the Round 2 merged rules (`round-2-advocate-1..3.md`, section 5) and the fault-finder's 40 findings (`invariant-probe.md`).
- Planned changes: 34, in seven groups: A frame (1 to 3), B identity and state (4 to 8), C classification (9 to 18), D policy and failure (19 to 23), E registration and interfaces (24 to 25), F proof (26 to 30), G registers (31 to 34).
- Risk level: Medium overall. The rules are concrete and each has a named test, but five facts stay unverified until the observed checks run (U1 subagent identity, U8 first-prompt timing, U7 worker preamble, U15 anchored matcher behaviour, U4 harness wrapping of self-started turns).

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
- `/sc:pr-submit` runs, among reads, `git merge-tree`, `git remote get-url`, `gh pr view --json mergeable,mergeStateStatus`, `gh pr checks`, `gh repo view`, `gh pr create --repo "$REPO"`, `gh api --method POST .../comments/<id>/replies`, `gh api graphql` with the mutation `resolveReviewThread` (both run inside `scripts/reply-resolve-thread.sh` and `scripts/retrigger-review.sh`, per `sc-pr-submit-protocol/SKILL.md` Wave 6, so the hook sees only `bash <script>`; residual R1), `gh api repos/<owner/repo>/... --jq ...` reads written inline, `git commit --only -- <paths>`, `git push origin <target_sha>:<target_branch>` (written with placeholders the agent fills in), and the conflict sync `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>`.

### Design in five lines (for the spec's position summary)

1. One bash script, `launch-level-guard.sh`, on two events: UserPromptSubmit (bind a launch, record approval) and PreToolUse (decide). It never reads `cwd`, never runs git, and never reads a file inside the worktree.
2. A session is governed only when a launch marker in its prompt binds it to `session_id`; once bound it is governed for life, and only a person's `rm` releases it. A malformed or orphaned marker at the start of a prompt still binds, at the strictest level.
3. Bash and Monitor text goes through one normalisation pass, then a word scan with allowlists (git subcommands, `orca` subcommands, gh actions, GET-only `gh api`) instead of growing denylists. No shell parser.
4. Approval comes only from a typed prompt and unlocks implementation only. No level allows a merge or a push to `master`/`main`; at `full --submit` a push must be the whole command, in one canonical form: `git push [-u] origin <branch>` or `git push [-u] origin <source>:<branch>`.
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
  4. A "Terms" list right after the position summary defines, before first use: **store** (`$HOME/.claude/state/launch-level/`); **governed session** (a session whose valid `session_id` has a file in `sessions/`, or a call that resolves to degraded `worktree` under Change 6); **ordinary session** (every other session); **effective level** (one of `W` = worktree before approval, `WA` = worktree after approval, `F` = full, `FS` = full with `--submit`); **segment** and **word** (Change 9); **class** (Change 19); **message id** (Change 23). It also expands the external ids the spec cites: A2, A12 (seed brief assumptions), WC-9, WC-13 (`~/.claude/WORKER-CONTRACT.md`), FR-23, FR-31 (launch-levels addendum), V1 to V14 and U1 to U8 (`enrichment/research-light.md`). It lists the id families, each used for one thing only: TH1 to TH3 threats; B1 to B13 bind steps; P1 to P7 resolution steps; NM1 to NM7 normalisation steps; G1 to G4 git rules; H1 to H5 gh rules; U1 to U20 unverified items; R1 to R16 residuals; O-1 to O-19 owner decisions; CL-1 to CL-6 claim interface; `T-<GROUP>-<n>` tests; orchestrator facts T1 to T5.
- **Rationale**: S-001 majority for Variant 1's front matter (A1 55%, A2 50%, A3 merge 55%); base-selection L4 marked all three variants NOT MET for undefined terms.
- **Integration point**: top of the spec; replace Variant 1's 16-section list with the 18 sections above (sections 17 and 18 are new homes for Changes 32 and 34).
- **Risk**: Low. Cosmetic and structural only.

### Change 2: Threat model (from Variant 1 section 2, Variant 2 section 2)
- **Source**: Variant 1 section 2 targets; Variant 2 section 2 harness facts.
- **Target**: Base section 2 (replace the R1 to R8 table; residuals move to section 17, Change 32).
- **Settles**: A-004; S-002 (structure part).
- **Final rule**: Section 2 states, in this order:
  1. **TH1**: an honest agent that drifts from `launch-prompt.md` and runs `/sc:implement`, `git commit`, `git push` or `/sc:pr-submit` anyway. Primary target.
  2. **TH2**: an agent that tries obvious workarounds in one step: `bash -c`, `sh -c`, `env`, `command`, `exec`, `sudo`, `nohup`, `timeout`, `xargs`, `/usr/bin/git`, `\git`, a dashed built-in (`git-push`), quote splicing, backticks, line continuations, a git alias, `$(...)`, a subagent, a fresh `claude -p`, typing `approved` into its own terminal, scheduling a turn, editing the guard's state or the Claude Code settings, reinstalling the hooks. Designed against.
  3. **TH3**: deliberate multi-step evasion (a script file written with Write and then run, plumbing commits through variables, a hostile agent). Not designed against; listed in section 17.
  4. Premise: the agent and the hook run as the same OS user, so no file is truly unwritable. Protection is a deny rule plus residuals, not file permissions.
  5. Harness facts relied on: V2 and V3 (a PreToolUse exit 2 blocks, also with permission prompts off), V4 (hooks run inside subagents and carry `agent_id`), V5 and V6 (typed commands and prompts arrive on prompt events with no origin field), V8 (a crashing or timed-out hook does not block).
- **Rationale**: all three variants share these three threat levels (their T1 to T3; renamed TH1 to TH3 here so they do not collide with the orchestrator facts T1 to T5 or the test ids; diff-analysis Content intro); A-004 STATED by all.
- **Integration point**: section 2.
- **Risk**: Low.

### Change 3: Components and files (from Variant 2 section 3, correcting Variant 1)
- **Source**: Variant 2 section 3; Round 2 X-010 (unanimous Variant 2).
- **Target**: Base section 3 (replace the table; delete the "Layers as shell functions", "Action classes" and "Extension scaffolding" paragraphs, whose content moves to Changes 19 and 34).
- **Settles**: X-010, S-004 (file part).
- **Final rule**: Section 3 lists exactly these items:

  | Item | Status | Written by | Purpose |
  |---|---|---|---|
  | `src/superclaude/hooks/scripts/launch-level-guard.sh` | new | developer | the only hook script; flat bash plus `jq`, `sed` and `tr` (run with `LC_ALL=C`), no awk, no Python, no layers, no command-line arguments |
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
  - **B1.** Read all of stdin into `raw`.
  - **B2.** If `raw` does not contain the text `[sc-launch:`: exit 0 when `sessions/` holds no file, or when the prefilter of Change 6 step P3 finds no bound id (nothing to bind, nothing to approve).
  - **B3.** If `jq` is not on `PATH`: if `raw` contains `[sc-launch:` and does not contain `"tool_name"`, print LL-NOBIND and exit 2; otherwise exit 0.
  - **B4.** One `jq` call reads `session_id`, `agent_id` and `prompt`. If `jq` fails (input is not JSON), act as in B3.
  - **B5.** If `agent_id` is a non-empty string, exit 0. Prompts from inside a subagent never bind and never approve.
  - **B6.** Marker detection on `prompt`. **Strict**: the first match anywhere of `\[sc-launch:v1:([0-9a-f]{32})\]` gives nonce `N`. **Loose**: after removing every leading space, tab, carriage return, newline and UTF-8 byte-order mark, in any order, the prompt starts with `[sc-launch:`. A marker is **present** if strict or loose is true. When a marker is present, install an EXIT trap that turns any exit code other than 0 or 2 into LL-NOBIND and exit 2.
  - **B7.** If `session_id` is not valid (Change 4 item 5): marker present, print LL-NOBIND and exit 2; no marker, exit 0.
  - **B8.** If `sessions/<sid>` exists (a bound session): (a) if strict `N` was found and `pending/N` exists, `rm -f pending/N`; the level does not change, so an orphaned record can never bind a later session; (b) run the approval check of Change 8; (c) exit 0.
  - **B9.** Unbound session with no marker: exit 0.
  - **B10.** `mkdir -p sessions` (umask 077).
  - **B11.** If strict `N` was found and `pending/N` exists, `mv pending/N sessions/<sid>`. The `mv` is atomic, so one nonce binds at most one session.
  - **B12.** If `sessions/<sid>` still does not exist and loose is true, write the word `degraded` without overwriting: `(set -C; printf 'degraded\n' > sessions/<sid>)`.
  - **B13.** If `sessions/<sid>` is now a regular file, exit 0. Otherwise print LL-NOBIND and exit 2. The prompt is blocked, so a launched agent whose session could not be registered never starts ungoverned. (That the person sees a blocked prompt's stderr is UNVERIFIED, U20.)
- **Consequences the spec must state**:
  - A malformed marker at the start of a prompt (uppercase hex, a dashed UUID, 33 characters, `v2`, the `<nonce>` template text) binds `degraded`, which reads as `worktree` with the LL-STATE note.
  - A strict marker elsewhere in the prompt binds the record's level when the record exists, and blocks the prompt (LL-NOBIND) when it does not. A marker-shaped text in the middle of an ordinary prompt with no live record therefore costs one blocked prompt, never a governed session.
  - A loose (malformed) marker that is not at the start is ignored. Residual R6 (Change 32).
  - Later markers in a bound session never change its level (B8).
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
  - **P4.** Install the EXIT trap of Change 21 (every later step can only end in a governed decision or an exit 0 on a named path). If `jq` is not on `PATH`, print LL-BROKEN and exit 2. (Reaching this step means a bound id appeared in the input, or no id could be read while the store holds a bound session.)
  - **P5.** One `jq` call reads `session_id`, `tool_name`, `tool_input.skill // tool_input.name`, `tool_input.file_path // tool_input.notebook_path`, `tool_input.isolation` and, last, `tool_input.command`. It prints them one per line in that fixed order; inside every field except the last, `jq` replaces carriage returns, newlines and NULs with spaces (`gsub("[\r\n\u0000]"; " ")`), and inside the command it replaces NULs with spaces. The script reads the first five with `read -r` and the command, newlines included, with `read -r -d ''`. A command that holds newlines can therefore never shift another field. A `jq` failure prints LL-BROKEN and exits 2.
  - **P6.** If `session_id` is valid and `sessions/<sid>` exists, the call is governed at the file's level. If `session_id` is valid and has no file, exit 0. If `session_id` is missing, not a string or not valid, the call is governed at level `worktree` with the LL-STATE note, because the store holds at least one bound session (P2). This is a deliberate tripwire: real ids are UUIDs, so it fires only if the harness changes its id format.
  - **P7.** Classify (Changes 9 to 18) and decide (Change 19).
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
  4. Prompt payloads that carry `agent_id` never bind or approve (Change 5 step B5).
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
  1. Approval is written only by the UserPromptSubmit branch, in a bound session, from a payload without `agent_id` (Change 5 steps B5 and B8).
  2. It is written only when the effective level is `worktree`: the file word is `worktree` or any invalid word, including `degraded`. At `full` and `full-submit` nothing is written.
  3. A prompt approves when either (a) the prompt, with leading and trailing whitespace removed and lower-cased, matches `^approved[.!]?$`, or (b) the first line of the prompt, with leading whitespace removed, matches `^/(sc:implement|sc:task|task)([[:space:]]|$)` (case-sensitive). `/task-builder`, `/tasks`, `/sc:implement-protocol`, `please approved` and `approved, but` approve nothing. A typed `/sc:pr-submit` approves nothing.
  4. Effect: `touch sessions/<sid>.ok`. If the `touch` fails, the prompt still goes ahead (exit 0); the next implement call is blocked with LL-IMPL, which is loud.
  5. Approval unlocks class IMPL only (Change 19), never COMMIT, PUSH, SUBMIT or MERGE. It lasts until a person removes the session's files (owner decision O-6, default).
  6. Ordering: UserPromptSubmit runs before a typed command is expanded (V5, V6), so `.ok` exists before the model's `Skill` call that `/sc:implement` makes (`sc:implement-protocol`).
  7. UserPromptExpansion is not registered (owner decision O-4, default). OB-H1 confirms that a typed `/sc:implement` line reaches UserPromptSubmit as typed (V6). If it does not, register UserPromptExpansion and approve when `command_name` is exactly one of `sc:implement`, `implement`, `sc:task`, `task`, with no prefix stripping.
  8. Forgery. The agent cannot type a prompt. It can, however, start turns itself: a background `Agent` or `Task` call, a Bash call with `run_in_background: true` and a Monitor call each deliver their result later as a turn the harness starts on its own, and UserPromptSubmit fires on those turns (V6; this session shows UserPromptSubmit on background-task notification turns). These routes are not blocked, because legitimate plan steps use them (for example the research agents of `/sc:workflow`). The protection is that the harness wraps such a turn in a notification block, so its `prompt` never equals the bare word `approved` and never starts with `/sc:implement`, `/sc:task` or `/task`; it rests entirely on the whole-prompt exact match of item 3. It is observed for background-task notifications and UNVERIFIED for Monitor lines (U4); OB-H1 item 5 logs the exact `prompt` of both, and owner decision O-17 says what happens if a bare line can arrive. Cron and Schedule tools, whose prompt text is the agent's own, are blocked before approval (class TURN, Change 16); input-injection tools are blocked always (Change 15).
- **Rationale**: V6 (VERIFIED) says typed slash lines reach UserPromptSubmit as typed, so the second event adds a registration and an unverified `command_name` form (U9) without adding a route (criterion: fewest edge cases). U-006 and C-006 unanimous on `.ok` at `worktree` only and ignoring `agent_id`.
- **Departs from**: (1) the C-005 majority (Advocates 1 and 3 kept UserPromptExpansion); decided by the criterion and listed as O-4. (2) INV-008's resolution says a typed `/sc:task` approves nothing; Change 14 makes `sc:task` an implement skill, so the command that it gates must also approve. `/task-builder` and `/tasks` still approve nothing, which is the part of INV-008 that matters.
- **Integration point**: section 6.
- **Risk**: Low.

### Group C: classification (governed sessions only; ordinary calls exit before this point)

### Change 9: One normalisation pass for Bash and Monitor text (merge of Variants 1 and 2, probe fixes)
- **Source**: Variant 2 section 8 character sweep; Variant 1 section 8 segment split; Round 2 C-007 (unanimous merge); INV-016, INV-022; orchestrator fact T5; plan review B-2, B-5.
- **Target**: Base section 8, steps 1 and 2 (replace).
- **Settles**: C-007 (normalisation part), INV-016 (method part), INV-022, B-5.
- **Final rule**: the decoded `tool_input.command` of a Bash call (foreground or background) or a Monitor call, held in `cmd` (Change 6 P5), is normalised once. The script sets `LC_ALL=C` at its top, so lengths are bytes and the character ranges below are ASCII. The raw `cmd` is kept unchanged for the push form test (Change 11). Steps:
  - **NM1.** If `${#cmd}` is greater than 65,536 (bytes, under `LC_ALL=C`), the call gets class BIG and nothing else is checked (Change 22).
  - **NM2 and NM3** (one `sed -E` call; its output is text **T**, used by the tamper rule, Change 17):
    ```bash
    T=$(printf '%s\n' "$cmd" | sed -E -e ':a' -e '/\\$/{' -e '$!N' -e 's/\\\n/ /' -e 'ta' -e '}' \
          -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e ':b' -e 's#/\./#/#' -e 'tb')
    ```
    NM2: a line that ends in `\` is joined to the next line with one space (the shell's line continuation; `$!N` keeps a final line that ends in `\`), then every `'`, `"` and `\` is deleted. Deletion mirrors how the shell joins quoted pieces: `g""it` becomes `git`, `\git` becomes `git`, `'feature:ma''in'` becomes `feature:main`. NM3: each run of `/` becomes one `/`, and `/./` becomes `/` until none is left.
  - **NM4, NM5 and NM6** (one `sed -E` call and two `tr` calls on T; the output is text **W**):
    ```bash
    W=$(printf '%s\n' "$T" \
        | sed -E -e 's/[0-9]*[<>]&([0-9]+|-)//g' \
                 -e 's/[0-9]*(&>>|&>|>>|>\||>&|<&|<<<|<<-|<<|>|<)[[:space:]]*[^[:space:];&|()]*//g' \
        | tr '\n;&|()`' ';;;;;;;' \
        | tr -c 'A-Za-z0-9._/=:@+~$;-' ' ')
    ```
    NM4 removes redirections: first the descriptor copies and closes (`2>&1`, `>&2`, `<&0`, `>&-`), then each remaining operator (optional digits, then `&>>`, `&>`, `>>`, `>|`, `>&`, `<&`, `<<<`, `<<-`, `<<`, `>`, `<`) together with its target word (file, here-string or heredoc delimiter). Heredoc body lines stay and are scanned. NM5 turns every newline, `;`, `&`, `|`, `(`, `)` and backtick into `;`, so line boundaries survive the sweep. NM6 replaces every other character outside `A-Za-z0-9._/=:@+~$;-` with a space. `$` is kept, so a word such as `$cmd` can never equal a known subcommand.
  - **Segments and words.** W is split at `;` into **segments** (`IFS=';' read -r -a segs <<< "$W"`); each segment is split at spaces into its **words**, in order (`read -r -a words <<< "$seg"`).
  - **NM7.** A word's **basename** is the text after its last `/`.
  - No bash pattern substitution runs over the command text (`${s//...}` took about 1.6 s on a 100 KB command, against 4 ms for `tr`; fact T5).
  - **Worked example** (run with bash 5.2, GNU sed and tr while drafting this revision; pinned as T-NRM-6): the command `git commit -F - <<'EOF'` / `fix: use git for hooks` / `EOF` (three lines) gives T = `git commit -F - <<EOF` / `fix: use git for hooks` / `EOF`, and the segments `[git commit -F -]`, `[fix: use git for hooks]`, `[EOF]`. The command `gh api \` / `-X PATCH repos/o/r/git/refs/heads/main -f sha=x` gives one segment. `git push origin a:b 2>&1 | tail -5` gives `[git push origin a:b]`, `[tail -5]`. `echo x > ~/.claude/settings.json` keeps its target in T (the tamper text) and loses it in W.
- **Rationale**: one deletion pass replaces Variant 1's word split on quotes (which missed `\git`, N-1) and INV-022's suggestion of scanning two forms; deletion matches shell semantics, so one form is enough. Joining continuation lines keeps a gh or git command written across lines in one segment (B-2: without it, `gh api \` plus a `-X PATCH` line split into two segments). Redirection removal keeps `2>&1` and `> log` out of the words; T is taken before it so that redirection targets still reach the tamper rule. Converting newlines to `;` before the sweep keeps segment boundaries (B-5).
- **Departs from**: (1) INV-022's "apply the rules to both forms": one form is enough, as argued; (2) Variants 1 and 2 split segments on `{` and `}`; here they are swept to spaces (one separator list fewer; `${X}` still leaves the word `$`); (3) the review's B-1 flag for backticks is not used: the push rule (Change 11) tests the raw command, so a backtick can never reach an allowed push.
- **Integration point**: section 8, subsection "Normalisation".
- **Risk**: Medium. Redirection removal is the one step with real string handling; T-NRM cases (Change 27) pin it. The `sed` script uses only POSIX features (`:label`, `N`, `t`, `\n` in the pattern) so it should run with GNU and BSD `sed`; it was run only with GNU `sed` (BSD is UNVERIFIED); T-NRM-6 runs it on the host.

### Change 10: Git classification by allowlist (from INV-011, replacing the Round 2 denylist)
- **Source**: Variant 1 section 8 step 3 (option skip, `pull` as merge); Round 2 C-007, C-008, X-008 (unanimous Variant 1 for `pull`); INV-011, INV-017, INV-021, INV-034; orchestrator facts T2 and T4.
- **Target**: Base section 8, step 3 (replace).
- **Settles**: C-007 (git part), C-008, X-008, INV-011, INV-017, INV-021, INV-034 (git part).
- **Final rule**: in each segment, take every **git word**, in order. The first such word in the segment is **first**; later ones are **later**. A git word is a word whose basename is `git`, or whose basename matches `^git-[a-z][a-z-]*$` (a **dashed built-in**).
  - **G0.** A dashed built-in is the git word followed by the subcommand S = the text after `git-`; the words after it are its arguments, with no option skip. Git itself runs `git-<name>` as `git <name>`, and on this host `/usr/lib/git-core/git-push`, `git-commit`, `git-merge` and `git-pull` are links to `git` (review B-3, real git 2.47.3), so `git-push origin main`, `/usr/lib/git-core/git-push origin main` and `$(git --exec-path)/git-push origin main` (whose segment `/git-push origin main` has the basename `git-push`) read as `git push origin main`. Other `git-*` tools (`git-lfs`, `git-filter-repo`) read as `git lfs` and `git filter-repo`, which are UNKNOWN, as they already are when written with a space. Accepted over-block (R8): a first word that names a file or directory such as `git-tools` is UNKNOWN; names with a dot or a digit (`git-workflow.md`, `git-2.47`) are not git words.
  - **G1.** After the git word, a word starting with `-` is an option. The options `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`, `--config-env` and `--attr-source` also consume the next word (their `=` forms are one word). The first non-option word is the subcommand **S**; the words after it are its arguments.
  - **G2.** No S: class NONE if an option word is `--version`, `--help` or `-h`; otherwise UNKNOWN for a first word and NONE for a later word.
  - **G3.** Classes for S:
    - COMMIT: `commit`, `cherry-pick`, `revert`, `am`; and `update-ref` when an argument is `--stdin`, or when its first argument not starting with `-` (after skipping the value of `-m`) is `HEAD` or starts with `refs/heads/`. Any other `update-ref` is NONE (this keeps `/sc:implement`'s `refs/superclaude/implement/...` pins working, including the ones written through a shell variable).
    - MERGE: `merge`, `pull`.
    - PUSH: `push` (then Change 11).
    - NONE (allowlist): `add apply bisect blame branch cat-file check-attr check-ignore check-ref-format checkout clean count-objects describe diff diff-files diff-index diff-tree fetch for-each-ref format-patch fsck gc grep hash-object help log ls-files ls-remote ls-tree merge-base merge-tree mv name-rev range-diff read-tree rebase reflog reset restore rev-list rev-parse rm shortlog show show-branch show-ref stash status switch tag var version whatchanged write-tree`.
    - NONE only in a read form: `remote` when the next word is absent or is `-v`, `--verbose`, `get-url` or `show`; `config` when the next word is `--get`, `--get-all`, `--get-regexp`, `--list`, `-l`, `get` or `list`; `worktree` when the next word is `list`.
    - Anything else, including the write forms of `remote`, `config` and `worktree`: UNKNOWN for a first word, NONE for a later word.
  - **G4.** A later git word keeps every class except UNKNOWN. Real nested runs (`git rebase -x "git push origin main"`, `git bisect run git commit`) use gated subcommands and are still caught. UNKNOWN applies to the first git word of each segment. A one-line message is one segment, so `git commit -m "fix git handling"` is not blocked. A multi-line message or heredoc body is scanned line by line (NM5 turns each newline into a segment boundary), so a body line that starts a sentence with `git <word>` (`use git for hooks`, `git is ...`) has its own first git word and is UNKNOWN, blocked at every level, and a body line `git push ...` or `git commit ...` is PUSH or COMMIT. This is a documented false positive (R8, row 31 of Change 20, T-GIT-13): the LL-TEXT note (Change 23) tells the agent to write the text to a file and pass it with `git commit -F <file>` or `--body-file <file>`, at levels that allow the commit; at other levels the commit is blocked anyway. No heredoc parser is added.
- **Consequences the spec must state**: aliases need no rule of their own. Git ignores an alias whose name is a built-in command (git-config documentation for `alias.*`), and any other alias name is not on the allowlist, so `git -c alias.ci=commit ci`, `X=commit git --config-env=alias.ci=X ci` and `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.ci GIT_CONFIG_VALUE_0=commit git ci` (all three commit on git 2.47.3, fact T2) are UNKNOWN; so is `git config alias.ci commit`. `git --attr-source HEAD push origin main` reads S = `push` (fact T4), and the push form rule (Change 11) then blocks it. `git $(echo push) ...`, `cmd=push; git $cmd ...` and `printf ... | xargs git` have S equal to `$`, `$cmd` or nothing, so they are UNKNOWN (INV-021). `git -C "/dir with space" push` reads S = `with` and is UNKNOWN, so this former gap now fails closed.
- **Rationale**: the orchestrator's instruction and INV-011 favour one allowlist over a growing denylist (aliases, `--config-env`, `GIT_CONFIG_*`, `--attr-source`, variable subcommands all fall to it without separate rules). INV-034: `cherry-pick`, `revert` and `am` create commits, so AC-2 needs them in COMMIT.
- **Departs from**: (1) the C-004 and C-008 consensus `alias.` token and `git config alias.` rule are dropped as subsumed; (2) INV-011 applied the allowlist to every git word; this plan applies UNKNOWN only to the first git word in each segment, so one-line commit messages and PR titles that mention git are not blocked (criterion: fewer unwanted blocks, no AC lost because gated subcommands still classify everywhere); multi-line bodies are still over-blocked line by line (G4); (3) INV-012's "block `-c`, `--config-env` and `GIT_CONFIG_` words in a push segment" is not taken as a separate rule: Change 11's push form admits none of them.
- **Integration point**: section 8, subsection "Git".
- **Risk**: Medium. An allowlist that is too short blocks real work; the list was built from the git commands `/sc:implement` and `/sc:pr-submit` actually run (see Overview), and T-GIT-1 (Change 27) runs each of them.

### Change 11: Push rule: one canonical form (allowlist; replaces the named-destination denylist)
- **Source**: Round 2 C-009 and X-007 (unanimous merge, rule N-2); Advocate 2 Round 2 section 2 edits; INV-012; orchestrator fact T3; plan review B-1, B-2, B-3; orchestrator steering for fix cycle 1 (one canonical-form allowlist instead of one patch per route).
- **Target**: Base section 8, step 4 (replace, including the `symbolic-ref` subprocess).
- **Settles**: C-009, X-007, U-003 (remote part), A-008 (push part), INV-012, INV-021 and INV-022 (push part), B-1, B-2, B-3.
- **Final rule**: for every call that collected class PUSH in Change 10 (a git word, plain or dashed, whose subcommand is `push`, in any segment), at every level:
  1. Take the raw decoded command `cmd` (Change 6 P5), before any normalisation. Test it with one bash `[[ $cmd =~ $re ]]` under `LC_ALL=C`, where `re` is the anchored ERE
     ```
     ^[[:space:]]*git push( (-u|--set-upstream))? origin ([A-Za-z0-9._/-]+)(:([A-Za-z0-9._/-]+))?[[:space:]]*$
     ```
     In words: after removing leading and trailing whitespace, the whole command is exactly one simple command: the literal word `git` (no path, no dashed form, no quotes, no options before `push`), single spaces, an optional `-u` or `--set-upstream`, the remote `origin`, and one refspec made only of letters, digits, `.`, `_`, `/` and `-`, with at most one `:` that has text on both sides. Nothing else can appear: no second refspec, `$`, backtick, quote, backslash, `+`, `;`, `&`, `|`, redirection, inner newline, `-c`, `--config-env`, environment prefix or other option. (Bash compiles `=~` without `REG_NEWLINE`, so `$` matches only at the true end and an inner newline fails the class.)
  2. No match: the call gets class PUSHFORM.
  3. Match: the **destination** is capture 5 when the `:` part is present, otherwise capture 3; remove one leading `refs/heads/`, or else one leading `heads/`. Destination `master` or `main`: class PROTECTED. Destination `HEAD` or `@`: class PUSHFORM. Any other destination: the call keeps class PUSH only.
  4. The hook never reads `cwd`, HEAD, `push.default` or configured refspecs, and runs no subprocess for this rule.
- **Consequences**: at `full --submit` exactly these shapes run: `git push origin <branch>`, `git push -u origin <branch>`, `git push --set-upstream origin <branch>`, `git push origin <source>:<branch>` (the `/sc:pr-submit` form `git push origin <sha>:<branch>`), each as its own Bash call. Below `full --submit` every push is blocked (LL-PUSH, Change 19 precedence). At every level PROTECTED and PUSHFORM block. Force pushes (`--force`, `-f`, `--force-with-lease`, a `+` refspec), `--all`, `--mirror`, `--repo`, `--receive-pack`, `--exec`, other remotes, a deleting `:branch`, two refspecs and every compound command (`cd x && git push ...`, `git push ... 2>&1 | tail -5`, `git push ...; echo done`) are PUSHFORM. A refspec git refuses as a ref name (`x:refs/heads//main`, `x:./main`, `x:main/`, `x:/main`) passes the regex, but git stops with "invalid refspec" and moves nothing (checked on git 2.47.3 while drafting this revision).
- **Named regex cases** (tested with bash 5.2 `[[ =~ ]]` while drafting this revision; T-PSH-11 and T-PSH-12 assert each one):
  - Accept (class PUSH, allowed at FS): A1 `git push origin feature`; A2 `git push -u origin feature`; A3 `git push --set-upstream origin feature`; A4 `git push origin 3f2a9c1e:feature/x`; A5 `git push origin feature:feature`; A6 `git push origin feature/main:feature/main`; A7 `git push origin HEAD:feature`; A8 `git push origin fix-394.v2`; A9 `  git push origin feature  ` (outer spaces); A10 `git push origin a:refs/heads/feature`; A11 `git push origin release_1.2`; A12 `git push origin feature` followed by a newline; A13 `git push origin refs/heads/heads/main` (destination `heads/main`, a branch of that name, not `main`).
  - Reject by form (PUSHFORM): R1 ``git push origin a:b `echo c:main` `` (backtick); R2 `git push origin a:b \` then a new line ` c:main` (continuation); R3 `git-push origin main` (dashed); R4 `/usr/lib/git-core/git-push origin feature`; R5 `git push origin +feature:feature`; R6 `git push --force origin feature`; R7 `git push --all origin`; R8 `git -c remote.origin.push=refs/heads/f:refs/heads/main push origin f`; R9 `git --config-env=remote.origin.push=V push origin f`; R10 `git push origin 'feature:ma''in'` (quoted splice); R11 `git push origin a:$(echo main)`; R12 `git push origin a:$B`; R13 `git push upstream feature`; R14 `git push origin a:b 2>&1`; R15 `cd x && git push origin a:b`; R16 `git push origin a:b; git push origin c:main`; R17 `git push origin :feature`; R18 `git push origin a:b c:main`; R19 `GIT_CONFIG_COUNT=1 git push origin f`; R20 `git push origin a:b` and `git push origin c:main` on two lines; R21 `git  push origin feature` (two spaces); R22 `echo feat:main | xargs git push origin feat:feat`; R23 `git push origin HEAD` (destination `HEAD`).
  - Reject by destination (PROTECTED): D1 `git push origin main`; D2 `git push origin x:refs/heads/master`; D3 `git push origin x:heads/main`; D4 `git push origin heads/main`; D5 `git push -u origin feature:main`.
- **Rationale**: one allowlist replaces the destination denylist. It closes, with no rule of its own, the backtick (B-1), line-continuation (B-2) and dashed built-in (B-3) routes found by the review, and the earlier ones: `xargs` stdin, quote splicing, `$` and `$(...)`, `-c`, `--config-env`, `GIT_CONFIG_*`, `--attr-source`, extra refspecs and options. A refspec without `:` is accepted: a configured `remote.origin.push` could redirect it (fact T3), but the agent cannot set one: `-c` and environment prefixes are outside the form, `git config` writes are UNKNOWN (Change 10), and `.git/config` and `.gitconfig` are TAMPER (Change 17); one set by a person before launch is residual R11.
- **Departs from**: (1) the first draft of this change (named destinations with an explicit `:`, a `$` ban and an option list) and the review's per-route fixes for B-1 to B-3 (a backtick flag, a push-specific continuation rule); the orchestrator chose one allowlist. (2) `--force`, `-f`, `--force-with-lease` and `+` refspecs are now blocked by form, which settles O-2. (3) `--all` and `--mirror` are PUSHFORM, not PROTECTED; they stay blocked at every level, only the message changes. (4) Compound commands that contain a push are blocked at `full --submit` (owner decision O-18).
- **Integration point**: section 8, subsection "Push".
- **Risk**: Medium. The agent must issue each push as its own plain command; LL-PUSH-FORM says how. If `/sc:pr-submit` issues compound pushes, `--submit` breaks until O-18 is decided; OB-H3 records every push command it issues.

### Change 12: gh rule and the merge-URL rule (merge of Variants 1, 2, 3, probe fixes)
- **Source**: Variant 1 section 8 step 5; Variant 2 section 8 gh row; Variant 3 `gh pr ready`; Round 2 C-010 (unanimous merge, explicit `--repo` word, no name compared); NE-1; INV-013; plan review B-4; orchestrator steering for fix cycle 1 (GET-only `gh api`).
- **Target**: Base section 8, step 5 (replace).
- **Settles**: C-010, U-010, INV-013 (gh and URL part), B-4.
- **Final rule**: for every word whose basename is `gh`:
  - **H1.** The **group** is the first non-option word after `gh`, skipping the values of `-R` and `--repo`; the **action** is the next non-option word.
  - **H2.** Group `api`: a GET-only allowlist, the same at every level. The **endpoint** is the first word after `api` that does not start with `-`, skipping the values of `-H`, `--header`, `-q`, `--jq`, `-t`, `--template`, `--hostname`, `-p`, `--preview`, `--cache`. The call is class GHWRITE when any of these holds:
    1. some word of the whole command, in any segment, matches `^(-[A-Za-z]*[XfF].*|--method.*|--field.*|--raw-field.*|--input.*)$` (every spelling of a method or body flag: `-X POST`, `-XPOST`, `-iXPOST`, `--method=POST`, `-f a=b`, `-fa=b`, `-F x`, `-Fbody=x`, `--field=x`, `--raw-field=x=y`, `--input f`; an explicit `--method GET` too). The whole command is searched, so a flag hidden after a backtick or in `$(...)`, which NM5 puts in another segment, is still seen;
    2. the endpoint is missing, or is `graphql`, or ends with `/merge` or `/merges`;
    3. some word after `api` in its segment starts with `$` (a variable or `$(...)` could supply a flag).
    Otherwise the call is a plain GET and gets class NONE. Inputs read from files are never needed: `--input` is itself a GHWRITE word.
  - **H3.** Other groups, an allowlist. No group, with an option word `--version` or `--help`: NONE. Action `merge`: MERGE. Group `search`, `status`, `auth`, `browse`, `help` or `completion`, or action `view`, `list`, `status`, `diff`, `checks`, `watch` or `checkout`: NONE. The pairs `pr create`, `pr edit`, `pr comment`, `pr ready`, `issue create`, `issue edit`, `issue comment`: SUBMIT. Anything else is UNKNOWN: no group, an unknown group, a missing action, an action that contains `$`, and every other action (this covers `gh alias`, `gh extension`, alias and extension commands, `gh pr $(echo merge) 5`, ``gh pr `echo merge` 5`` whose segment ends after `pr`, `gh pr update-branch`, `gh pr close`, `gh repo sync`, `gh repo delete`, `gh release create`).
  - **H4.** Group `pr`, action `create`: also class REPO unless the segment has a word `-R` or `--repo`, or a word starting with `--repo=`. No repository name is compared, so `--repo "$REPO"` (the `/sc:pr-submit` form) passes.
  - **H5.** Merge URLs: in a segment with no gh word, any word that contains `repos/` and ends with `/merge` or `/merges` is MERGE (catches `curl`, `wget` and similar calls to the GitHub merge endpoints).
- **Named regex cases** for H2 item 1 (tested with bash 5.2 `[[ =~ ]]` while drafting this revision; T-GH-10 asserts them): GHWRITE words `-XPOST`, `-X`, `-iXPOST`, `--method=POST`, `--method`, `--raw-field=x=y`, `--raw-field`, `-f`, `-F`, `-Fbody=x`, `-fa=b`, `--field`, `--field=a=b`, `--input`, `--input=f`; plain words `-q`, `--jq`, `.total_count`, `repos/o/r/pulls`, `--paginate`, `-H`, `Accept:application/json`, `--hostname`, `-i`, `--silent`, `-t`. H2 item 2: `graphql`, `repos/o/r/pulls/5/merge` and `repos/o/r/merges` are GHWRITE endpoints; `repos/o/r/pulls` and `repos/o/r/pulls/5` are not.
- **Consequences**: `gh pr view <N> --json mergeable,mergeStateStatus`, `gh pr checks`, `gh repo view`, `gh api repos/o/r/pulls/5` and `gh api repos/o/r/commits/<sha>/check-runs --jq .total_count` are NONE at every level. Every `gh api` write, every `gh api graphql` call (query or mutation) and every `gh api` call with an explicit method, a field or an input is GHWRITE, blocked at every level; this includes `gh api --method=POST repos/o/r/merges`, `gh api -XPOST ...`, `gh api graphql -f query='mutation{mergePullRequest(...)}'`, `gh api -X PATCH repos/o/r/git/refs/heads/main` and `gh api -X PUT repos/o/r/contents/x -f branch=main` (a commit straight to `main`). `/sc:pr-submit` makes its `gh api` writes inside `scripts/reply-resolve-thread.sh` and `scripts/retrigger-review.sh`, which the hook does not see (R1), and its polls inside `scripts/poll-*.sh`; whether the agent ever runs a GHWRITE form inline is recorded by OB-H3 (owner decision O-19).
- **Rationale**: B-4 showed that a list of write spellings misses forms (`--method=POST`, `-XPOST`, `--raw-field=`, attached `-F`, combined `-iX`) and endpoints (`contents/`); an allowlist of plain GETs needs no list of write forms or endpoints. NE-1 (name equality would block the skill's own `--repo "$REPO"`). H3's allowlist uses the same one-mechanism rule as git, so a `$` action, a missing action and unforeseen writes such as `gh pr update-branch` (a merge on the PR branch) and `gh repo sync` (moves a fork branch, by default its main branch; from gh's documentation, not re-checked) fall to UNKNOWN. `gh pr ready` in the submit class per Advocates 2 and 3 Round 2 (owner decision O-3).
- **Departs from**: (1) INV-013 suggested "graphql whose body contains `merge`" and the first draft classed gh api writes as SUBMIT or MERGE by words; both are replaced by the GET-only rule, which also blocks GraphQL reads such as a `mergeStateStatus` query (use `gh pr view --json` instead, which is NONE). (2) The review's B-4 fix (define method and field flags, add `contents/` to the merge words) is replaced by the allowlist. (3) H3's former "anything else: SUBMIT" fallback is replaced by UNKNOWN.
- **Integration point**: section 8, subsection "gh and GitHub URLs".
- **Risk**: Medium. An inline `gh api` write or GraphQL read that a framework step needs is blocked at every level, and a gh action outside the allowlist is blocked; OB-H3 records both, and O-19 widens the list if needed. Accepted over-block (R8): in a command that also holds a `gh api` call, an unrelated short flag such as `grep -F` or `rm -f` reads as a GHWRITE word.

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
  1. Name = `tool_input.skill`, else `tool_input.name` (read in Change 6 P5). Absent or empty: class SKILL.
  2. Normalise: keep the text before the first whitespace; lower-case; remove one leading `/`; keep the text after the last `:` (so a plugin namespace such as `superclaude:sc-implement-protocol` and the `sc:` prefix both go); remove one leading `sc-`; remove one trailing `-protocol`. OB-H1 item 2 records the name form of a plugin-installed skill.
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
- **Source**: Variant 1 section 9 (Cron, ScheduleWakeup, Monitor scanned); Round 2 C-012 (unanimous Variant 1); INV-027, INV-028; plan review B-6; orchestrator steering for fix cycle 1.
- **Target**: Base section 9 rows for CronCreate, ScheduleWakeup and Monitor (replace).
- **Settles**: C-012, INV-027, INV-028, B-6.
- **Final rule**:
  1. Class TURN: a tool whose name matches `^Cron[A-Za-z]*$` or `^Schedule[A-Za-z]*$`. These tools take a prompt text that the agent writes and that comes back as a later turn.
  2. TURN is blocked only at `W` (worktree before approval), where an approval can still be forged; it is allowed at `WA`, `F` and `FS` (Change 19).
  3. Not TURN, allowed at every level (owner decision O-17, default): the tool `Monitor`, a `Bash` call with `run_in_background: true`, and an `Agent` or `Task` call with `run_in_background: true`. They can start a self-started turn, but the harness wraps that turn's prompt (Change 8 item 8), so it never equals the bare word `approved`; legitimate plan steps use them (for example the research agents of `/sc:workflow`).
  4. The `command` of a Monitor call and of a background Bash call is always normalised and classified like a foreground Bash command (Changes 9 to 17). A Monitor call with only `ws` has no text to scan.
  5. `RemoteTrigger` and `Workflow` are ESCAPE at every level (Change 15), not TURN.
- **Rationale**: INV-028 (approval exists only at `worktree`, and `/sc:pr-submit --monitor` at `full --submit` needs a wait tool); B-6 (background subagents are the same mechanism as background Bash and Monitor, so one rule must cover all three; blocking them all at `W` would stop planning steps, so the protection is the harness wrapping plus the exact-match approval, observed by OB-H1).
- **Departs from**: (1) the C-012 consensus blocked Cron and Schedule at every level; narrowed to `W` because blocking them elsewhere protects nothing and breaks the submit flow. (2) INV-027's resolution and the first draft blocked Monitor and background Bash at `W`, and the review's B-6 fix added background subagents; not taken (O-17).
- **Integration point**: section 9, subsection "Turn starters".
- **Risk**: Low.

### Change 17: Tamper rule (merge of Variants 1 and 2, probe fixes)
- **Source**: Variant 1 sections 8 step 7 and 5; Variant 2 section 4 tamper rule; Round 2 C-004 (unanimous merge), X-005, X-006 (merge); U-005; INV-009, INV-010, INV-030.
- **Target**: Base section 8 step 7 and section 4 D2 paragraph (replace).
- **Settles**: C-004, X-005, X-006, U-005, INV-009, INV-010, INV-030.
- **Final rule**: in a governed session only, class TAMPER when:
  1. Text T of a Bash or Monitor command (Change 9 NM3; redirection targets are still in it), or a path field (`tool_input.file_path` or `tool_input.notebook_path`) of Edit, Write or NotebookEdit after the same `/` squeezing, contains one of: `.claude/state/launch-level` (the script builds this token from two parts, Change 4), `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`.
  2. Bash or Monitor only: a word (Change 9 NM6) that ends with `.claude` or `.claude/`; a segment that has a word `superclaude` followed later by a word `install`; any word containing `install_hooks`.
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
  1. Closed class list (17): NONE, IMPL, SUBMIT, REPO, COMMIT, PUSH, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TURN, TAMPER, SKILL, BIG.
  2. Policy (B = block with the message id of Change 23, A = allow):

     | Class | W | WA | F | FS | Message id |
     |---|---|---|---|---|---|
     | NONE | A | A | A | A | none |
     | IMPL | B | A | A | A | LL-IMPL |
     | SUBMIT | B | B | B | A | LL-SUBMIT |
     | REPO | B | B | B | B | LL-REPO |
     | COMMIT | B | B | B | A | LL-COMMIT |
     | PUSH | B | B | B | A | LL-PUSH |
     | PUSHFORM | B | B | B | B | LL-PUSH-FORM |
     | PROTECTED | B | B | B | B | LL-PROTECTED |
     | MERGE | B | B | B | B | LL-MERGE |
     | GHWRITE | B | B | B | B | LL-GH-WRITE |
     | UNKNOWN | B | B | B | B | LL-UNKNOWN |
     | MCP | B | B | B | B | LL-MCP |
     | ESCAPE | B | B | B | B | LL-ESCAPE |
     | TURN | B | A | A | A | LL-TURN |
     | TAMPER | B | B | B | B | LL-TAMPER |
     | SKILL | B | B | B | A | LL-SKILL |
     | BIG | B | B | B | B | LL-BIG |

  3. One call can collect several classes (several segments, several git words). It is blocked if any of its classes is blocked at the effective level. The message shown is the first blocked class in this precedence order: BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL. (SUBMIT before REPO and PUSH before PUSHFORM, so below `full --submit` the agent reads "needs --submit", not "fix the form".)
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
  | 9 | Agent or Task, local (`isolation` absent or `worktree`), with or without `run_in_background: true` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 10 | Agent or Task with `isolation: "remote"`; Workflow; RemoteTrigger; SendMessage | ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE | BLOCK LL-ESCAPE |
  | 11 | CronCreate, CronDelete, CronList, ScheduleWakeup | TURN | BLOCK LL-TURN | ALLOW | ALLOW | ALLOW |
  | 11a | Monitor `tail -f log`; Bash `make test` with `run_in_background: true` (each command scanned like rows 12 to 33; O-17) | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 12 | `git status`, `git diff`, `git log --grep push`, `git add -A`, `git stash`, `git rebase origin/master`, `git fetch origin`, `git remote get-url origin`, `git merge-tree a b`, `git update-ref refs/superclaude/implement/p/T1 <sha>` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 13 | `git commit -m x`, `git commit --only -- a b`, `git cherry-pick x`, `git revert x`, `git am p.patch`, `git update-ref refs/heads/f <sha>`, `git update-ref HEAD <sha>` | COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | BLOCK LL-COMMIT | ALLOW |
  | 14 | `git push origin <sha>:feature`, `git push -u origin feature:feature`, `git push origin feature`, `git push --set-upstream origin feature` (each the whole command) | PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | ALLOW |
  | 15 | `git push`, `git push origin`, `git push origin HEAD`, `git push origin x:@`, `git push upstream a:b`, `git push --repo=x a:b`, `git push origin a:$B`, `git push origin a:b 2>&1`, `cd x && git push origin a:b`, ``git push origin a:b `echo c:main` ``, `git push origin a:b \` plus a line `c:main`, `git-push origin feature`, `/usr/lib/git-core/git-push origin main`, `git push --force origin f`, `git push origin +f:f`, `git push --all`, `--mirror`, `--receive-pack`, `--exec`, `git --attr-source HEAD push origin main`, `echo f:main \| xargs git push origin f:f` | PUSH, PUSHFORM | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH-FORM |
  | 16 | `git push origin main`, `git push origin x:main`, `git push origin x:refs/heads/master`, `git push origin x:heads/main`, `git push -u origin feature:main` (each the whole command) | PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED | BLOCK LL-PROTECTED |
  | 17 | `git merge x`, `git pull`, `git -c merge.conflictStyle=zdiff3 merge --no-commit --no-ff <sha>`, `git-merge x`, `gh pr merge 5`, `curl -X PUT https://api.github.com/repos/o/r/pulls/5/merge`, MCP `merge_pull_request` | MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE | BLOCK LL-MERGE |
  | 17a | `gh api -X POST repos/o/r/merges`, `gh api --method=POST repos/o/r/merges`, `gh api -XPOST repos/o/r/pulls/5/merge`, `gh api graphql -f query='mutation{mergePullRequest(...)}'`, `gh api graphql -f query='query{...mergeStateStatus...}'`, `gh api -X PATCH repos/o/r/git/refs/heads/main`, `gh api -X PUT repos/o/r/contents/x -f branch=main`, `gh api --method POST repos/o/r/pulls/5/comments/1/replies -f body=x`, `gh api graphql -f query='mutation{resolveReviewThread(...)}'`, `gh api repos/o/r/pulls --raw-field=x=y`, ``gh api repos/o/r/git/refs/heads/main `echo -XPATCH` `` | GHWRITE | BLOCK LL-GH-WRITE | BLOCK LL-GH-WRITE | BLOCK LL-GH-WRITE | BLOCK LL-GH-WRITE |
  | 18 | `git ci`, `git -c alias.ci=commit ci`, `X=commit git --config-env=alias.ci=X ci`, `git $(echo push) origin a:b`, `cmd=push; git $cmd`, `printf x \| xargs git`, `git notes add`, `git worktree add`, `git remote set-url origin u`, `git config alias.ci commit`, `git commit-tree t`, `git-lfs push`, `gh alias set co 'pr merge'`, `gh co 5`, `gh pr $(echo merge) 5`, `gh pr update-branch 5`, `gh repo sync` | UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN |
  | 19 | `gh pr view 5 --json mergeable,mergeStateStatus`, `gh issue view 5`, `gh pr checks 5`, `gh repo view`, `gh api repos/o/r/pulls/5`, `gh api repos/o/r/commits/<sha>/check-runs --jq .total_count` | NONE | ALLOW | ALLOW | ALLOW | ALLOW |
  | 20 | `gh issue create`, `gh issue comment 5`, `gh pr comment 5`, `gh pr edit 5`, `gh pr ready 5` | SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | BLOCK LL-SUBMIT | ALLOW |
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
  | 31 | Pinned over-match: `echo "use git for x"`, `grep -rn "git worktree" docs/`, `cd git-tools`, and a multi-line message whose later line starts a sentence with git: `git commit -m "$(cat <<'EOF'` / `feat: x` / `use git for hooks` / `EOF` / `)"` (G4, T-GIT-13) | UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN | BLOCK LL-UNKNOWN |
  | 32 | Pinned over-match: `git commit -m "explain git push"`; a multi-line message with a line `git push origin main is never run` | COMMIT, PUSH, PUSHFORM | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH | BLOCK LL-PUSH-FORM |
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
  1. Ordinary sessions are never blocked by a failure: every failure before identity is known exits 0, except where a bound id or a launch marker is seen (Change 5 B3, Change 6 P4).
  2. Default deny once governed: the script's last line prints LL-BROKEN and exits 2. Allowing takes an explicit `exit 0` on a named path.
  3. From Change 6 step P4 on (the first step reached only when a bound id was seen or no id was readable while the store holds a session), and in the prompt branch once a marker is present (Change 5 B6), an EXIT trap turns any exit code other than 0 or 2 into a printed LL-BROKEN (LL-NOBIND in the prompt branch) and exit 2. The script uses `set -u` and `set -o pipefail`, not `set -e`, and no ERR trap.
  4. The exit status of every `jq`, `sed` and `tr` call is checked; a failure prints LL-BROKEN and exits 2.
  5. Failure table (governed session unless stated):

     | Failure | Result |
     |---|---|
     | `jq` missing, ordinary session | exit 0 (Change 6 P3) |
     | `jq` missing, bound id in the input | BLOCK LL-BROKEN on every matched call; Read, Grep and Glob are never matched, so reading still works |
     | `jq` missing, launch marker in a prompt | BLOCK LL-NOBIND |
     | input not JSON | exit 0 when the store is empty or the text names only unbound ids (P2, P3); otherwise BLOCK LL-BROKEN |
     | session file empty, unreadable, `degraded`, unknown word | level `worktree` plus LL-STATE; `.ok` still counts |
     | `session_id` missing or invalid while the store holds a session | level `worktree` plus LL-STATE |
     | Skill name unreadable | class SKILL |
     | command over 65,536 bytes | class BIG |
     | `sed` or `tr` failure or other internal error | BLOCK LL-BROKEN |
     | bind failure (`mkdir`, `mv`, write) | BLOCK LL-NOBIND on the prompt |
     | hook killed at its timeout | the call goes ahead (V8); residual R2 |
     | session file deleted | the session reads as ordinary; this is also the release route; residual R3, owner decision O-16 (AC-5's fail-closed clause does not cover it) |

  6. `onFailure: "block"` is not set on either registration: it would block ordinary sessions whenever the hook breaks (V8).
- **Rationale**: X-002 (V8 does not force fail-open; a governance hook that exits 0 when it cannot judge is silent non-enforcement); X-003 (degrading to `worktree` keeps planning and approval working); INV-031 (the trap and the default-deny line must print a message, or AC-7 fails).
- **Integration point**: section 10.
- **Risk**: Low.

### Change 22: Command size cap, timeout and speed budget (from Variant 3 section 10, Variant 1 section 10, probe fixes)
- **Source**: Variant 3 section 10 (p95, 100 runs, ratio guard); Variant 1 section 10 absolute limits; Round 2 C-017 (majority Variant 3); U-009; INV-016, INV-018, INV-040.
- **Target**: Base section 10, "Budget" paragraph (replace).
- **Settles**: C-017, U-009, INV-016 (cap), INV-018, INV-040 (speed part).
- **Final rule**:
  1. Size cap: in a governed session a Bash or Monitor command longer than 65,536 bytes is class BIG (Change 9 NM1). Ordinary sessions have no cap.
  2. Timeout: 5 seconds on both registrations (Change 24). One value, stated once.
  3. Subprocesses: at most one `jq` per call that passes the prefilter; for Bash and Monitor text in governed sessions, two `sed` calls and two `tr` calls (Change 9); and `mkdir`, `mv`, `touch`, `rm` only on prompt events. No git, no network, no Python, no awk.
  4. Budget, measured by the T-SPD cases of Change 27 with 100 real subprocess runs each (helper `time.monotonic()`, as in `tests/hooks/test_block_bare_python.py`). Every test prints its measured numbers. Only the ratio line and the 1-second line are asserted; the absolute millisecond lines are printed and reported, not asserted, because they are flaky on loaded CI:
     - ordinary session, empty store: median at most 20 ms, p95 at most 50 ms;
     - ordinary session, store holding 1,000 session files and 50 pending files: the same limits;
     - ordinary median at most 1.5 times the median of `block-bare-python.sh` on the same Bash payload in the same run;
     - governed allow (`git status`) and governed block (`git commit -m x` at `F`): p95 at most 60 ms;
     - governed 65,536-byte realistic command (heredoc-like text with git words) and a 1 MB command: every run under 1 second, one fifth of the timeout.
- **Rationale**: T-SPD-3's same-run ratio catches regressions that absolute limits miss on fast CI (all three advocates); INV-002 and INV-016 require the stale-store and large-command cases; INV-018 requires one fixed timeout.
- **Departs from**: INV-018 suggested 3 s. 5 s gives slow hosts more margin before V8 lets a governed call through, and the 1 s assertion keeps the real cost far below either value.
- **Integration point**: section 10, subsection "Speed".
- **Risk**: Medium. The ratio test and the 1-second ceiling are the regression guards; the absolute limits are reported only.

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
     | LL-PUSH-FORM | a push that is not one plain git push command. | The guard can check a push only when the whole command is git push [-u] origin <branch> (or <source>:<branch>), with nothing before or after it; other forms (force, --all, another remote, variables, backticks, line continuations, chained or piped commands) can reach another remote or the main branch. | Run the push as its own command, exactly: git push origin <branch> or git push -u origin <branch>, with the branch name written out. |
     | LL-PROTECTED | a push to master or main. | No launch level may change the main branch. | Push the feature branch by name, then merge it through a reviewed pull request. |
     | LL-MERGE | a merge (git merge, git pull, gh pr merge, a call to a GitHub merge URL, or an MCP merge tool). | No launch level may merge; only a person reviews and merges. | Leave the merge to a person. To update the branch, run git fetch, then git rebase. |
     | LL-GH-WRITE | a gh api call that is not a plain read (it sets a method, a field or an input, or calls graphql or a merge endpoint). | In a launched session gh api may only read; a gh api write can merge, comment or change the main branch, and the guard cannot check where it lands. | Use a gh command for the step (for example gh pr view --json, gh pr comment, gh pr create --repo ...), at a level that allows it, or ask the person. |
     | LL-SUBMIT | /sc:pr-submit or a GitHub write (opening, editing, readying or commenting on a pull request or issue). | Publishing work needs a launch with --pipeline full --submit. | Run it yourself in your own session, or claim the issue again with --pipeline full --submit. |
     | LL-REPO | gh pr create without --repo. | Without --repo, gh can open the pull request on the parent repository of a fork. | Retry with --repo <owner>/<name> (or -R). |
     | LL-UNKNOWN | a git or gh command the guard does not recognise. | In a launched session only known git and gh commands may run, so a renamed command or an alias cannot commit, push or merge. | Use the standard command (for example git status, git diff, git add), or ask the person to run it. |
     | LL-MCP | a GitHub write through an MCP tool. | The guard cannot check where an MCP write lands, so a launched session writes to GitHub only through git and gh. | Use git or gh for this step. |
     | LL-ESCAPE | starting or messaging another agent or session (claude, ccsession, orca, SendMessage, /sc:issue, a remote subagent, a workflow, a remote trigger) or typing into a terminal (tmux, screen, xdotool). | That work would run outside this session's launch level. | Do the work here (local subagents are allowed), or ask the person to start it. |
     | LL-TURN | scheduling a turn (a cron job or a wake-up) before the plan is approved. | Its prompt text arrives later as a new turn and could look like a person replying approved. | Wait until the person approves the plan, or use a background task or a monitor instead. |
     | LL-TAMPER | touching the launch-level state, the Claude Code settings or hooks, a git configuration file, or reinstalling the hooks. | The session must not change its own limits. | Ask the person. To release this session they run, in their own terminal: rm "{store}/sessions/{sid}" "{store}/sessions/{sid}.ok" |
     | LL-SKILL | a skill call whose name the guard cannot read. | The guard cannot tell whether the skill is allowed at this level. | Report it (the hook input format may have changed); the person can release the session. |
     | LL-BIG | a command longer than 64 KB. | The guard cannot check a command that long in time. | Write the content to a file with the Write tool, then run a short command. |
     | LL-BROKEN | this action, because the launch-level guard could not run (jq missing, unreadable input or an internal error). | In a launched session the guard fails closed. | Install jq, or ask the person to release the session by deleting its files in {store}/sessions/. |
     | LL-NOBIND | this launch prompt. | The session was started by /sc:issue --claim, but the guard could not register it, so its limits could not be enforced. | Check that jq is installed and {store} is writable, then claim the issue again. |

     When `{sid}` is not a valid id (Change 6 P6), LL-TAMPER uses the LL-BROKEN wording "deleting its files in {store}/sessions/".
  3. Notes, appended after "You can:":
     - **LL-STATE**: `Note: the launch record was missing or unreadable, so the strictest level (worktree) applies.` Added to every block in a session whose level came from an invalid word or an invalid `session_id` (Change 4 item 3, Change 6 P6).
     - **LL-TEXT**: `Note: the guard reads command text line by line, including message and heredoc lines. If the command only mentions this action inside a message, write the text to a file with the Write tool and pass it with git commit -F <file> or gh ... --body-file <file>.` Added to every block whose class came from Bash or Monitor text. (At a level that blocks the commit itself, the commit stays blocked after the retry; the note only removes the false match.)
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
  2. Helpers: `bind(home, sid, word)` writes `sessions/<sid>` directly; `launch(home, sid, word)` writes `pending/<nonce>` and sends the marker prompt through the script; `approve(home, sid)` sends `approved`; `pre(tool_name, tool_input, sid, **extra)` and `prompt(text, sid, agent_id=None)` build payloads; `path_without(name)` builds a temporary `PATH` directory of symlinks to `bash` and every tool the script uses (`jq`, `sed`, `tr`, `mkdir`, `mv`, `touch`, `rm`), minus the named one (`jq`, `sed` or `tr`); `ob_h1(name)` loads a captured payload.
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
  | T-ISO-5 | `test_fail_open_shapes_ordinary` | not-JSON input, empty `tool_input`, unknown tool, no `jq`: exits 0 with an empty store, or when the text holds only an unbound `session_id` |
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
  | T-APR-10 | `test_wrapped_notification_does_not_approve` | a prompt shaped like a harness notification turn whose body is the line `approved` (hand-written shape until OB-H1 item 5 supplies the real one) writes no `.ok` |
  | T-GRID-1 | `test_policy_grid` | every oracle row at every level |
  | T-GRID-2 | `test_grid_complete` | every class of Change 19 has W, WA, F, FS entries in the oracle |
  | T-GRID-3 | `test_worktree_stops_at_plan` | at `W`: IMPL, COMMIT, PUSH, SUBMIT blocked; Write of `.dev/tasks/x/plan.md` and Skill `sc:workflow` allowed |
  | T-GRID-4 | `test_full_implements_without_submitting` | at `F`: IMPL allowed; COMMIT, PUSH, SUBMIT blocked |
  | T-GRID-5 | `test_full_submit_allows_commit_push_prsubmit` | at `FS`: commit, a canonical-form push, `sc:pr-submit`, `gh pr create --repo "$REPO"` allowed |
  | T-SKL-1 | `test_impl_name_spellings` | the six IMPL spellings of Change 14, plus `SC:IMPLEMENT`, `/sc:implement args` and `superclaude:sc-implement-protocol` |
  | T-SKL-2 | `test_submit_name_spellings` | `sc:pr-submit`, `sc:pr-submit-protocol` |
  | T-SKL-3 | `test_skill_name_keys` | name under `skill`, then under `name` |
  | T-SKL-4 | `test_skill_without_name` | LL-SKILL at W, WA, F; allowed at FS |
  | T-SKL-5 | `test_issue_skill_escape` | `sc:issue`, `sc:issue-protocol`: LL-ESCAPE |
  | T-NRM-1 | `test_quote_and_backslash_splicing` | `g""it push origin main`, `\git push origin main`, `git push origin 'feature:ma''in'`, `git push origin feature:ma\in`: blocked at every level (LL-PUSH below FS, LL-PUSH-FORM at FS); `g""it commit -m x` and `\git commit -m x`: LL-COMMIT at F |
  | T-NRM-2 | `test_redirections_removed` | at FS allowed: `git commit -m x < /dev/null`, `git commit -m x > /tmp/log 2>&1`, `git status 2>&1 \| tail -5`; at FS blocked with LL-PUSH-FORM: `git push origin a:b 2>&1 \| tail -5` (Change 11) |
  | T-NRM-3 | `test_segment_separators` | `;`, `&&`, `\|\|`, `\|`, newline, `$( )`, backtick each start a new segment |
  | T-NRM-4 | `test_json_escaped_slash_decoded` | a payload with `\/` escapes in a tamper path is blocked |
  | T-NRM-5 | `test_backslash_newline_joins` | `gh api \` plus a line `-X PATCH repos/o/r/git/refs/heads/main`: LL-GH-WRITE at every level; `git \` plus a line `commit -m x`: LL-COMMIT at F, allowed at FS; `git push origin a:b \` plus a line `c:main`: LL-PUSH-FORM at FS |
  | T-NRM-6 | `test_normalisation_worked_example` | the NM2 to NM6 commands of Change 9 run on the host give exactly the T text and segments of Change 9's worked example (heredoc, continuation, `2>&1 \| tail -5`, redirection target kept in T) |
  | T-GIT-1 | `test_framework_git_commands_allowed` | every read or local git command of `/sc:implement` and `/sc:pr-submit` listed in the Overview (not `commit`, `push` or the conflict-sync `merge`), at `F` |
  | T-GIT-2 | `test_unknown_or_missing_subcommand_blocked` | row 18 of Change 20 |
  | T-GIT-3 | `test_alias_routes_blocked` | the three alias forms of fact T2 |
  | T-GIT-4 | `test_alias_cannot_shadow_builtin` | in a temporary repo, real `git -c alias.status=commit status` makes no commit (checks the git behaviour Change 10 relies on) |
  | T-GIT-5 | `test_attr_source_value_skipped` | `git --attr-source HEAD push origin main`: blocked at every level (LL-PUSH below FS, LL-PUSH-FORM at FS); `git --attr-source HEAD status`: allowed |
  | T-GIT-6 | `test_commit_class_variants` | row 13 of Change 20: blocked at F, allowed at FS |
  | T-GIT-7 | `test_update_ref_rules` | `refs/superclaude/...` and `"$ref"` allowed; `HEAD`, `refs/heads/x`, `--stdin` are COMMIT |
  | T-GIT-8 | `test_later_git_word_rules` | `git commit -m "fix git handling"` allowed at FS; `git rebase -x "git push origin main" main` blocked at every level (LL-PUSH below FS, LL-PUSH-FORM at FS); `git bisect run git commit` LL-COMMIT at F |
  | T-GIT-9 | `test_wrappers_every_level` | `bash -c`, `sh -c`, `env`, `command`, `exec`, `sudo`, `nohup`, `timeout 30`, `xargs`, `/usr/bin/git`, `git -C /x`, `NAME=x git`, a `python -c "subprocess.run(['git','push','origin','main'])"` one-liner: same class as the bare command |
  | T-GIT-10 | `test_pull_is_merge` | `git pull`, `git pull --rebase`: LL-MERGE at every level |
  | T-GIT-11 | `test_space_in_C_path_blocked` | `git -C "/dir with space" push`: LL-UNKNOWN |
  | T-GIT-12 | `test_dashed_builtins` | `git-push origin main` and `/usr/lib/git-core/git-push origin main`: blocked at every level (LL-PUSH below FS, LL-PUSH-FORM at FS); `git-commit -m x` at F: LL-COMMIT; `git-merge x`: LL-MERGE at every level; `git-lfs push`: LL-UNKNOWN; `cat docs/git-workflow.md`: allowed |
  | T-GIT-13 | `test_multiline_message_line_scanned` | `git commit -m "$(cat <<'EOF'` / `feat: x` / `use git for hooks` / `EOF` / `)"`: LL-UNKNOWN at every level with the LL-TEXT note (documented false positive, G4); the same text passed with `git commit -F msg.txt`: allowed at FS |
  | T-PSH-1 | `test_named_push_allowed_at_submit` | `git push origin <sha>:<branch>`, `git push -u origin <branch>`: allowed at FS, LL-PUSH below |
  | T-PSH-2 | `test_unnamed_push_blocked_at_submit` | bare, `origin`, `origin HEAD`, `origin x:@`: LL-PUSH-FORM at FS |
  | T-PSH-3 | `test_push_all_mirror_blocked` | `--all`, `--mirror`: blocked at every level (LL-PUSH-FORM at FS) |
  | T-PSH-4 | `test_push_main_destinations_protected` | D1 to D5 of Change 11: LL-PROTECTED at every level; `+main`, `:main`: blocked at every level (LL-PUSH-FORM at FS) |
  | T-PSH-5 | `test_push_other_remote_or_options_blocked` | `upstream a:b`, `--repo=x`, `--receive-pack=x`, `--exec=x`: LL-PUSH-FORM at FS |
  | T-PSH-6 | `test_push_option_blocked` | `git push -o ci.skip origin a:b`: LL-PUSH-FORM at FS |
  | T-PSH-7 | `test_push_variable_blocked` | `git push origin a:$B`: LL-PUSH-FORM at FS |
  | T-PSH-8 | `test_configured_refspec_cannot_redirect` | fact T3 replayed: `git -c remote.origin.push=refs/heads/feature:refs/heads/main push origin feature`: LL-PUSH-FORM; `git config remote.origin.push x`: LL-UNKNOWN; `git push origin feature`: allowed at FS |
  | T-PSH-9 | `test_feature_slash_main_allowed` | `git push origin feature/main:feature/main` allowed at FS |
  | T-PSH-10 | `test_force_pushes_blocked` | `--force`, `-f`, `--force-with-lease`, `+a:b`: LL-PUSH-FORM at FS (O-2) |
  | T-PSH-11 | `test_push_form_accept_cases` | A1 to A13 of Change 11: allowed at FS, LL-PUSH at W, WA, F |
  | T-PSH-12 | `test_push_form_reject_cases` | R1 to R23 of Change 11: LL-PUSH-FORM at FS, LL-PUSH below; D1 to D5: LL-PROTECTED at every level |
  | T-GH-1 | `test_gh_pr_merge_every_level` | LL-MERGE |
  | T-GH-2 | `test_gh_api_merge_and_ref_writes` | `/merges` POST, GraphQL `mergePullRequest`, `enablePullRequestAutoMerge`, `git/refs/heads/main` PATCH, `contents/x` PUT with `-f branch=main`: LL-GH-WRITE at every level |
  | T-GH-3 | `test_gh_pr_create_without_repo` | LL-REPO at FS; LL-SUBMIT below |
  | T-GH-4 | `test_gh_pr_create_repo_forms` | `--repo "$REPO"`, `-R o/r`, `--repo=o/r` allowed at FS |
  | T-GH-5 | `test_gh_writes_need_submit` | row 20 of Change 20 |
  | T-GH-6 | `test_gh_pr_ready_submit_class` | blocked below FS, allowed at FS (O-3) |
  | T-GH-7 | `test_gh_reads_every_level` | row 19 of Change 20 |
  | T-GH-8 | `test_merge_url_suffix` | `curl` to `.../pulls/5/merge` and `.../merges`: LL-MERGE (H5); `gh api repos/o/r/pulls/5/merge` with no flags: LL-GH-WRITE (H2 item 2, not H5) |
  | T-GH-9 | `test_gh_unknown_group_or_action` | `gh alias set co 'pr merge'`, `gh co 5`, `gh extension install x`, `gh pr $(echo merge) 5`, ``gh pr `echo merge` 5``, `gh pr update-branch 5`, `gh repo sync`, `gh pr close 5`: LL-UNKNOWN at every level |
  | T-GH-10 | `test_gh_api_get_only` | every GHWRITE word and endpoint listed under Change 12 "Named regex cases" gives LL-GH-WRITE at every level (for example `gh api --method=POST repos/o/r/merges`, `gh api -XPOST repos/o/r/pulls`, `gh api repos/o/r/pulls --raw-field=x=y`, `gh api -f a=b repos/o/r/issues`, `gh api graphql -f query=x`, ``gh api repos/o/r/git/refs/heads/main `echo -XPATCH` ``, `gh api $M repos/o/r/pulls`); every plain word listed there leaves `gh api repos/o/r/pulls` allowed at every level |
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
  | T-TRN-1 | `test_turn_starters_blocked_before_approval` | CronCreate, CronDelete, ScheduleWakeup at `W`: LL-TURN |
  | T-TRN-2 | `test_turn_starters_allowed_later` | same calls at WA, F, FS |
  | T-TRN-3 | `test_monitor_and_background_commands_scanned` | Monitor `git push origin main` at FS: LL-PROTECTED; background `git commit -m x` at F: LL-COMMIT |
  | T-TRN-4 | `test_turn_and_input_route_table` | one table of every route by which the agent can start a turn or inject input. Blocked at `W`: Cron*, Schedule* (own prompt text), `orca terminal send`, `orca computer type-text`, `tmux send-keys`, `screen -X stuff`, `xdotool`, SendMessage. Allowed at `W` with a harmless command, because the harness wraps their turns (Change 8 item 8, O-17): Monitor, Bash with `run_in_background: true`, Agent and Task with `run_in_background: true` |
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
  | T-FC-3 | `test_internal_error_prints_broken` | `PATH` without `tr`, then without `sed`, governed Bash: exit 2, stderr has the header and `Blocked:` |
  | T-FC-4 | `test_script_ends_in_default_deny` | the script's last command prints LL-BROKEN and exits 2 |
  | T-FC-5 | `test_not_json_governed` | raw text holding a bound id but invalid JSON: LL-BROKEN |
  | T-FC-6 | `test_missing_session_id_with_store` | no `session_id` key while the store holds a session: `W` column plus LL-STATE |
  | T-FC-7 | `test_big_command` | 65,537 bytes governed (counted as bytes, including a command of multi-byte characters): LL-BIG; ordinary: exit 0 |
  | T-FC-8 | `test_multiline_fields_do_not_shift` | at `W`, a Bash command of three lines whose middle line is `remote`, and an Agent call with `isolation: "remote"` and a newline in its `description`: each decision equals that of the single-line version (P5 field order) |
  | T-MSG-1 | `test_every_message_has_header_and_three_lines` | first line header, then lines starting `Blocked:`, `Why:`, `You can:` |
  | T-MSG-2 | `test_every_message_id_reachable` | one oracle payload per id produces it |
  | T-MSG-3 | `test_no_unresolved_template_variables` | no `{level}`, `{store}` or `{sid}` in any output |
  | T-MSG-4 | `test_precedence_order` | TAMPER over MERGE; MERGE over GHWRITE; SUBMIT over REPO below FS; PUSH over PUSHFORM below FS; PROTECTED over PUSH |
  | T-MSG-5 | `test_level_rendered_in_header` | the four renderings |
  | T-MSG-6 | `test_state_and_text_notes` | LL-STATE on degraded sessions; LL-TEXT on Bash-derived blocks only |
  | T-SPD-1..5 | `test_speed_empty_store`, `test_speed_stale_store`, `test_speed_ratio_to_block_bare_python`, `test_speed_governed`, `test_speed_large_commands` | the five budget lines of Change 22, in that order; T-SPD-3 and T-SPD-5 assert, T-SPD-1, 2 and 4 print and report only |
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
  | AC-1 worktree stops at plan; blocks implement, task, commit, push, pr-submit | 8, 14, 18, 19, 20 | T-GRID-3, T-SKL-1, T-APR-5, T-APR-9 | OB-H3; limit: framework scripts that run git or gh inside (`scripts/finish-merge.sh`, `reply-resolve-thread.sh`, `retrigger-review.sh`) are not inspected (R1, O-7) |
  | AC-2 full implements, blocks submission; full --submit allows it | 10, 11, 12, 19, 20 | T-GRID-4, T-GRID-5, T-GIT-6, T-PSH-1, T-PSH-11, T-GH-4 | OB-H3; limits: the `/sc:pr-submit` conflict-sync `git merge` stays blocked at FS (O-10); a compound push command is blocked at FS (O-18); an inline `gh api` write or GraphQL call is blocked at every level (O-19) |
  | AC-3 approval by typing or `approved`; human versus agent | 5, 8, 15, 16 | T-APR-1, T-APR-2, T-APR-3, T-APR-4, T-APR-10, T-TRN-1, T-TRN-4 | OB-H1 items 4 and 5; limit: for self-started turns (background Agent, Task or Bash, Monitor) the distinction rests on the harness wrapping their prompt (Change 8 item 8, U4, O-17) |
  | AC-4 claim sessions only; Bash, Skill, Task; nested subagents | 6, 7, 14, 24 | T-ISO-1, T-ISO-4, T-ISO-7, T-ISO-8, T-ISO-9, T-REG-3 | OB-H1 items 1 and 6, OB-H2; met for nested subagents only when OB-H1 item 1 passes, otherwise O-9 |
  | AC-5 uneditable state, fail closed, tamper, rename, re-claim | 4, 5, 17, 21, 25 | T-BIND-2, T-BIND-7, T-BIND-12, T-BIND-13, T-TAM-1, T-TAM-2, T-FC-1, T-FC-2 | OB-H2; limit: a deleted session file reads as ordinary (R3, O-16) |
  | AC-6 no merge or main push at any level, including wrappers | 9, 10, 11, 12, 13 | T-PSH-3, T-PSH-4, T-PSH-11, T-PSH-12, T-GIT-9, T-GIT-12, T-NRM-1, T-NRM-5, T-GH-1, T-GH-2, T-GH-9, T-GH-10, T-MCP-1 | OB-H3; limit: owner decision O-7 |
  | AC-7 plain-words explanation for every block | 21, 23 | T-MSG-1, T-MSG-2, T-MSG-3, T-FC-3 | OB-H3 (one live message read) |
  | AC-8 tests per level, approval, isolation, nested, missing state, wrappers, edges; speed | 22, 26, 27 | T-GRID-1, T-SPD-1..5, plus every group above | OB-H3 timing |

  Section 13 also carries this sentence under the table: "AC-5's fail-closed clause covers an unreadable, empty, invalid or unknown session file, a missing or invalid `session_id` while the store holds a session, and a missing launch record at bind; it does not cover deletion of the session file, which reads as ordinary (R3, owner decision O-16)."
- **Integration point**: section 13.
- **Risk**: Low.

### Change 29: Observed checks OB-H1 to OB-H3 (merge of all variants)
- **Source**: Variant 1 section 12 "Observed"; Variant 2 OB-H1 to OB-H5; Variant 3 OB-H2 mandatory; Round 2 C-020 (unanimous merge), NE-3, NE-4; INV-005, INV-015, INV-027, INV-028, INV-036, INV-040.
- **Target**: Base section 12, "Observed" paragraph (replace).
- **Settles**: C-020 (content), INV-040 (observation part), B-6 (observation part).
- **Final rule**:
  - **OB-H1** (first; needs no claim feature). A throwaway log-only hook, registered on PreToolUse with matcher `*`, on PreToolUse with a copy of the Change 24 matcher, and on UserPromptSubmit, appends each payload to a log. It records: (1) a subagent Bash call and a nested-subagent Bash call: `session_id` against the parent's, `agent_id`, `agent_type` (U1); (2) a model Skill call: `tool_input` keys and the name form, including a plugin-installed skill if one exists (U2); (3) an Agent call: tool name and the `isolation` key (U3, U13); (4) a typed `/sc:implement x` line on UserPromptSubmit (V6 reading, O-4 contingency); (5) a Monitor call's `tool_input`, and the exact `prompt` field of the UserPromptSubmit payload, if any, of a Monitor-delivered line (the monitor prints the single line `approved`), of a background-Bash completion notice and of a background-subagent (`Agent` with `run_in_background: true`) completion notice; the result decides O-17 (U4, U11, INV-027, B-6); (6) whether a `TaskCreate` call reaches the anchored-matcher copy (U15); (7) the names of SendMessage and any team or cross-session tool, and the GitHub MCP tool names if a server is configured (U12, INV-032); (8) whether `claude` without `-p` starts from the Bash tool with no terminal (U14). Payloads are saved to `tests/hooks/fixtures/launch_level/ob_h1/` with secrets removed. Ship gate: item 1 must show the parent's `session_id` (Change 7).
  - **OB-H2** (after the claim feature ships; once per Orca account and config directory in use). Launch a real claim at `worktree` and record: the session file exists before the first tool call (U8); the exact first prompt text, including any Orca preamble and the marker's position (A-007, U7); the hook process's `HOME` and `CLAUDE_CONFIG_DIR` (A-006, INV-005); the claim script refuses to launch without `jq` and without the registration (CL-4); with a deliberately read-only `sessions/`, whether the person sees the LL-NOBIND text of a blocked launch prompt (U20). Mandatory before any real governed launch.
  - **OB-H3** (after OB-H2, on a test issue; one run per level). `W`: the session stops at the plan; in separate runs a typed `/sc:implement` and a reply `approved` each unlock implementation; commit stays blocked. `F`: implementation runs with no commit or push; record every git command `/sc:implement` runs (U10). `FS`: commit, `git push origin <sha>:<branch>`, and `/sc:pr-submit --monitor 3` opens a pull request on the fork and completes one full cycle (INV-028); record every push command and every inline `gh api` command it issues, verbatim, and whether any was blocked (O-18, O-19); a deliberately conflicting pull request shows the conflict-sync merge blocked and how `/sc:pr-submit` reacts (O-10). At every level: one attempt to push to `main` and one to merge, both blocked; record how often LL-PUSH-FORM, LL-GH-WRITE and LL-TEXT fire, and how many LL-TEXT and LL-UNKNOWN blocks came from multi-line message bodies (G4), `ccsession`/`screen`/`orca` prose (R8) or words naming `install_hooks` (R8); record whether the session carries an Orca worker preamble (U7, O-11); read one live block message for wording (AC-7); record the hook's timing from the session debug log.
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

### Change 31: Unverified register (merge of Variant 1's U1 to U13, Variant 2's N1 to N5, Variant 3's test column)
- **Source**: Variant 1 section 16 (U9 to U13); Variant 2 section 16 (N1 to N5); Variant 3 section 16 (Test column); Round 2 S-005 (unanimous merge).
- **Target**: Base section 16 (replace).
- **Settles**: S-005.
- **Final rule**: section 16 carries one table with columns Item, Question, Tolerance, Check. Rows:

  | Item | Question | Tolerance | Check |
  |---|---|---|---|
  | U1 | Subagent and nested-subagent `session_id` equal the parent's | Ship gate (Change 7); no fallback built | OB-H1 item 1, T-ISO-7, T-ISO-8 |
  | U2 | Skill payload key | Read `skill`, then `name`; neither gives SKILL | OB-H1 item 2, T-SKL-3 |
  | U3 | `Agent` also named `Task` | Both handled | OB-H1 item 3, T-ISO-9 |
  | U4 | `!cmd`, Monitor lines, background-task and background-subagent notices, cron turns via UserPromptSubmit: is the `prompt` wrapped by the harness? Observed wrapped for background-task notifications in this session; not observed for Monitor lines | Whole-prompt exact-match approval; Cron and Schedule (TURN) blocked at `W`; if a bare line can arrive, O-17 | OB-H1 item 5, T-APR-10, T-TRN-1 |
  | U5 | UserPromptSubmit for a typed command queued mid-turn | The reply `approved` always works | OB-H3 |
  | U6 | Hooks under `claude --bare` or `--settings` | Human-chosen; residual R4; the agent's launch flags are ESCAPE | T-ESC-1 |
  | U7 | Orca worker preamble on launched sessions (WC-9 versus `--submit`) | Owner decision O-11; the hook never reads the preamble | OB-H2, OB-H3 |
  | U8 | UserPromptSubmit fires before the first model call for a command-line prompt | If it does not fire, nothing binds and the session is ordinary; OB-H2 is mandatory before real use | OB-H2 |
  | U9 | `command_name` form on UserPromptExpansion | Moot while the event is not registered; contingency in Change 8 | OB-H1 item 4 |
  | U10 | Git commands `/sc:implement` runs | Static check: no `commit`, `push`, `merge`, `pull` (Overview); its `update-ref` targets are allowed | OB-H3, T-GIT-1 |
  | U11 | Monitor input fields | `command` scanned; `ws` has nothing to scan | OB-H1 item 5 |
  | U12 | GitHub MCP tool names | Keyword matcher plus read prefixes (Change 13); unmatched names are residual R10 | OB-H1 item 7 |
  | U13 | Agent `isolation` key in the hook payload | This session's tool definitions show `isolation: "remote"`; if the key is absent, ESCAPE never fires for it | OB-H1 item 3, T-ESC-3 |
  | U14 | `claude` without `-p` can start from the Bash tool with no terminal | Residual R5; terminal tools are ESCAPE | OB-H1 item 8 |
  | U15 | The harness honours `^` and `$` inside a matcher | The script re-checks names (Change 24 item 7) | OB-H1 item 6, T-REG-3 |
  | U16 | What `git push --repo`, `--receive-pack`, `--exec` do (taken from Advocate 1; the review confirmed they exist in `git push -h`) | Moot: none fits the push form, so all are PUSHFORM at every level | T-PSH-5 |
  | U17 | UserPromptSubmit inside subagents (Variant 2's N1) | Payloads with `agent_id` are ignored | T-APR-3, T-BIND-15 |
  | U18 | `/clear` gives a new `session_id` (Variant 2's N3) | Residual R4 | none |
  | U19 | Payload escapes `/` (Variant 2's N5) | Moot: `jq` decodes values | T-NRM-4 |
  | U20 | A person sees the stderr of a blocked UserPromptSubmit (Change 5 B13) | The prompt is blocked either way, so the session never runs ungoverned; only the explanation could be lost | OB-H2 |

  Variant 2's N2 and N4 are merged into U13 and U10. The git behaviour "an alias cannot shadow a built-in" is not listed: T-GIT-4 checks it on every test run.
- **Integration point**: section 16.
- **Risk**: Low.

### Change 32: Residual risks (Variant 1 numbering, Variant 2 "what it leaves open")
- **Source**: Variant 1 section 2 R1 to R8; Variant 2 section 2 cut table; Variant 3 section 2; Round 2 S-002 (unanimous merge); INV-003, INV-023, INV-030; diff-analysis closing note on shell startup files.
- **Target**: new section 17 (Change 1).
- **Settles**: S-002, INV-003, INV-023, INV-030; residual statements for A-004, A-006, A-007.
- **Final rule**: section 17 lists these plain statements, each with "why accepted":
  - **R1** A file written with Write or any other tool and then run (`bash push.sh`, a `make` target, `uv run python x.py`), and programs that start git, gh or Claude internally (the claim script, `superclaude sprint run` and similar runners, and the framework's own scripts: `/sc:pr-submit`'s `scripts/finish-merge.sh` runs `git commit`, its `scripts/reply-resolve-thread.sh` and `scripts/retrigger-review.sh` run `gh api` POSTs), are not inspected. AC-6's "including through shell wrappers around git" is therefore met only for wrappers written inline in the command (owner decision O-7). Why: scanning file content would block every plan that mentions a push.
  - **R2** A hook that times out or crashes lets the call go ahead (V8). Why: `onFailure: "block"` would also block ordinary sessions.
  - **R3** The store reached indirectly (a glob such as `~/.cl*`, a variable, a script) or deleted from another terminal turns the session ordinary: a deleted session file reads as ordinary, so AC-5's fail-closed clause does not cover deletion (owner decision O-16). Reaching the delete from inside the session needs a command that names a tamper token, which is blocked, so only an obfuscated shell command or a script can do it. Read, Grep and Glob are not matched (Change 18), so the store can be read with them while `cat` of the store is blocked. Why: the token rule catches direct names only, and deletion is also the release route.
  - **R4** Human-chosen bypasses: `claude --bare`, `--settings`, a person setting `disableAllHooks`, `--fork-session` and `/clear` (new ids), or a person launching under another `CLAUDE_CONFIG_DIR` (CL-4 refuses this only for claim launches). "A new `session_id` from `--fork-session` or `/clear` is a person's choice and makes the session ordinary." Why: they are a person's choice.
  - **R5** An interactive `claude`, `claude -c` or `claude -r` started some way other than tmux or screen, and input-injection tools not on the ESCAPE list (UNVERIFIED U14). Why: a command-position parser would be needed.
  - **R6** A malformed marker that is not at the start of the prompt (for example after an Orca preamble), with no usable record, leaves the session ordinary. OB-H2 records the real first prompt. Why: matching loose markers anywhere would govern people who quote the marker.
  - **R7** A shell alias or function defined in `~/.bashrc` or another startup file the Bash tool loads can hide `git` from the scan; whether a mid-session edit takes effect is unverified; edits to startup files are not tamper. Why: no variant protects them, and adding them over-blocks ordinary dotfile work.
  - **R8** Accepted over-blocks in governed sessions: prose that mentions git, gh, `orca` or the claude family inside a Bash command (LL-TEXT names the way around); in particular a multi-line commit message, heredoc or PR body, which is scanned line by line, so a body line that starts with `git <word>` is UNKNOWN (or PUSH or COMMIT) at every level (Change 10 G4, T-GIT-13); a commit scope such as `fix(ccsession): ...` (the word `ccsession` is ESCAPE) and the English word `screen` (ESCAPE); any Bash word containing `install_hooks` (TAMPER), which blocks `git add`, `git diff`, `grep` and `pytest` on `install_hooks.py` in a governed session; a first word naming a file or directory `git-<letters>` such as `git-tools` (Change 10 G0); in a command that also holds a `gh api` call, an unrelated short flag containing `X`, `f` or `F` (`grep -F`, `rm -f`; Change 12 H2); the tracked project `.claude/settings.json`; `orca` worker subcommands (O-11); every push that is not the canonical form, including compound commands (O-18). OB-H3 records how often each fires. Why: governed sessions only, plain message, cheap retry.
  - **R9** Local plumbing commits through variables (`git update-ref "$ref" ...`, `git reset --hard <stash commit>`) are not COMMIT, and local branch moves without a commit or merge word (`git rebase <branch>` while on `master`, `git reset --hard`, `git branch -f`, `git checkout -B`) are class NONE; "no level permits a merge" covers the named merge routes only. Why: `/sc:implement` writes refs through variables and uses these commands locally; a push still needs the canonical form and a non-`main` destination.
  - **R10** GitHub writes outside the checked routes: `curl` with a token to endpoints other than merge URLs, MCP tools whose names lack the matcher keywords (for example issue comments). Every `gh api` write is blocked (Change 12 H2). Why: no acceptance criterion names them; merge routes are covered.
  - **R11** Fork rule at `full --submit`: `gh pr create --repo <upstream>` passes (no name compared, O-12). A push in the canonical form goes to whatever `origin` points at and follows any `remote.origin.push`, `remote.origin.pushurl` or `url.<x>.pushInsteadOf` already in a config file; the agent cannot set one (`-c` and environment prefixes are outside the push form, `git config` writes are UNKNOWN, `.git/config` and `.gitconfig` are TAMPER), but one set by a person before launch applies (feature branches only for the name check; a configured `remote.origin.push` could map a no-colon refspec to `main`). Why: the hook is installed in every project, cannot know the right repository and never reads config.
  - **R12** A hostile agent (TH3) running as the same user can defeat any same-user guard. Why: out of scope (A-004).
  - **R13** A person who pastes a launch prompt at the start of their own first prompt is governed at `worktree` until they `rm` the session file. Why: the price of "a marker always governs" (X-001).
  - **R14** If U1, U8 or A-006 is false and the observed checks are skipped, the guard silently does nothing for that case; tests use a temporary `HOME` and synthetic payloads and cannot see it. Why: only OB-H1 and OB-H2 can; they are gates (Change 30).
  - **R15** Another person's session typing `approved` into the governed terminal (for example `orca terminal send` from an ordinary session) is indistinguishable from the person (V6, no origin field). Why: the governed agent itself cannot do it (Change 15).
  - **R16** Self-started turns (background Agent, Task or Bash, Monitor) are not blocked. If the harness ever delivered such a turn's text bare, a line that is exactly `approved` would approve. Why: legitimate plan steps use these tools; the harness wraps the turns it starts (Change 8 item 8, U4); OB-H1 item 5 checks it and O-17 blocks them at `W` if it fails.
- **Integration point**: section 17.
- **Risk**: Low.

### Change 33: Open decisions for the owner (all variants, residual splits added)
- **Source**: section 15 of all variants; Round 2 residual splits (INV-020).
- **Target**: Base section 15 (replace).
- **Settles**: INV-020; the residual splits on the `cwd` cross-check, `--force`, `gh pr ready`, UserPromptExpansion and the issue number.
- **Final rule**: section 15 copies the table in this plan's section "Open decisions for the owner", ids O-1 to O-19, with the default and the alternative for each. The spec states each default as the rule in force.
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
| S-002 | unanimous merge | Numbered residuals R1 to R16, each with "why accepted" | 2, 32 |
| S-003 | unanimous merge | Decision table of literal commands with class column and failure rows; the test oracle is a hand copy | 20, 26 |
| S-004 | majority merge | One flat script; policy as a literal `case` table; independent oracle in the test file; no `--classify`, no ERR trap | 3, 19 |
| S-005 | unanimous merge | One unverified register U1 to U20 with Tolerance and Check columns | 31 |
| S-006 | unanimous merge | `LL-*` ids in the header plus Blocked, Why, You can shape | 23 |
| C-001 | unanimous merge | Strict marker anywhere with a record binds by `mv`; a marker at the start (after whitespace or BOM) with no record binds `degraded`; a strict marker elsewhere with no record blocks the prompt; later markers never change the level; no age check; no `cwd` cross-check (O-1) | 5 |
| C-002 | majority merge | U1 is a ship gate; no fallback built; reserve design recorded for O-9 | 7 |
| C-003 | majority V2 | One word per file; approval is a separate empty file | 4 |
| C-004 | unanimous merge | Governed only; tokens on normalised command text and path fields, never content; `..` paths; `.claude` word ending; reinstall rule | 17 |
| C-005 | majority merge (split) | UserPromptSubmit only; whole-prompt `approved` or a first line `/sc:implement`, `/sc:task`, `/task`; `agent_id` ignored; UserPromptExpansion not registered (O-4) | 8 |
| C-006 | unanimous V2 | `touch sessions/<sid>.ok` only at `worktree` | 4, 8 |
| C-007 | unanimous merge | One normalisation pass (`sed` continuation join and quote deletion, `sed` redirection removal, `tr` sweep keeping `$` and line boundaries), option skip list including `--attr-source`, git allowlist with dashed built-ins | 9, 10 |
| C-008 | unanimous V1 | `pull` is MERGE; non-`origin` push blocked by the push form; aliases fall to the allowlist | 10, 11 |
| C-009 | unanimous merge | Canonical push form allowlist on the raw command, then a destination check for `master`, `main`, `HEAD`, `@`; no subprocess; force pushes blocked by form (O-2) | 11 |
| C-010 | unanimous merge | `gh pr merge` always MERGE; `gh api` GET-only at every level (GHWRITE otherwise); a fixed set of gh write actions is SUBMIT, other actions UNKNOWN; `gh pr create` needs an explicit `--repo`/`-R` word at submit; `gh pr ready` is SUBMIT (O-3); merge URLs for `curl` | 12 |
| C-011 | unanimous merge | Two events; anchored PreToolUse matcher with `SendMessage` and MCP keywords; timeout 5 | 24 |
| C-012 | unanimous V1 | Monitor and background Bash commands scanned like Bash; Cron and Schedule blocked only at `W`; Monitor, background Bash and background Agent/Task allowed (O-17); Workflow and RemoteTrigger always ESCAPE | 15, 16 |
| C-013 | unanimous merge | MCP: read prefixes allowed, `merge` names MERGE, other matched writes MCP at every level (O-14) | 13 |
| C-014 | majority merge | `orca` read allowlist; `ccsession*` always; `claude`/`claude-code` with launch flags; terminal tools; remote isolation; SendMessage; Skill `issue` | 14, 15 |
| C-015 | unanimous merge | Default deny last line; EXIT trap from P4 printing LL-BROKEN; checked `jq`, `sed` and `tr` status | 21 |
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
| X-007 | unanimous merge | HEAD, bare push, `--all`, `--mirror`, `+main`, `:main` blocked without reading HEAD (outside the push form, or destination `HEAD`) | 11 |
| X-008 | unanimous V1 | `git pull` is MERGE at every level | 10 |
| X-009 | unanimous V1 | Git-level hooks rejected with the corrected reason | 34 |
| X-010 | unanimous V2 | `_FRESHNESS_SCRIPTS` lives in `install_hooks.py`; no Makefile line; no `manual` marker | 3, 26 |

Unique contributions: U-001 (Change 5), U-002 (Change 19), U-003 (Changes 11, 12; repo-name check dropped per NE-1), U-004 (Changes 12, 13, 16), U-005 (Changes 4, 17), U-006 (Change 8), U-007 (Changes 12, 25), U-008 (not taken, O-1), U-009 (Changes 22, 30), U-010 (Changes 12, 20).

## Shared assumptions A-001 to A-008

| Id | Assumption | Resolved condition (what the spec states or tests) | Changes |
|---|---|---|---|
| A-001 | A subagent's and a nested subagent's `session_id` equal the parent's | The spec states it as UNVERIFIED (U1) and makes it a ship gate: OB-H1 item 1 must pass before any real `full` or `--submit` launch. T-ISO-7 and T-ISO-8 run on the captured payloads. If it fails, O-9. | 7, 29, 30 |
| A-002 | Typed commands and agent actions are distinguishable, and a subagent cannot produce an approving prompt | Approval only from UserPromptSubmit without `agent_id`, and only for a whole prompt that is exactly `approved` or starts with a typed implement command. Turns whose prompt the agent writes (Cron, Schedule: TURN at `W`) and terminal typing (ESCAPE) are blocked; turns the harness starts for background Agent, Task and Bash calls and Monitor lines are allowed, and the protection there is the harness wrapping their prompt (U4, observed for background-task notifications, UNVERIFIED for Monitor; O-17); T-APR-3, T-APR-10, T-TRN-4 | 8, 15, 16 |
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
| INV-001 | Planned change #5 (B10, B13) | T-BIND-7, T-BIND-8 | `mkdir -p sessions`; any bind failure blocks the prompt with LL-NOBIND |
| INV-002 | Planned change #6 (P2, P3), #22 | T-SPD-2 | Prefilter keeps `jq` off ordinary calls; speed measured with 1,000 stale session files |
| INV-003 | Accepted residual R4 (Change 32) | none | "A new `session_id` from `--fork-session` or `/clear` is a person's choice and makes the session ordinary." |
| INV-004 | Planned change #5 (B8a), #25 (CL-5) | T-BIND-10 | Conflict: the probe also asked for a one-line note; not taken (a UserPromptSubmit note is not shown to the person reliably) |
| INV-005 | Planned change #25 (CL-4), #29 (OB-H2 per account) | OB-H2 | Residual R4 for launches outside the claim script |
| INV-006 | Planned change #4 (item 3) | T-FC-2 | An empty file reads as `worktree` plus LL-STATE |
| INV-007 | Planned change #14 | T-SKL-1, T-SKL-2 | Name normalisation |
| INV-008 | Planned change #8 | T-APR-4 | Conflict: typed `/sc:task` approves, because Change 14 makes `sc:task` an implement skill; `/task-builder` and `/tasks` approve nothing as the probe asked |
| INV-009 | Planned change #17 | T-TAM-2, T-TAM-5 | Conflict: `..` paths are blocked instead of resolved with `realpath -m`; the word-ending `.claude` rule replaces the `hooks/launch-level-guard` token |
| INV-010 | Planned change #17 (item 2) | T-TAM-6 | `superclaude ... install` and `install_hooks` are TAMPER |
| INV-011 | Planned change #10 | T-GIT-2, T-GIT-3, T-GIT-4 | Conflict: UNKNOWN applies to the first git word in each segment only, so one-line commit messages that mention git are not blocked (multi-line bodies are, R8); no separate `alias.` or `GIT_CONFIG_` rule (subsumed) |
| INV-012 | Planned change #11 | T-PSH-8, T-PSH-12 | The push must be the canonical form, which admits no `-c`, `--config-env` or environment prefix; `remote` and `config` writes are UNKNOWN via Change 10; conflict: a refspec without `:` is accepted (the agent cannot configure a redirect; a person-set one is R11) |
| INV-013 | Planned change #12, #13 | T-GH-2, T-GH-8, T-GH-9, T-GH-10, T-MCP-1, T-MCP-2 | `gh api` is GET-only at every level, so `/merges`, GraphQL mutations, ref PATCH and contents PUT are GHWRITE in every spelling of the method and field flags; gh actions outside a fixed set are UNKNOWN; conflict: GraphQL reads are blocked too (use `gh pr view --json`; O-19); MCP writes are blocked at every level instead of parsing `branch` arguments |
| INV-014 | Planned change #5 (B6 loose form) | T-BIND-3 | Conflict: loose markers bind only at the start of the prompt, not anywhere in the first line |
| INV-015 | Planned change #5 (B6), #29 (OB-H2) | T-BIND-4 | Leading whitespace and BOM accepted, in any order; conflict: no "first 512 characters" window; residual R6 |
| INV-016 | Planned change #9 (`sed` and `tr`), #22 (cap) | T-SPD-5, T-FC-7 | 65,536-byte cap; `sed` and `tr`, never `${s//...}` |
| INV-017 | Planned change #10 (G1 skip list and allowlist), #11 (push form) | T-GIT-5 | `--attr-source` consumes a value; a push written with it is outside the push form |
| INV-018 | Planned change #22, #24 | T-REG-1, T-SPD-5 | Conflict: 5 s, not 3 s; every governed run asserted under 1 s |
| INV-019 | Planned change #4 (item 5) | T-BIND-14 | No dots in ids; invalid ids degrade to `worktree` while the store holds a session |
| INV-020 | Planned change #33 and this plan's coverage index | none | One rule per point; residual splits are O-1 to O-5 |
| INV-021 | Planned change #9 (`$` kept, continuation join), #10 (allowlist, dashed built-ins), #11 (push form on the raw command), #12 (GET-only `gh api`, gh action allowlist) | T-GIT-2, T-GIT-12, T-NRM-5, T-PSH-12, T-GH-9, T-GH-10 | Variable, missing or substituted git subcommands and gh actions are UNKNOWN; any substitution, backtick, continuation or `xargs` around a push puts it outside the push form; a `gh api` flag hidden in another segment is still seen (whole-command word search) |
| INV-022 | Planned change #9 (NM2), #11 | T-NRM-1, T-PSH-12 | Conflict: one deletion form instead of scanning two forms; a quote-spliced push is outside the push form, so its destination is never parsed |
| INV-023 | Accepted residual R1 plus owner decision O-7 | T-GAP-1 | "A script file or a program that runs git internally is not inspected; AC-6's wrapper clause is met for inline wrappers only." |
| INV-024 | Planned change #6 (P6) | T-FC-6 | Missing or invalid `session_id` with a non-empty store governs at `worktree` |
| INV-025 | Planned change #15, plus accepted residual R5 | T-ESC-1, T-ESC-5 | Conflict: no command-position rule; `claude-code`, `ccsession*` and terminal tools added instead. Sentence: "`claude -c`, `claude -r` and an interactive `claude` started other than through tmux or screen are not blocked (UNVERIFIED U14)." |
| INV-026 | Planned change #15 | T-ESC-2, T-ESC-5 | `orca` read allowlist; tmux, screen, xdotool, ydotool |
| INV-027 | Planned change #8 (item 8), #16, #29 (OB-H1 item 5), plus owner decision O-17 and residual R16 | T-APR-10, T-TRN-3, T-TRN-4 | Conflict: neither "block Monitor and background Bash at `W`" nor "ignore approval while a monitor is live" is taken. Monitor, background Bash and background Agent/Task stay allowed; the harness wraps the turns they start, so the whole-prompt exact match never sees a bare `approved` (observed for background-task notifications, UNVERIFIED for Monitor, U4); OB-H1 logs the exact prompts; O-17 blocks them at `W` if a bare line can arrive |
| INV-028 | Planned change #16 | T-TRN-2, OB-H3 | TURN blocked at `W` only |
| INV-029 | Planned change #10 (remote and config writes UNKNOWN), plus owner decision O-12 and residual R11 | T-GIT-2 | Literal `--repo` not compared with origin by default |
| INV-030 | Accepted residual R8 | T-TAM-1 | "In a governed session, commands and edits that name `.claude/settings.json` are blocked, including the tracked project file." |
| INV-031 | Planned change #21, #23 | T-FC-3, T-FC-4 | The trap and the default-deny line print LL-BROKEN |
| INV-032 | Planned change #15, #24 | T-ESC-4, T-REG-3 | `SendMessage` is ESCAPE and in the matcher |
| INV-033 | Planned change #14, #18 (item 2), plus owner decision O-8 | T-SKL-1, T-GRID-3 | "AC-1's plan stop is command-level; direct edits stay allowed." |
| INV-034 | Planned change #10 (COMMIT list), #12, #13, plus residual R9 | T-GIT-6, T-GIT-7 | `cherry-pick`, `revert`, `am`, branch `update-ref` are COMMIT |
| INV-035 | Planned change #8, #15, #16, plus owner decision O-17 and residual R16 | T-TRN-4, T-APR-10 | One test table lists every turn-starting or input route: routes that deliver the agent's own text as a prompt (Cron, Schedule, terminal typing, SendMessage) are blocked; routes whose turn the harness wraps (background Agent, Task and Bash, Monitor) are allowed and rely on the wrapping (U4) |
| INV-036 | Planned change #15, #24, #25, #29 | T-REG-3, OB-H1 item 6 | Anchors checked by OB-H1 |
| INV-037 | Planned change #5, #17, plus residual R3 and owner decision O-16 | T-BIND-3, T-BIND-7, T-TAM-5, T-TAM-6 | All four falsifiers have cases. Not closed: a deleted session file reads as ordinary (review B-7); accepted by default (O-16), because reaching the delete needs a command naming a tamper token, which is blocked, so only an obfuscated shell command or a script can do it |
| INV-038 | Planned changes #9 to #13 and #22, plus owner decision O-7 | T-NRM-1, T-NRM-5, T-GIT-5, T-GIT-12, T-PSH-8, T-PSH-11, T-PSH-12, T-GH-2, T-GH-10, T-SPD-5 | The probe's falsifiers and the review's new ones (B-1 backtick, B-2 continuation, B-3 dashed built-ins, B-4 gh flag spellings and contents API) are closed by two allowlists: the canonical push form (Change 11) and GET-only `gh api` (Change 12). Open: script wrappers (R1, O-7) |
| INV-039 | Planned change #19 (precedence), #23 | T-MSG-2, T-MSG-3, T-MSG-4 | Messages use only `{level}`, `{store}`, `{sid}` |
| INV-040 | Planned change #22, #26, #29 | T-SPD-2, T-SPD-5, T-ISO-7 | Subagent tests driven by captured OB-H1 payloads; R14 for what tests cannot see |

## Open decisions for the owner

The default is the rule written into the spec. O-1 to O-5 are the Round 2 residual splits (INV-020), decided by the criterion; O-7 is the AC-6 limit and O-16 the AC-5 limit the owner must accept explicitly; O-16 to O-19 come from the plan review (fix cycle 1).

| Id | Question | Default (rule in force) | Alternative | Why the default |
|---|---|---|---|---|
| O-1 | Cross-check the record's worktree path against `cwd` at bind? | No | Record stores the launch path; a mismatch binds `degraded` and keeps the record (Advocate 3) | The nonce is single use and a failed bind can no longer free anyone; the check adds real-path and symlink cases |
| O-2 | `--force` at `full --submit` | Blocked: no force form fits the canonical push form (Change 11) | Widen the form to admit `--force-with-lease` (Advocate 1) | `/sc:pr-submit` never force pushes; one allowlist is simpler than a force rule |
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
| O-16 | AC-5 and a deleted session file (review B-7): a bound session whose `sessions/<sid>` is gone reads as ordinary | Accept (residual R3); deletion is also the release route | When the store holds any session file and `sessions/<sid>` is missing, read the first 2 KB of the payload's `transcript_path` and, if it starts with the launch marker, govern at degraded `worktree`. Cost: one file read per call while the store is non-empty; UNVERIFIED whether the transcript exists at the first call | Reaching the delete needs a command that names a tamper token, which is blocked, so only an obfuscated shell command or a script can do it |
| O-17 | Self-started turns (review B-6): Monitor, Bash with `run_in_background: true`, Agent or Task with `run_in_background: true` | Not blocked at any level; the harness wraps their turns, and approval needs an exact whole prompt (Change 8 item 8) | If OB-H1 item 5 shows that a bare Monitor line or notice text can reach UserPromptSubmit as the whole `prompt`, block Monitor and every `run_in_background: true` call at `W` (class TURN; Change 6 P5 then also reads `tool_input.run_in_background`) | Legitimate plan steps use them (for example the `/sc:workflow` research agents); background-task notifications are observed to arrive wrapped |
| O-18 | Compound commands that contain a push, such as `cd x && git push ...` or `git push ... 2>&1 \| tail -5`, at `full --submit` | Blocked (LL-PUSH-FORM); only the canonical form runs | Widen the push form (for example a trailing ` 2>&1`), or change `/sc:pr-submit` to issue each push as its own command | OB-H3 runs `/sc:pr-submit --monitor 3` through one full cycle and records every push command it issues; if it issues compound pushes, the owner chooses between the two alternatives |
| O-19 | Inline `gh api` calls that are not plain GETs (an explicit `--method GET`, `-F` query parameters, any `graphql` call, a write) | Blocked at every level (LL-GH-WRITE) | Admit an exact `--method GET` with `-F` parameters, or move the needed calls into framework scripts | `/sc:pr-submit` makes its writes and polls inside scripts; OB-H3 records every inline `gh api` command it issues |

## Changes NOT Being Made (with rationale)

Rows marked "alternative" are design alternatives that the spec lists in section 18 (Change 34); the other rows are base content dropped in the merge.

| Diff point | Approach not taken | Rationale (debate evidence) | Kind |
|---|---|---|---|
| D2 | HMAC over the state | The key is readable by the same user (A-004); no gain against TH2 | alternative |
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
| C-009 | `git symbolic-ref` lookup of HEAD (Variants 1, 2) | Subprocess, `cwd` and `-C` gaps; replaced by named destinations (N-2), now the canonical push form (Change 11) | base dropped |
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
| INV-027, B-6 | Monitor, background Bash and background Agent/Task blocked at `W` | Stops legitimate planning steps; the harness wraps their turns; kept as the O-17 alternative | alternative |
| B-1 to B-3 | One patch per push route (a backtick flag, a push-specific continuation rule, a dashed-word rule for pushes) | Each new spelling needs a new rule; replaced by the canonical push form (Change 11) | alternative |
| B-4 | A list of gh api write spellings and merge endpoint words | Missed `--method=POST`, `-XPOST`, `--raw-field=`, combined short flags and `contents/`; replaced by GET-only `gh api` (Change 12) | alternative |
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
| 9 | Medium | Redirection removal misreads a command | Drop NM4 (pushes no longer depend on it; other classes only see extra words) |
| 10 | Medium | Allowlist blocks a needed git command | Add the subcommand to the list (one word) |
| 11 | Medium | `/sc:pr-submit` issues a compound push and is blocked at FS | LL-PUSH-FORM names the form; O-18 widens the form or changes the skill; OB-H3 measures |
| 12 | Medium | A needed inline `gh api` call or gh action is blocked | O-19; add an action pair to the SUBMIT or read set (one word each) |
| 13, 14 | Low | MCP or skill name mismatch | Adjust the keyword or name set |
| 15 | Low | Orca worker commands blocked | Owner decision O-11 |
| 16 | Medium | A self-started turn arrives bare and forges `approved` (U4) | OB-H1 item 5 detects it before real use; O-17 blocks the routes at `W` |
| 17 | Low | Over-block on `.claude` paths | Narrow the word-ending rule |
| 18 | Low | None expected | Revert to base section 9 |
| 19, 20 | Low | Table and script disagree | T-GRID fails; fix whichever is wrong |
| 21 | Low | A failure path allows | T-FC cases fail; restore default deny |
| 22 | Low | A slow host exceeds the 1-second ceiling | Absolute limits are report-only; the ratio test and the ceiling assert |
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
- Revised: fix cycle 1 of 2, against `plan-review.md` (verdict FAIL, B-1 to B-8); see the revision log below.

## Revision log (fix cycle 1)

Governing criterion: maximum effect with the fewest edge cases and unwanted blocks; one general mechanism over a list of evasion cases. Change numbering 1 to 34 is unchanged; no change was added. New ids: class PUSHFORM (replaces PUSHNAME) and class GHWRITE; messages LL-PUSH-FORM (replaces LL-PUSHNAME) and LL-GH-WRITE; owner decisions O-16 to O-19; residual R16; unverified items U17 to U20; tests T-NRM-5, T-NRM-6, T-GIT-12, T-GIT-13, T-PSH-11, T-PSH-12, T-GH-10, T-APR-10, T-FC-8; decision-table rows 11a and 17a. Regexes and the normalisation pipeline were run with bash 5.2, GNU `sed`/`tr` and git 2.47.3 in `/tmp`; nothing in the repository was run or changed.

| Finding | Status | Changes edited | What changed |
|---|---|---|---|
| B-1 backtick push to `main` | Fixed | 9, 11, 19, 20, 23, 27, 28, 32, 33; probe rows INV-021, INV-022, INV-038; coverage C-008, C-009, X-007 | Per the steering, no per-route patch: Change 11 is now a canonical-form allowlist tested on the raw command with one anchored ERE; anything else that contains a push is PUSHFORM (LL-PUSH-FORM); destination `master`/`main` is PROTECTED, `HEAD`/`@` PUSHFORM. 13 accept and 28 reject cases named (A1 to A13, R1 to R23, D1 to D5), pinned by T-PSH-11 and T-PSH-12. Compound pushes blocked at FS recorded as O-18 (OB-H3 records every push `/sc:pr-submit` issues). O-2 settled: force pushes are blocked by form |
| B-2 continuation push to `main` | Fixed | 9, 11, 20, 27 | Closed for pushes by the Change 11 form. NM2 also joins `\` plus newline (general shell semantics; it keeps `gh api \` plus a `-X PATCH` line in one segment); T-NRM-5 |
| B-3 dashed built-ins | Fixed | 10, 11, 20, 27, 32 | G0: a word whose basename matches `^git-[a-z][a-z-]*$` is the git word plus that subcommand (same treatment as `git <name>`); a dashed push is outside the push form. T-GIT-12; over-block on `git-tools`-style names in R8 |
| B-4 gh api write forms and contents API | Fixed | 12, 19, 20, 23, 27, 32, 33; probe row INV-013; coverage C-010 | Per the steering, the list of write spellings is replaced by a GET-only `gh api` allowlist at every level (class GHWRITE, LL-GH-WRITE). Departures from the steering text, with reason: the flag regex is widened from `-X.*\|-f\|-F` to `-[A-Za-z]*[XfF].*` so attached and combined short flags (`-Fbody=x`, `-iXPOST`) are caught; the word test covers the whole command, and a `$`-word or missing endpoint is GHWRITE, so a flag hidden in a backtick, `$(...)` or variable is caught (checked: ``gh api repos/... `echo -XPATCH` `` splits into two segments). H3's "anything else: SUBMIT" fallback became UNKNOWN with a fixed SUBMIT pair set, which also closes `gh pr $(echo merge) 5` (allowed at FS before), `gh pr update-branch` and `gh repo sync`. `gh pr merge` stays MERGE at every level; `gh pr create` rules unchanged. Inline GraphQL reads and `--method GET` calls are now blocked (O-19) |
| B-5 N3/N4 tool and lost boundaries | Fixed | 3, 9, 21, 22, 26, 27 | Exact commands named: one `sed -E` for NM2 and NM3 (text T), one `sed -E` plus two `tr` for NM4 to NM6, newline turned into `;` before the sweep; worked example on a heredoc pinned as T-NRM-6. Subprocess list, `path_without` and T-FC-3 include `sed` |
| B-6 background subagents | Fixed (claim corrected, routes not blocked, per the steering) | 8, 16, 20, 23, 27, 28, 29, 31, 32, 33; A-002; probe rows INV-027, INV-035; coverage C-012; Not-made table; Overview | Monitor, background Bash and background Agent/Task are no longer TURN; TURN is Cron and Schedule only. Change 8 item 8 states that these routes start self-started turns whose prompt the harness wraps, that the protection is the whole-prompt exact match, observed for background-task notifications and UNVERIFIED for Monitor (U4). OB-H1 item 5 logs the exact prompts; O-17 (default: do not block) blocks them at `W` if a bare line can arrive; R16; T-APR-10. Every "all turn-starting routes are blocked" sentence was rewritten |
| B-7 deleted session file and AC-5 | Fixed (recorded residual, owner decision) | 21, 28, 32, 33; probe row INV-037 | O-16 (default accept, with the `transcript_path` alternative and its cost), R3 extended, AC-5 limit in the acceptance map and the section 13 sentence |
| B-8 multi-line message claim | Fixed | 10, 20, 23, 27, 29, 32; probe row INV-011 | G4 and "Departs from (2)" corrected: each newline-separated segment's first git word is classified, so multi-line bodies are over-blocked; documented false positive in rows 31 and 32, R8, T-GIT-13; LL-TEXT names `git commit -F <file>` / `--body-file`; OB-H3 counts it. No heredoc parser |

Minor findings:

| Finding | Status | Where or why |
|---|---|---|
| M-1 id collisions | Applied | Bind steps B1 to B13 (Change 5 and every reference), normalisation NM1 to NM7, threats TH1 to TH3, Variant 2's N1/N3/N5 now U17 to U19; Change 1 Terms lists the id families |
| M-2 trap too late | Applied | EXIT trap installed at P4 (Changes 6, 21) |
| M-3 untagged claims | Applied | Change 8 items 6 (V5, V6) and 8 (U4); new U20 for "a person sees a blocked prompt's stderr", checked by OB-H2 |
| M-4 namespaced skill names | Applied | Change 14 keeps the text after the last `:`; T-SKL-1 and OB-H1 item 2 |
| M-5a BOM order | Applied | Change 5 B6: any order |
| M-5b strict mid-prompt marker | Skipped | Removing the block reopens X-001 ("a marker always governs") and changes B13, T-BIND-6, A-007 and C-001; a design choice for the owner, not a one-line fix |
| M-6 prose over-blocks | Applied as a note | `fix(ccsession):`, `screen`, `install_hooks` added to R8 and counted by OB-H3. The narrowing rule (command-position words) was skipped: it adds a mechanism |
| M-7 framework scripts | Applied | Named in R1; AC-1 and AC-2 limits (O-10, O-18, O-19). Classifying the script names as SUBMIT was skipped: it adds a list |
| M-8 test wording | Applied | T-ISO-5, T-GIT-1, Change 21 "input not JSON" row |
| M-9 AC-4 conditional | Applied | AC-4 row |
| M-10 release recipe in messages | Skipped | Changes three messages and CL-6 for little gain; the store path is public in the spec and the claim output |
| M-11 bytes | Applied | `LC_ALL=C` (Changes 3, 9, 11); T-FC-7 |
| M-12 residual statements | Applied | (a) `xargs` stdin now closed by the push form (R22); (b) R9; (c) R3; R4 carries the INV-003 sentence |
| M-13 field transport | Applied | P5: fixed field order with the command last, newlines removed from the other fields in `jq`, command read with `read -r -d ''`; `run_in_background` no longer read; T-FC-8 |
| M-14 absolute timing | Applied | Change 22 item 4 and risk row: absolute limits reported only; T-SPD-3 and T-SPD-5 assert |
