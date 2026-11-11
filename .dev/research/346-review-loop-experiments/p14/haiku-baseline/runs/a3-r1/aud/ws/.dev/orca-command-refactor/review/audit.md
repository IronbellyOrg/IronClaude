review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines) |
| Candidate SHA-256 | `e9171857b793b520e3e6291ce69b77aaa2e13a035d1f119ba47eb5a42eff8f83` |
| Baseline | not applicable: a first review (neither `--re-review` nor `--baseline` was given) |
| Reviewer model actually used | claude-sonnet-5-5 |
| Review date | 2026-11-10 |
| Labelled scope | whole-document audit of the final spec, first review, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| Brief clauses overridden | none (the brief narrows nothing and widens nothing) |

Citation keys. SPEC = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. README = `.dev/orca-command-refactor/README.md`. INV-A, INV-B, CAPS = `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Every `path:line` below was read in this sandbox. The spec also cites `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` and Orca's installed files, none of which exist in the sandbox: those citations are UNVERIFIED here except where an inventory quotes them (and then only "as quoted").

## What was covered

- Read in full: `command.md`, the review-loop prompts file, README, SPEC (all 286 lines), INV-A (120), INV-B (323), CAPS (188).
- Checked the `INV-A:`, `INV-B:`, `CAPS:` line citations in SPEC sections 1-4, 8-9 and the UNVERIFIED list against the inventory lines (all those checked resolved to the claimed content; sections 5-7 were read for logic, with only the citations that matter to a finding re-checked). Checked the counts: 21 + 22 = 43 (INV-A:3, INV-B:3); 10 ready (SPEC:81-92) + 27 needs-change (SPEC:97-125, counted row by row) + 6 coordinator-only (SPEC:130-137) = 43; phase assignment sums to 35 commands with a phase plus brainstorm and init-lite with none = 37 worker-capable (see the Quantity Flow Diagram).
- Not covered: whether any `src/` line, `CLAUDE.md` line, Orca source line or `EVIDENCE.md` line is correct (not in the sandbox); whether the PR #329 run worked; nothing was run.
- Panel: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture; Whittaker (active in every review). Fixed review order per command.md. `--focus correctness` was not requested, so the State Variable Registry is not produced.

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Guards found: conditional logic in WC-2, WC-3, WC-4, WC-5, WC-6, WC-9, WC-10, in section 2.3 and in the phase rules. Constructed by Nygard, completeness-checked by Crispin's rules, attacked by Whittaker. Classes left out are named in the line under each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `unattended_switch` | SPEC:51,73,146 | Zero/Empty | no `--unattended` | false | today's behaviour unchanged (SA-1) | OK |
| `unattended_switch` | SPEC:159,195 | One/Minimal | `--unattended` on brainstorm or init-lite (no gate, no small fix, SPEC:84,87) | true | P1 says the flag is accepted by every command in 3.1 and 3.2 (SPEC:159); AC-1.1 says these two have no `## Unattended mode` section (SPEC:195); 3.1 lists no change for them | GAP (B-1) |
| `unattended_switch` | SPEC:73,159 | Typical | `--unattended` on analyze after P1 | true | section, contract, no-op gate | OK |
| `unattended_switch` | SPEC:159,195 | Maximum/Overflow | all 37 worker-capable commands (SPEC:159) vs 12 asserted by AC-1.1 (SPEC:195) | true | two counts, no reconciliation | GAP (B-1) |
| `unattended_switch` | SPEC:73,100,160 | Sentinel Value Match | `--unattended` inside quoted prompt text, e.g. `/sc:troubleshoot "login fails with --unattended"` | unspecified | no tokenization rule; user data and control signal collide | GAP (M-10) |
| `unattended_switch` | SPEC:67,73,100,159,160 | Legitimate Edge Case | `/sc:auggie-review <PR> --unattended` after P1, before P2 | true (flag accepted, P1) | gate conversion and "posting off" arrive in P2 only | GAP (B-1) |
| `output_dir` (WC-4) | SPEC:62,73 | Zero/Empty | `--unattended` with no output directory passed | unspecified | contract path undefined | GAP (M-11) |
| `output_dir` | SPEC:62,159 | One/Minimal | `--output <dir>` where the flag names a directory (brainstorm, reflect, workflow) | true | `<dir>/return-contract.yaml` | OK |
| `output_dir` | SPEC:62,87,90,200 | Legitimate Edge Case | `--output <file>` (tdd, init-lite, and the AC-2.2 run) | true | contract placed at `<output-dir>`, which is a file | GAP (B-2) |
| `output_dir` | SPEC:85,86,196 | Sentinel Value Match | commands with a fixed output location and no output flag (cleanup-audit, index-repo) while AC-1.2 passes `--output <dir>` | n/a | no flag exists to pass; contract path not derivable | GAP (B-2) |
| `outcome_map` (WC-5) | SPEC:63 | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| `outcome_map` | SPEC:63,264 | One/Minimal | `partial` | true | `succeeded`, first body sentence says `partial` | OK |
| `outcome_map` | SPEC:63 | Typical | `succeeded` | true | `succeeded` | OK |
| `outcome_map` | SPEC:63,CAPS:89 | Sentinel Value Match | contract `blocked` vs Orca Task status `blocked` | true | mapped to outcome `failed` explicitly | OK |
| `outcome_map` | SPEC:62,263 | Legitimate Edge Case | an existing contract whose `status` uses other values | unspecified | "keep their fields" (SPEC:62) vs "fixed set" (SPEC:263); existing vocabularies never listed | GAP (M-6) |
| `wait_split` (WC-10) | SPEC:68 | Typical | one wait of 2 minutes | false | no split | OK |
| `wait_split` | SPEC:68,114,211 | Legitimate Edge Case | one tool call of 4.5 minutes | false (not over 5) | WC-10 requires nothing; pr-submit row and AC-4.3 require under 4 minutes | GAP (n-1) |
| `wait_split` | SPEC:68,104 | Maximum/Overflow | eval wait of 3600 s | true | split into waits of at most 4 minutes | OK |
| `ask_or_stop` (WC-3) | SPEC:61,60 | Zero/Empty | gate fires, no preamble (plain session) | true | resolve as blocked | OK |
| `ask_or_stop` | SPEC:61,200,209 | Typical | gate fires, preamble present | true | "may" ask, then re-invoke; AC-2.2 and AC-4.1 require outcome `failed` and `blocked` | GAP (M-2) |
| `ask_or_stop` | SPEC:61,CAPS:60 | Maximum/Overflow | coordinator never answers | true | `ask` timeout resumes the same message ID | OK |
| `resume_or_fresh` (WC-6) | SPEC:64,62 | Typical | command without a resume flag, retried | true | "writes each run into a fresh output directory" vs contract at the coordinator-passed directory | GAP (M-3) |
| `resume_or_fresh` | SPEC:64,84 | One/Minimal | command with a resume flag (brainstorm, tdd) | true | resumes | OK |
| `outward_default_off` (WC-9) | SPEC:67,100 | Typical | auggie-review default posting | true | off; `--post-pr` restores | OK |
| `outward_default_off` | SPEC:67,113,114,121 | Legitimate Edge Case | task `commit`/`push`, post-release commit and PR, pr-submit push | true | "command's own explicit flag" named for none of them | GAP (M-4) |

