review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (review 1 of 3)

## Header

- mode: critique (`/sc:spec-panel --mode critique --focus requirements,architecture`), plus the per-criterion pass test the brief adds.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (computed in this run; equals the hash in `review/lint-1.md:1`).
- baseline: missing. None was given, so this is a first review of the full document. No prior report, so no re-review table.
- reviewer model: claude-haiku-5-5 (single reviewer, single context).
- lint: `review/lint-1.md` (review-lint/1), checks REF, 0 findings (`review/lint-1.md:3-5`). No lint id to address.
- evidence block: not applicable (first review).
- citation keys, all repo-relative under `.dev/orca-command-refactor/`: `S` = `specs/orca-worker-contract-spec.md` (the candidate, bare `S:N`); `INV-A` = `inventory/commands-a.md`; `INV-B` = `inventory/commands-b.md`; `CAPS` = `inventory/orca-capabilities.md`. Citations to `src/superclaude/`, `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/`, `EVIDENCE.md`, `pyproject.toml`, `Makefile` or install code are not in the sandbox and are marked UNVERIFIED. No blocking finding rests on an UNVERIFIED citation.
- files read in full: the candidate (`S:1-286`), `README.md`, `INV-A`, `INV-B`, `CAPS`, `lint-1.md`, the command definition, and the FIRST-REVIEW prompt in `document_review_loop_prompts.md` (under the sandbox home).

### Process deviations (read before using this report)

1. The FIRST-REVIEW prompt asks for two independent first reviews and then a MERGE. This worker is one reviewer in one context and cannot brief a second one. No MERGE was done. This report is therefore not a merged report. The coordinator must brief a second first reviewer, merge the two reports under the MERGE rule, and treat the merged list as authoritative. The blocking list below may change after the merge.
2. The VERIFY prompt needs a verifier in a fresh context that sees only the candidate and the finding list. It was not run. Each blocking finding was checked by reading the cited lines in this run. Per the VERIFY rule, a missing `confirmed:` line confirms every finding, so the coordinator must run VERIFY before any revision.
3. Because of deviation 1, the verdict below is provisional for the coordinator. It is `FAIL` on this reviewer's findings, and any single confirmed blocking finding keeps it `FAIL`.

## Summary

- 14 blocking findings (B1-B14), 21 Medium findings (M1-M21, follow-up candidates), and 4 minor notes. Every blocking finding is about a requirement or acceptance check that cannot be met as written, or two stated texts that disagree. None is about a wording preference.
- The acceptance-criteria and live-check pass test (section A) covers 32 rows. 10 cannot pass as written for every command and phase they cover, and 13 can pass only under a stated condition. The spec's Phase 0 gate (AC-0.4) cannot pass at all as written.
- The spec's core decision (Orca on top, commands as units of work, section 1) is not challenged here. The defects are in the contract mechanics that make the decision testable.

## Section A: acceptance criteria and live-check steps, one by one

Pass test: "can it pass as written for every command and phase it covers". Yes, Conditional, or No. Finding IDs point to section C.

