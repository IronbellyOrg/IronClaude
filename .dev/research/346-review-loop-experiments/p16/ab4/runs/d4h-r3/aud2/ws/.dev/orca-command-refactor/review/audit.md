review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

Whole-document audit of the final spec: a first review of the whole document (labelled). Mode `critique`, focus `requirements,architecture`, format standard (prose and tables). Reviewed per the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing).

## Header

| Item | Value |
|---|---|
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines) |
| candidate sha256 | `150cd2160e83032be24b36d6510052c36e52b128ef009a46dab2f911fab14ca3` |
| baseline | none given (first review; `--re-review` and `--baseline` absent; `baseline: missing` is not applicable to a first review) |
| reviewer model | claude-sonnet-5-5 |
| README read first | `.dev/orca-command-refactor/README.md` (binding shared context) |
| evidence I could check | `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B), `inventory/orca-capabilities.md` (CAPS). Every other cited path is UNVERIFIED (listed at the end). |
| brief clauses overridden | none |

Citation shorthand in this report: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the three inventory files; `README:N` = line N of `.dev/orca-command-refactor/README.md`.

## Coverage statement

Covered: the whole candidate (sections 1 to 9, Decisions, UNVERIFIED items). Cross-checked against the three inventories: the 43-command partition (10 + 27 + 6; per inventory 5+13+3 = 21 and 5+14+3 = 22, both sums hold), the phase assignment of each section 3.2 row against the section 6 command lists (P1 9, P2 11 + 4 from 3.1, P3 4, P4 3: counts hold), every `CAPS:` and `INV-A/INV-B:` line cited in sections 1, 2, 3.1 (spot rows), 4 and the UNVERIFIED list (all found as cited, details below), and the acceptance checks in section 7 against the requirements they test. Not covered: any citation to a file outside the three inventories and the README (UNVERIFIED, listed at the end); the Orca guide text itself (only the inventory's quotations of it).

## Panel and method

Review sequence followed command order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Findings below are grouped by analysis bucket. Each blocking finding carries the sentence required by the Grading check.

Grading used: CRITICAL and blocking findings need a sentence that holds with no further assumption (two stated texts that contradict each other, or an acceptance criterion that cannot pass). Anything that needs a guess about which of two allowed readings an implementer picks, or that is a requirement the document never states, is Medium and sits under `follow-up candidates`.

## Findings table (all ids)

| id | severity | grade | bucket | expert | one line |
|---|---|---|---|---|---|
| F-01 | MAJOR | blocking | requirements | Wiegers / Crispin | AC-1.1 and the P1 scope sentence require all 37 dispatchable commands to change in P1; the phase column and P1 command list put 28 of them in P2 to P4 |
| F-02 | MAJOR | blocking | requirements | Wiegers / Crispin | `/sc:load` is "changed" and "P1" but has no contract and no `## Unattended mode` section by the spec's own text; AC-1.1 and AC-1.2 require both |
| F-03 | MAJOR | Medium | architecture | Fowler / Whittaker | file-valued `--output` commands (`tdd`, `init-lite`) write a sibling `return-contract.yaml` that two workers in one directory overwrite, against WC-11 |
| F-04 | MAJOR | Medium | architecture | Fowler | AC-C1 forbids `orca orchestration ...` text in `src/superclaude/core`, but P0 adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md`, both in `core/` |
| F-05 | MAJOR | Medium | architecture | Hohpe / Whittaker | no rule says whether `--unattended` and the contract file propagate into a command's nested command invocations |
| F-06 | MAJOR | Medium | requirements | Wiegers | WC-6 "fresh output directory" and WC-4 "path known before dispatch" are not reconciled, and section 2.3 never tells the coordinator to pass a new directory on retry |
| F-07 | MAJOR | Medium | requirements | Wiegers / Adzic | WC-4's fixed four-value `status` set versus "keep their fields" for existing contracts; AC step 4 asserts the set |
| F-08 | MAJOR | Medium | requirements | Nygard / Wiegers | WC-9 "turns on only through the command's own explicit flag" has no flag for several outward actions (auggie-review `--post-pr`, task `commit`/`push`, post-release commit/PR) |
| F-09 | MAJOR | Medium | architecture | Fowler / Nygard | reflect row: `--unattended` makes `--remediate` "follow the headless auto-accept rule"; tasklist Stage 10.5 then auto-accepts remediation inside N subagents; the inventory recommended dropping `--remediate` |
| F-10 | MINOR | Medium | requirements | Crispin | AC-2.2 expects `worker_done --outcome failed` for blocked gates, but WC-3 lets the worker `ask` instead |
| F-11 | MINOR | Medium | requirements | Wiegers | `/sc:troubleshoot` brief carries no output flag, so WC-4's "known before dispatch" report path is not met |
| F-12 | MINOR | minor | requirements | Wiegers | SA-3 and WC-4 differ on when the contract is written (`--unattended` only versus also on the new output flag) |
| F-13 | MINOR | minor | requirements | Crispin | WC-10 splits waits above 5 minutes into 4-minute waits; AC-4.3 fails any single call above 240 s |
| F-14 | MINOR | minor | architecture | Gregory | section 6 says phases 1-3 need no user decision; D1 (flag versus detection) is a prerequisite for all of them |
| F-15 | MINOR | minor | architecture | Nygard | blocked outcomes map to `failed`, which does not count toward Orca's circuit breaker, and no cap on coordinator retries of a blocked Task is stated |

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR, Wiegers, priority High)
- **Sentence.** An implementer who follows the stated text as written builds P1 so that every command in sections 3.1 and 3.2 accepts `--unattended` and has a `## Unattended mode` section, because SPEC:159 and SPEC:195 say so; and the same implementer, following SPEC:94-125 and the P1 command list in the same SPEC:159 row, builds only 9 plus 6 of them, and AC-1.1 cannot pass for the other 22 until P2 to P4, which by SPEC:154 do not start until P1's checks pass.
- **Evidence.**
  - SPEC:159: P1 scope is "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"; its command column lists only analyze, build, business-panel, design, document, explain, index, test, load, plus adversarial, cleanup-audit, index-repo, workflow, brainstorm and init-lite.
  - SPEC:160-162: auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot are P2; roadmap, validate-roadmap, validate-tests, save are P3; implement, post-release, pr-submit are P4. The section 3.2 Phase column agrees (SPEC:99-125).
  - SPEC:195: AC-1.1 "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - SPEC:154: "Later phases do not start until the earlier phase's checks in section 7 pass."
