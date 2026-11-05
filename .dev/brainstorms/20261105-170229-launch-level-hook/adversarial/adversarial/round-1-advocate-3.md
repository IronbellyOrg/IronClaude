---
round: 1
advocate: 3
variant: variant-3-haiku-qa.md
status: design debate, nothing implemented
---

# Round 1 Advocate 3 (QA): launch-level guard

## Position summary

Variant 3 is the test-first specification of the guard: every rule is a named case with a literal JSON payload, harmlessness is proven before governance (T-ISO-1 and T-FO pass first), and the speed budget has a relative regression net (T-SPD-3 anchors the ordinary path to `block-bare-python.sh` in the same run). I concede three state-mechanics errors the diff analysis found (fail-open posture, the always-on cwd fallback, the narrow tamper and push rules) and one repository-fact error, all checked against the sources below. My claim for the merge is the test architecture, not the decision rules: the merged design should run V1's decision table and failure posture through V3's literal-payload test plan and speed guard.

## Steelman of Variant 1

Variant 1 is the only variant that answers every "what if the state is wrong" question in the safe direction, and those are the questions that decide whether this hook is a guard or a decoration. "A marker always governs" (section 4, step 4) closes X-001: a lost, stale or stolen nonce cannot silently release a launched agent, which is the single worst failure mode available to this design. Its push check is the most defensive of the three (branch words, refspec suffixes, `--all`/`--mirror`, and `git symbolic-ref` with failure or detached HEAD treated as protected), it is the only variant gating `git pull` (a pull can create a merge commit, so AC-6 arguably demands it), the only one with a remote check (push to anything but `origin` blocked, which on this fork is not paranoia but the CLAUDE.md rule), and the only one covering MCP tool names, `RemoteTrigger`, `Workflow`, Monitor command scanning and `isolation: remote`. The layered architecture with the policy as a literal data block plus grid-completeness tests means a new level or class is a data row and a test row, and the versioned record lets a v2 sit beside a v1. That is real extension scaffolding, not gold-plating, because issue #394 names four levels and the tool surface is provably mobile (V7 lists `Agent` today; `Task` may also exist).

## Steelman of Variant 2

Variant 2 is the smallest design that is still a guard, and it is the only variant whose repository facts are all correct: it alone places `_FRESHNESS_SCRIPTS` in `install_hooks.py`, which I verified (`src/superclaude/cli/install_hooks.py` line 42 defines it; the Makefile `verify-sync` target imports it at Makefile line 309, so no Makefile list exists to edit). Its tamper engineering is the best of the three: the store name is assembled from two parts inside the script so the guard's own source and tests cannot trip its own rule, and tokens are tested in both `/` and `\/` forms. Its one-word session file is quietly brilliant for failure modes: it needs no `jq` to read, which removes a whole class of parse failures that V1 and V3 must handle. Its discipline on U1 is the correct shape: a ship gate, not a fallback, because the contingency (cwd match) misgoverns a person's own session, exactly the false positive the diff analysis proved against my variant (X-004). The explicit cut table is honest risk management: every deletion names what it leaves uncovered, and nothing is cut silently.

## Strengths claimed

1. Every rule has a named, runnable test with a literal payload. Section 12 gives the exact JSON for each case (`["Skill",{"skill":"sc:implement"}]` exit 2 MSG-PLAN, and so on), so a reviewer can count coverage against the eight acceptance criteria line by line. The pattern is proven in this repo: `tests/hooks/test_block_bare_python.py` runs the real script, JSON on stdin, `HOME` in `tmp_path` via `subprocess.run` (lines 6 to 7, 34, 38), which is precisely my fixture design.
2. Harmlessness is proven before governance. Order of work step 1 makes T-ISO-1 (unbound session, every gated payload exits 0, empty stderr) and T-FO pass before any decision logic exists, so the false-positive master case, the one that would hurt every user of the framework, is the first thing tested rather than an afterthought. This is the cheapest regression insurance in the whole exercise.
3. The relative speed guard catches what absolute budgets miss. T-SPD-3 requires the ordinary-path median to stay at or under 1.5 times the median of `block-bare-python.sh` measured in the same run, plus p95 budgets over 100 real subprocess invocations. Absolute budgets pass on a fast CI machine while regressing user laptops; a same-run ratio cannot. A speed precedent already exists in the sibling test (`test_100kb_command_blocked_under_one_second`, line 255), so the mechanism is native to this suite.
4. Binding cross-checks the record's `worktree_real_path` against the resolved payload `cwd` (section 4), so a marker replayed into a session in another directory binds nothing (T-ISO-5). Neither V1 nor V2 has this test; it is the concrete anti-cross-bind case and it also partially covers A-007, because a preamble that moves the marker still binds only in the right directory.
5. The documented over-match is pinned by a test. `echo "git commit"` in a bound worktree session is asserted BLOCK MSG-COMMIT (T-NEG group), so loosening the scan is a deliberate, test-failing act rather than silent drift. `gh pr ready` is also named never-allowed, a small real gap the others miss (marking a draft PR ready publishes it).
6. U8 is named as "the one item that can silently void the design" with OB-H2 mandatory before any governed level touches a real issue (section 16). That is the sharpest statement of the highest-severity unknown in the whole set, and it converts an assumption into a gate.

