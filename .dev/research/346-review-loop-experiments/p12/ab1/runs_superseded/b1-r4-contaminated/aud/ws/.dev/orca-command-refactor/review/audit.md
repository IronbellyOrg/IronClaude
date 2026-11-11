review: 1 of 3

# Spec-panel critique: whole-document audit of the Orca worker-contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `a86859da35221feef00405e0c095e0a2d20bb75210af188b81511d9626e0e50d`
- re-review inputs: none given (no `--re-review`, no `--baseline`), so this is a first review of the full document
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`, labelled whole-document audit
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- brief clauses overridden: none
- citation rule: every claim cites `path:line`. `SPEC:N` = the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. A citation to a file that is not in the workspace (for example `EVIDENCE.md`, `CLAUDE.md`, `install_core.py`, `HOW-WE-WORK.md`, any `sk/` or `cmd/` line) is checked only as far as an inventory quotes it. Anything beyond that is marked UNVERIFIED.

## Coverage

Covered: the whole candidate, SPEC:1-285 (sections 1-9, Decisions, UNVERIFIED items). I read the README (binding context) and all three inventories in full and checked these against them:
- the 10 / 27 / 6 split, and the per-phase counts: P1 9, P2 11 plus 4 ready, P3 4, P4 3 (27 rows in SPEC:97-125, 10 in SPEC:82-92)
- every `CAPS:N` and `INV-x:N` cite in sections 1, 2, 4, 5 and 7: all landed on the line that supports the claim
- each section 3 row against the inventory row it cites

Not covered: `src/`, `~/.claude`, Orca itself and `EVIDENCE.md`, none of which is in the sandbox. The "re-read 11 locations" and "340 citations" statements (SPEC:11, SPEC:285) are the spec's own claims and I could not repeat them.

## Panel and method

Review order (command Expert Review Sequence): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus `requirements` (Wiegers lead, Adzic, Cockburn) and `architecture` (Fowler lead, Newman, Hohpe, Nygard). Whittaker is active on every panel.

Grading follows Review Loop bullet 2 and the Grading check: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption. Otherwise it is Medium, whatever its label.

## Finding table (ids used by the verdict)

| id | Severity label | Graded | Bucket | Expert |
|---|---|---|---|---|
| F-01 | MAJOR | **blocking** | requirements | Wiegers |
| F-02 | MAJOR | Medium | requirements | Wiegers, Fowler |
| F-03 | MAJOR | Medium | requirements | Whittaker |
| F-04 | MAJOR | Medium | architecture | Nygard |
| F-05 | MAJOR | Medium | requirements | Cockburn, Whittaker |
| F-06 | MAJOR | Medium | requirements | Wiegers, Newman |
| F-07 | MAJOR | Medium | architecture | Fowler, Nygard |
| F-08 | MINOR | Medium | requirements | Crispin |
| F-09 | MINOR | Medium | requirements | Crispin |
| F-10 | MINOR | Medium | requirements | Crispin |
| F-11 | MINOR | Medium | requirements | Wiegers |
| F-12 | MAJOR | Medium | architecture | Nygard |
| F-13 | MINOR | Medium | architecture | Hightower |
| F-14 | MAJOR | Medium | architecture | Newman, Hohpe |
| M-1 to M-8 | MINOR | minor | various | various |

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking): AC-1.1 requires a contract section on three P1 commands whose own rows say they get none
- Expert: Wiegers (testability, internal consistency). Priority: High. Quality impact: Consistency -2, Testability -1.
- Stated texts that contradict:
  - SPEC:195, AC-1.1: the test asserts that "every command in sections 3.1-3.2 whose phase is P1 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - SPEC:112, the `load` row, which has phase P1: Report (WC-4) is "none (see note)", Resume "n/a", and "use it as a step inside another worker's brief, not as its own Task". SPEC:265 (Decisions) adds: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - SPEC:86, the `index-repo` row, phase P1: the only change is "State the output location (P1)". No contract is added, although SPEC:62 (WC-4) says every unattended run writes one.
  - SPEC:85, the `cleanup-audit` row, phase P1: the only change is "Name the `--pass all` final report". It also adds no contract.
  - SPEC:159 (P1 scope) lists `load (usage line only)` and "fixes to ... index-repo" as P1 work, so these three do fall inside AC-1.1's quantifier.
- Grading sentence: An implementer who follows AC-1.1 as written gives `load`, `index-repo` and `cleanup-audit` an Unattended section that names `return-contract.yaml`. That contradicts the `load` row and the Decisions row, which say no report file is added, and gives `index-repo` and `cleanup-audit` a contract the rows never specify. An implementer who follows the rows instead fails AC-1.1. No further assumption is needed, because the phase labels are in the spec. This is "two stated texts that contradict each other" and "a stated text that an acceptance criterion cannot pass" (prompt file :31).
- Recommendation: narrow AC-1.1 to the P1 commands that write a contract (SPEC:99-111 minus `load`, plus adversarial and workflow). Alternatively, state a contract for `index-repo` and `cleanup-audit` in their rows and drop `load` from the AC-1.1 quantifier.

### F-02 (Medium): two ready commands never get `--unattended` or the WC-4 contract, yet the brief must pass both
- Expert: Wiegers, Fowler. Priority: Medium.
- SPEC:73 (section 2.3): the brief states "the exact command line including `--unattended`" for each Task. SPEC:79: ready commands report "the named file until Phase 1 adds the contract". But `brainstorm` (SPEC:84) and `init-lite` (SPEC:87) have "Small fix: None" and no phase, and appear in no P1 to P4 scope (SPEC:159-162). So `--unattended` is never added to them and the WC-4 fields `status`, `command` and `artifacts` are never added. `init-lite` writes `context-audit.md`, not a `return-contract.yaml`.
- Consequence: 7.2 step 4 (SPEC:183) would fail for these two. What `--unattended` does on a command that does not define it is not stated, so the grade rests on a reading choice, hence Medium.
- Recommendation: give both a phase, or say in 3.1 that the brief omits `--unattended` for them.

### F-03 (Medium): behavior of `--unattended` with no output flag is not stated
- Expert: Whittaker (Zero/Empty attack). Priority: Medium.
- Attack: invoke `/sc:analyze src/x.py --unattended` with no `--output`. WC-4 (SPEC:62) defines `<output-dir>` as "the directory the coordinator passed", so there is no directory and nowhere to write a contract, including for the "stops before any other output exists" case. SPEC:73 says the brief carries the directory, but no rule says what the command does when the brief omits it (refuse and write nothing, or default location).
- Recommendation: add one sentence to WC-4 fixing this case.

### F-05 (Medium): WC-3 (ask the coordinator), WC-5 (blocked maps to failed) and the P2 live test (AC-2.2) disagree on who chooses
- Expert: Cockburn (actor and goal), Whittaker (Divergence attack). Priority: Medium.
- WC-3 (SPEC:61) lets the worker "instead ask the coordinator once ... then re-invoke the command with the answer as a flag". WC-5 (SPEC:63) sends `blocked` to `--outcome failed`. AC-2.2 (SPEC:200) requires `worker_done --outcome failed` on a gate hit. When both paths are open, the spec does not say which applies, so a worker that asks (WC-3) fails AC-2.2.
- Divergence at the `/sc:implement` Ruling gate (SPEC:109, SPEC:233-236): WC-3 re-invokes "with the answer as a flag", but a Ruling is not a flag. Under D2(a) the coordinator's reply "is not acceptance" (`qa.md:238` via INV-A:66). WC-3 does not carve this gate out.
- Recommendation: say that the brief chooses ask-or-stop per Task, and exempt the Ruling from WC-3 under D2(a).

### F-06 (Medium): `partial` is undefined, and the fixed status vocabulary may clash with contracts that already exist
- Expert: Wiegers, Newman. Priority: Medium.
- WC-5 (SPEC:63) maps `partial` to `--outcome succeeded`, which settles the Task as completed and unblocks its dependents (CAPS:77). Nothing in WC-4 (SPEC:62) says when a command may report `partial` rather than `failed`. A command that finishes half its work and reports `partial` hands incomplete input to dependent Tasks.
- SPEC:62 says commands that already write a contract "keep their fields" and also fixes `status` to four values. The existing workflow contract has `status` including `failed` (INV-B:272). Whether its other values fall inside the four is not checked and nothing in the inventories states them (UNVERIFIED).
- Recommendation: define `partial` in one line (a usable deliverable exists), and add a check that existing `status` values map onto the four.

### F-08 (Medium): the common check for "no Orca calls" and the permission to mention Orca in core files disagree
- Expert: Crispin. Priority: Low.
- SA-2 (SPEC:147) allows a mention of Orca "inside the contract file". P0 (SPEC:158) adds that contract file and an "Orca section" to `HOW-WE-WORK.md`, both under `src/superclaude/core`. AC-C1 (SPEC:172) greps `src/superclaude/core` and excludes only `ccsession-tag`. Whether P0 fails depends on whether the new text spells `orca orchestration ...` (as section 7.2 itself does), which the spec does not say.
- Recommendation: exempt `WORKER-CONTRACT.md` and the new routing section in AC-C1, or forbid the literal command names there.

### F-09 (Medium): AC-C5 (no removed lines) versus "new flags" on existing Usage lines
- Expert: Crispin. Priority: Low.
- SA-4 (SPEC:149) calls the Phase 1-3 edits additive and allows "new flags"; AC-C5 (SPEC:176) fails on any `^-` diff line. Adding `--unattended` to an existing `## Usage` line removes and re-adds that line. Whether the flag is documented only in the new section or also in Usage is not stated.
- Recommendation: say where the flag is documented.

