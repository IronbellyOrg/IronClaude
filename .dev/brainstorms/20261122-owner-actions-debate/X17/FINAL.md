# X17 FINAL: settle Coder issue 516 (the Coordinator branch, worktree and session)

Reconciled 2026-11-22 from A-0, B-0, A-3, B-3. Everything here is a recommendation until the owner says so in chat. Only reads were done.

## 1 Unified proposal
Post ONE correction comment on IronbellyOrg/Coder issue 516 after the owner's go. Build nothing. The 2026-11-20 hold (Clay's request to wait for the design comparison) stays. 516 shrinks to three template jobs per Orca repo whose owner is on the watcher's allowed owners list: a local `Coordinator` branch (never pushed), a `Coordinator` worktree made by `orca worktree create` with an agent at `/home/coder/workspaces/worktrees/<repo>/Coordinator`, and one session `COORD-<RepoName>`.

Statements to fix, in the owner's 2026-11-18 comment: (a) "config is created with enabled: true" becomes "not a template job; the end state is kept, timing is the owner's open call in IronClaude" (not "withdrawn": the owner repeated it on 2026-11-21 in the 515 thread, and only the owner can withdraw it); (b) "duties come from the launch prompt" becomes "pending the owner's chat approval"; (c) "a repo that already has a coordinator is not touched" becomes "IronClaude is not exempt"; (d) the quoted help text "a taken name gets a numeric suffix" is marked unverified (see 10).

