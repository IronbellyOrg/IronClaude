review: 1 of 3

# /sc:spec-panel critique, round 1

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review of the full document; `--re-review` and `--baseline` absent)
- lint file: `.dev/orca-command-refactor/review/lint-1.md`, sha256 `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-37` (read in full). This is ONE of the two first reviews; the MERGE rule (`:36`) is the coordinator's job.
- cap: first review, so `review: 1 of 3`; a `Reviser brief` precedes the verdict.

## Lint evidence
`review/lint-1.md:1` records the candidate hash above, so the lint ran on this exact file. `review/lint-1.md:3` says "Checks: REF. Findings: 0." and `:5` "No findings." There is no lint id to confirm or dismiss. No lint id fails the review.

## Coverage statement
Read in full: the command definition (`command.md`), the review prompts file, `README.md`, the candidate (1-285) and the lint file. Evidence that can be checked inside the workspace is only `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323 lines) and `inventory/orca-capabilities.md` (188 lines). I spot-checked about 45 `CAPS:` lines, `INV-A:3,62,76-83,90,94-98,106,113,118,120`, `INV-B:3,31-52,215,285-289,292-301,311,320,323` and the 10/27/6 split (counted from the candidate's own tables: 10 rows at `spec:81-92`, 27 rows at `spec:99-125`, 6 rows at `spec:132-137`; per-inventory ready 5+5, needs-change 13+14, coordinator-only 3+3, total 21+22=43 matches `spec:76`). Phase membership also reconciles: P1 9, P2 15, P3 4, P4 3 (the 27 plus the 4 ready commands that P2 also lists, `spec:159-162`).
Every citation to `cmd/`, `sk/`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `CLAUDE.md`, `Makefile`, `pyproject.toml` and the `orca-ide` binary or guides points at a file that is NOT in this sandbox. Those citations are UNVERIFIED here, including the 11 locations the candidate says it re-read (`spec:11`) and the 340-citation check (`spec:285`). Where the inventories quote a location I say so, but a quote in an inventory is a second-hand source.
Experts applied in the command's fixed order for the `requirements` and `architecture` focus: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. `--focus correctness` is not active, so no State Variable Registry is produced. Pipeline Dimensional Analysis does not trigger (the document describes no data pipeline whose counts diverge); the only count chain, 43 = 10 + 27 + 6, is conserved (above).

## Findings

Grading used the grading check (`document_review_loop_prompts.md:34`) for every finding.

### === REQUIREMENTS ANALYSIS ===

#### B1 (blocking) CRITICAL-as-graded-by-consequence. Wiegers + Crispin. The P0 acceptance check cannot pass as written, and the next phase cannot start until it does.
- Quoted texts:
  1. `spec:182` (7.2 step 3): "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
  2. `spec:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1."
  3. `spec:79`: "the worker reports the named file until Phase 1 adds the contract"; `spec:91` troubleshoot reports `REPORT.md`; `spec:92` workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml`; `spec:83` adversarial's contract "filename not fixed".
  4. Gate: `spec:154` "Later phases do not start until the earlier phase's checks in section 7 pass"; `spec:167` "A phase passes only when every check in its block and every common check passes."
- Stated wrong outcome: An implementer who follows the stated text as written runs the three P0 smoke commands, and each worker sends `worker_done --report-path` with the file the command writes today (`REPORT.md` for troubleshoot, the workflow ledger contract, an unnamed adversarial contract). Step 3 then fails for each, because no contract has `status` yet under WC-4's `<output-dir>/return-contract.yaml` (`spec:62`) and the reported path is not "the WC-4 contract path". AC-0.4 says step 3 must pass, and only step 4 is carved out. So AC-0.4 cannot be passed, P0 can never pass, and `spec:154` bars P1. The two texts contradict each other with no further assumption.
- Recommendation (narrow): in AC-0.4 carve out the "WC-4 contract" clauses of step 3 as well as step 4 (state that P0 compares `--outcome` with the command's own existing report), or move the "contract path" clause of step 3 into the P1+ checks. Delete rather than add.
- Priority: High. Quality impact: removes an unpassable gate on the smoke runs that the spec says test its core decision (`spec:158`, `spec:43`).

### === ARCHITECTURE ANALYSIS ===
No architecture finding reached blocking. The decision itself (Orca above, commands as units) is consistent with the inventories: no command calls Orca (E5 is UNVERIFIED here, the grep ran outside the sandbox), depth 1 is quoted at `CAPS:97-98`, lifecycle messages are tied to the dispatched pane at `CAPS:76,150`, subagent limits are honestly UNVERIFIED at `CAPS:186`. Medium findings follow.

### Medium findings (warnings, follow-up candidates, never fail the review)

#### M1 Wiegers/Hohpe. Where the contract file goes is undefined when the command's output flag is a file.
- Texts: `spec:62` defines `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)". But `spec:87` (init-lite `--output <file>`), `spec:90` (tdd `--output <file>`), `spec:120` (spec-panel "add `--output`") and the AC at `spec:200` (`/sc:tdd "auth" --unattended --output <file>`) pass a file. `spec:183` then does `test -s <contract>`. The command definition in this sandbox treats `--output` as file-valued and adds a separate `--report-dir`, with the contract in `<report-dir>/return-contract.yaml` (`command.md:460-461`).
- Why Medium: the implementer must guess among `<file>/return-contract.yaml` (a literal reading), the file's parent directory, or a new directory flag. The text does not state which. No wrong outcome follows without that guess.
- Also note `spec:120` asks to "add `--output`" to spec-panel while the sandbox command already has `--output`, `--target-release` and `--unattended` (`command.md:22-23,455-465`); I cannot tell whether row `spec:120` is stale, since `cmd/spec-panel.md` is not in the workspace (UNVERIFIED).
- Priority: Medium.