## Weaknesses identified in Variants 1 and 2

Against Variant 1:

1. Largest code surface of the three: twelve action classes, thirteen message ids, layered functions, versioned records, a degraded mode and a `--classify` argument (S-004). This repo's own hook history is the counter-evidence to "layers are free": the #357 scanner needed 300 lines of awk, three review rounds and still lists nine ceilings. Every layer is a place a bug can live and a test must reach.
2. The degraded bind creates a marker-text false positive not listed in its own residual table: any prompt starting with the marker text binds at `worktree` even with no record (section 4, step 4). The launch prompt template lives in this repository, so a human pasting it as a first line bricks an ordinary session until someone removes a state file. The trade (nonce-theft protection versus marker-text governance) is defensible but should be stated as a residual.
3. `jq` missing bricks a governed session entirely ("Block everything except Read, Grep, Glob: LL-BROKEN"). The direction is right for a guard, but reading `tool_name` without `jq` means regex over raw JSON, which is fragile against payload shape changes, and the launched agent has no in-session remedy.
4. O-5 asserts an answer to U7 ("an `orca agent launch` session has no Task or Dispatch ID, so it is an ordinary session") that the diff analysis shows is supported only if no preamble is sent, which is still UNVERIFIED. Presenting an unverified fact as settled is the exact failure my persona exists to catch.
5. No relative speed guard: medians "with a CI margin" over 30 runs (C-017) can pass on fast hardware while doubling every user's latency.

Against Variant 2:

1. X-001 is the decisive weakness: a lost, stale or consumed nonce leaves the launched session fully ungoverned with no warning ("A session never bound looks like an ordinary one", section 2). A guard whose failure mode is silent absence of enforcement is not enforcing at the moment it is most needed, and A-007 (a preamble displacing the marker) makes that path realistic.
2. Monitor is not matched at all (section 9 cut row), and the PreToolUse matcher alternation is the root cause: a Monitor tool call with `command: "git push origin main"` never reaches the hook. That is a concrete T2 wrapper escape, not a theoretical one, and V1 (scan like Bash) and V3 (block any Monitor with a command) both cover it.
3. `git pull` is allowed at every level (X-008): it appears in no gated row, yet it can create a merge commit on the branch, which is what AC-6's merge rule exists to prevent.
4. Approval hangs on one event reading: with UserPromptExpansion cut (section 2, cut row 1), the typed-implement route lives or dies with the V6 reading that typed slash text reaches UserPromptSubmit, and V2 itself flags this as a risk in section 6. Cutting one registration to save a line removes a route V5 documents as the typed-command event.
5. The speed plan is the loosest of the three (C-017): no measurement, "a few milliseconds", a 3x tolerance on the budget, no p95, no relative anchor.

## Concessions

I checked each flagged claim against the sources; here is the honest score.

- X-002 (conceded): my appeal to V8 was wrong. V8 says a crashing hook does not block; it does not stop a script from testing `command -v jq` and exiting 2. The repo precedent I relied on is real but misapplied: `block-bare-python.sh` lines 67 to 68 do fail open on missing `jq`, but that hook is advisory lint, and a governance hook failing open is silent non-enforcement. V1 and V2's fail-closed-in-governed-sessions is the right posture; my design must change.
- X-004 (conceded in full): my claim that "rule 2's false positive needs a top-level session carrying `agent_id`; top-level sessions do not (V4)" misidentified the precondition. V4 says subagent payloads carry `agent_id`; the false positive is a subagent of an unbound top-level session in the same worktree, whose calls do carry `agent_id` and whose `session_id` misses rule 1 under either answer to U1. V2 named this exact wrong case. The fallback must ship off, decided by OB-H1, as V1 has it.
- X-005 (conceded): "blocked in every session" contradicts my own "ordinary sessions are never blocked" and T-ISO-1. The tamper rule must be scoped to governed sessions, and T-ISO-1's wording must say "gated payloads" excludes the state-naming rule.
- X-006 (conceded): under my own rules an Edit of `~/.claude/settings.json` is checked only for the store path, and the escape check reads Bash command words, not Edit file paths, so the edit passes and V11's `disableAllHooks` switches my hook off. A real AC-5 hole. The fix is to adopt V1/V2's `.claude/settings` and `.claude/hooks` tokens on both Bash strings and Edit/Write paths.
- X-007 (conceded): my push check reads literal words after `push`, so `git push origin HEAD` on `master`, a bare `git push` on `master`, and `--all`/`--mirror` all pass at FS while my section 1 claims no level allows a master push. Internal contradiction violating AC-6. The fix is V1's check: add `--all`/`--mirror` and run `symbolic-ref`, treating failure or detached HEAD as protected.
- X-009 (conceded): I verified the worktree's `.git` is a file reading `gitdir: /home/coder/workspaces/IronClaude/.git/worktrees/hook-launch-level-394`, so hooks resolve to the main checkout's common directory, not inside the worktree. V1's rationale is correct and mine was wrong. The decision is unchanged (all three reject git-level hooks), and the underlying writability concern survives via A-004, but my stated reason was false.
- X-010 (conceded on all three sub-points): the Makefile has no `_FRESHNESS_SCRIPTS` list (it imports the one in `install_hooks.py` line 42, Makefile line 309); `pyproject.toml` sets `--strict-markers` (line 114) and registers no `manual` marker (lines 117 to 148), so my `@pytest.mark.manual` placeholders fail collection unless the marker is registered; and `session-init.sh` has no `state` reference (grep found none), so only `freshness-subagent-start.sh` (line 6, `STATE_DIR="$HOME/.claude/state"`) supports my state-convention claim. What survives from my variant: the dual skill-key read is verified in `sc-recommend-phase0.sh` line 31.

