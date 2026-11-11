review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (first review, whole document)

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec; a first review. Prompt used: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `5c1ab8696d3015841916a6b721ba37673ca41cc95d7518dd2f44d176aa42898f`
- baseline / prior report: none given (first review; `--re-review` and `--baseline` absent, so no `baseline: missing` note applies)
- reviewer model actually used: claude-sonnet-5-5 (simulating the 11-expert panel by native reasoning)
- brief clauses overridden: none
- format: critique-mode buckets plus a compact standard-format YAML summary
- no `--unattended`, `--improve` or `--iterations`; one review, no revised specification written

## Citation conventions
`SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Only these files exist in the sandbox. Any `src/...`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...` or Orca installation path the spec cites cannot be opened here, so a claim that rests only on such a path is UNVERIFIED (it is checked, where possible, through the inventory line that quotes it).

## What was covered
- Read in full: the spec (319 lines), `README`, all three inventories (120 + 323 + 188 lines), the command definition and the review-loop prompt file.
- Citation spot check: every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in sections 1, 2, 3, 4, 8, 9, Decisions and the UNVERIFIED list was compared with the cited inventory line. All matched the claim they support (examples: SPEC:62 vs INV-B:272 and INV-A:97; SPEC:114 vs INV-B:34,87-95; SPEC:131-137 vs INV-A:36,49,50 and INV-B:32,42,44). No wrong-line citation found.
- Arithmetic: 21 + 22 = 43 commands (INV-A:3, INV-B:3); 5 + 5 ready (INV-A:73, INV-B:278), 13 + 14 needs-change (INV-A:73, INV-B:278), 3 + 3 coordinator-only. The spec's 10 / 27 / 6 split (SPEC:76) is conserved; section 3.1 lists 10 rows, 3.2 lists 27, section 4 lists 6. Phase column of 3.2: P1 = 9, P2 = 11, P3 = 4, P4 = 3 (27); the AC-2.2 table (SPEC:229-243) has the 15 P2 rows (11 + reflect, release-split, tdd, troubleshoot). Consistent.
- Not covered: whether any `src/superclaude` line the spec cites says what the spec claims (not in sandbox); the live Orca behaviour (no Orca here). Testing and cloud-native experts (Crispin, Gregory, Hightower) are outside `--focus requirements,architecture` and did not speak.
- Pipeline Dimensional Analysis (FR-17): not triggered. The spec has no multi-stage data flow whose output count differs from its input count; the only count flow is the 43 -> 10 / 27 / 6 partition, checked above. No Quantity Flow Diagram is required.
- State Variable Registry: not required (`--focus correctness` not active).

---

