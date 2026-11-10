review: 1 of 3

# Spec panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the whole document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `eb7a9219ddeed9546c90120ee7c914556a7d57ba7d99b5a503bf74f7881bf609`
- baseline: not given (first review; no `--re-review`, no `--baseline`)
- reviewer model used: claude-sonnet-5-5
- panel: Wiegers, Adzic, Cockburn (requirements lead); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (always active)
- citation convention: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: `command.md`, the review-loop prompts file, `README.md`, the candidate (all 285 lines).
- Cross-checked against the three inventories: the 43-command arithmetic (21 + 22; 10 ready + 27 needs-change + 6 coordinator-only, recounted from the section 3 and 4 tables, S:79-139, and INV-A:3, INV-B:3, INV-B:289), phase membership (P1 9+14, P2 15, P3 4, P4 3, all 43 placed once), and about 45 `INV-*`, `CAPS:*` and `README:*` citations. All checked ones match what they are cited for, with one tension noted at F-M5.
- UNVERIFIED (cannot be checked in this sandbox): every citation into `src/superclaude/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `Makefile`, `pyproject.toml`, `install_core.py`, the `.dev/codegraph-migration/` and `.dev/evals/` files, and the Orca install files. The spec's own self-attested checks (S:12, S:285 item 14: "about 340 citations re-read", the grep runs in S:26) are also UNVERIFIED here.
- Not covered: the Orca guides themselves (only the inventory lines that quote them).

## === REQUIREMENTS ANALYSIS ===

### F-1 (blocking, MAJOR, Wiegers/Adzic): the P0 acceptance check cannot pass as written
- Grading sentence: an implementer who follows the stated text as written runs AC-0.4 and gets a check that cannot pass, because S:194 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file", while step 3 of the live check (S:182) requires "its report path is `<report-dir>/return-contract.yaml` (WC-4)" and "its `--outcome` matches the contract's `status`". In P0 no command has `--report-dir` or `--unattended`: S:79 says "a brief before that phase omits them", and S:158-159 puts the contract in P1. So the three smoke commands (troubleshoot, workflow, adversarial) cannot produce a worker_done pointing at that path. Two stated texts contradict (S:182 vs S:79/S:194), and P0's gate decides whether "a failure here reopens section 1" (S:194) and whether P1 may start (S:155).
- Priority: High. Quality impact: the only evidence step that tests the core decision (S:44, S:158) would be reported as failing, or the clause would be silently skipped.
- Recommendation: in AC-0.4 say that step 3's path and contract-status clauses are replaced by "the report path is the command's existing report file (section 3.1 column 'Report today') and the outcome follows WC-5 applied to that file".

### Medium findings (follow-up candidates, none blocking)
- F-M1 (Wiegers): `--unattended` without `--report-dir` has no stated behavior. WC-4 (S:62) says the command writes `<report-dir>/return-contract.yaml`; SA-3 (S:148) says files appear "when the caller passes `--report-dir`"; nothing says whether the command refuses, blocks or falls back. The sibling `command.md:460` refuses before any work. Needs a guess about which reading the implementer picks.
- F-M2 (Wiegers): required inputs are named without being defined. S:104 (cli-eval "the safety flags"), S:113 (post-release "an explicit pre-tag choice"), S:121 (task "refused unless authorized (WC-9)") name no flag; WC-9 (S:67) says authorization is "the command's own explicit flag", but task's EXEMPT `commit`/`push` has no such flag in the spec. Requirement never stated.
- F-M3 (Adzic/Crispin): AC-2.2 (S:200) says "Gate-trigger run per P2 command" with pass condition `blocked`. Several P2 rows have no blocked resolution (auggie-review S:100, cleanup S:103, improve S:110, research S:116, tasklist S:122), so no input can trigger it. Reading it as "per command that has a blocked resolution" passes; the literal reading cannot.
- F-M4 (Wiegers): AC-C5 (S:176) requires that edits to existing lines never appear (`grep '^-[^-]'` prints nothing), yet every changed command gains flags (S:77) and the natural place is the existing Usage line. A flag appended to that line shows as a removed line. Passes only if the implementer adds a new Usage line, which no text says.
- F-M5 (Cockburn): E3 (S:23) cites `return-contract.yaml:10` `invocation_method: "skill-direct"` as proof it "has worked before", while S:43 says that run used the nested Agent-tool route and proves only that route. INV-A:35 says the adversarial skill call was "Proven as a direct Orca-worker skill call". The spec discloses the gap (S:43, S:272), so this is a wording tension in E3 and not a hidden defect.
- F-M6 (Whittaker, Sequence attack): WC-4 requires `<report-dir>` known before dispatch (S:62, S:73) and WC-6 requires a retry not to corrupt the first attempt (S:64). Attack: `worker-start --retry-of` reuses the same brief, so the same `<report-dir>`; the retry overwrites the first attempt's `return-contract.yaml` while the coordinator may still read it. S:73 (what the coordinator owes) does not say a retry brief gets a new report dir, nor that two Tasks never share one.
- F-M7 (Whittaker, Divergence attack): precedence of `--unattended` against `--interactive` is unstated for commands that only say "never `--interactive`" in the brief (adversarial, brainstorm, release-split, S:83-84, S:89). Only some 3.2 rows say "refused" (cleanup S:103, improve S:110, roadmap S:118).
- F-M8 (Whittaker, Sentinel collision): `--unattended` is detected as a token; the spec never says it must be a standalone argument outside quoted prompt text (compare `command.md:459`). Several commands take free-text prompts (tdd S:90, troubleshoot, task).

## === ARCHITECTURE ANALYSIS ===

Overall the decision (Orca on top, commands as units, S:15-16) is consistent with the evidence it cites (E1-E6, R1-R5 match CAPS:92, 97-103, 145-150, 155-161; INV-A:90, INV-B:285-286), and the counts, phases and section 3 versus section 4 split are internally consistent. No architectural contradiction rises to blocking.

- F-M9 (Fowler/Hohpe, Medium): AC-C1 (S:172) greps all of `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output, but SA-2 (S:147) allows Orca to be named "as an example ... inside the contract file", and the contract file lives in `core/` (S:52). A contract file that quotes the `ask` or `worker_done` command line fails AC-C1 in P0. The implementer picks the worse reading only by guessing.
- F-M10 (Nygard, Medium): failure modes are only partly specified. A worker that crashes or is closed before writing the contract gets WC-5 "no report exists" only if it still sends `worker_done`; otherwise the coordinator relies on `worker-show` `agentWait` (S:45) and an unbounded Dispatch (UNVERIFIED item 11, S:282; CAPS:188). No coordinator-side timeout or stall rule is stated. A requirement the document never states.
- F-M11 (Newman, Medium): the contract has no version field. WC-4 (S:62) lists `status`, `command`, `report_path`, `artifacts`, `blocked_question`; the existing workflow contract carries "contract 1.1" (INV-B:272). Later changes to the shared file (S:52) cannot be detected by the test at S:195.
- F-M12 (Hohpe, Medium): WC-10's 5-minute heartbeat cadence (S:68) is taken from one worker's own preamble, not a guide (CAPS:130), yet it is written as a requirement on every future worker session and is encoded in AC-4.3 (S:210). If a coordinator's preamble differs the 4-minute wait split is arbitrary.
- F-M13 (Cockburn, minor): the coordinator's brief template is promised in P0 (S:158) and S:73 lists its contents, but section 2.3 does not state a minimal wording for the `on a blocked gate:` line beyond the two options; consistent enough to implement.

