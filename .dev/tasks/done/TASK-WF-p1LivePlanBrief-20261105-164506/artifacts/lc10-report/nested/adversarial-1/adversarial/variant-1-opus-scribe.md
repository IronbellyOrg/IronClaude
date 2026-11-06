# Requirements: naming report directories for parallel Orca workers

Variant 1, persona: scribe (documentation clarity, decision rationale, audit trail).

## Purpose and sources

An Orca coordinator gives each worker Task exactly one report directory. The worker writes `<report-dir>/return-contract.yaml` there. The worker contract requires that this directory is unique to the Task, known before dispatch and never reused by a retry. It does not say how to name the directory, so each brief makes up its own name. This specification fixes one pattern and records why each part exists.

Sources read for this variant:

- `~/.claude/WORKER-CONTRACT.md`: WC-4, WC-6, WC-11, section 1 (report directory, nested propagation rule), section 4 (brief contents, child worktrees, worked example), section 5 (brief template).
- `.dev/p1-live/brainstorm/seed-brief.md`: constraints, success criteria, open questions.
- `.dev/p1-live/brainstorm/enrichment/codebase-context.md`: naming schemes already used in the repository.

## Recommended pattern

```text
.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/
```

| Part | Meaning | Chosen by | When |
|---|---|---|---|
| `.dev/orca/` | fixed root for all coordinator report directories | this specification | fixed |
| `<runStamp>` | UTC `YYYYMMDD-HHMMSS` when the coordinator started planning the run | coordinator | before the first Task |
| `<runSlug>` | camelCase name of the run, at most 16 characters | coordinator | before the first Task |
| `<command>` | `/sc:` command name without the prefix (`tdd`, `troubleshoot`) | coordinator | when writing the brief |
| `<subject>` | camelCase name of this piece of work, at most 16 characters, unique within the run | coordinator | when writing the brief |
| `<attempt>` | `1` for the first Task of this piece of work, plus one for each retry | coordinator | when writing the brief |

Rationale, part by part:

- **Date once, at run level.** Every generated scheme in the repository pairs a readable subject with a timestamp or counter (`.dev/brainstorms/<ts>-<slug>/`, `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`; codebase-context, "Naming schemes already in use"). Putting the stamp on the run folder, not on each Task, keeps Task names short and groups one run's reports together. The stamp is the coordinator's own time, which satisfies "known before dispatch" (codebase-context, "Observations").
- **Readable subject plus counter, not the Task ID.** The seed brief's success criteria ask that a reader can tell the command and attempt from the name. A Task ID is opaque, and whether `task-create` returns the ID before the spec is stored is UNVERIFIED. The Task ID is recorded next to the name instead (FR-009).
- **Attempt in the name, not a parent folder.** This matches the contract's worked example, `.dev/tdd/auth-1/` then `.dev/tdd/auth-2/` (WORKER-CONTRACT section 4). Siblings make the history of one piece of work visible in a single listing.

## Functional requirements

