# Round 2 rebuttal: advocate D (variant 4, coordinator runs git through an Agent-tool subagent)

Persona: security (least privilege, attack surface, authorization) plus analyzer (evidence quality). Date: 2026-11-02. Fourth rebuttal, after A, B and C.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, `round2-advocate-b.md`, `round2-advocate-c.md`, the five variants, `diff-analysis.md`.

Citation keys as in Round 1. Added keys:
- `CC-PERM` = https://code.claude.com/docs/en/permissions, fetched this round. Line numbers refer to the saved fetch.
- `CC-MODES` = https://code.claude.com/docs/en/permission-modes, fetched this round, first 100k characters.
- `CC-HOOKS` = https://code.claude.com/docs/en/hooks, characters 100k-200k read this round.

"Verified" means re-read this round.

## 1. Response to criticisms

These are the criticisms of variant 4 in the four other Round 1 files and in A's, B's and C's Round 2 files. Where several advocates raised the same point, it is grouped into one row.

| # | Criticism (raised by) | Response |
|---|---|---|
| D1 | D cannot run `/sc:pr-submit`. That skill must run top-level and never hand a side effect to a subagent, so D covers local commits only and falls back to A for every outward action (A R1, B R1 weakness 6, C R1 critique 1 and weakness 7, E R1 weakness 8) | **Conceded. This was Round 1 concession 1.** Verified at `sc-pr-submit-protocol/SKILL.md:47-49,82-84`. D is a way of carrying out a commit, not an ownership model. In the merge base it executes a local commit in two places: the coordinator's shared-worktree commit row, and, optionally, a granted worker's own commit (D9). |
| D2 | The "narrow tool list" claim was unsupported: no evidence that Bash can be limited to git (X-005) (A R1, B R1, C R1, E R1) | **Conceded on V4's original mechanism, corrected in my Round 1.** A, B and C now credit the corrected mechanism (frontmatter `hooks`, CC-SUB) and moved X-005 to "V4 as amended". Section 3 adds evidence that the corrected guard works even under `bypassPermissions`. |
| D3 | D breaks provenance when provenance was requested: "Never substitute a non-Orca subagent tool when Orca orchestration provenance was requested" (`[G]` 46-47) (A R1, C R1 critique 2 and weakness 8) | **Conceded for that case, bounded otherwise.** Verified with `orca-ide skills get orchestration` in Round 1. When a user requests Orca provenance for git actions, the committer subagent must not be used. The action then goes to a per-action Task (C's shape) or stays in the coordinator's main chat. A coordinator's main-chat commit has no Orca record either, so this rule restricts D exactly as much as it restricts A's default. The spec should state the rule once, for both. |
| D4 | D adds an authorization hop (the coordinator's prompt) without adding an Orca record (B R1 weakness 6, E R1 weakness 8) | **Conceded on the hop, bounded on the harm.** The hop is inside one session's transcript, so the person sees the subagent prompt next to the reasoning that produced it. That is the same audit surface A has. The guard (section 2) limits the worst a mis-written prompt can cause to a wrong local commit of explicit paths. It cannot cause a push, a sweep, a force or a `.claude/` staging. Under E's default-off grant, nothing visible outside the machine depends on the hop. |
| D5 | D inherits A's limits: no per-task commits, quiescence must be known, contract file lists may be incomplete (B R1 weakness 6, E R1 weakness 7) | **Conceded on per-task commits; partly rebutted on the other two.** Per-task commits belong to E's worker row (D concession 7). On the file lists (A-002), the committer is the cheapest place for the `git status --porcelain` cross-check that A, B and C all now require. It reads the diff outside the coordinator's context and returns only the unlisted paths. On quiescence (A-003), no committer, D or otherwise, can see writers. P1 and M1 make quiescence a placement fact, which D adopts unchanged. |
| D6 | **A's N2:** a settings-level `PreToolUse` hook runs in the coordinator's main chat too, so a mechanical git guard is not unique to a subagent (A R2 R9 and N2; B R2 B11; C R2 C12) | **Conceded on uniqueness. Rebutted on equivalence.** My Round 1 Strength 1 said no variant could restrict a main chat "without blocking that session's other legitimate Bash use". A is right that a deny-list hook can run there, and I withdraw "only". The two forms are not equal, for two verified reasons. (1) **The main chat must keep push authority.** `/sc:pr-submit` performs "the actual `git push origin <target_sha>:<target_branch>`" itself from the main session (`SKILL.md:274`, verified) and stages with `git add -- <paths>` and commits there too. A hook sees only command text, not "this call is inside pr-submit". So a main-chat guard cannot block push, commit or add without breaking the mandatory PR path (`CLAUDE.md:50`). A's proposed "`push` outside pr-submit" rule cannot be expressed as a hook. The main-chat guard is limited to forms the repo forbids absolutely. A subagent allowlist removes push, `gh` and everything else from the committer entirely. (2) **Deny-lists on command text are not a security boundary; allowlists fail closed.** CC-PERM line 250 says a Bash rule "isn't a security boundary around the program": `Bash(git push *)` stops `git push origin main` but not `git -C . push origin main`, `git -c push.default=current push origin main` or `git 'push' origin main` (CC-PERM 252-256, verified). A deny-list hook has the same weakness unless it parses the command fully. An allowlist that accepts only one fixed grammar and rejects everything else blocks any form it does not recognise. So both forms belong in the spec, at different strengths (section 2). |
| D7 | Whether exit 2 blocks under `bypassPermissions` is UNVERIFIED, so the guard cannot be a spec dependency (A R2, B R2, C R2; my own Round 1 concession 3) | **Settled for settings-level hooks by documentation plus a live observation; frontmatter hooks remain inferred.** See section 3, N1. CC-PERM line 625: "PreToolUse hooks run before the permission prompt". Line 651: "A hook that exits with code 2 stops the tool call before permission rules are evaluated". CC-MODES says bypass "disables permission prompts and safety checks", which are steps that come after the hook. In this session, which runs with `--dangerously-skip-permissions`, a user-level `PreToolUse` hook exiting 2 blocked my Edit while I was a subagent. I still accept "optional, tested control" (section 2), because the frontmatter form has not been run. |
| D8 | Subagent hooks are ignored for plugin agents, and project-level agent hooks wait for workspace trust (A R2, citing my Round 1 concession 4) | **Conceded, with a spec rule.** The committer must not ship in `plugins/superclaude/agents/` (21 files there today, verified in Round 1). It installs only to `~/.claude/agents/` through `superclaude install`. The live test in section 2 must run against the installed copy. |
| D9 | A subagent allowlist does not apply to a worker's own commits; the relevant form for B's or E's lane is a settings-level deny-list in the worker session (B R2 B11 and section 2) | **Rebutted.** An Orca worker is a top-level Claude session and may spawn Agent-tool subagents. Orca's depth fence does not count them (`CAPS:155`, verified Round 1). WC-7 restricts only lifecycle messages and commands like pr-submit to the top-level session, not ordinary tool work (`SPEC:71`, verified Round 1). A granted E-row worker can therefore make its local commit through the same committer subagent and get the allowlist. The settings-level floor applies to it as well. |
| D10 | Taking the pr-submit loop off the coordinator is a larger context saving than D's commit offload; C-006 belongs to C's per-PR opt-in (C R2 table) | **Conceded for the opt-in case.** When the user requests D3 (b), the per-PR Task removes the largest load. In the default D3 (a) path, pr-submit stays on the coordinator in every variant, and D's commit offload is the only saving left. I record C-006 as split. |
| D11 | The authorization report returns "in the same confident register" whether right or wrong (my own Round 1 concession 2, echoed by A R1 weakness 6) | **Conceded; mitigated by the contract shape.** The committer returns machine-checkable facts: the commit SHA, `git show --stat --name-only <sha>`, and the unlisted paths. The coordinator compares the committed path list with the contract list before reporting to the person. The check is cheap and does not depend on trusting the subagent's prose. |

## 2. Updated assessment

**Decision: I accept the merge base as stated, in full.** It is E's table plus A's four conditions:
1. the worker-commit lane is off by default, with a scoped, quoted grant;
2. "sole writer" is a placement fact the coordinator records;
3. the lane stays dormant until #326 K3;
4. workers otherwise never write the user index, commit, move HEAD or touch remotes.

On top of that I accept the per-PR D3 (b) opt-in, B's P1 and C's M1, M2 and M3. Reasons for each addition:
- **P1:** verified this round. The revert domain is the whole-worktree diff `$start`..`now` (`refs/retry.md:201`). The exclusions cover only the run's own files and `.dev/` paths (`retry.md:202-208`). Step 5 restores or `rm -f`s every domain path (`retry.md:220`). From a security view this is an integrity hazard: one actor silently rewrites another actor's files. It exists whoever owns git, so placement is the right control.
- **M1:** verified this round. pr-submit binds to the PR head (`SKILL.md:268`) and makes a fix commit with `git add -- <paths>` and a push from that checkout (`SKILL.md:274`). Every pr-submit run is therefore a HEAD-moving writer and needs a sole-writer checkout. The committer subagent must never run in a worktree while a pr-submit loop runs there.
- **M2 and M3:** accepted as C states them. M3's reuse path stays UNVERIFIED, as C says.

**What D becomes in the merge: the guard, as a two-layer control, optional for this spec's phases.** The spec should state it like this.

**Layer 1: floor deny-list (settings-level `PreToolUse` hook, matcher `Bash`).**
- **Where it runs.** It is installed by `superclaude install` into user-level `~/.claude/settings.json` hooks, so it runs in every session on the machine. That covers the coordinator's main chat, every Orca worker's top-level session and every subagent ("Hooks from settings files ... also run inside subagents", CC-HOOKS, verified Round 1).
- **What it blocks.** Only forms the repo forbids absolutely, so that it can never break `/sc:pr-submit`:
  - `git add` with `-A`, `--all`, `.` or `-f`/`--force` (`CLAUDE.md:22-23`, V1 "no cross-worker sweep");
  - any path under `.claude/` other than `.claude/settings.json` in `git add` (`CLAUDE.md:22`);
  - `--no-verify` on `git commit` or `git push`, or `-n` on `git commit` (on `git push`, `-n` means dry run and is allowed) (`HWW:280`, "Never turn off a quality check");
  - `push` with `--force`, `-f`, `--force-with-lease` or a `+` refspec (pr-submit itself says "never a force push", `SKILL.md:274`);
  - `push` to the remote named `upstream` (`CLAUDE.md:47`);
  - `gh pr create` without `--repo` (`CLAUDE.md:45`).
- **Parsing.** It parses `git` global options (`-C`, `-c`) and quoted subcommands before matching, because a plain text match misses those forms (CC-PERM 256). Any command it cannot parse that contains `git` or `gh` is blocked (exit 2 with a reason).
- **What it does not do.** It does not remove push or commit authority from the main chat. pr-submit needs both.

**Layer 2: committer allowlist (the D lane).**
- **Definition.** `src/superclaude/agents/git-committer.md`, installed to `~/.claude/agents/` only, never to `plugins/superclaude/agents/` (D8).
- **Frontmatter.** `tools: Bash, Read`. `disallowedTools: Agent`, so it spawns nothing. No `isolation` (`worktree` would commit in a temporary tree, CC-SUB). No `omitClaudeMd`, because it must see the repo's staging rules. No `permissionMode` (it cannot loosen its parent anyway, CC-SUB).
- **Hook.** `hooks: PreToolUse` with `matcher: "Bash"` and an allowlist script. The script accepts a call only if it is one simple command with no `;`, `&&`, `||`, `|`, `&`, newline, `$(`, backtick or redirect. The command must be `git` with an optional `-C <path>`, where `<path>` equals the worktree named in the prompt. The subcommand must be one of:
  - `status --porcelain[=v1] [-z] [--untracked-files=all]`;
  - `diff [--cached] [--stat|--name-only] [-- <paths>]`;
  - `add -- <explicit paths>`, with no directory equal to the worktree root and no `.claude/` path except `.claude/settings.json`;
  - `commit -m <msg>` or `commit -F <file in /tmp>`, with no `-a`, `--amend`, `--no-verify` or `-n`;
  - `show --stat --name-only <sha>` and `rev-parse HEAD`.

  Everything else exits 2.
- **Who may use it.**
  - The coordinator, for E's shared-worktree commit row at a quiescent point.
  - A granted E-row worker, for its own local commit (D9).
  - Never when the user requested Orca provenance for that git action (D3).
- **What it returns.** The SHA, the committed path list and the unlisted `git status` paths (D11).

**Tests that gate the guard before any rule relies on it.**
1. **Unit tests** (pytest, run with `uv run pytest`) for both scripts. Each feeds hook JSON on stdin (`tool_input.command`) and asserts the exit code over an allow/deny table. The deny rows include the CC-PERM 256 forms, quoted subcommands, `sh -c` wrappers and compound commands.
2. **A live smoke test under the run's own permission mode.** In a scratch repo outside the checkout, start `claude` once with `--dangerously-skip-permissions` and once in default mode, both with the installed user-level committer. Ask it to spawn the committer and run `git add -A`. Pass means the transcript shows the PreToolUse block and `git status` shows nothing staged. Repeat with a main-chat `git push --force` against Layer 1.
3. **A configuration check.** `make verify-sync` style: the committer file exists in `~/.claude/agents/` and is absent from `plugins/superclaude/agents/`.

Until tests 1 and 2 pass, the spec names the guard as a recommended control. No safety argument in the spec may depend on it. Once they pass, I would ask (Round 3) that Layer 1 be on by default, since it blocks nothing any command legitimately needs.

**On A, B, C, E.**
- **A.** Its N2 corrected an overclaim in my Round 1 and I accept it. Its R10 point holds too: ambient authority over injected worker-report text is not specific to A. Layer 1 is the shared answer, and it now applies to A's main chat.
- **B.** P1 is the best new evidence of the round. It also strengthens the security case: the revert hazard is an integrity breach between actors that no git-ownership rule prevents.
- **C.** Withdrawing the long-lived session removes my main objection (a full session holding all git and GitHub authority). The per-PR Task should also run with Layer 1 active. M1 makes its checkout a sole-writer one.
- **E.** E is the base. D adds the executor for E's local-commit rows and the floor under all of E's rows.

## 3. New evidence

None of the following appears in any Round 1 file or in A's, B's or C's Round 2 file as stated here.

- **N1. A `PreToolUse` exit 2 blocks under `bypassPermissions`. Documented ordering plus a live observation; settled for settings-level hooks.**
  - **Docs on ordering.**
    - CC-PERM line 625: "When Claude Code makes a tool call, PreToolUse hooks run before the permission prompt, for every tool except `EndConversation`. The hook output can deny the tool call".
    - CC-PERM line 651: "A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed."
    - CC-PERM line 636: "A call that a `PreToolUse` hook blocked stays blocked, whichever settings file the hook comes from" (stated for the mod-approval path).
    - CC-HOOKS (100k-200k): "A hook that blocks by exiting 2 routes the same way as `"deny"`".
  - **Docs on what bypass removes.** CC-MODES: "`bypassPermissions` mode disables permission prompts and safety checks". CC-PERM line 81: it "Skips permission prompts". Neither page lists hooks among the things bypass skips. The hook step runs before the prompt step that bypass removes.
  - **What no doc says.** No sentence on these pages says "exit 2 blocks in `bypassPermissions`" in those words. I searched CC-PERM and the CC-MODES and CC-HOOKS portions I read for `bypassPermissions` and `PreToolUse` together and found none. So the docs settle the ordering, not the mode by name.
  - **Live observation (read-only, this session).**
    - This session's process is `claude --dangerously-skip-permissions ...` (`ps -o args -p $PPID`, 2026-11-02). That flag is equivalent to `bypassPermissions` (CC-MODES).
    - I run as a subagent, which inherits a `bypassPermissions` parent's mode (CC-SUB).
    - In Round 1 my first `Edit` was refused with `PreToolUse:Edit hook error: [~/.claude/hooks/freshness-pre-edit.sh]: FRESHNESS BLOCK`.
    - That script blocks by "stderr + exit 2" (`~/.claude/hooks/freshness-pre-edit.sh:3`, exit at line 138, verified).
    - It is registered as a user-level settings hook (`~/.claude/settings.json:185`, verified).
    - So a settings-level `PreToolUse` exit 2 blocked a tool call in a subagent under bypass.
  - **Limits.** The blocked tool was `Edit`, not `Bash`. The hook was settings-level, not subagent frontmatter. I changed no settings to test further, as instructed. Frontmatter hooks enter the same `PreToolUse` event (CC-SUB: hooks "scoped to the subagent"), so the same ordering should apply, but that remains UNVERIFIED until section 2's test 2 runs.
  - **Effect.** This removes the main open question that kept every advocate from relying on the guard. It is also why the spec should require test 2 under the exact mode Orca launches workers in.
- **N2. Claude Code's own docs say command-text deny rules are not a security boundary.** CC-PERM line 250: a Bash rule "covers the invocation Claude usually produces and isn't a security boundary around the program". Line 256: `Bash(git push *)` "Doesn't stop" `git -C . push origin main`, `git -c push.default=current push origin main` or `git 'push' origin main`. CC-PERM line 260 points to sandboxing for enforcement "that doesn't depend on the command text". Consequences:
  - A's proposed main-chat deny-list, and B's and C's worker-session deny-lists, must parse git's global options and quoting, and fail closed on what they cannot parse. Otherwise they are bypassable by the forms the docs list.
  - An allowlist that accepts one fixed grammar does not have this weakness. That is the concrete sense in which D's subagent-scoped allowlist is stricter than a main-chat deny-list, beyond "fewer commands".
- **N3. The main chat cannot shed push authority, because pr-submit pushes from it.** `SKILL.md:274` (verified): "the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push)", after staging "only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`)". A hook cannot tell a pr-submit push from any other push. So in the coordinator's main chat, least privilege is reachable only by blocking the forms pr-submit itself forbids (Layer 1). Removing push altogether is possible only in an actor that never runs pr-submit, that is, the committer subagent (Layer 2). This is the precise security residue of D after A's N2.
- **N4. pr-submit's own forbidden forms match Layer 1 exactly.** The same line says never `git add -A` or `git add .`, never force push, and never the upstream parent remote. These are the forms Layer 1 blocks, alongside the repo's `.claude/` ban (`CLAUDE.md:22-23`), the "never `--no-verify`" rule (`HWW:280`) and `gh pr create` without `--repo` (`CLAUDE.md:45`). So Layer 1 turns into mechanism rules the repo and the mandatory PR skill already state in prose. It adds no new policy.

## 4. Updated shared-assumption responses

Only the responses that changed are listed. A-004 is unchanged (REJECT: hooks can rewrite files; stop and report, never `--no-verify`).

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | Round 1 said an unattended coordinator leaves "only a mechanical control", with bypass behaviour UNVERIFIED. N1 now shows settings-level `PreToolUse` blocks hold under bypass, so the floor works when no one is watching. I now rank E's cap (a default-off grant limits unattended exposure to reversible local commits, `issue-326-evaluation.md:74`, verified) as the primary control and the guard as the backstop. |
| A-002 (contract file lists complete) | **REJECT** (unchanged verdict) | Added: B is right that a sole-writer worker's own `git status` is ground truth, so the worker row is the stronger answer. For shared-worktree rows, the committer subagent runs the porcelain cross-check and returns unlisted paths (D5, D11). |
| A-003 (quiescence knowable) | **QUALIFY** | Added from B's N1 and C's N1: quiescence must hold for the whole run of an implement ladder or a pr-submit loop, not only at commit time. A committer cannot check that. P1 and M1 make it a placement fact. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified): per-task commits are "allowed as an authorized option, never a default", and the owner's comment "does not by itself authorize commits in a worker". The committer prompt or worker brief must carry the scoped grant verbatim. |

## 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner and condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified the Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), rule from V1, with P1 | Yes (was V4) | Ownership is E's shared row at quiescence. D is an optional executor under it. A's N2 removed D's uniqueness claim. |
| C-002 | V5 (E) | No | Only E times commits in the ladder-safe window with a sole-writer guard; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V5) | Shown as a tie: coordinator main chat by default; one pr-submit Task per PR only on explicit request. |
| C-004 | V5 (E) | Yes (was V1) | Direct authorization for outward actions; a scoped, quoted, default-off grant for reversible local commits (`issue-326-evaluation.md:74`). |
| C-005 | V3 (C) | No | A per-action Orca Task record, carried by the per-PR opt-in. |
| C-006 | V4 (D) for commits; V3 (C) per-PR opt-in for pr-submit | Yes (qualified) | In the default D3 (a) path, D's offload is the only saving; when D3 (b) is requested, the per-PR Task removes the larger load (D10). |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; pr-submit resumes from its run-log. |
| C-008 | V5 (E), with P1 and M1 | Yes (qualified) | Shared worktree for report-only workers; own worktree for granted committers, implement ladders and pr-submit loops. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | No (qualified) | Attended top-level loop by default; parallel or overlapping PR work as one Task per PR, with M2's HALT resume. |
| C-010 | V1 (A) | No | Wording only. The guard adds tested code, so it stays optional. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 and M1 add worktrees to clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit, never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and pr-submit's run-log remain the outward record. |
| X-003 | V1 = V4 = V5, with per-PR opt-in | Yes (was V1) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; the opt-in is the only exception. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); the plan should name the PR owner. |
| X-005 | V4 (D), as amended | No (strengthened) | The frontmatter `hooks` allowlist is the restriction (CC-SUB). Blocking under bypass is now shown for settings hooks (N1). It is stricter than a deny-list (N2, N3). |
| A-001 | V5 (E), guard as backstop | Yes (was V4) | E's default-off grant is the primary unattended control; the guard works under bypass (N1) but stays optional until tested. |
| A-002 | V5 (E) | Yes (was V4) | A sole-writer worker's `git status` is ground truth; the committer's cross-check covers shared rows. |
| A-003 | V5 (E), with P1 and M1 | No (qualified) | Placement makes run-long quiescence true for ladders and pr-submit loops. |
| A-004 | V5 (E) | No | Both E commit paths keep hook rewrites away from concurrent writers; stop and report, never `--no-verify`. |
| A-005 | V5 (E) | No | Per-Task quoting of a scoped, default-off grant. |

**Tally:**
- E: 13 alone (S-001, C-001, C-002, C-004, C-007, C-008, C-011, X-001, A-001, A-002, A-003, A-004, A-005), plus 2 shared (C-003, X-003).
- C: 4 alone (S-002, S-004, C-005, X-002), plus a share of C-006.
- A: 4 alone (S-003, C-009, C-010, X-004), plus 2 shared.
- D: 1 alone (X-005), plus a share of C-006 and of X-003.
- B: 0.

Ten points changed (C-001, C-003, C-004, C-006, C-008, X-003, X-005 strengthened, A-001, A-002, plus the A-003 qualifier). All moved toward E or toward ties that keep outward actions with the coordinator.

**Overall:** D is not an ownership model and I no longer argue for it as one. Its surviving contribution to the merge is the guard, specified in two layers:
- a Layer 1 floor of the repo's absolute prohibitions, enforced in every session;
- a Layer 2 committer allowlist for E's local-commit rows.

The guard works under `bypassPermissions` for settings hooks (N1). It is stated in section 2 with its tests, and it stays optional until those tests pass under the run's own permission mode.
