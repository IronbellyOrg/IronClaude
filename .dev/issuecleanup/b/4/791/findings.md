# Round 2 findings for #791 (C10): Worker check-in template and the hourly status pass

Checked against master `f2894fc44` (2026-11-24). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/4/791/findings.md`. Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick` (report `.dev/issuecleanup/b/4/analyze/analyze-report.md`). Paths of the form `WORKER-CONTRACT.md:N` mean `src/superclaude/core/WORKER-CONTRACT.md` (byte-identical to `~/.claude/WORKER-CONTRACT.md`, checked with `diff`). `SPEC` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md`; `DEC` = `.../DECISIONS.md`; `D15` = `.../debates/D15/VERDICT.md`. `R38` = row 64 of `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`.

## Alignment with architectural decisions

- **R38 (owner, 2026-11-21; `requirements.md:64`, merged by PR #729): in conflict on the flag, UNVERIFIED on the template.** R38 lists "tier keys, living work report, read-only merge gate and flags" among Clay's parts that are not adopted, and keeps only the names `coordinator` and `/sc:coordinator`. `/sc:coordinator --hourly` (S02-F32, S08-F7) and the "Monday to Friday, 24 hours" schedule come only from issue 655 (`gh issue view 655`, body line 112, the "Worker status" row), which was closed as not planned. SPEC FR-24 (`SPEC.md:226`) and DEC:591 ("G2 flags ... adopt with change") list `--hourly`, but R38 states it supersedes the HYBRID rows. So the flag name has no standing; whether the check-in template itself counts as "an element of Clay's design" is not stated in R38 (UNVERIFIED: owner must say).
- **D12 (`D15:96`): aligned.** "One supervised `worker-start` route: mailbox, one message handled once per id, check-ins, restart" is Adopt with change. The template itself is not specified there.
- **D14 (`D15:98`) and FR-40 (`SPEC:242`): partly aligned.** A fixed template is fine; the rule is "type into worker terminals only under the four typing rules (never approve a permission prompt); never interrupt a worker". The text of the four typing rules is not in the files read (only the names "rules 1, 2, 3, 5" at `D15:98`): UNVERIFIED. The 60-second condition in this issue's test matches `DEC:416` ("idle, empty draft, 60 seconds without output"), but `DEC:416` governs the typed wake line to person-opened sessions, not workers.
- **WORKER-CONTRACT input veto (`:138`) and "Never on silence" (`:183-193`): in conflict if the request is typed.** "Never interrupt; never type into a busy, S11 or S4 session." A routine hourly typed request to every running worker would break this. No conflict if it goes through the Orca mailbox: WC-12 (`:62`) says coordinator follow-ups are pulled by the worker at its checkpoints.
- **WC-16 and the sweep (`:290`, `:111-115`) and DEC:502: partly aligned.** DEC:502 maps "hourly sweep = `/sc:sweep` (built, read-only)", and D11 VERDICT:43 puts the sweep "at the bottom" as a script that runs at most every 5 minutes. The hourly pass in this issue adds a per-worker request on top of the built sweep; the plan never gave it a cadence (`SPEC:229-242` names none).
- **L3 ask (`:154`) and answer/ack timeline (`:132-139`): aligned.** A status request with fixed fields already exists as L3 ("Reply with `status`: current step, what you are waiting for"), used only after a failed nudge. The template makes it routine; the A1 to A4 ack pattern can be reused for the answer.
- **SEC-16 (`SPEC:305`): aligned.** "Let no GitHub text reach a prompt, typed line, mailbox subject or argv." The id-only done-when matches it.
- **FR-26 (`SPEC:228`): dependency, not built.** `refuse(argv)` and its failing test per pattern are NEW; the done-when's `refuse(argv)` clause cannot run until C6 (#787) builds the list (no code on master: `grep -rn 'refuse(' src/superclaude/cli/sweep` finds nothing).
- **Closing review of #716 (comment of 2026-11-24, steps 1 and 2): aligned.** C10 is not in the set to start first (C1, C2, C4, C6, C25) and is not authorized merely by being listed.
- **Owner comment of 2026-11-24 on #716** ("watcher should be purely on the programmatic side; determine the current full handoff process before anything else is adopted"): neutral; C10 sits after the handoff.

## Complementary issues

- **#782 (C1, skill layout):** C10's template and a `refs/watch.md` live in the skill C1 creates. Interface: C1's file table must list the template and the ref. Blocked by C1.
- **#787 (C6, verbs per step, `refuse(argv)` list):** supplies the refusal list the done-when test calls. Interface: the verb name and the list API. Blocked by C6 if the typed path stays.
- **#806 (C25, one test per template):** generic template test (render with fixtures, no unfilled placeholders, every sending step names a template). Interface: C10 supplies the template file; C25 owns the generic test.
- **#789 (C8, issue body hash and re-read):** shares the status pass. Round 1 batch 3 moved the issue re-read (S08-F8) into C10; C8 keeps the hash record.
- **#793 (C12, playbook):** its S07-F4 line asks for the same template and test; the playbook says what to do with the answer.
- **#757 (run the sweep outside the session, wake on change):** possible trigger for the pass; also a tension (see below).
- **#792 (C11):** the answer's fixed fields and the "missing field is no answer" rule share the contract-field style.
- **#800 (C19):** the pass stops for a worker at its `worker_done`; C19 settles the terminal at the same event.
- **#766 and #590 (sweep misreads workers):** the pass reads "Orca state" from the same sweep reads; those bugs make the state column unreliable until fixed.

## Closest overlap

**#789 (C8) "Record the issue body hash at handoff and re-read the issue on every status pass".** Shared: the per-worker status pass and the issue re-read (C10's S02-F32 and S10-F25 texts both say "reading Orca state and the issue"; C8's S08-F8 is the same read). Estimated share of C10's done-when covered: about 20 percent of the scope text, 0 of its 3 tests (none of C10's tests exercises the re-read). Next two: **#806 (C25)**, about 15 percent (the generic render-and-placeholder test; C10's ids-only and answer-field tests are specific), and **#793 (C12)**, about 15 percent (S07-F4 asks for the same template and a "each check-in uses the template" test). #757 shares the periodic-check idea but defines no template, per-worker request or schedule (about 10 percent).

## Standalone or merge

**Verdict: stand alone.** Tested against #789:

- Owner: same (coordinator skill author); no difference.
- Acceptance test: different. C10: filled template has no GitHub text, answer missing a field is no answer, fake clock gives one check per running worker per interval on weekdays and none after `worker_done`. C8: `body_sha` equals sha256 of the body read at handoff, plus fake `gh` cases (reassigned, closed, edited).
- Files: C10 a template file, `refs/watch.md`, a schedule piece and tests; C8 the per-issue state file `issues/<repo-key>__<N>.json`, the handoff step and tests.
- Build phase: C8 belongs to the handoff wave, C10 to the watching wave after C1; C8 also carries a report-entry line that waits for #720.
- Risk if merged: C10 would be parked with C8's report-entry line (parked until #720's trigger, per the #716 closing review step 3), and the template would be held back by the state-file design.

Merging into #789 would be right only if the owner drops the check-in template and keeps just the issue re-read; then S08-F8 moves and C10 closes. No merge candidate beats stand-alone.

## Closed issues and merged PRs checked

- **#655 (closed as not planned):** source of the hourly, Monday-to-Friday, 24-hour pass (body line 112) and of "typing and approvals included" (line 42); the approvals part is rejected (D15:98).
- **PR #729 (merged 2026-11-23):** records R38; this is the decision that voids the flag and Clay-parts. Contradicts the `--hourly` flag, not the idea of a status request.
- **PR #539 (merged 2026-11-14):** the read-only sweep and WC-16 (5-minute pass). Delivers the observation half of the pass; the sweep has no code that sends or types (analyze finding A1).
- **PR #434 (merged 2026-11-08) and closed #431:** liveness rules (states, L0 to L5, ack timeline). Delivers the nudge and ask that C10 would make routine. #431 incident 5 (mailbox answers not seen for 35 to 40 minutes, cause not established) is a warning for a mailbox-only request: UNVERIFIED whether a worker reads the mailbox at its checkpoints in time.
- **PR #591 (merged 2026-11-17):** coordinator handoff (WC-17 and guard G2: a bound worker may send and ask only to its own coordinator). Constrains the answer path: the answer must be an `ask`/`send` reply with no `--to`.
- **PR #707 (merged):** the watcher; cron every minute per #450's closing comment (via #774, UNVERIFIED by me). No coordinator status request there.
- **#444 (closed, evaluation):** origin of the `--sub` flag in D08; no check-in.

## Updated recommendation

- **Action: keep open with changes.** (1) Deliver the request through the Orca mailbox and, at most, the contract's single typed copy to a positively idle prompt (`WORKER-CONTRACT.md:136`); drop the `refuse(argv)` 60-second clause or rewrite it as the idle-prompt test. (2) Drop the `--hourly` flag name and the weekday 24-hour schedule; let the owner set the interval (R38 voids the flag; no source for the schedule). (3) Build the issue re-read (S08-F8) here once; C8 keeps the hash. (4) Move the generic template test to #806. (5) Add: do not run it on a timer that adds noise while #757 is open; tie it to change or silence.
- **Priority: P3. Complexity: medium, size M.**
- **Versus round 1: action, priority, complexity and size unchanged.** Changed: R38 now cited as the reason the flag has no standing (round 1 did not cite R38 for it); DEC:502 duty map and #787 (refuse list) dependency added; #757 tension added; the closest overlap is named as #789 with the share estimated.

## Scan record

- Lists read in full (columns number and title; other columns not read): open-issues.tsv 134 of 134; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms: check-in, status, hourly, sweep, liveness, heartbeat, wake, worker_done, contract, template, playbook, coordinator, C-numbers, Orca, restart.
- Opened with `gh` (bodies read in part, by sections and keyword): open #716 (all 5 comments), #782, #787, #789, #790, #793, #795, #800, #806, #757, #766, #590, #770, #771, #767, #774, #725, #794, #810, #811, #801; closed #431, #444, #655 (keyword lines only); PRs #434, #539, #591, #693, #729. #707 and #809 not opened (git log and list title only).
- Plan files read: R38 (`requirements.md:64`), `design-comparison-655.md:3`, SPEC rows 84, 226, 228, 242, 243, 305, 677; DEC rows 327, 416, 502, 579, 591, 603; D15:96-98; D11 VERDICT:43; D08 VERDICT:63. UNVERIFIED: the text of the "four typing rules"; whether Orca delivers mailbox follow-ups in time.
