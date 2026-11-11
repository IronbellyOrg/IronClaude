review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

## Header
| Field | Value |
|---|---|
| Command run | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Baseline / prior | none given: first review of the full document (`--re-review` and `--baseline` both absent) |
| Reviewer model actually used | `claude-sonnet-5-5` |
| Review date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, lines 1-55), values: candidate = the spec above |
| Panel | Focus panel in command order: Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Newman, Hohpe; Whittaker (active in every review, after Fowler and Nygard). Crispin, Gregory, Hightower are outside both focus panels and did not speak. |
| Not run | Improve step (not requested with `--improve`; the brief limits output to this file; the candidate is unmodified). State Variable Registry (only for `--focus correctness`). Pipeline Dimensional Analysis and Quantity Flow Diagram (not triggered, see Coverage). |

## Coverage (what this review covered)
- Read in full: `.dev/orca-command-refactor/README.md` (39 lines, binding context), the candidate (285 lines), `inventory/commands-a.md` (121 lines), `inventory/commands-b.md` (324 lines), `inventory/orca-capabilities.md` (189 lines), `command.md` (the command definition) and the loop prompts file.
- Checked: internal consistency of counts (10 + 27 + 6 = 43; per-phase command lists in section 6 against sections 3.1 and 3.2), every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in sections 1 to 4 against the inventory files in the workspace, requirement-to-acceptance-check traceability (WC-1 to WC-12, SA-1 to SA-6, phases P0 to P4), the shell patterns of AC-C1 and AC-C5 (run in the sandbox, see M-08), and the guard conditions (table below).
- Citation status: every `INV-A`, `INV-B` and `CAPS` line cited by the spec exists and says what the spec says it says (spot-checked about 120 of them, all found as cited). The inventories themselves quote files that are not in the workspace; those second-hand citations are **UNVERIFIED here**: all `cmd/`, `sk/`, `src/`, `CLAUDE.md:N`, `pyproject.toml:38`, `Makefile:68-74`, `install_core.py`, `EVIDENCE.md`, `.dev/codegraph-migration/...` lines, the Orca guide lines `[G]`/`[H:...]` and `/opt/Orca/...` lines, and the spec's own grep and re-read claims (E5, line 11, UNVERIFIED item 14). I did not treat any of them as wrong.
- Not covered: the truth of the inventory verdicts (no source command files exist in the sandbox), and the phase plan's effort or ordering beyond consistency.
- Pipeline Dimensional Analysis: not triggered. The spec describes Task, worker and report flows, but no stage filters or fans out a data collection where a downstream consumer assumes the input count; the one count-changing step (retry attempts per Task) is covered in M-05.
- `--focus correctness` is not active. Auto-suggestion (advisory only): the spec has 3 or more mutable states (Task status, Dispatch, contract `status`, retry count) and numeric thresholds (60 s, 5 min, 4 min, 0.70, depth 1), so a later pass with `--focus correctness` is recommended.

## Quality assessment (standard format)
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7        # strong tables, explicit rejected alternative, explicit evidence gaps
  completeness: 6   # report-path rule, nested invocation and error-path edges missing
  testability: 6    # most requirements have a check; four checks are defective (M-08, M-09, M-10, M-11)
  consistency: 6    # two blocking self-contradictions (R1-B1, R1-B2)
critical_issues:
  - {category: phase-plan, severity: CRITICAL, expert: Fowler, id: R1-B1, issue: "P1 scope and AC-1.1 vs WC-2 and sections 3.2/6/9", recommendation: "see Reviser brief"}
  - {category: requirement, severity: CRITICAL, expert: Wiegers, id: R1-B2, issue: "WC-4 contract location contradicts the per-command rows and AC-2.2", recommendation: "see Reviser brief"}
expert_consensus:
  - "The decision (Orca on top, commands unchanged units of work) is well argued, and the evidence gaps are stated honestly (section 1.4)."
  - "The worker contract is not yet implementable as written: the one rule that makes a worker checkable (WC-4, the report file) is defined three incompatible ways."
  - "The phase plan promises independent usefulness per phase but P1 as written breaks that promise."
improvement_roadmap:
  immediate: [R1-B1, R1-B2]
  short_term: [M-01, M-02, M-04, M-05, M-08, M-09, M-11]
  long_term: [M-03, M-06, M-07, M-10, M-12, M-13, M-14]