Classes left out: `wait_split` One/Minimal and Sentinel (a wait cannot be one unit or collide with a sentinel); `ask_or_stop` One/Minimal and Sentinel (a single yes/no per ask has no minimal form); `outward_default_off` Zero, One, Maximum and Sentinel (a default is on or off); `resume_or_fresh` Zero, Maximum and Sentinel (no state to count or collide). Each is a one-line reason, not a quota. Gate FR-10 satisfied: no unpopulated cell.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

The classification funnel and the phase plan are a 2-stage count flow, so the heuristic triggers.

```text
[Source: 43 commands = INV-A 21 + INV-B 22]  (INV-A:3, INV-B:3, SPEC:76)
   --> [Stage 1 classify, SPEC:76]  --> 6 coordinator-only (SPEC:130-137)   N != M (43 -> 37)
                                    --> 37 worker-capable = 10 ready (SPEC:81-92) + 27 needs-change (SPEC:97-125)
   --> [Stage 2 phase assignment, SPEC:156-162]
         P1 = 13 (9 from 3.2 incl. load, + 4 small fixes: adversarial, cleanup-audit, index-repo, workflow)
         P2 = 15 (11 from 3.2 + 4 from 3.1: reflect, release-split, tdd, troubleshoot)
         P3 = 4, P4 = 3            => 35 with a phase
         no phase: brainstorm, init-lite => 2        35 + 2 = 37  (conserved)
   --> [Consumer A: AC-1.1 (SPEC:195)  expects 12 commands with an Unattended section in P1]
   --> [Consumer B: P1 scope (SPEC:159) expects the --unattended flag on 37]            <-- MISMATCH (37 vs 12)
   --> [Consumer C: SPEC:79 "Phase 1 adds the contract" to the ready commands]            <-- MISMATCH (4 of 10 get a P1 change)
```

