review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, focus requirements,architecture)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 290 lines, sha256 `7a4862cc38412204ffb4afcc88a846d7268c3e6c8447b8a5b344d795ad99f4df`
- Baseline: none (first review of the whole document, labelled whole-document audit). No `--re-review`, so the prior-findings table does not apply.
- Reviewer model actually used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full). Grading check applied to every finding below.
- Citation key: `SPEC:N` = candidate line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage

Covered: all 290 lines of the candidate; README (all 39 lines); all three inventories in full (INV-A 121 lines, INV-B 324 lines, CAPS 189 lines). I checked every `INV-A`/`INV-B`/`CAPS` line the spec cites in sections 1 to 3 against the inventory text. All match except where stated below.

Not checkable in this sandbox, so UNVERIFIED: every `src/superclaude/...` line (`cmd/`, `sk/`), `CLAUDE.md:N` line numbers, `Makefile`, `pyproject.toml:38`, `install_core.py`, `EVIDENCE.md:N` (quoted only second-hand at CAPS:49,52,162), `.dev/codegraph-migration/...` (SPEC:23, SPEC:43, SPEC:174), `HOW-WE-WORK.md:N`, the `grep -rlni orca` result (SPEC:25), and the "11 re-read locations" and "about 340 citations re-read" claims (SPEC:11, SPEC:290). Where a finding rests on one of these it is marked UNVERIFIED.

Not covered: no test, no command and no Orca call was run; the candidate was not edited.

Counting check (Pipeline Dimensional Analysis, see the Quantity Flow Diagram): 10 + 27 + 6 = 43, and the phase lists in SPEC:158-162 cover every one of the 37 non-coordinator commands exactly once. No dropped or double-counted command.

## Panel note

Experts in the fixed order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Under focus requirements the lead is Wiegers; under architecture the lead is Fowler. Findings carry the expert who raised them.

=== REQUIREMENTS ANALYSIS ===

### F-1 (blocking, MAJOR). WC-5 fails successful runs between Phase 1 and Phase 2 (Wiegers, Adzic, Whittaker Sequence Attack)

- Location: SPEC:63 (WC-5), SPEC:79 (3.1 intro), SPEC:73 (2.3), SPEC:159-160 (P1/P2 scope), SPEC:88,89,90,91 (reflect, release-split, tdd, troubleshoot rows).
- Grading sentence: An implementer who follows the stated text as written builds a worker that sends `--outcome failed` for a successful `/sc:tdd`, `/sc:release-split` or `/sc:troubleshoot` run made after Phase 1 passes and before Phase 2 is done, and that is wrong because the run produced its deliverable and only the contract file the spec itself defers to P2 is missing.
- Contradicting texts:
  - WC-5 (SPEC:63): "From P1 on ... `--outcome failed` when the contract is absent, empty or unparseable, has no `status` or a value outside the four". Only P0 is exempted.
  - SPEC:79: ready commands "report the named file until Phase 1 adds the contract".
  - SPEC:159 limits the `--unattended` flag and `## Unattended mode` section to the listed P1 commands "and no others"; tdd, release-split, troubleshoot and reflect are P2 (SPEC:160, rows at SPEC:88-91 mark their `--unattended` change "(P2)").
  - SPEC:73: Phase 0 runs ready commands without `--unattended`; the flag arrives "from the phase that gives the command its section".
  - SPEC:62 (WC-4): the contract is written "in unattended mode".
- State trace: P1 accepted -> `/sc:tdd "<component>" --output <file>` dispatched without `--unattended` (the flag does not exist there yet) -> TDD written, no `return-contract.yaml` -> WC-5 literal: contract absent -> `worker_done --outcome failed`. The Task becomes `failed` and its dependents stay blocked (CAPS:90).
- Also open under the same rule: `/sc:reflect` writes a contract today (INV-B:112) but its `status` vocabulary and `command` field are not shown to match the WC-4 four-value set. WC-4 says such a contract "maps them" and gives no mapping (SPEC:62), so WC-5 would read an unmapped value as outside the four and return `failed` (the mapping gap is M-3). Whether reflect's vocabulary matches is UNVERIFIED (not in the inventories).
- Recommendation: narrow WC-5's "From P1 on" to "for a command whose section 3 phase is done and a run made with `--unattended`", or name the P0-style fallback (a non-empty deliverable file as the report, AC-0.4) for ready commands until their own phase. Do not add a rule; narrow the existing one. Priority High.

