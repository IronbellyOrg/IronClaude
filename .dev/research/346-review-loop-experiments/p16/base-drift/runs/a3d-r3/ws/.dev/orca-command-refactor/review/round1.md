review: 1 of 3

# Spec panel review, round 1: orca-worker-contract-spec.md

- Mode: `--mode critique`, `--focus requirements,architecture`, first review (no `--re-review`, no `--baseline`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- sha256 candidate: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Reviewer model actually used: claude-sonnet-5-5
- Date: 2026-11-10
- Prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing).
- Citation notation: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: command definition, README, review-loop prompts, candidate, and all three inventories.
- Cross-checked: about 70 `INV-*`/`CAPS:*` citations in the candidate against the inventory lines (all found as cited). Counts reconcile: 43 = 21 + 22; 10 ready + 27 needs-change + 6 coordinator-only; the P1/P2/P3/P4 command lists cover exactly the 27 section 3.2 rows plus the 8 small fixes to 3.1 commands (checked row by row).
- Checked internal consistency of WC-1..WC-12, SA-1..SA-6, the phase plan, the acceptance checks and D1..D5.
- **Not checkable in this sandbox (UNVERIFIED):** every citation to `CLAUDE.md:*`, `src/superclaude/**` (for example `install_core.py:4,33,13-24`, `HOW-WE-WORK.md:171,249,254`, `pyproject.toml:38`, `Makefile:68-74`), `.dev/codegraph-migration/**`, the E5 grep results (`SPEC:25`), the "11 re-read locations" claim (`SPEC:11`), and the "about 340 citations re-read" claim (`SPEC:285`). They are outside the workspace; no finding below depends on them. Where a finding rests on a `cmd/` or `sk/` line it is carried from an inventory line and said so.
- Not done: no command was run, no Orca call made; the candidate was not edited.

## Expert sequence (summary lines)

1. **Wiegers:** WC-1..WC-12 are mostly testable and each names an owner and evidence. Weak spots: WC-4's location rule (F-1, M-1, M-2), WC-10's scope (M-4).
2. **Adzic:** the acceptance checks in 7.2 are concrete and runnable. AC-2.2 contradicts WC-4 for file-valued `--output` (F-1). AC-0.4 omits the flag that section 2.3 makes mandatory (M-7).
3. **Cockburn:** primary actor (coordinator) and goal (collect a deterministic report per worker) are clear. The worker's own entry step, how a preamble-first prompt becomes a command run, is not stated (M-8).
4. **Fowler:** the decision (Orca on top, commands untouched by Orca) is sound and well argued (R1-R5). Single shared contract file plus per-command `## Unattended mode` section is a good boundary. Count flow reconciles (diagram below). The contract's schema is under-specified (M-6).
5. **Nygard:** failure modes covered well (blocked, partial, ask timeout, consumer_fenced). Unbounded `ask` wait and the heartbeat claim are open (M-4, M-9).
6. **Whittaker:** attacks below. One breaks the spec (F-1).
7. **Newman:** contract versioning and the status vocabulary vs existing contracts (M-6).
8. **Hohpe:** the message exchange (`ask` / `reply` / `check` / `worker_done`) is cited to Orca output and consistent; pull-only follow-ups are acknowledged (WC-12). Open: what "natural checkpoints" are inside one command run (M-9).
9. **Crispin:** per-phase checks exist for every phase; P0 smoke tests close the evidence gap in section 1.4. Gap: AC-C1 versus the P0 deliverables (M-5).
10. **Gregory:** the open decisions D1-D5 are self-contained with recommendations; good. Section 6 wording on "no user decision" is loose (minor note).
11. **Hightower:** operational concerns (executable name per platform, `runtime_unavailable`) are handled by keeping Orca out of commands (R2, R4). No finding.

## Grading check for the blocking finding

F-1: An implementer who follows the stated text as written builds `<output-dir>/return-contract.yaml` with `<output-dir>` equal to the value of `--output` (`SPEC:62`), and for `/sc:tdd "auth" --unattended --output <file>` (`SPEC:90`, `SPEC:200`) that makes the contract path `<file>/return-contract.yaml`, a path below a directory that has the same name as the TDD file the command must also write; X is wrong because the deliverable and the report cannot both exist at that path, and AC-2.2 step 4 (`test -s <contract>`) has no defined path to test.

=== REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, graded blocking] Contract location is undefined for commands whose `--output` is a file
- **Expert:** Wiegers (lead), Adzic.
- **Issue:** WC-4 fixes the report at `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`) and section 2.3 requires the output directory in the brief so the path is known before dispatch (`SPEC:73`). But the spec's own rows pass `--output` as a file: tdd "`--output <file>`" (`SPEC:90`), init-lite "`--output <file>`" (`SPEC:87`), spec-panel "add `--output`" for a single review document (`SPEC:120`; the review document is a file, `INV-B:182`), research (`SPEC:116`, one `claudedocs/research_*.md` file, `INV-B:132`). The acceptance check AC-2.2 itself runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked` (`SPEC:200`). Init-lite's `--output` is a file (`INV-A:55`). No flag for a separate report directory is named for these commands, and no rule says "use the parent directory" or "use a sibling file".
- **Wrong outcome:** see the grading check above. Using the parent directory instead is a guess the text does not make, and would put several workers' `return-contract.yaml` into one shared directory (for example `docs/<domain>/`), which WC-11 (`SPEC:69`) forbids.
- **Recommendation:** state one rule for file-valued `--output` (for example a named sibling file, or a required separate `--report-dir`) and apply it in the tdd, init-lite, spec-panel and research rows and in AC-2.2. Prefer narrowing WC-4 to one sentence over adding mechanism.
- **Priority:** High. **Quality impact:** Testability +1.5, Consistency +1.

(Contract-location gaps that need a guess to become wrong are M-1, M-2 and M-3.)

### Medium findings (warnings, listed under follow-up candidates; none triggers a revision)

- **M-1 [MAJOR label, Medium] Workflow's contract path contains a generated id.** 3.1 workflow: `.dev/tasks/to-do/<id>/return-contract.yaml`, brief passes only `--handoff none` (`SPEC:92`); the contract is "not written for pre-creation STOPs" (`INV-B:272`). WC-4 demands a file "on every outcome ... including stops before any other output exists" and a path known before dispatch (`SPEC:62`, `SPEC:73`). The P1 fix "write the contract for pre-creation STOPs too" (`SPEC:92`) gives no location, because the package directory does not exist yet. The implementer must guess where the file goes. Why Medium: the sentence needs a guess about the location, not a contradiction that holds as written.
- **M-2 [MAJOR label, Medium] No rule for `--unattended` without an output argument.** Section 3.2 adds `--output` to many commands (`SPEC:99-125`) but nothing says what a command does under `--unattended` when the brief omits it: refuse, default to a timestamped path (WC-11, `SPEC:69`), or write nowhere. The command definition used for this review shows how a sibling spec solves it (refuse before any work); this spec is silent. Medium: missing restriction.
- **M-3 [MINOR-MAJOR label, Medium] "Fresh output directory" versus "path known before dispatch".** WC-6 says a command without a resume flag writes each run "into a fresh output directory" (`SPEC:64`); WC-4 says the report sits in the directory the coordinator passed (`SPEC:62`). If the command creates the fresh directory itself the coordinator's path is wrong; if the coordinator supplies a new path per retry that duty is not in section 2.3 (`SPEC:73`). Two readings; Medium.
- **M-6 [MAJOR label, Medium] Status vocabulary and schema version.** WC-4 requires `status` in the fixed set `succeeded|partial|failed|blocked` and says existing contracts "keep their fields and add the missing ones" (`SPEC:62`, `SPEC:262`). Workflow's contract is versioned "contract 1.1" with its own statuses (`INV-B:272`); the spec does not say whether `status` values change, nor define a version field for the shared shape. AC step 4 (`SPEC:183`) asserts the four-value set for every command. If an existing value is outside the set, the check fails on a correct contract. Whether any existing value is outside the set is not checkable from the inventories (UNVERIFIED), so Medium.
- **M-7 [MINOR label, Medium] P0 smoke commands omit `--unattended`.** Section 2.3 and 7.2 step 1 require the brief to contain "the exact command line including `--unattended`" (`SPEC:73`, `SPEC:180`), but AC-0.4 lists the three smoke commands without it (`SPEC:194`) and 3.1 says they run "if the brief uses the stated flags" (`SPEC:79`), because the flag is accepted only from P1 (`SPEC:159`). What a command does with an unknown `--unattended` before P1 is unstated. The implementer follows AC-0.4, so no wrong build follows from the text; Medium.
- **M-11 [MINOR label, Medium] Flag interactions under `--unattended`.** Only roadmap, cleanup, improve, test, explain, business-panel and pr-submit say what happens with their person-mode flag (`SPEC:100-123`); adversarial, brainstorm and release-split rely on the brief saying "never `--interactive`" (`SPEC:83-84`, `SPEC:89`). WC-2 (`SPEC:60`) covers the outcome (never asks), so this is a clarity gap, not a wrong outcome. No rule says how the switch token is recognised when the same string appears inside quoted content.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The decision in section 1 is consistent with the Orca facts it cites (R1 `CAPS:97-103`, R2 `CAPS:147-149`, R3 `CAPS:76,148,150`, R4 `CAPS:145`, R5 `INV-A:90`, `INV-B:285-286`).