## Guard Condition Boundary Table (completed before synthesis; FR-10)
Guards found: threshold checks and sentinel comparisons in the spec. Input classes omitted for a guard are named in the line under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 wait-split (blocking call > 5 min -> waits <= 4 min) | SPEC:68 | Zero/Empty | no wait | false | none needed | OK |
| G1 | SPEC:68 | Typical | 10 min poll | true | split into waits <= 4 min | OK |
| G1 | SPEC:68 | Maximum/Overflow | 3600 s eval (INV-A:65) | true | split into waits <= 4 min; Monitor-based job (INV-A:44) | OK |
| G1 | SPEC:68 | Legitimate Edge Case | one call of 4.5 min, or 4 min wait + a 2 min script | false (not > 5 min) | none: the heartbeat gap can pass 5 min; only pr-submit has a per-iteration check (SPEC:114, SPEC:316) | GAP (F-M10) |
| G2 outcome mapping (status -> `--outcome`) | SPEC:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| G2 | SPEC:63 | Typical | `succeeded` / `partial` | true | `--outcome succeeded` (SPEC:296) | OK |
| G2 | SPEC:63 | Sentinel Value Match | `status: blocked` | true | `--outcome failed`; Orca Task status `blocked` is a different state (CAPS:89) | OK (see W-3) |
| G2 | SPEC:62, SPEC:295 | Legitimate Edge Case | an existing contract whose `status` uses another word (workflow contract 1.1, INV-B:272) | unspecified | "keep their fields and add the missing ones" with a fixed four-value set: no merge rule | GAP (F-M12) |
| G3 output-dir guard (contract at `<output-dir>/return-contract.yaml`) | SPEC:62 | Zero/Empty | `--unattended` with no output flag | unspecified | not stated | GAP (F-M2) |
| G3 | SPEC:62 | One/Minimal | `--output <file>` (tdd, SPEC:90; init-lite, SPEC:87) | unspecified | "beside the report" only for init-lite; tdd none | GAP (F-M2) |
| G3 | SPEC:62, SPEC:83, SPEC:92 | Legitimate Edge Case | adversarial (`<output>/adversarial/`), workflow (`.dev/tasks/to-do/<id>/`), cleanup-audit (fixed `.claude-audit/`), index-repo (no flag) | false for WC-4 path | rows name a different or no location | GAP (F-01, blocking) |
| G4 retry guard (resume flag, else fresh dir) | SPEC:64 | Typical | retry worker, same brief, same output dir | unspecified | "fresh output directory" vs a coordinator-fixed directory (SPEC:62, SPEC:73) | GAP (F-M1) |
| G5 `--unattended` token | SPEC:261 | Sentinel Value Match | the string `--unattended` inside a quoted prompt | unspecified | D1(a) says "explicit flag"; no tokenising rule | GAP (F-M7) |
| G6 gate resolution a/b/c | SPEC:60 | Typical | cli-portify approval gates (SPEC:105) | true for all three | all three resolve as (c) blocked; no (a) or (b) exists | GAP (F-02, blocking) |
| G7 readiness (60 s default) | SPEC:59 | Maximum/Overflow | fallback "well inside" the limit | unspecified | evidence says 30 s passes and about 45 s fails (CAPS:49); the requirement gives no number | GAP (F-M11, minor wording) |
| G8 nesting depth = 1 | SPEC:33, SPEC:66 | Zero/Empty | malformed setting | true | falls back to 1 (CAPS:100) | OK |
| G8 | SPEC:33 | Legitimate Edge Case | depth raised by the user | false | D5 keeps 1 (SPEC:282-286) | OK |
| G9 confidence < 0.70 (task) | SPEC:121 | Sentinel Value Match | exactly 0.70 | false | proceeds; matches `< 0.70` (INV-B:199) | OK |
| G9 | SPEC:121 | Zero/Empty | confidence 0 | true | blocked | OK |
| G10 `--depth deep` short symptom (troubleshoot) | SPEC:91 | Legitimate Edge Case | exactly 10 words | false | proceeds; matches "< 10 words" (INV-B:239) | OK |

Classes left out: G1 One/Minimal (no behaviour change below 5 min), G1 Sentinel (no sentinel); G2 One/Minimal and Maximum (a status is one enum value); G3 Maximum (a path has no capacity rule in the spec); G4/G5/G6 Zero/Empty where listed as typical only (the guard is a flag, not a quantity); G7 Zero (a zero fallback is not a requirement); G8 One/Typical (depth is a fixed setting); G9 Typical/Maximum (covered by the 0.70 edge rows); G10 Maximum (no upper limit stated). Every GAP row has a finding below.

---

## === REQUIREMENTS ANALYSIS ===
Experts in review order: Wiegers (lead), Adzic, Cockburn.

