# Round 1: Variant 2 advocate (D4 option (b): never; no worker commits)

Citation key as in `diff-analysis.md:12` (`SPEC`, `PRL`, `HWW`, `EVAL`, `RETRY`, `MW`, `QA`), plus `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`. Every line below was re-read on this branch on 2026-11-02.

**Correction to my own variant.** V2:8 used `CLAUDE.md:68` as a general session rule; it covers upstream contributions only (OVERSTATED, `diff-analysis.md:102`). I withdraw it. The rules that apply to outward actions generally are `PRL:351` ("committing, and opening a PR all get confirmed first unless the user pre-authorized them this session") and `PRL:347` ("Commit/push only when the user asks"); the argument rests on those and `QA:254`.

## Position summary
No brief can authorize a worker to push, open a PR, post to GitHub, install on a real target, provision a VM, start a paid run, or commit. Workers leave working-tree changes and a contract; the coordinator, in the session the person talks to, does every outward step and every commit after reading the contracts (`SPEC:347`). This keeps one provenance rule across D2 and D4 and is the only option that works under the spec's default shared worktree without new command mechanisms.

## Steelman

### Variant 1 (a): named authorization per action and Task
At its strongest, (a) says: the user already decided, and making them wait for the coordinator to repeat it is friction. The repo recognises advance authorization: post-release refuses outward steps "without confirmation (or standing authorization)" (`PRL:340`), a phrase with no session qualifier (`diff-analysis.md:104`). Only (a) lets a worker deliver post-release's main value, the new-user install "to green on the classified target" (`PRL:333`), in one run. Flags stay explicit per command (`SPEC:123`), WC-9 stays the default (`SPEC:73`), and V1 names its own provenance gap (V1:14).

### Variant 3 (c): local commits yes, nothing that leaves the machine
At its strongest, (c) copies a line the repo already draws for people: "Commit locally, show your lead what changed, and push only when they say go" (`HWW:282`); "Commit locally on the feature branch only when authorized" (`HWW:212`); `/sc:git` "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). It gives issue #326's owner the per-task history he asked for (`EVAL:19`) while keeping every published action at the coordinator. It is the only variant with executable commit rules: Task files plus `.dev/tasks`, never the default branch, never push, SHAs in the contract, and a commit window keyed to `RETRY:41` (V3:5). It also adds a cheap check, `git log origin/<branch>` unchanged (V3:17).

## Strengths claimed
1. **One provenance rule for D2 and D4.** implement refuses a Ruling carried by "another agent's message" (`QA:254`), and the spec keeps that rule for workers under D2 (a) because "a coordinator's reply is 'another agent's message'" (`SPEC:67`, `SPEC:335`). A brief is the same thing: the coordinator's text. `PRL:351` asks for authorization "this session", and a worker is a different session. (b) never asks a worker to act on authority it cannot check. The spec's recommendation cites `PRL:351` as support for (a) (`SPEC:348`), marked OVERSTATED (`diff-analysis.md:105`). Side note: `SPEC:67` and `SPEC:334` cite this rule as `qa.md:238`/`232,238`; on this branch it is `QA:254`.
2. **No-commit is the only rule that is safe under the spec's default placement.** Workers share the current worktree by default (WC-11, `SPEC:75`), so they share HEAD and branch. A commit by worker A moves HEAD inside worker B's implement task window, and B's retry ladder then refuses to run because "HEAD has not moved" fails (`RETRY:41`; `q0-head` written at task start, `sc-implement-protocol/SKILL.md:114`). `git add .dev/tasks` (`CLAUDE.md:37`) is repo-wide, so A's commit also captures B's half-written ledger. (b) has none of these failure modes. This replaces my weaker V2:20 framing that the ban "rests on" the README rule: the real basis is mechanics, not `README.md:31`.
3. **Needs no command feature that does not exist.** implement has no commit step and says acceptance "never ... authorizes commit, PR, merge or release" (`MW:67`); "A FINAL pass is not a commit" (`MW:63`). The per-task commit step is #326 follow-up work (`EVAL:63`, K3). (b) is consistent with every command as written; AC-4.2 already tests it ("`git log -1` unchanged and no new PR", `SPEC:275`).
4. **Outward steps stay where a person can be asked at the moment of action.** The coordinator is the session the person talks to; it can confirm per `PRL:351` right before pushing, rather than relying on an instruction relayed hours earlier. PRs keep their one path through `/sc:pr-submit` (`CLAUDE.md:50`), whose monitor is an "attended, in-session" loop (`PRS:43`).
5. **Cheapest and easiest to change later.** Zero spec mechanism beyond WC-9 and the section 4 row (`SPEC:73`, `SPEC:156`). Loosening to (c) or (a) later is additive; tightening after a wrong push or public comment cannot undo what was published (V1:15 concedes this).

