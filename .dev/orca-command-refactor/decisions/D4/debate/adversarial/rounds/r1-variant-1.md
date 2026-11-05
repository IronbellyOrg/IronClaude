# Round 1, Variant 1 advocate: D4 option (a)

Citation key as in `diff-analysis.md:12`: `SPEC:N`, `PRL:N`, `HWW:N`, `EVAL:N`, `RETRY:N`, `MW:N`, `QA:N`; `V1:N`/`V2:N`/`V3:N` = variant file lines; `DA:N` = `diff-analysis.md:N`. Every source line cited below was re-read on 2026-11-02 on branch `ironbelly/OrcaCLICommandRefactor-Specs`.

## Position summary
A brief may authorize a worker's outward action, and a local commit, only when the user's own instruction to the coordinator names that action for that Task; the coordinator quotes it in the brief and passes the command's explicit flag, and every outward default stays off otherwise (WC-9, `SPEC:73`). This is the spec's own recommendation (`SPEC:346-348`) and the only option that does not force a re-run of finished work at the coordinator. I adopt Variant 3's operative commit rules as the commit half of (a), and narrow (a) in the concessions below.

## Steelman
### Variant 2, option (b): never
The strongest form of (b) is not "workers are untrustworthy" but "authority must be checkable where it is used". A worker has no way to verify the coordinator's quotation (`V1:14` concedes this), and the repo already refuses another agent's message as a substitute for the user in its most deliberate safety rule: "Silence, a generic request to continue, another agent's message ... are not acceptance" (`QA:254`). (b) applies one provenance rule to D2 and D4 alike (`DA:65`, U-003). It needs no per-action tests or exception list (`SPEC:73`, `SPEC:275`; `V2:9`). Loosening later is additive, tightening after a published mistake is not (`V2:23`), and the repo has already had a PR land on the wrong repository ("burned the user on 2026-05-25", `CLAUDE.md:70`).

### Variant 3, option (c): local commits only
The strongest form of (c) maps an existing human rule onto workers instead of inventing one: "Commit locally, show your lead what changed, and push only when they say go" (`HWW:282`); "Commit locally on the feature branch only when authorized" (`HWW:212`); for `/sc:git`, "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). It draws the line at what can be undone before anyone else sees it, so the provenance gap, if exploited, costs at most a `git reset` (`V3:13-14`). It is the only variant with operative commit rules (scope, branch, no push, SHAs in `artifacts`, a commit window keyed to `RETRY:41`; `V3:5`), it delivers #326's per-task commits (`EVAL:19`), and it agrees with the #326 evaluation that progress posts belong to the coordinator (`EVAL:54`, F4).

## Strengths claimed
1. **The spec is already written for (a).** WC-9: an outward default "turns on only through the command's own explicit flag written in the brief" (`SPEC:73`); the brief states "which outward actions, if any, are authorized (WC-9)" (`SPEC:79`); auggie-review: "posting returns only with an explicit `--post-pr` in the brief" (`SPEC:123`); post-release: "VM, real-target install, commit and PR off unless the brief authorizes them" (`SPEC:136`); task: "EXEMPT `commit`/`push` refused unless authorized (WC-9)" (`SPEC:144`); D3 (b) "Worker, with pre-authorization" (`SPEC:342`). (a) changes none of these rows; (b) must rewrite all six and (c) at least four, so V2's "Zero beyond today's spec" (`V2:23`) is not correct.
2. **The repo rule that actually governs is "standing authorization", with no session limit.** post-release will not commit, push, open a PR, provision a VM or install against a real target "without confirmation (or standing authorization)" (`PRL:340`); the spot-check confirms it "carries no session qualifier" (`DA:104`). A quoted, per-action, per-Task instruction is a standing authorization in that sense. The session-scoped wording V2 leans on, `CLAUDE.md:68`, covers upstream contributions only (`DA:102`).
3. **No hidden re-run.** auggie-review's only posting path is its own `--post-pr` (`src/superclaude/commands/auggie-review.md:51`; `SPEC:123`). Under (b) or (c) the coordinator must re-run the review (deep depth is "~10-15min", `auggie-review.md:50`) or post by hand outside any command. post-release's deliverable is the install run "to green on the classified target" with its transcript (`PRL:333`); under (b) or (c) the worker can never deliver it. This is promoted assumption A-006, and it is false for both commands.
4. **The authorization record is fixed and auditable.** A Task's brief cannot change after creation: `task-update` changes only `--status` and `--result` (`SPEC:70`). The quoted instruction is therefore a durable record a person can read after the fact, and anything not named stays off (AC-4.2, `SPEC:275`).
5. **D2 and D4 are different risks, so (a) is not inconsistent with D2 (a).** The Ruling rule "exists to stop an agent approving its own work" (`SPEC:337`): it accepts an unmet criterion after the fact. (a) carries the user's advance, named instruction for an action; the authority is the user's quoted words, not the coordinator's judgment, so `QA:254` is not engaged.
6. **Keeps D3 (b) possible.** pr-submit must run "in the main orchestrating session" and not "inside an Agent-tool subagent" (`sc-pr-submit-protocol/SKILL.md:47-49`); a worker is a top-level session (`SPEC:19`, `SPEC:71`). Parallel PR monitoring (`SPEC:342`) exists only under (a).