### F-01 [CRITICAL-equivalent: blocking] WC-4's one contract path contradicts the rows and checks that must satisfy it
- Experts: Wiegers (testability), Fowler (interface consistency), Whittaker (divergence attack, see W-1)
- Grading check: an implementer who follows the stated text as written builds the contract for adversarial at `<output>/adversarial/return-contract.yaml` (SPEC:83), for workflow at `.dev/tasks/to-do/<id>/return-contract.yaml` with an id the coordinator cannot know before dispatch (SPEC:92, INV-B:272), and for cleanup-audit and index-repo at no stated place (SPEC:85-86, "output dir is fixed"; no `--output` flag, INV-A:42,53); WC-4 says every contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory the coordinator passed (SPEC:62) and 2.3 says the report path is known before dispatch (SPEC:73). Those contracts are wrong because AC-1.2 runs each P1 command with `--unattended --output <dir>` (SPEC:208; adversarial, cleanup-audit, index-repo and workflow are named P1 commands, SPEC:159) and 7.2 steps 3 and 4 then require the report path to be "the WC-4 contract path" and `test -s <contract>` (SPEC:194-195). Two stated texts contradict each other, and an acceptance criterion cannot pass for these four commands. cleanup-audit and index-repo do not even accept `--output <dir>`.
- Evidence: SPEC:62, 73, 79, 83, 85, 86, 92, 159, 194, 195, 208, 210; INV-A:35 (adversarial contract written at `<output>/adversarial/` or `.../adversarial/adversarial/`), INV-A:42,53; INV-B:272.
- Recommendation: state one rule for where the contract goes (for example "WC-4 path = `<output-dir>/return-contract.yaml`, and a command whose own contract lives elsewhere writes this file as well or the AC names the command's own path"), and for workflow, cleanup-audit and index-repo state how the coordinator learns or passes the directory, or exempt them by name as M1 does for load. Narrow AC-1.2 and 7.2 step 3 accordingly.
- Severity: blocking (it names a contradiction and an AC that cannot pass). Priority: High. Quality impact: Testability +2, Consistency +2.

### F-02 [MAJOR: blocking] cli-portify can never reach `succeeded` under `--unattended`, but AC-2.3 requires it
- Experts: Cockburn (goal/actor), Wiegers, Adzic (example), Whittaker (sequence attack)
- Grading check: an implementer who follows the stated text builds cli-portify so that each of its three approval gates "resolves as blocked" (SPEC:105: review after phases 1 and 2, approval before phase 3, final approval before delivery; INV-A:45) with only a `--resume <contract>` flag added. X is: every unattended run stops at the first gate with `status: blocked`, and a resumed run stops at the next gate; no stated flag, default or answer-as-flag makes any gate pass, and WC-3 only says "re-invoke or resume the command with the answer as a flag" (SPEC:61) without naming such a flag. X is wrong because AC-2.3 requires a happy-path run of every P2 command, cli-portify included, that ends with `--outcome succeeded` (SPEC:213, SPEC:160), and the other P2 commands do have a way through (a documented default or a caller flag: SPEC:104, SPEC:115, SPEC:117, SPEC:120-121). The acceptance criterion cannot pass.
- Evidence: SPEC:60, 61, 105, 160, 213, 231; INV-A:45, INV-A:79 (inventory asked for "ask or an explicit auto-approve flag"), INV-A:116 (how a resume is invoked is UNVERIFIED).
- Recommendation: give cli-portify resolution (a) or (b) for at least the in-run gates (for example an explicit approval flag the brief carries, naming the artifact approved), or take it out of the AC-2.3 happy-path set and say the worker can only deliver up to the next gate. State whether the answer to a gate is passed as a flag on resume.
- Severity: blocking. Priority: High. Quality impact: Completeness +1, Testability +1.

