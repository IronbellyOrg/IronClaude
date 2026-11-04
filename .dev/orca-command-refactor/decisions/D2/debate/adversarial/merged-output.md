<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (option a: keep the Ruling rule; the person gives the Ruling in their own session) -->
<!-- Merge date: 2026-11-02T18:14:25Z -->

# D2 merged position: keep the Ruling rule; (a) by default, (c) as the way back into Orca; reject (b)

<!-- Source: Base (original, modified) — title and Position restated as (a)+(c) per Change #1 (unanimous Round 2 result; resolves X-002 and S-005) -->
Position: keep the `/sc:implement` Ruling rule word for word. When `/sc:implement` halts for a Ruling inside a worker (`E-HALT-QA` or `E-NO-RULING`), the worker writes the halt to its ledger and its contract as `blocked`, sends `worker_done --outcome failed`, and never asks the coordinator (`SPEC:335`; WC-3 at `SPEC:67`). The person then gives the Ruling by one of two routes:
- (a), the default and the only route for a `dispute` halt: the person runs `/sc:implement <plan>` in their own session, which resumes from the ledger. This is the spec's current recommendation (`SPEC:337`).
- (c), the way back into Orca: the person types the Ruling line into the ledger themselves; once the coordinator's read-only check passes, it starts a resume Task that finishes the plan unattended.
- (b), a Ruling relayed by the coordinator through Orca `ask` (`SPEC:336`), is rejected for now.

All three advocates recommended (a)+(c) in Round 2 (`debate-transcript.md:390,469,552`).

<!-- Source: Base (original, modified) — citation key extended and drift note widened per Change #2 (S-003 kept; K3 installed-copy note added) -->
Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `QA:N`, `LEDGER:N`, `RETRY:N`, `MW:N` = `src/superclaude/skills/sc-implement-protocol/refs/{qa,ledger,retry,managed-workspace}.md:N`; `SKILL:N` = `src/superclaude/skills/sc-implement-protocol/SKILL.md:N`; `IMPL:N` = `src/superclaude/commands/implement.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`. Bare `debate-transcript.md:N` and `invariant-probe.md` refer to those files in this debate directory.

