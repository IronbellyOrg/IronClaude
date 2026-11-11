review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 58733 bytes)
- candidate sha256: `ad7680cf8b39696f9eede626f872afc9b90b8426c6886d766a44d4d26c306157`
- baseline: not applicable (first review; neither `--re-review` nor `--baseline` given)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- invocation: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`; not `--unattended`, so the coordinator asks the user about follow-up candidates.
- Citation convention: `S:N` = line N of the candidate; `INV-A/INV-B/CAPS` = lines of the three files under `.dev/orca-command-refactor/inventory/`. Any citation to a file outside the workspace (`src/`, `CLAUDE.md`, `EVIDENCE.md`, `HOW-WE-WORK.md`, `pyproject.toml`) is UNVERIFIED here.

## Coverage (what was and was not checked)

Covered: all 285 lines of the candidate; `README.md` (binding context); the three inventories read in the parts the spec cites (INV-A:76-120, INV-B:3,31,65,105,112,285-323, CAPS lines 10-188 spot-checked). Panel order applied: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower; only the requirements and architecture buckets are reported, per `--focus`.

Not covered or UNVERIFIED: every `src/superclaude/...` line citation (the only per-command source evidence is the two inventories), `CLAUDE.md:N`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:N`, `.dev/codegraph-migration/...`, `src/superclaude/core/HOW-WE-WORK.md:171,249,254`, `src/superclaude/cli/install_core.py`, `pyproject.toml:38`, and the spec's own claims about its grep runs (`S:25`) and its "11 locations re-read" (`S:11`). One discrepancy needs a source check: the spec cites the pr-submit top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`S:65`, `S:11`), while the installed copy quoted at `CAPS:161` has it at lines 47-49. Possibly different file versions; UNVERIFIED which is current.

Checks that came out clean (verified against the inventories):
- The 43-command count: INV-A:3 lists 21 commands and INV-B:3 lists 22; the 22 names at INV-B:3 count to 22.
- The 10 / 27 / 6 split: recomputed from the spec's own rows (`S:81-92` = 10; `S:97-125` = 27; `S:132-137` = 6) and phase assignment of the 27 rows (P1 9, P2 11, P3 4, P4 3 = 27). The six coordinator-only commands match INV-A:90-92 and INV-B:285-287.
- The Orca facts used in the rationale (depth 1, 60 s readiness, `worker_done` bound to the pane, `--outcome` mandatory, report path as pointer only, heartbeat from the preamble) match `CAPS:44,73,76,79,97-99,130,150`.

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] The P0 acceptance check cannot pass as written
Grading sentence: an implementer who follows the stated text as written builds the P0 live check so that step 3 requires "its report path is the WC-4 contract path" and "its `--outcome` matches the contract's `status`" (`S:182`), and AC-0.4 requires "steps 1-3 and 5-7 pass" (`S:194`) for `/sc:troubleshoot` and `/sc:adversarial`. X is wrong because the same spec says these two commands have no WC-4 contract at P0: troubleshoot reports `REPORT.md` and gets its contract only in P2 (`S:91`, `S:160`), adversarial's contract filename is not fixed until P1 (`S:83`, `S:159`, and INV-A "adversarial, return-contract location" note: two different locations in the earlier run), and `S:79` says the worker reports "the named file until Phase 1 adds the contract". Step 3 therefore fails for two of the three mandated smoke runs, and `S:154` ("Later phases do not start until the earlier phase's checks in section 7 pass") then blocks P1. AC-0.4 carves out only step 4 ("step 4 uses the command's existing report file"), not step 3.
- Experts: Wiegers (testability), Adzic (the check as an executable example), Crispin.
- Recommendation: narrow AC-0.4 to say that for P0 step 3 accepts the command's existing report file as `--report-path` and the outcome follows the report's own status (delete the contract clause for P0 rather than add a mechanism).
- Priority: High. Quality impact: the evidence-gap closure the spec depends on (`S:43`, `S:272`) cannot be recorded as passed.

### M-1 [Medium] Ready-today commands with no phase never get `--unattended`, and WC-4 or Section 2.3 expects them to
`S:73` says every brief includes `--unattended`; `S:155` and `S:159-160` give the flag only to commands "listed in this row"; `S:81-92` lists `brainstorm` and `init-lite` with "None" and no phase in the P1/P2 lists, and `S:62` names `init-lite` as a command whose contract goes to `<output-file>.return-contract.yaml`. `S:79` says the contract is added "in Phase 1" for the ready commands, but the P1 list (`S:159`) contains only fixes for adversarial, cleanup-audit, index-repo and workflow, and tdd, troubleshoot, release-split and reflect are P2 (`S:160`). So no phase delivers a contract for init-lite, and brainstorm is told to receive a flag no phase adds. This needs the guess that the implementer reads "ready" as "no change at all" versus "change at a later phase". The text does no harm that holds without a guess, so it is Medium.
- Experts: Wiegers (traceability), Cockburn.
- Recommendation: add one clause saying how a command with no phase row is briefed (no `--unattended`, report is the file named in 3.1), or give init-lite a phase.

