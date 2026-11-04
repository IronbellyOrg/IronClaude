# Diff Analysis: D4 decision-position Comparison

## Metadata
- Generated: 2026-11-02T15:38:00Z
- Variants compared: 3
  - Variant 1 (V1): `variant-1-original.md`, option (a): the brief may authorize a named outward action, and a local commit, when the user's own instruction names it
  - Variant 2 (V2): `variant-2-original.md`, option (b): never; no worker commits
  - Variant 3 (V3): `variant-3-original.md`, option (c): local commits may be authorized; nothing that leaves the machine
- Decision under debate: D4, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:345-348` (cited `SPEC:N`), including whether workers may commit (`SPEC:156`)
- Total differences found: 48
- Categories: structural (7), content (15), contradictions (7), unique (9), shared assumptions (10: UNSTATED 3, STATED 4, CONTRADICTED 3)
- Citation conventions: `V1:N`, `V2:N`, `V3:N` = line N of the variant file; `SPEC:N` = spec line; `PRL:N` = `src/superclaude/skills/sc-post-release-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `EVAL:N` = `.dev/orca-command-refactor/review/issue-326-evaluation.md:N`; `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/retry.md:N`; `MW:N` = `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:N`; `QA:N` = `src/superclaude/skills/sc-implement-protocol/refs/qa.md:N`. All lines were read on branch `ironbelly/OrcaCLICommandRefactor-Specs` on 2026-11-02.
- Taxonomy tags: L1 surface (wording, format, citation style), L2 structural (policy organization, component boundaries, dependencies), L3 state-mechanics (session/authorization state, guard conditions, git HEAD and branch state, concurrency). Priority L3 > L2 > L1; default L2.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Tag |
|---|------|-----------|-----------|-----------|----------|-----|
| S-001 | Position statement | One paragraph; commit rule appended as a last clause (V1:3) | One paragraph; commit rule appended as a last clause (V2:3) | Two paragraphs: an action split, then a separate "Commit rule" paragraph with operative constraints (V3:3-5) | Low | L1 |
| S-002 | Citation key | `SPEC`, `PRL`, `HWW`, `EVAL` (V1:5) | `SPEC`, `PRL`, `HWW`, `PRS`; the issue #326 evaluation is cited by full path, not keyed (V2:5, V2:20) | `SPEC`, `HWW`, `PRL`, `EVAL` (V3:7) | Low | L1 |
| S-003 | Section set | "Strongest case for it", Safety, Reliability, day to day, Implementation cost (V1:7-24) | Same five headings (V2:7-23) | "Why a third option" replaces "Strongest case for it"; other four headings the same (V3:9-23) | Low | L1 |
| S-004 | Where each variant states its own weakness | Inside Safety: concedes the cross-session provenance gap and irreversibility (V1:14-15) | Inside day to day: concedes no per-task commits and that the commit ban rests on a run-local rule (V2:20) | No weakness section; one UNVERIFIED caveat in Reliability (V3:17) | Medium | L2 |
| S-005 | Operative rule density | Policy level only; no rule for commit scope, branch or timing | Policy level only (one rule: never) | Gives executable constraints: files staged, branch, no push, commit window, contract `artifacts` entry (V3:5) | Medium | L2 |
| S-006 | Declared but unused citation key | `HWW` declared (V1:5) but no `HWW:` citation appears in the body | All declared keys used | All declared keys used | Low | L1 |
| S-007 | Verification marking | No UNVERIFIED marks | No UNVERIFIED marks | Marks the retry-ladder compatibility "UNVERIFIED live" (V3:17) | Low | L1 |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity | Tag |
|---|-------|-------------------|-------------------|-------------------|----------|-----|
| C-001 | Provenance of authorization across sessions ("this session") | The user's words reach the worker only as the coordinator's quotation; the worker "cannot check them"; repo rules say "this session" and a worker is a different session. Accepts this gap (V1:14). | Treats the gap as disqualifying: a worker's "only authority is the coordinator's text" (V2:8). | Accepts the gap only for the one undoable action, the local commit (V3:14); published actions stay with the coordinator, where `PRL:351`'s "this session" holds (V3:13). | High | L3 |
| C-002 | Reversibility (local commit vs push/post) | Concedes pushes and posts by an unwatched worker are visible at once and hard to reverse (V1:15), but authorizes them anyway when named. | Nothing a worker does is published or committed (V2:13). | Draws the line at reversibility: a local commit is "local and undoable (`git reset` on its own branch)" (V3:13). Analyst note: undoable only while unpushed and only if no other worker shares the branch (see A-004, A-009). | High | L3 |
| C-003 | Per-task commits and implement's retry-ladder HEAD guard | Silent on the retry ladder; authorizes commits per Task without timing rules (V1:3). | No worker commits, so a worker never moves HEAD under an implement task (V2:3). | Commits only after a task's `complete` line and before the next task's Q0, so `RETRY:41` ("HEAD has not moved") is not tripped (V3:5). Analyst note: that holds for one sequential implement run; Q0 writes `q0-head` at task start (`src/superclaude/skills/sc-implement-protocol/SKILL.md:114`). A commit by another worker in a shared worktree (`SPEC:75`, WC-11 default) moves HEAD inside this task's window and disables its ladder; implement also has no commit step today (`MW:63,67`; `EVAL:63`, K3). | High | L3 |
| C-004 | post-release real-target install, VM and PR steps (`PRL:340`, `SPEC:136`) | Worker may run the new-user install "to green on the classified target" when authorized, so the worker delivers the whole result (V1:9, `PRL:333`). | Worker reports these steps skipped; coordinator does them afterwards (V2:19). | Same as V2 (V3:20). | Medium | L2 |
| C-005 | auggie-review posting (`SPEC:123`) | Explicit `--post-pr` in the brief may turn posting back on (V1:11). | Never by a worker (V2:3, V2:13). | Never by a worker; "GitHub comment" is in the never-list (V3:3). None of the three says how the coordinator posts a worker's `REVIEW.md` afterwards (see A-006). | Medium | L2 |
| C-006 | task's EXEMPT `commit`/`push` (`SPEC:144`; EXEMPT list includes commit and push at `src/superclaude/skills/sc-task-protocol/SKILL.md:61`) | Not discussed; by its rule both commit and push are authorizable. | Not discussed; by its rule both refused. | Not discussed; by its rule commit authorizable, push refused. No variant addresses the TFEP report that the skill commits (`sc-task-protocol/SKILL.md:266`), which `SPEC:144` keeps uncommitted in unattended mode. | Medium | L2 |
| C-007 | Consistency with D2 ("another agent's message ... not acceptance") | Names the inconsistency itself: "the same provenance gap the spec refuses for Rulings under D2 (`SPEC:334`)" (V1:14). | Uses D2's rule as its main reason, quoting `QA:254` (V2:8). | Does not cite D2; argues the gap is acceptable because a commit can be undone (V3:14). | High | L3 |
| C-008 | Testability | AC-4.2 covers the no-flag case; each authorized action needs its own live check on a scratch fork PR (V1:18). | One rule, AC-4.2 as written; "no per-action flags to test" (V2:16). | AC-4.2 plus an added "`git log origin/<branch>` unchanged" check (V3:17). | Medium | L2 |
| C-009 | Implementation cost | WC-9 sentence, section 4 `/sc:git` row; every outward flag honoured under `--unattended` and reported in the contract (V1:24). | "Zero beyond today's spec" (V2:23). | WC-9 sentence, `/sc:git` row, implement row commit window; "No command needs a new outward flag" (V3:23). | Medium | L2 |
| C-010 | Issue #326 alignment | Claims full alignment: per-task commits and GitHub status updates (V1:10, `EVAL:18-19`). | Concedes it fails the per-task-commit request (V2:20). | Delivers per-task commits (V3:20); GitHub posting stays with the coordinator, matching the evaluation's F4 (`EVAL:54`). | Medium | L2 |
| C-011 | PR path | Not addressed beyond explicit per-command flags (V1:11). | PRs only via `/sc:pr-submit` run by the coordinator or person, citing its top-level attended rule (V2:10). | PRs via `/sc:pr-submit` at the coordinator (V3:13). | Low | L2 |
| C-012 | Commit scope and branch boundary | No scope rule beyond "authorized the same way" (V1:3). | n/a (no commits). | Only the Task's own files plus `.dev/tasks`; never on `master` or the default branch; never pushes; SHAs listed in contract `artifacts` (V3:5). Analyst note: `git add .dev/tasks` (`CLAUDE.md:37`) is repo-wide, so in a shared worktree it stages other workers' ledgers. | Medium | L3 |
| C-013 | Cost of changing the decision later | "Later tightening means re-auditing every brief template" (V1:24). | "Loosening later ... is additive and cheap; tightening after an incident is not" (V2:23). | "Loosening to (a) later stays possible" (V3:23). | Low | L2 |
| C-014 | Person's day-to-day work | Says once, per action and per Task, what workers may do; trusts the coordinator's quoting (V1:21). | Coordinator with the person commits, pushes and opens the PR (V2:19). | Person reviews a per-task commit history before the coordinator pushes (V3:20). | Low | L2 |
| C-015 | Basis of today's commit ban | `README.md:31` is run-local, not repo policy (V1:10). | Same reading (V2:20). | Drops the README citation from the section 4 row only (V3:23). Analyst note: WC-9 itself also cites `.dev/orca-command-refactor/README.md:31` (`SPEC:73`); no variant flags that second citation. | Low | L1 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact | Tag |
|---|-------------------|-------------------|-------------------|-------------------|--------|-----|
| X-001 | May a brief authorize push, PR, GitHub post, install, VM or paid run? | "a worker may push, open a PR, post to GitHub, install, provision or run a paid external job only when the user's own instruction to the coordinator names that action for that Task" (V1:3) | "no brief can authorize a worker's outward action" (V2:3) | "Every action that leaves the machine or touches a shared target ... is never done by a worker" (V3:3) | High | L3 |
| X-002 | May a worker make git commits? | "a local commit is authorized the same way" (V1:3) | "none, as the spec says today" (V2:3) | "a brief may authorize a worker to make **local commits** on its own feature branch, and nothing else outward" (V3:3) | High | L3 |
| X-003 | What `PRL:351`'s "this session" implies for a worker | Cites it as support: "Pre-authorization is already a recognised form" (V1:8), then in Safety says the repo rules say "this session" and "a worker is a different session" (V1:14); the variant holds both readings. The spec's own recommendation also cites `PRL:340,351` for (a) (`SPEC:348`). | "A worker is a separate session whose only authority is the coordinator's text" (V2:8) | Applies "this session" to the coordinator only: outward steps "confirmed ... unless the user pre-authorized them this session" at the top-level coordinator (V3:13) | High | L3 |
| X-004 | Who should post #326's GitHub status updates | Cites #326 wanting "status updates through GitHub (`EVAL:18`)" as a reason to let briefs authorize worker outward actions (V1:10) | Nobody but the coordinator or person posts (V2:3) | "Everything published still passes through the top-level coordinator" (V3:13). The cited evaluation sides with V2/V3 here: progress posts are made "only [by] the coordinator ... workers report progress only through heartbeats and `worker_done`" (`EVAL:54`, F4). | Medium | L2 |
| X-005 | Is a local commit in the same class as outward actions? | Same authorization path as pushes and posts (V1:3) | Grouped with publishing: "no worker can publish, push, commit, install ..." (V2:13) | Separate class: "local and undoable" (V3:13) | Medium | L3 |
| X-006 | Do commands need new mechanisms? | "each outward flag must be honoured under `--unattended` and reported in the contract" (V1:24) | "Zero beyond today's spec" (V2:23) | "No command needs a new outward flag under `--unattended`" (V3:23), yet its commit rule requires commits inside `/sc:implement` between tasks (V3:5), a step implement does not have (`MW:63,67`; `EVAL:63`, K3: "The flag or step that performs per-task commits inside `/sc:implement`" is #326 work) | Medium | L2 |
| X-007 | Can a worker run `/sc:pr-submit` at all? | In D4 scope via D3 (b) (`SPEC:345`); not argued in V1 | Reads `PRS:43-49` (top-level, attended) as meaning "only the coordinator or person ever runs it" (V2:10); but a worker is itself a top-level session (WC-7, `SPEC:71`), and D3 (b) contemplates a pre-authorized worker (`SPEC:342`) | Coordinator only (V3:13) | Low | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Names the concrete value lost under (b) and (c): post-release's new-user install run "to green on the classified target" with a transcript always moves back to the coordinator (V1:9, `PRL:333`). | Medium |
| U-002 | V1 | States its own strongest counter-argument: authorization crosses sessions through an agent, and that is the provenance gap the spec refuses for D2 Rulings (V1:14, `SPEC:334`). | High |
| U-003 | V2 | Ties D4 directly to the implement rule text: "another agent's message ... not acceptance" (`QA:254`, confirmed on this branch), giving one consistent provenance rule across D2 and D4 (V2:8). | High |
| U-004 | V2 | Asymmetric change cost: loosening later is additive, tightening after an incident is not (V2:23). | Medium |
| U-005 | V2 | Keeps one PR path through `/sc:pr-submit` run by the coordinator or person (V2:10, `CLAUDE.md:50`). The supporting reading of `PRS:43-49` is overstated (X-007). | Low |
| U-006 | V3 | Maps the repo's existing human rule onto workers: "Commit locally ... push only when they say go" (`HWW:282`), "Commit locally on the feature branch only when authorized" (`HWW:212`), and `/sc:git`'s "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`) (V3:10). | High |
| U-007 | V3 | Operative commit rule: Task's own files plus `.dev/tasks`, never `master`/default branch, never push, each SHA listed in contract `artifacts` (V3:5). | High |
| U-008 | V3 | Implement commit window: after a task's `complete` line and before the next task's Q0, keyed to `RETRY:41` (V3:5). Correct for one sequential run; needs a commit step implement lacks (X-006) and fails under a shared worktree (A-004). | High |
| U-009 | V3 | A mechanical check for "nothing left the machine": `git log origin/<branch>` unchanged, added to AC-4.2 (V3:17). | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted | Tag |
|---|------------------|-----------|----------------|----------|-----|
| A-001 | All three keep WC-9's default | Under `--unattended` every outward default stays off unless authorized; this is the baseline each option starts from (V1:3, V2:9, V3:3; `SPEC:73`). | STATED | No | L3 |
| A-002 | All three on commits | A commit needs authorization, because repo policy is "commit only when asked" (`CLAUDE.md:37`; V1:10, V2:20, V3:5). | STATED | No | L2 |
| A-003 | All three route unauthorized outward steps to the coordinator | The coordinator session is the session in which the user's authorization was given, so `PRL:351`'s "this session" is satisfied there and the coordinator may perform or relay outward steps. No variant states this; all depend on it. An Orca coordinator can run long after the user's instruction or be restarted, which would put it in the same position as a worker. | UNSTATED | Yes [SHARED-ASSUMPTION] | L3 |
| A-004 | V1 and V3 (V2 makes no commits) | A worker's commits land on a branch no other worker writes. V3 states "its own feature branch" (V3:3); V1 is silent. Contradicted by the spec default: workers share the current worktree (WC-11, `SPEC:75`), so they share HEAD and branch; `git add .dev/tasks` (`CLAUDE.md:37`) stages every worker's ledgers; and another worker's commit moves HEAD inside an implement task's window, failing `RETRY:41`. | CONTRADICTED | No (flagged) | L3 |
| A-005 | V1 and V3 | The command a worker runs has a commit step that the brief's authorization can switch on. Contradicted for `/sc:implement`: acceptance "never ... authorizes commit, PR, merge or release" (`MW:67`), "A FINAL pass is not a commit" (`MW:63`), and the per-task commit step is #326 follow-up work (`EVAL:63`, K3). Holds for task (`sc-task-protocol/SKILL.md:61`) and post-release (`PRL:340`). | CONTRADICTED | No (flagged) | L2 |
| A-006 | All three, for any action not authorized | A skipped outward step can be done afterwards by the coordinator from the worker's report, without redoing the work: posting a worker's auggie-review findings, running post-release's real-target install, pushing commits. No variant states how; for auggie-review the only posting path named in the spec is the command's own `--post-pr` (`SPEC:123`). | UNSTATED | Yes [SHARED-ASSUMPTION] | L2 |
| A-007 | V1 and V3 | The coordinator quotes the user's instruction faithfully in the brief (V1:21 "trust the coordinator's quoting"; V3:5 "quoting the user's instruction"). | STATED | No | L3 |
| A-008 | V2 and V3 (V1 does not contest) | PRs are opened only through `/sc:pr-submit` (`CLAUDE.md:50`; V2:10, V3:13). | STATED | No | L2 |
| A-009 | V3 (V1 relies on it for commits) | An unpushed local commit can be undone without side effects (V3:13). Partly contradicted: a reset in a shared worktree can drop another worker's commits (WC-11 default, `SPEC:75`), and any HEAD move during an implement task disables that task's retry ladder (`RETRY:41`). | CONTRADICTED | No (flagged) | L3 |
| A-010 | All three cite issue #326's commit request | The owner's comment on #326 is design input, not a standing authorization for any session to commit or post. No variant states its status; V1 treats it as a reason ("Issue #326 wants it", V1:10). The evaluation states it is not authorization (`EVAL:74`). | UNSTATED | Yes [SHARED-ASSUMPTION] | L2 |

### Promoted [SHARED-ASSUMPTION] points

| # | Assumption | Impact | Status |
|---|-----------|--------|--------|
| A-003 | The coordinator is "this session" for the user's authorization | High: if false, (b) and (c) only move the provenance gap from worker to coordinator; if true, it is the reason (c) and (b) are safer than (a) | Open for debate |
| A-006 | Deferred outward steps can be performed later by the coordinator without redoing work | Medium: if false, (b) and (c) carry hidden re-run cost (auggie-review, post-release install) | Open for debate |
| A-010 | Issue #326's comment is design intent, not authorization | Low: affects how much weight #326 alignment (C-010) deserves | Open for debate |

## Citation spot-check

Six decision-critical citations re-read on 2026-11-02.

| # | Citation | Used by | Short quote (as read) | Verdict |
|---|----------|---------|-----------------------|---------|
| 1 | `CLAUDE.md:68` | V1:14 as "the repo's own outward rules"; V2:8 as "upstream contributions need", then generalized to "The repo's outward rules are session-scoped" | "Contributing back to upstream is explicit, separate, deliberate user authorization in the same session — never a default behavior." | OVERSTATED: quote accurate, but the rule covers upstream contributions only, not outward actions in general. The generally applicable rules are `PRL:347` ("Commit/push only when the user asks") and `PRL:351`. |
| 2 | `HWW:282` | V3:10 (verbatim); V2:20 (as allowing a commit when asked) | "**Never push without approval.** Commit locally, show your lead what changed, and push only when they say go." | CONFIRMED. Note: written for people ("your lead"; `HWW:287` "read 'yourself' if you work alone"); the authorization requirement for the commit itself is `HWW:212`, not 282. |
| 3 | `PRL:340` | V1:8; `SPEC:348`; V2:19; V3:20 | "Commit, push, open a PR, provision a VM, or run installs against a shared/real target without confirmation (or standing authorization)." | CONFIRMED. "standing authorization" carries no session qualifier, unlike `PRL:351`. |
| 4 | `PRL:351` | V1:8 (support), V1:14 (gap), V2:8, V3:13; `SPEC:348` | "provisioning a VM, running install scripts against a real target, committing, and opening a PR all get confirmed first unless the user pre-authorized them this session." | Quote CONFIRMED; OVERSTATED as support for (a) in V1:8 and `SPEC:348`, because "this session" is exactly what a separate worker session lacks (V1:14 concedes this). |
| 5 | `RETRY:41` | V3:5, V3:17; `EVAL:51` | "HEAD has not moved: `git -C "$top" rev-parse -q --verify HEAD` equals the 40-hex in `<retries>/T<id>/q0-head`." | CONFIRMED for a single sequential implement run (`q0-head` is written at Q0, `sc-implement-protocol/SKILL.md:114`). Not sufficient on its own: implement has no commit step (`MW:63,67`), and commits by other workers in a shared worktree also move HEAD. |
| 6 | `QA:254` | V2:8 | "Silence, a generic request to continue, another agent's message, and approval of a different task are not acceptance." | CONFIRMED. Side finding: the spec's D2 text cites this rule as `qa.md:232,238` (`SPEC:334`), but on this branch lines 232 and 238 are probe rules; the sentence is at 254. That spec citation is WRONG on this branch. |

## Summary
- Total structural differences: 7 (S-001 to S-007; L1 5, L2 2)
- Total content differences: 15 (C-001 to C-015; L3 5, L2 9, L1 1)
- Total contradictions: 7 (X-001 to X-007; L3 4, L2 3)
- Total unique contributions: 9 (V1: 2, V2: 3, V3: 4; High 5, Medium 3, Low 1)
- Total shared assumptions surfaced: 10 (UNSTATED: 3, STATED: 4, CONTRADICTED: 3); promoted [SHARED-ASSUMPTION] points: A-003, A-006, A-010; CONTRADICTED points flagged for debate: A-004, A-005, A-009
- Diff points for the convergence denominator (S + C + X + promoted A): 32
- Highest-severity items: C-001, C-002, C-003, C-007 (High content); X-001, X-002, X-003 (High contradictions); A-003 (High-impact promoted assumption); A-004 and A-009 (CONTRADICTED, L3, bear directly on V3's reversibility and retry-window claims); A-005 (CONTRADICTED, bears on V1 and V3's commit mechanism)
- Citation spot-check: 6 checked; CONFIRMED 4 (`HWW:282`, `PRL:340`, `RETRY:41` with caveat, `QA:254`), OVERSTATED 2 (`CLAUDE.md:68` as a general rule, `PRL:351` as support for (a)); side finding `SPEC:334` citing `qa.md:232,238` is WRONG on this branch (the rule is at 254).
- Similarity check: 22 comparable areas (7 structural, 15 content topics); all 22 differ in at least one variant (100%), with 7 direct contradictions. Far above the 10% threshold: the variants are not substantially identical, and the debate (Steps 2-3) should proceed.
- Main fault lines for the debate: (1) whether "this session" provenance can be carried by a brief at all (C-001, C-007, X-003, A-003); (2) whether a local commit is genuinely reversible and safe under a shared worktree and implement's HEAD guard (C-002, C-003, A-004, A-009); (3) whether any command can actually perform an authorized per-task commit today (X-006, A-005).