#### M2 Nygard/Whittaker (Sequence attack). No rule for a missing, stale or unidentified contract.
- Texts: `spec:62` (contract "written on success, failure, blocked and partial outcomes"; fields `status`, `command`, `report_path`, `artifacts`, `blocked_question` only), `spec:64` (a retry resumes "from its on-disk state" into the same output), `spec:73` ("the coordinator opens the report file"), `spec:63` (no report means `--outcome failed`).
- Concrete attack: attempt 1 writes `status: blocked`. The retry (`--retry-of`) resumes into the same `<output-dir>`, the session dies (context exhaustion, crash) before it overwrites the file, and it sends nothing or a `worker_done`. The coordinator opens the old file and reads `blocked`/`succeeded` for the wrong attempt. The contract carries no `task_id`, `dispatch_id` or timestamp, and nothing says to move the old file aside at start. Also, a crash cannot honour "written on every outcome" (`spec:62`).
- Why Medium: it is a requirement the document never states (a missing restriction), not a stated text that does harm.
- Recommendation: add the dispatch id to the contract fields and say the coordinator treats a contract without the current dispatch id as absent. Priority: Medium.

#### M3 Wiegers. The undefined "no output directory" case under `--unattended`.
- Texts: `spec:62` ties the contract to the directory "the coordinator passed"; `spec:113` (post-release) and `spec:104` (cli-eval) resolve a missing value as blocked, which requires a contract written somewhere, but the directory is the thing that is missing. The sandbox command refuses before any work and prints in chat only (`command.md:460`). The candidate has no equivalent rule, and `spec:63` then maps "no report" to `failed`, which is an acceptable but unstated fallback.
- Why Medium: unspecified edge case; no stated text does harm. Priority: Medium.

