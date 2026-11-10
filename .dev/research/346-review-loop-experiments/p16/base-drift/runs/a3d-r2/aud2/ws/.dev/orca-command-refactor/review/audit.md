review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (labelled whole-document audit, first review)

- Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `0c0dfe399e2121731d70aeb7cfd72ce90647f551183721fbf9e5d10ed5273f3a`
- Baseline: none given, none needed (first review of the whole document). No `--re-review` file, so no prior-findings table.
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full at lines 1-55 before reviewing).
- Brief clauses overridden: none.
- Citation conventions: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: the candidate (286 lines), the README, all three inventories, and `command.md`.
- Checked every `INV-A`, `INV-B` and `CAPS` citation the candidate makes against those three files (SPEC:21-45, 59-70, 83-125, 132-137, 261-269). Each cited inventory line exists and says what the candidate says it says. The one exception is in the Medium findings below.
- Re-derived the 43 = 10 + 27 + 6 split (SPEC:76) from the two inventory summaries (INV-A:73 gives 5/13/3, INV-B:278 gives 5/14/3, sum 10/27/6). Section 3.1 lists 10 rows (SPEC:83-92), section 3.2 lists 27 rows (SPEC:99-125), section 4 lists 6 (SPEC:132-137). The counts hold.
- Not covered: nothing outside the sandbox. Every citation to `src/superclaude/...`, `CLAUDE.md`, `.dev/evals/...`, `.dev/codegraph-migration/...` and `Makefile` is UNVERIFIED here (see the last section). Where the candidate carries such a line through an inventory, I checked only that the inventory says it.

## Tally

- Blocking findings: 0 (no CRITICAL; no MAJOR or FR-8/FR-9 finding meets the grading check).
- Medium (warnings, listed under follow-up candidates): 11.
- Minor notes: 7.

Grading check applied to every finding: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is blocking only when that sentence holds with no extra guess (two stated texts that contradict, a stated text that causes data loss or breaks a security or safety boundary, or a stated text an acceptance criterion cannot pass). Each Medium below needs one guess, usually that the implementer picks the worse of two readings the text allows, or is a requirement the document does not state. I considered M1 and M5 for blocking and graded them down for that reason (the reason is given under each).

## Expert panel (review sequence per `command.md`, filtered to the two focus areas plus the always-on Whittaker pass)

Active: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Nygard, Newman, Hohpe; Whittaker (always active). Crispin, Gregory and Hightower are outside the `requirements,architecture` focus and did not review. Correctness focus is not active, so the State Variable Registry is not produced. The Guard Condition Boundary Table is triggered by the spec's thresholds and conditionals and is produced below. Pipeline Dimensional Analysis is not triggered: the spec has no multi-stage data flow with count divergence beyond the command partition, which is checked above and below.

=== REQUIREMENTS ANALYSIS ===

### R-M1. Report-path rule (WC-4) is contradicted by the spec's own rows for adversarial, workflow and research
- Severity: MAJOR label, graded **Medium** (see grading note). Expert: Wiegers (lead), Adzic. Priority: High. Quality impact: Testability and Consistency, about -1.0 each.
- Evidence: WC-4 says the contract is `<output-dir>/return-contract.yaml` and is "known before dispatch" (SPEC:62; SPEC:73 repeats it for the brief). Three rows say otherwise:
  - adversarial: the fixed path becomes `<output>/adversarial/return-contract.yaml` (SPEC:83; INV-A:35, INV-A:60 show real runs wrote it in two different nesting depths).
  - workflow: `.dev/tasks/to-do/<id>/return-contract.yaml` (SPEC:92). The `<id>` is generated at run time (INV-B:272), and the package directory does not exist at a pre-creation STOP (INV-B:272 says the contract "is not written for pre-creation STOPs"). The only fix the spec names is "write the contract for pre-creation STOPs too" (SPEC:92) with no location.
  - research: "contract naming the generated `claudedocs/research_*.md` path" (SPEC:116). The contract has no stated location, and the command gets no output flag in this row (INV-B:132 shows the report name is generated at run time).
- Why it matters: A coordinator that computes `<out>/return-contract.yaml` per WC-4, finds nothing, and applies WC-5 ("or no report exists" gives `--outcome failed`, SPEC:63) marks a successful adversarial or workflow run failed.
- Grading note: this needs the guess that the coordinator ignores the per-command rows at SPEC:83 and SPEC:92. The rows are explicit, so a careful implementer will use them. Hence Medium, not blocking. The pre-creation-STOP location for workflow has no stated answer at all (a missing requirement).
- Recommendation: state in WC-4 that the path is `<output-dir>/return-contract.yaml` except where section 3 names a different fixed path, list those exceptions in one place, and give the workflow pre-creation STOP and research contracts a location the coordinator can know before dispatch.