adversarial_analysis: "see Whittaker section"
```

## Findings

Grading: each blocking finding carries its grading sentence. Medium and minor findings are under `follow-up candidates` and do not affect the verdict.

### === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

#### R1-B1. CRITICAL, blocking. Phase P1 contradicts WC-2 and the phase and decision structure
- **Expert**: Wiegers, confirmed by Fowler. **Priority**: High. **Quality impact**: consistency -2, testability -1.
- **Grading sentence**: An implementer who follows the stated text as written builds, in Phase 1, an `--unattended` flag and a `## Unattended mode` section on all 37 commands of sections 3.1 and 3.2, including gated ones (task, cleanup, cli-eval, roadmap, implement, post-release, pr-submit); each accepts the flag while still prompting, and X is wrong because WC-2 says that under `--unattended` the command never prompts, and AC-1.1 passes on the mere presence of the section, so nothing in P1 detects the stall.
- **Contradicting texts**:
  - P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec line 159); AC-1.1 asserts the section exists "for every command in sections 3.1-3.2" (line 195).
  - Section 6 assigns gate conversion to P2 (line 160), interface drift to P3 (line 161) and implement, post-release and pr-submit to P4 (line 162), with P4 waiting on D2 to D4 (lines 154, 162, 225).
  - WC-2: "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question ... Each gate resolves one of three ways" (line 60).
  - Section 2.1: each section "lists only its own gate resolutions" (line 52). For implement, post-release and pr-submit those resolutions are defined only by the unresolved D2 to D4 (lines 109, 113, 114).
  - D3(a), the recommendation, says "no pr-submit changes in Phase 4" (line 240) yet pr-submit is one of the 27 commands "needing a change" (line 76) and AC-1.1 requires its section at P1.
- **Wrong outcome (state trace)**: after P1, installed `/sc:task` and `/sc:cleanup` accept `--unattended` and name a contract (AC-1.1 passes); a coordinator reads `~/.claude/WORKER-CONTRACT.md`, dispatches `/sc:task "<x>" --unattended` with confidence 0.65; the command still prompts (the P2 conversion is not built), the worker parks silently with no `worker_done`, which the spec itself says is invisible (line 44; `CAPS:52,129`).
- **Recommendation**: state which behaviour each phase adds per command (flag plus contract only, or gate handling too), and either narrow AC-1.1 and the P1 scope to the P1 command set or make a command refuse `--unattended` (resolve as blocked) until its gate conversion phase.