| ID | Covers | Can pass as written | Reason (citation) | Finding |
|---|---|---|---|---|
| AC-C1 | every phase | No | Pattern covers four words only, is case-sensitive, and is escaped as `\|` in the raw text (`S:172`). The SA-2 allowance for the contract file makes it fail a permitted text (`S:147`, `S:158`). | B11, M1 |
| AC-C2 | every phase | Conditional | Needs `make sync-dev` run in each phase; no phase step says so (`S:150`, `S:158-162`). Makefile target UNVERIFIED. | M2 |
| AC-C3 | every phase | Yes | Baseline is captured before each phase (`S:174`). | none |
| AC-C4 | every phase | Yes | Checks staged files only (`S:175`). | none |
| AC-C5 | every edited command | Conditional | Compares `master...HEAD`, so uncommitted edits are invisible and the check passes vacuously (`S:176`). | M3 |
| AC-0.1 | P0 | Yes | Import check; `install_core.py` UNVERIFIED. | none |
| AC-0.2 | P0 | Conditional | `cmp` covers one of the two mirrors; the level-table copy depends on a test that is UNVERIFIED (`S:192`). | MN5 |
| AC-0.3 | P0 | Yes | Diff of removed lines (`S:193`). | none |
| AC-0.4 | P0 | No | Step 3 expects WC-4 contract paths that P0 does not have; step 4 parses REPORT.md as YAML; step 5 cannot see subagent wrapping; the brief uses `--unattended`, which P0 lacks (`S:73`, `S:79`, `S:159`, `S:182-184`, `S:194`). | B3, B4, B5 |
| AC-1.1 | P1 | No | Requires the section in every command of 3.1-3.2 at P1, but P2-P4 commands get it later (`S:159`, `S:195`); `load` cannot name a contract (`S:112`). | B8 |
| AC-1.2 | P1 | No | 7.2 on each P1 command: `load` is not a Task (`S:265`), and `workflow` has no `--output` (`S:92`, `S:196`). | B6, B8 |
| AC-1.3 | P1 | Conditional | Requires a "scratch worktree" (conflicts with the Orca-only worktree rule, see M4) and the commands are not named; adversarial and workflow write a contract today (`INV-A:35`, `INV-B:272`). | M4 |
| AC-1.4 | P1 | Yes | Grep for a name and a sentence; the content check is weak. | M16 (note) |
| AC-2.1 | P2 | Conditional | Text assertions only; passes with no behaviour (`S:199`). | M16 |
| AC-2.2 | P2 | No | Expects `blocked` for every P2 gate-trigger, but WC-2 allows a documented default, and research, cleanup and improve resolve without blocking (`S:60`, `S:103`, `S:110`, `S:116`, `S:200`). | B7 |
| AC-2.3 | P2 | Conditional | Uses 7.2, so inherits B1-B5 and B12. | B1, B2, B12 |
| AC-2.4 | P2 | Yes | `gh api` counts before and after (`S:202`); named repo, as the fork rule requires. | none |
| AC-2.5 | P2 | Yes | Manual check. | none |
| AC-3.1 | P3 | Yes | Once the names are reconciled. | none |
| AC-3.2 | P3 | Conditional | Requires `--output` on roadmap; no row adds it (`S:118`, `S:205`). Whether roadmap already has one is UNVERIFIED. | M7 |
| AC-3.3 | P3 | Conditional | Depends on the P3 default-target and report fixes; does not require 7.2 (`S:206`). | M17 |
| AC-3.4 | P3 | Conditional | Weak when the single-owner files do not exist before the run (`S:207`). | M16 |
| AC-4.1 | P4 | Conditional | Depends on D2 (`S:232-236`, `S:208`). | none |
| AC-4.2 | P4 | No | Says "no install, VM"; checks only `git log -1` and the PR list (`S:209`). | B10 |
| AC-4.3 | P4 | No (not mechanically) | "Heartbeats at most 5 minutes apart" is not measured by any named tool (`S:210`). | M18 |
| 7.2 step 1 | live | Conditional | Outside an Orca terminal the commands are refused: no `--from` or `--terminal` (`S:167`, `S:180`, `CAPS:149`). | B12 |
| 7.2 step 2 | live | No | Cadence conflicts with step 3's 15-minute wait; the pass holds on an absent field (`S:181-182`, `CAPS:129`). | B1 |
| 7.2 step 3 | live | No | No branch for `question` or `escalation`; the report path cannot match in P0 (`S:182`). | B2, B3 |
| 7.2 step 4 | live | Conditional | Passes a contract missing WC-4 fields; cannot parse a Markdown report (`S:183`, `S:62`). | M10, B3 |
| 7.2 step 5 | live | Conditional | Can detect AskUserQuestion; cannot detect subagent wrapping, which AC-0.4 claims (`S:184`, `S:194`). | B5 |
| 7.2 step 6 | live | No in a shared worktree | Fails on any unrelated change in the shared worktree, and the phase's own uncommitted edits (`S:185`, `CAPS:115`). | M3 |
| 7.2 step 7 | live | Yes | `worker-release`, then `worker-list` reclaimable check (`S:186`, `CAPS:111-113`). | none |

Count over the 32 rows: No = 10 (AC-C1, AC-0.4, AC-1.1, AC-1.2, AC-2.2, AC-4.2, AC-4.3, step 2, step 3, step 6); Conditional = 13; Yes = 9. Several Conditional rows also carry a blocking finding through 7.2.

## Section B: the mandatory guard, flow and expert artifacts

### B.1 Guard Condition Boundary Table

