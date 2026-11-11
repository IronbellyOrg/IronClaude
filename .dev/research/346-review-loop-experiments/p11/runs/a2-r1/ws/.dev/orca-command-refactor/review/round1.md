review: 1 of 3

# Spec-panel review, round 1: `orca-worker-contract-spec.md`

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d   # 285 lines
  review_date: 2026-11-10
  mode: critique
  focus_areas: [requirements, architecture]
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]   # focus panels plus Whittaker (always active)
  re_review: false   # first review of the full document, no prior findings file, no baseline
```

Citation key. `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (the only evidence checkable in this sandbox). `README:N` = `.dev/orca-command-refactor/README.md`. A citation to any file outside those four is marked UNVERIFIED.

## What I covered

- Read in full: the README, the candidate (285 lines), and all three inventories.
- Checked every `INV-A`, `INV-B`, `CAPS` and `README` line citation in `SPEC:11-26`, `SPEC:29-45`, `SPEC:59-70`, `SPEC:83-92`, `SPEC:99-125`, `SPEC:132-137`, `SPEC:147`, `SPEC:260-268` and `SPEC:272-285` against the inventory text (about 120 citations). Each lands on the content the candidate claims. The 43-command split (10 ready, 27 needing a change, 6 coordinator-only) matches the inventory totals (INV-A:73, INV-B:278). The per-phase assignment adds up: 13, 15, 4, 3 and 2 unscheduled (brainstorm, init-lite) make 37 worker candidates.
- Not checkable here, so UNVERIFIED: every `src/superclaude/...` line citation not quoted by an inventory (for example `SPEC:11`, `SPEC:52`, `SPEC:155`, `SPEC:150`), the E5 grep results (`SPEC:25`), the `CLAUDE.md` line numbers, `EVIDENCE.md:33-56` beyond what CAPS and INV-A quote, the claimed independent citation check (`SPEC:285`), and the pass condition of every acceptance check (nothing was executed; no Orca, no repo).
- Did not edit the candidate or any other file, and started no other review.

### Grading applied
The Review Loop makes FR-8 and FR-9 findings blocking. The brief's grading check is stricter: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption. The brief may narrow the blocking set, so I ran every guard-table GAP (each generates an FR-8 finding) through that check. A GAP that is a requirement the document never states, or that needs a guess between two readings, is graded Medium and listed under follow-up candidates, even where its label is MAJOR.

## Guard Condition Boundary Table

