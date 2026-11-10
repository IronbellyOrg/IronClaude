review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review of the full document; not a re-review)
- reviewer model used: claude-sonnet-5-5
- lint: `.dev/orca-command-refactor/review/lint-1.md:1-5` (sha256 of the candidate matches the header at line 1; checks REF; findings 0). There is no lint id to confirm or dismiss. Nothing in the lint file is graded.
- evidence limit: the workspace holds only `.dev/orca-command-refactor/`. Every citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/evals/`, `.dev/codegraph-migration/`, `~/.claude` or `orca-ide` output cannot be opened here and is UNVERIFIED unless the inventories quote it. I checked the spec's `INV-A`, `INV-B`, `CAPS` lines that bear on the findings below against `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`; they match what the spec says unless a finding says otherwise.
- coverage: whole spec read (lines 1-286): sections 1-9, Decisions and UNVERIFIED. Counts re-derived: section 3.1 has 10 rows, section 3.2 has 27 rows, section 4 has 6 rows (43 total); phase assignment 9 (P1) + 15 (P2, including reflect, release-split, tdd, troubleshoot) + 4 (P3) + 3 (P4) matches section 6. Panel run in the fixed order with Whittaker's attack pass; focus experts Wiegers, Adzic, Cockburn (requirements) and Fowler, Newman, Hohpe, Nygard (architecture).

## Grading check (blocking findings only)

Each blocking finding carries the sentence required by the grading check.

## Open blocking findings

### B1. Phase 1 acceptance test demands changes to commands whose Phase 4 depends on user decisions D2-D4

- severity: CRITICAL-by-consequence (two stated texts contradict); expert: Wiegers, Whittaker (Sequence Attack)
- cited texts:
  - `specs/orca-worker-contract-spec.md:159` P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - `specs/orca-worker-contract-spec.md:195` AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
  - `specs/orca-worker-contract-spec.md:154` "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
  - `specs/orca-worker-contract-spec.md:240` D3 (a), the recommended option: "no pr-submit changes in Phase 4"; `specs/orca-worker-contract-spec.md:139` "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
  - Section 3.2 rows for `implement` (line 109), `post-release` (line 113) and `pr-submit` (line 114) are in sections 3.1-3.2 and carry phase P4.
- stated wrong outcome: An implementer who follows the stated text as written builds, in Phase 1, an `--unattended` flag and a `## Unattended mode` section on `/sc:pr-submit`, `/sc:post-release` and `/sc:implement`, because AC-1.1 passes only when all 37 commands in 3.1-3.2 have one. That is wrong because the spec says Phases 1-3 need no user decision and D3 (a) (recommended) says pr-submit does not become a worker and gets no change; AC-1.1 therefore fails on the spec's own recommended choice. The same Phase 1 also publishes `--unattended` on gated commands (cleanup, cli-portify, task, tdd, pr-submit and others) whose gate resolutions only arrive in P2 or P4 (lines 160, 162). A worker briefed with `--unattended` under section 2.3 (line 73) then stalls on the old prompt while the flag claims no person is needed, which WC-2 (line 60) forbids.
- coverage line: both texts read at the cited lines; the 37-command set is the sum of lines 78-92 and 94-125.

### B2. WC-4 puts the contract at `<output-dir>/return-contract.yaml` but several commands take a file as `--output`

- severity: MAJOR graded blocking (a stated text an acceptance criterion cannot pass); expert: Adzic, Fowler
- cited texts:
  - `specs/orca-worker-contract-spec.md:62` WC-4: "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - `specs/orca-worker-contract-spec.md:90` tdd row: "`--output <file>`; ... the TDD at `--output`".
  - `specs/orca-worker-contract-spec.md:87` init-lite row: "`--output <file>`".
  - `specs/orca-worker-contract-spec.md:200` AC-2.2: "`/sc:tdd "auth" --unattended --output <file>` with a bare topic" must end with "contract `status: blocked` with a non-empty `blocked_question`".
  - `specs/orca-worker-contract-spec.md:182` and `:183` (7.2 steps 3-4): the report path must be "the WC-4 contract path" and `test -s <contract>` must exit 0.
