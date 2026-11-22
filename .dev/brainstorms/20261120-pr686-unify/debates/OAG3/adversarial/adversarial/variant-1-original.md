# Position OURS (OAG3): default-on after the throwaway run, NG-2 covers the poll cycle only

Paths: "planb" = worktree /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb (branch ironbelly/issue-watcher-zero-setup-plan, head d0a0a433b). "MR" = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md. "REQ" = planb .dev/releases/backlog/issue-watcher-zero-setup/requirements.md.

## Claim

OA-28a: a new repo that passes `first_run`'s six checks switches itself on. The owner's recorded line (REQ R18) is that nothing in setup is manual. A staging key may hold it off until the single throwaway run has proved the chain, but after that one owner go the default for every later repo is on, with no per-repo go.

OA-28b: NG-2 ("the poll never writes to GitHub") governs the poll cycle (`issue-watch once`). Per-repo init may create the trigger label once and `hold:backlog` once, behind the owner's chat OK before the first real run. Setup is not the poll.

## Mechanism

1. `run-all` lists Orca repos, filters them to allowed owners, and for a repo with no config calls `ensure_config` then `first_run` (planb `dispatch.py:411, 417`).
2. `ensure_config` skips the repo unless it has exactly one Project (or a mapped one), readable approvers and a maintainer list (planb `generate.py:192-250`). It writes `enabled: false`.
3. `first_run` runs six checks in order (config, label, init_state, dry_run, lock, restart) and writes `enabled: true` only when all pass; a failed check leaves `enabled: false` and writes a report (planb `first_run.py:1-22`).
4. The label create is one `gh label create` behind a read of `gh label list`, idempotent (planb `repo_init.py:93-116`). The cycle's own read form is separate: `trigger_label_state` "reads only, never creates (the cron loop, R14)" (planb `repo_init.py:93-94`), so the code already splits cycle from init.
5. Being enabled launches nothing by itself. A launch needs a person's per-issue approval (D01: approval is the start gate; OA-1 settled) and the ship gate `GOVERNED_LEVELS_ALLOWED = False` keeps every level above Pipeline None off (planb `launch.py:48`).

## Cited facts

1. R17 and R18 are the owner's decisions of 2026-11-18: "Nothing in the setup is manual" and "A generated watcher config is created with `enabled: true` ... a failed check leaves that repo `enabled: false` and reports why" (REQ R17, R18, lines 43-44). Memory `zero-setup-watcher-decisions` repeats: "Every manual step becomes automatic (... `enabled: true` ...)".
2. Reach is already bounded in code. `BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)` (planb `defaults.py:30`) and a repo whose origin owner is elsewhere is skipped `foreign_owner` (planb `repos.py:141`). The upstream SuperClaude-Org repo can never be generated for.
3. Generation is itself a filter: no Project, several Projects with no mapping, unreadable approvers or no approvers each skip the repo (planb `generate.py:218-246`).
4. Fail-safe is built: a failed check keeps `enabled: false` (planb `first_run.py:16-17`); a held lock and a restart are tested (planb `first_run.py:1-22`; tests `tests/issue_watch/test_first_run.py:195-215`).
5. The owner's own requirement R33 ("R33 before R18") is met: the closed ship gate exists in planb (planb `launch.py:48`; D01 and D03 condition; D03 verdict line 60). So the condition that D01/D03 attached to default-on is satisfied by planb itself.
6. NG-2 was written about the poller. Design D2 says "the poller itself never assigns, comments or moves Project items ... NG-2 test over every argv and GraphQL constant ... unchanged, it covers the poller only" (`docs/designs/issue-watcher.md:48`). The pinned argv tests scan the cycle (`tests/issue_watch/test_security_invariants.py:652, 683`), not init.
7. D09 verdict rule 2 already says "The per-repo init creates both labels once" and the poll "never creates a label"; Q03 verdict item 7 repeats that the poll writes nothing (`debates/D09/VERDICT.md`, `debates/Q03/VERDICT.md`).
8. Clay's own design is not a strict NG-2 reading: it has the poll create and change `hold:plan` under a grant (`docs/designs/orchestrator.md:410, 436-445`, snapshot master). The strict "no write anywhere in setup" is narrower than Clay's design, so it is not Clay's rule.
9. K24 itself records the owner's alternative as a live option: "The owner keeps R18 default-on after the throwaway run (OA-28): `auto_enable` true in the defaults file" (MR line 326), and S17 enables ONE throwaway repo only (MR line 550).

## Costs

- The first time `run-all` meets a new in-scope repo, a label is created on GitHub without a fresh chat go. This is a one-time, reversible, idempotent write (a label can be deleted).
- Everything after the throwaway run depends on that run being a real proof; the proof is the owner's go at S17, not a property of the code.
- `hold:backlog` creation is not built in planb: `ensure_trigger_label` creates only the trigger label (planb `first_run.py:193`). D09 rule 2 and K18 expect both, so a small addition is needed.

## Risks

- A repo that passes the checks but that the owner did not mean to watch is switched on. Bounded by the owner filter, the Project and approver requirements, the per-issue approval and the closed ship gate. A claim session at Pipeline None still comments and assigns on an approved issue (REQ R24; INV-025 says the guard reads command text only, MR line 28).
- If Coder issue 516 (coordinator per project) is not done, every repo reports `worktree_invalid` (MR line 577) and stays off; so the risk is a missing safety net, not an unsafe launch.

## What it gets right

- Zero setup stays true for every repo after the first, which is the whole purpose of the zero-setup plan (memory `zero-setup-watcher-decisions`).
- The owner filter, generation filters, six checks, closed gate and per-issue approval together are a layered brake; a per-repo chat go adds a human step to a path that already needs a human approval before any work starts.
- Keeping the write in init keeps the cycle's NG-2 test meaningful: every `once` argv remains a read.
