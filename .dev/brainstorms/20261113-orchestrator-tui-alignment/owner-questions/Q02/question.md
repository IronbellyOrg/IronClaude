# Q2: the watcher's claim level and written acceptance of permission-free sessions for its first live test

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q2 (line 529).

> Watcher claim level (`--pipeline none` or default `worktree`), and written acceptance that the FU-1 session runs with permission checks off

Original wording (ADJ Part 7, line 772): "Should the watcher's claim run at `--pipeline none` (claim only: assign, comment, no worktree, no second agent) or at the default `worktree` level (claim plus worktree `issue-<N>` plus a governed second agent)? And do you accept in writing that the first session runs with permission checks off on the FU-1 test issue?"

## Recommended answer in the spec

`--pipeline none`; yes, in writing, for the test issue only. (`merged-requirements.md:529`; ADJ line 772)

## Default if unanswered

PLAN INFERENCE: WA-01 and WA-04 do not start; FU-1 does not run; #450 edit 1 is not posted (omitted from the WA-02 set and recorded; the set still posts once, XC-02 (6)). (`merged-requirements.md:529`)

## What it gates (work items, in words)

- WA-01: encode the chosen claim level in the watcher (for `--pipeline none`, the prompt pattern, the prompt builder, the 12-element argument pin, the retry argument list, a property test and runbook strings change, in one small PR with no file shared with #539; for the default, record it as a deliberate chain with the claim command's ship gates as preconditions). (section 2, WA-01 row)
- WA-02: the five edits to issue #450 (the watcher rollout issue); edit 1 is worded per Q2. (WA-02 row)
- WA-04: FU-1, the watcher's first live test on one test issue, which records among other things the owner's written acceptance of the first session's permission mode. (WA-04 row)
- WA-07: the deferred design in which the watcher hands an approved issue to an orchestrator. (WA-07 row)
- SW-13: the deferred sub-orchestrator design (#444) as the watcher's handoff target. (SW-13 row)
- V2-01 (one clause): the #423 rewrite changes its #331 "Related" bullet if Q2 = `--pipeline none`, because there is then no second agent. (V2-01 row)
- Wave needed by: W0 (owner answers before any code). Asked after Q1, Q33 and Q26. (`merged-requirements.md:523`)

## Facts the question depends on

| Fact | Source |
|---|---|
| The watcher (#331, rollout #450) is a poller that starts a claim session for an approved issue with the fixed prompt `/sc:issue --claim <N>`; the prompt pattern allows nothing else, so no `--pipeline` is passed. | `src/superclaude/cli/issue_watch/launch.py:33` (`PROMPT_PATTERN = ^/sc:issue --claim [1-9][0-9]{0,8}$`), `:84`; ADJ E-10 (line 136) |
| Without `--pipeline`, the claim runs at its default `worktree` level: it assigns, posts two marked comments, writes `.dev/issues/<N>/`, then creates or reuses worktree `issue-<N>` and launches a second governed agent that stops at a plan a human approves. `none` stops after the comments: no worktree, no agent. | `src/superclaude/commands/issue.md:16`, `:43` |
| The watcher design says the job is claim-only and "the claim stops at `next-steps.md`" (design decision D2). The built default contradicts it (X-001, 91 percent). | `docs/designs/issue-watcher.md:44`; ADJ line 372 |
| Ship gate: no governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1, OB-H2 and OB-H3 have passed (the claim command's hook gates, #394). The same text also requires OB-H1 item 5 "before a claim at any level". Whether these gates have passed is UNVERIFIED here. | `src/superclaude/skills/sc-issue-protocol/refs/claim.md:131`; `issue.md:16` |
| On this host launched Claude sessions run with permission checks off (`--dangerously-skip-permissions --allowedTools=Grep` seen in `ps`; `CCSESSION_PERMISSIONS` unset); a non-empty `CC_CLAUDE_FLAGS` replaces the flags whatever `CCSESSION_PERMISSIONS` says. Verified on this host only. | ADJ E-11 (line 137); INV-011 (line 462); trust boundary TB-PERM (`merged-requirements.md:631`) |
| `--pipeline none` removes only the second agent. The first session still assigns the issue, posts comments and runs the accuracy check over untrusted issue text, with permission checks off (INV-012, HIGH, addressed by making the written acceptance an FU-1 precondition). | ADJ line 271 action 2 (b); ADJ line 477 |
| Issue text is untrusted input; only a validated integer issue number reaches the session prompt (design decision D3). | TB-UNTRUSTED (`merged-requirements.md:632`); `issue-watcher.md:39` |
| FU-1 also records the real argv, both permission variables, Orca run and worker lists before and after one launch, the worktree agent row, the real launch-reply id path, the Orca build, the tab-map entry and the list of writes; the test issue is closed or unlabelled afterwards so the enabled watcher cannot claim it again. One write (a ClickUp script, if its environment is set) has unknown reversibility. | WA-04 row; ADJ line 271 action 2 |
| Q2's test permission consent does not authorise any future issue (INV-012). | `merged-requirements.md:572` |
| What each answer does: `--pipeline none` means one small PR and no second agent; the default means a worktree and a governed second agent per claim. | `merged-requirements.md:562`; ADJ line 796 |
| A watcher session is Run-less, unowned and unrecorded; the watcher keeps only an Orca operation id. Who owns the agent in the watcher worktree is a separate question (Q20). | ADJ line 269; `merged-requirements.md:547` |