The trigger matches (the spec has WC-2, WC-5, WC-6 and check guards), so the table is produced even though `--focus correctness` is not active. It is partial: it covers the guards in WC-2 to WC-6, WC-11 and section 7. The 27 per-command gate rows of section 3.2 are checked only through AC-2.2 (B7), not row by row. FR-10 is therefore not satisfied for those rows, and the second reviewer must complete them before synthesis.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome | `S:63` | Zero/Empty | no report file | true | `failed` | OK |
| WC-5 outcome | `S:63` | Zero/Empty | 0-byte or unparseable contract present | false | "succeeded otherwise" | GAP (B13) |
| WC-5 outcome | `S:63` | Sentinel | `status: partial` | false | `succeeded` (decision `S:263`) | OK |
| WC-5 outcome | `S:63` | Legitimate Edge | audit verdict FAIL, status succeeded | false | `succeeded` (`S:63`) | OK |
| WC-4 write | `S:62` | Zero/Empty | pre-creation STOP, no output dir (workflow) | n/a | path undefined | GAP (B6) |
| WC-2 gate | `S:60` | Typical | cleanup approval item, no `--interactive` | true | list unapplied, not blocked (`S:103`) | GAP vs AC-2.2 (B7) |
| 7.2 step 2 | `S:181` | Zero/Empty | `agentWait` absent (never looked) | pass | pass | GAP (B1) |
| 7.2 step 3 | `S:182` | Legitimate Edge | `question` event before `worker_done` | not done, keep waiting | none specified | GAP (B2) |
| 7.2 step 4 | `S:183` | Zero/Empty | contract with status and command, no `artifacts` or `report_path` | pass | pass | GAP (M10) |
| 7.2 step 4 | `S:183` | Typical | troubleshoot `REPORT.md` (Markdown) | parse fails | fail | GAP (B3) |
| AC-C1 | `S:172` | Sentinel | `orca status --json` in a command | no match | pass | GAP (M1) |
| AC-C1 | `S:172` | Typical | `orca orchestration ask` in the contract file | match | fail, though `S:147` permits it | GAP (B11) |
| AC-C5 | `S:176` | Zero/Empty | uncommitted edits | empty diff | pass | GAP (M3) |
| 7.2 step 6 | `S:185` | Legitimate Edge | unrelated change in shared worktree | non-empty status | fail | GAP (M3) |
| WC-6 | `S:64` | Legitimate Edge | init-lite retry on the same output file | overwrite | neither resume nor fresh dir | GAP (M12) |
| AC-1.3 | `S:197` | Typical | adversarial or workflow plain run | contract written | fail, though SA-3 `S:148` says "same as today" | GAP (M4) |
| WC-11 | `S:69` | Typical | two index-repo runs, default path | same file written | forbidden | GAP (B14) |

Blank or "unspecified" Specified Behavior cells (FR-9): none blank. The cells that say "path undefined" or "none specified" are counted as unspecified, so they are GAP rows above.

### B.2 Pipeline Dimensional Analysis and Quantity Flow Diagram

Not triggered. The spec describes a coordinator-worker process and a contract. It contains no multi-stage data flow whose count changes between stages.

### B.3 State Variable Registry

Not required. `--focus correctness` is not active.

### B.4 Whittaker adversarial probing

Whittaker is active in every panel review, so these probes are included.

- **A1 (FR-2.1 zero/empty). "I can break this specification by Zero/Empty Attack."** The invariant at `S:63` (WC-5) fails when the report file is present but empty or truncated. Concrete attack: a worker dies after writing a 0-byte `return-contract.yaml` for a failed run. WC-5 sends `failed` only when the report says `failed` or `blocked`, or when no report exists, so it sends `succeeded`. Maps to B13. Severity MAJOR (blocking, as a concrete wrong outcome).
- **A2 (FR-2.4 sequence). "I can break this specification by Sequence Attack."** The invariant at `S:62-63` (WC-4 contract written, WC-5 `worker_done` sent once) has no ordering. Concrete attack: the worker sends `worker_done --report-path <contract>` before writing the contract. Step 4 then reads a missing file. Maps to M11. Severity MAJOR (specification ambiguous under attack).
- **A3 (FR-2.2 divergence). "I can break this specification by Divergence Attack."** The invariant at `S:116` (`--unattended` pins `--strategy planning`) fails when the brief also passes `--strategy intent`. Concrete attack: the brief passes both flags. The spec does not say which one wins. Maps to M21. Severity MAJOR (ambiguous under attack).
- **A4 (FR-2.3 sentinel). "I can break this specification by Sentinel Collision Attack."** The invariant at `S:52` (the contract `status` field, one of four values) fails when a command writes a contract with `blocked_question` set but `status: succeeded`. WC-2 and WC-5 do not say which field governs. Maps to M10. Severity MINOR (behaviour inferrable from WC-5).

## Section C: findings

Grade rule applied (FIRST-REVIEW): blocking needs a sentence that holds with no further assumption, or a contradiction, or an outward or safety-boundary risk. Otherwise Medium.

### Requirements analysis

=== REQUIREMENTS ANALYSIS ===

**B1. [BLOCKING, High] Live-check steps 2 and 3 cannot both hold, and step 2 passes with no observation.**
- Experts: Wiegers (testability), Nygard (stall detection).
- Cites: `S:181`, `S:182`; `CAPS:63` (the `check --wait ... --timeout-ms 900000` example); `CAPS:129` (absent vs null `agentWait`).
- Text: step 2 says `worker-show` "at least once per 5 minutes"; step 3 runs `check --wait --timeout-ms 900000` "until worker_done arrives".
- Wrong outcome: "An implementer who runs step 2 and then step 3 as ordered makes one `worker-show` call and then waits 15 minutes, so the 5-minute cadence is missed." The step-2 pass ("`agentWait` is never non-null") also holds when the field is absent, and `CAPS:129` says an absent field "means it never looked", so a run with zero observations passes.
- Recommendation: run step 3 as waits of at most 4 minutes with a `worker-show` between them (WC-10). Require at least one observation per 5-minute interval, with `agentWait` explicitly `null`.
- Quality impact: a stalled worker can go unseen for 15 minutes, and the check can pass with no observation at all.