Trigger: the candidate contains thresholds and boolean guards (60 s readiness, 5 min and 4 min waits, outcome mapping, the 0.70 confidence gate, the `--unattended` switch, resume-or-fresh-dir). Six guards, six rows each, all cells populated (36 rows, 16 GAP). Every GAP is an FR-8 finding, mapped to a follow-up id in the Status column after grading.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| GC-1 launch prompt fallback inside the readiness limit | SPEC:59 | Zero/Empty | no fallback (prompt waits forever) | violates WC-1 | worker-start fails at `agent_readiness` (SPEC:59, quoting EVIDENCE.md:39 via CAPS:49) | OK |
| GC-1 | SPEC:59 | One/Minimal | fallback 1 s | satisfies | no lower bound needed | OK |
| GC-1 | SPEC:59 | Typical | fallback 30 s | satisfies | passes in 34 s (SPEC:59; CAPS:49) | OK |
| GC-1 | SPEC:59 | Maximum/Overflow | fallback 45 s to 60 s | "well inside" undefined | evidence says about 45 s fails again, but no numeric maximum is stated | GAP -> M-10 |
| GC-1 | SPEC:59 | Sentinel Value Match | coordinator raises `--timeout-ms` (for example 120000) | unspecified | brief (SPEC:73) never mentions the timeout; WC-1 says only "default 60 s" | GAP -> M-10 |
| GC-1 | SPEC:44, SPEC:59 | Legitimate Edge Case | command's own prompt appears after `input_accepted` | not a WC-1 case | stated as non-failing (SPEC:44; CAPS:52) | OK |
| GC-2 single blocking call vs heartbeat | SPEC:68 | Zero/Empty | no blocking call | no split | nothing to do | OK |
| GC-2 | SPEC:68 | One/Minimal | 1 s call | no split | none needed | OK |
| GC-2 | SPEC:68 | Typical | 3 min call | no split | heartbeat fits | OK |
| GC-2 | SPEC:68 | Maximum/Overflow | one foreground Agent-tool call that runs 30 min (cleanup-audit waves, tdd research, INV-A:42, INV-B:47) | split required | "split into waits of at most 4 minutes" cannot apply to an Agent call; only poll waits and evals are named | GAP -> M-5 |
| GC-2 | SPEC:68 | Sentinel Value Match | call of exactly 5:00, or 4:01 to 5:00 | trigger is "longer than 5 min", target is "at most 4 min" | the 4 to 5 minute band is neither split nor allowed | GAP -> M-5 |
| GC-2 | SPEC:68, SPEC:101, SPEC:123 | Legitimate Edge Case | project build or test run of 20 min (`build`, `test` rows) | split required | rows carry no WC-10 note and no check | GAP -> M-5 |
| GC-3 outcome mapping | SPEC:63 | Zero/Empty | contract file exists, 0 bytes or unparseable | "no report exists" ambiguous | not stated (AC step 4 uses `test -s`, WC-5 does not) | GAP -> M-7 |
| GC-3 | SPEC:63 | One/Minimal | `status: succeeded` | true | `--outcome succeeded` | OK |
| GC-3 | SPEC:63 | Typical | `status: partial` | true | `--outcome succeeded`, first sentence says partial | OK |
| GC-3 | SPEC:62, SPEC:63 | Maximum/Overflow | existing contract keeps its own `status` value outside the four (for example `success`, `error`) | "succeeded otherwise" | any unrecognised value maps to succeeded | GAP -> M-7 |
| GC-3 | SPEC:62, SPEC:63 | Sentinel Value Match | `status: blocked` with empty `blocked_question` | failed | WC-4 says the question is carried; nothing says what an empty one means | GAP -> M-7 |
| GC-3 | SPEC:63 | Legitimate Edge Case | audit verdict FAIL, status succeeded | true | `--outcome succeeded`, stated | OK |
| GC-4 task confidence gate | SPEC:121 | Zero/Empty | confidence 0.0 | below 0.70 | blocked | OK |
| GC-4 | SPEC:121 | One/Minimal | confidence 0.01 | below 0.70 | blocked | OK |
| GC-4 | SPEC:121 | Typical | confidence 0.85 | not below | proceeds (row is silent, standalone text unchanged) | OK |
| GC-4 | SPEC:121 | Maximum/Overflow | confidence 1.0 | not below | proceeds | OK |
| GC-4 | SPEC:121 | Sentinel Value Match | confidence exactly 0.70 | "below 0.70" false | proceeds, same boundary as INV-B:199 | OK |
| GC-4 | SPEC:121 | Legitimate Edge Case | confidence not computable (missing or NaN) | undefined | not stated | GAP -> M-13 |
| GC-5 `--unattended` switch | SPEC:51, SPEC:60, SPEC:146 | Zero/Empty | flag absent | standalone | today's behaviour (SA-1) | OK |
| GC-5 | SPEC:62, SPEC:73 | One/Minimal | flag present, no output directory | WC-4 has no `<output-dir>` | the brief is expected to supply it; command-side behaviour is not stated | GAP -> M-6 |
| GC-5 | SPEC:60, SPEC:62 | Typical | flag plus output directory | unattended | WC-2 and WC-4 apply | OK |
| GC-5 | SPEC:128 | Maximum/Overflow | flag passed to a section-4 command (`/sc:pm`, `/sc:git`) | "get no mode" | refuse, ignore or run is not stated | GAP -> M-6 |
| GC-5 | SPEC:51 | Sentinel Value Match | the token `--unattended` inside quoted prompt content (`/sc:research "what does --unattended do"`) | collides with the control flag | not stated; D1 (a) only says "explicit flag" (SPEC:228) | GAP -> M-6 |
| GC-5 | SPEC:159, SPEC:160 | Legitimate Edge Case | flag accepted after P1 by a command whose gate converts in P2 (auggie-review) | accepted, gate still live | "a no-op where a command has no gate" covers only no-gate commands | GAP -> M-2 |
| GC-6 resume or fresh dir | SPEC:64 | Zero/Empty | retry with no earlier output | fresh start | trivially clean | OK |
| GC-6 | SPEC:64, SPEC:205 | One/Minimal | retry, earlier state present, brief omits the resume flag (roadmap) | not resuming | AC-3.2 says "starts fresh" in the same directory, over the first attempt's files | GAP -> M-8 |
| GC-6 | SPEC:64 | Typical | resume flag given | resumes | stated | OK |
| GC-6 | SPEC:64; CAPS:80 | Maximum/Overflow | fourth attempt of one Task | Orca circuit breaker | owned by Orca (CAPS:116, CAPS:80), not by the candidate | OK |
| GC-6 | SPEC:112, SPEC:115, SPEC:124, SPEC:125 | Sentinel Value Match | resume column says "n/a" (load, recommend, validate-roadmap, validate-tests) | neither branch of WC-6 | "n/a" does not say fresh directory | GAP -> M-8 |
| GC-6 | SPEC:62, SPEC:64, SPEC:73 | Legitimate Edge Case | command creates its own fresh directory | breaks "known before dispatch" | WC-4 and WC-6 disagree on who picks the directory | GAP -> M-8 |

