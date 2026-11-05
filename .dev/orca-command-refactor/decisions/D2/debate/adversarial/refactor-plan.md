# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (`variant-1-original.md`, option (a): keep the Ruling rule; the person gives the Ruling in their own session). Selected in `base-selection.md` by tiebreaker (Level 1 debate wins 7 to 6, Level 2 Correctness 5/5 to 3/5; combined scores V3 0.8406, V1 0.7996, margin 0.041 < 0.05).
- Incorporating strengths from: Variant 3 (option (c), hand-written Ruling plus resume Task) and Variant 2 (option (b), only its contract fields and its case against relaying).
- Target position (the debate's unanimous Round 2 result, `debate-transcript.md` "Advocates' final recommendations"): **(a)+(c)**. Keep the Ruling rule word for word; (a) is the default and the only route for a `dispute`; (c) is an optional second route back into Orca; (b) is rejected for now.
- Planned changes: 13.
- Risk level: Medium overall. The merge adds rules that the debate did not test: the fixes for the 6 HIGH invariants come from the fault-finder's "fix shape" notes (`invariant-probe.md`), not from a debate round.
- Fixed constraints applied (user decisions made after the debate started; not debated, applied as given by the team lead on 2026-11-02):
  - K1. Every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/` (`changes/CR-01-feature-worktree-hierarchy.md:41`). This supersedes the `.dev/worktrees/` disposable worktree in the spec's live check (`SPEC:235`).
  - K2. SuperClaude upstream is never pushed to or interacted with (`CR-01:45`). D2 adds no outward action, so this only rules out Orca issue/PR linking in any D2 step.
  - K3. Merged PR #343 (commit `80f934de`): only blocking findings fail a review, minors are notes, review loops cap at 2 fix cycles then escalate to the user, and `/sc:implement` dropped its second A2 in-place repair. Re-read in this run: the source refs say "A2 with its one repair" (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:267`) and "A2 gets one repair at most" (`.../refs/retry.md:142`). The installed copy under `~/.claude/skills/sc-implement-protocol/refs/` still has the pre-#343 text in 6 places (`qa.md:267`, `ledger.md:143`, `retry.md:141-142,147-149,189,193`: "A2 with repairs 1 and 2", "second A2 repair"); every line D2 cites is byte-identical in both copies and at the same line number. Citations below use the source copy.
  - K4. Proposed change CR-01: one feature worktree; `/sc:implement` gets its own child worktree when another worker writes outside `.dev/` in the same worktree (trigger T2, `CR-01:18`); CR-01 is still "Status: PROPOSED" (`CR-01:3`); merge-back and removal belong to the git owner after the child's result is admitted (`CR-01:23`).

## Planned Changes

Citation key as in `diff-analysis.md` (`SPEC:N`, `QA:N`, `LEDGER:N`, `RETRY:N`, `SKILL:N`, `CAPS:N`, `IMPL:N`) plus `MW:N` = `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:N` and `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`. `V<n> L<k>` = line k of variant n.

### Change 1: Restate the position as (a)+(c) (from all three Round 2 recommendations)
- **Source**: r2-variant-1 "Overall recommendation"; r2-variant-2 "Overall recommendation"; r2-variant-3 "Overall recommendation" (`debate-transcript.md:390,469,552`).
- **Target**: Base, title and Position paragraph (V1 L1, L3) (restructure).
- **Rationale**: Unanimous Round 2 result; S-005 (V3 wins, 95%): (c) is a superset of (a), so the real choice was (a), (a)+(c) or (b). X-002 (V3, 98%): the rule does not force the plan out of Orca; V1 conceded (r2-variant-1 response 2).
- **Integration point**: Title becomes "D2 merged position: keep the Ruling rule; (a) by default, (c) as the way back into Orca; reject (b)". Position keeps V1's halt behaviour sentence and adds the (c) branch and the (b) rejection.
- **Risk**: Medium — changes the headline claim of the base.

