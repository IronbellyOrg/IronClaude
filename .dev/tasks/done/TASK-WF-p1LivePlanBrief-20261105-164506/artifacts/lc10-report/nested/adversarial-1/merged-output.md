<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 2 (sonnet:analyzer) -->
<!-- Incorporated: Variant 1 (opus:scribe), per refactor-plan.md Changes 1 to 5 -->
<!-- Merge date: 2026-11-05 -->

# Requirements: naming report directories for parallel workers

<!-- Source: Base (original, modified) - second sentence added so the evidence statement covers the files cited by FR-017 (Change 1) -->
Persona: analyzer. Evidence sources: `seed-brief.md`, `enrichment/codebase-context.md`, and `~/.claude/WORKER-CONTRACT.md` (cited as WC-n or by section). Anything I could not confirm from those three files is marked UNVERIFIED. This merged version also cites `src/superclaude/commands/reflect.md`, `src/superclaude/commands/brainstorm.md` and `.dev/README.md` (FR-017), whose lines were checked during the debate.

## Problem and root cause

<!-- Source: Base (original) -->
The contract requires one report directory per Task, known before dispatch, never shared, never reused by a retry (WC-4, WC-6, WC-11), but fixes no format. The only enforcement today is after the fact: a command refuses a directory that already holds a `return-contract.yaml` (WC-4). So a collision is caught late, as a failed worker, not prevented by the coordinator.

The root cause of any collision is that uniqueness is left to each brief author. Uniqueness is cheapest where one party holds all the state: the coordinator is the only party that sees every Task before dispatch (section 4), so it must be the sole source of the name. Workers cannot be the source, because the path must exist before the worker starts (WC-4).

## Recommended pattern

<!-- Source: Base (original, modified) - last sentence added to point at the UNRESOLVED date and root decisions (Changes 1 and 5) -->
```text
.dev/<command>/<subject>-<n>/
```

- `<command>`: the command name without `/sc:` (`tdd`, `troubleshoot`, `adversarial`).
- `<subject>`: a short lowercase kebab slug of the logical piece of work, characters `[a-z0-9-]`, at most 24 characters.
- `<n>`: the attempt number, a positive integer starting at 1, held by the coordinator per (command, subject) and never reused.

This is the contract's own worked example generalized (`.dev/tdd/auth-1/`, retry `.dev/tdd/auth-2/`; section 4). It carries command, work and attempt in the name, uses only information the coordinator holds when it writes the brief, and needs no timestamp and no Orca Task ID. The seed brief's open questions resolve as follows: readable slug plus counter (not Task ID); attempt in the name (not a parent folder); no date in the name; a fixed per-check name is not enough once a check can re-run. The date answer and the root folder for some commands are UNRESOLVED: see "Decisions on the open questions", FR-017 and "Unresolved conflicts".

## Decisions on the open questions

<!-- Source: Variant 1 (opus:scribe), Decisions on the open questions, merged per Change #5 (answers are the base's; the date and subject-style rows are UNRESOLVED) -->
| Open question (seed brief) | Base answer | Reason | Status |
|---|---|---|---|
| Task ID or slug plus counter | Readable slug plus counter in the name; Task ID in the brief and the run notes (FR-008, FR-018) | A reader can tell command and attempt from the name; whether `task-create` returns the ID before the spec is stored is UNVERIFIED | Agreed by both variants |
| Attempt in the name or in a parent folder | In the name (`<subject>-<n>`) | Matches the contract's worked example (`.dev/tdd/auth-1/`, then `.dev/tdd/auth-2/`) | Agreed by both variants |
| Where the date goes | No date in the name (FR-009) | Git history and the contract carry time | UNRESOLVED (C-002). Variant 1 alternative: one UTC `YYYYMMDD-HHMMSS` stamp, chosen by the coordinator before the first Task, on a run folder (FR-017 Option A) |
| Fixed per-check names | Not enough on their own; add `-1` from the first run (FR-019) | A fixed name has no free name for a re-run | Agreed by both variants |
| Subject style (not a seed question; diff point C-006) | Lowercase kebab `[a-z0-9-]`, at most 24 characters; subjects better kept free of trailing digits (open risk 3) | The base states no reason beyond the trailing-digit warning | UNRESOLVED (C-006). Variant 1 alternative: camelCase, at most 16 characters, matching the workflow package rule (`.dev/README.md:47`) |

## Functional requirements