The first two stages conserve counts. The consumers do not: that is finding B-1. FR-19 labels a dimensional mismatch CRITICAL; the grade below follows consequence (the finding names a concrete wrong outcome and a safety-boundary risk).

## === REQUIREMENTS ANALYSIS ===

### B-1 CRITICAL, blocking: the P1 scope for `--unattended` contradicts itself, AC-1.1 and section 2.3
- **Experts**: Wiegers (lead, consistency and traceability), Adzic (the example below), Whittaker (Sequence Attack).
- **Grading check.** An implementer who follows the stated text as written builds, in Phase 1, `--unattended` acceptance and a WC-4 contract "in unattended mode" for every command in sections 3.1 and 3.2 (SPEC:159), including brainstorm, init-lite and `load`; AC-1.1 then asserts that brainstorm, init-lite and `load` have no `## Unattended mode` section (SPEC:195), so the P1 acceptance check cannot pass. X is wrong because two stated texts contradict each other. The same text builds a second wrong outcome: SPEC:73 tells the coordinator to put `--unattended` in every brief "from Phase P1 on", SPEC:159 makes the flag accepted by every command including those whose gates are converted only in P2 (SPEC:160), and WC-9 (SPEC:67) makes outward defaults off only under the converted command. After P1 and before P2, `/sc:auggie-review <PR> --unattended` is accepted and still posts a review to GitHub by default with no prompt (`cmd/auggie-review.md:51-54` as quoted at SPEC:67 and INV-A:38). That is a safety-boundary outcome, and it needs no guess about the implementer.
- **Evidence**: SPEC:51 (the mode is "the only command-side change"), SPEC:73, SPEC:76 ("Every changed command also gains the section"), SPEC:79 ("the worker reports the named file until Phase 1 adds the contract"), SPEC:84 and SPEC:87 (brainstorm and init-lite: small fix "None"), SPEC:159, SPEC:160, SPEC:195, SPEC:112 (`load` exempt, SPEC:62 exception [F-3]). The line SPEC:79 is also wrong for 6 of the 10 ready commands: only adversarial, cleanup-audit, index-repo and workflow get a P1 change (SPEC:83,85,86,92).
- **Example (Adzic)**. Given P1 is merged and a coordinator follows SPEC:73, when it dispatches `/sc:brainstorm ... --unattended --output d/`, then the brainstorm command has no flag handling and no section (SPEC:84, SPEC:195); and when it dispatches `/sc:auggie-review 123 --unattended`, then the review is posted (before: 0 reviews, after: 1), against WC-9.
- **Recommendation**: narrow, do not add. State one rule in one place: the flag and the section exist exactly on the commands whose row names the phase being delivered (the 13 of the P1 row, 12 asserted plus `load` as usage-line only); say that SPEC:73 applies to a command only after its phase has passed its checks; say in SPEC:79 that the contract appears for the ready commands in the phase their row names, and that brainstorm and init-lite keep their current report file with no `--unattended` handling and are briefed without it. Delete "(a no-op where a command has no gate)" and "every command in sections 3.1 and 3.2" from SPEC:159.
- **Priority**: High. **Quality-impact estimate**: Consistency +2 of 10, Testability +1.