### Change 2: Citation key, anchor drift note and PR #343 note (base weakness S-003 kept; K3 added)
- **Source**: V1 L5-L7 (base); `diff-analysis.md` citation key; K3.
- **Target**: Base, citation key and drift paragraph (V1 L5-L7) (replace).
- **Rationale**: S-003 (V1, 95%): the spec's `qa.md:232,238` (`SPEC:334`), `qa.md:238` (`SPEC:67`, `SPEC:319`) and `qa.md:231-238` (`SPEC:132`) now land on the Family probe section; the rule is at `QA:247-249` and `QA:254-256`. The merged paper also uses `LEDGER`, `RETRY`, `SKILL`, `IMPL`, `CAPS`, `MW`, `CR-01`, which V1's key lacks.
- **Integration point**: Extend the key; keep the drift paragraph; add one sentence on the installed copy lagging PR #343 with no effect on cited lines.
- **Risk**: Low — reference text only.

### Change 3: Add route (c), corrected (from Variant 3)
- **Source**: V3 L3 (Position) and L7-L10 ("Why this works with no protocol change").
- **Target**: Base, new section "Route (c): hand-written Ruling, then a resume Task" after Safety (insert).
- **Rationale**: X-002 (V3, 98%); C-005 (V3, 95%): row R precedes P and H and completes the task with no review (`LEDGER:149-154`). Corrections required by the diff and debate: the record kind is current grammar, not only backward compatibility ("Operator `Ruling:` lines may appear between any two records", `LEDGER:110`), but no line sanctions it as a route, so the spec needs one sentence (SC-2 OVERSTATED; r2-variant-3 response 3); a malformed last line stops resume at `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`), not "ignored" (SC-4 WRONG); a well-formed but ineligible line is ignored (`RETRY:500`) and resume then falls to row H (`LEDGER:141`, `LEDGER:156`).
- **Integration point**: New section stating the mechanism (line format `LEDGER:65,71`; eligibility both clauses `RETRY:498`; row R `LEDGER:154`; implicit `--resume` `IMPL:57`) with the two corrections inline.
- **Risk**: Medium — adds a route; safe only with Changes 4-8.

### Change 4: Coordinator rules after an `/sc:implement` stop (from V1 R2 new evidence 1, V2 R2, V3 R2; closes INV-002, INV-005, INV-016 residue, INV-023)
- **Source**: r2-variant-1 new evidence 1 and recommendation (1); r2-variant-2 recommendation (contract fields); r2-variant-3 response 9 and recommendation (1); `invariant-probe.md` INV-002, INV-005, INV-023 fix shapes.
- **Target**: Base, new section "What the coordinator does after the halt" (insert).
- **Rationale**: A plain WC-6 retry (`SPEC:84`) of a Ruling-halted plan resumes implicitly (`IMPL:57`) into row P or H, which runs an operator review by automation (`LEDGER:155-156`), against `QA:283` ("user-initiated after a halt, never started by automation"). A-008 (equal, all three need the same rule, `CAPS:63`). INV-005: WC-4 carries no STOP code (`SPEC:68`), so the coordinator cannot tell `E-HALT-QA` from `E-RESUME-NEEDED` (re-run, "do not write a Ruling", `RETRY:494`) or `E-ARCHIVE-BLOCKED` (`SKILL:42`). INV-002: a freeze kept only in the coordinator's memory is lost on restart.
- **Integration point**: Rules (debated: (iii) the show-and-freeze rule, and the contract carrying the ledger path and worktree; this plan's, not debated: (i)'s STOP-code field, (ii), (iv), (v)): (i) the implement contract names the STOP code in `reason` for every non-success outcome, `blocked` included (a WC-4 edit: today `reason` is written only "when failed", `SPEC:68`), and for `blocked` also lists the halted task id(s), the halt reason (`none` after `E-NO-RULING`), the absolute ledger path and the worktree (absolute path, used as the Orca `path:` selector); (ii) the coordinator may re-run without the person only after `E-RESUME-NEEDED`, only as "re-run the same command" in the same worktree, and only when the ledger freeze in (iv) does not hold (otherwise resume would land on row P or H, `LEDGER:155-156`); (iii) every other implement stop is shown to the person with the contract's fields and the full halt text, and no Task for that plan is dispatched until the freeze lifts; (iv) the freeze is derived from durable state, so a coordinator restart or a missing contract cannot lose it: the plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP other than `E-RESUME-NEEDED`, **or** the ledger's first non-complete task has `halt` or `blocked` as its last record with no eligible Ruling after it (`LEDGER:123-129`, `LEDGER:141`); (v) the freeze lifts only when both hold: the ledger condition for the chosen route (Change 5 for (c), Change 8 for (a)) **and** the person's explicit hand-back ("Ruling written" for (c), "session ended" for (a)), which the coordinator records in its run notes before dispatching anything; for a stop with no halted task (for example `E-ARCHIVE-BLOCKED`, `E-LEDGER-CORRUPT`, `E-PLAN-CHANGED`, `SKILL:36-42`) it lifts only on the person's recorded instruction.
- **Risk**: Medium — new coordinator behaviour; needs WORKER-CONTRACT.md text and an AC.