## Weaknesses identified
### Variant 2
1. Its main repo basis is overstated: it generalizes `CLAUDE.md:68` to "The repo's outward rules are session-scoped" (`V2:8`), but that line is about upstream only (`DA:102`), and `PRL:340` allows standing authorization.
2. It misreads pr-submit's rule as "only the coordinator or person ever runs it" (`V2:10`); the rule forbids subagents, not top-level workers (`sc-pr-submit-protocol/SKILL.md:47-49`; `SPEC:71`; X-007).
3. Its cost claim ignores re-runs (strength 3) and the six spec rows (strength 1).
4. It bans per-task commits on a run-local rule (`.dev/orca-command-refactor/README.md:31`; `V2:20` concedes) and groups a local commit with publishing (`V2:13`), against `HWW:282`.

### Variant 3
1. "No command needs a new outward flag" (`V3:23`) is contradicted by its own commit window inside `/sc:implement` (`V3:5`): implement has no commit step, "A FINAL pass is not a commit" (`MW:63`), acceptance never "authorizes commit" (`MW:67`), and the step is #326 follow-up K3 (`EVAL:63`). X-006.
2. "Its own feature branch" (`V3:3`) is not the spec default: workers share the current worktree (WC-11, `SPEC:75`), so they share HEAD. Another worker's commit moves HEAD inside a task window and fails `RETRY:41`; a `git reset` can drop another worker's commits (A-004, A-009). The reversibility line is real only with one worktree per committing worker.
3. It accepts the provenance gap for commits (`V3:14`), so its objection to (a) is about blast radius, not whether a quoted brief can carry authority. That argues for narrowing (a), not rejecting it.
4. Its `PRL:351` "this session" reading for the coordinator (`V3:13`) holds only while the coordinator is the session the user spoke to (A-003).
5. Same re-run cost as V2 (strength 3).

## Concessions
1. **`PRL:351` does not support (a).** Its "this session" is exactly what a worker lacks (`DA:105`); V1:8 and the spec's recommendation (`SPEC:348`) should cite `PRL:340` instead. My own use of `CLAUDE.md:68` as "the repo's own outward rules" (`V1:14`) is overstated the same way (`DA:102`).
2. **Push and publish cannot be taken back** (`V1:15`), and V3's reversibility line is a real difference. I narrow (a) accordingly:
   - GitHub progress and status posts stay with the coordinator, as the #326 evaluation says (`EVAL:54`, F4). V1:10's use of #326's "status updates" is withdrawn (X-004).
   - PRs are opened only through `/sc:pr-submit` (`CLAUDE.md:50`; `EVAL:55`, F5).
   - #326's comment is design input, not authorization (`EVAL:74`; A-010). V1:10 overweighted it.