- **FR-001. One directory per Task.** Each Task's brief names exactly one report directory, passed as `--report-dir` or the command's own directory-valued output flag, never both. Depends on: WC-4; section 1, "Report directory".
- **FR-002. Name fixed before dispatch.** Every part of the name comes from information the coordinator holds when it writes the brief. No part may come from the worker at run time. Depends on: WC-4; seed brief, Constraints.
- **FR-003. Unique within the run.** `<command>-<subject>` is unique among the run's pieces of work. The coordinator records each name in its placement map before calling `task-create`, so two Tasks dispatched at the same moment cannot share a name. Neither worker has to look at the other. Depends on: WC-11; section 4, "placement map".
- **FR-004. Retry gets the next attempt number.** A retry is a new Task (WC-6) and uses the same `<command>-<subject>` with `<attempt>` raised by one. The earlier directory is never written again, so its contract stays untouched. Depends on: WC-6; worked example steps 4 and 5.
- **FR-005. Attempts stay visible to the circuit breaker.** Because only `<attempt>` changes between retries, the coordinator can compare command lines with the report directory removed and apply the three-failed-starts limit. A brief that changes only the attempt number is not new work. Depends on: WC-6, first bullet.
- **FR-006. Existing contract blocks reuse.** Before dispatch the coordinator confirms the chosen directory has no `return-contract.yaml`. If one exists, it raises `<attempt>` and never deletes the old file. The command's own refusal stays as the last safety check. Depends on: WC-4; seed brief, Q4.
- **FR-007. Allowed characters and places.** Name parts use only `A-Z a-z 0-9` and `-`. `<runSlug>` and `<subject>` follow the workflow package's limit of at most 16 camelCase characters. The path stays under `.dev/`, never inside `.git/`, `.codegraph/` or a distributable `.claude/` folder, and never under `.dev/tasks/`, so it does not mix with the always-staged task tree. Depends on: WC-11 ("goes under `.dev/`"); seed brief, Constraints; `.dev/README.md:47` (as cited in codebase-context).
- **FR-008. Nested commands keep the contract's rule.** A command that invokes another command under `--unattended` writes the nested report to `<report-dir>/nested/<command>-<n>/`, with `<n>` counted from 1 and never reused. This specification adds nothing to that rule. Depends on: section 1, "Nested propagation rule".
- **FR-009. Audit record per name.** For every report directory the coordinator's run notes hold one line: directory, Task ID, command line, worktree, and for a retry the replaced Task ID. The brief of a retry also carries `replaces <old Task ID>`. This is how a reader links an opaque Task ID to a readable name. Depends on: WC-6 ("recording the old Task ID"); section 4, worked example step 4.
- **FR-010. Child worktrees keep the relative part.** A Task placed in a child worktree gets the absolute path `<child root>/.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/`. The part after the child root is the same as it would be in the feature worktree, so names stay unique across worktrees, and merge-back does not collide. Depends on: section 4, "Feature worktree and child worktrees".
- **FR-011. Fixed per-check names gain an attempt suffix.** A plan that uses one fixed directory per check (the P1 live plan's `.dev/p1-live/<command-name>/`) adds `-1` from the first run, so a re-run becomes `-2` without renaming the first. Depends on: seed brief, Q3 and open question 4; WC-6.

## Worked examples

Run started 2026-11-05 19:56:00 UTC, run slug `p1Live`.

| Situation | Report directory |
|---|---|
| First `/sc:tdd` for the auth service | `.dev/orca/20261105-195600-p1Live/tdd-auth-1/` |
| Retry after a blocked gate (replaces T1) | `.dev/orca/20261105-195600-p1Live/tdd-auth-2/` |
| Three parallel troubleshoot workers | `.../troubleshoot-hookTimeout-1/`, `.../troubleshoot-hookOrder-1/`, `.../troubleshoot-hookEnv-1/` |
| Merge of those three | `.../adversarial-hookMerge-1/` |
| Workflow's nested adversarial call inside attempt 1 | `.../workflow-orcaNaming-1/nested/adversarial-1/` |
| `/sc:implement` in a child worktree | `/abs/child/.dev/orca/20261105-195600-p1Live/implement-authPlan-1/` |

Run-notes line for the retry (FR-009):

```text
.dev/orca/20261105-195600-p1Live/tdd-auth-2/ | T2 | /sc:tdd "token-based login service..." --unattended --report-dir ... | feature worktree | replaces T1
```

## Decisions on the open questions

| Open question (seed brief) | Decision | Reason |
|---|---|---|
| Task ID or slug plus counter | Slug plus counter in the name; Task ID in run notes | Readable; Task ID before spec storage is UNVERIFIED |
| Attempt in name or parent folder | In the name | Matches the contract's worked example |
| Where the date goes | Once, on the run folder | Matches repository practice; keeps Task names short |
| Fixed per-check names | Valid only with `-1` from the start | A re-run otherwise has no free name |

## Open risks

- **R1. Counter lives in the coordinator's memory.** If the coordinator session is resumed and its run notes are lost, it could reuse an attempt number. FR-006 catches this only when the earlier attempt wrote a contract. A guard-refused attempt writes none (WORKER-CONTRACT section 1, "Brief guard"), so its directory may be empty, and reuse is then harmless but breaks the audit trail.
- **R2. Subject collisions are a convention, not a mechanism.** Nothing in Orca enforces FR-003. Two coordinators sharing one worktree with the same run stamp and slug could collide. Whether two coordinators can run in one feature worktree is UNVERIFIED.
- **R3. Commands with their own fixed deliverables.** Workflow's `TASK-WF-*` package and cleanup-audit's `.claude-audit/` land outside the report directory (WC-4). Parallel runs of such commands can still collide there; this pattern protects only `return-contract.yaml`.
- **R4. Root choice `.dev/orca/` is new.** No existing file names this root. It may conflict with a convention a reviewer prefers (for example per-command roots like `.dev/tdd/`). UNVERIFIED whether any tooling scans `.dev/` by folder name.
- **R5. Path length.** Deep nesting inside a child worktree's absolute path is untested against tool path limits. UNVERIFIED.