- **Wrong outcome.** Deadlock: AC-1.1 as written can pass only if P2 to P4 edits already exist, and P2 to P4 cannot start until AC-1.1 passes. An implementer who resolves it toward the command list ships a P1 whose own acceptance test fails; one who resolves it toward AC-1.1 pulls 22 commands (including pr-submit, post-release and implement, which SPEC:162 holds for user decisions D2 to D4) into P1.
- **Recommendation.** Narrow AC-1.1 and the SPEC:159 sentence to the commands the P1 row lists (or to "commands whose Phase column says P1 or earlier"). Delete, do not add.
- **Quality impact.** Consistency 6 to 9 for the phase plan.

### F-02 (blocking, MAJOR, Wiegers, priority High)
- **Sentence.** An implementer who follows the stated text as written builds a `/sc:load` that changes only its usage line and writes no contract (SPEC:76, SPEC:112, SPEC:265), and builds the P1 acceptance tests that demand a `## Unattended mode` section naming `return-contract.yaml` for it (SPEC:76 "Every changed command also gains the section", SPEC:195 AC-1.1), so the tests fail on a correct `/sc:load`.
- **Evidence.**
  - SPEC:76: "load has no contract, because it is not dispatched as its own Task"; the same paragraph says "Every changed command also gains the `## Unattended mode` section".
  - SPEC:112: load row: Report "none (see note)"; Phase "P1 (usage line only)"; "use it as a step inside another worker's brief, not as its own Task".
  - SPEC:159: load is in the P1 command list; SPEC:79 says the 3.1 table gains the flag, and SPEC:159 says every command in 3.1 and 3.2 accepts it.
  - SPEC:196: AC-1.2 runs the 7.2 live check "on each P1 command" with `--unattended --output <dir>`; 7.2 step 4 (SPEC:183) is `test -s <contract>`, which cannot pass for load.
  - SPEC:265 (Decisions): "a report file would be an unrequested addition."
  - INV-B:31 and INV-B:65 support the load verdict (writes no file; use as a brief step).