#### M4 Crispin/Wiegers. AC-1.1 requires one uniform section from commands the spec treats differently.
- Texts: `spec:195` AC-1.1 asserts "every command in sections 3.1-3.2" has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`. But `/sc:load` gets "usage line only" (`spec:112`, `spec:159`) with report "none", and `spec:265` rejects a report file for load ("unrequested addition"). Also `implement`, `post-release`, `pr-submit` have their gate resolutions waiting on D2-D4 (`spec:154`, `spec:162`, `spec:225`), yet P1 is said to need no user decision.
- Why Medium: an implementer can satisfy the assertion by a stub section, or may add a contract to load. Which one is a guess. Priority: Medium.

#### M5 Crispin. AC-C5 and the additive-edit rule collide with adding a flag to a Usage line.
- Texts: `spec:176` AC-C5 requires `git diff -U0 ... | grep -E '^-[^-]'` to print nothing; `spec:149` SA-4 allows "new flags"; `spec:159` P1 requires "the `--unattended` flag accepted by every command". Commands document flags in their Usage line (the sandbox command lists them on one line, `command.md:22-23`), so editing it removes an old line in the diff.
- Why Medium: the flag could be documented only inside the new section, which passes. The text does not say so. Priority: Medium.

#### M6 Fowler. AC-C1 scans `src/superclaude/core` while P0 adds Orca content there.
- Texts: `spec:172` (the grep covers `src/superclaude/core`, "prints nothing"), `spec:158` and `spec:150` (P0 writes `core/WORKER-CONTRACT.md` with a "coordinator brief template" and adds an Orca section to `core/HOW-WE-WORK.md`), `spec:147` (SA-2 allows an Orca mention in the contract file). If either file names an `orca orchestration ...` command, AC-C1 fails on P0 itself.
- Why Medium: whether those files contain such strings is a guess. Recommendation: exclude those two files from AC-C1, or state they use no such string. Priority: Medium.

### Minor notes (never fail the review)
- N1 Citation mismatch. `spec:22` (E2) cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`". `CAPS:161` quotes the pr-submit top-level rule, and no `worker-start` line 38 appears anywhere in `inventory/orca-capabilities.md` (grep). The claim is still supported by `CAPS:49` and `EVIDENCE.md:45` (UNVERIFIED file).
- N2 `spec:16` says the command change is "limited to the worker contract in section 2", while `spec:149` (SA-4) and rows `spec:102,118,124,125` also fix defects (business-panel frontmatter, roadmap flag drift, validate-tests target). Reword `spec:16`.
- N3 WC-10 against AC-4.3: `spec:68` splits only waits "longer than 5 minutes" into at most 4 minutes, while `spec:210` fails any call over 240 s. A 4.5-minute single call passes the rule and fails the check.
- N4 WC-1 evidence: the 45 s cliff at `spec:59` comes from a 45 s limit supplied in that run (`CAPS:49`), not from the 60 s default, so "about 45 s" is not the default's boundary.
- N5 WC-11 (`spec:69`) says no two workers write one file, yet cleanup-audit and index-repo are classed "ready today" with a fixed output location (`spec:85,86`); the table already warns "one audit per worktree at a time".
- N6 The `--unattended` token detection (standalone token, not inside quoted content) is defined in the sandbox command (`command.md:459`) but not in D1 (`spec:227-230`).
- N7 Heartbeat cadence "every 5 minutes" (`spec:68`) rests on one worker's preamble, which `CAPS:130` itself says is not a guide.

### Whittaker adversarial analysis (FR-3 template)
- I can break this specification by **Sequence Attack**. The invariant at **WC-4/WC-6 (`spec:62,64`)** fails when **a retry resumes into the directory of a finished attempt and dies before writing**. Concrete attack: before: `contract.status = blocked` (attempt 1); retry starts, state unchanged; retry crashes; after: coordinator reads `blocked` as the retry's result. Graded Medium (M2).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (`spec:227-229`)** fails when **specification text passed to a command contains the string `--unattended`** (for example a quoted topic). The spec does not say the switch is a standalone token. Graded minor (N6).
- I can break this specification by **Divergence Attack**. The invariant at **WC-10 (`spec:68`) against AC-4.3 (`spec:210`)** fails when **a single wait lasts between 240 s and 300 s**. Concrete attack: one 270 s poll; before: heartbeat last sent at t=0; after: rule passes, check fails. Graded minor (N3).
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`spec:62`)** fails when **no output directory is passed**. Graded Medium (M3).
- Accumulation Attack: no counter or buffer is specified beyond the 3-failure circuit breaker (`CAPS:80`, `CAPS:116`); nothing to break.