- stated wrong outcome: An implementer who follows the stated text as written builds, for tdd and init-lite, a contract at `<value of --output>/return-contract.yaml`, which is `<file>/return-contract.yaml` inside a regular file. That is wrong because the path cannot be created, so AC-2.2 and 7.2 step 4 cannot pass; the spec gives no other location for the contract of a command whose `--output` names a file. (`spec-panel` at line 120 says "add `--output`" without saying file or directory, and the same split applies to it.)
- coverage line: the file-valued `--output` for tdd and init-lite is the spec's own text (lines 87, 90); no inventory text says tdd's `--output` is a directory.

## Reviser brief

Blocking finding ids: B1, B2.

Contract for the reviser (restated from the command's Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Do not award yourself a PASS.

## Requirements analysis

- Wiegers: the WC-1..WC-12 table gives owner and evidence for every requirement, and the 43-command split re-derives. B1 and B2 are the two places where a stated requirement and a stated check disagree. WC-1 has an owner ("Launch setup, not commands", line 59) but no phase in section 6 and no acceptance check except the generic `state: ready` pass at line 180; recorded as a follow-up, not blocking, because no stated text does harm.
- Adzic: the acceptance checks in section 7 are mostly concrete (commands plus pass conditions). Exceptions are in the follow-up list (F2, F3, F6).
- Cockburn: the actors (coordinator, worker session, command, person) and their goals are clear in section 2.2 and D1-D5.

## Architecture analysis

- Fowler: the decision "Orca on top, commands stay units of work" (lines 13-16) is consistently applied; R1-R5 (lines 31-37) match `CAPS:97-101` (nesting depth 1, `nested_worker_depth_exceeded`; `orca-capabilities.md:97-103`). Interface boundary (command knows `--unattended`, never Orca) is clean except for the AC-C1 / SA-2 tension in F4.
- Newman: backward compatibility is handled by SA-1..SA-6; the additive-edit check is weak (F1).
- Hohpe: message flow (`ask`, `check`, `worker_done`, `--report-path`) matches the capabilities inventory (`orca-capabilities.md:63-67,73-79`). Nygard: failure modes are covered by `blocked`/`failed`; retry behaviour has an unresolved seam (F6).
- Whittaker (attacks): Sequence Attack found B1 (P1 before P2/P4 gates). Sentinel Collision Attack found B2 (file-valued `--output` colliding with a directory convention) and F3 (fixed status set versus existing contracts). Zero/Empty Attack: `--unattended` with no output directory (F6).

## Guard Condition Boundary Table

Guards are the numeric and boolean thresholds the spec states. Classes left out: One/Minimal and Maximum for G-1 and G-4 (a single state or a 0/1 value cannot differ from Typical).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G-1 outcome mapping | WC-5 (line 63) | Zero/Empty | no report file | true (`failed`) | `--outcome failed` | OK |
| G-1 outcome mapping | WC-5 (line 63) | Typical | status `partial` | true | `--outcome succeeded`, body says partial | OK |
| G-1 outcome mapping | WC-5 (line 63) | Sentinel Value Match | status value outside the four (existing contracts keep their own fields, line 62) | unspecified | not stated | GAP (Medium, F3) |
| G-2 wait split | WC-10 (line 68) | Typical | wait 4 min | true | allowed, heartbeat between | OK |
| G-2 wait split | WC-10 (line 68) | Maximum/Overflow | eval timeout 3600 s (`INV-A:65` via line 68) | true | split into waits of at most 4 min | OK |
| G-2 wait split | WC-10 (line 68) | Legitimate Edge Case | pr-submit iteration where poll script runtime plus sleep exceeds 4 min | unknown | UNVERIFIED, deferred to a check (lines 114, 283) | GAP (Medium, stated UNVERIFIED) |
| G-3 contract location | WC-4 (line 62) | Zero/Empty | no output directory in the brief | n/a | not stated (WC-4 assumes one) | GAP (Medium, F6) |
| G-3 contract location | WC-4 (line 62) | Legitimate Edge Case | `--output` is a file (tdd, init-lite) | contract path invalid | not stated | GAP (blocking, B2) |
| G-4 nesting depth | R1 (line 33) | Typical | depth 1 reached by a worker calling `worker-start` | true | refused `nested_worker_depth_exceeded` | OK |
| G-4 nesting depth | R1 (line 33) | Legitimate Edge Case | `task-create` at depth 1 | unknown | UNVERIFIED (line 276) | GAP (Medium, stated UNVERIFIED) |

No multi-stage count-divergent data pipeline is specified, so no Quantity Flow Diagram is produced.

## Follow-up candidates (Medium and minor; never fail the review)

Per the command, the session that ran this review asks the user once per loop whether to open an issue for these; none is opened by this report.

- F1 (Medium): AC-C5 and AC-0.3 use `grep -E '^-[^-]'` on `git diff -U0` (lines 176, 193). A deleted markdown bullet `- x` appears in a diff as `-- x`, which the pattern excludes, so deletion of bullet lines passes the additive-edit check that SA-4 (line 149) relies on. Needs the guess that an implementer deletes bullets.
- F2 (Medium): section 2.3 (line 73) requires `--unattended` in every brief, but 3.1 says ready commands run "if the brief uses the stated flags" (line 79) and the P0 smoke commands at line 194 omit `--unattended`; the flag does not exist until P1 (line 159). Reading depends on whether P0 is exempt.
- F3 (Medium): WC-4 fixes the status set to `succeeded|partial|failed|blocked` and AC step 4 asserts it (lines 62, 183), while "commands that already write a contract keep their fields" (line 62). The existing workflow contract has its own `status` (`commands-b.md:272`, values not quoted); whether it fits the set is UNVERIFIED.
- F4 (Medium): AC-C1 (line 172) requires no `orca orchestration|worktree|terminal|agent` text anywhere under `src/superclaude/core`, with only `ccsession-tag` exempt, while SA-2 (line 147) allows an Orca example in the contract file and SA-5/P0 add an Orca section to HOW-WE-WORK.md (lines 150, 158). Whether those files contain the matching text depends on how they are written.
- F5 (Medium): WC-9 and the auggie-review row (lines 67, 100) name an explicit `--post-pr` flag; the inventories show only `--no-post-pr` and `--no-remediation-offer` (`commands-a.md:38,78`). The row says "Other required change: none", so a new flag is unstated.
- F6 (Medium): WC-6 says a re-run uses a fresh output directory (line 64) while WC-4 says the directory is fixed by the coordinator before dispatch (lines 62, 73); a `--retry-of` worker given the same brief reuses the first attempt's directory unless the coordinator changes it. Section 3 "fresh dir" rows (about 20) rely on this.
- F7 (Medium): WC-3 lets a worker `ask` the coordinator instead of ending blocked (line 61), but AC-2.2 expects `worker_done --outcome failed` and `status: blocked` for gate runs (line 200); the check does not say which path the worker takes.
- F8 (Medium): the tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (line 122); reflect Tier 2 and adversarial Mode A add further layers (`sk/sc-reflect-protocol` per line 88), not counted. UNVERIFIED (`commands-a.md:14` gives three layers).
- F9 (Medium): SA-4 lists the named defect fixes allowed to change existing lines (line 149); the reflect row (line 88) and the cli-portify/implement rows also change existing behaviour but are not in that list, so AC-C5 would flag them.
- F10 (minor): WC-1 has no phase or acceptance check of its own (line 59); WC-12 `consumer_fenced` (line 70) is a second path that ends without `worker_done`, against WC-5's "exactly once" (line 63) when read without the exception.
- F11 (minor): citations into `CLAUDE.md`, `HOW-WE-WORK.md`, `src/`, `Makefile`, `pyproject.toml` and the `.dev/evals`, `.dev/codegraph-migration` files (for example lines 52, 146, 150, 183) could not be checked in this workspace: UNVERIFIED. The spec's own UNVERIFIED list (lines 271-286) already names the main ones.

verdict: FAIL
