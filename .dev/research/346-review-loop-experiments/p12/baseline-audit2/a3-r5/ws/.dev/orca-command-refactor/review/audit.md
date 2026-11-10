review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`. Labelled whole-document audit of the final spec, run as a first review per the FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, `home/.claude/rules/prompts/document_review_loop_prompts.md:27-32`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `5d3d225a6ef33d0f0c3eb9b745dd4e780b4ca5a0b2dd745dd00ce966449d2b61` (58448 bytes, 285 lines).
- Baseline / prior report: none given. Neither `--re-review` nor `--baseline` was passed, so this is a first review of the full document.
- Reviewer model actually used: claude-sonnet-5-5.
- Brief clauses overridden: none. The brief narrowed nothing and widened nothing.
- Citation conventions (same as the spec): `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Anything cited by the spec that is not a file in this workspace (`src/`, `CLAUDE.md`, `Makefile`, `.dev/codegraph-migration/`, `.dev/evals/`, Orca installation files, `orca-ide` output) is UNVERIFIED here; where the inventories quote it, the quote is second-hand and marked as such.

## Coverage

Read in full: README, the candidate (all of sections 1-9, Decisions, UNVERIFIED), the three inventories, `command.md`. Reviewed whole-document against the requirements the spec states. Focus areas requirements and architecture (lead experts Wiegers, Adzic, Cockburn; Fowler, Newman, Hohpe, Nygard), with Whittaker active as the command requires; Crispin contributes the acceptance-check findings. Gregory and Hightower raised nothing in the two focus areas. `--focus correctness` was not requested, so no State Variable Registry is produced. The Guard Condition Boundary Table is produced (the spec contains thresholds and guards), and so is the Quantity Flow Diagram (the spec contains a multi-stage triage and rollout). The Improve step was not run: the brief restricts writes to this report and the command forbids modifying a specification without consent.

Checked mechanically: every `INV-A:N`, `INV-B:N`, `CAPS:N` citation in sections 1-5 and the per-command rows of section 3 was looked up in the inventories. The row-level ones (for example `INV-A:35-55`, `INV-B:107-115`, `INV-B:267-275`, `CAPS:44-45`, `CAPS:97-103`, `CAPS:145-151`) land on the content the spec attributes to them. Not checkable here: every `cmd/` and `sk/` line the spec carries from the inventories (the inventories are the only witness), all `CLAUDE.md:N` and `src/superclaude/cli/install_core.py:N` lines, the 11 locations the spec says it re-read (SPEC:11), and the three greps of section 1.2 (E5). They are UNVERIFIED.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Trigger: the spec triages a population through filters (43 commands to three verdicts to five phases). Counts conserve at every stage; the one divergence is in the acceptance population of Phase 1.

```text
[Source: 43 commands = 21 (INV-A:3) + 22 (INV-B:3); SPEC:76]
   --> [Triage: three-way partition, SPEC:76]
        ready 10 (SPEC:81-92)  |  needs-change 27 (SPEC:97-125)  |  coordinator-only 6 (SPEC:130-137)      10+27+6 = 43 conserved
        (inventory split A 5/13/3 + B 5/14/3 = 10/27/6; INV-A:73, INV-B:278)
   --> [Phase assignment, SPEC:156-162]
        needs-change 27 -> P1 9 (analyze build business-panel design document explain index test load)
                         -> P2 11 (auggie-review cleanup improve cli-eval cli-portify recommend research review-translation spec-panel task tasklist)
                         -> P3 4 (roadmap save validate-roadmap validate-tests)
                         -> P4 3 (implement post-release pr-submit)                                      9+11+4+3 = 27 conserved
        ready 10        -> P1 small fixes 4 (adversarial cleanup-audit index-repo workflow)
                         -> P2 4 (reflect release-split tdd troubleshoot)
                         -> no phase 2 (brainstorm, init-lite; "None" in SPEC:84,87)                      4+4+2 = 10 conserved
   --> [Consumer: AC-1.1 / AC-1.2, SPEC:195-196, "every command in the P1 row ... except load"]
        P1 row names 13 commands; minus load = 12.  Commands given a `## Unattended mode` section in P1 = 8 (the 9 above minus load).
        The 4 small-fix commands get none (SPEC:83,85,86,92)                                              12 expected vs 8 built   <-- MISMATCH (reading-dependent)
   --> [Consumer: WC-4/WC-5 report-path rule, SPEC:62-63]
        brainstorm and init-lite never accept `--unattended` (no phase), so they never write the WC-4 contract; WC-5 must read their own report.   accounted for, no mismatch