### F-10 (Medium): AC-0.4 contradicts itself on which live-check steps apply
- Expert: Crispin. Priority: Low.
- SPEC:194 says "steps 1-3 and 5-7 pass; steps 3 and 4 use the command's existing report file". Step 3 is in both groups. Step 4 (SPEC:183) parses YAML and asserts `d['status']` and `d['command']`, which cannot hold for troubleshoot's markdown `REPORT.md` (INV-B:242). So the P0 pass condition for that command is unclear.
- Recommendation: state that step 4 is skipped in P0 for commands whose existing report is not a contract.

### F-11 (Medium): auggie-review row names a `--post-pr` flag that does not exist today
- Expert: Wiegers. Priority: Low.
- SPEC:100 and WC-9 (SPEC:67) say posting "returns only with an explicit `--post-pr` in the brief". The command today has only `--no-post-pr`, with posting on by default (INV-A:38, citing `cmd/auggie-review.md:51-52`). The flag is new and not marked new. Precedence between `--unattended` (implies off) and an explicit `--post-pr` is stated only for the second, not for `--no-post-pr` plus `--post-pr`.
- Recommendation: mark it as a new flag and state its precedence.

## === ARCHITECTURE ANALYSIS ===

Assessment (Fowler, Hohpe, Cockburn): the core decision is well bounded. Orca owns planning, Tasks and lifecycle messages; each command is a unit of work with a pull-based report file (a document message the coordinator opens, SPEC:62, CAPS:79). The rejected alternative has five reasons that each cite a verified capability (SPEC:31-37, checked against CAPS:97-103, 145-150). Evidence gaps are stated honestly (SPEC:41-45), and Phase 0 tests the decision before anything depends on it (SPEC:158). No finding below disputes the decision.

