review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the whole document (not a re-review)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `2d14bcd06b4ba445afa8a700e4b20d34af0ab4a0f9ac87d402e2488534d77270` (285 lines)
- baseline: none given, not a re-review
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- panel (requirements focus lead Wiegers, Adzic, Cockburn; architecture focus lead Fowler, Newman, Hohpe, Nygard; Whittaker active in every review; Crispin validates the boundary table)

## Coverage

Read in full: the candidate, `README.md`, the command definition and the review-loop prompt file. Checked against the three inventories (`inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`):

- the 43 = 21 + 22 command count and the 10 / 27 / 6 split (verified by counting rows: 3.1 has 10, 3.2 has 27, section 4 has 6; `commands-a.md:3`, `commands-b.md:3`, `commands-b.md:289`)
- the phase assignment of all 27 section-3.2 commands (P1 9, P2 11, P3 4, P4 3; P2 adds reflect, release-split, tdd and troubleshoot from 3.1, so section 6 lists 15 for P2 and the sum is consistent)
- the `INV-A`, `INV-B` and `CAPS` line citations used in sections 1, 2, 4, 8 and 9

A `cmd/...`, `sk/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/...` or `orca-ide` guide citation cannot be checked in this sandbox (only `.dev/orca-command-refactor/` exists). Those are marked UNVERIFIED wherever a finding leans on one. Not covered: whether the source files say what the inventories say they say.

## Citation spot-check (inventory lines, verified)

| Spec claim | Checked against | Result |
|---|---|---|
| 21 + 22 commands (spec:76) | `commands-a.md:3`, `commands-b.md:3` | holds |
| 14 needs-change in B (spec:76 split) | `commands-b.md:289` | holds (3.2 has 14 B commands) |
| Depth 1, `nested_worker_depth_exceeded` (spec:33) | `orca-capabilities.md:97-99,103` | holds, spec keeps the UNVERIFIED label |
| Only `succeeded`/`failed` outcomes (spec:63, 262) | `orca-capabilities.md:73` | holds |
| Report path is metadata only (spec:62) | `orca-capabilities.md:79` | holds |
| PR #329 brief used an Agent-tool subagent (spec:43) | `orca-capabilities.md:156` | holds; `commands-a.md:35` calls the same run "proven as a direct Orca-worker skill call", the spec's reading (nested route) is the more careful one |
| Troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (spec:91 "REPORT.md") | `commands-b.md:242` | holds |
| Workflow contract is not written for pre-creation STOPs (spec:92) | `commands-b.md:272` | holds |
| `--post-pr` as an explicit flag (spec:100) | `commands-a.md:38,78` mention only `--no-post-pr`, `--remediation-offer` | not found; see M-05 |

## Guard Condition Boundary Table

Triggered: the spec contains numeric thresholds and boolean guards. Nygard builds, Crispin checks completeness, Whittaker attacks. Classes that cannot occur for a guard are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit (60 s) | WC-1, spec:59 | Typical | fallback 30 s | passes | passes at 30 s | OK |
| readiness limit (60 s) | WC-1, spec:59 | Maximum/Overflow | prompt fallback ~45 s | fails | spec says it fails again above about 45 s; the rule is "well inside" the limit with no number | OK |
| `--output`/`--output-dir` as the report location | WC-4, spec:62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite, spec:87, 90) | undefined | WC-4 defines `<output-dir>` as the directory passed; a file-valued flag has no directory | GAP (F-01) |
| `--output` as the report location | WC-4, spec:62 | Zero/Empty | flag omitted, unwritable or nonexistent directory | undefined | "written on every outcome" with no rule when the directory itself cannot be written | GAP (M-04) |
| contract path known before dispatch | WC-4, spec:62; 2.3, spec:73 | Legitimate Edge Case | workflow `.dev/tasks/to-do/<id>/` (spec:92), `<id>` unknown | false | not specified | GAP (F-01) |
| contract on every unattended outcome | WC-4, spec:62 vs load row, spec:112 | Zero/Empty | command with "Report: none" (load) | true vs false | WC-4 says written; load row says none; AC-1.1 requires the section | GAP (F-02) |
| `partial` maps to `--outcome succeeded` | WC-5, spec:63 | Sentinel Value Match | `partial` | succeeded | stated, body names `partial` | OK |
| wait split at 4 min, heartbeat at 5 min | WC-10, spec:68 | Maximum/Overflow | cli-eval 3600 s eval | wait split | split into 240 s waits | OK |
| confidence guard (task) | task row, spec:121 | Typical | < 0.70 | blocked | blocked | OK |
| confidence guard (task) | task row, spec:121 | Legitimate Edge Case | 0.70 to 0.89 ("present alternatives, ask questions", `commands-a.md:36` for the agent threshold) | undefined | spec resolves only "below 0.70"; the middle band of the same rule is not addressed | GAP (M-06; `cmd/task.md:93` UNVERIFIED) |
| nesting depth (default 1) | R1, spec:33; D5 | One/Minimal | depth 1 | refused | stated, UNVERIFIED call sites kept | OK |
| `--unattended` plus `--interactive` | WC-2, spec:60; 3.1 rows | Legitimate Edge Case | both passed (adversarial, brainstorm, release-split) | undefined | only "never `--interactive`" in the coordinator brief, nothing in the command | GAP (M-07) |
| WC-4 status enum | WC-4, spec:62 | Sentinel Value Match | a command's own status word (for example a skill's `PARTIAL`) | undefined | fixed four-value set is stated in the Decisions table (spec:262) | OK |
| `consumer_fenced` | WC-12, spec:70 | Typical | check returns it | stop, no `worker_done` | stated | OK |

