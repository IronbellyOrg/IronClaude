review: 1 of 3

# /sc:spec-panel review, round 1: Orca worker-contract spec

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  candidate_sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
  candidate_size: 285 lines, 57763 bytes
  baseline: none given (first review of the full document)
  prior_report: none (first review)
  reviewer_model: claude-sonnet-5-5 (Sonnet 5.5)
  mode: critique
  focus_areas: [requirements, architecture]
  panel_in_review_order: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe]
  brief_clauses_overridden: none
quality_assessment:   # 0-10, advisory only; verdict below is decided by blocking findings
  clarity: 7
  completeness: 6
  testability: 5
  consistency: 5
```

Citation key. `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (all read in full this run). Any `sk/...`, `cmd/...`, `src/...`, `CLAUDE.md:`, `pyproject.toml:`, `Makefile:`, `EVIDENCE.md:` or `.dev/codegraph-migration/...` line that the inventories do not quote is UNVERIFIED here, because those files are not inside the sandbox.

## Findings index

| id | grade | label | location | expert | status |
|---|---|---|---|---|---|
| F-1 | blocking | MAJOR | spec:159, spec:195 vs spec:60, spec:154, spec:162, spec:240 | Wiegers, Whittaker | open |
| F-2 | blocking | MAJOR | spec:176, spec:193 (AC-C5, AC-0.3) | Adzic, Whittaker | open |
| F-3 | blocking | MAJOR | spec:180, spec:73 vs spec:158-159, spec:182, spec:194 (AC-0.4) | Adzic, Wiegers | open |
| M-1 | Medium | MAJOR | spec:64, spec:73, spec:205 (WC-6) | Nygard | open |
| M-2 | Medium | MAJOR | spec:65, spec:68, spec:210 (WC-7, WC-10, AC-4.3) | Nygard, Whittaker | open |
| M-3 | Medium | MAJOR | spec:62 (WC-4) | Wiegers, Fowler | open |
| M-4 | Medium | MAJOR | spec:63, spec:263, spec:73 (WC-5, 2.3) | Cockburn, Hohpe | open |
| M-5 | Medium | MAJOR | spec:61, spec:200 (WC-3, AC-2.2) | Adzic | open |
| M-6 | Medium | MAJOR | spec:62, spec:261, spec:183 (WC-4, AC status check) | Fowler, Newman | open |
| M-7 | Medium | MINOR | spec:172 vs spec:147, spec:150 (AC-C1, SA-2) | Newman | open |
| M-8 | Medium | MAJOR | spec:44, spec:73, spec:180-182 (coordinator side) | Nygard, Cockburn | open |
| M-9 | Medium | MAJOR | spec:88, spec:122, spec:151, spec:280 | Nygard, Whittaker | open |
| M-10 | Medium | MINOR | spec:118, spec:124, spec:204 (P3 "reconcile") | Wiegers | open |
| M-11 | Medium | MINOR | spec:69 vs spec:85-86 (WC-11) | Whittaker | open |
| M-12 | Medium | MINOR | spec:60 (WC-2), flag-combination rule | Whittaker | open |
| N-1 | minor | MINOR | spec:133 | Wiegers | note |
| N-2 | minor | MINOR | spec:285 | Wiegers | note |
| N-3 | minor | MINOR | spec:51 | Cockburn | note |
| N-4 | minor | MINOR | spec:52, spec:195 | Newman | note |
| N-5 | minor | MINOR | spec:184 | Adzic | note |

Blocking findings open: F-1, F-2, F-3.

## What was covered