```

Grading of the mismatch: the command labels any dimensional mismatch CRITICAL (FR-19), but Review Loop bullet 2 grades by consequence. Whether AC-1.1/AC-1.2 include the four small-fix commands depends on reading the semicolon in SPEC:159, so the grading check needs a guess; it is Medium (M-12), not blocking.

## Guard Condition Boundary Table

Guards enumerated (all thresholds, caps and conditional rules in the spec): G1 readiness limit (WC-1), G2 wait-split rule (WC-10), G3 outcome mapping (WC-5), G4 outward-default-off (WC-9), G5 task confidence gate, G6 nested-depth fence, G7 pr-submit `--monitor` ordinal, G8 retry and circuit breaker (WC-6/CAPS), G9 contract-write condition (WC-4/SA-3). Input classes left out are named in the line under each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 readiness limit | SPEC:59 (WC-1) | Zero/Empty | no startup prompt | true (ready) | start passes, `state: ready` (CAPS:49) | OK |
| G1 readiness limit | SPEC:59 | Typical | prompt with 30 s fallback | true | passes at 34 s (CAPS:49) | OK |
| G1 readiness limit | SPEC:59 | Maximum/Overflow | fallback above about 45 s | false | fails at `agent_readiness` (CAPS:49); WC-1 says only "well inside the readiness limit", no number | GAP |
| G1 readiness limit | SPEC:59 | Legitimate Edge Case | coordinator raises `--timeout-ms` (CAPS:45) | true | WC-1 does not say whether a raised limit excuses a slower fallback | GAP |
| G2 wait split | SPEC:68 (WC-10) | Zero/Empty | no long wait | n/a (guard not triggered) | no action | OK |
| G2 wait split | SPEC:68 | Typical | one blocking call of 2 min | false | no split; heartbeat on schedule | OK |
| G2 wait split | SPEC:68, 114, 210 | Legitimate Edge Case | one blocking call of 4 to 5 min | false (trigger is "longer than 5 minutes") | WC-10 allows it; row 114 ("under 4 minutes") and AC-4.3 ("no single tool call exceeds 240 s") fail it | GAP |
| G2 wait split | SPEC:68 | Maximum/Overflow | 3600 s eval, 600 s cumulative poll budget | true | split into waits of at most 4 min | OK |
| G2 wait split | SPEC:114, 283 | Legitimate Edge Case | one unsplittable iteration above 4 min (poll script runtime unknown) | true | "confirm" only; no fallback if it cannot be split (UNVERIFIED 12) | GAP |
| G3 outcome mapping | SPEC:63 (WC-5) | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G3 outcome mapping | SPEC:63 | One/Minimal | `status: blocked` or `failed` | true | `--outcome failed` | OK |
| G3 outcome mapping | SPEC:63, 263 | Typical | `succeeded`, `partial`, audit verdict FAIL | false | `--outcome succeeded` | OK |
| G3 outcome mapping | SPEC:63 | Sentinel Value Match | report exists but `status` missing, malformed, or another vocabulary | false ("otherwise") | `--outcome succeeded` | GAP |
| G4 outward default off | SPEC:67 (WC-9) | Zero/Empty | command with no outward default | n/a | nothing to turn off | OK |
| G4 outward default off | SPEC:67, 100 | Typical | auggie-review PR posting | true | off under `--unattended`; turns on only with `--post-pr`, a flag no inventory shows (INV-A:38) | GAP |
| G4 outward default off | SPEC:67, 114, 241 | Legitimate Edge Case | pr-submit, whose default is outward (INV-B:94) | true | off, with no enabling flag named; AC-4.3 expects a PR | GAP |
| G4 outward default off | SPEC:67 | Sentinel Value Match | "paid external run" (research via Tavily, swarm) | undefined set | no list of covered commands | GAP |
| G5 task confidence | SPEC:121 | Zero/Empty | confidence 0 | true (below 0.70) | blocked | OK |
| G5 task confidence | SPEC:121 | Sentinel Value Match | exactly 0.70 | false | proceeds (inventory gate is "< 0.70", INV-B:199) | OK |
| G5 task confidence | SPEC:121 | Typical | 0.90 | false | proceeds | OK |
| G5 task confidence | SPEC:121 | Legitimate Edge Case | below 0.70 with `--compliance <tier>` supplied by the brief (the override the prompt offers, INV-B:199) | unspecified | WC-2 (b) lets a flag resolve a gate; the row says only "resolves as blocked" | GAP |
| G6 nested-depth fence | SPEC:33, 66 (R1, WC-8) | Zero/Empty | coordinator at depth 0 | false | may call `worker-start` (CAPS:97) | OK |
| G6 nested-depth fence | SPEC:33, 66 | Typical | worker at depth 1 calls `worker-start` | true | refused `nested_worker_depth_exceeded` (CAPS:99); call sites UNVERIFIED (CAPS:103) | OK |
| G6 nested-depth fence | SPEC:249-252 (D5) | Maximum/Overflow | setting raised above 1 | false | WC-8 still forbids a command from calling Orca | OK |
| G7 pr-submit ordinal | SPEC:114 | Zero/Empty | `--monitor 0` | unspecified | spec states only that 1 is refused and 3 is the default (INV-B:89) | GAP |
| G7 pr-submit ordinal | SPEC:114 | One/Minimal | `--monitor 1` | true | refused under `--unattended` | OK |
| G7 pr-submit ordinal | SPEC:114 | Legitimate Edge Case | `--monitor 2` | unspecified | no statement | GAP |
| G8 retry/circuit breaker | SPEC:64 (WC-6), CAPS:116, CAPS:80 | Zero/Empty | no earlier attempt | n/a | normal start | OK |
| G8 retry/circuit breaker | SPEC:63-64 | Maximum/Overflow | repeated `blocked` reports retried with `--retry-of` | false (a worker's own `failed` report does not count, CAPS:80) | no cap on re-dispatching a blocked Task | GAP |
| G9 contract-write condition | SPEC:62, 148 (WC-4, SA-3) | Typical | `--unattended` passed | true | contract written | OK |
| G9 contract-write condition | SPEC:62, 148 | Legitimate Edge Case | new output flag passed, `--unattended` absent | unspecified | WC-4 says unattended mode; SA-3 says "or when the caller passes the new output flag" | GAP |

Input classes left out, one line each: G1 One/Minimal (one prompt equals the typical row, WC-1 forbids any prompt); G1 Sentinel (the 60 s default is a default, not a control value); G2 One/Minimal and Sentinel (no value distinct from typical, no reserved value); G3 Maximum (the mapping has no count); G4 One/Minimal and Maximum (boolean per command); G5 One/Minimal and Maximum (1.0 equals typical); G6 One/Minimal and Sentinel (a depth setting, no count or reserved value; a malformed setting falls back to the default, CAPS:100, and the spec does not rely on it); G7 Typical, Maximum, Sentinel (the ordinal domain is 0 to 3 and rows above cover it); G8 One/Minimal, Typical and Sentinel (single retry equals the zero row for this rule; no reserved value); G9 Zero/Empty, One/Minimal, Maximum and Sentinel (a boolean switch). The GAP rows are graded under FR-8/FR-9: none names a wrong outcome an implementer produces from the stated text alone, so each is Medium or minor and is listed under follow-up candidates. Mapping: G1 to M-5; G2 to M-8 and m-8; G3 to M-4; G4 to M-2; G5 and G7 to m-11; G8 to M-1; G9 to m-5. (B-1 comes from the requirement text, not from a table row.)

## === REQUIREMENTS ANALYSIS ===

### B-1  MAJOR, blocking (Wiegers, with Adzic)  WC-4 path rule contradicts the commands and the acceptance checks it governs
- Location: SPEC:62 (WC-4), SPEC:73 (section 2.3), SPEC:83, 85, 87, 90, 92 (section 3.1 rows), SPEC:200 (AC-2.2).
- Grading check: an implementer who follows WC-4 as written builds `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" and "known before dispatch" (SPEC:62, 73), and that is wrong because the spec's own rows and checks give commands no such directory:
  - `/sc:tdd` and `/sc:init-lite` take `--output <file>` (SPEC:87, 90). WC-4 applied literally puts the contract under a regular file (`docs/x/TDD_X.md/return-contract.yaml`). AC-2.2 (SPEC:200) runs `/sc:tdd "auth" --unattended --output <file>` and requires a contract with `status: blocked`; nothing in WC-4 says where that contract is.
  - `/sc:workflow`'s contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92), an `<id>` the command generates, so the path is not known before dispatch; the same row demands the contract "for pre-creation STOPs too", when no package directory exists.
  - `/sc:cleanup-audit` has a fixed output directory and no output flag (SPEC:85); `/sc:adversarial` writes `<output>/adversarial/return-contract.yaml` (SPEC:83), not `<output-dir>/return-contract.yaml`.
  - The AC-2.2 example `/sc:cli-eval run --unattended` with no `--suite` (SPEC:200) passes no directory at all, and a gate that is blocked because a required flag is missing (post-release without `--output`, SPEC:113; missing `$1` in cli-eval, SPEC:104) has no `<output-dir>` to write into.
  Two stated texts contradict (WC-4 versus rows and AC-2.2), and AC-2.2 and 7.2 step 3 (SPEC:182, "its report path is the WC-4 contract path") cannot pass for tdd, workflow or the missing-flag cases. The spec itself concedes this once, for P0 only (F-2, SPEC:194); it never resolves it for P1 to P4.