What survives overall: the test architecture, the literal payloads, the harmlessness-first order of work, T-SPD-3, the cwd cross-check on binding, and the pinned over-match. The decision rules must come from V1's stricter table.

## Shared assumptions

| Id | Verdict | Reason |
|---|---|---|
| A-001 | QUALIFY | Rely on `session_id` equality only behind OB-H1; since my always-on fallback is conceded broken, the merged design must hold with the fallback off until the observation settles it. |
| A-002 | QUALIFY | The event split is verified (V5, V6), but "a subagent cannot produce a prompt event" is not (V2's N1), so approval must ignore prompts carrying `agent_id` (V2's U-006 guard). |
| A-003 | ACCEPT | Real and currently unguarded by all three; the claim script should verify the hook registration exists before launching, and I accept the diff's promotion. |
| A-004 | ACCEPT | Stated by all three from the seed constraints; it is the fact that correctly kills HMAC, mode bits and root-owned directories. |
| A-005 | QUALIFY | Accept for this host, but the script must still fail closed in governed sessions when `jq` is absent (conceding X-002), not fail open as I wrote. |
| A-006 | ACCEPT | Real and unguarded; temporary-`HOME` tests cannot catch a shim that sets a different `HOME`, and I accept the promotion. |
| A-007 | QUALIFY | Accept only after OB-H2 confirms the marker's position; otherwise the starts-with rule must degrade to V2's first-match-anywhere, with my cwd cross-check as the second factor. |
| A-008 | QUALIFY | Accept cwd equality for binding (resolved paths), but not for push checks: a `git -C` inside the command can point elsewhere, so `symbolic-ref` must honour an in-command `-C` or the check must be conservative. |

## Per-point verdicts