- Read in full: `README.md`, the candidate (285 lines), `inventory/orca-capabilities.md`, `inventory/commands-a.md`, `inventory/commands-b.md`. The `~/.claude/rules/prompts/document_review_loop_prompts.md` FIRST-REVIEW prompt was read in full and followed (grading check applied to every finding below).
- Requirements focus: WC-1 to WC-12 (spec:57-70), section 2.3, SA-1 to SA-6, the per-command rows of 3.1 and 3.2 (spec:81-125), section 4, the acceptance checks of section 7, the open decisions D1 to D5.
- Architecture focus: the coordinator/worker split (section 1), the rejected alternative R1 to R5 (spec:31-37), the contract-file design, the phase order (section 6), the nesting and heartbeat interplay.
- Citation spot-check against the inventories: E1 to E6 (spec:21-26), R1 to R5 (spec:33-37), the WC evidence column and the 3.1/3.2 `INV-*` cites matched the text the inventories quote. The 43 = 10 + 27 + 6 split (spec:76) re-counts correctly from INV-A:33-55 and INV-B:29-52 (10 ready, 27 needs-change, 6 coordinator-only), and the 3.1 and 3.2 rows list exactly those commands. Phase lists (spec:159-162) name 35 of the 37 worker commands; `brainstorm` and `init-lite` appear only through the generic "every command in 3.1 and 3.2" clause of P1. No count mismatch needs a Quantity Flow Diagram (Pipeline Dimensional Analysis is not triggered: the spec describes a rollout plan, not a multi-stage data pipeline).
- Not covered: the real behaviour of any command or of Orca (no source files outside the inventories are checkable); `--focus correctness` was not requested, so no State Variable Registry is produced.
- Follow-up candidates (Medium and minor) are listed at the end. The coordinator-side question "open an issue for them?" is not asked in this run because the brief fixes the final reply format; no issue was created.

=== REQUIREMENTS ANALYSIS ===

### F-1 (blocking, MAJOR): `--unattended` availability and guarantee are stated three incompatible ways; P1 gives it to commands whose gates are not resolved until P2-P4
- Expert: Wiegers (consistency of requirements), Whittaker (Sequence Attack).
- Evidence. WC-2 says that under `--unattended` the command "never calls `AskUserQuestion`, never ends its turn on a chat question ... never says STOP AND WAIT" (spec:60). P1 says the phase delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (spec:159), and AC-1.1 requires every command in 3.1 and 3.2 to have an `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (spec:195). But the gate resolutions that WC-2 demands arrive later: P2 for 15 commands (spec:160), P3 for 4 (spec:161), P4 for implement, post-release and pr-submit (spec:162), and spec:154 says "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4". The section a command gains lists "only its own gate resolutions" (spec:52); for implement, post-release and pr-submit those resolutions depend on D2, D3 and D4 (spec:109, 113, 114), and under D3(a), the recommended option, "no pr-submit changes in Phase 4" (spec:240) while AC-1.1 still requires a pr-submit section.
- Grading sentence. An implementer who follows P1 and AC-1.1 as written gives roughly 22 gate-bearing commands (for example `task`, `auggie-review`, `roadmap`, `implement`, `pr-submit`) an `--unattended` flag and an `## Unattended mode` section in P1, and the result is wrong because those commands then accept `--unattended`, pass AC-1.1, yet still prompt or wait on a person until P2 to P4, which is the silent stall WC-2 and spec:44 say the contract exists to prevent; for the P4 commands P1 would also have to write D2 to D4 outcomes that spec:154 says are not decided. AC-1.2 live-checks only the 13 P1 commands (spec:159, 196), so nothing in P1 catches it.
- Recommendation: state per phase which commands gain the flag and the section, and make the flag exist on a command only in the phase that resolves all of that command's gates; restrict AC-1.1 to the commands of that phase. Rationale: it removes the P1 contradiction by narrowing, not by adding mechanism, and keeps spec:154 true.
- Priority: High. Quality impact: Consistency +2, Testability +1.

### F-3 (blocking, MAJOR): AC-0.4, the live smoke check whose failure "reopens section 1", cannot pass as written
- Expert: Adzic (testable examples), Wiegers (traceability).
- Evidence. P0 smoke-runs troubleshoot, workflow and adversarial "invoked directly" before any command edit (spec:158, 194); the flag `--unattended` and the WC-4 contract arrive in P1 (spec:159, 79). Step 1 of the live check says "task-create --spec \"<brief per section 2.3>\"" (spec:180), and section 2.3 says the brief states "the exact command line including `--unattended`" (spec:73). Step 3 requires the `--outcome` to match "the contract's `status` under WC-5" and the report path to be "the WC-4 contract path" (spec:182). AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file" (spec:194), so only step 4 is relaxed. In P0 troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242, and spec:91 names `REPORT.md`), adversarial's contract filename is "not fixed" (spec:83; INV-A:35, INV-A:60), and spec:79 says the worker "reports the named file until Phase 1 adds the contract". AC-0.4 ends: "a failure here reopens section 1" (spec:194).
- Grading sentence. An implementer who follows step 1 with section 2.3 builds a P0 brief containing `--unattended`, which none of the three commands accepts before P1, and who follows step 3 looks for a WC-4 contract and a contract `status` that troubleshoot does not write, and the result is wrong because the check the spec uses to validate its own central decision (spec:194) fails or tests a non-existent flag, for a reason unrelated to whether Orca can run commands as workers.
- Recommendation: for P0 only, say the brief omits `--unattended` and step 3 compares the outcome with the command's existing report instead of the WC-4 contract. Rationale: narrowing AC-0.4's text to what P0 can produce; no new mechanism.
- Priority: High. Quality impact: Testability +2.

