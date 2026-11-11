review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec (a first review of the full document, not a re-review). No `--re-review` and no `--baseline` were given, so this is a first review and no `baseline: missing` note applies.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines)
- candidate sha256: `b72ae0165828ae31e6e86c4c17ddcc94a378f90648e36bc5398fab3017942e03`
- baseline sha256: none given
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full first (the hard gate at `command.md:266-268`).
- binding context read first: `.dev/orca-command-refactor/README.md:1-39`.
- Notation: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `CMD:N` = line N of the `/sc:spec-panel` definition file `command.md` that sits in the audit sandbox root.

## Coverage

What I covered:
- The whole candidate, sections 1-9, the Decisions table and the 15 UNVERIFIED items.
- Cross-checks against the three inventories. I re-read every `INV-A`, `INV-B` and `CAPS` line I cite below.
- Arithmetic checks:
  - 21 + 22 = 43 commands.
  - Split 10 / 27 / 6, matching `INV-A:73` (5 / 13 / 3) and the INV-B tallies (5 / 14 / 3).
  - Phase assignment: P1 9 needs-change + P2 11 + P3 4 + P4 3 = 27, and the 10 ready commands are spread over P1 fixes (4), P2 gate fixes (4) and no change (2). The counts are conserved.
- The `/sc:spec-panel` row against the command definition `command.md`, which is inside the sandbox and so checkable.

What I could not check: every citation into `src/superclaude/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `tests/` and `.dev/codegraph-migration/...` or `.dev/evals/...`. None of those paths exist in the workspace, so each one is UNVERIFIED here (SPEC:11 says 11 of them were re-read by the author, which I cannot confirm). Inventory line numbers that quote those files were checked only as far as the inventory text itself.

One citation discrepancy:
- SPEC:65, `INV-A:14` and `CAPS:161` cite the pr-submit top-level rule at `SKILL.md:37-39` and at `SKILL.md:47-49`. The two numbers come from two different copies of the file (`src/` versus `~/.claude/`). UNVERIFIED which is current. Minor.

## Hard-gate artifacts

### Guard Condition Boundary Table (candidate guards)
Mandatory Outputs under `--focus correctness` are not active (focus is requirements,architecture). I still ran the table because the candidate is full of numeric and boolean guards (`command.md:313`). Classes that cannot occur for a guard are omitted with a reason (`command.md:317`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` token present | SPEC:51, SPEC:195 (AC-1.1) | Zero/Empty: `--unattended` given but no output directory or flag | no `--output`/`--output-dir` | WC-4 path undefined | Not specified. SA-3 says report files are written "only in unattended mode or when the caller passes the new output flag" (SPEC:148), so the file is expected, but its location is not stated | GAP (follow-up M-2) |
| `--unattended` token present | SPEC:51, SPEC:195 | Typical | `--unattended --output <dir>` | true | contract at `<dir>/return-contract.yaml` (SPEC:62) | OK |
| `--unattended` token present | SPEC:159 (P1), SPEC:195 (AC-1.1) | Legitimate Edge Case: gated command (implement, post-release, pr-submit) receives the flag before D2-D4 are answered | `--unattended` on a P4 command at P1 | flag accepted, gate unresolved | AC-1.1 demands an `## Unattended mode` section at P1; SPEC:162 and SPEC:241 defer the behaviour to P4 or to "no change" | GAP (blocking B-2) |
| report status to `--outcome` map | SPEC:63 (WC-5) | Zero/Empty: no report file | none | `--outcome failed` | specified | OK |
| report status to `--outcome` map | SPEC:63 | Sentinel Value Match: status outside the four-value set | e.g. a command's own `completed` | n/a | Not specified (WC-4 fixes the set at SPEC:62, but no rule for an unknown value) | GAP, minor |
| report status to `--outcome` map | SPEC:63, SPEC:262-263 | Legitimate Edge Case: `partial` | `partial` | `succeeded` | specified, with the body sentence | OK |
| Heartbeat/wait threshold 5 min / 4 min | SPEC:68 (WC-10) | Maximum/Overflow: a single blocking call over 5 min | cli-eval up to 3600 s per eval | split into waits of at most 4 min | specified; only checked for pr-submit (AC-4.3, SPEC:210), not for cli-eval | OK for the rule, GAP for acceptance (follow-up M-6) |
| Heartbeat/wait threshold | SPEC:68 | Zero/Empty: a command with no waits | n/a | n/a | not applicable: the guard only applies to blocking waits | OK (omitted class) |
| Readiness limit 60 s | SPEC:59 (WC-1) | Maximum/Overflow: a prompt falling back at 45 s or more | 45 s | fails again | specified at `EVIDENCE.md:45,56` via SPEC:59 | OK |
| Readiness limit 60 s | SPEC:59 | Typical | 30 s fallback | passes | specified | OK |
| Retry gate `--retry-of` / resume flag | SPEC:64 (WC-6) | One/Minimal: second attempt with the same `<output-dir>` and no resume flag | same dir, no flag | roadmap "starts fresh" (AC-3.2, SPEC:205) | WC-6 says a re-run must not corrupt the first attempt; AC-3.2 starts fresh inside the same directory, which overwrites it | GAP (follow-up M-6) |
| Confidence below 0.70 (task) | SPEC:121 | Zero/Empty: confidence exactly 0.70 | 0.70 | not stated at this spec level | "below 0.70" resolves as blocked; 0.70 itself is left to the command (`INV-B:292` quotes `< 0.70`) | OK (inherited, minor) |
| `--monitor 1` (pr-submit) | SPEC:114 | Legitimate Edge Case | `--monitor 1` | refused under `--unattended` | specified | OK |
| Depth limit 1 | SPEC:33 (R1), `CAPS:97-98` | Maximum/Overflow: depth 2 | 2 | `nested_worker_depth_exceeded` | specified, call sites UNVERIFIED (`CAPS:103`) | OK |
| Depth limit 1 | SPEC:33 | Zero/Empty | depth 0 (coordinator) | allowed | specified at `CAPS:97` | OK |
| Output directory per command | SPEC:62 (WC-4) | One/Minimal: command with a fixed output location (cleanup-audit `.claude-audit/`, index-repo `PROJECT_INDEX.md`) | no output flag | contract location | Not specified for these two rows (SPEC:85-86) | GAP (follow-up M-3) |

