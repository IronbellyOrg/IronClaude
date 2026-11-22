<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS) -->
<!-- Merge date: 2026-11-20 -->

# Merged position (OAG3): staged default-on, NG-2 covers the poll cycle only
<!-- Source: Base (original, modified) - H1 retitled per merge instruction -->

Paths: "planb" = worktree /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb (branch ironbelly/issue-watcher-zero-setup-plan, head d0a0a433b). "MR" = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md. "REQ" = planb .dev/releases/backlog/issue-watcher-zero-setup/requirements.md.
<!-- Source: Base (original) -->

## Claim
<!-- Source: Base (original, modified) - OA-28a replaced per Change #1, OA-28b replaced per Change #3 -->

OA-28a: staged default-on. The `auto_enable` defaults key ships false, so no config is switched on before the S17 throwaway run. After S17 passes, the owner turns the key on once in the defaults file (one recorded chat go). From then on a new repo that passes `first_run`'s six checks switches itself on with no per-repo go. The end state is on because the owner's recorded line (REQ R17, R18) is that nothing in setup is manual.
<!-- Source: Variant 2 (CLAY), Claim and Mechanism step 2 - merged per Change #1; zero-setup rationale from Base (original) -->

OA-28b: NG-2 ("the poll never writes to GitHub") covers the poll cycle only (`issue-watch once`). Init creates the trigger label once, and only after the owner's go that turns `auto_enable` on. Setup is not the poll.
<!-- Source: Variant 2 (CLAY), Claim OA-28b and fact 1 - merged per Change #3; NG-2 scope sentence from Base (original) -->

## Mechanism
<!-- Source: Base (original, modified) - step 4 appended per Change #4, steps 6 and 7 inserted per Changes #2 and #7, closing note per Change #8 -->

1. `run-all` lists Orca repos, filters them to allowed owners, and for a repo with no config calls `ensure_config` then `first_run` (planb `dispatch.py:411, 417`). <!-- Source: Base (original) -->
2. `ensure_config` skips the repo unless it has exactly one Project (or a mapped one), readable approvers and a maintainer list (planb `generate.py:192-250`). It writes `enabled: false`. <!-- Source: Base (original) -->
3. `first_run` runs six checks in order (config, label, init_state, dry_run, lock, restart) and writes `enabled: true` only when all pass; a failed check leaves `enabled: false` and writes a report (planb `first_run.py:1-22`). <!-- Source: Base (original) -->
4. The label create is one `gh label create` behind a read of `gh label list`, idempotent (planb `repo_init.py:93-116`). The cycle's own read form is separate: `trigger_label_state` "reads only, never creates (the cron loop, R14)" (planb `repo_init.py:93-94`), so the code already splits cycle from init. With the key false the label step only calls `trigger_label_state` and reports `would_create`; it neither creates the label nor fails the check. With the key true it calls `ensure_trigger_label`. The `would_create` result is a design proposal, not existing code (UNVERIFIED against code). <!-- Source: Base (original, modified) - appended per Change #4; Variant 2 (CLAY), Mechanism step 3 -->
5. Being enabled launches nothing by itself. A launch needs a person's per-issue approval (D01: approval is the start gate; OA-1 settled) and the ship gate `GOVERNED_LEVELS_ALLOWED = False` keeps every level above Pipeline None off (planb `launch.py:48`). <!-- Source: Base (original) -->
6. S17 passes when the six `first_run` checks are green on the throwaway repo, a `run-all --dry-run` shadow run has generated nothing and written nothing, the X-001 live check has been run, and the owner has said go in chat; this list is a proposal, not a recorded owner rule (UNVERIFIED). <!-- Source: Variant 2 (CLAY), shared assumption A-001 - merged per Change #2 -->
7. When the key is on, each repo that switches itself on is listed in the owner's session report (proposal; the mechanism for telling the owner is not built and not part of this decision). <!-- Source: Variant 2 (CLAY), shared assumption A-004 - merged per Change #7 -->

Line numbers cite the planb head d0a0a433b; after the rebase cite the symbols (`ensure_config`, `first_run`, `ensure_trigger_label`, `trigger_label_state`) and re-verify.
<!-- Source: Variant 2 (CLAY), C-004 and A-005 - merged per Change #8 -->

## Cited facts
<!-- Source: Base (original, modified) - fact 10 appended per Change #5 -->