### F-04 (Medium): a retry worker gets the same output directory
- Expert: Nygard. Priority: Medium.
- WC-6 (SPEC:64) says a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean". The command cannot create a fresh directory when the brief names it, and WC-4 and SPEC:73 make the coordinator name it. A `--retry-of` worker (CAPS:116) started from the same Task brief gets the same `<output-dir>`, so it overwrites the first attempt's contract and artifacts. This is the case WC-6 exists to prevent.
- Recommendation: SPEC:73 should say a retry brief carries a new output directory for "fresh dir" commands.

### F-07 (Medium): the `/sc:tasklist` row asserts a nesting result the inventory marks unverified, and leaves one halt unresolved
- Expert: Fowler, Nygard. Priority: Medium.
- SPEC:122 states that tasklist's reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-A:14 states only the general limit ("up to three layers below the main conversation"). INV-B:210 says the same chain is subagent-to-agent nesting and "UNVERIFIED whether nested spawning works". INV-B:215 recommends running the reflect fan-out at the worker's top level. Tier 2 reflect also fans out to reviewers and an adversarial merge (INV-B:111), so whether the chain stays inside three layers is not shown.
- The row also departs from the inventory recommendation ("drop `--remediate` in 10.5", INV-B:215) by passing `--unattended` instead. The reason is not recorded in Decisions (SPEC:268 says verdicts were kept).
- Stage 10.5 says `needs_human_decision` items HALT (INV-B:209). The row never says how that halt resolves, which leaves a WC-2 gate open.
- Recommendation: mark the nesting claim UNVERIFIED, and resolve the halt as blocked.

