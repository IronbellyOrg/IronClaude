review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate sha256: `746b5ffc5ac4b78a7e2053e0e341cc67756a46ac8a09ff6161b886dedded7fa2`
- Baseline: none given (first review of the whole document; no `--re-review`, so no baseline note is owed).
- Reviewer model actually used: `claude-sonnet-5-5`
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before reviewing).
- Context read first: `.dev/orca-command-refactor/README.md` (binding shared context, 38 lines).
- Coverage: the whole candidate (all 284 lines: sections 1-9, Decisions, UNVERIFIED items), checked against the three inventory files `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. Coverage is whole-document; this is not a scoped re-review.
- Experts run (fixed order): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower. Focus leads: Wiegers (requirements), Fowler (architecture). Findings are attributed to the expert who raised them.

## Evidence limits (UNVERIFIED)
Only the three inventory files are checkable in this sandbox. Every citation to `cmd/...` (`src/superclaude/commands/`), `sk/...` (`src/superclaude/skills/`), `ag/...`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `pyproject.toml`, `Makefile`, `install_core.py`, `EVIDENCE.md`, `.dev/codegraph-migration/...` and every Orca guide or `/opt/Orca/...` path is UNVERIFIED here. Where the spec quotes an inventory line, I checked that line.

Inventory citations checked and found as cited:
- Command counts: 21 rows in `INV-A:35-55`, 22 rows in `INV-B:31-52`. The 10 / 27 / 6 split matches both inventories' own summaries (A: 5 ready, 13 needs-change, 3 coordinator-only; B: 5, 14, 3).
- Phase partition counts add up (see the Quantity Flow Diagram below).
- `INV-B:285-286, 289-299, 301, 311, 320, 323`; `INV-A:76-83, 90, 94-98, 106, 113, 118, 120`: each line holds what the spec says it holds.
- `CAPS:44-47, 52, 58-61, 64, 66-68, 72-80, 92, 97-103, 107-116, 129-130, 145-151, 155-161, 178-188`: each holds what the spec says it holds (for example `CAPS:80` supports the claim that a worker's own `failed` report does not trip the circuit breaker, which makes the blocked-to-failed mapping safe).
- Only a pointer, not a defect: `CAPS:161` quotes the pr-submit top-level rule as `SKILL.md:47-49` in the installed copy, while the spec and `INV-A` cite `SKILL.md:37-39` in `src/`. Two copies, two line numbers; I cannot tell which is current.

## What the spec states (requirements under review)
Orca coordinates and commands stay the units of work (spec 13-16). Twelve worker-contract rules WC-1 to WC-12 (57-70), per-command changes for 43 commands (75-125), six coordinator-only commands (127-139), six standalone-safety rules SA-1 to SA-6 (141-151), five phases P0-P4 (153-164), acceptance checks (166-210), non-goals (212-222), five open decisions D1-D5 (224-253).

Overall: the decision is well argued, the evidence gaps are stated honestly (spec 41-45), the rejected alternative is reasoned against `CAPS` lines, the fork-only `gh` forms in AC-2.4 and AC-4.2 (spec 202, 209) match the repo rule in the brief context, and the per-command table is internally complete. No finding below is a stated text that, followed as written, causes data loss, breaks a security or safety boundary, or contradicts another stated text with no allowed reading. The findings are Medium or minor.

=== REQUIREMENTS ANALYSIS ===

### R-1 Where the contract file goes is undefined for file-valued and fixed output paths
- Expert: Wiegers (lead), Crispin. Label MAJOR, graded Medium. Priority High. Quality impact: Testability and Completeness down about 1 point each.
- Issue: WC-4 says the contract is `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" and must be "known before dispatch" (spec 62). But section 3 briefs several commands with a file-valued `--output`: tdd `--output <file>` (90), init-lite `--output <file>` (87), and "add `--output`" for analyze, spec-panel and others with no stated type (99, 120). No directory is passed for those. cleanup-audit has a fixed `.claude-audit/` directory and no output flag (85), index-repo has a fixed repo-root location (86). Yet AC-1.2 runs every P1 command "with `--unattended --output <dir>`" (196), and 7.2 step 3 requires the report path to equal "the WC-4 contract path" (182). The phase text says "output flags for commands that lack one" are added (159), but the 3.1 rows for cleanup-audit and index-repo do not list that flag.
- Grading sentence: An implementer who follows the stated text as written builds a tdd worker whose contract path is unstated (parent directory of the file? a sibling file?), and that is wrong because the coordinator cannot know the path before dispatch, which is what WC-4 requires. This needs a guess about which reading the implementer picks, so it is Medium.
- Concrete attack: `/sc:tdd "auth component" --unattended --output .dev/tdd/auth.md` blocks on the topic-only gate (90). WC-2 says write `status: blocked`. Path options: `.dev/tdd/return-contract.yaml` (shared by any other tdd worker writing into `.dev/tdd/`, breaking WC-11, spec 69) or `.dev/tdd/auth.return-contract.yaml`. AC-2.2 (200) cannot then assert a specific path.
- Recommendation: state one rule for file-valued outputs (for example `<output-file>.return-contract.yaml` beside the file) and one for commands with fixed directories (name the contract path inside that directory). Add the two fixed-directory commands' flag to their 3.1 rows or say in AC-1.2 which commands are exempt.