### Change 5: The read-only pre-dispatch check for route (c) (from V3 R2 item 3, V1 R2 item 4, V2 R2; closes INV-006, INV-007, INV-011, INV-012, INV-014, INV-022; replaces V3's porcelain guard per INV-020)
- **Source**: r2-variant-3 recommendation item 3; r2-variant-1 new evidence 2; r2-variant-2 recommendation ("test both clauses"); `invariant-probe.md` fix shapes.
- **Target**: Base, new section "The check before a resume Task" (insert, after Change 4's section).
- **Rationale**: r2-variant-3 response 9: the check is load-bearing, because an ineligible line sends resume to row H and an automated review (`LEDGER:141,156`, `QA:283`). INV-014: `.+` accepts placeholders and whitespace (`LEDGER:71`), and row R then completes with no review. INV-022: row R records the latest `blocked` verdict "unchanged" (`LEDGER:82,154`), which describes attempt k, not the tree, after a `no-evidence` halt (`RETRY:229`) or a resume-time revert-guard halt (`RETRY:492`); the halt line itself does not say whether it was written on a resume (`LEDGER:93`); a resume re-check through row O writes `no-snapshot` or `head-moved` (`RETRY:44`) and the revert guards through row X can also write `no-evidence` (`RETRY:456`), so all three are routed to (a). INV-007: test every `halt` after the latest `start`, not only the latest. INV-012: check every line appended after the anchor record, not only the last line.
- **Integration point**: This check applies to route (c) only; the hand-back after (a) has its own check (Change 8). Debated: a read-only check of format, both eligibility clauses and the `dispute` exclusion (r2-variant-1 item 4, r2-variant-2, r2-variant-3 item 3). This plan's, not debated: conditions (2)-(3)'s anchor, count, newline and placeholder rules, (5)'s extra reasons, (6) and (7). The coordinator reads the ledger and the worktree (never edits either) and dispatches the resume Task only if all hold: (1) the plan is frozen per Change 4, the halted worker has settled (`SPEC:70`) and the person has said "Ruling written"; (2) anchor = the later of the halted task's latest `halt` and latest `blocked` record; after it, the only new lines are exactly one Ruling line per halted task named in the contract, each with that task's id, each ending in `\n` with no `\r`, each matching `LEDGER:71`; (3) none of the three fields is blank, whitespace-only, punctuation-only or an angle-bracket placeholder (any field matching `^\s*<[^>]*>\s*$`, which covers `<what>`, `<why>`, `<cost-if-wrong>` and `QA:259`'s `<what, including user confirmation provenance>`), and the line has exactly two ` — ` separators; (4) it is eligible for that task under clause (a) or (b) of `RETRY:498`; (5) no `halt` after the task's latest `start` has `reason=dispute`, and the latest `halt` reason is not `no-evidence`, `no-snapshot` or `head-moved`; (6) the tree has not drifted (Change 6 ii); (7) the resume brief has no `--force` token (`SKILL:50`). On any failure: tell the person which condition failed, route them to (a), never edit the ledger.
- **Risk**: Medium — the largest new rule set; each condition is mechanical (regex, `git rev-parse`, `git diff --quiet`).