Citation drift found while writing: the spec cites the Ruling rule as `qa.md:232,238` (`SPEC:334`), `qa.md:238` (WC-3 at `SPEC:67`, the P4 phase row at `SPEC:185`, non-goal 6 at `SPEC:319`) and `qa.md:231-238` (the implement row at `SPEC:132`, the citation note at `SPEC:14`). On this branch those lines are the Family probe section; the rule is now at `QA:254` ("Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance") and the Halt table rows at `QA:247-249`; the whole Ruling block is `QA:247-256`. The file last changed in commit 80f934de (PR #343). The rule's content is unchanged; only the line moved.

The installed copy under `~/.claude/skills/sc-implement-protocol/refs/` still has the pre-#343 text in a few places (for example "A2 with repairs 1 and 2" at its `qa.md:267`). Apart from `QA:267` and `RETRY:142`, which this paper cites only to show that change (Fixed constraints, K3), every line cited here is byte-identical in both copies and at the same line number. Citations use the source copy.

## Fixed constraints
<!-- Source: refactor-plan.md, Overview, fixed constraints K1-K4 (user decisions applied as given on 2026-11-02; required in the paper by the merge brief) -->
User decisions made after the debate started. They were not debated; they are applied as given.
- K1. Every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/` (`CR-01:41`). This supersedes the `.dev/worktrees/` disposable worktree in the spec's live check (`SPEC:235`).
- K2. SuperClaude upstream is never pushed to or interacted with (`CR-01:45`). D2 adds no outward action, so this only rules out Orca issue or PR linking in any D2 step.
- K3. Merged PR #343 (commit `80f934de`): only blocking findings fail a review, minors are notes, review loops cap at 2 fix cycles and then escalate to the user, and `/sc:implement` dropped its second A2 in-place repair ("A2 with its one repair", `QA:267`; "A2 gets one repair at most", `RETRY:142`).
- K4. Proposed change CR-01, still "Status: PROPOSED" (`CR-01:3`): one feature worktree; `/sc:implement` gets its own child worktree when another worker writes outside `.dev/` in the same worktree (trigger T2, `CR-01:18`); merge-back and removal belong to the git owner after the child's result is admitted (`CR-01:23`).

## Safety
<!-- Source: Base (original) -->
- The rule exists to stop an agent approving its own or another agent's work: "another agent's message ... not acceptance" (`QA:254`); "executor-invented approval" is a STOP (`QA:249`). An Orca coordinator is another agent (`SPEC:334`). Keeping the rule keeps the one human checkpoint the protocol has.
- A Ruling accepts a deliverable that failed its acceptance criteria with a confirmed blocker: `E-HALT-QA` is "reachable only after an attempt failed on a confirmed blocker that a repair could not close" (`QA:280`). That is exactly the decision a person should make directly.

<!-- Source: Variant 3, Safety (L13) and diff point A-010 — merged per Change #10 -->
- A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval" (`QA:249`), and the spec must say so. Under (c) only the person types the line.
- Eligibility is positional only (`RETRY:498`): no ledger record proves who typed a line, so "only the person types the line" is policy, not mechanism. This residual risk is accepted, as it already is today for every operator-written line (`LEDGER:195`).

## Route (c): hand-written Ruling, then a resume Task
<!-- Source: Variant 3, Position (L3) and "Why this works with no protocol change" (L7-L10) — merged per Change #3, corrected for spot-checks SC-2 (OVERSTATED) and SC-4 (WRONG) -->
- The line: after the halt, the person types the existing three-field Ruling line, `T<id>: Ruling: <what> — <why> — <cost-if-wrong>` (`LEDGER:65`), which must match `^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$` (`LEDGER:71`), em dashes included.
- The current grammar admits it: "Operator `Ruling:` lines may appear between any two records" (`LEDGER:110`). No line sanctions a newly hand-written line as a route ("remain valid" at `QA:256` and `LEDGER:195` reads as backward compatibility), so the spec needs one sentence that makes it one.
- Eligibility has two clauses (`RETRY:498`): (a) a `halt` follows the task's latest `blocked` line, the Ruling comes after that `halt`, and no verdict line lies between; or (b) the task has no `retry` and no `halt` record, the Ruling follows its latest `blocked` line, and no verdict line lies between.
- Resume consumes it with no review: row R, "An eligible Ruling with no `complete` after it", appends the post-ruling `complete` with the latest `blocked` verdict unchanged (`LEDGER:154`), and it is checked before rows P and H (`LEDGER:149-156`). `--resume` is implicit when a ledger matches (`IMPL:57`), so the resume Task's command line is the same, with a fresh report directory (WC-6, `SPEC:70`).
- A malformed line is not ignored: it is the ledger's last line, so resume stops at `E-LEDGER-CORRUPT` (`LEDGER:123`, `SKILL:36`), and recovery needs a hand edit of the ledger.
- A well-formed but ineligible line is ignored (`RETRY:500`), and resume then falls to row H (`LEDGER:141`, `LEDGER:156`), an operator review that automation must never start (`QA:283`). So (c) is safe only with the coordinator rules, the check and the placement rules in the next three sections.

## What the coordinator does after the halt
<!-- Source: Variant 1, Variant 2 and Variant 3 Round 2 recommendations (show-and-freeze; contract carries ledger path and worktree) plus invariant-probe.md fix shapes for INV-002, INV-005, INV-023 — merged per Change #4 -->
Why rules are needed, whichever route the person picks:
- A plain WC-6 retry (`SPEC:84`) of a Ruling-halted plan resumes implicitly (`IMPL:57`) into row P or H, which runs an operator review by automation (`LEDGER:155-156`). That breaks `QA:283`: operator review is "user-initiated after a halt, never started by automation".
- The contract does not say which STOP fired: `reason` is written only "when failed" (`SPEC:68`). So the coordinator cannot tell `E-HALT-QA` from `E-RESUME-NEEDED` ("Re-run the same command; do not write a Ruling", `RETRY:494`) or from `E-ARCHIVE-BLOCKED` (`SKILL:42`).
- A freeze kept only in the coordinator's memory is lost when the coordinator restarts.

The rules:
- (i) The implement contract names the STOP code in `reason` for every non-success outcome, `blocked` included; this is a WC-4 edit (`SPEC:68`) (added in the merge; not debated). For `blocked` it also lists the halted task id(s), the halt reason (`none` after `E-NO-RULING`), the absolute ledger path and the worktree as an absolute path, used as the Orca `path:` selector (the ledger path and worktree were debated).
- (ii) The coordinator may re-run without the person only after `E-RESUME-NEEDED`, only as "re-run the same command" in the same worktree, and only when the ledger freeze in (iv) does not hold; otherwise the resume would land on row P or H (`LEDGER:155-156`) (added in the merge; not debated).
- (iii) Every other implement stop is shown to the person with the contract's fields and the full halt text, and no Task for that plan is dispatched until the freeze lifts (debated).
- (iv) The freeze comes from durable state, so a coordinator restart or a missing contract cannot lose it. The plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP other than `E-RESUME-NEEDED`, or when the ledger's first non-complete task has `halt` or `blocked` as its last record with no eligible Ruling after it (`LEDGER:123-129`, `LEDGER:141`) (added in the merge; not debated).
- (v) The freeze lifts only when both hold: the ledger condition for the chosen route (for (c), "The check before a resume Task"; for (a), the hand-back check in "How a person works day to day") and the person's explicit hand-back ("Ruling written" for (c), "session ended" for (a)), which the coordinator records in its run notes before dispatching anything. For a stop with no halted task (for example `E-ARCHIVE-BLOCKED`, `E-LEDGER-CORRUPT`, `E-PLAN-CHANGED`, `SKILL:36-42`), it lifts only on the person's recorded instruction (added in the merge; not debated).

## The check before a resume Task
<!-- Source: Variant 3 Round 2 recommendation item 3, Variant 1 Round 2 new evidence 2, Variant 2 Round 2 ("test both clauses") plus invariant-probe.md fix shapes for INV-006, INV-007, INV-011, INV-012, INV-014, INV-022 — merged per Change #5; replaces Variant 3's Round 2 porcelain guard (INV-020) -->
This check applies to route (c) only; the hand-back after (a) has its own check ("How a person works day to day"). It is load-bearing:
- An ineligible line sends resume to row H and an operator review by automation (`LEDGER:141`, `LEDGER:156`, `QA:283`).
- The regex's `.+` accepts placeholders and whitespace (`LEDGER:71`), and row R then completes the task with no review (`LEDGER:154`).
- Row R records the latest `blocked` verdict "unchanged" (`LEDGER:82`, `LEDGER:154`). After a `no-evidence` halt (`RETRY:229`) or a revert-guard halt on a resume (`RETRY:492`), that verdict describes attempt k, not the tree as it stands. The halt line does not say whether it was written on a resume (`LEDGER:93`); a resume re-check through row O writes `no-snapshot` or `head-moved` (`RETRY:44`), and the revert guards on row X can write `no-evidence` (`RETRY:456`). So all three reasons go to (a), where row H reviews the tree first (`LEDGER:156`).

The coordinator reads the ledger and the worktree, never edits either, and dispatches the resume Task only if all of these hold. Debated: a read-only check of the line format, both eligibility clauses and the `dispute` exclusion.
- (1) The plan is frozen ("What the coordinator does after the halt", rule iv), the halted worker has settled (`SPEC:70`), and the person has said "Ruling written".
- (2) Anchor = the later of the halted task's latest `halt` and latest `blocked` record. After it, the only new lines are exactly one Ruling line per halted task named in the contract, each with that task's id, each ending in `\n` with no `\r`, each matching `LEDGER:71` (the anchor, one-line count and newline rules: added in the merge; not debated).
- (3) None of the three fields is blank, whitespace-only, punctuation-only or an angle-bracket placeholder (any field matching `^\s*<[^>]*>\s*$`, which covers `<what>`, `<why>`, `<cost-if-wrong>` and `QA:259`'s `<what, including user confirmation provenance>`), and the line has exactly two ` — ` separators (added in the merge; not debated).
- (4) The line is eligible for that task under clause (a) or (b) of `RETRY:498`.
- (5) No `halt` after the task's latest `start` has `reason=dispute`, and the latest `halt` reason is not `no-evidence`, `no-snapshot` or `head-moved` (the `dispute` exclusion was debated; the three extra reasons are added in the merge; not debated).
- (6) The tree has not drifted (drift check in "Where the resume runs", rule ii) (added in the merge; not debated).
- (7) The resume brief has no `--force` token (`SKILL:50`) (added in the merge; not debated).

On any failure the coordinator tells the person which condition failed and routes them to (a). It never edits the ledger. Each condition is mechanical (a regex, `git rev-parse`, `git diff --quiet`).

## Where the resume runs
<!-- Source: invariant-probe.md fix shapes for INV-001, INV-018, INV-019, INV-020, Variant 3 Round 2 new evidence 1 (the drift-check idea only) and CR-01 (K1, K4) — merged per Change #6 -->
Why placement matters:
- A legacy ledger is never `git add`ed (`LEDGER:3`), so a resume Task in another worktree finds no ledger and starts again from T1.
- Another writer can change the halted task's files while the person decides, and row R accepts "the tree as it stands" with no review (`RETRY:500`, `LEDGER:154`).
- Variant 3's Round 2 guard (compare `git status --porcelain`) always refuses on a managed ledger: that ledger sits under `.dev/tasks/`, which is always staged (`LEDGER:3`), so the person's own appended line changes the porcelain output. It is dropped.
- CR-01 already gives `/sc:implement` its own child worktree when others write alongside it (T2, `CR-01:18`).

The rules (added in the merge; not debated, except the idea of a drift check, which is Variant 3's):
- (i) The halted Task's worktree is frozen with the plan and lifts with it ("What the coordinator does after the halt", rule v). No Task that writes outside its own report directory is dispatched into it. Neither the coordinator nor the git owner runs a git command there that changes HEAD, the index or the working tree (commit, merge, rebase, reset, checkout, stash, clean, worktree removal). A child worktree holding a halted ledger is neither admitted nor discarded under CR-01 until the freeze lifts.
- (ii) Drift check, from durable records only. `HEAD` must equal `<retries>/T<id>/q0-head`, which Q0 writes for every tree-snapshot task (`SKILL:114`); it is the same test the ladder uses (`RETRY:41`). The paths in the `files=` field of the task's latest `blocked` line must be unchanged against the tree that verdict's review graded, which is pinned as `r<k>-<j>` (`QA:178-179`) and kept until `complete` (`RETRY:433`). Test it read-only with `GIT_OPTIONAL_LOCKS=0 git diff --quiet <tree> -- <paths>`. A missing `q0-head` (a `nogit` or HEAD-fallback start, `QA:202`) or no recorded tree routes the person to (a).
- (iii) The resume Task starts in that exact worktree by Orca selector (`worker-start --worktree path:<absolute worktree path>`), never `new-child` and never a new worktree. This takes precedence over CR-01 T2 for the resume Task. If a writer started before the halt is still running there, the coordinator waits for it to settle first.
- (iv) Under (a), the person runs `/sc:implement` from that same worktree with the same absolute plan path, because the legacy slug hashes the absolute path (`SKILL:64`).
- (v) Worktrees are created by Orca at Orca's default paths (K1).
- (vi) If the implement Task ran in the shared feature worktree, that whole worktree stays frozen while the person decides. To avoid that, implement Tasks should run in their own child worktree, which needs CR-01's T2 widened to every `/sc:implement` worker. That is a CR-01 decision, flagged here, not made here.

<!-- Source: invariant-probe.md fix shape for INV-017 — merged per Change #7 -->
- Implement worker briefs (added in the merge; not debated). Why: for an inline prompt the slug hashes the full prompt (`SKILL:61`), and every token after the first non-option token is source or prompt text (`SKILL:52`). Wave 0 knows no `--unattended` or `--report-dir` today (`SKILL:50`), the spec's own AC-4.1 command puts them after the plan path (`SPEC:274`), and WC-6 gives each retry a new report directory (`SPEC:70`). So unless Wave 0 parses those flags, even a file source can resolve to the wrong source or slug, or stop at `E-NO-SOURCE` / `E-SOURCE-MISSING`, and the resume Task never reads the Ruling. File sources hash the absolute path; managed packages use `<package>/progress.md` (`SKILL:64`). The rules:
  - P4's change to `/sc:implement` adds `--unattended` and `--report-dir <dir>` to Wave 0's known options, so they are never part of source resolution or the slug hash. The implement row does not list this today ("none on the happy path", `SPEC:132`).
  - Implement briefs put every option before the source.
  - Implement briefs pass a plan file path or a managed package path, never an inline prompt, so a person retyping the command under (a) gets the same slug.
  - AC-4.1 asserts that the resume Task's contract names the same absolute ledger path as the halted Task's contract.

## Reliability
<!-- Source: Base (original, modified) — "No new mechanism" narrowed to the ledger side, because the merged paper adds coordinator rules (post-merge contradiction fix); implement.md path shortened to the IMPL key -->
- No new ledger mechanism for either route: the halt, the ledger, row R and resume already exist (`LEDGER:149-156`; `IMPL:57`). What the merge adds are coordinator rules ("What the coordinator does after the halt"). AC-4.1 checks the halt live (`SPEC:274`).

<!-- Source: Base (original, modified) — bullet 2 rewritten per Change #13 to cover K3 -->
- Halts are rare by design. Every minor and note finding is recorded and cleared with "no halt, no Ruling, no user prompt" (`QA:274`); "No other path may stop automation or prompt the user" (`QA:288`); and `E-HALT-QA` needs a confirmed blocker that a repair could not close (`QA:280`). PR #343 (K3) does not weaken this: minors still never halt (`QA:274`), and the dropped second A2 repair ("A2 gets one repair at most", `RETRY:142`) only changes which in-place fixes run before the adviser route. Whether halts become more frequent is UNVERIFIED (no run data).

<!-- Source: Variant 3, Reliability (L17) — merged per Change #11, adjusted for K1 and INV-018 -->
- AC-4.1 gains a return path. After the halt: (1) the coordinator does not attempt a plain retry (the freeze holds); (2) a hand-written line with the halted task id is appended; (3) the pre-dispatch check passes; (4) the resume Task, started in the same Orca-created worktree, ends with that task `complete`, carrying the unchanged non-compliant verdict (`QA:248`, `LEDGER:82`); (5) a second run with a skeleton line (`<what> — <why> — <cost-if-wrong>`) is refused by the check and dispatches nothing. The live check's worktree is created by Orca (K1, `CR-01:41`, superseding `SPEC:235`), and the resume Task runs in that same worktree before it is removed.

## How a person works day to day
<!-- Source: Variant 3, "How a person works day to day" (L19-L21) and Variant 3 Round 2 response 1 and new evidence 2 — replaces Base L17-L19 per Change #9 (C-003 kept: only (a) gives the executor's explanation) -->
- After a halt, the coordinator shows the person the contract's fields and the full halt text: ledger path, task, verdict, missing citations, checkpoint shas and briefs (`RETRY:490`, `QA:247`). The person picks (a) or (c).
- Under (a), the person resumes the run in their own session from the halted worktree. The executor explains the task id, unmet AC or finding, current outcome, proposed acceptance, reason and cost-if-wrong, then records the Ruling (`QA:254-256`). Only (a) gives the executor's own scoped explanation before acceptance (`QA:254`).
- Under (c), the person types all three fields themselves from the halt text, then tells the coordinator "Ruling written". The coordinator shows the line format only, never pre-filled words: a line drafted by the coordinator turns (c) into (b).
- Weakness of (c), stated plainly: a hand-written line skips the executor's scoped explanation (`QA:254`), and the person must write what, why and cost-if-wrong (`LEDGER:65`) from the halt text alone. (a) is always one choice away.
- Cost to the person: one context switch per halt. Under (c) the rest of the plan stays in Orca. Under (a) it runs in the person's session, unless the person hands it back as below.

<!-- Source: invariant-probe.md INV-003, INV-004; Variant 1 Round 2 responses 2 and 6; Variant 3 Safety (L14) — appended per Change #8 -->
Single writer and the hand-back after (a). The ledger has no lock (`LEDGER:145`).
- (i) The person writes the line or resumes only after the worker has settled (`SPEC:70`) (debated).
- (ii) Under (a), the person either lets their session finish the plan (the coordinator then treats the plan as done by the person and dispatches nothing for it), or ends that session after the Ruling is recorded and tells the coordinator "session ended". A ledger condition alone never lifts the freeze, because the person's session writes the Ruling and `complete` and then goes on to T{i+1} (`QA:248`, `QA:256`) (added in the merge; not debated).
- (iii) Hand-back check after (a), read-only: the person's "session ended" is recorded in the coordinator's run notes; the ledger's last line parses (`LEDGER:123`); the halted task's latest status is `complete`; the drift baseline is re-recorded at that moment. Only then may the coordinator dispatch a resume Task, which skips complete tasks (`LEDGER:153`) (added in the merge; not debated).
- (iv) After telling the coordinator "Ruling written" or "session ended", the person makes no further ledger or tree edit in that worktree until the resume Task settles (added in the merge; not debated).

## Why not (b)
<!-- Source: Variant 2, Safety (L13-L14) and Variant 2 Round 2 recommendation and new evidence 1, 2, 4 — merged per Change #12 -->
- The relayed answer reaches the worker as the coordinator's own `reply` (`CAPS:62`), which `QA:254` excludes by name ("another agent's message"). The worker cannot tell the person's words from the coordinator's, so a paraphrase is an "executor-invented approval" it cannot detect (`QA:249`), and AC-4.1 cannot test relay fidelity.
- The scope check is weaker: the person sees the coordinator's rendering of the executor's explanation (`QA:254`), not the executor's own.
- (b) cannot clarify an unclear answer such as "fine, go ahead": `QA:254` then requires one targeted question, but WC-3 allows one ask per Task (`SPEC:67`).
- An answer that arrives after the worker has settled needs a new Task (`SPEC:67`), so a late answer collapses into (c) with an agent-written line.
- A `dispute` halt needs the person to read the advice file (`RETRY:107`, `QA:281`).
- Variant 2's own advocate withdrew (b) in Round 2 (`debate-transcript.md:469`). (b) is recorded only as a possible later opt-in that the user explicitly accepts, and never for `reason=dispute`.

## Implementation cost
<!-- Source: Base (original, modified) — replaced per Change #13 (Base L21-L22 and Variant 3 L23-L24, updated for K3); the SKILL.md Wave 0 line is carried from Change #7 and "one new AC step" is worded as one AC-4.1 extension to match Changes #7 and #11, so this section does not contradict them (post-merge consistency fixes) -->
- Zero edits to `qa.md`, `ledger.md` and `retry.md`: the Ruling rule stays word for word.
- One `/sc:implement` change outside those files, which P4 needs anyway: Wave 0 in `SKILL.md` learns `--unattended` and `--report-dir <dir>` as known options (`SKILL:50`; "Where the resume runs").
- Spec text only for the rest: the D2 recommendation; one WC-3 sentence that sanctions a hand-written Ruling line after a halt and names a line written by the coordinator or any worker "executor-invented approval"; the WC-4 `reason` edit; the coordinator rules (freeze, pre-dispatch check, placement, hand-back); the stale `qa.md` anchors listed in the drift note; and one AC-4.1 extension (the return path in Reliability, plus the same-ledger-path assertion in "Where the resume runs").
- If people find hand-writing the line awkward, (a) stays available unchanged. Easy to relax later if a safe relay route is found; hard to restore trust if relaxed first and a relayed Ruling goes wrong.

## Accepted residual risks
<!-- Source: refactor-plan.md, "Invariant coverage" residual risks R1 and R2 (required in the paper by the merge brief) -->
The fixes for the six HIGH invariants come from the fault-finder's fix shapes (`invariant-probe.md`), not from a debate round. Two residual risks remain and are accepted explicitly:
- R1. The person's own edits to the halted worktree before they write the line are not prevented; the drift check sees them only for the `files=` paths (INV-001).
- R2. A well-formed line can still name the wrong scope, which no format check can catch (INV-014). (a) is one choice away.