Table complete. 16 GAP rows generated 16 FR-8 findings; after the grading check all 16 fall under Medium follow-up candidates (the requirement is unstated, or needs a reading choice). The two blocking findings below come from the requirements and architecture passes, not from the table.

## Quantity Flow Diagram (pipeline dimensional analysis)

Triggered: the command inventory is filtered and fanned out across phases, and one consumer assumes the unfiltered count.

```text
[43 commands in cmd/ (INV-A:3 21 + INV-B:3 22)] --> [Stage 1: section 4 filter, -6 coordinator-only] --> [37 worker candidates]
   37 --> [Stage 2: readiness split] --> [10 ready (SPEC:78-92)] + [27 need a change (SPEC:94-125)]
   37 --> [Stage 3: phase assignment] --> P1 13 (9 + 4 fixes) | P2 15 (11 + 4) | P3 4 | P4 3 | none 2 (brainstorm, init-lite)   = 37
        |
        v
   [Consumer: P1 scope row, flag accepted by 37 (SPEC:159)]
   [Consumer: AC-1.1, a Unattended-mode section in 37 (SPEC:195)]   <-- count 37 vs 13 commands with P1 work: DIVERGENCE POINT (M-2, B-2)
   [Consumer: AC-1.2, live check on "each P1 command" = 13, including load (SPEC:196)]   <-- load has no report (B-2)
```

Counts are conserved everywhere except at the P1 consumers. FR-19 would label the mismatch CRITICAL; the grading check puts the scheduling part under M-2 (it needs a coordinator to dispatch between phases) and the `load` part under B-2 (a direct contradiction).

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking) AC-0.4 requires a step that Phase 0 cannot pass
- Expert: Adzic (lead), Wiegers. Priority High. Quality impact: Testability +2.
- Grading sentence: an implementer who follows AC-0.4 as written runs the 7.2 live check on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` at P0 and must pass steps 1-3, so builds a Phase 0 gate that cannot pass, because step 3 requires the worker's report path to be "the WC-4 contract path" and its outcome to match "the contract's `status`" (SPEC:182), while AC-0.4 itself says "the contract arrives in P1" (SPEC:194) and P0 makes no command edits (SPEC:158). Troubleshoot's report today is REPORT.md and it writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242).
- Evidence: AC-0.4 carves out step 4 only (SPEC:194). Step 3 is listed as required with no carve-out. Even the carved-out step 4 runs a YAML parse asserting `d['status']` and `d['command']` (SPEC:183), which a markdown REPORT.md cannot satisfy. "Later phases do not start until the earlier phase's checks in section 7 pass" (SPEC:154), so P1 never starts.
- Recommendation: state which parts of step 3 apply at P0 (exactly one `worker_done`, outcome matches the command's own report), and replace step 4 at P0 with a check that suits the command's own report file.

### B-2 (CRITICAL, blocking) AC-1.1 and P1 require a report contract for `/sc:load`, which the same document says must have none
- Expert: Wiegers (lead), Cockburn. Priority High. Quality impact: Consistency +2.
- Grading sentence: an implementer who follows AC-1.1 as written gives `/sc:load` a `## Unattended mode` section naming `return-contract.yaml` and, through WC-4 and AC-1.2, a contract written in unattended mode, and that is wrong because the load row says its report is "none (see note)" and that it is used "as a step inside another worker's brief, not as its own Task" (SPEC:112), and the Decisions table rejects a report file as "an unrequested addition" (SPEC:265).
- Evidence: AC-1.1 asserts the section for "every command in sections 3.1-3.2" (SPEC:195), and load is in section 3.2 (SPEC:112). P1 lists load for the flag (SPEC:159) and AC-1.2 runs the live check on "each P1 command" (SPEC:196), whose steps 3 and 4 need a contract (SPEC:182-183). WC-4 says the contract is written "on every outcome" in unattended mode (SPEC:62). The load row's own text (INV-B:65: "writes no file") agrees with the row, not with AC-1.1.
- Recommendation: exclude load from AC-1.1 and AC-1.2, or say once that load accepts no `--unattended` and gets no section. The same sweep should check the other 3.2 rows whose report column is not a contract (validate-tests, SPEC:125).