### F-12 (Medium): reflect writes a tracked shared file and moves folders by default, which WC-9 and WC-11 do not cover
- Expert: Nygard. Priority: Medium.
- INV-B:114: reflect writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and, by default in UC-2, moves the validated work-unit folder (Wave 7). SPEC:88 handles only the move, through `--no-promote`. Two parallel reflect workers on the same slug write the same tracked file, which WC-11 (SPEC:69) forbids but no row addresses.
- Recommendation: add the file to the reflect row.

### F-13 (Medium): the pr-submit wait reading contradicts the inventory it cites
- Expert: Hightower. Priority: Low.
- INV-B:95 says the loop "waits up to `--timeout` 600 s per wait over several rounds", and INV-B:299 files this under "Heartbeats during long attended waits". WC-10 (SPEC:68) and SPEC:114 re-read `cmd/pr-submit.md:49` as a cumulative budget over poll-then-sleep iterations, citing `SKILL.md:46-64`. That line range is not in the spec's own list of re-read locations (SPEC:11) and not quoted in any inventory (UNVERIFIED). Item 12 (SPEC:283) admits the poll runtime is unknown.
- Recommendation: keep the WC-10 requirement, but present the iteration reading as UNVERIFIED.

### F-14 (Medium): the shared contract schema has no version or correlation field
- Expert: Newman, Hohpe. Priority: Low.
- WC-4 (SPEC:62) lists `status`, `command`, `report_path`, `artifacts`, `blocked_question`. The existing workflow contract is versioned ("contract 1.1", INV-B:272), so five commands carry their own contract versions. A new shared schema with no `contract_version` cannot evolve safely, and there is no field tying a file to its Task or Dispatch. The coordinator's per-Task directory is the only correlation (SPEC:73), which works only while F-04 is fixed.
- Recommendation: add `contract_version`.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when `--unattended` is given with no output directory. Concrete attack: before = brief `/sc:build --unattended`, no flags; after = no `<output-dir>`, no contract, `worker_done` has no `--report-path` (CAPS:72-74), WC-5 sends `--outcome failed` ("no report exists"). Graded Medium: F-03.