**B2. [BLOCKING, High] Step 3 has no branch for a worker `question` or `escalation`.**
- Experts: Whittaker (sequence), Hohpe (messaging).
- Cites: `S:61` (WC-3: a worker may ask the coordinator); `S:182` (types include `question`, loop "until worker_done arrives"); `CAPS:62` (`reply --id`); `CAPS:63`.
- Wrong outcome: "An implementer who follows step 3 as written, receives a `question`, and loops again never sends `reply`, so the worker stays parked in `ask` and no `worker_done` arrives."
- Recommendation: add branches: on `question`, read it and `reply --id <msg> --body`; on `escalation`, stop the check and report. Then restate the pass condition.
- Quality impact: any run that uses the WC-3 path cannot pass the live check.

**B3. [BLOCKING, High] AC-0.4 cannot pass for the three P0 commands.**
- Experts: Fowler (interface), Hohpe (integration).
- Cites: `S:182` (step 3 path must be "the WC-4 contract path"); `S:183` (step 4 parses YAML with `status` and `command`); `S:194` (AC-0.4 says step 4 "uses the command's existing report file"); `S:62` (WC-4 path `<output-dir>/return-contract.yaml`); `INV-B:242` (troubleshoot writes `REPORT.md`); `INV-B:272` (workflow writes `.dev/tasks/to-do/<id>/return-contract.yaml`); `INV-A:35`, `INV-A:60` (adversarial writes under `<output>/adversarial/`).
- Wrong outcome: "An implementer who runs AC-0.4 on `/sc:troubleshoot` gets `REPORT.md`, which is neither the WC-4 path nor YAML, so step 3 and step 4 fail; the same holds for the workflow and adversarial paths." The contract arrives in P1 (`S:194`), so the P0 gate cannot pass.
- Recommendation: in P0 check each command against its existing report (troubleshoot: `report_path` in `REPORT.md`; workflow: its contract; adversarial: its contract). Or move the contract checks to P1 and keep P0 to steps 1, 2 (fixed), 3 (outcome only), 5, 6 and 7.
- Quality impact: the P0 gate, which section 1.4 says must run first, never passes.

**B4. [BLOCKING, High] P0 briefs must carry `--unattended`, which the spec adds only in P1.**
- Experts: Cockburn (actor and brief), Hightower (operations).
- Cites: `S:73` (2.3: each brief carries "the exact command line including `--unattended`"); `S:79` (3.1: ready commands run "if the brief uses the stated flags", and no stated flag is `--unattended`); `S:159` (P1 adds the flag "accepted by every command"); `S:180` (step 1 uses the 2.3 brief); `S:194` (AC-0.4 runs the commands "as real Orca workers").
- Wrong outcome: "An implementer who builds the P0 brief from 2.3 passes `--unattended` to `/sc:troubleshoot`, which has no such flag in P0, so the smoke run tests an undefined argument path, not the ready-today path the gate is meant to test."
- Recommendation: state in 2.3 that P0 briefs omit `--unattended`, and that the flag is required from P1.

**B5. [BLOCKING, High] AC-0.4 claims the direct-run condition is checked in step 5, but step 5 checks only AskUserQuestion.**
- Experts: Whittaker (sequence), Crispin (test design).
- Cites: `S:184` (step 5 pass: "no AskUserQuestion call"); `S:194` ("no Agent-tool wrapper, verified in the step-5 transcript"); `S:43` (gap 1: no direct-route end-to-end run exists).
- Wrong outcome: "A P0 run in which the worker wraps the command in an Agent-tool subagent passes step 5 and AC-0.4." The direct route, which section 1.4 names as the main unproven point, is therefore never tested.
- Recommendation: step 5 must also check that the command is the top-level tool call, with no Agent or Task call before it.

**B6. [BLOCKING, High] The WC-4 fixed-path rule conflicts with the per-command rows, and pre-creation output has no location.**
- Experts: Fowler (interface design), Newman (contract evolution).
- Cites: `S:62` (WC-4: `<output-dir>/return-contract.yaml`, "known before dispatch", includes "stops before any other output exists"); `S:83` (adversarial: `<output>/adversarial/return-contract.yaml`); `S:92` (workflow: pre-creation STOP contract, no output flag); `S:198` (AC-1.4 requires workflow to "state the contract is written for pre-creation STOPs"); `INV-B:272` (workflow writes no contract for pre-creation STOPs today); `INV-B:52`.
- Wrong outcome: "An implementer who follows WC-4 for workflow has no `--output` directory to write into, and the pre-creation contract's path depends on an id that does not exist before creation, so the coordinator cannot know the path before dispatch, which WC-4 requires."
- Recommendation: give workflow an `--output-dir` that holds pre-creation contracts. Either make the adversarial path `<output-dir>/return-contract.yaml`, or amend WC-4 to allow a command subdirectory and say so in the row.