### M-1 (Medium, MAJOR label): retry and re-run safety (WC-6) leaves "fresh directory" without an owner, and no retry-brief rule or stale-contract rule exists
- Expert: Nygard (failure and recovery).
- Evidence. WC-6: a command without a resume flag "writes each run into a fresh output directory" (spec:64), but WC-4 and section 2.3 fix the contract at `<output-dir>/return-contract.yaml` in the directory the coordinator passes "so the report path is known before dispatch" (spec:62, 73). A command-created fresh subdirectory would make the path unknown; a coordinator-supplied directory is not stated for retries. AC-3.2 requires a run with an existing `<dir>/.session-memory.md` and no resume flag to "start fresh" in that same directory (spec:205). Orca's retry reuses the same Task (`--retry-of`, CAPS:116).
- Grading sentence. The guess needed: whether the coordinator or the command creates the fresh directory and whether the retry brief repeats the old `--output`. Two readings are allowed, so this is Medium, not blocking.
- Recommendation: one sentence in 2.3 saying each retry brief passes a new output directory or the command's resume flag, and that a command replaces an existing `return-contract.yaml` at start. Rationale: closes the stale-contract case (a retry that dies early leaves the first attempt's contract, so WC-5's "no report exists" test and step 4 of 7.2 cannot detect it).
- Priority: Medium.

### M-3 (Medium, MAJOR label): WC-4 gives no contract location when `--output` is a file, absent, or a fixed path
- Expert: Wiegers, Fowler (interface).
- Evidence. WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62). Rows pass `--output <file>` for tdd and init-lite (spec:87, 90), name no output flag for research (spec:116: contract naming `claudedocs/research_*.md`), recommend (spec:115), and keep fixed paths for cleanup-audit and index-repo (spec:85, 86). WC-4 also requires the contract "including stops before any other output exists" (spec:62), which needs a directory even when none was given. No text says where the contract goes in these cases.
- Grading sentence. The guess needed: for tdd the implementer may write `return-contract.yaml` beside the TDD in the shared `docs/[domain]/` folder, where two workers' contracts collide (spec:69, WC-11); or elsewhere. Medium.
- Recommendation: add the rule for the file-valued and missing cases (for example a required `--report-dir`) or list the exception per row. Rationale: the single fixed name was chosen so the coordinator checks every worker the same way (spec:261); that fails without a location rule.
- Priority: Medium.

### M-4 (Medium, MAJOR label): `partial` and an audit FAIL map to `succeeded`, which completes the Task and makes dependents ready; section 2.3 gives the coordinator no duty to check the status first
- Expert: Cockburn (coordinator goal), Hohpe (message semantics).
- Evidence. WC-5 sends `--outcome succeeded` for `partial` and for an audit whose verdict is FAIL (spec:63; rationale spec:263). Orca marks a succeeded Task completed and "a failed or cancelled Task keeps dependents blocked" (CAPS:90); the ready view is the coordinator's "external memory" (CAPS:86). Section 2.3 says only that the coordinator "opens the report file, then releases or reuses the worker" (spec:73).
- Grading sentence. The guess needed: that the coordinator reads the body's first sentence before starting dependents; a coordinator that works from the ready list starts a dependent on a partial deliverable. Medium.
- Recommendation: add to 2.3 that the coordinator reads the contract `status` before it starts any dependent Task, and what it does for `partial` and `blocked`. Rationale: the mapping is a deliberate decision (spec:263); the missing half is the reader's rule.
- Priority: Medium.