### R-M2. `--unattended` without an output directory is unspecified
- Severity: MAJOR label, **Medium** (FR-9 blank behavior). Expert: Wiegers, Whittaker (Zero/Empty attack). Priority: Medium.
- Evidence: WC-4 requires the coordinator to pass the directory (SPEC:62, SPEC:73) but does not say what a command does when `--unattended` arrives with no output flag. Commands with a default location (reflect `.dev/reflect/...`, INV-B:112; auggie-review `.dev/reviews/...`, INV-A:38) would write there, and the coordinator would not know where to look.
- Wrong outcome an implementer could produce: a contract at a default path the coordinator never reads. Needs the guess that the implementer picks the default over refusing.
- Recommendation: one sentence in WC-4: without a stated output location under `--unattended`, the command resolves as blocked (WC-2 c), as the spec already does for other missing inputs (SPEC:104, SPEC:113).

### R-M3. "Fresh output directory" (WC-6) does not say who makes it fresh
- Severity: MAJOR label, **Medium**. Expert: Wiegers, Nygard. Priority: High.
- Evidence: WC-6 says a command with no resume flag "writes each run into a fresh output directory" (SPEC:64), and 20-plus rows say "fresh dir" (SPEC:99-125). WC-4 and section 2.3 say the coordinator passes the directory (SPEC:62, SPEC:73). A retry worker started with `--retry-of` gets the same brief unless the coordinator changes it.
- Two readings: (a) the command makes a new subdirectory, so the contract lands at `<output-dir>/<new>/return-contract.yaml` and WC-4's path is wrong; (b) the coordinator passes a new directory per Dispatch, and the spec never tells it to. Under a third reading the same directory is reused and the first attempt's output is overwritten, which WC-6 exists to prevent.
- Recommendation: add to section 2.3 that the coordinator passes a directory unique to the Dispatch, and say a command refuses (blocked) a non-empty output directory unless it has a resume flag and the flag was passed.

### R-M4. "Keep their fields" and a fixed four-value `status` can both not hold
- Severity: MAJOR label, **Medium**. Expert: Wiegers, Fowler. Priority: Medium.
- Evidence: WC-4 says `status` is one of `succeeded|partial|failed|blocked` and also that "commands that already write a contract keep their fields and add the missing ones" (SPEC:62). The Decisions table picks the fixed set over each command's own statuses (SPEC:262). The existing `status` vocabularies of workflow, reflect, brainstorm and adversarial are not recorded in any inventory (INV-B:272 only says a `status` field exists). UNVERIFIED whether they already match. If one differs, the two sentences contradict for that command.
- Recommendation: either record the four existing vocabularies and show they map, or say the existing `status` is kept and a new `worker_status` field carries the fixed set.

### R-M5. Phase coverage leaves ready commands without the flag or contract the brief requires
- Severity: MAJOR label, graded **Medium**. Expert: Wiegers, Cockburn. Priority: Medium.
- Evidence:
  - Section 2.3 says every brief states "the exact command line including `--unattended`" (SPEC:73). Section 3.1 gives brainstorm and init-lite "None" as their fix (SPEC:84, SPEC:87), and neither appears in any phase row (SPEC:158-162). They never gain the flag, so the template hands them an argument they do not define. Their behavior on an unknown flag is not stated.
  - SPEC:79 says the worker reports the named file "until Phase 1 adds the contract", but tdd, release-split and troubleshoot (P2, SPEC:160) are not in the P1 command list (SPEC:159) and their rows only convert gates (SPEC:89-91). AC-2.2 nevertheless requires a contract with `status: blocked` for tdd (SPEC:200). INV-B:242 shows troubleshoot writes a contract only with `--caller task-unified`.
  - AC-1.1 asserts a `## Unattended mode` section for "every command in the P1 row" and none for "a command of a later phase" (SPEC:195). The P1 row mixes 9 commands with "fixes to" 4 ready commands (SPEC:159); it is unclear whether those 4 need the section.
- Grading note: WC-2 (c) plus WC-4 can be read as requiring the contract for blocked outcomes everywhere, which would cover the P2 ready commands, so this needs a reading choice. Medium.
- Recommendation: add one column to section 3.1, "gains `--unattended` / contract in phase", with an explicit "n/a, already compatible" for brainstorm and init-lite, and state whether the 4 P1 "fixes to" commands get the section.