### M-1 (Medium). WC-10 and AC-4.3 disagree between 4 and 5 minutes (Nygard, Whittaker Divergence Attack)

- Location: SPEC:68 (WC-10) vs SPEC:215 (AC-4.3).
- WC-10 only requires splitting a wait that blocks "longer than 5 minutes"; AC-4.3 fails any "single tool call [that] exceeds 240 s". A 270-second poll call satisfies WC-10 and fails AC-4.3. The grading needs a guess (which of the two the implementer follows), so Medium.
- Recommendation: state one threshold (4 minutes, as the Decisions row at SPEC:271 says) in both places.

### M-2 (Medium). Output option and contract location left open on about eight rows (Wiegers, Cockburn)

- Location: SPEC:99,101,102,106,107,108,111,120 (analyze, build, business-panel, design, document, explain, index, spec-panel: "add an output path/`--output`; contract").
- WC-4 (SPEC:62) defines two contract locations (`<output-dir>/return-contract.yaml` for a directory, `<file>.return-contract.yaml` for a file) and says a command with no output option gets "one, or a fixed contract path, in its section 3 row". These rows name neither form, so the report path "known before dispatch" (SPEC:62,73) is not determined for them, and the AC-1.2 `test -s <contract>` check (SPEC:188,201) cannot be written. A missing statement, not a contradiction, so Medium. spec-panel is the command used for this run's own review task (INV-B:185).

### M-3 (Medium). WC-4 says existing statuses are "mapped" but gives no mapping (Wiegers)

- Location: SPEC:62 vs SPEC:63. The status vocabularies of existing contracts (workflow, brainstorm, reflect, adversarial, troubleshoot with `--caller task-unified`: INV-B:242,272, INV-A:35,39) are not listed anywhere in the inventories I could check, so no mapping can be built from the spec. Feeds F-1. Recommendation: either list the mapping per command in section 3 or require the P1/P2 edits to rewrite the field.

### M-4 (Medium). WC-3 re-invocation after `ask` has no path rule (Adzic, Nygard)

- Location: SPEC:61 vs SPEC:64 and SPEC:73. A gate resolves as blocked, the command writes `status: blocked` and stops (SPEC:60). WC-3 then lets the session `ask`, wait and "re-invoke or resume the command with the answer as a flag". WC-6 says a fresh attempt gets a new output path and a resume reuses the old one; a re-invocation with an answer is neither, so it is unclear whether the blocked contract is overwritten, kept, or the new run goes elsewhere, and which one `worker_done --report-path` carries.

### M-5 (Medium). auggie-review `--post-pr` is not evidenced to exist (Wiegers, Nygard)

- Location: SPEC:100 ("posting returns only with an explicit `--post-pr` in the brief") and SPEC:67 (WC-9: "only through the command's own explicit flag"). The inventories show `--no-post-pr` and `--remediation-offer` (INV-A:38, INV-A:78) and a default-on post, not a `--post-pr` flag. If it is new, it is a new outward-capable flag, which conflicts with SPEC:160 ("add no outward capability"). If both `--post-pr` and `--no-post-pr` are given the result is unspecified. UNVERIFIED against `cmd/auggie-review.md` (not in the sandbox).

### M-6 (Medium). Section 3.1 "Brief must pass" omits output flags that WC-6 and 2.3 need (Crispin, Gregory)

