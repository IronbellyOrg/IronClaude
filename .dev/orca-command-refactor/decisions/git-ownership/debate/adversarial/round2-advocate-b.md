# Round 2 rebuttal: advocate B (variant 2, workers run their own git under brief rules)

Persona: backend (data integrity, scalability, fault tolerance) plus analyzer (evidence quality). Date: 2026-11-02.
Inputs read in full: `round1-advocate-a.md` .. `round1-advocate-e.md`, `round2-advocate-a.md`, the five variants, `diff-analysis.md`.
Citation keys as in the variants. "Verified" means re-read this round with `sed -n`, `grep -n` or `orca-ide skills get orchestration --reference references/<name>.md | cat -n`. Protocol behaviour derived from text but not run is marked UNVERIFIED (live).

## 1. Response to criticisms

Every criticism of variant 2 in the four other Round 1 files and in A's Round 2 file, grouped where several advocates raised the same point.

| # | Criticism (raised by) | Response |
|---|---|---|
| B1 | B is unsafe in Orca's default shared worktree: two committers collide on `index.lock`, `git add -A` sweeps other workers' files, and a commit moves HEAD and halts running implement tasks (A R1 critique and weakness 1; C critique 1, weakness 4; D critique; E critique, weakness 3) | **Conceded (Round 1 concession 1).** B is correct only with one committing writer per worktree. I add one point here. Section 3 (N1) shows that, independent of who commits, a `/sc:implement` worker whose retry ladder can revert must not share a worktree with any other source writer. The placement condition B needs is therefore one the spec needs anyway, for a reason unrelated to git ownership. |
| B2 | B forces a worktree per committing worker, against Orca's placement default "Use the current or an exact existing workspace by default. Create a worktree only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (A R1 and R2 section 2; C critique 1; D critique; E critique) | **Partly conceded, partly rebutted.** Quote verified at `[G:pl] 8-11`. Conceded: a blanket "worktree for every committing worker" is wrong for report-only workers, whose WC-11 report directories (`SPEC:75`, verified) give them no conflict. Rebutted: the rule's own exception, "a concrete checkout or filesystem conflict makes sharing unsafe", is met by two cases. (a) A worker granted local commits: its commits move the shared HEAD (`retry.md:41,44`). (b) An implement worker whose revert can delete or restore other workers' files (N1). So my plan in section 2 is narrowed to those two cases, which Orca's own text licenses. |
| B3 | A worktree per committer has a setup cost: `--setup run` (`[G:pl] 18,21`) and `make sync-dev` in each new worktree (EVAL F2) (A R2 section 2) | **Conceded on cost, rebutted on the alternative.** Verified: `[G:pl] 18,21` pass `--setup run` for `new-child` and `new-top-level`; `issue-326-evaluation.md:52` requires "the same setup the 7.2 check needs ... `make sync-dev` run there". The cost is real, and it is paid once per worker, not per commit. The alternative for an implement worker sharing a worktree is either the N1 hazard or switching the retry ladder off. That trades a known one-time setup cost for a silent data-integrity risk, and "Never turn off a quality check" (`HWW:280`, verified) argues against switching the ladder off. |
| B4 | Outward actions from workers multiply what WC-9 is built to switch off, and need D3 (b), which the spec does not recommend (A, C, D, E) | **Conceded (Round 1 concession 2).** WC-9 (`SPEC:73`, verified) and D3's recommendation of (a) "unless parallel PR monitoring is a real need" (`SPEC:343`, verified) stand. B keeps only the parallel-PR case. A's Round 2 proposal (one pr-submit Task per PR, on explicit user request) is a better shape than B's, so I adopt it in place of B's version (section 2). |
| B5 | Authorization is second-hand and "spread over many briefs and transcripts" (D weakness 2; E weakness 4; A weakness 6, briefs cannot change after creation, `SPEC:70`) | **Conceded for outward actions; bounded for local commits.** Briefs are immutable (`SPEC:70`, verified), so a revoked grant persists until a new Task replaces it. For a local, unpushed commit the damage of a stale grant is bounded: the commit stays local and the coordinator can drop it before any push. With A's condition 1 (default-off, quoted, scoped to run and branch) and SHAs in the contract, every worker commit traces to one quoted grant in one brief. The "scattered" objection then reduces to "one brief per granted Task", which is the same per-action record C is credited for (C-005). |
| B6 | Highest implementation cost; every committing command needs a commit step, a stale-lock rule and SHA fields, against SA-4's additive rule (`SPEC:172`); implement says acceptance never authorizes a commit (`managed-workspace.md:63,67`) (A strength 4; C critique 3, weakness 6; D weakness 2; E critique) | **Conceded.** Under the merge base, the in-run commit step is #326's K3 (`issue-326-evaluation.md:63`, verified), not a spec P1-P3 change. That moves B's main cost out of this spec. The cost that remains is spec wording plus one placement rule (section 2). |
| B7 | Merges back still need a single owner, so B is never complete alone, and B's claim to remove A-003 is overstated because merges need the placement map (A R1 critique, R2 section 2; C critique 4) | **Conceded.** A merge into the shared branch moves the main worktree's HEAD, so it needs that worktree to be quiet, which needs the coordinator's placement map. I narrow the claim: worker commits in a sole-writer worktree need no quiescence map at commit time. The coordinator's merges still need it. |
| B8 | B's stale-lock recovery is "a step no command has today" (E weakness 3; V2's own Recovery) | **Conceded, with a safer replacement.** A worker should not delete a lock on its own judgement that "no git process runs", because a wrong judgement deletes a live lock. Proposed rule: a retry Task that finds `index.lock` in its own worktree stops with `worker_status: blocked` and names the path. The coordinator, or the person, removes the lock after checking. This needs no new command step: a blocked contract is already a WC-4 outcome (`SPEC` WC-4 row, verified). |
| B9 | A stale lock from a coordinator crash blocks no worker under A, because workers never write the user index; `/sc:implement`'s Q0 uses a private temporary index (`SKILL.md:110-111`) (A R8, against B strength 4) | **Conceded.** Verified: Q0 snapshots "**without** staging in the user index" with `GIT_INDEX_FILE="$idx"` (`SKILL.md:110-111`). My Round 1 claim that a coordinator crash leaves the lock "where every worker writes" was wrong for the index. B strength 4 is reduced to the survival of earlier commits, which E has too. |
| B10 | Serializing N experiment commits through one session costs seconds, not minutes; the serial cost that matters is N pr-submit loops (A R11, against B strength 5) | **Conceded.** Local commits are cheap to serialize. B's throughput argument survives only for PR monitoring, and the per-PR-Task opt-in covers that. |
| B11 | B has the biggest attack surface: every committing worker holds mutating git, with no mechanical guard (D critique and weakness 2) | **Partly conceded.** Under the merge base a granted worker holds local-commit authority only, in its own worktree, and never pushes. D's guard can bound it further: a settings-level `PreToolUse` hook runs in any Claude session, including an Orca worker's top-level session (A's N2, citing CC-HOOKS; I did not fetch CC-HOOKS this round, UNVERIFIED by me). A deny-list for push, `gh pr`, `--no-verify` and `-f` costs the worker nothing it needs. Whether exit 2 still blocks under `bypassPermissions` remains UNVERIFIED (D concession 3). |
| B12 | B missed the shared-refs hazard (`refs/superclaude/implement/<slug>/T<id>`) (E weakness 9; A R14) | **Conceded (Round 1 concession 5).** A's correction holds: workers write these refs whatever the commit ownership (`SKILL.md:113,116`, verified). Distinct slugs per run must be a spec rule under every option. |

## 2. Updated assessment of the other variants

**Decision: I accept E plus A's four conditions as the merge base.** I also accept the D3 (b) per-PR opt-in and D's guard as an optional, tested control. Each condition matches a concession B already made.
- Condition 1 (default-off, scoped, quoted grant): matches `issue-326-evaluation.md:74` (verified): per-task commits are "allowed as an authorized option, never a default".
- Condition 2 (sole writer is a recorded placement fact): what B called "one worker per worktree".
- Condition 3 (dormant until K3): B concession 4.
- Condition 4 (worker invariant, distinct slugs): B12.
- One pr-submit Task per PR on explicit request replaces B's broader worker-PR claim (B4).

**What I still argue: my Round 1 plan, narrowed to what the evidence supports.** I withdraw "committing work should go in its own worktree by default" as a blanket rule; A is right that report-only workers should share (B2, B3). I keep, and now ground in new evidence, a placement rule with two triggers:

> **P1 (placement).** The coordinator places a worker in its own worktree (`--worktree new-child` or `new-top-level`) when either (a) its brief grants local commits, or (b) it runs `/sc:implement` with the retry ladder able to revert while any other worker writes outside `.dev/` in the same worktree. Report-only workers share the current worktree as Orca's default says.

Why this is more than a restatement of condition 2:
1. **Trigger (b) is needed whoever owns git.** N1 below shows that implement's revert can delete or restore another worker's files in a shared worktree. Under pure A, C or D the hazard is unchanged, because it comes from the ladder, not from commits. The spec's WC-11 ("Two workers in one worktree must never write the same file", `SPEC:75`, verified) is silently broken by the revert, which writes files the task never wrote.
2. **With P1, E's shared-worktree coordinator row shrinks to its safe core.** Once implement workers are not in the shared worktree:
   - the shared worktree holds report-only workers, which write their own WC-11 report directories;
   - the coordinator's explicit-path staging is then a list of report directories, so A-002 has little to miss;
   - no implement ladder runs there, so a coordinator commit cannot cause `head-moved` (`retry.md:41,44`).

   That is what I meant by making the coordinator's shared-worktree commit "the exception". It remains in the table, but only for the low-risk case.
3. **Orca's text licenses it.** Both triggers are "a concrete checkout or filesystem conflict" (`[G:pl] 8-11`, verified). P1 does not override Orca's default. It names the conflicts the coordinator must recognise.
4. **Cost.** P1 adds one `--setup run` and the F2 setup per isolated worker (B3). This is the price of keeping the retry ladder on (`HWW:280`).

**A (now inside E).** A's Round 2 is the most useful file in the debate, and I agree with its merged shape. A rejected my Round 1 plan for two reasons: the default is to share, and setup costs. Both apply to the blanket version, which I have withdrawn. Neither addresses trigger (b), which A did not consider. A's R8 rests on Q0 using a private index (`SKILL.md:110-111`). Its own N3 says the same protocol "rewrites working-tree files on a revert" (`retry.md:398`, per A; I verified the step at `retry.md:220`). That is the N1 hazard. A noted it as a fact about refs but not as a hazard to other workers' files.

**C.** I keep C's wins on S-002, S-004, C-005 and X-002. I accept A's case against a long-lived git session as the default outward owner. A's case has four parts: pr-submit as a worker turns operator HALTs into `blocked` (`SPEC:137`, verified); the loop is "attended, in-session" (`sc-pr-submit-protocol/SKILL.md:43`, verified); one git session serializes PR loops; and retention stretches `worker-retain`'s purpose (C concession 3). The per-PR Task opt-in keeps C's per-action record without retention.

**D.** I accept D's guard as optional and tested, as A proposes. For B's lane specifically, a settings-level deny-list in the worker session is the relevant form (B11). A subagent allowlist does not apply to a worker's own commits.

**E.** E is the base. It still needs three additions from this round:
- P1 (above), which E's "sole writer" condition presumes but never places;
- E's own concession 4, that "sole writer" also excludes user-taken-over terminals and hooks;
- B8's blocked-on-lock rule in place of E's "retry Task checks for it first" (E concession 3).

## 3. New evidence

None of these points appears in any Round 1 file or in A's Round 2 file as stated here. All were verified this round.

- **N1. `/sc:implement`'s revert can delete or overwrite other workers' files in a shared worktree.**
  - **The domain.** "Domain = every path printed by `git -C "$top" diff -z --no-renames --name-only "$start" "$now"`", minus fixed exclusions (`src/superclaude/skills/sc-implement-protocol/refs/retry.md:201`). `now` is a fresh whole-worktree snapshot taken at revert time (`retry.md:199`). So any path another worker changed in that worktree after this task's Q0 is in the domain.
  - **The exclusions.** They protect the run dir, ledger, retries dir, source file, `.dev/troubleshoot/`, other `.dev/` paths not in this task's `files=`, and submodules (`retry.md:202-208`). They do not protect any other worker's file outside `.dev/`.
  - **Step 5.** It restores each domain path that existed at `$start` (`git restore --source="$start" --worktree`). It deletes each one that did not ("Otherwise `rm -f -- "$top/$p"`", `retry.md:220`).
  - **Consequence.** In a shared worktree, a concurrent worker's source edits are reverted, and its new files are deleted. One example is `/sc:research`'s `claudedocs/research_*.md` (`src/superclaude/commands/research.md:103`, verified), which is outside `.dev/`. The content survives only in the sweep ref pinned at step 3 (`retry.md:218`).
  - **Why the guard misses it.** Check 2 (the batch guard) looks only at this ledger's own tasks: "read from the ledger on every check" (`retry.md:40`). It cannot see other Orca workers.
  - **Second effect.** Step 6 flags "every path that `git -C "$top" diff --name-only "$now" "$v"` lists outside the domain" as residue (`retry.md:221`). A concurrent writer during a revert therefore also causes a spurious `E-RESUME-NEEDED` stop.
  - **Spec coverage.** `grep -n -i revert` over the spec returns nothing (verified), so the spec does not address this.
  - **Status.** The hazard follows from the protocol text but has not been observed in a run: UNVERIFIED (live). It exists under every ownership option. It is the strongest evidence that implement workers belong in their own worktree, and once they are there, E's worker-commit lane is available to them at no extra placement cost.
- **N2. WC-11 is the spec's only parallel-write rule, and N1 breaks it.** WC-11: "Two workers in one worktree must never write the same file" (`SPEC:75`, verified). The revert writes files the task never wrote, so WC-11 cannot be met by output-path discipline alone while an implement worker shares a worktree. P1 trigger (b) is the minimal fix.
- **N3. The evaluation's F2 line already draws the boundary P1 extends.** "Workers that edit the same source files as alternative attempts (an experiment) each get their own worktree ...; workers that write only their own report directories share the current worktree" (`issue-326-evaluation.md:52`, verified). P1 adds two triggers to F2's experiment case, granted commits and an active implement ladder, and keeps F2's sharing rule for report-only workers.
- **N4. A lock-deleting retry step is riskier than a blocked outcome.** The spec already has a `blocked` `worker_status` with `blocked_question` (`SPEC` WC-4 row, verified). Routing a found `index.lock` to `blocked` (B8) keeps lock removal with the coordinator or person, who can check for a live git process. No worker then deletes a lock on its own inference.

## 4. Updated shared-assumption responses

A-002 is unchanged (REJECT as a basis for staging; stage from `git status` in a sole-writer worktree, porcelain cross-check elsewhere).

| ID | Response | What changed |
|---|---|---|
| A-001 (coordinator attended) | **QUALIFY** | I now prefer E's handling explicitly. With the person absent, a default-off grant (`issue-326-evaluation.md:74`) caps exposure at reversible local commits, and every outward action still needs an instruction that names it. |
| A-003 (quiescence knowable) | **QUALIFY** | Accept A's point that the map is the coordinator's own placement bookkeeping (`[G:pl] 15-21`, verified), and that merges need it under B too (B7). New: for an implement worker, "quiet" must hold for the **whole run**, not only at commit time. A revert can fire at any failed review (N1), so a commit-time check is not enough. P1 makes that true by placement. |
| A-004 (commit does not rewrite files) | **QUALIFY** | Add the agreed rule: a hook rewrite or failure is stop-and-report, never `--no-verify` ("Never turn off a quality check", `HWW:280`, verified). A worker in its own worktree reports `partial` or `blocked`. |
| A-005 (standing instruction covers later commits) | **QUALIFY** | Now anchored in `issue-326-evaluation.md:74` (verified): an authorized option, never a default, and an issue comment is not authorization. A standing grant covers local commits only, for the named run and branch, quoted in each brief, and never pushes. |

## 5. Updated per-point table

| Point | Superior variant | Changed from Round 1? | Reason |
|---|---|---|---|
| S-001 | V5 (E) | No | The per-action owner/condition table is the merge base's form. |
| S-002 | V3 (C) | No | Only C verified Orca reuse, serialization, retention and idle-rule mechanics. |
| S-003 | V1 (A) | No | GITDEMO is the procedure everyone cites. |
| S-004 | V3 (C) | No | Only C explains why the #326 relay cannot be something commands call. |
| C-001 | V5 (E), with P1 | No (qualified) | Coordinator commits in a shared worktree at quiescence; P1 keeps implement ladders out of that worktree, so the row is safe (N1, N2). |
| C-002 | V5 (E) | Yes (was V2 tie V5) | E's row with A's four conditions is B's rule with the guards B lacked; dormant until K3. |
| C-003 | V1 = V5 | Yes (was V5) | Shown as a tie: coordinator main chat by default; one pr-submit Task per PR only on explicit request. |
| C-004 | V5 (E) | No | Direct for outward actions; scoped, quoted, default-off grant for reversible local commits. |
| C-005 | V3 (C) | No | Per-action Orca Task record; adopted for the per-PR opt-in. |
| C-006 | V5 (E) | Yes (was V2) | E keeps B's "read SHAs, not diffs" benefit for granted workers and adds nothing to outward load; B's lead depended on worker PRs, now dropped. |
| C-007 | V5 (E) | No | Lock confined to one worktree, earlier commits survive; with the B8 refinement (blocked, not lock deletion). |
| C-008 | V5 (E), with P1 | No (qualified) | Sole-writer worker commits plus shared default for report-only workers; P1 names when isolation is required. |
| C-009 | V1 (A) default, per-PR D3 (b) opt-in | Yes (was V2) | Attended top-level loop by default (`SKILL.md:43`, `SPEC:343`); A's one-Task-per-PR shape beats B's per-worker PRs. |
| C-010 | V1 (A) | No | Wording only; E's spec cost is also wording, plus P1. |
| C-011 | V5 (E) | No | Only E names the owner and the F3 guard; P1 increases the worktrees it must clean up. |
| X-001 | V5 (E) | No | A quoted, scoped grant suffices for a reversible local commit; never for outward actions. |
| X-002 | V3 (C) | No | Per-action Orca records beat a transcript; GitHub and pr-submit's run-log remain the outward record. |
| X-003 | V1 = V4 = V5 | Yes (was V5 alone) | Coordinator main chat matches D3 (a) and pr-submit's top-level rule; the opt-in is the only exception. |
| X-004 | V1 (A) | No | The rule is conditional on a named owner (`[G:cl] 62-65`); the plan should name the PR owner. |
| X-005 | V4 (D), as amended | Yes (was V1) | The frontmatter `hooks` mechanism makes D's restriction real; a settings-level deny-list also covers worker sessions; bypass behaviour UNVERIFIED. |
| A-001 | V5 (E) | No | With the person gone, E caps exposure at reversible local commits. |
| A-002 | V5 (E) | Yes (was V2) | Same mechanism B argued (sole writer stages from `git status`), now inside E; P1 shrinks the shared-row residue to report directories. |
| A-003 | V5 (E), with P1 | Yes (was V2) | Map is coordinator bookkeeping (A); P1 makes "no other writer for the whole implement run" true by placement (N1). |
| A-004 | V5 (E) | Yes (was V2) | Both E commit paths keep hook rewrites away from concurrent writers; stop-and-report, never `--no-verify`. |
| A-005 | V5 (E) | No | Per-Task quoting of a scoped, default-off grant (`issue-326-evaluation.md:74`). |

**Tally:** E 14 alone plus 2 shared (C-003, X-003), A 4 alone (S-003, C-009, C-010, X-004) plus 2 shared, C 4, D 1 alone (X-005) plus 1 shared, B 0. Nine points changed (C-002, C-003, C-006, C-009, X-003, X-005, A-002, A-003, A-004), all toward E, toward D's amended guard, or toward ties that keep outward actions with the coordinator.

**Overall:** B's substance (worker-owned local commits in a sole-writer worktree, per-task timing, crash survival, staging from ground truth) survives inside E. B's outward-action claims do not. B's remaining contribution to the merge is P1. That placement rule is needed for N1's revert hazard whoever owns git, and it is what makes E's worker lane and E's shared-worktree row safe together.