I can break this specification by **Sequence Attack**. The invariant at **WC-6 (SPEC:64)** fails when a worker is retried with the original brief. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: failed` and partial artifacts; `worker-start --retry-of` re-runs the same command with the same `<dir>`; attempt 2 overwrites both while attempt 1's Dispatch is still readable. Graded Medium: F-04.

I can break this specification by **Divergence Attack**. The invariants at **WC-3 and WC-5 (SPEC:61, SPEC:63)** both apply when a gate resolves as blocked and a preamble exists. Concrete attack: a `/sc:tdd "auth"` worker hits the bare-topic gate (SPEC:90); WC-3 says it may ask, AC-2.2 (SPEC:200) expects `failed` plus `status: blocked` with no `ask`; both are valid under the text. Graded Medium: F-05.

I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4's four-value `status` (SPEC:62)** fails when an existing contract uses a value outside the set. Concrete attack: a command that already writes `status: completed` keeps its fields ("keep their fields"), and WC-5 matches no rule for it, so the outcome falls to the "no report exists" branch only if the file is not parsed. Graded Medium: F-06. The sandbox has no evidence of the existing values, so this is stated as a risk, not a fact.

I can break this specification by **Accumulation Attack**. The invariant at **WC-3 "ask the coordinator once" (SPEC:61)** fails on a command with several gates. Concrete attack: `/sc:review-translation` (Phase 1 and Phase 7 gates, SPEC:117) asks once at Phase 1; the Phase 7 gate arrives and "once" is read per run, so the second gate has no stated resolution. Graded minor, because the per-gate defaults in each row (SPEC:117, "Phase 7 defaults to skip") already resolve it for that command.

## Guard Condition Boundary Table

Guards found: readiness limit, `--unattended` switch, wait size, outcome mapping, nesting depth, confidence threshold, ask count, `--monitor` ordinal. Classes left out are named in the one-line notes below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness-limit | WC-1 SPEC:59 | Zero/Empty | no startup prompt | pass | worker reaches `input_accepted` (CAPS:49) | OK |
| readiness-limit | WC-1 SPEC:59 | Typical | 30 s fallback | pass | start succeeds in 34 s (CAPS:49) | OK |
| readiness-limit | WC-1 SPEC:59 | Maximum/Overflow | fallback above about 45 s | fail | start fails at `agent_readiness` (CAPS:49) | OK |
| `--unattended` present | WC-2 SPEC:60 | Zero/Empty | flag with no output flag | true | not specified | GAP (F-03, Medium) |
| `--unattended` present | WC-2/WC-4 SPEC:60,62 | Typical | flag plus `--output <dir>` | true | gates resolve per section 3, contract written | OK |
| `--unattended` present | SPEC:73, 84, 87 | Legitimate Edge Case | command with no change (brainstorm, init-lite) | true | not specified | GAP (F-02, Medium) |
| `--unattended` absent | SA-1 SPEC:146 | Typical | plain session | false | today's behavior | OK |
| `--unattended` token | D1 SPEC:228 | Sentinel Value Match | the token appears inside quoted task text | unclear | not specified | GAP (M-4, minor) |
| wait-size | WC-10 SPEC:68 | One/Minimal | 1 s poll | pass | heartbeat can interleave | OK |
| wait-size | WC-10 SPEC:68 | Maximum/Overflow | single call over 5 min | split into at most 4 min | stated | OK |
| wait-size | WC-10 SPEC:68, AC-4.3 SPEC:210 | Legitimate Edge Case | single call of 4 to 5 min | no split required, but AC-4.3 fails above 240 s | thresholds differ | GAP (M-8, minor) |
| outcome-mapping | WC-5 SPEC:63 | Typical | `succeeded` | to `succeeded` | stated | OK |
| outcome-mapping | WC-5 SPEC:63 | Legitimate Edge Case | `partial` | to `succeeded` | meaning of `partial` not defined | GAP (F-06, Medium) |
| outcome-mapping | WC-5 SPEC:63 | Zero/Empty | no report file | to `failed` | stated | OK |
| outcome-mapping | WC-5 SPEC:63 | Sentinel Value Match | existing `status` value outside the four | unclear | not specified | GAP (F-06, Medium) |
| nesting-depth | WC-8 SPEC:66 | Maximum/Overflow | worker calls `worker-start` | refused (depth 1) | stated (CAPS:97-99) | OK |
| nesting-depth | D5 SPEC:249-253 | Legitimate Edge Case | depth raised to 2 | still forbidden by WC-8 | stated | OK |
| confidence <0.70 | task row SPEC:121 | Typical | 0.50 | blocked | stated | OK |
| confidence <0.70 | task row SPEC:121 | Legitimate Edge Case | exactly 0.70 | not below, proceeds | follows from "below 0.70" | OK |
| ask once | WC-3 SPEC:61 | Maximum/Overflow | second gate in one run | unclear | per-row defaults cover the known cases | GAP (minor, see Accumulation attack) |
| `--monitor` ordinal | pr-submit SPEC:114 | Typical | 1 | refused | stated | OK |
| `--monitor` ordinal | pr-submit SPEC:114 | Zero/Empty | 0 | unclear | not specified | GAP (minor; P4 and D3(a) make pr-submit coordinator-side) |

Classes left out: "One/Minimal" and "Maximum" for the readiness limit (a lower bound cannot fail; the upper bound is the 45 s row) and "Sentinel" for the nesting guard (a depth value has no reserved meaning here). Every GAP in the table is graded Medium or minor: none names a concrete wrong outcome without a guess about the implementer's reading, so none blocks (Review Loop bullet 2).

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler leads, Whittaker attacks)

Triggered by the classification funnel of section 3 into the phase plan of section 6.

```text
[cmd/ inventory: 43 commands]
   --> [Verdict split]: 10 ready / 27 needs-change / 6 coordinator-only   (10+27+6 = 43, conserved)
          |
          +--> [10 ready] --> phase assignment: P1 x4 (adversarial, cleanup-audit, index-repo, workflow)
          |                                     P2 x4 (reflect, release-split, tdd, troubleshoot)
          |                                     none x2 (brainstorm, init-lite)        <-- 8 of 10, MISMATCH
          |        consumers: section 2.3 / WC-4 expect 10; AC-1.1 expects the 4 P1
          +--> [27 needs-change] --> P1 x9, P2 x11, P3 x4, P4 x3   (27, conserved)
          |        consumer: AC-1.1 takes the 9 P1 plus 4 ready P1 = 13; load is among the 9 but has no contract   <-- MISMATCH (F-01)
          +--> [6 coordinator-only] --> no phase, no --unattended (SPEC:128)
