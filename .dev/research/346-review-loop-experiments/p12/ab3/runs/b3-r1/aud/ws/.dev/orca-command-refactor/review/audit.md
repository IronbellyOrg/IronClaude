review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Kind: labelled whole-document audit of the final spec, a first review of the whole document (no `--re-review`, no `--baseline`; `baseline: missing` is expected and not an error).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate sha256: `f3f06d442b7ecafec248d6a15af6b7f95431da195ed53de987f98ee1119f1751`
- Baseline sha256: none given
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- Checkable evidence: only `.dev/orca-command-refactor/README.md` and the three files under `inventory/`. Citations to `src/`, `~/.claude`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `orca-ide` output and other repo files cannot be opened in this sandbox and are UNVERIFIED unless the inventory line that quotes them was read.
- Note on the command definition in the sandbox: the definition of `/sc:spec-panel` used here (`command.md:455-465`) already contains an `## Unattended mode` section that cites `~/.claude/WORKER-CONTRACT.md`, takes `--report-dir`, and writes `<report-dir>/return-contract.yaml`. The spec treats spec-panel as a command that lacks all of this (spec `:120`, `INV-B:177-185`). See M-5.

## Coverage

Read in full: the spec (all 285 lines), README, all three inventories' decisive regions (`commands-a.md:1-120`, `commands-b.md:1-8,28-56,177-186,280-323`, `orca-capabilities.md:10-21,40-190`).

Checked against the inventories: the 43 / 10 / 27 / 6 split (counted from the section 3.1, 3.2 and 4 tables: 10 + 27 + 6 = 43, matching `INV-A:3` and `INV-B:3`); the phase lists (P1 flag set of 14 counts correctly; P2 list of 15 = 11 section 3.2 rows + 4 ready commands; P3 4; P4 3); the `INV-A:` / `INV-B:` / `CAPS:` line citations I sampled (about 70 lines): all pointed at the content claimed, except the notes in M-4 and M-6.

Not covered (UNVERIFIED): every `sk/…`, `cmd/…`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `install_core.py` and `HOW-WE-WORK.md` citation read only through the inventories or not at all; the 340-citation validator claim at spec `:285` was not re-run. Correctness focus is not active, so no State Variable Registry is produced; the Guard Condition Boundary Table is produced because the spec contains threshold guards.

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn.

### F-1 (BLOCKING, MAJOR, Wiegers/Nygard-style consistency): the fixed contract path in WC-4 contradicts WC-11 for every command that takes a file-valued `--output`

- Stated text: WC-4 (spec `:62`) puts a fixed-name `return-contract.yaml` "in the directory that holds the file when `--output` is a file (tdd, init-lite)"; section 3.2 does the same for spec-panel (`:120`, `INV-B:177-185`, "add `--output`"); section 3.1 repeats it for tdd and init-lite (`:87,90`). WC-11 (`:69`) says "Two workers in one worktree must never write the same file".
- Grading check: an implementer who follows the stated text as written builds, for tdd, init-lite and spec-panel, a `return-contract.yaml` at `dirname(--output)/return-contract.yaml`. This is wrong because two workers whose `--output` files share a directory both write that one file, so the second run overwrites the first worker's `status` and `blocked_question`, and the coordinator opens the wrong contract (a `blocked` run read as `succeeded`, or the reverse). This holds with no extra assumption: the spec's own task layout is the case, since this run's reviews are `review/spec-panel.md`, `review/disposition.md` and `review/audit.md` in one directory (README `:19-27`), and the spec never says the brief must give each file-valued `--output` its own directory. WC-11's carve-out (timestamp or slug in default paths) covers default report paths, not the contract name, and section 3.1 handles the same hazard for cleanup-audit only (`:85`, "one audit per worktree").
- Expert: Wiegers (requirement consistency), Whittaker (FR-2.4 sequence/accumulation: the shared file is overwritten).
- Recommendation: either name the contract per output (for example `<output-stem>.return-contract.yaml`) for file-valued `--output`, or add to section 2.3 and WC-4 that a file-valued `--output` must sit in a directory no other worker uses. Narrowing beats adding.
- Priority: High. Quality impact: coordinator reads of worker status become unreliable under parallel dispatch, the headline use of the design.

### F-2 (BLOCKING, MAJOR, Wiegers/Adzic): AC-2.2 names a run whose contract location the spec never defines