- Recommendation: replace the single `<output-dir>` rule with one rule that every command can follow, for example a dedicated report-directory flag separate from file-valued `--output`, plus a stated location for a contract written before the directory is known (the working directory, named in the brief), and list in section 3 the contract path of each command that cannot use the rule (workflow, cleanup-audit, adversarial). Prefer narrowing WC-4 to one sentence over adding a table.
- Priority: High. Quality impact: Testability and Consistency, about +1.5 each.

### M-1  MAJOR label, Medium (Cockburn, Nygard)  `blocked` has no closing procedure
- Location: SPEC:60-63 (WC-2, WC-3, WC-4, WC-5), SPEC:73, SPEC:200.
- A command that resolves a gate as blocked writes the exact question and stops (SPEC:60); the worker "may" ask the coordinator once, re-invoke "with the answer as a flag" (SPEC:61), or end `failed` (SPEC:63). Missing: which of the two the worker does (AC-2.2 asserts `worker_done --outcome failed`, SPEC:200, which holds only if the worker chooses not to ask); which flag answers the question (the contract carries only `blocked_question`, SPEC:62); what the coordinator does with a `blocked` contract (answer, re-dispatch with `--retry-of`, CAPS:90, 116); and any bound on repeated blocked retries (CAPS:80 says a worker's own `failed` report does not count toward the circuit breaker).
- Grade: the finding is a procedure the document never states, not a stated text that does harm, so Medium.
- Recommendation: add `blocked_flag` and the allowed answer values to the contract fields, say "ends `failed`; the coordinator re-dispatches", and delete the "may ask" branch or make it the single path.

### M-2  Medium (Wiegers)  WC-9's enabling flags are undefined
- Location: SPEC:67, 100, 113, 114, 121, 244.
- WC-9 turns an outward default on "only through the command's own explicit flag written in the brief". `--post-pr` appears only in the spec (SPEC:100, 244); the inventories show only `--no-post-pr` (INV-A:38, 78). post-release, task and pr-submit are given no named enabling flag (SPEC:113, 114, 121; INV-B:85 asks for "explicit pre-authorization inputs"). pr-submit's default is itself outward (INV-B:94), so WC-9 switches the command off with nothing to switch it on, while AC-4.3 (SPEC:210) expects a PR. The auggie-review row lists "Other required change: none" (SPEC:100) while introducing a flag. WC-9 also leaves "paid external run" undefined and does not mention local destructive edits (see M-9).
- Recommendation: name each enabling flag in section 3 or state that the flag is created in the command's phase.

### M-3  Medium (Wiegers, Crispin)  Requirements without an acceptance check
- Location: SPEC:59, 61, 64, 68, 70 against SPEC:166-210.
- WC-1 (no prompt before readiness), WC-3 (ask path), WC-6 (retry safety: no check starts a `--retry-of` worker), WC-12 (check and `consumer_fenced`) and WC-10 for cli-eval have no check in section 7; WC-11 has one (AC-3.4, save only). Section 7 maps the other WC rules to a check.
- Recommendation: one line per uncovered rule, or an explicit "not tested, reason".

### M-4  Medium (Wiegers)  WC-5 and the status vocabulary
- Location: SPEC:62, 63, 183, 262, 263; INV-B:272.
- WC-4 says commands with a contract "keep their fields and add the missing ones" while `status` takes one of four values; the inventories show the existing vocabularies only for workflow (a `failed` value, INV-B:272), so reflect, brainstorm and adversarial may use other values for the same key, and 7.2 step 4 (SPEC:183) asserts the four values for every command. WC-5 maps "otherwise" to `succeeded`, so a report that exists but has no recognizable `status` yields success. `partial` is never defined per command, and it maps to `succeeded`, which makes the Task `completed` and its dependents ready (CAPS:77, 90).
- Recommendation: say that a missing or unrecognized `status` maps to `failed`, and add a `contract_version` field (workflow's contract already has a version, INV-B:272).

### M-5  Medium (Wiegers)  WC-1 has no number and no deliverable
- Location: SPEC:59, 156-162.
- "Well inside" is unquantified although the evidence has one (passes at 30 s, fails above about 45 s, CAPS:49). The owner is "Launch setup, not commands" and no phase delivers or checks a launch-setup change.

### M-6  Medium (Adzic)  Decision dependencies are stated inconsistently
- Location: SPEC:154, 225, 228, 73, 159, 244, 100, 121.
- SPEC:154 says "Phases 1-3 need no user decision"; SPEC:225 says Phases 0-3 proceed "on the recommendations"; D4 (SPEC:244) affects auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (SPEC:100, 121). D1(a) says the coordinator writes `--unattended` "into every worker's command line" (SPEC:228) while section 2.3 and P1 say only once the command's phase has landed (SPEC:73, 159), and brainstorm and init-lite never land a phase (see the diagram).

### M-7  Medium (Adzic, Cockburn)  Section 4's git row uses this run's rule as policy
- Location: SPEC:133, 67, 241, 245; README:31.
- SPEC:133 says "workers make no commits or pushes", citing README:31, which binds the workers of this planning run. D3(b), D4(a) and WC-9 (SPEC:67, 241, 245) let a pre-authorized worker push and open PRs. A reader takes the absolute from SPEC:133 and builds the opposite of the recommended D4(a).

### M-8  Medium (Crispin)  Acceptance population and trigger conditions
- Location: SPEC:195-196, 200, 85, 100, 103, 110, 116, 122.
- AC-1.1/AC-1.2 say "every command in the P1 row ... except load": 12 commands read literally, 8 built (see the diagram), and cleanup-audit has no `--output` (SPEC:85). AC-2.2 asks for a gate-trigger run "per P2 command" with `status: blocked`, but research, cleanup, improve, auggie-review and tasklist resolve their gates by a default or a flag (SPEC:100, 103, 110, 116, 122) and have no blocked path. WC-10 triggers only for a call "longer than 5 minutes" and then caps waits at 4 minutes (SPEC:68), while SPEC:114 and AC-4.3 (SPEC:210) fail any call over 240 s, so a compliant 4-to-5-minute call fails the check (guard G2).

## === ARCHITECTURE ANALYSIS ===

### M-9  Medium (Fowler, Whittaker)  Parallel safety covers default paths, not edits to the shared tree
- Location: SPEC:69 (WC-11), SPEC:73, SPEC:103, 110, 107; CAPS:115.
- WC-11 forbids two workers writing "the same file" through default output paths. Workers share the worktree by default (CAPS:115), and cleanup, improve, document, test `--fix` and implement edit source files (SPEC:103, 107, 110). The spec puts no duty on the coordinator's brief for disjoint targets or separate worktrees (section 2.3 lists "the worktree placement" only), and the rollback of cleanup and improve is UNVERIFIED (INV-A:43, 52). Two cleanup workers on overlapping directories, or one deleting files another worker has uncommitted, are not excluded. Requirement never stated, so Medium.

### M-10  Medium (Fowler)  Where `--unattended` takes effect
- Location: SPEC:52, 149, 176, 118, 122; INV-B:149, 210.
- Many gates sit in the skill, not the command (roadmap's "[Y/n]" at `sk/sc-roadmap-protocol/SKILL.md:433-438` per INV-B:149; tdd at `sk/tdd/SKILL.md:52-61`; review-translation at `sk/sc-review-translation-protocol/SKILL.md:44`). The contract adds a section to the command file (SPEC:52) and SA-4 and AC-C5 govern command-file edits only (SPEC:149, 176). Nothing says how the mode reaches the skill or a nested command (tdd to `/task`, workflow to reflect, brainstorm and release-split to adversarial, pr-submit to troubleshoot and auggie-review); the single stated propagation is tasklist to reflect (SPEC:122). The tasklist row also says reflect runs "one layer below the worker" (SPEC:122) while INV-B:210 and INV-B:314 record that reflect spawns its own agents and that nested spawning is UNVERIFIED, and the `needs_human_decision` HALT in Stage 10.5 (INV-B:209) is not resolved by any WC-2 rule.

### M-11  Medium (Nygard)  No stall policy on the coordinator side
- Location: SPEC:44, 73, 181-182; CAPS:111, 126, 188.
- The spec says the real failure of a command prompt is "a silent stall with no `worker_done`" (SPEC:44) and describes how to observe it (section 7.2) but sets no coordinator duty: no deadline, no escalation, no rule that silence never authorizes release or retry (CAPS:111, 126). Whether Orca bounds a Dispatch's run time is UNVERIFIED (CAPS:188, SPEC:282), and the 900000 ms `check --wait` of 7.2 step 3 is a test device, not a requirement.

### M-12  Medium (Newman, Hohpe)  Worker-session rules have no carrier
- Location: SPEC:52, 61, 63, 65, 70, 73.
- WC-3, WC-5, WC-7 and WC-12 are owned by the "worker session". Section 2.3 lists what the brief carries (command line, output directory, authorized outward actions, worktree) and omits the outcome mapping, the `ask` use and the `check` duty. The contract file is read by the command when its `## Unattended mode` section says so (SPEC:52), and the ready commands that never get that section (brainstorm, init-lite, SPEC:84, 87) never trigger the read.

### M-13  Medium (Nygard)  Preconditions of the acceptance runs
- Location: SPEC:52, 147, 158, 172, 178-186.
- The contract exists at `~/.claude/WORKER-CONTRACT.md` only after install (SPEC:52); the live checks never include installing it, so P1 onward runs in a dev worktree could not find it. AC-C1 (SPEC:172) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent`, while SA-2 allows an Orca example inside the contract file (SPEC:147) and P0 adds an Orca section to `HOW-WE-WORK.md` (SPEC:158); if either text names an Orca verb, P0 fails its own common check.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4, SPEC:62** ("written on every outcome, including stops before any other output exists") fails when **the caller passes no output directory**. Concrete attack: `/sc:cli-eval run --unattended` with no `--suite` (AC-2.2, SPEC:200). Before: no `<output-dir>`, no contract. The command resolves "blocked" (SPEC:104) and has nowhere to write. After: the worker sees "no report exists" and sends `--outcome failed` (SPEC:63), which matches the expected outcome while the expected `blocked_question` is unreadable. Feeds B-1. Severity as graded: blocking through B-1.
- I can break this specification by **Divergence Attack**. The invariant at **WC-10, SPEC:68 versus SPEC:114 and 210** fails when **a blocking call lasts 4 to 5 minutes**. Concrete attack: a pr-submit poll iteration of 270 s. WC-10 does not trigger (it needs "longer than 5 minutes"), the heartbeat stays on schedule, yet AC-4.3 (no single call over 240 s) fails the compliant run. Medium (guard table G2, folded into M-8).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4/WC-5, SPEC:62-63** fails when **an existing contract uses `status` for another vocabulary**. Concrete attack: a reflect contract carries `status: error` (vocabulary UNVERIFIED). WC-5 sends `--outcome succeeded` ("otherwise"); 7.2 step 4 (SPEC:183) fails the same file. Before: Task `dispatched`; after: Task `completed`, dependents ready (CAPS:77, 90). Medium (M-4).
- I can break this specification by **Sequence Attack**. The invariant at **WC-3/WC-5, SPEC:61, 63** fails when **the worker asks, gets an answer, and re-invokes**. Concrete attack: blocked contract written (`status: blocked`), `ask` answered, command re-run writes `status: succeeded` over the same path; the first `blocked` file is gone and nothing says whether one or two `worker_done` messages follow (WC-5 says exactly once). Medium (M-1).
- I can break this specification by **Accumulation Attack**. The invariant at **WC-6, SPEC:64** fails when **a blocked Task is retried without the answer**. Concrete attack: `blocked` maps to `failed`, `worker-start --retry-of` re-runs the command, the command blocks again; a worker's own `failed` report does not count toward the circuit breaker (CAPS:80), so the loop has no bound. Medium (M-1, G8).

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: M-1 to M-13 above (open and listed, not blocking). The session that ran this review did not ask the user whether to open an issue (no user in this sandbox, unattended-style run); the list is only recorded.

Minor notes:
- m-1  `F-1`, `F-2`, `F-3` are used as references (SPEC:73, 76, 159, 176, 193-196) with no definition in the document; a reader without the earlier review report cannot resolve them.
- m-2  UNVERIFIED item 14 (SPEC:285) is a verification claim ("9 defects ... fixed"), not an unverified item; the claim cannot be checked from the workspace.
- m-3  The commands in section 7 escape the pipe as `\|` inside table cells (SPEC:172, 175, 176, 193); copied from the raw file, `grep -E '...\|...'` treats it as a literal pipe, and AC-C1 then matches nothing and passes. The AC-C1 verb list also omits other Orca verbs (`status`, `open`, `skills`).
- m-4  7.2 step 5 (SPEC:184) searches the transcript for the string `AskUserQuestion`, which also matches the command text read into the transcript; it should look for a tool call.
- m-5  SA-3 (SPEC:148) says the new files are written "only in unattended mode or when the caller passes the new output flag", WC-4 says "in unattended mode" (SPEC:62); G9 in the guard table.
- m-6  `/sc:load` is counted among the 27 commands needing a change (SPEC:112) although the row says it is not dispatched as its own Task; the count is a triage count, not a work count.
- m-7  E2 (SPEC:22) says a worker has "the same tools as a command a person runs"; the cited line (EVIDENCE.md:45 via CAPS:49) shows only that the worker reached readiness.
- m-8  WC-10's premise for pr-submit rests on reading the 600 s default as a cumulative budget (SPEC:68, 114); INV-B:95 and INV-B:299 read it as "per wait". The spec's re-read list (SPEC:11) does not include `sk/sc-pr-submit-protocol/SKILL.md:46-64`, and the file is not in the workspace: UNVERIFIED. If the inventories are right, pr-submit as a worker violates WC-10 as written.
- m-9  Completeness of the 43 (that `cmd/` holds exactly these commands) is UNVERIFIED in the workspace. The reviewer's own session skill list also names `sc:graph`, `sc:impact` and `sc:issue` (the last described as creating an Orca worktree); that is not workspace evidence and is recorded only as a pointer. If correct, E5 (SPEC:25, no skill calls Orca today) and the "43" would need rechecking.
- m-10  The contract has no `contract_version` field although workflow's contract is versioned (INV-B:272).
- m-11  Unspecified guard values: pr-submit `--monitor 0` and `--monitor 2` under `--unattended` (SPEC:114; only 1 and the default 3 are discussed, INV-B:89), and task below 0.70 when the brief already passes `--compliance` (SPEC:121; INV-B:199).

## Scores (0 to 10)

Clarity 7, Completeness 6, Testability 6, Consistency 6. Evidence quality is high for the Orca facts and the per-command rows (most citations resolve in the inventories); the weakest area is the shared contract's path and carrier rules.

## Reviser brief

Blocking finding ids: B-1.

Rules for the reviser (restated from the command; the reviser reads this report, not the command):
- Revise only text a blocking finding names; here that is WC-4 (SPEC:62), its dependents in section 2.3 (SPEC:73) and the contract-path cells named in B-1, and AC-2.2 only if the new rule makes its example wrong.
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id (B-1).
- Prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave every Medium finding (M-1 to M-13) and every minor note (m-1 to m-11) alone; they are not part of this brief.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