Comment text (an agent posts it as ironbelly with `--repo IronbellyOrg/Coder`):
> Settlement of this issue against the IronClaude code and plan, 2026-11-22. Posted on the owner's go, from the IronClaude coordinator session. No build starts; the 2026-11-20 hold stays until the owner says go in chat.
> 1. Builds: for each Orca repository whose owner is on the watcher's allowed owners list, a local Coordinator branch made from the default branch and never pushed; a worktree made by orca worktree create with an agent at exactly /home/coder/workspaces/worktrees/<repo>/Coordinator, whose origin is that repo; one session named COORD-<RepoName>. Never raw git worktree add. Safe to repeat. The check runs at boot and at the start of each watcher run, in the one existing timer entry (no second entry), before and outside the flock, joined with a semicolon so a failed check never stops the watcher.
> 2. Does not build: switching the watcher on, granting duties, labels, approvals. The template never writes the enabled setting.
> 3. The note "the watcher config is created with enabled: true" is not a template job and is not what the code does. IronClaude creates configs with enabled false and its first-run check switches a repo on only after six checks pass (on master today that happens by itself for a passing repo). The IronClaude plan adds a stop, auto_enable false, until one throwaway-repo run. The owner's end state, nothing manual, is kept; whether a passing repo switches itself on from day one or after that run is the owner's open call in IronClaude.
> 4. Pending: "duties come from the launch prompt". The owner has not yet approved in chat the contract change that lets a script-started coordinator rely on it. Until then the prompt grants nothing beyond the owner's recorded words.
> 5. Sessions need consent: starting or restarting COORD-<RepoName> needs the owner's consent recorded in chat (per repo, or one line for the allowed owners list if the owner gives it). Without it the check reports the session missing and starts nothing. With it: at most 3 starts per repo per UTC day. This check is the only restarter; the IronClaude watcher only reports a missing coordinator.
> 6. IronClaude is not exempt. It has no Coordinator branch or folder, so it takes the create path. ORCH-IronClaude (today's hand-opened session) keeps the duties until the owner retires it in chat.
> 7. After creating: wrong folder path, log and stop for that repo (the watcher refuses it); wrong branch name, log and go on (the watcher does not check the branch name).
> 8. Existing remote Coordinator branch: the note quotes Orca help saying a taken name gets a numeric suffix. The help on the IronClaude host says only "Git branch name to use instead of the prefixed default"; the suffix is unverified and the Orca version here may differ. First a three-case test on a scratch repository (no Coordinator branch, remote only, local only): create the worktree, read the folder path and branch name, post Orca's version and the result here. Until then a repo whose remote already has a Coordinator branch is reported and skipped.
> 9. Order: the answer on 515 stands and nothing here changes what 515 builds. The Orca test result and an IronClaude guard (no watcher config is made while the Coordinator folder is missing) land before any timer entry goes live on a host with no Coordinator folders.

Order versus 515: 515's answer was posted 2026-11-21 and it pointed here, so this comment goes first and waits on nothing. One later build go covers both; the Orca test and the guard come first, then 516, then the timer entry goes live.

## 2 Context
515 (cron) is answered. 516's owner note says configs are created `enabled: true`; the code creates them `enabled: false` and `first_run` flips them on after its checks. The plan ships `auto_enable` false until the throwaway run. `auto_enable` is not in master code yet, so master today already switches a passing repo on. The 516 note also says Orca suffixes a taken branch name.

## 3 Implications
Changes: one comment on 516; IronClaude edits (reword requirement R18, the handoff doc's "switch to it" line, fill the open Orca row, record the ruling); a guard follow-up issue. Stays blocked: all building (Clay's hold), any timer entry going live, any session started by script without recorded consent, the watcher switch-on (separate owner go after the throwaway run).

## 4 Benefits
No false instruction left in 516 for a Coder agent to build. One restarter, one timer entry. No stuck-off config. The throwaway-run stop stays real. The Orca question is answered by a test, not by a guess.

## 5 Risks and containment
- Owner reads items 3 to 5 as reversing 2026-11-18: the text says what is kept; the owner says go only after reading it.
- Clay reads the comment as a go: first line says the hold stays.
- Orca suffixes the branch: the dispatcher does not check the branch name, so this is untidy, not unsafe; the test decides the fallback.
- Cron live before the folder exists leaves a config off for good (verified in dispatch.py: first-run runs only when the config was just generated): guard lands first.
- Idle `COORD-IronClaude` next to `ORCH-IronClaude` uses memory (size UNVERIFIED): sessions start only with consent.

## 6 Costs (estimates, none measured)
Comment and IronClaude doc edits 0.5 h (one comment, three small edits). Orca three-case test 1 to 2 h (scratch repo, three creates, cleanup). Guard 1 to 2 h (one check, one test; an existing test may need a change, UNVERIFIED). Later 516 build 5 to 10 h (basis: 515 is estimated 3 to 5 h; 516 adds Orca calls, repeat-safety, the daily cap, tests). Restart wording in the plan 0.5 h, done at the stage that builds it.

## 7 The sentence the owner says in chat
"Go 1: post the 516 settlement comment as drafted. Go 2: run the three-case Orca test on a scratch repository. The hold stays."

## 8 What an agent does after it
Posts the comment (`gh issue comment 516 --repo IronbellyOrg/Coder`). Records the owner's words in the decision ledger. Runs the test on a local bare origin (no GitHub write); if Orca refuses that, asks for a separate go before using a throwaway GitHub repo. Posts Orca's version and the three results on 516. Files the guard follow-up in IronClaude. Prepares the IronClaude doc edits and opens them with `/sc:pr-submit --monitor 3` only when asked.

## 9 Consensus: full on the comment
A and B agree on all of section 1 except wording I settled: neither "withdrawn" nor "Orca's help says" appears. Residual owner choices (the comment is the same either way):
1. Consent for sessions. (a) Name repos in the build go (recommended now): no script starts a session unasked, one extra sentence per repo. (b) One line covering the allowed owners list: no per-repo step, but weaker than the plan's per-repo consent rule.
2. When a passing repo switches itself on: day one (matches master and the owner's 2026-11-21 line, but the 515 "safe by default" argument then needs rework) or after the throwaway run (plan default). This belongs to the IronClaude plan, not 516.
I decided the guard question: file it now, land it before the timer entry, so it no longer needs an owner choice.

## 10 Not verified
How Orca treats an existing remote `Coordinator` branch (no Orca create was run; this host's help has no suffix wording). Which Orca version the owner read. Whether Orca accepts a local bare origin. Memory cost of idle sessions. Whether the Coder startup script holds any coordinator code (A read it, I did not). Clay's 655 comment that 516 is "replaced" (read only through the 516 hold comment). Which test file the guard changes.

Verified by me: generate.py and first_run.py start configs `enabled: false`; dispatch.py skips non-true configs and checks only folder, `.git` and origin; first-run runs only for a just-generated config; origin has only the `coordinators` branch; handoff doc has the cron line and the open Orca row; this host's Orca help text; 516 and 515 text.