### Follow-up candidates in this bucket (Medium or minor; they never fail the review)
- F-M2 [Medium, Wiegers] WC-4 leaves the contract location undefined when the command's only output control is a file or there is none. `--unattended` with no output flag has no stated outcome (Whittaker zero/empty attack W-2). tdd takes `--output <file>` and the AC-2.2 tdd row expects `status: blocked` in a contract with no location (SPEC:90, SPEC:229); spec-panel "add `--output`" and research "contract naming the generated path" give no directory (SPEC:116, SPEC:120); recommend writes an "envelope to a file" (SPEC:115). Needs a guess of which directory. Fix: one sentence in WC-4 for the file-valued and absent cases, including a refusal printed in chat when no directory is known.
- F-M3 [Medium, Wiegers] Phase scope of the flag is stated two ways. Section 6 P1 puts "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" in P1 (SPEC:159); AC-1.1 and N1 say the P2-P4 commands of 3.2 get their section in their own phase (SPEC:207); 3.1 gives reflect, release-split, tdd and troubleshoot the section in P1 while their gate resolutions arrive in P2 (SPEC:79, SPEC:88-91). If a gated command accepts the flag in P1 without its resolution, a brief that passes `--unattended` stalls on the prompt (WC-2). Needs the reading "worse of two" to be picked, so Medium. Fix: say a gated command accepts `--unattended` only in the phase that converts its gates.
- F-M5 [Medium, Wiegers] WC-9 turns off any default that "calls a paid external run" (SPEC:67) but never defines it; research's default web search (Tavily, INV-B:134) is kept on by its own row (SPEC:116). Name the class or list the commands.
- F-M6 [Medium, Adzic] task: "EXEMPT `commit`/`push` refused unless authorized (WC-9)" (SPEC:121) but WC-9 authorises only through "the command's own explicit flag" (SPEC:67) and the inventory shows EXEMPT keywords run "immediately with no skill" and no such flag (INV-B:204). The authorising flag is unspecified and D4 is a P4 decision (SPEC:277-280) while the task row is P2.
- F-M11 [minor note, Wiegers] WC-1 says a startup prompt must fall back "well inside" the 60 s limit (SPEC:59); the cited evidence gives 30 s passing and about 45 s failing (CAPS:49). Give a number. WC-1's owner is "Launch setup, not commands" and no phase in section 6 delivers it and no AC but 7.2 step 1 checks it (SPEC:192).
- F-M14 [Medium, Adzic] WC-3 lets the worker `ask` instead of ending blocked (SPEC:61), but AC-2.2 expects exactly `failed` plus `status: blocked` for every (c) row and 7.2 step 3 expects one `worker_done` (SPEC:194, SPEC:212, SPEC:229-237). If the worker asks, the check's expected sequence does not occur. Add a line saying which path the AC exercises (the brief forbids `ask`, or the AC accepts both).

## === ARCHITECTURE ANALYSIS ===
Experts in review order: Fowler (lead), Nygard, Whittaker, Newman, Hohpe.

No blocking architecture finding beyond F-01 (interface consistency of the contract path). The decision itself (SPEC:13-39) is well supported: depth 1 forbids command-side `worker-start` (CAPS:97-103), the worker is a top-level session (CAPS:161), and no command mentions Orca today (SPEC:25 E5; UNVERIFIED here). Section 1.4 states its evidence gaps plainly (SPEC:41-45) and P0 tests the decision first (SPEC:158, SPEC:206).

### Follow-up candidates (Medium or minor)
- F-M1 [Medium, Nygard/Hohpe] Retry versus fresh directory. WC-6 says a command with no resume flag "writes each run into a fresh output directory" (SPEC:64) and 21 rows say "fresh dir" (SPEC:99-125). WC-4 and 2.3 fix the directory in the brief before dispatch (SPEC:62, SPEC:73), and `worker-start --retry-of` re-runs the same Task (CAPS:116). If the command writes into the passed directory a retry overwrites or mixes with the first attempt's output; if it makes its own subdirectory the WC-4 path is wrong. The reading "the coordinator passes a new directory on a retry" would remove the conflict but 2.3 does not say it. Fix: add "a retry brief names a new output directory" to 2.3.
- F-M4 [Medium, Nygard] WC-11 says two workers in one worktree "must never write the same file" (SPEC:69) but cleanup-audit (fixed `.claude-audit/`, SPEC:85) and index-repo (fixed `PROJECT_INDEX.md`, SPEC:86; INV-A:53) do. The first row accepts "one audit per worktree at a time" and the second says nothing, and 2.3's list of what the coordinator owes has no serialisation duty (SPEC:73).
- F-M10 [Medium, Nygard] WC-10 splits only waits above 5 minutes into waits of at most 4 (SPEC:68). A 4.5 minute call, or a 4 minute wait plus a script run, gives a heartbeat gap over 5 minutes; only pr-submit asks for an iteration bound (SPEC:114) and its poll runtime is UNVERIFIED (SPEC:316). State the bound on total time between heartbeats instead.
- F-M12 [Medium, Newman] The contract has no version field and "keep their fields and add the missing ones" (SPEC:62) conflicts with the fixed four-value `status` set (SPEC:295) for a command that already has a `status` with other values (workflow contract 1.1, INV-B:272). Add a `contract_version` and a rule for the mapping.
- F-M13 [Medium, Newman] Mirror drift. The spec records that `plugins/superclaude/commands/` holds copies and that the update rule was not read (SPEC:312), but no AC checks the mirror, and AC-C2 `make verify-sync` covers only `.claude/` (SPEC:185). Add a mirror-parity check, or state the mirror is generated.
- F-M15 [Medium, Nygard] Stall recovery. 7.2 step 2 observes `agentWait` (SPEC:193) and 2.3 says the coordinator opens the report after `worker_done` (SPEC:73), but nothing says what the coordinator does when no `worker_done` arrives and the worker is not parked on a prompt (CAPS:126 allows leaving a wait only on positive proof). The spec cites that rule nowhere in section 2.
- F-M16 [minor note, Hohpe] 7.2 step 7 calls `worker-release` with no identifier (SPEC:198); the capability inventory gives only prose for it (CAPS:109), so the exact arguments are UNVERIFIED.
- F-M7 [Medium, Whittaker, see W-4] `--unattended` token handling.
- F-M8 [Medium] AC-C5 prints any removed line in a command file (SPEC:188), while SA-4 allows "new flags" (SPEC:149). Adding a flag to the Usage line is a changed line and fails the check. Say flags are added on new lines, or exempt the Usage line.
- F-M9 [Medium] AC-2.4 counts reviews and comments with `gh api ... --jq length` (SPEC:214); without `--paginate` the default page size caps the count, so a PR already past one page cannot show new posts. Add `--paginate` to the check.