- Stated text: AC-2.2 (spec `:200`) runs `/sc:cli-eval run --unattended` with no `--suite` and requires the contract "in the report directory" with `status: blocked`. WC-4 (`:62`) defines the report directory from `--output-dir`, a directory-valued `--output`, the directory of a file-valued `--output`, or "for a command with no such flag, the directory its section 3.1 row names". cli-eval is a section 3.2 command (`:104`), its row says only "contract for both pipelines", and no output flag is added for it.
- Grading check: an implementer who follows the stated text builds a cli-eval contract with no defined location; the fallback in WC-4 points at section 3.1, which does not contain cli-eval. AC-2.2 therefore cannot pass as written: the check has no path to open, and the pre-dispatch requirement of WC-4 ("known before dispatch") cannot hold. The same gap exists for the other section 3.2 rows that say only "contract" and add no flag or directory: cli-portify (`:105`, "file location unnamed"), research (`:116`, generated path only), review-translation (`:117`), roadmap (`:118`), tasklist (`:122`), task (`:121`), recommend (`:115`) and save (`:119`). cli-eval is the one the acceptance table names.
- Expert: Wiegers (testability), Adzic (no concrete example of the cli-eval blocked case).
- Recommendation: extend the WC-4 fallback from "section 3.1 row" to "the section 3.1 or 3.2 row", and give each of those rows a directory or a flag; for the blocked-before-parse case (missing `--suite`) state where the contract goes when no directory has been parsed yet.
- Priority: High.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard.

The central decision (Orca on top, commands unchanged units of work, `--unattended` opt-in, shared contract file) is coherent and the rejected alternative is argued from checkable lines (`CAPS:97-103,145-150`). No blocking architecture finding beyond F-1 and F-2. The Medium findings below are follow-ups.

## Guard Condition Boundary Table

The spec contains threshold guards. Rows are limited to guards the spec itself defines; an input class that cannot occur is left out with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit 60 s | WC-1, spec `:59` | Typical | prompt falls back at 30 s | pass | worker-start succeeds (`EVIDENCE.md:45` via spec) | OK |
| readiness limit 60 s | WC-1, spec `:59` | Legitimate Edge Case | fallback at about 45 s | fail | stated as failing again (`:59`) | OK |
| readiness limit 60 s | WC-1, spec `:59` | Sentinel Value Match | per-start `--timeout-ms` raised by caller | pass | allowed (`CAPS:44-45`) but no phase or AC delivers the fallback (M-1) | GAP |
| wait size 4 min / heartbeat 5 min | WC-10, spec `:68` | One/Minimal | wait of 4 min | pass | heartbeat between waits | OK |
| wait size 4 min / heartbeat 5 min | WC-10, spec `:68` | Maximum/Overflow | single tool call over 5 min | fail | must be split | OK |
| wait size 4 min / heartbeat 5 min | WC-10, spec `:68` | Legitimate Edge Case | wait between 4 and 5 min | not stated | blank: WC-10 says "at most 4", the 4-5 min band is only covered by the decision row (`:266`) | OK (covered by `:266`) |
| nesting depth 1 | R1, WC-8 | Zero/Empty | depth 0 | not stated | not specified; leave out: D5 compares only 1 versus raised | OK (class left out: depth 0 is not a setting the spec considers) |
| nesting depth 1 | R1, WC-8 | Typical | depth 1 (this machine) | pass | worker may not start workers | OK |
| confidence < 0.70 (task) | spec `:121` | Typical | 0.69 | true | resolves as blocked | OK |
| confidence < 0.70 (task) | spec `:121` | Legitimate Edge Case | 0.70 to 0.89 band | false | the spec only names "below 0.70"; the 0.70-0.89 "present alternatives, ask questions" band (`INV-A:` agent row, same threshold family) is not resolved for task | GAP |
| `partial` status | WC-5, spec `:63` | Legitimate Edge Case | `partial` | maps to succeeded | stated, with rationale (`:263`) | OK |
| `blocked` with a worker `ask` (WC-3) | WC-2(c)/WC-3/WC-5 | Legitimate Edge Case | gate fires and worker holds a preamble | either path | WC-3 says "may" ask, WC-5 and AC-2.2 assume `failed`; see M-2 | GAP |

Status GAP rows are graded: the readiness row is Medium (M-1), the task 0.70-0.89 row is Medium (M-7), the ask-versus-blocked row is Medium (M-2). None names a concrete wrong outcome without a guess about which reading an implementer picks.

## Medium and minor findings (follow-up candidates)

None of these triggers a revision and none is in the Reviser brief.

