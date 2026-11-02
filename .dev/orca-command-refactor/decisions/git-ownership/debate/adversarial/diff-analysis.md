# Diff Analysis: git-ownership position papers Comparison

## Metadata
- Generated: 2026-11-02T16:10:00Z (approximate, session clock)
- Variants compared: 5
  - Variant 1 = option A (coordinator runs git in its main chat), `variant-1-original.md`
  - Variant 2 = option B (workers run their own git), `variant-2-original.md`
  - Variant 3 = option C (dedicated long-lived git session, an Orca worker), `variant-3-original.md`
  - Variant 4 = option D (coordinator's Agent-tool subagent runs git), `variant-4-original.md`
  - Variant 5 = option E (hybrid: sole-writer workers may commit locally; coordinator owns all outward actions), `variant-5-original.md`
- Total differences found: 33
- Categories: structural (4), content (11), contradictions (5), unique (8), shared assumptions (5 promoted)
- Mode: A (compare existing files); depth standard; convergence threshold 0.80; focus: all.

## Structural Differences

| # | Area | V1 (A) | V2 (B) | V3 (C) | V4 (D) | V5 (E) | Severity |
|---|---|---|---|---|---|---|---|
| S-001 | Proposal form | Prose proposal | Prose proposal | Prose proposal plus "How Orca can keep it alive" mechanics section | "What D buys / What D costs" split | Per-action ownership table (action, owner, condition) | Medium |
| S-002 | Orca-mechanics coverage | None beyond queueing | None | Dedicated section (reuse, serialization, retention, depth) | Short ("No Orca overhead") | None | Medium |
| S-003 | Evidence appendix | "Self-check" section with the GITDEMO procedure | References GITDEMO | References GITDEMO | References GITDEMO | References GITDEMO | Low |
| S-004 | #326 relation | Implicit | Implicit (per-task commits) | Dedicated "Relation to #326's central relay" section | None | Implicit (per-task commits, F3) | Low |

## Content Differences

| # | Topic | V1 (A) | V2 (B) | V3 (C) | V4 (D) | V5 (E) | Severity |
|---|---|---|---|---|---|---|---|
| C-001 | Who stages and commits settled work in a shared worktree | Coordinator, explicit paths from contracts | Each worker (needs one worktree per committing worker) | Git session, explicit paths, at quiescent points | Coordinator's subagent, one at a time | Coordinator at quiescent points | High |
| C-002 | Per-task commits inside one `/sc:implement` run (#326) | Impossible until #326 K3 | Possible: worker knows task boundaries | Not solved | Not solved | Allowed for a sole-writer worker between tasks and batches, when the brief quotes the user's authorization | High |
| C-003 | Owner of push, PR, review replies, issue/status comments | Coordinator main chat | Workers (PR needs D3 (b)) | Git session (PR needs D3 (b)) | Falls back to coordinator main chat | Coordinator main chat | High |
| C-004 | Authorization path | Direct (person to actor) | Second-hand via brief (D4 (a)) | One hop via brief, per-action Task | One hop via subagent prompt | Direct for outward; quoted brief for local commits | High |
| C-005 | Audit trail | Coordinator transcript plus commits | `git log` plus scattered briefs | One Task, brief, `worker_done` and contract per action | Coordinator transcript plus subagent summary; no Orca record | Contract SHAs for worker commits; coordinator transcript for outward | Medium |
| C-006 | Context load on coordinator | Highest (diffs, messages, pr-submit loop) | Lowest for commits; merges still on coordinator | Lower (git session reads diffs) | Lower for commits; pr-submit unchanged | Middle | Medium |
| C-007 | Crash mid-commit | Stale lock; coordinator inspects | Stale lock only in that worker's worktree; retry Task must clear it | Coordinator inspects; re-issue as new Task | Subagent error returns to coordinator | Lock only in that worktree; earlier commits survive | Medium |
| C-008 | Worktree layout required | Shared allowed | One worktree per committing worker | Shared or separate (git -C) | Shared | Worker commits only as sole writer; shared worktree commits only by coordinator | Medium |
| C-009 | `/sc:pr-submit` attended loop blocking the coordinator | Accepted; messages queue durably; D3 (a) puts it after workers | Moves to worker under D3 (b) | Solved: runs in git session | Cannot help (must stay top-level) | Accepted as in A | Medium |
| C-010 | Implementation cost | Lowest (wording only) | Highest (command changes, K3, merge step) | Medium (brief template, git contract, retention) | Low (agent definition) | Spec wording; no command changes in spec phases | Medium |
| C-011 | Creation and removal of run worktrees and branches | Coordinator (implicit) | Implicit | Implicit | Implicit | Coordinator, explicit, with the F3 guard (no unmerged or open-PR branch removed without instruction) | Medium |

## Contradictions

| # | Point of Conflict | Positions | Impact |
|---|---|---|---|
| X-001 | Is a coordinator-written brief that quotes the user sufficient authorization for a worker's local commit under "commit only when asked" (`CLAUDE.md:37`)? | V2 and V5: yes, under D4 (a) quoting ("The worker's authority is the quoted instruction in its brief", V5 Safety). V1: the asking session and the acting session should be the same ("No second hop can lose, broaden or forge the authorization", V1 Safety). V4: one more hop weakens it ("Approvals pass one more hop"). | High |
| X-002 | Which audit trail is best | V3: "The audit trail is the clearest of all options: one Task per action". V1: "one transcript (the coordinator's) holds every git decision, next to the contracts it read". | Medium |
| X-003 | Where `/sc:pr-submit` runs | V3: in the git session (a worker), needing D3 (b). V1, V4, V5: coordinator main chat, matching spec D3 (a) (`SPEC:341`). V2: in workers under D3 (b). | High |
| X-004 | Meaning of Orca's review-ownership rule (`[G:cl] 62-65`) | V1 concedes it cuts against the coordinator doing PR preparation unless the user's plan names it owner. V3 and V2 imply a non-coordinator owner fits it. V5 is silent. | Medium |
| X-005 | D's "narrow tool list" benefit (intra-variant) | V4 claims a narrow allowlist as a benefit but also states Bash cannot be shown to be restrictable to git subcommands (UNVERIFIED), so the allowlist cannot stop a non-git Bash call. | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V3 (C) | Verified Orca mechanics for a persistent session: same-terminal reuse per new Task (`[G:cl] 46-55`), one active Dispatch per terminal (`[G:rc] 108`), retention only on explicit user request (`[G:rc] 157`), loop-Task forbidden by the idle rule (`[G:wc] 77-80`) | High |
| U-002 | V5 (E) | Per-action ownership table with conditions | High |
| U-003 | V5 (E) | Shared `refs/superclaude/implement/<slug>/T<id>` pins across linked worktrees: two implement runs need distinct slugs | Medium |
| U-004 | V1 (A) | GITDEMO procedure (index.lock refusal; separate per-worktree index and HEAD; shared refs) | High |
| U-005 | V2 (B) | Commits made before a crash survive (work not lost); implement parallel batches have no ladder (`SKILL.md:97`) | Medium |
| U-006 | V4 (D) | Subagents inherit the parent's permission mode; subagent work leaves no Orca record | Medium |
| U-007 | V3 (C) | Orchestration-level reading of #326's "central relay": commands cannot call a relay (SA-2, WC-8), so the relay is a session the coordinator feeds | Medium |
| U-008 | V1 (A) | Quiescence rule: never commit in a worktree while an `/sc:implement` worker runs there (HEAD-moved halt, `retry.md:41,44`); later adopted by V3 and V5 | High |

## Shared Assumptions

Agreement points found: (1) every PR goes through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`); (2) `/sc:git` cannot be the worker tool today (`cmd/git.md:90`); (3) a commit in a shared worktree moves HEAD and halts a running implement task's ladder; (4) workers share the current worktree by default (`CAPS:115`); (5) staging uses explicit paths from contracts.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All variants route authorization through "the user's instruction" given to the coordinator | The coordinator session is attended: a person is present to give, and see, each instruction. If the person gives one instruction and leaves, every option acts on an up-front authorization, so A's "same session" advantage shrinks to an up-front grant too. | UNSTATED | Yes |
| A-002 | Agreement point 5 | A settled contract's `artifacts` plus `worker_done --files-modified` lists every file the worker changed. A drive-by edit, a formatter rewrite or a generated cache missing from the list is either left uncommitted or swept by a broad `git add`. | UNSTATED | Yes |
| A-003 | Quiescence rule (V1, V3, V5) | The committer can know that a worktree is quiescent (no running worker writes there). Orca reports per-Dispatch status (`worker-list`), but no Orca verb maps worktrees to running writers; the coordinator must keep that map from its own placements. | UNSTATED | Yes |
| A-004 | All variants treat `git commit` as a pure record of existing files | A commit does not itself rewrite files. The repo's `.pre-commit-config.yaml` defines file-fixing hooks (`trailing-whitespace`, `end-of-file-fixer`, `ruff-format` at lines 9, 11, 111; `default_stages: [commit]`, line 143). They are not installed in this clone (`git rev-parse --git-common-dir`/hooks holds only samples, checked 2026-11-02), but where installed a commit can rewrite files other workers are editing, or fail. | CONTRADICTED (true here, false wherever hooks are installed) | Yes |
| A-005 | All variants say "the user's instruction" authorizes several commits | One standing instruction ("commit after each task") counts as "asked" for every later commit in the run, rather than per-commit approval. `CLAUDE.md:37` says "commit only when asked" without saying whether a standing instruction covers future commits. | UNSTATED | Yes |
| A-006 | V2, V5 | Authorized commits also stage `.dev/tasks` (`CLAUDE.md:37`). | STATED | No |
| A-007 | All | The run branch is a feature branch, never master/main (global rule 4 in `~/.claude/CLAUDE.md`). | STATED in environment, not in variants; low impact | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status | Taxonomy |
|---|---|---|---|---|---|
| A-001 | Coordinator session is attended | Authorization routing | High | Open | L3 (guard on authorization) |
| A-002 | Contract file lists are complete | Explicit-path staging | High | Open | L3 (boundary of what is staged) |
| A-003 | Quiescence is knowable | Quiescence rule | High | Open | L3 (state) |
| A-004 | A commit does not rewrite files | Commit as pure record | Medium | Contradicted where hooks are installed | L3 (state, concurrency) |
| A-005 | Standing instruction covers later commits | Authorization scope | High | Open | L3 (guard) |

## Taxonomy tagging of diff points
- L1 (surface): S-003, S-004.
- L2 (structural): S-001, S-002, C-003, C-005, C-006, C-008, C-009, C-010, C-011, X-002, X-003, X-004, X-005.
- L3 (state mechanics): C-001, C-002, C-004, C-007, X-001, A-001 to A-005.

## Summary
- Total structural differences: 4
- Total content differences: 11
- Total contradictions: 5
- Total unique contributions: 8
- Total shared assumptions surfaced: 7 (UNSTATED: 4, STATED: 2, CONTRADICTED: 1); promoted: 5
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, X-003, A-001, A-002, A-003, A-005
- Similarity check: differences far exceed 10% of comparable items; debate proceeds.
- Convergence denominator: S (4) + C (11) + X (5) + A (5) = 25 points.