---

## Adversarial analysis (Whittaker; review position 6, after Fowler and Nygard)
Severity uses the panel scale. A finding is blocking only where the grading check above holds.

- W-1: I can break this specification by **Divergence Attack**. The invariant at **WC-4 / SPEC:62 plus SPEC:83 and SPEC:92** fails when **the same command is asked for its contract path by the general rule and by its own row**. Concrete attack: brief = `/sc:adversarial a.md b.md --output /o --unattended`. Before: `/o` empty. After (row reading): `/o/adversarial/return-contract.yaml`. AC-1.2 step 4 (`test -s /o/return-contract.yaml`) exits 1. Workflow: no `--output`, brief names no directory, contract lands in `.dev/tasks/to-do/<generated id>/`, so the coordinator cannot pass `--report-path` it never learned. Severity: MAJOR, blocking (F-01).
- W-2: I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 / SPEC:62** ("`<output-dir>` is the directory the coordinator passed") fails when **no directory is passed**. Concrete attack: `/sc:analyze src/x.py --unattended`. Before: no files. After: the spec defines neither a default directory nor a refusal; the command may write beside the source, or nothing, and WC-5's "no report exists" then reads as `failed` for a run that did its work. Severity: MAJOR, graded Medium (a requirement the document never states; F-M2).
- W-3: I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 / SPEC:63** (`blocked` -> `--outcome failed`) fails when **a legitimate Orca Task status shares the word**. Orca has a Task status `blocked` for unmet dependencies (CAPS:89) and a failed Task keeps dependents blocked (CAPS:90). Concrete attack: coordinator sees a contract `status: blocked` and a Task `failed`; it retries (`--retry-of`), counts toward the three-failure circuit breaker only if the start fails (CAPS:80, so a worker's own failed report is not counted), but a coordinator that also reads the contract as the Task's `blocked` could wait for dependencies that never clear. The spec does not tell the coordinator that a contract `blocked` means "a person must answer". Severity: MINOR (the behaviour is inferable from SPEC:60 and 63).
- W-4: I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) / SPEC:261** ("explicit `--unattended` flag") fails when **the sentinel string appears inside user text**. Concrete attack: `/sc:troubleshoot "login fails when --unattended is set"` typed by a person. Before: interactive command. After: a naive match switches the command to unattended mode, so an interactive run loses its prompts (SA-1 broken, SPEC:146). The spec offers no rule that the flag counts only as a standalone token outside quoted content. Severity: MAJOR, graded Medium (needs the implementer to pick the naive reading; F-M7). Recommendation: one sentence in the contract file.
- W-5: I can break this specification by **Sequence Attack**. The invariant at **WC-6 / SPEC:64** fails when **a retry starts with the first attempt's files present**. Concrete attack: attempt 1 writes `/o/return-contract.yaml` with `status: failed` and a partial report; worker start for attempt 2 uses the same brief (`/o`); attempt 2 dies before writing; the coordinator reads attempt 1's stale file as attempt 2's result. Severity: MAJOR, graded Medium (F-M1).
- W-6: I can break this specification by **Accumulation Attack**. The invariant at **WC-11 / SPEC:69** fails when **two workers use a fixed output directory**. Concrete attack: two `/sc:cleanup-audit --pass 1` workers in one worktree both write `.claude-audit/progress.json`; the second resumes the first's checkpoint (INV-A:42, "enables resume-from-checkpoint"). Severity: MAJOR, graded Medium (F-M4; SPEC:85 documents the limit but 2.3 does not oblige the coordinator).
- W-7: I can break this specification by **Sequence Attack**. The invariant at **cli-portify row / SPEC:105 with WC-3 / SPEC:61** fails when **gate 1 is answered**. Concrete attack: worker blocked at gate 1 -> coordinator replies -> worker resumes at phase 3 -> reaches gate 3 (final approval) -> blocked again; each cycle ends `failed` and the Task's dispatch count rises toward the circuit breaker (CAPS:116). Severity: MAJOR, blocking (F-02).

