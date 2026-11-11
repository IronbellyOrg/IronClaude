review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36` (read in full). This file is ONE first-review report. The prompt calls for three independent first reviews and a coordinator MERGE; the coordinator does that merge, not this report.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none given, `baseline: missing` is not applicable (first review, `--re-review` and `--baseline` both absent).
- Reviewer model actually used: claude-sonnet-5-5
- Panel (review order): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture).
- Citation conventions: the same `INV-A`, `INV-B`, `CAPS` shorthand as the spec (`.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`). Citations to files outside `.dev/orca-command-refactor/` (`src/...`, `CLAUDE.md`, `.dev/codegraph-migration/...`, `.dev/evals/...`) cannot be checked in this workspace and are marked UNVERIFIED where a finding leans on them.

## Coverage

Read in full: the candidate (286 lines), `README.md`, the review-loop prompts file, `command.md`. Read and used for checking: `CAPS:1-188` (all cited lines in sections 1-10 spot-checked), `INV-A:1-120`, `INV-B:1-12, 57-66, 87-115, 197-215, 277-323`. Checked mechanically:

- Command counts. The candidate says 10 + 27 + 6 = 43 (`spec:76`). The section 3.1 table has 10 rows (`spec:83-92`), the 3.2 table has 27 rows (`spec:99-125`), section 4 has 6 (`spec:132-137`). INV-A:73 gives 5 ready, 13 needs-change, 3 coordinator-only; INV-B:278 gives 5, 14, 3. 5+5, 13+14 and 3+3 match. The section 6 phase lists total 9 (P1) + 15 (P2) + 4 (P3) + 3 (P4) = 31 phase-assigned commands (27 from 3.2, plus 4 ready commands in P1 and 4 in P2 with a named fix); brainstorm and init-lite have no phase (see F1). No count mismatch.
- Citation spot check: every `CAPS:N` the spec cites for a guide quote was compared with the capabilities file. All match except E2's `CAPS:161` (see M11). Every `INV-A:N` and `INV-B:N` the spec cites was compared with the inventories; all match.
- Not covered: the 11 `src/` and `.dev/codegraph-migration` locations that the spec says it re-read (`spec:11`), `CLAUDE.md` line cites, `src/superclaude/cli/install_core.py`, `Makefile`, `pyproject.toml`. All UNVERIFIED here. Testing, compliance and correctness focus areas were not requested; the Guard Condition Boundary Table below is produced because the spec contains threshold and conditional logic (`command.md:311-313`).

## === REQUIREMENTS ANALYSIS ===

### F1. CRITICAL-in-effect, blocking: AC-1.1 cannot pass for `load`, `brainstorm` and `init-lite` as the spec defines them

- Experts: Wiegers (testability), Adzic (a concrete example fails).
- Stated texts that contradict:
  - `spec:195` (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". `spec:159` (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2". `spec:196` (AC-1.2): "7.2 live check on each P1 command", whose step 4 requires `test -s <contract>` (`spec:183`).
  - `spec:112` (`load` row, section 3.2, phase P1): report "none (see note)", resume "n/a", "none: use it as a step inside another worker's brief, not as its own Task"; the decision row at `spec:265` repeats it: "a report file would be an unrequested addition. Only its usage-line defect is fixed."
  - `spec:79`: for the 3.1 commands "The only command changes are the small fixes in the last column", and `spec:84` (`brainstorm`) and `spec:87` (`init-lite`) give "None" as the small fix. Neither is assigned to a phase in `spec:158-162`.
- Grading sentence: An implementer who follows the stated text as written adds a usage-line fix to `load`, no contract and no `## Unattended mode` section to `load`, `brainstorm` or `init-lite`, and AC-1.1 (which every phase check list requires to pass, `spec:167`) fails for those three commands, because AC-1.1 demands the section and the contract name on every 3.1-3.2 command. The acceptance criterion cannot pass on the spec's own per-command rows. For `load`, the AC-1.2 live check also cannot pass: the command writes no `return-contract.yaml`, so `test -s` fails.
- Why not Medium: no guess is needed. Two quoted rules ("every command ... has a section naming `return-contract.yaml`" and "`load`: report none, no file") exclude each other for `load`, and for `brainstorm`/`init-lite` the "None" cells and the 3.1 intro exclude the section AC-1.1 requires.
- Recommendation (Wiegers): state once which of the 37 non-coordinator commands get a section, or narrow AC-1.1 to the commands that have a contract.