- **Wrong outcome.** AC-1.1 and AC-1.2 fail on the `/sc:load` the spec itself specifies; two stated texts contradict each other.
- **Recommendation.** State once that `/sc:load` is exempt from the `## Unattended mode` section, the flag and AC-1.1/AC-1.2 (same treatment as section 4 commands), or remove load from the P1 acceptance scope. Delete or narrow only.
- **Quality impact.** Consistency 6 to 9 for section 3.2 versus section 7.

### F-07 (Medium, MAJOR label, Wiegers, priority Medium)
- WC-4 fixes `status` to `succeeded|partial|failed|blocked` (SPEC:62) and also says commands with existing contracts "keep their fields" (SPEC:62). The existing contracts' `status` vocabularies are not recorded in the inventories (INV-B:272 lists `status` for workflow without its values; INV-A:35 and INV-A:97 give no values). If an existing contract uses another value (for example a command-specific `completed`), the AC step 4 assertion `d['status'] in {...}` (SPEC:183) fails, and WC-5 (SPEC:63) maps an unknown value to `succeeded` by "otherwise". Needs a guess about the existing values, so Medium.
- Recommendation: say whether existing `status` values are mapped to the set or renamed.

### F-06 (Medium, MAJOR label, Wiegers, priority Medium)
- WC-4 requires the contract path "known before dispatch" and equal to `<output-dir>/return-contract.yaml` (SPEC:62, SPEC:73). WC-6 says a command with no resume flag "writes each run into a fresh output directory so a re-run starts clean" (SPEC:64), and 18 section 3 rows say "fresh dir". If the command makes the fresh directory itself (timestamp subdirectory), the path is not known before dispatch; if the coordinator supplies it, SPEC:73 (what the coordinator owes each worker) does not say a retry brief must carry a new directory, and a retry with the same `--output-dir` overwrites the first attempt's contract. The implementer picks one of two readings, so Medium.
- Recommendation: add to section 2.3 that the retry brief names a new output directory (one clause).

### F-08 (Medium, MAJOR label, Nygard, priority Medium)
- WC-9 (SPEC:67): outward defaults are off under `--unattended` and "turn on only through the command's own explicit flag written in the brief". The evidence supplied shows only `--no-post-pr` for auggie-review (INV-A:38 "Off with `--no-post-pr` (C:52)"); no positive `--post-pr` appears in the inventories, and the auggie-review row lists "Other required change: none" (SPEC:100). D4 (SPEC:244) and AC-2.4 (SPEC:202) refer to `--post-pr`. The same gap applies to task `commit`/`push` ("refused unless authorized", SPEC:121) and post-release commit and PR ("off unless the brief authorizes them", SPEC:113): neither row names the authorizing flag. As written, the brief has no defined way to authorize these actions. Requirement not stated, so Medium.
- Recommendation: name the authorizing flag per outward action, or state that no brief can authorize it (D4 option b).

### F-10 (Medium, MINOR label, Crispin, priority Low)
- WC-3 (SPEC:61) lets a worker with a preamble `ask` the coordinator instead of ending blocked; AC-2.2 (SPEC:200) expects `worker_done --outcome failed` and `status: blocked` for blocked gates. A worker that follows WC-3 passes neither. Needs the worker to choose the `ask` branch, so Medium. Recommendation: have the AC-2.2 brief say "do not ask".