| Point | Superior approach | Confidence | Evidence |
|---|---|---|---|
| S-001 | Merge | 60% | Frame is cosmetic; V1's front matter aids tooling, any form works. |
| S-002 | Variant 1 | 70% | Numbered R1-R8 with "why accepted" is the only traceable residual register. |
| S-003 | Merge | 75% | V2's "table is the test data" mechanism applied to V3's literal-command rows is drift-proof and directly runnable. |
| S-004 | Merge | 65% | V2's size discipline with V1's policy-as-data block; my flat dispatch is testable but V1's `--classify` separates classifier from policy tests. |
| S-005 | Merge | 80% | V1's U9-U13 and V2's N1-N5 each found real unknowns the other missed; add my per-item Test column. |
| S-006 | Variant 3 | 65% | Eight one-line ids each pinned by T-MSG-1..8 is the smallest set that stays consistent. |
| C-001 | Variant 1 | 75% | Degraded bind closes X-001, the worst failure mode; merge my cwd cross-check (U-008) into it. |
| C-002 | Merge | 85% | V1's designed-but-off posture decided by OB-H1; my always-on version is conceded broken (X-004) and V2's bare gate loses V1's prepared mechanism. |
| C-003 | Variant 2 | 75% | The one-word file needs no jq to read, removing a failure class V1 and V3 must both handle. |
| C-004 | Merge | 85% | V1's token set (settings, hooks, aliases, gitconfig) on V2's two-part-name source trick with escaped-slash tests, scoped to governed sessions. |
| C-005 | Variant 1 | 80% | Both approval routes with the first-line fallback is robust to U5; merge V2's `agent_id` ignore (U-006). |
| C-006 | Variant 2 | 75% | `touch` of a separate `.ok` only at `worktree` is atomic and never rewrites the governing file; my in-JSON rewrite can drop approval on a crash. |
| C-007 | Merge | 65% | V2's character-class normalisation with V1's fuller option-skip list; my one-level `bash -c` re-scan adds explicit nesting. |
| C-008 | Variant 1 | 80% | Only V1 gates `git pull` (X-008), non-origin remotes and `git config alias.`; on this fork the remote rule is CLAUDE.md policy. |
| C-009 | Variant 1 | 90% | Words, suffixes, `--all`/`--mirror` and `symbolic-ref` with failure treated as protected; my check is conceded broken (X-007). |
| C-010 | Variant 1 | 75% | The `/merge` suffix anywhere catches curl, and the repo check comes from the record, not a hard-coded name that breaks other users' installs. |
| C-011 | Merge | 70% | V1 and V3 equivalent (no matcher or `*`, justified by V10); V2's alternation is the root cause of its Monitor and MCP gaps. |
| C-012 | Variant 1 | 80% | Only V1 covers Cron, ScheduleWakeup, RemoteTrigger, Workflow and scans Monitor like Bash rather than my blanket block. |
| C-013 | Variant 1 | 65% | The only MCP coverage of the three; over-blocking in governed sessions is the safe direction even with unverified names (U12). |
| C-014 | Variant 1 | 75% | Subcommand-level escape rules plus `isolation: remote`; my bare-`orca` block over-blocks read-only calls and I miss remote isolation entirely. |
| C-015 | Variant 2 | 80% | Default-deny once governed is the single cleanest rule; V1's traps plus LL-BROKEN messaging is equivalent but larger; my fail-open is conceded (X-002). |
| C-016 | Merge | 70% | V1/V2's empty-store shortcut (no jq at all) on V3's `*` matcher; my no-shortcut path pays jq on every call everywhere. |
| C-017 | Variant 3 | 85% | p95 budgets, 100 runs and the same-run ratio to `block-bare-python.sh` (T-SPD-3) catch regressions absolute medians miss. |
| C-018 | Variant 1 | 75% | The header naming issue and level plus three-part text serves AC-7 best; my one-liners lack a next step in MSG-SELF and MSG-ESCAPE. |
| C-019 | Merge | 70% | V3's literal payloads generated by V2's table mechanism, plus V1's grid-completeness and message-id tests. |
| C-020 | Merge | 65% | V2's five observed checks with V3's U8-mandatory-before-use gate; V1 runs OB-H1 first to decide the fallback, which matches C-002. |
| X-001 | Variant 1 | 90% | "A marker always governs" is the only answer that keeps a lost nonce from silently ungoverning the launch. |
| X-002 | Variant 1 | 75% | Fail closed in governed sessions with a named remedy (LL-BROKEN); my V8 citation was wrong and the repo's fail-open precedent serves advisory hooks. |
| X-003 | Variant 1 | 70% | Degrade to `worktree` with a note keeps enforcement and usefulness; V2 bricks all matched calls and my version also drops approval (separate-file fix needed). |
| X-004 | Variant 2 | 90% | V2 named the exact false positive; my V4-based rebuttal misidentified the precondition and is conceded. |
| X-005 | Merge | 85% | V1's token breadth on V2's two-part assembly and escaped-slash tests, scoped to governed sessions; my every-session rule was self-contradictory. |
| X-006 | Variant 1 | 90% | Verified V11 kills my settings claim; V1 blocks the edit, the token and the git alias route. |
| X-007 | Variant 1 | 90% | Verified against my own table row allowing `git push origin HEAD` at FS; V1's check closes every variant I missed. |
| X-008 | Variant 1 | 80% | Only V1 treats `pull` as a merge class; a pull can create the merge commit AC-6 forbids. |
| X-009 | Variant 1 | 85% | I verified the `.git` file points at the main checkout's gitdir, so V1's rationale is the factually correct one; the rejection of git hooks is unchanged. |
| X-010 | Variant 2 | 95% | Verified: `install_hooks.py` line 42 holds the list (Makefile line 309 imports it), `--strict-markers` with no `manual` marker (pyproject lines 114, 117-148), and `session-init.sh` has no state reference.

## What the merge should take from Variant 3

Three things, all in the test layer where my variant is genuinely strongest: the literal-payload case set with the harmlessness-first order of work (T-ISO-1 and T-FO before any governance), the relative speed guard T-SPD-3 with p95 budgets, and the binding cwd cross-check with T-ISO-5. Everything on the decision side, the failure posture, the push check, the tamper tokens and the fallback gating, should follow Variant 1, with Variant 2's one-word state file, two-part store name and claim-side `jq` refusal merged in. That combination meets the eight acceptance criteria with the fewest untested edges, which is the goal the brief named.
