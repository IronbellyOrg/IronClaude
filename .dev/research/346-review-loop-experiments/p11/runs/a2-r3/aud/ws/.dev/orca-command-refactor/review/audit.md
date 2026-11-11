review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit of the final spec; FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: not applicable (first review; neither `--re-review` nor `--baseline` given).
- Reviewer model actually used: `claude-sonnet-5-5`.
- Mode: critique. Format: standard (YAML summary below) plus critique buckets. `--iterations` ignored (one review per run).
- Brief clauses overridden: none.
- Citation keys: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = line N of the `/sc:spec-panel` command definition `command.md` in the sandbox.
- Citation checkability: only the README, the three inventories, the candidate, `command.md` and the prompts file exist in the sandbox. Every candidate citation that points at `src/`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `plugins/`, `EVIDENCE.md`, `.dev/codegraph-migration/` or at Orca files is UNVERIFIED here unless an inventory quotes it; I checked those only through the inventory line that quotes them.

## Coverage (what I covered)

- Read all 285 lines of the candidate, the README, and all three inventories in full.
- Checked every `INV-A`, `INV-B` and `CAPS` line citation in SPEC sections 1.2, 1.3, 1.4, 2.2, 3.1, 3.2, 4, 8, 9 and the Decisions table against the inventory text. Each cited line holds the text the claim relies on; I found no wrong line. The totals reconcile: 10 ready, 27 needs-change, 6 coordinator-only = 43 (SPEC:76; INV-A:73 gives 5/13/3, INV-B:278 gives 5/14/3). The phase lists at SPEC:159-162 cover the 3.1 and 3.2 rows exactly (P1 9+4, P2 11+4, P3 4, P4 3).
- Not covered (UNVERIFIED): the 340-citation check the candidate reports at SPEC:285, all source-file lines outside the inventories (list above), and whether the spec's grep and pytest commands run.
- Not run: no command can be run in this sandbox, so no acceptance check was executed.

## Quality assessment (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 7 | Requirements are numbered and owner-tagged (SPEC:57-70); per-command rows are dense but consistent. |
| Completeness | 6 | No acceptance check for WC-1, WC-3, WC-6, WC-12 (MED-6); no rule for a silent stall (MED-7). |
| Testability | 5 | AC-1.1 cannot pass as written (REQ-1); the WC-4 path that steps 3-4 of 7.2 read is not defined for several commands (ARCH-1). |
| Consistency | 5 | Three blocking contradictions (REQ-1, REQ-2, ARCH-1) and several Medium ones (MED-1 to MED-5). |

## === REQUIREMENTS ANALYSIS ===

Experts in order: Wiegers (lead), Adzic, Cockburn, then Crispin and Gregory where noted.

### REQ-1 [BLOCKING] AC-1.1 requires an `## Unattended mode` section on `/sc:load`, which the spec says gets none
- Severity: MAJOR (blocking by the grading check). Expert: Wiegers, with Crispin (completeness). Priority: High. Quality impact: Testability +1, Consistency +1.
- Issue: AC-1.1 asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (SPEC:195). `/sc:load` is a section 3.2 row (SPEC:112; INV-B:31). That row says its report is "none (see note)" and that it is used "as a step inside another worker's brief, not as its own Task". P1 scopes it to "load (usage line only)" (SPEC:159). The Decisions table says "a report file would be an unrequested addition. Only its usage-line defect is fixed" (SPEC:265).
- Grading sentence: An implementer who follows AC-1.1 as written either adds a section naming `return-contract.yaml` to `/sc:load`, a command SPEC:112, SPEC:159 and SPEC:265 say gets no report, or leaves load alone and fails P1, and then no later phase may start (SPEC:154); both outcomes are wrong because the criterion contradicts the load row it tests.
- Recommendation: narrow the AC-1.1 assertion to the commands that get a section (exclude `/sc:load`). Rationale: the criterion should test the rows, not override them. Smallest edit: add "except load" to SPEC:195.