1. R17 and R18 are the owner's decisions of 2026-11-18: "Nothing in the setup is manual" and "A generated watcher config is created with `enabled: true` ... a failed check leaves that repo `enabled: false` and reports why" (REQ R17, R18, lines 43-44). Memory `zero-setup-watcher-decisions` repeats: "Every manual step becomes automatic (... `enabled: true` ...)". <!-- Source: Base (original) -->
2. Reach is already bounded in code. `BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)` (planb `defaults.py:30`) and a repo whose origin owner is elsewhere is skipped `foreign_owner` (planb `repos.py:141`). The upstream SuperClaude-Org repo can never be generated for. <!-- Source: Base (original) -->
3. Generation is itself a filter: no Project, several Projects with no mapping, unreadable approvers or no approvers each skip the repo (planb `generate.py:218-246`). <!-- Source: Base (original) -->
4. Fail-safe is built: a failed check keeps `enabled: false` (planb `first_run.py:16-17`); a held lock and a restart are tested (planb `first_run.py:1-22`; tests `tests/issue_watch/test_first_run.py:195-215`). <!-- Source: Base (original) -->
5. The owner's own requirement R33 ("R33 before R18") is met: the closed ship gate exists in planb (planb `launch.py:48`; D01 and D03 condition; D03 verdict line 60). So the condition that D01/D03 attached to default-on is satisfied by planb itself. <!-- Source: Base (original) -->
6. NG-2 was written about the poller. Design D2 says "the poller itself never assigns, comments or moves Project items ... NG-2 test over every argv and GraphQL constant ... unchanged, it covers the poller only" (`docs/designs/issue-watcher.md:48`). The pinned argv tests scan the cycle (`tests/issue_watch/test_security_invariants.py:652, 683`), not init. <!-- Source: Base (original) -->
7. D09 verdict rule 2 already says "The per-repo init creates both labels once" and the poll "never creates a label"; Q03 verdict item 7 repeats that the poll writes nothing (`debates/D09/VERDICT.md`, `debates/Q03/VERDICT.md`). <!-- Source: Base (original) -->
8. Clay's own design is not a strict NG-2 reading: it has the poll create and change `hold:plan` under a grant (`docs/designs/orchestrator.md:410, 436-445`, snapshot master). The strict "no write anywhere in setup" is narrower than Clay's design, so it is not Clay's rule. <!-- Source: Base (original) -->
9. K24 itself records the owner's alternative as a live option: "The owner keeps R18 default-on after the throwaway run (OA-28): `auto_enable` true in the defaults file" (MR line 326), and S17 enables ONE throwaway repo only (MR line 550). <!-- Source: Base (original) -->
10. The planb test `test_only_complete_and_repo_init_may_write_to_github` already permits `complete.py` and `repo_init.py` as the only writers and keeps `github.py` and `cycle.py` read-only (`test_security_invariants.py:1059-1079`). The owner's own tests already read NG-2 as 'the cycle writes nothing'. <!-- Source: Variant 2 (CLAY) debate evidence, concession X-003 - merged per Change #5 -->

## Costs
<!-- Source: Base (original, modified) - bullet 1 replaced per Change #3, bullet 3 replaced per Change #8 -->

- The first time `run-all` meets a new in-scope repo, a label is created on GitHub without a per-repo chat go, under the class-level go given when the key is turned on. This is a one-time, reversible, idempotent write (a label can be deleted). <!-- Source: Variant 2 (CLAY), Claim OA-28b and fact 1 - merged per Change #3 -->
- Everything after the throwaway run depends on that run being a real proof; the proof is the owner's go at S17, not a property of the code. <!-- Source: Base (original) -->
- `hold:backlog` creation is not built in planb; it stays by hand (Clay design D:445) until the owner asks for it, and is outside this decision. <!-- Source: Variant 2 (CLAY), C-004 and A-005 - merged per Change #8 -->

## Risks
<!-- Source: Base (original, modified) - second bullet appended per Change #6 -->

- A repo that passes the checks but that the owner did not mean to watch is switched on. Bounded by the owner filter, the Project and approver requirements, the per-issue approval and the closed ship gate. A claim session at Pipeline None still comments and assigns on an approved issue (REQ R24; INV-025 says the guard reads command text only, MR line 28). <!-- Source: Base (original) -->
- If Coder issue 516 (coordinator per project) is not done, every repo reports `worktree_invalid` (MR line 577) and stays off; so the risk is a missing safety net, not an unsafe launch. The layered brake is not proved until S17: the X-001 live check (claim agents share one `Coordinator` worktree) has not been run, and INV-025 means the guard reads command text only. So the staged `auto_enable` key stays false until S17. <!-- Source: Base (original, modified) - appended per Change #6; Variant 2 (CLAY), facts 6-8, U-007, X-001, C-003 -->

## What it gets right
<!-- Source: Base (original) -->

- Zero setup stays true for every repo after the first, which is the whole purpose of the zero-setup plan (memory `zero-setup-watcher-decisions`).
- The owner filter, generation filters, six checks, closed gate and per-issue approval together are a layered brake; a per-repo chat go adds a human step to a path that already needs a human approval before any work starts.
- Keeping the write in init keeps the cycle's NG-2 test meaningful: every `once` argv remains a read.