### M-5 (Medium, MAJOR label): WC-3 makes `ask` optional, while AC-2.2 assumes the blocked-and-fail path
- Expert: Adzic.
- Evidence. WC-3: the session "may instead ask the coordinator once" (spec:61). AC-2.2 expects, for a gate-trigger input, "`worker_done --outcome failed`; contract `status: blocked`" (spec:200).
- Grading sentence. A conforming worker that chooses `ask` leaves AC-2.2 waiting for a `worker_done` that comes only after the coordinator replies; which choice the worker makes is not fixed by the brief (spec:73 lists no such field). Medium (two readings allowed).
- Recommendation: make the choice a brief field, or state the AC-2.2 run uses the no-`ask` path. Rationale: keeps the acceptance run deterministic.
- Priority: Medium.

### M-6 (Medium, MAJOR label): "keep their fields" and the fixed four-value status set can contradict for the contracts that already exist
- Expert: Fowler (interface consistency), Newman (versioning).
- Evidence. WC-4: "Commands that already write a contract keep their fields and add the missing ones" (spec:62); the Decision table fixes `succeeded / partial / failed / blocked` (spec:262), and 7.2 step 4 asserts `status` is in that set (spec:183). The spec cites four commands that already write `return-contract.yaml` (spec:261) but never states their current `status` values; the inventories give only that workflow's contract has a `status` field with `failed` among its outcomes (INV-B:272). WC-4 also does not say whether an empty `blocked_question` is valid, while AC-2.2 needs it non-empty (spec:200).
- Grading sentence. If an existing contract uses different status words, the stated "keep" and "fixed set" cannot both hold. Whether they differ is not in the evidence, so Medium.
- Recommendation: list the existing status words next to WC-4, or say the coordinator maps them. Rationale: step 4 of 7.2 would otherwise fail correct existing contracts.
- Priority: Medium.

### M-10 (Medium, MINOR label): the P3 "reconcile" items name no winning side
- Expert: Wiegers.
- Evidence. roadmap and validate-roadmap rows say "reconcile" (spec:118, 124); AC-3.1 asserts the two files agree (spec:204). The inventory records that "no file in scope says which side wins" (INV-B:309).
- Grading sentence. The guess needed is which side an implementer keeps; SA-1 forbids changing standalone behaviour (spec:146), SA-4 allows defect fixes (spec:149), so either direction can be argued. Medium.
- Recommendation: name the source of truth per pair. Priority: Low.

### M-12 (Medium, MINOR label): no precedence rule for `--unattended` combined with `--interactive`, or for an empty flag value
- Expert: Whittaker (Divergence Attack: both branches apply at once).
- Evidence. Some rows refuse `--interactive` under `--unattended` (cleanup, improve, roadmap, spec-panel `target_release` flag: spec:103, 110, 118, 120), others only say the brief never passes it (adversarial, brainstorm, release-split: spec:83, 84, 89). WC-2 states no general rule (spec:60).
- Grading sentence. The guess needed: a person or brief passing both flags to adversarial or brainstorm gets undefined behaviour. Medium.
- Recommendation: one sentence in WC-2 saying `--unattended` wins and `--interactive` is refused. Priority: Low.

=== ARCHITECTURE ANALYSIS ===

