review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| Candidate sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Baseline / prior report | none given: first review of the full document (no `--re-review`, no `--baseline`) |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; grading check applied to every finding) |
| Brief clauses overridden | none (the brief narrowed scope to one output file and asked for path:line citations; neither widens the command) |
| Format | standard (default) with critique-mode buckets |
| Improve step (Behavioral Flow 6) | not run; the brief assigns only this file, so no revised specification is written and the candidate is untouched |
| Input type | not a TDD (heading count `## N.` = 9, so 0 points; no TDD frontmatter, section names or phrase; score 0 < 5) and not a PRD; no `target_release` question applies |

## What I covered, and what I could not check

Covered: the whole candidate; `.dev/orca-command-refactor/README.md` (binding context); `inventory/commands-a.md` (120 lines), `inventory/commands-b.md` (323), `inventory/orca-capabilities.md` (188). Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in the candidate was resolved against those three files; the row-to-line mapping for all 43 commands and the CAPS ranges quoted in sections 1-2 and 7-9 matched. I re-derived the 10 / 27 / 6 split and the per-phase membership. I read the 12 WC rules, 6 SA rules, 5 phases, every acceptance check in section 7 and all 5 decisions for internal consistency.

UNVERIFIED (outside the workspace, nothing here could be opened): every citation to `src/superclaude/**` (`cmd/`, `sk/`, `ag/`), `CLAUDE.md`, `Makefile`, `pyproject.toml:38`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/**`, and the candidate's own claims of a 11-location re-read (line 11) and a 340-citation validator pass (line 285). Where this report relies on those, it relies on the inventory line that quotes them and says so.

## Guard Condition Boundary Table (completed before synthesis; Nygard builds, Crispin checks completeness, Whittaker attacks)

Trigger fired: the candidate contains thresholds (60 s readiness, 5 min / 4 min waits, `< 0.70` confidence, depth 1, `--monitor` ordinals), boolean guards (`--unattended`) and a status-keyed mapping. Classes left out of a guard are named in its "omitted" line. A GAP is blocking only if it names a concrete wrong outcome or a safety-boundary risk (command FR-8 / FR-9); otherwise it is Medium and listed under follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract path `<output-dir>/return-contract.yaml` | spec:62, 73, 182 | Typical | brainstorm / reflect, `--output <dir>` | path matches | `<output>/return-contract.yaml` (spec:84, 88) | OK |
| contract path | spec:62, 83 | Legitimate Edge | adversarial, `--output <dir>` | path differs | contract at `<output>/adversarial/return-contract.yaml` (spec:83) while WC-4 says `<output-dir>/return-contract.yaml` | GAP (F-01) |
| contract path | spec:62, 92 | Legitimate Edge | workflow: no output dir in brief, `<id>` made at run time | path unknown before dispatch | contract at `.dev/tasks/to-do/<id>/...` (spec:92); WC-4 title says "known before dispatch" | GAP (F-01) |
| contract path | spec:92 | Zero/Empty | workflow stops before the package folder exists | no folder to hold the file | "Write the contract for pre-creation STOPs too" with no location | GAP (F-01) |
| contract path | spec:62, 87, 90, 120 | Legitimate Edge | `--output <file>` (tdd, init-lite, spec-panel after change) | `<output-dir>` undefined | not specified | GAP (F-01) |
| contract path | spec:62, 159 | Zero/Empty | `--unattended` with no output dir or flag (cleanup-audit, index-repo, load) | no `<output-dir>` | not specified | GAP (F-08) |
| contract path | spec:62 | Maximum/Overflow | omitted: a path has no capacity bound in this spec | n/a | n/a | OK |
| outcome map (WC-5) | spec:63 | Zero/Empty | contract file absent | "no report exists" true | `--outcome failed` | OK |
| outcome map | spec:62, 63 | Zero/Empty | file present but empty, truncated, or `status` key missing | no-report false; failed/blocked false | "succeeded otherwise" gives `succeeded` | GAP (F-05) |
| outcome map | spec:63 | One/Minimal | contract with only `status: failed` | true | `failed` | OK |
| outcome map | spec:63 | Typical | `status: succeeded` | true | `succeeded` | OK |
| outcome map | spec:63, 263 | Sentinel Value Match | `status: partial` / `status: blocked` | partial maps to succeeded; blocked to failed | stated, with rationale (spec:263) | OK |
| outcome map | spec:62, 262, 63 | Sentinel Value Match | `status` outside the four values (existing contracts "keep their fields", spec:62) | not in set | "succeeded otherwise" | GAP (F-05, F-17) |
| outcome map | spec:63 | Legitimate Edge | audit whose own verdict is FAIL, `status: succeeded` | true | `succeeded`, body states the verdict | OK |
| outcome map | spec:63 | Maximum/Overflow | omitted: no size or count enters the mapping | n/a | n/a | OK |
| wait split (WC-10) | spec:68 | Zero/Empty | step blocks 0 s | trigger (> 5 min) false | no split; nothing to do | OK |
| wait split | spec:68 | One/Minimal | 1 s | false | no split | OK |
| wait split | spec:68 | Typical | 2 min poll | false | heartbeat between waits | OK |
| wait split | spec:68, 114, 210 | Legitimate Edge | one call of 4 min < t <= 5 min | WC-10 trigger false | WC-10 requires no split; AC-4.3 (spec:210) fails any call over 240 s and the pr-submit row (spec:114) wants each iteration under 4 min | GAP (F-07) |
| wait split | spec:68, 104 | Maximum/Overflow | cli-eval eval up to 3600 s | true | split into waits of at most 4 min (spec:104) | OK |
| wait split | spec:65, 68, 24 | Legitimate Edge | one Agent-tool fan-out call (cleanup-audit waves, tdd) blocking > 5 min | true as written | cannot be split; spec:65 and E4 keep fan-out "as it is" | GAP (F-07) |
| wait split | spec:68 | Sentinel Value Match | omitted: no sentinel value in the guard | n/a | n/a | OK |
| `--unattended` switch | spec:51, 146 | Zero/Empty | flag absent | false | today's behaviour unchanged (SA-1) | OK |
| `--unattended` switch | spec:60, 73 | One/Minimal | flag plus every required flag and an output dir | true | per section 3 rows | OK |
| `--unattended` switch | spec:102, 103, 108, 110, 114, 123 | Legitimate Edge | flag together with an interactive-only flag (`--mode socratic`, `--interactive`, `--format interactive`, `--monitor 1`, `--watch`) on a section 3.2 command | true | refused (named per row) | OK |
| `--unattended` switch | spec:60, 83, 84, 89 | Legitimate Edge | flag together with `--interactive` on adversarial / brainstorm / release-split | true | only "never `--interactive`" in the brief column; no refusal rule | GAP (F-08) |
| `--unattended` switch | spec:51, 228 | Sentinel Value Match | the string `--unattended` inside quoted prompt text (`/sc:tdd "explain --unattended"`) | ambiguous | not specified | GAP (F-21) |
| `--unattended` switch | spec:159 | Typical | flag on a command whose gate is converted in a later phase (auggie-review, task, post-release) | true | accepted in P1, gates converted in P2-P4 (spec:159-162) | GAP (F-02) |
| `--unattended` switch | spec:51 | Maximum/Overflow | omitted: a boolean flag has no capacity | n/a | n/a | OK |
| task confidence `< 0.70` | spec:121 | Zero/Empty | confidence 0.0 | true | blocked | OK |
| task confidence | spec:121 | Zero/Empty | confidence not produced (null) | undefined | not specified | GAP (F-22) |
| task confidence | spec:121 | Typical | 0.85 | false | proceeds | OK |
| task confidence | spec:121; INV-B:199 | Legitimate Edge | exactly 0.70 | false ("below 0.70") | proceeds | OK |
| task confidence | spec:121 | Maximum/Overflow | 1.0 | false | proceeds | OK |
| pr-submit `--monitor` | spec:114 | Zero/Empty | `--monitor 0` | not stated | not specified (INV-B:89 describes only ordinal 1 and the default 3) | GAP (F-19) |
| pr-submit `--monitor` | spec:114 | One/Minimal | `--monitor 1` | true | refused under `--unattended` | OK |
| pr-submit `--monitor` | spec:114 | Typical | `--monitor 2` | not stated | not specified | GAP (F-19) |
| pr-submit `--monitor` | spec:114, 241 | Legitimate Edge | `--monitor 3` (default, INV-B:89) | false | no y/n gate; its pushes and thread resolutions fall under WC-9 (spec:67) and D3 (spec:238-242) | OK |
| pr-submit `--monitor` | spec:114 | Maximum/Overflow | omitted: values outside {0,1,2,3} are rejected by the command's own parser (UNVERIFIED, not read) | n/a | n/a | OK |
| nesting depth | spec:33, 66; CAPS:97-101 | Zero/Empty | setting 0 or malformed | falls back to 1 | CAPS:100 | OK |
| nesting depth | spec:33, 66 | One/Minimal | depth 1 (current) | worker may not dispatch | WC-8 forbids command calls | OK |
| nesting depth | spec:252, 66 | Maximum/Overflow | setting >= 2 (D5 option b) | allowed by Orca | WC-8 still forbids command calls | OK |
| nesting depth | spec:24, 45; CAPS:155 | Legitimate Edge | Agent-tool subagent inside a worker | not counted by the Orca fence | stated; Orca limits on subagents UNVERIFIED (spec:45) | OK |
| readiness limit (WC-1) | spec:59 | Zero/Empty | no startup prompt | ready | passes | OK |
| readiness limit | spec:59; CAPS:49 | Typical | startup prompt with 30 s fallback | within 60 s | passes (EVIDENCE via CAPS:49) | OK |
| readiness limit | spec:59; CAPS:49 | Maximum/Overflow | fallback above about 45 s | exceeds | fails again (CAPS:49) | OK |
| readiness limit | spec:59 | Legitimate Edge | fallback between 30 s and 45 s | "well inside" undefined | no number in WC-1 | GAP (F-22) |
| readiness limit | spec:44; CAPS:47 | Legitimate Edge | command gate that fires in the first 60 s of an argv-delivered prompt | unknown | spec:44 says it cannot fail worker-start; evidence does not show that | GAP (F-11) |
| retry (WC-6) | spec:64 | Zero/Empty | first run, no prior attempt | n/a | fresh | OK |
| retry | spec:62, 64, 73; CAPS:116 | One/Minimal | first `--retry-of` with the same brief and `<output-dir>` | dir not fresh | WC-6 says "fresh output directory"; WC-4 and 2.3 fix the dir in the brief | GAP (F-06) |
| retry | spec:64; CAPS:80 | Maximum/Overflow | third consecutive failure | Orca circuit-breaks | a worker's own `failed` report does not count | OK |
| retry | spec:84, 109 | Legitimate Edge | command with a resume flag | resume | resumes from disk | OK |
| phase gate | spec:154, 194 | Typical | P0 smoke run of `/sc:troubleshoot` | step 3 needs the WC-4 contract and its `status` | no WC-4 contract exists before P1 | GAP (F-03) |
| phase gate | spec:195 | Legitimate Edge | AC-1.1 over brainstorm, init-lite, load | section required | rows say "None" or "none" (spec:79, 84, 87, 112) | GAP (F-02) |
| phase gate | spec:196 | Legitimate Edge | AC-1.2 `--unattended --output <dir>` on index-repo, cleanup-audit, load, workflow | flag missing | those rows have no `--output` (spec:85, 86, 92, 112) | GAP (F-02) |
| phase gate | spec:154 | Zero/Empty | no check run | phase not passed | later phase does not start | OK |

Completion check (FR-10): every guard above has all cells populated and every omitted class carries its one-line reason. Synthesis follows.

## Pipeline Dimensional Analysis

Not triggered as a data pipeline (no multi-stage flow where a stage drops or fans out items). The one count flow is the command partition, checked for conservation: 21 + 22 = 43 (INV-A:3, INV-B:3); 10 (spec:81-92) + 27 (spec:99-125) + 6 (spec:132-137) = 43; phase membership 13 (P1) + 15 (P2) + 4 (P3) + 3 (P4) = 35, plus brainstorm and init-lite, which have no phase (spec:84, 87), = 37 = 10 + 27. Counts hold. The two phase-less rows feed F-02.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### F-01 [MAJOR, blocking] WC-4 names one contract path; the section 3 rows deliver others
- Experts: Wiegers, Adzic, Whittaker (Divergence attack). Priority High. Quality impact: Testability and Consistency, about -2 each.
- Grading sentence: an implementer who follows the stated text builds adversarial with its contract at `<output>/adversarial/return-contract.yaml` (spec:83) and workflow with its contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92), while WC-4 (spec:62), section 2.3 (spec:73), check 7.2 step 3 (spec:182) and AC-1.2 (spec:196) look for `<output-dir>/return-contract.yaml` in the directory the brief passed; the coordinator finds no file, and WC-5 (spec:63) maps "no report exists" to `--outcome failed` for a command that succeeded.
- Evidence: INV-A:35 and INV-A:60 (adversarial writes under `<output>/adversarial/`, sometimes `.../adversarial/adversarial/`); INV-B:272 (workflow contract lives in the package folder and "Not written for pre-creation STOPs"); the workflow brief passes only `--handoff none` (spec:92), so no `<output-dir>` exists; `--output <file>` commands (tdd spec:90, init-lite spec:87, spec-panel after the change spec:120) have no `<output-dir>` either.
- Also: the workflow row (spec:92) requires a contract for pre-creation STOPs, but the contract's only location is the package folder created after those STOPs. The text cannot be built as written.
- Recommendation: let each section 3 row name its contract path, derived from what the brief passes, and let WC-4 say "the path named in the command's row"; give workflow and the file-valued `--output` commands an explicit location. Rationale: one rule per command removes the conflict without changing any command's existing output.

### F-03 [MAJOR, blocking] AC-0.4 cannot pass: its step 3 needs a contract that P0 cannot produce
- Experts: Wiegers, Crispin, Whittaker (Sequence attack). Priority High. Quality impact: Testability -3.
- Grading sentence: an implementer who follows the stated text builds P0 exactly as scoped (no command edits, spec:158) and runs AC-0.4 (spec:194), which requires "steps 1-3 and 5-7 pass"; step 3 (spec:182) requires the `--outcome` to match "the contract's status under WC-5" and the report path to be "the WC-4 contract path", and no WC-4 contract exists before P1 (spec:79, 159); `/sc:troubleshoot` writes REPORT.md only (spec:91; INV-B:242). Phase gating (spec:154) then keeps P1 from starting, so the plan cannot advance.
- Also in the same check: step 1 builds the brief "per section 2.3" (spec:180, 73), which requires `--unattended` in the command line, while the AC-0.4 command lines carry none (spec:194) and no command accepts the flag until P1 (spec:159).
- Recommendation: narrow P0's step 3 and step 1 to the command's existing report file and its own status text, and say the WC-4 and `--unattended` conditions start at P1. Rationale: the smoke run's purpose (spec:158) is to test the direct-route decision, which needs neither.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

### F-02 [MAJOR, blocking] P1 scope and AC-1.1 / AC-1.2 contradict the rest of the plan and leave `--unattended` unsafe between phases
- Experts: Fowler, Nygard, Whittaker (Sequence attack). Priority High. Quality impact: Consistency -3, safety posture of the interim state.
- Grading sentence: an implementer who follows the stated text builds P1 so that `--unattended` is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159) and so that AC-1.1 (spec:195) finds a `## Unattended mode` section naming `return-contract.yaml` in all 37 commands, while the gate conversions that make the flag safe arrive in P2 to P4 (spec:160-162); at the end of P1, `/sc:auggie-review <PR> --unattended` still posts to the PR and offers remediation (spec:100, INV-A:38), `/sc:task` still commits and pushes on EXEMPT keywords (spec:121), and `/sc:post-release` still installs and provisions (spec:113), which WC-2 and WC-9 (spec:60, 67) say never happens under `--unattended`; the plan says every phase is independently useful (spec:154).
- Contradictions inside the same scope, each a stated text:
  - 3.1 intro: "The only command changes are the small fixes in the last column" (spec:79), and brainstorm and init-lite say "None" (spec:84, 87) and appear in no phase (section 6, spec:159-162); AC-1.1 requires them to gain a section.
  - load: report "none", "use it as a step inside another worker's brief, not as its own Task" (spec:112, 265); AC-1.1 requires it to name `return-contract.yaml`, and AC-1.2 runs it with `--unattended --output <dir>` (spec:196).
  - AC-1.2 runs every P1 command with `--output <dir>` (spec:196), but index-repo, cleanup-audit and workflow have no such flag in their rows (spec:85, 86, 92).
  - pr-submit, implement and post-release are listed in AC-1.1's set, yet "Phases 1-3 need no user decision" (spec:154) and P4 waits on D2-D4 (spec:162); under D3 option (a) the recommended outcome is "no pr-submit changes" (spec:240).
- Recommendation: restrict the `--unattended` flag, its section and its AC-1.x checks to the commands the phase converts (the P1 list in spec:159, using the section 6 command list), and add that a command accepts `--unattended` only in the phase that resolves its gates. Rationale: it deletes scope instead of adding rules and removes the unsafe interim state.

## === ADVERSARIAL ANALYSIS === (Whittaker; one attack per methodology, using the evidence above)

1. I can break this specification by **Divergence Attack**. The invariant at **WC-4 / 2.3 (spec:62, 73)** ("report path known before dispatch") fails when **the command's own row sets a different path**. Concrete attack: brief passes `--output .dev/x/`, adversarial writes `.dev/x/adversarial/return-contract.yaml`; before: coordinator expects `.dev/x/return-contract.yaml` and finds none; after: `worker_done --outcome failed` for a successful run (F-01).
2. I can break this specification by **Sequence Attack**. The invariant at **section 6 ordering plus WC-9 (spec:154, 159-162, 67)** fails when **a coordinator uses the flag after P1 only**. Concrete attack: P1 merged, P2 not; brief `/sc:auggie-review 123 --unattended --output d/`; before: PR 123 has N reviews; after: N + 1 and the worker idles on the chat remediation offer with no `worker_done` (F-02).
3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (spec:63)** fails when **the contract file exists but is empty or lacks `status`**. Concrete attack: a command is killed after `touch return-contract.yaml`; before: Task running; after: worker sends `--outcome succeeded` ("succeeded otherwise") and the Task settles as completed (F-05).
4. I can break this specification by **Accumulation Attack**. The invariant at **WC-6 / WC-4 (spec:62, 64, 73)** fails when **a retry re-uses the same brief**. Concrete attack: attempt 1 writes `d/return-contract.yaml` (`status: failed`) and half its artifacts; `worker-start --retry-of` re-runs with `--output d/`; before: 5 files from attempt 1; after: 3 overwritten, 2 stale files from attempt 1 remain beside a contract that says `succeeded` (F-06). A second accumulation: two reflect workers on one slug both write `docs/memory/reflect/deviation-patterns-<slug>.md` (INV-B:114; F-13).
5. I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (spec:228)** ("a person never types it, cannot misfire") fails when **the literal `--unattended` appears inside a quoted topic**. Concrete attack: `/sc:tdd "document the --unattended flag"`; before: interactive run; after: depends on token parsing the spec never defines (F-21).

## Expert sequence (fixed review order)

1. Wiegers: WC-4 and the section 3 rows disagree on the contract path (F-01); acceptance checks over-assert (F-02, F-03); WC-6 has no acceptance check at all (spec:64; no AC row names WC-6); "well inside" (spec:59) is unmeasured (F-22).
2. Adzic: the example commands in section 7 are strong (spec:194, 200), but the P0 example cannot produce the pass condition it states (F-03).
3. Cockburn: primary actor is the coordinator agent, goal "read a trustworthy report"; the contract's weakest point is the report-existence test (F-05).
4. Fowler: `--unattended` bundles five concerns (no prompts, outward defaults off, report file, parallel-safe writes, nesting); acceptable, but the per-phase slice of it is undefined (F-02).
5. Nygard: retry, missed-heartbeat and crash paths are thin (F-05, F-06, F-07); the circuit-breaker note is right (spec:263; CAPS:80).
6. Whittaker: attacks above.
7. Newman: the contract has no schema version and may collide with a versioned existing contract (F-17).
8. Hohpe: nested command invocations carry no propagation rule for `--unattended` or contract paths (F-09).
9. Crispin: static string-presence tests (AC-1.1, AC-2.1) prove text, not behaviour, but the live checks in 7.2 do cover behaviour; no live check covers WC-6, WC-11 outside save, or WC-12 (F-06, F-23).
10. Gregory: the quality conversation for D1-D5 is well framed; Phases 1-3 "need no user decision" while D1 decides P1's mechanism (F-20).
11. Hightower: operationally sound; heartbeat gaps during subagent waits are the operational risk (F-07).

## Findings table

| id | label | graded | blocking | location |
|---|---|---|---|---|
| F-01 | MAJOR | blocking | yes | spec:62, 73, 83, 87, 90, 92, 120, 182 |
| F-02 | MAJOR | blocking | yes | spec:79, 84, 87, 112, 154, 159-162, 195, 196 |
| F-03 | MAJOR | blocking | yes | spec:158, 180, 182, 194 |
| F-04 to F-20 | MAJOR / MINOR | Medium | no | follow-up candidates |
| F-21 to F-28 | MINOR | minor | no | follow-up candidates |

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.3
  clarity: 7
  completeness: 7
  testability: 5
  consistency: 6
critical_issues:
  - {category: requirements, severity: MAJOR, expert: Wiegers, issue: "WC-4 contract path vs adversarial/workflow/file-valued rows (F-01)", recommendation: "name the path per row"}
  - {category: architecture, severity: MAJOR, expert: Fowler, issue: "P1 scope and AC-1.1/1.2 contradict rows and leave --unattended unsafe between phases (F-02)", recommendation: "restrict flag, section and checks to the phase that converts the gates"}
  - {category: requirements, severity: MAJOR, expert: Crispin, issue: "AC-0.4 cannot pass in P0 (F-03)", recommendation: "limit P0 step 3 and step 1 to existing report files"}
expert_consensus:
  - "The decision (coordinator on top, commands as workers) is well supported by CAPS and the inventories."
  - "Counts, inventory line mappings and CAPS citations check out; the defects are in rollout and acceptance wording."
improvement_roadmap:
  immediate: [F-01, F-02, F-03]
  short_term: [F-04, F-05, F-06, F-07, F-08, F-09]
  long_term: [F-10 to F-28]
adversarial_analysis:
  - {attack: Divergence, severity: MAJOR, invariant: "spec:62,73", finding: F-01}
  - {attack: Sequence, severity: MAJOR, invariant: "spec:154,159-162,67", finding: F-02}
  - {attack: Zero/Empty, severity: MAJOR, invariant: "spec:63", finding: F-05}
  - {attack: Accumulation, severity: MAJOR, invariant: "spec:62,64,73", finding: F-06}
  - {attack: Sentinel Collision, severity: MINOR, invariant: "spec:228", finding: F-21}
```

Correctness-focus suggestion (advisory only, not activated): the candidate has numeric thresholds (60 s, 5 / 4 min, 0.70, depth 1) and a status-keyed mapping; `--focus correctness` on a later review would add a State Variable Registry.

## Follow-up candidates (Medium and minor; never trigger a revision, never in the Reviser brief)

Medium (a warning; the label may say MAJOR but the sentence needs a guess between two allowed readings, or the item is a requirement the document never states):

| id | label | expert | issue (path:line) | recommendation | priority | impact |
|---|---|---|---|---|---|---|
| F-04 | MAJOR | Nygard | WC-3 lets the worker "re-invoke ... with the answer as a flag" (spec:61) while WC-9 turns outward actions on "only through the command's own explicit flag written in the brief" (spec:67) and D4(a) wants the user's own instruction quoted in the brief (spec:245); a coordinator answer could switch on `--post-pr` or a VM flag. Needs the guess that the implementer lets WC-3 win. | state that an `ask` answer never enables an outward flag | Medium | safety clarity |
| F-05 | MAJOR | Whittaker | WC-5 "succeeded otherwise" (spec:63) sends an empty, truncated or out-of-vocabulary `status` to `succeeded`; WC-4 only defines the set for conforming writers (spec:62). | `succeeded` only when `status` parses to `succeeded` or `partial` | Medium | outcome reliability |
| F-06 | MAJOR | Nygard | WC-6 "fresh output directory" (spec:64) vs a brief-fixed dir reused by `--retry-of` (spec:62, 73; CAPS:116); about 20 rows say "fresh dir" (spec:99-125) with no mechanism; no AC in section 7 mentions WC-6. | say who makes the dir fresh (coordinator per attempt) and add one retry check | Medium | retry safety |
| F-07 | MAJOR | Nygard | WC-10 splits only above 5 min, into 4 min waits (spec:68) vs AC-4.3 (no call over 240 s, spec:210) and the pr-submit row (under 4 min, spec:114); Agent-tool waits that block longer cannot be split and are "left as they are" (spec:65, 24). Effect of a missed heartbeat is UNVERIFIED (CAPS:130, 182). | one threshold; scope WC-10 to Bash/poll waits | Medium | liveness |
| F-08 | MAJOR | Wiegers | `--unattended` with no output dir / flag (cleanup-audit spec:85, index-repo spec:86, init-lite spec:87, load spec:112), and `--unattended --interactive` on adversarial / brainstorm / release-split (spec:83, 84, 89) have no stated behaviour. | refuse or define the default | Medium | clarity |
| F-09 | MAJOR | Hohpe | No nested-invocation rule: troubleshoot to adversarial (INV-B:241), release-split to brainstorm to adversarial (INV-B:119, 121), workflow to reflect (INV-B:271), tdd to /task (INV-B:219), brainstorm to adversarial (INV-A:39). Only tasklist to reflect is specified (spec:122). | one sentence: nested commands inherit `--unattended` and write under a sub-directory | Medium | gate coverage |
| F-10 | MAJOR | Newman | AC-C1 greps `src/superclaude/core` and requires no match (spec:172) while P0 adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to the core contract file (spec:158); E5 records 0 Orca mentions there today (spec:25). SA-2 exempts only "the contract file" (spec:147). | narrow the grep or the exemption | Medium | test consistency |
| F-11 | MAJOR | Nygard | Section 1.4(2) states a command's own question "comes after readiness, so it does not fail worker-start" (spec:44), but Claude's task is passed on the command line (CAPS:47), CAPS:52 only shows an `input_accepted` worker waiting is healthy, and E2 (spec:22) generalises one readiness test to "same tools". Not marked UNVERIFIED. | mark UNVERIFIED; P0 tests it | Medium | evidence strength |
| F-12 | MAJOR | Wiegers | Three "interactive mode may wait" cases are handled differently: business-panel and explain are refused under `--unattended` (spec:102, 108), index says "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (spec:111; INV-A:54, 113). | refuse the interactive example as for the others | Medium | consistency |
| F-13 | MAJOR | Nygard | reflect is "ready today" with `--no-promote` optional (spec:88), but by default it writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and moves the work-unit folder (INV-B:114); cleanup-audit uses a fixed `.claude-audit/` dir (spec:85). WC-11 (spec:69) and WC-9 (spec:67) cover neither. | list both in the rows | Medium | parallel safety |
| F-14 | MINOR | Cockburn | Section 4 git row: "workers make no commits or pushes" (spec:133, citing README:31 which governs this run only) vs D4(a), D3(b), the task and post-release rows (spec:113, 121, 241, 245) that allow authorised worker commits. | reword to "unless authorised" | Low | consistency |
| F-15 | MAJOR | Nygard | tasklist row resolves only the reflect pass-through (spec:122); the HALT on `needs_human_decision` items (INV-B:209) and what reflect's headless rule "skips" (INV-B:109; spec:280) are unresolved though WC-2 says every gate resolves (spec:60). | add the HALT resolution | Medium | gate coverage |
| F-16 | MAJOR | Fowler | roadmap and validate-roadmap "reconcile" command and skill without choosing the winner (spec:118, 124; INV-B:309 says no file decides); AC-3.1 passes for either (spec:204); any choice changes a standalone filename (SA-1, SA-4). | name the side | Medium | build ambiguity |
| F-17 | MINOR | Newman | The contract has no schema version, and "keep their fields" (spec:62) may collide with the four-value status set (spec:262) and the versioned workflow contract (INV-B:272). | add `contract_version` | Low | evolution |
| F-18 | MINOR | Wiegers | WC-9 "calls a paid external run" is undefined (spec:67); research and review-translation use Tavily (INV-B:134, 144) and every fan-out command spends tokens. | enumerate | Low | clarity |
| F-19 | MAJOR | Wiegers | `--monitor 0` and `2` unspecified under `--unattended` (spec:114; INV-B:89); behaviour of ordinals 0 and 2 is UNVERIFIED. | state them | Medium | completeness |
| F-20 | MINOR | Gregory | "Phases 1-3 need no user decision" (spec:154) while D1 decides P1's mechanism (spec:227-230); spec:225 reconciles by "proceed on recommendations". | merge the two sentences | Low | clarity |

Minor (notes):

- F-21 Sentinel: the quoted `--unattended` token case has no parsing rule (spec:51, 228).
- F-22 WC-1 "well inside" the limit is unquantified though the evidence gives 30 s passes and about 45 s fails (spec:59; CAPS:49); the `task` confidence-not-produced case is unstated (spec:121).
- F-23 Section 7 has no live check for WC-12 (spec:70) or for WC-11 beyond save (spec:207); AC-C3 baselines only `tests/skills/` (spec:174) although P0 edits `install_core.py` (spec:158).
- F-24 7.2 step 5 searches the transcript for the string `AskUserQuestion` (spec:184); loaded command text mentions it, so the search can false-positive; test for tool calls.
- F-25 AC-C5's `grep -E '^-[^-]'` (spec:176) skips removed lines that begin with `--` (a removed `---` frontmatter delimiter).
- F-26 `/sc:load`'s missing `--checkpoint` usage entry is in scope (spec:112, P1) while non-goal 8 limits scope to defects that stop worker use (spec:220); agent's frontmatter defect is out.
- F-27 research "pins `--strategy planning`" (spec:116) silently overrides a strategy the brief names.
- F-28 Section 1.2 E3 reads "It has worked before" (spec:23) while section 1.4(1) says the precedent proves only the nested route (spec:43); both are stated, the E3 wording is stronger than the evidence.

Not checked by me and therefore not graded: all claims whose only source is outside the workspace (see coverage). No finding above depends on them except where a line says UNVERIFIED.

Issue question (command Review Loop 3): this run is a worker run with a fixed one-line reply, so the user was not asked whether to open an issue for the follow-up candidates above, and none was created. The coordinator session asks once for this loop.

## Reviser brief

Blocking finding ids: F-01, F-02, F-03. Nothing else is in scope.

Contract for the reviser (Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the candidate's byte size before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS. Use the REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`.

verdict: FAIL