### B-2 CRITICAL, blocking: the WC-4 contract location is undefined where the output flag names a file or does not exist
- **Experts**: Wiegers (lead), Cockburn (the coordinator must know the path before dispatch), Whittaker (Sentinel Collision).
- **Grading check.** An implementer who follows the stated text as written builds `<output-dir>/return-contract.yaml` where "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62) and where the coordinator "states the output directory, so the report path is known before dispatch" (SPEC:73). For `/sc:tdd` and `/sc:init-lite` section 3.1 tells the coordinator to pass `--output <file>` (SPEC:87,90; INV-B:222 "TDD file at `--output`"), and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and then requires a contract with `status: blocked` (SPEC:200). The implementer writes `<file>/return-contract.yaml`, which cannot exist beside a file; nothing writes the contract and the AC-2.2 and 7.2 step 4 checks (SPEC:183) have no path to open. For cleanup-audit and index-repo section 3.1 says the output location is fixed and no output flag exists (SPEC:85,86), yet AC-1.2 runs every P1 command with `--output <dir>` (SPEC:196). X is wrong because a stated text and an acceptance criterion cannot both pass.
- **Evidence**: SPEC:62, SPEC:73, SPEC:85-87, SPEC:90, SPEC:183, SPEC:196, SPEC:200; INV-A:42,53,55 (fixed locations); SPEC:261 (the Decisions row says one fixed name `return-contract.yaml`, not where).
- **Recommendation**: narrow WC-4 to one sentence that fixes the location for each output flag shape: when the flag names a file, the contract is written in the same directory under the name `return-contract.yaml`; when a command has no output flag, the brief names the report directory through the one new directory flag that command gains in P1, or the command is briefed without `--unattended` until it has one (this ties to B-1). Make AC-1.2 and AC-2.2 use the same shape.
- **Priority**: High. **Quality-impact estimate**: Testability +2, Completeness +1.

### M-6 Medium: the existing contracts' `status` vocabularies and a schema version are never listed
WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62) and the Decisions table picks a fixed four-value `status` (SPEC:263), but neither inventory records the `status` values of the existing contracts (INV-B:272, INV-A:39,97). If an existing contract uses other values, "keep" and "fixed set" conflict. The contract also has no version field (workflow already names "contract 1.1", INV-B:272). Not blocking: it needs a guess about the existing values. Wiegers/Newman. Priority Medium.

### M-2 Medium: WC-3 makes the coordinator question optional, but AC-2.2 and AC-4.1 require one outcome
WC-3 says the worker "may" ask once (SPEC:61); AC-2.2 requires `worker_done --outcome failed` with `status: blocked` (SPEC:200); AC-4.1 requires `blocked` and `failed` (SPEC:209). A worker that takes the permitted `ask` path fails a gate-trigger check that the spec declares a pass condition. The brief template (SPEC:73) does not say whether the worker may ask. Medium because the coordinator can write "do not ask" in a brief; the spec should say which one the brief template carries. Adzic/Hohpe.

### M-3 Medium: "fresh output directory" (WC-6) conflicts with a contract path that is known before dispatch (WC-4)
WC-6 has a command without a resume flag write "each run into a fresh output directory" (SPEC:64) while WC-4 fixes the path to the directory the coordinator passed (SPEC:62). A command that creates a fresh subdirectory moves the contract; one that does not, overwrites the first attempt. The `ask`-then-re-invoke path in WC-3 hits this on every "fresh dir" row of section 3.2. The text allows either reading; say that the coordinator passes a new directory per attempt. Fowler/Nygard.