### Quantity Flow (Pipeline Dimensional Analysis)
The spec is a 43-command to phase assignment, so I checked count conservation; the check passes.

```text
[43 commands]
  --> [10 ready]        --> [P0 smoke 3 | P1 fixes 4 | P2 gate fixes 4 | no change 2 (brainstorm, init-lite)]   = 10 ... but 3 smoke commands are inside the 10
  --> [27 need change]  --> [P1 9 | P2 11 | P3 4 | P4 3]                                                         = 27
  --> [6 coordinator-only]                                                                                       = 6
  Consumers: AC-1.1 asserts a section on "every command in 3.1-3.2 except load" = 36 commands, at P1  <-- MISMATCH with the 3 P4 commands (B-2)
```

### Whittaker attack summary (all five methodologies were tried; each hit is a finding below, the rest found nothing blocking)
- Zero/Empty: `--unattended` with no output dir (M-2); P0 smoke runs with no `--unattended` and no contract (B-1).
- Divergence: ready commands vs P2 gate fixes (the "ready today" label, SPEC:78-79, against SPEC:88-91, which still need P2 changes) is stated, not contradicted. No finding.
- Sentinel Collision: `blocked` status vs Orca's two-value outcome (SPEC:63) is handled by the mapping. No finding.
- Sequence: P1 before P4, with `--unattended` accepted early (B-2).
- Accumulation: two workers in one worktree on fixed output paths (M-3).

## Findings

### Requirements analysis

**B-1 (CRITICAL as graded: blocking) AC-0.4 cannot pass as written. Experts: Wiegers, Adzic.**
- Stated texts:
  - AC-0.4 (SPEC:194) says the three P0 smoke runs must pass "steps 1-3 and 5-7" of the 7.2 live check, and that "step 4 uses the command's existing report file, since the contract arrives in P1".
  - 7.2 step 3 (SPEC:182) requires that "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
  - Section 2.3 (SPEC:73) says the brief states "the exact command line including `--unattended`".
  - At P0 no command accepts `--unattended`, and no WC-4 contract exists for troubleshoot (it reports `REPORT.md`, SPEC:91). Workflow's contract is at a generated path (SPEC:92) and adversarial's filename is unfixed until P1 (SPEC:83).