### REQ-2 [BLOCKING] P1 ships `--unattended` on commands whose gates are not converted until P2 or P4
- Severity: MAJOR (blocking). Expert: Wiegers, with Nygard (safety boundary). Priority: High. Quality impact: Consistency +1, safety.
- Issue: P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (SPEC:159). Gate conversion is P2 (SPEC:160) and P4 (SPEC:162). WC-2 defines `--unattended` as "never calls AskUserQuestion, never ends its turn on a chat question" (SPEC:60) and WC-9 turns every outward default off under it (SPEC:67). Section 2.3 tells the coordinator to put `--unattended` in every worker's command line (SPEC:73). Each phase is "independently useful" (SPEC:154). AC-1.2 tests only P1 commands (SPEC:196).
- Grading sentence: An implementer who follows P1 as written ships `/sc:auggie-review` (and cli-eval, task, post-release, pr-submit) accepting `--unattended` with its gate untouched; a coordinator that follows 2.3 passes the flag, and auggie-review posts to the PR with no prompt and then waits on its remediation offer (INV-A:38, INV-A:62); this is wrong because the flag is defined to forbid exactly that (SPEC:60, SPEC:67), and no P1 check detects it.
- Recommendation: in P1 add the flag only to commands whose row phase is P1 (plus the ready commands that need no gate change), and say a gated command does not accept `--unattended` until its own phase. Rationale: a flag that is accepted but not honoured is worse than an unknown-flag refusal. Smallest edit: narrow SPEC:159 and add the same limit to AC-1.2.

### Medium and minor requirement findings (follow-up candidates, never blocking)
- MED-1 (Medium; Wiegers). P0 contradicts section 2.3. Section 2.3 says the brief carries "the exact command line including `--unattended`" (SPEC:73), but P0 runs only the ten ready commands "before any command changes" (SPEC:158) and AC-0.4 gives command lines without the flag (SPEC:194), because the flag arrives in P1. Medium because the reader must guess that AC-0.4 wins. Fix: say in 2.3 that P0 briefs omit `--unattended`.
- MED-2 (Medium; Cockburn). Decision dependency is mis-scoped. "Phases 1-3 need no user decision" (SPEC:154) and "Phases 0-3 can proceed on the recommendations" (SPEC:225), yet D4 governs auggie-review `--post-pr` and task `commit`/`push` (SPEC:244), both P2 rows (SPEC:100, SPEC:121), and under D4(b) ("Never") those P2 rows are wrong. D3(a) leaves pr-submit as a non-worker (SPEC:240), yet P1 adds it the flag and section (SPEC:159, SPEC:195). Fix: state that P2 rows assume D4(a) and P1 omits pr-submit unless D3(b).
- MED-3 (Medium; Wiegers). Section 4 says of `/sc:git` "workers make no commits or pushes" (SPEC:133), while WC-9 and D4(a) let an authorized brief turn on commit, push and PR (SPEC:67, SPEC:244; task EXEMPT `commit`/`push` at SPEC:121, post-release at SPEC:113). Fix: "workers make no commits or pushes unless D4(a) authorizes them".
- MED-4 (Medium; Wiegers/Nygard). WC-3 lets a blocked worker ask the coordinator and re-invoke the command "with the answer as a flag" (SPEC:61), while WC-9 allows an outward flag only when "written in the brief" (SPEC:67) and D4(a) only when the user's instruction is quoted in the brief (SPEC:244); D2(a) keeps the implement Ruling rule (SPEC:233-236). An answer-as-flag route to `--post-pr`, `push` or a Ruling is not excluded by WC-3. Medium because the stated WC-9 and D4 text still reads as the stricter rule. Fix: add "except flags WC-9 and D2 reserve" to WC-3.
- MED-5 (Medium; Wiegers). `--unattended` with no output location is undefined (Zero/Empty attack on WC-4, SPEC:62). Section 3.2 says "add `--output`" for 14 commands but never says what a command does when `--unattended` arrives without it. (`CMD:460` shows one way to define it: refuse before any work and print the refusal in chat only.) Fix: one sentence in WC-4 or WC-2.
- MED-6 (Medium; Crispin/Gregory, traceability). Requirements with no acceptance check in section 7: WC-1 (owner "launch setup", no phase delivers it), WC-3 (no run exercises `ask`), WC-6 (no retry or resume check for any command), WC-12 (`check`/`consumer_fenced`), and WC-10 for cli-eval (only pr-submit is checked, AC-4.3 at SPEC:210, although cli-eval gets the split in P2 at SPEC:104). Fix: add one check each, or mark them "design rule, not checked".
- MED-7 (Medium; Nygard). No coordinator rule for a silent stall. WC-2 says a stall is invisible except through `agentWait` or a missing report (SPEC:44, SPEC:60); step 3 of 7.2 waits "until `worker_done` arrives" (SPEC:182) with no exit; `agentWait` may not fire for a command that ends its turn on a chat question (INV-A:62). The positive-proof rules already exist (CAPS:126). Fix: add a stop rule to 7.2 citing CAPS:126.
- MED-8 (Medium; Fowler). `status` vocabulary collision. WC-4 says commands with a contract "keep their fields and add the missing ones" (SPEC:62), the Decisions table fixes `status` to four values instead of copying each command's own (SPEC:262), and step 4 of 7.2 asserts `status` is in that set (SPEC:183). The inventories do not list the status values of the existing workflow, adversarial, reflect or brainstorm contracts (INV-B:272, INV-A:35, INV-B:112, INV-A:39), so the check may fail on a correct existing contract. Fix: record each existing vocabulary in section 3.1 and map it.
- MED-9 (Medium; Nygard/Whittaker). Parallel-safety gaps against WC-11 ("must never write the same file", SPEC:69). `index-repo` writes a fixed `PROJECT_INDEX.md` (SPEC:86; INV-A:53); `cleanup-audit` uses a fixed `.claude-audit/` and the spec handles it by a rule outside the contract ("one audit per worktree at a time", SPEC:85); `save` keys are named `<key>-<session-or-timestamp>` with no stated timestamp precision, so two workers starting in the same unit collide (SPEC:119, SPEC:207). Fix: state the precision and add the one-at-a-time rule to 2.3.
- MED-10 (Medium; Wiegers). `tasklist` Stage 10.5 can still HALT on `needs_human_decision` items (INV-B:209), which WC-2 requires to resolve as default, flag or blocked; the tasklist row names only the headless auto-accept (SPEC:122). Fix: add the HALT resolution to the row.
- MED-11 (Medium; Adzic, evidence strength). Section 1.4 item 2 states as fact that a command's own `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`" (SPEC:44). CAPS:47 records that for Claude the command line carries the task (argv injection), so the command is the first turn and the claim is an inference; it is absent from the UNVERIFIED list (SPEC:272-285; item 9 at SPEC:280 covers only `--print`). The decision does not depend on it, because WC-2 forbids the prompt anyway. Fix: add it to the UNVERIFIED list.