**B7. [BLOCKING, High] AC-2.2 requires a `blocked` outcome for every P2 gate, but WC-2 allows a documented default.**
- Experts: Wiegers (acceptance criteria).
- Cites: `S:200` (AC-2.2: "contract `status: blocked` with a non-empty `blocked_question`"); `S:60` (WC-2 (a) default, (b) flag, (c) blocked); `S:116` (research pins `--strategy planning`, no block); `S:103` (cleanup lists approval items, no block); `S:110` (improve, same).
- Wrong outcome: "An implementer runs AC-2.2 on `/sc:research --unattended`. The planning strategy is pinned (`S:116`), no blocked outcome occurs, and the AC requires one, so a correct implementation fails."
- Recommendation: AC-2.2 should state the expected resolution per row (default, flag or blocked), taken from section 3, and test that one.

**B8. [BLOCKING, High] AC-1.1 and AC-1.2 cannot pass at P1, and `load` cannot produce a contract.**
- Experts: Cockburn (scope by phase), Crispin (test coverage).
- Cites: `S:195` (AC-1.1: every command in 3.1-3.2 has the section); `S:159` (P1 scope lists 13 commands); `S:160-161` (P2-P3 scope); `S:112` (load: report "none", phase "P1 (usage line only)"); `S:265` (load is used inside a brief, not as a Task; no report file); `S:76-77` (every changed command gains the section); `S:196` (7.2 on each P1 command).
- Wrong outcome: "An implementer who finishes P1 as listed cannot pass AC-1.1, because auggie-review (P2, `S:160`) has no section. An implementer who adds the section to `load` writes a contract the spec says the command never writes (`S:112`)."
- Recommendation: scope AC-1.1 to the P1 list. Exclude `load` from the contract requirement and the 7.2 check, and say it is a brief step.