## === ARCHITECTURE ANALYSIS ===
No finding in this bucket meets the blocking bar. The architectural decision (Orca above, commands as units, section 1.3) is consistent with CAPS:97-103, CAPS:145-150, INV-A:90 and INV-B:285-286; the architecture-side issues are all under follow-up candidates below (M-1, M-3, M-6, M-8, M-9, M-12).

## Follow-up candidates (Medium and minor; none fails the review)

Each Medium finding: label, expert, the sentence, why it is Medium. All priorities Medium unless stated.

**M-1 (MAJOR, graded Medium) Where the contract lives is not defined for several commands.** Experts: Fowler, Hohpe.
- Sentence: an implementer who follows WC-4 writes `<output-dir>/return-contract.yaml` where `<output-dir>` is the "directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62), and builds a path that does not exist for the commands whose `--output` is a file (tdd and init-lite, SPEC:87, SPEC:90; spec-panel's new `--output`, SPEC:120), and conflicts with the adversarial row, which fixes it at `<output>/adversarial/return-contract.yaml` (SPEC:83), and with workflow, whose package directory `<id>` is created by the command (SPEC:92), so the path is not "known before dispatch" (SPEC:62, SPEC:73).
- Why Medium: the implementer must pick between dirname-of-the-file, a new directory flag, or the per-row path; the text allows each. AC-2.2 for tdd (SPEC:200) cannot be run deterministically until this is chosen. The P1 workflow fix "write the contract for pre-creation STOPs" (SPEC:92) names no location, since by definition no package directory exists yet. For context only, not evidence for the candidate: the spec-panel command definition in this sandbox resolves the same collision with a separate `--report-dir`, noting that `--output` is file-valued.
- Recommendation: define one location rule (for example a required directory flag, distinct from any file-valued `--output`) and list the exceptions in one table.

**M-2 (MAJOR, graded Medium) `--unattended` is shipped in P1 to commands whose gates and outward defaults convert later.** Experts: Nygard, Wiegers.
- Sentence: an implementer who follows the P1 row builds `--unattended` acceptance in all 37 commands in P1 and a section in all 37 (SPEC:159, SPEC:195), while the gate conversions land in P2 to P4 (SPEC:160-162), and a coordinator that follows the brief rule (SPEC:73) and passes `--unattended` to `/sc:auggie-review` after P1 still gets the default PR post (INV-A:38), though WC-9 says outward defaults are off under the flag (SPEC:67).
- Why Medium: it needs a coordinator to dispatch between phases and an implementer to read "accepted" as "parsed and ignored". The same row also adds the flag to pr-submit, implement and post-release (P4, waiting on D2 to D4, SPEC:154, SPEC:162) before the user decides whether pr-submit is a worker (D3 option a, SPEC:240). The parenthesis "a no-op where a command has no gate" covers only no-gate commands.
- Recommendation: add `--unattended` to a command in the phase that converts its gates, or make a command refuse the flag until it does.