Table complete: every guard enumerated, no blank behavior left unexplained.

## === REQUIREMENTS ANALYSIS ===

### F-01 (MAJOR, blocking) Wiegers, Adzic: the report location rule in WC-4 contradicts the rows that use a file-valued or fixed output

Grading sentence: an implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` for `/sc:tdd` and `/sc:init-lite`, and that is wrong because the briefs for those two pass `--output <file>` (spec:87, spec:90), so the path becomes `<file>/return-contract.yaml`, which cannot exist, and acceptance check AC-2.2 (spec:200, `/sc:tdd "auth" --unattended --output <file>`) then reads a contract that has no defined location.

Same defect, two more instances, all in stated text:
- WC-4 (spec:62) says the report is "known before dispatch" and sits in the directory the coordinator passed, and section 2.3 (spec:73) makes the coordinator state the output directory. The workflow row (spec:92) puts the contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, a path the coordinator cannot know before the package exists, and the same row asks for a contract on pre-creation STOPs, when that directory does not exist yet.
- The adversarial row (spec:83) fixes the path as `<output>/adversarial/return-contract.yaml`, while WC-4 says `<output-dir>/return-contract.yaml`. AC-1.4 (spec:198) then tests "one fixed path" without saying which. `cleanup-audit` (spec:85) has a fixed `.claude-audit/` directory, so the coordinator cannot choose a per-run directory.

Recommendation (for the reviser, narrowest fix): state in WC-4 one rule for where the contract goes when the command's output is a file or a fixed directory, and name the exception rows (tdd, init-lite, workflow, adversarial, cleanup-audit). Priority High.

### F-02 (MAJOR, blocking) Wiegers: `/sc:load` is required to have, and not to have, a contract

Grading sentence: an implementer who follows the stated text builds, for `/sc:load`, either no contract (the load row says report "none", spec:112, and Decisions says a report file "would be an unrequested addition", spec:265) or a contract (WC-4 says it is written "on every outcome" in unattended mode, spec:62; section 3 intro says every changed command gains the `## Unattended mode` section, spec:76; AC-1.1 asserts every 3.1-3.2 command has a section naming `return-contract.yaml`, spec:195), and the two cannot both hold, so AC-1.1 and AC-1.2 (spec:196, "each P1 command", which includes load by spec:159) fail against the load row as written.

Recommendation: remove load from the AC-1.1/AC-1.2 quantifier, or give load the contract; the spec's own Decisions row points to the first. Priority High.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca coordinates, commands stay units of work; sections 1.1-1.3, spec:15-39) is backed by the inventory evidence: depth 1 (`orca-capabilities.md:97-99`), `worker_done` pane binding (`orca-capabilities.md:76,150`), the standalone-use argument. The spec states its own evidence gaps (section 1.4, spec:41-45), which is the right way to hold an unproven direct route.

## Follow-up candidates (Medium and minor; not part of the Reviser brief)