### R-2 Gate-resolution flags are named by description only, so AC-2.1 cannot assert them
- Expert: Crispin, Wiegers. Label MAJOR, graded Medium. Priority Medium.
- Issue: Several rows resolve a gate with "a value the caller supplied as a flag" (WC-2 b, spec 60) but never name the flag: post-release "an explicit pre-tag choice" (113), review-translation "a pre-confirmed context input" and "a resume input" (117), cli-portify's three approval gates resolve as blocked but nothing says how a resumed run is told the artifact was approved (105; the only mechanism named is `--resume <contract>`, which carries `resume_phase`/`resume_substep`, not an approval), research and roadmap name their flags. AC-2.1 requires "one assertion per gate listed in the section 3 row" (199).
- Grading sentence: An implementer builds the flag name by guess; the text does not say which, so two implementers diverge. It is a requirement the document never states, so Medium.
- Recommendation: name each flag in the row (or say the name is chosen in that phase's plan and recorded in the contract file's brief template, spec 158).

### R-3 The live checks can fail on a correct implementation because WC-3 lets the worker ask instead of block
- Expert: Adzic, Crispin. Label MAJOR, graded Medium. Priority Medium.
- Given/When/Then: Given a worker running `/sc:cli-eval run --unattended` with no `--suite` (the example in AC-2.2, spec 200); When the worker session holds a preamble, WC-3 lets it ask the coordinator and re-invoke with the answer (61); Then it may end `succeeded`, but AC-2.2 requires `worker_done --outcome failed` and `status: blocked` (200).
- Grading sentence: Following WC-3 and AC-2.2 as written, a conforming worker can fail the acceptance check. The word "may" in WC-3 makes this depend on the worker's choice, which needs a guess, so Medium.
- Recommendation: say in 7.2 (or AC-2.2) that the gate-trigger runs brief the worker not to use `ask`, or accept either path as a pass.

### R-4 P0 smoke runs conflict with the brief rule that every command line carries `--unattended`
- Expert: Cockburn, Adzic. Label MAJOR, graded Medium. Priority Medium.
- Issue: Section 2.3 says the brief states "the exact command line including `--unattended`" (73), and 7.2 step 1 builds the Task from that brief (180). In P0 no command has the flag (it arrives per command in P1/P2, spec 159-160), and 3.1 says the ten ready commands run "if the brief uses the stated flags" with no `--unattended` among them (79-92). AC-0.4 runs the three smoke commands without it (194). For troubleshoot, tdd, reflect and release-split the flag arrives only in P2 (160), so between P1 and P2 a coordinator following 2.3 passes a flag the command does not know.
- Grading sentence: Following 2.3 for troubleshoot in P1, the brief contains `--unattended`, which the command does not parse, so it may be read as part of the symptom text. Needs a guess about command parsing (not evidenced in the inventories), so Medium.
- Recommendation: add one sentence to 2.3: the flag is passed only once the command's own row phase has landed; until then use the 3.1 "Brief must pass" column alone.

### R-5 "Phases 1-3 need no user decision" is contradicted by P2 rows that depend on D4
- Expert: Cockburn, Wiegers. Label MAJOR, graded Medium. Priority Medium.
- Issue: Spec 154 says Phases 1-3 need no user decision and only Phase 4 waits for D2-D4. D4 (244-247) says it affects "post-release, pr-submit under D3 (b), auggie-review `--post-pr`, task `commit`/`push`". auggie-review and task are P2 rows (100, 121; phase list 160). Under D4 option (b) "Never", the row's opt-in `--post-pr` path (100) must not exist; under (a) it does. Section 9's own intro says phases 0-3 may proceed on the recommendations (225), which softens it, so the two sentences do not strictly contradict.
- Grading sentence: An implementer of P2 who builds the opt-in `--post-pr` path builds something D4(b) forbids, but only if the user later picks (b), which is a guess about a future answer. Medium.
- Recommendation: either move the `--post-pr` and task `commit`/`push` opt-in parts to P4, or change 154 to say P2 proceeds on D4's recommendation.