### F-11 (Medium, MINOR label, Wiegers, priority Low)
- SPEC:91 and SPEC:158/SPEC:194: the troubleshoot brief carries "no `--fix`" only, and the contract is written "beside `REPORT.md`" (SPEC:76). No flag fixes the REPORT.md directory in the P0 line or in section 3.1, so the report path is not known before dispatch (WC-4, SPEC:62; SPEC:73). INV-B:49 gives `report_path` REPORT.md without a location. UNVERIFIED whether a flag exists. Recommendation: state the flag in the 3.1 "Brief must pass" cell.

### F-12 (minor note)
- SPEC:148 (SA-3) allows the contract "in unattended mode or when the caller passes the new output flag"; SPEC:62 (WC-4) says "In unattended mode the command writes". The AC-1.3 check (SPEC:197) tests neither combination (`--output` without `--unattended`). Note only.

### F-13 (minor note)
- WC-10 (SPEC:68) triggers splitting at calls over 5 minutes and sets waits at most 4 minutes; AC-4.3 (SPEC:210) fails any call over 240 s. A 4 to 5 minute call is allowed by WC-10 and fails AC-4.3. The pr-submit row (SPEC:114) already uses the 4-minute figure; note only.

## === ARCHITECTURE ANALYSIS ===

### F-03 (Medium, Fowler / Whittaker, priority Medium)
- Divergence and accumulation attack. I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (SPEC:69) and SPEC:76** fails when **two workers in one worktree use `--output` files in the same directory**. Concrete attack: before: `docs/tdd/` empty; worker 1 runs `/sc:tdd ... --unattended --output docs/tdd/auth.md`, worker 2 runs `... --output docs/tdd/billing.md`; after: both write `docs/tdd/return-contract.yaml` (SPEC:76: "tdd and init-lite, whose `--output` is a file, write a sibling `return-contract.yaml` in that file's directory"); the second write overwrites the first; the coordinator opens the path from worker 1's `worker_done` and reads worker 2's status. `init-lite` has a default location `.dev/superclaude/context-audit.md` (SPEC:87), so its sibling contract is at a fixed path. The spec does not require distinct directories (SPEC:73 only requires "the output directory"). Whether the coordinator shares a directory is a coordinator choice, so Medium.
- Recommendation: require a per-Task directory for these two (or name the contract after the output file).

### F-04 (Medium, Fowler, priority Medium)
- AC-C1 (SPEC:172) is a grep over `src/superclaude/core` that "prints nothing" for `orca (orchestration|worktree|terminal|agent)`. P0 (SPEC:158) adds an Orca section to `src/superclaude/core/HOW-WE-WORK.md` and writes `src/superclaude/core/WORKER-CONTRACT.md` with a "coordinator brief template"; SA-2 (SPEC:147) allows Orca mentions "as an example of a caller's question channel inside the contract file", and WC-3 (SPEC:61) refers to the preamble's `ask` command. The spec does not say those two files avoid the strings, and a coordinator section naturally contains `orca-ide orchestration ...` (CAPS:145). Whether P0 text includes such strings is not stated, so Medium.
- Recommendation: exclude the two named files from AC-C1 or state they use no such command text.

### F-05 (Medium, Hohpe / Whittaker, priority Medium)
- Sequence attack. I can break this specification by **Sequence Attack**. The invariant at **WC-2 and WC-4 (SPEC:60, SPEC:62)** fails when **an unattended command invokes another command whose own gate or contract path the spec does not cover**. Concrete attack: `/sc:release-split --unattended --output D` runs a nested brainstorm and adversarial (INV-B:37 lists brainstorm + adversarial fan-out); if the nested brainstorm is given `D` and its own `--unattended`, WC-4 has it write `D/return-contract.yaml`, which is also release-split's contract path (SPEC:76), so the parent's file is overwritten or the child's contract is mistaken for the parent's; if `--unattended` is not passed down, a nested prompt (for example `/task` "ask the user", SPEC:90, or `--interactive` passed on by brainstorm, INV-A:39) reappears. Only tasklist to reflect (SPEC:122) and workflow to reflect (SPEC:92 "no `--remediate`") are mentioned. No general rule exists. Requirement not stated, so Medium.
- Recommendation: one sentence in WC-2 or the contract file: nested commands receive `--unattended` and a distinct output directory.