- **M-4 [MAJOR label, Medium] WC-10 is universal in wording, local in application.** WC-10 says the worker "sends a heartbeat every 5 minutes while working" and any step that "blocks a single tool call for longer than 5 minutes" must be split to at most 4 minutes (`SPEC:68`). Only cli-eval and pr-submit are given a split (`SPEC:104`, `SPEC:114`), only pr-submit is checked (AC-4.3, `SPEC:210`). A foreground Agent-tool fan-out is also a single blocking tool call and cannot be split into 4-minute waits; commands marked ready fan out heavily (cleanup-audit waves `INV-A:42`, tdd 2-10+ agents `INV-B:221`, reflect Tier 2 `INV-B:111`). Read literally these ready commands violate WC-10 with no acceptance check failing. The spec itself says whether Orca uses heartbeat age is UNVERIFIED (`SPEC:68` cites `CAPS:130`; `CAPS:182` item 7) and that silence never authorizes stop or release (`CAPS:125`). The implementer must guess whether Agent fan-out is in scope; Medium.
- **M-5 [MAJOR label, Medium] AC-C1 can fail on the P0 deliverables.** AC-C1 greps `src/superclaude/core` for `orca(-ide) orchestration|worktree|terminal|agent` and requires no output, excluding only `ccsession-tag` (`SPEC:172`). P0 adds `core/WORKER-CONTRACT.md` and an Orca section to `core/HOW-WE-WORK.md` (`SPEC:158`, `SPEC:150`), and SA-2 explicitly allows one Orca mention "as an example of a caller's question channel inside the contract file" (`SPEC:147`). AC-C1 is a common check for every phase including P0 (`SPEC:167`). Whether the new text uses a matching phrase is the author's choice, so the failure needs a guess; Medium. Narrow the grep to `commands skills agents` or exclude the two core files.
- **M-8 [MAJOR label, Medium] How a worker turns its Task into a command run is not stated.** The worker "runs the command directly in its own session" (`SPEC:16`, `SPEC:65`), but an Orca worker's first prompt is the dispatch preamble plus the Task block (`CAPS:47` shows Claude takes the task on the command line; the preamble content is described at `CAPS:73-78,148`), so the message does not begin with `/sc:`. Whether a slash command inside such a prompt is expanded, or the worker must call the Skill tool, is not specified. AC-0.4 would find out, but no requirement tells the implementer of WORKER-CONTRACT.md what the brief template says. Medium: missing mechanism.
- **M-9 [MINOR label, Medium] `ask` wait is unbounded; "natural checkpoints" undefined.** WC-3 lets the worker `ask` once and wait with no cap and no sentinel for "coordinator never answers" (`SPEC:61`); `CAPS:129` says a waiting worker is healthy, so nothing flags it. WC-12 has the worker run `check` "at natural checkpoints" (`SPEC:70`), but inside one long command invocation the worker session does not control turn boundaries. Not a wrong build; Medium.
- **M-10 [MINOR label, Medium] Evidence for the direct route is stated twice, differently.** E3 cites `invocation_method: "skill-direct"` as proof that it worked (`SPEC:23`); section 1.4 says the same run proves only the nested route because the brief told workers to use an Agent-tool subagent (`SPEC:43`; `CAPS:156`). `INV-A:13` reads the same contract field as direct. The spec does not reconcile the two. The conclusion (run P0 first) stands either way.

## Guard Condition Boundary Table

