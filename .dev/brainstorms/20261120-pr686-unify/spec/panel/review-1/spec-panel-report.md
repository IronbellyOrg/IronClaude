review: 1 of 3

# Spec panel report: unification spec candidate-1 (critique, detailed, unattended)

| Field | Value |
|---|---|
| Candidate | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/candidate-1.md` (738 lines) |
| Candidate sha256 | `6f16cdf0b2ec7bb5714a9d19fe55c6b4ea1206a3f7daf0fc748bbdd9c97b6fbc` (taken with `sha256sum`; equals the frozen hash in the brief) |
| Baseline | none (first review; no `--re-review`, no `--baseline`) |
| Reviewer model actually used | `claude-gw-tier1b[1m]` |
| Date | 2026-11-20 |
| Mode, focus, format | critique; requirements, architecture, testing, compliance, correctness; detailed |
| Report directory | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/panel/review-1` |
| Inputs read in full | the command file `spec-panel.md`, `~/.claude/WORKER-CONTRACT.md`, `~/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt followed), the whole candidate |
| Panel | one reviewer session playing the 11 experts in the fixed order. The coordinator's panel and merge steps (`superclaude review panel resolve`, `superclaude review merge`, ledger) were not run by this session: the brief asked for one review and the command lists no nested invocations. The findings block at the end is written for that merge. |

## Summary

One blocking finding, 13 Medium findings (warnings) and 11 Notes. Verdict FAIL because F1 is open.

| ID | Severity label | Grade | Spec section | One line |
|---|---|---|---|---|
| F1 | MAJOR | BLOCKING | 4.1 FR-82; 1.3; 8.2 S9; 4.5 SEC-07 | FR-82 says only `repo_init.py` may write to GitHub, but its own acceptance check (the planb NG-2 test, "unchanged") asserts that `complete.py` also writes; planb's `complete.py` (result comment plus Status move) lands at S9 with no requirement, no grant name and no step in the flow |
| F2 | MAJOR | Medium | 4.4 FR-52; 4.1 FR-20; 8.2 S9 | FR-52 says the Pipeline field is not read; planb (landed at S9) reads it and skips `level_gated` |
| F3 | MAJOR | Medium | 4.2 FR-25, FR-27; 4.5 SEC-01, SEC-08; 4.1 NFR-02; 3.3 row 6 | No requirement says which coordinator invocation merges, or which session writes the go entry |
| F4 | MAJOR | Medium | 8 rules; 4.2 FR-32; 4.5 SEC-15; 13.2 | "A typed go precedes every push" is never reconciled with `/sc:pr-submit --monitor 3` fix-round pushes or with the Full Submit per-issue go |
| F5 | MAJOR | Medium | 4.2 FR-34 vs FR-27 | Coordinator restart is not gated by the autostart consent that FR-27 requires for any script start |
| F6 | MAJOR | Medium | 5.1 L-07; 4.5 SEC-15; 4.2 FR-26, FR-29 | The revert restores the old "Issue pipeline duties" (adoption rows, GitHub-read approval, label and Status mirror); L-07 edits lines 298 and 300 but no requirement says how; two adoption records now exist |
| F7 | MAJOR | Medium | 8.2 S13, S14, S15 | S15a (wake pull) has no precondition on S11 (the wake writer) |
| F8 | MAJOR | Medium | 4.7 FR-75 to FR-78; 9; 8.2 | The process package (CODEOWNERS, ruleset, throwaway test, decisions file) has no stage row, rollback or owner-gate column |
| F9 | MAJOR | Medium | header; 2; 8.2 S5; 10.3 | "Binding decisions" and "a verdict is binding" against "all are recommendations until the owner rules"; S5 treats OA-9 as settled |
| F10 | MAJOR | Medium | 4.1 FR-23, FR-82; 8.2 S17 | The S17 pass list needs the trigger label to exist while the label step is read-only; one go is said to cover later repos' labels |
| F11 | MAJOR | Medium | 4.2 FR-33; 4.5 SEC-21; 11.3 | Cap: "key default 3, first build enforces 1"; value 0 undefined; the phase that frees a store entry is not defined, so the waiting-go slot has no test |
| F12 | MAJOR | Medium | 4 (all subsections) | About 25 requirements have a bare `NEW` as their acceptance check |
| F13 | MAJOR | Medium | 10.2; 8.2 S17 | The exposed Orca runtime token is an owner action with no stage and no precondition |
| F14 | MAJOR | Medium | 4.1 FR-07 vs 4.5 SEC-06 | The fixture line FR-07 cites also holds `pr.merge`, a grant name SEC-06 says to refuse |
| N1 to N11 | MINOR | Note | various | see follow-up candidates |

## Coverage (what this review checked)

- Whole candidate read once (738 lines). Hash verified.
- Section 2 against the requirements: all 42 rows (D01 to D16, Q01 to Q03, OD-1 to OD-13, ten OA sub-answers) have at least one implementing requirement; counts 42, 26 contradictions (7 R plus 19 X) and 71 Clay elements (13+11+8+20+7+5+7) re-added and correct; every Clay element id A1 to G7 appears in section 7.
- Numbers and paths re-read against sources: master snapshot lines `cycle.py:216, 228, 979`, `launch.py:33`, `record.py:34-35`, `predicates.py:14`, `cli.py:165`, `cli/sweep/commands.py:277-278`, `report.py:621-631, 642-661`, `launch-level-guard.sh:265-272, 785-790`, `orca_worktree.py:822, 1515`, `test_security_invariants.py:652, 683`, `test_launch.py:75`, `test_launch_level_observations.py:79-84`, `test_worker_contract.py:426-429, 3220`, `WORKER-CONTRACT.md:57, 70, 241, 244, 245`, `core/CLAUDE.md:58`, `ccsession-tag/README.md:423`, `observe/questions.py:9-12`, `agent-work-report/scripts/common.py:139-141`, `sweep/models.py:265-266`, `classify.py:994-999`: all match. pr-a `wake.py:46-47`, `audit.py:92-93`, `cycle.py:1293-1300`, `github.py:983`, `repos.py:295-299`, `conftest.py:286`: match. pr-p `plan_body.py:138`: matches. Live GitHub reads (read-only, `--repo IronbellyOrg/IronClaude`): PR 681 opened 22:32:39Z and merged 00:02:33Z (about 90 minutes), PR 682 opened 22:56:28Z and merged 00:02:36Z (66 minutes), 36 files, 4,599 deletions; PR 686 head `8e5ae29ad`, 59 files; PR 690 head `f3bc77981`, 13 files; PR 693 and PR 690 share exactly four files; PRs 539, 584, 591, 661, 670, 683, 684 merged; PR 685 has 266 files, all under `.dev/`; `origin/master` is `61ac2c2e6`. Planb: HEAD `d0a0a433b`, branch name, 225 status entries, requirements file 121 lines with R1 to R36, ledger tail `T28: complete`, `FINAL: pass`, `ARCHIVE: start`: all match.
- Not checked: the full text of the 42 verdict files beyond D03, D05, D06, D12 spot reads; the FULL-REPORT; Clay's PR list in 6.3; organisation rulesets; the "89 of 100 merged by their own author" figure; the planb ledger beyond its tail.
- Method note: the Guard Condition Boundary Table is complete (section "CORRECTNESS ANALYSIS"); the Pipeline Dimensional Analysis ran and found no unhandled count divergence (it found one under-specified one, F11).

=== REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn. What holds: every FR, NFR and SEC row has an id, a "shall" sentence, a source and a check column; the traceability appendix covers every FR and SEC id; section 12.4 states which rows rest on the brainstorm alone; every one of the 42 binding decisions has an implementing requirement.

**F2 (MAJOR, Medium) FR-52 says the Pipeline field is not read; the planb code that S9 lands reads it.** Expert: Wiegers. FR-52 (4.4): "Not read the Pipeline field while `GOVERNED_LEVELS_ALLOWED` is false". Planb `github.py:109` queries `pipeline: fieldValueByName(name: "Pipeline")` and planb `cycle.py:1032-1036` skips with `level_gated` when the item's Pipeline is anything but None. S9 lands planb and its acceptance says "no governed level launches while R33 is false". Both can hold, but they differ for an issue whose Pipeline is Full Submit: FR-52 claims it at none-level, planb skips it. FR-20 (reasons table "equal to the code", MC-10) never names `level_gated`. Grade: Medium, because the implementer must guess which behaviour the spec wants; no stated text causes harm on its own. Recommendation: say whether planb's `level_gated` skip stays (then FR-52 reads "does not act on Pipeline except to skip a non-None level") or is removed. Priority Medium.

**F9 (MAJOR, Medium) The document calls its verdicts both binding and recommendations.** Expert: Wiegers. Header: "A verdict is binding unless two verdicts contradict (section 11)"; section 2 is titled "Binding decisions" yet says "All are recommendations until the owner rules in chat"; the status row says the same. S5 (8.2) lists its precondition as "none (OA-9 settled)" and 10.3 says "the sweep file location is settled (OA-9)", while the cited D11 verdict says "owner decides: saved beside the report, or each reader sweeps" and OA-9 was only debated (OAG2, 85%). X-19 in the same document says an owner rule outranks a triage label. Grade: Medium: S5 still carries an owner go, so the worst case is a premature change reviewed by the owner. Recommendation: rename section 2, and give S5 the precondition "owner answer to OA-9". Priority Medium.

**F12 (MAJOR, Medium) Bare `NEW` as an acceptance check.** Experts: Wiegers, Adzic, Crispin. The row form defines "NEW = to be written", but a bare `NEW` names no command, test or observable, so the row has no pass criterion. Rows with only `NEW`: FR-16, FR-17, FR-18, FR-19, FR-24, FR-25, FR-28, FR-36, FR-37, FR-38, FR-40, FR-46, FR-47, FR-48, FR-49, FR-52, FR-56, FR-59, FR-61, FR-67, SEC-06, SEC-09, SEC-13, SEC-17, NFR-03, NFR-04. Others cite prose rather than a check: FR-04 ("doc; NEW"), FR-32 (`WORKER-CONTRACT.md:244-246`), NFR-02 ("review against merged section 4"). Example: FR-28 ("Pull the wake folder at every `check --wait` return, at most every 5 minutes") has no observable that distinguishes pulling at every return from pulling every hour. Grade: Medium: the sentence "an implementer builds a pull that passes no check and nobody can say it is wrong" needs the guess that no one adds a test later. Recommendation: give each row one named test and its one-line assertion. Priority Medium.

**F14 (MAJOR, Medium) FR-07 fixes one grant in a fixture line and leaves another that SEC-06 forbids.** Expert: Wiegers. FR-07: "drop the `issue.hold` grant from reference config and fixtures (`tests/issue_watch/conftest.py:286`)". That pr-a line is `"grants": ["issue.assign", "issue.hold", "pr.merge"]`. SEC-06: "Carry no standing `pr.merge` or `issue.close`; refuse both as grant names." An implementer who follows FR-07 to the letter keeps `pr.merge` in the fixture, and a loader that refuses `pr.merge` (SEC-06) then rejects the reference fixture. This is also the one place where the document would ship a standing merge grant name in a reference config. Grade: Medium: test fixture only. Recommendation: FR-07 drops `issue.hold` and `pr.merge` from that line. Priority Medium.

=== ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard. What holds: one writer per file is stated (NFR-02) and the interface table names a writer and a reader for each path; at-least-once delivery is designed with the M1 and M2 rules; the poll is separated from the coordinator by files, not calls.

**F3 (MAJOR, Medium) No requirement names the session that merges, or the writer of a go entry.** Experts: Fowler, Nygard. FR-25: "Treat flag-less `/sc:coordinator` as person-opened: no grant, no merge; grants have one door (`--wake` or `--take`)". FR-27 makes a `--wake` session script-started. SEC-01: the go is "typed in live chat after the gate output"; SEC-08: "typed by a person in their own session, never relayed". NFR-02 says the coordinator writes go entries; row 6 of 3.3 says "coordinator; recording agent". So: a flag-less session cannot merge, a `--wake` session has no person in its chat, and `--take` is never tied to merging in any requirement. Which session runs `merge-gate`, `gh pr merge` and writes `goes/<PR>-<sha12>.json` is not stated, and the one-writer rule is broken between NFR-02 and row 6. Grade: Medium: the implementer picks a session; the worst reading (the merging coordinator writes its own go entry) is the residual risk RK-3 already admits. Recommendation: one sentence in SEC-01: merge runs only under `--take` in a session the person opened, and the recording agent is the sole writer of go entries. Priority High within Medium.

**F6 (MAJOR, Medium) The revert restores duties that the requirements neither carry nor amend.** Experts: Fowler, Newman. S7 restores the pre-deletion "Issue pipeline duties". Pre-deletion `WORKER-CONTRACT.md` line 298 (read from `01e7a9e23^`) says to "read GitHub through `stage-status`", "write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status"; line 296 says "Create the adoption row (`adopt-create`) before `worker-start`"; line 300 says "post an issue write without that issue's grant row". L-07 (5.1) says to edit "pre-deletion lines 298, 300", but SEC-15 lists only lines 57, 70, 245, and S8's check ("finds no 'still written by the owner'") tests none of the three. Consequences: (a) approval is read from GitHub in the restored text while SEC-14 says approvals are given in chat; (b) "mirror the label and Status" is a GitHub write outside the three grants of SEC-07; (c) FR-29 defines a second adoption record (`issues/<repo-key>__<N>.json`) for the same step as the restored `adopt-create` row; (d) FR-26 says "one verb group `superclaude coordinator`" while FR-30 and FR-31 use the restored `issue-pipeline` group (`check-approval`, `release-worker`) and planb adds `issue-pipeline complete` (F1). Grade: Medium: L-07 names the lines, so the step exists, but the target text and the authoritative record are left to a guess. Recommendation: add a requirement that states, for lines 296 to 300, what replaces them and which of the two records is authoritative. Priority High within Medium.

**F7 (MAJOR, Medium) S15a does not depend on the stage that writes wakes.** Expert: Hohpe. S15 preconditions: "S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder 516 for restart". Wake files under `<state_dir>/wakes/` are produced by the PR 686 adaptation (L-10, S11: "wakes under `<state_dir>/wakes/`, M1, M2"), and master has no wake code (1.3). S13 requires only S10 and S12 requires S9 and S11. Sequence attack: S13, S14 and S15a can all run before S11, and S15a's kill-and-restart tests have no wake to pull. Grade: Medium: numeric order puts S11 first, so a sequential builder does the right thing. Recommendation: add S11 to S15's preconditions. Priority Low within Medium.

=== TESTING ANALYSIS ===

Experts: Crispin (lead), Gregory, Adzic. What holds: 12 mechanical merge checks are defined once (8.1) and reused by id; every stage has a tests column; 13.1 lists existing tests that must stay green and 13.2 lists the live firing tests; unproven numbers are labelled UNVERIFIED and each names the check that settles it (12.2). Weak points: F12 (bare `NEW`), F11 (cap tests), F1 (a check that cannot pass, below) and these:

- FR-23 and S9 test that `enabled` stays false and that `--dry-run` writes nothing, but FR-82 (no label creation while `auto_enable` is false) has only `NEW`. See F10.
- SEC-21 (waiting go keeps its slot and counts toward the cap) is tested only for display ("a go waiting 3 days is shown with its age, no message sent"). See F11.
- The S6 dry run is "no PR, nothing pushed" with owner gate "none"; the way the throwaway checkout is made is not stated (N9).

=== COMPLIANCE ANALYSIS ===

Experts: Wiegers (lead), Nygard, Hightower. The five owner rules are checked first, then the findings.

| Owner rule | Where the spec states it | Result |
|---|---|---|
| 1 The poll writes nothing to GitHub outside the allowed steps | FR-06, FR-82, MC-8, diagram "seven read-only gh calls" | Holds for the poll cycle. Two defects at the edge: F1 (a second writer module exists in the landed code) and F10 (one go said to cover later repos' labels) |
| 2 A person's typed go before every push and merge | section 8 rules, FR-32, SEC-01, SEC-02, SEC-08 | Holds for merge. Push has two unreconciled cases: F4 (`/sc:pr-submit --monitor 3` fix-round pushes, and the Full Submit per-issue go in SEC-15) |
| 3 Workers never run `/sc:pr-submit` | SEC-05, FR-32, FR-38, FR-61, E-1 | Holds in the requirements. 13.2's guard probe still lists "a full `/sc:pr-submit --monitor 3` cycle only if level FS is ever opened" (F4) |
| 4 No standing merge or close grant | SEC-06, SEC-07, SEC-12, FR-07 | Holds in the requirements; the fixture defect is F14 |
| 5 Approvals given in chat, recorded by an agent | SEC-14, SEC-08, Q01, line 57 amendment | Holds in the requirements; the restored contract lines 296 to 300 still read approval from GitHub (F6); S5 treats a debate result as settled (F9) |

**F1 (MAJOR, BLOCKING) FR-82's "only `repo_init.py` may write" contradicts its own acceptance check and the landed code; the second writer has no requirement.** Experts: Wiegers, Nygard, Whittaker (divergence attack).
- Stated text A, FR-82 (4.1): "only `repo_init.py` may write, only `gh label create` for the trigger label, only after the owner's chat OK".
- Stated text B, the same row's acceptance check: "planb `test_security_invariants.py:1059-1079` unchanged". That planb test is `test_only_complete_and_repo_init_may_write_to_github`: `_WRITER_MODULES = {"complete.py", "repo_init.py"}` and `assert {"complete.py", "repo_init.py"} <= writers  # the scan is not vacuous`. Unchanged, it requires `complete.py` to be a GitHub writer.
- The code: planb `src/superclaude/cli/issue_pipeline/complete.py` posts a result comment on the issue and, for a succeeded run, moves the Project Status to `In review`. Its header says "This module and `issue_watch/repo_init.py` are the only code that writes to GitHub". It rests on the owner's R24 (requirements file line 50, decided 2026-11-19) and on a `superclaude issue-pipeline complete` verb. Section 1.3 lists `complete.py` among the planb-only pieces and S9 lands planb, but no FR, SEC, flow step (3.2 steps 1 to 10) or grant name covers it. SEC-07's closed list is `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; a Status move is none of them.
- Grading check: an implementer who follows FR-82 as written makes `repo_init.py` the only writer and keeps the cited test "unchanged"; that test fails (`complete.py` is not a writer) or, if left as planb has it, passes only while `complete.py` writes, so the text says both "only one writer" and "a check that requires two". An implementer who keeps the check lands an unlisted coordinator GitHub write (comment plus Status move) at S9 with no grant, no flow step and no owner gate, against the document's own statement that the coordinator's GitHub writes are the three granted ones. Two stated texts contradict and the acceptance check cannot pass with the first: blocking (categories: contradiction, unpassable-check).
- Recommendation: either (a) rewrite FR-82 to "only `repo_init.py` and the coordinator-only `issue_pipeline/complete.py` may write; the poll cycle and `github.py` never", add the completion step to 3.2, name its grant in SEC-07 (or state that the Status move is refused until a grant exists) and keep the planb test; or (b) require S9 to remove `complete.py` and change the test, with the owner's R24 decision answered in chat. Priority High.

**F4 (MAJOR, Medium) "A typed go precedes every push" is not reconciled with two cases.** Experts: Nygard, Fowler. (1) Section 8 rules: "a typed go precedes every push and merge"; FR-32: "push and `/sc:pr-submit --monitor 3` only on a typed go in a person-opened session". The project rule for `/sc:pr-submit --monitor 3` says it "pushes the fixes without asking" after the PR is open (the same fact appears in DECISIONS.md line 569: it "pushes after review"). The spec never says whether the one go covers those later round pushes, whether each round needs its own go, or that the loop is stopped for one. (2) SEC-15 amends contract line 245 so that "Full Submit push is the person's go for that push and PR only", L-07 ties it to R25 "Full Submit as a per-issue go", and 13.2 plans a "full `/sc:pr-submit --monitor 3` cycle" if FS is ever opened; that is an approval label, not a typed go, and a worker-bound FS session pushing, against SEC-05 and the "typed go" sentence. Grade: Medium: both readings are allowed and the worse one needs a guess; FS is behind OA-20 and lines 70 and 245 are "drafted, not in force". Recommendation: add one sentence stating what the push go covers (the first push only, or the whole monitor loop) and name the Full Submit per-issue go as the only exception to "typed", under OA-7. Priority High within Medium.

**F5 (MAJOR, Medium) Restart is a script start, but FR-34 does not require the consent FR-27 requires.** Expert: Nygard. FR-34: "Restart a dead coordinator with a resume wake, at most 3 times (stored counter)". FR-27: a script may start the coordinator only with an owner authorization recorded in chat, "`coordinator_autostart` absent means false". E-2 and 10.6 (OA-18) say the default is no script start. Nothing says the restart honours `coordinator_autostart`. The 3-restart counter is bounded, so the harm is limited. Recommendation: add "only when `coordinator_autostart` is true" to FR-34. Priority Medium.

**F10 (MAJOR, Medium) The label path for the first live repo is circular, and one go is said to cover later repos.** Experts: Hightower, Nygard. FR-82: while `auto_enable` is false the label step "reads only and reports `would_create`"; "the go that turns `auto_enable` on covers later repos' trigger label". Planb `first_run.py` lists the checks in order and check 2 is "`label`: the trigger label exists on the repository (created through `repo_init`)". S17's pass list needs "the six `first_run` checks green on the throwaway repo" before the owner turns `auto_enable` on. With the label step read-only the label check cannot go green unless the label already exists, and no step says who creates the throwaway repo's label or under which owner OK. Second, a go given once on `auto_enable` then lets cron-run `run-all` create a label on every later repo: a standing GitHub write for repos that do not exist yet, outside the closed grant list (SEC-07) and not what FR-82's own first clause ("only after the owner's chat OK") says. Grade: Medium: the sequence needs a guess (a hand-made label), and the second point is a verdict choice (OAG3, 88%) the owner still has to rule on. Recommendation: say in S17 that the owner's chat OK names the throwaway repo's label creation, and state in FR-82 whether the later-repo cover is accepted by the owner or limited to listed repos. Priority Medium.

**F8 (MAJOR, Medium) The process package has no stage, rollback or owner-gate entry.** Experts: Wiegers, Hightower. FR-75 ("Add `.github/CODEOWNERS` (sole owner `@ironbelly`;"), FR-76, FR-77 and FR-78 are required, and section 9 gives ranks, cost and who. Section 8's stage table has S0 to S17 and S0 only says "recommend the ruleset". None of the S rows carries the CODEOWNERS PR, the ruleset activation, the throwaway test or the decisions file, and section 9 has no rollback column (S0 alone says "admin deletes any ruleset"). Section 5.1 (L-01 to L-13) omits them too. The ruleset is the one control that the document says would make "a worker cannot merge" true, so its ordering against S7 and S14 matters. Grade: Medium: section 9 states an order and an owner gate in prose. Recommendation: add stage rows (for example S0b to S0e) with rollback and owner gate. Priority Medium.

**F13 (MAJOR, Medium) The exposed Orca token has no stage and no precondition.** Expert: Hightower. Section 10.2: "Rotate the local Orca runtime auth token a debate agent printed into its own transcript ... not rotated". S17's preconditions are "all HIGH rows of 12.1 proven or accepted in chat" and the token is not a risk row. S17 starts the cron watcher and coordinator that type into terminals while a live Orca control token sits in a transcript on the host. The text does not expose the secret further (it names the file, not the value), so this is a missing precondition, not a leak. Grade: Medium. Recommendation: add the rotation to S17's preconditions and to the risk register. Priority Medium.

=== CORRECTNESS ANALYSIS ===

Experts: Nygard (lead), Fowler, Adzic, Crispin, Whittaker.

### State Variable Registry (FR-15.1)

| Variable | Type | Initial value | Invariant | Read by | Written by |
|---|---|---|---|---|---|
| `enabled` (per-repo config) | bool | false; absent means off (FR-23) | true only after the six `first_run` checks and `auto_enable` on, or an owner chat go | poll, dispatcher | generator (false), `first_run` (true) |
| `auto_enable` | bool | false | flips once, on the owner's chat go after S17 (OA-28a) | `first_run` | recording agent on the owner's words |
| `DISABLED` kill file | file | absent | presence stops every cycle (`disabled`, `disabled_mid_cycle`) | poll | operator |
| store entry state | enum: pending, launched, claimed, woken, acked, unknown, failed, abandoned, waiting_reapproval | none | one entry per issue, counted once; closed by the poll from the per-issue phase (FR-33) | poll, `status`, coordinator (read) | poll only (NFR-02) |
| `max_in_flight` | int | key default 3; first build enforces 1 | in-flight count never above the cap | poll | config, protected by SEC-10 |
| wake delivery attempts | int | 0 | at most 3, 10 minutes apart, then unread and exit 7 | poll | poll |
| restart counter | int | 0 | at most 3 restarts (FR-34) | restart step | writer and file not named (NFR-02 lists none) |
| hand-back round | int | 1 | at most `HANDBACK_MAX` 3 (not measured); the poll owns it, the file copies it, the ack echoes it | poll, coordinator | poll |
| `grants` | list of strings | empty | subset of three names; `pr.merge` and `issue.close` refused (SEC-06, SEC-07) | coordinator verbs | `repos grant` on a recorded chat go |
| go entry | file `goes/<PR>-<sha12>.json` | absent | one-shot, void on a head move, a consumed go is never restored (SEC-08) | merge verb | "coordinator" (NFR-02) or "recording agent" (row 6): F3 |
| `.ok` file per session | file | absent | exists only after the recorded plan approval and `check-approval` (FR-31) | guard L1 | `release-worker` |
| `WORKER_BINDING_PROVEN` | constant | false | flipped only by a reviewed commit after the probe | coordinator start step | code change |
| `GOVERNED_LEVELS_ALLOWED` | constant | False | no level above None launches (planb `launch.py:48`) | poll | code change |
| `IR7_REFUSE` | constant | False | stays off until issue 442's observations pass (master `orca_worktree.py:822`) | claim launch | owner-approved commit |
| `coordinator_autostart` | bool | absent means false | script start only when true and authorized (FR-27) | dispatcher | recording agent on the owner's words |
| `probe_issues` | list | empty | worker start only for a listed issue while binding is unproven | coordinator | recording agent on the owner's words |
| `reach_daily_max` | int | absent or 0 means no notice cap | malformed value is a config error | notice step | protected key (SEC-10) |
| interim ledger | file | absent | one entry per answer, written by the recorder only | agents | recording agent |

### Guard Condition Boundary Table

An input class with no row for a guard is left out because it cannot occur for that guard; the last row gives the reason for the sentinel class.

| Guard | Location | Input condition | Variable value | Guard result | Specified behavior | Status |
|---|---|---|---|---|---|---|
| in-flight cap | FR-33 | Zero/Empty | `max_in_flight` = 0 | cap reached at once, or no cap | not stated: could mean "start nothing" or "no limit" | GAP (F11) |
| in-flight cap | FR-33 | One/Minimal | `max_in_flight` = 1 | true when one issue in flight | `coordinator_full` recorded | OK |
| in-flight cap | FR-33 | Typical | key 3 | cap 3 or 1? | "Key default 3 (D07); first build enforces 1": which governs a configured 3 is not stated | GAP (F11) |
| in-flight cap | FR-33, SEC-21 | Legitimate edge: a PR waiting for a go | store entry after `worker_done` | counted or closed? | SEC-21 says it counts; FR-33's counted list has no PR-open phase and the phase that closes an entry is not defined | GAP (F11) |
| in-flight cap | FR-35 | Legitimate edge: `waiting_reapproval` | 3 entries | not counted | "three waiting hand-backs never cause `coordinator_full`" | OK |
| start gate | FR-01, FR-05 | Zero/Empty | empty body | plan check fails | skip `held_incomplete` | OK |
| start gate | FR-05 | Sentinel match | `<...>`-only section | counts as empty | fails plan check | OK |
| start gate | FR-01, FR-04 | Legitimate edge: body edited after approval | edit timestamp later | approval void | `edited_after_approval` skip | OK |
| wake size | FR-13 | Typical | 1 item, 139-character repo name | fits | `test_full_wake_with_139_char_repo_names_fits_64_kib` | OK |
| wake size | FR-13 | Maximum/Overflow | items over 64 KiB | exceeds | not stated | GAP (N1) |
| wake folder | FR-28 | Zero/Empty | no wake files | nothing to pull | not stated (benign) | GAP (N1) |
| wake delivery | FR-13 | Maximum | 3 deliveries done | stop | mark workspace unread, exit 7 | OK |
| restart counter | FR-34 | Maximum | 3 restarts used | refuse | "at most 3 times" | OK |
| restart counter | FR-34 | Legitimate edge: terminal list unreadable | unreadable | unknown | "restarts nothing" | OK |
| restart counter | FR-34 | Legitimate edge: stored counter unreadable | unreadable | unknown | not stated | GAP (N1) |
| hand-back | FR-35 | Zero/Empty | empty remaining list | stop | "stop on empty list" | OK |
| hand-back | FR-35 | Maximum | round 3 reached | stop | `HANDBACK_MAX` 3, `no_progress` | OK |
| merge go age | SEC-01 | Typical | any age | no expiry in the first build | go ends on action, head move or revoke | OK |
| merge go age | SEC-01 | Sentinel match | owner records "none" or hours | automation refuses without a number | stated; 0 hours not defined | GAP (N11) |
| reviewer hold | SEC-04 | Typical | 59 minutes | holds | stated test: 59 holds, 60 escalates | OK |
| reviewer hold | SEC-04, SEC-10 | Sentinel match | `reviewers: none` | explicit exception, but also a "weakening value" | fails closed unless a record names it | OK |
| reviewer hold | SEC-04 | Zero/Empty | `reviewers: []` | none listed | not stated (differs from `none`) | GAP (N1) |
| zero repos | FR-11 | Zero/Empty | no repo served | alarm | stated; failed `orca repo list` is an error, never "zero repos" | OK |
| notice cap | FR-12, FR-47 | Zero/Empty and sentinel | `reach_daily_max` absent or 0 | no cap | stated (K23); malformed is a config error | OK; 0 collides with "zero notices" (N11) |
| binding probe | FR-30 | Maximum/timeout | `pending/<nonce>` not gone in 60 s | stop | stop the worker and escalate; no `jq` means no worker | OK |
| binding switch | FR-30 | Zero/Empty | `probe_issues` empty, binding unproven | refuse | refuse any start | OK |
| claim marker | FR-03 | Legitimate edge: hand claim | marker not from the poll | no wake | `test_manual_claim_gets_no_wake` | OK |
| cleanup | FR-39 | Legitimate edge: open PR with this head | head open | keep branch | "keep the branch if any PR with this head is OPEN or its `headRepositoryOwner` is not ours" | OK |
| cap, pull, cleanup | Sentinel class | no sentinel exists for these guards | n/a | n/a | left out: these guards compare plain counts or states | n/a |

The table is complete: every guard has a row or a stated reason. Eight rows are GAP: three belong to F11 (graded Medium), five to N1 and N11 (notes; no stated text does harm and nothing named rests on them).

### Pipeline Flow Diagram with counts (Quantity Flow Diagram, FR-21)

```text
[Open issues in the repo: N]
   --> [Start gate FR-01: assigned only to the watcher, Approved, Status, plan passes, no hold:backlog]
   --> [K eligible, K <= N]
   --> [Cap FR-33: launches L = min(K, cap - in_flight); first build cap 1]    --> [L claim sessions, L <= 1]
   --> [Marker seen next poll (FR-03: hand claims excluded)]                    --> [C claimed, C <= L]
   --> [Wake file FR-13: one item per claimed issue, ids only, <= 64 KiB]       --> [W wakes, W = C]
   --> [Coordinator FR-28 to FR-29: accepted A + skipped S + rejected R = W; the ack names each item (FR-19)]
   --> [Worker start FR-30: refused outside probe_issues while binding unproven]  --> [B workers, B <= A]
   --> [worker_done, coordinator commit, typed go, push, PR]                    --> [P PRs, P <= B]
   --> [Typed go to merge (SEC-01)]                                             --> [G merged, G <= P]
        Cap counter FR-33 counts: pending, launched, claimed, woken, acked, unknown, open claim files.
        SEC-21 says "waiting for a go" counts too; FR-33 names no PR-open phase  <-- UNDER-SPECIFIED (F11)
        waiting_reapproval: outside the cap (OD-13)                              <-- handled