### M-2 [Medium] Contract path is unknowable before dispatch for ready commands with a fixed or implied output location
WC-4 requires the path to be recorded before dispatch (`S:62`, `S:73`) and defaults to `<output-dir>/return-contract.yaml`. cleanup-audit has a fixed `.claude-audit/` directory (`S:85`, INV-A table row cleanup-audit), index-repo's location is "implied" (`S:86`, INV-A index-repo row: "location (repo root) implied, UNVERIFIED"), and neither row names a contract path or an output flag. Also the 3.2 rows say "add a report path" or "add an output path" for about 15 commands without naming the flag (`S:99-125`; SA-3 refers to "the new output flag", `S:148`), while `S:62` says `--output` / `--output-dir`, and `--output` is a file for some commands. An implementer must choose the flag name per command; the P1 test (`S:195`) only greps for `return-contract.yaml`, so differing choices pass. Medium: it is a requirement the spec never states, not a stated text that does harm.
- Recommendation: one sentence in WC-4 fixing the flag name for commands that lack one, and naming the contract path for cleanup-audit and index-repo.

### M-3 [Medium] Stale contract after a resume or retry reads as the current outcome
WC-6 lets a retry resume from on-disk state in the same output directory (`S:64`; resume flags at `S:83-84,109,114`). WC-4 says the contract is written on every outcome, and WC-5 maps "no report exists" to `failed` (`S:63`). Attack (sequence/accumulation): attempt 1 writes `status: failed`; attempt 2 resumes in the same directory and is killed before it writes; the coordinator opens the old contract and cannot tell it is attempt 1's. The spec does not say a command removes or overwrites the contract at start. Medium: a missing requirement.
- Recommendation: one clause in WC-4 that the contract is replaced or marked at start of the run.

### M-4 [Medium] `status: blocked` with an empty or missing `blocked_question`; malformed or out-of-set `status`
WC-4 says `blocked_question` is carried "when blocked" (`S:62`) but nothing requires it non-empty; AC-2.2 does (`S:200`). WC-5 defines the outcome for "no report", `failed`, `blocked`, otherwise `succeeded` (`S:63`), so an unparseable contract or a `status` outside the four values falls into "otherwise" and maps to `--outcome succeeded`. This needs a guess about what the worker does with a malformed file. Medium.

### M-5 [Medium] Several WC requirements have no acceptance check
Section 7 has no check for WC-1 (launch path, `S:59`), WC-3 (the `ask` path, `S:61`), WC-12 (`check` before `worker_done`, `S:70`), or WC-11 beyond P3's `save` (`S:207`); the P2 gate-trigger runs (`S:200`) test the blocked path, not the `ask` path. Section 7 states "A phase passes only when every check in its block passes" (`S:167`), so these requirements can be unmet with every phase passing. Missing coverage, not a stated text that does harm: Medium.

### M-6 [Medium] Fixed default output paths versus the parallel-safety rule
WC-11 says two workers in one worktree must never write the same file and default paths carry a timestamp or slug (`S:69`). The spec's own rows keep fixed paths: cleanup-audit "one audit per worktree at a time" (`S:85`), index-repo `PROJECT_INDEX.md` (`S:86`), init-lite's default file (`S:87`), research's `claudedocs/research_*.md` (`S:116`). Only cleanup-audit says how the coordinator avoids the clash; the others rely on the brief passing a path the command may not accept. Medium: a guess about which text wins.

## === ARCHITECTURE ANALYSIS ===

### M-7 [Medium] "Phases 1-3 need no user decision" versus D4
`S:154` and `S:225` say Phases 0-3 need no user decision; D4 is stated to affect auggie-review `--post-pr` and task `commit`/`push` (`S:244`), both P2 rows (`S:100`, `S:121`), whose rows already encode D4's recommended answer ("returns only with an explicit `--post-pr` in the brief"). Two readings are allowed (proceed on the recommendation, or wait): Medium.

### M-8 [Medium] SA-4 / AC-C5 additivity versus adding flags to command Usage lines
SA-4 calls Phase 1-3 edits "additive: a new `## Unattended mode` section and new flags" (`S:149`) and AC-C5 requires no removed line for any command edit without a named defect fix (`S:176`, `git diff -U0 ... | grep -E '^-[^-]'`). A new flag shown on a command's Usage line replaces that line, so the check prints it. The check passes if the implementer documents the flags only inside the new section; the spec does not say that. The named-fix exemptions (`S:149`) cover roadmap, validate-roadmap, validate-tests, adversarial, workflow, explain, business-panel and load only. Medium: one reading passes, one fails.