- An implementer who follows the stated text as written builds a P0 gate whose step 3 asks for a WC-4 contract path and a contract `status` that do not exist yet, and whose step 1 brief asks for a flag that is not accepted yet. The P0 phase can never pass, and P0 gates everything (SPEC:154), so the whole rollout cannot start. The failure follows from the two stated texts alone.
- Evidence: SPEC:73, SPEC:83, SPEC:91-92, SPEC:154, SPEC:182, SPEC:194; also SPEC:79 ("the worker reports the named file until Phase 1 adds the contract").
- Recommendation (narrow, no new mechanism): make AC-0.4 say which pass conditions of step 3 apply in P0 (outcome matches the existing report file's status; report path is that existing file), and say the P0 brief omits `--unattended`. Priority High. Quality impact: restores a passable P0 gate.

**B-2 (CRITICAL as graded: blocking) P1 acceptance and P1 scope contradict the P4 deferral and decision D3. Experts: Wiegers, Fowler.**
- Stated texts:
  - AC-1.1 (SPEC:195): the test asserts that "every command in sections 3.1-3.2 except `/sc:load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - P1 scope (SPEC:159): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
  - Section 3.2 (SPEC:109, SPEC:113-114) lists implement, post-release and pr-submit as P4, each with a gate that is not a no-op.
  - SPEC:154: "Phase 4 waits for answers to D2-D4". SPEC:162 puts the implement halt path, the post-release pre-authorization and pr-submit-as-worker in P4.
  - D3(a), the recommendation (SPEC:240): "no pr-submit changes in Phase 4". SPEC:139 says pr-submit is a worker candidate "only if the user accepts open decision D3".
- An implementer who follows the stated text as written builds, in P1, an `## Unattended mode` section and an accepted `--unattended` flag on `/sc:pr-submit`, `/sc:implement` and `/sc:post-release`. That ships three things the document says must wait for a user decision, and under the recommended D3(a) ships a change to pr-submit the spec says not to make. It also ships a flag that is accepted but does not resolve the command's gates, so a coordinator that follows SPEC:73 and passes `--unattended` to implement or post-release gets a worker that stalls on the Ruling or the outward-action confirmation. Both texts are stated; no extra assumption is needed.
- Evidence: SPEC:109, SPEC:113-114, SPEC:139, SPEC:154, SPEC:159, SPEC:162, SPEC:195, SPEC:240.
- Recommendation (narrow): restrict P1's flag scope and AC-1.1 to the commands whose phase is P1 to P3, and name implement, post-release and pr-submit as exempt until P4 (same way `/sc:load` is exempted by name). Priority High.

### Architecture analysis

No blocking architecture finding. The central decision (Orca coordinates, commands stay units of work, SPEC:13-39) is internally consistent with `CAPS:97-103` (depth 1), `CAPS:147-150` (standalone failure modes) and the two inventories (INV-A:90, INV-B:285-286). Section 1.4 states its own evidence gaps plainly (SPEC:41-45); the live-run gap is the one B-1 puts at risk.

## Follow-up candidates (Medium and minor; none triggers a revision)

Each Medium finding needs a guess about which of two readings an implementer picks, or is a requirement the document never states. None is graded blocking.

- **M-1 (Medium, MAJOR label) The `/sc:spec-panel` row is stale against the command definition.**
  - SPEC:120 says "no output flag exists today, `INV-B:182`". `INV-B:182` says no `--output` flag exists at `cmd/spec-panel.md:22`.
  - The command definition now has `--output <file>` and `--report-dir <dir>` (`CMD:22-23`), an `## Unattended mode` section that points at `~/.claude/WORKER-CONTRACT.md` (`CMD:455-465`), and a contract at `<report-dir>/return-contract.yaml` (`CMD:461`). Its `(WC-4)` there refers to a rule about git-ignored paths (`CMD:461`) that the candidate's WC-4 (SPEC:62) does not contain.
  - SPEC:286 (item 15) already hedges the directory-flag part, which is why this is Medium and not blocking. It does not cover the `--output <file>` claim, the existing `## Unattended mode` section (so SPEC:76's 27 "needs a change" overcounts by one if the section already exists), or the WC-4 numbering clash.
  - Recommendation: re-read the command and restate the row as "already has `--report-dir`" or reconcile the WC numbering. Priority Medium.
- **M-2 (Medium) `--unattended` with no output directory has no stated behaviour.** SPEC:62 says the brief passes the output flag, SPEC:148 writes files "only in unattended mode", but nothing says what a command does when the flag is absent. The command definition refuses before any work and prints in chat only (`CMD:460`); that is the kind of rule the spec lacks. A reader may pick a default path, break WC-4 "known before dispatch" or refuse. Priority Medium.
- **M-3 (Medium) Fixed-output commands have no contract location and break WC-11.**
  - cleanup-audit writes `.claude-audit/` (SPEC:85); index-repo writes `PROJECT_INDEX.md`, location only implied (SPEC:86; `INV-A:53`, `INV-A:117`).
  - Neither row names a flag or a directory for `return-contract.yaml`, though AC-1.1 requires the section and WC-4 requires a known path.
  - WC-11 (SPEC:69) says two workers in one worktree must never write the same file. The cleanup-audit row records the limit ("one audit per worktree at a time"); the index-repo row does not, and two index-repo workers would clobber one file.
- **M-4 (Medium) AC-C1 and SA-2 do not agree on the contract file and the routing guide.**
  - AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing.
  - P0 adds `core/WORKER-CONTRACT.md` and an Orca section to `core/HOW-WE-WORK.md` (SPEC:158). SA-2 allows an Orca mention "inside the contract file" (SPEC:147), and a routing section about Orca will plausibly name orchestration commands. The text does not say those files avoid the pattern, so the P0 check could fail on its own deliverable. Priority Medium.
- **M-5 (Medium) `--output` changes type between commands.** SPEC:62 and N-1 say `--output <dir>` and `--output-dir <dir>` take a directory, but tdd, init-lite and spec-panel's existing `--output` take a file (SPEC:62, SPEC:90; `CMD:23`), and the analyze row "add `--output`" (SPEC:99) leaves its type to the reader. One flag name with two meanings across commands invites a wrong brief. Priority Medium.
- **M-6 (Medium) Acceptance coverage is thin for several requirements.**
  - WC-1, WC-6, WC-12 and the cli-eval part of WC-10 have no check in section 7 (SPEC:59, 64, 68, 70; only pr-submit is checked at AC-4.3, SPEC:210).
  - AC-3.2 (SPEC:205) starts roadmap fresh in an existing directory, which sits uneasily with WC-6 "must not corrupt the first attempt's output" (SPEC:64).
- **M-7 (Medium) AC-C5 forbids all removed lines, but adding `--unattended` to a Usage line replaces that line.** AC-C5 (SPEC:176) and SA-4 (SPEC:149) say edits are additive, and the check is `grep '^-[^-]'`. A flag added to an existing Usage code line shows as a `-` line. The text does not say new flags go on new lines. Priority Medium.
- **m-1 (minor)** Decisions table: "ladder rung 2" (SPEC:261) is not defined in the document.
- **m-2 (minor)** SPEC:59-70 WC rows use "Owner" but WC-12 and WC-5 list the worker session, not a command, so AC-1.1's per-command section cannot carry them; fine, but SPEC:70 could say so.
- **m-3 (minor)** Pr-submit citation differs between copies (`SKILL.md:37-39` at SPEC:65 versus `:47-49` at `CAPS:161`); UNVERIFIED which is current.
- **m-4 (minor)** Section 3.1 is titled "Ready today" yet four rows carry P2 gate fixes (SPEC:88-91); the intro (SPEC:79) explains the stated flags, so this is only wording.

Per `command.md:260`, the session that ran this review asks the user once whether to open an issue for the follow-up candidates. No user channel exists in this sandbox, so none was asked and none was created.

## Brief clauses overridden
None. The brief narrowed nothing beyond the command's scope, and no clause asked to grade a minor or Medium finding as blocking.

## Reviser brief
Repair only the blocking findings B-1, B-2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