### R-M6. WC-10 threshold and AC-4.3 threshold differ
- Severity: MINOR-to-Medium (stated as Medium). Expert: Adzic, Whittaker (Divergence attack). Priority: Low.
- Evidence: WC-10 splits a call only when it exceeds 5 minutes, into waits of at most 4 (SPEC:68). AC-4.3 passes only if "no single tool call exceeds 240 s" (SPEC:210). A 270 s poll wait needs no split under WC-10 but fails AC-4.3.
- Recommendation: make WC-10 say "no single blocking call longer than 4 minutes" and keep AC-4.3.

### R-M11. AC-2.2 is not deterministic because WC-3 says the worker "may" ask
- Severity: Medium. Expert: Adzic. Priority: Low.
- Evidence: AC-2.2 expects `worker_done --outcome failed` and `status: blocked` on a gate-trigger run (SPEC:200). WC-3 lets the worker instead `ask` the coordinator and resume (SPEC:61). A worker that asks passes neither expectation. The brief for the check does not say to withhold answers.
- Recommendation: state in AC-2.2 that the coordinator brief for the run says "do not use `ask`", or that the coordinator never replies.

=== ARCHITECTURE ANALYSIS ===

### A-M7. AC-C1 forbids text that SA-2 and Phase 0 require
- Severity: MAJOR label, **Medium**. Expert: Fowler (lead), Newman. Priority: Medium.
- Evidence: AC-C1 greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and requires no output except `sk/ccsession-tag/` (SPEC:172). SA-2 allows one mention of Orca "as an example of a caller's question channel inside the contract file" (SPEC:147), and that contract file is `src/superclaude/core/WORKER-CONTRACT.md` (SPEC:52). Phase 0 also adds an "Orca section" to `src/superclaude/core/HOW-WE-WORK.md` (SPEC:158), which today has no Orca mention (SPEC:25). An example channel or a coordinator brief template naturally contains `orca orchestration ask`. The example SA-2 allows would fail AC-C1.
- Wrong outcome: an implementer either writes the example and fails the phase gate, or drops the example and the HOW-WE-WORK section the spec asks for. Needs the guess that wording will avoid the pattern.
- Recommendation: exempt `core/WORKER-CONTRACT.md` and the new HOW-WE-WORK section from AC-C1, or narrow the pattern to the four directories that hold commands, skills and agents.

### A-M8. Phase 0 order contradicts itself
- Severity: Medium. Expert: Fowler. Priority: Low.
- Evidence: section 1.4 says "Phase 0 therefore starts with live smoke runs" (SPEC:43). The P0 row writes the contract file, `KNOWN_CORE_FILES` entry, HOW-WE-WORK section and the test file first, "Then run three ready commands" (SPEC:158), and the "why this order" cell says the smoke runs test the decision "before anything is built on it" (SPEC:158). AC-0.4 also says a failure "reopens section 1" (SPEC:194), which would waste the files already written.
- Recommendation: either run the smoke runs first with a hand-written brief, or drop the "before anything is built" claim.

### A-M9. Section 4 says workers never commit or push; D3(b) and D4(a) allow it
- Severity: Medium. Expert: Fowler, Nygard. Priority: Medium.
- Evidence: the git row says "workers make no commits or pushes" (SPEC:133). D4(a) lets the user authorize "task commit/push", post-release and pr-submit outward actions for a worker (SPEC:244-246), and pr-submit as a worker commits and pushes fixes (SPEC:241; INV-B:94).
- Wrong outcome: an implementer enforcing the git-row sentence blocks the authorized path D4(a) describes. Needs the guess that the git row is scoped to the `/sc:git` command only.
- Recommendation: reword SPEC:133 to "no commit or push unless the brief authorizes it under WC-9".

### A-M10. Tasklist nesting is stated as safe; the inventory marks it UNVERIFIED and recommends the opposite
- Severity: Medium. Expert: Fowler, Newman. Priority: Medium.
- Evidence: the tasklist row says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (SPEC:122), citing INV-A:14. INV-B:210 says N subagents each run `/sc:reflect`, which spawns its own agents, and marks "whether nested spawning works" UNVERIFIED; INV-B:215 recommends running the per-phase reflect "at the worker's top level, not inside subagents"; INV-B:314 lists it again as UNVERIFIED. INV-A:14 supports only "up to three layers" for Claude Code in general, from a docs page. The spec's UNVERIFIED list (SPEC:272-285) omits the item.
- Recommendation: add this to the UNVERIFIED list and either adopt INV-B:215 or make a P2 acceptance check that exercises tasklist with reflect on (AC-2.3 covers the happy path only for "every required flag").

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Scope: specification correctness only, not resilience (Nygard) or test strategy (Crispin).

