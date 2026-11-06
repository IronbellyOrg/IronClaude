# Requirements: naming report directories for parallel workers

Persona: analyzer. Evidence sources: `seed-brief.md`, `enrichment/codebase-context.md`, and `~/.claude/WORKER-CONTRACT.md` (cited as WC-n or by section). Anything I could not confirm from those three files is marked UNVERIFIED.

## Problem and root cause

The contract requires one report directory per Task, known before dispatch, never shared, never reused by a retry (WC-4, WC-6, WC-11), but fixes no format. The only enforcement today is after the fact: a command refuses a directory that already holds a `return-contract.yaml` (WC-4). So a collision is caught late, as a failed worker, not prevented by the coordinator.

The root cause of any collision is that uniqueness is left to each brief author. Uniqueness is cheapest where one party holds all the state: the coordinator is the only party that sees every Task before dispatch (section 4), so it must be the sole source of the name. Workers cannot be the source, because the path must exist before the worker starts (WC-4).

## Recommended pattern

```text
.dev/<command>/<subject>-<n>/
```

- `<command>`: the command name without `/sc:` (`tdd`, `troubleshoot`, `adversarial`).
- `<subject>`: a short lowercase kebab slug of the logical piece of work, characters `[a-z0-9-]`, at most 24 characters.
- `<n>`: the attempt number, a positive integer starting at 1, held by the coordinator per (command, subject) and never reused.

This is the contract's own worked example generalized (`.dev/tdd/auth-1/`, retry `.dev/tdd/auth-2/`; section 4). It carries command, work and attempt in the name, uses only information the coordinator holds when it writes the brief, and needs no timestamp and no Orca Task ID. The seed brief's open questions resolve as follows: readable slug plus counter (not Task ID); attempt in the name (not a parent folder); no date in the name; a fixed per-check name is not enough once a check can re-run.

## Functional requirements

**FR-001. The coordinator alone assigns the directory.** It writes the full path into the brief's `Report directory:` slot and into the single `--report-dir` or `--output` token of the `Command:` line. Depends on: WC-4 (known before dispatch), section 5 template slot.

**FR-002. Name = `<command>-subject-attempt` as above, and uniqueness is global to the run.** No two Tasks of one coordinator run share a relative path, even when they run in different worktrees. Reason: child branches are merged back into the feature branch (section 4, "Feature worktree and child worktrees"); two children that both wrote `.dev/tdd/auth-1/` would collide at merge, and WC-11 only guarantees separation inside one worktree. Depends on: WC-11, section 4.

**FR-003. Simultaneous dispatch needs no cross-worker lookup.** The coordinator assigns names serially from its own placement map, so Tasks created in the same moment still differ. Workers never inspect each other's directories. Depends on: seed-brief success criterion 1; section 4 placement map.

**FR-004. Fan-out siblings differ in `<subject>`, not in `<n>`.** N parallel workers on one command (for example N `/sc:troubleshoot` lenses feeding `/sc:adversarial --compare`, fan-in rule) each get a distinct subject token (`auth-lens-a`, `auth-lens-b`). `<n>` counts attempts at one piece of work only. This keeps "which attempt" and "which sibling" readable and separate. Depends on: section 4 fan-in rule.

**FR-005. The coordinator checks the path is free before dispatch.** It confirms in the target worktree that the directory does not exist, or exists empty. A refusal by the command (existing `return-contract.yaml`) is a backstop, not the check. Depends on: WC-4.

**FR-006. Forbidden locations.** The root never lies inside `.git/`, `.codegraph/`, or a distributable `.claude/` folder (skills, agents, commands), which the command refuses (seed-brief constraints; WC-4 gives the refusal behaviour). Never place report directories under `.claude/skills/*-workspace/` (project CLAUDE.md). Use `.dev/`, which WC-11 names for shared-worktree reports.

**FR-007. No worker-derived parts.** The name never contains the worker's run-time timestamp, Dispatch ID, or anything learned after `worker-start`. Dispatch ID is known only after `worker-start` returns ready (WC-6, last bullet). Depends on: WC-4, WC-6.

**FR-008. Task ID is recorded, not embedded.** The Task ID is written in the brief (`replaces T1` on a retry) and in the coordinator's run notes next to the path, not put in the directory name. Whether `task-create` can return the ID before the spec (the brief) is stored is UNVERIFIED (seed brief; `codebase-context.md` observations), so a name built from it cannot be relied on.