### F-09 (Medium, Fowler / Nygard, priority Medium)
- SPEC:88 changes reflect so that, under `--unattended`, `--remediate` "follow[s] the existing headless auto-accept rule instead of the `[yes / no]` prompt". INV-B:107 (reflect (a)) records that under headless `claude --print` it "auto-accepts for auto-fixable registers and skips the gates". SPEC:122 has tasklist Stage 10.5 pass `--unattended` to each reflect so the headless rule applies. INV-B:46 (tasklist (g)) recommends the opposite: "drop `--remediate` in 10.5". The result is a tasklist run that auto-accepts remediation handoffs in N nested reflect subagents, with no statement of what the auto-accepted hand-off then does or writes. I could not see the rule's text (UNVERIFIED), so the effect is a guess; Medium.
- Recommendation: either follow INV-B:46 or say what auto-accept does and where it writes.

### F-14 (minor note)
- SPEC:154 "Phases 1-3 need no user decision" versus SPEC:225 "Phases 0-3 can proceed on the recommendations" and D1 (SPEC:227-230), which P1 depends on. The two sentences are compatible only if the recommendation counts as a decision; note only.

### F-15 (minor note)
- Accumulation attack. SPEC:63 maps `blocked` to `--outcome failed`; SPEC:263 notes a worker's own `failed` "does not trip Orca's circuit breaker" (CAPS:80). A coordinator that retries a blocked Task with `--retry-of` gets the same block each time with no breaker (CAPS:116). The spec gives no retry cap; this is coordinator practice. Note only.

## Expert notes (consensus and disagreement)

- Wiegers, Crispin: requirements tables are traceable (WC ids to section 3 rows to AC ids); the two blocking findings are acceptance-criterion scope errors, not design errors.
- Fowler, Newman: the central decision (Orca above, commands as units, no Orca call in a command) is consistent with CAPS:97-103, CAPS:147-150 and INV-A:90, INV-B:285-287; I found no evidence that contradicts it. The spec states its own evidence gaps (SPEC:41-45).
- Cockburn: the primary actor (the coordinator) and its goal (read one contract per worker) are explicit at SPEC:16 and SPEC:73.
- Adzic: AC-2.2 and AC-4.1 to AC-4.3 are concrete scenarios; no Given/When/Then is needed for the findings above.
- Nygard, Whittaker: no disagreement with the panel; the failure-mode coverage (blocked, partial, fenced) is better than usual.
- Hightower: not applicable beyond the Orca process facts, which are inventory-sourced.

## Guard Condition Boundary Table