## === ARCHITECTURE ANALYSIS ===

Experts in order: Fowler (lead), Nygard, Whittaker, Newman, Hohpe, Hightower.

### ARCH-1 [BLOCKING] WC-4's one contract-path formula conflicts with the per-command rows and cannot be read at the path steps 3-4 of 7.2 use
- Severity: MAJOR (blocking). Expert: Fowler, with Hohpe (message/contract shape). Priority: High. Quality impact: Consistency +1, Testability +1.
- Issue: WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch" (SPEC:62). Four rows differ:
  - adversarial: the contract is fixed at `<output>/adversarial/return-contract.yaml` (SPEC:83, AC-1.4 at SPEC:198; INV-A:35 records real runs at both `.../adversarial/` and `.../adversarial/adversarial/`).
  - tdd and init-lite: the brief passes `--output <file>` (SPEC:87, SPEC:90), and AC-2.2 runs `/sc:tdd ... --output <file>` and expects a contract with `blocked_question` (SPEC:200). A file path is not a directory.
  - workflow: the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), and the package id does not exist before dispatch; P1 adds the contract "for pre-creation STOPs too" (SPEC:92), when no package directory exists (INV-B:272).
  - cleanup-audit and index-repo take no output flag in the inventories (INV-A:42, INV-A:53).
  Corroboration that `--output` is file-valued in this family: `CMD:460` ("`--report-dir <dir>` only (`--output` is file-valued)").