- Location: SPEC:88,89,91 (reflect, release-split, troubleshoot) vs SPEC:64 and SPEC:73 (every fresh attempt gets its own output path). The inventories show only default output directories for these three (INV-B:112,122,242). Whether `--output` exists for them is not shown; the spec's own D1 example uses `/sc:troubleshoot ... --output` (SPEC:233) and AC-0.4 (SPEC:199) requires "the brief's output directory". UNVERIFIED.

### M-7 (Medium). tasklist row asserts nested reflect fits the nesting limit, while the inventory marks it unverified (Fowler, Newman)

- Location: SPEC:122 ("its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`") vs INV-B:210, INV-B:314, INV-B:322. INV-A:14 states the docs rule (three layers, Agent withheld at the limit) and does not trace reflect Tier 2 (reviewers, then adversarial fan-out) under a tasklist-spawned subagent. INV-B:322 also notes it is unstated who answers a reflect HALT on `needs_human_decision` (INV-B:209); SPEC:122 resolves the remediation offer through `--unattended` but not that HALT, which WC-2 forbids as a wait. A stall rather than a wrong build, so Medium.

### M-8 (Medium). Section 4 says "workers make no commits or pushes", WC-9 and D4 allow them when authorized (Cockburn)

- Location: SPEC:133 vs SPEC:67, SPEC:121 (task `commit`/`push`), SPEC:113, SPEC:249-252 (D4 (a)). The git row also cites `README:31` as its basis; README:31 is a rule for the workers of this planning run ("No git commits, pushes, PRs or GitHub comments"), not product policy, and the same citation backs WC-9 (SPEC:67). The conclusion (git stays coordinator-only) is defensible on INV-A:49 alone. Recommendation: drop the README:31 citations and reword the "workers make no commits" cell to "unless D4 authorizes".

=== ARCHITECTURE ANALYSIS ===

### Strengths (no finding)