```

Divergence points (N != M): the start gate (K <= N), the cap (L <= K), claim (C <= L), skip and reject at the coordinator (A <= W), worker refusal (B <= A), PR and merge (P <= B, G <= P). Downstream tracing: every consumer states its own count source (poll reads the store and per-issue phase, coordinator reads wakes, observer reads `status --json`); none assumes the original N. FR-19's CRITICAL rule is for a stage that "assumes count conservation". None does: the one candidate (waiting go and the cap) is handled in words by SEC-21 and OA-25b and is under-specified only in the phase list, so it is graded Medium (F11), not a CRITICAL mismatch.

Concrete scenario for F11, cap 1: issue A has `worker_done` and an open PR waiting for a merge go. If the store entry for A is closed when the worker finishes, the counted set is empty, the poll launches issue B, and two issues are in flight against SEC-21's "keeps its slot". If the entry stays `acked` until merge, the count is 1 and B waits, as SEC-21 intends. The text does not say which phase closes the entry.

**F11 (MAJOR, Medium) The cap has three open points.** Experts: Nygard, Crispin, Whittaker (zero and divergence attacks). (1) FR-33: "Key default 3 (D07); first build enforces 1 until claim agents have their own worktree"; 11.3 repeats it. A configured 3 gives no stated outcome; there is no test that cap 1 holds when the key says 3. (2) `max_in_flight` = 0 is undefined (the FR-12 rule "an absent authority key means the most restrictive value" covers absent, not zero). (3) SEC-21: "a waiting merge go keeps its slot, counts toward `max_in_flight` and never expires" has only a display test; the phase that closes a store entry ("The poll closes a store entry from the per-issue phase") is never listed. Grade: Medium: each point needs a guess; the worse guesses (cap 3 enforced, entry closed at `worker_done`) raise the number of simultaneous issues past the owner's intent but need a second wrong reading. Recommendation: one sentence per point and a test for each. Priority Medium.

### Whittaker adversarial analysis

Each attack uses the template "I can break this specification by [attack]. The invariant at [location] fails when [condition]. Concrete attack: [trace]".

1. **Zero/Empty Attack.** The invariant at FR-33 (in-flight never above the cap) fails when `max_in_flight` is 0. Trace: key set to 0 by a person editing the config; before: store empty; after: either nothing ever starts or the cap check `count >= 0` is true for all, or an implementer reads 0 as "no limit". The text decides none. (F11.)
2. **Divergence Attack.** The invariant at SEC-01 (a go is typed by a person in their own session) fails when the merging session is the `--wake` coordinator: FR-25 allows grants only through `--wake` or `--take`, and a `--wake` session has no person in it. Trace: go typed in session X, recorded in X; merge verb runs in session Y; Y either writes its own go entry (NFR-02) or trusts a file. (F3.)
3. **Sentinel Collision Attack.** `reach_daily_max` 0 means "no cap" and is also the default; an owner who writes 0 meaning "no notices" gets no limit. No push notice exists in the first build (OA-25a), so no harm now; it becomes real when a notice sender is built. `none` is also a typed word for both `reviewers` and the go age, and SEC-10 treats `reviewers: none` as a weakening value that fails closed unless a record names it: consistent. (N11.)
4. **Sequence Attack.** S15a (wake pull and ack, with kill-and-restart tests) can run before S11 (wake writer) because no precondition links them. Trace: S13 and S14 merge (their preconditions are S10 and S13); S15a starts; `<state_dir>/wakes/` has no writer on master. (F7.) Also: S4 puts the orchestrator.md banner in a PR before S7, while 6.2 step 5 and FR-68 put the same banner in the revert PR (S7); the second banner edit conflicts or doubles (N8).
5. **Accumulation Attack.** With cap 1, a PR waiting for a go counts toward the cap and never expires (OA-25b) and no push notice exists (OA-25a). Trace: PR waits 3 days; all other issues wait; the only signal is the observer line with the age. The document accepts this knowingly (OAG1); it is recorded as N10 so the owner sees it, not as a defect.

## Follow-up candidates

Medium warnings and notes never fail the review, trigger a revision or appear in the Reviser brief. This run is `--unattended`, so the list is only recorded; no issue is opened.

Medium (13): F2 Pipeline read (4.4 FR-52); F3 merge session and go-entry writer (4.2 FR-25, 4.5 SEC-01); F4 push go scope for `/sc:pr-submit --monitor 3` rounds and the Full Submit per-issue go (8, 4.2 FR-32, 4.5 SEC-15); F5 restart against autostart consent (4.2 FR-34); F6 restored issue-pipeline duties and the two adoption records (5.1 L-07, 4.5 SEC-15); F7 S15a precondition (8.2); F8 process package without stage rows (4.7, 9); F9 "binding" against "recommendation" and S5 (header, 2, 8.2); F10 label path circularity and the later-repo cover (4.1 FR-23, FR-82, 8.2 S17); F11 cap semantics (4.2 FR-33, 4.5 SEC-21); F12 bare `NEW` checks (4); F13 token rotation unscheduled (10.2); F14 fixture `pr.merge` (4.1 FR-07).

Notes (11):

- N1 Unspecified edge behaviour with no harmful stated text: a wake over 64 KiB (FR-13), an empty wake folder (FR-28), an unreadable restart counter (FR-34), `reviewers: []` against `reviewers: none` (SEC-04).
- N2 Section 6.2 step 3 says "(4,599 lines: 2,969 test, 1,618 source)"; the parts sum to 4,587. The 4,599 is GitHub's deletion count (verified) and the split is D03's own; the other 12 lines are not named.
- N3 FR-55 cites `skills/test_issue_protocol.py` lines 131-135, 745-784, 462 with no snapshot prefix; in the master snapshot lines 131-135 are the end of `chain_rows` and a blank comment line (in pr-p the function sits at 132-136).
- N4 Section 12.4 lists FR-23 among the rows resting on the brainstorm alone; FR-23's source column reads "D03, D14, OAG3" with no `BS` tag.
- N5 Section 9 says "about 120-150 minutes ... (arithmetic over the estimates)"; the listed ranks 1, 3, 4, 6 (three PRs at 5 minutes), 7 and 9 add up to about 133 to 165 minutes.
- N6 FR-34 names the duty holder `ORCH-IronClaude` while FR-62 limits "orchestrator" to Orca's layer, 63 installed files and quoted titles; the FR-62 allowlist test must permit this one name (the merged design K14 explains it).
- N7 Terms gaps: FR-30 uses `pending --level worktree` (guard level W, master `launch-level-guard.sh:265-272`) but the Terms table never maps the word to W; FR-24 adds a `--sub` flag next to the non-goal "the sub-coordinator (issue 444)".
- N8 The banner on `docs/designs/orchestrator.md` appears in S4 (L-02, "banner on `docs/designs/orchestrator.md`") and again in the revert PR (6.2 step 5, FR-68); two PRs edit the same banner.
- N9 L-06 and S6 run a dry run in "a clean throwaway checkout" with owner gate "none"; the way that checkout is made (the project rule is an Orca worktree, except the listed internal temporary checkouts) is not stated.
- N10 Accumulation: with cap 1, a PR waiting for a go keeps its slot forever and no push notice exists (SEC-21), so one waiting PR stops all new work and the only signal is the observer's age line. Accepted by OAG1; recorded so the owner sees the cost.
- N11 Sentinels: `reach_daily_max` 0 is both the default and "no cap" (an owner who means "zero notices" gets no limit); a go age of `0` hours is not defined next to "hours or none" (SEC-01).

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "only `repo_init.py` may write, only `gh label create` for the trigger label", "anchor2": "planb `test_security_invariants.py:1059-1079` unchanged", "refs": ["FR-82", "SEC-07", "S9", "1.3"], "claim": "FR-82 says only repo_init.py may write to GitHub while its cited acceptance check (the planb NG-2 test) requires complete.py to be a writer, and complete.py's result comment and Status move land at S9 with no requirement, grant or flow step."}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Not read the Pipeline field while `GOVERNED_LEVELS_ALLOWED` is false", "anchor2": "no governed level launches while R33 is false", "refs": ["FR-52", "FR-20", "S9"], "claim": "FR-52 says Pipeline is not read, but the planb code landed at S9 reads it and skips with level_gated, which FR-20 does not list."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Treat flag-less `/sc:coordinator` as person-opened: no grant, no merge", "anchor2": "typed in live chat after the gate output", "refs": ["FR-25", "FR-27", "SEC-01", "SEC-08", "NFR-02"], "claim": "No requirement names the session that runs the merge or the single writer of a go entry, and NFR-02 and row 6 disagree."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "a typed go precedes every push and merge", "anchor2": "push and `/sc:pr-submit --monitor 3` only on a typed go in a person-opened session", "refs": ["FR-32", "SEC-15", "13.2"], "claim": "The spec does not say whether one push go covers the fix-round pushes of /sc:pr-submit --monitor 3, or that the Full Submit per-issue go is the only exception to a typed go."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Restart a dead coordinator with a resume wake, at most 3 times (stored counter)", "anchor2": "`coordinator_autostart` absent means false", "refs": ["FR-34", "FR-27", "OA-18"], "claim": "FR-34 restarts a coordinator without requiring the autostart consent that FR-27 requires for any script start."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "pre-deletion lines 298, 300", "anchor2": "Provide one verb group `superclaude coordinator`", "refs": ["L-07", "SEC-15", "FR-26", "FR-29", "SEC-14"], "claim": "L-07 edits restored contract lines 298 and 300 but no requirement says what they become, and the restored adoption rows, GitHub-read approval and label and Status mirror sit beside FR-29's second adoption record."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder 516 for restart", "anchor2": "wakes under `<state_dir>/wakes/`", "refs": ["S15", "S11", "L-10"], "claim": "S15a pulls wakes but has no precondition on S11, which writes them."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Add `.github/CODEOWNERS` (sole owner `@ironbelly`;", "anchor2": "recommend the ruleset", "refs": ["FR-75", "FR-76", "FR-77", "FR-78", "9"], "claim": "The process package has no stage row, rollback or owner-gate entry in the staged migration."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "A verdict is binding unless two verdicts contradict (section 11)", "anchor2": "none (OA-9 settled)", "refs": ["2", "S5", "10.3", "X-19"], "claim": "Verdicts are called binding and also recommendations until the owner rules, and S5 treats a debated owner decision as settled."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "the go that turns `auto_enable` on covers later repos' trigger label", "anchor2": "the six `first_run` checks green on the throwaway repo", "refs": ["FR-23", "FR-82", "S17", "OA-28"], "claim": "The S17 pass list needs the label check green while the label step is read-only, and one go is said to cover label creation for repos not yet listed."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Key default 3 (D07); first build enforces 1 until claim agents have their own worktree", "anchor2": "a waiting merge go keeps its slot, counts toward `max_in_flight` and never expires", "refs": ["FR-33", "SEC-21", "OD-13", "11.3"], "claim": "The enforced cap when the key says 3, the meaning of 0, and the phase that closes a store entry (which decides whether a waiting go holds its slot) are not stated or tested."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Pull the wake folder at every `check --wait` return (at most every 5 minutes)", "refs": ["FR-16", "FR-17", "FR-24", "FR-28", "SEC-06", "SEC-13", "NFR-03"], "claim": "About 25 rows give a bare NEW as the acceptance check, so they have no named test or observable."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Rotate the local Orca runtime auth token a debate agent printed into its own transcript", "anchor2": "all HIGH rows of 12.1 proven or accepted in chat", "refs": ["10.2", "S17"], "claim": "Rotating the exposed Orca token has no stage and is not a precondition of the live enable."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "drop the `issue.hold` grant from reference config and fixtures (`tests/issue_watch/conftest.py:286`)", "anchor2": "Carry no standing `pr.merge` or `issue.close`; refuse both as grant names.", "refs": ["FR-07", "SEC-06"], "claim": "The cited fixture line also lists pr.merge, which FR-07 leaves in place and SEC-06 says to refuse."}
{"id": "N1", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "items `repo`, `number`, `url` only; three deliveries 10 minutes apart", "refs": ["FR-13", "FR-28", "FR-34", "SEC-04"], "claim": "Edge behaviour is unstated for a wake over 64 KiB, an empty wake folder, an unreadable restart counter and an empty reviewers list."}
{"id": "N2", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "(4,599 lines: 2,969 test, 1,618 source)", "refs": ["6.2"], "claim": "The two parts sum to 4,587, not 4,599; the source D03 states the same split."}
{"id": "N3", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "edits to `skills/test_issue_protocol.py` lines 131-135, 745-784, 462", "refs": ["FR-55"], "claim": "The line citation has no snapshot prefix and lines 131-135 are blank or comment lines in the master snapshot."}
{"id": "N4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "FR-19, FR-21 to FR-23, NFR-01 to NFR-04", "refs": ["12.4", "FR-23"], "claim": "Section 12.4 lists FR-23 as brainstorm-only but its source column has no BS tag."}
{"id": "N5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "about 120-150 minutes of session, maintainer and chat time", "refs": ["9"], "claim": "The stated total does not match the sum of the listed estimates (about 133 to 165 minutes)."}
{"id": "N6", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "until Coder 516 the duty holder is `ORCH-IronClaude` and nothing restarts", "refs": ["FR-34", "FR-62"], "claim": "The retired name ORCH-IronClaude sits in a requirement beside the FR-62 allowlist rule."}
{"id": "N7", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`--sub` (evaluation only)", "anchor2": "the sub-coordinator (issue 444)", "refs": ["FR-24", "FR-30", "1.2"], "claim": "The Terms never map the word worktree to guard level W, and FR-24 adds a --sub flag next to a stated non-goal."}
{"id": "N8", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "banner on `docs/designs/orchestrator.md`; merge PR 685", "anchor2": "corrections go in the same PR (FR-68)", "refs": ["L-02", "S4", "6.2", "FR-68"], "claim": "The orchestrator.md banner is placed in both the S4 text PR and the S7 revert PR."}
{"id": "N9", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Revert dry run in a clean throwaway checkout (6.2 step 2)", "refs": ["L-06", "S6"], "claim": "The way the throwaway checkout is created is not stated although the project rule requires Orca worktrees except listed temporary checkouts."}
{"id": "N10", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "no push notice in the first build; a waiting merge go keeps its slot", "refs": ["SEC-21", "OA-25"], "claim": "With cap 1 a single waiting PR blocks all new work and is visible only on the observer; accepted by the verdict, recorded for the owner."}
{"id": "N11", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`reach_daily_max` absent or 0 means no notice cap", "refs": ["FR-12", "FR-47", "SEC-01"], "claim": "Zero is both a default and a legitimate value (reach_daily_max, go age) with different readings."}
```

## Reviser brief

Blocking finding ids: F1 only.

Restated from the Review Loop (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after and the bytes added and deleted per finding id; leave Medium and minor findings (F2 to F14, N1 to N11) alone; do not award yourself a PASS.

- F1: repair FR-82 (4.1) and, only if needed to keep the two statements consistent, the planb test citation in its check column and the S9 row. Either name `issue_pipeline/complete.py` as the second permitted writer (and say where its coordinator step, grant name or refusal is stated), or require S9 to remove it; make FR-82's statement and its acceptance check agree.

verdict: FAIL