**M-3 (MAJOR, graded Medium) WC-3 lets a worker take a coordinator's answer for any blocked gate, with no carve-out for safety gates.** Experts: Nygard, Hohpe.
- Sentence: an implementer who follows WC-3 builds a worker that, at any gate resolving as blocked, asks the coordinator once and re-invokes with the answer as a flag (SPEC:61), which for `/sc:implement`'s Ruling lets a coordinator reply stand in for the user, while D2 (a) and Non-goal 6 keep the rule that another agent's message is not a Ruling (SPEC:218, SPEC:233-236; INV-A:66), and for outward steps lets a reply stand in for the flag that WC-9 says must be "written in the brief" (SPEC:67).
- Why Medium: the Ruling command still has no "answer flag" (SPEC:109 says the rule is unchanged), so the harm depends on the worker session improvising. A safety gate list is simply missing.
- Recommendation: add a sentence to WC-3 naming which gates may not be answered by relay (Ruling, outward authorizations) and cross-reference D2 and D4.

**M-4 (MAJOR, graded Medium) The authorization flags for WC-9 are not defined.** Experts: Wiegers, Adzic.
- Sentence: an implementer who follows WC-9 makes outward defaults "turn on only through the command's own explicit flag written in the brief" (SPEC:67) and must invent the flags for post-release, task `commit`/`push` and pr-submit, whose rows say only "unless the brief authorizes" (SPEC:113, SPEC:121). For auggie-review the re-enabling flag is `--post-pr` (SPEC:100), but the inventory documents only `--no-post-pr` and says posting is the default (INV-A:38), so `--post-pr` may not exist.
- Why Medium: a requirement the document never states; the implementer chooses names. AC-4.2 tests only the case with no flags (SPEC:209).
- Recommendation: list the authorization flag per command in one table, mark any that must be created.

**M-5 (MAJOR, graded Medium) WC-10 covers poll waits and evals but not Agent-tool calls or long builds.** Experts: Nygard, Hohpe. FR-8 for GC-2 rows 4, 5, 6.
- Sentence: an implementer who follows WC-10 splits only the waits it names (SPEC:68, cli-eval at SPEC:104, pr-submit at SPEC:114) and builds `build`, `test`, cleanup-audit waves and tdd research as single blocking calls of unbounded length (INV-A:42, INV-A:40, INV-B:47-48), so the worker cannot heartbeat on the preamble's 5-minute cadence (CAPS:130).
- Why Medium: Orca's use of heartbeat age is itself UNVERIFIED (CAPS:182), so the wrong outcome is not shown. The 4-minute target and the "longer than 5 minutes" trigger also leave a gap (GC-2). Only AC-4.3 checks heartbeat spacing, and only for pr-submit (SPEC:210).
- Recommendation: state the rule for foreground Agent calls (poll in the background, or exempt them) and add one cadence check to 7.2.

**M-6 (MAJOR, graded Medium) Switch semantics are incomplete.** Experts: Whittaker, Fowler. FR-8 for GC-5 rows 2, 4, 5.
- Sentence: an implementer who follows WC-2 and D1 (a) builds a command that treats any `--unattended` substring as the switch (SPEC:51, SPEC:228), so `/sc:research "what does --unattended do"` runs unattended in a person's session; the spec never says the flag must be a standalone token. It also never says what a command does with the flag and no output directory, what `/sc:pm` does when passed it (SPEC:128), or that nested commands inherit it: roadmap calls `sc:save` at every wave (INV-B:154) and cli-eval create runs `/sc:spec-panel` and adversarial (INV-A:44), while only the tasklist-to-reflect case is specified (SPEC:122).
- Why Medium: unspecified edge cases; the harm needs a particular input or invocation chain.
- Recommendation: define the switch as a standalone argument token outside quotes, require nested commands to receive it, and say what each of the three missing cases does.

**M-7 (MAJOR, graded Medium) The outcome mapping has holes.** Experts: Wiegers, Adzic. FR-8 for GC-3 rows 1, 4, 5.
- Sentence: an implementer who follows WC-5 sends `--outcome succeeded` for every report that is not `failed` or `blocked` (SPEC:63), so a kept existing field value such as `status: success` or `error` (WC-4 keeps existing fields, SPEC:62, against the fixed four-value set, SPEC:262) maps to succeeded, and a 0-byte contract is neither "no report" nor a status.
- Why Medium: the existing contracts' real `status` values are not read anywhere in the candidate (INV-B:272 and INV-A:97 give field names only), so whether any conflicts is unknown.
- Recommendation: map unknown or unparseable status to `failed`, and check the vocabulary of the workflow, brainstorm, reflect and adversarial contracts once.