### R-6 Minor notes (requirements)
- N-1 (Wiegers, MINOR): WC-1 (spec 59) has no phase and no acceptance check. The `EVIDENCE.md:39,45,56` fix (wrapper fallback) is cited as already applied (`CAPS:49`), so the live check at 7.2 step 1 covers it indirectly. State that explicitly.
- N-2 (Wiegers, MINOR): Spec 16 and 51 say the command-side change is limited to unattended mode, report files and resume, but the "Other required change" column adds tool-list, frontmatter, default-target and flag-surface fixes (102, 105, 108, 124, 125). SA-4 (149) lists them, so only the earlier sentences overstate.
- N-3 (Wiegers, MINOR): SA-1 says every default flag value and output path stays as today (146); P3 changes the validate-tests default target and the validate-roadmap report filename (124-125). SA-4 (149) allows documented-defect fixes. Say in SA-1 that SA-4 is its only exception.
- N-4 (Gregory, MINOR): `blocked_question` is only required "when blocked" (62); AC-2.2 requires it non-empty (200). Put the non-empty rule into WC-4.
- N-5 (Gregory, MINOR): The UNVERIFIED section lists item 14 (spec 284), which is a citation-check record, not an unverified item. Move it to Decisions or section 1.

=== ARCHITECTURE ANALYSIS ===

### A-1 The generic contract path in WC-4 disagrees with the adversarial row
- Expert: Fowler (lead), Hohpe. Label MAJOR, graded Medium. Priority Medium.
- Issue: WC-4 fixes the path as `<output-dir>/return-contract.yaml` (62). The adversarial row fixes it as `<output>/adversarial/return-contract.yaml` (83), consistent with `INV-A:35`, which records that real runs wrote there. 7.2 step 3 checks the report path against "the WC-4 contract path" (182). A coordinator that reads WC-4 looks in the wrong directory for adversarial.
- Grading sentence: A coordinator that follows WC-4 reads `<dir>/return-contract.yaml` for an adversarial worker and the file is not there. The row is the more specific text and an implementer can read it as an override, so there is an allowed reading and it is Medium.
- Recommendation: add "or the command-specific path named in section 3" to WC-4, or put adversarial's contract at the generic path.

### A-2 Liveness rule covers Bash waits only; Agent-tool calls block the session just as long
- Expert: Nygard (lead), Newman. Label MAJOR, graded Medium. Priority Medium.
- Issue: WC-10 splits long single tool calls into waits of at most 4 minutes so the session can heartbeat (68). The examples are poll waits and evals. The spec's own E4 keeps Agent-tool fan-out inside commands (24), and the inventories show heavy fan-out (cleanup-audit waves, tdd, adversarial, post-release). A foreground Agent call can run well past 5 minutes with no chance to heartbeat. AC-4.3 then asserts "no single tool call exceeds 240 s" for pr-submit (210), which includes its per-finding troubleshoot and evidence-validator dispatches (`INV-B:34`).
- Grading sentence: Following AC-4.3 as written, a pr-submit run that dispatches a multi-minute subagent fails the check, while WC-10 and E4 allow that dispatch. This depends on subagent duration (not evidenced), and `CAPS:130` marks whether Orca uses heartbeat age as UNVERIFIED, so Medium.
- Recommendation: say whether WC-10 applies to Agent-tool calls; if not, restrict AC-4.3 to Bash waits; if yes, say how (background agents with short polls).

### A-3 "Fresh output directory" on retry has no owner and clashes with "known before dispatch"
- Expert: Nygard, Newman. Label MAJOR, graded Medium. Priority Medium.
- Issue: WC-6 says a retry must not corrupt the first attempt and, for commands with no resume flag, "writes each run into a fresh output directory" (64). About twenty rows say "fresh dir" (83-125). WC-4 says the output directory is passed by the coordinator and known before dispatch (62), and 2.3 lists the output directory among what the coordinator owes (73). The spec never says who creates the fresh directory on a retry, or what the coordinator passes on `worker-start --retry-of`. Stale-file risk follows (see W-1).
- Grading sentence: An implementer who writes into the passed directory on retry overwrites attempt 1 (violating WC-6); one who invents a subdirectory breaks the path known before dispatch (violating WC-4). The text allows either, so Medium.
- Recommendation: make it a coordinator duty in 2.3: pass a new output directory per attempt; commands never invent one.