<!-- Source: Base (original, modified) - "single token" wording aligned with the new FR-011 (consequence of Change #2) -->
**FR-001. The coordinator alone assigns the directory.** It writes the full path into the brief's `Report directory:` slot and into the `--report-dir` or `--output` token of the `Command:` line, and into any file path inside that directory that the line also passes (FR-011). Depends on: WC-4 (known before dispatch), section 5 template slot.

<!-- Source: Base (original) -->
**FR-002. Name = `<command>-subject-attempt` as above, and uniqueness is global to the run.** No two Tasks of one coordinator run share a relative path, even when they run in different worktrees. Reason: child branches are merged back into the feature branch (section 4, "Feature worktree and child worktrees"); two children that both wrote `.dev/tdd/auth-1/` would collide at merge, and WC-11 only guarantees separation inside one worktree. Depends on: WC-11, section 4.

**FR-003. Simultaneous dispatch needs no cross-worker lookup.** The coordinator assigns names serially from its own placement map, so Tasks created in the same moment still differ. Workers never inspect each other's directories. Depends on: seed-brief success criterion 1; section 4 placement map.

**FR-004. Fan-out siblings differ in `<subject>`, not in `<n>`.** N parallel workers on one command (for example N `/sc:troubleshoot` lenses feeding `/sc:adversarial --compare`, fan-in rule) each get a distinct subject token (`auth-lens-a`, `auth-lens-b`). `<n>` counts attempts at one piece of work only. This keeps "which attempt" and "which sibling" readable and separate. Depends on: section 4 fan-in rule.

<!-- Source: Base (original, modified) - recovery of the attempt number moved from the directory listing to written run notes and Task specs, per Change #3 (Variant 1 R1) -->
**FR-005. The coordinator checks the path is free before dispatch, and takes the attempt number from its written records.** It confirms in the target worktree that the directory does not exist, or exists empty. A refusal by the command (existing `return-contract.yaml`) is a backstop, not the check. A free directory does not prove that its attempt number is unused: a guard-refused attempt (FR-012) runs nothing, writes no contract and may leave no directory (WORKER-CONTRACT section 1, "Brief guard"). So the next `<n>` comes from the coordinator's written run notes (FR-018) and from the Task specs, whose briefs carry each report directory; the directory listing is only a cross-check. Depends on: WC-4, FR-012, FR-018.

<!-- Source: Base (original) -->
**FR-006. Forbidden locations.** The root never lies inside `.git/`, `.codegraph/`, or a distributable `.claude/` folder (skills, agents, commands), which the command refuses (seed-brief constraints; WC-4 gives the refusal behaviour). Never place report directories under `.claude/skills/*-workspace/` (project CLAUDE.md). Use `.dev/`, which WC-11 names for shared-worktree reports.

**FR-007. No worker-derived parts.** The name never contains the worker's run-time timestamp, Dispatch ID, or anything learned after `worker-start`. Dispatch ID is known only after `worker-start` returns ready (WC-6, last bullet). Depends on: WC-4, WC-6.

<!-- Source: Variant 1 (opus:scribe), R4 and Recommended pattern (dedicated root), with the Variant 2 advocate's reserved-name concession, merged per Change #1 -->
**FR-017. Report directories never sit directly in a folder another tool owns.** A coordinator report directory must not be placed directly inside a folder that a command already uses as its default output, or that the repository preserves for another purpose. Verified cases:

- `src/superclaude/commands/reflect.md:101` makes `.dev/reflect/<mode>-<slug>-<ts>/` the default output of `reflect`.
- `.dev/README.md:63` lists `.dev/workflow/<slug>/` and `.dev/implement/` (path-hashed ledgers) as preserved legacy locations. Current workflow ledgers sit inside the plan package (`.dev/README.md:54`).
- `src/superclaude/commands/brainstorm.md:62` makes `.dev/brainstorms/<ts>-<slug>/` the brainstorm default.

Under the plain pattern `.dev/<command>/<subject>-<n>/`, report directories of `reflect`, `workflow` and `implement` would land directly in `.dev/reflect/`, `.dev/workflow/` and `.dev/implement/`. Two candidate fixes are recorded; neither is chosen:

- **Option A (Variant 1).** A dedicated root for every command: `.dev/orca/<runStamp>-<runSlug>/<command>-<subject>-<attempt>/`. It brings Variant 1's run stamp, which conflicts with FR-009 (C-002). The root `.dev/orca/` is new; whether any tooling scans `.dev/` by folder name is UNVERIFIED.
- **Option B (Variant 2).** Keep `.dev/<command>/<subject>-<n>/` and give the reserved commands a parent folder that no tool owns. The folder name is to be decided by the person.

Status: UNRESOLVED. The debate did not converge on this point (C-001, X-001, A-002 in "Unresolved conflicts"), and unattended mode cannot ask. Depends on: WC-11 (`.dev/`); FR-006.

<!-- Source: Base (original, modified) - run-notes line format now defined by FR-018, per Change #3 -->
**FR-008. Task ID is recorded, not embedded.** The Task ID is written in the brief (`replaces T1` on a retry) and in the coordinator's run notes next to the path, in the line format of FR-018, not put in the directory name. Whether `task-create` can return the ID before the spec (the brief) is stored is UNVERIFIED (seed brief; `codebase-context.md` observations), so a name built from it cannot be relied on.

<!-- Source: Variant 1 (opus:scribe), FR-009 "Audit record per name" and its run-notes example, merged per Change #3 -->
**FR-018. One run-notes line per report directory.** For every report directory the coordinator's run notes hold one line: directory, Task ID, command line, worktree, and for a retry the replaced Task ID. The brief of a retry also carries `replaces <old Task ID>`. This is how a reader links an opaque Task ID to a readable name, and it is the record that FR-005 and open risk 2 use to recover the counter. Depends on: WC-6 ("recording the old Task ID"); section 4, worked example step 4.

Example line for a retry (the path follows the base pattern; it changes if FR-017 Option A is chosen):

```text
.dev/tdd/auth-2/ | T2 | /sc:tdd ... --unattended --report-dir .dev/tdd/auth-2/ | feature worktree | replaces T1
```

<!-- Source: Base (original) -->
**FR-009. Date is excluded.** Git history and the contract carry time. This differs from `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` (`.dev/README.md:47`, as cited in `codebase-context.md`), which names a package a command generates, not a coordinator-assigned report directory.

## Retries

<!-- Source: Base (original) -->
**FR-010. Every retry gets `<n>+1` and a new Task.** Never `worker-start --retry-of`, never reuse the old directory. The old contract stays untouched. Depends on: WC-6; worked example (`auth-1` then `auth-2`).

<!-- Source: Variant 1 (opus:scribe), FR-005 "Attempts stay visible to the circuit breaker", merged per Change #2 (replaces base FR-011) -->
**FR-011. Only the attempt number changes between retries.** The coordinator must itself decide whether a retry is "unchanged apart from its report-directory value" (WC-6, circuit-breaker bullet; Orca counts failures only per Task). Between retries only the attempt number changes. The path can appear more than once on the `Command:` line: the contract's own example passes `--output .dev/tdd/auth-1/tdd.md --report-dir .dev/tdd/auth-1/` (WORKER-CONTRACT.md line 159). Before it compares command lines for the three-failed-starts limit, the coordinator removes every path token that carries the attempt number (the directory and any file path inside it). After three failed starts with an otherwise identical line, no fourth Task is created. Depends on: WC-6; WORKER-CONTRACT.md line 159.

<!-- Source: Base (original) -->
**FR-012. Brief-guard refusals consume attempts.** A `guard refused:` result ran nothing, but the fix is still a new Task with a new `<n>`; the limit is 2 brief fixes (3 attempts) for the same work. Depends on: section 4, "Reading a result".

**FR-013. A WC-3 re-invocation keeps the directory.** This is the one case where the same path is reused: the worker re-runs the command in the same session with the same report directory after `ask`, and the second contract replaces the blocked one whole. It is not a retry. Depends on: WC-3.

<!-- Source: Variant 1 (opus:scribe), FR-011 "Fixed per-check names gain an attempt suffix", merged per Change #4 (moved from base open risk 1) -->
**FR-019. Fixed per-check names gain an attempt suffix.** A plan that uses one fixed directory per check (the P1 live plan's `.dev/p1-live/<command-name>/`, cited in `codebase-context.md`, from the P1 plan lines 73 to 565, not re-read by me) adds `-1` from the first run, so a re-run becomes `-2` without renaming the first. A fixed name such as `.dev/p1-live/impact/` has no free name for a re-run. Renaming paths already in the P1 plan is a plan edit outside this spec. Depends on: seed brief, Q3 and open question 4; WC-6.

## Nested commands

<!-- Source: Base (original) -->
**FR-014. Nested directories live inside the parent.** A command that calls another command under `--unattended` passes `<report-dir>/nested/<command>-<n>/`, `<n>` from 1, never reused. The coordinator does not name these and does not count them toward its own counter. Depends on: section 1, nested propagation rule; WC-4, WC-11. Because the parent directory is unique (FR-002), nested paths are unique without further coordination.

## Child worktrees

<!-- Source: Base (original) -->
**FR-015. A Task in a child worktree gets an absolute path inside that child.** The coordinator reads it by absolute path before merge-back. The relative part still follows FR-002. Depends on: section 4, "Feature worktree and child worktrees".

**FR-016. Staging and merge-back.** Report directories under `.dev/tasks/` are always staged by the coordinator; other `.dev/` report directories are outside that rule (seed brief constraints). Whether child report directories should be merged into the feature branch or discarded with the child is not stated in the contract. UNVERIFIED; the coordinator decides per run and records it in the placement map.

## Worked examples

<!-- Source: Base (original) -->
| Case | Directory |
|---|---|
| First TDD for auth | `.dev/tdd/auth-1/` |
| TDD hit a blocked gate; answer known | `.dev/tdd/auth-2/` (new Task, brief says `replaces T1`) |
| Three troubleshoot lenses at once | `.dev/troubleshoot/auth-lens-a-1/`, `.dev/troubleshoot/auth-lens-b-1/`, `.dev/troubleshoot/auth-lens-c-1/` |
| Fan-in merge of those | `.dev/adversarial/auth-compare-1/`; its own nested call: `.dev/adversarial/auth-compare-1/nested/<command>-1/` |
| Task in a child worktree | `<child worktree path>/.dev/tdd/billing-1/` (absolute) |
| P1 live check `impact`, first run | `.dev/p1-live/impact-1/` (today: `.dev/p1-live/impact/`) |

## Open risks

<!-- Source: Base (original, modified) - risk 1 now points to FR-019 (Change #4); risk 2 recovery wording changed (Change #3); risks 3 to 6 unchanged -->
1. **Fixed names in the P1 live plan.** The `-1` suffix is now a requirement (FR-019). The remaining risk: the P1 live plan's `.dev/p1-live/<command-name>/` (cited in `codebase-context.md`, from the P1 plan lines 73 to 565, not re-read by me) keeps its fixed names until the plan is edited, and renaming existing planned paths is a plan edit outside this spec.
2. **Coordinator state loss.** The counter lives in the coordinator's written run notes (FR-018). If the coordinator session is lost, the next one must recover the highest `<n>` from those run notes and from the Task specs, whose briefs carry each report directory, and must not trust memory. Listing the directories (FR-005) is only a cross-check, because a guard-refused attempt can leave no directory (FR-012). The contract does not say where run notes persist. UNVERIFIED. Whether Orca lets a replacement coordinator list the Task specs is also UNVERIFIED.
3. **Subject ambiguity.** A subject ending in digits (`oauth2`) reads `oauth2-1`; the rule is that the last `-<digits>` is the attempt. Subjects are better kept free of trailing digits.
4. **Slug quality.** Two different pieces of work that shorten to the same slug would share a counter and look like retries. The coordinator must keep subject distinct per logical work item (FR-004).
5. **Merge-back policy** for child report directories (FR-016) is undecided.
6. **Default-path commands.** Some commands put their own deliverable at a generated location (workflow's `TASK-WF-*` package, cleanup-audit's `.claude-audit/`; WC-4). The report directory is separate from that deliverable and its contract points at it; two Tasks of those commands can still collide on the generated location. Whether the command guards against that is UNVERIFIED.

## Unresolved conflicts

<!-- Source: debate-transcript.md, Scoring Matrix and Convergence Assessment (6 unresolved diff points); positions are the two advocates' Round 1 verdicts -->
The debate reached 62.5% agreement (10 of 16 points) against a 75% threshold. These six points have no winner; this document records both positions and chooses neither.

| Point | What it is about | Variant 1 advocate (opus:scribe) | Variant 2 advocate (sonnet:analyzer) |
|---|---|---|---|
| S-001 | How the document opens (section order) | MERGE, 60%: keep Variant 2's root-cause opening and add Variant 1's sources list | Variant 2, 55%: start from the root cause (collision caught late by WC-4) |
| C-001 | Root folder shape | MERGE, 70%: Variant 1's dedicated root and run folder, with the shared `<command>-<subject>-<n>` leaf | Variant 2, 62%: per-command root that matches the contract's worked example, patched with a reserved-name rule |
| C-002 | Date in the path | Variant 1, 65%: one coordinator-chosen UTC stamp per run separates runs and is known before dispatch | Variant 2, 58%: no date; time is in git history, and a run stamp is extra state the contract never asks for |
| C-006 | Subject style | Variant 2, 55%: lowercase kebab, at most 24 characters, avoids case-sensitivity problems | Variant 1, 60%: camelCase, at most 16 characters, matches `.dev/README.md:47` |
| X-001 | Clash with folders other tools own under `.dev/` | Variant 1, 80%: the clash is verified, so use a separate root | MERGE, 60%: the overlap shown by `.dev/README.md:63` is real but legacy-only; keep per-command roots and add a reserved-name rule |
| A-002 | Assumption that a per-command root under `.dev/` is free | Variant 1, 75%: a separate root avoids the verified clash; its own safety is UNVERIFIED | MERGE, 62%: the risk is real but narrow; a reserved-name rule fixes it without a new root |

C-001, X-001 and A-002 share one cause, the choice of root folder; FR-017 records the two fixes. C-002 and C-006 appear as UNRESOLVED rows in "Decisions on the open questions".