### M-4 Medium: WC-9 depends on "the command's own explicit flag", but no flag is named for task, post-release or pr-submit; D4 reaches P2
SPEC:67 turns an outward action on "only through the command's own explicit flag written in the brief". The rows for task (`commit`/`push` "refused unless authorized", SPEC:121), post-release ("explicit pre-tag choice", "unless the brief authorizes them", SPEC:113) and pr-submit (SPEC:114) name no flag, and the source quotes the authorization as a conversation fact ("unless the user pre-authorized them this session", INV-B:79). Separately D4 lists auggie-review `--post-pr` and task `commit`/`push` as affected (SPEC:245), both P2 rows (SPEC:100,121,160), while SPEC:154 says "Phases 1-3 need no user decision" and SPEC:226 says "Phases 0-3 can proceed on the recommendations" (these two sentences differ). Not blocking: an implementer can invent a flag or follow recommendation (a). Wiegers.

### M-5 Medium: several requirements have no acceptance check
Traceability from SPEC:57-70 to SPEC:169-211: WC-3 (the `ask` path) has none; WC-6 (retry does not corrupt the first attempt) has none; WC-12 has none; WC-10 is checked only for pr-submit (AC-4.3, SPEC:211), not for cli-eval (SPEC:104); WC-1 is covered only by 7.2 step 1 (SPEC:180). Wiegers/Crispin rule: a requirement without a check is not verifiable. Priority Medium.

### M-13 Medium: the 7.2 step 2 pass condition can pass on an absent field
Step 2 passes when `observation.agentWait` "is never non-null" (SPEC:181). CAPS:129 says null means Orca looked and found no wait and an absent field means it never looked; an absent field also reads as "never non-null". Say "is present and null at each poll". Step 5 (SPEC:184) partly compensates. Crispin.

### M-10 Medium: `--unattended` has no tokenization rule
The switch is a flag in free-text arguments (SPEC:51,229). A prompt such as `/sc:troubleshoot "login fails when --unattended is set"` contains the string as user data. The spec has no rule that only a standalone token outside quoted content counts. Whittaker (Sentinel Collision Attack).

### M-11 Medium: no rule for `--unattended` without an output directory
SPEC:62 requires the directory the coordinator passed; SPEC:73 makes the brief carry it; no text says what a command does when it is missing (refuse, default, or write nowhere). Whittaker (Zero/Empty Attack). Related to B-2.

## === ARCHITECTURE ANALYSIS ===

The decision itself (SPEC:13-45) is well supported by the inventories: the rejected alternative is excluded by the depth-1 setting (CAPS:97-101), by standalone use (CAPS:147-149) and by the single owner of `worker_done` (CAPS:76,150). The boundary between coordinator, worker session and command is clear in WC-1 to WC-12. The findings below concern gaps in that boundary, not the decision.

### M-7 Medium: section 1.4 item 2 states as fact that a command's own question comes after readiness
SPEC:44 says a command's `AskUserQuestion` "comes after readiness, so it does not fail `worker-start`". CAPS:47 records that for Claude the task is passed on the command line (argv injection), so the command starts as Claude starts, and CAPS:49 and CAPS:52 only cover a wrapper question before Claude and a worker that is already `input_accepted`. Whether an `AskUserQuestion` on the first turn blocks Orca's readiness is not shown anywhere in the sandbox. The consequence is a missing premise, not a wrong build: WC-2 forbids the prompt either way. Mark the statement UNVERIFIED and add it to the UNVERIFIED list. Fowler/Nygard.

### M-8 Medium: how a worker invokes a command is not specified
The worker's first message is an Orca preamble plus the Task block (CAPS:78, CAPS:148, SPEC:50), so a command line inside it does not start the message. The spec says "run the command directly" (SPEC:65, SPEC:194) but not through which mechanism (typed slash command, Skill tool, reading the command file). 15 of the 37 worker-capable commands have no skill (INV-A:70, INV-B:8). The only proven route was an Agent-tool subagent (SPEC:43). Phase 0 would find out, but AC-0.4 does not ask the phase report to record the mechanism. Fowler/Newman.