## Weaknesses identified

### Variant 1
1. **It authorizes the action it admits it cannot verify.** V1:14 says the worker "cannot check" the quoted words and that this is "the same provenance gap the spec refuses for Rulings under D2". A published PR or comment is "visible at once" (V1:15). The option grants authority through exactly the channel `QA:254` rejects, for the least reversible actions.
2. **Its main citation cuts the other way.** `PRL:351` says "this session"; V1:8 reads it as support and V1:14 as the gap (`diff-analysis.md:53`, X-003).
3. **Its commit rule has no mechanism.** "A local commit is authorized the same way" (V1:3) names no scope, branch or timing, so it inherits every shared-worktree failure in Strength 2 and has no implement commit step to switch on (`MW:63,67`; A-005).
4. **Highest test and maintenance cost.** Every outward flag must be honoured under `--unattended`, reported in the contract, and given a live check on a scratch fork PR (V1:18, V1:24).
5. **#326 does not support it on posting.** The evaluation it cites puts progress posts on the coordinator only (`EVAL:54`, F4), and says the owner's comment is not a standing instruction (`EVAL:74`).

### Variant 3
1. **"Local and undoable" fails in the default placement.** `git reset` on a shared branch can drop another worker's commits (`SPEC:75`; A-009). "Its own feature branch" (V3:3) needs a worktree per worker, which the spec does not default to; the evaluation's F2 proposes it only for experiments (`EVAL:52`).
2. **The commit window is correct for one implement run only.** Another worker's commit still moves HEAD inside this task's window (`RETRY:41`), and implement has no commit step to time (`MW:63,67`; `EVAL:63`). V3:23 "No command needs a new outward flag" conflicts with its own V3:5 requirement (X-006).
3. **Scope rule leaks.** "Task's own files plus `.dev/tasks`" (V3:5) stages every worker's ledgers in a shared worktree, because the `.dev/tasks` rule is repo-wide (`CLAUDE.md:37`).
4. **Same provenance gap, smaller.** The commit still rests on the coordinator's quotation (V3:5), which `QA:254` would not accept for a Ruling. V3 does not address D2 consistency (C-007).