## Expert consensus and disagreements
- Consensus: the Orca-on-top decision, the rejection of command-side Orca calls (SPEC:28-39), the coordinator-only list (SPEC:127-139) and the explicit evidence gaps (SPEC:41-45, SPEC:304-318) are sound and well sourced.
- Consensus: the weak points are the places where a general rule (WC-4, WC-6, WC-11, `--unattended` scope) meets a per-command row, and one command (cli-portify) whose row removes its own happy path.
- Disagreement: Newman wants a `contract_version` field now (F-M12); Fowler would hold it until two consumers exist. Left to the author; it is a follow-up candidate either way.

## Standard-format summary
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 7
  testability: 6
  consistency: 6
critical_issues:
  - {category: requirements, severity: blocking, expert: wiegers, issue: "F-01 WC-4 contract path contradicted by adversarial, workflow, cleanup-audit, index-repo rows; AC-1.2 cannot pass", recommendation: "one path rule; narrow AC-1.2 and 7.2 step 3"}
  - {category: requirements, severity: blocking, expert: cockburn, issue: "F-02 cli-portify has no gate resolution other than blocked; AC-2.3 cannot pass", recommendation: "add a flag/answer path or drop it from the happy-path set"}
expert_consensus:
  - "Decision and evidence handling are sound"
  - "General rules and per-command rows disagree at WC-4, WC-6, WC-11"
improvement_roadmap:
  immediate: [F-01, F-02]
  short_term: [F-M1, F-M2, F-M3, F-M7, F-M14]
  long_term: [F-M4, F-M5, F-M6, F-M8, F-M9, F-M10, F-M11, F-M12, F-M13, F-M15, F-M16]
adversarial_analysis:
  blocking: [W-1, W-7]
  medium: [W-2, W-4, W-5, W-6]
  minor: [W-3]
```

## Follow-up candidates (Medium and minor; none triggers a revision or fails the review)
Medium: F-M1, F-M2, F-M3, F-M4, F-M5, F-M6, F-M7, F-M8, F-M9, F-M10, F-M12, F-M13, F-M14, F-M15.
Minor notes: F-M11, F-M16, W-3; AC-C1's pass condition "prints nothing" while scan 2 may print the routing guide's Orca section (SPEC:172, SPEC:179) is stated in the comment, not in the table.
The question whether to open an issue for these was not asked: this audit ran as a worker with no person to answer. The coordinator should ask the user once for this loop; no issue was created.

## Reviser brief
Blocking finding ids: F-01, F-02. Nothing else is to be touched.
- Revise only text a blocking finding names (SPEC:62, 73, 83, 85, 86, 92, 194-195, 208 for F-01; SPEC:61, 105, 213, 231 for F-02).
- Add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table.
- Prefer deleting or narrowing text to adding it.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, including the follow-up candidates above.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