#### R1-B2. CRITICAL, blocking. The contract file location is defined by incompatible rules
- **Expert**: Wiegers, Adzic (the check cannot be run), Fowler. **Priority**: High. **Quality impact**: testability -2, consistency -1.
- **Grading sentence**: An implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (WC-4, line 62), and X is wrong because the same spec makes `--output` a file for tdd and init-lite and runs AC-2.2 with `--output <file>`, so the path is `<TDD file>/return-contract.yaml`, a file used as a directory, and AC-2.2's required contract cannot be located or created.
- **Conflicting texts**:
  - (a) File-valued flag: tdd "`--output <file>`", report "the TDD at `--output`" (line 90); init-lite "`--output <file>`" (line 87); AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked` with a non-empty `blocked_question`" (line 200). No sentence says where the contract goes for a file-valued flag; a guess of `dirname(--output)` would put two parallel tdd workers' contracts in one shared directory and breaks WC-11 (line 69).
  - (b) Adversarial: WC-4 gives `<output>/return-contract.yaml`, while the P1 fix says `<output>/adversarial/return-contract.yaml` (line 83); AC-1.4 only requires "one fixed path" (line 198). The brief (section 2.3, line 73) must give "the output directory, so the report path is known before dispatch", and the two rules give two different paths for one command.
  - (c) Workflow: contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (line 92); the id is chosen by the command, so WC-4's "known before dispatch" (line 62) is false for it. The P1 fix "write the contract for pre-creation STOPs too" (line 92) names no location, since no package directory exists before creation, and it is an unconditional change that SA-3 (line 148, "only in unattended mode or when the caller passes the new output flag") forbids.
  - (d) The research row names a contract "naming the generated `claudedocs/research_*.md` path" (line 116) but no output flag or contract location for it.
- **Recommendation**: define one rule that covers a directory flag, a file flag and a command-chosen directory (for example, a contract path the brief passes explicitly, or a derived path stated per command), and make adversarial, workflow and the file-valued commands follow it.

#### Requirements findings graded Medium or minor
Listed under `follow-up candidates` (M-01, M-02, M-03, M-04, M-07, M-11, M-12; N-1 to N-4).

### === ARCHITECTURE ANALYSIS === (Fowler lead, Nygard, Newman, Hohpe)
- **Fowler (boundaries)**: the layering is sound: coordinator owns planning and Orca calls (section 1.1), the worker session owns lifecycle messages (WC-7, WC-12), commands own only gates and report files. The rejected-alternative table (section 1.3) is the strongest part of the spec; R2 to R5 are each backed by `CAPS` lines I confirmed. The only structural defect found is the phase boundary in R1-B1.
- **Nygard (failure modes)**: failure paths are mostly covered (stall, blocked, fenced, timeout). Gaps are edge handling, graded Medium: invalid or truncated contract (M-02), retry after a first attempt left a stale contract (M-05), missing output directory (M-01), a worker fenced between writing the contract and sending `worker_done` is acceptable as written (WC-12).
- **Newman (interfaces and evolution)**: the contract interface (fixed four-value status, `command`, `report_path`, `artifacts`, `blocked_question`) is versionable but has no version field and no rule for commands that already write a `return-contract.yaml` with their own `status` values (see M-12). Nested invocations have no propagation rule (M-04).
- **Hohpe (message exchange)**: `ask` resume by message ID, `worker_done` once, and pull-only follow-ups are correctly taken from Orca (`CAPS:58-67`). WC-3 says "once" without saying once per gate or per command; cli-portify has three gates (line 105). Minor, N-3.

### === ADVERSARIAL ANALYSIS === (Whittaker)
Each finding follows the template. Severity here is the panel label; the loop grade is stated in brackets.

1. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / section 2.3 (lines 62, 73)** ("written on every outcome, including stops before any other output exists") fails when **`--unattended` is passed with no output directory**. Concrete attack: before: `/sc:build --unattended`, no `--output`; the command must write `<output-dir>/return-contract.yaml` but has no directory; after: no contract, `worker_done` carries no report path, WC-5 maps "no report exists" to `failed`. Only post-release says "require an explicit `--output`, else blocked" (line 113); the other 36 rows do not. MAJOR [Medium, M-01: the outcome needs the guess that the command improvises a path].
2. I can break this specification by **Divergence Attack**. The invariant at **WC-5 (line 63)** ("`succeeded` otherwise") fails when **the contract exists but is truncated, unparseable or has no valid `status`**. Concrete attack: a command is killed while writing; `return-contract.yaml` holds `status: succ`; WC-5 sees a report that does not say `failed` or `blocked`, so `--outcome succeeded`; Orca settles the Task `completed` automatically (`CAPS:77`) and dependents become ready. MAJOR [Medium, M-02: an unspecified edge of an otherwise stated rule].
3. I can break this specification by **Divergence Attack** (boundary between branches). The invariant at **WC-5 / Decisions (lines 63, 263)** (`partial` maps to `succeeded`) fails when **a dependent Task needs the missing part**. Concrete attack: `partial` contract with 2 of 3 artifacts; Task `completed`; the dependent `/sc:adversarial` worker starts on 2 inputs. The spec records the rationale and says the body still says `partial`, but nothing makes the coordinator stop. MAJOR [Medium, M-03: a disclosed design trade-off].
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **section 2.1 and D1(a) (lines 51, 228)** ("explicit `--unattended` flag") fails when **free text contains the token**. Concrete attack: `/sc:troubleshoot "login hangs when --unattended is set"` in a person's plain session; with no stated parse rule (the command definition for this feature does state one, "standalone argument token outside any quoted argument"), a naive match switches a person's run to unattended mode and breaks SA-1 (line 146). The reverse also holds: a coordinator brief whose quoted prompt contains the token. MAJOR [Medium, M-07].
5. I can break this specification by **Sequence Attack**. The invariant at **WC-6 versus WC-4 and section 2.3 (lines 64, 62, 73)** fails when **a retry worker reuses the brief**. Concrete attack: attempt 1 writes `out/return-contract.yaml` with `status: blocked`, then attempt 2 (`--retry-of`, same Task spec, same `out/`) dies before writing; the coordinator opens the stale file and reads `blocked` for attempt 2. WC-6 says a command "writes each run into a fresh output directory", but section 2.3 says the coordinator passes the directory before dispatch, so who creates the fresh directory is not stated. MAJOR [Medium, M-05].
6. I can break this specification by **Sequence Attack**. The invariant at **WC-3 versus implement's Ruling rule (lines 61, 109, 232-238)** fails when **the worker uses `ask` on an implement halt**. Concrete attack: `E-HALT-QA`; WC-3 lets the session ask the coordinator and re-invoke with the answer as a flag; the command's unchanged rule says "another agent's message" is not a Ruling (`INV-A:51,66`), so the re-invocation halts again with `E-NO-RULING`. The spec resolves it only at section 3.2 and D2(a), not in WC-3. MAJOR [Medium, M-06].
7. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (line 68)** fails when **a blocking step lasts between 4 and 5 minutes**. Concrete attack: the trigger is "longer than 5 minutes", the required split is "at most 4 minutes", the Decisions rationale is a margin under 5 (line 266) and AC-4.3 checks "no single tool call exceeds 240 s" (line 210). A 4.5-minute wait needs no split by WC-10 and fails AC-4.3. MINOR [N-2].
8. I can break this specification by **Accumulation Attack** (boundary at capacity) on **WC-11 and section 3.1 cleanup-audit (lines 69, 85)**: the output directory `.claude-audit/` is fixed, so two cleanup-audit workers in one worktree overwrite each other; the spec handles it by "one audit per worktree at a time", an instruction to the coordinator with no check. MINOR [N-4].

### Guard Condition Boundary Table (Nygard builds, Whittaker attacks; Crispin's completeness validation was done by this reviewer because Crispin is outside the focus panels)
Triggered: the spec contains thresholds and boolean guards. Input classes that cannot occur for a guard are left out with a one-line reason below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `unattended_mode` (flag token present) | WC-2, D1 (lines 60, 228) | Zero/Empty | flag present, `--output` absent | true | Unspecified (see M-01) | GAP |
| `unattended_mode` | WC-2, D1 | One/Minimal | flag present, command has no gate | true | "a no-op where a command has no gate" (line 159) | OK |
| `unattended_mode` | WC-2, D1 | Typical | flag present, `--output <dir>`, gated command | true | gate resolves per section 3 row | OK |
| `unattended_mode` | WC-2, D1 | Sentinel Value Match | free-text prompt containing `--unattended` | true or false (unspecified) | Unspecified (see M-07) | GAP |
| `unattended_mode` | WC-2, D1 | Legitimate Edge Case | a person types the flag in a plain session | true | D1(a): "a person never types it" (line 228); no rule if one does, but behaviour is the safe unattended one | OK |
| `outcome_mapping` (report status to `--outcome`) | WC-5 (line 63) | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| `outcome_mapping` | WC-5 | One/Minimal | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| `outcome_mapping` | WC-5 | Typical | `status: failed` or `blocked` | failed | `--outcome failed`, first sentence states status | OK |
| `outcome_mapping` | WC-5 | Sentinel Value Match | `status: partial` | succeeded | `--outcome succeeded`; dependents unblocked (see M-03) | OK |
| `outcome_mapping` | WC-5 | Legitimate Edge Case | file present but unparseable, empty, or `status` outside the four values | succeeded ("otherwise") | Unspecified (see M-02) | GAP |
| `heartbeat_wait_split` (blocking call length vs 5 min) | WC-10 (line 68) | Zero/Empty | wait of 0 s | false | no split needed | OK |
| `heartbeat_wait_split` | WC-10 | Typical | 2-minute wait | false | no split needed | OK |
| `heartbeat_wait_split` | WC-10 | Maximum/Overflow | 3600 s eval wait | true | split into waits of at most 4 minutes | OK |
| `heartbeat_wait_split` | WC-10 | Legitimate Edge Case | wait of 4.5 minutes | false (not over 5) | not covered by the 4-minute margin, fails AC-4.3's 240 s (see N-2) | GAP |
| `nested_depth` (depth 1) | R1, WC-8 (lines 33, 66) | Typical | worker calls `worker-start` | true (refused) | WC-8 forbids; Orca refuses | OK |
| `nested_depth` | R1, D5 | Legitimate Edge Case | user raises depth to 2 | false | WC-8 still forbids a command from calling Orca | OK |
| `consumer_fenced` | WC-12 (line 70) | Typical | `check` returns `consumer_fenced` | true | stop, send no `worker_done` | OK |
| `consumer_fenced` | WC-12 | Legitimate Edge Case | fenced after the contract is written | true | worker stops; the file is left; coordinator decides | OK |
| `confidence_below_0_70` | task row (line 121) | Zero/Empty | confidence missing or not computable | unspecified | Unspecified | GAP |
| `confidence_below_0_70` | task row | Typical | 0.65 | true | resolves as blocked | OK |
| `confidence_below_0_70` | task row | Legitimate Edge Case | exactly 0.70 | false | "below 0.70" means 0.70 proceeds | OK |
| `retry_output_dir` (fresh vs resume) | WC-6 (line 64) | Legitimate Edge Case | retry reuses the brief's output directory | unspecified | Unspecified (see M-05) | GAP |
| `ready_readiness_limit` (60 s) | WC-1 (line 59) | Typical | launch path with a 30 s fallback | false | passes (`EVIDENCE.md:45`, via `CAPS:49`) | OK |
| `ready_readiness_limit` | WC-1 | Maximum/Overflow | fallback above about 45 s | true | "fails again" (`CAPS:49`); no phase or check owns it (see M-11) | OK |

Left out: `unattended_mode` Maximum/Overflow (a boolean cannot overflow); `outcome_mapping` Maximum/Overflow (four fixed values); `nested_depth` Zero/Empty (depth 0 is the coordinator, which is allowed to start workers); `consumer_fenced` Zero/Empty and Maximum (an event, not a quantity); `confidence_below_0_70` Maximum (a probability cannot exceed 1); `retry_output_dir` other classes (a mode, not a quantity); `ready_readiness_limit` Zero/Empty (a zero limit is impossible: `CAPS:44` uses the default for a non-positive value).

GAP rows (FR-8): five rows. Their grades: all five name a missing requirement or undefined state without a stated text that does harm, so under the loop grading they are Medium (M-01, M-02, M-05, M-07) or minor (N-2, and the confidence row folded into N-4); the blank-behaviour cells (FR-9) are the same rows. None is blocking.

## Follow-up candidates (Medium and minor, not blocking, never in the Reviser brief)

Medium (warnings):
- **M-01** `--unattended` without an output directory: no rule; nowhere to write the contract (WC-4 line 62; 2.3 line 73; only post-release has a rule, line 113). Needs the guess that the implementer improvises.
- **M-02** WC-5 "otherwise succeeded" covers a present but invalid or truncated contract (line 63); add a "no valid status means failed" clause.
- **M-03** `partial` maps to `succeeded`, which settles the Task and unblocks dependents on incomplete output (lines 63, 263; `CAPS:77`). A disclosed trade-off; consider a coordinator-side rule to check `partial` before releasing dependents.
- **M-04** No general rule for nested invocations. The command definition this review runs under has a per-command "Nested invocations" line; the spec has only the tasklist and tdd cases (lines 90, 122). Uncovered: cli-eval create W2 runs `/sc:spec-panel` (`INV-A:44`), cli-portify embeds brainstorm and spec-panel (`INV-A:45`), pr-submit's auggie-review fallback posts to the PR by default (`INV-B:91`, against WC-9, line 67), and parallel nested reflect outputs may share a directory (`INV-B:46`).
- **M-05** Retry and fresh output directory: WC-6 (line 64) versus section 2.3 (line 73) and the Task spec being reused by `--retry-of` (`CAPS:116`). State who makes the fresh directory and how a stale contract from attempt 1 is detected.
- **M-06** WC-3 (line 61) permits `ask` for any blocked gate, but implement's Ruling rule rejects a coordinator's answer (`INV-A:66`; D2, lines 232-236). Add the exception to WC-3.
- **M-07** No parse rule for the `--unattended` token inside quoted or free-text arguments (lines 51, 228); free-text commands: tdd, troubleshoot, research, recommend.
- **M-08** AC-C5 (line 176) uses `grep -E '^-[^-]'`. I ran it on sample diff lines in the sandbox: a removed markdown bullet shows as `-- item` and is not matched (only `-| row` and `-plain` were). Command files are bullet-heavy, so a deleted gate bullet passes the "edits are additive" check.
- **M-09** AC-0.4 (line 194) requires steps 1-3 and says the no-Agent-tool-wrapper property is "verified in the step-5 transcript", but step 5 (line 184) only searches for `AskUserQuestion`, and step 3's pass condition (line 182) needs "the WC-4 contract path", which the spec says arrives only in P1. This is the check that can reopen section 1, so it should be runnable.
- **M-10** AC-C1 (line 172) greps `src/superclaude/core` and must print nothing, while P0 adds `WORKER-CONTRACT.md` there and an Orca section to `HOW-WE-WORK.md` (lines 52, 158), and SA-2 allows an Orca mention "inside the contract file" (line 147). Text such as `orca orchestration ask` in either file fails AC-C1; the spec does not say which wins. Also SA-2 says "in a changed command ... inside the contract file", which mixes two files.
- **M-11** Traceability: WC-1 (line 59) has no owning phase and no check beyond step 1 of 7.2; WC-3, WC-6 and WC-12 (lines 61, 64, 70) have no acceptance check in 7.1 to 7.3. Step 2 of 7.2 (line 181) passes vacuously when `agentWait` is absent (`CAPS:125,129`: absent or null is not evidence).
- **M-12** SA-1 and SA-3 (lines 146, 148) say standalone behaviour, default flag values, output paths and files do not change, while rows change them unconditionally: validate-tests default target (line 125), adversarial contract path (line 83), validate-roadmap report name (line 124), workflow pre-creation contract (line 92). SA-4 (line 149) is the exception, but no sentence says SA-4 outranks SA-1 and SA-3. Also WC-4 requires `status` from a fixed four-value set while saying commands that already write a contract "keep their fields" (line 62); the existing `status` vocabularies are not in the inventories (UNVERIFIED), so the two may conflict.
- **M-13** The tasklist row (line 122) asserts the nested reflect fan-out is "inside Claude Code's nesting limit" while `INV-B:210` and `INV-B:322` mark nested spawning UNVERIFIED and no depth count is given. The same row makes reflect auto-accept remediation via the headless rule, the reverse of the inventory's own recommendation to drop `--remediate` (`INV-B:215`); the consequence is not stated.
- **M-14** pr-submit's iteration bound (line 114, WC-10 line 68): the sleep is "at least `--poll-interval`", and the default of that flag is not read anywhere in the inputs; UNVERIFIED item 12 (line 283) lists only the poll script runtime.

Minor (notes):
- **N-1** Section 1.4 lists three evidence gaps (lines 41-45) but R1's decisive refusal rests on "presumed" call sites (line 33; `CAPS:103`). It is flagged inline, not in the gap list.
- **N-2** WC-10 thresholds: over 5 minutes triggers, 4 minutes is the split size, 240 s is the check (lines 68, 210, 266).
- **N-3** WC-3 says "ask ... once" (line 61) without saying once per gate or per command; cli-portify has three gates (line 105).
- **N-4** Fixed output directories (`.claude-audit/`, `claudedocs/`) rely on coordinator discipline (line 85); the confidence-guard zero case is unspecified (task row, line 121).
- **N-5** `/sc:load` is counted among the 27 commands needing a change but is not to be dispatched as a Task (lines 112, 265); a count note would avoid confusion.
- **N-6** Plugin mirror of command edits is unresolved (UNVERIFIED item 8, line 279) and no phase check covers `plugins/superclaude/commands/`.

Unverified citations that the verdict does not depend on are listed in Coverage.

## Issue question
The loop asks the reviewing session to ask the user once whether to open an issue for the follow-up candidates. No interactive user exists in this sandbox run, so the question was not asked and no issue was created. The list above is the record.

## Brief clauses overridden
None. The brief asked for the FIRST-REVIEW prompt, report-only output, path:line citations and UNVERIFIED marking; all were applied as written.

## Reviser brief
Repair only the blocking findings R1-B1, R1-B2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
