# Verdict OAG3: What planb's first run may switch on and write (OA-28)

## Question

OAG3 What planb's first run may switch on and write: OA-28 (auto_enable default, and whether init may create labels)

- OA-28a Should a new repo that passes `first_run`'s checks switch itself on? OURS (the owner's recorded line, planb R18): default-on after the throwaway run, so zero setup stays true for every later repo. CLAY or alternative (the merged design's default, K24): `auto_enable` false; a new repo gets a config and its checks but stays off until the owner names it in chat (one recorded go per repo).
- OA-28b Does NG-2 ("the poll never writes to GitHub") cover only the poll cycle, so init may create the trigger and `hold:backlog` labels once per repo? OURS: yes, NG-2 covers the poll cycle only; init creates the two labels once (D09 rule 2, as planb already does), still behind the owner's chat OK before the first real run. CLAY or alternative: NG-2 means no GitHub write anywhere in setup; labels are created by hand and init only checks that they exist (Clay's design D:410, D:436-495 allows a poll label write, so the strict reading is the narrower end).

## Winner

HYBRID: OA-28a is a staged default-on (the owner's end state, reached through Clay's key that ships false until the throwaway run passes), and OA-28b goes to OURS (NG-2 covers the poll cycle only).

## Winning recommendation

Terms. "The poll" is the unattended cron job (`issue-watch run-all`) that looks for newly assigned issues. "Planb" is the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`, head d0a0a433b) that adds `run-all`, `first_run` and `repo_init`. `first_run` is planb's per-repo setup check: six checks, then it writes `enabled: true`. S17 is the merged design's stage "live tests, then enable one throwaway repo". The spec must say, one line per sub-question:

1. **OA-28a (does a repo that passes `first_run` switch itself on): staged default-on.**
   - Answer: the defaults key `auto_enable` ships **false**. No config is switched on before the S17 throwaway run. After S17 passes, the owner turns the key on once in `~/.config/superclaude/issue-watch-defaults.json` (one recorded chat go). From then on a repo that passes the six checks switches itself on with no per-repo go.
   - Reason: the owner's recorded rule is "nothing in the setup is manual" and a config created `enabled: true` with a failed check leaving it off (R17, R18, planb requirements lines 43-44); the end state is on. The key ships false because planb has no key today (`_enable` runs unconditionally on a pass) and the merged design says no config is switched on before S17 and `run-all` is not scheduled before it (MR lines 326, 416). Both advocates landed on this at 60 percent (point C-001).
   - Source: debate transcript C-001, C-007 (V1, 68 percent), A-001; MR K24 (line 326), MR line 416; planb `first_run.py` (`_enable`, `done()`); REQ R17, R18.
   - Default the spec can be written to: `auto_enable: false` in code and in the shipped defaults file. Test: `test_first_run_keeps_config_off_while_auto_enable_false`; `test_dry_run_generates_nothing` (MR line 503).
2. **OA-28a, the S17 pass list (proposal, not an owner rule; UNVERIFIED).** S17 counts as the proof when the six `first_run` checks are green on the throwaway repo, a 24-hour `run-all --dry-run` shadow run generated nothing and wrote nothing, the X-001 live check (claim agents share one `Coordinator` worktree) was run, and the owner said go in chat. Reason: both advocates said "passed" is undefined (A-001). Source: transcript A-001, MR line 550.
3. **OA-28b (does NG-2 cover only the poll cycle): yes.** NG-2 means the poll cycle `issue-watch once` makes no GitHub write. `repo_init.py` is the one setup module allowed to write, and only a `gh label create`. Reason: the design says the NG-2 test "covers the poller only" (`docs/designs/issue-watcher.md:48`); the code already splits the cycle's read (`trigger_label_state`, "reads only, never creates") from the init write (`ensure_trigger_label`, "Only the first run calls this") (planb `repo_init.py:93-117`); and the owner's own planb test already allows exactly `complete.py` and `repo_init.py` as the only writers and keeps `github.py` and `cycle.py` read-only (`tests/issue_watch/test_security_invariants.py:1059-1079`, read by this debate's orchestrator). Clay's advocate conceded the point (82 percent for OURS, point C-002). Source: transcript C-002, X-003, X-004.
4. **OA-28b, the owner's go for the label write (resolves OURS's own contradiction X-002).** The label write needs the owner's chat OK. That OK is the same recorded go that turns `auto_enable` on (a class-level go for the trigger label of later repos). Before that go, with the key false, `first_run`'s label step only reads (`trigger_label_state`) and reports `would_create` without failing the check; with the key true it calls `ensure_trigger_label`. The `would_create` result is a design proposal, not existing code (UNVERIFIED against code). Reason: OURS's paper said both "behind the owner's chat OK" and "without a fresh chat go"; both advocates agreed on V2's reading (85 percent, point X-002) and on the read-only label step (62 percent, C-006). Source: transcript X-002, C-006; MR lines 91, 361.
5. **OA-28b, `hold:backlog`.** Creating `hold:backlog` is not part of this decision. Planb creates only the trigger label (`first_run.py:193`). It stays by hand (Clay design D:445) until the owner asks for init to create it. Reason: C-004 is unresolved and leans V2 or HYBRID at 55 percent; nothing in the debate shows a reader of the label yet (also Q03). Source: transcript C-004; D09 rule 2.

## Strongest points

OURS:
1. NG-2 scoped to the poll cycle is already how the owner's code and tests work: `repo_init.py:93-117` separates read from write, and `test_security_invariants.py:1059-1079` permits only `complete.py` and `repo_init.py` as writers. Clay's advocate conceded (C-002, 82 percent).
2. Reach is bounded and failure keeps it off: `BUILTIN_ALLOWED_OWNERS = ("IronbellyOrg",)` (`defaults.py:30`), `foreign_owner` skip (`repos.py:141`), generation filters (`generate.py:192-250`), a failed check leaves `enabled: false` (`first_run.py:16-17`), and a launch still needs a person's per-issue approval plus the closed ship gate (`launch.py:48`).
3. The owner's recorded line is nothing manual: R17 and R18 (planb requirements lines 43-44) and memory `zero-setup-watcher-decisions`; a permanent per-repo go breaks that after repo 1 (C-007, 68 percent; Clay's own Risks section says setup becomes "not zero").

CLAY:
1. A default-on key contradicts "no config is switched on before S17": planb's `first_run` has no key and `run-all` reaches `first_run` unattended (`dispatch.py:411, 417`; `first_run.py:152-153`); K24 says without a key landing planb and scheduling cron would write a label and switch every new repo on (MR lines 326, 416).
2. The brake is thinner than "layered" says: the gate is one constant (D14 verdict line 58; `launch.py:48`), INV-025 means the guard reads command text only (MR line 28), the X-001 claim-route check has not been run (MR lines 311, 550), and Coder 516 is not landed (MR line 577). Both advocates accepted this as residual risk.
3. The label write needs the owner's chat OK (MR lines 91, 361), and OURS's paper contradicted itself on that (X-002, 85 percent for V2); the key costs one defaults key and two tests (MR lines 353, 503).

## Clay strengths to adopt

- **The `auto_enable` key shipping false until S17.** Why: it is the only way to make "after the throwaway run" true in code, and the merged design already requires no switch-on before S17. Merge: add the key to planb's defaults (default false); after S17 the owner flips it once; no per-repo go afterwards (override of Clay's per-repo go).
- **Label step read-only while the key is false.** Why: it keeps the poll process from writing to GitHub before the owner's go. Merge: report `would_create` without failing the check (design proposal), so the throwaway run can still prove the other five checks.
- **Pass criteria for S17 and the X-001 check as a precondition.** Why: neither paper defined "passed" (A-001) and the claim route is unproved. Merge: the list in recommendation 2, marked as a proposal for the owner to confirm.
- **An owner-visible report of self-enabled repos (proposal).** Why: both advocates said cheap reversal depends on the owner seeing which repos switched on (A-004). Merge: a line per self-enabled repo in the owner's session report; the mechanism is not built and not part of this decision.
- **Cite symbols, not line numbers, after the planb rebase (A-005).** Why: MR line 501 expects conflicts. Merge: spec cites `ensure_config`, `first_run`, `ensure_trigger_label`, `trigger_label_state`.

## Our strengths that must be kept

- NG-2 stays "the poll cycle writes nothing", with the argv test that keeps `github.py` and `cycle.py` read-only; the single allowed setup write is `gh label create` in `repo_init.py`.
- The end state is zero setup: after the one flip, a repo that passes the checks switches itself on with no per-repo go (R17, R18).
- The layered limits: allowed owners, generation filters, six checks with fail-safe `enabled: false`, per-issue approval as the start gate, the closed ship gate.
- The label create stays idempotent (read first, create only if absent) and lives only in init.

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Add defaults key `auto_enable` (default false) to planb; `first_run` rewrites `enabled: true` only when it is on | LOCAL CHANGE | planb branch `ironbelly/issue-watcher-zero-setup-plan`: `defaults.py`, `first_run.py` | Part of "commit planb as a draft" (D14); before the S17 stage |
| While the key is false, make the label step read-only and non-failing (`would_create`) | LOCAL CHANGE | planb `first_run.py`, `repo_init.py` | With the previous action |
| Add tests `test_first_run_keeps_config_off_while_auto_enable_false` and `test_dry_run_generates_nothing`; keep `test_only_complete_and_repo_init_may_write_to_github` unchanged | LOCAL CHANGE | planb `tests/issue_watch/` | With the previous actions |
| Write recommendations 1 to 5 into the unified spec, state NG-2 scope, mark the S17 pass list and the report line as proposals | DOC | unified design spec; `docs/designs/issue-watcher.md` NG-2 wording (scope sentence only, no new write allowed) | After the planb changes are decided; before the spec is final |
| Confirm the class-level go: "turning `auto_enable` on also covers creating the trigger label for later repos" | DECISION | owner, in chat; the recording agent writes it | At the S17 flip, after S17 passes |
| Run S17 and record the pass list | DECISION | owner go, recorded by an agent (K21) | After Coder 515 and 516 land and the X-001 check |
| Keep `hold:backlog` creation out of OA-28; ask the owner only if init should create it | DECISION | owner | Later, optional |
| Rebase planb onto post-revert master and re-verify cited symbols | LOCAL CHANGE | planb | After the revert (D14 order) |

## Implications

- **OA-28a, watcher and cron:** `run-all` is still not scheduled before S17 and nothing switches on before the owner's flip. After the flip every in-scope repo (allowed owner, one Project, readable approvers, a `Coordinator` worktree) that passes the checks self-enables. A repo that fails stays off with a report.
- **OA-28a, claim pipeline:** enabling launches nothing by itself; each issue still needs a person's approval. A claim session at Pipeline None can still comment and assign (INV-025), so the claim route stays unproved until the X-001 check.
- **OA-28a, what breaks:** planb's `first_run` today enables unconditionally (`first_run.py:152-153`) and creates the label at step 2 (`first_run.py:193`) before the dry-run, lock and restart checks, so a repo that later fails already has its label. The key and the read-only label step change that; the owner should know the label can exist for a repo that stays off.
- **OA-28b, coordinator and dashboard:** no change to what the coordinator or the observer reads. The report line for self-enabled repos is a proposal and not built.
- **OA-28b, label step:** a read-only label step means a new repo's label check does not fail the setup but also does not create the label until the key is on; the label by hand remains valid at any time.
- **Owner must know:** the OURS paper contradicted itself on the owner's go (X-002) and this verdict fixes it by tying the label go to the key flip; Clay's design is not a strict reading either (the poll writes `hold:plan` in D:436-445), so the strict reading would have been narrower than Clay's own rule.

## Confidence

78 percent. The OA-28b answer (NG-2 covers the poll cycle) is about 88 percent, because the owner's own test and the code split support it and Clay's advocate conceded. The OA-28a staging is about 70 percent, because it rests on the debate's HYBRID at 60 percent and on the owner accepting that the S17 flip is a single class-level go. It would change if: the owner says each repo must be named in chat even after S17 (then OA-28a goes to CLAY), the S17 run or the X-001 check shows the claim route unsafe, or a source shows the owner's R18 meant "on from day one".

## Unverified

- The S17 pass list in recommendation 2 is a proposal from the two advocates; no owner source states pass criteria.
- The `would_create` result of the label step is a design proposal; no code returns it.
- The owner-visible report of self-enabled repos has no mechanism; not built.
- Whether the owner accepts the S17 flip as a class-level go for later repos' label creation (MR lines 91, 361 say each label creation needs the owner's chat OK; they do not say it can be class-level).
- That every later repo has the same shape as the throwaway repo (shared assumption A-002, qualified by both advocates).
- Planb line numbers (`d0a0a433b`) will move after the rebase (MR line 501).
- The specificity ratio in the base scoring is an estimate by sampling, not an exhaustive count (it changes the margin by under 0.005).
- Both position-bias scoring passes were run by one orchestrator, not by independent agents. At depth quick there was one debate round only: convergence 68.4 percent (13 of 19 points) against the 80 percent threshold, so the run is NOT_CONVERGED and its status is partial. Six points stayed unresolved (S-003, C-003, C-004, C-005, X-001, A-003).
- The `/sc:adversarial` skill ran in full at depth quick with two advocate agents and a merge-executor agent; Round 2, Round 2.5 and Round 3 were skipped by the depth.

## Debate artifacts

- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/position-OURS.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/position-CLAY.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/return-contract.yaml (worker contract)
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/merged-output.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/debate-transcript.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/base-selection.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/refactor-plan.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/merge-log.md
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/return-contract.yaml (the skill's own contract)
- /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG3/adversarial/adversarial/variant-1-original.md and variant-2-original.md