- M-1 (Medium, FR-8): WC-1 (spec `:59`) has an owner "Launch setup, not commands" and no phase, deliverable or acceptance check; section 6 and section 7 never mention it. The only related check is 7.2 step 1 (`state: ready`). A requirement the document never schedules.
- M-2 (Medium): WC-3 (`:61`) lets the worker session `ask` instead of ending blocked, while WC-5 (`:63`) and AC-2.2 (`:200`) expect `worker_done --outcome failed` with a `blocked` contract. The text does not say which the brief selects; a worker that asks gives a legitimate run that fails AC-2.2 as written. Also WC-3 and WC-12 (`:70`) have no acceptance check in section 7.
- M-3 (Medium): AC-C1 (`:172`) requires that no command, skill, agent or core file contains `orca (orchestration|worktree|terminal|agent)`, while P0 (`:158`) adds an Orca section to `core/HOW-WE-WORK.md` and SA-2 (`:147`) allows an Orca example "inside the contract file" (`src/superclaude/core/WORKER-CONTRACT.md`, also under `core/`). If either text names an Orca command, AC-C1 fails on the spec's own deliverables. The spec does not say those two files must avoid the pattern. Also the pipes in AC-C1 are written `\|` for the markdown table, which is not valid ERE if pasted verbatim.
- M-4 (Medium): E3 (`:23`) presents `invocation_method: "skill-direct"` as evidence that Orca workers ran `/sc:adversarial`, while section 1.4(1) (`:43`) says only the nested Agent-tool route was proven and the direct route is untested. Both statements are in the spec; the first should be qualified. (`INV-A:35` row says "Proven as a direct Orca-worker skill call", so the spec's section 1.4 contradicts its own inventory; the contract line itself, `P3-command-set/adversarial/return-contract.yaml:10`, is UNVERIFIED here.)
- M-5 (Medium): the sandbox's command definition of `/sc:spec-panel` already has `--unattended`, `--report-dir` (not `--output`), a refusal without a report directory, and `<report-dir>/return-contract.yaml` (`command.md:459-465`). The spec's spec-panel row (`:120`, "add `--output`; contract", P2) and WC-4's list of directory flags (`--output-dir`, `--output`) do not match it, and WC-4 has no `--report-dir` case. Whether the repo's `cmd/spec-panel.md` matches the inventory or `command.md` is UNVERIFIED; the spec should be reconciled with the command as installed.
- M-6 (Medium): P0-P3 are said to "need no user decision" (`:154`, `:225`), but D4 (`:244`) governs auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (`:100,121,160`). P2 can proceed on D4's recommendation, but the text says phases 0-3 need nothing. Also section 2.3 (`:73`) requires every brief to carry `--unattended`, which no command accepts at P0; AC-0.4 (`:194`) omits it.
- M-7 (Medium): `/sc:task` row (`:121`) resolves confidence "below 0.70" as blocked but the 0.70-0.89 band ("present alternatives, ask questions") is not stated; the inventory source for that band is the agent row (`INV-A:` agent), so the claim for task at `cmd/task.md:93` is UNVERIFIED.
- M-8 (Medium): WC-6 (`:64`) says a retry must not corrupt the first attempt's output and gives "fresh dir" for most commands, but section 2.3 does not require the coordinator to pass a new directory per retry; commands with fixed locations (index-repo `PROJECT_INDEX.md`, init-lite's default path) re-write in place.
- M-9 (Medium): section 3.2 tasklist row (`:122`) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)"; `INV-B:210` records the nesting as Stage 10.5 subagent running `/sc:reflect`, which itself spawns reviewers and adversarial agents, and marks the top-level need UNVERIFIED. The claim is stronger than the inventory. The row also relies on reflect's "headless auto-accept rule" under `--unattended` without saying whether that rule accepts or declines remediation (`sk/sc-reflect-protocol/refs/remediation-handoff.md:239-247`, UNVERIFIED here); if it accepts, tasklist's unattended runs would start corrective work with no gate.
- m-1 (minor): the "10 ready today" label (`:76-79`) is used for commands that all gain a flag and a section in P1 or P2; "ready with the stated flags" would be clearer.
- m-2 (minor): `INV-A:` cites in the spec for "gates per command" (`:60`, `INV-A:76-83`) point at the change table; the row-level evidence is in `INV-A:35-55`.
- m-3 (minor): `CAPS:161` quotes `sc-pr-submit-protocol/SKILL.md:47-49` while the spec cites the repo copy at `:37-39`; line numbers differ between the home copy and the repo copy, UNVERIFIED which one is current.

## Citation spot checks

Citations that matched their inventory line: `INV-A:3,14,35,60-62,65-66,68,90-92,94-98,106,113,118,120`; `INV-B:3,65,105,112,272,285-286,289,292,294,296,301,311,320,323`; `CAPS:44-46,52,58,64,68,72-73,76,79,97-99,103,107,116,129-130,145,147-151,155-156,158-159,161,178,180,186-188`. Citations that could not be opened (UNVERIFIED): all `sk/…`, `cmd/…`, `src/superclaude/cli/install_core.py`, `CLAUDE.md`, `Makefile:68-74`, `pyproject.toml:38`, `EVIDENCE.md`, `.dev/codegraph-migration/…`, and the `grep` results in E5.

## Reviser brief

Repair only the blocking findings F-1, F-2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