### F-2 (blocking, MAJOR): the "additive edits" checks AC-C5 and AC-0.3 cannot detect a deleted or rewritten bullet line
- Expert: Adzic (an executable example), Whittaker (Zero/Empty Attack on the check).
- Evidence. AC-C5 passes when `git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'` "prints nothing: edits are additive" (spec:176); AC-0.3 uses the same filter on `HOW-WE-WORK.md` for "no existing routing row changed" (spec:193). A deleted markdown bullet `- Will Not: edit files` appears in a diff as `-- Will Not: edit files`, whose second character is `-`, so `^-[^-]` skips it, as it skips a deleted `---` frontmatter line. Command and skill files are mostly bullets (the spec's own quotes, for example spec:60, 187). Run in the sandbox this review: `printf -- '--- a/x.md\n+++ b/x.md\n@@ -3 +3 @@\n-- Will Not: edit files\n+- Will Not: edit files unless asked\n-| row | old |\n+| row | new |\n' | grep -E '^-[^-]'` printed only `-| row | old |`; the bullet deletion printed nothing.
- Grading sentence. An implementer who runs AC-C5 as written gets an empty output (a pass) after rewriting an existing bullet such as a `Will Not` line, and the result is wrong because AC-C5 and AC-0.3 are the only mechanical guards for SA-1, SA-4 and SA-5 (spec:146, 149, 150), so the standalone-unchanged guarantee the spec calls a "hard requirement on every phase" (spec:142) is unenforced for the commonest line type.
- Recommendation: replace the filter with one that excludes only the `--- a/` header, for example `grep -E '^-' | grep -vE '^--- (a/|/dev/null)'`, or count deletions with `git diff --numstat`. Rationale: a one-line correction of the stated command.
- Priority: High. Quality impact: Testability +2.

### M-2 (Medium, MAJOR label): foreground Agent-tool fan-out blocks the only session allowed to heartbeat, and WC-10 splits only polls and evals
- Expert: Nygard (liveness), Whittaker (Accumulation Attack on a wait budget).
- Evidence. WC-7: subagents never send lifecycle messages (spec:65). WC-10: the worker heartbeats every 5 minutes; only "a poll wait, a long eval" must be split into waits of at most 4 minutes (spec:68). Many commands fan out for long periods inside one session (troubleshoot Tier 2 with 2 to 4 agents plus adversarial and validator: INV-B:241; adversarial Mode B with 2 to 10 generators: INV-A:35; cleanup-audit waves of 7 to 8 agents: INV-A:42). While a foreground Agent call runs, the top-level session cannot send a heartbeat. AC-4.3 requires "no single tool call exceeds 240 s" for pr-submit (spec:210), yet pr-submit dispatches a troubleshoot fan-out per verified finding (INV-B:91; spec:114).
- Grading sentence. The guess needed: whether a missing heartbeat during fan-out matters. Whether Orca uses heartbeat age in its liveness verdict is itself UNVERIFIED (CAPS:130, CAPS:182), so no concrete wrong outcome is established. Medium. AC-4.3 applies only if the non-recommended D3(b) is chosen (spec:241, 242).
- Recommendation: state that WC-10 binds only commands whose single step the command controls, and that fan-out waits are exempt, or require background agents plus polling. Priority: Medium.

### M-7 (Medium, MINOR label): AC-C1 scans `src/superclaude/core`, but SA-2 limits the Orca ban to commands, skills and agents
- Expert: Newman (boundary).
- Evidence. SA-2: "No command, skill or agent file runs an `orca` or `orca-ide` command" and allows an Orca mention in the contract file (spec:147). AC-C1's grep covers `src/superclaude/core` too and must print nothing "(SA-2, WC-8)" (spec:172). The P0 deliverables are a core contract file with a coordinator brief template and an Orca section in `HOW-WE-WORK.md`, a core file (spec:158, 150).
- Grading sentence. If either core file names an `orca orchestration ...` command, which the Orca section of a routing guide plausibly does, AC-C1 fails a conforming P0 and "a phase passes only when every check ... passes" (spec:167). That depends on the wording the implementer picks. Medium.
- Recommendation: make AC-C1 exclude the two core files, or say they must avoid the command words. Priority: Low.

### M-8 (Medium, MAJOR label): the coordinator has no stated stall, timeout or retry policy
- Expert: Nygard, Cockburn.
- Evidence. Section 1.4 says the real failure for a command prompt is "a silent stall with no `worker_done`", visible "only through `worker-show`'s `agentWait` or a missing report" (spec:44), but a missing report is visible only after `worker_done`. Section 2.3 lists only what the brief must say and what happens after `worker_done` (spec:73). The `worker-show` cadence appears only as a test step (spec:181). Orca's bound on a Dispatch's run time is UNVERIFIED (spec:282; CAPS:188), and a worker's own `failed` report does not count toward the three-failure circuit breaker (CAPS:80), so a blocked-then-retry loop has no stop.
- Grading sentence. The guess needed: how long the coordinator waits and how many blocked retries it makes. Medium (requirement not stated).
- Recommendation: add two sentences to 2.3 (poll `worker-show` at the WC-10 cadence; cap blocked retries). Priority: Medium.

### M-9 (Medium, MAJOR label): under `--unattended`, tasklist makes reflect auto-accept its remediation hand-off, and the nested-spawning risk the inventories flag is missing from the UNVERIFIED list
- Expert: Nygard, Whittaker.
- Evidence. The tasklist row has Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies" and calls the reflect fan-out "inside Claude Code's nesting limit, INV-A:14" (spec:122). The headless rule auto-accepts remediation for auto-fixable registers (INV-B:109), and Stage 10.5 already passes `--remediate` (INV-B:209), so one tasklist run can start N remediation hand-offs. The inventory recommended dropping `--remediate` in 10.5 (INV-B:215) and marks nested spawning inside those subagents UNVERIFIED (INV-B:210, 314, 322); the spec's UNVERIFIED list (spec:271-285) does not carry that item, and item 9 (spec:280) says only that an Orca worker is assumed not headless. The reflect row also changes `--remediate` behaviour under `--unattended` (spec:88) against SA-6's "reuses it" (spec:151).
- Grading sentence. The guess needed: that auto-accepted remediation under tasklist is wanted and that nested reflect agents can spawn. Medium.
- Recommendation: decide whether Stage 10.5 drops `--remediate` under `--unattended`, and add the nested-spawn item to the UNVERIFIED list. Priority: Medium.

### M-11 (Medium, MINOR label): WC-11 says "must never" write the same file, but cleanup-audit and index-repo keep fixed output paths
- Expert: Whittaker.
- Evidence. WC-11: "Two workers in one worktree must never write the same file" (spec:69). The cleanup-audit row concedes "output dir is fixed, so one audit per worktree at a time (WC-11)" (spec:85); index-repo writes `PROJECT_INDEX.md` at a fixed location (spec:86; INV-A:53). Section 2.3 does not tell the coordinator to serialise such Tasks (spec:73).
- Grading sentence. The guess needed: that the coordinator serialises them. Medium.
- Recommendation: add the serialisation duty to 2.3 or give both commands an output flag. Priority: Low.

## Guard Condition Boundary Table

Trigger: the spec contains conditional logic and thresholds (wait split, outcome mapping, gate resolution, additive-diff check, depth fence). Construction by Nygard, completeness by Crispin-style review (Wiegers here), attack by Whittaker. The 7 columns follow the command's template; input classes that cannot occur for a guard are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 split rule | spec:68 | Zero/Empty | no blocking step | false | no split needed | OK |
| WC-10 split rule | spec:68 | Typical | 60 s poll | false | worker heartbeats between calls | OK |
| WC-10 split rule | spec:68 | Maximum/Overflow | foreground Agent-tool fan-out of 8 min | not covered | rule names only "a poll wait, a long eval"; subagents may not heartbeat (spec:65) | GAP (M-2) |
| WC-10 split rule | spec:68 | Legitimate Edge Case | one call of 4 min 50 s | false (not over 5 min) | unsplit; heartbeat still falls between calls | OK |
| WC-4 output dir | spec:62 | Zero/Empty | `--unattended` with no directory given | unspecified | none stated | GAP (M-3) |
| WC-4 output dir | spec:62 | Typical | directory passed | true | `<dir>/return-contract.yaml` written on every outcome | OK |
| WC-4 output dir | spec:62 | Legitimate Edge Case | `--output` is a file (tdd, init-lite) or a fixed path | unspecified | none stated | GAP (M-3, M-11) |
| WC-4 output dir | spec:62 | Sentinel Value Match | directory already holds a `return-contract.yaml` from a prior attempt | unspecified | none stated | GAP (M-1) |
| WC-5 outcome map | spec:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| WC-5 outcome map | spec:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| WC-5 outcome map | spec:63 | Legitimate Edge Case | `status: partial` or audit verdict FAIL | true | `--outcome succeeded`, body names the status; dependents then ready | OK as specified; coordinator side GAP (M-4) |
| WC-5 outcome map | spec:63 | Sentinel Value Match | `status` outside the four words, or empty `blocked_question` | unspecified | none stated | GAP (M-6) |
| WC-2 gate rule | spec:60 | Typical | gate with documented default | true | default used | OK |
| WC-2 gate rule | spec:60 | Legitimate Edge Case | `--unattended` with `--interactive`, or empty flag value | unspecified | rows differ; no general rule | GAP (M-12) |
| WC-3 ask | spec:61 | Legitimate Edge Case | gate blocked, worker holds a preamble | true | "may" ask or report blocked | GAP (M-5) |
| AC-C5 additive check | spec:176 | Zero/Empty | no deleted lines | true (prints nothing) | pass | OK |
| AC-C5 additive check | spec:176 | Typical | deleted table row | false (prints the row) | fail | OK |
| AC-C5 additive check | spec:176 | Legitimate Edge Case | deleted or rewritten bullet or `---` line | true (prints nothing) | pass, although the edit is not additive | GAP (F-2) |
| Depth fence | spec:33, CAPS:97-100 | Typical | depth 1, worker calls `worker-start` | refused | WC-8 forbids the call | OK |
| Depth fence | spec:33, CAPS:97-100 | Legitimate Edge Case | malformed or raised setting | falls back to 1 / R1 no longer holds | CAPS:100 covers malformed; raised depth is D5(b), not recommended | OK |
| Retry breaker | spec:64, CAPS:80 | Maximum/Overflow | repeated blocked reports then retry | not counted | no cap stated | GAP (M-8) |

Left out: a Sentinel row for WC-10 (no sentinel value exists in that rule); a Maximum row for the depth fence (the setting is a small integer with a documented fallback, CAPS:100). Completion: every cell is filled and every guard is enumerated; FR-10 satisfied. Every GAP above is graded in a finding: Medium where no concrete wrong outcome holds without a guess (M-1 to M-12), blocking for F-2.

## Adversarial notes (Whittaker, additional attacks that did not become findings)

- Sequence Attack on 7.2: step 7 releases only after settlement, but step 3 allows "exactly one `worker_done`"; a `consumer_fenced` worker (WC-12, spec:70) sends none, so step 3 hangs. The inventory documents the signal (CAPS:67); this is an acceptance-run gap covered by M-8.
- Divergence Attack on D1: option (a) is a flag the coordinator writes; if a person copies a brief, the flag travels with it. This is acceptable and noted in D1's own text (spec:228).

## Consensus and disagreements

- All panel members agree the central decision (Orca on top, commands unchanged as units) is well supported by the inventories (E1 to E6, R1 to R5 match the quoted capability lines), and that section 1.4 states its own evidence gaps honestly.
- Wiegers and Adzic weight the acceptance checks heavily (F-2, F-3). Nygard weighs the liveness and recovery gaps (M-1, M-2, M-8) as the architecture risk, graded Medium because each needs a guess about the worse reading.

## Minor notes

- N-1 (spec:133): the git row says most operations "need the user's authorization in this repo" and cites `README.md:31`, which is a rule for workers of this planning run only (`README.md:31`, verified). INV-A:91 words it the same way; the claim for the repository at large rests on UNVERIFIED sources.
- N-2 (spec:285): item 14 is a statement of a past independent check placed under "UNVERIFIED items"; the "about 340 citations" count cannot be checked from the inventories. Move or label it.
- N-3 (spec:51): "the only command-side change the contract asks for besides report files and resume" understates section 3, which also adds a `--resume` flag to cli-portify (spec:105) and a Write tool to explain (spec:108).
- N-4 (spec:52, spec:195): commands are told to point only at `~/.claude/WORKER-CONTRACT.md`. The project's dual-surface rule for installed primitives (project instructions, not in the sandbox, UNVERIFIED) asks primitives to name both the installed and the project copy; check it before P1.
- N-5 (spec:184): "search the transcript for `AskUserQuestion`" will also match prompt or file text that merely mentions the word; the pass condition says "no `AskUserQuestion` call", so search for tool-call records.

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11, M-12 (descriptions above).
Minor: N-1, N-2, N-3, N-4, N-5.
No issue opened; none of these triggers a revision.

## Reviser brief

Blocking finding ids: F-1, F-2, F-3.

Reviser rules (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the spec before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
