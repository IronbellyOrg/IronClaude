review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines
- candidate sha256: `89aa60a626c2210c7e3cd02a711923cbaf3990a333b6398f744d27073b0d61ba`
- baseline: none given (first review, nothing to hash)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`. The grading check was applied to every blocking finding.
- label: whole-document audit of the final spec. Not a scoped re-review.

## What was covered

- All of the candidate (sections 1-9, Decisions, UNVERIFIED items) was read.
- The README (`README.md:1-38`) was read first.
- Inventory lines were checked directly. They are the only checkable evidence.
  - `orca-capabilities.md` (CAPS) lines 44-47, 52-53, 58-80, 97-103, 107-116, 128-130, 145-151, 155-161, 178-188.
  - `commands-a.md` (INV-A) lines 3, 14, 35, 43-45, 53-55, 60-68, 76-83, 90-98, 106.
  - `commands-b.md` (INV-B) lines 3, 31, 34, 36-37, 43-46, 52, 107-115, 207-225, 272, 285-301, 311, 320-323.
- All CAPS and INV citations in the spec that I followed matched the inventory text. I found no wrong line.
- Counts were recounted. 43 = 10 ready + 27 changed + 6 coordinator-only.
  - Sources: 21 + 22 commands. Ready: 5 + 5. Changed: 13 + 14. Coordinator-only: 3 + 3.
  - The phase membership of the 27 re-adds correctly: P1 9, P2 11, P3 4, P4 3.
- UNVERIFIED (outside the workspace, cannot be checked): every `EVIDENCE.md:N`, `.dev/codegraph-migration/...:N`, `CLAUDE.md:N`, `src/superclaude/...:N`, `HOW-WE-WORK.md:N`, `install_core.py:N`, `Makefile:N` and `pyproject.toml:38` citation. Also `cmd/*.md` and `sk/*` lines that are not quoted in an inventory. I accepted them only where an inventory line quotes them.
- Not covered: the truth of any Orca behaviour beyond what CAPS quotes. No command was run.
- Pipeline Dimensional Analysis was not triggered. The only counted flow is the 43 split above, and it conserves.
- State Variable Registry: not produced. `--focus correctness` is not active.

## Guard Condition Boundary Table

Trigger: the spec has thresholds and conditional logic. Built by Nygard, completeness-checked by Crispin, attacked by Whittaker. The table is complete, so synthesis may proceed.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` plus output dir | WC-4, spec:62 | Zero/Empty | `--unattended` with no `--output`/`--output-dir` | n/a | not stated. WC-4 defines the path only "where `<output-dir>` is the directory the coordinator passed" | GAP (M-1) |
| `--unattended` plus output dir | WC-4, spec:62 | Typical | `--output .dev/x/` | true | `.dev/x/return-contract.yaml` | OK |
| `--unattended` plus output dir | WC-4, spec:62; 3.1 adversarial, spec:83; 3.1 workflow, spec:92 | Legitimate Edge Case | adversarial and workflow | true | WC-4 says `<dir>/return-contract.yaml`. The rows say `<output>/adversarial/...` and `.dev/tasks/to-do/<id>/...` | GAP (F-3) |
| `--unattended` plus output dir | WC-4, spec:62 | Sentinel Value Match | `--output` names a file (tdd, init-lite) | true | path plus `.return-contract.yaml` | OK |
| Outcome mapping | WC-5, spec:63 | Typical | status `succeeded` / `partial` / `failed` / `blocked` | true | succeeded, succeeded, failed, failed | OK |
| Outcome mapping | WC-5, spec:63 | Zero/Empty | no report file | true | `failed` | OK |
| Outcome mapping | WC-5, spec:63 | Legitimate Edge Case | file exists but is unparseable, or its `status` is outside the four values | n/a | not stated | GAP (M-3) |
| Resume or fresh dir | WC-6, spec:64 | Typical | resume flag given | true | resume | OK |
| Resume or fresh dir | WC-6, spec:64; 2.3, spec:73 | Legitimate Edge Case | retry with the same `--output` dir on a fresh-dir command | true | WC-6 says "writes each run into a fresh output directory". 2.3 does not tell the coordinator to pass a new dir per attempt | GAP (M-2) |
| Wait size | WC-10, spec:68 | Typical | wait of 3 min | false | no split | OK |
| Wait size | WC-10, spec:68 | Maximum/Overflow | single tool call over 5 min (cli-eval 3600 s) | true | split into waits of at most 4 min | OK |
| Gate: confidence | task row, spec:121 | One/Minimal | confidence exactly 0.70 | false | proceeds. Row says "below 0.70" blocks | OK |
| Gate: confidence | task row, spec:121 | Typical | 0.69 | true | blocked | OK |
| Depth limit | R1, spec:33; D5, spec:249-253 | Maximum/Overflow | depth raised to 2 or more (D5 b) | false | rejected design by decision. WC-8 still forbids calls | OK |
| Readiness limit | WC-1, spec:59 | Maximum/Overflow | a launch prompt with a 30 s fallback | false | passes. Above about 45 s it fails | OK |
| `--monitor` level | pr-submit row, spec:114 | Sentinel Value Match | `--monitor 1` | true | refused under `--unattended` | OK |
| `--monitor` level | pr-submit row, spec:114; WC-9, spec:67 | Legitimate Edge Case | `--monitor 2` or `3` under `--unattended` | n/a | deferred to D3 and P4 (deliberate) | OK |
| Plain run | SA-1, SA-3, spec:146,148 | Zero/Empty | no `--unattended` | false | today's behaviour, no new file | OK |

Classes left out, with the reason:
- Confidence gate: Zero/Empty and Maximum cannot occur (value is bounded by the scale).
- Outcome mapping: One/Minimal and Maximum do not apply (finite enum).
- Resume or fresh dir: Zero, Maximum and Sentinel do not apply (boolean flag).
- Wait size: Zero/Empty does not apply (no wait means no split).
- Depth, readiness and `--monitor` rows: only the classes that can occur are listed.

FR-8/FR-9 grading: each GAP row is graded below by consequence.
- F-3 is blocking, because it is a contradiction between two stated texts.
- M-1, M-2 and M-3 name no stated wrong outcome. They are Medium.

Whittaker attacks on the table entries:
- Sequence attack: P0 comes before the contract exists, and the P0 gate requires "step 3" (F-2).
- Divergence attack: the `--unattended` flag is accepted in P1 while its gates are converted in P2 (F-1).
- Sentinel attack: a legitimate output file named `return-contract.yaml` colliding with the contract. Covered by M-1 (no collision rule), minor.

=== REQUIREMENTS ANALYSIS ===

### F-1. BLOCKING, MAJOR. P1 scope, the phase column and AC-1.1 contradict each other (Wiegers, Whittaker). Priority High.

- Sentence: An implementer who follows the stated text as written builds a P1 in which `--unattended` and a `## Unattended mode` section exist on commands whose gates are converted only in P2/P3/P4. That is wrong because WC-2 and WC-9 say `--unattended` never prompts and never takes an outward default. Alternatively the implementer builds only the P1 command list, and AC-1.1 then fails.
- Text A: P1 scope says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except load (B-2) (a no-op where a command has no gate)" (spec:159).
- Text B: AC-1.1 requires the section on "every command in sections 3.1-3.2 except load" (spec:195).
- Text C: the Commands column of P1 lists only nine no-gate commands plus fixes to four ready ones (spec:159).
- Text D: the Phase column assigns auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task and tasklist to P2 (spec:100-122), roadmap, save, validate-roadmap and validate-tests to P3, and implement, post-release and pr-submit to P4.
- Counted evidence: brainstorm and init-lite (3.1, "Small fix: None", spec:84,87) appear in no phase's Commands column at all. Yet 3.1 says "The only command changes are the small fixes in the last column" (spec:79) while AC-1.1 requires both to gain the section.
- Wrong outcome: auggie-review in P1 would accept `--unattended` and still post a review to GitHub and end its turn on a chat offer (`INV-A:62`, `INV-A:76`).
- Wrong outcome: AC-1.2 checks only "each P1 command", so nothing catches this.
- Recommendation: state per command which phase adds the flag and the section. A command whose gates are not yet converted must refuse `--unattended` until its phase lands. Narrow AC-1.1 to the commands of that phase.

### F-2. BLOCKING, MAJOR. The P0 acceptance check cannot pass as written (Crispin, Adzic). Priority High.

- Sentence: An implementer who follows the stated text as written runs AC-0.4 and must make 7.2 steps 1-3 and 5-7 pass. That is impossible, because step 3's pass condition needs a WC-4 contract path, and no contract exists before P1.
- Step 3 requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (spec:182).
- AC-0.4 says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1" (spec:194).
- The same text sets P0's job: closing evidence gap 1.4 (1) and testing the decision before anything is built (spec:158, spec:43).
- The phase gate says later phases do not start until the checks pass (spec:154), so P0 could never complete.
- Recommendation: in AC-0.4, restate step 3 for P0 as "exactly one `worker_done`; `--report-path` names the command's existing report file; outcome matches the report".

### F-3. BLOCKING, MAJOR. WC-4's contract location contradicts the rows for adversarial and workflow (Wiegers, Fowler). Priority High.

- Sentence: An implementer who follows WC-4 as written builds the contract at `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed. That is wrong because the adversarial row fixes `<output>/adversarial/return-contract.yaml` (spec:83), and AC-1.4 checks that path (spec:198).
- Evidence: real runs wrote under `<output>/adversarial/` (`INV-A:35`, `INV-A:60`).
- The workflow row has the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92; `INV-B:272`). `<id>` is generated by the command.
- That contradicts WC-4 ("known before dispatch") and 2.3 ("so the report path is known before dispatch", spec:73).
- 7.2 step 3 ("its report path is the WC-4 contract path") therefore fails for both commands.
- Recommendation: define the path as "the path the command's row names". Alternatively require both commands to honour `<output-dir>/return-contract.yaml`. Say how the coordinator learns a generated `<id>`.

### M-1 to M-5 and further Medium items are listed under follow-up candidates. They are not blocking.

=== ARCHITECTURE ANALYSIS ===

- Fowler: the decision "Orca coordinates, commands stay the units of work" is well argued. R1-R5 rest on CAPS lines I could check: depth 1 at `CAPS:97-101`, `worker_done` bound to the pane at `CAPS:76,150`, the identity rules at `CAPS:147-149`. No blocking architectural defect was found.
- Nygard: one shared contract file with a short per-command section is a sound boundary. The weak points are the interim states between phases (F-1) and the retry path (M-2).
- Newman and Hohpe: the report-file hand-off is a pull model. The coordinator opens the file, because Orca does not check it (`CAPS:79`). The spec states this correctly (spec:62). The status vocabulary maps cleanly to Orca's two outcomes (`CAPS:73`).
- Whittaker:
  - Accumulation attack: the tasklist row (see M-4) claims the fan-out sits inside the nesting limit without counting the layers.
  - Sequence attack: see F-2.
  - Divergence attack: see F-1.

## follow-up candidates (Medium and minor; never trigger a revision)

Medium:
- M-1. `--unattended` without an output flag has no stated behaviour (WC-4, spec:62). P1 adds output flags to some commands only. A worker briefed with `--unattended` and no output dir has no stated place for the contract. Recommendation: refuse with a visible message, or default to a timestamped dir.
- M-2. Retry with a fixed contract path. WC-6 says a command without a resume flag "writes each run into a fresh output directory" (spec:64). 2.3 (spec:73) does not tell the coordinator to pass a new output dir on `--retry-of`. The first attempt's contract can be overwritten.
- M-3. Contract present but unparseable or with an unknown `status`. WC-5 (spec:63) maps only the four values and "no report".
- M-4. Tasklist row (spec:122) differs from the inventory and from the rest of the spec. These are evidence points, not a definite wrong outcome.
  - `INV-B:215` recommends Stage 10.5 call reflect without `--remediate` and run the fan-out at the worker's top level.
  - `INV-B:210` marks nested spawning UNVERIFIED.
  - The spec instead keeps `--remediate`, passes `--unattended`, and asserts the fan-out is "inside Claude Code's nesting limit" (`INV-A:14`) without counting layers.
  - Under reflect's headless rule the remediation is auto-accepted (`INV-B:107`), so every phase would start a corrective handoff.
  - The `needs_human_decision` HALT (`INV-B:209`) has no stated resolution, though WC-2 requires every gate to be resolved.
- M-5. WC-11 versus fixed paths. WC-11 says default output paths carry a timestamp or slug (spec:75). The ready rows leave `PROJECT_INDEX.md` fixed, `.claude-audit/pass<N>-summary.md` fixed and `.dev/superclaude/context-audit.md` as the default (spec:85-87). The rows only warn the coordinator. Index-repo has "Brief must pass: none".
- M-6. AC-C1 versus SA-2 (spec:172,153). AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag`. SA-2 allows an Orca mention in the contract file. P0 also adds an Orca section to `HOW-WE-WORK.md` (core). If either text names `orca orchestration`, AC-C1 fails. The grep should exclude `core/WORKER-CONTRACT.md` or SA-2 should forbid the literal.
- M-7. AC-C5 and AC-0.3 miss deleted bullet lines. The regex `^-[^-]` does not match a removed `- item`, which diffs as `-- item`. I tested this: only `-foo` matched, while `-- old bullet`, `---` and a lone `-` did not. SA-4 additivity is therefore not enforced for bullets or blank lines.
- M-8. WC-3 lets a blocked worker `ask` and continue (spec:61), but AC-2.2 demands `--outcome failed` and `status: blocked` for a gate-hitting run (spec:200). A conforming worker that asks and succeeds fails the check. The brief template in 2.3 does not say whether to ask.
- M-9. AC-2.4 uses `gh api .../reviews --jq length`. The default page is 30 items, so a count of 30 stays 30 after a new review. This applies only to PRs with many reviews.
- M-10. `plugins/superclaude/commands/` mirror handling is open (UNVERIFIED item 8, spec:279). Each phase edits commands, and AC-C2 `make verify-sync` may not cover the mirror. AC-0.2 compares only the HOW-WE-WORK mirror.
- M-11. The command definition used for this run (`command.md:23,455-465`) already has an `## Unattended mode` section. It uses `--report-dir`, writes `<report-dir>/return-contract.yaml`, and points at `~/.claude/WORKER-CONTRACT.md`. WC-4 names `--output` / `--output-dir` only, and the spec-panel row says "add `--output`; contract" (spec:120). Check whether the spec predates that change. Citations of `cmd/spec-panel.md:22,34-35` do not match `command.md` line numbers (e.g. `command.md:36` for the target-release step). UNVERIFIED, since `command.md` is not part of the inventory evidence.

Minor notes:
- n-1. Labels `B-1` and `B-2` (spec:62,76,112,159,195,196) and "ladder rung 2" (spec:261) are used but never defined in the document.
- n-2. 3.1 intro (spec:79) says ready commands run "now" with the stated flags. For tdd the nested `/task` still asks the user when several task files match (`INV-B:219`), and the row fixes this only in P2.
- n-3. UNVERIFIED item 14 (spec:285) states a citation check result about the spec itself. I could not check it. The self-reports at spec:17 are carried the same way.
- n-4. Several E-row and R-row evidence cells cite files that exist only in the repo (`EVIDENCE.md`, `.dev/codegraph-migration/...`). I could not check these. See the coverage list.

The session that ran this review asks the user once per loop whether to open an issue for the Medium and minor items. That question cannot be asked in this sandbox. No issue was created, and the list is recorded only.

## quality assessment (informational)

Clarity 7/10, Completeness 7/10, Testability 6/10, Consistency 6/10. The decision and the evidence are strong. The three blocking items are phasing and path contradictions and are small to repair.

## Reviser brief

Blocking finding ids: F-1, F-2, F-3. No others.

Restated rule (bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Do not award yourself a PASS.

Per finding, the text each one names:
- F-1: spec:79, 159, 195 and the Phase column rows at spec:100-122.
- F-2: spec:182 and spec:194.
- F-3: spec:62, 73, 83, 92 and 198.

verdict: FAIL