**B9. [BLOCKING, High, outward action] P1 accepts `--unattended` on commands whose outward default is still on.**
- Experts: Nygard (failure modes), Fowler (boundaries). Safety-boundary grade.
- Cites: `S:159` (P1: the flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"); `S:100` (the auggie-review `--unattended` implication is in P2); `INV-A:38` (auggie-review posts to GitHub by default, "No confirmation prompt"); `S:67` (WC-9: outward defaults are off under `--unattended`); `S:114` (pr-submit pushes and replies by default; its fix is in P4).
- Wrong outcome: "An operator who follows the P1 brief runs `/sc:auggie-review <PR> --unattended`. The flag is a no-op at P1, the command posts review comments to GitHub, and WC-9 forbids that under `--unattended`."
- Recommendation: at P1, do not accept `--unattended` on commands with outward defaults (auggie-review, pr-submit, task, post-release, cli-eval). Or move WC-9's default-off into P1 for those commands.

**B10. [BLOCKING, High, outward action] AC-4.2 claims to check for no install or VM, and checks only commit and PR.**
- Experts: Hightower (operations), Nygard (side effects).
- Cites: `S:209` (AC-4.2: "no install, VM, commit or PR"; checks `git log -1` and `gh pr list`); `S:67` (WC-9: installs and provisions are off by default); `S:113` (post-release fix: installs and VM "off unless the brief authorizes them"); `INV-B:33` (post-release runs real installs and VMs).
- Wrong outcome: "An implementer whose post-release provisions a VM or runs a real-target install without authorization passes AC-4.2, because the check looks only at `git log` and the PR list."
- Recommendation: add a check for each outward step: the contract lists it as `skipped`, and a process or venv audit shows none ran. Or narrow the AC's claim to commit and PR.

**B13. [BLOCKING, High] WC-5 maps a present but unparseable or empty contract to `succeeded`.**
- Experts: Whittaker (zero/empty attack).
- Cites: `S:63` (WC-5: `--outcome failed` only when "the report says failed or blocked, or no report exists"; otherwise `succeeded`); `CAPS:73` (outcome mandatory); `S:183` (step 4 parses the file, but WC-5 does not use step 4's result).
- Wrong outcome: "An implementer who follows WC-5 for a worker that writes a 0-byte contract after a failed run sends `--outcome succeeded`, because the file exists and is not `failed` or `blocked`." The coordinator reads `succeeded`.
- Recommendation: "`failed` when the report is absent, empty, unparseable or has a status outside the four values; `succeeded` only for `succeeded` or `partial`."

**B14. [BLOCKING, High] WC-11 forbids a shared default file, but three ready-today or P1 rows keep one.**
- Experts: Newman (shared state), Hohpe (parallel workers).
- Cites: `S:69` (WC-11: "must never write the same file"; default paths carry a timestamp or the coordinator's slug); `S:85` (cleanup-audit: fixed output dir, "one audit per worktree at a time (WC-11)"); `S:86` (index-repo: `PROJECT_INDEX.md`, brief passes none); `S:87` (init-lite: default `.dev/superclaude/context-audit.md`); `CAPS:115` (workers share the current worktree by default).
- Wrong outcome: "Two index-repo workers dispatched with the brief in `S:86` (no flags) in one worktree both write `PROJECT_INDEX.md`, which WC-11 forbids." The "one audit at a time" note in `S:85` is not in WC-11 and is not in the 2.3 coordinator duties.
- Recommendation: 2.3 requires a per-task slug in `--output` for each fixed-path command. Or the coordinator serializes them, and the rule is written into 2.3.

**M1. [Medium] AC-C1 coverage, case and escape.** Experts: Whittaker (sentinel).
- `S:172` covers only `orchestration`, `worktree`, `terminal`, `agent` after `orca`/`orca-ide`. `orca status`, `orca open`, `orca skills`, `orca send` pass, though SA-2 (`S:147`) forbids every orca command. The pattern has no `-i`, so `ORCA` (the spec's own placeholder, `S:167`) evades it. In the raw text the pipe is written `\|` (`S:172`); in ERE that matches a literal `|`, so copied raw the pattern matches nothing. Rendering in a table cell hides this.
- Recommendation: match `\borca(-ide)?\b` with `-i`, use `|` unescaped in the regex, and exclude only the documented contract mention.

**M2. [Medium] AC-C2 depends on a sync step no phase names.** `S:173`; `S:150` (SA-5 says `.claude/` comes from `make sync-dev`); `S:158-162` (phase scopes do not mention it). Makefile target UNVERIFIED.
- Recommendation: add `make sync-dev` to each phase's scope, before AC-C2.

**M3. [Medium] Checks depend on worktree state that the spec does not define.** `S:176` (AC-C5 uses `master...HEAD`, so uncommitted edits pass vacuously); `S:185` (step 6: only the output dir may change, but the shared worktree holds the phase's edits and any unrelated change, `CAPS:115`).
- Recommendation: define a baseline (`git status --short` before dispatch, compared after) and state whether the phase commits before its checks.

**M4. [Medium] AC-1.3 names a "scratch worktree" and does not name the commands; SA-3 is ambiguous about contracts.** `S:197`; `S:148` (SA-3: a standalone run writes "the same files it writes today"); `INV-A:35` (adversarial "MUST be written on every run"); `INV-B:272` (workflow writes a contract on post-creation outcomes). Creating a scratch worktree by hand conflicts with the project's Orca-only worktree rule (CLAUDE.md, not in the sandbox, UNVERIFIED here).
- Recommendation: name the two commands (analyze and design have no contract today), and create the check's worktree through Orca or use a temporary checkout inside the listed exceptions.

**M5. [Medium] WC-10 does not cover Agent-tool fan-out, which blocks for longer than a heartbeat.** `S:68` (splitting applies to "a command step that blocks a single tool call"); `INV-B:46` (tasklist: 2N validators, reflect fan-out); `INV-B:241`; `CAPS:130` (cadence from the preamble); `CAPS:162` (no upper bound found, UNVERIFIED). Whether a missed heartbeat matters is UNVERIFIED (`CAPS:130`).
- Recommendation: state what the worker does during an Agent call (for example, no split is possible, so accept the gap and rely on `worker-show`), or forbid such calls in unattended mode.

**M6. [Medium] Several requirements have no acceptance check.** WC-1 (`S:59`, owner "Launch setup", no phase); WC-3 (`S:61`); WC-6 (`S:64`); WC-12 (`S:70`); WC-10 except AC-4.3 (`S:68`); WC-9 for `task` commit and push (`S:121` vs `S:67`).
- Recommendation: add an AC or a 7.2 step for each, or say which phase owns WC-1.

**M7. [Medium] The output flag that WC-4 needs is not named for many rows.** `S:62` (`<output-dir>` is "the directory the coordinator passed"); rows with "add a report path" and no flag name: `S:103` (cleanup), `S:110` (improve), `S:123` (test); rows with no output flag at all: `S:104` (cli-eval), `S:115` (recommend), `S:116` (research), `S:117` (review-translation), `S:118` (roadmap), `S:119` (save), `S:121` (task), `S:122` (tasklist), `S:124` (validate-roadmap). AC-3.2 (`S:205`) requires `--output` for roadmap, which no row adds; whether it exists is UNVERIFIED (`cmd/roadmap.md` is not in the sandbox).
- Recommendation: a column with the exact flag name per row. Add the flag to rows that lack one.

**M8. [Medium, architecture] The WC-3 handoff from a blocked command to `ask` has no mechanism.** `S:60` (c): the command writes `blocked` and stops; `S:61`: "when a gate would resolve as blocked ... the session may ... ask". Nothing tells the worker session that the command reached a gate: the contract has no stop signal, and the brief template (`S:73`) does not tell the worker to read `~/.claude/WORKER-CONTRACT.md`. Who reads the contract file is not stated.
- Recommendation: name the worker-session step that reads the contract after the command ends, and say which field signals a gate.

**M9. [Medium] Evidence overreach in section 1.** (a) E2 (`S:22`) says a command run by a worker "has the same tools as a command a person runs". `CAPS:161` only says the worker is top-level, not that its tool set matches. (b) E3 (`S:23`) says Orca workers "invoked /sc:adversarial" and cites `invocation_method: "skill-direct"`, while 1.4 gap 1 (`S:43`) says only the nested route is proven. `INV-A:13,35` call the direct route "proven", so the inventories and the spec disagree.
- Recommendation: restate E2 as "a worker is a top-level session (CAPS:161)" and E3 as nested-route evidence only, unless the direct run is cited.

**M10. [Medium] Step 4 does not check the WC-4 required fields.** `S:62` (contract "carries at least" `status`, `command`, `report_path`, `artifacts`, `blocked_question` when blocked); `S:183` checks only `status` and `command`. A contract without `artifacts` passes, and the coordinator cannot find what was written.
- Recommendation: step 4 asserts all WC-4 fields, and `blocked_question` non-empty when `status: blocked`.

**M11. [Medium] WC-4 and WC-5 do not order the contract write before `worker_done`.** `S:62`; `S:63`. An implementer may send `worker_done` before writing the contract, and step 4 then finds no file (attack A2).
- Recommendation: state "write the contract, then send `worker_done`".

**M12. [Medium] WC-6 is not met by init-lite, and "fresh dir" is a brief rule, not a command rule.** `S:64` (WC-6: resume, or a fresh output directory, owner "Command"); `S:87` (init-lite re-run overwrites its report, which is neither). `S:73` (2.3) has no retry rule for passing a new `--output` on `--retry-of`.
- Recommendation: 2.3 requires a new output directory on every `--retry-of`; init-lite either gets a fresh path or is marked as overwriting in WC-6.

**M13. [Medium, architecture] pr-submit is classified needs-change, but D3's recommendation makes it coordinator-only.** `S:114` (3.2 row, needs-change); `S:240` (D3 (a) "Coordinator or person only (recommended)"); section 4 (`S:126-137`) does not include it.
- Recommendation: move pr-submit to section 4 if D3 (a) is accepted, or state in 3.2 that its row is conditional on D3.

**M14. [Medium, architecture] The reflect headless trigger changes.** `S:88` (P2: under `--unattended`, `--remediate` "follow[s] the existing headless auto-accept rule"); `S:151` (SA-6: the headless rule keeps working "exactly as today"); `S:280` (UNVERIFIED 9: an Orca worker is assumed not headless). `INV-B:109` (the rule keys on `claude --print`). So `--unattended` becomes a new trigger for auto-accept, and the auto-accept can run corrective work with no person.
- Recommendation: state whether auto-accept is wanted under `--unattended`, and record the trigger change against SA-6.

**M15. [Medium, architecture] SA-2 and the ccsession-tag exclusion.** `S:147` (no command, skill or agent runs an orca command); `S:25` (E5: `sk/ccsession-tag/` is the only Orca-aware primitive); `S:172` (AC-C1 excludes `skills/ccsession-tag/`). The spec does not say whether ccsession-tag runs an orca command, so a baseline SA-2 violation could be hidden by the exclusion.
- Recommendation: state what ccsession-tag does with Orca, and whether SA-2 applies to it.

**M16. [Medium] Weak checks: AC-2.1, AC-3.4 and AC-1.4.** AC-2.1 (`S:199`) asserts section text, not behaviour. AC-3.4 (`S:207`) compares hashes "where present"; when the single-owner files are absent before the run, the check cannot detect a clobber. AC-1.4 (`S:198`) greps for a sentence.
- Recommendation: add a behaviour check (for AC-2.1, the 7.2 run in AC-2.2 covers it); for AC-3.4 create the single-owner files before the run.

**M17. [Medium] Phase pass rule and the live check.** `S:167` (a phase passes when "every check in its block and every common check" passes); `S:178` (7.2 is "used by P0-P4"); `S:205-207` (AC-3.2 to AC-3.4 do not reference 7.2). It is not clear whether 7.2 is required for P3.
- Recommendation: list 7.2 explicitly in each phase block that needs it.

**M18. [Medium] AC-4.3 cannot measure heartbeat spacing.** `S:210` ("heartbeats arrive at most 5 minutes apart"). No named tool reports heartbeat times; `CAPS:130` says the cadence comes from the preamble.
- Recommendation: name where the timestamps come from (for example `worker-show` observations), or drop the claim.

**M21. [Medium] Precedence between unattended defaults and explicit flags is undefined.** `S:116` (research pins planning), `S:113` (post-release needs pre-authorization), `S:100` (auggie-review `--post-pr`). No rule says whether a brief flag overrides an unattended default. Attack A3.
- Recommendation: state "an explicit flag in the brief overrides the unattended default, and the contract records which one applied", or forbid the conflict.

### Architecture analysis

=== ARCHITECTURE ANALYSIS ===

**B11. [BLOCKING, High] AC-C1 fails the contract text that SA-2 permits.** Experts: Fowler (boundaries), Whittaker (contradiction probe).
- Cites: `S:147` (SA-2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"); `S:172` (AC-C1 greps `src/superclaude/core` and excludes only `ccsession-tag`); `S:158` (P0 writes `src/superclaude/core/WORKER-CONTRACT.md`); `S:52` (the contract file is a core file).
- Wrong outcome: "An implementer who writes SA-2's permitted example, `orca orchestration ask`, into WORKER-CONTRACT.md fails AC-C1, which runs in every phase, so the implementer must choose between the two texts."
- Recommendation: exclude `src/superclaude/core/WORKER-CONTRACT.md` from AC-C1, or forbid the example and restate SA-2 to match.

**B12. [BLOCKING, High] The 7.2 commands omit the identity that the spec's own ORCA definition requires outside an Orca terminal.** Experts: Hohpe (messaging), Hightower (operations).
- Cites: `S:167` (ORCA means `orca-ide` outside an Orca terminal); `S:180`, `S:182` (no `--from` or `--terminal` in any `ORCA` command); `CAPS:149` (outside an Orca terminal the caller must pass `--from`/`--terminal`; without identity lifecycle commands are refused with `no_active_sender_terminal`); `CAPS:148`.
- Wrong outcome: "An implementer who runs step 1 from outside an Orca terminal, which `S:167` allows, gets `no_active_sender_terminal`, so step 1 cannot pass."
- Recommendation: each `ORCA` command in 7.2 takes `--from <handle>` (or `--terminal`) from the coordinator's preamble, or the check requires an Orca terminal.

**M19. [Medium, architecture] The contract is a worker-session duty but is described as a command duty.** `S:50` (worker run: "Only such a session may send lifecycle messages"); `S:62` (WC-4 owner: Command); `S:63-65` (WC-5, WC-7 owner: worker session). Commands write the file; the worker session sends `worker_done` and must read the contract. The spec does not say which layer holds the final `worker_done`.
- Recommendation: a table with one owner per WC row, and one sentence in 2.3 on who reads the contract.

**M20. [Medium, architecture] The contract file is installed globally but its reader is not named.** `S:52` (installed to `~/.claude/WORKER-CONTRACT.md`); `S:52` says each command "points to the installed contract path". `INV-*` and the CLAUDE.md install rule (UNVERIFIED here) do not say that a worker session reads installed core files. This is the same gap as M8, stated at install level.
- Recommendation: state how the worker learns the contract path (the brief template in 2.3 is the natural place).

### Minor notes

- MN1: `S:14` cites `CAPS:155` as `nested-worker-depth.js:7-11,18-22`; `CAPS:155` cites 18-19 and `CAPS:40` cites 18-22. Use the same range everywhere.
- MN2: `S:11` and `S:285` (item 14) describe independent citation checks run on 2026-11-02. Neither check's output is in the sandbox, so both are UNVERIFIED.
- MN3: `S:121` (task) says "contract on every tier (today only on TFEP)". The row does not name the contract path for the non-TFEP tiers, so a worker has no path to report (`INV-B:202`).
- MN4: `S:100` names `--post-pr`, which `INV-A:38` does not show. The flag is proposed, not existing. Mark it as new.
- MN5: `S:192` (AC-0.2) runs `cmp` on one of the two HOW-WE-WORK mirrors. The level-table copy in `src/superclaude/core/CLAUDE.md` is checked only by a test that is UNVERIFIED here.

## Follow-up candidates (Medium and minor; not blocking, not in the Reviser brief)

- Medium: M1-M21 as listed in section C. The coordinator asks the user once whether to open an issue for these. None is created without that answer.
- Minor: MN1-MN5.

## Coverage statement

- Read in full: the candidate (all 286 lines), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `review/lint-1.md`, `README.md`.
- Inventory citations: the `CAPS:`, `INV-A:` and `INV-B:` citations used in this report were each matched to the cited line in this run. The one mismatch found in spot checks of the spec's own citations is MN1. The spec's other inventory citations were spot-checked, not exhaustively re-matched.
- UNVERIFIED: every `src/superclaude/`, `CLAUDE.md`, `.dev/evals/`, `.dev/codegraph-migration/`, `EVIDENCE.md`, `pyproject.toml` and `Makefile` citation. These are not in the sandbox, so none is used as the basis for a blocking finding.
- Not done: the second first review and the MERGE (deviation 1); the VERIFY pass in a fresh context (deviation 2); the row-by-row guard enumeration for section 3.2 (section B.1).

## Reviser brief

Blocking finding IDs: B1, B2, B3, B4, B5, B6, B7, B8, B9, B10, B11, B12, B13, B14.

Restated rule (review loop bullet 6): revise only the text that a blocking finding names. Add no rule, mechanism or section that a blocking finding does not call for. Each added paragraph or table cites its finding ID. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding ID. Leave Medium and minor findings alone.

verdict: FAIL