### A-4 The tasklist row keeps `--remediate`, auto-accepts it, and does not record the departure from the inventory
- Expert: Fowler, Nygard. Label MAJOR, graded Medium. Priority Medium.
- Issue: Under `--unattended` the row passes `--unattended` to each reflect so "the headless rule applies" (122). `INV-B:109` says that rule "auto-accepts for auto-fixable registers and skips the gates", and `INV-B:208-210` says Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase inside subagents. So an unattended tasklist run auto-launches remediation hand-offs per phase with no person. The inventory's recommendation was the opposite: "Stage 10.5 should call reflect without `--remediate`" (`INV-B:215`). The spec's Decisions say nothing read contradicted an inventory verdict (268) and record no choice here. The row also says the fan-out is "inside Claude Code's nesting limit" citing `INV-A:14`, while `INV-B:210` marks nested spawning from those subagents UNVERIFIED and notes `sk/tdd/SKILL.md:238` avoids it. WC-9 (67) covers outward actions only, so auto-remediation is not caught by it.
- Grading sentence: Following row 122, `tasklist --unattended` runs reflect remediation chains unattended in nested subagents; that is wrong only if auto-remediation is unwanted, which the spec does not say. Needs a guess, so Medium.
- Recommendation: follow `INV-B:215` (drop `--remediate` under `--unattended`) or record the choice in Decisions with the nesting evidence and an acceptance check.