**FR-009. Date is excluded.** Git history and the contract carry time. This differs from `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` (`.dev/README.md:47`, as cited in `codebase-context.md`), which names a package a command generates, not a coordinator-assigned report directory.

## Retries

**FR-010. Every retry gets `<n>+1` and a new Task.** Never `worker-start --retry-of`, never reuse the old directory. The old contract stays untouched. Depends on: WC-6; worked example (`auth-1` then `auth-2`).

**FR-011. The directory value is one isolated token.** Because the coordinator must itself decide whether a retry is "unchanged apart from its report-directory value" (WC-6, circuit-breaker bullet; Orca counts failures only per Task), the `Command:` line should contain the path exactly once, so the comparison strips one token. After three failed starts with an otherwise identical line, no fourth Task is created. Depends on: WC-6.

**FR-012. Brief-guard refusals consume attempts.** A `guard refused:` result ran nothing, but the fix is still a new Task with a new `<n>`; the limit is 2 brief fixes (3 attempts) for the same work. Depends on: section 4, "Reading a result".

**FR-013. A WC-3 re-invocation keeps the directory.** This is the one case where the same path is reused: the worker re-runs the command in the same session with the same report directory after `ask`, and the second contract replaces the blocked one whole. It is not a retry. Depends on: WC-3.

## Nested commands

**FR-014. Nested directories live inside the parent.** A command that calls another command under `--unattended` passes `<report-dir>/nested/<command>-<n>/`, `<n>` from 1, never reused. The coordinator does not name these and does not count them toward its own counter. Depends on: section 1, nested propagation rule; WC-4, WC-11. Because the parent directory is unique (FR-002), nested paths are unique without further coordination.

## Child worktrees

**FR-015. A Task in a child worktree gets an absolute path inside that child.** The coordinator reads it by absolute path before merge-back. The relative part still follows FR-002. Depends on: section 4, "Feature worktree and child worktrees".

**FR-016. Staging and merge-back.** Report directories under `.dev/tasks/` are always staged by the coordinator; other `.dev/` report directories are outside that rule (seed brief constraints). Whether child report directories should be merged into the feature branch or discarded with the child is not stated in the contract. UNVERIFIED; the coordinator decides per run and records it in the placement map.

## Worked examples

| Case | Directory |
|---|---|
| First TDD for auth | `.dev/tdd/auth-1/` |
| TDD hit a blocked gate; answer known | `.dev/tdd/auth-2/` (new Task, brief says `replaces T1`) |
| Three troubleshoot lenses at once | `.dev/troubleshoot/auth-lens-a-1/`, `.dev/troubleshoot/auth-lens-b-1/`, `.dev/troubleshoot/auth-lens-c-1/` |
| Fan-in merge of those | `.dev/adversarial/auth-compare-1/`; its own nested call: `.dev/adversarial/auth-compare-1/nested/<command>-1/` |
| Task in a child worktree | `<child worktree path>/.dev/tdd/billing-1/` (absolute) |
| P1 live check `impact`, first run | `.dev/p1-live/impact-1/` (today: `.dev/p1-live/impact/`) |

## Open risks

1. **Fixed names in the P1 live plan.** `.dev/p1-live/<command-name>/` (cited in `codebase-context.md`, from the P1 plan lines 73 to 565, not re-read by me) has no attempt suffix, so a re-run of a check would either collide or need an ad hoc name. Recommendation: add `-1` from the start; renaming existing planned paths is a plan edit outside this spec.
2. **Coordinator state loss.** The counter lives in the coordinator's run notes. If the coordinator session is lost, the next one must recover the highest `<n>` by listing the directories (FR-005) and must not trust memory. The contract does not say where run notes persist. UNVERIFIED.
3. **Subject ambiguity.** A subject ending in digits (`oauth2`) reads `oauth2-1`; the rule is that the last `-<digits>` is the attempt. Subjects are better kept free of trailing digits.
4. **Slug quality.** Two different pieces of work that shorten to the same slug would share a counter and look like retries. The coordinator must keep subject distinct per logical work item (FR-004).
5. **Merge-back policy** for child report directories (FR-016) is undecided.
6. **Default-path commands.** Some commands put their own deliverable at a generated location (workflow's `TASK-WF-*` package, cleanup-audit's `.claude-audit/`; WC-4). The report directory is separate from that deliverable and its contract points at it; two Tasks of those commands can still collide on the generated location. Whether the command guards against that is UNVERIFIED.