**M-8 (MAJOR, graded Medium) Retry rules leave stale or overwritten reports.** Experts: Nygard, Fowler. FR-8 for GC-6 rows 2, 5, 6.
- Sentence: an implementer who follows WC-6 and AC-3.2 builds a roadmap retry that "starts fresh" in the same directory when the brief omits the resume flag (SPEC:205), writing over the first attempt's files that WC-6 says must not be corrupted (SPEC:64), and builds "fresh output directory" commands that pick their own directory (SPEC:64) so the contract is not at the pre-dispatch path (SPEC:62, SPEC:73). Nothing says the contract is cleared or rewritten at start, so a retry that dies before `worker_done` leaves the earlier attempt's `status: blocked` for the coordinator to read.
- Why Medium: the first reading is the coordinator choosing a new directory per retry, which fits; the worse reading is allowed but not forced. The four "n/a" resume rows have no stated branch.
- Recommendation: say the coordinator passes a new directory on retry, the contract is rewritten as `status: running` at start, and give "n/a" rows an explicit fresh-directory statement.

**M-9 (MAJOR, graded Medium) WC-11 is violated by commands the candidate calls ready.** Experts: Nygard, Newman.
- Sentence: an implementer who follows WC-11 ("two workers in one worktree must never write the same file", SPEC:69) must change cleanup-audit (fixed `.claude-audit/`, SPEC:85) and index-repo (`PROJECT_INDEX.md`, SPEC:86), but the rows only accept the limit or "state the location", and 2.3 never tells the coordinator to avoid two same-command workers in one worktree (SPEC:73), whose placement default is a shared worktree (CAPS:115).
- Why Medium: the rule is sound; only one check (AC-3.4, SPEC:207) tests it.
- Recommendation: add a coordinator duty to 2.3, or make the outputs configurable.

**M-10 (MAJOR, graded Medium) WC-1 is untestable and has no owner.** Experts: Wiegers, Nygard. FR-8 for GC-1 rows 4, 5.
- Sentence: an implementer who follows WC-1 ("well inside the readiness limit", SPEC:59) has no numeric bound, no phase that does the launch-setup work (SPEC:156-162), and no acceptance check beyond the incidental `state: ready` in 7.2 step 1 (SPEC:180).
- Why Medium: a missing requirement; the evidence (30 s passes, about 45 s fails, SPEC:59) points to a bound the text could state.
- Recommendation: state a bound (for example 30 s) and name the owner and check.

**M-11 (MAJOR, graded Medium) SA-1 and SA-4 do not say which wins.** Experts: Wiegers, Newman.
- Sentence: an implementer who follows SA-1 keeps every default flag value and output path unchanged without `--unattended` (SPEC:146), yet SA-4 and section 3 change the validate-tests default target, the validate-roadmap report name, the adversarial contract name and the roadmap flag surface (SPEC:149, SPEC:118, SPEC:124-125), and section 5 calls SA-1 a "hard requirement on every phase" (SPEC:142).
- Why Medium: SA-4 names the exceptions, so the likely reading is that it wins; the text does not say so. The same inconsistency is in 1.1, which says the change is "limited to the worker contract" (SPEC:16).
- Recommendation: add "except the defects SA-4 names" to SA-1 and to 1.1.

**M-12 (MAJOR, graded Medium) AC-C1 can fail on content the candidate asks for.** Experts: Fowler, Adzic.
- Sentence: an implementer who follows P0 adds an Orca section to `HOW-WE-WORK.md` and writes the contract file with a question-channel example (SPEC:158, SPEC:147, SPEC:150), both under `src/superclaude/core`, which AC-C1 requires to print nothing for `orca orchestration ...` and similar (SPEC:172); SA-2 allows the mention "inside the contract file" (SPEC:147).
- Why Medium: it fails only if the text includes a literal command of those four verbs.
- Recommendation: exclude the contract file and routing guide from AC-C1, or forbid literal command lines there. Also the checks in 7.1 are written with `\|` in a table, which is only correct once rendered; copied raw they do not run.

**M-13 (MAJOR, graded Medium) The 0.70 gate has no value for an unavailable confidence.** Expert: Nygard. FR-8 for GC-4 row 6.
- Sentence: an implementer who follows the task row (SPEC:121) has no behaviour for a confidence that cannot be computed.
- Why Medium: unspecified edge case. Recommendation: treat it as below 0.70.