1. I can break this specification by **Divergence Attack**. The invariant at **WC-10 / AC-4.3 (SPEC:68, SPEC:210)** fails when **a single blocking call lasts 270 seconds**. Concrete attack: before, heartbeat age 0 s; the call blocks 270 s, which WC-10 allows (not above 5 minutes) and AC-4.3 rejects (above 240 s). After: the run is compliant with the rule and fails the acceptance check. Severity: MINOR to Medium (reported as R-M6).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **`--unattended` is passed with no output flag**. Concrete attack: the brief omits `--output`; reflect writes `.dev/reflect/<mode>-<slug>-<ts>/return-contract.yaml` (INV-B:112); the worker calls `worker_done --report-path` with a path it must guess, or with none; WC-5 then sees "no report" and sends `failed`. Medium (R-M2).
3. I can break this specification by **Sequence Attack**. The invariant at **WC-6 + WC-4 (SPEC:64, SPEC:62)** fails when **a retry worker starts with the same brief**. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: failed`; the retry reuses `<dir>`; a "fresh dir" command either overwrites attempt 1's files (corruption WC-6 forbids) or writes a subdirectory so the coordinator reads the stale `failed` contract and reports the retry as failed. Medium (R-M3).
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 `status` (SPEC:62)** fails when **an existing contract already uses a `status` value outside the four**. Concrete attack: a command keeps its field (as WC-4 says) with a value such as `completed`; the check at SPEC:183 asserts membership in the four values and fails a correct run. Existing vocabularies UNVERIFIED. Medium (R-M4).
5. I can break this specification by **Sequence Attack**. The invariant at **Phase 0 order (SPEC:43, SPEC:158)** fails when **the smoke run fails after the files are written**. Concrete attack: contract and HOW-WE-WORK edits land, then AC-0.4 fails and "reopens section 1" (SPEC:194); the written files must be reverted. Medium (A-M8).
6. I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (SPEC:69) with cleanup-audit (SPEC:85)** fails when **two workers run different `--pass N` in one worktree**. Concrete attack: both write `.claude-audit/progress.json`; the spec handles this by saying "one audit per worktree at a time", which is stated, so this attack does not break the text. Not a finding.
7. I can break this specification by **Divergence Attack** on **SA-1 vs WC-2 (SPEC:146, SPEC:60)**: a person who passes `--unattended` by hand loses all prompts. The spec declares a person never types it (SPEC:228). Inferrable; MINOR note only.

=== GUARD CONDITION BOUNDARY TABLE ===

Hard-gate rules applied: every cell below is populated, every guard the spec states is listed, and every input class is either a row or omitted with its one-line reason. Format is structured markdown for `sc:adversarial` AD-1.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit (60 s) | SPEC:59 (WC-1) | Zero/Empty | `--timeout-ms 0` | falls back to 60 s | CAPS:44 states a non-positive value falls back to the default; WC-1 relies on the default only | OK |
| readiness limit (60 s) | SPEC:59 (WC-1) | Typical | startup prompt with a 30 s fallback | true (passes) | EVIDENCE cited at SPEC:59: 34 s start passes | OK |
| readiness limit (60 s) | SPEC:59 (WC-1) | Maximum/Overflow | prompt fallback above about 45 s | false (fails) | SPEC:59 states "above about 45 s it fails again" | OK |
| unattended switch | SPEC:51, SPEC:60 (WC-2) | Zero/Empty | no `--unattended` | false | SA-1 keeps today's behavior (SPEC:146) | OK |
| unattended switch | SPEC:60 | Sentinel Value Match | `--unattended` given to a command with no `## Unattended mode` (brainstorm, init-lite) | flag unknown | not stated; see R-M5 | GAP |
| output location | SPEC:62 (WC-4) | Zero/Empty | `--unattended` with no output flag | unspecified | not stated; see R-M2 | GAP |
| output location | SPEC:62 (WC-4) | Legitimate Edge Case | contract path is nested (adversarial) or generated (workflow, research) | path differs from rule | per-row paths at SPEC:83, SPEC:92, SPEC:116 conflict with the rule; see R-M1 | GAP |
| `status` value | SPEC:62, SPEC:63 (WC-4, WC-5) | Typical | `succeeded` / `partial` / `failed` / `blocked` | each mapped | mapping stated in WC-5 | OK |
| `status` value | SPEC:63 | Legitimate Edge Case | existing vocabulary outside the four | not mapped | not stated; see R-M4 | GAP |
| `status` value | SPEC:63 | Zero/Empty | contract file exists but is empty or unparseable | unspecified | WC-5 covers only "no report exists"; SPEC:183 checks `test -s` for acceptance only | GAP (minor, see N-3) |
| outcome mapping | SPEC:63 (WC-5) | One/Minimal | audit with verdict FAIL | true | `succeeded` (audit itself succeeded) | OK |
| fresh run dir | SPEC:64 (WC-6) | Legitimate Edge Case | retry with the same output directory | unspecified | see R-M3 | GAP |
| heartbeat wait | SPEC:68 (WC-10) | Typical | call of 3 minutes | no split | heartbeat between calls | OK |
| heartbeat wait | SPEC:68, SPEC:210 | Legitimate Edge Case | call of 270 s | WC-10: no split; AC-4.3: fails | thresholds differ; see R-M6 | GAP |
| heartbeat wait | SPEC:68 | Maximum/Overflow | eval timeout 3600 s | split into at most 4-minute waits | stated | OK |
| nesting depth | SPEC:33 (R1), SPEC:66 (WC-8) | Sentinel Value Match | depth setting 1 | worker-start refused | stated; `task-create` from depth 1 UNVERIFIED but forbidden either way | OK |
| `--monitor` ordinal | SPEC:114 | One/Minimal | `--monitor 1` | refused under `--unattended` | stated | OK |
| `--monitor` ordinal | SPEC:114 | Typical | `--monitor 3` (default) | proceeds | stated through D3(b) | OK |
| confidence gate | SPEC:121 (task) | Sentinel Value Match | exactly 0.70 | not below 0.70 | not blocked; band edges at INV-B:199 and INV-B:45 | OK |
| confidence gate | SPEC:121 | Typical | 0.55 | true | resolves as blocked | OK |
| ask timeout | SPEC:61 (WC-3) | Legitimate Edge Case | timeout, then resume | resumes same ID | stated (CAPS:60) | OK |
| ask availability | SPEC:61 | Zero/Empty | no preamble held | no `ask` | gate resolves as blocked, stated | OK |
| outward-action default | SPEC:67 (WC-9) | Typical | no authorizing flag | off | stated | OK |
| outward-action default | SPEC:67 | Legitimate Edge Case | brief authorizes in prose but names no flag | unspecified | "only through the command's own explicit flag" (SPEC:67) reads as off; stated enough | OK |
| fork-PR counts | SPEC:202 (AC-2.4) | Maximum/Overflow | more than 30 reviews or comments | first page only | `gh api ... --jq length` with no pagination; see N-5 | GAP (minor) |