- Grading sentence: An implementer who follows WC-4 as written writes the adversarial contract at `<output>/return-contract.yaml`, and tdd and init-lite at a path under a file (`<file>/return-contract.yaml`), and workflow at a path nobody can know before dispatch, and each is wrong because SPEC:83, SPEC:198 and SPEC:200 require different paths and steps 3-4 of 7.2 read the WC-4 path (SPEC:182-183), which then does not exist.
- Recommendation: define one directory-valued input for the contract and let section 3 name the exact contract path per command in one column. Rationale: the per-command path is the real interface, and a formula that six rows break is not a requirement. Smallest edit: replace the `<output-dir>` clause of WC-4 with a pointer to that column and add the column.

### Medium and minor architecture findings (follow-up candidates, never blocking)
- MED-12 (Medium; Fowler). Count divergence in the illustrative flow of section 1.3: "several `/sc:troubleshoot` workers, then one `/sc:adversarial` worker on their reports" (SPEC:39). Workers that end `failed` or `blocked` leave no report (WC-5, SPEC:63), and adversarial takes 2-10 inputs (INV-A:35). If only one troubleshoot worker succeeds, or more than ten, the second stage has no stated behaviour. FR-19 would label this CRITICAL; the consequence test does not, because the text is an example, not a stated requirement. Fix: one sentence in 2.3.
- MED-13 (Medium; Newman). AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and expects no output (SPEC:172), but P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`, both in `core/` (SPEC:158), and SA-2 allows an Orca mention "inside the contract file" (SPEC:147). Whether the check fails depends on the exact wording written. Fix: exclude those two files from AC-C1 or state they avoid the pattern.
- MED-14 (Medium; Nygard, boundary). WC-10 splits a blocking step only when it exceeds 5 minutes (SPEC:68), while the Decisions table sets 4 minutes (SPEC:266) and AC-4.3 fails any single call above 240 s (SPEC:210). A 270 s call passes WC-10 and fails AC-4.3. Fix: trigger WC-10 at 4 minutes.
- MED-15 (Medium; Hightower, operations). WC-1 asks for a fallback "well inside" the readiness limit (SPEC:59) with no number; the evidence is 30 s passing and about 45 s failing (CAPS:49). Fix: state 30 s.
- MIN-1 (minor). Step 4 of 7.2 validates only `status` and `command` (SPEC:183); `report_path`, `artifacts` and `blocked_question` types are checked only in AC-2.2.
- MIN-2 (minor). AC-0.4 says step 4 "uses the command's existing report file" (SPEC:194), but step 4 is a YAML parse that would fail on a Markdown `REPORT.md`.
- MIN-3 (minor). After a blocked worker ends `failed`, the coordinator's next move (retry with `--retry-of`, re-brief with the answer, new output dir for WC-6) is not stated in 2.3 (SPEC:73; CAPS:116).

## Whittaker adversarial analysis (attack template, FR-3)

1. I can break this specification by **Sequence Attack**. The invariant at **P1 scope and WC-2 (SPEC:159, SPEC:60)** fails when **P1 is complete and P2 has not started**. Concrete attack: before = auggie-review has no `--unattended`; step = P1 adds the flag, gate unchanged; step = coordinator follows 2.3 and passes the flag; after = a PR comment is posted and the session waits on the remediation offer. Severity CRITICAL as a consequence, recorded as REQ-2.
2. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 `<output-dir>` (SPEC:62)** fails when **`--output` carries a file path (tdd, init-lite) or an existing nested contract path (adversarial)**. Concrete attack: before = brief `--output out/tdd.md`; step = command appends `return-contract.yaml`; after = path `out/tdd.md/return-contract.yaml`, which cannot exist. Recorded as ARCH-1.
3. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (SPEC:68) versus AC-4.3 (SPEC:210)** fails when **a single call lasts 4 to 5 minutes**. Concrete attack: before = one 270 s wait; WC-10 does not apply; AC-4.3 fails the run. MAJOR in label, Medium by consequence (MED-14).
4. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 "known before dispatch" (SPEC:62)** fails when **`--unattended` is passed with no output location**. Concrete attack: before = brief omits the output flag; after = the command's behaviour is unspecified. Recorded as MED-5.
5. I can break this specification by **Accumulation Attack**. The invariant at **section 1.3 fan-out example (SPEC:39)** fails when **successes fall below 2 or exceed 10**. Concrete attack: before = 3 troubleshoot workers, 2 end `blocked`; after = 1 report reaches adversarial, which needs 2-10. Recorded as MED-12.
6. Accumulation and Zero/Empty attacks on the Task chain: a failed Task keeps its dependents blocked (CAPS:90) and `blocked` maps to `failed` (SPEC:63), so every `blocked` gate blocks every dependent Task until a retry; the spec does not say who retries (MIN-3).

## Guard Condition Boundary Table (FR-8 to FR-10; Nygard builds, Crispin validates, Whittaker attacks)

Guards found: the `--unattended` switch (SPEC:60), the contract output location (SPEC:62), the outcome mapping (SPEC:63), the wait threshold (SPEC:68), the outward-action default (SPEC:67), the readiness fallback (SPEC:59), and the 2-10 input range of the `/sc:adversarial` stage (SPEC:39). Classes left out and why: Maximum/Overflow for the boolean `--unattended` and for the outward-action default (a boolean has no overflow); Zero/Empty for the wait threshold (a zero-length wait is not a blocking step); Sentinel for the readiness fallback (no sentinel value exists).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `unattended_switch` | WC-2, SPEC:60 | Zero/Empty | flag absent | false | Unchanged standalone behaviour (SA-1, SPEC:146) | OK |
| `unattended_switch` | WC-2, SPEC:60; P1, SPEC:159 | Typical | flag present on a P1 no-gate command | true | Contract written, no prompt | OK |
| `unattended_switch` | P1, SPEC:159-160 | Legitimate Edge Case | flag present on a gated command before its own phase | true | Flag accepted, gate unchanged | GAP (REQ-2, blocking) |
| `output_location` | WC-4, SPEC:62 | Zero/Empty | `--unattended`, no output flag | `""` | Unspecified | GAP (MED-5, Medium) |
| `output_location` | WC-4, SPEC:62 | Typical | `--output .dev/x/` | dir | `.dev/x/return-contract.yaml` | OK |
| `output_location` | SPEC:87, SPEC:90, SPEC:200 | Legitimate Edge Case | `--output out/tdd.md` (file) | file | Unspecified | GAP (ARCH-1, blocking) |
| `output_location` | SPEC:83, SPEC:92, SPEC:198 | Sentinel Value Match | adversarial nested path; workflow `<id>` | fixed or unknown | Conflicts with WC-4 | GAP (ARCH-1, blocking) |
| `outcome_mapping` | WC-5, SPEC:63 | Zero/Empty | no report file | none | `--outcome failed` | OK |
| `outcome_mapping` | WC-5, SPEC:63 | Typical | `partial` | partial | `--outcome succeeded`, body states `partial` | OK |
| `outcome_mapping` | WC-4/Decisions, SPEC:62, SPEC:262 | Sentinel Value Match | existing contract `status` in another vocabulary | unknown | Not stated | GAP (MED-8, Medium) |
| `wait_split` | WC-10, SPEC:68 | Typical | single call 10 min | true | Split into waits of at most 4 min | OK |
| `wait_split` | WC-10 vs AC-4.3, SPEC:68, SPEC:210 | Legitimate Edge Case | single call 270 s | false | WC-10 silent; AC-4.3 fails it | GAP (MED-14, Medium) |
| `outward_default` | WC-9, SPEC:67 | Typical | default push or post under `--unattended` | true | Off unless explicit flag in the brief | OK |
| `outward_default` | WC-3 vs WC-9, SPEC:61, SPEC:67 | Legitimate Edge Case | authorization arrives in an `ask` answer, not the brief | unknown | Not excluded by WC-3 | GAP (MED-4, Medium) |
| `readiness_fallback` | WC-1, SPEC:59 | Typical | fallback 30 s | true | Passes (CAPS:49) | OK |
| `readiness_fallback` | WC-1, SPEC:59 | Legitimate Edge Case | fallback 45-60 s | "well inside"? | No number | GAP (MED-15, Medium) |
| `adversarial_input_count` | SPEC:39; INV-A:35 | One/Minimal | one surviving report | N=1 | Not stated | GAP (MED-12, Medium) |
| `adversarial_input_count` | SPEC:39; INV-A:35 | Maximum/Overflow | more than 10 reports | N>10 | Not stated | GAP (MED-12, Medium) |

FR-8 grading: the table's GAP rows split as stated in the Status column; only the rows tied to REQ-2 and ARCH-1 name a concrete wrong outcome, so only those are blocking. FR-9: no blank "Specified Behavior" cell was left unfilled in the rows above; the "Unspecified" cells are the GAP rows. FR-10: every guard has at least one row or a one-line reason above, so synthesis is not blocked.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, triggered only by SPEC:39)

```text
[Coordinator: N Tasks, N >= 2] --> [N workers] --> [M reports, M <= N: failed/blocked leave none (SPEC:63)]
                                                      |
                                                      v
                                          [/sc:adversarial worker: expects 2..10 inputs (INV-A:35)]  <-- MISMATCH when M < 2 or M > 10