## Guard Condition Boundary Table

Guards found: the nested-depth limit, the readiness limit, the wait-split limit, the confidence threshold, the status vocabulary and the monitor level. One row per applicable class; omitted classes have a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| nested depth `maxDepth=1` | S:33, S:250 | Zero/Empty | depth 0 (root coordinator) | allowed | coordinator starts workers (S:15) | OK |
| nested depth `maxDepth=1` | S:33 | Typical | depth 1 worker calls `worker-start` | refused | `nested_worker_depth_exceeded`; WC-8 forbids it | OK |
| nested depth `maxDepth=1` | S:249-253 | Legitimate Edge Case | user raises depth (D5 b) | allowed | R1 protection said to break; WC-8 still forbids calls | OK |
| readiness limit 60 s | S:59 | Typical | prompt falls back at 30 s | pass | passes (EVIDENCE cited) | OK |
| readiness limit 60 s | S:59 | Maximum/Overflow | fallback above about 45 s | fail | fails again (cited) | OK |
| readiness limit 60 s | S:59 | Zero/Empty | no fallback at all | fail | WC-1 requires a fallback; owner is launch setup, no phase or check covers WC-1 | GAP (Medium: requirement without a check) |
| wait split 4 min | S:68 | Maximum/Overflow | single tool call over 5 min | breaks heartbeat | must be split | OK |
| wait split 4 min | S:68, S:114 | Legitimate Edge Case | pr-submit 600 s cumulative budget | per-iteration under 4 min | poll script runtime UNVERIFIED (S:283) | GAP (Medium: stated as UNVERIFIED) |
| confidence `< 0.70` (task) | S:121 | Sentinel Value Match | exactly 0.70 | not stated | spec says "below 0.70" only; boundary inherited from the command | GAP (Medium: edge value inferrable, minor) |
| `--monitor 1` (pr-submit) | S:114 | Legitimate Edge Case | `--monitor 0`, `2`, `3` under `--unattended` | not stated | only `1` is refused; others are unspecified | GAP (Medium) |
| status vocabulary | S:62-63 | Sentinel Value Match | `status` missing or outside the four values | not stated | WC-5 covers "no report exists" only; the S:184 check catches it, the rule does not | GAP (Medium) |
| `--report-dir` | S:62 | Zero/Empty | flag absent under `--unattended` | not stated | see F-M1 | GAP (Medium) |