Omitted input classes (one-line reasons): "Maximum/Overflow" for the unattended switch and confidence gate (a boolean and a bounded score have no overflow); "Zero/Empty" for the nesting depth (the Orca code falls back to 1, CAPS:100); "Sentinel Value Match" for the readiness limit (no sentinel value is defined for it).

Table result: 6 GAP cells in the main rows. Each was graded by the FR-8/FR-9 rule: none names a concrete wrong outcome without a guess or a security, data-loss or safety-boundary risk, so each is Medium (R-M1, R-M2, R-M3, R-M4, R-M5, R-M6) and none blocks. The two GAP cells flagged "(minor)" are notes.

## Quantity flow (partition check, FR-21 style)

```text
[43 commands] --> [Inventory split: 10 ready | 27 needs-change | 6 coordinator-only]   (INV-A:73, INV-B:278)
   |-- 10 ready  --> 4 in P1 (adversarial, cleanup-audit, index-repo, workflow)
   |                 4 in P2 (reflect, release-split, tdd, troubleshoot)
   |                 2 in no phase (brainstorm, init-lite)  <-- see R-M5
   |-- 27 needs  --> P1 9 + P2 11 + P3 4 + P4 3 = 27         (SPEC:99-125, SPEC:159-162)
   |-- 6 coordinator-only --> none dispatched                  (SPEC:132-137)
```

No count mismatch. 10 + 27 + 6 = 43 holds, and every needs-change command has exactly one phase.