Guards found: `--unattended` switch (WC-2), output argument (WC-4), status set and outcome map (WC-5), retry / fresh directory (WC-6), 5-minute heartbeat and 4-minute split (WC-10), `ask` timeout (WC-3), readiness 60 s and 45 s fallback bound (WC-1), phase gating (section 6). One row per input class that applies; classes that cannot occur are left out with the reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` present | WC-2, SPEC:60 | Zero/Empty | flag absent | false | SA-1 keeps today's behaviour (SPEC:146) | OK |
| `--unattended` present | WC-2, SPEC:60 | Typical | flag present, no person flag | true | no prompt; each gate resolves (a)/(b)/(c) | OK |
| `--unattended` present | WC-2, SPEC:60 | Legitimate Edge Case | with `--interactive` | true | per-row for 7 commands; not stated for adversarial, brainstorm, release-split | GAP (M-11) |
| `--unattended` present | WC-2, SPEC:60 | Sentinel Value Match | token inside quoted content | unspecified | not stated | GAP (M-11) |
| output argument | WC-4, SPEC:62 | Zero/Empty | `--output` omitted | unspecified | not stated | GAP (M-2) |
| output argument | WC-4, SPEC:62 | Typical | directory value | true | `<dir>/return-contract.yaml` | OK |
| output argument | WC-4, SPEC:62 | Legitimate Edge Case | file value (tdd, init-lite, spec-panel, research) | contradictory | contract path undefined; AC-2.2 assumes one | GAP (F-1, blocking) |
| output argument | WC-4, SPEC:62,92 | Legitimate Edge Case | path with generated id (workflow), pre-creation STOP | unspecified | location not stated | GAP (M-1) |
| contract `status` | WC-4/WC-5, SPEC:62-63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| contract `status` | WC-5, SPEC:63 | Typical / Edge | `partial`; audit verdict FAIL | n/a | `succeeded`, first sentence states status | OK |
| contract `status` | WC-4, SPEC:62,183 | Sentinel Value Match | existing contract value outside the four | false | not stated | GAP (M-6) |
| fresh directory | WC-6, SPEC:64 | Legitimate Edge Case | retry (`--retry-of`) without resume flag | true | "fresh output directory", who names it not stated | GAP (M-3) |
| wait split | WC-10, SPEC:68 | Typical | single poll/eval wait over 5 min | true | split into waits of at most 4 min | OK |
| wait split | WC-10, SPEC:68 | Maximum/Overflow | foreground Agent fan-out over 5 min | true | cannot be split; not addressed | GAP (M-4) |
| `ask` | WC-3, SPEC:61 | Maximum/Overflow | no reply ever | n/a | no bound | GAP (M-9) |
| `ask` timeout | WC-3, SPEC:61 | Typical | timeout | true | resume same message ID | OK |
| readiness | WC-1, SPEC:59 | Typical / Edge | prompt before ready; fallback 30 s passes, over about 45 s fails | true | "well inside" 60 s; evidence gives the numbers | OK (minor: no figure in the requirement) |
| `check` result | WC-12, SPEC:70 | Legitimate Edge Case | `consumer_fenced` | true | stop, no `worker_done` | OK |

Left out: negative and `MAX_INT` values (no numeric argument is introduced), one-element classes for the status set (covered by the typical row).
FR-8: the GAP rows are graded by consequence: F-1 blocking, the rest Medium. FR-9: one blank behaviour (F-1 row, M-1 row), graded the same way. FR-10: the table is complete for the guards found above, so synthesis proceeded.

## Quantity Flow Diagram (pipeline: inventory, rows, phases)

```text
[Commands in cmd/: 43] --> [Inventories: A 21 + B 22 = 43]       (INV-A:3, INV-B:3, SPEC:76)
    --> [Verdicts: ready 10 | needs-change 27 | coordinator-only 6]   (10+27+6 = 43, conserved)
    --> [Section 3.1: 10 rows] --> [Small fixes: P1 4 (adversarial, cleanup-audit, index-repo, workflow), P2 4 (reflect, release-split, tdd, troubleshoot); 2 none (brainstorm, init-lite)] = 10
    --> [Section 3.2: 27 rows] --> [P1 9 | P2 11 | P3 4 | P4 3] = 27
    --> [Section 4: 6 rows]    --> [no phase, no --unattended]
    --> [AC-1.1 asserts a Unattended-mode section for 3.1+3.2 = 37; section 4 = 0]