### M-9 Medium: gates reachable through nested handoffs are not constrained in the ready rows
brainstorm has an optional Wave 4 handoff to `sc-tasklist-protocol` or `task-builder` (INV-A:39); tasklist's Stage 10.5 reaches reflect with `--remediate` (INV-B:46,209). SPEC:84 forbids only `--interactive`, while SPEC:92 forbids the handoff for workflow (`--handoff none`) and SPEC:89 handles release-split's nested prompts. The default value of brainstorm's `--handoff` is not given in either inventory (UNVERIFIED). Hohpe/Whittaker (Sequence Attack).

### M-12 Medium: behaviour when the installed contract file is missing is not defined
Each changed command points to `~/.claude/WORKER-CONTRACT.md` (SPEC:52). On a machine installed before the file existed, the command in unattended mode cannot read the shared rules, and the spec says neither "block with status blocked" nor "use the in-command text". The repo rule on installed primitives asks for the installed path and, where a project copy exists, both (SPEC:150 cites it only for `.claude/` staging). Newman/Nygard.

### M-1 Medium: AC-C1 conflicts with the mentions SA-2 and SA-5 allow in `core/`
AC-C1 greps `src/superclaude/core` for `orca[-ide] orchestration|worktree|terminal|agent` and requires no output (SPEC:172). SA-2 allows one mention of Orca "as an example of a caller's question channel inside the contract file" (SPEC:147), the contract file is in `core/` (SPEC:52), and SA-5 adds an Orca section to `core/HOW-WE-WORK.md` (SPEC:150). A permitted example such as `orca orchestration ask` makes AC-C1 fail in every phase from P0. Medium because the implementer can avoid the literal text. Fowler.

### M-14 Medium: roadmap's internal `sc:save` calls and WC-11
roadmap "writes memory through `sc:save` at every wave" (INV-B:154). WC-11 forbids single-owner memory writes in unattended mode (SPEC:69) and the save row fixes `/sc:save` itself (SPEC:119), but the roadmap row (SPEC:118) does not say its internal save calls use the per-session keys. Hohpe/Fowler.

## Whittaker adversarial analysis (all five methodologies)

- **Zero/Empty Attack**: I can break this specification by passing `--unattended` with no output directory. The invariant at SPEC:62 (the contract is written on every outcome) fails when no directory is passed. Concrete attack: `/sc:analyze x --unattended` => no `<output-dir>`; before: no files, after: the spec requires a contract, but does not say where (M-11). Severity MAJOR; graded Medium.
- **Divergence Attack**: I can break this specification at the boundary between WC-10 and AC-4.3. The invariant at SPEC:68 fails when one tool call lasts 4.5 minutes: WC-10 requires nothing, SPEC:114 and SPEC:211 require under 4 minutes. MINOR (n-1).
- **Sentinel Collision Attack**: I can break this specification by writing `--output out/TDD.md`. The invariant at SPEC:62 (contract at `<output-dir>/return-contract.yaml`) fails when the value is a file: `out/TDD.md/return-contract.yaml` cannot be created (B-2). A second collision: `--unattended` inside quoted user text (M-10). A third, checked and OK: contract `blocked` against Orca Task `blocked` (CAPS:89) is resolved by the explicit mapping to `failed` (SPEC:63).
- **Sequence Attack**: I can break this specification by dispatching in the order the spec itself allows. The invariant at SPEC:73 and SPEC:159 (briefs carry `--unattended` from P1; outward defaults are off under it) fails when auggie-review runs after P1 and before P2: the review is posted (B-1). Also WC-3: the command has already written a `blocked` contract when the worker asks and re-invokes (M-3).
- **Accumulation Attack**: I can break this specification by retrying a task whose worker ends `blocked`. The invariant at SPEC:63 (blocked maps to `failed`) fails to bound retries: Orca's circuit breaker counts failed `worker-start` attempts, not a worker's own `failed` report (CAPS:80), so a coordinator can retry a blocked Task without limit. The spec states no retry cap for blocked outcomes. MINOR (n-2).

## Expert consensus and disagreements

