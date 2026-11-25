# Section 12 analysis: Build procedure, with the SC commands and the check for each step
Counts: COVERED 20, CONFLICT 9, NOT-COVERED 6

Sources read: 655 body lines 1-30, 163-174, 213-230; SPEC.md sections 2, 4, 5, 6, 7, 8, 9, 10, 13 and Appendix B (all under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/); DECISIONS.md lines 531-538; D02, D07, D11, D15 verdict lines named below; techref ISSUE-TO-WORK-PIPELINE lines named below; Makefile lines 46-55 and 354-359; .github/workflows/contract3-generator-constraint-lint.yml. "SPEC" below means that SPEC.md.

## Rows

### S12-F1 Spec step "done": design doc written with /sc:design and approved by Clay (ruling 37)
- 655 says: Step 1 (body line 165): the spec `docs/designs/orchestrator.md` on branch `clayphi/issue-655-spec` is finished and approved by Clay with additions A to E; line 7 repeats that the spec wins over the body.
- Status: CONFLICT
- Current plan: SPEC Appendix B.2 (SPEC.md:770) marks PR 681 (the design doc) "SUPERSEDED BY PR 700: design doc not on master; text on the archive branch". SPEC 6.1 (SPEC.md:389) and FR-68 (SPEC.md:325) say it is "contested, not owner-approved"; no builder starts PR B or PR E before an owner-reviewed amendment merges (SPEC.md:569, 10.5). The unification spec (SPEC.md) is the design of record; D16 (SPEC.md:92, 339-342) says approval by the author is not review. 655's "approved by Clay" is rejected.
- Evidence from our documents: SPEC.md:569 "no builder starts PR B or PR E before it merges"; SPEC.md:529 "PR 681 said 'the owner reviews and merges'; its author merged it about 90 minutes after opening."; SPEC.md:787 (B.3 item 2) the owner has not yet decided whether to restore the design text.
- Concerns: Any build task that cites `docs/designs/orchestrator.md` as approved is wrong; it is off master since PR 700 (commit `471f10511`, SPEC.md:758). The archive branch name is `clayphi/archive-orchestrator-655-20261120` (SPEC.md:759).