Trigger present (numeric thresholds, boolean gates). Table complete per FR-10; input classes left out are noted per guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | One/Minimal | `status: partial` | succeeded | `--outcome succeeded`, body states `partial` | OK |
| WC-5 outcome mapping | SPEC:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | `blocked` | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | existing contract with a `status` outside the four values | "otherwise" so succeeded | falls into `succeeded` by default | GAP (F-07, Medium) |
| WC-10 wait split | SPEC:68 | Zero/Empty | no long wait | n/a | no split | OK |
| WC-10 wait split | SPEC:68 | Typical | 3 min call | false | no split | OK |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | 5 min 01 s call | true | split into waits of at most 4 min | OK |
| WC-10 wait split | SPEC:68, SPEC:210 | Legitimate Edge Case | 4 to 5 min single call | false | allowed by WC-10, fails AC-4.3 (240 s) | GAP (F-13, minor) |
| WC-9 outward default off | SPEC:67 | Zero/Empty | no authorizing flag in the brief | off | action not taken | OK |
| WC-9 outward default off | SPEC:67 | Typical | explicit flag in the brief | on | action allowed | OK |
| WC-9 outward default off | SPEC:67, SPEC:100, SPEC:113, SPEC:121 | Legitimate Edge Case | action with no named flag (`--post-pr`, task `commit`/`push`, post-release commit/PR) | undefined | no flag defined to turn it on | GAP (F-08, Medium) |
| WC-2 gate resolution | SPEC:60 | Typical | gate with documented default | (a) | default taken | OK |
| WC-2 gate resolution | SPEC:60 | Sentinel Value Match | `--unattended` plus `--interactive` in one line | refused or absolute | WC-2 is absolute ("never calls AskUserQuestion"); rows say "never `--interactive`" or "refused" | OK |
| WC-2 gate resolution | SPEC:60, SPEC:88-90 | Legitimate Edge Case | gate inside a nested command | unspecified | only tasklist to reflect is stated | GAP (F-05, Medium) |
| Nested depth | SPEC:33, SPEC:66 | Maximum/Overflow | worker calls `worker-start` | refused (`nested_worker_depth_exceeded`) | WC-8 forbids it; CAPS:99 | OK |
| Nested depth | SPEC:66 | Legitimate Edge Case | depth-1 worker `task-create` | UNVERIFIED | WC-8 forbids either way | OK |
| Readiness limit | SPEC:59 | Typical | fallback 30 s | passes | EVIDENCE passes at 30 s (UNVERIFIED file; CAPS:49 quotes the 45 s failure) | OK |
| Readiness limit | SPEC:59 | Maximum/Overflow | fallback above about 45 s | fails | "well inside" the 60 s limit | OK |
| P1 acceptance scope | SPEC:159, SPEC:195-196 | Typical | command listed in the P1 row | pass | AC-1.1 and AC-1.2 apply | OK |
| P1 acceptance scope | SPEC:195 | Legitimate Edge Case | command in 3.1/3.2 with phase P2 to P4 | fail | AC-1.1 requires its section in P1 | GAP (F-01, blocking) |
| P1 acceptance scope | SPEC:112, SPEC:195 | Zero/Empty | command with no contract (`/sc:load`) | fail | AC-1.1 requires `return-contract.yaml` named | GAP (F-02, blocking) |
| Contract path | SPEC:76 | One/Minimal | one worker, one directory | pass | unique file | OK |
| Contract path | SPEC:76 | Maximum/Overflow | two workers, one directory (`tdd`, `init-lite`) | collision | not specified | GAP (F-03, Medium) |

Classes left out: WC-5 "Maximum" (a status has no maximum); WC-10 "Sentinel" (no sentinel); WC-9 "Maximum" (no capacity); Nested depth "Zero/Empty" (depth 0 is the coordinator, which may start workers, CAPS:97).

## Whittaker attack list (adversarial section)

| # | Attack | Location | Result | Severity |
|---|---|---|---|---|
| W-1 | Zero/Empty: brief without `--output-dir` for a command whose path rule needs it | SPEC:62, SPEC:76 | cleanup-audit and index-repo gain `--output-dir` in P1; before that the path is fixed (SPEC:85) | no break found |
| W-2 | Divergence: file-valued `--output` versus directory-valued output flag | SPEC:76 | sibling file rule; collides in a shared directory | MAJOR, graded Medium (F-03) |
| W-3 | Sentinel collision: contract file name `return-contract.yaml` reused by parent and nested command | SPEC:62, SPEC:76 | overwrite of the parent's file | MAJOR, graded Medium (F-05) |
| W-4 | Sequence: P1 acceptance before P2 to P4 exist | SPEC:154, SPEC:159, SPEC:195 | AC-1.1 cannot pass | blocking (F-01) |
| W-5 | Accumulation: unbounded coordinator retries of a blocked Task | SPEC:63, SPEC:263 | no cap | MINOR (F-15) |

## Pipeline Dimensional Analysis