```

The two mismatches are F-02 and F-01. Both are graded by consequence (F-01 blocking, F-02 Medium) rather than by the command's FR-19 label.

## Minor notes

- M-1: README:31 ("No git commits, pushes...") is a rule for this run's workers. WC-9 (SPEC:67) and section 4 on `/sc:git` (SPEC:133) cite it as general policy.
- M-2: Citations I could not check against any file in the sandbox, so UNVERIFIED: `CLAUDE.md:16,50,72-83,157,334,408`, `install_core.py:4,13-24,33`, `pyproject.toml:38`, `Makefile:68-74`, `HOW-WE-WORK.md:22,171,249,254`, `core/CLAUDE.md:65`, `EVIDENCE.md:35,39,45,56` (quoted at CAPS:49 only), `.dev/codegraph-migration/orchestration/README.md:31,33,42`, and every `sk/` and `cmd/` line the inventories quote but this review did not re-read.
- M-3: D5(b) (SPEC:252) says raising depth would "break R1's protection against runaway fan-out". R1 (SPEC:33) is a reason, not a protection, and its own text marks the enforcement UNVERIFIED.
- M-4: D1(a) (SPEC:228) says the flag "cannot misfire on a person". The spec does not say how `--unattended` inside quoted task text is treated.
- M-5: 7.2 step 5 (SPEC:184) searches the transcript for `AskUserQuestion`; loaded command text contains that word as prose, so the search needs to target tool calls.
- M-6: `/sc:pr-submit` is counted among the 27 changes although D3(a), the recommended option, never dispatches it (SPEC:114, SPEC:240).
- M-7: 7.2 step 2 (SPEC:181) requires polling "at least once per 5 minutes", a condition no run records, so it cannot be checked afterward.
- M-8: WC-10 uses 5 minutes as the trigger and 4 minutes as the target (SPEC:68, SPEC:266); the decision row justifies 4 but AC-4.3 enforces 240 s only for pr-submit.

## Quality assessment (0-10)

Clarity 8, Completeness 7, Testability 7, Consistency 6. Strengths: honest evidence gaps (SPEC:41-45), a rejected alternative with verifiable reasons, per-command rows traceable to inventory lines, and acceptance checks written as commands.

## Follow-up candidates

Medium (warnings, none triggers a revision): F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14.
Minor: M-1 to M-8.

Not asked: the session that ran this review would ask the user once whether to open an issue for these (Review Loop bullet 3). This sandbox run has no user channel, so the list is only recorded and no issue was created.

## Reviser brief

Blocking finding ids: F-01.

Restated from the command's Review Loop bullet 6: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings alone.

F-01 names: AC-1.1 at SPEC:195, the `load` row at SPEC:112 and the Decisions row at SPEC:265, the `index-repo` row at SPEC:86, the `cleanup-audit` row at SPEC:85, and the P1 scope line at SPEC:159. The smallest repair narrows the AC-1.1 quantifier so it no longer covers P1 commands that the spec says get no contract.

verdict: FAIL