- Consensus (all experts): the decision, the rejection of the alternative, the per-command table and the phase order are well grounded in the inventories; counts conserve (see the diagram); the citation discipline to INV-A, INV-B and CAPS held in every line I could check.
- Consensus on blocking items: B-1 and B-2 are both about one idea, "where the unattended report is and who has the flag", written in different places that disagree.
- Disagreement (recorded, not resolved): Wiegers would grade M-6 and M-4 as blocking because they leave requirements undefined; Adzic and Fowler hold them at Medium because the spec text does not itself cause a wrong build and the first-review prompt asks for a sentence with no further assumption. The prompt rule decides: Medium.

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
  consistency: 5
critical_issues:
  - {category: requirements, severity: CRITICAL, expert: wiegers, issue: "B-1 P1 scope for --unattended contradicts AC-1.1, section 2.3 and the phase order", recommendation: "narrow to the commands of each delivered phase"}
  - {category: requirements, severity: CRITICAL, expert: wiegers, issue: "B-2 WC-4 contract location undefined for file-valued or missing output flags", recommendation: "one sentence fixing the location per flag shape"}
expert_consensus:
  - decision and rejection of the alternative are well supported
  - counts conserve across classification and phases
  - two internal contradictions block a PASS
improvement_roadmap:
  immediate: [B-1, B-2]
  short_term: [M-2, M-3, M-4, M-5, M-6, M-11]
  long_term: [M-1, M-7, M-8, M-9, M-10, M-12, M-13, M-14]
adversarial_analysis: see the Whittaker section above
```

## follow-up candidates (Medium and minor; never trigger a revision, never in the Reviser brief)

Issue offer: the session that ran this review is a non-interactive worker whose only reply is the `DONE` line, so the user was not asked whether to open an issue for these and none was created. The coordinator asks the user once for this loop.

Medium (warnings): M-1 (AC-C1 vs SA-2/SA-5), M-2 (optional `ask` vs mandatory outcome), M-3 (fresh dir vs known contract path), M-4 (WC-9 flags undefined; D4 reaches P2), M-5 (requirements without a check), M-6 (existing contract vocabularies and version), M-7 (unsupported claim in 1.4 item 2), M-8 (invocation mechanism), M-9 (nested handoff gates), M-10 (`--unattended` inside quoted text), M-11 (no output directory), M-12 (installed contract file missing), M-13 (`agentWait` absent reads as pass), M-14 (roadmap `sc:save`).

Minor (notes):
- n-1: the 4 to 5 minute gap between WC-10 (SPEC:68) and the 4-minute checks (SPEC:114,211).
- n-2: no retry cap for repeated `blocked` outcomes (see Accumulation Attack; CAPS:80).
- n-3: AC-2.4 counts reviews and comments with `--jq length` (SPEC:202); without `--paginate` the count stops at the first page.
- n-4: 7.2 step 5 searches the transcript for the string `AskUserQuestion` (SPEC:184); the command's own text read by the model can contain it. Say "a tool call".
- n-5: SPEC:150 says the routing guide has "two mirrored copies"; the repo rule as shown in the session's project instructions names one byte-for-byte copy and a level-table copy, so an Orca section could be pasted into the wrong file (UNVERIFIED: `CLAUDE.md` is not a sandbox file).
- n-6: `worker_done` "exactly once" (SPEC:63) names no recovery for a lost response, although Orca's mutations accept `--retry-request` (CAPS:117).
- n-7: the tasklist row keeps `--remediate` and relies on the headless rule (SPEC:122) where INV-B:215 recommended dropping it; no Decisions row records the departure.
- n-8: D5 option (b) calls R1 a "protection" (SPEC:253); R1 is a refusal reason (SPEC:33).
- n-9: the claim that 43 commands is the full set (SPEC:76) cannot be checked in the sandbox (UNVERIFIED); the installed-skill list this session saw also names `/sc:graph`, `/sc:impact` and `/sc:issue`, which neither inventory covers. That list is not the worktree's `src/superclaude/commands/`, so it proves nothing, but the coordinator can run `ls` there once.
- n-10: SPEC:286 records an earlier fresh-context citation check (about 340 citations, 9 defects fixed); this review did not repeat it for `src/` citations.

## Reviser brief

Blocking finding ids: B-1, B-2.

Restated rules for the reviser (the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