### Guard Condition Boundary Table
Classes left out are named in the Status/Behavior text with one-line reasons. Experts: Nygard (construction), Crispin (completeness), Whittaker (attack).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | `spec:63` | Zero/Empty | no report file | failed branch | `--outcome failed` | OK |
| WC-5 outcome mapping | `spec:63` | One/Minimal | `status: partial` | succeeded branch | `--outcome succeeded`, body states `partial` | OK |
| WC-5 outcome mapping | `spec:63` | Typical | `status: succeeded` | succeeded branch | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `spec:63` | Sentinel Value Match | `status: blocked` | failed branch | `--outcome failed`; contract carries `blocked_question` (`spec:62`) | OK |
| WC-5 outcome mapping | `spec:63` | Legitimate Edge Case | status outside the four values, or stale contract | n/a | not specified for the worker; only the test at `spec:183` checks membership | GAP (see M2) |
| WC-5 outcome mapping | `spec:63` | Maximum/Overflow | omitted: enumerated set, no capacity | n/a | n/a | OK |
| WC-10 wait split | `spec:68` | Zero/Empty | no long wait | false | no split needed | OK |
| WC-10 wait split | `spec:68` | Typical | one 3-minute wait | false | heartbeat covered by cadence | OK |
| WC-10 wait split | `spec:68` | Maximum/Overflow | 3600 s eval timeout (`spec:104`) | true | split into waits of at most 4 min | OK |
| WC-10 wait split | `spec:68` | Legitimate Edge Case | single wait of 270 s | false (not longer than 5 min) | allowed by WC-10, fails AC-4.3 `spec:210` | GAP (N3, minor) |
| `--unattended` switch | `spec:51,228` | Zero/Empty | flag absent | false | today's behavior (SA-1, `spec:146`) | OK |
| `--unattended` switch | `spec:51,228` | Sentinel Value Match | token inside quoted content | undefined | not specified (spec text), defined only in `command.md:459` | GAP (N6, minor) |
| contract directory | `spec:62` | Zero/Empty | no `--output` passed | undefined | blocked rows need a place to write; not stated | GAP (M3) |
| contract directory | `spec:62` | Legitimate Edge Case | `--output <file>` | undefined | `<output-dir>` is a "directory" | GAP (M1) |
| task confidence | `spec:121` | Zero/Empty | confidence 0 | below 0.70 | blocked | OK |
| task confidence | `spec:121` | Typical | 0.90 | false | proceeds | OK |
| task confidence | `spec:121` | Legitimate Edge Case | 0.70 to 0.89 | false | unspecified for `--unattended` (the inventory records the "present alternatives" band only for `agent`, `INV-A:36`; for task only `< 0.70`, `INV-B:199`) | OK (no gate reported) |
| nesting depth | `spec:33` | Typical | depth 1 | exceeded on `worker-start` from a worker | refused, `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| nesting depth | `spec:33` | Legitimate Edge Case | `task-create` from a depth-1 worker | unknown | UNVERIFIED, WC-8 forbids either way (`spec:66`, `CAPS:103`) | OK |

FR-8/FR-9 grading: every GAP above was graded by consequence. None names a concrete wrong outcome that follows without a guess, so all are Medium or minor. The table is complete, so FR-10 does not block synthesis.

## Follow-up candidates
Medium: M1, M2, M3, M4, M5, M6. Minor: N1-N7. The session that ran this review asks the user once per loop whether to open an issue for these; it creates none without an answer, and an `--unattended` run only records the list. This report did not ask.
Downstream wiring (not used here): GAP entries and Whittaker findings would feed `sc:adversarial` AD-1 and AD-2.

## Reviser brief
Applies to blocking finding ids only: **B1**.
- Revise only the text B1 names (`spec:182` and `spec:194`); add no rule, mechanism or section that B1 does not call for; every added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave every Medium (M1-M6) and minor (N1-N7) item alone. A brief cannot make them blocking or authorize editing them, including through "apply all findings".
- Brief clauses overridden: none (the coordinator's brief gave only paths and the focus).

verdict: FAIL