```
No divergence point found. One consumer note: AC-1.1 asserts a section naming `return-contract.yaml` for all 37 commands (`SPEC:195`), including `load`, whose 3.2 row says "none" for the report (`SPEC:112`); the section can state "writes none", so this is a clarity note only.

## Adversarial analysis (Whittaker)

- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / section 2.3 (SPEC:62, SPEC:73)** fails when **the brief omits the output argument under `--unattended`**. Concrete attack: coordinator dispatches `/sc:analyze src/x --unattended` (no `--output`); before: no output path known to coordinator; after: command picks a timestamped default (WC-11) or writes nothing; `worker_done --report-path` carries a path the coordinator never saw. Severity: MAJOR label, graded Medium (M-2).
- I can break this specification by **Divergence Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--output` is a file**. Concrete attack: `/sc:tdd "auth" --unattended --output docs/auth/TDD_AUTH.md`; before: no `docs/auth/TDD_AUTH.md`; after literal WC-4: the command creates a directory `docs/auth/TDD_AUTH.md/` for the contract and then cannot write the TDD file at that path, or writes the contract into `docs/auth/` where a second worker also writes. Severity: MAJOR label, graded blocking (F-1).
- I can break this specification by **Sequence Attack**. The invariant at **WC-3 then WC-5 (SPEC:61, SPEC:63)** fails when **a blocked command is re-invoked after `ask` and the first run's contract already says `blocked`**. Concrete attack: run 1 writes `status: blocked`; worker asks, gets the answer, re-runs with the flag; if run 2 crashes before rewriting the contract, the stale `blocked` file is read and the worker reports `failed` for a run that never finished. The spec requires a contract "on every outcome" (SPEC:62), which includes the crash case only if the file is rewritten at start. Severity: MINOR (behaviour inferable), note only.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-2 switch (SPEC:60)** fails when **the string `--unattended` appears inside quoted specification text**. Concrete attack: `/sc:spec-panel "the flag --unattended must ..."`; before: person run; after: treated as unattended, gates vanish. Severity: MINOR label, Medium (M-11); no restriction stated.
- **Accumulation Attack:** the three-failure circuit breaker (`CAPS:80`, `CAPS:116`) counts failed starts, not a worker's own `failed` reports; WC-5 maps every `blocked` to `failed`. Repeated blocked retries therefore never trip the breaker. The spec does not claim otherwise; no finding.

## Quality assessment (0-10)

- Clarity 7, Completeness 7, Testability 7, Consistency 6.
- Consensus: the decision and the per-command table are strong and the evidence trail is honest about gaps (section 1.4, UNVERIFIED list). One contradiction in the report-location rule blocks.
- Disagreement: none among the simulated experts on severity; Newman and Wiegers both rate the contract schema (M-6) as the most likely next defect.

## Follow-up candidates (Medium and minor; no revision, no failure)

1. M-1 workflow contract location for generated ids and pre-creation STOPs.
2. M-2 behaviour under `--unattended` without an output argument.
3. M-3 who names the fresh directory on retry.
4. M-4 scope of WC-10 (Agent fan-out) and a matching acceptance check.
5. M-5 AC-C1 scope versus the two P0 core files and SA-2's allowed mention.
6. M-6 shared contract schema, status vocabulary versus existing contracts, version field.
7. M-7 P0 smoke commands without `--unattended`; behaviour of the flag before P1.
8. M-8 how a worker turns the Task into a command run (brief template content).
9. M-9 unbounded `ask`; meaning of "natural checkpoints".
10. M-10 E3 versus section 1.4 on `skill-direct`.
11. M-11 flag interactions and quoted-token recognition.
12. Minor notes: `SPEC:154` says "Phases 1-3 need no user decision" while D1 and D4 touch them (section 9 says they proceed on the recommendations); AC-C5's `^-[^-]` hides removed lines that start with `--`; `SPEC:133` cites `README:31` (a rule for this run's workers) as the repo's git-authorization policy; partial mapped to succeeded lets Orca dependents become ready before the coordinator reads the report (acknowledged at `SPEC:263`); the unverified-citation list at the top of this report.

Question for the user, once per loop: open an issue for the follow-up candidates above? This sandbox has no user channel and no GitHub access; the list is only recorded and no issue was created.

## Reviser brief

Blocking finding ids: F-1.

The reviser reads this report, not the command. Rules: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id; leave Medium and minor findings (M-1..M-11 and the notes) alone; return the candidate once and do not award yourself a PASS.
F-1 text to repair: `SPEC:62` (WC-4 location rule), with the rows and check that pass a file-valued `--output`: `SPEC:87`, `SPEC:90`, `SPEC:116`, `SPEC:120`, `SPEC:200`.

verdict: FAIL