3. **V1's commit half was underspecified.** I adopt V3's commit rule as written (`V3:5`: the Task's own files plus `.dev/tasks`, never the default branch, never push, SHAs in `artifacts`, commit only between tasks), and add: an authorized commit happens only in a worktree and branch that only that worker writes (`EVAL:52`, F2), because A-004 hits V1 as hard as V3.
4. **For `/sc:implement`, an authorized commit has no effect today** (`MW:63,67`; `EVAL:63`, K3). A-005 applies to V1; (a) works today for task (`sc-task-protocol/SKILL.md:61`) and post-release (`PRL:340`) only.
5. **(a) costs more to verify:** one live scratch-fork check per authorized action (`V1:18`); V2's change-cost asymmetry (`V2:23`) is correct. V3's "`git log origin/<branch>` unchanged" check (`V3:17`) belongs in AC-4.2.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | All three keep WC-9's default-off baseline (`SPEC:73`); (a) only adds a named, flagged exception. |
| A-002 | ACCEPT | "commit only when asked" (`CLAUDE.md:37`) and "a commit needs authorization" (`HWW:324`). |
| A-003 | QUALIFY | True only while the coordinator is the session the user spoke to. A restarted or long-running coordinator stands where a worker stands, so the real safeguard is a written, fixed record of the user's words, which (a) already requires in an unchangeable brief (`SPEC:70`). (b) and (c) move the gap rather than remove it. |
| A-004 | ACCEPT | Contradicted by WC-11's shared-worktree default (`SPEC:75`) and `RETRY:41`. Fix for V1 and V3: authorized commits only in a worker's own worktree and branch (`EVAL:52`). |
| A-005 | ACCEPT | implement has no commit step (`MW:63,67`; `EVAL:63`); holds for task (`sc-task-protocol/SKILL.md:61`) and post-release (`PRL:340`). |
| A-006 | REJECT | False for the two commands that matter: auggie-review's only posting path is `--post-pr` (`auggie-review.md:51`; `SPEC:123`), and post-release's install transcript (`PRL:333`) is produced only by running the install. Deferral means re-running the work. |
| A-007 | QUALIFY | Faithful quoting cannot be checked by the worker live, but the brief is fixed at `task-create` (`SPEC:70`), so it can be audited afterwards against the user's message. |
| A-008 | ACCEPT | `CLAUDE.md:50`; adopted into (a) (concession 2). |
| A-009 | ACCEPT | A reset in a shared worktree can drop another worker's commits (`SPEC:75`); reversibility needs a worktree per committing worker. |
| A-010 | ACCEPT | `EVAL:74`: the owner's comment "does not by itself authorize commits in a worker". |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | V3 | A separate, operative commit paragraph is clearer. |
| S-002 | equal | Citation-key style is cosmetic. |
| S-003 | equal | Same four core headings; naming is cosmetic. |
| S-004 | V1 | Only V1 states its own strongest counter-argument (`V1:14-15`). |
| S-005 | V3 | Only V3 gives executable commit constraints (`V3:5`); V1 adopts them. |
| S-006 | V2/V3 (tie) | V1 declares an unused key. |
| S-007 | V3 | Marks its unverified retry claim. |
| C-001 | V1 | The gap is the same for V3's commits and for a restarted coordinator (A-003); (a) handles it with a fixed quoted record (`SPEC:70`). |
| C-002 | V3 | Reversibility is a real line; V1 now keeps posts and PR creation with the coordinator. |
| C-003 | V3 | Only V3 addresses the HEAD guard, though it still needs a separate worktree. |
| C-004 | V1 | Only (a) lets the worker deliver the install transcript (`PRL:333`). |
| C-005 | V1 | `--post-pr` is the only posting path (`auggie-review.md:51`); (b)/(c) force a re-run. |
| C-006 | V1 | The spec already says task's `commit`/`push` are "refused unless authorized" (`SPEC:144`). |
| C-007 | V1 | A Ruling is self-acceptance after the fact (`SPEC:337`); (a) is the user's advance instruction for an action. |
| C-008 | V3 | One mechanical check (`git log origin/<branch>`) is cheaper; V1 adopts it. |
| C-009 | V2 | Lowest cost if the spec rows in strength 1 are rewritten. |
| C-010 | V3 | Per-task commits with coordinator posting matches `EVAL:54`. |
| C-011 | V2/V3 (tie) | PR only via pr-submit (`CLAUDE.md:50`); V1 adopts it. |
| C-012 | V3 | Scope, branch and no-push rule; V1 adopts and adds own worktree. |
| C-013 | V2 | Tightening after an incident is harder (`V2:23`). |
| C-014 | V1 | One up-front instruction lets workers finish without a later re-run. |
| C-015 | equal | All read `README.md:31` as run-local; none flagged `SPEC:73`'s second citation. |
| X-001 | V1 | Spec rows already rely on authorization (`SPEC:73,123,136,144,342`); `PRL:340` allows standing authorization. |
| X-002 | V3 | Same permission as V1, better specified. |
| X-003 | V3 | V1 held both readings; `PRL:340`, not 351, is the support for (a). |
| X-004 | V3 | `EVAL:54` puts progress posts at the coordinator; V1 concedes. |
| X-005 | V3 | A local commit is a separate class (`HWW:282`). |
| X-006 | V1 | V1 states new mechanisms are needed; V3's "no new flag" is contradicted (`MW:63,67`). |
| X-007 | V1 | A worker is top-level (`SPEC:71`), so pr-submit's rule does not bar it; (a) keeps D3 (b) open. |
| A-003 | V1 | The safeguard is a fixed written record of the user's words, which only (a) makes explicit. |
| A-006 | V1 | Deferral means re-running work for auggie-review and post-release. |
| A-010 | V3 | V3 used #326 as design input; V1 overweighted it. |