## Minor notes

- N-1. The ids B-1, B-2 and B-3 are used at SPEC:62, SPEC:120, SPEC:159, SPEC:194 and SPEC:195 and never defined in this document. They look like finding ids from a prior review; a reader of the spec alone cannot resolve them.
- N-2. AC-C1 and AC-C5 are written with `\|` inside the command (SPEC:172, SPEC:176). Copied raw into a shell with `grep -E`, `\|` is a literal pipe. They work only if the table is rendered first.
- N-3. WC-5 handles "no report exists" but not an empty or unparseable report file (SPEC:63). The acceptance check at SPEC:183 covers it only after the fact.
- N-4. AC-1.3 asks for a "scratch worktree" (SPEC:197). `CLAUDE.md` (not in the sandbox; UNVERIFIED) is described in the task context as requiring worktrees to be created through Orca with an agent. The check should name the safe way to run it.
- N-5. AC-2.4 counts reviews and comments with `--jq length` and no `--paginate` (SPEC:202), so more than one page of results hides an added review. Add `--paginate` or compare ids.
- N-6. `partial` maps to `succeeded` (SPEC:63, SPEC:263), which the Decisions row justifies. A coordinator that only reads the Orca outcome sees success; the body's first sentence is the only warning. Inferrable, noted for clarity.
- N-7. Section 1.1 says command changes are "limited to the worker contract" (SPEC:16), but section 3 also requires interface reconciliations, tool additions and a new `--resume` flag (SPEC:105, SPEC:108, SPEC:118, SPEC:124). SA-4 lists them (SPEC:149). Reword 1.1 to point at SA-4.

## Strengths

- The decision is argued against a named alternative with evidence per reason (SPEC:28-39), and section 1.4 states the gaps in the evidence plainly (SPEC:41-45).
- The partition, phase and citation arithmetic is consistent; every section 3 row cites lines that appear in the inventories.
- The spec marks 14 UNVERIFIED items and states which ones its rules do not depend on (SPEC:271-285).
- Standalone behavior is protected as a hard requirement (SPEC:141-151).

## UNVERIFIED citations (cannot be checked inside the sandbox)

These were not checked against a file: `CLAUDE.md:16,50,72-83,157,334,408`; `src/superclaude/cli/install_core.py:4,13-24,33`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65`; `Makefile:68-74`; `pyproject.toml:38`; `.dev/codegraph-migration/orchestration/README.md:31,33,42`; `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`; `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56`; every `cmd/*.md` and `sk/*` line cited directly (SPEC:11 says 11 were re-read by the author); the two `grep` runs at SPEC:25. Where the spec reaches these through an inventory line, the inventory line was checked and holds.

## Follow-up candidates

No issue has been opened. This run is unattended in effect (the reply is limited to a path), so the per-loop question to the session's user is not asked here; the coordinator should ask it once for the list below.

Medium (warnings):
1. R-M1: WC-4 path rule vs adversarial, workflow and research rows (SPEC:62, SPEC:83, SPEC:92, SPEC:116)
2. R-M2: `--unattended` with no output directory (SPEC:62)
3. R-M3: who makes the directory fresh (SPEC:64, SPEC:73)
4. R-M4: "keep their fields" vs the fixed `status` set (SPEC:62, SPEC:262)
5. R-M5: no phase gives brainstorm and init-lite the flag; tdd, release-split and troubleshoot contracts unscheduled (SPEC:73, SPEC:79, SPEC:158-162, SPEC:195, SPEC:200)
6. R-M6: WC-10 5-minute rule vs AC-4.3 240 s (SPEC:68, SPEC:210)
7. R-M11: AC-2.2 vs the WC-3 "may ask" (SPEC:61, SPEC:200)
8. A-M7: AC-C1 vs SA-2 and the Phase 0 Orca section (SPEC:147, SPEC:158, SPEC:172)
9. A-M8: Phase 0 order (SPEC:43, SPEC:158, SPEC:194)
10. A-M9: "workers make no commits or pushes" vs D3(b) and D4(a) (SPEC:133, SPEC:241, SPEC:244)
11. A-M10: tasklist nesting stated as safe, inventory says UNVERIFIED (SPEC:122; INV-B:210, INV-B:215, INV-B:314)

Minor: N-1 to N-7 above.

## Reviser brief

None. No blocking finding is open, so there is nothing for a reviser to repair. (Medium and minor findings never go into a Reviser brief, per `command.md` Review Loop item 2.)

verdict: PASS
