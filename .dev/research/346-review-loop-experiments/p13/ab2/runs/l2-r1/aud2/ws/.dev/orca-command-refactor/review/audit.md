review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (whole-document audit)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `746b5ffc5ac4b78a7e2053e0e341cc67756a46ac8a09ff6161b886dedded7fa2`
- baseline: missing (no `--baseline` and no `--re-review` given; this is a labelled first review of the whole document)
- mode: critique; focus: requirements, architecture; iterations: ignored (one review)
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full)
- citation shorthand: `S:N` = line N of the candidate; `CAPS:N`, `INV-A:N`, `INV-B:N` = line N of `.dev/orca-command-refactor/inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`.

## Coverage

- Read in full: command.md, README.md, the candidate (285 lines), and the three inventories (the capabilities file was read at every line the candidate cites, plus its summary table and UNVERIFIED list).
- Checked against the inventories (verified): the 10 / 27 / 6 split (A: 5 ready + 13 needs-change + 3 coordinator-only = 21 rows; B: 5 + 14 + 3 = 22 rows; S:76 matches), the 27 rows of section 3.2 and their phase assignment (P1 9 + P2 11 + P3 4 + P4 3 = 27, equal to S:159-162), the six section-4 commands, the Orca facts quoted from `CAPS:44-52,58-80,97-103,115-116,129-130,145-161`, and the command/skill line citations that the inventories relay (for example `INV-B:90` for `sc-pr-submit-protocol/SKILL.md:37-39`, `INV-A` rows for `qa.md:231-238`, `auggie-review.md:51-54`).
- UNVERIFIED (not checkable in this sandbox, only the three inventories exist): every citation to `src/superclaude/...` that the inventories do not relay, `CLAUDE.md:*`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:*`, `.dev/codegraph-migration/**`, `pyproject.toml:38`, `Makefile:68-74`, `src/superclaude/cli/install_core.py:*`, `src/superclaude/core/HOW-WE-WORK.md:*`, the E5 grep results (S:25), the "re-read 11 locations" claim (S:11) and the "340 citations re-read" claim (S:285). The `EVIDENCE.md` quotes are checkable only through `CAPS:31,49,52`.
- Not covered: the behaviour of any command (no command was run); correctness focus was not requested, so no State Variable Registry was produced; Pipeline Dimensional Analysis does not trigger (no multi-stage data flow with count divergence; the only counts are the command classification, reconciled above).

## Findings

Grading used the FIRST-REVIEW grading check for each finding. Only F-1 passes it.

### === REQUIREMENTS ANALYSIS ===

**F-1 (CRITICAL, blocking) The P0 acceptance check cannot pass as written.**
- Expert: Wiegers (testability), Adzic.
- Sentence: an implementer who follows AC-0.4 as written runs 7.2 on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` and requires "steps 1-3 and 5-7 pass" (S:194), and step 3 requires that "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (S:182). That is wrong because the same row says the contract "arrives in P1" (S:194), troubleshoot's report today is `REPORT.md` (S:91) and adversarial's contract filename is "not fixed" (S:83), so no WC-4 contract exists to match; the carve-out in AC-0.4 covers step 4 only. Two stated texts contradict each other.
- Consequence: P0 can never reach "every check passes" (S:167), and S:154 says later phases "do not start until the earlier phase's checks in section 7 pass". The gate that the spec uses to test its own decision (S:158, S:194 "a failure here reopens section 1") is unpassable for at least troubleshoot and adversarial, so it either deadlocks or is waived by judgement, defeating its purpose.
- Evidence: S:154, S:158, S:167, S:182, S:194, S:83, S:91, S:62 (WC-4 defines the contract path as `<output-dir>/return-contract.yaml`).
- Recommendation: make AC-0.4 say that step 3 uses "the command's existing report file" for the outcome comparison and the `--report-path` check, as it already does for step 4. Priority: High.

**M-1 (Medium) The WC-4 contract location is not defined for rows whose output is a file, nested, fixed or absent.**
- Expert: Wiegers.
- WC-4 puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)" (S:62). Rows then use `--output <file>` (tdd S:90, init-lite S:87, spec-panel S:120), a nested path `<output>/adversarial/return-contract.yaml` (S:83), a fixed directory with no output flag (cleanup-audit `.claude-audit/` S:85; index-repo, no flag, S:86), or the report is the final `REPORT.md` (troubleshoot S:91). AC-1.2 (S:196) and AC-2.2 (S:200: `/sc:tdd "auth" --unattended --output <file>`, then "contract `status: blocked`") need the path before dispatch (S:73) and for tdd cannot get it from the stated rule.
- Why Medium: the implementer must guess between readings (parent directory of the file, a sibling name, a new directory flag). It is a requirement the document never states, not a stated text that does harm.
- Recommendation: one sentence in WC-4 giving the rule for a file-valued `--output` and for commands with a fixed or nested directory.

**M-2 (Medium) WC-4 "keep their fields" against a fixed four-value `status` set.**
- Expert: Wiegers, Whittaker (sentinel collision).
- S:62 says commands that already write a contract keep their fields; S:262 and AC step 4 (S:183) fix `status` to `succeeded|partial|failed|blocked`. The inventories name a `status` field for workflow (`INV-B:272`) but never record its values, and give none for reflect, brainstorm or adversarial. If an existing value is outside the set, "keep" and the S:183 assertion contradict. Neither side can be checked here (UNVERIFIED).
- Recommendation: a one-line statement of how an existing differing `status` value is mapped.

**M-3 (Medium) Under-specified edges in the contract rules (from the Guard Condition Boundary Table below).**
- WC-5 does not say what happens when the report exists but is empty, unparseable, or has a `status` outside the four values (S:63); S:63 says only "no report exists" maps to failed.
- WC-3 allows a repeated `ask` after each timeout with no limit (S:61), and WC-10 sends no heartbeat while blocked in `ask` (CAPS:64 supports it), so a never-answered `ask` can hold a worker with no bound (CAPS:188 says Dispatch run time may be unbounded, UNVERIFIED).
- WC-10 says a blocking call "longer than 5 minutes" must be split to "at most 4 minutes" (S:68); a call of 4 to 5 minutes is neither required split nor within the target, and AC-4.3 (S:210) tests 240 s.
- task row (S:121): only confidence "below 0.70" is blocked; the 0.70-0.89 band (a present-alternatives prompt per `INV-A:36` for agent and `INV-B:...` for task, UNVERIFIED for task) is not addressed.
- All four are missing requirements, not stated harmful text, so Medium.

**M-4 (Medium) The tasklist and reflect unattended rules depart from the inventory without a recorded decision and rest on an overstated nesting claim.**
- Expert: Fowler, Nygard.
- S:122: under `--unattended`, tasklist Stage 10.5 "passes `--unattended` to each reflect so the headless rule applies". Reflect's headless rule auto-accepts remediation for auto-fixable registers and skips the gates (`INV-B:109`), and Stage 10.5 passes `--remediate` (`INV-B:211`). So an unattended tasklist worker would start remediation hand-offs per phase that the brief did not ask for. `INV-B:215` recommended the opposite (call reflect without `--remediate`, and run the per-phase reflect at the worker's top level). The same applies to reflect itself (S:88): `--unattended` plus `--remediate` auto-accepts a corrective-package hand-off.
- S:122 also says the reflect fan-out is "inside Claude Code's nesting limit, `INV-A:14`". `INV-A:14` only says nesting is allowed to three layers and that a command at the depth limit loses its Agent tool; `INV-B:211` marks the nested spawn UNVERIFIED, and reflect Tier 2 adds reviewers and an adversarial pass (`INV-B:110`) below that. The claim is stated as settled.
- S:268 says "nothing read in this task contradicts a verdict"; this change is not recorded in the Decisions table.
- Why Medium: whether auto-accepted remediation does harm needs a guess about what the hand-off writes; planning files only is the likely reading. Recommendation: record the decision, or follow `INV-B:215`.

**M-5 (Medium) The E3 evidence row overstates the precedent.**
- S:23 (E3) says "It has worked before" and cites `invocation_method: "skill-direct"`; S:43 (section 1.4 gap 1) says the PR #329 run used an Agent-tool subagent and proves "the nested route, not the direct route". `INV-A:13` and `INV-A:35` read `skill-direct` as a direct call. The spec states both readings in different places without reconciling them in E3. Section 1.4 does state the gap plainly, so the decision is not misrepresented; the table row should carry the caveat.

### === ARCHITECTURE ANALYSIS ===

**M-6 (Medium) AC-C1 conflicts with the P0 deliverables in `core/`.**
- Expert: Fowler.
- AC-C1 (S:172) scans `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` in every phase, including P0. P0 adds `core/WORKER-CONTRACT.md` and "an Orca section" to `core/HOW-WE-WORK.md` (S:158). SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (S:147) but AC-C1 has no exclusion for either file. If either text shows a literal command (the natural way to describe an `ask` or `check` example), P0 fails its own common check. Whether it does needs a guess, so Medium.
- Also: the pipes in AC-C1 and AC-C5 are written `\|` (S:172, S:176, S:175); copied verbatim into a shell, `\|` inside `grep -E` is a literal pipe and the check prints nothing whatever the tree contains. This is a presentation hazard (Note N-2).
- Recommendation: exclude the two named core files from AC-C1, or restrict them to a stated allowed form.

**M-7 (Medium) Decision D1 and SA-1 are consistent, but the same-session `ask` path (WC-3) re-invokes a command with a changed flag.**
- Expert: Newman, Hohpe.
- WC-3 (S:61) lets the worker session "re-invoke or resume the command with the answer as a flag". For commands with fresh-dir resume (most of section 3, "fresh dir" in the Resume column) a re-invoke after a blocked stop restarts the command and discards work. No row says which commands can take the answer without redoing work. Missing requirement; the safe default (stop, report blocked) is available, so Medium.

### Notes (minor; never fail the review)

- N-1: S:4 and S:63 refer to REQ-1 and REQ-2 (S:62, S:159) with no definition in the document; presumably prior review ids. UNVERIFIED.
- N-2: the `\|` escapes above (S:172, S:175, S:176) are markdown table escapes; state the unescaped command in a code block.
- N-3: `INV-B:311` is cited for all six coordinator-only commands (S:128) but covers only pm, spawn and swarm-wizard; agent, git and help are at `INV-A:90-92`.
- N-4: AC-0.4 refers to "the step-5 transcript" for the no-Agent-wrapper check (S:194), but step 5 only searches for `AskUserQuestion` (S:184).
- N-5: S:76 counts 43 commands from the two inventories. The host's skill listing in this session also shows `sc:graph`, `sc:impact` and `sc:issue`, which are in neither inventory, and `sc:issue` describes creating an Orca worktree. That listing is dated after the spec (2026-11-10 against 2026-11-02) and is not a file in the sandbox, so it is UNVERIFIED; if true it affects the 43 count and E5 (S:25).
- N-6: the "Decisions" table (S:255-269) and the 14 UNVERIFIED items are accurate against the inventories where checked (`CAPS:178,180,186-188`).

## Whittaker: adversarial analysis

- **Sequence attack, finding F-1.** I can break this specification by Sequence Attack. The invariant at S:154 ("later phases do not start until the earlier phase's checks pass") fails when P0 runs AC-0.4 on troubleshoot. Concrete attack: P0 done, contract file absent (before: no `return-contract.yaml`; step 3 asks for one; after: step 3 fails, P1 blocked or waived). CRITICAL.
- **Sentinel collision, M-2.** I can break this by Sentinel Collision. The invariant at S:62/S:183 (`status` in a fixed four-value set) fails when an existing contract writes another `status` word. Concrete attack: workflow writes its own `status`, WC-4 says keep it, the step-4 assertion rejects it. MAJOR, graded Medium (needs an unknown value).
- **Accumulation attack, M-3.** WC-3's repeated `ask` has no cap (S:61). MAJOR, graded Medium.
- **Divergence attack, M-4.** `--unattended` on reflect with `--remediate` branches between the existing prompt (SA-6, S:151) and the headless rule (S:88); both apply at once when a worker passes both flags. MAJOR, graded Medium.
- **Zero/empty attack, M-3.** Empty report file with `status` absent maps to nothing (S:63). MAJOR, graded Medium.

## Guard Condition Boundary Table

Guards identified: WC-5 outcome mapping, WC-10 wait threshold, WC-3 ask retry, task confidence threshold, P2 `--unattended` refusals, AC-C5 additive-edit guard. Input classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| report-exists (WC-5) | S:63 | Zero/Empty | report file present but empty | unclear | not specified | GAP (M-3) |
| report-exists (WC-5) | S:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| report-exists (WC-5) | S:63 | Sentinel Value Match | `status: partial`; or `blocked` | true | partial maps to succeeded; blocked to failed | OK |
| report-exists (WC-5) | S:63 | Legitimate Edge Case | `status` outside the four values (M-2) | unclear | not specified | GAP (M-2, M-3) |
| report-exists (WC-5) | S:63 | Maximum/Overflow | n/a: not a counted input | - | - | OK (left out: no capacity) |
| wait-split (WC-10) | S:68 | Zero/Empty | 0 s wait | false | no split needed | OK |
| wait-split (WC-10) | S:68 | Typical | 10 min wait | true | split into waits of at most 4 min | OK |
| wait-split (WC-10) | S:68 | Legitimate Edge Case | wait of 4 to 5 min | false | not split, yet target is 4 min | GAP (M-3, minor) |
| ask-retry (WC-3) | S:61 | Maximum/Overflow | N consecutive timeouts | true | resume the same message ID, no stated cap | GAP (M-3) |
| ask-retry (WC-3) | S:61 | Zero/Empty | no preamble held | false | command resolves blocked | OK |
| confidence (task) | S:121 | Typical | below 0.70 | true | blocked | OK |
| confidence (task) | S:121 | Legitimate Edge Case | 0.70 to 0.89 | false | not specified under `--unattended` | GAP (M-3) |
| confidence (task) | S:121 | Sentinel Value Match | exactly 0.70 | false | not blocked ("below 0.70") | OK |
| unattended refusals (`--monitor 1`, `--watch`, `--interactive`, socratic) | S:100,103,110,114,123 | Sentinel Value Match | flag present with `--unattended` | true | refused | OK |
| additive-edit (AC-C5) | S:176 | Zero/Empty | empty diff | true (nothing printed) | passes | OK |

FR-8/FR-9 graded by the rule: no GAP above names a concrete wrong outcome an implementer would produce on the stated text alone, so each is Medium and appears under follow-up candidates.

## follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7. Minor: N-1 to N-6. The session that ran this review asks the user once whether to open an issue for them and creates none without an answer.

## Quality scores (0-10)

Clarity 8, Completeness 7, Testability 6 (held down by F-1 and the path gaps), Consistency 7.

## Reviser brief

Blocking finding ids: F-1.
Restated rules for the reviser (bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.

verdict: FAIL