### F2. CRITICAL-in-effect, blocking: the `/sc:adversarial` contract path in section 3.1 contradicts the WC-4 path the coordinator will read

- Experts: Fowler (interface consistency), Whittaker (divergence attack, below), Wiegers.
- Stated texts that contradict:
  - `spec:62` (WC-4): the command writes `<output-dir>/return-contract.yaml`, "`<output-dir>` is the directory the coordinator passed", and the worker passes that path as `--report-path`. `spec:73` and `spec:182` / `spec:183` (7.2 steps 3-4): the report path is "the WC-4 contract path" and the check runs `test -s <contract>`.
  - `spec:83` (adversarial row): the brief passes `--output <dir>` and the P1 fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml`". `spec:198` (AC-1.4) accepts "adversarial names one fixed path" without saying which.
- Grading sentence: An implementer who follows the stated text as written fixes `/sc:adversarial` to write `<output>/adversarial/return-contract.yaml`; a coordinator that follows WC-4 and 7.2 reads `<output>/return-contract.yaml`, finds no file, and the live check at `spec:183` fails for adversarial, one of the three P0 smoke commands (`spec:158`, `spec:194`). Two stated paths for one file cannot both be the "WC-4 contract path". INV-A:60 confirms the on-disk drift this is meant to fix: contracts exist at two places, `.../P3-command-set/adversarial/return-contract.yaml` and a second one.
- Recommendation: pick one path; if `<output>/adversarial/` stays, say that for this command WC-4's `<output-dir>` means that subdirectory and have the brief pass it.

## === ARCHITECTURE ANALYSIS ===

The core decision (Orca on top, commands unchanged units, no Orca calls inside commands) is well supported: R1-R5 (`spec:31-37`) each cite a checked `CAPS` line (`CAPS:97-103`, `147-150`, `145`, `76`); E4 and E5 are consistent with `CAPS:155`. Section 1.4 states the evidence gaps honestly (`CAPS:156`, `CAPS:52`, `CAPS:129`, `CAPS:159-160`, `CAPS:186` all confirmed). No blocking architecture finding beyond F2. The structural issues below are Medium.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Severity here uses the panel scale; after the grading check each lands under follow-up candidates unless named blocking above.

1. I can break this specification by **Divergence Attack**. The invariant at **spec:62 (WC-4) / spec:83** fails when **one command has two stated contract paths**. Concrete attack: coordinator passes `--output /w/o`; adversarial (fixed per 3.1) writes `/w/o/adversarial/return-contract.yaml`; worker sends `worker_done --report-path /w/o/return-contract.yaml` (WC-4); `test -s` at `spec:183` fails: before, no file expected; after, the file exists at the other path. This is F2.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **spec:62, spec:73 (output directory known before dispatch)** fails when **`--unattended` is passed without an output flag**. Concrete attack: `/sc:analyze src/x.py --unattended`; WC-4 needs `<output-dir>`, nothing says where the contract goes, whether the command refuses, or whether it picks a default; the current definition of this very command refuses before any work and prints the refusal in chat only (`command.md:460`). Medium (M7).
3. I can break this specification by **Sequence Attack**. The invariant at **spec:64 (WC-6) vs spec:61 (WC-3)** fails when **a blocked command is re-invoked**. Concrete attack: tdd run 1 (`--output /w/t.md`) stops blocked, contract `status: blocked` written; worker uses `ask` (WC-3), gets the answer, re-invokes with the answer flag into the same `--output`; for commands whose resume is "fresh dir" (most rows at `spec:99-125`) the stale blocked contract and the new run share a directory the coordinator passed once. WC-6's remedy ("a fresh output directory") conflicts with the directory being fixed in the brief (`spec:73`). Medium (M2, M3).
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **spec:51, spec:229 (`--unattended` flag)** fails when **a quoted topic contains the token**. Concrete attack: `/sc:tdd "explain how --unattended works"` run by a person. The spec does not say the switch applies only to a standalone argument token outside quotes; the present spec-panel definition does (`command.md:459`). Medium (M14).
5. I can break this specification by **Accumulation Attack**. The invariant at **spec:68 (WC-10)** fails when **a single wait lies between 4 and 5 minutes**. Concrete attack: a 4.5-minute foreground wait: not "longer than 5 minutes", so not required to split, yet the rule states waits of "at most 4 minutes". Minor note (clarity only; the heartbeat cadence is still met).
6. I can break this specification by **Sequence Attack** on tasklist, `spec:122`. The invariant: "under `--unattended`, Stage 10.5 passes `--unattended` to each reflect so the headless rule applies". Concrete attack: reflect under its headless rule "auto-accepts for auto-fixable registers" (`INV-B:109`, `spec:88` row), i.e. with `--remediate` it proceeds to the remediation handoff with no person, once per phase, in N subagents; the 3.1 reflect row tells the coordinator to omit `--remediate` for exactly this reason (`spec:88`). Medium (M6).

## === TABLE: Guard Condition Boundary Table ===

Guards come from `spec:33` (nesting depth), `spec:59` (readiness), `spec:68` (wait size), `spec:62` (output dir), `spec:121` (task confidence), `spec:63` (outcome mapping). The classes "Sentinel Value Match" is left out for guards with no sentinel, and the reason is given per guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| nested depth fence | `spec:33`, `CAPS:97-103` | Zero/Empty | depth setting absent or malformed | falls back to 1 (`CAPS:100`) | refused as `nested_worker_depth_exceeded` (spec:33) | OK |
| nested depth fence | `spec:33` | Typical | depth 1 | worker may not start workers | WC-8 forbids; refused | OK |
| nested depth fence | `spec:252` (D5 b) | Maximum/Overflow | depth raised above 1 | fence passes | "break R1's protection"; no behavior for commands | GAP (Medium, user decision D5) |
| readiness limit | `spec:59` | Typical | 30 s fallback | true | passes (`EVIDENCE.md:45`, UNVERIFIED here) | OK |
| readiness limit | `spec:59` | Legitimate Edge Case | 45 s | fails | "above about 45 s it fails again" | OK |
| wait size (WC-10) | `spec:68` | Typical | 1 min | no split | OK | OK |
| wait size (WC-10) | `spec:68` | Legitimate Edge Case | 4 to 5 min | neither "longer than 5" nor "at most 4" | unspecified | GAP (minor) |
| wait size (WC-10) | `spec:68` | Maximum/Overflow | 3600 s eval | split into at most 4-minute waits | cli-eval row `spec:104` | OK |
| output dir present (WC-4) | `spec:62`, `spec:73` | Zero/Empty | `--unattended` without output flag | undefined | unspecified | GAP (Medium, M7) |
| output dir present (WC-4) | `spec:62` | Legitimate Edge Case | `--output <file>` (tdd, init-lite, spec-panel) | `<file>/...` is not a directory | unspecified | GAP (Medium, M1) |
| confidence (task) | `spec:121` | Legitimate Edge Case | exactly 0.70 | "below 0.70" false | proceeds | OK |
| confidence (task) | `spec:121` | Zero/Empty | 0.0 | true | blocked | OK |
| outcome mapping | `spec:63` | One/Minimal | status `partial` | to `succeeded` | first body sentence says `partial` | OK |
| outcome mapping | `spec:63` | Legitimate Edge Case | audit verdict FAIL | `succeeded` | OK | OK |
| outcome mapping | `spec:63` | Zero/Empty | no report file | `failed` | OK | OK |

Classes left out: "Sentinel Value Match" for depth, readiness, wait size and confidence (no sentinel value); "Maximum/Overflow" for readiness and confidence (bounded by definition); "One/Minimal" for depth, readiness, wait size, output dir (no distinct behavior). FR-10: the table is complete for the listed guards. Per the grading rule each GAP above is Medium: none names a concrete wrong outcome that follows from the stated text with no further assumption.

## Quantity Flow (Pipeline Dimensional Analysis)

Triggered because the spec describes a staged inventory-to-phase flow with counts. 43 commands in (21 + 22) -> 10 ready + 27 needs-change + 6 coordinator-only = 43 out. Phase assignment: 27 needs-change commands plus 8 ready commands with a named fix (4 in P1, 4 in P2); brainstorm and init-lite have no phase. The consumer AC-1.1 assumes every 3.1-3.2 command gets a section; that is the divergence (F1). No other mismatch.

## Follow-up candidates (Medium and minor; none triggers a revision)

- **M1 (Medium).** WC-4 (`spec:62`) puts the contract in a directory named by `--output`/`--output-dir`, but `tdd` and `init-lite` take `--output <file>` (`spec:87`, `spec:90`) and spec-panel's `--output` is file-valued (`command.md:23`, `command.md:460`; the current spec-panel definition already has `--unattended`, `--report-dir` and `<report-dir>/return-contract.yaml`, `command.md:457-465`, while `spec:120` says spec-panel needs "add `--output`"). Contract location for file-valued commands is not stated; a dedicated directory flag (as spec-panel uses) is the obvious fix. Needs a guess about which reading the implementer picks.
- **M2 (Medium).** WC-6 (`spec:64`) relies on "a fresh output directory" for most commands ("fresh dir" in about 20 rows of `spec:99-125`), but WC-4 and 2.3 (`spec:62`, `spec:73`) fix the directory in the brief and the coordinator is never told to pass a new one on `--retry-of`. Say who creates the fresh directory.
- **M3 (Medium).** WC-3 (`spec:61`) lets the worker `ask` and re-invoke instead of ending blocked, but AC-2.2 (`spec:200`) expects `worker_done --outcome failed` for every blocked run, and WC-5 (`spec:63`) maps blocked to failed. The two are not reconciled.
- **M4 (Medium).** 2.3 (`spec:73`) requires `--unattended` in every brief; 3.1 (`spec:79`) says the ten commands run as workers "now" with other flags, and the P0 smoke commands (`spec:158`, `spec:194`) have no `--unattended`; the flag does not exist until P1/P2. State that P0 briefs omit it.
- **M5 (Medium).** AC-C1 (`spec:172`) scans `src/superclaude/core` and requires no output, while SA-2 (`spec:147`) allows an Orca example in the contract file and P0 (`spec:158`) adds an Orca section to `HOW-WE-WORK.md` (a core file). An example written as a literal `orca orchestration ask` matches the pattern and fails AC-C1. Exempt the contract file and the new section, or word them to avoid the pattern.
- **M6 (Medium).** Tasklist row (`spec:122`) says the reflect fan-out runs "inside Claude Code's nesting limit, `INV-A:14`". INV-B marks nested spawning from tasklist Stage 10.5 as UNVERIFIED and asks who answers the remediation offer (`INV-B:210`, `INV-B:314`, `INV-B:322`); the spec's UNVERIFIED list (`spec:271-285`) drops both. Also `--unattended` reaching reflect's headless auto-accept (attack 6) runs remediation per phase without a person; `INV-B:215` recommended calling reflect without `--remediate`. Add both to UNVERIFIED and prefer the INV-B:215 form.
- **M7 (Medium).** `--unattended` without an output flag is undefined (attack 2, table row).
- **M8 (Medium).** WC-1 (`spec:59`) names "Launch setup, not commands" as owner but no phase in `spec:158-162` implements it and no check in section 7 tests it beyond a generic `state: ready` at `spec:180`.
- **M9 (Medium).** D4 (`spec:244`) covers auggie-review `--post-pr` and task `commit`/`push`, both P2 commands (`spec:100`, `spec:121`), yet `spec:225` says "Phases 0-3 can proceed on the recommendations; Phase 4 waits for D2-D4". Also `pr-submit` is counted in the 27 (`spec:114`) while D3(a), the recommendation, leaves it unchanged (`spec:139`, `spec:240`).
- **M10 (Medium).** Workflow's P1 fix "write the contract for pre-creation STOPs too" (`spec:92`) has no known directory (`.dev/tasks/to-do/<id>/`, `<id>` not yet created) and the 3.1 brief passes no output flag, against "known before dispatch" in WC-4 (`spec:62`).
- **M11 (minor).** E2 (`spec:22`) cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`"; `CAPS:161` is the pr-submit top-level line. The pr-submit rule is cited as `sk/sc-pr-submit-protocol/SKILL.md:37-39` (`spec:65`, `INV-B:90`) while `CAPS:161` cites the installed copy at `:47-49`; both UNVERIFIED here (different copies, possibly different line numbers).
- **M12 (Medium).** `cleanup` and `improve` (`spec:103`, `spec:110`) apply edits unattended and say the "rollback" mechanism is UNVERIFIED (`INV-A:118`). The report lists changed files, but there is no stated way to revert; the data-loss exposure rests on the "not Approval Required" list in files not available here.
- **M13 (Medium).** WC-4 says commands with an existing contract "keep their fields and add the missing ones" with a fixed `status` set (`spec:62`, `spec:262`). Whether existing `status` fields (workflow `refs/return-contract.md:3-19`, brainstorm, reflect) use other values is UNVERIFIED here; a clash is unaddressed.
- **M14 (Medium).** The `--unattended` token rule (standalone, unquoted) is stated in the current spec-panel definition (`command.md:459`) but not in WC-2 or the contract (`spec:51`, `spec:60`).
- Minor notes: AC-C5 (`spec:176`) rejects every `-` line, but adding flags to a command's existing Usage line is such a line; SA-4 (`spec:149`) lists the allowed exceptions without Usage lines. `CLAUDE.md` line cites (`spec:34`, `spec:52`, `spec:150`, `spec:164`, `spec:192`) and `install_core.py` / `Makefile` / `pyproject.toml` cites are UNVERIFIED in this workspace. The spec's own self-check note at `spec:285` ("about 340 citations ... 9 defects ... all fixed") is not independently checkable here.

Issue opening for the follow-up candidates: the session that ran this review asks the user once per loop; this report only lists them (no `--unattended` run, no issue created).

## Brief clauses overridden

None. The brief (README plus the run line) narrows nothing and widens nothing past this scope.

## Reviser brief

Blocking finding ids: F1, F2. Reviser rules (restated from the Review Loop, bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the file byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. The reviser does not award itself a PASS.

- F1: texts `spec:195` (AC-1.1), `spec:159` (P1 scope), `spec:196` (AC-1.2), `spec:112` (load row), `spec:265` (load decision), `spec:79` with `spec:84` and `spec:87` (brainstorm, init-lite "None"). Wrong outcome: AC-1.1 cannot pass for load, brainstorm and init-lite as the rows define them; AC-1.2 cannot pass for load.
- F2: texts `spec:62` (WC-4), `spec:73`, `spec:183` (7.2 step 4), `spec:83` (adversarial row), `spec:198` (AC-1.4). Wrong outcome: the contract is built at `<output>/adversarial/return-contract.yaml` and the coordinator checks `<output>/return-contract.yaml`, so the live check fails for adversarial.

verdict: FAIL