### Change 6: Placement and the frozen worktree (closes INV-001, INV-018, INV-019; replaces V3's porcelain guard, INV-020; applies K1 and K4)
- **Source**: `invariant-probe.md` INV-001, INV-018, INV-019, INV-020; r2-variant-3 new evidence 1; `CR-01:16-23,41`.
- **Target**: Base, new section "Where the resume runs" (insert).
- **Rationale**: A legacy ledger is never `git add`ed (`LEDGER:3`), so a resume Task in another worktree has no ledger and starts from T1 (INV-018). Another writer can change the halted task's files during the person's wait, and row R accepts "the tree as it stands" with no review (`RETRY:500`, `LEDGER:154`) (INV-001). V3's `git status --porcelain` guard always refuses on a managed ledger, because the person's own appended line changes the porcelain output (`LEDGER:3`: managed ledgers are under `.dev/tasks/`, always staged) (INV-020). CR-01 already gives `/sc:implement` its own child worktree when others write alongside it (T2).
- **Integration point** (this plan's, not debated, except V3's idea of a drift check, r2-variant-3 new evidence 1): (i) The halted Task's worktree is frozen with the plan and lifts with it (Change 4 v): no Task that writes outside its own report directory is dispatched into it, and no git command that changes HEAD, the index or the working tree is run there by the coordinator or the git owner (commit, merge, rebase, reset, checkout, stash, clean, worktree removal); a child worktree holding a halted ledger is neither admitted nor discarded under CR-01 until then. (ii) Drift check, from durable records only: `HEAD` must equal `<retries>/T<id>/q0-head` (written at Q0 for every tree-snapshot task, `SKILL:114`; the same test the ladder uses, `RETRY:41`), and the paths in the `files=` field of the task's latest `blocked` line must be unchanged against the tree that verdict's review graded (pinned as `r<k>-<j>`, `QA:178-179`, kept until `complete`, `RETRY:433`), tested read-only with `GIT_OPTIONAL_LOCKS=0 git diff --quiet <tree> -- <paths>`. A missing `q0-head` (a `nogit` or HEAD-fallback start, `QA:202`) or no recorded tree routes the person to (a). (iii) The resume Task starts in that exact worktree by Orca selector (`worker-start --worktree path:<absolute worktree path>`), never `new-child` and never a new worktree; this takes precedence over CR-01 T2 for the resume Task, and if a writer started before the halt is still running there, the coordinator waits for it to settle first. (iv) Under (a), the person runs `/sc:implement` from that same worktree with the same absolute plan path (the legacy slug hashes the absolute path, `SKILL:64`). (v) Worktrees are Orca-created at Orca's default paths (K1). (vi) If the implement Task ran in the shared feature worktree, that whole worktree stays frozen for the person's wait; to avoid that, implement Tasks should run in their own child worktree, which needs CR-01's T2 widened to every `/sc:implement` worker (a CR-01 decision, flagged in the recommendation, not made here).
- **Risk**: Medium — freezes one worktree for the length of the person's wait. Residual accepted risk: the person's own edits to the tree before they write the line are not prevented; the drift check catches them only for the `files=` paths.

