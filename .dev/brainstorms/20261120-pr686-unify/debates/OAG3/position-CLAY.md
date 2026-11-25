# Position CLAY (OAG3): `auto_enable` false, a recorded go per repo; no GitHub write anywhere in setup

Paths: "planb" = /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb (head d0a0a433b). "MR" = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md. "D:nnn" = `docs/designs/orchestrator.md` in /home/coder/.cache/ic-snap-20261120/master (Clay's merged design, PR 681).

## Claim

OA-28a: `auto_enable` stays false. A new repo gets its config and its checks, but is switched on only when the owner names it in chat, once per repo (merged design K24; recommended answer of OA-28, MR line 662).

OA-28b: NG-2 is read strictly: no GitHub write anywhere in setup. Labels are created by hand and init only checks that they exist.

## Mechanism

1. `run-all` is not read-only. For a listed repo with no config it generates one, creates the trigger label on GitHub and rewrites the config to `enabled: true` once its checks pass (planb `dispatch.py:411, 417`; `first_run.py:193`; `repo_init.py:108`). That is an unattended cron process doing a GitHub write and a switch-on with no human step (MR line 169).
2. With `auto_enable` false the dispatcher still generates the config and runs the checks, but does not rewrite `enabled: true` (MR line 326). The owner turns a repo on by naming it in chat; an agent records the go (MR line 91, K21).
3. For labels, the owner or the repo's setup step runs `gh label create` by hand; `first_run` calls only `trigger_label_state`, which reads (planb `repo_init.py:93-106`).

## Cited facts

1. The one-throwaway-repo rule: only ONE throwaway repo is enabled, on a go (S17; MR lines 326, 550). A default-on key contradicts "no config is switched on before S17" unless the key is false (MR line 416).
2. `run-all` plus default-on means that landing planb and scheduling cron "would, with no per-repo go, write a label to GitHub and switch every new repo on" (K24 consequence column, MR line 326).
3. NG-2 as written is flat: "NG-2 no GitHub write (REST GET only ...)" (`docs/designs/issue-watcher.md:76`). The pinned tests encode that sentence (`tests/issue_watch/test_security_invariants.py:652, 683`).
4. Clay's design creates `hold:backlog` once per repo by hand "so the poll needs no right to create it" (D:445), and treats switch-on as an owner-run list (O3, D:1025, D:1046) with each repo named by the owner before anything is created (D:1125).
5. The shadow run exists to be the proof before switch-on: `run-all --dry-run` reports `would_generate` and writes nothing (planb `dispatch.py:406-410`; MC-12, MR line 431). A per-repo go keeps that order for every repo, not only the first.
6. The ship gate is only a constant: "the 'brake' is one config default (`cycle.py:228`)" and the real held-back levels depend on `GOVERNED_LEVELS_ALLOWED = False` (D14 verdict line 58; planb `launch.py:48`). INV-025 (HIGH) says the guard reads command text only (MR line 28). A claim session on a switched-on repo can still comment and assign.
7. The claim route is unproved: claim agents share the one `Coordinator` worktree and the live check X-001 has not been run (MR lines 311, 550; D07 item 8). OA-23 depends on it.
8. Coder issue 516 (coordinator per project) is not landed; until then planb returns `worktree_invalid` for every repo (MR line 577). Auto-enable is untestable against its real dependencies today.
9. The key is cheap: one defaults key (MR line 353) and two tests, `test_first_run_keeps_config_off_while_auto_enable_false` and `test_dry_run_generates_nothing` (MR line 503).

## Costs

- A manual chat go per repo breaks R17/R18 "nothing manual" for the second and later repos, and adds an owner step each time a new Orca repo appears.
- Hand-creating two labels per repo is a manual step the owner did not ask for.
- A strict NG-2 reading is narrower than Clay's own design (the poll writes `hold:plan` in D:436-445), so it is a position of caution, not of design consistency.

## Risks

- Zero-setup is not zero: a repo stays dark until someone remembers to name it.
- Strictness may push the label creation back into the code under another name later.

## What it gets right

- Every switch-on and every GitHub write stays an owner-named action, in line with the owner's own rule that approvals are given in chat (memory `approvals-through-chat-never-files`; MR line 91).
- It keeps "the poll writes nothing" literally true everywhere an unattended process runs, so the NG-2 test never needs an exception.
- It stages risk: the first repo proves the chain, and every later repo is a decision.