### S12-F2 Spec gives every open question an answer, every carried-over item a disposition and every dropped item a removal plan
- 655 says: Step 1 (line 165): the spec "answers every open question of this issue and gives every carried-over item a disposition and every dropped item a removal plan".
- Status: COVERED
- Current plan: SPEC section 7 (SPEC.md:435-468, D15's 71 Clay elements decided one by one), section 6 (SPEC.md:376-433, one disposition per PR and branch), Appendix A traceability (SPEC.md:715-750) and the removal-plan row G5 "ADOPT" (SPEC.md:468). Same effect, different document.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC.md:754 says Appendix B was "NOT re-reviewed"; DECISIONS.md:608 says D15 did not read the IronFlow coordinator spec (UNVERIFIED coverage of that source).

### S12-F3 Plan step: a tasklist where every task names its files and an acceptance check
- 655 says: Step 2 (line 166): run `/sc:workflow` on the spec; check is a tasklist in which every task names its files and an acceptance check, with the PR split.
- Status: COVERED
- Current plan: The effect (files plus acceptance check per unit of work, with order) is delivered by SPEC 5.1 (SPEC.md:350-366, "Files and what", requirements, order), the stage table 8.2 columns "Deliverables and tests" and "Rollback" (SPEC.md:482-501) and section 13 (SPEC.md:690-713). The command `/sc:workflow` itself is not named for the stages (see S12-F4).
- Depends on: S12-F4
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC.md:696 states "A test marked NEW is an acceptance requirement, not a passing test; none was run by this spec's author." Builders must write them.

### S12-F4 Run /sc:workflow then /sc:implement once per PR; check that the ledger shows per-task QA passed
- 655 says: Step 2 (line 166) runs `/sc:workflow`; step 4 (line 168): `/sc:implement` once per PR; check "each run's ledger shows per-task QA passed".
- Status: NOT-COVERED
- Current plan: none found as a stated rule for stages S0 to S17; searched SPEC.md, FOLLOW-UPS.md, STATE.md for "sc:workflow", "sc:implement", "ledger" with Grep. Only hits: SPEC.md:276 (FR-55, a claim-chain rule for users of `/sc:issue`), SPEC.md:372 (the old planb `/sc:implement` run, ledger state UNCLEAR) and SPEC.md:416 (PR 653 routing). Section 8 rules (SPEC.md:474) say "one reviewable PR, one local action" per stage but not how it is built.
- Component (NOT-COVERED only): OTHER, a process rule for how each stage PR is built; it fits none of watcher, coordinator or dashboard.
- Feature statement (NOT-COVERED only): Each stage PR of section 8.2 is planned with `/sc:workflow` and built with one `/sc:implement` run whose ledger shows per-task QA passed, and the ledger is staged under `.dev/tasks/`.
- Done when (NOT-COVERED only): every stage PR body links its `/sc:implement` ledger and the ledger lists every task as QA passed.
- Depends on: S12-F3
- Evidence from our documents: SPEC.md:372 "The state of its `/sc:implement` run is UNCLEAR and must be re-checked ... the ledger ... ends `T28: complete`, `FINAL: pass`"; this shows an `/sc:implement` ledger is the practice but its state was disputed, which is the reason a "ledger shows QA passed" check has value.
- Concerns: The owner's global rule already routes planned work through `/sc:workflow` then `/sc:implement` (CLAUDE.md "How to choose a workflow", level 3), so this is a reminder, not a new design. `.dev/tasks/` must stay staged (owner rule).

### S12-F5 PR D "retire the gate first": delete the approval code in issue_pipeline, WC-17 and guard G2 rule 1
- 655 says: Step 3 (line 167): PR D retires the plan-approval gate first (Clay): the approval code in `issue_pipeline`, WC-17, the issue-pipeline duties of WORKER-CONTRACT and guard G2 rule 1. Acceptance line 229 repeats "no ... plan-approval gate remains".
- Status: CONFLICT
- Current plan: D03 and D14 (SPEC.md:79, 90): revert PR 682 (which made that deletion) because both gates stay. A13 "deletion of plan-approval code (PR 682): REJECT (revert)" (SPEC.md:448). PR 700 already restored the pre-682 tree on master (SPEC.md:388, 758). FR-31 keeps `check-approval` (WC-17) and `release-worker` (SPEC.md:233); SEC-20 restores G2 rule 1 (SPEC.md:309); OA-1 "do BOTH gates stay" is still an open owner answer (SPEC.md:554, 789). Branch 8.3 (SPEC.md:505-507) is the only way PR D could return, as a new removal PR if the owner says "only the start gate stays".
- Evidence from our documents: SPEC.md:507 "After PR 700 the plan-approval code is on master, so this branch now means a new removal PR ... Confidence in the disposition set falls to about 50 percent (D14)."; DECISIONS.md:535 "REVERT ... only if the owner says in chat that BOTH gates stay".
- Concerns: PR 682 was merged about 66 minutes after opening (SPEC.md:388) and its removal broke `superclaude --help` when combined with PR 686 (D03, SPEC.md:384). Not to be redone without OA-1.

### S12-F6 PR A as the vehicle for the poll core
- 655 says: Step 3 (line 167): PR A is the poll core, one pull request, opened second (after D).
- Status: COVERED
- Current plan: PR 686 (branch `clayphi/issue-655-pr-a`, the same PR A) is KEEP-ADAPT in place as ONE draft (SPEC.md:384; FR-73 SPEC.md:337; stage S11 SPEC.md:495), after planb (S9), names (D08) and PR 690's check. Same vehicle; it merges only on the owner's go (SPEC.md:474).
- Depends on: S12-F7
- Evidence from our documents: n/a (COVERED)
- Concerns: The owner's local branch "planb" overlaps PR 686 on 23 files (SPEC.md:370); order S9 before S11 is binding.

### S12-F7 Contents of PR A: assignment-only discovery, repo list and map, new-since-last-poll rule, routing with 3 in flight, hold with plan requests, 62 closed reasons, tier validation
- 655 says: Step 3 (line 167): PR A holds "assignment-only discovery, the repo list and map, the new-since-last-poll rule, routing (at most 3 in flight each), the hold with its plan requests, the 62 closed reasons, tier validation".
- Status: CONFLICT
- Current plan: Each item is decided elsewhere; the list as a bundle is rejected where it differs. Assignment-only discovery: A12 REJECT, FR-01 "Assignment alone never starts work" (SPEC.md:447, 191). Repo list and map: FR-11 one cron entry calling `run-all`, "no registry repository, no `repos.yaml`" (SPEC.md:201); C5 REJECT (SPEC.md:454). Routing with 3 in flight: FR-33 default key 3 but "first build enforces 1" (SPEC.md:235). Hold with plan requests: A4 DEFER, A5 REJECT now (SPEC.md:442-443), FR-06 strips label writes (SPEC.md:196). 62 closed reasons: FR-20 reasons table must equal the code (restore 14 approval reasons; SPEC.md:210), so "exactly 62" is rejected. Tier validation: OD-1 `plan_depth`, "no `plan_tier`" (SPEC.md:97, 280). Only the new-since-last-poll rule and per-repo routing idea are not contradicted; those belong to section 1 and 5 of 655 and are classified there.
- Evidence from our documents: DECISIONS.md:608 "The 62-reason table pin forbids the 14 approval reasons the approval gate needs."; SPEC.md:454 "C5 registry repository, allow list, idle end, `wrong_target`; C7 `setup-clone` | REJECT".
- Concerns: A builder who follows 655 for PR A would reproduce what D01, D09, D07 rejected. Use the stage list S9, S11, S12 instead.
- Depends on: 655 section 1 (discovery), section 2 (hold), section 5 (routing and tiers); classified by those analysts.

### S12-F8 PR P: `/sc:issue --plan` with `--remaining`, after D and before B
- 655 says: Step 3 (line 167): PR P is the `/sc:issue --plan` mode with `--remaining`, after D and before B.
- Status: COVERED
- Current plan: PR 690 (branch `clayphi/issue-655-pr-p`) is KEEP-ADAPT then merged in lane 1, after PR 693 (SPEC.md:385; S2 SPEC.md:486; FR-53, FR-59 SPEC.md:274, 280). It precedes the coordinator build (O1 before O4, SPEC.md:348). The "after D" part is moot: D is not planned (S12-F5).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: PR 690 needs four fixes and a merge-only trial on master plus PR 693 "never run" (SPEC.md:385); owner chooses who edits it (OA-2).

### S12-F9 PR B: the whole orchestrator skill and command as ONE pull request (ten waves, refs, four templates, playbook, verbs, limits.py, names.py, contract section)
- 655 says: Step 3 (line 167) and acceptance line 217: the skill `orchestrator` and command `/sc:orchestrator` land as one PR with all ten waves, refs, four templates, the playbook, the verbs, `limits.py`, `names.py` and an "Orchestrated issue flow" section of WORKER-CONTRACT.
- Status: CONFLICT
- Current plan: The role is "coordinator", command `/sc:coordinator`, skill `sc-coordinator-protocol`; "no `commands/orchestrator.md`, no `sc-orchestrator-protocol`" (FR-24, SPEC.md:226; FR-62 SPEC.md:319; D08 SPEC.md:84). Build is split: S13 substrate, S14 merge path and bound worker route (T13), S15 as four PRs (S15a to S15d), S16 observability glue (SPEC.md:497-500), each a separate PR with its own owner go. The merge path is one tested unit (SEC-01 to SEC-13), but not the whole skill. The contract amendment is S8 (SPEC.md:492), not part of the skill PR. The four-template and playbook content belongs to 655 sections 3 to 9 (classified there).
- Evidence from our documents: SPEC.md:499 "S15 ... (four PRs: S15a wake-check and wake-ack ...; S15b cap ...; S15c AU1-AU8, handback, `report-entry`, `escalate`; S15d cleanup `list`)"; SPEC.md:569 "no builder starts PR B or PR E before it merges".
- Concerns: A single PR of that size defeats per-stage rollback ("every stage reverts by reverting its PR", SPEC.md:474). No builder may start PR B until the owner-reviewed design amendment (FR-68, now needing the archive-branch decision B.3 item 2).
- Depends on: 655 sections 3 to 9 (wave content), S12-F1

### S12-F10 PR B opens only after A and P merge and the local end-to-end tests (T1 to T13) pass
- 655 says: Step 3 (line 167) and acceptance line 217: PR B is "opened after A and P merge and the local end-to-end tests pass"; results of T1 to T13 go in its description.
- Status: COVERED
- Current plan: Order O1 to O3 (PR 693, PR 690, planb, adapted PR 686) before O4 to O6 (coordinator build) (SPEC.md:348; DECISIONS.md:597). S13 needs S10 merged; S14 needs S13 and has test T13 `tests/coordinator/test_merge_path.py` (SPEC.md:497-498); the common gate MC-1 to MC-12 applies (SPEC.md:478, 692).
- Depends on: S12-F8, S12-F6
- Evidence from our documents: n/a (COVERED)
- Concerns: The panel found S15a could start before S11 because no precondition links them (spec-panel-report review-1 line 202, panel/review-1/spec-panel-report.md); the fix in the spec is partly UNVERIFIED. The 655 test list "T1 to T13" differs from the spec's "T1, T3, T4, T8, T10, T11 logic rewritten, T12 for hand-back" (SPEC.md:467); the numbering is Clay's, not ours.

### S12-F11 PR C: move the `agent-work-report` skill into IronClaude
- 655 says: Step 3 (line 167): PR C moves `agent-work-report` into IronClaude.
- Status: COVERED
- Current plan: PR 684 already moved it, then PR 700 removed it from master (SPEC.md:393, 758). Restoring it from the archive branch needs "a later owner-approved PR" and is an open owner decision (SPEC.md:786, B.3 item 1; row E1 SPEC.md:464). Until then FR-45, FR-46, FR-48 are blocked (SPEC.md:778). Same destination (skill lives in IronClaude), pending the owner's yes.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: Conditional on the owner answering B.3 item 1; if "No", FR-45, FR-46, FR-48 are dropped or rewritten against a new report skill. The report side (living report) belongs to 655 section 7.

### S12-F12 PR E: real fixtures, live-test record and rewritten runbook
- 655 says: Step 3 (line 167): PR E carries real fixtures, the live-test record and the rewritten runbook. Acceptance line 230 requires them before `enabled: true`.
- Status: COVERED
- Current plan: Stage S17 "live tests, then enable one throwaway repo" with a go/no-go record that includes "fixture captures" (SPEC.md:501); section 13.2 "real replies captured to replace assumed fixtures" (SPEC.md:705); PR 685 (the issue 442 runbook and results) is KEEP, merged beside S4 (SPEC.md:387, 488); the setup runbook text is corrected by FR-69 (SPEC.md:326, S4).
- Depends on: S12-F22
- Evidence from our documents: n/a (COVERED)
- Concerns: No "PR E" exists in the plan under that name; the work is spread over S4, S17 and PR 685. SPEC.md:569 still forbids starting "PR E" before the design amendment merges.

### S12-F13 Outside IronClaude: the orchestrator repo holds the spec, the work report state and the repo list
- 655 says: Step 3 (line 167) and acceptance line 228: a private repo `IronbellyOrg/IronOrchestrator` holds the coordinator spec and work-report state; line 28 says the orchestrator reads the repo list from it.
- Status: CONFLICT
- Current plan: D07 "Project-local coordinators, one dispatcher, per-repo config, no registry repository" (SPEC.md:83); C5 "registry repository ... REJECT" (SPEC.md:454); FR-11 "no registry repository, no `repos.yaml`" (SPEC.md:201). Where state lives instead: per-repo JSON config in `<config_dir>` (FR-11, FR-12) and an interim ledger in a `.dev/tasks/` package imported by a local commit on the `coordinators` branch (SEC-14 SPEC.md:303; S13 SPEC.md:497; FR-64 SPEC.md:321).
- Evidence from our documents: debates/D07/VERDICT.md:5 "CLAY keeps a registry `.orchestrator/orchestrators.json` in a separate repo `IronbellyOrg/IronOrchestrator` ... OURS ... coordinators live in each project"; SPEC.md:83 shows OURS/HYBRID won.
- Concerns: A separate private repo also moves state outside the checkout that the guard and sweep read; D07 judged it a registry that adds a second source of truth. Nothing here to build.

### S12-F14 Keep the IronFlow copy of the work report updated
- 655 says: Step 3 (line 167) and acceptance line 228: "keeping the IronFlow copy updated" (FR-13, FR-1, FR-2, FR-19, rows C25 to C29 are Clay's numbering).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, FOLLOW-UPS.md, STATE.md, inventory/clay-prs.md, D07/D11/D15 verdicts, both techrefs with Grep for "IronFlow" and "IronOrchestrator". Hits only say the IronFlow coordinator spec "was not read" (debates/D11/VERDICT.md:108, debates/D15/VERDICT.md:264) and a PR 684 note (inventory/clay-prs.md:200, not read in detail).
- Component (NOT-COVERED only): OTHER, a cross-repo upkeep task for a repo outside IronClaude; it fits no component of this project.
- Feature statement (NOT-COVERED only): When the work-report skill changes in IronClaude, the copy in the IronFlow repo is updated to match, or the owner records that it is no longer kept.
- Done when (NOT-COVERED only): a diff of the IronClaude skill files against the IronFlow copy shows no difference, or an owner decision in the ledger drops the copy.
- Depends on: S12-F11
- Evidence from our documents: debates/D11/VERDICT.md:108 "The IronFlow coordinator spec was not read."
- Concerns: UNVERIFIED which repo and which files "IronFlow copy" means; our documents never read it. Also touches an external repo; owner go needed, and nothing may touch SuperClaude-Org.

### S12-F15 Issue #668 (the closeout skill) is its own issue and a dependency of wave 8
- 655 says: Step 3 (line 167) and acceptance line 226: `/sc:closeout` is issue #668, a dependency of wave 8, merged before the live test.
- Status: COVERED
- Current plan: PR 683 (merged `/sc:closeout`; issue 668 is its request) is KEEP (SPEC.md:392); F1 `/sc:closeout` ADOPT (SPEC.md:465); FR-38 runs `/sc:closeout <PR>` per merged PR under a go naming the close (SPEC.md:240).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC.md:392 notes its two `/sc:issue --plan` references only resolve when PR 690 merges. The "wave 8" wording is 655's.

### S12-F16 Each PR passes the regression gate on its own and leaves `enabled: false`
- 655 says: Step 3 (line 167) check: "each PR passes the regression gate on its own and leaves `enabled: false`".
- Status: COVERED
- Current plan: Section 8 rules (SPEC.md:474): "a stage never enables a later one; no stage schedules `run-all` or installs cron before S17 ... `auto_enable` stays false". MC-5 "`enabled` absent means off" (SPEC.md:478); FR-23 (SPEC.md:213); FR-74 applies MC-1 to MC-12 to every PR touching `issue_watch/` (SPEC.md:338); "A green PR 686 alone does not prove the combined tree" (SPEC.md:474).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S12-F17 Regression gate: tests via uv, `make sync-dev` then `make verify-sync`
- 655 says: Step 5 (line 169): per PR run `make test` and `make sync-dev` then `make verify-sync`.
- Status: COVERED
- Current plan: Section 8 rules (SPEC.md:474) "Run suites with `uv run`; run `make sync-dev`; never stage `.claude/`"; MC-7 "`make verify-sync` passes and no `.claude/` path is staged" (SPEC.md:478); NFR-06 (SPEC.md:344). The Makefile target `make test` exists (Makefile:13, verified).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The spec names `uv run pytest` and suites, not `make test` literally; the effect is the same.

### S12-F18 Regression gate: `make lint`, `uv run ruff format --check src/ tests/`, `make verify-deps`
- 655 says: Step 5 (line 169): the gate also runs `make lint`, `uv run ruff format --check src/ tests/` and `make verify-deps`.
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md and spec/ with Grep for "verify-deps", "ruff format", "make lint", "lint". The MC-1 to MC-12 list (SPEC.md:478) has no lint, format or dependency check. The commands exist: `make lint` runs `lint-architecture` and `uv run ruff check .` (Makefile:48-50), `make verify-deps` runs `scripts/verify_deps.py` (Makefile:356-358).
- Component (NOT-COVERED only): OTHER, a build and CI process rule; no runtime component owns it.
- Feature statement (NOT-COVERED only): Every stage PR also passes `make lint`, `uv run ruff format --check src/ tests/` and `make verify-deps` before it is opened.
- Done when (NOT-COVERED only): each stage PR body records a pass for those three commands next to MC-1 to MC-12.
- Depends on: S12-F17
- Evidence from our documents: no evidence found in our documents (no verdict or risk row covers lint or dependency checks for this build).
- Concerns: Only `ruff format --check src/ tests/` is not a Makefile target (`make format` rewrites files, Makefile:53-55); a builder must run the check form, not `make format`. Whether CI already runs these is UNVERIFIED (workflows not read beyond contract3).

### S12-F19 Open each PR with `/sc:pr-submit --monitor 3 --head <branch>`; Augment and Codex findings of Medium or higher fixed, CI green
- 655 says: Step 6 (line 170): open each PR with `/sc:pr-submit --monitor 3 --head <branch>`; check that Augment and Codex findings of Medium severity or higher are fixed and CI is green.
- Status: COVERED
- Current plan: SPEC section 6 intro (SPEC.md:378) "PRs open only through `/sc:pr-submit --monitor 3`; a returned URL must read `github.com/IronbellyOrg/IronClaude/pull/N`"; Q04 and SEC-22 define the typed run line as the go for that run's pushes (SPEC.md:96, 311); project CLAUDE.md names the same command and the Medium-or-higher rule.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: Under SEC-22 a person types the run line; an agent or worker never does. A push needs a typed go except that line (SPEC.md:474).

### S12-F20 A PR that touches a gate or validator file carries a "## Generator-Constraint Considered" section
- 655 says: Step 6 (line 170): such a PR "carries the '## Generator-Constraint Considered' section".
- Status: NOT-COVERED
- Current plan: none found in SPEC.md, DECISIONS.md, techref, spec/ (Grep "Generator-Constraint" over the brainstorm folder: hits only in archived PR 682 JSON and D02 debate files, not in any requirement). The rule already exists in the repo as a CI check: `.github/workflows/contract3-generator-constraint-lint.yml` requires the heading when the PR touches `gates.py`, `structural_checkers.py` or `*_validator.py` (lines 6, 38-46, verified).
- Component (NOT-COVERED only): OTHER, a PR-body rule already enforced by an existing workflow, not by any of the three components.
- Feature statement (NOT-COVERED only): Stage PRs that touch a gate or validator file state in the body why a generator-side constraint was not enough, under the exact heading the workflow checks.
- Done when (NOT-COVERED only): the `Generator-Constraint Considered (Contract #3)` check is green on each such PR.
- Depends on: none
- Evidence from our documents: .github/workflows/contract3-generator-constraint-lint.yml:46 "this PR touches a validator/gate surface (gates.py / structural_checkers.py / *_validator.py) but the PR body lacks a '## Generator-Constraint Considered' section".
- Concerns: Automatic in CI; no backlog item needed beyond a reminder in the PR template or `/sc:pr-submit` text. Whether any planned stage touches those files is UNVERIFIED (the planned `merge-gate` and `plan-check` code might).

### S12-F21 No PR is merged by the orchestrator session or a worker; each stops at green for the owner's QA
- 655 says: Step 6 (line 170): "For this build no PR is merged by the orchestrator session or a worker: each stops at green for the owner's QA."
- Status: COVERED
- Current plan: Section 8 rules (SPEC.md:474) "every merge needs its own typed go"; SEC-01 merge only on a person's typed go naming repo, PR and 40-character head sha (SPEC.md:290); SEC-05 never run `/sc:pr-submit` or `/sc:closeout` as a worker (SPEC.md:294); D06 (SPEC.md:82); section 6 intro (SPEC.md:378) "none may be executed without the owner's go in chat". Stronger than 655: it also covers every push.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC.md:577 (OA-5): without a ruleset or a separate agent login, "a worker cannot merge" cannot be made true; the control "narrows" only.

### S12-F22 Live test (owner-run): real `gh` and Orca; every `_assumed_shape` fixture replaced by captured output or given a written reason; `tests/issue_watch/` passes; record committed
- 655 says: Step 7 (line 171) and acceptance line 230: owner-run live test with real `gh` and Orca; check that every `_assumed_shape` fixture is replaced by captured output (or has a written reason), `uv run pytest tests/issue_watch/` passes, and the record is committed.
- Status: COVERED
- Current plan: SPEC 13.2 "Cron shadow run ... real replies captured to replace assumed fixtures" (SPEC.md:705); S17 "live tests" with a go/no-go record of "fixture captures, failed and passed probes" kept by an agent (SPEC.md:501); section 13.2 intro "Nothing below has run. Each needs the owner's go" (SPEC.md:700); `uv run pytest tests/issue_watch` is part of the planb re-check (SPEC.md:372) and `test_security_invariants.py` etc. must stay green (SPEC.md:696).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: Techref says the live-test record file `docs/designs/issue-watcher-live-test.md` is absent and all 19 fixtures are assumed (ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:341, 672). The plan has no explicit "written reason" exception and does not name where the record is committed (S17 says "kept by an agent"); UNVERIFIED.

### S12-F23 Live test uses throwaway issues that are only assigned
- 655 says: Step 7 (line 171): the live test uses "throwaway issues that are only assigned".
- Status: CONFLICT
- Current plan: FR-01 "Assignment alone never starts work" (SPEC.md:191); D01 (SPEC.md:77); A12 "assignment alone as trigger: REJECT" (SPEC.md:447). S17 enables "one throwaway repo" whose trigger label is made first on the owner's chat OK naming that repo (SPEC.md:501); throwaway issue and repo used by guard probes (SPEC.md:706); OA-19 (SPEC.md:582). A live test must therefore label or approve the throwaway issue, not only assign it.
- Evidence from our documents: SPEC.md:447 "A12 assignment alone as trigger | REJECT | docs; O1 | keep Clay's 'conditions to revisit' (guard effective; workers cannot push or merge; skip when claim record exists; owner records the reversal)".
- Concerns: Writing the trigger label or issue edits on GitHub needs the owner's go (SPEC.md:700); the poll itself writes nothing (NG-2, FR-06).

### S12-F24 Shadow run: 24 hours in dry-run mode, then read the audit log
- 655 says: Step 8 (line 172): 24 hours in dry-run mode, then the audit log.
- Status: COVERED
- Current plan: SPEC 13.2 "the cron line runs `run-all --dry-run` for 24 hours under cron's environment; no agent, no config generated, no GitHub write" (SPEC.md:705); S17 pass list "a 24-hour `run-all --dry-run` shadow run that generated and wrote nothing" (SPEC.md:501); FR-23 `test_dry_run_generates_nothing` (SPEC.md:213); MC-12 (SPEC.md:478); the audit log is `audit.jsonl` (FR-05, SPEC.md:195; FR-20 reasons table).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The S17 pass list is "a proposal, UNVERIFIED" (SPEC.md:501). The cron entry may not be installed before S17 (SPEC.md:474), so the shadow run is the first time it exists; Coder 515 must land first (SPEC.md:547).

### S12-F25 Shadow-run check: every cycle ends with exit 0 or an understood reason
- 655 says: Step 8 (line 172): "every cycle ends with exit 0 or an understood reason".
- Status: NOT-COVERED
- Current plan: none found as a pass criterion; searched SPEC.md 8.2 S17, 13.2 and NFR-04 with Grep for "exit 0", "exit", "understood", "skipped". The 13.2 pass criterion (SPEC.md:705) lists only "no agent, no config generated, no GitHub write". NFR-04 adds `recent_skips[]` and a served-repo count to `status --json` (SPEC.md:217) and the existing tests pin exit codes (techref ISSUE-TO-WORK-PIPELINE:2215), but no step requires reading them after the shadow run.
- Component (NOT-COVERED only): WATCHER, it checks the poll's own cycle exit codes and skip reasons.
- Feature statement (NOT-COVERED only): After the 24-hour shadow run, every recorded cycle exited 0 or has a named reason from the reasons table (FR-20), and any other exit blocks switch-on.
- Done when (NOT-COVERED only): a script run over the shadow run's `audit.jsonl` and cron log lists zero cycles with an unexplained nonzero exit.
- Depends on: S12-F24
- Evidence from our documents: techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:2215 "`once` exit code = cycle code, crash gives exit 1 with class name only, `status` JSON fields and exit follows age".
- Concerns: Small gap; easy to fold into the S17 pass list. Cron hides exit 75 under the detach (D02 position, position-CLAY.md:19), so exit codes must be read from `status` and the audit log, not from cron.

### S12-F26 Two-process lock test: the second process exits 75
- 655 says: Step 8 (line 172): a two-process lock test; "the second process exits 75".
- Status: COVERED
- Current plan: The behaviour exists and is tested: `flock(LOCK_EX|LOCK_NB)` on `state_dir/lock`, held gives exit 75 (techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:703, 835, 1629); `tests/issue_watch/test_concurrency.py` runs two real processes on one store (techref :2226). FR-10 runs cron under `flock -n` (SPEC.md:200); the dispatcher keeps its own lock (debates/D02/position-OURS.md:12); FR-33 and NFR-02 keep one writer per file. The full suite is part of every PR's gate.
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: SPEC 13.1 does not list `test_concurrency.py` by name and S17 does not re-run it as a pre-enable step (UNVERIFIED); a rerun on the cron host before S17 would be cheap.

### S12-F27 Restart test: the state folder survives a restart
- 655 says: Step 8 (line 172): a restart test; "the state folder survives a restart".
- Status: COVERED
- Current plan: SPEC 13.2 "Cron and worktree in the image: after two restarts: one `crontab -l` line, one daemon (Coder 515); `Coordinator` worktree exists (Coder 516)" (SPEC.md:713); FR-29 "kill-and-restart tests" (SPEC.md:231); RK-9 and MC-6 (SPEC.md:653, 478); S15a kill-and-restart tests (SPEC.md:499); MC-11 backup before migration (SPEC.md:478); NFR-03 state root read from config (SPEC.md:216).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: No requirement names "state folder survives a restart" for the poll's own store directly; the closest are the kill-and-restart tests at the ack-to-state boundary. UNVERIFIED that these cover the whole folder.

### S12-F28 Switch-on: create the Orca automation
- 655 says: Step 9 (line 173) and acceptance line 215: create the Orca automation (poll script every 5 minutes, precheck exits non-zero so no agent starts) and have no cron entry.
- Status: CONFLICT
- Current plan: D02 "Cron stays the scheduler; fix the owner's false reason; Clay's precheck automation is a tested-first fallback" (SPEC.md:78); B2 "Orca automation as scheduler: REJECT; cron stays; fallback after the firing test" (SPEC.md:449); FR-10 one cron entry `*/5 * * * *` under `flock -n` installed by the image (SPEC.md:200). The only automation allowed is the disabled `orchestrator-poll` precheck test, run after a scheduled shadow run (SPEC.md:704).
- Evidence from our documents: SPEC.md:449 "B1 precheck pattern ... ADOPT+CHANGE (fallback); B2 Orca automation as scheduler | REJECT"; DECISIONS.md:198 "Decisive fact that would reverse the choice: a headless `*/5` automation with a `; exit 1` precheck fires for 1 to 24 hours with only skipped rows, survives an Orca restart ... UNVERIFIED: that an automation fires headless on this host".
- Concerns: The reversal depends on a live test nobody has run (SPEC.md:700). Clay's precheck claim is partly correct; FR-69 corrects the owner's wording, not Clay's design.

### S12-F29 Switch-on: set `enabled: true` and watch the first real cycles
- 655 says: Step 9 (line 173): set `enabled: true` and watch the first real cycles.
- Status: COVERED
- Current plan: OA-19 "switch a repo on: every repo off; at most one throwaway repo after the shadow run, cap 1, `claim_by: poll`" (SPEC.md:582); FR-23 (SPEC.md:213) and OA-28a: `auto_enable` ships false, the owner turns it on once in chat after the S17 throwaway run; S17 "then enable one throwaway repo" (SPEC.md:501); kill switches `DISABLED` and `enabled: false` (SPEC.md:501 rollback).
- Depends on: S12-F22, S12-F24
- Evidence from our documents: n/a (COVERED)
- Concerns: Stricter than 655: one throwaway repo, cap 1, then a second owner go for `auto_enable`.

### S12-F30 Switch-on check: `status` reports a healthy last cycle
- 655 says: Step 9 (line 173): check that `status` reports a healthy last cycle.
- Status: COVERED
- Current plan: NFR-04 extends `status --json` with `last_sweep_at`, `recent_skips[]`, stranded deliveries, served-repo count, unreadable-state alarm (SPEC.md:217); S12 "schema-pinned status" (SPEC.md:496); FR-44 the observer reads `issue-watch status --json` (SPEC.md:255); the existing `status` exit follows age (techref ISSUE-TO-WORK-PIPELINE:2215).
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: S17's pass list does not name this check (SPEC.md:501); it would be one line to add.

### S12-F31 Switch-on check: one assigned issue is claimed once and its worker started once
- 655 says: Step 9 (line 173): "one real assigned issue is claimed once and started once".
- Status: COVERED
- Current plan: for the "once" property only: FR-03 `marker_in_window` so a hand claim and a watcher start never run two workers (SPEC.md:193); FR-21 "an unknown launch receipt never relaunches" with replay tests (SPEC.md:211); FR-29 adoption record by exclusive create (SPEC.md:231); FR-33 cap 1 first build (SPEC.md:235); S17 throwaway run (SPEC.md:501). The "real assigned issue" part is S12-F32.
- Depends on: S12-F32
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S12-F32 Switch-on on a real assigned issue
- 655 says: Step 9 (line 173): the first live issue is a real assigned one; acceptance line 230 only requires #442's checks first.
- Status: CONFLICT
- Current plan: OA-20 "flip `WORKER_BINDING_PROVEN` after the probe" with default "not flipped: no worker on a real issue, probe issues only" (SPEC.md:583); FR-30 refuses a start for any issue outside per-repo `probe_issues` while `WORKER_BINDING_PROVEN` is false (SPEC.md:232); OA-23 real rollout stays off until the X-001 check is recorded (SPEC.md:585, FR-70 SPEC.md:327); SPEC 8.2 closing note: S17 "does not include raising the cap, Pipeline-field governed launches, label writes, `claim_by: coordinator` or a second polling host" (SPEC.md:503). Assignment alone is not the trigger either (S12-F23).
- Evidence from our documents: SPEC.md:583 "not flipped: no worker on a real issue, probe issues only"; SPEC.md:327 "real rollout stays off until the X-001 live check ... is recorded and the owner picks the route (OA-23)".
- Concerns: A real rollout is a later, separate owner decision; the first-cycle watch applies to the throwaway repo only.

### S12-F33 Schedule the 7-day review (FU-10) after switch-on
- 655 says: Step 9 (line 173) and the carried-over list (line 160): "the 7-day review (FU-10) is scheduled".
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, FOLLOW-UPS.md, STATE.md, DECISIONS.md with Grep for "FU-10", "SLO", "7-day", "seven-day" (no hits; hits only in the technical reference and old debate files). D16's 14-day review (FR-78, SPEC.md:342) is a different review (of the pull-request process, not of the watcher).
- Component (NOT-COVERED only): WATCHER, because FU-10 is the watcher's SLO review (approval-to-launch time, exit-0 share, claimed share, stale count) and its inputs come from the watcher store.
- Feature statement (NOT-COVERED only): Seven days after the first live enable, the owner (or a scheduled agent) reads the watcher's SLO numbers and decides whether to keep it on.
- Done when (NOT-COVERED only): a dated review entry exists in the ledger or a task, created at switch-on, that cites the four SLO numbers from `slo_numbers`.
- Depends on: S12-F29
- Evidence from our documents: techref ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1954 "D-03 SLO numbers ... `slo_numbers` (`P/cycle.py:1359`) and `SloNumbers` (`:1339`) have no caller; ... NOT BUILT"; :1990 "FU-10 SLO review ... 'None of these is built by this work' ... FU-10 'after 7 days live'".
- Concerns: `slo_numbers` has no caller today, so the review needs a reader first (maybe a status field); the review itself would need the owner's decision. FU-10 was in Clay's "carried over" list (line 160).

### S12-F34 Close issue #450 as replaced by #655
- 655 says: Step 9 (line 173) and acceptance line 230: "Close #450 as replaced by this issue."
- Status: CONFLICT
- Current plan: SPEC 6.4 "Issue 655 | KEEP and RESCOPE | assignee drops 'replaces #450' (D14)" and "Issue 450 | KEEP open | Clay's 2026-11-18 17:00:32 comment has no recorded answer; the owner answers" (SPEC.md:426-427); OA-22 "Answer Clay on issue 450; rescope issue 655" (DECISIONS.md:1247); posts to 450 and 655 are by their assignees only, agents write nothing (SPEC.md:565).
- Evidence from our documents: DECISIONS.md:537 "Issue 655: KEEP and RESCOPE (the assignee drops 'replaces #450'). Issue 450: KEEP open and answer Clay's 2026-11-18 comment."
- Concerns: Closing 450 is a GitHub write; a plan item, not a build step; agents may not do it.

### S12-F35 #442's launch checks pass before the first worker on a real issue
- 655 says: Acceptance line 230: "#442's checks pass before the first worker on a real issue."
- Status: COVERED
- Current plan: SPEC 13.2 "Guard probe (issue 442's twelve observations ...)" (SPEC.md:706); "Worker binding" test (SPEC.md:707); PR 685 (issue 442 runbook and results) merged beside S4 (SPEC.md:387); `test_launch_level_observations.py:79-84` twelve skipped observations, "un-skipped only by the owner" (SPEC.md:696); OA-20 gate (SPEC.md:583).
- Depends on: S12-F32
- Evidence from our documents: n/a (COVERED)
- Concerns: none

## Section summary
- Section 12 is a process section; its 35 rows split into 20 already delivered by the current plan (most through stages S2, S11, S17, section 13.2, MC-1 to MC-12 and the merge rules), 9 rejected conflicts (spec approved by Clay, PR D, PR A bundle, PR B as one PR with the old names, the orchestrator repo, assigned-only live test, Orca automation, real-issue switch-on, closing #450) and 6 gaps.
- The gaps are small and mostly process: use /sc:workflow and /sc:implement ledgers per stage (F4), the extra lint, format and verify-deps gate (F18), the Generator-Constraint PR section (F20, already enforced by an existing CI workflow), the IronFlow copy (F14), the shadow-run exit-code check (F25) and the FU-10 7-day review (F33).
- The build order itself is replaced: 655's D, A, P, B, C, E (six PRs) becomes the owner-gated stages S0 to S17, PR 700 already did the revert, and no PR B or PR E starts before an owner-reviewed design amendment.
- UNVERIFIED items a reader must keep: whether CI already runs lint and verify-deps (F18), what "IronFlow copy" means (F14), whether the S17 pass list will include lock, restart and status checks (F26, F27, F30).