```

State Variable Registry: not produced (`--focus correctness` is not active). Advisory only: the spec has numeric thresholds (SPEC:59, SPEC:68, SPEC:210) and a multi-stage flow (SPEC:39), so `--focus correctness` is suggested for a later run.

## Expert panel summary (fixed order)

1. Wiegers: requirements are numbered and owner-tagged; REQ-1 and REQ-2 break testability and safety; MED-1 to MED-6, MED-10.
2. Adzic: the examples in AC-2.2 and AC-3.x are concrete, but AC-2.2 uses a file-valued `--output` that WC-4 cannot place (ARCH-1); MED-11.
3. Cockburn: actors (coordinator, worker session, command, person) are clear; the stall and retry paths have no primary actor (MED-7, MIN-3); MED-2.
4. Fowler: one contract file and one report name are sound (SPEC:261, SPEC:264); the path formula is not (ARCH-1); MED-8, MED-12.
5. Nygard: gate-to-blocked is a clean failure mode; no stall-detection rule (MED-7); MED-9, MED-14.
6. Whittaker: attacks 1-6 above.
7. Newman: contract versioning and the plugin mirror are open (UNVERIFIED #8, SPEC:279); MED-13.
8. Hohpe: the `worker_done` plus report-path message pattern is correctly bound to the dispatched pane (CAPS:76); the pointer-not-content caveat is handled (CAPS:79, SPEC:62).
9. Crispin: acceptance traceability gaps (MED-6); boundary rows in the table above.
10. Gregory: the decision section gives the user self-contained options (SPEC:225-253); no blocking gap beyond MED-2.
11. Hightower: operational limits (readiness, heartbeat) are cited; MED-15.
Consensus: the decision (SPEC:13-16) and the evidence behind it (SPEC:18-45) are sound and honestly hedged; the defects are in the rollout and acceptance text. Disagreements: none.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin, gregory, hightower]
  focus_areas: [requirements, architecture]
quality_assessment: {overall_score: 5.75, clarity: 7, completeness: 6, testability: 5, consistency: 5}
critical_issues:
  - {id: REQ-1, severity: MAJOR, blocking: true, expert: wiegers}
  - {id: REQ-2, severity: MAJOR, blocking: true, expert: wiegers}
  - {id: ARCH-1, severity: MAJOR, blocking: true, expert: fowler}
expert_consensus: [decision and evidence are sound, defects are in rollout and acceptance text]
improvement_roadmap:
  immediate: [REQ-1, REQ-2, ARCH-1]
  short_term: [MED-1, MED-2, MED-4, MED-5, MED-6, MED-7, MED-8]
  long_term: [MED-3, MED-9, MED-10, MED-11, MED-12, MED-13, MED-14, MED-15]
adversarial_analysis: see Whittaker section above
```

## follow-up candidates (Medium and minor; none triggers a revision or fails this review)

MED-1 to MED-15 and MIN-1 to MIN-3 above. Issue creation: the command requires the session that ran the review to ask the user once per loop whether to open an issue for these. This worker has no user channel, so the question was not asked and no issue was created; the coordinator should ask once.

## Reviser brief

Blocking finding ids: REQ-1, REQ-2, ARCH-1. (Reviser: you read this report, not the command; this restates Review Loop bullet 6.)
- Revise only text a blocking finding names: REQ-1 (SPEC:195), REQ-2 (SPEC:159 and, if needed, SPEC:196), ARCH-1 (SPEC:62 and the section 3 rows it names).
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size before (57763) and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone (MED-1 to MED-15, MIN-1 to MIN-3), including through any "apply all findings" wording.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