- The decision (SPEC:16, section 1) is internally consistent with its rejection of the alternative: R1 (depth 1, CAPS:97-103), R3 (worker_done bound to the dispatched pane, CAPS:76,150) and E4 (subagent fan-out outside Orca's fence, CAPS:155) all check against the inventory.
- Honest evidence statement in 1.4 (SPEC:41-45) matches CAPS:156,186,187 and INV-B:323.
- Standalone preservation (section 5) is well formed: SA-1 to SA-6 are each tied to an AC (AC-1.3, AC-2.5, AC-C5).

### M-9 (Medium). 1.4 (2) states as fact that a command's own question does not fail `worker-start` (Fowler, Nygard)

- Location: SPEC:44. CAPS:47 shows Claude receives the task by `argv` (the prompt is part of launch), and readiness waits for a "fresh input box" (CAPS:47). The inventories do not show what readiness does when the argv-injected first command asks a question before the composer is fresh, which is the case for `/sc:tdd` with a bare topic or `/sc:cli-eval run`. The spec's own AC-2.2 (SPEC:205) and 7.2 step 1 would catch it, so this is a stated-as-fact risk, not a wrong build. Minor-to-Medium; listed Medium.

### M-10 (Medium). SA-2/SA-5 and P0 disagree on whether core files may mention Orca (Fowler)

- Location: SPEC:147 ("only the contract file under `src/superclaude/core/` may") vs SPEC:150 and SPEC:158 (P0 adds an Orca section to `HOW-WE-WORK.md`, also in core). AC-C1 (SPEC:180) greps only commands, skills and agents, so the check passes either way. Wording only.

### M-11 (Medium). WC-1 has no owner or phase in the plan (Hightower, Gregory)

- Location: SPEC:59 ("Launch setup, not commands"). No phase in SPEC:156-162 changes the launcher (the `ccsession-tag` wrapper) and section 8 does not exclude it. It is verified only indirectly by 7.2 step 1. A requirement with no delivery path.

### M-12 (Medium). AC-C5 can fail on edits SA-4 allows (Crispin, Newman)

- Location: SPEC:176 (AC-C5: no `^-[^-]` line, "edits are additive") vs SPEC:149 (SA-4 permits "new flags"). Adding a flag by editing the existing Usage line produces a deleted line and fails AC-C5. The spec does not say new flags go on new lines. The acceptance criterion passes only if the implementer picks that reading.

### Pipeline Dimensional Analysis (Fowler, Whittaker) and Quantity Flow Diagram

```text
[Inventories: 43 commands] --> [Verdict split] --> [10 ready | 27 needs-change | 6 coordinator-only]
   (INV-A 21 + INV-B 22)        (SPEC:76)                 |
                                                          v
   [Phase assignment SPEC:158-162]
     P0: 0 commands edited (3 smoke runs of ready commands)
     P1: 15  = 9 needs-change (analyze, build, business-panel, design, document, explain, index, test, load)
             + 6 ready (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow)
     P2: 15  = 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot)  <-- F-1 window: no contract yet
     P3: 4
     P4: 3
   Sum 15+15+4+3 = 37 = 10 + 27; + 6 coordinator-only = 43. No mismatch.
   Consumer WC-5 (SPEC:63) expects a contract from P1 on: reads 37 commands, but only
   15 + (reflect, workflow..) have one at P1  <-- MISMATCH (F-1)
```

Result: the counts reconcile; the only dimensional mismatch is the WC-5 consumer, reported as F-1 with the concrete trace above.

### Whittaker adversarial findings

- I can break this specification by **Sequence Attack**. The invariant at **SPEC:63 (WC-5) with SPEC:159-160** fails when **a ready command in P2 (tdd, release-split, troubleshoot) is dispatched after P1 passes and before P2 starts**. Concrete attack: P1 done -> `/sc:troubleshoot "x"` (no `--unattended`; flag not yet added) -> REPORT.md written, no contract -> WC-5: contract absent -> `--outcome failed`. Before: Task `ready`; after: Task `failed`, dependents blocked. Severity: blocking (F-1).
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:68 vs SPEC:215** fails when **a single wait lasts 270 s**: WC-10 does not require splitting, AC-4.3 fails the run. Severity: Medium (M-1).
- I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:62-63** (contract written on every outcome, including "stops before any other output exists") fails when **the output directory itself cannot be created** (WC-2 case, `--output` unwritable): there is nowhere to write the contract, and WC-5 reads "absent" as `failed` with no `blocked_question`. Behavior is inferrable (outcome failed), so MINOR; see follow-up candidates.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:63** treats `status: partial` as `succeeded`; an audit whose verdict is FAIL is also `succeeded`. A coordinator reading only `--outcome succeeded` cannot tell a FAIL verdict from a pass; the spec's mitigation is the first sentence of the body (SPEC:63), which is prose. Severity MINOR (behavior stated, mitigation weak).
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:61,64 with CAPS:80,116** fails when **a command is blocked repeatedly and each `--retry-of` start fails**; CAPS:80 says a worker's own `failed` report does not count toward the circuit breaker, so only failed starts do. No gap found.

### Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)

Guards identified: G1 contract-outcome mapping (WC-5), G2 wait-size threshold (WC-10), G3 `--unattended` selection (D1), G4 phase gating of the flag (SPEC:159). Input classes left out for a guard are stated in one line after the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 contract outcome | SPEC:63 | Zero/Empty | contract file empty or absent | outcome failed | `--outcome failed` (P1 on); P0 follows AC-0.4 | GAP (F-1: ready commands before their phase) |
| G1 contract outcome | SPEC:63 | One/Minimal | `status: partial` | outcome succeeded | succeeded, body states partial | OK |
| G1 contract outcome | SPEC:62-63 | Typical | `status: succeeded` | outcome succeeded | succeeded | OK |
| G1 contract outcome | SPEC:63 | Sentinel Value Match | `status: blocked` | outcome failed | failed, `blocked_question` present | OK |
| G1 contract outcome | SPEC:62-63 | Legitimate Edge Case | existing contract with another status vocabulary | mapping applied or failed | "maps them" with no mapping | GAP (M-3) |
| G2 wait size | SPEC:68 | Typical | wait 3 min | no split needed | stated | OK |
| G2 wait size | SPEC:68, 215 | Maximum/Overflow | wait 4 to 5 min | no split (WC-10) / fail (AC-4.3) | conflicting | GAP (M-1) |
| G2 wait size | SPEC:68 | Legitimate Edge Case | wait over 5 min | split into at most 4 min | stated | OK |
| G3 flag selection | SPEC:51, 232-235 | Typical | `--unattended` present | unattended mode | stated | OK |
| G3 flag selection | SPEC:51 | Legitimate Edge Case | `--unattended` in a quoted argument | not specified | UNVERIFIED for this spec (the spec does not say; the command side owns it) | GAP (minor) |
| G4 phase gate | SPEC:159, 73 | Sentinel Value Match | ready command run after P1, before its P2 | no section yet, no contract | contradictory with WC-5 | GAP (F-1) |

Classes left out: G2/G3/G4 Zero (a zero-length wait or empty flag cannot occur by definition); G1/G4 Maximum (no capacity bound; counts are fixed at 43).

GAP severities: F-1 blocking, M-1, M-3 Medium, the quoted-argument GAP is a MINOR note (the spec delegates mode selection to each command's own section, which the SA-1 text covers).

=== FOLLOW-UP CANDIDATES (Medium and minor; none triggers a revision) ===

Medium: M-1 WC-10/AC-4.3 threshold; M-2 output option and contract location on eight rows; M-3 status mapping for existing contracts; M-4 WC-3 re-invocation path; M-5 auggie-review `--post-pr` (UNVERIFIED); M-6 3.1 brief omits output flags (UNVERIFIED); M-7 tasklist nested reflect and HALT; M-8 "workers make no commits" vs D4 and README:31 misuse; M-9 readiness claim in 1.4 (2); M-10 core-file wording SA-2 vs P0; M-11 WC-1 no owner; M-12 AC-C5 vs SA-4.

Minor notes:

- N-1. SPEC:290 item 14 sits under the "UNVERIFIED items" heading but reports a completed check, not an open item. Its numbers (9 defects: 5+3+1) are consistent.
- N-2. SPEC:257 says raising depth "would break R1's protection against runaway fan-out"; R1 (SPEC:33) is a refusal reason, not a protection. Wording.
- N-3. 7.2 step 5 (SPEC:189) searches the transcript for the string `AskUserQuestion`; a transcript that merely quotes the command text containing that word would fail the check. Wording of the check.
- N-4. SPEC:60 and SPEC:61: the unwritable-output-directory case has no stated contract location (Zero/Empty attack above); the outcome `failed` is inferable.
- N-5. P2 contains both tasklist (passes `--unattended` to reflect, SPEC:122) and reflect (adds its `--unattended`, SPEC:88) with no order inside the phase.
- N-6. SPEC:139 and SPEC:112 note `/sc:load` and `/sc:recommend` as coordinator-side helpers while counting them in the 27 workers; consistent with the Decisions row at SPEC:273, noted only for the count.
- N-7. 3.2 counts pr-submit among the 27 changes needed while the recommended D3 (a) makes no change (SPEC:114, SPEC:245).

Question for the user, once per loop (not asked in this run because the coordinator brief said to write the report only): open an issue for the follow-up candidates above? None was created.

Brief clauses overridden: none. The brief narrowed to a whole-document first review and did not regrade any minor finding.

## Reviser brief

Applies only to blocking finding ids: **F-1**. The reviser reads this report, not the command. Rules (from the command's Review Loop, bullet 6):

- Revise only text that blocking finding F-1 names: SPEC:63 (WC-5 "From P1 on ..."), and if needed SPEC:79 (the 3.1 intro "until Phase 1 adds the contract") so the two agree with SPEC:159-160.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id (F-1).
- Prefer deleting or narrowing to adding: narrow WC-5's trigger rather than add a new rule or move commands between phases.
- Report the byte size of the specification before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-1 to M-12, N-1 to N-7) alone.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