### Change 7: Implement worker briefs use a file or managed source, never an inline prompt (closes INV-017)
- **Source**: `invariant-probe.md` INV-017.
- **Target**: Base, section "Where the resume runs" (append one rule).
- **Rationale**: For an inline prompt the slug hashes the full prompt (`SKILL:61`), and every token after the first non-option token is source or prompt text (`SKILL:52`). Wave 0 knows no `--unattended` or `--report-dir` today (`SKILL:50`), and the spec's own AC-4.1 command puts them after the plan path (`SPEC:274`); WC-6 gives each retry a new report directory (`SPEC:70`). So unless Wave 0 parses those flags, even a file source can resolve to the wrong source or slug, or stop at `E-NO-SOURCE` / `E-SOURCE-MISSING`, and the resume Task never reads the Ruling. File sources hash the absolute path (`SKILL:64`); managed packages use `<package>/progress.md` (`SKILL:64`).
- **Integration point** (this plan's, not debated): (i) P4's change to `/sc:implement` must add `--unattended` and `--report-dir <dir>` to Wave 0's known options, so they are never part of source resolution or the slug hash (this is a required P4 change the implement row does not list today: "none on the happy path", `SPEC:132`); (ii) implement briefs put every option before the source; (iii) implement briefs pass a plan file path or a managed package path, never an inline prompt, so a person retyping under (a) gives the same slug; (iv) AC-4.1 asserts the resume Task's contract names the same absolute ledger path as the halted Task's contract.
- **Risk**: Low — one Wave 0 option addition P4 needs anyway; briefs narrowed; a person's standalone use is unchanged.

### Change 8: Hand-back after route (a) and single writer in both directions (closes INV-004; keeps INV-003)
- **Source**: `invariant-probe.md` INV-003, INV-004; r2-variant-1 responses 2 and 6; V3 L14.
- **Target**: Base, section "How a person works day to day" (append).
- **Rationale**: The ledger has no lock (`LEDGER:145`). Consensus item (ii) covers worker→person only. After (a) the person's session records the Ruling, appends `complete` and goes on to T{i+1} (`QA:248`, "Yes"), so the (c) check alone has no defined hand-back.
- **Integration point** (debated: (i), r2-variant-1 recommendation (2); this plan's, not debated: (ii)-(iv)): (i) The person writes or resumes only after the worker has settled (`SPEC:70`). (ii) Under (a) the person either lets their session finish the plan (the coordinator then treats the plan as done by the person and dispatches nothing for it), or ends that session after the Ruling is recorded and tells the coordinator "session ended"; a ledger condition alone never lifts the freeze, because the person's session writes the Ruling and `complete` and then continues to T{i+1} (`QA:248`, `QA:256`). (iii) Hand-back check after (a), read-only: the person's "session ended" is recorded in the coordinator's run notes; the ledger's last line parses (`LEDGER:123`); the halted task's latest status is `complete`; the drift baseline is re-recorded at that moment, and only then may the coordinator dispatch a resume Task, which skips complete tasks (`LEDGER:153`). (iv) After telling the coordinator "Ruling written" or "session ended", the person makes no further ledger or tree edit in that worktree until the resume Task settles.
- **Risk**: Low — a stated precondition, like `LEDGER:145`; relies on the person's message, recorded durably.

### Change 9: Day-to-day text covers both routes and (c)'s weakness (from Variant 3)
- **Source**: V3 L19-L21; r2-variant-3 response 1 and new evidence 2.
- **Target**: Base, section "How a person works day to day" (V1 L17-L19) (replace).
- **Rationale**: C-003 (V1, 98%): only (a) gives the executor's own scoped explanation before acceptance (`QA:254`); V3 conceded. The coordinator shows the full halt text (`RETRY:490`: ledger path, task, verdict, missing citations, checkpoint shas, briefs). r2-variant-3 new evidence 2: a coordinator-drafted line turns (c) into (b).
- **Integration point**: Describe: the coordinator shows the halt; the person picks (a) or (c); under (c) the person types all three fields themselves from the halt text; the coordinator shows the format only, never pre-filled words. State the weakness plainly and that (a) is one choice away.
- **Risk**: Low.

### Change 10: Safety additions (from Variant 3 Safety)
- **Source**: V3 L13-L14.
- **Target**: Base, section Safety (V1 L9-L11) (append).
- **Rationale**: C-009 (equal V2, V3): the no-lock precondition must be stated (`LEDGER:145`). r2-variant-3 new evidence 2 and A-010 (equal V1, V3, 70%): eligibility is positional only (`RETRY:498`), so "only the person types the line" is policy, not mechanism; INV-010 records this as an accepted residual risk.
- **Integration point**: Two bullets: a line written or drafted by the coordinator or any worker is "executor-invented approval" (`QA:249`); the residual risk that no record proves who typed a line is accepted, as it already is for every operator-written line today (`LEDGER:195`).
- **Risk**: Low.

### Change 11: Reliability adds V3's AC-4.1 extension, adjusted for K1 and INV-018
- **Source**: V3 L17.
- **Target**: Base, section Reliability (V1 L13-L15) (append).
- **Rationale**: S-006 and C-008 (V3, 95%). The live check's worktree must be Orca-created (K1, `CR-01:41`, superseding `SPEC:235`), and the resume Task must run in that same worktree before it is removed (INV-018).
- **Integration point**: AC-4.1 gains: after the halt, (1) a plain coordinator retry is not attempted (freeze); (2) a hand-written line with the halted task id is appended; (3) the pre-dispatch check passes; (4) the resume Task, started in the same Orca-created worktree, ends with that task `complete` carrying the unchanged non-compliant verdict (`QA:248`, `LEDGER:82`); (5) a second run with a skeleton line (`<what> — <why> — <cost-if-wrong>`) is refused by the check and dispatches nothing.
- **Risk**: Low.

### Change 12: Record (b) as rejected, with V2's own case against it
- **Source**: V2 L13-L14; r2-variant-2 recommendation and new evidence 1, 2, 4.
- **Target**: Base, new short section "Why not (b)" (insert before Implementation cost).
- **Rationale**: X-001, C-001, A-010 (V1/V3); V2 conceded every safety point (r2-variant-2 responses 1, 2, 5, 7, 10). New evidence: (b) cannot clarify "fine, go ahead" within one ask per Task (`QA:254`, `SPEC:67`); a late answer collapses into (c) with an agent-written line; a dispute needs the advice file (`RETRY:107`, `QA:281`).
- **Integration point**: Short section; record (b) only as a possible later opt-in that the user explicitly accepts, excluding `reason=dispute`.
- **Risk**: Low.

### Change 13: Implementation cost and frequency, updated for K3
- **Source**: V1 L15, L21-L22; V3 L23-L24; r2-variant-3 response 13; K3.
- **Target**: Base, sections Reliability bullet 2 (V1 L15) and Implementation cost (V1 L21-L22) (replace).
- **Rationale**: C-007 (V1, 98%) holds for the rule itself; (c) and the coordinator rules cost spec text only. C-011 (V1, 98%): halts need a confirmed blocker (`QA:280`, `QA:274`, `QA:288`). K3 does not weaken this: minors still never halt (`QA:274`), and the dropped second A2 repair (`RETRY:142`) only changes which in-place fixes run before the adviser route; whether halts become more frequent is UNVERIFIED (no run data).
- **Integration point**: Cost list: zero edits to `qa.md`, `ledger.md`, `retry.md`; spec edits listed in the merged paper; one new AC step.
- **Risk**: Low.

## Invariant coverage (every HIGH UNADDRESSED INV-NNN)

The debate's convergence status is BLOCKED_BY_INVARIANTS (`debate-transcript.md`, Convergence Assessment). Each HIGH item has a planned change below. The fixes are this plan's, derived from the fault-finder's fix shapes and revised after the independent review (Review Status), and were not argued in a debate round. Two residual risks remain and are accepted explicitly: (R1) the person's own edits to the halted worktree before they write the line are not prevented, and the drift check sees them only for the `files=` paths (INV-001); (R2) a well-formed line can still name the wrong scope, which no format check can catch (INV-014; r2-variant-3 response 11), with (a) one choice away.

| INV | Severity | Disposition | Change | How it is closed |
|-----|----------|-------------|--------|------------------|
| INV-001 | HIGH | Planned change, residual R1 | 6, 5 (6) | Frozen worktree (no new writer; no git command that changes HEAD, index or tree) plus a durable drift check: `HEAD` against `q0-head` and the `files=` paths against the graded tree; missing records route to (a) |
| INV-004 | HIGH | Planned change | 8, 4 (v) | Freeze lifts only on the ledger condition plus the person's recorded "session ended"; separate hand-back check after (a); no person edit after hand-back |
| INV-014 | HIGH | Planned change, residual R2 | 5 (3) | Check refuses blank, whitespace-only, punctuation-only and angle-bracket placeholder fields and extra ` — ` separators; coordinator never pre-fills words (Change 9) |
| INV-017 | HIGH | Planned change | 7 | Wave 0 parses `--unattended` and `--report-dir` as options (P4); options before the source; file or managed source only; AC-4.1 asserts the same ledger path |
| INV-018 | HIGH | Planned change | 6 (iii), 11 | Resume Task started in the halted worktree by Orca selector; AC-4.1 runs it there before removal |
| INV-022 | HIGH | Planned change | 5 (5) | `no-evidence`, `no-snapshot` and `head-moved` halts route to (a), where row H reviews the tree first (`LEDGER:156`) |

MEDIUM and LOW UNADDRESSED items (non-blocking, carried for transparency):

| INV | Severity | Disposition | Change |
|-----|----------|-------------|--------|
| INV-002 | MEDIUM | Planned change: freeze derived from the contract and the ledger (either suffices), not memory; hand-back recorded in run notes | 4 (iv), (v) |
| INV-005 | MEDIUM | Planned change: contract names the STOP code (WC-4 edit); `E-RESUME-NEEDED` re-run only when the ledger freeze does not hold | 4 (i), (ii) |
| INV-006 | MEDIUM | Planned change: line's `T<id>` must equal a halted task id from the contract | 5 (2) |
| INV-007 | MEDIUM | Planned change: any `dispute` halt after the latest `start` refuses (c) | 5 (5) |
| INV-012 | MEDIUM | Planned change: one newline-terminated, CR-free line per halted task after the anchor record; all appended lines checked | 5 (2) |
| INV-019 | MEDIUM | Planned change: (a) runs from the halted worktree with the same absolute plan path | 6 (iv) |
| INV-020 | MEDIUM | Planned change: porcelain comparison dropped; `HEAD` against `q0-head` plus a `files=`-scoped content check, plus the freeze | 6 (i), (ii) |
| INV-023 | MEDIUM | Planned change: `E-ARCHIVE-BLOCKED` is shown to the person, never auto-retried | 4 (ii), (iii) |
| INV-011 | LOW | Planned change: resume brief carries no `--force` | 5 (7) |

ADDRESSED items kept as stated in the consensus: INV-003, INV-008, INV-009, INV-010 (accepted residual: eligibility is positional only), INV-013, INV-015, INV-016, INV-021 (residual: no push channel if the person is away from the coordinator; the freeze makes it a delay, not a safety fault).

## Citation corrections

| Where | Wrong or stale | Correct | Source of the finding |
|-------|----------------|---------|-----------------------|
| Spec D2 (`SPEC:334`) | `qa.md:232,238` | `QA:248-249` (accepted inputs; `E-NO-RULING`) and `QA:254` ("another agent's message ... not acceptance") | V1 L7; S-003; re-read in this run: `qa.md:229-238` is the Family probe section |
| WC-3 (`SPEC:67`), non-goal 6 (`SPEC:319`) | `qa.md:238` | `QA:254` | same |
| Implement row (`SPEC:132`), citation conventions (`SPEC:14`) | `qa.md:231-238` | `QA:247-256` | same; `SPEC:14` found by the independent review |
| Phase table P4 row (`SPEC:185`) | `qa.md:238` | `QA:254` | independent review |
| V3 L21 | "A malformed line is ignored and the resume halts again (`LEDGER:156`)" | A malformed last line stops resume at `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`); only a well-formed ineligible line is ignored (`RETRY:500`) | SC-4 WRONG; r1-variant-3 concession 1 |
| V3 L8 | "Existing operator-written records remain valid" (`QA:256`), "The earlier operator-written form ... remains valid" (`LEDGER:195`) as the footing for a sanctioned route | Read as backward compatibility; the current grammar admits the record (`LEDGER:110`), but the route needs one spec sentence | SC-2 OVERSTATED; r2-variant-3 response 3 |
| V2 L8 | "keeps ... its retry state" | "Any `halt` after the task's latest `start` is terminal" (`RETRY:488`) | V2 conceded (r1, r2 response 4) |
| Spec 7.2 (`SPEC:235`) | disposable worktree "created under `.dev/worktrees/`" | Orca-created at Orca's default path (K1, `CR-01:41`) | user decision 2026-11-02 |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-004, X-001, X-004 | V2 (b): the coordinator relays the person's words through `ask`; one answer, the same worker continues | V2 withdrew (b) (r2-variant-2 "Overall recommendation"). The reply is the coordinator's message (`CAPS:62`), which `QA:254` excludes by name; a paraphrase is undetectable and AC-4.1 cannot test relay fidelity (C-008, conceded r2-variant-2 response 5). C-004 (V2, 95%) is conceded as real but bought with an edit to the one human checkpoint. Recorded only as a later opt-in (Change 12). |
| A-009 | V2 (b) needs no access to the worker's files | Real advantage (V2, 95%), not adopted because it comes only with (b). Mitigated by the contract carrying the absolute ledger path and worktree (Change 4 i). Remote workers stay out of scope (`SPEC:322`). |
| C-009 | V2 (b) is single-writer by construction | Matched without (b) by the stated precondition (`LEDGER:145`, `SPEC:70`) in both directions (Change 8). |
| C-010, C-002 | V3: the person hand-types the line, with no agent formatting it | Not replacing (a): (a) keeps the executor-formatted line (`QA:256`; C-002 V1 98%, C-010 equal V1/V2). (c) is added as an option, with its typing risk reduced by the check (Change 5), not removed (r2-variant-3 response 11). |
| C-003 | V3 (c) as the default route | (a) stays the default because only it gives the executor's own scoped explanation before acceptance (`QA:254`; V1 98%, conceded by V2 and V3). |
| A-011 | V3 R1: `dispute` halts inside (c) | (a) is the only route for a dispute (`QA:281`, `RETRY:107`); V3 conceded (r2-variant-3 response 10). |
| INV-020 | V3 R2: compare `HEAD` and `git status --porcelain`; no other writer in the worktree | The porcelain comparison is dropped: it always refuses on managed ledgers (`LEDGER:3`) and changes with any parallel worker (`CAPS:115`). Replaced by a durable `HEAD` check against `q0-head`, a `files=`-scoped content check and a scoped freeze (Change 6). |
| C-005 | V1: (a)'s row-H review as the only resume | Kept for (a) as the protocol's designed step (`QA:283`); row R is added for (c) only, with the halt reasons whose tree is not the reviewed one routed back to (a) (Change 5). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Headline misstates the consensus | Revert to V1 L1, L3 and drop Changes 3-11 together |
| 2 | Low | A wrong anchor in the paper | Revert to V1 L5-L7 |
| 3 | Medium | (c) described without its guards reads as safe on its own | Remove the section; (a) remains complete |
| 4 | Medium | Coordinator retries a halted plan and starts an automated review (`QA:283`) | None needed for safety: without Change 4 every option is unsafe (V1 R2 new evidence 1); fix the wording rather than remove it |
| 5 | Medium | A malformed, skeleton, wrong-task or wrong-kind line becomes a no-review Ruling | Remove (c) (Change 3) together with Change 5 |
| 6 | Medium | Resume in the wrong worktree, or a Ruling accepts a tree changed by another writer | Remove (c); under (a) only the placement rule (iv) is needed |
| 7 | Low | Inline-prompt plans cannot be run as implement workers | Drop the constraint once P4 strips worker flags before hashing (`SKILL:61`) |
| 8 | Low | Two writers on one ledger after (a) | Revert to "(a) finishes the plan in the person's session" |
| 9 | Low | Person misled about (c)'s weaker explanation | Revert to V1 L17-L19 |
| 10 | Low | None beyond wording | Remove the two bullets |
| 11 | Low | AC-4.1 misses the return path | Revert to the current AC-4.1 (`SPEC:274`) |
| 12 | Low | None beyond wording | Remove the section |
| 13 | Low | Cost understated | Revert to V1 L21-L22 |

## Review Status
- [x] Auto-approved (default; run is non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto, after an independent analytical review (Step 4 delegation: orchestrator drafts, analytical agent reviews)
- Drafted: 2026-11-02, about 17:58Z, on resume after the 16:28 UTC interruption, by the resuming orchestrator from the Step 1-3 artifacts as written
- Independent review: one fresh general-purpose agent, read-only, adversarial brief (agent `a3037093fa8b47a1f`). Verdict on the first draft: FAIL, 3 BLOCKING and 8 MINOR. It re-read more than 40 citations and found them correct apart from its item 9, and confirmed that no agreed debate addition was dropped. Every finding was checked against the protocol lines by the orchestrator before acting (`RETRY:41,231,433,456`; `QA:178-179,202`; `SKILL:114`; `SPEC:14,185`; `CR-01:3,18`), and all 11 were applied:
  - B1 (INV-004 not closed; freeze lifted on ledger state alone during the person's session): Change 4 (iv)-(v), Change 8 (ii)-(iv).
  - B2 (INV-001 open for uncommitted edits; HEAD held in memory): Change 6 (i), (ii), (vi) and residual R1.
  - B3 (INV-017 depends on an unstated Wave 0 parse rule): Change 7 (i)-(iv).
  - M4 placeholder breadth: Change 5 (3), residual R2. M5 anchor and CR: Change 5 (2). M6 freeze from the ledger, no-task stops: Change 4 (ii), (iv), (v). M7 WC-4 edit named: Change 4 (i). M8 precedence over CR-01 T2: Change 6 (iii). M9 citations: Overview K4, Change 5 rationale, Citation corrections. M10 debated vs undebated tags: Changes 4-8. M11 residuals listed: Invariant coverage.
  - Not re-reviewed after revision; the merge executor's post-merge validation and the final citation check of `RECOMMENDATION.md` are the remaining independent checks.
- Approval timestamp: 2026-11-02T18:13Z (last revision of this plan, before the merge executor ran)