Medium (warnings):
- M-01 Fowler/Nygard: tasklist row (spec:122) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit", but `commands-b.md:210,295` flags subagent to agent nesting there as UNVERIFIED and proposes removing the nested fan-out; reflect Tier 2 adds reviewers and adversarial advocates below that subagent, and the new headless auto-accept path adds a remediation handoff. The depth count is not shown. Needs a worst-case layer count or a decision. (`INV-A:14` depth limit of three layers.)
- M-02 Newman: AC-C1 (spec:172) scans `src/superclaude/core` for `orca orchestration|worktree|terminal|agent`. SA-2 (spec:147) allows an Orca mention in the contract file as an example of the question channel, and SA-5 (spec:150) adds an Orca section to `HOW-WE-WORK.md`, also under `core`. If either names `orca orchestration ask` the common check prints a line and every phase fails. State whether AC-C1 excludes the contract file and the Orca section of the routing guide. (Needs a guess about the wording used, so Medium.)
- M-03 Wiegers: the claim "Phases 1-3 need no user decision" (spec:154) conflicts with D1 (decision on the switch itself, open) and D4 (spec:244, which lists auggie-review `--post-pr` and task `commit`/`push`, both P2 rows at spec:100 and spec:121). Section 9 (spec:225) says 0-3 proceed on the recommendations; the two statements should say the same thing.
- M-04 Whittaker, zero/empty attack: attack by passing an unwritable or missing `<output-dir>`. WC-4 requires a contract on every outcome (spec:62) but gives no outcome when the contract itself cannot be written. State the fallback (for example `worker_done --outcome failed` with the reason in the body).
- M-05 Wiegers: spec:100 and WC-9 (spec:67) rely on an explicit `--post-pr` flag; the inventory shows only `--no-post-pr` and `--remediation-offer` (`commands-a.md:38,78`). If `--post-pr` does not exist, the spec adds a flag without calling it new. Line `cmd/auggie-review.md:51-54` is UNVERIFIED here.
- M-06 Crispin/Nygard: the task row (spec:121) resolves the confidence guard "below 0.70" only; the 0.70-0.89 band of the same rule (alternatives and questions; see `commands-a.md:36` for the equivalent agent rule, and `commands-b.md:199,205`, which proposes defaulting to the higher tier) is not addressed. UNVERIFIED against `cmd/task.md:93`.
- M-07 Whittaker, divergence attack: for adversarial, brainstorm and release-split, "never `--interactive`" is a brief rule (spec:83-84, 89), not a command rule. A brief that passes both `--unattended` and `--interactive` is undefined, while cleanup and improve say "refused" (spec:103, 110). Use one rule.
- M-08 Whittaker, sequence attack: AC-3.2 (spec:205) runs `/sc:roadmap --unattended --output <dir>` with an existing `.session-memory.md` and no resume flag and expects "starts fresh". That fresh run writes into the same directory and discards the earlier incomplete session; WC-6 (spec:64) says a command without resume uses a fresh directory. Resolve as blocked or as a fresh directory.
- M-09 Adzic: AC-0.4 (spec:194) reads the outcome from the first status line of `REPORT.md` whose format the spec itself calls UNVERIFIED; the check is partly unfalsifiable until a sample exists.
- M-10 Fowler: AC-2.2 (spec:200) expects `--outcome failed` and a blocked contract for every gate-trigger run, but WC-3 (spec:61) lets the worker `ask` the coordinator instead. State that AC-2.2 runs with no `ask` path, or that `ask` is reported separately.
- M-11 Wiegers: SA-3 (spec:148) writes the contract "when the caller passes the new output flag", WC-4 (spec:62) only in unattended mode. Pick one.
- M-12 Nygard: cleanup and improve (spec:103, 110) apply changes in unattended mode while the spec itself says the rollback mechanism is UNVERIFIED; WC-9 only covers outward actions. A local-change rule (or a git-clean precondition) is not stated.
- M-13 Fowler: section 4 `/sc:git` (spec:133) cites `README.md:31`, a rule for the workers of this run, as if it were repository policy ("need the user's authorization in this repo"); D4(a) (spec:245) would let a brief authorize outward actions elsewhere, so the git row and D4 are not aligned.

Minor notes:
- n-1 Spec:14 says "10 ready today, 27 needing a change" but four of the ten (reflect, release-split, tdd, troubleshoot) also get a P2 change (spec:88-91); say "ready with the stated flags".
- n-2 AC-C5 (spec:176) greps `^-[^-]` and so skips removed lines that begin with `--` (YAML front-matter fences, option lists).
- n-3 AC-C1 (spec:172) shows `\|` inside a table cell; written literally in an ERE it matches a pipe character. A code block would avoid the ambiguity.
- n-4 UNVERIFIED #14 (spec:285) and the paragraph at spec:11 are self-attestations of earlier checks; they are not evidence for this review.
- n-5 E3 (spec:23) says the earlier run "invoked" `/sc:adversarial` and cites a contract field `skill-direct`, while section 1.4 (spec:43) says the route was nested; the E3 row should say "nested".

## Reviser brief

Blocking finding ids: F-01, F-02. Rules for the reviser (restating the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M-01 to M-13, n-1 to n-5) alone; they never trigger a revision and are not part of this brief.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