### Minor notes (never fail the review)
- N-1 (MINOR) `SPEC:44` states as fact that a command's own question "comes after readiness". CAPS:47 says Claude receives its task as argv; the claim is not evidenced, and WC-2 makes it harmless.
- N-2 (MINOR) `SPEC:122` sets the tasklist row's other change to "none" (nesting within the three-layer limit, INV-A:14), whereas INV-B:215 asked for the reflect fan-out at the worker's top level and INV-B:210 marks nested spawning UNVERIFIED. The Decisions row says no verdict was contradicted (SPEC:268).
- N-3 (MINOR) AC-2.4 uses `gh api ... --jq length` (SPEC:202), which counts one page; on a PR with 30 or more comments the before and after counts can match while a post happened. Use `--paginate`.
- N-4 (MINOR) The shared contract has no version field, whereas workflow's contract is versioned (INV-B:272, "contract 1.1"). Newman: add one.
- N-5 (MINOR) AC-0.4 omits `--unattended` from its command lines (SPEC:194) while 2.3 requires it in every brief (SPEC:73).
- N-6 (MINOR) UNVERIFIED item 14 (SPEC:285) is a claim of work done, not an unverified item. D5 says raising depth would "break R1's protection against runaway fan-out" (SPEC:252), but R1 (SPEC:33) is about refusal, not fan-out limits.
- N-7 (MINOR) Research row: `--strategy planning` is treated as the no-clarification strategy (SPEC:116), while INV-B:129 names it "Planning-Only" and says the command states no default.

## expert_consensus
- All experts agree the central decision and the per-command table are well evidenced; every inventory citation I checked resolves.
- Wiegers and Adzic: the weakest area is acceptance criteria, which assume artifacts that exist only after later phases (B-1, B-2, M-2).
- Nygard and Whittaker: the retry, switch and heartbeat rules leave edge states unspecified (M-5, M-6, M-8).
- Fowler and Newman: the contract location and phase scope need one rule rather than per-row exceptions (M-1, M-11).
- Disagreement: none recorded between experts.

## quality_assessment
Clarity 7, Completeness 6, Testability 5.5, Consistency 6, overall 6.1 of 10.

## improvement_roadmap
- immediate: fix B-1 and B-2.
- short_term: M-1, M-2, M-3, M-4, M-6, M-7, M-8.
- long_term: M-5, M-9 to M-13 and the minor notes.

## adversarial_analysis
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:51 and SPEC:228** (the flag marks a caller with no person) fails when **the quoted prompt contains the token**. Concrete attack: before, a person runs `/sc:research "what does --unattended do"` in a plain session and expects today's behaviour; after, the command reads the substring as the switch, and the person gets no prompts and a new `return-contract.yaml` in their tree (SA-1, SA-3 broken). Severity MAJOR (M-6).
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:62-64** (a report on every outcome, no corruption of the first attempt) fails when **a retry dies before writing**. Concrete attack: attempt 1 writes `status: blocked` to the directory; attempt 2 resumes in the same directory and crashes at start; the coordinator opens the contract and reads attempt 1's `blocked` as attempt 2's result. Severity MAJOR (M-8).
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:63** fails when **the contract is a 0-byte file**: `test -s` fails in the check (SPEC:183) but the mapping rule has no case for it. Severity MAJOR (M-7).
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62-63** fails when **a kept existing field holds `status: success`**: it is outside the four values and falls into "otherwise", so `--outcome succeeded`; with `status: error` the same mapping also reports success. Severity MAJOR (M-7).
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:69** fails when **two cleanup-audit workers share a worktree**: both write `.claude-audit/pass1-summary.md` (INV-A:42), the second overwrites the first and both report the same path. Severity MAJOR (M-9).

## Reviser brief
Blocking finding ids: B-1, B-2. Rules for the reviser (this restates the Review Loop; the reviser reads this report, not the command):
- Revise only text a blocking finding names: B-1 names AC-0.4 and step 3 of 7.2 (SPEC:182, SPEC:194); B-2 names AC-1.1, the P1 row and AC-1.2 as they apply to `/sc:load` (SPEC:195, SPEC:159, SPEC:196).
- Add no rule, mechanism or section that no blocking finding calls for; the Medium follow-up candidates are not part of this revision.
- Each added paragraph or table cites its finding id.
- Report the byte size of the specification before and after the edit.

verdict: FAIL