## Concessions
- **`CLAUDE.md:68` withdrawn** as a general session rule (see the correction above).
- **`PRS:43-49` overstated.** A worker is itself a top-level session (WC-7, `SPEC:71`), so pr-submit's top-level rule does not by itself bar a worker. "Only the coordinator or person runs it" (V2:10) is a D3 (a) outcome (`SPEC:341`), not a consequence of `PRS`. V3 states the same conclusion without the overreach.
- **Repo policy permits commits when asked** (`CLAUDE.md:37`; `HWW:212`). (b)'s commit ban is a safety choice for the shared-worktree default, not a repo rule. If the coordinator gives each committing worker its own worktree and branch, V3's commit rule becomes reasonable, and I would accept (c) for commits under that condition once implement has a commit step (K3).
- **Deferred steps cost real work (A-006).** auggie-review's only posting path is its own `--post-pr` (`SPEC:123`), so the coordinator re-runs the review or posts `REVIEW.md` by hand. post-release's real-target install moves to the coordinator, losing V1's one-run delivery (`PRL:333`). On convenience V1 is better.
- **#326 alignment.** V3 meets the per-task-commit request (`EVAL:19`); (b) does not.
- **V3's `git log origin/<branch>` check** (V3:17) is worth adding to AC-4.2 under any option.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | WC-9 turns every outward default off under `--unattended` (`SPEC:73`); all three start there. |
| A-002 | ACCEPT | "commit only when asked" (`CLAUDE.md:37`) and "a commit needs authorization" (`HWW:324`). (b) adds that a worker cannot receive that ask directly. |
| A-003 | QUALIFY | True only while the user's instruction sits in the coordinator's own live conversation. A restarted or long-running coordinator is not "this session" (`PRL:351`) for an old instruction either, so under (b) the coordinator confirms with the person at action time unless the person authorized it in that conversation. (b) is still safer than (a): the coordinator is the session a person can be asked in, a worker is not. |
| A-004 | ACCEPT | Workers share the worktree by default (`SPEC:75`), so they share HEAD and branch; this is the core reason (b) bans worker commits. |
| A-005 | ACCEPT | implement has no commit step (`MW:63,67`; `EVAL:63`); holds only for task (`sc-task-protocol/SKILL.md:61`) and post-release (`PRL:340`). |
| A-006 | QUALIFY | Pushing commits and opening PRs need no rework. auggie-review posting and post-release's real-target install do: the only posting path is `--post-pr` (`SPEC:123`). A genuine cost of (b) and (c); the spec should name the coordinator's follow-up step. |
| A-007 | REJECT | Faithful quoting may be likely, but the worker cannot verify it, and the repo refuses the same relay for Rulings (`QA:254`). It cannot be the safety basis for outward actions. |
| A-008 | ACCEPT | `CLAUDE.md:50`; restated in the evaluation's F5 (`EVAL:55`). |
| A-009 | ACCEPT | A reset on a shared branch can drop another worker's commits (`SPEC:75`), and any HEAD move breaks `RETRY:41` for a task in flight. |
| A-010 | ACCEPT | The evaluation says the owner's comment "does not by itself authorize commits in a worker" (`EVAL:74`). #326 is design input. |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | V3 | Separate commit-rule paragraph is clearer. |
| S-002 | V3 | All keys declared and used; V2 leaves EVAL unkeyed, V1 declares unused HWW. |
| S-003 | equal | Heading differences are cosmetic. |
| S-004 | V1 | V1 states its central weakness where it bites (Safety); V2 does too, V3 states none. |
| S-005 | V3 | Only variant with executable commit constraints (though they fail when worktrees are shared). |
| S-006 | V2 = V3 | Both use every declared key. |
| S-007 | V3 | Only variant that marks an UNVERIFIED claim. |
| C-001 | V2 | Refuses authority a worker cannot verify, matching `QA:254`. |
| C-002 | V2 | V3's reversibility is contradicted under shared worktrees (A-009); V1 concedes irreversibility. |
| C-003 | V2 | No worker HEAD moves, so `RETRY:41` is never tripped by another worker. |
| C-004 | V2 = V3 | Real-target install and VM are the hard-to-reverse class `PRL:351` names; V1's one-run delivery is a real but convenience-only gain (conceded). |
| C-005 | V2 = V3 | Posting stays with the coordinator; both still owe a follow-up path (A-006). |
| C-006 | V2 | One rule refuses task's EXEMPT commit and push and the TFEP commit, as `SPEC:144` already wants unattended. |
| C-007 | V2 | Same provenance rule as D2 (`SPEC:335`, `QA:254`). |
| C-008 | V2 | One rule, AC-4.2 as written (`SPEC:275`); adopt V3's `origin/<branch>` check too. |
| C-009 | V2 | No new command mechanism; V3 needs an implement commit step (X-006). |
| C-010 | V3 | Delivers per-task commits (`EVAL:19`) while keeping posts at the coordinator (`EVAL:54`). |
| C-011 | V2 = V3 | One PR path via `/sc:pr-submit` at the coordinator (`CLAUDE.md:50`). |
| C-012 | V3 | Only variant with a scope rule, though `.dev/tasks` staging leaks in shared worktrees. |
| C-013 | V2 | Loosening later is additive; published actions cannot be recalled. |
| C-014 | V3 | Reviewable per-task history is a better day-to-day experience, if worktrees are separate. |
| C-015 | equal | All three miss that WC-9 also cites `README.md:31` (`SPEC:73`); both citations should move to `PRL:347,351` and `CLAUDE.md:37`. |
| X-001 | V2 = V3 | Nothing that leaves the machine is done on relayed authority. |
| X-002 | V2 | Under the default shared worktree, no worker commits; V3 wins only with one worktree per committing worker plus K3. |
| X-003 | V2 = V3 | Both read "this session" as excluding the worker; V1 holds both readings. |
| X-004 | V2 = V3 | `EVAL:54` puts progress posts on the coordinator. |
| X-005 | V2 | In a shared worktree a commit is not "local and undoable" for the other workers. |
| X-006 | V2 | Zero new mechanisms; V3's commit window needs a step implement lacks (`MW:63,67`). |
| X-007 | V3 | V3 reaches "coordinator only" without V2's overstated `PRS:43-49` reading (conceded). |
| A-003 | V2 | Coordinator confirms at action time; a worker cannot be asked. |
| A-006 | V1 | Only (a) avoids deferred-step rework; cost conceded. |
| A-010 | V2 = V3 | #326 is design input (`EVAL:74`), so its commit request does not decide D4. |