### A-5 Fixed four-value status is imposed on contracts whose existing status values the spec never checked
- Expert: Newman, Hohpe. Label MAJOR, graded Medium. Priority Medium.
- Issue: WC-4 keeps existing contract fields and adds missing ones (62), and Decisions fix `succeeded/partial/failed/blocked` for every command (262). 7.2 step 4 asserts `d['status'] in {'succeeded','partial','failed','blocked'}` (183). The inventories show that workflow, brainstorm, reflect and adversarial already write contracts with a `status` or verdict field (`INV-B:272`, `INV-A:97`), but neither the spec nor the inventories list those existing value sets or the contract version (workflow's is "contract 1.1", `INV-B:272`). WC-4 itself has no version field.
- Grading sentence: If workflow's existing `status` takes values outside the four, "keep their fields" and the step-4 assertion cannot both hold. The inventories do not say whether it does, so Medium.
- Recommendation: add a one-row table of each existing contract's status values and either map them or rename; add `contract_version` to WC-4.

### A-6 AC-C1 may fail on the spec's own allowed Orca mentions
- Expert: Hightower, Fowler. Label MAJOR, graded Medium. Priority Medium.
- Issue: AC-C1 greps `src/superclaude/{commands,skills,agents,core}` for `orca (orchestration|worktree|terminal|agent)` and requires no output outside `ccsession-tag` (172). SA-2 permits one Orca mention, "as an example of a caller's question channel inside the contract file" (147), and the contract file lives in `core/` (52). P0 also adds an Orca section to `HOW-WE-WORK.md`, also in `core/` (150, 158). Writing either in the form `orca orchestration ask` matches the regex.
- Grading sentence: An implementer who writes the SA-2 example literally fails AC-C1 on every phase. The wording of the example is open, so Medium.
- Recommendation: exclude `core/WORKER-CONTRACT.md` and the HOW-WE-WORK Orca section from AC-C1, or forbid the literal command string there.

### A-7 Minor notes (architecture)
- N-6 (Newman, MINOR): WC-11 says two workers in one worktree "must never write the same file" (69), but cleanup-audit and index-repo write fixed locations and the rows accept "one audit per worktree at a time" (85-86). Say WC-11 is a coordinator scheduling rule for those two.
- N-7 (Hohpe, MINOR): The WC-10 trigger is "longer than 5 minutes" and the split target is "at most 4 minutes" (68); a 4.5-minute single call is neither required to split nor inside the 4-minute margin the Decisions row gives (266).
- N-8 (Fowler, MINOR): "Refused" under `--unattended` is used for cleanup/improve `--interactive`, business-panel/explain/test/pr-submit modes (102-103, 108, 110, 114, 123) while WC-2 defines only default, flag, or blocked. Say refused means blocked.
- N-9 (Hightower, MINOR): UNVERIFIED item 8 leaves the `plugins/superclaude/commands/` mirror rule unresolved (279) and AC-C1/AC-C2 do not cover it. The CLAUDE.md rule on that mirror cannot be checked here; each phase plan must close it, as the spec says.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

### W-1 Sequence attack (retry or resume leaves a stale contract)
I can break this specification by **Sequence Attack**. The invariant at **WC-4 / WC-6 (spec 62, 64)** fails when **a retry or resumed run reuses the directory of an earlier attempt and dies before it rewrites the contract**. Concrete attack: (1) attempt 1 of `/sc:cli-portify` writes `<dir>/return-contract.yaml` with `status: blocked`, `resume_phase: 3`. State: contract = blocked. (2) The person approves; coordinator starts `worker-start --retry-of` with the same brief and the same `<dir>` (the output directory is "known before dispatch", 62, 73). (3) Attempt 2 stops before writing (readiness failure after the terminal exists, context exhaustion). State: contract still = blocked from attempt 1. (4) The worker or coordinator reads the stale file and maps it to a current result. Nothing in WC-4 or WC-5 says the contract is deleted or overwritten at start. Severity MAJOR, graded Medium (needs the retry to die in a narrow window). Fix: a command writes `status: failed` placeholder at start or the coordinator passes a new directory per attempt (see A-3).

### W-2 Zero/Empty attack (absent or empty output location)
I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 "written on every outcome, including stops before any other output exists" (spec 62)** fails when **`--output` is omitted or empty under `--unattended`**. Concrete attack: `/sc:adversarial --unattended` with no `--output`; the skill derives the directory from the input file's directory (`INV-A` evidence note, adversarial "output directory default"), so the contract lands next to the input, not where the coordinator looks; WC-4 and 2.3 assume the coordinator passes it, but no rule says the command stops as blocked when it is missing. Severity MINOR to Medium (the inventory already says the brief should always pass `--output`); listed as a GAP row below.

### W-3 Divergence, Sentinel and Accumulation attacks
No concrete break found: the `partial` to `succeeded` and `blocked` to `failed` mappings are explicit (63, 263); the `blocked` value does not collide with a command's own data because the field is a fixed set; and the retry circuit breaker is not tripped by a worker's own `failed` report (`CAPS:80`). Residual note: a gate whose input sits exactly on a threshold (task confidence 0.70, spec 121) is covered in the table below.

## Guard Condition Boundary Table

The spec contains guards and thresholds, so the table is produced (FR-8/9/10). One row per applicable class; classes left out say why.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit | WC-1 (spec 59) | Zero/Empty | `--timeout-ms` 0, empty | falls back to default | default 60 s (`CAPS:44`, spec 59) | OK |
| readiness limit | WC-1 (spec 59) | Typical | 30 s wrapper fallback | pass | passes (`EVIDENCE.md:45` via spec 59) | OK |
| readiness limit | WC-1 (spec 59) | Maximum/Overflow | prompt above about 45 s | fail | worker-start fails (spec 59) | OK |
| gate resolution | WC-2 (spec 60) | Zero/Empty | caller flag present but `""` (for example `--suite ""`) | undefined | not stated | GAP (Medium) |
| gate resolution | WC-2 (spec 60) | Typical | flag absent | blocked | contract `blocked` plus question (60) | OK |
| output location | WC-4 (spec 62) | Zero/Empty | `--output` absent | undefined | not stated; relies on the brief (73) | GAP (Medium, W-2) |
| output location | WC-4 (spec 62) | Legitimate Edge Case | `--output` is a file, or command has a fixed directory | undefined | not stated | GAP (Medium, R-1) |
| contract written | WC-4 (spec 62) | Legitimate Edge Case | stop before the package exists (workflow) | no file | WC-5 maps to `failed` (62-63) | OK |
| outcome mapping | WC-5 (spec 63) | Legitimate Edge Case | report present but malformed or no `status` | undefined | "no report exists" is stated; malformed is not | GAP (minor) |
| outcome mapping | WC-5 (spec 63) | Sentinel Value Match | `partial`, audit verdict FAIL | succeeded | stated (63) | OK |
| wait size | WC-10 (spec 68) | Typical | 600 s poll budget | split into iterations | iterations under 4 minutes (114) | OK |
| wait size | WC-10 (spec 68) | Maximum/Overflow | 3600 s eval | split | at most 4-minute waits (104) | OK |
| wait size | WC-10 (spec 68) | Legitimate Edge Case | single call between 4 and 5 minutes; Agent-tool call over 5 minutes | undefined | not stated | GAP (minor N-7; Medium A-2) |
| nesting depth | WC-8, R1 (spec 66, 33) | Maximum/Overflow | worker calls `worker-start` at depth 1 | refused | `nested_worker_depth_exceeded`, call sites UNVERIFIED (33) | OK (UNVERIFIED stated) |
| circuit breaker | WC-6 (spec 64) | Maximum/Overflow | third failure for one Task | task failed | blocked runs end `failed` but do not count (`CAPS:80`) | OK |
| task confidence | task row (spec 121) | Sentinel Value Match | confidence exactly 0.70, or 0.70-0.89 band | undefined | only "below 0.70 resolves as blocked" (121); the band is not stated | GAP (minor, band behavior UNVERIFIED in `INV-B:199`) |
| pr-submit monitor | pr-submit row (spec 114) | Typical | `--monitor 3` (default, `INV-B:89`) | runs | stated | OK |
| pr-submit monitor | pr-submit row (spec 114) | Legitimate Edge Case | `--monitor 1` | refused | "refused" not defined (N-8) | GAP (minor) |
| ask timeout | WC-3 (spec 61) | Maximum/Overflow | timeout | pending | resume same message ID (61); default value UNVERIFIED (281) | OK |
| retry directory | WC-6 (spec 64) | One/Minimal | second attempt, same brief | undefined | not stated | GAP (Medium, A-3, W-1) |

Class left out: "One/Minimal" for most guards, because the guards are thresholds or modes with no meaningful size-1 input.

## Quantity Flow Diagram (pipeline: command classification into phases)

```text
[cmd/ commands: 43 = INV-A 21 + INV-B 22]            (spec 76; INV-A:35-55, INV-B:31-52)
   --> [Classify]
        --> ready ............ 10  (A 5 + B 5)  --> 4 get P1 small fixes, 4 get P2 gate fixes, 2 (brainstorm, init-lite) get P1 section only
        --> needs change ..... 27  (A 13 + B 14) --> P1: 9, P2: 11, P3: 4, P4: 3
        --> coordinator-only .. 6  (A 3 + B 3)   --> no phase, no section (AC-1.1 asserts none has one)
   --> [Phase assignment]
        P0: 0 command edits (3 smoke runs of 10 ready)
        P1: 9 + 4 + 2 = 15 commands     --> AC-1.1 asserts a section on 14 (load exempt)   <-- DIVERGENCE 15 -> 14 (stated, REQ-2)
        P2: 11 + 4    = 15 commands
        P3: 4 commands
        P4: 3 commands
        Total assigned 15 + 15 + 4 + 3 = 37 = 10 + 27 ; plus 6 unassigned = 43       <-- conserves
```

Counts conserve at every stage; the only divergence (load) is stated and consistent with section 3.2 and AC-1.1. No consumer assumes a conserved count wrongly.

## Priority-ranked improvement list (for the author; none is blocking)
1. R-1 + A-1 (one rule for where the contract file goes).
2. A-3 + W-1 (owner of the fresh directory per attempt).
3. A-5 (existing contract status values and a version field).
4. A-4 (tasklist remediation choice and Decisions entry).
5. R-3, R-4, A-6 (make three acceptance checks passable as written).
6. R-2, R-5, A-2 (name the flags, resolve the D4 timing, scope WC-10).

## Follow-up candidates
Medium (warnings, none blocks): R-1, R-2, R-3, R-4, R-5, A-1, A-2, A-3, A-4, A-5, A-6, W-1.
Minor (notes): N-1 to N-9, W-2, W-3.
The session that ran this review asks the user once whether to open an issue for these; none has been created here.

## Self-check on grading
Every finding above that carries the label MAJOR was graded Medium because its grading sentence needs a guess (a reading the text allows, a future user answer, or a requirement the document never states). No finding is two stated texts with no allowed reading, a data-loss or security or safety-boundary risk, or an acceptance criterion that cannot pass with no further assumption. No brief clause was overridden: the brief asked for a first review per the FIRST-REVIEW prompt and set no severity.

## Reviser brief
No blocking finding ids are open, so there is nothing to revise. If the coordinator revises anyway, the rules that apply are: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id; Medium and minor findings are left alone, including through "apply all findings".

verdict: PASS