### M-9 [Medium] AC-C1 versus the P0 deliverables that mention Orca
AC-C1 greps `src/superclaude/core` (and commands/skills/agents) for `orca[-ide] (orchestration|worktree|terminal|agent)` and requires no output (`S:172`), excluding only `skills/ccsession-tag/`. SA-2 permits an Orca mention in the contract file (`S:147`), and P0 adds an Orca section to `HOW-WE-WORK.md` and a "coordinator brief template" to `WORKER-CONTRACT.md` (`S:158`), both in `core/`. If either spells an `orca orchestration ...` command (the natural content of a coordinator section), AC-C1 fails on the spec's own deliverable. Needs the guess that those texts avoid the pattern. Medium.

### N-1 [Medium] D1 and D5 decide architecture the phases already assume
Phase text is "written for the recommended flag" (`S:51`), so D1 option (b) invalidates S:158-160 and 7.2; it is flagged as open but the spec does not say what changes. Note only.

## Guard Condition Boundary Table

Guards found: heartbeat/wait cadence, readiness limit, nesting depth, outcome mapping, blocked status, `--monitor 1` refusal. One row per class that can occur; omitted classes are given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | S:68 | Maximum/Overflow | single wait of exactly 5 min, 4 min, 4 min 1 s | split required above 4 min | "at most 4 minutes"; heartbeat "every 5 minutes" | OK |
| WC-10 wait split | S:68 | Zero/Empty | wait of 0 | not triggered | not stated, cannot cause harm (no wait) | OK (omitted class reasoned: harmless) |
| WC-1 readiness | S:59 | Maximum/Overflow | fallback 45 s vs limit 60 s | pass at 30 s, fail above ~45 s | "well inside" the limit, evidence 30 s / 45 s | OK |
| WC-5 outcome | S:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| WC-5 outcome | S:63 | Sentinel Value Match | `status` outside the four values, or unparseable file | falls to "otherwise" | `--outcome succeeded` by default reading | GAP (M-4) |
| WC-4 blocked | S:62, S:200 | Zero/Empty | `status: blocked` with `blocked_question: ""` | true | AC-2.2 wants non-empty; WC-4 silent | GAP (M-4) |
| WC-4/WC-6 stale file | S:62, S:64 | Legitimate Edge Case | old contract in a reused output dir, new run killed early | contract exists | not specified | GAP (M-3) |
| Nesting depth | S:33, S:66 | Maximum/Overflow | worker issues `worker-start` at depth 1 | refused | `nested_worker_depth_exceeded`; call sites presumed (UNVERIFIED at CAPS:103) | OK (UNVERIFIED enforcement) |
| `--monitor 1` refusal | S:114 | Sentinel Value Match | `--monitor 1` and `--unattended` together | true | refused | OK |
| Task confidence | S:121 | Maximum/Overflow | confidence exactly 0.70 | boundary | "below 0.70 resolves as blocked"; 0.70 is not blocked, matches INV-A's 0.70-0.89 band | OK |

Omitted classes: "One/Minimal" for every guard (a value of one is not distinct from typical for these guards).

The FR-8 and FR-9 GAP rows above are all Medium: none names a wrong outcome that follows from stated text without a guess. Pipeline Dimensional Analysis not triggered (no data pipeline); count conservation was checked by hand: 43 = 10 + 27 + 6, phases cover all 27 and 8 of the 10 (brainstorm and init-lite have no phase, M-1).

## Follow-up candidates (Medium and minor; none triggers a revision)

- M-1 to M-9 as above; N-1.
- Minor: the pr-submit source line mismatch between `S:65` (37-39) and `CAPS:161` (47-49) should be re-checked against the checkout (UNVERIFIED).
- Minor: `/sc:load` sits in the 27 "needing a change" but is advised as a brief step, not a Task (`S:112`, `S:139`); P1 gives it "usage line only" while AC-1.1 asserts each P1 command has an `## Unattended mode` section (`S:195`), so load is ambiguous there.
- Minor: Section 14 of UNVERIFIED items (`S:285`) reports self-run citation checks; not independently reproducible here.
- The session that runs this review (the coordinator) should ask the user once whether to open an issue for these follow-up candidates; this audit creates none.

## Quality scores (0-10)

Clarity 8, Completeness 7, Testability 6 (F-1, M-5), Consistency 7.

## Reviser brief

Blocking finding ids: F-1.
Rules (restated for the reviser, who reads this report and not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. No brief clause was overridden in this review.

verdict: FAIL
