review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `e83580105a91cbd66307f4ec8d971d860124f6e64bbad15157d508a0bfc3be1e`
- baseline: none given (no `--re-review`, no `--baseline`); this is a labelled whole-document first review
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- panel (focus requirements): Wiegers (lead), Adzic, Cockburn. Panel (focus architecture): Fowler (lead), Newman, Hohpe, Nygard. Whittaker (adversarial) is active in every review (`command.md:83`).
- brief clauses overridden: none.
- Citation basis: the only evidence checkable in this sandbox is `README.md`, `inventory/commands-a.md` (`INV-A`), `inventory/commands-b.md` (`INV-B`), `inventory/orca-capabilities.md` (`CAPS`) and the spec itself. Every `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` and Orca-binary citation is marked UNVERIFIED here unless it is a quote carried inside an inventory line I read.

## Coverage
Read in full: the spec (1-285), `README.md`, `command.md`, the review-loop prompts file. Read for citation checks: `INV-A:1-120`, `INV-B:1-66` and `INV-B:260-323`, `CAPS:8-188` (lines 40-165 in full). Spot-checked and found as cited: `INV-A:3,14,17,35-55,60-62,65-66,68,76-83,90-92,95-98,106,113,118,120`; `INV-B:3,31-52,65,105,112,267-275,285-301,311,320,323`; `CAPS:44-52,58-68,72-80,84-93,97-103,107-116,129-130,145-162,177-188`; `README.md:6,11-17,30-31,35`. The totals 10 / 27 / 6 = 43 check against `INV-A:73` (5+13+3) and `INV-B:278` (5+14+3), and the three spec tables list 10, 27 and 6 distinct commands. Phase column counts: 3.2 rows give P1 = 9, P2 = 11, P3 = 4, P4 = 3 (27); section 6 P2 lists 15 because it adds reflect, release-split, tdd, troubleshoot from 3.1.
NOT covered (UNVERIFIED, no file in sandbox): every `cmd/`, `sk/`, `ag/` line cited in sections 3 and 4, `CLAUDE.md:*`, `HOW-WE-WORK.md:*`, `install_core.py:*`, `Makefile:*`, `pyproject.toml:38`, `EVIDENCE.md:*` (except as quoted at `CAPS:49`), `.dev/codegraph-migration/*`, Orca binary files except as quoted in `CAPS`. I did not run `git`, `make` or any Orca command.

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking) AC-1.1 and the P1 scope contradict the phase column, D3(a), section 4 and the `load` row
Experts: Wiegers (traceability), Adzic.
Grading sentence: an implementer who follows the stated text as written builds a Phase 1 that adds a `## Unattended mode` section naming `return-contract.yaml` to all 37 worker-capable commands, and that is wrong because the same text says the opposite for several of them.
- `spec:195` (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `spec:159` (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". Those sets contain 37 commands, including implement, post-release and pr-submit (P4).
- `spec:162` and `spec:154`: Phase 4 "waits for answers to D2-D4" and only applies them then; `spec:114` and `spec:239-242`: D3(a) (recommended, and `spec:225` says phases 0-3 proceed on the recommendations) is "no pr-submit changes in Phase 4", and `spec:139` says pr-submit stays a worker candidate only if D3 is accepted. Under D3(a) pr-submit is coordinator-only like the section-4 commands, but AC-1.1 requires it to carry a worker section at P1 (while `spec:195` also requires that no section-4 command has one).
- `spec:112`: the `load` row says Report "none (see note)" and Phase "P1 (usage line only)", and `spec:265` decides no report file for `load`; `spec:76` says only changed commands gain the section. AC-1.1 still demands that its section name `return-contract.yaml`, which `load` never writes.
- `spec:83-92`: brainstorm and init-lite have "Small fix: None" yet AC-1.1 requires a new section on them in P1.
Count trace (Quantity Flow): AC-1.1 asserts 37 sections at P1; the Phase column assigns 9 (3.2) + 3 or 4 (3.1 fixes: adversarial, cleanup-audit, index-repo, workflow) = 12-13 commands to P1 and 24 elsewhere; 3 of the 24 are P4 commands the spec says must wait for a user decision. AC-1.1 cannot be passed at the end of P1 without either breaking D3(a)/the P4 wait or failing on `load`.
Recommendation: restrict AC-1.1 and the P1 scope sentence to the commands whose Phase column is P1 (plus the 3.1 commands P1 touches), and let later phases add their own assertion (AC-2.1, AC-3.x, AC-4.x already do this); delete the `load` requirement to name `return-contract.yaml`. Priority High.

### B-2 (CRITICAL, blocking) The contract path is undefined for commands whose output flag names a file, and AC-2.2 uses such a command
Experts: Wiegers, Whittaker (sentinel/degenerate input), Fowler.
Grading sentence: an implementer who follows WC-4 as written gives a `--output <file>` command no contract directory to write into, and that is wrong because AC-2.2 and 7.2 step 4 then have no `<contract>` path to test.
- `spec:62` (WC-4): the contract goes to `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; `spec:76` repeats it for every row that names no path.
- `spec:90` (tdd) and `spec:87` (init-lite) tell the brief to pass `--output <file>` and name the deliverable as that file; `spec:120` (spec-panel) adds `--output`; `spec:200` (AC-2.2) runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked`. The text passes no directory, so `<output-dir>` has no value, and `test -s <contract>` (`spec:183`) cannot be evaluated. The spec's own `F1` marker (`spec:62`, `spec:76`, `spec:182`) is never defined.
- Corroboration inside the sandbox: the later command text resolves this by adding a separate directory flag, `--report-dir <dir>` ("`--output` is file-valued"), `command.md:460-461`. The spec has no such flag (`grep report-dir` over the spec prints nothing).
Recommendation: state one rule for file-valued output flags (for example a separate contract directory flag named in the brief, or the file's parent directory), and apply it to tdd, init-lite, spec-panel and any other row that passes a file. Priority High.

## === ARCHITECTURE ANALYSIS ===

Positive checks (no finding): the core decision (section 1) is consistent with `CAPS:97-103` (depth 1), `CAPS:147-150` (outside-Orca failures, pane-bound `worker_done`) and `INV-A:90`, `INV-B:285-286` (orchestrating commands coordinator-only). Section 1.4 states its own evidence gaps and matches `INV-B:323` and `CAPS:156,187`. The R1 claim is hedged where `CAPS:103` is UNVERIFIED. Counts reconcile (see Coverage).

### Medium and minor findings (all under follow-up candidates, none blocking)

## === FOLLOW-UP CANDIDATES (Medium and minor) ===
Medium (warnings, no revision triggered):
- M-1 `/sc:tasklist` resolution contradicts its inventory and rests on an unverified nesting claim. `spec:122` makes Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies" and calls the reflect fan-out "one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)". `INV-B:46` recommends dropping `--remediate` in Stage 10.5 and marks the reflect-inside-subagent nesting UNVERIFIED; `INV-B:322` lists who answers the offer as open. The spec never says what the headless rule does (accept or decline) because the file it cites (`remediation-handoff.md:239-247`) is UNVERIFIED here; `spec:88` and `spec:151` call it "auto-accept", which could start a corrective-package hand-off per reflect. The spec needs to say the outcome and drop the "inside the nesting limit" assertion or mark it UNVERIFIED. (Whittaker, Sequence.)
- M-2 `AC-C1` vs `SA-2`. `spec:147` allows an Orca mention "inside the contract file" and `spec:158` adds an Orca section to `core/HOW-WE-WORK.md`; `spec:172` greps `src/superclaude/core` for `orca(-ide) orchestration|worktree|terminal|agent` and requires no output. A contract file that shows `orca orchestration ask` as an example fails its own check. Exclude the contract and routing guide from the grep or ban the literal form.
- M-3 Decisions D4 and the phase gates. `spec:154` says "Phases 1-3 need no user decision", yet `spec:244` lists auggie-review `--post-pr` and task `commit`/`push` (both P2 rows, `spec:100,121`) as affected by D4. Section 9's "proceed on the recommendations" (`spec:225`) covers it; say so in section 6.
- M-4 Concurrency of fixed output paths is a brief obligation the brief template omits. `spec:85` (cleanup-audit, "one audit per worktree at a time") and `spec:86` (`PROJECT_INDEX.md`) rely on WC-11 (`spec:69`), but section 2.3 (`spec:73`) does not tell the coordinator to serialize workers that share a fixed path. Two workers in one worktree (`CAPS:115`) would overwrite each other. (Whittaker, Accumulation/Divergence.)
- M-5 `--unattended` in P0 briefs. `spec:73` requires `--unattended` in every brief and `spec:158,194` run three commands in P0 before any command accepts it. Say whether P0 briefs omit the flag (the 3.1 "Brief must pass" column omits it).
- M-6 WC-10 vs pr-submit poll sleeps. `spec:114` leaves the poll script runtime UNVERIFIED (`spec:283`) and the sleep is "at least `--poll-interval`" (`spec:68`); a poll interval of 4 minutes or more breaks the 4-minute rule with no stated cap on the flag. State a maximum.
- M-7 AC-0.4 step 4 (`spec:194`) says to use "the command's existing report file", but 7.2 step 4 (`spec:183`) is a YAML status check; troubleshoot's `REPORT.md` has no `status` key. Give the P0 pass condition for a markdown report.
- M-8 SA-4's list of allowed defect fixes (`spec:149`) omits edits the spec itself calls for: cleanup-audit and index-repo (`spec:85-86`, P1), reflect (`spec:88`, P2). AC-C5 (`spec:176`) flags any deleted line. Add them or state they are additive.

Minor notes:
- m-1 `spec:62`, `spec:76`, `spec:182`, `spec:198`: the label `F1` is never defined in the document (revision trace left in the text).
- m-2 `spec:92` says the workflow row needs "None" for fixes while `spec:159` and AC-1.4 (`spec:198`) list a workflow fix in P1.
- m-3 `spec:59` (WC-1) cites the readiness limit as 60 s; the run it quotes failed at a 45-second limit (`CAPS:49`). Harmless, but the figure the 30 s fallback is tested against is 45 s, not 60 s.
- m-4 `CAPS:161` cites the pr-submit top-level rule at `~/.claude/skills/.../SKILL.md:47-49`; the spec cites `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`spec:65`, installed vs source copy, line numbers differ). UNVERIFIED which is right.
- m-5 WC-6 (`spec:64`) says a retry must not corrupt the first attempt, but init-lite and index-repo overwrite their reports by design (`spec:86-87`); say retries of those commands are idempotent overwrites.
- m-6 E5 (`spec:25`) and `spec:11`'s re-read list are claims about greps and files outside the sandbox: UNVERIFIED here.

## Guard Condition Boundary Table
Guards found in the spec. Classes left out are explained in one line each. Rows with GAP are graded in the findings above; a GAP is blocking only where noted.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit | `spec:59` WC-1 | Zero/Empty | no prompt, input box reached at 0 s | true | passes | OK |
| readiness limit | `spec:59` WC-1 | Typical | wrapper fallback 30 s | true | `EVIDENCE.md:45` passes at 34 s via `CAPS:49` | OK |
| readiness limit | `spec:59` WC-1 | Maximum/Overflow | fallback above about 45 s | false | fails again (`CAPS:49`) | OK |
| readiness limit | `spec:59` WC-1 | Legitimate Edge Case | `--timeout-ms` raised per start | true | `CAPS:44-45` | OK |
| unattended gate | `spec:60` WC-2 | Zero/Empty | command with no gate | true | no-op `--unattended` (`spec:159`) | OK |
| unattended gate | `spec:60` WC-2 | Typical | gate with a flag value supplied | true | caller flag wins | OK |
| unattended gate | `spec:60` WC-2 | Legitimate Edge Case | gate in a file-valued `--output` command (tdd) | true | contract path undefined | GAP (B-2) |
| contract path | `spec:62` WC-4 | Zero/Empty | stop before the directory exists | n/a | no contract; `worker_done` without `--report-path` | OK |
| contract path | `spec:62` WC-4 | Typical | `--output-dir` passed | true | `<dir>/return-contract.yaml` | OK |
| contract path | `spec:62` WC-4 | Legitimate Edge Case | `--output <file>` passed | false | unspecified | GAP (B-2) |
| outcome map | `spec:63` WC-5 | Legitimate Edge Case | status `partial` | true | `succeeded`, body says partial | OK |
| outcome map | `spec:63` WC-5 | Zero/Empty | no report exists | true | `failed` | OK |
| wait split | `spec:68` WC-10 | Typical | single call over 5 min | true | split into at most 4 min | OK |
| wait split | `spec:68` WC-10 | Maximum/Overflow | `--poll-interval` of 4 min or more | true | unspecified | GAP (M-6, Medium) |
| confidence guard | `spec:121` task | Typical | below 0.70 | true | blocked | OK |
| confidence guard | `spec:121` task | Legitimate Edge Case | exactly 0.70 | false | not stated; inventory line (`INV-B:45`) says "< 0.70" | OK (strict less-than is stated) |
| nesting depth | `spec:33` R1 | Typical | depth 1 | true | refusal presumed (hedged, `CAPS:103`) | OK |
| nesting depth | `spec:33` R1 | Sentinel Value Match | setting 0 or malformed | false | `CAPS:100` falls back to default | OK |
| phase gate AC-1.1 | `spec:195` | Maximum/Overflow | 37 commands asserted vs 12-13 assigned to P1 | true | contradicts phase column | GAP (B-1) |
| `--unattended` on P0 brief | `spec:73` vs `spec:158` | Legitimate Edge Case | flag not yet implemented | n/a | unspecified | GAP (M-5, Medium) |
Classes omitted: One/Minimal and Sentinel for WC-4, WC-5 and the readiness guard cannot occur beyond the rows shown (one report file, two outcome values, a time value).

## State Variable Registry
Not produced: `--focus correctness` is not active. Advisory: the spec describes a mutable per-run state machine (task, dispatch, report, release, retry counters), so `--focus correctness` would be worth running on a revision; this is a suggestion only.

## Quantity Flow Diagram (pipeline: 43 commands to phases)
```text
[cmd/: 43 commands] --> [Inventory verdict] --> [10 ready (3.1)] [27 needs change (3.2)] [6 coordinator-only (4)]
[3.1: 10] --> P1 fixes: adversarial, cleanup-audit, index-repo (+workflow listed, row says None) = 3-4 | P2: reflect, release-split, tdd, troubleshoot = 4 | no change: brainstorm, init-lite = 2
[3.2: 27] --> P1 9 | P2 11 | P3 4 | P4 3
[AC-1.1: asserts 37 sections at end of P1] <-- MISMATCH (12-13 assigned to P1; 3 of the rest are P4 and wait on D2-D4; load has no contract)
```

## Reviser brief
Blocking finding ids: B-1, B-2. Only these. Contract for the reviser (restating the command's Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names: B-1 (`spec:159`, `spec:195`, and the `load` requirement in AC-1.1) and B-2 (`spec:62`, `spec:76`, and the undefined `F1` marker where it carries the path rule).
- Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium findings (M-1 to M-8) and minor notes (m-1 to m-6) alone; they never trigger a revision.
- Return the candidate once; do not award a PASS.

follow-up candidates: M-1 to M-8, m-1 to m-6 (above). Issue creation for these: the session that ran this review asks the user once per loop whether to open an issue; this run could not ask and creates none.

coverage: whole-document first review (not scoped); citations to `src/`, `CLAUDE.md`, `EVIDENCE.md` and the Orca binary are UNVERIFIED in this sandbox.

verdict: FAIL