Classes left out: One/Minimal and Typical for the status vocabulary and the monitor level (no distinct behavior beyond the rows above). No GAP names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk, so under FR-8 and FR-9 none is blocking. The table is complete, so synthesis is not blocked (FR-10).

## Quantity check (count conservation)

43 commands (S:76) = 10 ready (S:81-93) + 27 needs-change (S:98-126) + 6 coordinator-only (S:131-138); phase cells place 14 + 9 (load excepted: 8 + load) in P1, 15 in P2, 4 in P3, 3 in P4 = 43 − 6. No mismatch found; no CRITICAL dimensional finding.

## Adversarial summary (Whittaker)

- Zero/Empty: F-M1 (no `--report-dir`), status vocabulary row. Divergence: F-M7. Sentinel collision: F-M8. Sequence: F-M6 (retry overwrites contract). Accumulation: no counters or buffers in the spec; none found.
- Concrete attack on F-1: P0 run, step 3, `worker_done --report-path` equals the troubleshoot `REPORT.md` path, the check demands `<report-dir>/return-contract.yaml`, so the phase's own gate reports FAIL for a correct run.

## Follow-up candidates

F-M1, F-M2, F-M3, F-M4, F-M5, F-M6, F-M7, F-M8, F-M9, F-M10, F-M11, F-M12, F-M13, plus the Medium GAP rows in the boundary table. Per the command, the session that ran the review asks the user once per loop whether to open an issue for these; this worker could not ask and created none, so the coordinator carries that question.

## Reviser brief

Blocking finding ids: F-1 only.

- Revise only text F-1 names (AC-0.4, S:194, and if needed the 7.2 step 3 pass condition, S:182).
- Add no rule, mechanism or section that no blocking finding calls for; cite the finding id (F-1) on each added paragraph or table.
- Prefer deleting or narrowing to adding.
- Report the byte size of the file before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings (F-M1 to F-M13) alone; a brief cannot make them blocking or authorize editing them, including through "apply all findings".
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