Not triggered: the spec describes a coordinator-to-worker task flow, not a data pipeline whose stage output counts may differ from input counts. Count conservation checks that do apply were performed and hold: 5 + 5 ready = 10 (SPEC:81-92 lists 10 rows), 27 rows in 3.2, 6 in section 4, 10 + 27 + 6 = 43 = 21 + 22 (INV-A:3, INV-B:3); phase lists total 9 + 11 + 4 + 3 = 27 for 3.2 plus 15 + 6 + 4 = 25 mentions with 3.1 fixes counted separately.

## Citation checks (what I could verify)

| Claim | Result |
|---|---|
| E1 to E6, R1 to R5 inventory citations (`CAPS:86,92,97-103,145-150,155,158,161`; `INV-A:76-83,90,94-98`; `INV-B:285-286,289-299`) | found as cited |
| WC-1 to WC-12 inventory citations (`CAPS:44-45,52,58-61,64,66-67,72-80,107-116,129-130,159-161`) | found as cited |
| Section 4 inventory citations (`INV-A:36,49-50,90-92`; `INV-B:32,42,44,67-75,167-175,187-195,285-287`) | found as cited |
| UNVERIFIED list citations (`CAPS:68,178,180,186-188`; `INV-A:113,120`; `INV-B:323`) | found as cited |
| SPEC:11 "re-read 11 load-bearing locations" and SPEC:285 "340 citations re-read, 9 defects" | UNVERIFIED (files not in the sandbox) |

## UNVERIFIED citations (cannot be checked inside the workspace)

`.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56`; `.dev/codegraph-migration/orchestration/README.md:31,33,42`; `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`; every `cmd/...`, `sk/...`, `ag/...` path (SPEC:11, 83-125, 132-137); `src/superclaude/cli/install_core.py:4,13-24,33`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65`; `CLAUDE.md:16,50,72-83,157,334,408`; `pyproject.toml:38`; `Makefile:68-74`; the grep results claimed at SPEC:25 (E5); `~/.claude/commands/sc/pr-submit.md` and `~/.claude/skills/sc-pr-submit-protocol/SKILL.md` (README:13). I treated these as unchecked and graded no finding on them.

## follow-up candidates

Medium and minor findings, none of which triggers a revision. No issue has been opened; the session that ran this review is expected to ask the user once for this loop whether to open one, and this run (no user prompt available in this sandbox) only records the list.

| id | grade | one line |
|---|---|---|
| F-03 | Medium | sibling `return-contract.yaml` collides across workers sharing a directory |
| F-04 | Medium | AC-C1 grep versus P0 Orca text in `core/` |
| F-05 | Medium | no rule for `--unattended` and contract path in nested invocations |
| F-06 | Medium | WC-6 fresh directory versus WC-4 known path; retry brief lacks a new directory |
| F-07 | Medium | existing contract `status` vocabularies versus the fixed set |
| F-08 | Medium | no authorizing flag for several outward actions |
| F-09 | Medium | reflect `--unattended` auto-accept inside tasklist Stage 10.5 |
| F-10 | Medium | AC-2.2 versus WC-3 `ask` |
| F-11 | Medium | troubleshoot report path not known before dispatch |
| F-12 | minor | SA-3 versus WC-4 trigger wording |
| F-13 | minor | WC-10 5 minute trigger versus AC-4.3 240 s |
| F-14 | minor | "no user decision" wording versus D1 |
| F-15 | minor | no cap on retries of blocked Tasks |

## Reviser brief

Blocking finding ids: F-01, F-02.

Contract for the reviser (this restates the command's reviser contract; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone.

- F-01: narrow the P1 scope sentence (SPEC:159) and AC-1.1 (SPEC:195) so they cover only commands whose Phase column is P1 (or P0/P1), not every command in 3.1 and 3.2.
- F-02: make `/sc:load` consistent: exempt it from the `## Unattended mode` section, the flag, AC-1.1 and AC-1.2 (SPEC:76, SPEC:112, SPEC:159, SPEC:195-196), or drop it from the P1 acceptance scope.

verdict: FAIL
